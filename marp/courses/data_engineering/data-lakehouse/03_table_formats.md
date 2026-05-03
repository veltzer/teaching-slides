---
tags:
  - data-and-ai:data-engineering
level: intermediate
category: data-engineering
audience:
  - audiences:data-engineers
  - audiences:architects

---
# Open Table Formats

---
## What This Chapter Covers

- Why a table format
- Snapshots
- Time travel
- Schema evolution
- Compaction

---
## Why a Table Format

- ACID over object storage
- Atomic commits
- Concurrent writers safely
- Catalog for metadata

---
## Family of Formats

- Iceberg
- Delta
- Hudi
- Each with strengths

---
## Table Formats Compared

![table_formats](svg/courses/data_engineering/data-lakehouse/03_table_formats/table_formats.svg)

---
## Snapshots

- Each commit creates a snapshot
- Immutable
- Lists which files belong
- Forms the basis for time travel

---
## Time Travel

- Query as-of timestamp or version
- Useful for debugging
- Useful for audits
- Reproducible analytics

---
## Snapshots Over Time

![snapshots_time_travel](svg/courses/data_engineering/data-lakehouse/03_table_formats/snapshots_time_travel.svg)

---
## Schema Evolution

- Add column
- Rename column
- Change nullability
- Drop column

---
## Schema Compatibility

- Strict reads on type changes
- Backfilled defaults for new columns
- Document deprecation
- Coordinate writers and readers

---
## Partition Evolution

- Change partition strategy without rewriting
- Iceberg supports
- Delta and Hudi differ
- Saves migration cost

---
## Compaction

- Merge small files
- Reduce metadata pressure
- Background or scheduled
- Tunable thresholds

---
## Vacuum and Retention

- Delete files past retention
- Reclaim cost
- Loses time travel for older versions
- Tune to compliance and cost

---
## Concurrency

- Optimistic concurrency
- Conflicts on overlapping writes
- Retry with rebase
- Most writes commute

---
## Streaming Writes

- Append-only into a table
- Compaction follows
- Mind exactly-once integration
- Producers must be idempotent

---
## Catalog

- Maps table name to metadata location
- Hive-compatible
- AWS Glue
- Cloud-native catalogs

---
## Common Table-Format Mistakes

- Mixed write engines without locks
- Vacuum too aggressive
- No compaction schedule
- Schema changes uncoordinated
- Catalog is single point of failure
