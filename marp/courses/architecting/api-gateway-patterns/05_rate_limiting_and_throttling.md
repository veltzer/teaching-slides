---
tags:
  - architecture:api-gateway
  - architecture:rate-limiting
level: intermediate
category: architecture
audience:
  - audiences:developers

---

# Rate Limiting and Throttling

---

## Token Bucket

![token_bucket](svg/courses/architecting/api-gateway-patterns/05_rate_limiting_and_throttling/token_bucket.svg)

---

## What This Chapter Covers

- Why rate limiting matters
- Token bucket vs leaky bucket
- Fixed window vs sliding window
- Distributed rate limiting
- Per-IP, per-user, per-endpoint
- HTTP headers
- Common pitfalls

---

## Why Rate Limit

- Prevent abuse (scraping, brute force)
- Protect backends from overload
- Fair sharing across consumers
- Cost control (cloud bills, third-party APIs)
- A baseline of resilience

---

## Token Bucket

- A bucket with N tokens; refills at rate R per second
- Each request takes 1 token
- Bucket empty &#8594; reject (or queue)
- Allows bursts up to bucket size
- Smooth, common, flexible

---

## Leaky Bucket

- Requests enter a queue (bucket)
- Bucket "leaks" at a fixed rate
- Bucket full &#8594; reject
- Smooths bursts to a constant outflow
- Good for protecting downstream that can't burst

---

## Fixed Window

- N requests per window (e.g., 100 / minute)
- Counter resets at window boundary
- Simple
- Issue: 100 at end of window 1 + 100 at start of window 2 = 200 in 2 seconds
- Burst at window edge

---

## Sliding Window

- Counts requests in the *last* 60 seconds, continuously
- More accurate; harder to game
- Slight performance cost (per-request bookkeeping)
- The modern default for serious rate limiting

---

## Sliding Window Log

- Store timestamps of every request
- Count those within the window
- Accurate; memory-heavy
- Use for low-volume / high-precision needs

---

## Sliding Window Counter

- Approximation: count current minute + (previous minute * weight)
- Memory-light
- Approximate but close enough
- The pragmatic choice for high-volume

---

## Algorithm Cheatsheet

![rate_limiting_algorithms](svg/courses/architecting/api-gateway-patterns/05_rate_limiting_and_throttling/algorithms.svg)

---

## Distributed Rate Limiting

- Multi-instance gateways need shared state
- Redis is the typical backend
- Each request increments counter; checks limit
- Latency cost: one Redis round trip per request
- Fall-open vs fall-closed on Redis failure

---

## Per-IP Rate Limiting

- Default for unauthenticated traffic
- Mitigates basic abuse
- Insufficient: NAT, mobile networks, IPv6 share
- Pair with: CAPTCHAs, account creation rate limits

---

## Per-User Rate Limiting

- After authentication
- Track by user ID
- Different tiers (free / paid / enterprise)
- The standard for SaaS APIs
- Implement at the gateway

---

## Per-Endpoint

- Different limits for different operations
- Login: tight (10 / minute)
- List items: loose (1000 / minute)
- Reflects the operation's cost
- Standard sophistication

---

## HTTP Headers

```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 23
X-RateLimit-Reset: 1700000000

# When over limit:
HTTP/1.1 429 Too Many Requests
Retry-After: 30
```

- Tells the client where they stand
- `Retry-After` for the back-off
- Standard headers; well-supported

---

## Throttling Strategies On Limit

- Reject (429): cleanest
- Queue: smoother for clients; backend may be overwhelmed
- Drop with response: cuts load; forgiving
- Different choice per endpoint and audience

---

## Common Rate Limiting Mistakes

- Per-IP only (NAT lets one user circumvent)
- Limit = 100/min when you mean 100/min sustained (be explicit)
- No `Retry-After` header (clients don't know when to come back)
- Synchronous Redis call in hot path with no timeout
- Limits never tested under load
