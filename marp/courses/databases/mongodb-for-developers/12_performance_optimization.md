---
tags:
  - databases:mongodb
  - databases:performance
level: intermediate
category: databases
audience:
  - audiences:developers

---
# Performance Optimisation

---
## Checklist

![perf_checklist](svg/courses/databases/mongodb-for-developers/12_performance_optimization/perf_checklist.svg)

---
## Performance Workflow

![perf_workflow](svg/courses/databases/mongodb-for-developers/12_performance_optimization/perf_workflow.svg)

---
## What This Chapter Covers

- Profiling
- Slow query log
- Index usage
- Memory and working set
- Connection pooling
- Common pitfalls

---
## Profiling

```javascript
db.setProfilingLevel(1, { slowms: 100 });
db.system.profile.find().sort({ts: -1}).limit(10);
```

- Level 0: off
- Level 1: slow ops
- Level 2: all ops (debug only)
- Inspect via system.profile collection

---
## Slow Query Log

- Logs queries above slowms
- Shows: collection, query, plan, time
- Standard ops practice
- Atlas: built-in slow query advisor

---
## explain() Plans

```javascript
db.users.find({email: "a@b.com"}).explain("executionStats");
```

- Reveals: index used, docs examined, time
- Look for: COLLSCAN (bad), IXSCAN (good)
- N docs examined &gt;&gt; N returned: index issue

---
## Index Usage

- $indexStats: per-index counters
- Drop unused
- Use compound indexes wisely
- ESR rule

---
## Working Set

- Active data fits in RAM &#8594; fast
- Doesn't fit &#8594; disk reads &#8594; slow
- Atlas: monitor cache usage
- Scale up tier or shard

---
## Connection Pooling

- 100 connections per app process default
- Tune for workload
- Under-pooled: queueing
- Over-pooled: server resource exhaustion

---
## Read Preferences For Scale

- Read from secondaries: spread load
- Not for read-your-write paths
- Eventually consistent
- Effective for analytics

---
## Bulk Writes

- Batch operations: 1 round trip vs N
- Massive speedup for inserts / updates
- Most drivers have bulkWrite

---
## Avoid

- Unbounded queries (no limit)
- Skip on huge collections
- Field manipulation in $where (slow)
- $regex without anchor on indexed field

---
## Aggregation Performance

- $match early
- $project to drop fields
- Use indexes in first stage
- $lookup is expensive; avoid in hot paths

---
## Index Build Performance

- Background by default in modern MongoDB
- Won't block
- Long for big collections
- Monitor progress

---
## Collection Scans

- COLLSCAN: read every document
- Acceptable on small / static collections
- Avoid on hot paths
- Add indexes

---
## Sharding

- For: data &gt; one node's capacity
- Shard key choice critical
- Cross-shard queries slow
- Last resort

---
## Atlas Performance Advisor

- Auto-suggests indexes based on slow queries
- Check periodically
- Implement what it recommends (after review)

---
## Common Performance Mistakes

- No profiling enabled
- Indexes not measured ($indexStats)
- Working set exceeding RAM
- Poor shard key (hot shards)
- N+1 patterns in app code
