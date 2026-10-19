# Hook Tests Documentation

## Overview

This directory contains comprehensive unit tests for the React hooks used in the BANKERCHANGER frontend application. Tests are written using `@testing-library/react` and `msw` (Mock Service Worker) to ensure all API interactions are mocked without requiring a real backend.

## Setup and Usage

### Running Tests

```bash
# Run all tests
npm test

# Run tests in watch mode
npm test -- --watch

# Run specific test file
npm test -- useMarkets.test.ts

# Run tests with coverage
npm test -- --coverage
```

### Key Features

- **MSW (Mock Service Worker)**: All API calls are intercepted and mocked at the network level
- **Fake Timers**: Uses `jest.useFakeTimers()` for controlling polling intervals
- **No External Dependencies**: Tests run in isolation without requiring a real backend
- **Comprehensive Coverage**: Tests cover happy paths, error cases, and edge cases

## Test Files

### `useMarkets.test.ts`

Tests the `useMarkets` hook, which fetches and auto-refreshes the market list.

#### Test Cases

1. **Initial Loading State**
   - `isLoading` starts as `true`
   - `markets` array starts empty
   - `error` is initially `null`
   - `total` starts at 0

2. **Markets Populated After Successful Fetch**
   - Markets array populated with API response data
   - `total` correctly reflects market count
   - `isLoading` transitions to `false`
   - `error` remains `null`

3. **Error State Set on Failed Fetch**
   - `error` is set when API returns error status
   - `isLoading` transitions to `false` even with error
   - Previous data is preserved during error recovery

4. **refetch() Triggers New Fetch**
   - Hook exposes a callable `refetch()` function
   - Calling `refetch()` triggers new API request
   - Errors during refetch are handled gracefully
   - `isLoading` stays `false` during background refetch

5. **Filter Support**
   - Hook respects status and weight_class filters
   - Hook updates when filters change

6. **Auto-Polling Every 30 Seconds**
   - Markets list automatically refreshes every 30 seconds
   - Polling stops when component unmounts

### `useMarket.test.ts`

Tests the `useMarket` hook, which fetches a single market and polls for updates when "open".

#### Test Cases

1. **Loading State Transitions Correctly**
   - `isLoading` starts as `true`
   - `market` is initially `null`
   - `error` starts as `null`
   - `isLoading` transitions to `false` after successful fetch
   - Market data is populated correctly
   - Error states are handled properly

2. **Polling Starts for Open Markets**
   - Polling begins automatically for `status === 'open'`
   - Polls every 10 seconds
   - Market data updates on each poll
   - Polling errors are handled gracefully

3. **Polling Stops When Market Becomes Locked**
   - Polling stops when status changes from `'open'` to `'locked'`
   - No polling occurs if market is initially locked
   - Polling stops for `'resolved'` status
   - Polling stops for `'cancelled'` status

4. **Component Unmounting**
   - Polling cleanup happens on unmount
   - No state updates occur after unmount

5. **Market ID Changes**
   - New market is fetched when `market_id` prop changes
   - Polling for previous market is cleaned up
   - Polling continues for new market if status is `'open'`

6. **Edge Cases**
   - Handles markets with undefined optional fields
   - Handles rapid market_id changes

## MSW Mock Setup

### Handlers Location: `__tests__/mocks/handlers.ts`

The mock handlers define the API responses for testing:

```typescript
// Mock markets data
export const mockMarkets: Market[] = [...]

// Request handlers
export const handlers = [
  http.get('http://localhost:3001/api/markets', ...,
  http.get('http://localhost:3001/api/markets/:market_id', ...),
]

// MSW Server
export const server = setupServer(...handlers)
```

### Test Data

- **openMarket**: Market with `status === 'open'`
- **lockedMarket**: Market with `status === 'locked'`
- **resolvedMarket**: Market with `status === 'resolved'`

## Best Practices Demonstrated

### 1. Fake Timers

```typescript
beforeEach(() => {
  jest.useFakeTimers();
});

afterEach(() => {
  jest.useRealTimers();
});

it('should poll every 10 seconds', async () => {
  const { result } = renderHook(() => useMarket('market-1'));
  
  // Fast-forward 10 seconds
  jest.advanceTimersByTime(10_000);
  
  // Assert polling occurred
});
```

### 2. MSW Handler Overrides

```typescript
// Override handler for specific test
server.use(
  http.get('http://localhost:3001/api/markets', () => {
    return HttpResponse.json(
      { error: 'Server Error' },
      { status: 500 }
    );
  })
);
```

### 3. Async Wait Patterns

```typescript
const { result } = renderHook(() => useMarkets());

// Wait for initial load
await waitFor(() => {
  expect(result.current.isLoading).toBe(false);
});

// Assert final state
expect(result.current.markets).toHaveLength(2);
```

## Configuration Files

### `jest.config.js`

- Root test environment configuration
- Sets up jsdom for DOM testing
- Configures ts-jest for TypeScript support
- Specifies test file patterns and setup file

### `setup.ts`

- Initializes MSW server
- Configures error handling for unhandled requests
- Resets handlers after each test
- Sets extended timeout for async operations

## Common Pitfalls and Solutions

### Issue: Tests Timeout During Polling

**Solution**: Increase `jest.setTimeout()` in setup file or override in specific tests:

```typescript
beforeEach(() => {
  jest.useFakeTimers();
  jest.setTimeout(10000);
});
```

### Issue: State Not Updating After Unmount

**Solution**: Always test cleanup by unmounting and advancing timers:

```typescript
const { unmount } = renderHook(() => useMarket('id'));
unmount();
expect(() => jest.advanceTimersByTime(10_000)).not.toThrow();
```

### Issue: Stale Handlers Between Tests

**Solution**: MSW automatically resets handlers, but you can manually reset if needed:

```typescript
afterEach(() => {
  server.resetHandlers();
});
```

## Coverage

Current test coverage targets:
- ✅ Initial state validation
- ✅ Happy path (successful API calls)
- ✅ Error handling
- ✅ Polling logic and intervals
- ✅ State cleanup on unmount
- ✅ Hook parameter changes
- ✅ Edge cases and boundary conditions

## Dependencies

Required packages:
- `@testing-library/react`
- `msw` (Mock Service Worker)
- `jest`
- `ts-jest`

These should be in your `package.json` devDependencies.
