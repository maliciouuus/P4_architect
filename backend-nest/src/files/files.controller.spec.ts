jest.mock('bcrypt', () => ({ hash: jest.fn(), compare: jest.fn() }));
jest.mock('typeorm', () => ({
  Entity: () => () => {},
  PrimaryGeneratedColumn: () => () => {},
  Column: () => () => {},
  CreateDateColumn: () => () => {},
  ManyToOne: () => () => {},
  JoinColumn: () => () => {},
  DataSource: jest.fn(),
  Repository: jest.fn(),
}));
jest.mock('@nestjs/typeorm', () => ({
  InjectRepository: () => () => {},
  getRepositoryToken: jest.fn(),
  TypeOrmModule: { forFeature: jest.fn(() => ({ module: class {} })) },
}));
jest.mock('fs', () => ({
  mkdirSync: jest.fn(),
  createReadStream: jest.fn(() => ({ pipe: jest.fn() })),
  unlinkSync: jest.fn(),
  existsSync: jest.fn(() => true),
  renameSync: jest.fn(),
}));

import * as fs from 'fs';
import { FilesController } from './files.controller';

const mockFilesService: any = {
  listUserFiles: jest.fn(),
  upload: jest.fn(),
  delete: jest.fn(),
  getByToken: jest.fn(),
  toResponse: jest.fn(),
  download: jest.fn(),
};

describe('FilesController', () => {
  let controller: FilesController;

  beforeEach(() => {
    controller = new FilesController(mockFilesService);
    jest.clearAllMocks();
  });

  describe('list()', () => {
    it('retourne les fichiers de l\'utilisateur connecté', async () => {
      const files = [{ id: '1' }, { id: '2' }];
      mockFilesService.listUserFiles.mockResolvedValue(files);

      const req = { user: { id: 1 } };
      expect(await controller.list(req)).toEqual(files);
      expect(mockFilesService.listUserFiles).toHaveBeenCalledWith(1);
    });
  });

  describe('upload()', () => {
    it('délègue l\'upload au service avec le bon utilisateur', async () => {
      const file = { originalname: 'test.txt' } as Express.Multer.File;
      const dto = { password: undefined, expiry_hours: undefined };
      const result = { share_url: 'http://x/download/tok' };
      mockFilesService.upload.mockResolvedValue(result);

      const req = { user: { id: 1 } };
      expect(await controller.upload(file, dto as any, req)).toEqual(result);
      expect(mockFilesService.upload).toHaveBeenCalledWith(file, req.user, undefined, undefined);
    });
  });

  describe('uploadAnonymous()', () => {
    it('délègue l\'upload anonyme avec owner null', async () => {
      const file = { originalname: 'anon.txt' } as Express.Multer.File;
      const dto = { password: undefined, expiry_hours: undefined };
      const result = { share_url: 'http://x/download/tok2' };
      mockFilesService.upload.mockResolvedValue(result);

      expect(await controller.uploadAnonymous(file, dto as any)).toEqual(result);
      expect(mockFilesService.upload).toHaveBeenCalledWith(file, null, undefined, undefined);
    });
  });

  describe('delete()', () => {
    it('appelle le service avec l\'id et l\'userId', async () => {
      mockFilesService.delete.mockResolvedValue({ deleted: true });
      const req = { user: { id: 1 } };

      await controller.delete('file-uuid', req);
      expect(mockFilesService.delete).toHaveBeenCalledWith('file-uuid', 1);
    });
  });

  describe('publicInfo()', () => {
    it('retourne les métadonnées publiques du fichier', async () => {
      const file = { id: '1', shareToken: 'tok' };
      const response = { original_name: 'test.txt', is_expired: false };
      mockFilesService.getByToken.mockResolvedValue(file);
      mockFilesService.toResponse.mockReturnValue(response);

      expect(await controller.publicInfo('tok')).toEqual(response);
      expect(mockFilesService.getByToken).toHaveBeenCalledWith('tok');
      expect(mockFilesService.toResponse).toHaveBeenCalledWith(file);
    });
  });

  describe('download()', () => {
    it('streame le fichier avec les bons headers', async () => {
      const file = {
        contentType: 'text/plain',
        originalName: 'test.txt',
        filePath: '/uploads/test.txt',
      };
      mockFilesService.download.mockResolvedValue(file);
      const mockStream = { pipe: jest.fn() };
      (fs.createReadStream as jest.Mock).mockReturnValue(mockStream);

      const res: any = { setHeader: jest.fn() };
      await controller.download('tok', '', res);

      expect(res.setHeader).toHaveBeenCalledWith('Content-Type', 'text/plain');
      expect(res.setHeader).toHaveBeenCalledWith(
        'Content-Disposition',
        'attachment; filename="test.txt"',
      );
      expect(mockStream.pipe).toHaveBeenCalledWith(res);
    });
  });
});
