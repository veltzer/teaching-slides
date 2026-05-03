---
tags:
  - concepts:domain-driven-design
  - architecture:saga
level: advanced
category: architecture
audience:
  - audiences:architects
  - audiences:developers

---
# Saga Pattern and Distributed Processes

---
## Why DDD Cares About Sagas

- An aggregate is a consistency boundary; one transaction per aggregate
- Cross-aggregate workflows can't be one transaction
- Sagas handle the cross-aggregate (and cross-service) case
- DDD's solution to "what if we need to coordinate"

---
## What a Saga Is

- A sequence of local transactions, each touching one aggregate (or service)
- Each step has a paired compensating action
- On failure, completed steps are compensated in reverse order
- Eventual consistency, not atomic

---
## Two Coordination Styles

![saga_pattern](svg/courses/architecting/domain-driven-design/05_saga_and_distributed_processes/saga_pattern.svg)

---
## A Process Manager

- A DDD term closely related to saga
- Listens for events; emits commands in response
- Has its own state and identity
- Is itself a domain concept; usually an aggregate

---
## Saga vs Process Manager

- Saga: emphasis on compensation and recovery
- Process manager: emphasis on coordinating a workflow
- Often the same code; different vocabulary
- Use whichever term the team is comfortable with

---
## Choreography vs Orchestration

- **Choreography**: each service reacts to events; no central coordinator
- **Orchestration**: a process manager directs the flow
- Same conceptual saga; different topology
- Each has trade-offs (covered in the saga course)

---
## Two Saga Styles

![choreography_vs_orchestration](svg/courses/architecting/domain-driven-design/05_saga_and_distributed_processes/choreography_vs_orchestration.svg)

---
## When to Choreograph

- Few steps, stable flow, autonomous teams
- Existing event infrastructure
- The flow is implicit in the event graph

---
## When to Orchestrate

- Many steps, evolving flow, complex compensation
- Need centralized visibility for ops
- The workflow is a domain concept the business names

---
## Compensating Transactions

- A new transaction that undoes the effect of a previous one
- Not a database rollback — a semantic undo
- Both events live in the audit log
- "Charged $100" + "Refunded $100" — both visible

---
## Designing Compensations

- Every step's compensation is defined alongside the step
- "Reserve inventory" → "Release inventory"
- "Capture payment" → "Refund payment"
- "Send physical mailing" → there is no compensation; pivot transaction

---
## Pivot Transactions

- A point past which compensation is impossible
- Once crossed, the saga must succeed (forward recovery only)
- Place the pivot at the last reversible step
- Often: physical or legal commitments

---
## Idempotency

- Saga steps may be retried; compensations may be retried
- Each must be idempotent — safe to call twice
- Use idempotency keys; deduplicate on the receiving side
- Without this, retries cause damage

---
## Saga as a DDD Aggregate

- The saga itself has identity and state
- It transitions through states as steps complete
- It emits events: `SagaStarted`, `StepCompleted`, `Compensated`
- Audit trail of the saga's life

---
## Saga State

- Saga id (correlation id across the flow)
- Current step
- Outcomes of completed steps
- Retry counts
- Persists across restarts and failures

---
## Where Saga State Lives

- Event-sourced: as a stream of saga events (recommended)
- Snapshot table: with the latest state
- Workflow engine (Temporal, Conductor): the engine handles persistence
- Pick what fits the team's operational model

---
## Cross-Service Sagas

- Each service performs its local steps
- Events flow between services
- The saga aggregates the events into a coherent workflow
- Each service is a participant; the saga is the conductor

---
## Halted Sagas

- A saga that can't complete and can't compensate cleanly
- Needs human intervention
- Operations should have an admin UI to inspect and resolve
- These are real production events; plan for them

---
## A Concrete Example: Order Saga

- Aggregates: Order, Inventory, Payment, Shipment
- Each lives in its own bounded context
- The saga coordinates them: place → reserve → charge → ship
- On failure: refund, release, cancel, notify

---
## The Saga in Code

- A new aggregate: `OrderSaga`
- Its events: `OrderSagaStarted`, `InventoryReserved`, `PaymentCaptured`, etc.
- Its state machine: each event drives a transition
- It emits commands to other services as it progresses

---
## Where to Go Deeper

- The dedicated **Saga Pattern** course covers:
    - Choreography and orchestration in depth
    - Compensation design, pivot transactions
    - Testing and operating sagas
    - Workflow engines

---
## Common Pitfalls

- Treating sagas as atomic transactions
- Forgetting compensations
- No timeouts, so sagas hang forever
- No correlation id, so debugging is impossible
- Hidden orchestration that pretends to be choreography

---
## Summary

- Sagas/process managers coordinate work across aggregates and services
- Compensation handles failure; pivot transactions limit it
- The saga itself is an aggregate with state and events
- Choreography and orchestration are both viable
- For depth, see the dedicated Saga Pattern course
