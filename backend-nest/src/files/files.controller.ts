import {
  Controller,
  Get,
  Post,
  Delete,
  Param,
  Query,
  UseGuards,
  UseInterceptors,
  UploadedFile,
  Request,
  Res,
  Body,
} from '@nestjs/common';
import { FileInterceptor } from '@nestjs/platform-express';
import { diskStorage } from 'multer';
import type { Response } from 'express';
import * as fs from 'fs';
import { FilesService } from './files.service';
import { JwtAuthGuard } from '../auth/jwt-auth.guard';
import { UploadFileDto } from './dto/upload-file.dto';

/**
 * Configuration du stockage temporaire Multer.
 *
 * Multer est le middleware Node.js standard pour gérer les uploads multipart/form-data.
 * On stocke d'abord le fichier dans /tmp avec un nom unique horodaté,
 * puis FilesService le déplace vers sa destination définitive.
 * Cette approche en deux étapes permet de valider le fichier avant de le stocker.
 */
const tempStorage = diskStorage({
  destination: (_, __, cb) => {
    fs.mkdirSync('tmp', { recursive: true });
    cb(null, 'tmp');
  },
  // Nom temporaire unique pour éviter les collisions si plusieurs uploads simultanés
  filename: (_, file, cb) => cb(null, `${Date.now()}-${file.originalname}`),
});

/**
 * Controller de gestion des fichiers — expose tous les endpoints liés aux fichiers.
 *
 * Routes exposées :
 *   GET    /api/files/                    → historique utilisateur (authentifié)
 *   POST   /api/files/upload              → upload connecté (US01)
 *   POST   /api/files/upload/anonymous    → upload anonyme (US07)
 *   DELETE /api/files/:id                 → suppression (US06)
 *   GET    /api/files/share/:token        → infos publiques (US02)
 *   GET    /api/files/download/:token     → téléchargement (US02)
 */
@Controller('files')
export class FilesController {
  constructor(private filesService: FilesService) {}

  /**
   * GET /api/files/
   * Retourne la liste des fichiers de l'utilisateur connecté (US05).
   * Protégé par JWT — 401 si pas de token valide.
   */
  @Get()
  @UseGuards(JwtAuthGuard)
  list(@Request() req: any) {
    return this.filesService.listUserFiles(req.user.id);
  }

  /**
   * POST /api/files/upload
   * Upload d'un fichier par un utilisateur connecté (US01).
   *
   * @UseInterceptors(FileInterceptor) active Multer pour ce endpoint.
   * 'file' est le nom du champ dans le formulaire multipart.
   * Le fichier est accessible via @UploadedFile().
   */
  @Post('upload')
  @UseGuards(JwtAuthGuard)
  @UseInterceptors(FileInterceptor('file', { storage: tempStorage }))
  async upload(
    @UploadedFile() file: Express.Multer.File,
    @Body() dto: UploadFileDto,
    @Request() req: any,
  ) {
    return this.filesService.upload(file, req.user, dto.password, dto.expiry_hours);
  }

  /**
   * POST /api/files/upload/anonymous
   * Upload sans compte (US07) — pas de guard JWT.
   * Le fichier n'est lié à aucun utilisateur (owner = null).
   */
  @Post('upload/anonymous')
  @UseInterceptors(FileInterceptor('file', { storage: tempStorage }))
  async uploadAnonymous(
    @UploadedFile() file: Express.Multer.File,
    @Body() dto: UploadFileDto,
  ) {
    return this.filesService.upload(file, null, dto.password, dto.expiry_hours);
  }

  /**
   * DELETE /api/files/:id
   * Supprime un fichier appartenant à l'utilisateur connecté (US06).
   * Le service vérifie que l'id + ownerId correspondent — on ne peut pas supprimer
   * le fichier d'un autre utilisateur.
   */
  @Delete(':id')
  @UseGuards(JwtAuthGuard)
  delete(@Param('id') id: string, @Request() req: any) {
    return this.filesService.delete(id, req.user.id);
  }

  /**
   * GET /api/files/share/:token
   * Retourne les métadonnées publiques d'un fichier (US02).
   * Accessible sans authentification — utilisé par la page de téléchargement
   * pour afficher nom, taille, expiration avant de déclencher le download.
   * Ne retourne jamais le chemin disque ni le hash du mot de passe.
   */
  /**
   * GET /api/files/share/:token
   * Retourne les métadonnées publiques en snake_case pour le frontend Vue.js.
   * On utilise toResponse() du service pour avoir les mêmes noms de champs
   * que dans la liste des fichiers — cohérence de l'API.
   */
  @Get('share/:token')
  async publicInfo(@Param('token') token: string) {
    const file = await this.filesService.getByToken(token);
    return this.filesService.toResponse(file);
  }

  /**
   * GET /api/files/download/:token?password=xxx
   * Télécharge le fichier si le token est valide et le mot de passe correct (US02).
   *
   * @Res() injecte l'objet Response Express directement — nécessaire pour streamer
   * le fichier avec createReadStream().pipe(res) sans le charger entièrement en mémoire.
   * C'est important pour les gros fichiers (jusqu'à 1 Go).
   */
  @Get('download/:token')
  async download(
    @Param('token') token: string,
    @Query('password') password: string,
    @Res() res: Response,
  ) {
    const file = await this.filesService.download(token, password);

    // En-têtes HTTP pour forcer le téléchargement côté navigateur
    res.setHeader('Content-Type', file.contentType);
    res.setHeader('Content-Disposition', `attachment; filename="${file.originalName}"`);

    // Streaming : lit le fichier par morceaux et l'envoie au client au fur et à mesure
    // Évite de charger 1 Go en RAM avant d'envoyer — essentiel pour la performance
    fs.createReadStream(file.filePath).pipe(res);
  }
}
