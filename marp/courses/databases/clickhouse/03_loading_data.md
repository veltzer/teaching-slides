---
tags:
  - databases:clickhouse
level: intermediate
category: databases
audience:
  - audiences:developers
  - audiences:data-engineers

---
# Loading Data

---
## What This Chapter Covers

- Insert patterns
- Batch sizing
- Async inserts
- File formats
- Streaming ingest

---
## Insert Basics

- INSERT INTO ... VALUES or SELECT
- Multi-row preferred
- Block size matters
- Avoid one-row inserts

---
## Why Batch

- Each insert creates a part
- Many small parts hurt merges
- Aim for hundreds of thousands of rows
- Or aggregate at the edge

---
## Insert Patterns

![insert_anti_patterns](svg/courses/databases/clickhouse/03_loading_data/insert_anti_patterns.svg)

---
## Pattern Compared

![batch_insert_pattern](svg/courses/databases/clickhouse/03_loading_data/batch_insert_pattern.svg)

---
## Async Inserts

- Server-side batching
- Multiple producers combine
- Reduces small-part problem
- Per-table setting

---
## Buffer Engine

- In-memory write buffer
- Flushes to backing table
- Volatile across restarts
- Useful for spiky writes

---
## Bulk Loading

- INSERT INTO FROM file or URL
- HTTP interface for clients
- Native protocol fastest
- Parallel inserts across nodes

---
## File Formats

- Tab-separated, CSV, JSON
- Native binary formats fastest
- Parquet for interchange
- Compress on the wire

---
## Compression on the Wire

- LZ4 default
- ZSTD for higher ratios
- Server CPU vs network
- Pick by load

---
## Streaming Ingest

- Kafka engine reads topics
- Materialized view writes to MergeTree
- Idempotent producers required
- Watch consumer lag

---
## RabbitMQ and More

- Similar pattern
- Engine reads, view writes
- Built-in for several queues
- HTTP for everything else

---
## CDC From Source DB

- Source emits change feed
- Land in raw table
- Materialized view shapes for query
- Use replacing variant for current state

---
## Schema On Write

- Plan columns up front
- Add columns easily
- Rename and drop with care
- Test with sample loads

---
## Errors and Retries

- Idempotent insert via unique key
- Or quorum across shards
- Retry on network failure
- Avoid duplicate rows

---
## Common Loading Mistakes

- Tiny inserts in production
- No async insert
- Streaming without idempotency
- One file format per pipeline
- Insert into Distributed without checking sharding
