---
tags:
  - tools:kafka
  - data-and-ai:streaming
level: beginner
category: message-queue
audience:
  - audiences:developers

---
# Overview

---
## What This Chapter Covers

- What Kafka is and why it exists
- The mental model: distributed commit log
- Use cases: messaging, streaming, log aggregation
- The Kafka ecosystem
- A short history
- Vocabulary you'll need

---
## What Kafka Is

- A distributed, partitioned, replicated commit log
- Producers append; consumers read
- Records are durable: persisted to disk and replicated
- Sub-millisecond latency at scale
- Originally built at LinkedIn (2010); now Apache top-level

---
## What "Commit Log" Means

- An append-only sequence of records
- Each record gets a monotonically-increasing offset
- Records are immutable once written
- Consumers read by offset
- Same log can be read by many consumers, at their own pace

---
## Distributed and Replicated

- Topics are split into *partitions*
- Each partition lives on multiple brokers (the replicas)
- One replica is the *leader*; others are *followers*
- Producers write to the leader; followers replicate
- Survives broker failures within the replication factor

---
## Why Kafka, Not RabbitMQ?

- Kafka: high-throughput, append-only log
- RabbitMQ: message queue with rich routing
- Kafka excels at: stream processing, event sourcing, log aggregation
- RabbitMQ excels at: per-message routing, request/reply, RPC patterns
- Different tools for different problems; sometimes both

---
## Why Kafka, Not Pulsar?

- Pulsar: similar features, different architecture
- Pulsar separates compute (brokers) from storage (BookKeeper)
- Kafka has the broader ecosystem and adoption
- Pulsar is gaining; Kafka is the safe pick today
- Both are good; pick by ecosystem fit

---
## Use Cases

- **Messaging**: like RabbitMQ but with persistence and replay
- **Stream processing**: continuous transformations on event streams
- **Log aggregation**: centralised collection of app and infra logs
- **Event sourcing**: the log is the source of truth for system state
- **Change data capture**: stream database changes downstream

---
## The Kafka Ecosystem

- **Kafka Core**: producers, consumers, brokers
- **Kafka Connect**: source/sink integrations (DB, S3, Elastic, etc.)
- **Kafka Streams**: stream processing library (Java)
- **ksqlDB**: SQL on streams
- **Schema Registry**: manage schemas (Avro, Protobuf, JSON)
- **MirrorMaker**: cross-datacenter replication

---
## Vocabulary: Topic

- A named stream of records
- Like a "table" in a DB, but append-only
- Topics are split into partitions
- Topic names are the namespacing unit
- Common: `orders`, `users`, `payments`, `clickstream`

---
## Vocabulary: Partition

- One ordered, append-only sequence within a topic
- A topic with N partitions = N parallel streams
- Each partition is read by *one* consumer per consumer group
- Number of partitions = max parallelism
- Partition count is hard to change later — pick carefully

---
## Vocabulary: Offset

- The position of a record within a partition
- Monotonically increasing
- Consumers track their offset; can re-read from any point
- "Replay from yesterday" = seek to yesterday's offset
- Offsets are per partition; not global

---
## Vocabulary: Producer / Consumer

- **Producer**: writes records to topics
- **Consumer**: reads records from topics
- Either can be many; topics scale by partition count
- Both interact with brokers, not each other
- Decoupling is the whole point

---
## Vocabulary: Broker / Cluster

- **Broker**: a Kafka server (one process)
- **Cluster**: a group of brokers
- Each broker hosts a subset of partitions
- A cluster of 5+ brokers is typical for production
- Replication spans brokers within the cluster

---
## Vocabulary: Consumer Group

- A logical group of consumers sharing the work
- Each partition is consumed by *one* consumer in the group at a time
- Add consumers = parallelism increases (up to partition count)
- Multiple groups = multiple independent consumers of the same data
- The basis of Kafka's pub-sub model

---
## A Short History

- 2010: built at LinkedIn for activity stream tracking
- 2011: open-sourced; Apache incubator
- 2014: Confluent founded by Kafka creators
- 2017: Kafka Streams; ecosystem maturity
- 2022: KRaft (Kafka Raft) replaces ZooKeeper dependency
- Today: industry standard for event streaming

---
## Confluent vs Apache Kafka

- Apache Kafka: open source, free
- Confluent Platform: enterprise extras (Schema Registry, Control Center, RBAC)
- Confluent Cloud: managed service
- Most learning materials use Apache Kafka
- Many production deployments use Confluent for the management

---
## What's Next

- Producer API: how to write records
- Consumer API: how to read records (high-level and low-level)
- Configuration: the knobs that matter
- Design points: how Kafka stays fast and reliable
- Each chapter goes deeper into the abstractions you'll meet
