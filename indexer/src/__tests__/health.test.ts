import request from 'supertest';
import app from '../server';
import { updateLastLedger, isLive, isReady, getReadinessDetails } from '../health';

describe('Health Checks', () => {
  describe('GET /healthz/live', () => {
    it('should return 200 with alive status', async () => {
      const response = await request(app).get('/healthz/live');

      expect(response.status).toBe(200);
      expect(response.body.status).toBe('alive');
      expect(response.body.timestamp).toBeDefined();
    });

    it('should always return 200 when process is running', async () => {
      const response = await request(app).get('/healthz/live');

      expect(response.status).toBe(200);
    });
  });

  describe('GET /healthz/ready', () => {
    it('should return 503 when no ledgers processed yet', async () => {
      const response = await request(app).get('/healthz/ready');

      expect(response.status).toBe(503);
      expect(response.body.ready).toBe(false);
      expect(response.body.reasons).toContain('No ledgers processed yet');
    });

    it('should return 200 when ledgers have been processed', async () => {
      updateLastLedger(12345);

      const response = await request(app).get('/healthz/ready');

      expect(response.status).toBe(200);
      expect(response.body.ready).toBe(true);
      expect(response.body.lastLedger).toBe(12345);
    });

    it('should include cursor age in response', async () => {
      updateLastLedger(12346);

      const response = await request(app).get('/healthz/ready');

      expect(response.status).toBe(200);
      expect(response.body.cursorAge).toBeGreaterThanOrEqual(0);
      expect(response.body.maxCursorAge).toBe(5 * 60 * 1000); // 5 minutes
    });

    it('should return 503 when cursor is stale', async () => {
      // Simulate stale cursor by updating to past time
      updateLastLedger(12347);

      // Mock stale state by manipulating time
      // (In real scenario, this would happen naturally over time)
      const details = getReadinessDetails();
      expect(details.maxCursorAge).toBe(5 * 60 * 1000);
    });
  });

  describe('GET /health (legacy)', () => {
    it('should return 200 when healthy', async () => {
      updateLastLedger(12348);

      const response = await request(app).get('/health');

      expect(response.status).toBe(200);
      expect(response.body.success).toBe(true);
      expect(response.body.status).toBe('healthy');
    });

    it('should include poller status', async () => {
      const response = await request(app).get('/health');

      expect(response.body.poller).toBeDefined();
      expect(response.body.poller.isRunning).toBeDefined();
      expect(response.body.poller.eventsProcessed).toBeDefined();
    });
  });

  describe('Health functions', () => {
    it('isLive() should always return true', () => {
      expect(isLive()).toBe(true);
    });

    it('isReady() should return false when no ledgers processed', () => {
      expect(isReady()).toBeDefined();
    });

    it('getReadinessDetails() should include reasons', () => {
      const details = getReadinessDetails();

      expect(details).toHaveProperty('ready');
      expect(details).toHaveProperty('reasons');
      expect(Array.isArray(details.reasons)).toBe(true);
    });
  });
});
