import type { Request, Response, NextFunction } from 'express';
import jwt from 'jsonwebtoken';
import { AppError } from '../utils/AppError';
import { getEnv } from '../config/env';
import { isSessionRevoked } from '../services/auth.service';

export interface AdminJwtPayload extends jwt.JwtPayload {
  role: 'admin';
}

declare global {
  namespace Express {
    interface Request {
      admin?: AdminJwtPayload;
    }
  }
}

/**
 * Verifies a dedicated admin service JWT signed with ADMIN_JWT_SECRET.
 * Used for service-to-service admin calls that do not carry a user session.
 */
export function requireAdminJwt(req: Request, _res: Response, next: NextFunction): void {
  const authHeader = req.headers.authorization;
  if (!authHeader?.startsWith('Bearer ')) {
    return next(new AppError(401, 'Missing or invalid Authorization header'));
  }

  const token = authHeader.slice(7);
  const env = getEnv();
  const secret = env.ADMIN_JWT_SECRET;

  try {
    const payload = jwt.verify(token, secret) as AdminJwtPayload;
    if (payload.role !== 'admin') {
      return next(new AppError(403, 'Forbidden: admin role required'));
    }
    req.admin = payload;
    next();
  } catch {
    next(new AppError(403, 'Invalid or expired token'));
  }
}

/**
 * Verifies an admin user's access JWT (signed with JWT_ACCESS_SECRET, falling
 * back to JWT_SECRET).
 * Checks token type, admin role, and Redis session revocation tombstone.
 * Used by all admin HTTP routes.
 */
export async function requireAdmin(req: Request, _res: Response, next: NextFunction): Promise<void> {
  try {
    const authHeader = req.headers.authorization;
    if (!authHeader?.startsWith('Bearer ')) {
      throw new AppError(401, 'Missing or invalid Authorization header');
    }

    const token = authHeader.slice(7);
    const { JWT_SECRET, JWT_ACCESS_SECRET } = getEnv();
    const payload = jwt.verify(token, JWT_ACCESS_SECRET || JWT_SECRET) as jwt.JwtPayload;

    if (payload.type !== 'access') {
      throw new AppError(401, 'Invalid token type');
    }

    if (payload.role !== 'admin') {
      throw new AppError(403, 'Forbidden: admin role required');
    }

    const userId = payload.sub as string;
    const sessionVersion: number = payload.sv ?? 0;

    const revoked = await isSessionRevoked(userId, sessionVersion);
    if (revoked) throw new AppError(401, 'Session has been invalidated');

    (req as unknown as Record<string, unknown>).userId = userId;
    (req as unknown as Record<string, unknown>).sessionVersion = sessionVersion;
    next();
  } catch (err) {
    next(err instanceof AppError ? err : new AppError(401, 'Invalid or expired token'));
  }
}
