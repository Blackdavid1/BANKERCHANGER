// ============================================================
// BANKERCHANGER — OracleReport Database Model
// ============================================================

export interface OracleReport {
  id: number;
  match_id: string;
  oracle_address: string;
  outcome: string;
  reported_at: Date;
  /** Hex-encoded Ed25519 signature */
  signature: string;
  /** True if this report was used to resolve the market on-chain */
  accepted: boolean;
  /** Null if submission failed before reaching the network */
  tx_hash: string | null;
  created_at: Date;
}
