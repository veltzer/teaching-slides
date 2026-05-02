---
tags:
  - databases:cassandra
level: intermediate
category: databases
audience:
  - audiences:developers
  - audiences:dba

---
# Performance

---
## What This Chapter Covers

- Storage internals
- Compaction
- Caching
- Read and write paths
- Tuning

---
## SSTables

- Sorted on-disk files
- Immutable
- New writes go to memtable then flush
- Compaction merges them later

---
## Memtable

- In-memory write buffer
- Flushed to SSTable
- Tunable size
- Big means fewer flushes

---
## Commit Log

- Append-only durability log
- Every write goes there first
- Survives crashes
- Replayed on startup

---
## Write Path

- Commit log append
- Memtable update
- Acknowledge
- Async flush to SSTable

---
## Read Path

- Bloom filter check
- Memtable lookup
- SSTable lookups
- Merge results

---
## Both Paths Visualized

![write_read_paths](svg/courses/databases/cassandra/04_performance/write_read_paths.svg)

---
## Bloom Filters

- Quickly reject misses
- Per-SSTable
- Tunable false positive rate
- Memory cost

---
## Key Cache

- Hot row positions in SSTables
- Speeds reads
- Tuned per node
- Free heap saves cost

---
## Row Cache

- Full rows in memory
- Hot data only
- Memory hungry
- Off by default

---
## Compaction Strategies

- Size-tiered: write-heavy
- Leveled: read-heavy
- Time window: time-series
- Pick per table

---
## Tombstone Cleanup

- Compaction removes tombstones
- gc_grace_seconds bounds visibility
- Too short risks resurrection
- Default 10 days

---
## Hot Partitions

- One key takes all traffic
- One node overloaded
- Re-shard with composite keys
- Monitor partition size

---
## Driver-Side Tips

- Token-aware policies
- Prepared statements
- Connection pooling
- Idempotent retries

---
## Common Performance Mistakes

- Wrong compaction strategy
- Wide partitions
- Read with large LIMIT
- Counters under heavy retry
- Heap too big or too small
