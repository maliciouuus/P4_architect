import { IsOptional, IsString, MinLength, IsInt, Min, Max } from 'class-validator';
import { Type } from 'class-transformer';

/**
 * DTO pour l'upload d'un fichier — les deux champs sont optionnels (US01).
 *
 * Ce DTO valide uniquement les métadonnées envoyées avec le fichier.
 * Le fichier lui-même est géré par FileInterceptor (Multer) dans le controller.
 *
 * Les données arrivent en multipart/form-data, pas en JSON.
 * @Type(() => Number) est nécessaire car Multer parse tout en string —
 * sans ça, '72' resterait une string et @IsInt() échouerait.
 */
export class UploadFileDto {
  // Mot de passe optionnel pour protéger l'accès au fichier (US09)
  // Minimum 6 caractères selon les spécifications
  @IsOptional()
  @IsString()
  @MinLength(6)
  password?: string;

  // Durée de validité du lien en heures — entre 1h et 168h (7 jours max, US01 et US10)
  // @Type(() => Number) convertit la string multipart en nombre avant validation
  @IsOptional()
  @Type(() => Number)
  @IsInt()
  @Min(1)
  @Max(168)
  expiry_hours?: number;
}
