---
tags:
  - tools:kafka
  - data-and-ai:streaming
  - concepts:distributed-systems
level: beginner
category: message-queue
audience:
  - audiences:developers

---
# Design Points

---
## What This Chapter Covers

- Kafka's persistence model
- Producer-side guarantees
- Consumer-side guarantees
- Message delivery semantics
- Replication
- Log compaction in depth
- Why Kafka is fast

---
## Persistence: Append-Only Log

- Each partition is a sequence of segment files on disk
- New records append to the active segment
- Old segments deleted (or compacted) on retention policy
- No random writes; only appends
- Sequential disk I/O is fast even on spinning disks

---
## Durability Levers

![durability_levers](svg/courses/queues/kafka/05_design_points/durability_levers.svg)

---
## Why It's Fast

- Sequential I/O (not random)
- Page cache: kernel handles caching, no app-side cache
- Zero-copy (`sendfile`): bytes go from disk to socket without copying through user space
- Batching everywhere: producer, network, consumer
- Modern Kafka clusters push GB/s per broker

---
## Producer Guarantees

- With `acks=all` + `enable.idempotence`: at-least-once with no duplicates from retries
- With transactional producer: exactly-once across multiple topics
- Without those: at-most-once (or worse)
- Default settings have improved over versions
- Always state your durability needs explicitly

---
## Consumer Guarantees

- Out of the box: at-least-once
- A consumer can re-process records after a crash
- Idempotent processing logic makes this OK
- Exactly-once requires Kafka Transactions or external dedup
- Most production systems work fine with at-least-once + idempotency

---
## Message Delivery Semantics

- **At-most-once**: messages may be lost; never duplicated
- **At-least-once**: messages may be duplicated; never lost
- **Exactly-once**: each message processed exactly once
- Most distributed systems are at-least-once + idempotent consumers
- Exactly-once is hard; Kafka can do it with care

---
## Replication

- Each partition has N replicas (one leader, N-1 followers)
- Producers write to the leader; followers replicate
- Followers fetch from the leader; track the high water mark
- A follower is "in-sync" if it's not too far behind
- Configurable: `replica.lag.time.max.ms`

---
## Leader Election

- When a leader fails, one in-sync replica becomes leader
- The cluster controller orchestrates
- Handled automatically; clients reconnect to the new leader
- Brief unavailability (seconds) during the switch
- `min.insync.replicas` prevents writing during partial failure

---
## Unclean Leader Election

- If no in-sync replica is available, an out-of-sync one can take over
- Risk: data loss
- `unclean.leader.election.enable=false` (the default) prevents this
- Trade-off: with it false, partition becomes unavailable
- Most production setups: false

---
## Log Compaction

- Alternative to time-based deletion
- Keeps the *latest* value per key
- Older values for the same key eventually deleted
- Useful when consumers need full state recovery from the topic
- Used internally for `__consumer_offsets`

---
## When To Use Compaction

- Topic represents *current state* per key (e.g., user profiles)
- Consumers need to bootstrap from the topic
- Bounded space: only as much as the unique key space
- Combined with retention.ms: keep recent history *and* latest
- A powerful pattern for event-sourced systems

---
## Tombstones

- A record with a key and `null` value
- Tells the compactor to delete the key entirely
- Used for "delete this entity"
- Tombstones themselves are eventually deleted (after `delete.retention.ms`)
- The mechanism for log-compacted deletion

---
## In-Sync Replicas (ISR)

- The set of replicas caught up to the leader
- `acks=all` means "all *in-sync* replicas have acked"
- Non-ISR replicas don't block writes
- ISR shrinks if a follower lags; expands when caught up
- `under-replicated-partitions` metric: ISR shrunk; investigate

---
## Producer-Broker Communication

- One TCP connection per broker
- Multiple in-flight requests possible
- Compression and batching reduce overhead
- TLS for security
- Connection pooling handled by the client

---
## Why Kafka Beats Polling Databases

- Polling: wasted queries when nothing changed
- Kafka: push when there's data
- Kafka: many consumers don't add load to the source
- Kafka: replay is built-in
- Kafka: backpressure via consumer groups

---
## When NOT to Use Kafka

- Low-volume messaging (RabbitMQ may be simpler)
- Request/reply patterns (Kafka is one-way)
- Per-message routing rules (use RabbitMQ exchanges)
- Single-message reliability above throughput
- Total ops cost too high for the value

---
## Operational Concerns

- ZooKeeper or KRaft: cluster coordination
- Monitoring: Confluent Control Center, Kowl, Conduktor
- Backup: MirrorMaker 2 for cross-cluster replication
- Capacity: plan for 50% headroom; scale before needing
- Patching: rolling upgrades require careful planning

---
## Common Design Mistakes

- One topic with too many partitions (overhead per partition)
- One topic with too few partitions (can't scale consumers)
- Hot partitions due to bad keying
- No retention policy &#8594; disk fills
- Treating Kafka as a database
- Underestimating the operational complexity

---
## Course Wrap-Up

- Kafka is a distributed commit log
- Producers append; consumers read
- Partitions are the unit of parallelism
- Configuration matters; the defaults aren't always right
- Operations is half the job
- Done well, Kafka is foundational infrastructure
