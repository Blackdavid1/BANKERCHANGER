# WebSocket Authentication

## Overview

The ActivityFeed WebSocket endpoint (`/ws`) requires JWT authentication via first-message authentication protocol. This prevents JWT tokens from being exposed in server access logs, which would otherwise record query parameters.

## Authentication Protocol

### Connection Setup

1. **Connect without authentication** — Open a WebSocket connection to the endpoint without any credentials:

```
ws://localhost:3001/
```

or for HTTPS:

```
wss://example.com/
```

2. **Send authentication message within 5 seconds** — After connection opens, send an auth message with your JWT token:

```json
{
  "type": "auth",
  "token": "<JWT_TOKEN>"
}
```

### Token Requirements

- Must be a valid JWT signed with `JWT_SECRET` (same as used for REST API auth)
- Token format: pass the raw JWT string (not `Bearer <token>`)
- No expiration validation on the server (tokens are validated structurally)

### Authentication Errors

Connection closes with error codes:

| Close Code | Reason | Cause |
|---|---|---|
| 4001 | `Authentication timeout` | Auth message not sent within 5 seconds |
| 4001 | `Expected auth message` | First message was not an auth message |
| 4001 | `Invalid token` | JWT signature verification failed |

## Example: Client Connection

### JavaScript/TypeScript

```typescript
// Get JWT from login endpoint
const loginRes = await fetch('/api/auth/login', {
  method: 'POST',
  body: JSON.stringify({ email: 'user@example.com', password: 'password' }),
});
const { accessToken } = await loginRes.json();

// Connect to WebSocket (without token in URL)
const ws = new WebSocket('ws://localhost:3001/');

ws.addEventListener('open', () => {
  // Send authentication message
  ws.send(JSON.stringify({
    type: 'auth',
    token: accessToken,
  }));
});

ws.addEventListener('message', (event) => {
  const message = JSON.parse(event.data);
  
  // Handle activity events (received after successful auth and subscription)
  if (message.type === 'trade' || message.type === 'dispute' || message.type === 'resolved') {
    console.log('Activity:', message);
  }
});

ws.addEventListener('close', (event) => {
  if (event.code === 4001) {
    console.error('Authentication failed:', event.reason);
  }
});

ws.addEventListener('error', (event) => {
  console.error('WebSocket error:', event);
});

// After connection opens and authentication succeeds, subscribe to markets
function subscribeToMarket(marketId: string) {
  if (ws.readyState === WebSocket.OPEN) {
    ws.send(JSON.stringify({
      type: 'subscribe_activity',
      marketId,
    }));
  }
}
```

## Message Protocol

### Subscribe Message

After successful authentication, send:

```json
{
  "type": "subscribe_activity",
  "marketId": "market-xyz"
}
```

### Activity Events

Server sends events in JSON format:

```json
{
  "type": "trade",
  "marketId": "market-xyz",
  "outcomeId": "outcome-a",
  "side": "buy",
  "sharesAmount": 100,
  "priceBps": 5000,
  "timestamp": "2025-01-15T10:30:00Z"
}
```

Event types:
- `trade` — Buy/sell trade executed
- `dispute` — Dispute filed on market
- `resolved` — Market resolved with outcome

## Rate Limiting

- **20 events/sec per market** — Events beyond this are dropped silently
- Applies to all authenticated connections
- Per-market, not per-connection

## Security Considerations

- **Token in Access Logs:** Query parameters are NOT logged; the token is only sent as a WebSocket frame, not visible to reverse proxies or load balancers
- **Token Reuse:** Tokens are not revoked; use short expiration in the REST API (`JWT_EXPIRES_IN`)
- **5-Second Deadline:** Clients must authenticate within 5 seconds or the connection is closed (prevents resource exhaustion from unauthenticated connections)
- **No Per-Message Auth:** Once authenticated, no further auth checks per message (connection-level auth only)

## Deployment Checklist

- [ ] Ensure `JWT_SECRET` is set in production
- [ ] Use `wss://` (WebSocket Secure) in production
- [ ] Monitor for 4001 close codes to detect auth failures
- [ ] Client code updated to send auth message instead of token in URL
- [ ] Update client reconnection logic to handle 5-second auth deadline
