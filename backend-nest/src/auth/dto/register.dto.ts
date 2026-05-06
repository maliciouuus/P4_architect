import { IsEmail, IsString, MinLength } from 'class-validator';

/**
 * DTO (Data Transfer Object) pour l'inscription d'un utilisateur.
 *
 * Un DTO définit la forme exacte des données attendues dans le body d'une requête HTTP.
 * Les décorateurs de class-validator déclenchent la validation automatiquement
 * grâce au ValidationPipe configuré dans main.ts.
 *
 * Si un champ est invalide, NestJS retourne automatiquement un 400 Bad Request
 * avec un message d'erreur détaillé — sans écrire une seule ligne de validation manuellement.
 */
export class RegisterDto {
  // Vérifie que la valeur est un email valide (format RFC 5322)
  @IsEmail()
  email: string;

  // Vérifie que c'est une chaîne d'au moins 3 caractères
  @IsString()
  @MinLength(3)
  username: string;

  // Mot de passe : minimum 8 caractères (US03 — règle de gestion)
  @IsString()
  @MinLength(8)
  password: string;
}
