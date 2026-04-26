---
tags:
  - architecture:cqrs
  - concepts:design-patterns
level: advanced
category: architecture
audience:
  - audiences:architects
  - audiences:developers

---
# Implementing Queries and Read Models

---
## What This Chapter Covers

- Query objects and query handlers
- Read models: purpose, ownership, structure
- Building denormalized views from events
- Multiple read models from a single stream
- Picking storage for the read side
- Caching, staleness, and the user experience

---
## A Query Is a Question

- Imperative? No — declarative: `GetOrderSummary`, not `LoadOrder`
- Carries the parameters that scope the answer
- Returns data shaped for a specific consumer
- Has no side effects and is safe to retry indefinitely

---
## Query Object Anatomy

```python
@dataclass(frozen=True)
class GetOrderSummary:
    order_id: OrderId

@dataclass(frozen=True)
class ListRecentOrders:
    customer_id: CustomerId
    limit: int = 20
    cursor: str | None = None
```

- Immutable
- Identifier-shaped, not aggregate-shaped
- Pagination is built in (cursor or offset, never assume small results)

---
## The Result Type Belongs to the Read Side

```python
@dataclass(frozen=True)
class OrderSummary:
    order_id: OrderId
    customer_name: str
    total: Money
    status: str
    line_count: int
    last_updated: datetime
```

- Includes the customer **name**, not just the id — because that is what the screen needs
- Pre-computed `line_count` and `total`
- This is **not** the aggregate; it is a view shaped for one screen

---
## Query Handler Shape

```python
class GetOrderSummaryHandler:
    def __init__(self, read_db: ReadDB):
        self._db = read_db

    def handle(self, query: GetOrderSummary) -> OrderSummary | None:
        row = self._db.fetch_one(
            "SELECT * FROM order_summary WHERE order_id = ?",
            (query.order_id,),
        )
        return OrderSummary(**row) if row else None
```

- Direct read from a denormalized table
- No aggregate loading, no event replay
- Fast and simple — that's the whole point

---
## Read Models Are Different From the Aggregate

- The aggregate is shaped for invariant enforcement
- The read model is shaped for query performance
- They share a domain identity but not a structure
- One change in the read model does not affect the write side

---
## Read Model Ownership

- A read model is owned by **one consumer**: a screen, a report, a search index
- Two consumers with different needs get two read models
- Avoid the temptation to make a "general purpose" read model
- General purpose read models drift back into the same problem CQRS solves

---
## Multiple Read Models From One Stream

![multiple_read_models](svg/courses/architecting/cqrs-and-event-sourcing/04_implementing_queries_and_read_models/multiple_read_models.svg)

---
## Read Model Examples for an Order

- **Order Summary** (mobile app): id, total, status, last_updated
- **Customer Order History** (web): id, date, total, item_count — paginated
- **Operations Dashboard** (admin): id, status, age_in_state, blocked_reason
- **Search Index**: full-text on customer name + items, faceted by status
- **Reporting Cube**: revenue by day, by region, by product category

---
## Building a Read Model From Events

```python
class OrderSummaryProjection:
    def __init__(self, db: ReadDB):
        self._db = db

    def handle(self, event: Event) -> None:
        match event:
            case OrderPlaced(order_id, customer_id, items):
                self._db.execute(
                    "INSERT INTO order_summary VALUES (?, ?, ?, ?, ?, ?)",
                    (order_id, customer_id, sum_total(items),
                     "placed", len(items), now()),
                )
            case OrderCancelled(order_id, _):
                self._db.execute(
                    "UPDATE order_summary SET status='cancelled', "
                    "last_updated=? WHERE order_id=?",
                    (now(), order_id),
                )
```

---
## The Projection Pattern

- One handler per event type the projection cares about
- Each handler is an idempotent SQL operation
- The projection tracks where it is in the stream (a checkpoint)
- New events arrive; the projection advances

---
## Projection Components

![projection_components](svg/courses/architecting/cqrs-and-event-sourcing/04_implementing_queries_and_read_models/projection_components.svg)

---
## Synchronizing Read Models With the Write Side

- Three options:
    1. **Inline** — update the read model in the same transaction as the event append
    1. **Asynchronous** — a subscriber tails the event log and projects later
    1. **On-demand** — replay the events when the query arrives
- Most production systems use asynchronous; chapter 6 goes deep

---
## Sync vs Async vs On-Demand

![sync_async_ondemand](svg/courses/architecting/cqrs-and-event-sourcing/04_implementing_queries_and_read_models/sync_async_ondemand.svg)

---
## Picking Storage for the Read Side

- The right answer depends on the query
- A single CQRS system commonly uses several stores at once
- The cost of duplication is low; the benefit of fit is high

---
## Relational Stores for Read Models

- Best when queries need joins, sorting, ranges, transactions across rows
- Strong indexing
- The schema is shaped for the query, not the aggregate
- Most mature tooling, well-understood operational profile
- Examples: PostgreSQL, MySQL, SQL Server

---
## Document Stores for Read Models

- Best when each query loads a self-contained document
- The shape of the document matches what the screen needs exactly
- One read = one document; minimal joins
- Examples: MongoDB, DynamoDB, Couchbase

---
## Search Engines for Read Models

- Best for full-text, fuzzy match, faceted search
- Update via projections; the search index is just another read model
- Eventually consistent by nature
- Examples: Elasticsearch, OpenSearch, Meilisearch

---
## Caches as Read Models

- A Redis hash or sorted set can be a read model in its own right
- Best when the query is hot, simple, and tolerates short-lived staleness
- Update via projections; cache eviction policies handle long tails
- Examples: Redis, Memcached, Hazelcast

---
## Picking Storage By Query Shape

![storage_by_query_shape](svg/courses/architecting/cqrs-and-event-sourcing/04_implementing_queries_and_read_models/storage_by_query_shape.svg)

---
## A Read Model Is Disposable

- If the projection logic changes, drop the read model and rebuild
- Replay the events from event 0 onto a fresh table or index
- This is normal operations, not an exotic recovery procedure
- Plan for read model rebuilds the way you plan for deploys

---
## Rebuild Capability Changes Everything

- "Add a column" — replay the projection with the new column added
- "Backfill historical data" — same: replay
- "Switch storage technology" — point a new projection at the old events
- This flexibility is one of the biggest payoffs of event sourcing

---
## Caching the Read Side

- Two layers: the read model itself, and a cache in front of it
- Read model: pre-computed, persistent, eventually consistent with events
- Cache: hot results in memory, evicted by TTL or pressure
- A query may hit cache → read model → (rarely) replay

---
## A Cache Hierarchy

![read_side_cache_hierarchy](svg/courses/architecting/cqrs-and-event-sourcing/04_implementing_queries_and_read_models/read_side_cache_hierarchy.svg)

---
## Cache Invalidation Strategies (Quick Recap)

- **TTL** — bounded staleness; cheap; lossy
- **Event-driven** — invalidate when the relevant event projects
- **Version-based** — bake a version into the cache key
- For depth, see Architecture Patterns ch 10

---
## Stale Reads Are Reality

- The read model lags the write model by milliseconds, sometimes seconds
- A user who just placed an order may not see it in their list yet
- The system is correct; the UI must explain
- Telling the user is cheaper than rebuilding the system to be strongly consistent

---
## UX Patterns for Eventual Consistency

- **Optimistic update**: show the new state immediately, reconcile when the server confirms
- **Polling for confirmation**: the UI re-queries until it sees the change
- **Server-pushed update**: webhook or websocket notifies the UI when the projection lands
- **Pending banner**: explicit "your order is being processed" UI

---
## Optimistic Update Example

```javascript
// User places an order
async function placeOrder(items) {
  const tempId = uuid();
  // Show immediately in the UI with the temp id
  ui.addOrder({ id: tempId, items, status: "submitting" });

  const realId = await api.placeOrder({ command_id: tempId, items });

  // Replace the optimistic row with the real one once confirmed
  ui.replaceOrder(tempId, { id: realId, status: "placed" });
}
```

---
## When Strong Consistency Is Required

- Some queries must reflect the write that just happened
- The reader must "see their own write" — e.g., a confirmation page
- Three honest options:
    1. Read from the write store directly (bypass projections)
    1. Wait for the projection to catch up to the version we just wrote
    1. Render from the events themselves on this one query

---
## Read-Your-Own-Write Pattern

```python
# Just appended events up to version 7 for order-42
# Now we want to render the confirmation page
def render_confirmation(order_id, expected_version):
    while True:
        row = read_db.fetch("SELECT version FROM orders WHERE id=?", order_id)
        if row and row.version >= expected_version:
            return render(row)
        sleep(0.05)  # tight bound; bail out after a deadline
```

- Caller passes the version it wrote
- Reader waits for the projection to catch up
- Bounded wait — fall back to a "still processing" page if exceeded

---
## Pagination

- Read models often serve large lists
- Cursor-based beats offset-based at scale
- The cursor encodes the position; the next page resumes from there
- The read model schema must include the cursor's sort key

---
## Cursor Pagination

```python
@dataclass(frozen=True)
class ListOrdersPage:
    items: list[OrderSummary]
    next_cursor: str | None

def list_orders(customer_id, limit, cursor):
    where = "customer_id = ?"
    if cursor:
        where += " AND (created_at, id) < (?, ?)"
    rows = db.query(f"... WHERE {where} ORDER BY created_at DESC, id DESC LIMIT ?",
                    bind(customer_id, cursor, limit + 1))
    has_more = len(rows) > limit
    return ListOrdersPage(rows[:limit], next_cursor_for(rows[-1]) if has_more else None)
```

---
## Authorization on the Read Side

- Like commands, queries need permission checks
- The check happens in middleware or in the query handler
- The check uses the actor in the query, not the data
- Filter results to what the actor may see — not what exists

---
## Read Model Schema Migrations

- Two strategies:
    1. **Rebuild**: drop, create new schema, replay
    1. **In-place**: ALTER, backfill from events, swap
- Rebuild is the safer default — the events are the source of truth
- In-place is faster for tiny changes (renaming a non-essential column)

---
## Common Smells

- **Querying the aggregate**: that's the write model; reads should hit a read model
- **Joining many read models in one query**: build a new read model that already has the join
- **Mutating the read model from a handler**: the read model is updated only by projections
- **One read model per database table**: think per-screen, not per-table

---
## A Concrete Example: Order Domain Read Models

- `orders_by_customer` — list view; cursor by created_at
- `order_details` — single record per order with totals and status
- `pending_shipments` — operations queue; one row per pending shipment
- `revenue_by_day` — analytics roll-up
- All built from the same event stream — independently rebuildable

---
## Summary

- Queries are immutable, declarative, side-effect free
- Read models are owned by one consumer and shaped for that consumer's screen
- Build them by projecting the same event stream into multiple shapes
- Pick storage to fit the query, not the other way around
- Read models are disposable; rebuilding from events is normal operations
- Cache layers and UX patterns make eventual consistency livable
