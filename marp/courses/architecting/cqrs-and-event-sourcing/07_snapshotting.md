---
tags:
  - architecture:event-sourcing
  - concepts:performance
level: advanced
category: architecture
audience:
  - audiences:architects
  - audiences:developers

---

# Snapshotting

---

## What This Chapter Covers

- Why long event streams are a performance problem
- What a snapshot is and where it fits
- When to snapshot
- Snapshot storage choices
- Loading aggregates with snapshots
- Snapshot versioning and migration
- Trade-offs

---

## The Problem: Long Streams

- An aggregate with 50,000 events takes 50,000 apply calls to load
- Even a few milliseconds per apply adds up
- Replay time grows linearly with the event count
- Hot aggregates (heavy use) suffer the most
- This is the cost of having a perfect history

---

## What Is a Snapshot?

- A saved aggregate state at a known stream version
- Not an event; not the source of truth
- A cache for the aggregate's "current state at version N"
- Loaded as a starting point so replay can skip events ≤ N

---

## Snapshot Visualized

![snapshot_overview](svg/courses/architecting/cqrs-and-event-sourcing/07_snapshotting/snapshot_overview.svg)

---

## Loading With a Snapshot

```python
def load_order(order_id):
    snapshot = snapshots.latest(f"order-{order_id}")
    if snapshot:
        order = Order.from_snapshot(snapshot)
        events = event_store.read_after(f"order-{order_id}",
                                        snapshot.version)
    else:
        order = Order.empty(order_id)
        events = event_store.read_stream(f"order-{order_id}")
    for event in events:
        order.apply(event)
    return order
```

- Latest snapshot is the starting state
- Replay only the events written after that version
- Falls back to full replay if no snapshot exists

---

## When to Take a Snapshot

- Periodic by event count: every N events (e.g., every 100)
- Periodic by elapsed time since the last snapshot
- After a "milestone" event: a state transition that fundamentally changes the aggregate
- On read pressure: if loading is slow, snapshot then keep reading
- Most teams use a simple "every N events" rule

---

## Where to Take a Snapshot

- Asynchronously, after the write commits
    - The append succeeded; the snapshot can be built off the same events
- A subscriber dedicated to snapshot creation, like a projection
- Or as part of a periodic background job
- Never in the critical write path — the append is already fast

---

## Snapshot Storage

- A separate table or store keyed by `(stream_id, version)`
- Body is the serialized aggregate state
- Can use the same database as the events, or a different one
- A small store; fast lookup; usually just the latest is needed

---

## A Postgres Snapshot Table

```sql
CREATE TABLE snapshots (
    stream_id   TEXT     NOT NULL,
    version     INT      NOT NULL,
    state       JSONB    NOT NULL,
    schema_ver  INT      NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (stream_id, version)
);
```

- Latest snapshot per stream is `MAX(version)`
- Old snapshots can be pruned, but keep at least one
- `schema_ver` is for snapshot format migrations (covered below)

---

## Snapshot Frequency Trade-Off

- More frequent snapshots → faster loads, more storage and CPU
- Less frequent snapshots → cheaper, slower loads
- Not a permanent decision; tunable per aggregate type
- Start simple, measure, adjust

---

## A Reasonable Default

- Take a snapshot every 100 events
- Keep the latest 3 snapshots; prune older ones (rollback safety)
- Build snapshots in a background subscriber, not inline
- Monitor the load latency distribution; tune if it drifts

---

## Snapshot Versioning

- The aggregate's class evolves; the snapshot format must too
- A snapshot from yesterday's code may be unreadable by today's code
- The `schema_ver` column captures which format the body uses
- Loading code knows how to handle each version it understands

---

## Strategy: Discard on Mismatch

- Loading code sees an older `schema_ver` than it can handle
- Discard the snapshot; fall back to full event replay
- The next snapshot taken will use the new format
- Simple; correct; pays the cost of one slow load per aggregate

---

## Strategy: Upcast Old Snapshots

```python
def from_snapshot(raw):
    if raw["schema_ver"] == 1:
        raw = upcast_v1_to_v2(raw)
    if raw["schema_ver"] == 2:
        raw = upcast_v2_to_v3(raw)
    return Order.from_v3(raw)
```

- Like event upcasters (chapter 2)
- Old snapshots remain useful through schema changes
- Trade complexity for not paying the discard cost

---

## Loading With Snapshot Versioning

![snapshot_load_flow](svg/courses/architecting/cqrs-and-event-sourcing/07_snapshotting/snapshot_load_flow.svg)

---

## Snapshots Are Optional

- The system runs correctly without snapshots — they are an optimization
- Adding them later is non-breaking (just speed up loading)
- Rebuilding snapshots from scratch is also non-breaking
- They never affect the source of truth, only the latency of accessing it

---

## What Snapshots Don't Solve

- A bad event in the stream still has to be dealt with
- A schema migration in events still requires upcasters
- A wrong projection still needs to be rebuilt
- Snapshotting only addresses one specific cost: aggregate load latency

---

## When You Don't Need Snapshots

- Aggregates with naturally short streams (< 50 events typical)
- Read-heavy aggregates served from projections, rarely loaded for commands
- Aggregates that don't live long (created, transitioned, retired)
- Many systems run for years without ever snapshotting

---

## When You Definitely Need Snapshots

- Aggregates that accumulate hundreds or thousands of events over their lifetime
- Workflows or sagas that emit an event per step
- Long-running processes (subscriptions, ledgers, audit trails)
- Any aggregate where loading takes long enough to feel in user latency

---

## Practical Snapshot Cadence

| Aggregate type | Typical event count | Snapshot every |
|---|---|---|
| Order (placed → delivered) | 5–50 | not needed |
| Subscription | 100–10,000 | 100 events |
| Account ledger | 1,000–100,000+ | 100 or 500 events |
| Workflow / Saga | 10–1,000 | 50 events if hot |

- Start without; add when you measure pain

---

## Common Mistakes

- **Snapshotting in the write path**: makes commands slower for no read-side benefit
- **Forgetting to version**: schema change forces emergency snapshot wipe
- **Pruning aggressively**: a single snapshot may be corrupt; keep a few
- **Snapshots as the source of truth**: they aren't; the events are
- **No fall-back to full replay**: makes the system fragile to snapshot store failures

---

## Operational Notes

- Monitor snapshot age: an aggregate with many new events but no recent snapshot is slow to load
- Monitor snapshot store size: snapshots can grow large (the entire aggregate state)
- Backup the snapshot store, but treat it as derivable; events are the source
- Test the "no snapshot" path regularly — verify it still works

---

## Summary

- Snapshots cache aggregate state at a known version, speeding up loading
- Take them asynchronously, every N events, with versioning baked in
- Loading: latest snapshot → replay only events after that version
- Optional, tunable, non-breaking; events remain the source of truth
- Add them when you measure load latency you care about
