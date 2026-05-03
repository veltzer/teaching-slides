---
tags:
  - databases:cassandra
level: intermediate
category: databases
audience:
  - audiences:developers
  - audiences:dba

---
# Introduction to Cassandra

---
## What This Chapter Covers

- What Cassandra is
- When to use
- When not to use
- Architecture
- Course outline

---
## What Cassandra Is

- Distributed wide-column store
- Eventually consistent by default
- Linear write scalability
- No master node

---
## History

- Born at Facebook
- Open sourced 2008
- Apache project since 2010
- Powers very large workloads

---
## When To Use

- Massive write throughput
- Multi-region active-active
- Time-series and event data
- Always-on requirement

---
## Strengths Visualised

![cassandra_strengths](svg/courses/databases/cassandra/01_introduction/cassandra_strengths.svg)

---
## When Not To Use

- Complex joins
- Strong consistency by default
- Ad-hoc analytics
- Small data with relational shape

---
## Architecture Highlights

- Ring of nodes
- Token-based partitioning
- Replication across nodes
- Tunable consistency

---
## No Master

- Every node is equal
- Coordinator role per request
- Survives node loss
- Simplifies operations

---
## Architecture Overview

![ring_overview](svg/courses/databases/cassandra/01_introduction/ring_overview.svg)

---
## Replication Factor

- Number of copies per row
- Set per keyspace
- Higher means safer and slower
- Cross-data-center common

---
## Consistency Levels

- ONE, QUORUM, ALL
- Per query
- Trade latency for safety
- R + W > N for strong reads

---
## Data Model

- Keyspaces hold tables
- Tables have partition keys
- Tables have clustering columns
- No joins, no constraints

---
## Query Language

- CQL looks like SQL
- Limited expressively
- Designed around partition key
- No subqueries or joins

---
## Hardware Profile

- Many commodity nodes
- SSD strongly preferred
- Lots of RAM
- Network is critical

---
## Cassandra vs Cousins

- ScyllaDB: C++ rewrite, faster
- DynamoDB: hosted, similar shape
- HBase: HDFS underneath
- Each tunes the trade-offs

---
## Course Outline

- Data modeling
- Operations
- Consistency
- Performance
- Failure modes

---
## Common Beginner Mistakes

- Treating it like a relational store
- Modeling around keys you do not query
- Low replication factor
- Reads with ALL consistency
- Ignoring tombstones
