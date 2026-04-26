---
tags:
  - architecture:saga
  - architecture:event-driven
level: advanced
category: architecture
audience:
  - audiences:architects
  - audiences:developers

---
# Choreography-Based Sagas

---
## What This Chapter Covers

- How choreography works at the message level
- Designing the event flow
- Event ownership and contracts
- Reactive compensation through events
- Avoiding event spaghetti
- Tracking saga progress without a coordinator
- Debugging via correlation ids
- Worked example: order fulfillment

---
## How Choreography Works

- Each service publishes events when its work completes
- Each service subscribes to events relevant to its responsibilities
- The "next step" is whichever service reacts to the previous step's event
- No service knows about the saga as a whole
- The saga emerges from the event topology

---
## A Worked Example: Order Fulfillment

```diagram
Sales       → publishes  OrderPlaced
Inventory   → reacts; reserves; publishes InventoryReserved
Payment     → reacts; captures; publishes PaymentCaptured
Shipping    → reacts; schedules; publishes ShipmentScheduled
Email       → reacts; sends confirmation
```

- Each arrow is an event published to a broker
- Each service subscribes to exactly the events it cares about
- The whole flow happens with no central code

---
## Event Contracts

- Every event published is a public contract for downstream services
- The schema must be stable; changes need versioning (chapter 5)
- Producers own the schema, but consumers depend on it
- Use a schema registry to enforce compatibility

---
## Designing the Event Flow

- Start from the business steps; map each to an event
- Identify which service owns each step (each event)
- Draw the dependency graph: who reacts to what
- Verify it's a directed acyclic graph — cycles are usually bugs
- Validate that every step's outcome (success or failure) is observable

---
## Reactive Compensation

- A failure event is itself an event
- Inventory cannot reserve → publishes `InventoryReservationFailed`
- Sales reacts to the failure → publishes `OrderCancelled`
- Other already-completed services react to `OrderCancelled` and undo their work
- Compensation is just more events

---
## Compensation Flow Example

```diagram
Sales     → OrderPlaced
Inventory → InventoryReserved
Payment   → PaymentFailed (insufficient funds)
Sales     → reacts; OrderCancelled
Inventory → reacts to OrderCancelled; releases reservation
```

- Forward: events build state
- Backward: events undo state
- Same machinery; different intent

---
## Reactive Compensation Diagram

![reactive_compensation](svg/courses/architecting/saga-pattern/03_choreography_based_sagas/reactive_compensation.svg)

---
## Avoiding Cyclic Dependencies

- A reacts to B's event; B reacts to A's event → potential infinite loop
- Detect at design time by drawing the event graph
- Acyclic by default; cycles need explicit termination conditions
- Service ownership review catches these before deployment

---
## Avoiding Event Spaghetti

- "Every service subscribes to every event" → fragile, hard to reason about
- Each service should subscribe to a small, stable set of events
- Service responsibilities should align with bounded contexts
- Publish coarse-grained integration events, not fine-grained internal ones

---
## Tracking Saga Progress

- No central state — but operators still need to ask "where is order 42?"
- The fix: include a **correlation id** in every event of the saga
- Aggregate events by correlation id to see the full flow
- A reporting projection can build a per-saga timeline

---
## Correlation IDs in Practice

```python
# When Sales publishes OrderPlaced
event = OrderPlaced(
    order_id=order_id,
    correlation_id=order_id,  # in this case, same as order_id
    causation_id=cmd.command_id,
    ...
)
```

- The correlation id ties together every event in the saga
- The causation id ties an event to its trigger
- Together they provide a debug trail

---
## Causation vs Correlation

- **Correlation**: "what saga am I part of?" — same value across the whole flow
- **Causation**: "what triggered me?" — points to the immediately preceding event/command
- Both are useful; both are cheap to add; both are painful to retrofit

---
## Building a Saga View

- A read model that aggregates events by correlation id
- Subscribe to all integration events
- For each event, append to the saga timeline keyed by correlation id
- Status is derived from the latest event type

---
## Saga View Schema

```sql
CREATE TABLE saga_timeline (
    correlation_id  TEXT NOT NULL,
    sequence        INT  NOT NULL,
    event_type      TEXT NOT NULL,
    payload         JSONB,
    occurred_at     TIMESTAMPTZ,
    PRIMARY KEY (correlation_id, sequence)
);
```

- One row per event in the saga
- Aggregating by correlation_id reconstructs the flow
- Operators see the full story; alerts can fire on stuck sagas

---
## Debugging a Stuck Saga

- Query saga_timeline for the correlation id
- Find the last event observed
- Identify which service was supposed to react to it
- Check that service's logs and metrics
- The problem is usually a missing subscription, a broken handler, or a poison message

---
## Failure Modes Specific to Choreography

- **Missed event**: a subscriber wasn't running when the event was published
- **No catch-up**: subscribers must read the durable log, not just live events
- **Schema drift**: producer and consumer versions diverge
- **Partial deployment**: a new event type is published before all consumers can handle it

---
## Strategies Against These Failures

- Durable subscriptions on a log (Kafka, EventStoreDB) — no missed events
- Schema registry with compatibility checks
- Roll out consumers before producers when adding new events
- Roll out producers before consumers when removing events
- Versioned events: emit V1 and V2 in parallel during migration

---
## When Choreography Excels

- Steps are loosely connected — each service has a clean, narrow trigger
- Teams own their service end-to-end and prefer autonomy
- The flow rarely changes; new requirements rarely cross service boundaries
- The team has invested in good event infrastructure already

---
## When Choreography Falls Short

- Many steps with strict ordering — debugging "where are we?" becomes painful
- Frequent flow changes that touch multiple services — every change is a coordinated release
- Stuck sagas need active intervention — you wish there were a "saga is in step 3" record somewhere
- New team members can't find the workflow because there is no workflow code

---
## A Concrete Trade-Off

- Choreography reduces coupling but distributes the workflow
- The workflow is implicit in the event graph, not explicit in code
- This is fine when the graph is stable and small
- It hurts when the graph is volatile or large

---
## Hybrid: Choreography Inside, Orchestration Across

- Choreography for tightly-related steps within a bounded context
- Orchestration for top-level multi-context workflows
- Use the right tool at the right level
- Don't pick one religion for the whole system

---
## Worked Example: Order Fulfillment Saga

![choreography_order_saga](svg/courses/architecting/saga-pattern/03_choreography_based_sagas/choreography_order_saga.svg)

---
## Order Saga: Forward Path

- Sales: `OrderPlaced` (correlation = order id)
- Inventory: reserves; emits `InventoryReserved`
- Payment: charges; emits `PaymentCaptured`
- Shipping: schedules; emits `ShipmentScheduled`
- Email: sends confirmation

---
## Order Saga: Compensation Path

- Suppose Payment fails: `PaymentFailed`
- Sales: emits `OrderCancelled`
- Inventory: reacts to `OrderCancelled`; releases reservation; emits `InventoryReleased`
- Email: sends apology
- The saga ends in a coherent failed state

---
## Implementation Notes

- Use a durable broker (Kafka, NATS JetStream, EventStoreDB) — not in-memory
- Store the position of each subscription; resume after restart
- Make handlers idempotent — at-least-once delivery is the norm
- Test compensation paths in CI; they're easy to forget

---
## Anti-Patterns to Avoid

- Hidden orchestration: a "side project" that subscribes to all events and dispatches commands — that's just orchestration in disguise; if you need it, make it explicit
- Direct service-to-service calls inside a saga: defeats the loose coupling — use events
- Compensations that fail silently: every compensation needs monitoring like any other step

---
## Summary

- Choreography: each service reacts to events; no central coordinator
- The saga emerges from the event graph
- Compensation is just more events
- Correlation IDs and a saga-timeline projection make it debuggable
- Best for stable flows, autonomous teams, and existing event infrastructure
- Worst for volatile flows, complex compensation, and operations needing centralized visibility
