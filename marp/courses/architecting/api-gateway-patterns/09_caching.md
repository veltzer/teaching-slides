---
tags:
  - architecture:api-gateway
  - architecture:caching
level: intermediate
category: architecture
audience:
  - audiences:developers

---
# Caching at the Gateway

---
## What This Chapter Covers

- Why cache at the gateway
- HTTP caching headers
- Cache invalidation
- Per-route caching policies
- CDN integration
- Pitfalls

---
## Why Cache At The Gateway

- Faster responses for repeated requests
- Reduces backend load
- One cache for many clients
- Cheaper than scaling backends
- The lowest-hanging perf optimisation

---
## What To Cache

- GET requests (idempotent, side-effect-free)
- Public data (same for all consumers)
- Expensive-to-generate responses
- Slowly-changing data
- Avoid: user-specific data without per-user cache keys

---
## HTTP Caching Headers

- `Cache-Control: public, max-age=60`
- `ETag: "abc123"`
- `Last-Modified: Wed, 01 May 2026 12:00:00 GMT`
- `Vary: Accept-Encoding, Authorization`
- The standard; works with browsers, CDNs, gateways

---
## Cache-Control Directives

- `public`: anyone can cache
- `private`: only the end user (browser)
- `no-cache`: revalidate every time (still cacheable)
- `no-store`: don't cache at all
- `max-age=N`: cache for N seconds
- `s-maxage=N`: shared cache TTL (overrides max-age for CDNs)

---
## ETag-Based Revalidation

- Server returns ETag with response
- Client sends `If-None-Match: "abc123"` on next request
- Server: still match? &#8594; 304 Not Modified (no body)
- Saves bandwidth even when data hasn't changed

---
## Cache Invalidation

- The hardest problem in caching
- Time-based: TTL; eventually consistent
- Tag-based: invalidate all keys with tag X (CDNs support this)
- Purge API: explicitly remove specific keys
- Versioned URLs: `/v1/users` &#8594; `/v2/users` (effectively cache bust)

---
## TTL Strategy

- Long TTL: fewer backend hits; staler data
- Short TTL: fresher data; more backend load
- Vary by endpoint: list endpoints often longer than single-item
- Health checks: short TTL or no cache

---
## Cache Keys

- Default: URL + method + relevant headers (Authorization, Accept)
- `Vary` header tells cache to differentiate by request header
- Without it: one user's cache hit for another user
- Critical for correctness

---
## Per-Route Caching

```yaml
routes:
  - path: /products
    cache: { ttl: 60 }
  - path: /products/{id}
    cache: { ttl: 300 }
  - path: /users/{id}
    cache: { ttl: 0 }   # don't cache
```

- Different policy per endpoint
- Match TTL to data volatility

---
## CDN Integration

- Gateway emits proper headers; CDN does the work
- Cloudflare, CloudFront, Akamai, Fastly
- Edge cache: closer to users; faster
- Origin shielding: CDN absorbs most traffic
- Gateway is the origin

---
## Cache Hit / Miss Metrics

- Track: cache hit ratio per route
- Below 50%: caching may not be helping
- 90%+: caching is doing its job
- Drives: TTL tuning, what to cache more aggressively

---
## Negative Caching

- Cache 404s briefly (a few seconds)
- Stops repeated lookups for non-existent resources
- Useful when DBs are slow on misses
- TTL much shorter than positive cache

---
## Stale-While-Revalidate

- `Cache-Control: max-age=60, stale-while-revalidate=300`
- Serve stale data; refresh in background
- Best for read-heavy APIs
- Trade-off: slight staleness for low latency

---
## Cache Stampede

- Cache expires; many clients request the same key simultaneously
- All hit the backend at once
- Tools: locks, "serve stale during refresh", request collapsing
- Most CDNs handle this automatically

---
## Common Caching Mistakes

- Caching user-specific data without `Vary: Authorization`
- Cache TTLs too long (stale data) or too short (no benefit)
- No invalidation strategy
- Caching POST/PUT (not safe)
- Forgetting `Vary` on content negotiation
