---
tags:
  - architecting:patterns
  - practices:scalability
level: intermediate
category: architecting
audience:
  - audiences:architects

---
# Caching

---
## What This Chapter Covers

- Cache layers
- Patterns
- Invalidation
- Eviction
- Pitfalls

---
## Why Cache

- Move work closer to user
- Shed load from origin
- Lower latency
- Lower cost

---
## Layers

- Browser
- CDN
- Reverse proxy
- Application
- Distributed cache
- Database

---
## Cache-Aside

- App reads from cache
- Miss: read DB, write cache
- Simple to implement
- Most common

---
## Patterns Compared

![cache_aside_patterns](svg/courses/architecting/web-architecture-and-scaling/03_caching/cache_aside_patterns.svg)

---
## Read-Through

- Cache fronts the DB
- Cache loads on miss
- App is unaware of source
- Fewer code paths

---
## Write-Through

- Writes go to cache and DB
- Cache always fresh
- Slower writes
- No staleness

---
## Write-Behind

- Writes to cache first
- Async flush to DB
- Risk of data loss
- High write throughput

---
## TTL

- Time to live per entry
- Drift bounded by TTL
- Tune to acceptable staleness
- Cheapest invalidation

---
## Active Invalidation

- Notify cache on write
- Targeted, fast
- Hard at scale
- Often combined with TTL

---
## Eviction

- Least recently used
- Least frequently used
- Frequency sketch hybrids
- First in first out

---
## Stampede

- Many misses for same key
- Origin overloaded
- Use single-flight
- Or stale-while-revalidate

---
## Negative Caching

- Cache misses too
- Avoids repeated origin loads
- Short TTL
- Beware cache poisoning

---
## Per-User Caching

- Hard to share
- High cardinality
- Often skipped
- Or pushed to client

---
## Common Caching Mistakes

- No invalidation plan
- Long TTL for hot data
- Cache the same key with different content
- No metric on hit rate
- Cache before measuring
