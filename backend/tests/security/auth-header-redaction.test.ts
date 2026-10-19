import type { Request, Response, NextFunction } from 'express';
import { requestLogging } from '../../src/middleware/request-logging.middleware';
import { logger } from '../../src/utils/logger';

jest.mock('../../src/utils/logger');

describe('Authorization Header Redaction (#283)', () => {
  let mockReq: Partial<Request>;
  let mockRes: any;
  let mockNext: NextFunction;

  beforeEach(() => {
    jest.clearAllMocks();
    
    mockReq = {
      ip: '192.168.1.1',
      method: 'GET',
      path: '/api/markets',
      body: {},
      headers: {},
      get: jest.fn().mockReturnValue(undefined),
      socket: { remoteAddress: '192.168.1.1' } as any,
    };

    mockRes = {
      statusCode: 200,
      send: jest.fn(function(data: unknown) { return this; }),
      flushHeaders: jest.fn(),
    };

    mockNext = jest.fn();
  });

  it('should redact Authorization header when logging', () => {
    const token = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...';
    (mockReq as any).get = jest.fn((header: string) => {
      if (header.toLowerCase() === 'authorization') {
        return token;
      }
      return undefined;
    });

    requestLogging(mockReq as Request, mockRes as Response, mockNext);

    // Call the wrapped send function
    const wrappedSend = mockRes.send;
    wrappedSend.call(mockRes, 'response');

    // Check that logger was called with redacted auth header
    const logCall = (logger.info as jest.Mock).mock.calls[0];
    expect(logCall).toBeDefined();
    expect(logCall[0].authorization).toBe('Bearer [REDACTED]');
    expect(logCall[0].authorization).not.toContain(token.split(' ')[1]);
  });

  it('should not include authorization header in log when not present', () => {
    (mockReq as any).get = jest.fn().mockReturnValue(undefined);

    requestLogging(mockReq as Request, mockRes as Response, mockNext);

    // Trigger the wrapped send
    const wrappedSend = mockRes.send;
    wrappedSend.call(mockRes, 'response');

    // Check logger call
    const logCall = (logger.info as jest.Mock).mock.calls[0];
    expect(logCall).toBeDefined();
    // Authorization header should not be in log if not provided
    expect(logCall[0].authorization).toBeUndefined();
  });

  it('should redact any bearer token format', () => {
    const testTokens = [
      'Bearer abc123',
      'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c',
      'Bearer token_with_special_chars!@#$%',
    ];

    testTokens.forEach((token) => {
      jest.clearAllMocks();
      
      (mockReq as any).get = jest.fn((header: string) => {
        if (header.toLowerCase() === 'authorization') {
          return token;
        }
        return undefined;
      });

      mockRes.send = jest.fn(function(data: unknown) { return this; });

      requestLogging(mockReq as Request, mockRes as Response, mockNext);

      const wrappedSend = mockRes.send;
      wrappedSend.call(mockRes, 'response');

      const logCall = (logger.info as jest.Mock).mock.calls[0];
      expect(logCall).toBeDefined();
      expect(logCall[0].authorization).toBe('Bearer [REDACTED]');
    });
  });

  it('should not log request body for sensitive paths', () => {
    mockReq.body = { password: 'secret123' };
    mockReq.path = '/auth/register';

    requestLogging(mockReq as Request, mockRes as Response, mockNext);

    const wrappedSend = mockRes.send;
    wrappedSend.call(mockRes, 'response');

    const logCall = (logger.info as jest.Mock).mock.calls[0];
    expect(logCall).toBeDefined();
    expect(logCall[0].body).toBe('[REDACTED]');
    expect(logCall[0].body).not.toContain('secret123');
  });

  it('should still log redacted auth header on sensitive paths', () => {
    const token = 'Bearer secrettoken123';
    (mockReq as any).get = jest.fn((header: string) => {
      if (header.toLowerCase() === 'authorization') {
        return token;
      }
      return undefined;
    });
    mockReq.body = { password: 'secret123' };
    mockReq.path = '/auth/login';

    requestLogging(mockReq as Request, mockRes as Response, mockNext);

    const wrappedSend = mockRes.send;
    wrappedSend.call(mockRes, 'response');

    const logCall = (logger.info as jest.Mock).mock.calls[0];
    expect(logCall).toBeDefined();
    // Body should be redacted
    expect(logCall[0].body).toBe('[REDACTED]');
    // Auth header should also be redacted
    expect(logCall[0].authorization).toBe('Bearer [REDACTED]');
  });
});
