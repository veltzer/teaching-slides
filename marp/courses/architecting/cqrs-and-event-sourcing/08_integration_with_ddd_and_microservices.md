---
tags:
  - architecture:cqrs
  - architecture:event-sourcing
  - practices:ddd
  - concepts:microservices
level: advanced
category: architecture
audience:
  - audiences:architects
  - audiences:developers

---

# Integration with DDD and Microservices

---

## What This Chapter Covers

- Mapping CQRS to DDD building blocks
- Bounded contexts and event ownership
- Domain events vs integration events
- Anti-corruption layers and event translation
- Process managers and sagas
- Sharing event stores across services (or not)
- Choreography vs orchestration
- Decomposing monoliths

---

## DDD Recap

- **Ubiquitous language** — shared vocabulary inside a context
- **Bounded context** — explicit boundary around a domain model
- **Aggregate root** — consistency boundary; one root per command
- **Domain event** — a meaningful business fact in the past tense
- CQRS and ES are implementation patterns; DDD is the modeling approach

---

## CQRS Maps Cleanly Onto DDD

| DDD concept | CQRS / ES expression |
|---|---|
| Aggregate | Write model; emits events |
| Domain event | Event in the stream |
| Repository | Event store reader/writer |
| Domain service | Command handler logic across aggregates |
| Bounded context | Service boundary; owns its event streams |
| Anti-corruption layer | Event translator at context boundary |

---

## DDD Mapping Visualized

![ddd_mapping](svg/courses/architecting/cqrs-and-event-sourcing/08_integration_with_ddd_and_microservices/ddd_mapping.svg)

---

## Aggregate Boundaries Are Event Boundaries

- A command operates on one aggregate (chapter 3)
- Events emitted belong to that aggregate
- The stream `order-42` only contains events from the Order aggregate
- This keeps the consistency story simple

---

## Bounded Context Boundaries Are Service Boundaries

- A bounded context typically becomes a service or module
- Each service owns its event streams
- Other services receive only the events the owning service decides to publish
- Internal events (the full stream) stay private to the context

---

## Domain Events vs Integration Events

- **Domain event**: emitted inside a bounded context; part of the write model's stream
    - "OrderItemAdded" — fine-grained, useful internally
- **Integration event**: published across context boundaries
    - "OrderPlaced" — coarser; only what other contexts need to know
- The two have different schemas, audiences, and lifecycles

---

## Domain vs Integration Events

![domain_vs_integration_events](svg/courses/architecting/cqrs-and-event-sourcing/08_integration_with_ddd_and_microservices/domain_vs_integration_events.svg)

---

## Why the Distinction Matters

- Domain events are an internal contract; the schema can evolve with the aggregate
- Integration events are an external contract; breaking them hurts other services
- Without the split, every internal change risks downstream breakage
- Treat integration events with the same care as a public API

---

## Publishing Integration Events

- A subscriber tails the internal event stream
- For each domain event, decide whether to publish an integration event (and which)
- Publish to a broker (Kafka, RabbitMQ, NATS, EventBridge)
- The integration event has its own schema, owned by the publishing context
- Subscribers in other contexts consume only what they care about

---

## Event Publishing Pipeline

![integration_event_publishing](svg/courses/architecting/cqrs-and-event-sourcing/08_integration_with_ddd_and_microservices/integration_event_publishing.svg)

---

## Anti-Corruption Layer

- A translator at the context boundary
- Maps incoming events into terms that make sense in this context
- Prevents another context's vocabulary from polluting yours
- Often the right place to handle versioning of integration events

---

## ACL Example

- The Billing context receives `OrderPlaced` from the Sales context
- Sales' `OrderPlaced` has fields like `customer_id`, `items`, `shipping_address`
- Billing only cares about `customer_id`, total amount, and a billing reference
- The ACL maps Sales' event into Billing's `BillingRequest` event
- Billing's domain language stays clean

---

## Process Managers

- An aggregate that coordinates a multi-step workflow across aggregates
- Listens for events; emits commands in response
- Has its own state and its own event stream
- "When OrderPlaced happens, reserve inventory, then capture payment, then schedule shipping"

---

## Saga Pattern

- A long-running workflow with explicit compensation steps
- Each step that succeeds may need to be undone if a later step fails
- Implemented as a process manager that tracks step status
- The compensation steps are themselves commands; the saga decides when to fire them

---

## Saga Example

![saga_example](svg/courses/architecting/cqrs-and-event-sourcing/08_integration_with_ddd_and_microservices/saga_example.svg)

---

## Saga Failure Compensation

```diagram
OrderPlaced              → ReserveInventory ✓
InventoryReserved        → CapturePayment ✓
PaymentCaptured          → ScheduleShipping ✗ (carrier outage)

# Saga compensates
ShippingScheduleFailed   → RefundPayment ✓
PaymentRefunded          → ReleaseInventory ✓
InventoryReleased        → MarkOrderFailed
```

- Each step has a reverse step
- The saga emits the reverse commands when needed
- Compensation may itself fail; the saga must handle that too

---

## Choreography vs Orchestration

- **Choreography**: each service reacts to events; no central coordinator
    - Loose coupling, but the workflow is implicit and hard to trace
- **Orchestration**: a process manager / saga drives the workflow explicitly
    - Tighter coupling, but the workflow is visible and debuggable
- Use orchestration when the workflow is non-trivial; choreography when it is simple

---

## Choreography vs Orchestration

![choreography_vs_orchestration](svg/courses/architecting/cqrs-and-event-sourcing/08_integration_with_ddd_and_microservices/choreography_vs_orchestration.svg)

---

## When Choreography Wins

- Few steps; each is independent
- The workflow is unlikely to grow
- Teams are autonomous and can change their service without coordinating

---

## When Orchestration Wins

- Many steps; they have dependencies and ordering constraints
- Compensation logic is complex
- The workflow itself is a domain concept the business cares about
- Debugging "why didn't this happen?" needs a single owner

---

## Sharing the Event Store?

- One event store per service: each context owns its streams
- One global event store: all services read and write to one place
- The first scales independently; the second simplifies cross-context queries
- Most production systems pick the first; integration events flow through a broker

---

## One Store Per Service

![one_store_per_service](svg/courses/architecting/cqrs-and-event-sourcing/08_integration_with_ddd_and_microservices/one_store_per_service.svg)

---

## Decomposing a Monolith

- Identify a bounded context to extract
- Add events to the monolith for that context's domain actions
- Build a parallel service that subscribes to those events and runs new logic
- Switch traffic from monolith to service per use case
- Eventually, retire the monolith's logic for that context

---

## Strangler Fig + Events

![strangler_fig_with_events](svg/courses/architecting/cqrs-and-event-sourcing/08_integration_with_ddd_and_microservices/strangler_fig_with_events.svg)

---

## Strangler Fig Steps

- Phase 1: monolith handles all traffic; events emitted internally
- Phase 2: parallel service consumes events, builds its own read model
- Phase 3: traffic for some commands is routed to the new service
- Phase 4: monolith stops handling those commands
- Phase 5: monolith and new service coexist; gradually more is moved

---

## Identity in Cross-Context Events

- An aggregate id is local to its context
- An integration event needs identifiers that work across contexts
- Common pattern: include both — the local id (for traceability) and a stable cross-context id
- Avoid leaking implementation-specific ids; use semantic ones

---

## Versioning Integration Events

- Integration events are an external contract; breaking changes hurt
- Strategies (similar to chapter 2's domain event strategies):
    - Additive only: never remove fields, never change types
    - Versioned types: `OrderPlacedV1`, `OrderPlacedV2` published in parallel for a window
    - Schema registry: every event validated against a registered schema
- Most teams use additive-only with a registry for safety

---

## Event Schema Registry

- A central place that holds the schema of every integration event
- Producers register; consumers validate
- Tools: Confluent Schema Registry, AWS EventBridge schemas, Apicurio
- Catches breaking changes before they reach production

---

## A Reasonable Topology

- One event store per bounded context (per microservice)
- Per-context streams for internal domain events
- Integration events published to a shared broker (Kafka, EventBridge)
- ACLs at every consuming boundary
- Process managers for workflows that span contexts
- Schema registry for integration event contracts

---

## Common Mistakes

- **Sharing aggregates across contexts**: defeats the boundary
- **Leaking domain events as integration events**: every internal change ripples outward
- **No anti-corruption layer**: another team's vocabulary infects yours
- **Choreographing complex workflows**: the workflow is invisible and unmaintainable
- **No versioning discipline on integration events**: every release is a risk

---

## Summary

- DDD provides the modeling; CQRS and ES provide the implementation
- Aggregate boundaries are event boundaries; bounded contexts are service boundaries
- Domain events stay internal; integration events are an external contract
- Process managers and sagas handle workflows that span aggregates or contexts
- Choreography for simple flows; orchestration for complex ones
- One event store per context; integrate via brokers and ACLs
