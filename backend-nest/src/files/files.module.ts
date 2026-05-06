import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { SharedFile } from './shared-file.entity';
import { FilesService } from './files.service';
import { FilesController } from './files.controller';
import { FilesCron } from './files.cron';

/**
 * Module de gestion des fichiers — regroupe tout ce qui concerne les fichiers partagés.
 *
 * TypeOrmModule.forFeature([SharedFile]) enregistre le Repository<SharedFile>
 * dans l'injecteur de ce module, ce qui permet à FilesService d'utiliser
 * @InjectRepository(SharedFile) pour accéder à la base de données.
 */
@Module({
  imports: [TypeOrmModule.forFeature([SharedFile])],
  providers: [FilesService, FilesCron],
  controllers: [FilesController],
})
export class FilesModule {}
