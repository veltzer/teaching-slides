---
tags:
  - concepts:microservices
  - concepts:distributed-systems
level: intermediate
category: architecture
audience:
  - audiences:developers
  - audiences:architects

---
# Inter-Service Communication

---
## Two Fundamental Styles

- **Synchronous request/response**: A calls B and waits for an answer
- **Asynchronous messaging**: A emits an event/message; B reacts later
- Most systems use both, deliberately, in different places
- Choosing per case is the design skill

---
## Synchronous: Examples

- HTTP/REST: most common
- gRPC: efficient binary protocol over HTTP/2
- GraphQL: flexible query API
- All are blocking calls; the caller waits

---
## Synchronous: Pros

- Simple mental model: like a function call
- Immediate feedback: you know if it worked
- Easier to reason about ordering
- Tooling and debugging are mature

---
## Synchronous: Cons

- Tight runtime coupling: if B is down, A is affected
- Cascading failures: B is slow → A is slow → A's caller is slow
- Latency stacks: chain of calls = sum of latencies
- Reduces availability (B's downtime = A's degraded mode)

---
## Asynchronous: Examples

- Message brokers: Kafka, RabbitMQ, NATS, AWS SQS
- Event-driven: A publishes, many can subscribe
- Command queues: A queues a command, B processes when ready
- All are non-blocking from the producer's perspective

---
## Asynchronous: Pros

- Loose runtime coupling: A doesn't need B to be up right now
- Better availability under partial failure
- Backpressure for free: queue absorbs spikes
- Multiple consumers easily

---
## Asynchronous: Cons

- Harder to reason about: ordering, timing, idempotency
- Debugging is harder — what triggered what?
- Eventual consistency: results aren't immediate
- More moving parts to operate

---
## When Synchronous Wins

- The caller genuinely needs the result before continuing
- Read operations (queries)
- User-facing flows where freshness matters
- Simple internal RPC where availability is high

---
## When Asynchronous Wins

- Side effects that don't block the caller (notifications, indexing)
- Workflows that span time (orders, deployments)
- One-to-many fan-out
- High-throughput data pipelines

---
## A Rule of Thumb

- Read = synchronous (usually)
- State change = synchronous if user-facing, async if user has waited enough
- Side effects of a state change = async
- Workflows = async

---
## REST vs gRPC

- REST: HTTP+JSON; universally readable; loose schema
- gRPC: HTTP/2+protobuf; efficient; strong schema
- REST for public APIs; gRPC for internal service-to-service
- GraphQL is a third option for client-facing aggregation

---
## Schema for Async

- Messages have schemas just like APIs
- Use Avro, Protobuf, or JSON Schema
- Versioning is harder for async — consumers may be on different versions for a long time
- Schema registries enforce compatibility

---
## Choosing a Broker

- Kafka: durable log; many consumers; high throughput; complex to operate
- RabbitMQ: classic queue; good routing; smaller scale
- NATS: lightweight; high speed; simpler durability story
- Cloud-managed (SQS, EventBridge, Pub/Sub): less operational burden, vendor lock-in

---
## Service Mesh

- A layer that handles service-to-service communication uniformly
- mTLS, retries, timeouts, circuit breakers, observability
- Examples: Istio, Linkerd, Consul Connect
- Adds complexity but centralizes the cross-cutting concerns

---
## Avoiding Sync Chains

- A → B → C → D — every hop adds latency and failure modes
- Refactor: A calls a coordinating service that knows the workflow
- Or: make the chain async with events
- Long synchronous chains are brittle

---
## API Gateway in Front

- A gateway translates external requests into internal calls
- Aggregates multiple service calls when needed
- Hides internal topology from clients
- Covered in detail in the API Design course

---
## Idempotency Across Boundaries

- Cross-service retries are inevitable
- Every state-changing call must be idempotent
- Use idempotency keys; deduplicate on the receiving side
- Without idempotency, retries cause duplicates

---
## Anti-Patterns

- Synchronous chains across many services for one user request
- Async messaging when the caller actually needs the result
- Custom protocols when REST or gRPC would do
- One broker for all data — operational single point of failure

---
## Summary

- Sync = simple but coupled; async = decoupled but complex
- Pick per case, not per system
- REST or gRPC for sync; Kafka/RabbitMQ/NATS for async
- Long sync chains are an anti-pattern
- Idempotency is mandatory for both styles
