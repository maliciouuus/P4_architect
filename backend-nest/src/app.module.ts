import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { ConfigModule } from '@nestjs/config';
import { AuthModule } from './auth/auth.module';
import { FilesModule } from './files/files.module';
import { User } from './auth/user.entity';
import { SharedFile } from './files/shared-file.entity';

/**
 * Module racine de l'application — le point de départ que NestJS charge en premier.
 * Il regroupe tous les sous-modules et configure les services globaux
 * (base de données, variables d'environnement).
 *
 * Architecture NestJS : chaque fonctionnalité est isolée dans son propre Module
 * (AuthModule, FilesModule), ce qui permet de tester et maintenir chaque partie
 * indépendamment.
 */
@Module({
  imports: [
    // ConfigModule charge les variables d'environnement depuis le fichier .env
    // isGlobal: true les rend accessibles dans toute l'application sans ré-import
    ConfigModule.forRoot({ isGlobal: true }),

    // TypeOrmModule connecte l'application à PostgreSQL via une URL de connexion
    // synchronize: true crée/met à jour les tables automatiquement depuis les entités
    // ⚠️ En production, remplacer synchronize par des migrations explicites
    TypeOrmModule.forRoot({
      type: 'postgres',
      url: process.env.DATABASE_URL,
      entities: [User, SharedFile],
      synchronize: true,
    }),

    // Module d'authentification : inscription, connexion, JWT
    AuthModule,

    // Module de gestion des fichiers : upload, download, suppression, historique
    FilesModule,
  ],
})
export class AppModule {}
