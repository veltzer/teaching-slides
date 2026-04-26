---
tags:
  - architecture:event-sourcing
  - concepts:design-patterns
level: advanced
category: architecture
audience:
  - audiences:architects
  - audiences:developers

---
# Event Sourcing Fundamentals

---
## What Is Event Sourcing?

- Persist application state as an ordered sequence of immutable events
- Each event records a fact: something that happened in the past
- Current state is a function of the event history
- The events are the source of truth — not a row in a table

---
## State-Based Persistence (The Default)

- Save the current value of each field
- Updates overwrite the previous value
- The history of how you arrived at the current state is lost
- Auditability requires a separate log that the application has to remember to write

---
## Event-Sourced Persistence

- Save what happened, not the resulting field values
- Each change appends a new event
- Reconstruct any past state by replaying events up to a point in time
- The log is the truth; current state is a derived view

---
## State vs Events Side by Side

![state_vs_events](svg/courses/architecting/cqrs-and-event-sourcing/02_event_sourcing_fundamentals/state_vs_events.svg)

---
## A Concrete Example

- Order with `total` field
- State-based: row says `total = 95`
- Event-sourced: stream says
    - `OrderCreated(total=0)`
    - `LineItemAdded(price=50)`
    - `LineItemAdded(price=50)`
    - `DiscountApplied(amount=5)`
- The state-based row tells you *what*; the event stream tells you *why*

---
## Domain Events: Definition

- A statement of fact about something that occurred in the domain
- Named in past tense: `OrderPlaced`, not `PlaceOrder`
- Owned by an aggregate; emitted when an invariant has been satisfied
- Carries the data needed to understand the change, not the resulting state

---
## Event Naming Conventions

- Past tense, business vocabulary
    - `PaymentCaptured`, not `CapturePayment` or `PaymentUpdated`
- Specific over generic
    - `ItemReturned` and `ItemRefunded` are two events, not one `OrderChanged`
- Reflect the domain expert's language, not implementation details
    - `CustomerSubscribed`, not `RowInserted`

---
## Event Structure

```python
@dataclass(frozen=True)
class OrderPlaced:
    event_id: UUID
    aggregate_id: OrderId
    aggregate_version: int
    occurred_at: datetime
    customer_id: CustomerId
    items: list[LineItem]
```

- Identity (`event_id`) for deduplication
- Aggregate id and version for ordering and concurrency control
- `occurred_at` is wall-clock time of the business action
- Payload carries the domain facts

---
## Events Are Immutable

- Once written, an event is never modified or deleted
- Mistakes are corrected by appending a new event (`OrderCorrected`)
- This is what makes audit, replay, and time-travel queries possible
- Treat the event store like a journal, not a notebook

---
## Replaying Events

```python
def replay(events: list[Event]) -> Order:
    order = Order.empty()
    for event in events:
        order.apply(event)
    return order
```

- Start from a zero state
- Apply each event in order
- The result is the current state of the aggregate
- The same code runs whether you replay 5 events or 50,000

---
## Replay Visualized

![replay_flow](svg/courses/architecting/cqrs-and-event-sourcing/02_event_sourcing_fundamentals/replay_flow.svg)

---
## The `apply` Method Pattern

```python
class Order:
    def apply(self, event: Event) -> None:
        match event:
            case OrderPlaced(items=items):
                self.items = list(items)
                self.status = "placed"
            case ItemShipped(item_id):
                self._mark_shipped(item_id)
            case OrderCancelled(reason):
                self.status = "cancelled"
                self.cancel_reason = reason
```

- One handler per event type
- Pure state mutation; no side effects
- Idempotent: applying the same events to a fresh aggregate yields the same state

---
## Two Phases: Decision and Application

- **Decision phase**: a command produces zero or more events; invariants are checked here
- **Application phase**: events update aggregate state via `apply`
- Replay only runs the application phase
- This separation makes `apply` safe to run anywhere — including projection code

---
## Decision and Application

![decision_and_application](svg/courses/architecting/cqrs-and-event-sourcing/02_event_sourcing_fundamentals/decision_and_application.svg)

---
## Schema Evolution: The Hard Problem

- Events written today may be replayed in five years
- The code that reads them will have evolved
- Fields will be added, renamed, removed, restructured
- The event log is forever; the code is not

---
## Strategies for Schema Evolution

- **Weak schema**: tolerant readers ignore unknown fields, default missing ones
- **Versioned events**: `OrderPlacedV1`, `OrderPlacedV2`; readers handle both
- **Upcasters**: a function that lifts an old event to the new shape on read
- **Copy-and-transform migration**: rewrite the stream into a new one (last resort)

---
## Versioning in Practice

```python
class OrderPlacedV1(Event):
    items: list[LineItem]

class OrderPlacedV2(Event):
    items: list[LineItem]
    promo_code: str | None  # added later

def upcast(raw: dict) -> Event:
    if raw["type"] == "OrderPlacedV1":
        return OrderPlacedV2(items=raw["items"], promo_code=None)
    return parse(raw)
```

- New events use the new shape
- Old events are upcast on read
- The aggregate only sees the latest shape

---
## Benefits: Audit Log for Free

- Every state change is recorded with timestamp and identity
- Compliance and forensic requirements are met by construction
- "Who changed this and when?" has a definite answer
- Better than a manual audit table because it cannot be skipped

---
## Benefits: Temporal Queries

- "What did this order look like on March 5th?"
- Replay events up to that timestamp on a fresh aggregate
- Reports about historical state become possible without snapshots
- Useful for legal disputes, analytics, and debugging production incidents

---
## Benefits: Debugging Production Bugs

- "How did this aggregate get into this impossible state?"
- Replay the events; watch the state machine evolve
- The bug becomes a question about the events, not the database
- Bugs become reproducible by replaying the same stream in a test

---
## Benefits: New Read Models For Free

- A new dashboard? Project the same events into a new shape
- No backfill from production database needed
- Run the projection from event 0 and you have a complete history
- Multiple read models can be built and rebuilt independently

---
## Benefits Recap

![benefits_of_event_sourcing](svg/courses/architecting/cqrs-and-event-sourcing/02_event_sourcing_fundamentals/benefits_of_event_sourcing.svg)

---
## Common Misconceptions

- "Event Sourcing means using Kafka" — Kafka is one option; not a requirement
- "Event Sourcing means CQRS" — they pair well but are independent
- "Event Sourcing replaces the database" — you still need read models in databases
- "Replay is slow" — bounded by the number of events; snapshots address long streams

---
## Common Pitfalls

- **CRUDDy events**: `OrderUpdated(field="status", value="shipped")` — avoid
- **Missing the why**: events should say what happened, including business reason
- **Too coarse-grained**: one giant event per command loses replay value
- **Too fine-grained**: per-field events explode the stream and bury intent
- **Mutating events**: this defeats the entire pattern

---
## CRUD Events Are an Anti-Pattern

- `OrderUpdated(field="address", value="...")` is not a domain event
- It records a database operation, not a business fact
- Replay tells you fields changed, not what business action occurred
- Prefer `ShippingAddressChanged(reason="customer-request", new=...)`

---
## Comparison: Event Sourcing vs Change Data Capture

- **CDC**: a tool reads the database WAL and emits change records
- Records are about rows, not domain events; the meaning is fragile
- CDC is great for replication and integration; weak for audit semantics
- Event Sourcing emits events at the domain level — the events have business meaning

---
## Comparison: Event Sourcing vs the Outbox Pattern

- **Outbox**: write the new state and an integration event in the same transaction
- A separate process publishes the integration events to a broker
- The state-of-truth is still the row; the event is a side effect for integration
- Event Sourcing inverts this: the events are the truth, the row is derived

---
## ES vs CDC vs Outbox

![es_vs_cdc_vs_outbox](svg/courses/architecting/cqrs-and-event-sourcing/02_event_sourcing_fundamentals/es_vs_cdc_vs_outbox.svg)

---
## Storage Requirements

- Append-only writes
- Strict ordering within a stream (per-aggregate)
- Optimistic concurrency check on append (expected version)
- Efficient read of all events for a stream
- Efficient subscription to all events globally

---
## Common Storage Choices

- **EventStoreDB**: purpose-built; first-class streams, projections, subscriptions
- **PostgreSQL**: an `events` table with `(stream_id, version)` unique constraint works well
- **Kafka**: a topic per aggregate type; partition by aggregate id
- **DynamoDB**: a partition key per stream; sort key is the version
- The pattern matters more than the technology

---
## When Event Sourcing Pays Off

- Audit and compliance are first-class requirements
- The domain is naturally event-shaped (orders, payments, workflows)
- Multiple consumers need different views of the same activity
- Time-travel and historical analysis are valuable
- The team has the appetite for the operational overhead

---
## When Event Sourcing Does Not Pay Off

- Simple CRUD with no audit requirements
- The team is small and unfamiliar with the pattern
- The domain is genuinely state-shaped (a counter, a config flag)
- Schema is volatile and the cost of maintaining upcasters dominates
- A traditional database with audit triggers would be enough

---
## Event Sourcing Without CQRS

- The aggregate is event-sourced, but reads still go through the same aggregate
- Useful in small systems where the read shape matches the aggregate shape
- Less common in practice — once you have an event log, projections are cheap
- A reasonable starting point that grows into CQRS naturally

---
## CQRS Without Event Sourcing

- The two patterns are independent (we covered this in chapter 1)
- Reminder: CQRS splits read and write models; ES is about persistence format
- Many production systems use one without the other

---
## A Mental Model for Events

- Events are like ledger entries in accounting
- You never erase an entry; you post a correcting entry
- The balance is computed from the entries, not stored separately
- Audit and reproducibility come from the ledger, not from a snapshot

---
## A Mental Model: Git for Aggregates

- Each event is a commit
- The current state is `HEAD`
- You can `git log` (audit), `git checkout <past>` (temporal query), `git bisect` (debug)
- You cannot rewrite history without breaking everyone downstream
- The analogy is imperfect but useful

---
## Summary

- Event Sourcing persists state as an ordered, immutable log of events
- Domain events are facts in the past tense, owned by aggregates
- Current state is a function of events: `replay(events) -> state`
- Schema evolution is the operational tax; design for it from day one
- Pays off when audit, history, or projection flexibility matter
- Independent of CQRS, but the two patterns reinforce each other
