---
tags:
  - data-and-ai:data-engineering
level: intermediate
category: data-engineering
audience:
  - audiences:data-engineers

---
# Tables and Storage

---
## What This Chapter Covers

- Table types
- Micro-partitions
- Clustering
- Time travel
- Cloning

---
## Permanent Tables

- Default table type
- Time travel and fail-safe
- Used for production data
- Cost includes retention

---
## Table Kinds

![table_kinds](svg/courses/data_engineering/snowflake/02_tables_and_storage/table_kinds.svg)

---
## Transient Tables

- No fail-safe
- Time travel up to one day
- Cheaper storage
- For staging data

---
## Temporary Tables

- Session-scoped
- Disappear at session end
- No cost beyond session
- Handy for scratch work

---
## External Tables

- Point at object storage
- Snowflake reads files in place
- No data ingest needed
- Useful for raw zone

---
## Micro-Partitions

- Small immutable column chunks
- 50 to 500 MB compressed
- Created automatically
- Foundation of pruning

---
## Pruning

- Skip partitions that cannot match
- Driven by min and max metadata
- Filter columns benefit most
- Watch the pruning metric

---
## Pruning Visualized

![micro_partitions](svg/courses/data_engineering/snowflake/02_tables_and_storage/micro_partitions.svg)

---
## Clustering

- Co-locate related rows
- Manual or automatic
- Helps when natural ingest order does not
- Costs re-clustering credits

---
## Time Travel

- Query past versions
- Default 1 day, up to 90 in higher editions
- Reverts and audits
- Stops costing once expired

---
## Fail-Safe

- 7 days after time travel ends
- Snowflake-managed recovery
- Not user-accessible
- Insurance against deletion

---
## Cloning

- Zero-copy clones
- Instant
- Independent writes
- Common for testing on real data

---
## Streams

- Track changes to a table
- Deltas since last consume
- Enables incremental processing
- Pairs with tasks

---
## Tasks

- Scheduled SQL
- Single statement or stored proc
- Chains form simple pipelines
- Cheap orchestration

---
## Common Storage Mistakes

- Permanent tables for staging
- No clustering on big tables
- Misuse of time travel for backup
- Cloning forgotten and not cleaned
- Ignoring fail-safe cost
