import { Request, Response } from 'express';
import { drizzle } from 'drizzle-orm/node-postgres';
import { pool } from '../../config/db';
import * as schema from '../../db/schema';
import { desc, eq, and } from 'drizzle-orm';
import { AppError } from '../../utils/AppError';

const db = drizzle(pool, { schema });

interface ListProposalsQuery {
  page?: string;
  limit?: string;
  status?: string;
}

/**
 * List all proposals with cursor-based pagination.
 * 
 * Pagination:
 *  - page: 1-indexed page number (default: 1)
 *  - limit: number of proposals per page (default: 20, max: 100)
 * 
 * Cursor-based approach: we sort by created_at DESC and use offset-limit
 * This is effectively keyset pagination; the cursor is the (id, created_at) pair.
 */
export async function listProposals(req: Request, res: Response) {
  try {
    const query = req.query as ListProposalsQuery;
    const page = Math.max(1, parseInt(query.page || '1', 10));
    const limit = Math.min(100, Math.max(1, parseInt(query.limit || '20', 10)));
    const status = query.status?.toLowerCase();

    // Validate pagination params
    if (isNaN(page) || isNaN(limit)) {
      throw new AppError('Invalid pagination parameters', 400);
    }

    // Build WHERE clause
    const whereConditions: any[] = [];
    if (status && ['active', 'passed', 'failed', 'executed'].includes(status)) {
      whereConditions.push(eq(schema.proposals.status, status));
    }

    // Fetch proposals ordered by creation (newest first)
    const rows = await db
      .select()
      .from(schema.proposals)
      .where(whereConditions.length > 0 ? and(...whereConditions) : undefined)
      .orderBy(desc(schema.proposals.created_at), desc(schema.proposals.id))
      .limit(limit)
      .offset((page - 1) * limit);

    // Get total count for pagination metadata
    const countResult = await db
      .select({ count: schema.proposals.id })
      .from(schema.proposals)
      .where(whereConditions.length > 0 ? and(...whereConditions) : undefined);

    const totalCount = countResult.length;
    const totalPages = Math.ceil(totalCount / limit);

    // Transform rows to match frontend expectations
    const data = rows.map((row: any) => ({
      id: row.proposal_id,
      type: row.type,
      value: row.value,
      description: row.description,
      status: row.status.charAt(0).toUpperCase() + row.status.slice(1), // 'active' -> 'Active'
      proposer: row.proposer,
      votesFor: parseInt(row.votes_for as string, 10),
      votesAgainst: parseInt(row.votes_against as string, 10),
      votesAbstain: parseInt(row.votes_abstain as string, 10),
      createdAt: row.created_at?.toISOString() || '',
      expiresAt: row.expires_at?.toISOString() || '',
    }));

    res.json({
      success: true,
      data,
      pagination: {
        page,
        limit,
        total: totalCount,
        totalPages,
        hasNextPage: page < totalPages,
        hasPrevPage: page > 1,
      },
    });
  } catch (error) {
    if (error instanceof AppError) {
      return res.status(error.statusCode).json({ success: false, error: error.message });
    }
    console.error('Error listing proposals:', error);
    res.status(500).json({ success: false, error: 'Internal server error' });
  }
}

/**
 * Get a single proposal by ID
 */
export async function getProposal(req: Request, res: Response) {
  try {
    const { proposal_id } = req.params;

    const row = await db.select().from(schema.proposals).where(eq(schema.proposals.proposal_id, proposal_id)).limit(1);

    if (row.length === 0) {
      throw new AppError('Proposal not found', 404);
    }

    const p = row[0];
    const data = {
      id: p.proposal_id,
      type: p.type,
      value: p.value,
      description: p.description,
      status: p.status.charAt(0).toUpperCase() + p.status.slice(1),
      proposer: p.proposer,
      votesFor: parseInt(p.votes_for as string, 10),
      votesAgainst: parseInt(p.votes_against as string, 10),
      votesAbstain: parseInt(p.votes_abstain as string, 10),
      createdAt: p.created_at?.toISOString() || '',
      expiresAt: p.expires_at?.toISOString() || '',
    };

    res.json({ success: true, data });
  } catch (error) {
    if (error instanceof AppError) {
      return res.status(error.statusCode).json({ success: false, error: error.message });
    }
    console.error('Error fetching proposal:', error);
    res.status(500).json({ success: false, error: 'Internal server error' });
  }
}

/**
 * Validation middleware for listProposals query parameters
 */
export function listProposalsValidation(req: Request, res: Response, next: Function) {
  try {
    const { page, limit, status } = req.query;

    // Validate types and ranges
    if (page !== undefined) {
      const p = parseInt(page as string, 10);
      if (isNaN(p) || p < 1) {
        throw new AppError('page must be a positive integer', 400);
      }
    }

    if (limit !== undefined) {
      const l = parseInt(limit as string, 10);
      if (isNaN(l) || l < 1 || l > 100) {
        throw new AppError('limit must be between 1 and 100', 400);
      }
    }

    if (status !== undefined) {
      const s = (status as string).toLowerCase();
      if (!['active', 'passed', 'failed', 'executed'].includes(s)) {
        throw new AppError('status must be one of: active, passed, failed, executed', 400);
      }
    }

    next();
  } catch (error) {
    if (error instanceof AppError) {
      return res.status(error.statusCode).json({ success: false, error: error.message });
    }
    res.status(400).json({ success: false, error: 'Invalid query parameters' });
  }
}
