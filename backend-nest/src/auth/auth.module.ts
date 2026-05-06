import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { JwtModule } from '@nestjs/jwt';
import { PassportModule } from '@nestjs/passport';
import { User } from './user.entity';
import { AuthService } from './auth.service';
import { AuthController } from './auth.controller';
import { JwtStrategy } from './jwt.strategy';

/**
 * Module d'authentification — regroupe tout ce qui concerne les utilisateurs et le JWT.
 *
 * En NestJS, un Module est un conteneur qui déclare :
 * - imports  : modules externes dont ce module dépend
 * - providers : services, stratégies, guards instanciés par l'injecteur NestJS
 * - controllers : classes qui gèrent les routes HTTP
 * - exports : ce que les autres modules peuvent utiliser depuis celui-ci
 */
@Module({
  imports: [
    // Enregistre le Repository<User> dans l'injecteur de ce module
    // Nécessaire pour que @InjectRepository(User) fonctionne dans AuthService
    TypeOrmModule.forFeature([User]),

    // PassportModule active le système de stratégies d'authentification
    PassportModule,

    // JwtModule configure la librairie de signature/vérification de tokens
    // La clé secrète doit être longue et aléatoire en production
    JwtModule.register({
      secret: process.env.JWT_SECRET ?? 'change_me_in_production',
      signOptions: { expiresIn: '7d' }, // Le token expire après 7 jours
    }),
  ],
  // AuthService et JwtStrategy sont instanciés par NestJS et injectables dans ce module
  providers: [AuthService, JwtStrategy],
  controllers: [AuthController],
  // On exporte AuthService pour que d'autres modules puissent l'utiliser si besoin
  exports: [AuthService],
})
export class AuthModule {}
