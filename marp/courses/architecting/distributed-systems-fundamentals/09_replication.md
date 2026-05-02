---
tags:
  - concepts:replication
level: intermediate
category: architecture
audience:
  - audiences:developers
  - audiences:architects

---
# Replication

---
## Topologies

![replication_topologies](svg/courses/architecting/distributed-systems-fundamentals/09_replication/replication_topologies.svg)

---
## What This Chapter Covers

- Why replicate
- Single leader vs multi leader vs leaderless
- Synchronous vs asynchronous
- Replication lag
- Read replicas
- Conflict handling
- Practical guidance

---
## Why Replicate

- Durability: survive a node failure
- Availability: read from any replica
- Read scaling: many replicas, more reads
- Latency: replicas closer to users
- Disaster recovery: cross-region copies

---
## Single-Leader Replication

- One node: leader; accepts writes
- Followers: replicate from leader; serve reads
- Most common pattern
- Postgres, MySQL, MongoDB (default), most relational DBs
- Simple; well-understood

---
## Multi-Leader Replication

- Multiple leaders accept writes
- Replicate to each other
- Conflicts possible: same key written on two leaders
- Conflict resolution required
- Active-active multi-region setups

---
## Leaderless Replication

- Any node accepts writes
- Writes go to multiple nodes (quorum)
- Reads from multiple nodes (quorum)
- Cassandra, DynamoDB, Riak
- High availability; no leader to fail

---
## Synchronous Replication

- Write succeeds only after replicas ack
- Stronger durability
- Higher latency (network round trip per replica)
- Risk: one slow replica blocks all writes
- Often: at least one synchronous replica

---
## Asynchronous Replication

- Leader writes locally; replicates later
- Faster
- Risk: leader fails before replication = data lost
- Standard for read replicas
- Trade-off: latency vs durability

---
## Semi-Synchronous

- At least one synchronous replica; others async
- Bounded latency; reasonable durability
- The Postgres / MySQL default in production
- Pragmatic compromise

---
## Replication Lag

- Followers are behind the leader
- Lag: tens of ms typical; can grow under load
- Reading from replica = reading stale data
- Read-your-writes: must read from leader (or session-pinned replica)
- Monitor lag; alert on growth

---
## Read Replicas

- Followers serve read traffic
- Leader: writes only (or writes + reads)
- Scales reads near-linearly
- Doesn't scale writes
- Most cloud DBs offer this

---
## Read-Your-Writes Consistency

- After your write, you should see it
- Write goes to leader; reads from replica may not see it yet
- Solutions:
    - Read from leader for "your" data
    - Wait for replica to catch up before reading
    - Pin user to one replica for session

---
## Failover

- Leader dies
- Promote a follower
- Replicate the rest of the data
- Update DNS / service discovery
- Time: seconds to minutes; may lose unrepicated data

---
## Conflict Resolution (Multi-Leader)

- **Last Write Wins**: timestamp-based; loses data
- **Multi-value**: keep both; let app resolve
- **Custom merge**: domain-specific
- **CRDTs**: deterministic merge
- Pick by data semantics

---
## Replication Topologies

- Star: one leader, many followers
- Chain: leader &#8594; follower &#8594; follower
- All-to-all: multi-leader full mesh
- Each: trade-offs in latency, write amplification, complexity

---
## Cross-Region Replication

- Slow links (50-150ms inter-continental)
- Bandwidth limited
- Async replication usually
- Disaster recovery; geographically-distributed reads
- Cost: replication bandwidth charges

---
## Common Replication Mistakes

- Async replication + reading from replicas without considering staleness
- One-replica setup ("we have backups") &#8594; not really replicated
- Failover not tested
- Replication lag not monitored
- Multi-leader without conflict strategy

---
## Practical Tips

- Always have at least one replica (durability + failover)
- Measure replication lag; alert on it
- Test failover regularly
- Read-your-writes: handle deliberately
- Match consistency model to user expectations
