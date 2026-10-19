// backend/src/api/controllers/disputes.controller.ts - Disputes Controller
import { Response } from 'express';
import { pool } from '../../config/db';
import { AuthenticatedRequest } from '../../types/auth.types';
import { logger } from '../../utils/logger';

const COOLDOWN_HOURS = 24;

class DisputesController {

  async submitDispute(req: AuthenticatedRequest, res: Response) {
    try {
      const userId = req.user!.userId;
      const { marketId, reason, evidenceUrl } = req.body;

      const cooldownCheck = await pool.query(
        `SELECT id FROM disputes
         WHERE user_id = $1 AND market_id = $2
         AND raised_at > NOW() - INTERVAL '${COOLDOWN_HOURS} hours'
         LIMIT 1`,
        [userId, marketId],
      );

      if (cooldownCheck.rows.length > 0) {
        return res.status(429).json({
          success: false,
          error: {
            code: 'DISPUTE_COOLDOWN',
            message: `You can only submit one dispute per market every ${COOLDOWN_HOURS} hours`,
          },
        });
      }

      const existingActive = await pool.query(
        `SELECT id FROM disputes WHERE market_id = $1 AND status IN ('open', 'reviewing') LIMIT 1`,
        [marketId],
      );

      if (existingActive.rows.length > 0) {
        return res.status(409).json({
          success: false,
          error: {
            code: 'ACTIVE_DISPUTE_EXISTS',
            message: 'An active dispute already exists for this market',
          },
        });
      }

      const result = await pool.query(
        `INSERT INTO disputes (market_id, user_id, reason, status, raised_at)
         VALUES ($1, $2, $3, 'open', NOW())
         RETURNING *`,
        [marketId, userId, reason],
      );

      return res.status(201).json({
        success: true,
        data: result.rows[0],
      });
    } catch (error) {
      logger.error(error instanceof Error ? error : new Error(String(error)), 'DisputesController.submitDispute');
      return res.status(500).json({ success: false, message: 'Internal server error' });
    }
  }

  async listDisputes(req: AuthenticatedRequest, res: Response) {
    try {
      const status = req.query.status as string | undefined;
      const marketId = req.query.marketId as string | undefined;
      const page = Math.max(1, parseInt(req.query.page as string, 10) || 1);
      const limit = Math.min(100, Math.max(1, parseInt(req.query.limit as string, 10) || 20));
      const offset = (page - 1) * limit;

      let query = `SELECT * FROM disputes WHERE 1=1`;
      const params: unknown[] = [];
      let paramIndex = 1;

      if (status) {
        query += ` AND status = $${paramIndex++}`;
        params.push(status);
      }
      if (marketId) {
        query += ` AND market_id = $${paramIndex++}`;
        params.push(marketId);
      }

      const countResult = await pool.query(
        query.replace('SELECT *', 'SELECT COUNT(*)'),
        params,
      );
      const total = parseInt(countResult.rows[0].count, 10);

      query += ` ORDER BY raised_at DESC LIMIT $${paramIndex++} OFFSET $${paramIndex++}`;
      params.push(limit, offset);

      const result = await pool.query(query, params);

      return res.status(200).json({
        success: true,
        data: {
          disputes: result.rows,
          pagination: {
            page,
            limit,
            total,
            totalPages: Math.ceil(total / limit),
            hasNext: page * limit < total,
            hasPrev: page > 1,
          },
        },
      });
    } catch (error) {
      logger.error(error instanceof Error ? error : new Error(String(error)), 'DisputesController.listDisputes');
      return res.status(500).json({ success: false, message: 'Internal server error' });
    }
  }

  async getDispute(req: AuthenticatedRequest, res: Response) {
    try {
      const { disputeId } = req.params;
      const result = await pool.query(
        `SELECT * FROM disputes WHERE id = $1`,
        [disputeId],
      );

      if (result.rows.length === 0) {
        return res.status(404).json({ success: false, message: 'Dispute not found' });
      }

      return res.status(200).json({ success: true, data: result.rows[0] });
    } catch (error) {
      logger.error(error instanceof Error ? error : new Error(String(error)), 'DisputesController.getDispute');
      return res.status(500).json({ success: false, message: 'Internal server error' });
    }
  }

  async reviewDispute(req: AuthenticatedRequest, res: Response) {
    try {
      const { disputeId } = req.params;
      const { adminNotes } = req.body;

      const result = await pool.query(
        `UPDATE disputes
         SET status = 'reviewing', admin_notes = $1, reviewed_at = NOW()
         WHERE id = $2 AND status = 'open'
         RETURNING *`,
        [adminNotes, disputeId],
      );

      if (result.rows.length === 0) {
        return res.status(404).json({ success: false, message: 'Dispute not found or already reviewed' });
      }

      return res.status(200).json({ success: true, data: result.rows[0] });
    } catch (error) {
      logger.error(error instanceof Error ? error : new Error(String(error)), 'DisputesController.reviewDispute');
      return res.status(500).json({ success: false, message: 'Internal server error' });
    }
  }

  async resolveDispute(req: AuthenticatedRequest, res: Response) {
    try {
      const { disputeId } = req.params;
      const { action, resolution, adminNotes, newWinningOutcome } = req.body;

      const status = action === 'DISMISS' ? 'dismissed' : 'resolved';

      const result = await pool.query(
        `UPDATE disputes
         SET status = $1, final_outcome = $2, admin_notes = COALESCE($3, admin_notes), resolved_at = NOW()
         WHERE id = $4 AND status = 'reviewing'
         RETURNING *`,
        [status, resolution, adminNotes || null, disputeId],
      );

      if (result.rows.length === 0) {
        return res.status(404).json({ success: false, message: 'Dispute not found or not in reviewing status' });
      }

      return res.status(200).json({ success: true, data: result.rows[0] });
    } catch (error) {
      logger.error(error instanceof Error ? error : new Error(String(error)), 'DisputesController.resolveDispute');
      return res.status(500).json({ success: false, message: 'Internal server error' });
    }
  }
}

export const disputesController = new DisputesController();
