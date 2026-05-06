import { Injectable } from '@nestjs/common';
import { AuthGuard } from '@nestjs/passport';

/**
 * Guard JWT — protège les routes qui nécessitent une authentification.
 *
 * Un Guard en NestJS est un intercepteur de requête qui décide si elle peut
 * continuer ou doit être rejetée (401 Unauthorized).
 *
 * Utilisation sur une route : @UseGuards(JwtAuthGuard)
 * Utilisation sur tout un controller : @UseGuards(JwtAuthGuard) au-dessus de la classe
 *
 * AuthGuard('jwt') fait référence à la stratégie nommée 'jwt' — c'est le nom
 * par défaut de PassportStrategy(Strategy) dans jwt.strategy.ts.
 */
@Injectable()
export class JwtAuthGuard extends AuthGuard('jwt') {}
