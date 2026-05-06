import { Entity, PrimaryGeneratedColumn, Column, CreateDateColumn, ManyToOne, JoinColumn } from 'typeorm';
import { User } from '../auth/user.entity';

/**
 * Entité représentant un fichier partagé en base de données.
 *
 * Correspond à la table shared_files_nest dans PostgreSQL.
 * Un fichier peut appartenir à un utilisateur connecté (US01) ou être anonyme (US07).
 * La relation avec User est optionnelle (nullable: true) pour supporter les deux cas.
 */
@Entity('shared_files_nest')
export class SharedFile {
  // UUID v4 comme clé primaire — non prédictible, contrairement à un entier auto-incrémenté
  // Empêche l'énumération des fichiers par un attaquant qui itèrerait sur les IDs
  @PrimaryGeneratedColumn('uuid')
  id: string;

  // Relation Many-to-One : plusieurs fichiers peuvent appartenir au même utilisateur
  // onDelete: 'CASCADE' — si l'utilisateur est supprimé, ses fichiers le sont aussi
  // nullable: true — un fichier anonyme (US07) n'a pas de propriétaire
  @ManyToOne(() => User, { onDelete: 'CASCADE', nullable: true })
  @JoinColumn({ name: 'owner_id' })
  owner: User | null;

  // Colonne owner_id dupliquée pour permettre les requêtes WHERE sans jointure
  // TypeORM n'expose pas directement la FK d'une relation — on la redéclare explicitement
  @Column({ name: 'owner_id', nullable: true })
  ownerId: number | null;

  // Nom original du fichier, conservé pour proposer le bon nom lors du téléchargement
  @Column()
  originalName: string;

  // Chemin absolu du fichier sur le disque (système de fichiers local)
  // Utilisé pour ouvrir le fichier lors du téléchargement
  @Column()
  filePath: string;

  // Taille en octets — bigint pour supporter les fichiers jusqu'à 1 Go (US01)
  @Column({ type: 'bigint' })
  size: number;

  // Type MIME (ex: 'image/png', 'application/pdf') — utilisé dans Content-Type
  @Column()
  contentType: string;

  // Token opaque inclus dans l'URL de partage : /api/files/share/<token>
  // UUID v4 généré à l'upload — pratiquement impossible à deviner (2^122 possibilités)
  @Column({ unique: true })
  shareToken: string;

  // Date d'expiration du lien — timestamptz inclut le fuseau horaire (UTC en PostgreSQL)
  @Column({ type: 'timestamptz' })
  expiresAt: Date;

  // Hash bcrypt du mot de passe optionnel — chaîne vide si pas de protection (US09)
  @Column({ default: '' })
  passwordHash: string;

  // Date d'upload, générée automatiquement par TypeORM à l'INSERT
  @CreateDateColumn()
  createdAt: Date;

  /**
   * Retourne true si la date d'expiration est dépassée.
   * Propriété calculée côté application — pas stockée en base.
   */
  get isExpired(): boolean {
    return new Date() > this.expiresAt;
  }

  /**
   * Retourne true si le fichier est protégé par un mot de passe.
   * On se base sur la présence du hash plutôt qu'un booléen séparé — source unique de vérité.
   */
  get isPasswordProtected(): boolean {
    return Boolean(this.passwordHash);
  }
}
