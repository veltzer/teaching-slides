---
tags:
  - concepts:api
  - concepts:resiliency
level: intermediate
category: architecture
audience:
  - audiences:developers
  - audiences:architects

---
# Rate Limiting and Idempotency

---
## Why Rate Limit

- Protect the service from abuse
- Ensure fair usage across consumers
- Bound resource consumption
- Make capacity planning predictable

---
## Two Concerns

![rate_idempotency](svg/courses/architecting/api-design-best-practices/07_rate_limiting_and_idempotency/rate_idempotency.svg)

---
## Rate Limiting Strategies

- **Fixed window**: N requests per minute, resets on the boundary
- **Sliding window**: N requests in any 60-second period
- **Token bucket**: bucket holds N tokens; each request takes one; refills over time
- **Leaky bucket**: requests queue and drain at a fixed rate

---
## Token Bucket: Most Common

- Allows bursts up to bucket size
- Average rate = refill rate
- Easy to tune: bucket size, refill rate
- Implementation in Redis or similar is straightforward

---
## Rate Limit Headers

- Standard practice: tell the client what's going on
- `X-RateLimit-Limit: 100` — your limit per window
- `X-RateLimit-Remaining: 87` — how many you have left
- `X-RateLimit-Reset: 1737000000` — when the window resets (Unix timestamp)
- `Retry-After: 30` — how long to wait if 429'd

---
## When Limits Are Hit

- Return 429 Too Many Requests
- Include `Retry-After` header
- The body can be a normal error response with details
- The client backs off; doesn't retry immediately

---
## Per-What Rate Limits

- Per API key — common
- Per user — for user-facing APIs
- Per IP — coarse-grained
- Per endpoint — different limits for cheap vs expensive endpoints
- Combinations: "10 calls per second per user, but unlimited reads"

---
## Quotas

- Like rate limits, but on a longer time window (daily, monthly)
- Often tied to billing tiers
- Usually paired with rate limits

---
## Idempotency

- An operation is idempotent if calling it twice has the same effect as calling it once
- `GET`, `PUT`, `DELETE` are idempotent by spec
- `POST` is generally **not** — but should be where it can be
- Idempotency makes retries safe

---
## Why Idempotency Matters

- Networks lose responses
- Clients retry
- Without idempotency: duplicate side effects (charged twice, two orders)
- This is a real production concern, not a theoretical one

---
## Idempotency Keys

- Client generates a unique key per logical operation
- Sends it with the request: `Idempotency-Key: order-2026-01-15-abc123`
- Server stores the key with the result
- A second request with the same key returns the original result

---
## Stripe-Style Idempotency

```http
POST /charges
Idempotency-Key: ord_42_attempt_1
Content-Type: application/json

{"amount": 9500, "customer": "c1"}
```

- The server records: "for key ord_42_attempt_1, charge result was..."
- Subsequent requests with the same key return the same result
- The window is bounded (e.g., 24 hours)

---
## Server-Side Implementation

- Hash the request body
- Store: `(key, body_hash, response, expires_at)`
- On request: check key; if exists with same body_hash, return stored response
- If exists with different body_hash, return 422 (key reuse with different request)

---
## Idempotent vs Non-Idempotent Methods

- Idempotent: GET, HEAD, PUT, DELETE
- Non-idempotent: POST (by default), PATCH (sometimes)
- Make POST idempotent with idempotency keys
- Document which endpoints are idempotent

---
## Retry-Safe API Design

- Use idempotency keys for any state-changing operation
- Make read endpoints free of side effects
- Make DELETE return 204 even if the resource was already deleted
- Make PUT replace; second PUT with same body is a no-op

---
## Anti-Patterns

- "POST creates a new resource on every retry" — duplicates
- Rate limits without headers (consumer can't pace itself)
- Hard limits with no graceful degradation
- Idempotency window too short (legitimate retries get a different result)

---
## Summary

- Rate limit to protect; quota to bill
- Use 429 + Retry-After + RateLimit headers
- Idempotency keys make retries safe
- Default idempotency on read methods; opt in for write methods
- Both are baseline production requirements, not optional
