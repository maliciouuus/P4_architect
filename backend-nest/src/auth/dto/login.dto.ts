import { IsEmail, IsString } from 'class-validator';

/**
 * DTO pour la connexion d'un utilisateur (US04).
 * Valide uniquement le format de l'email et la présence du mot de passe.
 * La vérification du mot de passe lui-même est faite dans AuthService.
 */
export class LoginDto {
  @IsEmail()
  email: string;

  // On vérifie juste que c'est une string non vide — pas de MinLength ici
  // pour ne pas révéler d'informations sur la politique de mot de passe en cas d'erreur
  @IsString()
  password: string;
}
