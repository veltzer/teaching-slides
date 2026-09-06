---
tags:
  - databases:clickhouse
level: intermediate
category: databases
audience:
  - audiences:developers
  - audiences:data-engineers

---

# Introduction to ClickHouse

---

## What This Chapter Covers

- What ClickHouse is
- When to use
- When not to use
- Architecture
- Course outline

---

## What ClickHouse Is

- Columnar OLAP database
- Designed for analytical queries
- Vectorized execution
- Fast scans on huge tables

---

## Vectorized Execution

![vectorized_engine](svg/courses/databases/clickhouse/01_introduction/vectorized_engine.svg)

---

## Why It Wins

- Bytes scanned per second is huge
- Compression is excellent
- SQL is familiar
- Open source

---

## When To Use

- Time-series and event data
- Real-time dashboards
- Log analytics
- High-cardinality counts

---

## Strengths Overview

![clickhouse_strengths](svg/courses/databases/clickhouse/01_introduction/clickhouse_strengths.svg)

---

## When Not To Use

- Transactional workloads
- Heavy updates and deletes
- Many small queries
- Strong consistency needs

---

## Architecture

- Tables on disk in column files
- Data parts merged in background
- Distributed across shards
- Replicated for safety

---

## Merge Tree Family

- Default engines
- Replacing, summing, and aggregating variants
- Each automates a pattern
- Pick by data and query

---

## Sharding and Replication

- Shard for capacity
- Replicate for durability
- Both required at scale
- ZooKeeper or Keeper coordinates

---

## Data Types

- Integers and floats sized like C
- Low-cardinality types for repeated strings
- Nullable cost
- Date and timestamp types built-in

---

## Indexing Model

- No traditional B-tree
- Sparse primary index
- Skip indexes for filters
- Min-max stats per granule

---

## Query Path

- Parse and plan
- Read parts in parallel
- Vectorized operations
- Stream results

---

## Hardware Profile

- Many cores help
- SSD strongly preferred
- RAM for caches and joins
- Network for distributed reads

---

## Course Outline

- Tables and engines
- Loading data
- Querying
- Operations
- Performance

---

## Common Beginner Mistakes

- Updating like a relational store
- Sort columns not aligned with filters
- Many small inserts
- Wide string columns without low-cardinality types
- Joins without distribution thought
