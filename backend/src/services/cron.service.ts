import { pool } from '../config/db';
import { logger } from '../utils/logger';
import {
  cronSessionsDeleted,
  cronResetTokensDeleted,
  cronNotificationsSoftDeleted,
  cronDistributionsArchived,
  cronBlockchainEventsDeleted,
} from './metrics.service';

/** Rows older than this are eligible for cleanup, and only once processed. */
const BLOCKCHAIN_EVENTS_RETENTION_INTERVAL = '90 days';

// ---------------------------------------------------------------------------
// DbAdapter interface — injected in tests, backed by pool in production
// ---------------------------------------------------------------------------

export interface CronDbAdapter {
  deleteExpiredSessions(): Promise<number>;
  deleteExpiredResetTokens(): Promise<number>;
  softDeleteOldNotifications(): Promise<number>;
  archiveFailedDistributions(): Promise<number>;
  writeAuditLog(action: string, details: Record<string, unknown>): Promise<void>;
  /** Optional: not implemented by older adapters/test doubles. */
  countOldBlockchainEvents?(): Promise<number>;
  deleteOldBlockchainEvents?(): Promise<number>;
}

const defaultAdapter: CronDbAdapter = {
  async deleteExpiredSessions() {
    const result = await pool.query(
      `DELETE FROM user_sessions WHERE expires_at < NOW()`,
    );
    return result.rowCount ?? 0;
  },

  async deleteExpiredResetTokens() {
    const result = await pool.query(
      `DELETE FROM password_reset_tokens WHERE expires_at < NOW()`,
    );
    return result.rowCount ?? 0;
  },

  async softDeleteOldNotifications() {
    const result = await pool.query(
      `UPDATE notification_jobs
          SET deleted_at = NOW()
        WHERE deleted_at IS NULL
          AND created_at < NOW() - INTERVAL '90 days'`,
    );
    return result.rowCount ?? 0;
  },

  async archiveFailedDistributions() {
    const result = await pool.query(
      `UPDATE distributions
          SET archived_at = NOW()
        WHERE status = 'failed'
          AND archived_at IS NULL
          AND created_at < NOW() - INTERVAL '30 days'`,
    );
    return result.rowCount ?? 0;
  },

  async writeAuditLog(action: string, details: Record<string, unknown>) {
    await pool.query(
      `INSERT INTO admin_audit_log (action, details) VALUES ($1, $2)`,
      [action, JSON.stringify(details)],
    );
  },

  async countOldBlockchainEvents() {
    const result = await pool.query(
      `SELECT COUNT(*) AS count
         FROM blockchain_events
        WHERE processed = true
          AND created_at < NOW() - INTERVAL '${BLOCKCHAIN_EVENTS_RETENTION_INTERVAL}'`,
    );
    return Number(result.rows[0]?.count ?? 0);
  },

  async deleteOldBlockchainEvents() {
    const result = await pool.query(
      `DELETE FROM blockchain_events
        WHERE processed = true
          AND created_at < NOW() - INTERVAL '${BLOCKCHAIN_EVENTS_RETENTION_INTERVAL}'`,
    );
    return result.rowCount ?? 0;
  },
};

let adapter: CronDbAdapter = defaultAdapter;

export function setDbAdapter(a: CronDbAdapter): void {
  adapter = a;
}

export function getCronAdapter(): CronDbAdapter {
  return adapter;
}

// ---------------------------------------------------------------------------
// Job functions — called by the cron schedule
// ---------------------------------------------------------------------------

export async function deleteExpiredSessions(): Promise<number> {
  const count = await adapter.deleteExpiredSessions();
  cronSessionsDeleted.inc(count);
  await adapter.writeAuditLog('session_cleanup', {
    deleted_sessions: count,
    run_at: new Date().toISOString(),
  });
  return count;
}

export async function deleteExpiredResetTokens(): Promise<number> {
  const count = await adapter.deleteExpiredResetTokens();
  cronResetTokensDeleted.inc(count);
  await adapter.writeAuditLog('session_cleanup', {
    deleted_reset_tokens: count,
    run_at: new Date().toISOString(),
  });
  return count;
}

export async function softDeleteOldNotifications(): Promise<number> {
  const count = await adapter.softDeleteOldNotifications();
  cronNotificationsSoftDeleted.inc(count);
  return count;
}

export async function archiveFailedDistributions(): Promise<number> {
  const count = await adapter.archiveFailedDistributions();
  cronDistributionsArchived.inc(count);
  return count;
}

/**
 * Deletes processed blockchain_events rows older than the retention window.
 * Set DRY_RUN=true to log the count that WOULD be deleted without committing
 * any changes, so an operator can audit the job before it runs for real.
 */
export async function cleanupOldBlockchainEvents(): Promise<number> {
  const dryRun = process.env.DRY_RUN === 'true';

  if (dryRun) {
    const count = (await adapter.countOldBlockchainEvents?.()) ?? 0;
    logger.info({ count, dryRun: true }, 'cleanupOldBlockchainEvents: dry-run, no rows deleted');
    return count;
  }

  const count = (await adapter.deleteOldBlockchainEvents?.()) ?? 0;
  cronBlockchainEventsDeleted.inc(count);
  await adapter.writeAuditLog('blockchain_events_cleanup', {
    deleted_blockchain_events: count,
    run_at: new Date().toISOString(),
  });
  return count;
}
