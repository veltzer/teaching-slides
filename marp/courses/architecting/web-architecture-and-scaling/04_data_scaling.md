---
tags:
  - architecting:patterns
  - practices:scalability
level: intermediate
category: architecting
audience:
  - audiences:architects

---
# Data Scaling

---
## What This Chapter Covers

- Replication
- Sharding
- Read replicas
- Consistency
- Polyglot persistence

---
## Why Data Is Hard

- Scaling reads is easy
- Scaling writes is harder
- Strong consistency limits both
- Trade-offs are physical

---
## Vertical Database Scaling

- Bigger instance
- Faster disk
- More memory
- Buys time, not eternity

---
## Read Replicas

- Async copy of primary
- Reads spread across replicas
- Writes still serial to primary
- Replica lag must be measured

---
## Lag Effects

- Read your writes broken
- Stale reads visible
- Application must tolerate
- Or pin reads for short window

---
## Sharding

- Partition data across nodes
- Each node owns a slice
- Linear write scaling
- Cross-shard queries are hard

---
## Replication vs Sharding

![replication_sharding](svg/courses/architecting/web-architecture-and-scaling/04_data_scaling/replication_sharding.svg)

---
## Shard Keys

- High cardinality
- Match the query pattern
- Avoid hot shards
- Often hardest design choice

---
## Resharding

- Adding nodes is painful
- Use consistent hashing
- Or virtual buckets
- Plan early, do late

---
## CAP

- Consistency, Availability, Partition tolerance
- Pick two during a partition
- Default is AP or CP
- Document the choice

---
## Eventual Consistency

- Updates converge
- Reads may be stale briefly
- Cheaper to operate
- App must show this state

---
## Strong Consistency

- Reads see latest write
- Coordination required
- Higher latency
- Some workloads demand it

---
## Polyglot Persistence

- Right database per use case
- Relational for transactions
- Document for nested data
- Search engine for text
- Wide-column for time series

---
## Caching Layer

- Read-through for hot data
- Independent of database
- Beware coherence
- Measure hit rate

---
## Common Data Scaling Mistakes

- Sharding before measuring
- Wrong shard key
- Read replicas treated as primaries
- Ignoring replication lag
- One database for everything
