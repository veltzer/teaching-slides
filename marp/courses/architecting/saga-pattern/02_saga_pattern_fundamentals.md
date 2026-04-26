---
tags:
  - architecture:saga
level: advanced
category: architecture
audience:
  - audiences:architects
  - audiences:developers

---
# Saga Pattern Fundamentals

---
## What This Chapter Covers

- The structure of a saga: steps, transactions, compensations
- Forward recovery vs backward recovery
- Saga state: where to keep it
- Idempotency requirements
- Choreography vs orchestration: the high-level choice

---
## A Saga, Defined

- A sequence of local transactions, each in a different service
- Every step has a paired compensating action
- If any step fails, completed steps are compensated in reverse order
- Coordination is explicit — either by events (choreography) or by an orchestrator
- The saga is itself a domain concept; name it like one

---
## Saga Anatomy

- **Steps**: discrete units of work, each owned by one service
- **Local transactions**: each step's work is committed atomically in its own service
- **Compensations**: per-step undo, executed if a later step fails
- **Saga state**: where we are in the sequence, retries, outcomes
- **Trigger**: the event or command that starts the saga

---
## Saga Anatomy Visualized

![saga_anatomy](svg/courses/architecting/saga-pattern/02_saga_pattern_fundamentals/saga_anatomy.svg)

---
## A Worked Example: Order Saga

- Step 1: Reserve inventory (compensation: release inventory)
- Step 2: Capture payment (compensation: refund payment)
- Step 3: Schedule shipment (compensation: cancel shipment)
- Step 4: Notify customer (compensation: send apology — usually no-op)
- Failure at step 3 triggers compensations for steps 2 and 1, in reverse

---
## Forward Recovery

- On failure, push forward to a known-good state instead of unwinding
- Retry the failing step until it succeeds (or human intervention)
- Useful when the next step is "almost done" and undoing earlier work is expensive
- Requires the failing step to be intermittently failing, not permanently broken

---
## Backward Recovery

- On failure, undo earlier steps via compensations
- The default model for sagas
- Cleaner end state — the system returns to "as if nothing happened"
- Requires every step to have a meaningful compensation

---
## Forward vs Backward

- Forward: "we're committed to finishing"
- Backward: "we can call it off cleanly"
- A real saga may use forward for some steps and backward for others
- The right choice depends on the business — talk to domain experts

---
## Semantic Rollback vs ACID Rollback

- ACID rollback: the database forgets it ever happened
- Semantic rollback: a new transaction undoes the effect of an earlier one
- The customer was charged → the customer is refunded
- The new transaction is visible in the audit log
- This is fundamentally different from "the charge never happened"

---
## Saga State

- Where are we in the sequence?
- Which steps have completed? Which compensations have run?
- How many retries have we attempted?
- This state must survive process restarts and crashes
- Persisting it is non-negotiable

---
## Where to Store Saga State

- **In the orchestrator's database** (orchestration-based sagas)
- **Distributed across participants' state machines** (choreography)
- **In a workflow engine** (Temporal, Conductor, Camunda)
- The choice affects observability, recovery, and team boundaries

---
## Idempotency: Required, Not Optional

- Every saga step must be idempotent — safe to call twice with no extra effect
- Networks lose responses; the saga retries; the step receives the same call again
- Without idempotency: double charges, double shipments, duplicate emails
- Use natural keys, dedup tables, or version numbers

---
## Idempotency in Practice

```python
def reserve_inventory(reservation_id, items):
    if dedup_table.contains(reservation_id):
        return existing_result(reservation_id)
    result = perform_reservation(items)
    dedup_table.record(reservation_id, result)
    return result
```

- The reservation_id is provided by the caller and is stable across retries
- The dedup table makes the operation idempotent
- Retries return the original result, not a new one

---
## Saga Triggers

- A user action (REST POST)
- An incoming integration event ("OrderPlaced" arrives from another context)
- A scheduled job ("monthly billing run")
- The trigger is not part of the saga; it kicks the saga off

---
## Two Implementation Styles

- **Choreography**: each service knows the next step; participants react to events
- **Orchestration**: a central orchestrator tells each participant what to do
- Same conceptual saga; different runtime topology
- The choice affects coupling, observability, and team coordination

---
## Choreography vs Orchestration

![choreography_vs_orchestration_overview](svg/courses/architecting/saga-pattern/02_saga_pattern_fundamentals/choreography_vs_orchestration_overview.svg)

---
## Choreography in One Slide

- Step A emits an event
- Step B is a subscriber; it does its work and emits its own event
- Step C subscribes to B's event, and so on
- No central authority; the saga emerges from the event graph

---
## Orchestration in One Slide

- A central orchestrator owns the saga
- It calls Step A; on completion, calls Step B; on completion, calls Step C
- On failure, it walks back through compensations
- The orchestrator is itself an aggregate with state

---
## Choosing Between Them

- **Few steps, few teams** → choreography is simple
- **Many steps, complex flow** → orchestration is clearer
- **Existing event infrastructure** → choreography fits
- **Need visibility for ops** → orchestration is easier to debug
- **Strong contracts between teams** → orchestration is more explicit

---
## When Choreography Wins

- The flow is short and changes infrequently
- Services already exchange events
- Teams own their service end-to-end and prefer autonomy
- The cost of a central orchestrator's deployment is high

---
## When Orchestration Wins

- The flow is long and likely to evolve
- Compensation logic is non-trivial
- Stuck sagas need a central place to inspect
- The business explicitly cares about the workflow as a thing

---
## Common Mistakes Already Worth Naming

- **Treating the saga as atomic**: it isn't; it is eventually consistent
- **Forgetting compensations**: every step needs one or the saga can't fail safely
- **Making compensations require things that aren't there**: e.g., needing the original payment id but storing only the amount
- **Skipping idempotency**: retries become visible bugs
- **Hiding the saga**: not naming it as a thing in the codebase

---
## What We Cover in the Rest of the Course

- Chapters 3-4: each style in depth
- Chapter 5: compensation design — semantic rollback, pivot transactions, non-compensatable steps
- Chapter 6: testing, debugging, monitoring, and operating sagas

---
## Summary

- A saga = sequence of local transactions + compensations
- Backward recovery (compensations) is the default; forward recovery exists for stubborn steps
- Saga state must persist; idempotency is mandatory
- Two implementation styles: choreography (event-reactive) and orchestration (centrally directed)
- Choosing between them is a question of scale, ownership, and visibility
