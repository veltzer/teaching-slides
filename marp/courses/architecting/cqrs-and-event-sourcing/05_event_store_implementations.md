---
tags:
  - architecture:event-sourcing
  - infrastructure:kafka
  - concepts:databases
level: advanced
category: architecture
audience:
  - audiences:architects
  - audiences:developers

---
# Event Store Implementations

---
## What This Chapter Covers

- What an event store must guarantee
- Append-only log design and stream layout
- Optimistic concurrency control
- Three implementation paths: EventStoreDB, RDBMS, Kafka
- Event metadata: timestamps, correlation, causation
- Partitioning and scaling

---
## Requirements of an Event Store

- **Append-only**: events are added, never updated or deleted
- **Per-stream ordering**: events for one aggregate are strictly ordered
- **Optimistic concurrency**: append accepts an `expected_version`
- **Efficient stream read**: load all events for one aggregate quickly
- **Subscription**: tail the global log to drive projections
- **Durability**: a successful append survives crashes

---
## Append-Only Log: The Core Idea

![append_only_log](svg/courses/architecting/cqrs-and-event-sourcing/05_event_store_implementations/append_only_log.svg)

---
## Two Levels of Stream

- **Per-aggregate stream**: `order-42` — strict order, one writer
- **Global stream**: every event from every aggregate, by append order
- Per-aggregate is for loading aggregates and concurrency
- Global is for projections and integrations
- An event has a position in both

---
## Stream Layout

![stream_layout](svg/courses/architecting/cqrs-and-event-sourcing/05_event_store_implementations/stream_layout.svg)

---
## Optimistic Concurrency Control

- Append takes `expected_version` — the version the writer thinks the stream is at
- Store rejects the append if the actual version differs
- No locks; the writer retries on conflict (we covered this in chapter 3)
- Cheap to implement; scales well; the write path stays single-writer per aggregate

---
## Optimistic Concurrency in SQL

```sql
INSERT INTO events (stream_id, version, type, data)
VALUES ($1, $2, $3, $4);
-- A unique constraint on (stream_id, version) does the work:
-- a duplicate (stream_id, version) raises a unique violation.
-- That's the conflict the application must catch and retry.
```

- Schema: one table, two important columns, one composite unique index
- Conflicts surface as a uniqueness violation
- Many production systems run on exactly this pattern

---
## EventStoreDB: Purpose-Built

- Streams are first-class entities, not derived from tables
- Built-in subscriptions (catch-up and persistent)
- Built-in projections engine
- Strong append semantics: `ExpectedRevision` is part of the protocol
- Operationally heavier than "Postgres + a table" but built for this job
- Open-source core, commercial cluster

---
## EventStoreDB Append

```python
client.append_to_stream(
    stream_name=f"order-{order_id}",
    current_version=expected_version,  # or ANY / NO_STREAM / STREAM_EXISTS
    events=[
        NewEvent(
            type="OrderPlaced",
            data=json.dumps(payload).encode(),
            metadata=json.dumps(meta).encode(),
        ),
    ],
)
```

- Stream name encodes the aggregate
- Concurrency is built into the API
- Metadata is a separate, structured field

---
## EventStoreDB Subscription

```python
async for event in client.subscribe_to_all(from_position=last_position):
    await projection.handle(event)
    await checkpoints.save(event.commit_position)
```

- Tail `$all` from the position you last processed
- Projection handlers update read models
- Checkpoint after each successful handler call
- Restart resumes from the saved checkpoint

---
## Postgres as an Event Store

- One table; an `events` table with columns:
    - `stream_id`, `version`, `global_position` (bigserial)
    - `type`, `payload` (jsonb), `metadata` (jsonb)
    - `occurred_at`, `appended_at`
- Unique index on `(stream_id, version)` for concurrency
- Index on `global_position` for projections
- Trustworthy, well-understood, easy to operate

---
## A Postgres Schema Sketch

```sql
CREATE TABLE events (
    global_position BIGSERIAL PRIMARY KEY,
    stream_id       TEXT     NOT NULL,
    version         INT      NOT NULL,
    type            TEXT     NOT NULL,
    payload         JSONB    NOT NULL,
    metadata        JSONB    NOT NULL,
    occurred_at     TIMESTAMPTZ NOT NULL,
    appended_at     TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (stream_id, version)
);
CREATE INDEX events_stream_idx ON events (stream_id, version);
```

---
## Reading a Stream From Postgres

```sql
SELECT version, type, payload, metadata
FROM events
WHERE stream_id = $1
ORDER BY version ASC;
```

- One indexed lookup
- Returns all events for the aggregate in order
- Pair with a snapshot table to short-circuit long streams (chapter 7)

---
## Postgres: The Projection Subscription

- Polling: `SELECT ... WHERE global_position > $last`
- LISTEN/NOTIFY: the inserter notifies subscribers immediately
- Logical replication: tail the WAL via a tool like Debezium
- All three work; choose based on latency and operational comfort

---
## Apache Kafka as an Event Log

- Topic per aggregate type (`orders`, `payments`)
- Partition key = aggregate id, so all events for one aggregate land on one partition
- Within a partition, order is strict
- Across partitions, order is not — but that's fine because aggregates don't share partitions

---
## Kafka Append Semantics

- Out of the box, Kafka does **not** support optimistic concurrency
- You build it on top: an idempotent producer + a per-aggregate sequence number you check
- Some teams use Kafka Streams' interactive queries to enforce versioning
- Others use Kafka as the **integration log** and another store as the **system of record**

---
## Kafka as Event Log: Diagram

![kafka_as_event_log](svg/courses/architecting/cqrs-and-event-sourcing/05_event_store_implementations/kafka_as_event_log.svg)

---
## Comparing the Three

![event_store_comparison](svg/courses/architecting/cqrs-and-event-sourcing/05_event_store_implementations/event_store_comparison.svg)

---
## Event Metadata

- **event_id**: stable per-event UUID (idempotent appends)
- **occurred_at**: business time the action happened
- **appended_at**: store time the event was persisted
- **correlation_id**: ties together events from one user action / workflow
- **causation_id**: the event_id of the event (or command) that caused this one
- **actor**: who issued the originating command

---
## Why Correlation and Causation Matter

- **Correlation** — debugging: "show me everything that happened in this checkout"
- **Causation** — tracing: "this projection update was triggered by which append?"
- Without them, distributed debugging is guesswork
- Free to add, expensive to bolt on later

---
## Causation Chain

![causation_chain](svg/courses/architecting/cqrs-and-event-sourcing/05_event_store_implementations/causation_chain.svg)

---
## Partitioning Strategies

- **By aggregate id**: each aggregate's events land together (the default)
- **By tenant**: all events for one customer share a partition (multi-tenant systems)
- **By aggregate type**: each type to its own partition (rarely a good idea — hot partitions)
- The partition key affects both write throughput and projection ordering

---
## Hot Partition Anti-Pattern

- A few aggregates produce most of the events
- They all hash to the same partition; throughput is bottlenecked
- Mitigations:
    - Compose the partition key (`tenant#aggregate_id`)
    - Sub-partition busy aggregates
    - Accept the bottleneck if the aggregate is naturally hot (a daily summary aggregate)

---
## Scaling: Reads vs Writes

- **Writes**: bounded by the slowest single-aggregate stream's append latency
- **Reads (loading aggregates)**: bounded by the per-stream read; snapshots help
- **Reads (projections)**: tail the global log; horizontal by projection consumer
- **Writes scale by aggregate cardinality** — split aggregates into smaller ones if needed

---
## Snapshotting Is Coming

- We will cover snapshots in chapter 7
- For now: a snapshot is a saved aggregate state at a known version
- Loading an aggregate becomes "load latest snapshot, then events after that version"
- Necessary when streams grow into thousands of events

---
## Operational Concerns

- **Backups**: the event store is a high-value target for backup; frequent and tested
- **Disk growth**: events accumulate forever; budget for it
- **Schema evolution**: every event format change forces upcasters or migration
- **Subscriptions**: lag must be monitored; backpressure if projections fall behind
- **Replay storms**: a full rebuild of all read models hammers the store; rate-limit

---
## A Practical Recommendation

- Start with **Postgres** unless you already have something better
    - Easy to reason about, easy to operate, well understood
- Move to **EventStoreDB** when subscription complexity outgrows polling
- Use **Kafka** as the integration log between services, not as the system of record
- Re-evaluate as the system grows; the write path is small enough to migrate

---
## Common Mistakes

- **Hot global stream**: every event going through one partition; rebuilds choke
- **Mutable events**: someone "fixed" an event in place; replay no longer reproduces state
- **Missing concurrency check**: two writers, both appending; lost update
- **No replay tooling**: rebuilding a read model from scratch is "scary" instead of "Tuesday"
- **Schema-less events**: no contract; readers fail in silence

---
## Summary

- The event store guarantees append-only writes, per-stream ordering, optimistic concurrency, and efficient subscriptions
- Postgres is a great default; EventStoreDB excels at subscriptions; Kafka excels as integration
- Stream design has two levels: per-aggregate and global; both matter
- Metadata (correlation, causation, ids) makes debugging tractable
- Partitioning, hot streams, and replay tooling determine operational happiness
