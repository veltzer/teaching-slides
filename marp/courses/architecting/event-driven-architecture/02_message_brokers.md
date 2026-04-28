---
tags:
  - infrastructure:brokers
  - tools:kafka
  - tools:rabbitmq
level: intermediate
category: architecture
audience:
  - audiences:developers
  - audiences:devops

---
# Message Brokers and Streaming Platforms

---
## What This Chapter Covers

- Topics, queues, partitions, consumer groups
- Apache Kafka in depth
- RabbitMQ exchanges and routing
- AWS SNS/SQS, Azure Service Bus
- Choosing a broker; serialization formats; dead-letter queues

---
## Broker Fundamentals

- A broker accepts events from producers and delivers to consumers
- Persists events for some duration
- Handles concurrency, ordering, and delivery guarantees
- Different brokers make different trade-offs
- The right broker depends on the workload

---
## Topics and Queues

- Topic: pub-sub channel; many consumers each see all messages
- Queue: point-to-point; one of N consumers gets each message
- Some brokers (RabbitMQ) build both via exchanges
- Some (Kafka) use topics with consumer groups for both modes
- Same vocabulary, different semantics across brokers

---
## Partitions

- A topic split into N parallel logs
- Each partition is processed in order by one consumer at a time
- Partition key chooses which partition a message lands in
- Concurrency = number of partitions
- Choosing the key is a critical design decision

---
## Consumer Groups

- A group of consumers cooperating to process a topic
- Each partition assigned to one consumer in the group
- Adding consumers up to N partitions scales horizontally
- Past N, extra consumers idle
- Different groups consume independently — pub-sub at the group level

---
## Broker Architecture Visualized

![broker_architecture](svg/courses/architecting/event-driven-architecture/02_message_brokers/broker_architecture.svg)

---
## Apache Kafka: The Big Idea

- A distributed, persistent, replicated log
- Topics are partitioned across brokers
- Replication factor controls durability
- Consumers track their own offset
- Re-reading old messages is a feature, not a bug

---
## Kafka Partitioning

- Each partition is an ordered, append-only log
- Messages with the same key always land in the same partition
- Within a partition, order is guaranteed
- Across partitions, order is not
- Pick partition keys to align with consumer locality

---
## Kafka Consumer Groups

- Each consumer instance reads a subset of partitions
- The group coordinates: rebalance on membership change
- Offsets are committed back to Kafka per group
- Scaling: add consumers up to the partition count
- One consumer per partition is the typical max

---
## Kafka Offsets and Replay

- Offset: the position a consumer has reached
- Committed manually (at-least-once) or automatically (at-most-once)
- Reset to a previous offset to replay history
- Powerful for backfills, A/B testing new consumer logic
- Be careful — replay can flood downstream systems

---
## RabbitMQ: Exchanges and Queues

- Producers send to an exchange, not a queue
- The exchange routes based on rules
- Direct, topic, fanout, headers — different routing strategies
- Queues bind to exchanges with routing keys
- More flexible routing than Kafka; less throughput

---
## RabbitMQ Routing Strategies

- Direct: exact match on routing key
- Topic: pattern match with wildcards (`order.*.created`)
- Fanout: broadcast to every bound queue
- Headers: route based on message headers
- Pick per use case; RabbitMQ shines at flexible routing

---
## AWS SNS and SQS

- SNS: pub-sub, fan-out to many subscribers
- SQS: queue, point-to-point work distribution
- SNS → SQS: a common pattern for fan-out + work distribution
- Fully managed, integrated with IAM
- Serverless workloads benefit from these

---
## SNS Filtering

- Subscribers can attach a filter policy
- Only matching messages are delivered to that subscriber
- Reduces unnecessary load on consumers
- Cheaper than each consumer dropping messages itself
- Filter policies are JSON-based and limited but useful

---
## Azure Service Bus

- Enterprise-focused, transactional messaging
- Topics with subscriptions (filters per subscription)
- Sessions for ordered processing per session ID
- Dead-letter queues built in
- More enterprise features (transactions, scheduling) than SQS

---
## Pulsar: A Modern Alternative

- Combines Kafka-style log with RabbitMQ-style queueing
- Multi-tenant by design
- Tiered storage: hot data on disk, old data in object storage
- Geo-replication built in
- Less mainstream but technically strong

---
## Choosing a Broker

- Throughput needs: Kafka and Pulsar handle millions/sec
- Routing complexity: RabbitMQ wins
- Cloud lock-in: SNS/SQS or Service Bus for AWS/Azure simplicity
- Operational team: Kafka requires more ops investment
- Ecosystem: Kafka has the largest

---
## Dead Letter Queues

- A separate queue for messages that consistently fail
- Most brokers have built-in support
- Configure max retry attempts before DLQ
- Monitor DLQ growth — it's an alert worth setting
- Triage process: investigate, fix, replay

---
## Serialization: JSON

- Human-readable; easy to debug
- No schema enforcement at the broker level
- Schema drift bites silently
- Verbose on the wire — bigger payloads
- Default for many teams; OK for low-throughput

---
## Serialization: Avro

- Schema-based, compact binary
- Schema registry stores and versions schemas
- Native compatibility checking (backward, forward, full)
- Confluent ecosystem favors Avro
- Better than JSON for high-throughput, schema-strict environments

---
## Serialization: Protobuf

- Schema-based, very compact, fast
- Strong typing across languages
- gRPC's native format
- Schema evolution works similarly to Avro
- Often paired with Buf for schema management

---
## Choosing a Format

- JSON for low-volume internal events; readability matters
- Avro for Kafka with schema registry; high-throughput
- Protobuf for cross-language polyglot teams
- Stick with one per system to reduce cognitive load
- Document schemas alongside service code

---
## Topology Patterns

- Single broker, single topic — simple, fast
- Topic per event type — discoverable but proliferates
- Topic per aggregate — aligns with business
- Hierarchical topics — `domain.subdomain.event` for routing
- Pick the granularity that matches your team boundaries

---
## Operational Concerns

- Broker downtime is critical infrastructure failure
- Disk space monitoring per partition
- Consumer lag is the canary metric
- Replication factor affects durability and cost
- Backups are different from replication — plan both

---
## Common Pitfalls

- Choosing Kafka without operational expertise
- Letting consumer lag accumulate silently
- Single-partition topics that block parallelism
- Not configuring dead letter queues until something fails
- Schema drift accepted as "we'll fix it later"

---
## Summary

- Brokers are critical infrastructure with diverse trade-offs
- Kafka for log-style high-throughput; RabbitMQ for routing flexibility
- Cloud brokers for managed simplicity
- Serialization choice matters at scale
- Operational discipline (lag, DLQ, schema) determines success
