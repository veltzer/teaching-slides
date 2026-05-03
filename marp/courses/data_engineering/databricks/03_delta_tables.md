---
tags:
  - data-and-ai:data-engineering
level: intermediate
category: data-engineering
audience:
  - audiences:data-engineers

---
# Delta Tables

---
## What This Chapter Covers

- Delta basics
- ACID
- Time travel
- Schema evolution
- Optimization

---
## What Delta Is

- Open table format on Parquet
- Transaction log per table
- ACID guarantees
- Default table format on Databricks

---
## Why Delta

- Safe concurrent writes
- Schema evolution
- Time travel
- Streaming and batch on one table

---
## Delta Features

![delta_features](svg/courses/data_engineering/databricks/03_delta_tables/delta_features.svg)

---
## Transaction Log

- JSON files in _delta_log
- Lists added and removed files
- Versioned, immutable
- Source of truth for the table

---
## ACID Properties

- Atomic commits
- Consistent reads
- Isolation between writers
- Durable on object store

---
## Time Travel

- Query as-of version or timestamp
- Useful for audits
- Reproduces past results
- Bounded by retention

---
## Schema Evolution

- mergeSchema option
- Add columns without rewrite
- Renames need explicit migration
- Strict mode prevents accidents

---
## Updates and Deletes

- UPDATE, DELETE, MERGE on tables
- Rewrites affected files
- Compaction needed afterward
- GDPR-style deletes supported

---
## MERGE

- Upsert pattern
- Match by keys
- Insert when absent
- Update when present

---
## OPTIMIZE

- Compact small files
- Improves read speed
- Run after heavy writes
- Schedulable

---
## Z-ORDER

- Multi-column clustering
- Skips files at read time
- Best on filter columns
- Use sparingly

---
## VACUUM

- Removes files past retention
- Frees storage
- Loses time travel for old versions
- Default retention is conservative

---
## Operations Compared

![merge_optimize_vacuum](svg/courses/data_engineering/databricks/03_delta_tables/merge_optimize_vacuum.svg)

---
## Streaming Sources and Sinks

- Read changes as a stream
- Write streams into tables
- Watermarks for late data
- Idempotent batches by default

---
## Common Delta Mistakes

- No OPTIMIZE schedule
- VACUUM with too short retention
- Z-ORDER on every column
- Schema evolution without coordination
- Ignoring small files alarms
