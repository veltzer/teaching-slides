---
tags:
  - concepts:domain-driven-design
  - architecture:cqrs
  - architecture:event-sourcing
level: advanced
category: architecture
audience:
  - audiences:architects
  - audiences:developers

---
# CQRS and Event Sourcing

---
## CQRS

![cqrs](svg/courses/architecting/domain-driven-design/04_cqrs_and_event_sourcing/cqrs.svg)

---
## Why DDD Pairs Well With CQRS and ES

- DDD aggregates emit domain events naturally
- Events as the persistence format = Event Sourcing
- Separate write and read models = CQRS
- Together: the write side preserves rich domain logic; the read side serves queries efficiently

---
## CQRS in One Slide

- Command Query Responsibility Segregation
- Commands change state via the write model (aggregates)
- Queries read state from the read model (denormalized views)
- The two models share a domain but not a structure

---
## Event Sourcing in One Slide

- Aggregate state is persisted as a sequence of immutable events
- Current state is `replay(events) -> state`
- Audit, time travel, replay all come for free
- Events are the source of truth

---
## CQRS Without ES

- Possible: write model in a normal database, read models updated separately
- Useful when you want the read/write split but not the operational cost of ES
- Many production systems use this combination

---
## ES Without CQRS

- Possible: aggregates are event-sourced; reads also go through aggregates
- Less common; once you have events, projections are cheap
- Usually ES leads naturally to CQRS

---
## Both Together

- The natural pairing
- Aggregates persist as events; events also feed read models
- One stream, multiple consumers
- Most modern DDD implementations use this combination

---
## Aggregate Implementation With ES

```python
class Order:
    def __init__(self):
        self.events: list[Event] = []
        self.status = "draft"

    def place(self, items: list[LineItem]) -> None:
        if self.status != "draft":
            raise OrderAlreadyPlaced()
        self._apply(OrderPlaced(items=items))

    def _apply(self, event: Event) -> None:
        match event:
            case OrderPlaced(items):
                self.status = "placed"
        self.events.append(event)
```

---
## Replay Pattern

- Load events from the store
- Apply them to a fresh aggregate
- Now the aggregate is in its current state
- Same code as forward execution; no special "load" logic

---
## Read Models From Events

- A subscriber tails the event log
- Each event updates one or more read models
- Read models are shaped per consumer (mobile, search, reports)
- The same event can feed many read models

---
## Read Model Examples

- `order_summary`: id, total, status, last_updated — for the order screen
- `customer_orders`: per-customer list of orders — for the history page
- `pending_shipments`: queue of orders ready to ship — for warehouse staff
- All built from the same `Order` events

---
## Eventual Consistency

- The read model lags the write model by milliseconds-seconds
- The write side is strongly consistent within an aggregate
- The read side is eventually consistent
- Communicate this to users in the UX

---
## DDD Aggregates as ES Aggregates

- Same concept, different persistence strategy
- The aggregate's invariants enforced in code (decide phase)
- The events emitted (apply phase)
- Replay = many apply calls; no decide calls

---
## Domain Events as the Source of Truth

- The events are auditable, replayable, durable
- The current state is derived
- Schema evolution is harder (event format changes need handling)
- Trade complexity for power

---
## Snapshot Optimization

- Long event streams → slow loads
- A snapshot is a saved aggregate state at a known version
- Load from snapshot + replay events after that version
- See the dedicated CQRS / Event Sourcing course

---
## When to Use Together

- Audit and history are first-class requirements
- The domain is naturally event-shaped (orders, payments, workflows)
- Multiple consumers need different views of the same activity
- The team has the appetite for the operational cost

---
## When Not to Use Together

- Simple CRUD without audit needs
- Small team without ops capacity for event stores
- Domain that's truly state-shaped, not event-shaped
- "Because Netflix uses it" — not a reason

---
## Where to Go Deeper

- The dedicated **CQRS and Event Sourcing** course covers:
    - Implementation details for commands and queries
    - Event store choices (Postgres, EventStoreDB, Kafka)
    - Projections, snapshotting
    - Testing and operating event-sourced systems

---
## Common Pitfalls

- Treating aggregate state as the source of truth instead of events
- Skipping schema versioning for events
- Building read models without checkpointing — replay storms break things
- Over-using events: not every change needs an event

---
## Summary

- CQRS and ES are independent; together they're powerful
- DDD aggregates fit naturally as event-sourced
- Read models projected from events, shaped per consumer
- Eventual consistency is the price; audit and replay are the payoff
- For depth, see the dedicated CQRS/ES course
