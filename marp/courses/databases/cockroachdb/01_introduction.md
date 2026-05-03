---
tags:
  - databases:cockroachdb
level: intermediate
category: databases
audience:
  - audiences:developers
  - audiences:dba

---
# Introduction to CockroachDB

---
## What This Chapter Covers

- What CockroachDB is
- Why distributed SQL
- Architecture overview
- Use cases
- Course outline

---
## What CockroachDB Is

- Distributed SQL database
- Postgres-compatible wire protocol
- Strong consistency by default
- Survives node, zone, region loss

---
## Why Distributed SQL

- Single-node Postgres caps out
- Sharded MySQL is painful
- Want SQL plus horizontal scale
- Want survivability

---
## How It Differs From Cassandra

- Strong consistency
- Real SQL with joins and transactions
- Slower writes for safety
- Easier app porting

---
## In Context

![cockroach_compare](svg/courses/databases/cockroachdb/01_introduction/cockroach_compare.svg)

---
## How It Differs From Postgres

- No single primary
- Reads and writes scale out
- Some Postgres features missing
- Different tuning approach

---
## Architecture

- Each node serves SQL and storage
- Data ranges replicated using Raft
- Three replicas by default
- Ranges split as data grows

---
## Ranges

- Roughly 512MB chunks
- Replicated across nodes
- Each has a Raft group
- Split and rebalance automatically

---
## Ranges Visualized

![cockroach_ranges](svg/courses/databases/cockroachdb/01_introduction/cockroach_ranges.svg)

---
## Raft

- Consensus per range
- Quorum write
- Leader serves the range
- Tolerates minority loss

---
## Survival Goals

- Zone survivability
- Region survivability
- Configured per database or table
- Drives replica placement

---
## Multi-Region

- Place replicas across regions
- Pin tables by locality
- Trade latency vs survivability
- Native primitives

---
## Compatibility

- PostgreSQL wire and SQL
- Drivers from Postgres ecosystem
- Some functions missing
- Test for drift before porting

---
## Hardware Profile

- Three or more nodes minimum
- SSD strongly preferred
- Plenty of RAM
- Time-synced clocks essential

---
## Course Outline

- Schema design
- Transactions and consistency
- Multi-region
- Performance
- Operations

---
## Common Beginner Mistakes

- One-node deployments in production
- Hot range due to monotonic IDs
- Cross-region transactions for chatty apps
- No clock sync
- Treating it like a single-node DB
