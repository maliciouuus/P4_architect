import { Test, TestingModule } from '@nestjs/testing';
import { AuthController } from './auth.controller';
import { AuthService } from './auth.service';

const mockAuthService = {
  register: jest.fn(),
  login: jest.fn(),
  getProfile: jest.fn(),
};

describe('AuthController', () => {
  let controller: AuthController;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      controllers: [AuthController],
      providers: [{ provide: AuthService, useValue: mockAuthService }],
    }).compile();

    controller = module.get<AuthController>(AuthController);
    jest.clearAllMocks();
  });

  describe('register()', () => {
    it('délègue au service et retourne le profil créé', async () => {
      const dto = { email: 'a@test.com', username: 'alice', password: 'pass1234' };
      const result = { id: 1, email: 'a@test.com', username: 'alice' };
      mockAuthService.register.mockResolvedValue(result);

      expect(await controller.register(dto)).toEqual(result);
      expect(mockAuthService.register).toHaveBeenCalledWith(dto);
    });
  });

  describe('login()', () => {
    it('délègue au service et retourne le token JWT', async () => {
      const dto = { email: 'a@test.com', password: 'pass1234' };
      const result = { access_token: 'tok', user: { id: 1 } };
      mockAuthService.login.mockResolvedValue(result);

      expect(await controller.login(dto)).toEqual(result);
      expect(mockAuthService.login).toHaveBeenCalledWith(dto);
    });
  });

  describe('me()', () => {
    it('retourne le profil de l\'utilisateur connecté', async () => {
      const profile = { id: 1, email: 'a@test.com', username: 'alice' };
      mockAuthService.getProfile.mockResolvedValue(profile);

      const req = { user: { id: 1 } };
      expect(await controller.me(req)).toEqual(profile);
      expect(mockAuthService.getProfile).toHaveBeenCalledWith(1);
    });
  });
});
