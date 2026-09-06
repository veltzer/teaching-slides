---
tags:
  - architecture:cqrs
  - concepts:design-patterns
level: advanced
category: architecture
audience:
  - audiences:architects
  - audiences:developers

---

# Introduction to CQRS

---

## What Is CQRS?

- **Command Query Responsibility Segregation**
- A pattern that separates the model that updates state (commands) from the model that reads state (queries)
- Coined by Greg Young around 2010, building on Bertrand Meyer's Command-Query Separation
- Two models that share a name space and a domain — but not their internal structure

---

## Command-Query Separation: The Older Idea

- Bertrand Meyer (1988): every method should either
    - Perform an action and return nothing (a command), or
    - Return a value and have no side effects (a query)
- Operates at the method level — about clarity in object-oriented code
- A useful local discipline, but not an architecture

---

## CQRS Goes Further

- Splits the entire application into two cooperating models, not just methods
- Each model has its own object graph, its own persistence, its own scaling characteristics
- Reads and writes evolve independently
- The two halves are kept consistent by event flow, not by sharing tables

---

## The Classic Single-Model Picture

![single_model_architecture](svg/courses/architecting/cqrs-and-event-sourcing/01_introduction_to_cqrs/single_model_architecture.svg)

---

## The CQRS Picture

![cqrs_architecture](svg/courses/architecting/cqrs-and-event-sourcing/01_introduction_to_cqrs/cqrs_architecture.svg)

---

## What Problem Does It Solve?

- Read and write traffic almost always have different shapes
    - Reads: many concurrent requests, denormalized lookups, fast joins
    - Writes: fewer requests, strict invariants, transactional safety
- A single model serving both is a compromise that satisfies neither
- CQRS lets each side optimize for its real workload

---

## Why CQRS Was Introduced

- Domain models grew complex with read concerns
    - DTOs, ViewModels, and projections leaking into the aggregate
- Reporting requirements forced denormalization that didn't belong in the write model
- Performance tuning for reads polluted the write side and vice versa
- Teams needed to scale read replicas independently from the write path

---

## The Difference From Read Replicas

- A read replica is **the same schema** kept in sync at the database level
- CQRS is **a different model entirely**, often with a different schema, store, and update path
- Read replicas help with read throughput
- CQRS helps with read **shape** — joins precomputed, aggregates already rolled up
- A system can use both: CQRS read models on top of replicated stores

---

## Read Replicas vs CQRS

![read_replicas_vs_cqrs](svg/courses/architecting/cqrs-and-event-sourcing/01_introduction_to_cqrs/read_replicas_vs_cqrs.svg)

---

## Commands

- A request to change state, named in the imperative
    - `PlaceOrder`, `CancelReservation`, `ChangeShippingAddress`
- Carries everything the system needs to validate and apply the change
- May fail — invariant violations, conflicts, authorization
- Returns acknowledgement of acceptance, not data

---

## Anatomy of a Command

```python
@dataclass(frozen=True)
class PlaceOrder:
    order_id: OrderId
    customer_id: CustomerId
    items: list[LineItem]
    shipping_address: Address
    placed_at: datetime
```

- Immutable
- Self-describing — the type itself tells you what the user wants
- Includes a stable identifier so the operation can be made idempotent

---

## Queries

- A request to read state, named as a question
    - `GetOrderSummary`, `ListPendingShipments`, `OrderHistoryFor`
- Returns data shaped for a specific consumer
- Has no side effects and is safe to retry
- May be served from a denormalized cache or projection

---

## Anatomy of a Query

```python
@dataclass(frozen=True)
class GetOrderSummary:
    order_id: OrderId

@dataclass(frozen=True)
class OrderSummary:
    order_id: OrderId
    customer_name: str
    total: Money
    status: str
    last_updated: datetime
```

- The result type belongs to the read model, not the write model
- Names match the screen or API the result will fill

---

## Command and Query Responsibilities

- Commands own invariants, transactions, and emitting events
- Queries own joins, denormalization, caching, pagination
- Each side has its own validation rules
    - Commands: business invariants (must be enforced)
    - Queries: filter and authorization (must reflect what the caller may see)

---

## Synchronous Command Handling

- Caller waits for the command to be accepted, processed, and persisted
- Returns success or a specific error
- Easy to reason about; matches HTTP request/response well
- Couples the caller's latency to the slowest step on the write path
- Every async fan-out (notifications, integrations) must be deferred

---

## Asynchronous Command Handling

- Caller submits the command, gets an acknowledgement, and polls or subscribes for the result
- Decouples user-facing latency from background work
- Requires correlation IDs and a result channel (status endpoint, websocket, email)
- Makes "did my command succeed?" a real question with a real answer
- Standard for long-running or fan-out-heavy operations

---

## Sync vs Async at a Glance

![sync_vs_async_commands](svg/courses/architecting/cqrs-and-event-sourcing/01_introduction_to_cqrs/sync_vs_async_commands.svg)

---

## CQRS in a Layered Architecture

- The application layer accepts a command, hands it to the domain
- The domain enforces invariants and produces events
- The infrastructure layer persists events and updates read models
- Queries skip the domain entirely and hit the read model directly

---

## CQRS in Hexagonal Architecture

- Two primary ports: a command port and a query port
- The domain hexagon holds only the write model
- Read adapters project events into read stores
- Read queries hit a different adapter that talks to the read store
- The two halves never share an object — they share an event stream

---

## CQRS in Hexagonal Architecture (Diagram)

![cqrs_in_hexagonal](svg/courses/architecting/cqrs-and-event-sourcing/01_introduction_to_cqrs/cqrs_in_hexagonal.svg)

---

## When CQRS Pays Off

- Read and write workloads diverge sharply in shape or volume
- The domain has rich invariants that the read side does not need
- Multiple read models serve different consumers (mobile, reports, search)
- Audit, history, or replay are first-class requirements
- Teams need to scale read and write independently

---

## When CQRS Is Overkill

- Simple CRUD where reads are essentially the rows you just wrote
- Small teams who can't afford two models worth of code
- Strong read-after-write consistency is non-negotiable everywhere
- The added eventual consistency is a worse trade-off than the duplication you'd avoid

---

## A Common Anti-Pattern: CQRS Everywhere

- Splitting trivial CRUD into commands and queries adds ceremony without value
- Two models for a five-field entity is two times the code, half the clarity
- Apply CQRS to bounded contexts where the trade-off pays — not by default

---

## CQRS Without Event Sourcing

- The two patterns are independent
- A CQRS system can store its write model in a normal relational database
- Read models are then updated via change data capture or explicit projection events
- Useful when the team wants the read/write split but not the operational cost of an event store

---

## CQRS With Event Sourcing

- The natural pair: events are both the persistence format **and** the projection input
- The same event stream rebuilds aggregates and feeds read models
- Adds time travel, audit, and replay essentially for free
- Pays for itself when the domain is event-shaped to begin with

---

## Frameworks and Libraries

- **Java/Kotlin**: Axon Framework, Eventuate, Lagom
- **.NET**: NEventStore, Marten, Wolverine
- **Python**: eventsourcing, dddesign, message-bus styles built on FastAPI
- **Node/TypeScript**: Wolkenkit, NestJS CQRS module
- **Polyglot infrastructure**: EventStoreDB, Apache Kafka, Apache Pulsar
- A framework is optional — CQRS is a structure, not a technology

---

## The Cost Side of the Ledger

- Two models means two sets of types, repositories, and tests
- Eventual consistency leaks into the user experience
- Operational complexity: more queues, more topics, more dashboards
- Onboarding cost: developers need to learn the split before they can ship

---

## Common Misconceptions

- "CQRS means using events" — no, CQRS is the read/write split; events are common but optional
- "CQRS means microservices" — also no, CQRS works inside a monolith
- "CQRS solves consistency" — it usually relaxes it on the read side; consistency on the write side is up to you
- "CQRS is always faster" — it's often slower for trivial cases, faster for complex ones

---

## A Decision Framework

- Map the read patterns and the write patterns in the bounded context
- If they differ in shape or volume by an order of magnitude, CQRS likely pays
- If they're symmetric, prefer a single model and revisit later
- Decide per bounded context, not per system

---

## Course Roadmap

- Chapter 2: Event Sourcing fundamentals (the natural companion)
- Chapters 3-4: implementing the command side and the query side
- Chapter 5: event store implementations
- Chapter 6: eventual consistency and projections
- Chapter 7: snapshotting
- Chapter 8: integration with DDD and microservices
- Chapter 9: testing CQRS/ES systems

---

## Summary

- CQRS splits the read model from the write model
- It is older and more general than Event Sourcing — they are independent patterns
- It pays off when read and write workloads diverge or the domain has rich invariants
- It costs more code, more operational surface, and more cognitive overhead
- Apply it per bounded context, not by default
