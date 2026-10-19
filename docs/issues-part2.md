# BANKERCHANGER — Issues Part 2 (continuing from #48)

> Global numbering: Backend #1–40 · Frontend #41–80 · Contracts #81–120
> Part 1 ended at Issue #48 (Frontend #8 — HomePage).
> Labels follow the same guide defined in the per-area issue files.

---

## Issue #49 — Implement `MarketCard` component

**Labels:** `good first issue` `frontend`

**File:** `frontend/src/components/market/MarketCard.tsx`

**Description**
Render a clickable card summarising a single market.

**What to render**
- Fighter A vs Fighter B heading
- Weight class badge; title fight crown icon if `title_fight === true`
- `MarketStatusBadge`
- `MarketOddsBar` (pool proportions)
- `CountdownTimer`
- Total pooled XLM (format: "12,400 XLM")
- Entire card wrapped in `<Link href={/markets/${market.market_id}}>`

**Acceptance Criteria**
- [ ] Clicking card navigates to correct market detail page
- [ ] All data points rendered
- [ ] Responsive: card readable on 375px viewport

---

## Issue #50 — Implement `MarketOddsBar` component

**Labels:** `frontend` `intermediate`

**File:** `frontend/src/components/market/MarketOddsBar.tsx`

**Description**
Three-segment horizontal bar showing pool proportions.

**What to render**
- Segments: [Fighter A][Draw][Fighter B], widths proportional to pool sizes
- If `total_pool == 0`: render equal thirds (33/33/33)
- Show percentage label inside each segment (hide if segment < 10% wide)
- Animate width changes with `transition: width 0.4s ease`

**Acceptance Criteria**
- [ ] Correct proportions for known pool values
- [ ] Equal thirds for empty pools (no divide-by-zero)
- [ ] Smooth animation on odds change
- [ ] BigInt used for pool math (no floating point)

---

## Issue #51 — Implement `MarketStatusBadge` component

**Labels:** `good first issue` `frontend`

**File:** `frontend/src/components/market/MarketStatusBadge.tsx`

**Description**
Pill badge with colour-coded market status.

**Color mapping**
- `open` → green
- `locked` → amber
- `resolved` → blue
- `cancelled` → gray
- `disputed` → red

**Acceptance Criteria**
- [ ] Correct colour for each status
- [ ] Text capitalised ("Open", "Locked", etc.)
- [ ] Pill/badge shape with readable contrast

---

## Issue #52 — Implement `CountdownTimer` component

**Labels:** `good first issue` `frontend`

**File:** `frontend/src/components/ui/CountdownTimer.tsx`

**Description**
Countdown display using `useMarketCountdown` internally.

**States**
- Counting down: "Starts in 2h 14m 32s"
- At `scheduled_at`: pulsing red "LIVE" badge
- After resolution window: gray "ENDED"

**Acceptance Criteria**
- [ ] Updates every second while counting down
- [ ] Shows LIVE state correctly
- [ ] Cleans up timer on unmount

---

## Issue #53 — Implement `useMarketCountdown` hook

**Labels:** `good first issue` `frontend`

**File:** `frontend/src/hooks/useMarketCountdown.ts`

**Description**
Drives the countdown display with a 1-second interval.

**What to implement**
- Compute initial countdown string on mount
- `setInterval(fn, 1000)` to update every second
- Format: `Xh Ym Zs` — omit hours if 0, omit minutes if 0 and hours are 0
- Return "LIVE" when `Date.now() >= scheduled_at_ms && Date.now() < scheduled_at_ms + resolution_window_ms`
- Return "ENDED" after resolution window (`scheduled_at + 24h` as safe default)
- Clean up interval in `useEffect` return

**Acceptance Criteria**
- [ ] Accurate countdown with correct format
- [ ] State transitions to LIVE and ENDED at correct times
- [ ] No memory leak — interval cleaned up on unmount

---

## Issue #54 — Implement `fetchMarketById()` in api.ts

**Labels:** `good first issue` `frontend`

**File:** `frontend/src/services/api.ts`

**Description**
Typed fetch wrapper for a single market.

**What to implement**
- `fetch(`${API_BASE}/api/markets/${market_id}`)`
- Parse JSON as `Market`
- Throw `NotFoundError` on 404
- Throw `NetworkError` on other non-200 responses

**Acceptance Criteria**
- [ ] Returns typed Market on success
- [ ] Throws `NotFoundError` on 404
- [ ] Handles network failures gracefully

---

## Issue #55 — Implement `useMarket` hook

**Labels:** `frontend` `intermediate`

**File:** `frontend/src/hooks/useMarket.ts`

**Description**
Fetches and live-polls a single market's data.

**What to implement**
- Fetch market on mount via `fetchMarketById(market_id)`
- If `market.status === 'open'`: poll every 10 seconds for updated odds
- Stop polling when status changes to locked/resolved/cancelled
- Return `{ market, isLoading, error }`

**Acceptance Criteria**
- [ ] Live odds update every 10s while market is open
- [ ] Polling stops automatically when market is no longer open
- [ ] 404 sets error state (does not crash page)

---

## Issue #56 — Implement `MarketDetailPage`

**Labels:** `frontend` `advanced`

**File:** `frontend/src/app/markets/[market_id]/page.tsx`

**Description**
Full detail view for a single market.

**Page sections**
1. Fight header: fighter names, weight class badge, title fight indicator, venue
2. `CountdownTimer` + `MarketStatusBadge`
3. `MarketOddsBar` — updates live
4. Pool sizes: "12,400 XLM on Fury | 800 XLM Draw | 5,200 XLM on Usyk"
5. `BetPanel` — right column on desktop, below pools on mobile
6. Recent bets table: last 20 bets, newest first (bettor address truncated, side, amount, time)
7. Oracle info section: visible after resolution — oracle address, tx hash link, outcome

**Acceptance Criteria**
- [ ] All sections render with correct data
- [ ] 404 message shown for unknown `market_id`
- [ ] Two-column layout on desktop; single column on mobile

---

## Issue #57 — Implement `BetPanel` component

**Labels:** `frontend` `advanced`

**File:** `frontend/src/components/bet/BetPanel.tsx`

**Description**
The primary betting UI on the market detail page.

**What to render**
- Three toggle buttons: [Fighter A] [Draw] [Fighter B] — selected state highlighted
- Amount input in XLM with min/max hints
- Estimated payout preview (updates live as inputs change)
- Fee display: "Platform fee: 2%"
- Submit button — disabled when: no wallet connected, amount invalid, `isSubmitting`
- "Connect Wallet to Bet" prompt when wallet not connected
- "Betting is closed" message when market is not Open
- `TxStatusToast` after submission

**Acceptance Criteria**
- [ ] Full bet flow works end-to-end on testnet
- [ ] Payout preview updates with each keystroke
- [ ] Submit button correctly disabled in all invalid states

---

## Issue #58 — Implement `useBet` hook

**Labels:** `frontend` `advanced`

**File:** `frontend/src/hooks/useBet.ts`

**Description**
Manages all state for the bet placement flow.

**What to implement**
- `side` state: `null | 'fighter_a' | 'fighter_b' | 'draw'`
- `amount` state: string (raw input value)
- `estimatedPayout`: recompute on side/amount change using local parimutuel formula (no API call per keystroke)
- `submitBet()`: show confirmation modal → on confirm → call `wallet.submitBet()` → update `txStatus`
- `reset()`: clear all form state after successful bet

**Acceptance Criteria**
- [ ] Estimated payout recalculates on input change without API call
- [ ] `txStatus` transitions: idle → pending → success/error
- [ ] Reset clears form correctly

---

## Issue #59 — Implement `BetConfirmModal` component

**Labels:** `frontend` `intermediate`

**File:** `frontend/src/components/bet/BetConfirmModal.tsx`

**Description**
Confirmation modal before submitting a bet transaction.

**What to render**
- Overlay backdrop (semi-transparent)
- Modal card: "Confirm your bet" title, fighter chosen, bet amount, platform fee, estimated net payout
- "Confirm Bet" button → calls `onConfirm()`
- "Cancel" button → calls `onCancel()`

**Behavior**
- Close on backdrop click
- Close on Escape key
- Rendered as a React portal (`document.body`)

**Acceptance Criteria**
- [ ] Closes on backdrop click and Escape key
- [ ] Correct values displayed for all fields
- [ ] Accessible: focus trapped inside modal while open

---

## Issue #60 — Implement `submitBet()` in wallet.ts

**Labels:** `frontend` `advanced`

**File:** `frontend/src/services/wallet.ts`

**Description**
Builds, signs, and submits the `place_bet` contract invocation.

**What to implement**
- Convert `amount_xlm` to stroops via `xlmToStroops()`
- Build XDR for `InvokeContractHostFunction` calling `place_bet` on the market contract
- Sign via `freighter.signTransaction(xdr, { network: STELLAR_NETWORK })`
- Submit signed XDR to Stellar (via Horizon or backend proxy at `POST /api/tx/submit`)
- Poll for tx confirmation (max 30s)
- Return tx hash on SUCCESS

**Acceptance Criteria**
- [ ] Bet successfully placed and confirmed on Stellar testnet
- [ ] Throws `WalletSignError` if user rejects signing
- [ ] Throws `TxSubmissionError` on network rejection

---

## Issue #61 — Implement `TxStatusToast` component

**Labels:** `frontend` `intermediate`

**File:** `frontend/src/components/ui/TxStatusToast.tsx`

**Description**
Toast notification showing transaction status.

**States**
- `idle`: render nothing
- `pending`: spinner + "Transaction pending..."
- `success`: green check + "Bet placed!" + Stellar Explorer link
- `error`: red X + error message + "Try again" suggestion

**Behavior**
- Fixed position: bottom-right of screen
- Auto-dismiss after 6 seconds on success
- Stays visible until dismissed on error
- Dismiss button (×) always visible

**Explorer link**
- Testnet: `https://stellar.expert/explorer/testnet/tx/{hash}`
- Mainnet: `https://stellar.expert/explorer/public/tx/{hash}`

**Acceptance Criteria**
- [ ] All four states render correctly
- [ ] Auto-dismiss timer clears on unmount
- [ ] Explorer link opens in new tab

---

## Issue #62 — Implement `PortfolioPage`

**Labels:** `frontend` `intermediate`

**File:** `frontend/src/app/portfolio/page.tsx`

**Description**
User's personal betting dashboard.

**Page sections**
1. Stats row: Total Staked / Total Won / Total Lost / Win Rate % (in XLM)
2. "Pending Claims" section — golden highlight; Claim buttons
3. "Active Bets" — bets in open/locked markets
4. "Bet History" — `BetHistoryTable` with all past bets

**No wallet state**
- Full-page prompt: "Connect your wallet to view your portfolio"
- Connect button centered on page

**Empty portfolio**
- "No bets yet — find a fight to bet on" with link to `/`

**Acceptance Criteria**
- [ ] Correct connect prompt when wallet not connected
- [ ] Correct empty state when portfolio is empty
- [ ] Claim buttons work and refresh portfolio after confirmation

---

## Issue #63 — Implement `usePortfolio` hook

**Labels:** `frontend` `advanced`

**File:** `frontend/src/hooks/usePortfolio.ts`

**Description**
Fetches and manages portfolio data and claim actions.

**What to implement**
- Get address from `useWallet()`
- Fetch portfolio via `fetchPortfolio(address)` on mount and when address changes
- `claimWinnings(market_contract_address)`: call `wallet.submitClaim()`, then refetch portfolio
- `claimRefund(market_contract_address)`: call `wallet.submitRefund()`, then refetch portfolio
- Track claim tx status via `claimTxStatus`

**Acceptance Criteria**
- [ ] Portfolio null when wallet not connected
- [ ] Portfolio refreshes after successful claim
- [ ] `claimTxStatus` reflects pending/success/error

---

## Issue #64 — Implement `BetHistoryTable` component

**Labels:** `frontend` `intermediate`

**File:** `frontend/src/components/bet/BetHistoryTable.tsx`

**Description**
Tabular view of all user bets.

**Columns:** Market | Side | Amount (XLM) | Status | Payout (XLM) | Action

**Action column rules**
- Winning + unclaimed → "Claim" button (calls `onClaim`)
- Cancelled market + unclaimed → "Refund" button (calls `onRefund`)
- Already claimed → payout amount in green text
- Lost bet → "—" (no action)
- Market not yet resolved → "Pending" badge

**Acceptance Criteria**
- [ ] Correct action for each bet state
- [ ] Empty state shows "No bets yet" message
- [ ] Responsive: scrollable horizontally on mobile

---

## Issue #65 — Implement `fetchPortfolio()` in api.ts

**Labels:** `good first issue` `frontend`

**File:** `frontend/src/services/api.ts`

**Description**
Typed fetch wrapper for portfolio data.

**What to implement**
- `fetch(`${API_BASE}/api/portfolio/${address}`)`
- Parse JSON as `Portfolio`
- Throw `NetworkError` on non-200

**Acceptance Criteria**
- [ ] Returns typed Portfolio
- [ ] Handles network errors with informative message

---

## Issue #66 — Implement `submitClaim()` in wallet.ts

**Labels:** `frontend` `advanced`

**File:** `frontend/src/services/wallet.ts`

**Description**
Builds and submits the `claim_winnings` contract invocation.

**What to implement**
- Build XDR for `InvokeContractHostFunction` calling `claim_winnings` on the market contract
- Use connected wallet address as the `bettor` argument
- Sign and submit via Freighter (same flow as `submitBet`)
- Return tx hash on confirmation

**Acceptance Criteria**
- [ ] Payout received in wallet after confirmation on testnet
- [ ] Throws on user rejection or network failure

---

## Issue #67 — Implement `submitRefund()` in wallet.ts

**Labels:** `frontend` `advanced`

**File:** `frontend/src/services/wallet.ts`

**Description**
Builds and submits the `claim_refund` contract invocation.

**What to implement**
- Build XDR for `InvokeContractHostFunction` calling `claim_refund` on the market contract
- Sign and submit via Freighter
- Return tx hash on confirmation

**Acceptance Criteria**
- [ ] Full stake refunded to wallet after confirmation
- [ ] Throws clearly on failure

---

## Issue #68 — Implement `CreateMarketPage` (admin)

**Labels:** `frontend` `advanced` `admin`

**File:** `frontend/src/app/create/page.tsx`

**Description**
Admin-only page for creating new markets.

**Form fields**
- Match ID, Fighter A, Fighter B, Weight Class (select), Venue, Title Fight (checkbox)
- Scheduled At (datetime-local input)
- Min Bet (XLM), Max Bet (XLM), Fee % (0–10), Lock Before Fight (minutes)

**Submit flow**
1. Validate all fields
2. Convert XLM values to stroops
3. Build `create_market` contract invocation
4. Sign + submit via `wallet.ts`
5. Show `TxStatusToast`
6. Redirect to `/markets/[new_market_id]` on success

**Access guard**
- Wallet not connected → show connect prompt
- Connected address not in `NEXT_PUBLIC_ADMIN_ADDRESSES` → show "Access denied"

**Acceptance Criteria**
- [ ] Form validation prevents submission of invalid data
- [ ] Admin guard works correctly
- [ ] Successful market creation redirects to detail page

---

## Issue #69 — Implement wallet connect prompt for unauthenticated actions

**Labels:** `good first issue` `frontend`

**File:** `frontend/src/components/ui/ConnectPrompt.tsx`

**Description**
Reusable prompt shown when wallet-required action attempted without connection.

**What to render**
- Message: "Connect your Freighter wallet to place bets"
- "Connect Wallet" button — triggers `useWallet().connect()`
- Link to Freighter install page: "Don't have Freighter? Get it here →"

**Where to use it**
- Inside `BetPanel` when wallet not connected
- On `PortfolioPage` when wallet not connected

**Acceptance Criteria**
- [ ] Component is reusable (accepts optional `message` prop)
- [ ] Clicking connect triggers wallet flow
- [ ] Freighter install link opens in new tab

---

## Issue #70 — Add loading skeleton components

**Labels:** `good first issue` `frontend`

**File:** `frontend/src/components/ui/Skeleton.tsx`

**Description**
Skeleton placeholder components for loading states.

**Skeletons to create**
- `MarketCardSkeleton`: same dimensions as `MarketCard`, pulsing gray blocks
- `BetPanelSkeleton`: placeholder for `BetPanel` content
- `StatsRowSkeleton`: placeholder for portfolio stats row

**Implementation note**
Use Tailwind's `animate-pulse` class on gray rounded blocks.
Do NOT use a third-party skeleton library.

**Acceptance Criteria**
- [ ] Skeletons match dimensions of their real components
- [ ] Home page shows `MarketCardSkeleton` grid on initial load
- [ ] No layout shift when real content loads

---

## Issue #71 — Implement weight class filter on Home page

**Labels:** `frontend` `intermediate`

**File:** `frontend/src/app/page.tsx`

**Description**
Add weight class filter dropdown to market list.

**Weight classes to include**
Heavyweight, Light Heavyweight, Super Middleweight, Middleweight, Super Welterweight, Welterweight, Super Lightweight, Lightweight, Super Featherweight, Featherweight, Super Bantamweight, Bantamweight, Super Flyweight, Flyweight, Minimumweight

**What to implement**
- `<select>` dropdown with "All Weight Classes" as default
- On change: update filter state → triggers new `fetchMarkets()` call
- Selected filter persisted in URL query param `?weight_class=Heavyweight`

**Acceptance Criteria**
- [ ] Selecting a weight class filters the market list
- [ ] Refreshing the page restores the filter from URL
- [ ] "All Weight Classes" shows unfiltered list

---

## Issue #72 — Add Testnet / Mainnet network indicator

**Labels:** `frontend` `intermediate`

**File:** `frontend/src/components/layout/Header.tsx`

**Description**
Display clear network indicator and warn users on mainnet.

**What to implement**
- Read `NEXT_PUBLIC_STELLAR_NETWORK` env var
- Show badge in Header: "TESTNET" (amber) or "MAINNET" (green)
- On mainnet: show dismissable banner at top of page: "You are betting with real XLM on mainnet"
- Store dismiss state in `sessionStorage` (reappears on new session)

**Acceptance Criteria**
- [ ] Testnet badge shown in development
- [ ] Mainnet banner appears and can be dismissed
- [ ] Banner reappears after closing and reopening the browser

---

## Issue #73 — Implement error boundary for market detail page

**Labels:** `frontend` `intermediate`

**File:** `frontend/src/components/ui/ErrorBoundary.tsx`

**Description**
React error boundary wrapping `MarketDetailPage` content.

**What to implement**
- Class component implementing `componentDidCatch`
- Fallback UI: "Something went wrong loading this market." with a "Try again" button calling `window.location.reload()`
- Wrap main content of `MarketDetailPage` with it

**Acceptance Criteria**
- [ ] App does not crash on unexpected render error
- [ ] Fallback UI shown with retry button
- [ ] Error logged to console (or error tracking service)

---

## Issue #74 — Implement responsive layout for mobile

**Labels:** `frontend` `intermediate`

**Description**
Ensure all pages are fully usable on a 375px viewport (iPhone SE size).

**Pages to verify and fix**
- Home page: market grid becomes single column
- Market Detail: `BetPanel` moves below odds bar; recent bets table scrolls horizontally
- Portfolio: stats row stacks vertically; `BetHistoryTable` scrolls horizontally
- Header: nav collapses to hamburger menu

**Acceptance Criteria**
- [ ] No horizontal scroll on any page at 375px
- [ ] All interactive elements reachable and tappable (min 44×44px touch targets)
- [ ] Text readable (min 14px)

---

## Issue #75 — Add XLM / stroops conversion utilities

**Labels:** `good first issue` `frontend`

**File:** `frontend/src/services/wallet.ts`

**Description**
Integer-safe conversion helpers between XLM and stroops.

**What to implement**
```typescript
// 1 XLM = 10_000_000 stroops — integer arithmetic only
xlmToStroops(xlm: number): bigint
stroopsToXlm(stroops: bigint | string): number
```

**Acceptance Criteria**
- [ ] `xlmToStroops(1)` returns `10000000n`
- [ ] `xlmToStroops(0.0000001)` returns `1n`
- [ ] `stroopsToXlm(10000000n)` returns `1`
- [ ] `stroopsToXlm("123456789")` returns `12.3456789`
- [ ] Unit tests for edge cases (very small and very large amounts)

---

## Issue #76 — Add Stellar Explorer deep links

**Labels:** `good first issue` `frontend`

**File:** `frontend/src/utils/stellarExplorer.ts`

**Description**
Utility for generating correct Stellar Explorer URLs.

**What to implement**
```typescript
function stellarExplorerUrl(type: 'tx' | 'account' | 'contract', id: string): string
```
Returns the correct URL based on `NEXT_PUBLIC_STELLAR_NETWORK`.

**Where to use**
- `TxStatusToast`: tx hash link
- Market detail page: oracle address link, resolution tx link
- Portfolio page: tx hash links in bet history

**Acceptance Criteria**
- [ ] Testnet links point to `stellar.expert/explorer/testnet/`
- [ ] Mainnet links point to `stellar.expert/explorer/public/`
- [ ] All explorer links open in new tab with `rel="noopener noreferrer"`

---

## Issue #77 — Write unit tests for `useMarkets` and `useMarket` hooks

**Labels:** `frontend` `testing` `intermediate`

**Description**
Unit tests for both hooks using `@testing-library/react` and `msw`.

**Test cases for `useMarkets`**
- [ ] Initial loading state is true
- [ ] Markets populated after successful fetch
- [ ] Error state set on failed fetch
- [ ] `refetch()` triggers a new fetch

**Test cases for `useMarket`**
- [ ] Loading state transitions correctly
- [ ] Polling starts for open market
- [ ] Polling stops when market becomes locked

**Acceptance Criteria**
- [ ] Tests pass with mocked API (no real backend needed)
- [ ] No real timers (use `jest.useFakeTimers()`)

---

## Issue #78 — Write E2E test for bet placement flow

**Labels:** `frontend` `testing` `advanced`

**Description**
Playwright end-to-end test covering the complete bet placement flow.

**Flow to test**
1. Navigate to home page — verify market list loads
2. Click a market card — verify detail page loads
3. Click "Connect Wallet" — mock Freighter connection
4. Select Fighter A in `BetPanel`
5. Enter 10 XLM
6. Verify estimated payout appears
7. Click "Place Bet" — verify confirm modal opens
8. Click "Confirm Bet" — mock Stellar tx submission
9. Verify `TxStatusToast` shows success with tx hash

**Acceptance Criteria**
- [ ] E2E test passes against a running dev environment
- [ ] Freighter wallet mocked (no real browser extension required)
- [ ] Tx submission mocked (no real Stellar network required)

---

## Issue #79 — Implement Zustand store for global app state

**Labels:** `frontend` `intermediate`

**File:** `frontend/src/store/index.ts`

**Description**
Global Zustand store (stub currently has a `TODO` body).

**What to implement**
- Initial state: `walletAddress: null`, `walletBalance: null`, `isConnecting: false`, `network: "testnet"`, `lastTxStatus: { hash: null, status: "idle", error: null }`
- `setWallet(address, balance)`: update wallet state
- `clearWallet()`: reset wallet state to null
- `setNetwork(network)`: update network
- `setTxStatus(status)`: update `lastTxStatus`

**Acceptance Criteria**
- [ ] Store accessible across all components without prop drilling
- [ ] State persists within a session (not to localStorage — wallet hook handles that)
- [ ] All actions produce correct state

---

## Issue #80 — Set up Storybook for UI components

**Labels:** `frontend` `devops` `intermediate`

**Description**
Set up Storybook 8 and add stories for core UI components.

**What to implement**
- `npx storybook@latest init` in the frontend directory
- Add stories for:
  - `MarketCard` (open, locked, resolved, cancelled variants)
  - `MarketOddsBar` (equal pools, dominant one side, empty pools)
  - `MarketStatusBadge` (all 5 statuses)
  - `CountdownTimer` (counting down, LIVE, ENDED)
  - `TxStatusToast` (all 4 states)
  - `BetPanel` (wallet connected, wallet disconnected, market locked)

**Acceptance Criteria**
- [ ] `npm run storybook` launches Storybook at port 6006
- [ ] All listed stories render without errors
- [ ] Stories work without a backend connection (all data hardcoded in story args)

---

## Issue #81 — Initialize MarketFactory contract

**Labels:** `good first issue` `smart-contract`

**File:** `contracts/market_factory/src/lib.rs` → `fn initialize`

**Description**
Sets up the factory for the first time after deployment.

**What to implement**
- Store `admin` in `ADMIN` storage key
- Store `oracles` Vec in `ORACLE_WHITELIST` storage key
- Store a default `MarketConfig` derived from `default_fee_bps`
- Set `PAUSED = false`
- Return `ContractError::AlreadyInitialized` if called a second time

**Acceptance Criteria**
- [ ] Factory stores admin, oracles, paused = false on first call
- [ ] Second call returns `AlreadyInitialized`
- [ ] Unit test covers both cases

---

## Issue #82 — Implement `create_market()` in MarketFactory

**Labels:** `smart-contract` `intermediate`

**File:** `contracts/market_factory/src/lib.rs` → `fn create_market`

**Description**
Deploys a fresh Market contract instance and registers it.

**What to implement**
- Reject if factory is paused
- Validate fight details (scheduled_at in the future, non-empty fighter names)
- Validate config (min_bet > 0, fee_bps ≤ 1000)
- Deploy new Market wasm via `env.deployer()`
- Call `Market::initialize()` on the new contract
- Store `market_id → contract_address` in `MARKET_MAP`
- Increment `MARKET_COUNT`
- Emit `MarketCreated` event
- Return the new `market_id`

**Acceptance Criteria**
- [ ] New market address stored in `MARKET_MAP`
- [ ] `MARKET_COUNT` incremented after each call
- [ ] `MarketCreated` event emitted with correct payload
- [ ] Invalid inputs return correct `ContractError`

---

## Issue #83 — Implement `get_market_address()`

**Labels:** `good first issue` `smart-contract`

**File:** `contracts/market_factory/src/lib.rs` → `fn get_market_address`

**Description**
Lookup a market's contract address by ID.

**What to implement**
- Read `MARKET_MAP` from storage
- Return the `Address` for the given `market_id`
- Return `ContractError::MarketNotFound` if ID is not in the map

**Acceptance Criteria**
- [ ] Returns correct address for valid ID
- [ ] Returns `MarketNotFound` for unknown ID
- [ ] Unit test covers both cases

---

## Issue #84 — Implement `list_markets()` with pagination

**Labels:** `smart-contract` `intermediate`

**File:** `contracts/market_factory/src/lib.rs` → `fn list_markets`

**Description**
Paginated list of markets with their current status.

**What to implement**
- Read `MARKET_MAP` and cross-reference `MARKET_COUNT`
- Apply `offset` and `limit` (cap limit at 100 on-chain)
- For each market in range, read its status via cross-contract call
- Return `Vec<(u64, MarketStatus)>`

**Acceptance Criteria**
- [ ] Returns correct slice for any valid offset/limit
- [ ] Returns empty Vec for offset beyond `MARKET_COUNT`
- [ ] Limit is capped at 100

---

## Issue #85 — Implement `add_oracle()` and `remove_oracle()`

**Labels:** `smart-contract` `intermediate`

**File:** `contracts/market_factory/src/lib.rs`

**Description**
Oracle whitelist management functions.

**What to implement**
- `add_oracle()`: require admin auth; append to `ORACLE_WHITELIST` if not already present (idempotent)
- `remove_oracle()`: require admin auth; remove from list; return `OracleNotWhitelisted` if not found

**Acceptance Criteria**
- [ ] Only admin can call either function; non-admin returns `Unauthorized`
- [ ] `add_oracle` is idempotent
- [ ] `remove_oracle` returns `OracleNotWhitelisted` for unknown address
- [ ] Unit tests for both happy paths and error paths

---

## Issue #86 — Implement `transfer_admin()`

**Labels:** `smart-contract` `intermediate`

**File:** `contracts/market_factory/src/lib.rs` → `fn transfer_admin`

**Description**
Transfers factory admin rights to a new address.

**What to implement**
- Require `current_admin` authorization
- Update `ADMIN` storage key to `new_admin`
- Emit `AdminTransferred` event

**Acceptance Criteria**
- [ ] Old admin loses rights after transfer
- [ ] New admin can call admin-only functions
- [ ] Non-admin call returns `Unauthorized`
- [ ] Event emitted with both addresses

---

## Issue #87 — Implement `pause_factory()` and `unpause_factory()`

**Labels:** `good first issue` `smart-contract`

**File:** `contracts/market_factory/src/lib.rs`

**Description**
Circuit breaker functions for the factory.

**What to implement**
- `pause_factory()`: set `PAUSED = true`; require admin auth
- `unpause_factory()`: set `PAUSED = false`; require admin auth
- `is_paused()`: read and return `PAUSED`

**Acceptance Criteria**
- [ ] Paused factory rejects `create_market()` with `FactoryPaused`
- [ ] `unpause_factory()` restores normal operation
- [ ] Only admin can pause/unpause

---

## Issue #88 — Implement Market contract `initialize()`

**Labels:** `smart-contract` `intermediate`

**File:** `contracts/market/src/lib.rs` → `fn initialize`

**Description**
Sets up a freshly deployed Market contract.

**What to implement**
- Verify caller is the factory contract stored at deploy time
- Build initial `MarketState` with status = Open, all pools = 0
- Store STATE, empty BETS map, empty BETTOR_LIST
- Store FACTORY address
- Return `AlreadyInitialized` on second call

**Acceptance Criteria**
- [ ] State stored correctly with all zero pools
- [ ] Second call returns `AlreadyInitialized`
- [ ] Non-factory caller returns `NotFactory`

---

## Issue #89 — Implement `place_bet()` in Market

**Labels:** `smart-contract` `intermediate`

**File:** `contracts/market/src/lib.rs` → `fn place_bet`

**Description**
Core betting function.

**What to implement**
- Validate market status == Open
- Validate current time is before lock threshold
- Validate amount ≥ min_bet and ≤ max_bet
- Transfer token from bettor to contract
- Append `BetRecord` to `BETS[bettor]`
- Add bettor to `BETTOR_LIST` if first bet
- Update the correct pool and `total_pool`
- Emit `BetPlaced` event
- Return the `BetRecord`

**Acceptance Criteria**
- [ ] Correct pool incremented on each side
- [ ] `BetPlaced` event emitted with correct payload
- [ ] All invalid calls return correct `ContractError`
- [ ] Token transfer executed before state mutation

---

## Issue #90 — Implement bet timing lock validation

**Labels:** `good first issue` `smart-contract`

**File:** `contracts/market/src/lib.rs` → inside `fn place_bet`

**Description**
Time-lock check preventing bets after the lock threshold.

**What to implement**
- Compute lock threshold: `fight.scheduled_at - config.lock_before_secs`
- If `env.ledger().timestamp() >= lock_threshold`, return `ContractError::BettingClosed`

**Acceptance Criteria**
- [ ] Bets placed before threshold succeed
- [ ] Bets placed at or after threshold return `BettingClosed`
- [ ] Unit test covers boundary condition (exactly at threshold)

---

## Issue #91 — Implement `lock_market()`

**Labels:** `good first issue` `smart-contract`

**File:** `contracts/market/src/lib.rs` → `fn lock_market`

**Description**
Transitions market from Open to Locked.

**What to implement**
- Verify caller is a whitelisted oracle or admin
- Verify current time >= lock threshold
- Set status to Locked
- Emit `MarketLocked` event

**Acceptance Criteria**
- [ ] Only callable after lock threshold
- [ ] Status transitions Open → Locked
- [ ] `MarketLocked` event emitted
- [ ] Already-locked market returns `InvalidMarketStatus`

---

## Issue #92 — Implement `resolve_market()` with oracle validation

**Labels:** `smart-contract` `advanced`

**File:** `contracts/market/src/lib.rs` → `fn resolve_market`

**Description**
Resolves a locked market using a signed oracle report.

**What to implement**
- Verify market status == Locked
- Verify current time is within resolution_window
- Verify oracle is in factory's `ORACLE_WHITELIST` via cross-contract read
- Verify `OracleReport.oracle_address == caller`
- Verify Ed25519 signature (see Issue #93)
- Set outcome, status = Resolved, resolved_at, oracle_used
- Emit `MarketResolved` event

**Acceptance Criteria**
- [ ] Non-whitelisted oracle returns `OracleNotWhitelisted`
- [ ] Expired resolution window returns `ResolutionWindowExpired`
- [ ] Invalid signature returns `InvalidOracleSignature`
- [ ] State updated correctly after valid resolution

---

## Issue #93 — Implement Ed25519 oracle signature verification

**Labels:** `smart-contract` `advanced` `security`

**File:** `contracts/market/src/lib.rs` → inside `fn resolve_market`

**Description**
Cryptographic verification of the oracle's signed report.

**What to implement**
- Construct signed message: `concat(match_id_bytes, outcome_byte, reported_at_bytes_big_endian)`
- Use `env.crypto().ed25519_verify()` to verify `report.signature` against `report.oracle_address`'s public key
- Return `ContractError::InvalidOracleSignature` on failure

**Acceptance Criteria**
- [ ] Valid signature passes verification
- [ ] Tampered signature returns `InvalidOracleSignature`
- [ ] Tampered message (different outcome) returns `InvalidOracleSignature`
- [ ] Unit test with known test keypair

---

## Issue #94 — Implement proportional payout calculation in `claim_winnings()`

**Labels:** `smart-contract` `advanced`

**File:** `contracts/market/src/lib.rs` → `fn claim_winnings`

**Description**
Parimutuel payout formula using checked i128 arithmetic.

**Formula**
```
fee        = floor(total_pool * fee_bps / 10_000)
net_pool   = total_pool - fee
payout     = floor((bettor_stake / winning_pool) * net_pool)
```
Use `i128` checked arithmetic throughout — no floating point.

**Acceptance Criteria**
- [ ] Formula correct for normal case (multiple bettors)
- [ ] Formula correct when bettor is the only winner (gets net_pool)
- [ ] No overflow on large amounts (checked arithmetic)
- [ ] Rounding always floors (never overpays)

---

## Issue #95 — Implement fee deduction and treasury transfer in `claim_winnings()`

**Labels:** `smart-contract` `advanced`

**File:** `contracts/market/src/lib.rs` → `fn claim_winnings`

**Description**
Routes fee to treasury and payout to bettor following CEI pattern.

**What to implement**
- Mark all winning bets as claimed BEFORE any token transfer (CEI pattern)
- Call `Treasury::deposit_fees(token, fee_amount)` on the treasury contract
- Transfer `payout` to bettor via token contract
- Emit `WinningsClaimed` event with `ClaimReceipt`
- Return `ClaimReceipt`

**Acceptance Criteria**
- [ ] Fee correctly routed to treasury
- [ ] Correct net payout transferred to bettor
- [ ] Bets marked claimed BEFORE transfers (reentrancy protection)
- [ ] Double-claim attempt returns `AlreadyClaimed`

---

## Issue #96 — Implement `claim_refund()`

**Labels:** `smart-contract` `intermediate`

**File:** `contracts/market/src/lib.rs` → `fn claim_refund`

**Description**
Full stake refund for bettors in cancelled markets.

**What to implement**
- Verify market status == Cancelled
- Fetch `BETS[bettor]`; return `NoBetsFound` if empty
- Sum all unclaimed bet amounts (no fee deducted)
- Mark all bets as claimed
- Transfer sum to bettor
- Emit `RefundClaimed` event
- Return the refund amount

**Acceptance Criteria**
- [ ] Full original stake returned (no fee deducted)
- [ ] Double-refund attempt returns `AlreadyClaimed`
- [ ] Returns `NoBetsFound` for address with no bets

---

## Issue #97 — Implement `cancel_market()`

**Labels:** `smart-contract` `intermediate`

**File:** `contracts/market/src/lib.rs` → `fn cancel_market`

**Description**
Cancels an open or locked market.

**What to implement**
- Verify caller is admin or whitelisted oracle
- Verify market status is Open or Locked
- Set status to Cancelled
- Store the reason string
- Emit `MarketCancelled` event

**Acceptance Criteria**
- [ ] Unauthorized caller returns `Unauthorized`
- [ ] Already-resolved market returns `InvalidMarketStatus`
- [ ] Event emitted with reason string
- [ ] Bets can be refunded after cancellation

---

## Issue #98 — Implement `dispute_market()`

**Labels:** `smart-contract` `intermediate`

**File:** `contracts/market/src/lib.rs` → `fn dispute_market`

**Description**
Flags a resolved market as disputed, blocking claims.

**What to implement**
- Verify caller is admin
- Verify market status == Resolved
- Set status to Disputed
- Emit `MarketDisputed` event with reason
- Claims must fail (checked by status) until dispute is resolved

**Acceptance Criteria**
- [ ] Only admin can call; non-admin returns `Unauthorized`
- [ ] Only Resolved markets can be disputed
- [ ] `claim_winnings()` returns `InvalidMarketStatus` during dispute
- [ ] Event emitted with reason

---

## Issue #99 — Implement `resolve_dispute()`

**Labels:** `smart-contract` `advanced`

**File:** `contracts/market/src/lib.rs` → `fn resolve_dispute`

**Description**
Admin override to set a final outcome on a disputed market.

**What to implement**
- Verify caller is admin
- Verify market status == Disputed
- Set outcome = `final_outcome`
- Set status = Resolved
- Set `oracle_used = OracleRole::Admin`
- Emit `DisputeResolved` event
- Claims must work after this call

**Acceptance Criteria**
- [ ] Claims work correctly after dispute resolution
- [ ] `oracle_used` set to Admin
- [ ] Non-admin call returns `Unauthorized`
- [ ] `DisputeResolved` event emitted

---

## Issue #100 — Implement `get_current_odds()`

**Labels:** `good first issue` `smart-contract`

**File:** `contracts/market/src/lib.rs` → `fn get_current_odds`

**Description**
Read-only odds query returning basis-point values.

**Formula**
```
odds_x = floor(pool_x * 10_000 / total_pool)
```
Return `(0, 0, 0)` if `total_pool == 0`.

**Acceptance Criteria**
- [ ] Returns `(0, 0, 0)` for empty pools
- [ ] Values are basis points (0–10000)
- [ ] No divide-by-zero panic
- [ ] Unit test with known pool sizes verifying expected output

---

## Issue #101 — Implement `estimate_payout()` as read-only simulation

**Labels:** `good first issue` `smart-contract`

**File:** `contracts/market/src/lib.rs` → `fn estimate_payout`

**Description**
Simulates a hypothetical bet payout without mutating state.

**What to implement**
- Do NOT mutate any storage
- Simulate adding `amount` to the given `side`'s pool
- Run the parimutuel formula on the hypothetical pools
- Return 0 if market is not Open

**Acceptance Criteria**
- [ ] Does not modify storage (test by calling then verifying state unchanged)
- [ ] Accounts for existing pool + hypothetical new stake
- [ ] Returns 0 for non-Open markets

---

## Issue #102 — Implement Treasury `initialize()`

**Labels:** `good first issue` `smart-contract`

**File:** `contracts/treasury/src/lib.rs` → `fn initialize`

**Description**
Sets up the treasury contract for the first time.

**What to implement**
- Store admin address
- Store `withdrawal_limit`
- Initialize empty `ACCUMULATED_FEES` map
- Initialize empty `DAILY_WITHDRAWN` map
- Return `AlreadyInitialized` on second call

**Acceptance Criteria**
- [ ] Correct initial state stored
- [ ] Second call returns `AlreadyInitialized`
- [ ] Unit test covers both cases

---

## Issue #103 — Implement `deposit_fees()` in Treasury

**Labels:** `smart-contract` `intermediate`

**File:** `contracts/treasury/src/lib.rs` → `fn deposit_fees`

**Description**
Accepts fee deposits from approved market contracts.

**What to implement**
- Verify caller is in `APPROVED_MARKETS`
- Transfer `amount` of `token` from caller to this contract
- Increment `ACCUMULATED_FEES[token]` by amount
- Emit `FeeDeposited` event

**Acceptance Criteria**
- [ ] Non-approved caller returns `MarketNotApproved`
- [ ] Balance correctly accumulated across multiple deposits
- [ ] `FeeDeposited` event emitted with correct payload

---

## Issue #104 — Implement `withdraw_fees()` with daily limit enforcement

**Labels:** `smart-contract` `advanced`

**File:** `contracts/treasury/src/lib.rs` → `fn withdraw_fees`

**Description**
Admin withdrawal with per-transaction and daily caps.

**What to implement**
- Require admin authorization
- Verify `amount <= WITHDRAWAL_LIMIT`
- Compute `day_bucket = floor(env.ledger().timestamp() / 86400)`
- Verify `DAILY_WITHDRAWN[day_bucket] + amount <= WITHDRAWAL_LIMIT * 5`
- Verify `ACCUMULATED_FEES[token] >= amount`
- Deduct from `ACCUMULATED_FEES`
- Increment `DAILY_WITHDRAWN[day_bucket]`
- Transfer token to destination
- Emit `FeeWithdrawn` event

**Acceptance Criteria**
- [ ] Over-limit single transaction returns `DailyWithdrawalLimitExceeded`
- [ ] Daily cap enforced correctly across multiple withdrawals same day
- [ ] Insufficient balance returns `InsufficientBalance`
- [ ] Rolling 24h window resets correctly on new day

---

## Issue #105 — Implement `approve_market()` and `revoke_market()` in Treasury

**Labels:** `smart-contract` `intermediate`

**File:** `contracts/treasury/src/lib.rs`

**Description**
Market approval management for the treasury.

**What to implement**
- `approve_market()`: admin-only; append to `APPROVED_MARKETS` (idempotent)
- `revoke_market()`: admin-only; remove from `APPROVED_MARKETS`

**Acceptance Criteria**
- [ ] Approved market can call `deposit_fees()`
- [ ] Revoked market returns `MarketNotApproved` on `deposit_fees()`
- [ ] Both functions require admin auth

---

## Issue #106 — Implement `emergency_drain()` in Treasury

**Labels:** `smart-contract` `advanced`

**File:** `contracts/treasury/src/lib.rs` → `fn emergency_drain`

**Description**
Emergency full-balance withdrawal to admin address.

**What to implement**
- Require admin authorization
- Read full balance of `token` held by this contract
- Transfer entire balance to admin address
- Zero out `ACCUMULATED_FEES[token]`
- Emit `EmergencyDrain` event

**Acceptance Criteria**
- [ ] Only admin can call; others return `Unauthorized`
- [ ] Full balance transferred to admin
- [ ] `ACCUMULATED_FEES` zeroed after drain
- [ ] `EmergencyDrain` event emitted

---

## Issue #107 — Define and emit all contract events

**Labels:** `smart-contract` `intermediate`

**File:** `contracts/shared/src/events.rs`

**Description**
Implement all event emit functions (currently `todo!()` bodies).

**What to implement**
For each function, call `env.events().publish(topics, data)` with the correct topics and data as described in the function comments.

**Acceptance Criteria**
- [ ] All 13 emit functions implemented
- [ ] Each event has correct topics (Vec of Symbols) and data (ScVal)
- [ ] Integration test confirms events are emitted and parseable

---

## Issue #108 — Implement `ContractError` propagation throughout all contracts

**Labels:** `smart-contract` `intermediate`

**File:** `contracts/shared/src/errors.rs` + all contract `lib.rs` files

**Description**
Ensure every public function uses `Result<T, ContractError>` and never panics.

**What to implement**
- Replace any `unwrap()` or `expect()` with `?` or explicit error handling
- Ensure every error path returns a typed `ContractError` variant
- Add `#[contracterror]` attribute to `ContractError` in shared crate

**Acceptance Criteria**
- [ ] Zero `unwrap()` calls in non-test contract code
- [ ] `cargo clippy` passes with no warnings
- [ ] All error variants are reachable (no dead code warnings)

---

## Issue #109 — Write unit tests for `place_bet()` edge cases

**Labels:** `smart-contract` `testing`

**File:** `contracts/market/src/lib.rs` → `#[cfg(test)]`

**Description**
Comprehensive unit tests for `place_bet()`.

**Test cases to cover**
- [ ] Bet amount below `min_bet` → `BetTooSmall`
- [ ] Bet amount above `max_bet` → `BetTooLarge`
- [ ] Bet on Locked market → `InvalidMarketStatus`
- [ ] Bet at exact lock threshold → `BettingClosed`
- [ ] Valid bet on each side (FighterA, FighterB, Draw)
- [ ] Second bet by same address — both bets stored
- [ ] Pool totals correct after multiple bets

**Acceptance Criteria**
- [ ] All listed test cases pass
- [ ] Tests use Soroban `testutils` mock environment

---

## Issue #110 — Write unit tests for `claim_winnings()` payout math

**Labels:** `smart-contract` `testing` `advanced`

**File:** `contracts/market/src/lib.rs` → `#[cfg(test)]`

**Description**
Verify the parimutuel payout formula against manual calculations.

**Test cases to cover**
- [ ] Single winner takes full net pool
- [ ] Two equal bettors on winning side — each gets ~50%
- [ ] Fee deduction is correct (e.g. 2% fee)
- [ ] Payout always floors (never overpays total)
- [ ] Bettor on losing side gets 0 (cannot claim)
- [ ] `AlreadyClaimed` on second claim attempt

**Acceptance Criteria**
- [ ] All math verified against manual calculation
- [ ] Tests pass with 0 tolerance for overpayment

---

## Issue #111 — Write integration test for full market lifecycle

**Labels:** `smart-contract` `testing` `advanced`

**File:** `contracts/market/src/lib.rs` → `#[cfg(test)]`

**Description**
End-to-end integration test covering the complete happy path.

**Flow to test**
1. Deploy MarketFactory + Market wasm + Treasury
2. Call `initialize()` on factory and treasury
3. Call `create_market()` → get `market_id`
4. Multiple bettors call `place_bet()` on different sides
5. Call `lock_market()`
6. Oracle calls `resolve_market()` with signed report
7. Winners call `claim_winnings()`
8. Verify treasury received correct fee

**Acceptance Criteria**
- [ ] Full flow passes without error
- [ ] Final balances correct for all parties
- [ ] Treasury balance matches expected fee

---

## Issue #112 — Add storage TTL to market entries

**Labels:** `smart-contract` `intermediate`

**File:** `contracts/market/src/lib.rs`

**Description**
Set Soroban storage TTL so inactive markets don't consume ledger storage indefinitely.

**What to implement**
- On `initialize()`, set TTL on STATE, BETS, BETTOR_LIST via `env.storage().instance().extend_ttl()`
- On each `place_bet()`, extend TTL to `MAX_TTL`
- After resolution, do not extend TTL further (let it expire naturally)

**Acceptance Criteria**
- [ ] TTL set on creation
- [ ] TTL extended on each bet
- [ ] Expired market cannot receive new bets (status check handles this)

---

## Issue #113 — Implement reentrancy guard for `claim_winnings()`

**Labels:** `smart-contract` `advanced` `security`

**File:** `contracts/market/src/lib.rs` → `fn claim_winnings`

**Description**
Protect `claim_winnings()` against reentrancy attacks.

**What to implement**
- Follow CEI pattern strictly:
  1. **Checks**: verify all preconditions
  2. **Effects**: mark bets as claimed and update state BEFORE any token transfers
  3. **Interactions**: perform token transfers last
- Add a `CLAIMING` boolean lock in storage as a secondary guard

**Acceptance Criteria**
- [ ] State mutations happen before token transfers in code order
- [ ] `CLAIMING` lock prevents reentrant calls
- [ ] Test simulating a reentrant token callback is rejected

---

## Issue #114 — Implement `get_bettor_count()`

**Labels:** `good first issue` `smart-contract`

**File:** `contracts/market/src/lib.rs` → `fn get_bettor_count`

**Description**
Returns the number of unique bettors in a market.

**What to implement**
- Read `BETTOR_LIST` from storage
- Return its length as `u32`

**Acceptance Criteria**
- [ ] Returns 0 for market with no bets
- [ ] Returns correct count after multiple unique bettors
- [ ] Same bettor placing a second bet does not increment count

---

## Issue #115 — Implement `get_pool_sizes()`

**Labels:** `good first issue` `smart-contract`

**File:** `contracts/market/src/lib.rs` → `fn get_pool_sizes`

**Description**
Returns current pool sizes as a tuple.

**What to implement**
- Read STATE from storage
- Return `(state.pool_a, state.pool_b, state.pool_draw)`

**Acceptance Criteria**
- [ ] Returns `(0, 0, 0)` for fresh market
- [ ] Values match accumulated `place_bet()` calls
- [ ] Return tuple order matches signature: (pool_a, pool_b, pool_draw)

---

## Issue #116 — Write deploy script for testnet

**Labels:** `smart-contract` `devops`

**File:** `contracts/scripts/deploy.sh`

**Description**
End-to-end deploy script (stub currently has TODO comments).

**What to implement**
- Build all contracts with `cargo build --release --target wasm32-unknown-unknown`
- Optimize each wasm with `stellar contract optimize`
- Deploy MarketFactory, upload Market wasm, deploy Treasury using `stellar contract deploy`
- Call `initialize()` on MarketFactory and Treasury
- Write all addresses to `.contract-addresses.env`

**Acceptance Criteria**
- [ ] Script runs end-to-end on Stellar testnet
- [ ] All three contracts deployed and initialized
- [ ] Addresses written to output file
- [ ] Script is idempotent (re-running doesn't break existing markets)

---

## Issue #117 — Write contract upgrade mechanism in MarketFactory

**Labels:** `smart-contract` `advanced`

**File:** `contracts/market_factory/src/lib.rs`

**Description**
Allow admin to update the Market wasm hash used for new deployments.

**What to implement**
- Add `MARKET_WASM_HASH: BytesN<32>` storage key
- Add `update_market_wasm(env, admin, new_wasm_hash)` function
- `create_market()` reads `MARKET_WASM_HASH` dynamically instead of hardcoding

**Acceptance Criteria**
- [ ] New markets after upgrade use new wasm
- [ ] Existing markets are unaffected
- [ ] Only admin can call `update_market_wasm()`

---

## Issue #118 — Add multi-oracle consensus (2-of-3)

**Labels:** `smart-contract` `advanced`

**File:** `contracts/market/src/lib.rs` → `fn resolve_market`

**Description**
Extend `resolve_market()` to require 2-of-3 oracle signatures.

**What to implement**
- Add `PENDING_REPORTS: Map<Address, OracleReport>` storage key
- First oracle report stores into `PENDING_REPORTS`
- Second oracle report with matching outcome triggers resolution
- Conflicting second report emits `ConflictingOracleReport` event and waits for third
- Third report breaks tie by majority

**Acceptance Criteria**
- [ ] Single oracle report does not resolve market
- [ ] Two matching reports resolve market
- [ ] Two conflicting reports wait for third
- [ ] Majority of three conflicting reports resolves correctly

---

## Issue #119 — Document all public functions with rustdoc

**Labels:** `smart-contract` `docs` `good first issue`

**File:** All files under `contracts/`

**Description**
Add `///` rustdoc comments to every public function across all contracts.

**What to implement**
- Convert all block comments above functions to `///` rustdoc
- Add `# Errors` section listing possible `ContractError` variants
- Add `# Examples` section for the most important functions

**Acceptance Criteria**
- [ ] `cargo doc --no-deps` builds without warnings
- [ ] Every public function has a doc comment
- [ ] `# Errors` section present on all functions returning `Result`

---

## Issue #120 — Set up cargo workspace and CI

**Labels:** `smart-contract` `devops` `good first issue`

**File:** `contracts/Cargo.toml` · `.github/workflows/contracts-ci.yml`

**Description**
Verify the cargo workspace compiles cleanly and CI passes.

**What to implement**
- Confirm `contracts/Cargo.toml` workspace includes all four crates
- Fix any compilation errors in stub code (replace `todo!()` calls that block compilation with placeholder returns where needed for CI)
- Ensure `.github/workflows/contracts-ci.yml` passes on a test PR

**Acceptance Criteria**
- [ ] `cargo build` succeeds from `contracts/`
- [ ] `cargo clippy` passes with no errors
- [ ] CI workflow runs and passes on GitHub Actions
- [ ] `cargo test` runs (all tests may be empty stubs — that is OK for this issue)
