import { Injectable, Logger } from '@nestjs/common';
import { FilesService } from './files.service';

/**
 * Tâche planifiée de purge des fichiers expirés (US10).
 *
 * NestJS ne dispose pas d'un scheduler intégré dans la version de base.
 * On utilise setInterval natif Node.js pour déclencher la purge toutes les 24 heures.
 * En production, utiliser @nestjs/schedule avec @Cron() pour plus de contrôle.
 *
 * La purge supprime à la fois le fichier physique sur le disque
 * et ses métadonnées en base de données.
 */
@Injectable()
export class FilesCron {
  private readonly logger = new Logger(FilesCron.name);

  constructor(private filesService: FilesService) {
    // Lance la première purge 1 minute après le démarrage du serveur
    // puis toutes les 24 heures
    setTimeout(() => this.purge(), 60_000);
    setInterval(() => this.purge(), 24 * 3600 * 1000);
  }

  private async purge() {
    try {
      const count = await this.filesService.purgeExpired();
      if (count > 0) {
        this.logger.log(`Purge des fichiers expirés : ${count} fichier(s) supprimé(s)`);
      }
    } catch (err) {
      this.logger.error('Erreur lors de la purge des fichiers expirés', err);
    }
  }
}
