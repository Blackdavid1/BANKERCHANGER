#!/usr/bin/env python3
"""
Script to create labels and push 125 comprehensive issues to doradenise-jpg/BANKERCHANGER GitHub repository.
Covers all repository components: Smart Contracts, Backend API, Database, Indexer, Frontend, and DevOps/CI.
Note: 'Stellar Wave' label is intentionally omitted to avoid automated Drips Wave point assignment.
"""

import os
import sys
import json
import subprocess
import time

REPO = "doradenise-jpg/BANKERCHANGER"

# Comprehensive labels required for the 125 issues
LABELS = [
    {"name": "bug", "color": "ee0701", "description": "Bug fix"},
    {"name": "enhancement", "color": "a2eeef", "description": "New feature or request"},
    {"name": "security", "color": "ee0701", "description": "Security-critical"},
    {"name": "testing", "color": "0075ca", "description": "Test coverage"},
    {"name": "devops", "color": "fbca04", "description": "Docker, CI/CD, and deployment"},
    {"name": "contracts", "color": "0e8a16", "description": "Soroban smart contracts layer"},
    {"name": "backend", "color": "0075ca", "description": "Backend / API work"},
    {"name": "frontend", "color": "1d76db", "description": "Frontend Next.js application"},
    {"name": "indexer", "color": "5319e7", "description": "Blockchain event indexer"},
    {"name": "database", "color": "bfd4f2", "description": "Database schema and migrations"},
    {"name": "oracle", "color": "5319e7", "description": "Oracle integration"},
    {"name": "markets", "color": "e4e669", "description": "Market discovery and lifecycle"},
    {"name": "trading", "color": "f9d0c4", "description": "Trading, betting, and AMM pools"},
    {"name": "wallet", "color": "006b75", "description": "Wallet & balance management"},
    {"name": "treasury", "color": "0e8a16", "description": "Treasury operations"},
    {"name": "auth", "color": "ee0701", "description": "Authentication & authorization"},
    {"name": "disputes", "color": "b60205", "description": "Dispute resolution"},
    {"name": "notifications", "color": "fbca04", "description": "Notification system"},
    {"name": "leaderboard", "color": "1d76db", "description": "Leaderboard & rankings"},
    {"name": "users", "color": "bfd4f2", "description": "User profile & management"},
    {"name": "referrals", "color": "d93f0b", "description": "Referral system"},
    {"name": "achievements", "color": "0075ca", "description": "Achievement & reward system"},
    {"name": "websocket", "color": "5319e7", "description": "Real-time WebSocket layer"},
    {"name": "middleware", "color": "e4e669", "description": "Express middleware"},
    {"name": "blockchain", "color": "0e8a16", "description": "Stellar / Soroban blockchain layer"},
    {"name": "cron", "color": "fbca04", "description": "Scheduled / background jobs"},
    {"name": "repository", "color": "bfd4f2", "description": "Data access layer"},
    {"name": "performance", "color": "d4c5f9", "description": "Performance and optimization"},
    {"name": "observability", "color": "0052cc", "description": "Logging and metrics"},
    {"name": "reliability", "color": "c2e0c6", "description": "Fault tolerance and resilience"},
    {"name": "refactor", "color": "d4c5f9", "description": "Code cleanup and refactoring"},
    {"name": "critical", "color": "b60205", "description": "Critical blocker"},
    {"name": "ux", "color": "fef2c0", "description": "User experience"},
    {"name": "accessibility", "color": "0075ca", "description": "A11y improvements"},
    {"name": "seo", "color": "bfdadc", "description": "Search engine optimization"},
    {"name": "ci-cd", "color": "fbca04", "description": "Continuous integration & deployment"},
    {"name": "tech-debt", "color": "e99695", "description": "Technical debt resolution"},
    {"name": "devex", "color": "7057ff", "description": "Developer experience"},
    {"name": "docs", "color": "0075ca", "description": "Documentation"},
    {"name": "portfolio", "color": "006b75", "description": "User portfolio management"},
    {"name": "hooks", "color": "1d76db", "description": "React custom hooks"},
    {"name": "architecture", "color": "5319e7", "description": "System architecture"}
]

ISSUES = [
    {
        "num": 1,
        "title": "#1 \u2014 contracts/Cargo.toml Includes shared/fuzz in Default Workspace Causing Build Failures",
        "body": "**Labels:** `bug` `contracts` `devops`\n\n## Description\n`contracts/Cargo.toml` lists `shared/fuzz` inside `[workspace] members`. Because `shared/fuzz` depends on `libfuzzer-sys`, running standard cargo workspace commands like `cargo test --all` or `cargo check --workspace` fails on systems without cargo-fuzz installed or without a nightly sanitizer toolchain. The fuzz crate should either be excluded from the default members or placed behind a dedicated workspace profile.\n\n## Complexity\n**Medium**\n\n## Acceptance Criteria\n- [ ] Exclude `shared/fuzz` from the default `members` list in `contracts/Cargo.toml` or configure `default-members`\n- [ ] Ensure `cargo check --workspace` and `cargo test --workspace` pass out of the box on stable Rust\n- [ ] Update `.github/workflows/contracts-ci.yml` fuzz job to explicitly pass `--manifest-path shared/fuzz/Cargo.toml`\n- [ ] Document fuzz testing invocation instructions in `contracts/README.md`",
        "labels": [
            "bug",
            "contracts",
            "devops"
        ]
    },
    {
        "num": 2,
        "title": "#2 \u2014 Market Contract Integration Tests Lack TreasuryClient Dependency Feature Flag",
        "body": "**Labels:** `bug` `contracts` `testing`\n\n## Description\nIn `contracts/market/Cargo.toml`, `boxmeout-treasury = { path = \"../treasury\" }` is declared under `[dev-dependencies]` without `features = [\"testutils\"]`. During integration tests in `contracts/market/tests/integration_tests.rs`, attempting to instantiate or interact with `TreasuryClient` fails to compile because client code generation requires the `testutils` feature.\n\n## Complexity\n**Medium**\n\n## Acceptance Criteria\n- [ ] Add `features = [\"testutils\"]` to `boxmeout-treasury` dev-dependency in `contracts/market/Cargo.toml`\n- [ ] Verify `cargo test -p boxmeout-market --test integration_tests` compiles and runs successfully\n- [ ] Add a cross-contract test verifying market fee deposits into treasury contract mock\n- [ ] Ensure no circular feature dependency warnings between market and treasury crates",
        "labels": [
            "bug",
            "contracts",
            "testing"
        ]
    },
    {
        "num": 3,
        "title": "#3 \u2014 Market Factory Does Not Clean Up Storage Upon Emergency Market Cancellation",
        "body": "**Labels:** `enhancement` `contracts` `markets`\n\n## Description\nWhen an admin or emergency guardian cancels a market in `contracts/market_factory/src/lib.rs`, the factory contract marks the market status as cancelled but leaves its address in `OPEN_MARKETS` set and persistent storage without state pruning. As a result, indexers and frontend discovery endpoints continue to query the cancelled market contract as if active.\n\n## Complexity\n**High**\n\n## Acceptance Criteria\n- [ ] Implement `remove_open_market` helper in `MarketFactory` to remove cancelled market from active storage set\n- [ ] Emit `MarketCancelled(market_id, reason)` contract event with cancellation timestamp\n- [ ] Add test case in `contracts/market_factory` verifying cancelled market is excluded from active markets query\n- [ ] Verify storage rent overhead is minimized after cancellation",
        "labels": [
            "enhancement",
            "contracts",
            "markets"
        ]
    },
    {
        "num": 4,
        "title": "#4 \u2014 Market Contract State Rent Extension Not Invoked During Claim Window",
        "body": "**Labels:** `bug` `contracts` `blockchain`\n\n## Description\nIn `contracts/market/src/lib.rs`, the constant `CLAIM_WINDOW_LEDGERS = 2_000_000` is defined for extending state rent for winning position holders, but the `claim_winnings` execution path fails to call `env.storage().persistent().extend_ttl()` on the bettor's balance entry before verifying claims. On long-running markets, persistent storage records risk archival before late claimants redeem their payouts.\n\n## Complexity\n**High**\n\n## Acceptance Criteria\n- [ ] Invoke `extend_ttl` on persistent storage keys for `BET_PREFIX` and `STATE` in `claim_winnings` and `place_bet`\n- [ ] Ensure TTL is extended to at least `CLAIM_WINDOW_LEDGERS` when a market resolves\n- [ ] Add integration test simulating ledger threshold progression to verify TTL extension behavior\n- [ ] Audit all persistent storage keys in `market/src/lib.rs` for proper TTL extension coverage",
        "labels": [
            "bug",
            "contracts",
            "blockchain"
        ]
    },
    {
        "num": 5,
        "title": "#5 \u2014 Shared AMM Integer Division Truncation in calculate_buy_amount Under Asymmetric Pools",
        "body": "**Labels:** `bug` `contracts` `trading`\n\n## Description\nIn `contracts/shared/src/amm.rs`, `calculate_buy_amount` calculates returned shares using integer division. When liquidity pools are heavily unbalanced (e.g. 100:1 ratio between fighter A and fighter B), small bet amounts truncate down to zero shares due to intermediate division before scale multiplication. Users lose their deposited stroops without receiving any pool shares.\n\n## Complexity\n**High**\n\n## Acceptance Criteria\n- [ ] Reorder arithmetic operations to multiply by precision factor (10^7) before division in `calculate_buy_amount`\n- [ ] Add guard returning `Err(ContractError::ZeroSharesAllocated)` if calculated share count is zero\n- [ ] Add property-based test with `proptest` testing asymmetric pool ratios from 1:1 up to 1000:1\n- [ ] Verify all existing AMM unit tests continue to pass with zero precision regression",
        "labels": [
            "bug",
            "contracts",
            "trading"
        ]
    },
    {
        "num": 6,
        "title": "#6 \u2014 Market Factory Allows Non-Admin Caller to Trigger WASM Hash Replacement Under Race Condition",
        "body": "**Labels:** `security` `contracts` `blockchain`\n\n## Description\nIn `contracts/market_factory/src/lib.rs`, the function updating `MARKET_WASM_HASH` checks `require_admin`, but the check occurs after reading existing hash from storage rather than as the immediate first statement. In addition, missing reentrancy protection on administrative calls creates potential upgrade vulnerabilities under concurrent execution.\n\n## Complexity\n**High**\n\n## Acceptance Criteria\n- [ ] Enforce `caller.require_auth()` and `require_admin` at the very beginning of `set_market_wasm_hash`\n- [ ] Validate that the provided `new_wasm_hash` is 32 bytes and non-zero\n- [ ] Emit `MarketWasmHashUpdated(old_hash, new_hash, admin)` audit event\n- [ ] Add test verifying non-admin address gets `ContractError::NotAdmin` and state remains unchanged",
        "labels": [
            "security",
            "contracts",
            "blockchain"
        ]
    },
    {
        "num": 7,
        "title": "#7 \u2014 Treasury Daily Withdrawal Counter Does Not Prune Obsolete Daily Buckets",
        "body": "**Labels:** `bug` `contracts` `treasury`\n\n## Description\nIn `contracts/treasury/src/lib.rs`, `record_token_withdrawal` collects expired day bucket keys into a `stale: Vec<u64>` vector (lines 117-120), but the vector is never iterated over to actually delete the stale keys from the persistent map `daily`. Over months of operation, obsolete ledger days accumulate indefinitely in contract storage.\n\n## Complexity\n**Medium**\n\n## Acceptance Criteria\n- [ ] Iterate through `stale` keys and call `daily.remove(k)` to delete expired day buckets from persistent storage\n- [ ] Cap the maximum stale keys pruned per transaction to avoid hitting CPU instruction limits\n- [ ] Write a unit test simulating 10 consecutive daily withdrawals and verify only active buckets are retained\n- [ ] Verify gas consumption remains constant over time",
        "labels": [
            "bug",
            "contracts",
            "treasury"
        ]
    },
    {
        "num": 8,
        "title": "#8 \u2014 Market Contract Dispute Cooldown Ledger Calculation Uses Inconsistent Block Time Assumption",
        "body": "**Labels:** `bug` `contracts` `disputes`\n\n## Description\nIn `contracts/market/src/lib.rs`, `DEFAULT_DISPUTE_COOLDOWN_LEDGERS` is hardcoded to 720 ledgers based on an assumption of exactly 5 seconds per ledger (1 hour). On Stellar network fluctuations where ledger close times range between 3.5s and 6s, the dispute window can expire prematurely or remain open too long. The cooldown should use timestamp-based comparison or allow factory configuration.\n\n## Complexity\n**Medium**\n\n## Acceptance Criteria\n- [ ] Support configuring dispute cooldown in seconds alongside ledger counts in `MarketConfig`\n- [ ] Verify cooldown expiration against `env.ledger().timestamp()` in addition to ledger sequence\n- [ ] Add test verifying dispute window remains locked until both time and ledger requirements are met\n- [ ] Document dispute timing rules in `docs/architecture.md`",
        "labels": [
            "bug",
            "contracts",
            "disputes"
        ]
    },
    {
        "num": 9,
        "title": "#9 \u2014 Market Contract Claim Winnings Lacks Idempotency Check When Shares Equal Zero",
        "body": "**Labels:** `enhancement` `contracts` `trading`\n\n## Description\nIn `contracts/market/src/lib.rs`, calling `claim_winnings` for an account that already claimed or never held winning shares iterates through position records and invokes token transfer with an amount of 0 stroops. This emits empty transfer events and wastes transaction fees.\n\n## Complexity\n**Low**\n\n## Acceptance Criteria\n- [ ] Check total calculated payout before token transfer; return `Err(ContractError::NoWinningsToClaim)` if zero\n- [ ] Ensure bets are marked as claimed in storage before external token transfer (CEI pattern)\n- [ ] Emit `WinningsClaimed(bettor, market_id, payout)` event only on positive payout\n- [ ] Add unit test verifying zero-balance claim reverts cleanly",
        "labels": [
            "enhancement",
            "contracts",
            "trading"
        ]
    },
    {
        "num": 10,
        "title": "#10 \u2014 Shared Event Parser Fails on Missing Optional Outcome in Oracle Consensus Event",
        "body": "**Labels:** `bug` `contracts` `oracle`\n\n## Description\nIn `contracts/shared/src/event_parser.rs`, parsing `MarketResolved` events unwrap the `winning_outcome` directly without handling `OptionalOutcome::None`. In scenarios where a match is declared a No-Contest or Cancelled without a winner, the parser panics, preventing downstream indexers and contracts from processing resolution data.\n\n## Complexity\n**Medium**\n\n## Acceptance Criteria\n- [ ] Handle `OptionalOutcome::None` and `Outcome::NoContest` cleanly in `event_parser.rs`\n- [ ] Return a structured `ParsedResolution` enum representing all valid terminal match states\n- [ ] Add test vectors covering FighterA, FighterB, Draw, NoContest, and Void states\n- [ ] Ensure zero unwrap panics across the event parser module",
        "labels": [
            "bug",
            "contracts",
            "oracle"
        ]
    },
    {
        "num": 11,
        "title": "#11 \u2014 Treasury Fee Lock Does Not Revert When Cross-Contract Transfer Panics",
        "body": "**Labels:** `security` `contracts` `treasury`\n\n## Description\nIn `contracts/treasury/src/lib.rs`, `acquire_fee_lock` sets `FEE_LOCK = true` in storage. If the token contract transfer reverts or runs out of gas mid-execution, the persistent lock flag might not be cleared if trapped, causing subsequent legitimate treasury withdrawals to fail with `ContractError::ReentrancyGuard`.\n\n## Complexity\n**High**\n\n## Acceptance Criteria\n- [ ] Utilize Soroban's transient storage or ensure state rollback on cross-contract call failure\n- [ ] Add an emergency admin unlock function `force_release_fee_lock` protected by timelock and admin auth\n- [ ] Write a test triggering a simulated token contract failure and verify reentrancy lock state\n- [ ] Add audit logging in `AUDIT_LOG` whenever fee lock state is forcibly cleared",
        "labels": [
            "security",
            "contracts",
            "treasury"
        ]
    },
    {
        "num": 12,
        "title": "#12 \u2014 Market Factory get_markets Pagination Does Not Cap Upper Limit Resulting in Gas Exhaustion",
        "body": "**Labels:** `bug` `contracts` `performance`\n\n## Description\nIn `contracts/market_factory/src/lib.rs`, the `list_markets` query function accepts `offset` and `limit` parameters but does not enforce a maximum ceiling on `limit`. Calling with `limit = 1000` causes cross-contract calls to each market contract within the loop, exceeding Soroban's CPU instruction and memory budget.\n\n## Complexity\n**Medium**\n\n## Acceptance Criteria\n- [ ] Enforce `MAX_PAGE_LIMIT = 50` on `limit` argument in `list_markets`\n- [ ] Default `limit` to 20 if zero or negative is provided\n- [ ] Return pagination metadata `{ total, offset, limit }` alongside market vector\n- [ ] Add test verifying `limit > 50` is automatically clamped to 50 without error",
        "labels": [
            "bug",
            "contracts",
            "performance"
        ]
    },
    {
        "num": 13,
        "title": "#13 \u2014 Market Contract Disallow Draw Outcome Edge Case When Bets Placed on Draw",
        "body": "**Labels:** `bug` `contracts` `markets`\n\n## Description\nIn `contracts/market/src/lib.rs`, the `ALLOW_DRAW` storage setting determines whether a draw outcome can be selected. If an admin initializes a market with draw enabled and bettors deposit funds into the draw pool, but an administrative update toggles `ALLOW_DRAW` to false, draw pool funds become permanently locked upon resolution.\n\n## Complexity\n**High**\n\n## Acceptance Criteria\n- [ ] Disallow modifying `ALLOW_DRAW` once any bets have been placed in the market\n- [ ] In resolution logic, if draw was disabled but outcome is draw, automatically trigger market refund\n- [ ] Add test case verifying `toggle_allow_draw` fails with `ContractError::BetsAlreadyPlaced` if pool > 0\n- [ ] Verify all pool balances can be claimed or refunded under draw resolution",
        "labels": [
            "bug",
            "contracts",
            "markets"
        ]
    },
    {
        "num": 14,
        "title": "#14 \u2014 Market Factory Duplicate Fighter Name Validation Allows Leading/Trailing Whitespace Bypass",
        "body": "**Labels:** `bug` `contracts` `markets`\n\n## Description\nIn `contracts/market_factory/src/lib.rs`, the validation preventing identical fighter names (`fighter_a == fighter_b`) does not normalize or trim whitespace. A creator can pass `\"Canelo \"` and `\"Canelo\"`, bypassing validation and creating a broken market where both sides represent the same fighter.\n\n## Complexity\n**Low**\n\n## Acceptance Criteria\n- [ ] Trim and normalize whitespace on fighter names before comparison\n- [ ] Reject names with length less than 2 characters after trimming\n- [ ] Add test verifying creation fails when names differ only by leading/trailing whitespace\n- [ ] Return `ContractError::InvalidFighterNames` on duplicate names",
        "labels": [
            "bug",
            "contracts",
            "markets"
        ]
    },
    {
        "num": 15,
        "title": "#15 \u2014 Treasury Fee Distribution Splits Do Not Validate Sum Equals 10000 BPS",
        "body": "**Labels:** `bug` `contracts` `treasury`\n\n## Description\nIn `contracts/treasury/src/lib.rs`, `set_fee_tiers` receives a list of `FeeTier` records with basis points allocation. The contract does not validate that the sum of split basis points equals exactly 10,000 (100%). If configured with >10,000 bps, fee distribution over-distributes funds, draining treasury reserves.\n\n## Complexity\n**High**\n\n## Acceptance Criteria\n- [ ] Add validation in `set_fee_tiers` ensuring sum of `bps` equals exactly 10,000\n- [ ] Reject configurations with duplicate recipient addresses in the same tier list\n- [ ] Add test verifying configuration with 10,001 bps reverts with `ContractError::InvalidFeeSplit`\n- [ ] Add test verifying valid 10,000 bps configuration applies cleanly",
        "labels": [
            "bug",
            "contracts",
            "treasury"
        ]
    },
    {
        "num": 16,
        "title": "#16 \u2014 Shared Types Lack Serialization Attributes for Contract Client Integration Tests",
        "body": "**Labels:** `bug` `contracts` `testing`\n\n## Description\nIn `contracts/shared/src/types.rs`, several structs and enums like `FightDetails` and `MarketConfig` are missing `#[derive(serde::Serialize, serde::Deserialize)]` or `#[cfg_attr(test, derive(Debug, PartialEq))]`. When writing external Rust integration tests with `soroban-sdk::Env`, asserting equality on these types requires manual field-by-field matching.\n\n## Complexity\n**Medium**\n\n## Acceptance Criteria\n- [ ] Add `#[derive(Clone, Debug, Eq, PartialEq)]` to all shared structs and enums in `types.rs`\n- [ ] Ensure no std dependencies are introduced into no_std release wasm builds\n- [ ] Verify all test files can use `assert_eq!` directly on shared types\n- [ ] Ensure wasm binary sizes remain unchanged after adding test derivations",
        "labels": [
            "bug",
            "contracts",
            "testing"
        ]
    },
    {
        "num": 17,
        "title": "#17 \u2014 Market Contract Expiry Grace Period Calculation Allows Premature Refund Requests",
        "body": "**Labels:** `bug` `contracts` `markets`\n\n## Description\nIn `contracts/market/src/lib.rs`, `refund_expired` compares `env.ledger().timestamp()` against `fight.scheduled_at + EXPIRY_GRACE_PERIOD`. However, if the fight was locked by admin but not yet resolved, the function does not check whether oracle resolution is actively pending in cooldown, enabling users to cancel an in-flight fight result.\n\n## Complexity\n**Medium**\n\n## Acceptance Criteria\n- [ ] Check that market status is not `ResolutionPending` before executing `refund_expired`\n- [ ] Ensure `refund_expired` only triggers if status is `Open` or `Locked` past the grace period\n- [ ] Emit `MarketExpiredRefunded(market_id, total_refunded)` event upon successful execution\n- [ ] Add test verifying refund is blocked when oracle consensus report is under dispute cooldown",
        "labels": [
            "bug",
            "contracts",
            "markets"
        ]
    },
    {
        "num": 18,
        "title": "#18 \u2014 Market Contract Seed Liquidity Deposit Does Not Check Caller Token Balance Before Reserve Transfer",
        "body": "**Labels:** `bug` `contracts` `trading`\n\n## Description\nIn `contracts/market/src/lib.rs`, when `initialize` or `deposit_seed_liquidity` is called, the contract initiates a token transfer from caller to market contract without verifying that caller balance is at least `MIN_SEED_LIQUIDITY` (10 XLM in stroops). If balance is insufficient, the transaction fails with opaque token error rather than informative `ContractError`.\n\n## Complexity\n**Low**\n\n## Acceptance Criteria\n- [ ] Query token client balance of creator before initiating seed transfer\n- [ ] Return `ContractError::InsufficientSeedLiquidity` if balance is below required minimum\n- [ ] Add test case testing market creation with zero token balance\n- [ ] Verify clear error message is returned in test environment",
        "labels": [
            "bug",
            "contracts",
            "trading"
        ]
    },
    {
        "num": 19,
        "title": "#19 \u2014 Market Factory Missing Event Emission on Admin Timelock Update",
        "body": "**Labels:** `enhancement` `contracts` `observability`\n\n## Description\nIn `contracts/market_factory/src/lib.rs`, functions `set_admin_timelock` and `propose_admin` update sensitive governance parameters in persistent storage without emitting structured Soroban contract events. Indexers and audit systems cannot detect administrative parameter updates without polling full storage.\n\n## Complexity\n**Low**\n\n## Acceptance Criteria\n- [ ] Emit `AdminTimelockUpdated(old_timelock, new_timelock)` event in `set_admin_timelock`\n- [ ] Emit `AdminTransferProposed(current_admin, pending_admin, unlock_time)` event in `propose_admin`\n- [ ] Emit `AdminTransferAccepted(old_admin, new_admin)` event in `accept_admin`\n- [ ] Add tests verifying event topics and payloads match indexer expectations",
        "labels": [
            "enhancement",
            "contracts",
            "observability"
        ]
    },
    {
        "num": 20,
        "title": "#20 \u2014 Treasury Contract Minimum Reserve Check Allows Partial Drain Under High Concurrency",
        "body": "**Labels:** `security` `contracts` `treasury`\n\n## Description\nIn `contracts/treasury/src/lib.rs`, the minimum reserve enforcement (`DEFAULT_MINIMUM_RESERVE = 100 XLM`) calculates available balance as `token_balance - amount`. In concurrent transactions, balance reading before state update can allow two parallel withdrawals to both pass validation, leaving treasury balance below the reserve floor.\n\n## Complexity\n**High**\n\n## Acceptance Criteria\n- [ ] Enforce atomic check-and-subtract on reserved treasury balances\n- [ ] Strictly check `current_balance - amount >= MINIMUM_RESERVE` with reentrancy fee lock held\n- [ ] Return `ContractError::ReserveFloorBreached` if post-withdrawal balance drops below floor\n- [ ] Add concurrent simulation test verifying reserve floor is never breached",
        "labels": [
            "security",
            "contracts",
            "treasury"
        ]
    },
    {
        "num": 21,
        "title": "#21 \u2014 Shared Math Safe Multiply-Divide Overflow Check Skips 256-bit Intermediate Precision",
        "body": "**Labels:** `bug` `contracts` `trading`\n\n## Description\nIn `contracts/shared/src/math.rs`, `mul_div` computes `(a * b) / c` using standard 128-bit integers. When total betting volume exceeds 18 million XLM (in stroops: 1.8e14), `a * b` exceeds `i128::MAX` (1.7e38) during fee exponentiation, causing contract panic. Using 256-bit intermediate integers prevents unexpected integer overflows.\n\n## Complexity\n**High**\n\n## Acceptance Criteria\n- [ ] Implement safe 256-bit intermediate multiplication using `U256` or double-word arithmetic in `mul_div`\n- [ ] Return `ContractError::MathOverflow` instead of panicking on values exceeding max bounds\n- [ ] Add unit tests with inputs near `i128::MAX` to verify overflow safety\n- [ ] Benchmark gas cost impact to verify zero performance degradation",
        "labels": [
            "bug",
            "contracts",
            "trading"
        ]
    },
    {
        "num": 22,
        "title": "#22 \u2014 Market Contract Oracle Report TTL Expiration Does Not Clean Up Stale Pending Reports",
        "body": "**Labels:** `enhancement` `contracts` `oracle`\n\n## Description\nIn `contracts/market/src/lib.rs`, `PENDING_REPORTS` stores oracle submissions under `REPORT_TTL = 172_800` (48 hours). If oracles submit divergent reports that never reach the 2-of-3 consensus threshold, stale reports remain indefinitely in the map, accumulating storage rent fees.\n\n## Complexity\n**Medium**\n\n## Acceptance Criteria\n- [ ] Implement `prune_stale_reports(env)` to purge reports older than `REPORT_TTL`\n- [ ] Call pruning during subsequent `submit_oracle_report` invocations\n- [ ] Add test verifying report submitted 49 hours ago is ignored and removed\n- [ ] Verify clean consensus detection when fresh reports are submitted after expiry",
        "labels": [
            "enhancement",
            "contracts",
            "oracle"
        ]
    },
    {
        "num": 23,
        "title": "#23 \u2014 Market Factory Admin Transfer Allows Indefinite Pending State Without Expiration Enforcement",
        "body": "**Labels:** `bug` `contracts` `security`\n\n## Description\nIn `contracts/market_factory/src/lib.rs`, constant `PENDING_ADMIN_TTL_SECS = 604_800` (7 days) is declared, but `accept_admin` checks only `PENDING_ADMIN_UNLOCK` without asserting that `env.ledger().timestamp() <= PENDING_ADMIN_EXPIRY`. A proposed admin can accept ownership months after proposal without renewal.\n\n## Complexity\n**Medium**\n\n## Acceptance Criteria\n- [ ] Assert `env.ledger().timestamp() <= pending_expiry` in `accept_admin`\n- [ ] Return `ContractError::AdminTransferExpired` if 7-day acceptance window has lapsed\n- [ ] Allow current admin to cancel pending transfer via `cancel_admin_proposal`\n- [ ] Add tests covering expired acceptance, valid acceptance, and admin cancellation",
        "labels": [
            "bug",
            "contracts",
            "security"
        ]
    },
    {
        "num": 24,
        "title": "#24 \u2014 Deploy Script deploy.sh References Deprecated Soroban CLI Commands and Syntax",
        "body": "**Labels:** `devops` `contracts` `ci-cd`\n\n## Description\n`contracts/scripts/deploy.sh` uses old `soroban` CLI binary syntax (e.g. `soroban contract deploy`) rather than the standardized `stellar` CLI syntax (e.g. `stellar contract deploy`). Developers following local setup instructions encounter command not found errors on up-to-date toolchains.\n\n## Complexity\n**Low**\n\n## Acceptance Criteria\n- [ ] Update `deploy.sh` to use `stellar contract deploy` and `stellar contract invoke`\n- [ ] Add fallback detection for environments with `soroban` alias\n- [ ] Add `--network testnet` flag support with configurable RPC URL and secret key arguments\n- [ ] Add automated test script `contracts/scripts/test-deploy.sh` to validate CLI script syntax",
        "labels": [
            "devops",
            "contracts",
            "ci-cd"
        ]
    },
    {
        "num": 25,
        "title": "#25 \u2014 Contracts CI Workflow Disables Integration Test Suite Execution",
        "body": "**Labels:** `bug` `contracts` `ci-cd` `testing`\n\n## Description\nIn `.github/workflows/contracts-ci.yml`, lines 49-53 comment out `# cargo test --all --all-features` with note `# Tests disabled - test structure refactoring in progress`. Pull requests modifying smart contract code are merged without any automated Rust unit or integration test validation.\n\n## Complexity\n**Medium**\n\n## Acceptance Criteria\n- [ ] Uncomment and restore `cargo test --all --all-features` in `.github/workflows/contracts-ci.yml`\n- [ ] Fix all failing tests or feature flags preventing workspace test execution\n- [ ] Ensure contract tests run on pull requests touching `contracts/**`\n- [ ] Verify CI test run completes in under 5 minutes",
        "labels": [
            "bug",
            "contracts",
            "ci-cd",
            "testing"
        ]
    },
    {
        "num": 26,
        "title": "#26 \u2014 backend/src/index.ts Uses Unimported requireAdminJwt Middleware Causing Runtime Crash",
        "body": "**Labels:** `bug` `backend` `auth` `critical`\n\n## Description\nIn `backend/src/index.ts`, route `app.get(\"/health/detailed\", requireAdminJwt, ...)` references `requireAdminJwt` on line 96 without importing it from `backend/src/middleware/requireAdminJwt.middleware.ts`. When starting the backend with `npm run build` or `npm run dev`, TypeScript compilation crashes with `Cannot find name 'requireAdminJwt'`. This is a critical blocker preventing server initialization.\n\n## Complexity\n**Medium**\n\n## Acceptance Criteria\n- [ ] Import `requireAdminJwt` from `./middleware/requireAdminJwt.middleware` in `backend/src/index.ts`\n- [ ] Verify `npm run build` succeeds without compilation errors\n- [ ] Add integration test verifying GET `/health/detailed` returns 401 without valid admin JWT\n- [ ] Add integration test verifying GET `/health/detailed` returns 200 with valid admin JWT",
        "labels": [
            "bug",
            "backend",
            "auth",
            "critical"
        ]
    },
    {
        "num": 27,
        "title": "#27 \u2014 Backend Routes Group 1 through 18 Defined But Not Mounted in Main Express App",
        "body": "**Labels:** `bug` `backend` `refactor`\n\n## Description\nIn `backend/src/routes/`, over 20 route modules exist including `disputes.routes.ts`, `oracle.routes.ts`, `wallets.routes.ts`, `notifications.routes.ts`, `marketAnalytics.routes.ts`, and `*Group*.routes.ts` (Group 1 through 18). However, `backend/src/index.ts` only mounts 7 routes (`auth`, `markets`, `governance`, `engagement`, `claims`, `bets`, `users`, `admin`). Endpoints for disputes, oracles, wallets, and notifications return 404.\n\n## Complexity\n**High**\n\n## Acceptance Criteria\n- [ ] Mount `disputesRouter` on `/api/disputes` in `backend/src/index.ts`\n- [ ] Mount `oracleRouter` on `/api/oracle` in `backend/src/index.ts`\n- [ ] Mount `walletsRouter` on `/api/wallets` in `backend/src/index.ts`\n- [ ] Mount `notificationsRouter` on `/api/notifications` in `backend/src/index.ts`\n- [ ] Harmonize and consolidate redundant `*Group*.routes.ts` endpoints into canonical route modules",
        "labels": [
            "bug",
            "backend",
            "refactor"
        ]
    },
    {
        "num": 28,
        "title": "#28 \u2014 Duplicate PostgreSQL Connection Pools in db.service.ts and config/db.ts",
        "body": "**Labels:** `bug` `backend` `database`\n\n## Description\n`backend/src/config/db.ts` creates and exports a `pool = new Pool(...)` instance with connection pool parameters, ssl settings, and event listeners. Concurrently, `backend/src/services/db.service.ts` creates a second independent `pool = new Pool({ connectionString: DATABASE_URL })`. Having two separate pools exhausts PostgreSQL connection limits and leads to transaction isolation issues.\n\n## Complexity\n**Medium**\n\n## Acceptance Criteria\n- [ ] Consolidate `backend/src/services/db.service.ts` to re-export `pool` from `../config/db`\n- [ ] Update all services and repositories to import `pool` exclusively from `../config/db`\n- [ ] Add pool connection limit metrics to Prometheus `/metrics` endpoint\n- [ ] Verify graceful shutdown properly drains the single unified pool",
        "labels": [
            "bug",
            "backend",
            "database"
        ]
    },
    {
        "num": 29,
        "title": "#29 \u2014 Duplicate Validation Middleware Implementations in validate.ts and validation.middleware.ts",
        "body": "**Labels:** `bug` `backend` `middleware` `refactor`\n\n## Description\nThe backend contains two divergent validation middlewares: `backend/src/api/middleware/validate.ts` (which provides `validate`, `validateBody`, `validateQuery`, `validateParams`) and `backend/src/middleware/validation.middleware.ts` (which provides `validate(schema)`). They return different error shapes (`{ error: string }` vs `{ status: 'error', errors: [...] }`), breaking API consistency.\n\n## Complexity\n**Medium**\n\n## Acceptance Criteria\n- [ ] Unify validation middlewares into a single canonical module in `backend/src/middleware/validation.middleware.ts`\n- [ ] Standardize API validation error response format to `{ success: false, error: { message, code: 'VALIDATION_ERROR', details } }`\n- [ ] Update all routes in `backend/src/routes/` to import the unified validation middleware\n- [ ] Add unit tests verifying request validation for body, query, and path parameters",
        "labels": [
            "bug",
            "backend",
            "middleware",
            "refactor"
        ]
    },
    {
        "num": 30,
        "title": "#30 \u2014 Unimplemented OracleController.getOracleReports Endpoint Returns Empty Response",
        "body": "**Labels:** `bug` `backend` `oracle`\n\n## Description\nIn `backend/src/api/controllers/OracleController.ts`, lines 97-103 define `getOracleReports` with a single comment `// TODO: implement`. Calling GET `/api/oracle/reports/:match_id` never sends an HTTP response, causing client requests to hang indefinitely until browser or gateway timeout.\n\n## Complexity\n**Medium**\n\n## Acceptance Criteria\n- [ ] Implement `getOracleReports` to query `oracle_reports` table for the specified `match_id`\n- [ ] Return 200 with `{ match_id, reports: [...] }` containing timestamp, oracle address, outcome, and signature\n- [ ] Return 404 if no reports exist for the specified match ID\n- [ ] Add controller unit tests covering successful lookup and not-found scenarios",
        "labels": [
            "bug",
            "backend",
            "oracle"
        ]
    },
    {
        "num": 31,
        "title": "#31 \u2014 In-Memory Notification Settings Map in notifications.routes.ts Loses State on Restart",
        "body": "**Labels:** `bug` `backend` `notifications` `database`\n\n## Description\nIn `backend/src/routes/notifications.routes.ts`, user notification settings are stored in an in-memory Map: `const notificationSettings = new Map<string, Record<string, unknown>>()`. Whenever the server restarts, crashes, or scales across multiple containers, all user notification preferences are wiped.\n\n## Complexity\n**Medium**\n\n## Acceptance Criteria\n- [ ] Create database migration for `user_notification_settings` table (user_id, email_enabled, push_enabled, created_at, updated_at)\n- [ ] Update `notifications.routes.ts` to persist and fetch settings from PostgreSQL `pool`\n- [ ] Cache settings in Redis with 1-hour TTL and invalidate on update\n- [ ] Add unit and integration tests for notification settings persistence",
        "labels": [
            "bug",
            "backend",
            "notifications",
            "database"
        ]
    },
    {
        "num": 32,
        "title": "#32 \u2014 Backend package.json Declares Non-Existent and Invalid Dependency Versions",
        "body": "**Labels:** `bug` `backend` `devops` `critical`\n\n## Description\nIn `backend/package.json`, several dependencies declare non-existent versions that break package managers during fresh installation: `\"node-cron\": \"^4.6.0\"` (latest stable is 3.x), `\"pg\": \"^8.22.0\"` (latest is 8.12.x/8.13.x), `\"zod\": \"^4.4.3\"` (Zod v4 is not released), `\"ws\": \"^8.21.2\"`, and `\"@sentry/node\": \"10.68.0\"`. In addition, both `pino` and `winston` are included redundantly.\n\n## Complexity\n**High**\n\n## Acceptance Criteria\n- [ ] Update `backend/package.json` dependencies to valid, stable npm versions (e.g., zod ^3.23.8, pg ^8.11.5, node-cron ^3.0.3, ws ^8.18.0)\n- [ ] Remove redundant `winston` logging library and standardize on `pino`\n- [ ] Generate clean `backend/package-lock.json` and ensure `npm ci` completes with 0 errors\n- [ ] Run `npm test` to verify all backend tests pass with corrected package versions",
        "labels": [
            "bug",
            "backend",
            "devops",
            "critical"
        ]
    },
    {
        "num": 33,
        "title": "#33 \u2014 @stellar/stellar-sdk Placed in devDependencies Causing Production Docker Runtime Failure",
        "body": "**Labels:** `bug` `backend` `devops` `security`\n\n## Description\nIn `backend/package.json`, `@stellar/stellar-sdk` is listed under `devDependencies`. When building the production Docker image via `backend/Dockerfile`, stage 2 executes `npm ci --omit=dev`. Consequently, `@stellar/stellar-sdk` is missing from the container, and `StellarService.ts` / `StellarIndexer.ts` crash with `Cannot find module '@stellar/stellar-sdk'`.\n\n## Complexity\n**High**\n\n## Acceptance Criteria\n- [ ] Move `@stellar/stellar-sdk` from `devDependencies` to `dependencies` in `backend/package.json`\n- [ ] Test Docker container build: `docker build -t bankerchanger-backend ./backend`\n- [ ] Verify container starts and passes `/health` check without module not found error\n- [ ] Add CI verification step checking production dependency completeness",
        "labels": [
            "bug",
            "backend",
            "devops",
            "security"
        ]
    },
    {
        "num": 34,
        "title": "#34 \u2014 Duplicate Admin Middleware Implementations in admin.middleware.ts and requireAdminJwt.middleware.ts",
        "body": "**Labels:** `security` `backend` `auth` `refactor`\n\n## Description\nThe backend contains two competing admin authentication middlewares: `backend/src/middleware/admin.middleware.ts` (checks `req.user.role === 'admin'`) and `backend/src/middleware/requireAdminJwt.middleware.ts` (directly parses Bearer token and checks `ADMIN_SECRET`). Routes in `admin.routes.ts` and `index.ts` mix and match both, leading to disparate authentication mechanisms.\n\n## Complexity\n**Medium**\n\n## Acceptance Criteria\n- [ ] Consolidate admin authentication into a single robust middleware in `backend/src/middleware/admin.middleware.ts`\n- [ ] Verify standard JWT claims (`role === 'admin'`) and ensure token has not been revoked in Redis blacklist\n- [ ] Export `requireAdmin` and deprecate `requireAdminJwt` with backward-compatible alias\n- [ ] Add comprehensive test suite verifying valid tokens, expired tokens, tampered tokens, and non-admin tokens",
        "labels": [
            "security",
            "backend",
            "auth",
            "refactor"
        ]
    },
    {
        "num": 35,
        "title": "#35 \u2014 Duplicate Migration Timestamps in backend/migrations Cause Out-of-Order Execution",
        "body": "**Labels:** `bug` `backend` `database`\n\n## Description\nIn `backend/migrations/`, multiple migration files share duplicate timestamps: `1723000000000_add-indexer-ledger-ranges.js` and `1723000000000_add-engagement-features.js`, as well as `1753000000000_register-oracle-public-keys.js` and `1753000000000_add-bet-odds-snapshot.js`. Depending on filesystem ordering, migrations execute non-deterministically across development, staging, and CI environments.\n\n## Complexity\n**Medium**\n\n## Acceptance Criteria\n- [ ] Renumber duplicate migration timestamps sequentially to establish an unambiguous migration order\n- [ ] Update migration verification script `backend/scripts/migration-check.js` to assert timestamp uniqueness\n- [ ] Verify `npm run migrate` runs smoothly on an empty PostgreSQL database\n- [ ] Verify `npm run migrate:down` rolls back cleanly",
        "labels": [
            "bug",
            "backend",
            "database"
        ]
    },
    {
        "num": 36,
        "title": "#36 \u2014 Migration Scripts Mix Drizzle ORM and node-pg-migrate Without Unified Config",
        "body": "**Labels:** `bug` `backend` `database` `devops`\n\n## Description\nIn `backend/package.json`, scripts mix Drizzle ORM and node-pg-migrate without a cohesive configuration. `\"migrate\": \"drizzle-kit migrate\"` fails because `drizzle.config.ts` is missing, while `\"migrate:down\": \"node-pg-migrate down\"` and `\"migrate:create\": \"node-pg-migrate create\"` use `node-pg-migrate`. All existing files in `backend/migrations/` are `node-pg-migrate` format.\n\n## Complexity\n**High**\n\n## Acceptance Criteria\n- [ ] Align `backend/package.json` scripts to use `node-pg-migrate` uniformly for migrations\n- [ ] Update `\"migrate\": \"node-pg-migrate up\"` and provide corresponding rollback scripts\n- [ ] Provide `drizzle.config.ts` if Drizzle Studio introspection is desired alongside migrations\n- [ ] Test migration cycle in CI workflow to ensure seamless execution on fresh databases",
        "labels": [
            "bug",
            "backend",
            "database",
            "devops"
        ]
    },
    {
        "num": 37,
        "title": "#37 \u2014 Missing OpenAPI YAML Specification Referenced by CI Validation Script",
        "body": "**Labels:** `bug` `backend` `ci-cd` `docs`\n\n## Description\nIn `.github/workflows/backend-ci.yml`, the job `Validate OpenAPI spec` executes `node -e \"const S = require('@apidevtools/swagger-parser'); S.validate('openapi.yaml')\"`. However, `openapi.yaml` is not present in the backend directory, causing the CI pipeline step to fail when triggered.\n\n## Complexity\n**Low**\n\n## Acceptance Criteria\n- [ ] Generate or commit the canonical `openapi.yaml` in `backend/` using swagger-jsdoc extraction\n- [ ] Add script `npm run openapi:generate` in `backend/package.json`\n- [ ] Ensure `npm run openapi:validate` executes successfully locally and in CI\n- [ ] Verify all endpoints in `backend/src/routes/` have accurate OpenAPI tags and schemas",
        "labels": [
            "bug",
            "backend",
            "ci-cd",
            "docs"
        ]
    },
    {
        "num": 38,
        "title": "#38 \u2014 Test and Production Root Route Handlers Statically Stubbed in backend/src/index.ts",
        "body": "**Labels:** `bug` `backend` `security` `refactor`\n\n## Description\nIn `backend/src/index.ts`, lines 142-166 register mock test routes in production: `app.post(\"/trading/bet\", (_req, res) => res.json({ ok: true }))`, `app.post(\"/wallet/withdraw\", ...)`, `app.get(\"/test-error\", ...)`, `app.get(\"/test-unhandled\", ...)`, and duplicate `app.post(\"/api/users\", ...)`. These dummy endpoints bypass business validation and conflict with real service implementations.\n\n## Complexity\n**Medium**\n\n## Acceptance Criteria\n- [ ] Remove mock test routes from production `backend/src/index.ts`\n- [ ] Relocate test fixtures to a dedicated `tests/routes/test-helpers.routes.ts` enabled only when `NODE_ENV === 'test'`\n- [ ] Route `/trading/bet` to real `BetController.placeBet` handler\n- [ ] Route `/wallet/withdraw` to real `WalletsController.withdraw` handler",
        "labels": [
            "bug",
            "backend",
            "security",
            "refactor"
        ]
    },
    {
        "num": 39,
        "title": "#39 \u2014 MarketService Database Error Handler Leaks Raw SQL Column Names to Clients",
        "body": "**Labels:** `security` `backend` `database`\n\n## Description\nIn `backend/src/services/MarketService.ts`, catch blocks for database query failures format the raw PostgreSQL driver error message into the response: `throw AppError.badRequest(\"Database error: \" + err.message)`. This exposes internal database table structures, column names, and constraint names to unauthenticated users.\n\n## Complexity\n**Low**\n\n## Acceptance Criteria\n- [ ] Sanitize database error responses to return generic error messages (e.g. 'Unable to process market query')\n- [ ] Log the full database error and stack trace internally via Pino logger with request ID context\n- [ ] Map PostgreSQL constraint violation codes (e.g. 23505 unique violation) to specific HTTP 409 Conflict codes\n- [ ] Add unit tests asserting internal SQL details are not present in error response bodies",
        "labels": [
            "security",
            "backend",
            "database"
        ]
    },
    {
        "num": 40,
        "title": "#40 \u2014 BetService Concurrent Bet Placement Race Condition Under Transaction Rollback",
        "body": "**Labels:** `security` `backend` `trading` `database`\n\n## Description\nIn `backend/src/services/BetService.ts`, when concurrent bets are submitted for the same market, the service queries current pool balances with `SELECT ... FROM markets WHERE id = $1` without acquiring a row lock (`FOR UPDATE`). Simultaneous transactions calculate odds against outdated pool balances, causing discrepancies between database states and blockchain states.\n\n## Complexity\n**High**\n\n## Acceptance Criteria\n- [ ] Use `SELECT ... FROM markets WHERE id = $1 FOR UPDATE` within a PostgreSQL transaction block\n- [ ] Verify pool share calculations occur with acquired row lock\n- [ ] Add optimistic concurrency version column or serializable transaction isolation\n- [ ] Write a concurrent betting load test simulating 50 simultaneous bets on a single market",
        "labels": [
            "security",
            "backend",
            "trading",
            "database"
        ]
    },
    {
        "num": 41,
        "title": "#41 \u2014 TOTP Service Backup Code Verification Does Not Invalidate Used Codes Atomically",
        "body": "**Labels:** `security` `backend` `auth`\n\n## Description\nIn `backend/src/services/totp.service.ts`, backup code verification reads the code from `totp_backup_codes` and marks it used in two separate queries without an encompassing transaction. Under high-concurrency race conditions, the same single-use backup code can be submitted simultaneously to authenticate two sessions.\n\n## Complexity\n**High**\n\n## Acceptance Criteria\n- [ ] Execute backup code validation and invalidation in an atomic `UPDATE ... SET used = true WHERE code_hash = $1 AND used = false RETURNING id` query\n- [ ] Ensure duplicate submissions return 401 Unauthorized immediately\n- [ ] Emit `SecurityEvent(type: 'BACKUP_CODE_USED', userId, ip)` audit log\n- [ ] Add integration test verifying simultaneous backup code requests fail",
        "labels": [
            "security",
            "backend",
            "auth"
        ]
    },
    {
        "num": 42,
        "title": "#42 \u2014 Export Service CSV Stream Lacks Header Sanitization Against Formula Injection (CSV Injection)",
        "body": "**Labels:** `security` `backend`\n\n## Description\nIn `backend/src/services/export.service.ts`, exporting transaction histories and bet records directly interpolates user input (e.g. display names, transaction memos, notes) into CSV cells. If a user enters a memo starting with `=`, `+`, `-`, or `@`, spreadsheet applications like Microsoft Excel execute external formulas when opened.\n\n## Complexity\n**Medium**\n\n## Acceptance Criteria\n- [ ] Prepend a single quote `'` to any string cell value starting with `=`, `+`, `-`, or `@`\n- [ ] Escape internal double quotes `\"` according to RFC 4180 CSV specifications\n- [ ] Add unit tests testing malicious formula payloads in export data\n- [ ] Verify exported CSVs render safely without execution warnings",
        "labels": [
            "security",
            "backend"
        ]
    },
    {
        "num": 43,
        "title": "#43 \u2014 Engagement Service XP Calculation Accumulates Double Points on Retried Events",
        "body": "**Labels:** `bug` `backend` `achievements`\n\n## Description\nIn `backend/src/services/engagement.service.ts`, `awardXp` inserts records into `user_xp_history` without enforcing idempotency keys. If the blockchain indexer re-polls an earlier ledger or replays a transaction event after transient failure, users are credited with duplicate XP and erroneous achievement badge unlocks.\n\n## Complexity\n**Medium**\n\n## Acceptance Criteria\n- [ ] Add unique constraint on `(user_id, source_event_id)` in `user_xp_history` table\n- [ ] Make `awardXp` idempotent using `ON CONFLICT (user_id, source_event_id) DO NOTHING`\n- [ ] Recalculate user level dynamically based on verified XP total\n- [ ] Add test verifying replaying identical event ID does not increment XP or badges",
        "labels": [
            "bug",
            "backend",
            "achievements"
        ]
    },
    {
        "num": 44,
        "title": "#44 \u2014 Cache Service Redis Disconnection Throws Unhandled Promise Rejections",
        "body": "**Labels:** `bug` `backend` `reliability`\n\n## Description\nIn `backend/src/services/cache.service.ts`, methods `get`, `set`, and `del` directly await Redis calls without local error handling. If Redis restarts or drops connection, unhandled rejections bubble up and crash API requests instead of falling back to direct database queries.\n\n## Complexity\n**Medium**\n\n## Acceptance Criteria\n- [ ] Wrap all Redis operations in safe try/catch blocks that degrade gracefully to database lookups\n- [ ] Log Redis connection anomalies with rate-limited warnings\n- [ ] Emit cache hit/miss/failure metrics to Prometheus\n- [ ] Add test simulating Redis offline state and verify API returns fresh database data",
        "labels": [
            "bug",
            "backend",
            "reliability"
        ]
    },
    {
        "num": 45,
        "title": "#45 \u2014 User Activity Feed Fails to Sanitize Sensitive Account Details Before Broadcasting",
        "body": "**Labels:** `security` `backend` `websocket` `users`\n\n## Description\nIn `backend/src/websocket/realtime.ts`, the activity feed broadcaster passes raw database user objects into WebSocket messages. Sensitive user properties including hashed passwords, TOTP secret flags, email addresses, and internal user UUIDs are broadcast to all connected WebSocket clients in the global activity room.\n\n## Complexity\n**Medium**\n\n## Acceptance Criteria\n- [ ] Create a strict `sanitizeActivityEvent` transformer that strips all private user fields\n- [ ] Broadcast only public information: public wallet address (truncated), market title, bet outcome, and amount\n- [ ] Add automated test asserting no private fields exist in WebSocket broadcast payload\n- [ ] Review all WebSocket room message serialization paths",
        "labels": [
            "security",
            "backend",
            "websocket",
            "users"
        ]
    },
    {
        "num": 46,
        "title": "#46 \u2014 Disputes Controller Missing Stellar Address Format Validation on Challenger Key",
        "body": "**Labels:** `bug` `backend` `disputes` `security`\n\n## Description\nIn `backend/src/api/controllers/disputes.controller.ts`, submitting a dispute accepts the challenger's address as an arbitrary string. Non-Stellar strings or SQL strings cause downstream blockchain verification queries to fail with unhandled 500 exceptions.\n\n## Complexity\n**Low**\n\n## Acceptance Criteria\n- [ ] Validate challenger address with `@stellar/stellar-sdk` `StrKey.isValidEd25519PublicKey`\n- [ ] Return 400 Bad Request with descriptive message if address format is invalid\n- [ ] Add unit tests testing invalid addresses, truncated keys, and valid Ed25519 public keys\n- [ ] Ensure validation occurs in route schema validator before controller execution",
        "labels": [
            "bug",
            "backend",
            "disputes",
            "security"
        ]
    },
    {
        "num": 47,
        "title": "#47 \u2014 StellarService Transaction Submission Lacks Jittered Exponential Backoff Retry",
        "body": "**Labels:** `enhancement` `backend` `blockchain` `reliability`\n\n## Description\nIn `backend/src/services/StellarService.ts`, `submitTransaction` submits transactions to Stellar Horizon / Soroban RPC without retry logic on network timeouts or HTTP 504 Gateway Timeout responses. Under normal Stellar testnet congestion, transactions fail needlessly and leave bets unconfirmed.\n\n## Complexity\n**High**\n\n## Acceptance Criteria\n- [ ] Implement retry loop with jittered exponential backoff (e.g. 1s, 2s, 4s up to 3 attempts)\n- [ ] Inspect Horizon error codes; retry on 504 Gateway Timeout, 429 Too Many Requests, and socket hangup\n- [ ] Do NOT retry on non-retryable 400 transaction bad errors (e.g. op_underfunded, bad_auth)\n- [ ] Add unit tests using mocked Horizon responses to verify retry behavior",
        "labels": [
            "enhancement",
            "backend",
            "blockchain",
            "reliability"
        ]
    },
    {
        "num": 48,
        "title": "#48 \u2014 Auto-Resolution Cron Auto-Locks Markets Without Verifying Ledger Timestamps",
        "body": "**Labels:** `bug` `backend` `cron` `markets`\n\n## Description\nIn `backend/src/cron/autoResolution.cron.ts`, `startAutoLockCron` compares market `scheduled_at` against server system time (`Date.now()`). If the backend server clock drifts or differs from Stellar ledger close time, markets are locked prematurely while on-chain contracts still accept bets.\n\n## Complexity\n**Medium**\n\n## Acceptance Criteria\n- [ ] Query latest ledger close time from `StellarIndexer` or Horizon RPC rather than host machine clock\n- [ ] Allow a 60-second grace buffer to prevent race conditions around fight start times\n- [ ] Log audit trail when auto-lock triggers on a market\n- [ ] Add integration test verifying auto-lock respects ledger timestamps",
        "labels": [
            "bug",
            "backend",
            "cron",
            "markets"
        ]
    },
    {
        "num": 49,
        "title": "#49 \u2014 Backend Request Logging Middleware Logs Unredacted Authorization Headers",
        "body": "**Labels:** `security` `backend` `middleware`\n\n## Description\nIn `backend/src/middleware/request-logging.middleware.ts`, incoming request headers are logged using Pino logger without masking `authorization` or `cookie` headers. Bearer JWT tokens and session secrets are stored in plaintext server log files and log aggregation tools.\n\n## Complexity\n**Low**\n\n## Acceptance Criteria\n- [ ] Configure Pino `redact` options for `req.headers.authorization`, `req.headers.cookie`, and `req.body.password`\n- [ ] Mask sensitive token strings with `[REDACTED]`\n- [ ] Add test verifying authorization header is sanitized in log output\n- [ ] Audit all middleware logging calls for confidential credential leakage",
        "labels": [
            "security",
            "backend",
            "middleware"
        ]
    },
    {
        "num": 50,
        "title": "#50 \u2014 System Health Detailed Endpoint Exposes Internal Connection Pool Metrics Publicly",
        "body": "**Labels:** `security` `backend` `observability`\n\n## Description\nIn `backend/src/index.ts`, the `/health/detailed` route exposes detailed database connection pool stats (idleCount, totalCount, waitingCount), Redis status, and internal version numbers. If accessible without authentication, attackers can gather reconnaissance on database capacity and connection pool exhaustion.\n\n## Complexity\n**Low**\n\n## Acceptance Criteria\n- [ ] Enforce `requireAdmin` authentication strictly on `/health/detailed`\n- [ ] Ensure public `/health` endpoint only exposes `{ status: 'healthy', timestamp }`\n- [ ] Add test verifying unauthenticated GET `/health/detailed` returns 401 Unauthorized\n- [ ] Document health check monitoring recommendations in `docs/runbook.md`",
        "labels": [
            "security",
            "backend",
            "observability"
        ]
    },
    {
        "num": 51,
        "title": "#51 \u2014 Webhook Delivery Lacks Retry Queue and Exponential Backoff for Failed Deliveries",
        "body": "**Labels:** `enhancement` `backend` `reliability`\n\n## Description\nIn `backend/src/routes/webhooksGroup9.routes.ts`, outgoing webhook notifications to third-party endpoints fail permanently on a single network timeout. There is no dead-letter queue, retry mechanism, or failure log to guarantee delivery of critical market resolution events.\n\n## Complexity\n**Medium**\n\n## Acceptance Criteria\n- [ ] Implement a durable webhook delivery queue backed by PostgreSQL or Redis\n- [ ] Retry failed deliveries up to 5 times with exponential backoff (1m, 5m, 15m, 1h, 6h)\n- [ ] Store delivery status and last error response code in `webhook_deliveries` table\n- [ ] Add manual retry admin endpoint `POST /api/admin/webhooks/:id/retry`",
        "labels": [
            "enhancement",
            "backend",
            "reliability"
        ]
    },
    {
        "num": 52,
        "title": "#52 \u2014 Auth Service Password Reset Token Generation Uses Insecure Math.random Instead of Crypto",
        "body": "**Labels:** `security` `backend` `auth`\n\n## Description\nIn `backend/src/services/auth.service.ts`, password reset tokens are generated using `Math.random().toString(36)`. V8's pseudo-random number generator is cryptographically insecure and predictable, allowing attackers to guess password reset tokens and hijack user accounts.\n\n## Complexity\n**High**\n\n## Acceptance Criteria\n- [ ] Replace `Math.random` with `crypto.randomBytes(32).toString('hex')` for reset token generation\n- [ ] Store only the SHA-256 hash of the reset token in the database\n- [ ] Enforce 15-minute expiration on all generated password reset tokens\n- [ ] Add test verifying entropy and uniqueness of generated reset tokens",
        "labels": [
            "security",
            "backend",
            "auth"
        ]
    },
    {
        "num": 53,
        "title": "#53 \u2014 Market Management Route Missing Category ID Foreign Key Validation",
        "body": "**Labels:** `bug` `backend` `markets` `database`\n\n## Description\nIn `backend/src/routes/marketManagement.routes.ts`, creating a market accepts a `category_id` parameter without verifying that the referenced category exists in the `categories` table. Submitting an invalid category ID triggers an unhandled foreign key constraint error resulting in a 500 error instead of a 400 Bad Request.\n\n## Complexity\n**Low**\n\n## Acceptance Criteria\n- [ ] Validate that `category_id` exists in `categories` before attempting market insertion\n- [ ] Return 400 Bad Request with message `'Invalid category_id: category does not exist'`\n- [ ] Add foreign key constraint test case in `tests/routes/marketManagement.test.ts`\n- [ ] Cache active categories list in Redis to minimize database lookups",
        "labels": [
            "bug",
            "backend",
            "markets",
            "database"
        ]
    },
    {
        "num": 54,
        "title": "#54 \u2014 Transaction History Route Cursor Pagination Calculates HasNextPage Incorrectly",
        "body": "**Labels:** `bug` `backend` `repository`\n\n## Description\nIn `backend/src/routes/transactionHistory.routes.ts`, cursor pagination fetches exactly `limit` rows and calculates `hasNextPage` based on total count query. This causes off-by-one errors and unnecessary full table count queries on large transaction history datasets.\n\n## Complexity\n**Medium**\n\n## Acceptance Criteria\n- [ ] Query `limit + 1` rows using cursor index to determine `hasNextPage` without full count query\n- [ ] Slice returned results to `limit` and set `nextCursor` to the ID of the last item if `hasNextPage` is true\n- [ ] Add unit tests for first page, middle page, and last page cursor boundaries\n- [ ] Verify cursor pagination performance on tables with >100,000 transaction records",
        "labels": [
            "bug",
            "backend",
            "repository"
        ]
    },
    {
        "num": 55,
        "title": "#55 \u2014 Affiliate Commission Calculation Off-By-One at Tier Threshold Boundaries",
        "body": "**Labels:** `bug` `backend` `referrals`\n\n## Description\nIn `backend/src/constants/affiliateTiers.ts` and `backend/src/routes/affiliateGroup18.routes.ts`, tier qualification compares `referralCount < tier.threshold` instead of `<=`. Users reaching the exact milestone threshold (e.g., exactly 25 referrals for Silver or 100 for Gold) remain stuck in the lower commission tier.\n\n## Complexity\n**Medium**\n\n## Acceptance Criteria\n- [ ] Fix comparison logic to correctly qualify users reaching exact tier threshold\n- [ ] Add automated test verifying referral counts at threshold - 1, threshold, and threshold + 1\n- [ ] Verify affiliate payout calculation uses updated tier commission rate\n- [ ] Document affiliate tier qualifications in `docs/architecture.md`",
        "labels": [
            "bug",
            "backend",
            "referrals"
        ]
    },
    {
        "num": 56,
        "title": "#56 \u2014 Duplicate Indexer Implementations in /indexer and /backend/src/indexer Cause Split Architecture",
        "body": "**Labels:** `bug` `indexer` `backend` `refactor`\n\n## Description\nThe repository contains two separate indexers: one in `indexer/src/` (standalone microservice) and one in `backend/src/indexer/` (`StellarIndexer.ts`, `EventProcessor.ts`, `ledgerTracker.ts`). Both poll Horizon and Soroban RPC, but write to different database tables using different schema definitions, leading to race conditions and duplicate polling overhead.\n\n## Complexity\n**High**\n\n## Acceptance Criteria\n- [ ] Establish a clear architectural boundary by designating `indexer/` as the single authoritative indexer microservice\n- [ ] Deprecate duplicate background polling inside `backend/src/indexer/StellarIndexer.ts` in favor of reading shared event store\n- [ ] Update `docker-compose.yml` to run the standalone indexer container cleanly\n- [ ] Document indexer deployment and service boundaries in `docs/architecture.md`",
        "labels": [
            "bug",
            "indexer",
            "backend",
            "refactor"
        ]
    },
    {
        "num": 57,
        "title": "#57 \u2014 Indexer Default Port 3001 Collides with Backend Default Port",
        "body": "**Labels:** `bug` `indexer` `devops`\n\n## Description\nIn `indexer/src/index.ts`, line 5 sets `const PORT = process.env.PORT || 3001`. In `backend/src/index.ts`, the backend also defaults to port 3001. When running both locally without custom `.env` overrides, the second service fails to start with `Error: listen EADDRINUSE: address already in use :::3001`.\n\n## Complexity\n**Low**\n\n## Acceptance Criteria\n- [ ] Change default port in `indexer/src/index.ts` to 3002 (matching Dockerfile and docker-compose port mappings)\n- [ ] Update `indexer/.env.example` to declare `PORT=3002`\n- [ ] Verify local startup of backend (3001) and indexer (3002) concurrently without port collision\n- [ ] Update health check command in `indexer/Dockerfile` to use port 3002",
        "labels": [
            "bug",
            "indexer",
            "devops"
        ]
    },
    {
        "num": 58,
        "title": "#58 \u2014 Indexer Poller Imports Foreign and Unused upsertInvoice Function from SQLite DB Module",
        "body": "**Labels:** `bug` `indexer` `refactor`\n\n## Description\nIn `indexer/src/poller.ts`, line 2 imports `upsertInvoice` from `./db`. This function is leftover boilerplate from an unrelated lightning/invoice payment template and has no relevance to Stellar boxing prediction markets. Leaving dead foreign code confuses contributors and causes lint errors.\n\n## Complexity\n**Low**\n\n## Acceptance Criteria\n- [ ] Remove `upsertInvoice` import from `indexer/src/poller.ts`\n- [ ] Remove unused invoice table and invoice handling methods from `indexer/src/db.ts`\n- [ ] Verify TypeScript compiles with `npm run build` in `indexer/` without unused variable warnings\n- [ ] Add clean test verifying poller imports only Soroban market event handlers",
        "labels": [
            "bug",
            "indexer",
            "refactor"
        ]
    },
    {
        "num": 59,
        "title": "#59 \u2014 Indexer Uses SQLite While Backend Uses PostgreSQL Causing Inconsistent Event Storage",
        "body": "**Labels:** `bug` `indexer` `database`\n\n## Description\nIn `indexer/src/db.ts`, the database adapter initializes a SQLite database using `better-sqlite3` and writes to `cursor.json`. Meanwhile, the backend queries PostgreSQL `blockchain_events` table. Events captured by the indexer are trapped in local SQLite storage and not accessible by the backend API.\n\n## Complexity\n**High**\n\n## Acceptance Criteria\n- [ ] Refactor `indexer/src/db.ts` to persist indexed events into shared PostgreSQL database (`blockchain_events`)\n- [ ] Store indexer cursor checkpoints in PostgreSQL table `indexer_checkpoints`\n- [ ] Provide connection pooling using `pg.Pool` with reconnection resilience\n- [ ] Add migration verifying PostgreSQL indexer schema compatibility",
        "labels": [
            "bug",
            "indexer",
            "database"
        ]
    },
    {
        "num": 60,
        "title": "#60 \u2014 Indexer package.json Has Conflicting TypeScript and Jest Peer Dependencies",
        "body": "**Labels:** `bug` `indexer` `devops`\n\n## Description\nIn `indexer/package.json`, dependencies declare `\"typescript\": \"^6.0.3\"` (TypeScript 6 does not exist) and `\"jest\": \"^30.4.2\"` paired with `\"ts-jest\": \"^29.4.9\"` (ts-jest 29 requires Jest 29). Running `npm install` fails with unresolved peer dependency conflicts (`ERESOLVE unable to resolve dependency tree`).\n\n## Complexity\n**Medium**\n\n## Acceptance Criteria\n- [ ] Pin `typescript` to `^5.4.5` in `indexer/package.json`\n- [ ] Align `jest` to `^29.7.0` and `ts-jest` to `^29.1.5`\n- [ ] Update `@types/jest` to `^29.5.12`\n- [ ] Verify `npm install` and `npm test` execute cleanly in `indexer/`",
        "labels": [
            "bug",
            "indexer",
            "devops"
        ]
    },
    {
        "num": 61,
        "title": "#61 \u2014 Indexer Cursor File Storage cursor.json Suffers from Non-Atomic File Writes on Crash",
        "body": "**Labels:** `bug` `indexer` `reliability`\n\n## Description\nIn `indexer/src/db.ts`, `saveCursor` writes the latest ledger sequence to `cursor.json` using non-atomic filesystem operations. If the indexer container is terminated (SIGKILL/OOM) while writing, `cursor.json` is left partially written or corrupted with zero bytes, causing the indexer to fail on restart.\n\n## Complexity\n**Medium**\n\n## Acceptance Criteria\n- [ ] Implement atomic file writes by writing to `cursor.json.tmp` and renaming atomically via `fs.rename`\n- [ ] Validate JSON integrity before replacing the active cursor file\n- [ ] Persist cursor to database checkpoint table as primary source of truth with file as secondary cache\n- [ ] Add test verifying recovery from simulated truncated cursor file",
        "labels": [
            "bug",
            "indexer",
            "reliability"
        ]
    },
    {
        "num": 62,
        "title": "#62 \u2014 Fault Tolerant Poller Fails to Reconnect to Horizon After Network Timeout",
        "body": "**Labels:** `bug` `indexer` `reliability`\n\n## Description\nIn `indexer/src/faultTolerantPoller.ts`, when a network timeout occurs while connecting to Soroban RPC or Horizon, the poller catches the error but fails to reset the underlying HTTP agent or re-initialize the client. Subsequent poll attempts reuse a broken connection socket, causing infinite consecutive timeout errors.\n\n## Complexity\n**High**\n\n## Acceptance Criteria\n- [ ] Re-instantiate the Soroban RPC Server client instance upon 3 consecutive network failures\n- [ ] Implement connection socket reset and DNS re-resolution\n- [ ] Add jittered exponential backoff with a maximum delay cap of 30 seconds\n- [ ] Write a test simulating network disconnect and verify automatic poller recovery",
        "labels": [
            "bug",
            "indexer",
            "reliability"
        ]
    },
    {
        "num": 63,
        "title": "#63 \u2014 Event Pipeline Missing Transactional Dead Letter Queue for Malformed Soroban Events",
        "body": "**Labels:** `enhancement` `indexer` `reliability`\n\n## Description\nIn `indexer/src/eventPipeline.ts`, if a contract emits an event with unexpected data structure or corrupted XDR, the event processing pipeline throws an exception that halts the entire polling batch. The indexer cannot advance past the faulty ledger, resulting in an indefinite sync stall.\n\n## Complexity\n**High**\n\n## Acceptance Criteria\n- [ ] Catch event deserialization errors individually without failing the entire ledger batch\n- [ ] Route malformed events to a `failed_events` dead-letter queue table with error stack and raw XDR\n- [ ] Emit Prometheus counter `indexer_malformed_events_total`\n- [ ] Allow the indexer cursor to advance while alerting operators of quarantined events",
        "labels": [
            "enhancement",
            "indexer",
            "reliability"
        ]
    },
    {
        "num": 64,
        "title": "#64 \u2014 Event Schema Validation Fails to Parse Negative Int128 Values in Bet Amount",
        "body": "**Labels:** `security` `indexer` `blockchain`\n\n## Description\nIn `indexer/src/eventSchemas.ts`, the Zod schema for contract event validation accepts string representations of integers but does not validate that `amount` or `shares` are strictly positive integers. A malicious or mock contract emitting negative values would corrupt pool accounting in the indexer database.\n\n## Complexity\n**Medium**\n\n## Acceptance Criteria\n- [ ] Enforce positive non-zero bigint validation in `eventSchemas.ts` for all bet amounts and payouts\n- [ ] Reject events containing negative numbers or invalid decimal formats\n- [ ] Add unit tests with malicious and boundary numeric payloads\n- [ ] Ensure schema parsing errors are logged with detailed contract address context",
        "labels": [
            "security",
            "indexer",
            "blockchain"
        ]
    },
    {
        "num": 65,
        "title": "#65 \u2014 Indexer Distributed Lock Does Not Release On Uncaught Process Signal SIGTERM",
        "body": "**Labels:** `bug` `indexer` `reliability`\n\n## Description\nIn `indexer/src/distributedLock.ts`, the Redis-based distributed lock (`acquireDistributedLock`) does not register `process.on('SIGTERM')` or `process.on('SIGINT')` signal handlers. When Kubernetes or Docker restarts the indexer pod, the lock remains held in Redis until TTL expiration (15 minutes), preventing the new instance from indexing.\n\n## Complexity\n**Medium**\n\n## Acceptance Criteria\n- [ ] Register graceful shutdown hooks that release the Redis lock token before process exit\n- [ ] Set lock TTL to a reasonable 30 seconds with automatic heartbeat renewal\n- [ ] Add release verification test during container shutdown simulation\n- [ ] Log lock acquisition, renewal, and release events with instance ID",
        "labels": [
            "bug",
            "indexer",
            "reliability"
        ]
    },
    {
        "num": 66,
        "title": "#66 \u2014 Ledger Continuity Resync Skips Ledger Sequences When RPC Batch Size Exceeds 100",
        "body": "**Labels:** `bug` `indexer` `blockchain`\n\n## Description\nIn `indexer/src/ledgerContinuity.ts`, `computeResyncStartLedger` detects gaps between current ledger and last known ledger. When the gap is large (>100 ledgers) and batch querying is used, pagination cursor calculations off-by-one by starting from `lastLedger + 1` instead of `lastLedger`, skipping the first ledger of the gap.\n\n## Complexity\n**High**\n\n## Acceptance Criteria\n- [ ] Fix gap boundary logic so resync spans `[lastProcessedLedger + 1, currentLedger]` inclusive\n- [ ] Add safety assertions that no intermediate ledgers are omitted during resync batches\n- [ ] Add test case with synthetic 500-ledger gap and verify every single ledger is processed in sequence\n- [ ] Emit `indexer_resync_gap_size` metric",
        "labels": [
            "bug",
            "indexer",
            "blockchain"
        ]
    },
    {
        "num": 67,
        "title": "#67 \u2014 WebSocket Server ws.ts Drops Connections on High Event Volume Without Backpressure",
        "body": "**Labels:** `bug` `indexer` `websocket` `performance`\n\n## Description\nIn `indexer/src/ws.ts`, `broadcast` iterates over all connected client sockets and calls `client.send(data)` immediately. When multiple ledger events are processed rapidly, slow clients accumulate unbounded buffered data in memory (`ws.bufferedAmount`), resulting in high memory usage and socket disconnects.\n\n## Complexity\n**High**\n\n## Acceptance Criteria\n- [ ] Check `ws.bufferedAmount` before sending; drop or throttle non-critical market updates for slow clients\n- [ ] Terminate unresponsive client sockets whose buffer exceeds `MAX_BUFFER_SIZE` (1MB)\n- [ ] Implement ping/pong heartbeat with 30s interval to prune dead connections\n- [ ] Add test simulating slow client receiving high-frequency broadcast stream",
        "labels": [
            "bug",
            "indexer",
            "websocket",
            "performance"
        ]
    },
    {
        "num": 68,
        "title": "#68 \u2014 Indexer Health Check Fails to Compare Current System Time with Latest Ledger Close Time",
        "body": "**Labels:** `bug` `indexer` `observability`\n\n## Description\nIn `indexer/src/health.ts`, the `/health` endpoint returns `{ status: 'healthy' }` as long as the HTTP server is running, even if the background poller crashed or hasn't processed a ledger in hours. Operators and container orchestrators receive false positive health signals.\n\n## Complexity\n**Medium**\n\n## Acceptance Criteria\n- [ ] Compare current UTC time with `lastProcessedLedgerTimestamp` in `/health` check\n- [ ] Mark health status as `degraded` if lag is > 2 minutes and `unhealthy` (HTTP 503) if lag > 10 minutes\n- [ ] Include `ledger_lag_seconds` and `last_processed_ledger` in health response JSON\n- [ ] Add unit tests testing healthy, degraded, and unhealthy threshold states",
        "labels": [
            "bug",
            "indexer",
            "observability"
        ]
    },
    {
        "num": 69,
        "title": "#69 \u2014 Backoff Calculation Allows Jitter to Exceed Configured Maximum Retry Interval",
        "body": "**Labels:** `bug` `indexer` `reliability`\n\n## Description\nIn `indexer/src/backoff.ts`, `calculateBackoff` computes exponential delay `base * 2^attempt` and subsequently adds random jitter `Math.random() * jitterFactor`. When delay is near `maxInterval`, adding jitter causes the total backoff time to exceed the configured maximum interval ceiling.\n\n## Complexity\n**Low**\n\n## Acceptance Criteria\n- [ ] Clamp the final computed backoff duration so `totalDelay <= maxInterval` at all times\n- [ ] Ensure jitter is applied symmetrically or subtracted within bounds\n- [ ] Add unit test with high retry attempt count asserting result is strictly <= `maxInterval`\n- [ ] Add property tests verifying deterministic bounds on backoff generator",
        "labels": [
            "bug",
            "indexer",
            "reliability"
        ]
    },
    {
        "num": 70,
        "title": "#70 \u2014 Indexer Metrics Service Lacks Prometheus Counters for Re-Org Ledgers Encountered",
        "body": "**Labels:** `enhancement` `indexer` `observability`\n\n## Description\nIn `indexer/src/metrics.ts`, Prometheus metrics track processed events and poll duration, but omit counters for ledger rollbacks, re-orgs, and RPC rate-limit events. Monitoring systems cannot trigger alerts when the network experiences ledger sequence anomalies.\n\n## Complexity\n**Low**\n\n## Acceptance Criteria\n- [ ] Add `indexer_reorg_detected_total` Counter metric\n- [ ] Add `indexer_rpc_rate_limit_total` Counter metric\n- [ ] Increment counters in `poller.ts` and `ledgerContinuity.ts` upon anomaly detection\n- [ ] Verify all new metrics appear on `/metrics` endpoint with proper labels",
        "labels": [
            "enhancement",
            "indexer",
            "observability"
        ]
    },
    {
        "num": 71,
        "title": "#71 \u2014 Poller Memory Leak in Event Deduplication Cache When Running for Extended Periods",
        "body": "**Labels:** `bug` `indexer` `performance`\n\n## Description\nIn `indexer/src/poller.ts`, an in-memory `Set` or `Map` is used to deduplicate received event IDs across poll cycles. Because old event IDs are never evicted from the set, memory usage grows continuously over days of operation, ultimately causing Node.js out-of-memory crashes.\n\n## Complexity\n**Medium**\n\n## Acceptance Criteria\n- [ ] Replace unbounded in-memory collection with an LRU cache capped at 50,000 entries or TTL-based eviction\n- [ ] Rely on PostgreSQL primary key unique constraints for persistent deduplication\n- [ ] Add test verifying cache size stays bounded after processing 100,000 synthetic event IDs\n- [ ] Monitor process heap memory usage in Prometheus metrics",
        "labels": [
            "bug",
            "indexer",
            "performance"
        ]
    },
    {
        "num": 72,
        "title": "#72 \u2014 Stellar SDK RPC Method Call Does Not Handle Rate Limiting (HTTP 429) Gracefully",
        "body": "**Labels:** `bug` `indexer` `blockchain` `reliability`\n\n## Description\nIn `indexer/src/poller.ts`, calls to `rpc.getEvents()` throw an uncaught exception when the public Soroban RPC node rate-limits requests with HTTP 429. The poller logs an error and retries immediately without honoring the `Retry-After` HTTP header.\n\n## Complexity\n**Medium**\n\n## Acceptance Criteria\n- [ ] Extract `Retry-After` header value from RPC 429 response when available\n- [ ] Sleep for the specified retry interval (or default 5s if header is absent) before next poll request\n- [ ] Log rate-limiting event at WARN level rather than ERROR\n- [ ] Add unit test with mocked 429 response verifying backoff delay",
        "labels": [
            "bug",
            "indexer",
            "blockchain",
            "reliability"
        ]
    },
    {
        "num": 73,
        "title": "#73 \u2014 WebSocket Client Reconnection Floods Indexer with Unchecked Subscriptions",
        "body": "**Labels:** `security` `indexer` `websocket`\n\n## Description\nIn `indexer/src/ws.ts`, connected clients can send unlimited `subscribe` messages for market channels. A single client can subscribe to thousands of non-existent market IDs, consuming server memory and degrading broadcast performance for all users.\n\n## Complexity\n**Medium**\n\n## Acceptance Criteria\n- [ ] Limit maximum active market subscriptions per client connection to 50\n- [ ] Validate that subscribed `market_id` matches numeric or UUID format\n- [ ] Rate-limit incoming WebSocket messages to max 20 messages per second per IP\n- [ ] Add test verifying subscription limit rejection",
        "labels": [
            "security",
            "indexer",
            "websocket"
        ]
    },
    {
        "num": 74,
        "title": "#74 \u2014 Indexer Database Migration Lacks Unique Index on Event Transaction Hash and Index",
        "body": "**Labels:** `bug` `indexer` `database`\n\n## Description\nIn `indexer/src/db.ts` and `backend/migrations/`, the `blockchain_events` table does not enforce a unique constraint on `(transaction_hash, event_index)`. When the indexer restarts after a mid-batch failure, re-processing the same ledger inserts duplicate rows, duplicating user activity and bet counts.\n\n## Complexity\n**Medium**\n\n## Acceptance Criteria\n- [ ] Add migration creating a `UNIQUE INDEX idx_blockchain_events_tx_idx ON blockchain_events (transaction_hash, event_index)`\n- [ ] Use `ON CONFLICT (transaction_hash, event_index) DO NOTHING` in event insertion queries\n- [ ] Add test verifying inserting identical event twice results in single database row\n- [ ] Verify query performance on event lookups by transaction hash",
        "labels": [
            "bug",
            "indexer",
            "database"
        ]
    },
    {
        "num": 75,
        "title": "#75 \u2014 Indexer Graceful Shutdown Does Not Drain In-Flight Event Batches Before Process Exit",
        "body": "**Labels:** `bug` `indexer` `reliability`\n\n## Description\nIn `indexer/src/server.ts`, the process termination handler calls `process.exit(0)` immediately upon receiving `SIGTERM`. Any event batch currently being written to the database or broadcast to WebSocket clients is cut off mid-transaction, leading to partial ledger persistence.\n\n## Complexity\n**Medium**\n\n## Acceptance Criteria\n- [ ] Implement graceful shutdown coordinator that stops accepting new poll tasks on `SIGTERM`\n- [ ] Wait for current in-flight ledger batch to finish processing and commit transaction\n- [ ] Close WebSocket server and database connection pool with 10-second timeout\n- [ ] Log clean shutdown message before calling `process.exit(0)`",
        "labels": [
            "bug",
            "indexer",
            "reliability"
        ]
    },
    {
        "num": 76,
        "title": "#76 \u2014 frontend/package.json Has Conflicting React 19 and React-DOM 18 Dependencies",
        "body": "**Labels:** `bug` `frontend` `devops` `critical`\n\n## Description\nIn `frontend/package.json`, dependencies declare `\"react\": \"^19.2.7\"` paired with `\"react-dom\": \"^18.3.1\"` alongside `\"next\": \"14.2.3\"`, `\"eslint-config-next\": \"16.2.9\"`, and `\"@next/bundle-analyzer\": \"16.2.9\"`. Mismatching major versions across React, React-DOM, and Next.js causes severe peer dependency failures during `npm install` and runtime hydration crashes in Next.js 14 App Router.\n\n## Complexity\n**High**\n\n## Acceptance Criteria\n- [ ] Align React and React-DOM versions to `^18.3.1` in `frontend/package.json`\n- [ ] Align `@types/react` and `@types/react-dom` to `^18.3.0`\n- [ ] Align `eslint-config-next` and `@next/bundle-analyzer` to `14.2.3`\n- [ ] Generate a clean `frontend/package-lock.json` and ensure `npm run build` succeeds",
        "labels": [
            "bug",
            "frontend",
            "devops",
            "critical"
        ]
    },
    {
        "num": 77,
        "title": "#77 \u2014 Frontend Missing type-check and generate:types Scripts Required by CI Workflow",
        "body": "**Labels:** `bug` `frontend` `ci-cd`\n\n## Description\nIn `.github/workflows/frontend-ci.yml`, steps execute `npm run type-check` (line 50) and `npm run generate:types` (line 55). Neither script is defined in `frontend/package.json`, causing the frontend CI workflow to fail immediately with `npm ERR! missing script: type-check`.\n\n## Complexity\n**Low**\n\n## Acceptance Criteria\n- [ ] Add `\"type-check\": \"tsc --noEmit\"` to `frontend/package.json` scripts\n- [ ] Add `\"generate:types\": \"openapi-typescript ../backend/openapi.yaml -o src/types/api.ts\"` script\n- [ ] Verify `npm run type-check` passes without TypeScript errors\n- [ ] Ensure the frontend CI workflow executes both steps successfully",
        "labels": [
            "bug",
            "frontend",
            "ci-cd"
        ]
    },
    {
        "num": 78,
        "title": "#78 \u2014 Duplicate API Client Implementations in frontend/lib/api.ts and frontend/src/services/api.ts",
        "body": "**Labels:** `bug` `frontend` `refactor`\n\n## Description\nTwo divergent API client implementations exist in `frontend/`: `frontend/lib/api.ts` (throwing `APIError` and using basic fetch) and `frontend/src/services/api.ts` (throwing `NotFoundError`, `NetworkError`, with retry logic). Components and hooks import from both locations inconsistently, causing divergent error handling and retry behaviors.\n\n## Complexity\n**Medium**\n\n## Acceptance Criteria\n- [ ] Standardize on `frontend/src/services/api.ts` as the canonical API client\n- [ ] Re-export or deprecate `frontend/lib/api.ts` with backward compatibility warnings\n- [ ] Update all hooks in `frontend/src/hooks/` to import from `src/services/api`\n- [ ] Verify uniform error throwing (`APIError`, `NotFoundError`, `NetworkError`) across all API calls",
        "labels": [
            "bug",
            "frontend",
            "refactor"
        ]
    },
    {
        "num": 79,
        "title": "#79 \u2014 Duplicate Stellar Wallet Utilities in frontend/lib/stellar.ts and frontend/src/services/wallet.ts",
        "body": "**Labels:** `bug` `frontend` `wallet` `refactor`\n\n## Description\nWallet and Soroban interaction utilities are split across `frontend/lib/stellar.ts`, `frontend/lib/freighter.ts`, and `frontend/src/services/wallet.ts`. They maintain duplicate network passphrase constants and conflicting transaction simulation helpers, leading to intermittent transaction simulation failures.\n\n## Complexity\n**Medium**\n\n## Acceptance Criteria\n- [ ] Consolidate Soroban transaction building, simulation, and signing into `frontend/src/services/wallet.ts`\n- [ ] Use centralized network configuration from `NEXT_PUBLIC_STELLAR_NETWORK`\n- [ ] Add comprehensive unit tests for transaction building and error parsing\n- [ ] Remove dead and redundant helper functions in `frontend/lib/`",
        "labels": [
            "bug",
            "frontend",
            "wallet",
            "refactor"
        ]
    },
    {
        "num": 80,
        "title": "#80 \u2014 Duplicate UI Components for Market Odds and Pool Bars Across Components Directory",
        "body": "**Labels:** `enhancement` `frontend` `ux` `refactor`\n\n## Description\nIn `frontend/src/components/market/`, three separate components implement horizontal odds/pool bars: `MarketOddsBar.tsx`, `PoolBar.tsx`, and `PoolProportionBar.tsx`. Each component has slightly different styling, prop names, and color codes, creating a fragmented visual appearance across market cards and detail pages.\n\n## Complexity\n**Low**\n\n## Acceptance Criteria\n- [ ] Consolidate into a single canonical `MarketOddsBar.tsx` component supporting responsive size variants ('sm', 'md', 'lg')\n- [ ] Ensure proper handling of 0 pool volume (renders equal proportions without NaN)\n- [ ] Update `MarketCard.tsx` and `MarketDetailContent.tsx` to use the unified component\n- [ ] Remove redundant `PoolBar.tsx` and `PoolProportionBar.tsx` files",
        "labels": [
            "enhancement",
            "frontend",
            "ux",
            "refactor"
        ]
    },
    {
        "num": 81,
        "title": "#81 \u2014 Duplicate Wallet Button Components in frontend/src/components/layout",
        "body": "**Labels:** `enhancement` `frontend` `wallet` `refactor`\n\n## Description\nIn `frontend/src/components/layout/`, both `WalletButton.tsx` (224 lines, feature-rich) and `WalletConnectButton.tsx` (10 lines, stub) exist. `Header.tsx` imports `WalletButton`, while other sections attempt to import `WalletConnectButton`, causing duplicate code and confusion.\n\n## Complexity\n**Low**\n\n## Acceptance Criteria\n- [ ] Remove the redundant stub `WalletConnectButton.tsx`\n- [ ] Ensure `WalletButton.tsx` handles connecting, connected (with address truncation and balance display), and disconnected states\n- [ ] Add unit tests verifying clipboard copy, explorer link navigation, and disconnect trigger\n- [ ] Ensure accessibility with `aria-haspopup` and keyboard dropdown support",
        "labels": [
            "enhancement",
            "frontend",
            "wallet",
            "refactor"
        ]
    },
    {
        "num": 82,
        "title": "#82 \u2014 Missing frontend/Dockerfile Referenced in Root docker-compose.yml",
        "body": "**Labels:** `bug` `frontend` `devops`\n\n## Description\nIn `docker-compose.yml`, service `frontend` declares `build: ./frontend`. However, `frontend/Dockerfile` does not exist in the repository. Running `docker compose up --build` fails immediately with `unable to prepare context: path \"./frontend/Dockerfile\" not found`.\n\n## Complexity\n**Medium**\n\n## Acceptance Criteria\n- [ ] Create production multi-stage `frontend/Dockerfile` using Node.js 20 Alpine and Next.js standalone output\n- [ ] Configure non-root user `nextjs` for container security\n- [ ] Include `HEALTHCHECK` verifying `http://localhost:3000/` or `/api/time`\n- [ ] Verify `docker compose up --build frontend` runs and serves the Next.js app successfully",
        "labels": [
            "bug",
            "frontend",
            "devops"
        ]
    },
    {
        "num": 83,
        "title": "#83 \u2014 Next.js Config Lacks Content Security Policy (CSP) Headers for Production",
        "body": "**Labels:** `security` `frontend`\n\n## Description\nIn `frontend/next.config.js`, HTTP security headers are configured but omit a `Content-Security-Policy` header. Web3 applications interacting with browser extension wallets require strict CSP directives (`connect-src`, `script-src`) to prevent malicious script injection and wallet credential exfiltration.\n\n## Complexity\n**Medium**\n\n## Acceptance Criteria\n- [ ] Add strict Content-Security-Policy header in `frontend/next.config.js`\n- [ ] Allow required connections: Soroban RPC endpoints, Horizon, backend API URL, and WebSocket hosts\n- [ ] Disallow `unsafe-eval` in production builds\n- [ ] Add Playwright security test asserting CSP header presence and directives",
        "labels": [
            "security",
            "frontend"
        ]
    },
    {
        "num": 84,
        "title": "#84 \u2014 Market Detail Page Missing Dynamic Metadata and OpenGraph Image Generation for Social Sharing",
        "body": "**Labels:** `enhancement` `frontend` `seo`\n\n## Description\nIn `frontend/src/app/markets/[market_id]/page.tsx`, the page does not export a `generateMetadata` function. When market URLs are shared on Twitter/X, Discord, or Telegram, social cards show generic site metadata instead of the fighter names, scheduled fight date, and betting volume.\n\n## Complexity\n**Medium**\n\n## Acceptance Criteria\n- [ ] Export dynamic `generateMetadata` function fetching market details in `page.tsx`\n- [ ] Set dynamic `title`: `{fighter_a} vs {fighter_b} \u2014 Boxing Prediction Market`\n- [ ] Wire `frontend/src/app/api/og/route.tsx` to dynamically render custom OpenGraph cards with odds and logos\n- [ ] Add unit test verifying metadata generation for valid and non-existent market IDs",
        "labels": [
            "enhancement",
            "frontend",
            "seo"
        ]
    },
    {
        "num": 85,
        "title": "#85 \u2014 Market Filters URL Search Parameters Reset Selected Tab on Page Refresh",
        "body": "**Labels:** `bug` `frontend` `ux`\n\n## Description\nIn `frontend/src/components/market/MarketFilters.tsx`, filter buttons for market status (Open, Locked, Resolved) update URL search parameters, but during component initialization the active filter state defaults to 'All' rather than reading the existing URL parameter. Users refreshing the page lose their selected filter context.\n\n## Complexity\n**Low**\n\n## Acceptance Criteria\n- [ ] Initialize state in `MarketFilters.tsx` from `useSearchParams().get('status')`\n- [ ] Sync weight class and category dropdowns with corresponding URL parameters\n- [ ] Ensure back and forward browser buttons update active filter pills reactively\n- [ ] Add component test verifying filter persistence across re-renders",
        "labels": [
            "bug",
            "frontend",
            "ux"
        ]
    },
    {
        "num": 86,
        "title": "#86 \u2014 Bet Confirm Modal Allows Double-Submission on Slow Mobile Networks",
        "body": "**Labels:** `bug` `frontend` `trading` `ux`\n\n## Description\nIn `frontend/src/components/bet/BetConfirmModal.tsx`, the confirm button does not disable immediately upon click. On slow mobile networks, users who tap the button multiple times trigger duplicate transaction signing prompts in Freighter, causing subsequent attempts to fail with sequence errors.\n\n## Complexity\n**Medium**\n\n## Acceptance Criteria\n- [ ] Immediately disable the confirm button and show loading spinner upon first click\n- [ ] Prevent modal dismissal via backdrop click or Escape key while transaction is in flight\n- [ ] Display clear status progression: 'Awaiting wallet signature' -> 'Submitting to Stellar' -> 'Confirmed'\n- [ ] Add test verifying confirm handler is called exactly once despite rapid multiple clicks",
        "labels": [
            "bug",
            "frontend",
            "trading",
            "ux"
        ]
    },
    {
        "num": 87,
        "title": "#87 \u2014 useWallet Hook Fails to Detect Freighter Wallet Disconnection or Account Switching",
        "body": "**Labels:** `bug` `frontend` `wallet`\n\n## Description\nIn `frontend/src/hooks/useWallet.ts`, the hook queries the wallet address upon initial mount and caches it in `localStorage`. If the user switches accounts or disconnects inside the Freighter browser extension, the frontend remains connected to the old address, leading to authorization errors when placing bets.\n\n## Complexity\n**Medium**\n\n## Acceptance Criteria\n- [ ] Listen for Freighter account change events or poll account state periodically\n- [ ] Update `useWallet` state automatically when active public key changes in extension\n- [ ] Clear cached session and reset queries when wallet disconnects\n- [ ] Add test case verifying account switch triggers state update",
        "labels": [
            "bug",
            "frontend",
            "wallet"
        ]
    },
    {
        "num": 88,
        "title": "#88 \u2014 usePlaceBet Hook Does Not Invalidate Portfolio and Market Queries on Error Rollback",
        "body": "**Labels:** `bug` `frontend` `hooks` `trading`\n\n## Description\nIn `frontend/src/hooks/usePlaceBet.ts`, optimistic updates are applied to the market odds cache when a user submits a bet. If transaction submission fails or is rejected by the user, the hook reverts local state but does not invalidate React Query caches, leaving stale odds displayed on screen.\n\n## Complexity\n**Medium**\n\n## Acceptance Criteria\n- [ ] Call `queryClient.invalidateQueries(['market', marketId])` in `onError` handler\n- [ ] Call `queryClient.invalidateQueries(['portfolio', userAddress])` on error rollback\n- [ ] Display an informative error toast explaining why the transaction failed\n- [ ] Add hook unit test verifying optimistic update rollback on transaction rejection",
        "labels": [
            "bug",
            "frontend",
            "hooks",
            "trading"
        ]
    },
    {
        "num": 89,
        "title": "#89 \u2014 useClaimWinnings Hook Does Not Check Transaction Hash Confirmation Before Updating UI",
        "body": "**Labels:** `bug` `frontend` `hooks`\n\n## Description\nIn `frontend/src/hooks/useClaimWinnings.ts`, the UI immediately marks the user's winning position as 'Claimed' as soon as the wallet submits the transaction hash. If the transaction fails on-chain due to out-of-gas or contract error, the user is left with a false 'Claimed' state and cannot re-attempt.\n\n## Complexity\n**Medium**\n\n## Acceptance Criteria\n- [ ] Wait for Horizon transaction status confirmation before marking position as claimed\n- [ ] Show 'Claiming...' pending indicator while transaction is being included in ledger\n- [ ] Revert to 'Claim Winnings' button if transaction execution status is failed\n- [ ] Add unit tests testing confirmed vs failed claim transaction responses",
        "labels": [
            "bug",
            "frontend",
            "hooks"
        ]
    },
    {
        "num": 90,
        "title": "#90 \u2014 CountdownTimer Component Causes SSR Hydration Mismatch Due to Date.now() Call",
        "body": "**Labels:** `bug` `frontend` `ux`\n\n## Description\nIn `frontend/src/components/ui/CountdownTimer.tsx`, the component calls `Date.now()` during initial render. Because the server rendering time differs from client hydration time, Next.js logs hydration mismatch warnings in the browser console: `Warning: Text content did not match. Server: ... Client: ...`.\n\n## Complexity\n**Low**\n\n## Acceptance Criteria\n- [ ] Use a `mounted` state flag with `useEffect` to render static placeholder on server and start live timer on client mount\n- [ ] Ensure server and initial client render outputs match exactly\n- [ ] Clean up `setInterval` timer on component unmount\n- [ ] Verify zero hydration mismatch warnings in Next.js development console",
        "labels": [
            "bug",
            "frontend",
            "ux"
        ]
    },
    {
        "num": 91,
        "title": "#91 \u2014 MarketCard Odds Bar Renders NaN When Total Pool Volume is Zero",
        "body": "**Labels:** `bug` `frontend` `ux`\n\n## Description\nIn `frontend/src/components/market/MarketCard.tsx`, odds calculation computes `(poolA / totalPool) * 100`. For newly created markets with zero bets where `totalPool === 0`, the calculation evaluates to `0 / 0 = NaN`, displaying 'NaN%' on the fighter card progress bar.\n\n## Complexity\n**Low**\n\n## Acceptance Criteria\n- [ ] Check `totalPool === 0` and display neutral 50/50 split (or 33/33/33 if draw enabled)\n- [ ] Display 'No bets yet' or 'Even odds' badge when pool is empty\n- [ ] Add test verifying `MarketCard` renders cleanly with 0 pool volume\n- [ ] Ensure BigInt division does not throw divide-by-zero errors",
        "labels": [
            "bug",
            "frontend",
            "ux"
        ]
    },
    {
        "num": 92,
        "title": "#92 \u2014 Portfolio Page Pagination Query Lacks Offset Validation for Out of Range Pages",
        "body": "**Labels:** `bug` `frontend` `portfolio`\n\n## Description\nIn `frontend/src/app/portfolio/page.tsx`, requesting a page number greater than `totalPages` (e.g. `?page=99`) causes the page to render broken pagination controls and an empty list without guidance. If total items shrink, users can become trapped on an empty page.\n\n## Complexity\n**Low**\n\n## Acceptance Criteria\n- [ ] Redirect to `page=1` or maximum available page if requested page exceeds `totalPages`\n- [ ] Display an empty state message with a 'Back to first page' button\n- [ ] Disable the 'Next' pagination button when `page >= totalPages`\n- [ ] Add unit tests testing pagination boundary conditions in `portfolio/__tests__/pagination.test.tsx`",
        "labels": [
            "bug",
            "frontend",
            "portfolio"
        ]
    },
    {
        "num": 93,
        "title": "#93 \u2014 Governance Proposal Voting UI Does Not Update Optimistically on Successful Vote",
        "body": "**Labels:** `enhancement` `frontend` `ux`\n\n## Description\nIn `frontend/src/app/governance/[id]/page.tsx`, casting a governance vote submits the transaction successfully, but the vote count bars and percentages do not update until the user manually hard-refreshes the page. Users frequently double-vote thinking their vote was not recorded.\n\n## Complexity\n**Medium**\n\n## Acceptance Criteria\n- [ ] Apply optimistic vote increment to active proposal state upon wallet transaction confirmation\n- [ ] Invalidate governance query cache using `queryClient.invalidateQueries(['proposal', id])`\n- [ ] Show 'Vote recorded' success banner with transaction explorer link\n- [ ] Disable voting action buttons for addresses that have already cast a vote",
        "labels": [
            "enhancement",
            "frontend",
            "ux"
        ]
    },
    {
        "num": 94,
        "title": "#94 \u2014 Create Market Form Lacks Client-Side Validation for Minimum Betting Window Duration",
        "body": "**Labels:** `bug` `frontend` `markets`\n\n## Description\nIn `frontend/src/app/create/page.tsx` and `frontend/src/schemas/createMarket.schema.ts`, the form allows selecting a fight start time in the past or less than 1 hour in the future. Users fill out the entire form and pay transaction fees only for the Soroban smart contract to reject the transaction with `MIN_MARKET_DURATION` error.\n\n## Complexity\n**Medium**\n\n## Acceptance Criteria\n- [ ] Enforce in Zod schema that `scheduled_at` must be at least 1 hour (3600 seconds) in the future\n- [ ] Set HTML datetime-local `min` attribute to current time + 1 hour\n- [ ] Display inline validation warning if selected time is too soon\n- [ ] Add test verifying form submission is blocked with invalid scheduled dates",
        "labels": [
            "bug",
            "frontend",
            "markets"
        ]
    },
    {
        "num": 95,
        "title": "#95 \u2014 Leaderboard Page Fails to Highlight Current Connected User Position",
        "body": "**Labels:** `enhancement` `frontend` `leaderboard` `ux`\n\n## Description\nIn `frontend/src/app/leaderboard/page.tsx`, the leaderboard ranks top bettors by XP and profit. When a user connects their wallet, their row is not visually highlighted, and if they are ranked outside the top 10, they cannot see their ranking without paging through all pages.\n\n## Complexity\n**Low**\n\n## Acceptance Criteria\n- [ ] Highlight the connected user's row with distinctive border and badge in the table\n- [ ] Render a sticky `YourRankCard` at the top or bottom displaying current user rank, XP, and win rate\n- [ ] Fetch user rank from `/api/engagement/leaderboard/rank` when wallet is connected\n- [ ] Add test verifying `YourRankCard` renders correctly with connected wallet",
        "labels": [
            "enhancement",
            "frontend",
            "leaderboard",
            "ux"
        ]
    },
    {
        "num": 96,
        "title": "#96 \u2014 Payer Page Lacks Input Sanitization on Stellar Public Key Input Field",
        "body": "**Labels:** `security` `frontend` `wallet`\n\n## Description\nIn `frontend/src/app/payer/page.tsx`, the recipient address field allows entering arbitrary text without validating Stellar public key formatting. Submitting an invalid address triggers an unhandled SDK error that crashes the payment flow.\n\n## Complexity\n**Low**\n\n## Acceptance Criteria\n- [ ] Validate recipient address format using `StrKey.isValidEd25519PublicKey` on input blur\n- [ ] Display inline error 'Please enter a valid Stellar address starting with G' if invalid\n- [ ] Disable submit button until both address and amount pass validation\n- [ ] Add unit tests covering valid, invalid, and empty recipient addresses",
        "labels": [
            "security",
            "frontend",
            "wallet"
        ]
    },
    {
        "num": 97,
        "title": "#97 \u2014 Toast Notification Provider Does Not Dismiss Automatically on Route Change",
        "body": "**Labels:** `bug` `frontend` `ux`\n\n## Description\nIn `frontend/src/components/ui/ToastProvider.tsx`, active toasts linger across page navigations. For example, a bet failure toast triggered on a market detail page remains stuck in the corner when navigating to the portfolio page.\n\n## Complexity\n**Low**\n\n## Acceptance Criteria\n- [ ] Listen to Next.js route change events and dismiss transient route-specific error toasts\n- [ ] Retain persistent transaction progress toasts across route transitions\n- [ ] Add auto-dismiss countdown timer (default 5 seconds) to all success/info toasts\n- [ ] Add dismiss 'X' button to all toast variants for manual dismissal",
        "labels": [
            "bug",
            "frontend",
            "ux"
        ]
    },
    {
        "num": 98,
        "title": "#98 \u2014 Dark Mode Theme Toggle Fails to Synchronize with System Color Scheme Preference",
        "body": "**Labels:** `enhancement` `frontend` `ux`\n\n## Description\nIn `frontend/src/components/layout/ThemeToggle.tsx`, theme preference is stored in `localStorage` under `theme`, but the app does not listen for system OS color scheme changes (`prefers-color-scheme`). Users whose operating system switches themes at sunset do not see the app update dynamically.\n\n## Complexity\n**Low**\n\n## Acceptance Criteria\n- [ ] Add `prefers-color-scheme` media query listener in theme provider\n- [ ] Support three modes: 'Light', 'Dark', and 'System Default'\n- [ ] Prevent initial page flash by setting class on `<html>` before hydration\n- [ ] Add unit test verifying system theme preference detection",
        "labels": [
            "enhancement",
            "frontend",
            "ux"
        ]
    },
    {
        "num": 99,
        "title": "#99 \u2014 useMarketOdds Hook Does Not Re-Subscribe to WebSocket Room After Network Reconnect",
        "body": "**Labels:** `bug` `frontend` `hooks` `websocket`\n\n## Description\nIn `frontend/src/hooks/useMarketOdds.ts`, the hook establishes a WebSocket connection and emits `join_market` to subscribe to live odds updates. If the internet drops and reconnects, the socket re-establishes connection but never re-subscribes to the active market room, leaving odds static until page reload.\n\n## Complexity\n**Medium**\n\n## Acceptance Criteria\n- [ ] Re-emit subscription messages for all active market rooms upon socket `open` event\n- [ ] Fallback to REST polling (every 10s) if WebSocket connection fails permanently\n- [ ] Display subtle visual indicator when live odds stream is disconnected\n- [ ] Add test verifying room re-subscription after simulated socket drop",
        "labels": [
            "bug",
            "frontend",
            "hooks",
            "websocket"
        ]
    },
    {
        "num": 100,
        "title": "#100 \u2014 Playwright E2E Tests Hardcode Port 3000 Without Checking Port Availability",
        "body": "**Labels:** `devops` `frontend` `testing`\n\n## Description\nIn `frontend/playwright.config.ts` and `frontend/e2e/core-flows.spec.ts`, the base URL defaults strictly to `http://localhost:3000`. In development environments where port 3000 is occupied by another app or indexer, Playwright tests run against the wrong server and fail with obscure element lookup errors.\n\n## Complexity\n**Low**\n\n## Acceptance Criteria\n- [ ] Use `process.env.PLAYWRIGHT_BASE_URL || 'http://localhost:3000'` in `playwright.config.ts`\n- [ ] Add health check verification before test suite execution in `frontend/e2e/cleanup.ts`\n- [ ] Update README with instructions on running E2E tests against custom ports\n- [ ] Verify all E2E test files use relative navigation paths",
        "labels": [
            "devops",
            "frontend",
            "testing"
        ]
    },
    {
        "num": 101,
        "title": "#101 \u2014 Bet History Table Fails to Format Stroops to XLM When Bet Amount Exceeds 1 Million",
        "body": "**Labels:** `bug` `frontend` `trading`\n\n## Description\nIn `frontend/src/components/bet/BetHistoryTable.tsx`, converting stroops to XLM uses `Number(amount) / 10_000_000`. For large bets (>100,000 XLM = >1,000,000,000,000 stroops), JavaScript floating point precision issues cause inaccurate decimal display (e.g. `100000.00000000001 XLM`).\n\n## Complexity\n**Low**\n\n## Acceptance Criteria\n- [ ] Use BigInt arithmetic or `bignumber.js` / Stellar SDK formatting helper for stroop conversions\n- [ ] Format displayed XLM with standard thousand separators and maximum 2 decimal places\n- [ ] Add test cases testing 1 stroop, 10 XLM, 1,000,000 XLM, and max stroop values\n- [ ] Ensure uniform formatting in `BetList.tsx` and `ClaimWinningsPanel.tsx`",
        "labels": [
            "bug",
            "frontend",
            "trading"
        ]
    },
    {
        "num": 102,
        "title": "#102 \u2014 Sitemap Generation Route Fails on Backend API 500 Error During Static Build",
        "body": "**Labels:** `bug` `frontend` `seo`\n\n## Description\nIn `frontend/src/app/sitemap.ts`, `sitemap()` fetches the list of active markets from `/api/markets` without a fallback catch block. If the backend is temporarily unavailable during `npm run build`, Next.js build fails completely.\n\n## Complexity\n**Low**\n\n## Acceptance Criteria\n- [ ] Wrap backend market fetching in `sitemap.ts` in try/catch block\n- [ ] Fallback to returning core static routes (`/`, `/markets`, `/portfolio`, `/leaderboard`, `/governance`) if API is unreachable\n- [ ] Log warning during build if dynamic market routes could not be generated\n- [ ] Add test in `sitemap.test.ts` verifying fallback behavior when API returns 500",
        "labels": [
            "bug",
            "frontend",
            "seo"
        ]
    },
    {
        "num": 103,
        "title": "#103 \u2014 Frontend Accessibility: Missing Aria Labels and Keyboard Traps on Modal Dialogs",
        "body": "**Labels:** `accessibility` `frontend` `ux`\n\n## Description\nIn `frontend/src/components/bet/BetConfirmModal.tsx` and `frontend/src/components/layout/HeaderMobileNav.tsx`, dialogs do not trap keyboard focus or provide `aria-labelledby` / `aria-describedby` attributes. Screen reader users and keyboard-only navigators can lose focus behind open modal backdrops.\n\n## Complexity\n**Medium**\n\n## Acceptance Criteria\n- [ ] Trap focus within modal dialogs using `focus-trap-react` or custom focus cycle hook\n- [ ] Add `role=\"dialog\"`, `aria-modal=\"true\"`, and `aria-labelledby` attributes to all modals\n- [ ] Ensure pressing `Escape` key closes active dialogs\n- [ ] Pass `@axe-core/playwright` accessibility audit without violations",
        "labels": [
            "accessibility",
            "frontend",
            "ux"
        ]
    },
    {
        "num": 104,
        "title": "#104 \u2014 Error Boundary Component Does Not Reset Query Cache on Retry Button Click",
        "body": "**Labels:** `bug` `frontend` `ux`\n\n## Description\nIn `frontend/src/components/ui/ErrorBoundary.tsx`, clicking the 'Try Again' button resets local React error boundary state but does not call `QueryErrorResetBoundary` or `queryClient.resetQueries()`. As a result, React Query immediately re-throws the cached error and returns to the error screen.\n\n## Complexity\n**Low**\n\n## Acceptance Criteria\n- [ ] Wrap error boundaries with `@tanstack/react-query` `QueryErrorResetBoundary`\n- [ ] Call `reset()` inside ErrorBoundary retry button click handler\n- [ ] Add unit test verifying clicking retry triggers query refetch\n- [ ] Verify clean recovery after network restoration",
        "labels": [
            "bug",
            "frontend",
            "ux"
        ]
    },
    {
        "num": 105,
        "title": "#105 \u2014 API Service apiFetch Lacks AbortController Timeout Cleanup on Early Return",
        "body": "**Labels:** `bug` `frontend` `performance`\n\n## Description\nIn `frontend/src/services/api.ts`, `apiFetchOnce` registers `const timeoutId = setTimeout(() => controller.abort(), TIMEOUT_MS)`. In some early return or non-standard error throw paths, `clearTimeout(timeoutId)` can be skipped, leaving pending timer handles in the browser event loop.\n\n## Complexity\n**Low**\n\n## Acceptance Criteria\n- [ ] Ensure `clearTimeout(timeoutId)` is placed strictly in a `finally` block for all fetch requests\n- [ ] Cancel active in-flight requests when components unmount using React Query cancellation signals\n- [ ] Add test verifying timers are cleared on both success and error responses\n- [ ] Verify no memory leak warnings during Jest test execution",
        "labels": [
            "bug",
            "frontend",
            "performance"
        ]
    },
    {
        "num": 106,
        "title": "#106 \u2014 Stale Markdown Summary and Fix Reports Cluttering Workspace Root Directory",
        "body": "**Labels:** `tech-debt` `docs` `devex`\n\n## Description\nThe root workspace directory contains over 20 transient fix reports and scratch text files: `DRAW_BET_FIX.md`, `FIXES_QUICK_REFERENCE.md`, `FIXES_SUMMARY.md`, `FIX_SUMMARY.md`, `IMPLEMENTATION_CHANGES.md`, `IMPLEMENTATION_SUMMARY.md`, `INDEXER_ENV_FIX.md`, `INDEXER_POLLING_RESILIENCE.md`, `ISSUES_FIXED.md`, `ISSUES_FIX_SUMMARY.md`, `RACE_CONDITION_FIX.md`, `README_FIXES.md`, `SECURITY_FIXES_SUMMARY.md`, `STELLAR_SERVER_FIX.md`, `VERIFICATION_CHECKLIST.md`, `VERIFICATION_REPORT.md`, `WORK_COMPLETE.md`, `commit_msg.txt`, and `task1.md`. These transient files obscure primary project files and should be organized into `docs/archive/` or cleaned up.\n\n## Complexity\n**Low**\n\n## Acceptance Criteria\n- [ ] Create directory `docs/archive/` and relocate historical fix reports and verification summaries into it\n- [ ] Remove scratch files like `commit_msg.txt` and `task1.md` from git tracking\n- [ ] Keep only essential top-level markdown files (`README.md`, `CONTRIBUTING.md`, `SECURITY.md`, `CHANGELOG.md`, `LICENSE`) in the repo root\n- [ ] Update `.gitignore` to prevent future temporary commit notes and markdown scratch files from being committed",
        "labels": [
            "tech-debt",
            "docs",
            "devex"
        ]
    },
    {
        "num": 107,
        "title": "#107 \u2014 docker-compose.yml Defines Duplicate indexer Service with Conflicting Ports and Volumes",
        "body": "**Labels:** `bug` `devops` `critical`\n\n## Description\nIn `docker-compose.yml`, the `indexer` service is defined twice: lines 32-42 (exposing port 3002:3002 and depending on postgres) and lines 57-68 (depending on backend, setting SOROBAN_RPC_URL, and mounting data without ports). This invalid syntax causes Docker Compose to overwrite the service definition non-deterministically and fail during startup.\n\n## Complexity\n**Medium**\n\n## Acceptance Criteria\n- [ ] Merge the two `indexer` definitions in `docker-compose.yml` into a single canonical service definition\n- [ ] Configure indexer to depend on `postgres` (condition: service_healthy) and `backend` (condition: service_started)\n- [ ] Expose port 3002:3002 and map `./indexer/.env` cleanly\n- [ ] Verify `docker compose config` validates with 0 syntax errors or duplicate key warnings",
        "labels": [
            "bug",
            "devops",
            "critical"
        ]
    },
    {
        "num": 108,
        "title": "#108 \u2014 docker-compose.yml Has Circular Dependency Between Backend and Indexer Services",
        "body": "**Labels:** `bug` `devops` `critical`\n\n## Description\nIn `docker-compose.yml`, line 51 specifies `backend` depends on `indexer: condition: service_started`, while line 60 has the second indexer definition depend on `backend: condition: service_started`. This circular dependency prevents `docker compose up` from resolving service startup ordering.\n\n## Complexity\n**Medium**\n\n## Acceptance Criteria\n- [ ] Break the circular dependency by having `indexer` depend on `postgres` and `backend` (or vice-versa)\n- [ ] Configure health checks on all dependent containers\n- [ ] Verify all containers spin up in correct topological order on a fresh machine\n- [ ] Test full stack boot with `docker compose up -d`",
        "labels": [
            "bug",
            "devops",
            "critical"
        ]
    },
    {
        "num": 109,
        "title": "#109 \u2014 Backend Dockerfile Runs Node Process as Root User Instead of node User",
        "body": "**Labels:** `security` `devops` `backend`\n\n## Description\nIn `backend/Dockerfile`, the runtime container stage executes as `root`. If an attacker exploits a remote code execution vulnerability in a dependency or endpoint, they immediately gain root access inside the container namespace.\n\n## Complexity\n**Low**\n\n## Acceptance Criteria\n- [ ] Add `USER node` directive before `CMD [\"node\", \"dist/index.js\"]` in `backend/Dockerfile`\n- [ ] Ensure `/app` directory ownership is granted to `node:node` via `chown -R node:node /app`\n- [ ] Verify the application boots and writes logs without permission errors as user `node`\n- [ ] Audit `indexer/Dockerfile` to also enforce non-root execution",
        "labels": [
            "security",
            "devops",
            "backend"
        ]
    },
    {
        "num": 110,
        "title": "#110 \u2014 Backend CI Workflow References Missing package-lock.json Causing npm ci Cache Failure",
        "body": "**Labels:** `bug` `ci-cd` `backend`\n\n## Description\nIn `.github/workflows/backend-ci.yml`, actions cache uses `key: ${{ runner.os }}-node-modules-${{ hashFiles('backend/package-lock.json') }}` and `cache-dependency-path: backend/package-lock.json`. Because `backend/package-lock.json` is missing from the repository, the cache key evaluates to an empty hash and dependency caching fails.\n\n## Complexity\n**Low**\n\n## Acceptance Criteria\n- [ ] Generate and commit `backend/package-lock.json` with resolved dependencies\n- [ ] Ensure `npm ci` in `backend-ci.yml` successfully hits cache and installs reproducibly\n- [ ] Verify GitHub Actions cache step passes without warnings\n- [ ] Add lockfile lint step in CI ensuring package.json and package-lock.json remain in sync",
        "labels": [
            "bug",
            "ci-cd",
            "backend"
        ]
    },
    {
        "num": 111,
        "title": "#111 \u2014 Backend CI Workflow References Non-Existent Load Test Script activity-feed.loadtest.js",
        "body": "**Labels:** `bug` `ci-cd` `backend` `testing`\n\n## Description\nIn `.github/workflows/backend-ci.yml`, the `load-test` job attempts to execute `k6 run tests/load/activity-feed.loadtest.js`. The directory `backend/tests/load/` and the script `activity-feed.loadtest.js` do not exist, causing the load-test CI step to fail with file not found error.\n\n## Complexity\n**Medium**\n\n## Acceptance Criteria\n- [ ] Create `backend/tests/load/activity-feed.loadtest.js` simulating 100 concurrent WebSocket connections receiving activity feed updates\n- [ ] Assert latency thresholds: p95 < 200ms and 0 error rate under simulated load\n- [ ] Verify `k6 run` executes successfully locally and in GitHub Actions\n- [ ] Document load testing guidelines in `docs/runbook.md`",
        "labels": [
            "bug",
            "ci-cd",
            "backend",
            "testing"
        ]
    },
    {
        "num": 112,
        "title": "#112 \u2014 E2E Soroban Workflow Uses Incorrect WASM File Names for Deployment",
        "body": "**Labels:** `bug` `ci-cd` `contracts`\n\n## Description\nIn `.github/workflows/e2e-soroban.yml`, lines 83 and 93 deploy `--wasm target/wasm32-unknown-unknown/release/market_factory.wasm` and `market.wasm`. Because the Cargo package names are `boxmeout-market-factory` and `boxmeout-market`, cargo produces `boxmeout_market_factory.wasm` and `boxmeout_market.wasm`. The deployment step fails because the referenced files do not exist.\n\n## Complexity\n**Low**\n\n## Acceptance Criteria\n- [ ] Update WASM paths in `e2e-soroban.yml` to `target/wasm32-unknown-unknown/release/boxmeout_market_factory.wasm` and `boxmeout_market.wasm`\n- [ ] Verify contract deployment steps in Soroban E2E workflow find the built WASM artifacts\n- [ ] Add step building backend before `node dist/index.js` in `e2e-soroban.yml`\n- [ ] Ensure full Soroban E2E workflow completes green",
        "labels": [
            "bug",
            "ci-cd",
            "contracts"
        ]
    },
    {
        "num": 113,
        "title": "#113 \u2014 Contracts CI Fuzzing Step Uses Fixed 60s Duration That Times Out in GitHub Actions",
        "body": "**Labels:** `bug` `ci-cd` `contracts` `testing`\n\n## Description\nIn `.github/workflows/contracts-ci.yml`, the `fuzz` job runs `cargo install cargo-fuzz --locked`. Compiling `cargo-fuzz` and all its dependencies from source on a standard GitHub Actions runner takes 12-15 minutes, frequently exceeding job timeout limits or burning monthly CI minutes.\n\n## Complexity\n**Medium**\n\n## Acceptance Criteria\n- [ ] Use precompiled `cargo-binstall` or pre-built binary for `cargo-fuzz` in GitHub Actions\n- [ ] Cache cargo-fuzz binary in runner cache\n- [ ] Limit fuzzing runs to scheduled nightly builds and pull requests modifying `contracts/shared/src/amm.rs`\n- [ ] Reduce fuzz step duration to 30s in PR checks",
        "labels": [
            "bug",
            "ci-cd",
            "contracts",
            "testing"
        ]
    },
    {
        "num": 114,
        "title": "#114 \u2014 Root package.json Lacks Unified Workspace Scripts for Test, Lint, and Build",
        "body": "**Labels:** `enhancement` `devex` `ci-cd`\n\n## Description\nThe root `package.json` only defines `test:e2e` and `test:integration`. Developers cloning the repository cannot run `npm run test`, `npm run lint`, or `npm run build` from the workspace root to check all packages simultaneously.\n\n## Complexity\n**Low**\n\n## Acceptance Criteria\n- [ ] Add root scripts `test`, `lint`, `build`, and `type-check` using npm workspaces or `--prefix` triggers\n- [ ] Ensure `npm test` runs backend, indexer, and frontend test suites sequentially\n- [ ] Ensure `npm run lint` lints all subprojects and reports unified status\n- [ ] Document root commands in `README.md`",
        "labels": [
            "enhancement",
            "devex",
            "ci-cd"
        ]
    },
    {
        "num": 115,
        "title": "#115 \u2014 Staging Docker Compose Configuration Missing Redis Password and Environment Secrets",
        "body": "**Labels:** `security` `devops`\n\n## Description\n`docker-compose.staging.yml` configures staging services without authentication on Redis and database instances. Anyone with network access to the staging host can connect directly to Redis without a password and read cached session tokens and user data.\n\n## Complexity\n**Medium**\n\n## Acceptance Criteria\n- [ ] Configure `requirepass ${REDIS_PASSWORD}` for Redis in `docker-compose.staging.yml`\n- [ ] Update backend and indexer environment variables to pass Redis authentication credentials\n- [ ] Ensure `.env.staging.example` includes `REDIS_PASSWORD` with strong placeholder requirement\n- [ ] Verify staging environment boots securely with password-protected Redis",
        "labels": [
            "security",
            "devops"
        ]
    },
    {
        "num": 116,
        "title": "#116 \u2014 Database Backup Scripts in backend/scripts Lack S3 or Remote Object Storage Upload",
        "body": "**Labels:** `enhancement` `devops` `reliability` `database`\n\n## Description\nIn `backend/scripts/backup-db.sh`, database backups created with `pg_dump` are saved exclusively to the local disk path `/var/backups/bankerchanger/`. If the host disk crashes or the container is terminated, all database backups are lost simultaneously with the primary database.\n\n## Complexity\n**Medium**\n\n## Acceptance Criteria\n- [ ] Add optional AWS S3 or Google Cloud Storage upload step to `backup-db.sh` using AWS CLI / rclone\n- [ ] Encrypt backup dumps with GPG / AES-256 before uploading to off-site storage\n- [ ] Add retention lifecycle pruning to delete off-site backups older than 30 days\n- [ ] Document off-site backup configuration in `backend/BACKUP_STRATEGY.md`",
        "labels": [
            "enhancement",
            "devops",
            "reliability",
            "database"
        ]
    },
    {
        "num": 117,
        "title": "#117 \u2014 Database Restore Script Does Not Validate Backup Checksum Before Restoring",
        "body": "**Labels:** `security` `devops` `database`\n\n## Description\nIn `backend/scripts/restore-db.sh`, the restore procedure accepts a backup file and immediately executes `pg_restore` into the database without checking SHA-256 integrity checksums. Restoring from a corrupted or tampered file can cause database corruption or arbitrary command execution via SQL injection in malformed dumps.\n\n## Complexity\n**Low**\n\n## Acceptance Criteria\n- [ ] Generate a `.sha256` checksum file alongside every backup in `backup-db.sh`\n- [ ] Validate `sha256sum -c` in `restore-db.sh` before executing restore operations\n- [ ] Abort restore immediately with non-zero exit code if checksum verification fails\n- [ ] Add test verifying restore script rejects corrupted backup files",
        "labels": [
            "security",
            "devops",
            "database"
        ]
    },
    {
        "num": 118,
        "title": "#118 \u2014 Staging Deployment Workflow Deploys Unverified WASM Artifacts to Network",
        "body": "**Labels:** `security` `ci-cd` `contracts`\n\n## Description\nIn `.github/workflows/deploy-staging.yml`, smart contract artifacts are built and deployed directly to the network without verifying WASM build hashes or running security audits. Deploying unverified bytecode risks deploying vulnerable contract versions to staging.\n\n## Complexity\n**High**\n\n## Acceptance Criteria\n- [ ] Add step computing SHA-256 hash of compiled WASM bytecode in `deploy-staging.yml`\n- [ ] Log and record WASM hashes in deployment summary artifact\n- [ ] Require `cargo audit` and `cargo test` to pass before deploy stage is unlocked\n- [ ] Add verification check comparing deployed bytecode hash on-chain against build output",
        "labels": [
            "security",
            "ci-cd",
            "contracts"
        ]
    },
    {
        "num": 119,
        "title": "#119 \u2014 Testnet Deployment Workflow Embeds Plaintext Deployer Key In Command Arguments",
        "body": "**Labels:** `security` `ci-cd` `devops`\n\n## Description\nIn `.github/workflows/deploy-testnet.yml`, the deployer secret key is passed as a command-line parameter: `./contracts/scripts/deploy.sh --secret ${{ secrets.STELLAR_DEPLOYER_SECRET }}`. Command-line parameters are visible to system process monitors (`ps aux`) and can be logged in CI step transcripts.\n\n## Complexity\n**High**\n\n## Acceptance Criteria\n- [ ] Pass deployer key via environment variable `STELLAR_DEPLOYER_SECRET` or temporary file rather than command-line arguments\n- [ ] Ensure deployment scripts mask secrets in all stdout / stderr outputs\n- [ ] Add secret scanner verification in CI to detect leaked private keys\n- [ ] Update `contracts/scripts/deploy.sh` to read credentials securely from environment",
        "labels": [
            "security",
            "ci-cd",
            "devops"
        ]
    },
    {
        "num": 120,
        "title": "#120 \u2014 Backup Drill Workflow Fails on Empty Database Due to Missing Initial Seed Step",
        "body": "**Labels:** `bug` `ci-cd` `database`\n\n## Description\nIn `.github/workflows/backup-restore-drill.yml`, the automated backup/restore validation drill starts PostgreSQL containers and runs backup/restore tests immediately without seeding dummy data. The drill asserts `row_count > 0`, which fails because the freshly started database is empty.\n\n## Complexity\n**Medium**\n\n## Acceptance Criteria\n- [ ] Add database migration and synthetic test data seeding step before executing backup drill\n- [ ] Verify row counts for `markets`, `bets`, and `users` before and after restore\n- [ ] Ensure `backup-restore-drill.yml` workflow runs successfully end-to-end\n- [ ] Send alert notification on drill failure to maintainers",
        "labels": [
            "bug",
            "ci-cd",
            "database"
        ]
    },
    {
        "num": 121,
        "title": "#121 \u2014 Dependabot Configuration Missing for Docker and GitHub Actions Ecosystems",
        "body": "**Labels:** `enhancement` `ci-cd` `security`\n\n## Description\nIn `.github/dependabot.yml`, Dependabot is configured only for `npm` in `backend` and `frontend`. Outdated Docker base images (e.g. `postgres:15-alpine`, `node:20-alpine`) and GitHub Actions dependencies (`actions/checkout@v4`, `actions/setup-node@v4`) do not receive automated security patches.\n\n## Complexity\n**Low**\n\n## Acceptance Criteria\n- [ ] Add `package-ecosystem: docker` for `/backend`, `/indexer`, and `/frontend` in `dependabot.yml`\n- [ ] Add `package-ecosystem: github-actions` for `/.github/workflows`\n- [ ] Add `package-ecosystem: cargo` for `/contracts`\n- [ ] Configure weekly check schedule with grouped pull requests for minor and patch updates",
        "labels": [
            "enhancement",
            "ci-cd",
            "security"
        ]
    },
    {
        "num": 122,
        "title": "#122 \u2014 Contributing Guidelines in CONTRIBUTING.md Reference Stale Branch Names and Commands",
        "body": "**Labels:** `docs` `devex`\n\n## Description\nIn `CONTRIBUTING.md`, instructions reference creating pull requests against branch `master` (the repository default branch is `main`), and recommend obsolete Soroban CLI commands (`soroban contract build` instead of `stellar contract build`). New contributors following the guide face git branch confusion and failed build instructions.\n\n## Complexity\n**Low**\n\n## Acceptance Criteria\n- [ ] Update all references from `master` to `main` across `CONTRIBUTING.md`\n- [ ] Update contract build commands to use current `stellar-cli` syntax\n- [ ] Add section explaining mono-repo folder structure and local development startup steps\n- [ ] Include links to code style guidelines and PR checklist",
        "labels": [
            "docs",
            "devex"
        ]
    },
    {
        "num": 123,
        "title": "#123 \u2014 README.md Architecture Diagram Does Not Reflect Current Dual-Service Split",
        "body": "**Labels:** `docs` `architecture`\n\n## Description\nIn `README.md`, the ASCII architecture diagram depicts the blockchain indexer as an internal component embedded inside the backend server. It does not reflect the dedicated `/indexer` standalone microservice or the real-time WebSocket event bus.\n\n## Complexity\n**Low**\n\n## Acceptance Criteria\n- [ ] Update architecture diagram in `README.md` and `docs/architecture.md` with Mermaid diagram\n- [ ] Illustrate relationships between Soroban contracts, standalone Indexer, PostgreSQL, Redis, Backend API, and Frontend\n- [ ] Add port overview table (Frontend: 3000, Backend: 3001, Indexer: 3002, Postgres: 5432, Redis: 6379)\n- [ ] Verify all links in README point to valid documentation files",
        "labels": [
            "docs",
            "architecture"
        ]
    },
    {
        "num": 124,
        "title": "#124 \u2014 Security Policy SECURITY.md Missing Responsible Disclosure PGP Key and SLA Targets",
        "body": "**Labels:** `security` `docs`\n\n## Description\nIn `SECURITY.md`, the security policy provides a generic placeholder contact email without PGP encryption keys, disclosure response SLA timelines, or bug bounty program scope details. Security researchers discovering critical smart contract or key management issues cannot submit encrypted reports.\n\n## Complexity\n**Low**\n\n## Acceptance Criteria\n- [ ] Add dedicated security contact email and public PGP key fingerprint in `SECURITY.md`\n- [ ] Define response SLAs: 24h initial response, 72h severity assessment, 7-day patch target for critical issues\n- [ ] Specify in-scope and out-of-scope targets (Smart Contracts, Backend API vs third-party RPCs)\n- [ ] Document safe harbor guidelines for ethical vulnerability research",
        "labels": [
            "security",
            "docs"
        ]
    },
    {
        "num": 125,
        "title": "#125 \u2014 .gitignore Missing Entries for Rust Target Artifacts and Playwright Test Results",
        "body": "**Labels:** `devex` `devops`\n\n## Description\nIn `.gitignore`, entries are missing for `frontend/test-results/`, `frontend/playwright-report/`, `backend/dist/`, `indexer/dist/`, `indexer/data/`, and `contracts/**/target/`. Running local tests or builds produces unstaged binary blobs and screenshot traces that clutter git status and risk accidental commits.\n\n## Complexity\n**Low**\n\n## Acceptance Criteria\n- [ ] Add Playwright test artifacts (`test-results/`, `playwright-report/`) to `.gitignore`\n- [ ] Add TypeScript compilation output directories (`**/dist/`, `**/.tsbuildinfo`) to `.gitignore`\n- [ ] Add SQLite and indexer local data files (`indexer/data/`, `*.db`, `cursor.json`) to `.gitignore`\n- [ ] Verify `git status` remains completely clean after running local build and test commands",
        "labels": [
            "devex",
            "devops"
        ]
    }
]

def ensure_labels(gh_bin, token):
    print("Verifying and creating labels...")
    for label in LABELS:
        name = label["name"]
        color = label["color"]
        desc = label.get("description", "")
        if gh_bin:
            cmd = [gh_bin, "label", "create", name, "--color", color, "--description", desc, "--repo", REPO, "--force"]
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        elif token:
            url = f"https://api.github.com/repos/{REPO}/labels"
            data = json.dumps({"name": name, "color": color, "description": desc})
            subprocess.run(["curl", "-s", "-X", "POST", "-H", f"Authorization: token {token}", "-H", "Accept: application/vnd.github.v3+json", url, "-d", data], stdout=subprocess.DEVNULL)
    print("All labels verified.")

def create_issue_api(gh_bin, token, title, body, labels):
    payload = json.dumps({"title": title, "body": body, "labels": labels})
    if gh_bin:
        cmd = [gh_bin, "api", f"repos/{REPO}/issues", "--input", "-"]
        proc = subprocess.run(cmd, input=payload, text=True, capture_output=True)
        return proc.returncode == 0, proc.stdout, proc.stderr
    elif token:
        url = f"https://api.github.com/repos/{REPO}/issues"
        proc = subprocess.run(
            ["curl", "-s", "-w", "\n%{http_code}", "-X", "POST",
             "-H", f"Authorization: token {token}",
             "-H", "Accept: application/vnd.github.v3+json",
             url, "-d", payload],
            capture_output=True, text=True
        )
        lines = proc.stdout.strip().split("\n")
        code = lines[-1] if lines else "500"
        body_resp = "\n".join(lines[:-1])
        return code in ["200", "201"], body_resp, f"HTTP {code}"
    return False, "", "No gh CLI or GH_TOKEN found"

def main():
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    gh_bin = subprocess.run(["which", "gh"], capture_output=True, text=True).stdout.strip()
    if not gh_bin and os.path.exists(os.path.expanduser("~/.local/bin/gh")):
        gh_bin = os.path.expanduser("~/.local/bin/gh")

    print(f"Total issues to process: {len(ISSUES)}")
    ensure_labels(gh_bin, token)

    success_count = 0
    failed = []

    print(f"\nStarting creation and push of {len(ISSUES)} issues to {REPO}...")
    for idx, item in enumerate(ISSUES, 1):
        title = item["title"]
        body = item["body"]
        labels = item["labels"]

        retries = 3
        created = False
        while retries > 0 and not created:
            ok, out, err = create_issue_api(gh_bin, token, title, body, labels)
            if ok:
                try:
                    res_json = json.loads(out)
                    issue_num = res_json.get("number", "N/A")
                    print(f"[{idx}/{len(ISSUES)}] Created issue #{issue_num}: {title}")
                except Exception:
                    print(f"[{idx}/{len(ISSUES)}] Created issue: {title}")
                success_count += 1
                created = True
            else:
                if "rate limit" in (out + err).lower() or "secondary" in (out + err).lower() or "403" in (out + err) or "429" in (out + err):
                    print(f"[{idx}/{len(ISSUES)}] Rate limit hit, backing off 10s...")
                    time.sleep(10)
                else:
                    print(f"[{idx}/{len(ISSUES)}] Error creating '{title}': {err[:150]}")
                    time.sleep(2)
                retries -= 1

        if not created:
            failed.append((idx, title))

        # 1-second delay to comply with GitHub secondary rate limits
        time.sleep(1.0)

    print(f"\n==================================================")
    print(f"Finished! Successfully created {success_count} / {len(ISSUES)} issues on {REPO}.")
    if failed:
        print(f"Failed issues ({len(failed)}): {failed}")
    print(f"==================================================")

if __name__ == "__main__":
    main()
