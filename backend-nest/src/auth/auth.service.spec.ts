/**
 * Tests unitaires du service d'authentification (AuthService).
 *
 * Ces tests vérifient la logique métier des US03 et US04 sans démarrer
 * de serveur HTTP ni toucher une vraie base de données.
 *
 * Stratégie : on utilise des "mocks" (faux objets) pour simuler
 * le repository TypeORM et le service JWT. Cela permet de tester
 * uniquement le code du service, isolé de ses dépendances.
 *
 * Pourquoi des mocks et pas une vraie base ?
 * → Les tests unitaires doivent être rapides (< 1s) et reproductibles.
 *   Une vraie base de données les rendrait lents, fragiles et dépendants
 *   de l'environnement. Les tests d'intégration (E2E) couvrent ça.
 */

import { Test, TestingModule } from '@nestjs/testing';
import { getRepositoryToken } from '@nestjs/typeorm';
import { JwtService } from '@nestjs/jwt';
import { ConflictException, UnauthorizedException } from '@nestjs/common';
import * as bcrypt from 'bcrypt';

import { AuthService } from './auth.service';
import { User } from './user.entity';

// Faux repository TypeORM — simule les méthodes find/save sans base de données
const mockUserRepository = {
  findOneBy: jest.fn(),
  create: jest.fn(),
  save: jest.fn(),
};

// Faux JwtService — on n'a pas besoin de vrai secret pour tester la logique
const mockJwtService = {
  sign: jest.fn().mockReturnValue('fake.jwt.token'),
};

describe('AuthService', () => {
  let service: AuthService;

  // Avant chaque test, on recrée le module NestJS avec les mocks injectés
  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [
        AuthService,
        // On remplace le vrai repository par notre mock
        { provide: getRepositoryToken(User), useValue: mockUserRepository },
        { provide: JwtService, useValue: mockJwtService },
      ],
    }).compile();

    service = module.get<AuthService>(AuthService);

    // Réinitialise les appels enregistrés entre chaque test pour éviter
    // qu'un test précédent pollue le suivant
    jest.clearAllMocks();
  });

  // ─── US03 : Création de compte ───────────────────────────────────────────

  describe('register()', () => {
    it('crée un utilisateur et retourne son profil sans le mot de passe', async () => {
      // GIVEN : aucun utilisateur existant avec cet email
      mockUserRepository.findOneBy.mockResolvedValue(null);

      // Le repository.create() retourne l'entité construite, save() simule l'INSERT
      mockUserRepository.create.mockReturnValue({
        id: 1,
        email: 'test@test.com',
        username: 'testuser',
        password: 'hashed',
      });
      mockUserRepository.save.mockResolvedValue(undefined);

      // WHEN : on appelle register()
      const result = await service.register({
        email: 'test@test.com',
        username: 'testuser',
        password: 'password123',
      });

      // THEN : le profil retourné ne contient pas le mot de passe
      expect(result).toEqual({
        id: 1,
        email: 'test@test.com',
        username: 'testuser',
      });

      // On vérifie que save() a bien été appelé (INSERT en base)
      expect(mockUserRepository.save).toHaveBeenCalled();
    });

    it('lève ConflictException si l\'email est déjà utilisé (US03 — unicité email)', async () => {
      // GIVEN : un utilisateur existe déjà avec cet email
      mockUserRepository.findOneBy.mockResolvedValue({
        id: 1,
        email: 'test@test.com',
      });

      // WHEN / THEN : register() doit lancer une exception 409 Conflict
      await expect(
        service.register({ email: 'test@test.com', username: 'other', password: 'pass1234' }),
      ).rejects.toThrow(ConflictException);

      // Aucun utilisateur ne doit avoir été créé
      expect(mockUserRepository.save).not.toHaveBeenCalled();
    });

    it('hache le mot de passe avant de sauvegarder (US03 — sécurité)', async () => {
      // GIVEN
      mockUserRepository.findOneBy.mockResolvedValue(null);
      mockUserRepository.create.mockImplementation((dto) => dto);
      mockUserRepository.save.mockResolvedValue(undefined);

      // WHEN
      await service.register({
        email: 'new@test.com',
        username: 'newuser',
        password: 'plaintext',
      });

      // THEN : le mot de passe transmis à create() ne doit pas être "plaintext"
      const createdWith = mockUserRepository.create.mock.calls[0][0];
      expect(createdWith.password).not.toBe('plaintext');

      // On vérifie que c'est bien un hash bcrypt valide
      const isHash = await bcrypt.compare('plaintext', createdWith.password);
      expect(isHash).toBe(true);
    });
  });

  // ─── US04 : Connexion utilisateur ────────────────────────────────────────

  describe('login()', () => {
    it('retourne un token JWT pour des identifiants valides', async () => {
      // GIVEN : un utilisateur existant avec un mot de passe hashé
      const hashedPassword = await bcrypt.hash('password123', 12);
      mockUserRepository.findOneBy.mockResolvedValue({
        id: 1,
        email: 'test@test.com',
        username: 'testuser',
        password: hashedPassword,
      });

      // WHEN
      const result = await service.login({ email: 'test@test.com', password: 'password123' });

      // THEN : on reçoit un access_token et le profil utilisateur
      expect(result.access_token).toBe('fake.jwt.token');
      expect(result.user.email).toBe('test@test.com');

      // Le token doit avoir été signé avec le bon payload
      expect(mockJwtService.sign).toHaveBeenCalledWith({
        sub: 1,
        email: 'test@test.com',
      });
    });

    it('lève UnauthorizedException si l\'email est inconnu', async () => {
      // GIVEN : aucun utilisateur avec cet email
      mockUserRepository.findOneBy.mockResolvedValue(null);

      // WHEN / THEN : 401 Unauthorized
      await expect(
        service.login({ email: 'unknown@test.com', password: 'anything' }),
      ).rejects.toThrow(UnauthorizedException);
    });

    it('lève UnauthorizedException si le mot de passe est incorrect', async () => {
      // GIVEN : utilisateur existant mais mot de passe différent
      const hashedPassword = await bcrypt.hash('correct_password', 12);
      mockUserRepository.findOneBy.mockResolvedValue({
        id: 1,
        email: 'test@test.com',
        password: hashedPassword,
      });

      // WHEN / THEN : 401 — même message générique que pour l'email inconnu
      // (sécurité : on ne révèle pas si c'est l'email ou le mot de passe qui est faux)
      await expect(
        service.login({ email: 'test@test.com', password: 'wrong_password' }),
      ).rejects.toThrow(UnauthorizedException);
    });
  });
});
