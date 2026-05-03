---
tags:
  - patterns:event-sourcing
  - patterns:cqrs
level: advanced
category: architecture
audience:
  - audiences:developers
  - audiences:architects

---
# Event Sourcing and CQRS

---
## What This Chapter Covers

- Event sourcing: state as a sequence of events
- Event store design and rebuilding state
- Snapshots and performance
- CQRS: separating reads from writes
- Eventual consistency in user-facing systems

---
## What Is Event Sourcing?

- Don't store current state; store the events that produced it
- Current state derived by replaying events
- Append-only — events never modified
- Full audit trail by construction
- Different mental model than traditional CRUD

---
## A Concrete Example

- Bank account: balance is current state
- Traditional: store balance directly, update on each transaction
- Event sourced: store every deposit and withdrawal
- Balance = sum of events in order
- The events are the source of truth

---
## Event Sourcing Visualized

![event_sourcing](svg/courses/architecting/event-driven-architecture/03_event_sourcing_and_cqrs/event_sourcing.svg)

---
## Snapshotting

![snapshotting](svg/courses/architecting/event-driven-architecture/03_event_sourcing_and_cqrs/snapshotting.svg)

---
## Projection Lifecycle

![projection_lifecycle](svg/courses/architecting/event-driven-architecture/03_event_sourcing_and_cqrs/projection_lifecycle.svg)

---
## Why Event Sourcing?

- Audit trail is automatic and complete
- Time travel: query state as of any moment
- New projections from existing events without database migration
- Aligns with business: events match real-world facts
- Enables temporal queries impossible in CRUD

---
## Why Not Event Sourcing?

- Complex to implement correctly
- Querying current state requires replay or read models
- Schema evolution applies to events too — and they're immutable
- Tooling and team knowledge are harder to find
- Many systems don't need it

---
## Event Store Basics

- An append-only log per aggregate
- Operations: append events, read events from offset
- Optimistic concurrency: append fails if expected version doesn't match
- Built specially or on Kafka, EventStoreDB, Postgres, etc
- The schema of the log is part of your domain

---
## Aggregate as Event Stream

- An aggregate (DDD concept) becomes a stream of events
- Stream ID = aggregate ID
- Loading: read all events, fold into in-memory state
- Saving: append new events with version check
- One stream per aggregate keeps concurrency local

---
## Snapshots for Performance

- Replaying thousands of events on every load is slow
- Snapshot: cached state at a specific event version
- Load: latest snapshot + events since
- Snapshot frequency: every N events or M ms
- Snapshots are derived data — can be rebuilt

---
## Rebuilding Projections

- A read model is a derived view of events
- Project events into a database optimized for queries
- New projection: replay all events through new logic
- Existing projection: keeps catching up as events arrive
- Projection logic is just a function from events to state

---
## CQRS: The Big Idea

- Command Query Responsibility Segregation
- Reads use one model; writes use another
- The two models live in different stores
- Connected by events: writes emit events, reads project them
- Each model is optimized for its purpose

---
## CQRS Visualized

![cqrs_flow](svg/courses/architecting/event-driven-architecture/03_event_sourcing_and_cqrs/cqrs_flow.svg)

---
## Why CQRS?

- Read and write workloads have different shapes
- Reads scale easily; writes don't
- Read models can be denormalized for speed
- Multiple read models from one write model
- The price: eventual consistency between sides

---
## Why Not CQRS?

- Two models double the complexity
- Eventual consistency confuses users used to "read your write"
- Requires discipline in keeping projections in sync
- Many systems don't need this scale
- Don't adopt CQRS for fashion

---
## CQRS Without Event Sourcing

- The two patterns are independent
- Can do CQRS with traditional persistence: emit events at the boundary
- Can do event sourcing without CQRS: same store for read and write
- Most teams that do both find synergy
- They are *not* the same pattern

---
## Building Read Models

- Subscribe to the event stream
- Apply each event to update read tables
- Idempotent — events may arrive twice
- Different read models for different consumers
- A read model can be wiped and rebuilt safely

---
## Eventual Consistency: User Experience

- "I made a change but it's not visible yet"
- The classic CQRS UX challenge
- Solutions: optimistic UI, polling, websockets, "read your write" via cache
- Communicate the lag honestly to users
- Don't pretend it's strongly consistent — that's worse

---
## Read-Your-Writes Patterns

- Optimistic UI: show the write immediately, reconcile on response
- Cache the write locally for the user's session
- Subscribe to the event stream and update on confirmation
- Server hint: "your update is in flight"
- Pick what fits the user's expectation

---
## Event Sourcing Pitfalls

- Schema evolution: events are immutable, so old events keep their old shape
- Sensitive data in events: GDPR right-to-be-forgotten conflicts
- Replays without isolation: integration events fire again on rebuild
- Performance: snapshot strategy is operational, not architectural
- Concurrency: optimistic locking required

---
## Sensitive Data in Event Stores

- Right to be forgotten conflicts with immutable logs
- Strategies: crypto-shredding (delete the key; encrypted data stays)
- Strategies: separate PII into a side store you can delete
- Strategies: not storing sensitive data in events at all
- Plan this from day one — retrofit is painful

---
## Replays and Integration

- Rebuilding a read model triggers events again
- Don't notify external systems during a replay
- Mark replay events distinctly; consumers ignore for side effects
- This separation is critical and often missed
- Test replay paths separately from real-time paths

---
## When CQRS Without ES Helps

- Read-heavy systems with complex queries
- Multiple read models for different UIs (mobile, web, reporting)
- Search indices kept eventually consistent
- Reporting databases derived from operational data
- All without committing to event sourcing

---
## When ES Without CQRS Helps

- Audit-heavy domains: finance, healthcare, legal
- Systems requiring time-travel queries
- Domains where the business cares about history
- Replay is needed for compliance reasons
- Single read path is enough; just need the audit trail

---
## Common Anti-Patterns

- "Event-sourcing CRUD" — events that are just SET FIELD events
- Reading from the event store directly for queries
- Not snapshotting and watching load times explode
- Mixing temporal/business events with technical/system events in one stream
- Trying to retrofit ES onto a working CRUD app without redesign

---
## Summary

- Event sourcing: state derived from events, not stored
- Snapshots and projections handle performance and queries
- CQRS: separate models for read and write, connected by events
- The two patterns work well together but are independent
- Powerful tools — adopt deliberately, not by fashion
