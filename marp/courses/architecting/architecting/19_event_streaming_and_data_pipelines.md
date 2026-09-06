---
tags:
  - concepts:architecture
  - concepts:event-streaming
  - concepts:kafka
  - concepts:data-pipelines
level: advanced
category: architecture
audience:
  - audiences:developers
  - audiences:architects

---

# Event Streaming and Data Pipelines

---

## Why Event Streaming Is Architectural

- Events decouple services in time and in knowledge
- A streaming platform becomes the circulatory system of a distributed architecture
- The same events drive online services, analytics, and audit logs
- Architecture decisions about the stream reach every team that touches data

---

## Messages vs Events vs Streams

- **Message** — a unit of communication; request/response or fire-and-forget
- **Event** — a fact about something that happened, named in past tense
- **Stream** — an append-only sequence of events, retained for replay
- Queue semantics delete on consumption; stream semantics retain for all consumers

---

## Why Kafka Won

- Append-only log with per-partition ordering
- Retention decoupled from consumption — multiple consumers read independently
- Horizontal scalability via partitions
- At-least-once and exactly-once semantics available
- Ecosystem: Connect, Streams, Schema Registry, ksqlDB

---

## Kafka Concepts

- **Topic** — a named stream of events
- **Partition** — a shard of a topic; ordering is per-partition, not per-topic
- **Offset** — a monotonically increasing position within a partition
- **Producer** — writes events to a topic
- **Consumer** — reads events from a topic, tracks its own offset
- **Consumer group** — a set of consumers sharing partitions for parallelism

---

## Topic Design

- One topic per event type, not per service
- Partition count determines maximum consumer parallelism within a group
- Partition key determines ordering — pick the key so related events land on the same partition
- Changing partition counts later breaks key-based ordering — choose carefully

---

## Retention Strategies

- **Time-based** — retain events for N days (7, 30, 365 common)
- **Size-based** — cap per-partition storage
- **Compaction** — keep the latest event per key, discard older versions
- **Infinite retention** — event sourcing, audit logs, system-of-record use cases

Compacted topics act like a key-value store backed by a log.

---

## Producers: Delivery Semantics

- **At-most-once** — fire and forget; data loss possible
- **At-least-once** — retry until acked; duplicates possible
- **Exactly-once** — idempotent producer + transactions
- Exactly-once is real in Kafka but constrains throughput and requires careful design

---

## Consumers: Position and Replay

- Each consumer group tracks its own offsets
- A new consumer group can read from the beginning — full replay
- Reset offsets to reprocess after a bug fix
- Retention must be long enough to recover from the slowest consumer's outage

---

## Event Schema Evolution

- Events outlive the code that produced them — schema must evolve backward-compatibly
- **Avro + Schema Registry** — enforces compatibility at produce time
- **Protobuf** — similar story, strongly typed codegen
- **JSON with JSON Schema** — simpler but no enforcement by default
- Rule: add optional fields; never remove or rename in place

---

## The Outbox Pattern

The dual-write problem: updating the database and publishing an event are not atomic.

Outbox fixes it:

- Write the event to an `outbox` table *in the same transaction* as the business change
- A relay process reads the outbox and publishes to Kafka
- On failure, retry — the outbox row is still there
- Guarantees at-least-once delivery without 2PC

---

## Change Data Capture (CDC)

- Tail the database's write-ahead log and publish each change as an event
- No application-side outbox needed — the database itself is the source
- Tools: `Debezium`, `AWS DMS`, `Fivetran`
- Great for legacy systems that cannot be refactored to emit events

---

## CDC Trade-Offs

- **Pros**: zero code changes, every change captured, naturally ordered
- **Cons**: events reflect schema, not domain concepts; tight coupling to DB internals; heavy replication slots
- Works best as an integration mechanism for read models, not as a primary domain event source
- Pair with a transformation layer to map rows to domain events

---

## Event Sourcing Revisited

- Store every state change as an immutable event; derive current state by replay
- Kafka (with compaction off) is a plausible event store
- Dedicated event stores: `EventStoreDB`, `Axon`
- Snapshotting every N events keeps replay tractable for long-lived aggregates

---

## Event Sourcing Considerations

- Schema evolution is harder — old events must still be replayable
- Reporting requires projections; no ad-hoc SQL over state
- Rehydration cost grows with aggregate lifetime — plan for snapshots
- Strong fit: audit-heavy domains (finance, healthcare); weak fit: simple CRUD

---

## Stream Processing

- Transform streams into new streams or materialized views in real time
- Stateful operations: joins, aggregations, windowing
- Exactly-once processing requires end-to-end coordination
- Tools: `Kafka Streams`, `Apache Flink`, `Spark Streaming`, `ksqlDB`

---

## Stream Processing Use Cases

- Real-time analytics — windowed aggregations over clickstreams
- Fraud detection — joining transaction and signal streams
- Enrichment — augmenting events with reference data
- Materialized views — read models updated continuously
- Alerting — thresholds evaluated on live data

---

## Windowing

- **Tumbling** — non-overlapping fixed-size windows (every 5 minutes)
- **Hopping** — overlapping fixed-size windows (5-minute window, 1-minute hop)
- **Session** — groups events separated by inactivity
- **Event-time vs processing-time** — correct handling of out-of-order and late events

---

## Watermarks and Late Data

- Processing-time is the clock the system sees
- Event-time is when the thing actually happened
- Events arrive out of order due to network and retry delays
- A **watermark** is the processing system's estimate of "event-time has advanced past T"
- Handle late data with allowed lateness + side outputs

---

## Exactly-Once Processing

- Consume + process + produce must be atomic with offset commit
- Kafka Streams implements this via transactions across topics
- Flink does it via distributed snapshots and two-phase commit with sinks
- Every external sink must cooperate (idempotent or transactional)

---

## Kafka Connect

- Framework for moving data in and out of Kafka without custom code
- **Source connectors** — JDBC, Debezium (CDC), filesystems, APIs
- **Sink connectors** — Elasticsearch, S3, JDBC, Snowflake, BigQuery
- Offsets managed by Connect — resumable, fault-tolerant

---

## Data Pipeline Architecture

- **Ingestion** — raw events land in Kafka (or equivalent)
- **Processing** — stream processors transform, join, enrich
- **Storage** — materialized views, analytical stores, data lakes
- **Serving** — APIs and dashboards over the processed data
- **Governance** — schemas, lineage, quality checks at every stage

---

## Lambda vs Kappa Architecture

- **Lambda** — batch pipeline for accuracy + streaming pipeline for freshness
    - Pro: robust, two independent paths
    - Con: two codebases to maintain, reconciliation headaches
- **Kappa** — single streaming pipeline; reprocess by replaying
    - Pro: one codebase, simpler
    - Con: requires long retention and fast reprocessing

Most modern systems target Kappa with Lambda-as-fallback.

---

## Data Lakehouse

- Combines data-lake economics (object storage, open formats) with warehouse features (ACID, schema)
- Formats: `Apache Iceberg`, `Delta Lake`, `Apache Hudi`
- Enables streaming ingestion directly into analytical tables
- Same table queryable by Spark, Trino, Flink, and warehouse engines

---

## Kafka Alternatives

- **Pulsar** — similar capabilities, separated storage/compute
- **Redpanda** — Kafka-compatible, no ZooKeeper/JVM, lower latency
- **NATS JetStream** — lighter-weight streaming for smaller systems
- **Managed** — Confluent Cloud, AWS MSK, Azure Event Hubs, GCP Pub/Sub
- Pick based on ecosystem fit and operational comfort, not raw benchmarks

---

## Operational Concerns

- Partition count vs broker count — too many partitions stress the cluster
- Consumer lag monitoring — the canary of stream health
- ZooKeeper (or KRaft) — the metadata service needs its own care and feeding
- Schema Registry availability — producers and consumers both depend on it
- Topic sprawl — treat topics as first-class resources with owners and docs

---

## Common Mistakes

- **Topic-per-service** instead of topic-per-event-type — couples consumers to service topology
- **JSON without a schema registry** — schema drift becomes everyone's problem
- **Ignoring partition keys** — ordering guarantees vanish silently
- **Dual-writes without outbox** — your database and Kafka will disagree
- **Under-retention** — the first consumer outage becomes a data loss incident

---

## Summary

- Events are facts; streams are retained sequences of facts
- Kafka is the default streaming backbone — partitions, offsets, and consumer groups
- Schema registry + Avro/Protobuf enforces backward-compatible evolution
- The outbox pattern and CDC both solve the dual-write problem
- Stream processing turns streams into real-time views
- Exactly-once is real but costs throughput and constrains design
- Event streaming is architectural — topic layout, retention, and schema are long-lived decisions
