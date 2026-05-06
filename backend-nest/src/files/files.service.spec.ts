/**
 * Tests unitaires du service de fichiers (FilesService).
 *
 * Couvre les US01, US02, US06 et US10 — les fonctionnalités MVP du service.
 *
 * On mocke :
 * - Le repository TypeORM (pas de vraie base de données)
 * - Le système de fichiers (fs) — on ne crée pas de vrais fichiers sur le disque
 *
 * Chaque test suit le pattern AAA (Arrange / Act / Assert) :
 * - Arrange (GIVEN) : prépare l'état initial et les mocks
 * - Act (WHEN) : appelle la méthode à tester
 * - Assert (THEN) : vérifie le résultat ou les effets de bord
 */

import { Test, TestingModule } from '@nestjs/testing';
import { getRepositoryToken } from '@nestjs/typeorm';
import { NotFoundException, ForbiddenException, GoneException } from '@nestjs/common';
import * as bcrypt from 'bcrypt';

import { FilesService } from './files.service';
import { SharedFile } from './shared-file.entity';

// Mock partiel de fs : on remplace uniquement les méthodes utilisées par FilesService,
// mais on conserve le vrai module via jest.requireActual pour que TypeORM
// (qui utilise fs en interne) continue de fonctionner correctement.
jest.mock('fs', () => ({
  ...jest.requireActual('fs'),
  mkdirSync: jest.fn(),
  renameSync: jest.fn(),
  unlinkSync: jest.fn(),
  existsSync: jest.fn().mockReturnValue(true),
  createReadStream: jest.fn(),
}));

// Mock de uuid pour avoir des valeurs prédictibles dans les assertions
jest.mock('uuid', () => ({ v4: jest.fn().mockReturnValue('mock-uuid-1234') }));

// Mock de bcrypt — en test unitaire on vérifie que bcrypt EST appelé,
// pas que l'algorithme de hachage lui-même fonctionne (c'est le rôle des tests bcrypt).
// Cela évite aussi de charger le module natif C++ dans l'environnement Jest.
jest.mock('bcrypt', () => ({
  hash: jest.fn().mockResolvedValue('$2b$12$mockedhash'),
  compare: jest.fn(),
}));

// Faux repository TypeORM
const mockFileRepository = {
  findOneBy: jest.fn(),
  find: jest.fn(),
  create: jest.fn(),
  save: jest.fn(),
  remove: jest.fn(),
  createQueryBuilder: jest.fn(),
};

// Faux fichier Multer — simule un fichier uploadé par le client
const mockMulterFile = {
  originalname: 'document.pdf',
  path: '/tmp/1234-document.pdf',
  size: 1024,
  mimetype: 'application/pdf',
} as Express.Multer.File;

describe('FilesService', () => {
  let service: FilesService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [
        FilesService,
        { provide: getRepositoryToken(SharedFile), useValue: mockFileRepository },
      ],
    }).compile();

    service = module.get<FilesService>(FilesService);
    jest.clearAllMocks();
  });

  // ─── US01 : Upload avec compte ───────────────────────────────────────────

  describe('upload()', () => {
    it('crée un SharedFile avec les bonnes métadonnées', async () => {
      // GIVEN : un utilisateur connecté et un faux fichier
      const fakeUser = { id: 1, email: 'user@test.com' } as any;
      const savedFile = {
        id: 'mock-uuid-1234',
        originalName: 'document.pdf',
        shareToken: 'mock-uuid-1234',
        isExpired: false,
        isPasswordProtected: false,
        expiresAt: new Date(),
        createdAt: new Date(),
        size: 1024,
        contentType: 'application/pdf',
      } as SharedFile;

      mockFileRepository.create.mockReturnValue(savedFile);
      mockFileRepository.save.mockResolvedValue(savedFile);

      // WHEN
      const result = await service.upload(mockMulterFile, fakeUser);

      // THEN : le repository a bien reçu un appel create() avec le bon propriétaire
      expect(mockFileRepository.create).toHaveBeenCalledWith(
        expect.objectContaining({
          ownerId: 1,
          originalName: 'document.pdf',
          contentType: 'application/pdf',
        }),
      );

      // La réponse doit être en snake_case (format attendu par le frontend)
      expect(result).toHaveProperty('original_name');
      expect(result).toHaveProperty('share_url');
      expect(result).toHaveProperty('is_expired');
    });

    it('rejette les fichiers interdits (.exe) et supprime le fichier temporaire', async () => {
      // GIVEN : un fichier .exe
      const exeFile = { ...mockMulterFile, originalname: 'virus.exe', path: '/tmp/virus.exe' } as Express.Multer.File;
      const fs = require('fs');

      // WHEN / THEN : ForbiddenException levée
      await expect(service.upload(exeFile, null)).rejects.toThrow(ForbiddenException);

      // Le fichier temporaire doit être supprimé immédiatement pour ne pas laisser
      // de fichier dangereux sur le serveur (US01 — contrôles de saisie)
      expect(fs.unlinkSync).toHaveBeenCalledWith('/tmp/virus.exe');
    });

    it('hashage du mot de passe si fourni (US09)', async () => {
      // GIVEN
      const savedFile = {
        id: 'uuid',
        originalName: 'doc.pdf',
        shareToken: 'uuid',
        isExpired: false,
        isPasswordProtected: true,
        expiresAt: new Date(),
        createdAt: new Date(),
        size: 1024,
        contentType: 'application/pdf',
      } as SharedFile;
      mockFileRepository.create.mockReturnValue(savedFile);
      mockFileRepository.save.mockResolvedValue(savedFile);

      // WHEN : upload avec un mot de passe
      await service.upload(mockMulterFile, null, 'secret123');

      // THEN : bcrypt.hash doit avoir été appelé avec le mot de passe en clair
      // On vérifie l'appel au mock, pas le résultat du vrai algorithme bcrypt
      expect(bcrypt.hash).toHaveBeenCalledWith('secret123', 12);

      // Et create() doit avoir reçu le hash retourné par bcrypt.hash (notre mock)
      const createdWith = mockFileRepository.create.mock.calls[0][0];
      expect(createdWith.passwordHash).toBe('$2b$12$mockedhash');
    });
  });

  // ─── US05 : Historique utilisateur ───────────────────────────────────────

  describe('listUserFiles()', () => {
    it('retourne uniquement les fichiers du propriétaire connecté', async () => {
      // GIVEN : deux fichiers en base appartenant à l'utilisateur 1
      const files = [
        { id: 'a', ownerId: 1, originalName: 'a.pdf', shareToken: 'tok-a', isExpired: false, isPasswordProtected: false, size: 1, contentType: 'application/pdf', expiresAt: new Date(), createdAt: new Date() },
        { id: 'b', ownerId: 1, originalName: 'b.pdf', shareToken: 'tok-b', isExpired: false, isPasswordProtected: false, size: 2, contentType: 'application/pdf', expiresAt: new Date(), createdAt: new Date() },
      ] as SharedFile[];
      mockFileRepository.find.mockResolvedValue(files);

      // WHEN
      const result = await service.listUserFiles(1);

      // THEN : on reçoit 2 fichiers, filtrés par ownerId: 1
      expect(mockFileRepository.find).toHaveBeenCalledWith({ where: { ownerId: 1 } });
      expect(result).toHaveLength(2);
      // Les champs doivent être en snake_case pour le frontend
      expect(result[0]).toHaveProperty('original_name', 'a.pdf');
    });
  });

  // ─── US02 : Téléchargement via lien ──────────────────────────────────────

  describe('download()', () => {
    it('retourne le fichier si le token est valide et non expiré', async () => {
      // GIVEN : fichier non expiré et non protégé
      const file = {
        shareToken: 'valid-token',
        isExpired: false,
        isPasswordProtected: false,
        filePath: '/uploads/doc.pdf',
      } as SharedFile;
      mockFileRepository.findOneBy.mockResolvedValue(file);

      // WHEN
      const result = await service.download('valid-token');

      // THEN : le fichier est retourné sans erreur
      expect(result).toBe(file);
    });

    it('lève GoneException (410) si le lien est expiré (US02)', async () => {
      // GIVEN : fichier expiré
      const file = { shareToken: 'expired-token', isExpired: true } as SharedFile;
      mockFileRepository.findOneBy.mockResolvedValue(file);

      // WHEN / THEN : 410 Gone = la ressource a existé mais n'est plus disponible
      await expect(service.download('expired-token')).rejects.toThrow(GoneException);
    });

    it('lève ForbiddenException si le mot de passe est incorrect (US09)', async () => {
      // GIVEN : fichier protégé — bcrypt.compare est mocké pour retourner false
      (bcrypt.compare as jest.Mock).mockResolvedValue(false);
      const file = {
        shareToken: 'tok',
        isExpired: false,
        isPasswordProtected: true,
        passwordHash: '$2b$12$somehash',
      } as SharedFile;
      mockFileRepository.findOneBy.mockResolvedValue(file);

      // WHEN / THEN : 403 Forbidden si bcrypt.compare retourne false
      await expect(service.download('tok', 'wrong')).rejects.toThrow(ForbiddenException);
    });

    it('autorise le téléchargement si le mot de passe est correct (US09)', async () => {
      // GIVEN : bcrypt.compare mocké pour retourner true (bon mot de passe)
      (bcrypt.compare as jest.Mock).mockResolvedValue(true);
      const file = {
        shareToken: 'tok',
        isExpired: false,
        isPasswordProtected: true,
        passwordHash: '$2b$12$somehash',
        filePath: '/uploads/secret.pdf',
      } as SharedFile;
      mockFileRepository.findOneBy.mockResolvedValue(file);

      // WHEN / THEN : pas d'exception levée — le fichier est retourné directement
      const result = await service.download('tok', 'correct');
      expect(result).toBe(file);
    });

    it('lève NotFoundException si le token est inconnu (US02)', async () => {
      // GIVEN : aucun fichier avec ce token
      mockFileRepository.findOneBy.mockResolvedValue(null);

      // WHEN / THEN : 404
      await expect(service.download('unknown-token')).rejects.toThrow(NotFoundException);
    });
  });

  // ─── US06 : Suppression d'un fichier ─────────────────────────────────────

  describe('delete()', () => {
    it('supprime le fichier en base et sur le disque', async () => {
      // GIVEN : le fichier appartient à l'utilisateur 1
      const file = { id: 'file-uuid', ownerId: 1, filePath: '/uploads/doc.pdf' } as SharedFile;
      mockFileRepository.findOneBy.mockResolvedValue(file);
      mockFileRepository.remove.mockResolvedValue(undefined);
      const fs = require('fs');

      // WHEN
      await service.delete('file-uuid', 1);

      // THEN : suppression physique sur le disque ET en base de données
      expect(fs.unlinkSync).toHaveBeenCalledWith('/uploads/doc.pdf');
      expect(mockFileRepository.remove).toHaveBeenCalledWith(file);
    });

    it('lève NotFoundException si le fichier n\'appartient pas à l\'utilisateur (US06)', async () => {
      // GIVEN : aucun fichier avec cet id + ownerId combinés
      // (TypeORM retourne null si les deux conditions ne sont pas remplies)
      mockFileRepository.findOneBy.mockResolvedValue(null);

      // WHEN / THEN : 404 plutôt que 403 pour ne pas révéler l'existence du fichier
      await expect(service.delete('other-file', 1)).rejects.toThrow(NotFoundException);
    });
  });
});
