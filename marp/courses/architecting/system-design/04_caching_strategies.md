---
tags:
  - architecture:system-design
  - architecture:caching
level: intermediate
category: architecture
audience:
  - audiences:developers

---
# Caching Strategies

---
## What This Chapter Covers

- Where to cache
- Cache patterns: read-through, write-through, write-back
- Invalidation
- Eviction policies
- Cache-aside
- Distributed caching
- Common pitfalls

---
## Why Cache

- Reduce load on the origin
- Reduce latency
- Save bandwidth
- The biggest perf optimisation, often
- "Cache invalidation" is famously one of the hard things

---
## Where To Cache

- Browser: HTTP cache, service workers
- CDN: edge cache (Cloudflare, CloudFront)
- API gateway: in front of services
- App server: in-process cache
- Distributed cache: Redis, Memcached
- DB: query result cache

---
## Cache-Aside

- App reads from cache; on miss, reads DB; writes to cache
- The most-common pattern
- Stale data possible
- Cache misses are expensive (DB hit + cache write)
- Easy to reason about

---
## Read-Through

- App reads from cache; cache reads DB on miss
- Cache transparent to the app
- Slightly less code; same logic
- Common in: Redis with custom logic, ORM caches

---
## Write-Through

- App writes to cache; cache writes to DB synchronously
- Cache always fresh
- Higher write latency
- Used when reads dominate; consistency matters

---
## Write-Back

- App writes to cache; cache writes to DB asynchronously
- Fast writes; risk of data loss
- Used in: high-write systems, OS file caches
- Application must tolerate brief data-loss windows

---
## Invalidation Strategies

- TTL: expire after N seconds
- Event-based: update cache when DB changes
- Tag-based: invalidate everything with a tag
- Purge API: explicitly remove
- Each has trade-offs

---
## Eviction Policies

- LRU: least-recently-used; popular
- LFU: least-frequently-used
- FIFO: first-in-first-out
- Random: cheap; surprisingly OK
- TTL: not exactly eviction; expiration

---
## TTL Choice

- Too short: cache barely helps
- Too long: stale data frustrates users
- Match TTL to acceptable staleness
- Different per data type
- Refresh-ahead pattern: re-fetch before expiry

---
## Distributed Caching

- Multiple cache nodes; data sharded across
- Redis Cluster, Memcached with consistent hashing
- Adding nodes: rebalances some keys
- Replicas for availability
- The standard at scale

---
## Cache Stampede

- Cache expires; many clients request same key
- All hit the DB
- Solutions: locks, request collapsing, stale-while-revalidate
- Most CDNs handle natively

---
## Cache Poisoning

- Wrong data cached; persists for TTL
- Cause: bug in app, race in invalidation
- Prevention: validate before caching; conservative TTL
- Detection: monitor cache hit rates and downstream errors

---
## What NOT To Cache

- Per-user data without per-user keys (privacy leak)
- Frequently-changing data (low hit rate)
- Tiny / cheap-to-compute data
- Cache: high-cost, slow-changing things

---
## Common Caching Mistakes

- Forgetting to invalidate on write
- Caching user-specific data globally
- TTLs that are wrong by an order of magnitude
- No metrics on hit ratio
- Cache as a "fix" instead of fixing the root cause
