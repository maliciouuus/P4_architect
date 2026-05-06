import { Injectable } from '@nestjs/common';
import { PassportStrategy } from '@nestjs/passport';
import { ExtractJwt, Strategy } from 'passport-jwt';

/**
 * Stratégie JWT pour Passport — définit comment valider un token entrant.
 *
 * Passport est une librairie d'authentification modulaire pour Node.js.
 * NestJS s'intègre avec Passport via @nestjs/passport.
 * Une "stratégie" définit la méthode d'authentification (JWT, OAuth, local...).
 *
 * Flux d'une requête protégée :
 * 1. Le client envoie "Authorization: Bearer <token>" dans l'en-tête HTTP
 * 2. JwtAuthGuard intercepte la requête et appelle cette stratégie
 * 3. ExtractJwt extrait le token de l'en-tête
 * 4. passport-jwt vérifie la signature avec JWT_SECRET
 * 5. validate() est appelé avec le payload décodé
 * 6. L'objet retourné par validate() est disponible dans req.user
 */
@Injectable()
export class JwtStrategy extends PassportStrategy(Strategy) {
  constructor() {
    super({
      // Extrait le token depuis l'en-tête "Authorization: Bearer <token>"
      jwtFromRequest: ExtractJwt.fromAuthHeaderAsBearerToken(),

      // Clé secrète utilisée pour vérifier la signature HMAC du token
      // Doit être identique à celle utilisée pour signer dans AuthService
      secretOrKey: process.env.JWT_SECRET ?? 'change_me_in_production',
    });
  }

  /**
   * Appelé par Passport après vérification de la signature du token.
   * Le payload est le contenu décodé du JWT (ce qu'on a mis dans jwtService.sign()).
   * La valeur retournée est injectée dans req.user par NestJS.
   */
  validate(payload: { sub: number; email: string }) {
    // sub = subject (convention RFC 7519) = id de l'utilisateur
    return { id: payload.sub, email: payload.email };
  }
}
