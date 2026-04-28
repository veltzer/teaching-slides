---
tags:
  - concepts:reliability
  - concepts:idempotency
level: intermediate
category: architecture
audience:
  - audiences:developers
  - audiences:devops

---
# Reliability and Delivery Guarantees

---
## What This Chapter Covers

- At-most-once, at-least-once, exactly-once
- Idempotency in consumers
- Deduplication and idempotency keys
- Transactional outbox pattern
- Ordering, retries, poison messages

---
## Three Delivery Semantics

- At-most-once — may be lost, never duplicated
- At-least-once — never lost, may be duplicated
- Exactly-once — never lost, never duplicated
- Most systems offer at-least-once
- Exactly-once is conditional, not absolute

---
## Delivery Semantics Visualized

![delivery_semantics](svg/courses/architecting/event-driven-architecture/04_reliability_and_delivery/delivery_semantics.svg)

---
## At-Most-Once

- The producer sends, doesn't track
- If anything fails, the message is lost
- Lowest latency, lowest overhead
- Suitable: telemetry, low-value notifications
- Not suitable: orders, payments, anything that matters

---
## At-Least-Once

- Producer retries until acknowledgment
- Consumer commits only after successful processing
- May see duplicates from retries
- The default in most reliable brokers
- Requires consumers to be idempotent

---
## Exactly-Once

- The hardest guarantee — and often misunderstood
- Achievable in narrow conditions (Kafka transactions, idempotent producers)
- Across heterogeneous systems, not generally possible
- "Effectively once" via at-least-once + idempotent consumers
- This is what most teams actually deliver

---
## What Is Idempotency?

- An operation is idempotent if applying it twice has the same effect as once
- Mathematical: f(x) = f(f(x))
- Practical: handling the same event twice produces the same result
- The key technique for at-least-once + correctness
- Design for idempotency from the start

---
## Idempotency Patterns

- Track processed message IDs in a database
- Check before applying; ignore if already seen
- Use upserts (INSERT IF NOT EXISTS) where natural
- Naturally idempotent operations: setting state, not incrementing
- Reframe non-idempotent operations into idempotent ones

---
## Idempotency Keys

- A unique ID attached to each message
- Producer assigns; consumer tracks
- Independent of broker-level message IDs
- Persists deduplication across producer retries
- Standard in payment APIs (Stripe, others)

---
## Deduplication Storage

- Where do you track processed IDs?
- Per-aggregate state — natural fit for event-sourced systems
- Dedicated table — `(message_id, processed_at)`
- TTL on dedup records — old IDs eventually expire
- Trade-off: storage cost vs window of dedup

---
## Transactional Outbox Pattern

- Problem: write to DB and emit event atomically
- Without it: DB succeeds, event fails (or vice versa) — split state
- Solution: write event to a local outbox table in the same transaction
- A separate process publishes outbox events to the broker
- Atomicity preserved at the cost of slight latency

---
## Outbox Pattern Visualized

![outbox_pattern](svg/courses/architecting/event-driven-architecture/04_reliability_and_delivery/outbox_pattern.svg)

---
## Implementing Outbox

- Outbox table: `(id, event, status, created_at)`
- Application transaction writes business data + outbox row
- Background worker reads unsent rows, publishes, marks sent
- Handle worker failures: at-least-once publishing
- Tools: Debezium can stream from DB to broker automatically

---
## Inbox Pattern

- The dual: deduplication on the consumer side
- Inbox table tracks processed message IDs
- Consumer transaction: check inbox + process + record in inbox
- Atomic with the business operation
- Pair outbox + inbox for end-to-end exactly-once feel

---
## Ordering Guarantees

- Ordering is a per-partition (Kafka) or per-queue (Rabbit) property
- Across partitions, no global order
- Choose partition keys so related events land together
- Trade-off: more partitions = more parallelism, less ordering scope
- Don't fight ordering — design around it

---
## Retry Policies

- Linear retry: same delay between attempts
- Exponential backoff: doubling delay
- With jitter: randomized to avoid thundering herd
- Cap the number of retries
- Where to retry: in the consumer, or via a delay queue

---
## Poison Messages

- A message that always fails, no matter how many retries
- Without limit, it blocks the queue
- Strategy: max-retries, then move to DLQ
- DLQ requires monitoring — silent rot otherwise
- Triage process: investigate, fix, replay (or accept loss)

---
## Circuit Breakers

- Stop trying when downstream is failing
- Avoid pounding a sick system into worse state
- States: closed (try), open (don't try), half-open (probe)
- Common library: resilience4j, polly, hystrix legacy
- Pair with retries and DLQ for full resilience

---
## Backpressure

- Producer outpaces consumer; queue grows unbounded
- Eventually: out of memory, broker crash
- Solutions: bounded queues, slow producer, drop old messages
- Reactive Streams provides protocol-level backpressure
- Plan for sustained imbalance, not just spikes

---
## Rate Limiting Producers

- Sometimes the producer is the problem
- Token-bucket or leaky-bucket per producer
- Cooperative: producer participates in slowing down
- Coercive: broker rejects when over limit
- Coordinate with capacity planning

---
## End-to-End Latency

- Producer write + broker durability + consumer read + processing
- Each step has its own SLO
- Measure each separately to find bottlenecks
- Latency budget: don't let one step eat the whole budget
- Dashboards per step are non-negotiable

---
## Cross-Service Consistency

- Each local operation is atomic; cross-service is not
- Design with eventual consistency in mind
- Sagas (next chapter) coordinate multi-service transactions
- Don't pretend strong consistency you don't have
- Document the consistency contract per use case

---
## Operational Discipline

- Monitor consumer lag per group per topic
- Alert when lag exceeds budget
- Monitor DLQ growth
- Track event publishing failures
- Reliability is operations, not architecture

---
## Common Pitfalls

- Forgetting idempotency until duplicates appear in production
- Outbox without monitoring — silent data loss when worker hangs
- DLQ without process — fills up, gets ignored
- Retrying everything indefinitely
- Treating "exactly-once" as a guarantee instead of a careful construction

---
## Summary

- At-least-once + idempotent consumers is the typical target
- Idempotency keys make deduplication explicit
- Transactional outbox solves the dual-write problem
- Dead letter queues and retries need operational care
- Reliability comes from discipline, not from any single feature
