---
tags:
  - architecture:cqrs
  - architecture:event-sourcing
  - concepts:distributed-systems
level: advanced
category: architecture
audience:
  - audiences:architects
  - audiences:developers

---

# Eventual Consistency and Projections

---

## What This Chapter Covers

- What eventual consistency means in CQRS systems
- Three projection modes: inline, asynchronous, catch-up
- Rebuilding projections; managing projection state
- Out-of-order events and idempotency
- Tracking position; checkpointing
- Live vs replay; user experience patterns
- Monitoring projection lag

---

## What Eventual Consistency Means Here

- The write side commits an event
- The read side updates a moment later
- For a window of time, reads do not reflect the write
- The window is bounded; the system is correct given enough time
- "Eventual" is a guarantee, not a hope

---

## The Window Has a Name: Projection Lag

- Time between event append and read model update
- Measured in milliseconds for healthy systems, seconds when stressed
- Bounded under normal load; unbounded if the projection falls behind
- A first-class operational metric, with alerts

---

## Why Eventual Consistency Is Acceptable

- Most user actions tolerate a tiny window
- The alternative — synchronous updates — slows every write to the slowest read store
- The alternative breaks scaling: you can't add a new read model without changing the write path
- The window is closable for the queries that need it (read-your-own-write, ch 4)

---

## Three Projection Modes

![projection_modes](svg/courses/architecting/cqrs-and-event-sourcing/06_eventual_consistency_and_projections/projection_modes.svg)

---

## Inline Projections

- Update the read model in the same transaction as the event append
- Strong consistency; zero lag
- The read store must be reachable from the write transaction
- Couples the write path to read store availability
- Useful for the one read model that absolutely must agree

---

## Asynchronous Projections

- A subscriber tails the event log
- Updates the read model some time after the append
- The default for most systems
- Each projection is independent; failure in one doesn't affect others
- Lag is the price; flexibility is the payoff

---

## Catch-Up Projections

- A new projection starts at position 0 and processes the entire history
- A rebuilt projection drops its read store and starts over
- A "live" projection has caught up and is processing new events as they arrive
- The same code runs both modes — the difference is just where it starts

---

## Catch-Up vs Live Mode

- Catch-up: reading events from the past; the projection is behind the head of the log
- Live: tracking the head of the log as new events arrive
- Transition is invisible to the projection code — it's the same loop
- Some stores expose a "now caught up" signal so projections can switch from batch reads to push notifications

---

## Building a Projection

```python
class OrderSummaryProjection:
    def __init__(self, db, checkpoints):
        self.db = db
        self.checkpoints = checkpoints

    def run(self, source):
        position = self.checkpoints.get("order_summary") or 0
        for event in source.read_from(position):
            self.handle(event)
            self.checkpoints.set("order_summary", event.position)
```

- Resume from the saved position
- Handle each event
- Save the position after each successful handler

---

## Idempotent Handlers

- The same event may be delivered more than once (at-least-once semantics)
- Handlers must produce the same effect whether called once or twice
- For SQL: use `INSERT ... ON CONFLICT DO NOTHING` or upsert with the event id
- For Redis: use `SETNX` keyed by event id, or version-checked updates

---

## Idempotent Insert Example

```sql
INSERT INTO order_summary (order_id, customer_id, total, status)
VALUES ($1, $2, $3, $4)
ON CONFLICT (order_id) DO UPDATE
SET total = EXCLUDED.total,
    status = EXCLUDED.status,
    last_updated = now();
```

- Safe to run twice
- Last-write-wins on conflict
- Pair with event ordering to make "last" deterministic

---

## Out-of-Order Events

- Within a stream, events arrive in order
- Across streams (the global view), events can interleave non-deterministically
- Across partitions in Kafka, order is not guaranteed
- Projections that span streams must handle this

---

## Strategies for Out-of-Order

- **Idempotent + commutative**: order doesn't matter (counters, sets)
- **Tombstone**: track which events have been applied by id; drop duplicates
- **Buffer + sort**: hold events briefly, sort by causation, then apply
- **Stream-key projection**: only project from one stream per partition; order is preserved

---

## Out-of-Order Visualized

![out_of_order](svg/courses/architecting/cqrs-and-event-sourcing/06_eventual_consistency_and_projections/out_of_order.svg)

---

## Checkpointing

- The projection's "I am here" marker on the global stream
- Persisted at a known cadence (per event, per batch, per second)
- Restart resumes from the checkpoint
- Trade-off: checkpoint per event = safe but slow; per batch = fast but more replay on crash

---

## Checkpoint Storage

- A small table or key per projection: `(projection_name, position, updated_at)`
- The same store as the read model is convenient — atomic update with the projection write
- A separate store works too — accept potential double-application on crash recovery
- The projection must always be idempotent regardless

---

## Atomic Projection + Checkpoint

```sql
BEGIN;

INSERT INTO order_summary (...) VALUES (...) ON CONFLICT ... ;

UPDATE projection_checkpoints
SET position = $1
WHERE name = 'order_summary';

COMMIT;
```

- Read model write and checkpoint update in one transaction
- Crash before COMMIT: both rolled back; replay from old checkpoint
- Crash after COMMIT: checkpoint advanced; nothing to replay
- Idempotency keeps replay safe

---

## Projection Rebuilds

- Drop the read model
- Reset the checkpoint to 0
- Start the projection
- It catches up to live mode; the read model is recreated
- Duration: depends on event count and per-event handler cost

---

## When to Rebuild

- Schema change to the read model
- Bug in the projection that left the read model wrong
- New columns or new aggregates added to the projection
- Migration to a new storage technology
- Treat rebuilds as routine, not exotic

---

## Rebuilding Lifecycle

![rebuild_lifecycle](svg/courses/architecting/cqrs-and-event-sourcing/06_eventual_consistency_and_projections/rebuild_lifecycle.svg)

---

## Blue-Green Projections

- Don't drop the live read model — build a new one alongside
- Project events into both old and new versions
- Switch reads to the new version when it has caught up
- Drop the old version after a stability window
- Standard zero-downtime migration pattern

---

## Blue-Green Diagram

![blue_green_projection](svg/courses/architecting/cqrs-and-event-sourcing/06_eventual_consistency_and_projections/blue_green_projection.svg)

---

## Failure Modes

- **Projection lag**: subscriber falls behind; reads grow stale
- **Bad event**: an event format the handler doesn't understand crashes the loop
- **Schema mismatch**: the read store schema doesn't match what the handler expects
- **Subscription lost**: connection drops; resume from checkpoint
- **Handler bug**: event was applied incorrectly; rebuild required to fix

---

## Poison Events

- An event the handler can't process — bad data, missing field, schema break
- The handler crashes; the projection halts
- Three responses:
    - **Skip**: log and move on (only safe with idempotent + non-critical events)
    - **Park**: move to a poison queue, alert, continue with the next
    - **Stop**: halt the projection until a human intervenes
- Choose by criticality

---

## Communicating Eventual Consistency to Users

- The UI is the place where users encounter the lag
- Three patterns (we covered these in ch 4):
    - Optimistic update with reconciliation
    - Polling for confirmation
    - Server-pushed updates
- Honesty is cheap; pretending to be strongly consistent is expensive

---

## Read-Your-Own-Write Pattern (Recap)

```python
def confirm_order(order_id, expected_version):
    # poll the read model until projection catches up
    deadline = now() + 2.seconds
    while now() < deadline:
        row = read_model.fetch(order_id)
        if row and row.version >= expected_version:
            return render_confirmation(row)
        sleep(0.05)
    return render_pending_page(order_id)
```

- Bounded wait
- Tight, not infinite
- Fall back to a pending page if the projection is stuck

---

## Monitoring Projection Lag

- **Position lag**: latest_global_position − projection_position
- **Time lag**: now − occurred_at_of_last_processed_event
- Alert when either exceeds a threshold for longer than a window
- Dashboard per projection; track lag across deploys
- Trends matter: a slowly growing lag is a leak

---

## What to Alert On

- Lag exceeds a threshold (e.g., 30 seconds) for over 5 minutes
- Projection has stopped (no advance for over 1 minute)
- Error rate per handler exceeds a baseline
- Poison event queue depth grows
- Each alert is paired with a runbook

---

## Common Mistakes

- **Forgetting idempotency**: at-least-once delivery breaks the read model on retry
- **Checkpointing before the handler succeeds**: lost work on crash
- **No monitoring**: the projection silently falls behind for hours
- **No rebuild tooling**: schema changes require manual surgery
- **Strong consistency expectations**: building a UI that assumes immediate visibility

---

## A Reasonable Starting Configuration

- Asynchronous projections by default
- Each projection: subscriber + idempotent handlers + checkpoint
- Atomic transaction over read model write + checkpoint
- Position lag and time lag dashboards from day one
- Rebuild tooling exercised regularly (don't wait for the emergency)

---

## Summary

- Eventual consistency is a contract, not a flaw — bounded, observable, livable
- Three projection modes: inline (rare), asynchronous (default), catch-up (rebuilds)
- Idempotent handlers + atomic checkpoint = safe at-least-once
- Rebuilds are routine; blue-green is the zero-downtime variant
- The user experience must reflect the contract; the dashboard must monitor it
