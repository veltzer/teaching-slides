---
tags:
  - databases:cassandra
level: intermediate
category: databases
audience:
  - audiences:developers
  - audiences:dba

---
# Data Modeling

---
## What This Chapter Covers

- Query-first design
- Partition keys
- Clustering columns
- Denormalization
- Common patterns

---
## Query-First Design

- Start with the queries
- Tables shape around queries
- Reverse of relational thinking
- Multiple tables per entity is normal

---
## Partition Key

- Determines node placement
- All rows for a key live together
- Bound size to a few MB
- High cardinality required

---
## Composite Partition Keys

- Multiple columns combine into one key
- Distribute hot tenants
- Distribute hot timestamps
- Common for time-series

---
## Clustering Columns

- Within a partition
- Define on-disk order
- Enable range queries
- Multiple columns supported

---
## Why Range Within Partition

- Reads are partition-local
- Range scans within a partition are cheap
- Cross-partition scans are expensive
- Plan accordingly

---
## Denormalization

- Same data in multiple tables
- One table per query pattern
- Writes get expensive
- Reads stay fast

---
## Materialized Views

- Server-maintained denormalized copies
- Primary table updates trigger views
- Simplifies app code
- Trade write cost

---
## Counters

- Special distributed counter type
- Increment and decrement
- Not idempotent under retries
- Use carefully

---
## Time-Series Pattern

- Bucket by time period
- Partition key includes bucket
- Clustering by timestamp
- Trim old buckets via TTL

---
## TTL

- Per-row or per-column
- Auto-deletes after window
- Creates tombstones
- Cleaned up by compaction

---
## Tombstones

- Markers for deletes
- Slow reads when many
- Avoid wide partitions of deletes
- Tune compaction to clean fast

---
## Anti-Patterns

- Unbounded partitions
- Querying without partition key
- High-cardinality clustering
- Range over many partitions

---
## Common Modeling Mistakes

- Modeling like SQL
- Tables for entities, not queries
- Partition key with low cardinality
- Hot partitions
- Filtering on non-key columns
