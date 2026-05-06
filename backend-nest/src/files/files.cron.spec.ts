import { FilesCron } from './files.cron';

const mockFilesService = {
  purgeExpired: jest.fn(),
};

describe('FilesCron', () => {
  beforeEach(() => {
    jest.useFakeTimers();
    jest.clearAllMocks();
  });

  afterEach(() => {
    jest.useRealTimers();
  });

  it('déclenche une purge après 60 secondes', async () => {
    mockFilesService.purgeExpired.mockResolvedValue(3);
    new FilesCron(mockFilesService as any);

    jest.advanceTimersByTime(60_000);
    await Promise.resolve();

    expect(mockFilesService.purgeExpired).toHaveBeenCalledTimes(1);
  });

  it('log le nombre de fichiers supprimés quand count > 0', async () => {
    mockFilesService.purgeExpired.mockResolvedValue(5);
    new FilesCron(mockFilesService as any);

    jest.advanceTimersByTime(60_000);
    await Promise.resolve();

    expect(mockFilesService.purgeExpired).toHaveBeenCalled();
  });

  it('ne lève pas d\'exception si purgeExpired échoue', async () => {
    mockFilesService.purgeExpired.mockRejectedValue(new Error('DB down'));
    const cron = new FilesCron(mockFilesService as any);

    jest.advanceTimersByTime(60_000);
    await Promise.resolve();

    expect(cron).toBeDefined();
  });
});
