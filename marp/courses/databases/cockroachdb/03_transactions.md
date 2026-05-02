---
tags:
  - databases:cockroachdb
level: intermediate
category: databases
audience:
  - audiences:developers
  - audiences:dba

---
# Transactions

---
## What This Chapter Covers

- Isolation level
- Retries
- Contention
- Locks
- Best practices

---
## Default Isolation

- Serializable
- Strongest standard SQL level
- No anomalies under contention
- Costs more than weaker levels

---
## Serializable and Retries

![serializable_retries](svg/courses/databases/cockroachdb/03_transactions/serializable_retries.svg)

---
## Why Serializable

- App developers reason simply
- No phantom reads
- No write skew
- Trade against latency

---
## Optimistic Concurrency

- Reads do not block writers
- Conflicts detected on commit
- Failed transactions retry
- Driver retry helpers exist

---
## Retries

- Transactional save points
- Or full retry from app
- Use idempotent statements
- Cap retries to avoid loops

---
## Hot Rows

- Same row written constantly
- Cluster overhead per write
- Aggregate before write
- Or shard the row

---
## Locks

- Row-level
- Acquired on first read or write
- SELECT FOR UPDATE pre-locks
- Helps reduce retries

---
## Lock Wait

- Default short timeout
- Long waits indicate contention
- Inspect with built-in views
- Tune transaction size

---
## Transaction Size

- Smaller is better
- Bigger transactions hold locks longer
- Bigger means more retries
- Break into idempotent steps

---
## Time and Hybrid Clocks

- Hybrid logical clocks
- Order across nodes
- Requires NTP-class clock sync
- Bounded skew default 500ms

---
## Read Latency

- Local reads possible with leaseholders
- Bounded staleness queries trade for speed
- Follower reads from any replica
- Pick by need

---
## Bounded Staleness

- AS OF SYSTEM TIME
- Read from any replica
- Reduces cross-region latency
- App must tolerate

---
## Causal Consistency

- Across sessions
- Reads see prior writes
- Default for the same connection
- Inspect when sharing connections

---
## Common Transaction Mistakes

- Long-running transactions
- Hot row patterns
- No retry handler
- Misuse of follower reads
- Ignoring contention metrics
