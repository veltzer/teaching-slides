---
tags:
  - concepts:microservices
  - concepts:observability
level: intermediate
category: architecture
audience:
  - audiences:developers
  - audiences:devops

---

# Event-Driven Microservices in Practice

---

## What This Chapter Covers

- Decomposing monoliths into events
- Service boundaries and event ownership
- Testing strategies
- Observability: tracing, metrics, logging
- Anti-patterns and performance considerations

---

## From Monolith to Events

- Identify the bounded contexts
- Find the natural seams: where one team's work meets another's
- Replace internal calls with events
- Strangler fig: split one boundary at a time
- Decomposition takes time

---

## Bounded Contexts as Service Boundaries

- A bounded context is a coherent model with shared language
- Across boundaries, the same word means different things ("order" in sales vs shipping)
- Events translate between contexts
- Each context owns its data
- Service boundaries should match context boundaries

---

## Service Boundaries Visualized

![service_boundaries](svg/courses/architecting/event-driven-architecture/07_microservices_in_practice/service_boundaries.svg)

---

## EDA Smells

![eda_smells](svg/courses/architecting/event-driven-architecture/07_microservices_in_practice/eda_smells.svg)

---

## Event Ownership

- Each event is owned by one service
- Other services consume but don't define
- Changes go through the owner
- The owner publishes the schema and contract
- Cross-service events need cross-team coordination

---

## Internal vs Public Events

- Internal: within a bounded context, rich and detailed
- Public: across boundaries, curated and stable
- Don't expose internal events as public — they change too often
- Have a translation layer at the boundary
- Treat public events as a stable API

---

## Testing Event-Driven Systems

- Unit: pure logic per service, with test events as input
- Integration: service + broker + DB, in-process or Testcontainers
- Contract: producer and consumer agree on schema and behavior
- End-to-end: full system, expensive but necessary
- Each level catches different bugs

---

## Unit Testing

- Test the event handler logic in isolation
- Mock the broker, DB, downstream services
- Cover: happy path, validation failures, edge cases, idempotency
- Fast feedback for developers
- The first line of defense

---

## Integration Testing

- Spin up the broker (Testcontainers, embedded Kafka)
- Spin up the database
- Publish test events; verify state changes and emitted events
- Catches schema and broker config errors
- Slower but invaluable

---

## Contract Testing

- Producer and consumer share a contract
- Producer publishes per the contract; consumer verifies
- Pact, Spring Cloud Contract, AsyncAPI testing
- Catches mismatches before production
- Especially valuable across team boundaries

---

## Consumer-Driven Contracts

- Consumers describe what they need from events
- Producers verify they meet those expectations
- Inverts the typical "producer dictates" model
- Forces explicit communication about needs
- Reduces "broken by surprise" incidents

---

## End-to-End Testing

- Full stack: real services, real broker, real DB
- Slow and expensive
- Reserve for critical workflows: order placement, payment
- Often run nightly, not per commit
- Necessary but not sufficient

---

## Observability: Distributed Tracing

- Correlation ID flows through every event
- Trace shows the path: service A → event → service B → event → service C
- OpenTelemetry is the industry standard
- Without traces, debugging async flows is brutal
- Instrument from day one

---

## Tracing in Event Systems

- Producer creates a span; correlation ID in headers
- Broker passes headers (most do natively now)
- Consumer extracts correlation ID; creates child span
- The trace shows the cross-service flow
- Latency per step becomes visible

---

## Metrics That Matter

- Producer rate per topic
- Consumer lag per consumer group per partition
- Processing latency per consumer
- Error rate (DLQ growth)
- Schema validation failures
- Broker health: disk, throughput, partition count

---

## Logging in Event Systems

- Structured logs (JSON) with correlation ID always
- Log every event received, sent, processed, failed
- Log levels: INFO for normal flow, WARN for retries, ERROR for failures
- Don't log full event payloads if sensitive
- Centralized log aggregation is mandatory

---

## Correlation IDs in Practice

- Generated at the entry point (HTTP request, scheduled job)
- Propagated in event headers
- Logged in every log statement
- Searchable across services
- The single most useful operational tool

---

## Anti-Pattern: Event Soup

- Every change emits a generic event
- Many small events, hard to compose meaning
- A generic "item updated" event hides what actually changed
- Prefer business-meaningful events like "item price changed"
- Granularity matters

---

## Anti-Pattern: Distributed Monolith

- Microservices that must deploy together
- Service A breaks if service B is down — synchronously
- Often: services share a DB, or a release coordinates them
- The opposite of what microservices promise
- Events should decouple, not just distribute

---

## Anti-Pattern: Temporal Coupling

- Service A assumes service B processes events within X seconds
- Works in test, fails under load
- Replace assumptions with explicit waits or async patterns
- Document timing requirements
- Verify under realistic load conditions

---

## Performance Considerations

- Throughput vs latency trade-offs
- Larger batches: higher throughput, higher latency
- Partition count drives parallelism
- Serialization choice affects both
- Profile before optimizing

---

## Scaling Consumers

- Add consumer instances up to partition count
- Beyond that, increase partitions (carefully — order changes)
- Vertical scaling per consumer for CPU-bound work
- Stateless consumers scale most easily
- Stateful consumers (read models) need coordination

---

## Backpressure Handling

- Slow consumer + high producer = lag accumulates
- Strategies: scale consumers, drop old messages, rate-limit producer
- Bounded queues to prevent OOM
- Choose the strategy per workload
- Monitor lag; alert before it's catastrophic

---

## Deployment Considerations

- Deploy producers and consumers independently
- Schema changes need deployment ordering
- Blue-green deployments work well with consumer groups
- Canary one consumer instance for risky changes
- Rollback plans for schema changes are critical

---

## Migration Strategies

- Strangler fig: extract one capability at a time
- Read first: build read models alongside the monolith
- Then writes: emit events from monolith, consumers act
- Eventually: turn off monolith capabilities
- Patient, iterative; not a big-bang

---

## Common Pitfalls

- Treating events as "messages" — losing semantic meaning
- Schemas without governance
- No observability — debugging by hope
- Sync calls hidden behind async wrappers
- Microservices without a real reason

---

## Course Recap

- Fundamentals — events, commands, queries, types
- Brokers — Kafka, RabbitMQ, cloud options
- Event sourcing and CQRS
- Reliability and delivery guarantees
- Sagas and choreography
- Schema evolution and governance
- Microservices in practice

---

## Summary

- Event-driven microservices need disciplined contracts and observability
- Boundaries should match bounded contexts
- Test at multiple levels; contracts catch the most
- Tracing and correlation IDs are non-negotiable
- The patterns work — when you respect their constraints
