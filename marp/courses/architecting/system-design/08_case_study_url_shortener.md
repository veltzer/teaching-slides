---
tags:
  - architecture:system-design
level: intermediate
category: architecture
audience:
  - audiences:developers

---
# Case Study: URL Shortener

---
## What This Chapter Covers

- Requirements
- Capacity estimation
- API
- ID generation
- Storage
- Caching
- Scaling

---
## Requirements

- Long URL &#8594; short URL
- Short URL &#8594; redirect
- Custom aliases
- Analytics (clicks)
- 100M URLs / month

---
## Capacity Estimation

- 100M / month = ~40 / sec writes
- Read:write 100:1 &#8594; 4000 / sec reads
- 5 years storage: 6B URLs
- 6B * 100 bytes = 600 GB
- One mid-size DB

---
## API

- POST /shorten { url, custom_alias? } &#8594; { short_url }
- GET /:code &#8594; 301 redirect to long URL
- GET /:code/stats &#8594; click count

---
## Short Code Generation

- Hash + base62: 7 chars = 3.5T URLs
- Counter + base62: simpler; predictable
- Random: collision-checked
- Pre-generate batches: fast issuance

---
## Storage

- Postgres: codes, urls, owner, created_at
- Index on code (primary key)
- Click counts: separate (hot column)
- Or denormalised for read perf

---
## Caching

- Redis cache: code &#8594; long URL
- 95% hit rate possible (popular links)
- TTL: 1 day, refresh on access
- Massive read cost reduction

---
## Read Path

- Request: /abc123
- Check Redis: cache hit &#8594; redirect (1ms)
- Cache miss &#8594; query DB &#8594; cache &#8594; redirect (5ms)
- 95% hit: avg latency near 1ms

---
## Write Path

- POST /shorten
- Generate code (avoid collisions)
- Insert DB
- Return short URL
- Async: pre-warm cache

---
## Analytics

- Each click: write event to log / Kafka
- Background: aggregate to clicks table
- Query stats: aggregate table
- Don't update click count on every request (write contention)

---
## Scaling Reads

- Cache absorbs 90%+
- Read replicas for misses
- DNS-based geo-routing for global
- CDN caches the redirect (HTTP 301 with TTL)

---
## Scaling Writes

- Single DB writes 40/sec — easy
- 100x = 4000/sec — sharding might help
- Most URL shorteners stay on one DB
- Code generation might bottleneck if not careful

---
## Failure Modes

- Cache down: hit DB; latency rises but works
- DB down: serve from cache; stale OK for redirects
- Code collision: rare; retry with new code
- Plan for each

---
## Common Discussion Points

- "Why hash and not counter?" — hashing prevents enumeration
- "How do you handle expired URLs?" — TTL or background cleanup
- "How do you handle malicious URLs?" — blocklists, scanning
- "How do you handle billions of URLs?" — shard by code prefix
- Be ready for trade-off questions
