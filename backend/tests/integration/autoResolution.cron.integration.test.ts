import cron from 'node-cron';

// Mocks must be set up before importing the module under test
jest.mock('../../src/oracle/OracleService', () => ({
  runAutoResolutionJob: jest.fn(),
  runAutoLockMarketsJob: jest.fn(),
}));

jest.mock('../../src/utils/logger', () => ({
  logger: {
    debug: jest.fn(),
    info: jest.fn(),
    warn: jest.fn(),
    error: jest.fn(),
  },
}));

import { runAutoResolutionJob } from '../../src/oracle/OracleService';
import { startAutoResolutionCron } from '../../src/cron/autoResolution.cron';
import { logger } from '../../src/utils/logger';

describe('autoResolution.cron integration', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    jest.restoreAllMocks();
    // Ensure env var is not set to disabled
    delete process.env.AUTO_RESOLUTION_CRON_DISABLED;
  });

  describe('startAutoResolutionCron', () => {
    it('should schedule a cron job with the correct expression and invoke runAutoResolutionJob', async () => {
      const scheduleSpy = jest.spyOn(cron, 'schedule');
      (runAutoResolutionJob as jest.Mock).mockResolvedValue({ processed: 2, resolved: 1 });

      startAutoResolutionCron();

      // Verify cron was scheduled
      expect(scheduleSpy).toHaveBeenCalledTimes(1);
      const [expression, callback] = scheduleSpy.mock.calls[0];
      expect(expression).toBe('*/10 * * * *');
      expect(typeof callback).toBe('function');

      // Manually invoke the callback to simulate cron firing
      await (callback as () => Promise<void>)();

      // Assert the job ran and logged completion
      expect(runAutoResolutionJob).toHaveBeenCalledTimes(1);
      expect(logger.info).toHaveBeenCalledWith(
        { processed: 2, resolved: 1 },
        'autoResolutionJob: completed',
      );
    });

    it('should skip execution when previous run is still in progress', async () => {
      const scheduleSpy = jest.spyOn(cron, 'schedule');
      let resolveJob!: () => void;
      (runAutoResolutionJob as jest.Mock).mockImplementation(
        () => new Promise<void>((resolve) => { resolveJob = resolve; }),
      );

      startAutoResolutionCron();
      const [, callback] = scheduleSpy.mock.calls[0];

      // Fire first invocation (starts running but doesn't complete)
      const firstRun = (callback as () => Promise<void>)();

      // Fire second invocation while first is still running
      await (callback as () => Promise<void>)();

      // Should have warned about skipping
      expect(logger.warn).toHaveBeenCalledWith(
        'autoResolutionJob: previous run still in progress, skipping',
      );
      // Job should only have been called once
      expect(runAutoResolutionJob).toHaveBeenCalledTimes(1);

      // Clean up: resolve the first run so the promise settles
      resolveJob();
      await firstRun;
    });

    it('should handle fatal errors gracefully and reset the running flag', async () => {
      const scheduleSpy = jest.spyOn(cron, 'schedule');
      const fatalError = new Error('DB unavailable');
      (runAutoResolutionJob as jest.Mock).mockRejectedValueOnce(fatalError);

      startAutoResolutionCron();
      const [, callback] = scheduleSpy.mock.calls[0];

      // Invoke once — should catch the fatal error
      await (callback as () => Promise<void>)();

      expect(logger.error).toHaveBeenCalledWith(
        { err: fatalError },
        'autoResolutionJob: fatal error, batch aborted',
      );

      // Reset mock and invoke again — should run since the flag was reset
      (runAutoResolutionJob as jest.Mock).mockResolvedValueOnce({ processed: 0, resolved: 0 });
      await (callback as () => Promise<void>)();

      expect(runAutoResolutionJob).toHaveBeenCalledTimes(2);
    });

    it('should not schedule when AUTO_RESOLUTION_CRON_DISABLED is true', () => {
      process.env.AUTO_RESOLUTION_CRON_DISABLED = 'true';
      const scheduleSpy = jest.spyOn(cron, 'schedule');

      startAutoResolutionCron();

      expect(scheduleSpy).not.toHaveBeenCalled();
      expect(logger.info).toHaveBeenCalledWith(
        'Auto-resolution cron job is disabled via AUTO_RESOLUTION_CRON_DISABLED',
      );
    });
  });

  describe('node-cron schedule API with 1-second interval', () => {
    beforeEach(() => {
      jest.useFakeTimers();
    });

    afterEach(() => {
      jest.useRealTimers();
    });

    it('should fire and complete within a one-second interval', async () => {
      (runAutoResolutionJob as jest.Mock).mockResolvedValue({ processed: 1, resolved: 1 });

      let jobRunCount = 0;

      // Schedule using node-cron's API with a 1-second interval
      const scheduledTask = cron.schedule('* * * * * *', async () => {
        jobRunCount++;
        await runAutoResolutionJob();
      });

      expect(scheduledTask).toBeDefined();

      // Advance time by 1 second to trigger the cron
      jest.advanceTimersByTime(1000);

      // Allow pending microtasks to flush
      await Promise.resolve();

      // Verify the job was invoked at least once
      expect(jobRunCount).toBeGreaterThanOrEqual(1);
      expect(runAutoResolutionJob).toHaveBeenCalled();

      // Clean up the scheduled task
      scheduledTask.stop();
    });
  });
});
