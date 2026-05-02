---
tags:
  - databases:design
  - databases:performance
level: intermediate
category: databases
audience:
  - audiences:developers

---
# Performance Optimisation in Design

---
## Design for Performance

![perf_design](svg/courses/databases/database-design/07_performance_optimization_in_design/perf_design.svg)

---
## What This Chapter Covers

- Indexes for queries
- Avoiding N+1
- Materialised views
- Read replicas
- Sharding strategies
- Caching layers

---
## Index For Queries

- Add indexes for: WHERE, JOIN, ORDER BY
- Watch query plans (EXPLAIN)
- Per-table: 3-10 indexes typical
- Maintenance: each adds write cost

---
## Index For Foreign Keys

- Almost always: index your foreign keys
- Joins use them
- Cascades use them
- Postgres doesn't auto-index FKs (unlike MySQL)

---
## N+1 Queries

- Loop: 1 query for the list, N for each item
- Anti-pattern
- Fix: join, or batch fetch (IN clause)
- ORMs hide; profile to find

---
## Materialised Views

- Pre-computed query result
- Stored as a table
- Refresh periodically or on-demand
- For complex aggregations queried often

---
## Read Replicas

- Followers serve read traffic
- Scales reads
- Replication lag: stale reads
- Standard in cloud DBs

---
## Sharding

- Split data across nodes
- By hash (even distribution)
- By range (date-based)
- Cross-shard queries: expensive
- Last resort

---
## Connection Pooling

- DB connections expensive
- App pools and reuses
- pgbouncer, RDS Proxy
- Critical for web apps

---
## Query Cache

- Memcached / Redis in front
- Cache common query results
- Invalidate on write (or TTL)
- 80%+ hit ratio common

---
## Denormalisation For Reads

- Add summary columns
- Trade write complexity for read speed
- Common: counters, totals
- Update via triggers or events

---
## Hot Rows

- A few rows get most updates
- Lock contention; cache thrashing
- Mitigation: queue updates, batch
- Detect: per-row update counters

---
## Common Performance Mistakes

- No indexes &#8594; full table scans
- Too many indexes &#8594; slow writes
- ORM hiding N+1
- Materialised views never refreshed
- Reading from replica without considering staleness
