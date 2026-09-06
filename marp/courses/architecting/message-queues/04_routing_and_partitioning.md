---
tags:
  - architecting:patterns
  - queues:overview
level: intermediate
category: architecting
audience:
  - audiences:architects
  - audiences:developers

---

# Routing and Partitioning

---

## What This Chapter Covers

- Partitioned queues
- Routing keys
- Order guarantees
- Hot keys
- Schema management

---

## Partitions

- Queue split into shards
- Each shard ordered
- Across shards no order
- Parallel consumers per shard

---

## Partition Keys

- Function of message field
- Same key, same partition
- Enables per-key ordering
- Distribution depends on key choice

---

## Partitioning Visualized

![partitions_keys](svg/courses/architecting/message-queues/04_routing_and_partitioning/partitions_keys.svg)

---

## Choosing a Key

- High cardinality
- Even distribution
- Stable across messages
- Match the natural unit of order

---

## Hot Partitions

- One key dominates
- Worker overloaded
- Other workers idle
- Solve with composite key or fan-out

---

## Re-Partitioning

- Add shards on load growth
- Order may break across change
- Plan a quiet window
- Or use consistent hashing

---

## Routing Keys

- Topic plus pattern
- Wildcards in some brokers
- Consumers subscribe by pattern
- Powerful but complex

---

## Routing Models

![routing_models](svg/courses/architecting/message-queues/04_routing_and_partitioning/routing_models.svg)

---

## Topic Hierarchy

- "orders.placed", "orders.cancelled"
- Subscribers match prefixes
- Discoverable, debuggable
- Pick a convention early

---

## Schemas

- Producers and consumers must agree
- Schema registry stores definitions
- Validation at write time
- Compatibility rules

---

## Compatibility

- Backward: new consumer reads old data
- Forward: old consumer reads new data
- Full: both directions
- None: only same-version

---

## Avro, Protobuf, JSON Schema

- Binary formats save bytes
- JSON is easy to debug
- Choose by team and infra
- Stick to one per topic

---

## Versioning

- Tag schema version on message
- Or implicit by topic
- Migration plans for breaking changes
- Deprecate, do not delete

---

## Cross-Region

- Replicate selected topics
- Mind ordering across replication
- Producer pinning by region
- Consumer fail-over plan

---

## Common Routing Mistakes

- Single-partition default forever
- Bad partition key choice
- No schema registry
- Breaking schema with no plan
- Wildcard subscriptions in production
