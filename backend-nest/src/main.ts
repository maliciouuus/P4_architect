import { NestFactory } from '@nestjs/core';
import { ValidationPipe } from '@nestjs/common';
import { AppModule } from './app.module';

/**
 * Point d'entrée de l'application NestJS.
 * Cette fonction configure et démarre le serveur HTTP.
 */
async function bootstrap() {
  // Crée l'instance de l'application NestJS à partir du module racine
  const app = await NestFactory.create(AppModule);

  // Préfixe global : toutes les routes seront sous /api/...
  // Ex: /api/auth/login, /api/files/upload
  app.setGlobalPrefix('api');

  // ValidationPipe applique automatiquement les décorateurs de class-validator
  // sur tous les DTOs (Data Transfer Objects) — ex: @IsEmail(), @MinLength()
  // whitelist: true supprime silencieusement les champs non déclarés dans le DTO
  app.useGlobalPipes(new ValidationPipe({ whitelist: true }));

  // CORS : autorise le frontend Vue.js (port 5173) à faire des requêtes HTTP
  // credentials: true permet l'envoi des cookies et en-têtes d'autorisation
  app.enableCors({
    origin: process.env.FRONTEND_URL ?? 'http://localhost:5173',
    credentials: true,
  });

  // Démarre le serveur sur le port défini dans .env ou 8000 par défaut
  await app.listen(process.env.PORT ?? 8000);
}
bootstrap();
