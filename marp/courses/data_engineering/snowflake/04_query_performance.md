---
tags:
  - data-and-ai:data-engineering
level: intermediate
category: data-engineering
audience:
  - audiences:data-engineers

---
# Query Performance

---
## What This Chapter Covers

- Warehouse sizing
- Caching
- Pruning
- Joins
- Plan inspection

---
## Warehouse Sizing

- Bigger means more memory and compute
- Cost doubles each step
- Test on representative load
- Resize without downtime

---
## Auto-Suspend

- Keep small for ad-hoc
- Larger for batch
- Tune suspend timer
- Suspend pause is free

---
## Result Cache

- Same query, same result
- Free for 24 hours
- Invalidated on data change
- Watch for stale-looking expectations

---
## Local Disk Cache

- Per-warehouse cache of micro-partitions
- Warms over time
- Lost on suspend
- Larger warehouses cache more

---
## Pruning Quality

- Filter on clustered or natural-ordered columns
- Inspect bytes scanned vs total
- Add clustering when pruning is poor
- Avoid functions on filter columns

---
## Joins

- Hash joins for most
- Broadcast for small tables
- Skew breaks joins
- Distribute on join keys when ingesting

---
## Plan Inspection

- EXPLAIN
- Query profile UI
- Operator tree
- Spend time on the longest operator first

---
## Materialized Views

- Pre-computed query result
- Maintained as data changes
- Watch maintenance cost
- Best for hot, narrow queries

---
## Search Optimization Service

- Accelerates point lookups
- Costs storage and credits
- Useful for needle-in-haystack
- Not for big scans

---
## Clustering Keys

- Auto-clustering keeps data sorted
- Pick low-cardinality, high-filter columns
- Re-clustering credits monitored
- Drop if not paying off

---
## Spill

- When working set exceeds memory
- Spill to local disk, then remote
- Resize up or rewrite query
- Watch for it in profile

---
## Concurrency

- Multiple warehouses isolate workloads
- Multi-cluster warehouse for spikes
- Batch and BI on different warehouses
- Predictable performance

---
## Common Performance Mistakes

- Too-small warehouse for batch
- One warehouse for all workloads
- No clustering for time-series
- Functions on filter columns
- Ignoring spill
