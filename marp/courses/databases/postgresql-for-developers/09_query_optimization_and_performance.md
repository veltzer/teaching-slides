---
tags:
  - databases:postgresql
  - databases:performance
level: intermediate
category: databases
audience:
  - audiences:developers

---

# Query Optimisation and Performance

---

## EXPLAIN Anatomy

![explain_anatomy](svg/courses/databases/postgresql-for-developers/09_query_optimization_and_performance/explain_anatomy.svg)

---

## What This Chapter Covers

- EXPLAIN
- ANALYZE for actual times
- Common slow patterns
- Statistics
- Configuration tuning
- A practical workflow

---

## EXPLAIN

```sql
EXPLAIN SELECT * FROM users WHERE email = 'a@b.com';
```

- Shows query plan
- Without running
- Gives expected costs and rows

---

## EXPLAIN ANALYZE

```sql
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'a@b.com';
```

- Actually runs the query
- Shows actual times and rows
- The truth-teller

---

## Reading Plans

- Indented tree
- Each node: a step (Seq Scan, Index Scan, Hash Join, ...)
- Cost: planner's estimate
- Actual time: real measurement
- Rows: estimated vs actual

---

## Common Plan Issues

- Seq Scan on a big table (no index)
- Hash Join when Nested Loop would be better (or vice versa)
- Sort that doesn't fit in memory
- Wildly wrong row estimates (statistics out of date)

---

## ANALYZE Statistics

```sql
ANALYZE users;
ANALYZE;  -- all tables
```

- Updates planner statistics
- Run after big data changes
- autovacuum does this; sometimes needs manual

---

## Slow Patterns

- N+1 queries (fetch list, then one per item)
- Cartesian product (missing JOIN condition)
- LIKE with leading wildcard (`'%foo'`)
- Functions on indexed columns (`WHERE LOWER(email) = ...`)

---

## Configuration

- shared_buffers: 25% of RAM typical
- effective_cache_size: 75% of RAM
- work_mem: per-query; tune per workload
- max_connections: tune to actual usage
- autovacuum_*: never disable

---

## Connection Pooling

- pgbouncer: lightweight pooler
- Most apps don't open thousands of connections
- A pooler limits to ~50-100 actual connections
- Critical for cloud DBs

---

## Auto Explain

```bash
shared_preload_libraries = 'auto_explain'
auto_explain.log_min_duration = '500ms'
```

- Logs plans for slow queries
- Catches one-off slowness
- Standard in production

---

## Indexes Aren't Always Used

- Small tables: seq scan faster
- Functions on indexed columns
- Type mismatches
- Statistics out of date
- Each disables index use

---

## Vacuuming

- Reclaims space
- Updates visibility map
- autovacuum tunes by table activity
- Manual VACUUM ANALYZE for special cases

---

## Bloat

- Update / delete creates dead tuples
- Indexes bloat too
- Vacuum reclaims; doesn't shrink
- VACUUM FULL or pg_repack to shrink

---

## A Workflow

- Find slow query (pg_stat_statements)
- EXPLAIN ANALYZE
- Identify the bad node
- Add / fix index, rewrite, change config
- Re-measure

---

## Common Performance Mistakes

- No pg_stat_statements
- Indexes never measured (some never used)
- Vacuum disabled
- shared_buffers default (128MB)
- ORM queries unprofiled (N+1 hidden)

---

## Course Wrap-Up

- Postgres is a powerful, mature database
- Internals: WAL, MVCC, vacuum
- Advanced SQL: CTEs, lateral, windows
- JSONB for semi-structured data
- Indexes: many types; pick by query
- Performance: measure, then tune
