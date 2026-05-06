import { JwtStrategy } from './jwt.strategy';

describe('JwtStrategy', () => {
  let strategy: JwtStrategy;

  beforeEach(() => {
    process.env.JWT_SECRET = 'test_secret';
    strategy = new JwtStrategy();
  });

  describe('validate()', () => {
    it('retourne { id, email } depuis le payload JWT', () => {
      const payload = { sub: 42, email: 'user@test.com' };
      expect(strategy.validate(payload)).toEqual({ id: 42, email: 'user@test.com' });
    });

    it('mappe sub vers id', () => {
      const result = strategy.validate({ sub: 99, email: 'x@x.com' });
      expect(result.id).toBe(99);
    });
  });
});
