---
tags:
  - databases:cockroachdb
level: intermediate
category: databases
audience:
  - audiences:developers
  - audiences:dba

---

# Schema and Indexes

---

## What This Chapter Covers

- Tables and primary keys
- Hot ranges
- Secondary indexes
- Constraints
- Schema changes

---

## Tables

- Standard SQL CREATE TABLE
- Most Postgres types supported
- JSONB, ARRAY, INTERVAL all there
- UUIDs are first-class

---

## Primary Keys

- Required for every table
- Determines key range layout
- Drives data distribution
- Pick carefully

---

## Hot Range Problem

- Monotonic IDs concentrate writes
- One range, one node, one bottleneck
- Use hash-prefixed primary keys
- Or random UUIDs

---

## Hot Range Visualized

![hot_range](svg/courses/databases/cockroachdb/02_schema_and_indexes/hot_range.svg)

---

## Hash-Sharded Index

- Built-in attribute for primary or secondary
- Bucket count chosen
- Spreads load across ranges
- Easy fix for monotonic keys

---

## Secondary Indexes

- Standard CREATE INDEX
- Maintained on writes
- Each index is its own ranges
- Each index multiplies write cost

---

## Index Kinds

![index_kinds](svg/courses/databases/cockroachdb/02_schema_and_indexes/index_kinds.svg)

---

## Inverted Indexes

- For JSONB and arrays
- Allows containment queries
- Larger than B-tree indexes
- Use when needed

---

## Storing Columns

- STORING clause caches columns
- Avoid extra lookup to base table
- Cost in write time and storage
- Pick by query pattern

---

## Constraints

- Primary key
- Foreign key
- Unique
- Check

---

## Foreign Key Cost

- Verified on every write
- Cross-range checks
- Useful but not free
- Sometimes drop in hot tables

---

## Schema Changes

- Online by default
- Multi-step under the hood
- May take hours on huge tables
- Track progress in admin UI

---

## Online Schema Change Phases

- Add backfill
- Validate
- Promote
- Cleanup

---

## Partitioning

- Logical row partitioning by value
- Used heavily for multi-region
- Affects placement and pruning
- Per table or per index

---

## Common Schema Mistakes

- Sequential primary keys at scale
- Too many indexes
- No FK on critical relationships
- Schema change on huge table at peak hours
- Wide JSONB columns without inverted index
