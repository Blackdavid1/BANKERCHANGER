import type { Request, Response, NextFunction } from 'express';
import { errorMiddleware } from '../../src/middleware/error.middleware';
import { AppError } from '../../src/utils/AppError';
import { logger } from '../../src/utils/logger';

jest.mock('../../src/utils/logger');

describe('Error Stack Trace Hiding in Production (#282)', () => {
  let mockReq: Partial<Request>;
  let mockRes: any;
  let mockNext: NextFunction;

  beforeEach(() => {
    jest.clearAllMocks();
    mockReq = {};
    mockRes = {
      status: jest.fn().mockReturnThis(),
      json: jest.fn().mockReturnThis(),
    };
    mockNext = jest.fn();
  });

  describe('Response protection', () => {
    it('should never include stack trace in response body for AppErrors', () => {
      const error = new AppError(500, 'Internal error', 'ERR_INTERNAL');
      errorMiddleware(error, mockReq as Request, mockRes as Response, mockNext);

      const response = (mockRes.json as jest.Mock).mock.calls[0][0];
      expect(response.error).toBeDefined();
      expect(response.error.stack).toBeUndefined();
      expect(response.error.message).toBe('Internal error');
    });

    it('should never include stack trace in response body for generic errors', () => {
      const error = new Error('Database connection failed');
      errorMiddleware(error, mockReq as Request, mockRes as Response, mockNext);

      const response = (mockRes.json as jest.Mock).mock.calls[0][0];
      expect(response.error).toBeDefined();
      expect(response.error.stack).toBeUndefined();
    });

    it('should never include stack trace in response for 5xx errors', () => {
      const error = new AppError(500, 'Internal error', 'ERR_INTERNAL');
      errorMiddleware(error, mockReq as Request, mockRes as Response, mockNext);

      const response = (mockRes.json as jest.Mock).mock.calls[0][0];
      expect(response.error).toBeDefined();
      expect(response.error.stack).toBeUndefined();
    });

    it('should not include stack in response for 4xx errors', () => {
      const error = new AppError(401, 'Unauthorized', 'ERR_UNAUTHORIZED');
      errorMiddleware(error, mockReq as Request, mockRes as Response, mockNext);

      const response = (mockRes.json as jest.Mock).mock.calls[0][0];
      expect(response.error.stack).toBeUndefined();
    });
  });

  describe('Response structure', () => {
    it('should include statusCode in response', () => {
      const error = new AppError(400, 'Bad request', 'ERR_BAD_REQUEST');
      errorMiddleware(error, mockReq as Request, mockRes as Response, mockNext);

      const response = (mockRes.json as jest.Mock).mock.calls[0][0];
      expect(response.error.statusCode).toBe(400);
    });

    it('should include code when provided', () => {
      const error = new AppError(422, 'Validation error', 'ERR_VALIDATION');
      errorMiddleware(error, mockReq as Request, mockRes as Response, mockNext);

      const response = (mockRes.json as jest.Mock).mock.calls[0][0];
      expect(response.error.code).toBe('ERR_VALIDATION');
    });

    it('should include details when provided', () => {
      const details = { field: 'email', reason: 'already exists' };
      const error = new AppError(400, 'Validation failed', 'ERR_VALIDATION', details);
      errorMiddleware(error, mockReq as Request, mockRes as Response, mockNext);

      const response = (mockRes.json as jest.Mock).mock.calls[0][0];
      expect(response.error.details).toEqual(details);
    });

    it('should not include code when not provided', () => {
      const error = new AppError(404, 'Not found');
      errorMiddleware(error, mockReq as Request, mockRes as Response, mockNext);

      const response = (mockRes.json as jest.Mock).mock.calls[0][0];
      expect(response.error.code).toBeUndefined();
    });

    it('should not include empty details', () => {
      const error = new AppError(400, 'Bad request', 'ERR_BAD_REQUEST');
      errorMiddleware(error, mockReq as Request, mockRes as Response, mockNext);

      const response = (mockRes.json as jest.Mock).mock.calls[0][0];
      expect(response.error.details).toBeUndefined();
    });
  });

  describe('Logging behavior', () => {
    it('should not log 404 errors', () => {
      const error = new AppError(404, 'Not found');
      errorMiddleware(error, mockReq as Request, mockRes as Response, mockNext);

      expect(logger.error).not.toHaveBeenCalled();
    });

    it('should not log 400 errors', () => {
      const error = new AppError(400, 'Bad request');
      errorMiddleware(error, mockReq as Request, mockRes as Response, mockNext);

      expect(logger.error).not.toHaveBeenCalled();
    });

    it('should log 5xx errors', () => {
      const error = new AppError(500, 'Internal error', 'ERR_INTERNAL');
      errorMiddleware(error, mockReq as Request, mockRes as Response, mockNext);

      expect(logger.error).toHaveBeenCalled();
    });

    it('should log 503 errors with details', () => {
      const error = new AppError(503, 'Service unavailable', 'ERR_SERVICE', { reason: 'database down' });
      errorMiddleware(error, mockReq as Request, mockRes as Response, mockNext);

      const logCall = (logger.error as jest.Mock).mock.calls[0][0];
      expect(logCall.message).toBe('Service unavailable');
      expect(logCall.statusCode).toBe(503);
      expect(logCall.code).toBe('ERR_SERVICE');
      expect(logCall.details).toEqual({ reason: 'database down' });
    });
  });

  describe('Security: No sensitive data exposure', () => {
    it('should not expose stack traces to client', () => {
      const error = new Error('File not found: /home/user/.ssh/private_key');
      errorMiddleware(error, mockReq as Request, mockRes as Response, mockNext);

      const response = (mockRes.json as jest.Mock).mock.calls[0][0];
      expect(response.error.stack).toBeUndefined();
    });

    it('should maintain security posture for all error types', () => {
      const errors = [
        new AppError(400, 'Validation error'),
        new AppError(500, 'Server error'),
        new Error('Generic error'),
      ];

      errors.forEach((error) => {
        jest.clearAllMocks();
        errorMiddleware(error, mockReq as Request, mockRes as Response, mockNext);
        const response = (mockRes.json as jest.Mock).mock.calls[0][0];
        expect(response.error.stack).toBeUndefined();
      });
    });
  });
});
