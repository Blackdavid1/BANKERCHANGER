// ============================================================
// BANKERCHANGER — BlockchainEvent Database Model
// Raw events ingested by the indexer before processing.
// ============================================================

export interface BlockchainEvent {
  id: number;
  contract_address: string;
  /** e.g. "BetPlaced", "MarketResolved", "WinningsClaimed" */
  event_type: string;
  /** Fully deserialized event payload */
  payload: Record<string, unknown>;
  ledger_sequence: number;
  ledger_close_time: Date;
  tx_hash: string;
  processed: boolean;
  created_at: Date;
}

export interface IndexerCheckpoint {
  id: number;
  last_processed_ledger: number;
  updated_at: Date;
}
