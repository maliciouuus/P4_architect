import { Controller, Post, Get, Body, UseGuards, Request } from '@nestjs/common';
import { AuthService } from './auth.service';
import { RegisterDto } from './dto/register.dto';
import { LoginDto } from './dto/login.dto';
import { JwtAuthGuard } from './jwt-auth.guard';

/**
 * Controller d'authentification — expose les endpoints HTTP liés aux utilisateurs.
 *
 * Un Controller en NestJS reçoit les requêtes HTTP entrantes, applique les DTOs
 * pour la validation, puis délègue le traitement au Service correspondant.
 * Il ne contient aucune logique métier — son rôle est uniquement de faire le lien
 * entre HTTP et le Service.
 *
 * @Controller('auth') → toutes les routes ici sont préfixées par /api/auth/
 * (le préfixe /api vient du setGlobalPrefix dans main.ts)
 */
@Controller('auth')
export class AuthController {
  // Injection de dépendance : NestJS instancie AuthService et l'injecte automatiquement
  constructor(private authService: AuthService) {}

  /**
   * POST /api/auth/register
   * Accessible sans authentification.
   * @Body() dto — NestJS désérialise le JSON du body et valide via RegisterDto
   */
  @Post('register')
  register(@Body() dto: RegisterDto) {
    return this.authService.register(dto);
  }

  /**
   * POST /api/auth/login
   * Retourne un token JWT si les identifiants sont valides.
   */
  @Post('login')
  login(@Body() dto: LoginDto) {
    return this.authService.login(dto);
  }

  /**
   * GET /api/auth/me
   * Protégé par JwtAuthGuard — retourne 401 si pas de token valide.
   * req.user est peuplé par JwtStrategy.validate() après vérification du JWT.
   */
  @Get('me')
  @UseGuards(JwtAuthGuard)
  me(@Request() req: any) {
    return this.authService.getProfile(req.user.id);
  }
}
