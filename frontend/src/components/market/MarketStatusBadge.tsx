// ============================================================
// BANKERCHANGER — MarketStatusBadge Component
// ============================================================

import type { MarketStatus } from '../../types';

interface MarketStatusBadgeProps {
  status: MarketStatus;
}

/**
 * Small pill-shaped badge indicating market status.
 *
 * Each status has a distinct colour AND a text label AND a unique icon so
 * that colour-blind users (e.g. red-green) can distinguish them without
 * relying on colour alone (#359).
 *
 * Color mapping:
 *   open       → green   🟢
 *   locked     → amber   🔒
 *   resolved   → blue    ✓
 *   cancelled  → gray    ✕
 *   disputed   → red     ⚠
 */
export function MarketStatusBadge({ status }: MarketStatusBadgeProps): JSX.Element {
  const config: Record<
    typeof status,
    { color: string; icon: string; label: string }
  > = {
    open:      { color: 'bg-green-100 text-green-800', icon: '●', label: 'Open' },
    locked:    { color: 'bg-amber-100 text-amber-800', icon: '🔒', label: 'Locked' },
    resolved:  { color: 'bg-blue-100  text-blue-800',  icon: '✓',  label: 'Resolved' },
    cancelled: { color: 'bg-gray-100  text-gray-800',  icon: '✕',  label: 'Cancelled' },
    disputed:  { color: 'bg-red-100   text-red-800',   icon: '⚠',  label: 'Disputed' },
  };

  const { color, icon, label } = config[status];

  return (
    <span
      className={`inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-medium ${color}`}
      aria-label={`Market status: ${label}`}
    >
      {/* aria-hidden: the text label already conveys the status to screen readers */}
      <span aria-hidden="true">{icon}</span>
      {label}
    </span>
  );
}
