---
tags:
  - databases:cassandra
level: intermediate
category: databases
audience:
  - audiences:developers
  - audiences:dba

---
# Consistency and Replication

---
## What This Chapter Covers

- Replication topology
- Consistency levels
- Read repair
- Hinted handoff
- Multi-region

---
## Replication Strategy

- Simple strategy: dev only
- Network topology strategy: production
- Configured per keyspace
- Defines copies per data center

---
## Replication Factor

- How many copies of each row
- Per data center
- Higher means more durable and slower
- Common: 3 in production

---
## Ring &amp; Replication

![cassandra_ring](svg/courses/databases/cassandra/03_consistency_and_replication/cassandra_ring.svg)

---
## Tunable Consistency

- Per query
- Read and write levels independent
- Trade latency vs safety
- Application chooses

---
## Common Levels

- ONE: any one replica
- QUORUM: majority
- LOCAL_QUORUM: majority in local DC
- ALL: every replica

---
## Strong Consistency Recipe

- W + R > N
- QUORUM both sides on RF=3 works
- Latency cost on each request
- Use only when needed

---
## Eventual Consistency

- Replicas converge
- Reads may see stale
- Cheaper and faster
- Default mindset

---
## Read Repair

- Coordinator detects mismatch
- Updates stale replicas
- Probabilistic or on every read
- Helps convergence

---
## Hinted Handoff

- Coordinator stores writes for down nodes
- Replays when node returns
- Bounded duration
- Avoids lost writes for short outages

---
## Anti-Entropy Repair

- Background process
- Compares replicas
- Fixes drift
- Schedule in production

---
## Multi-Region

- Replicate across data centers
- Local quorum for low latency
- Cross-DC replication async
- Watch network costs

---
## CAP

- Cassandra is AP by default
- Tunable toward CP per query
- Partitions are tolerated
- Application sees stale during partition

---
## Lightweight Transactions

- Compare-and-set semantics
- Paxos protocol
- Slower than normal writes
- Use sparingly

---
## Common Consistency Mistakes

- ALL for daily reads
- Single-DC for multi-region traffic
- No anti-entropy schedule
- Lightweight transactions everywhere
- Assuming reads see latest write
