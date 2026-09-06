---
tags:
  - concepts:architecture
  - concepts:events
level: intermediate
category: architecture
audience:
  - audiences:developers
  - audiences:architects

---

# EDA Fundamentals

---

## What This Chapter Covers

- What an event is — and isn't
- Events vs commands vs queries
- Domain, integration, and notification events
- Producer-consumer model
- Trade-offs versus request-driven systems

---

## What Is an Event?

- A statement of fact: "something happened"
- Past-tense by convention: `OrderPlaced`, `PaymentReceived`
- Immutable: facts don't change
- Owned by the producer; consumers cannot rewrite
- Carries enough context to act on without callbacks

---

## What Is Event-Driven Architecture?

- Components communicate by emitting and reacting to events
- Producers don't know who consumes
- Consumers don't know who produced
- Loose coupling — services evolve independently
- Async is the default

---

## EDA Visualized

![eda_overview](svg/courses/architecting/event-driven-architecture/01_eda_fundamentals/eda_overview.svg)

---

## Kinds Of Events

![event_types](svg/courses/architecting/event-driven-architecture/01_eda_fundamentals/event_types.svg)

---

## Events vs Commands

- Event: "OrderPlaced" — a fact, possibly with many listeners
- Command: "PlaceOrder" — an instruction to one specific recipient
- Events look backward; commands look forward
- Mixing them is the most common modeling mistake
- Different mechanics, different guarantees

---

## Events vs Queries

- Event: a fact has occurred — push, async
- Query: I need information — pull, sync (usually)
- Queries can be over event-derived projections
- CQRS makes this distinction architectural
- Don't try to query through an event bus — use a query API

---

## Three Event Types

- Domain events — within a bounded context, reflecting business meaning
- Integration events — between bounded contexts or services
- Notification events — "something happened, ask if you care"
- Different sizes, different consumers, different SLAs
- Don't model all three the same way

---

## Domain Events

- Internal to one service or bounded context
- Rich payload — full state of the changed entity
- Often used to update read models within the same service
- Typically not exposed externally
- The unit of internal communication in DDD

---

## Integration Events

- Cross-service, the API of an event-driven system
- Curated payload — only what consumers need
- Versioned and contract-tested
- Privacy and security considered explicitly
- The most expensive to change once published

---

## Notification Events

- Minimal payload: an ID and the event type
- Consumer pulls full data via a query if interested
- Reduces broker load and avoids stale data
- Increases latency and complexity
- Useful when payload is large or sensitive

---

## Producers and Consumers

- Producer: emits events, doesn't know who reads
- Consumer: subscribes, processes, may emit downstream events
- One producer, many consumers — fan-out
- Many producers, one consumer — convergence
- Both are first-class participants

---

## Pub-Sub vs Point-to-Point

- Pub-sub: one event, many independent consumers — broadcasts
- Point-to-point: one event, one of N consumers — work distribution
- Most brokers support both
- Pub-sub for notifications; point-to-point for tasks
- Mix them within one system as needed

---

## Coupling and Cohesion

- Loose temporal coupling — producer and consumer don't run at the same time
- Loose location coupling — consumers don't need producer's address
- Tight contract coupling — they agree on the schema
- Explicit contracts beat implicit assumptions
- The schema is the API

---

## EDA Trade-Offs: Wins

- Independent scaling per service
- Independent deployment without coordination
- Resilience: queue absorbs producer/consumer downtime
- Natural audit log — events are records
- Easier to add new consumers without changing producer

---

## EDA Trade-Offs: Costs

- Eventual consistency is hard to reason about
- Distributed debugging is genuinely harder
- Schema evolution becomes a permanent concern
- Operational complexity: brokers add a critical dependency
- Test infrastructure must include async paths

---

## When EDA Fits

- Cross-service workflows that aren't request-response
- Many consumers needing the same data
- High-throughput pipelines
- Long-running processes with multiple steps
- Systems that benefit from reactive UX

---

## When Not To Use EDA

- Simple CRUD with one consumer — REST is fine
- Strong consistency requirements with one writer
- Workflows where the response is needed synchronously
- Teams without operational experience for brokers
- Cases where the broker becomes a single point of failure with no plan

---

## EDA in the System Landscape

- Often coexists with REST/GraphQL APIs
- Frontend reads via API; backend reacts via events
- Service-to-service async via events; sync queries via APIs
- Hybrid is the norm — pure EDA is rare
- Pick the mode per use case, not for the whole system

---

## Event Granularity

- Too fine: chatty, expensive, hides intent
- Too coarse: events do too much, consumers filter heavily
- Aim for "what would the business call this?"
- One event per business decision, typically
- Refine over time — granularity isn't fixed in stone

---

## Common Anti-Patterns

- Using events as RPC (request event followed by response event)
- Treating events as transient messages
- Having one consumer that depends on event order across producers
- "Event soup" — every change emits 30 events
- Producers expecting consumers to behave in a specific way

---

## Course Roadmap

- Chapter 2: brokers and streaming platforms
- Chapter 3: event sourcing and CQRS
- Chapter 4: reliability and delivery guarantees
- Chapter 5: sagas and choreography
- Chapter 6: schema evolution
- Chapter 7: microservices in practice

---

## Summary

- Events are immutable facts; commands are instructions
- Three event types: domain, integration, notification
- EDA loosens coupling but adds eventual consistency and operational complexity
- Hybrid with sync APIs is the norm, not the exception
- Get the granularity and contracts right first; the rest follows
