import {
  Injectable,
  NotFoundException,
  ForbiddenException,
  GoneException,
  PayloadTooLargeException,
} from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { v4 as uuidv4 } from 'uuid';
import * as bcrypt from 'bcrypt';
import * as fs from 'fs';
import * as path from 'path';
import { SharedFile } from './shared-file.entity';
import { User } from '../auth/user.entity';

// Extensions interdites selon la politique de sécurité (US01 — contrôles de saisie)
const FORBIDDEN_EXTENSIONS = ['.exe', '.bat', '.cmd', '.sh', '.ps1', '.msi', '.com'];

// Taille maximale en octets — 1 073 741 824 octets = 1 Go (US01)
const MAX_FILE_SIZE = Number(process.env.MAX_FILE_SIZE ?? 1073741824);

// Durée d'expiration par défaut : 168h = 7 jours (US01 et US10)
const DEFAULT_EXPIRY_HOURS = Number(process.env.SHARE_LINK_EXPIRY_HOURS ?? 168);

// Dossier racine de stockage des fichiers sur le disque
const UPLOAD_DIR = process.env.UPLOAD_DIR ?? 'uploads';

/**
 * Service de gestion des fichiers — contient toute la logique métier de DataShare.
 * Gère l'upload, le téléchargement, la suppression et la purge des fichiers expirés.
 */
@Injectable()
export class FilesService {
  constructor(
    @InjectRepository(SharedFile) private fileRepo: Repository<SharedFile>,
  ) {}

  /**
   * Retourne le chemin du dossier de stockage pour un utilisateur donné.
   * Crée le dossier s'il n'existe pas (recursive: true évite l'erreur si déjà existant).
   * Structure : uploads/<userId>/ pour les connectés, uploads/anonymous/ pour les anonymes.
   */
  private getUploadDir(userId: number | null): string {
    const dir = userId
      ? path.join(UPLOAD_DIR, String(userId))
      : path.join(UPLOAD_DIR, 'anonymous');
    fs.mkdirSync(dir, { recursive: true });
    return dir;
  }

  /**
   * Gère l'upload d'un fichier (US01 connecté, US07 anonyme).
   *
   * Flux :
   * 1. Vérification de la taille côté serveur (double-vérif après le client)
   * 2. Vérification de l'extension
   * 3. Déplacement du fichier temporaire vers sa destination définitive
   * 4. Hash du mot de passe si fourni
   * 5. Insertion en base avec le token de partage généré
   *
   * @param file   Fichier uploadé par Multer (temporairement dans /tmp)
   * @param user   Utilisateur connecté, ou null si upload anonyme
   */
  async upload(
    file: Express.Multer.File,
    user: User | null,
    password?: string,
    expiryHours?: number,
  ) {
    // Vérification côté serveur — ne jamais faire confiance uniquement au client
    if (file.size > MAX_FILE_SIZE) {
      throw new PayloadTooLargeException('Le fichier dépasse la taille maximale autorisée (1 Go).');
    }

    const ext = path.extname(file.originalname).toLowerCase();
    if (FORBIDDEN_EXTENSIONS.includes(ext)) {
      // On supprime le fichier temporaire avant de rejeter — pas de fuite de fichiers
      fs.unlinkSync(file.path);
      throw new ForbiddenException(`Les fichiers ${ext} ne sont pas autorisés.`);
    }

    const hours = expiryHours ?? DEFAULT_EXPIRY_HOURS;
    // Date.now() retourne des millisecondes — on convertit les heures en ms
    const expiresAt = new Date(Date.now() + hours * 3600 * 1000);

    // UUID v4 comme token de partage — non prédictible (US02)
    const shareToken = uuidv4();

    // Déplacement du fichier temporaire vers sa destination finale
    // copyFileSync + unlinkSync car renameSync échoue entre volumes Docker différents
    const destDir = this.getUploadDir(user?.id ?? null);
    const destPath = path.join(destDir, `${uuidv4()}_${file.originalname}`);
    fs.copyFileSync(file.path, destPath);
    fs.unlinkSync(file.path);

    // Hash bcrypt du mot de passe — chaîne vide si pas de protection (US09)
    const passwordHash = password ? await bcrypt.hash(password, 12) : '';

    const sharedFile = this.fileRepo.create({
      owner: user ?? null,
      ownerId: user?.id ?? null,
      originalName: file.originalname,
      filePath: destPath,
      size: file.size,
      // Fallback MIME si le navigateur n'envoie pas de Content-Type
      contentType: file.mimetype || 'application/octet-stream',
      shareToken,
      expiresAt,
      passwordHash,
    });

    await this.fileRepo.save(sharedFile);
    return this.toResponse(sharedFile);
  }

  /**
   * Retourne l'historique des fichiers d'un utilisateur connecté (US05).
   * Filtre strictement par ownerId — un utilisateur ne voit jamais les fichiers d'un autre.
   */
  async listUserFiles(userId: number) {
    const files = await this.fileRepo.find({ where: { ownerId: userId } });
    return files.map((f) => this.toResponse(f));
  }

  /**
   * Convertit une entité SharedFile en objet de réponse snake_case.
   *
   * Le frontend Vue.js attend du snake_case (original_name, is_expired…)
   * et un share_url complet plutôt qu'un simple token.
   * Cette méthode centralise la sérialisation pour éviter les incohérences.
   */
  toResponse(file: SharedFile) {
    const frontendUrl = process.env.FRONTEND_URL ?? 'http://localhost:5173';
    return {
      id: file.id,
      original_name: file.originalName,
      size: file.size,
      content_type: file.contentType,
      share_token: file.shareToken,
      share_url: `${frontendUrl}/download/${file.shareToken}`,
      expires_at: file.expiresAt,
      created_at: file.createdAt,
      is_expired: file.isExpired,
      is_password_protected: file.isPasswordProtected,
    };
  }

  /**
   * Recherche un fichier par son token de partage.
   * Utilisé par les endpoints publics (info et download).
   * Retourne 404 si le token est inconnu — on ne révèle pas si le lien a expiré ici.
   */
  async getByToken(token: string) {
    const file = await this.fileRepo.findOneBy({ shareToken: token });
    if (!file) throw new NotFoundException('Lien invalide.');
    return file;
  }

  /**
   * Valide le token, l'expiration et le mot de passe, puis retourne le fichier (US02).
   * Utilise HTTP 410 Gone pour les liens expirés — plus précis que 404
   * car la ressource a existé mais n'est plus disponible.
   */
  async download(token: string, password?: string) {
    const file = await this.getByToken(token);

    // HTTP 410 Gone = la ressource a existé mais n'est plus disponible (RFC 7231)
    if (file.isExpired) throw new GoneException('Ce lien de téléchargement a expiré.');

    if (file.isPasswordProtected) {
      const valid = password ? await bcrypt.compare(password, file.passwordHash) : false;
      if (!valid) throw new ForbiddenException('Mot de passe incorrect.');
    }

    return file;
  }

  /**
   * Supprime un fichier physiquement et en base (US06).
   * La recherche par (id + ownerId) garantit qu'un utilisateur ne peut pas
   * supprimer le fichier d'un autre — retourne 404 plutôt que 403 pour ne pas
   * révéler l'existence du fichier à quelqu'un qui n'en est pas propriétaire.
   */
  async delete(fileId: string, userId: number) {
    const file = await this.fileRepo.findOneBy({ id: fileId, ownerId: userId });
    if (!file) throw new NotFoundException();

    // Suppression physique du fichier avant la suppression en base
    // existsSync évite une erreur si le fichier a déjà été supprimé manuellement
    if (fs.existsSync(file.filePath)) fs.unlinkSync(file.filePath);
    await this.fileRepo.remove(file);
  }

  /**
   * Purge tous les fichiers expirés — à appeler via une tâche cron (US10).
   * Retourne le nombre de fichiers supprimés pour les logs.
   *
   * createQueryBuilder permet d'écrire du SQL plus expressif que find()
   * pour les requêtes avec des conditions sur des dates.
   */
  async purgeExpired() {
    const expired = await this.fileRepo
      .createQueryBuilder('f')
      .where('f.expiresAt < NOW()')
      .getMany();

    for (const file of expired) {
      if (fs.existsSync(file.filePath)) fs.unlinkSync(file.filePath);
      await this.fileRepo.remove(file);
    }

    return expired.length;
  }
}
