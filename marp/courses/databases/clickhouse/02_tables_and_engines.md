---
tags:
  - databases:clickhouse
level: intermediate
category: databases
audience:
  - audiences:developers
  - audiences:data-engineers

---
# Tables and Engines

---
## What This Chapter Covers

- Engine families
- Merge tree details
- Specialized merge engines
- Distributed engine
- External engines

---
## Engine Families

- Merge-tree variants for storage
- Distributed for sharding
- Log family for small data
- Integration engines for sources

---
## Merge Tree

- Default workhorse
- Sorted by sort key
- Partitioned by partition key
- Indexed by primary key

---
## Compaction Over Time

![mergetree_compaction](svg/courses/databases/clickhouse/02_tables_and_engines/mergetree_compaction.svg)

---
## Sort Key

- On-disk order
- First columns matter most
- Drives skip-index efficiency
- Pick by query filters

---
## Partition Key

- Logical chunking
- One folder per partition
- Smaller chunks ease drop and TTL
- Often by month or day

---
## Primary Key

- Subset of sort key
- Sparse index in memory
- Granules of about 8K rows
- Skips data the query cannot need

---
## Replacing Variant

- Same key replaced on merge
- Eventual deduplication
- Use the explicit final modifier to ensure
- Good for upserts

---
## Summing Variant

- Sums same-key rows on merge
- Pre-aggregated totals
- Saves storage and reads
- Approximate until merged

---
## Aggregating Variant

- Stores aggregate states
- Combine on merge
- Materialized view target
- Power of pre-computation

---
## Collapsing Variant

- Sign column flips delete
- Pair of insert and delete rows
- Useful for change feeds
- Tricky to use correctly

---
## Distributed Engine

- Routes queries across shards
- Read fan-out
- Write either local or distributed
- Pair with sharding key

---
## External Engines

- Read object storage directly
- Read another relational source
- Federate without import
- Useful for ad-hoc joins

---
## Materialized Views

- Insert trigger pipelines
- Land into another table
- Often an aggregating target
- Powers fast dashboards

---
## Common Engine Mistakes

- Wrong sort key for the query
- Too many partitions
- Replacing variant without explicit final modifier when needed
- Distributed write without sharding key
- Materialized views without target table
