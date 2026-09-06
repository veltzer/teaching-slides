---
tags:
  - architecture:cqrs
  - architecture:event-sourcing
  - practices:testing
level: advanced
category: architecture
audience:
  - audiences:architects
  - audiences:developers

---

# Testing CQRS / Event-Sourced Systems

---

## What This Chapter Covers

- The given-when-then pattern for command handlers
- Unit-testing aggregates with event-based assertions
- Testing projections by replaying scenarios
- Integration tests across command and query pipelines
- Consumer-driven contract tests for integration events
- Test data and event fixture strategies
- Common pitfalls

---

## Why Testing Looks Different Here

- The system speaks in events; tests should too
- "Given these events, when this command, then these new events"
- Pure functions (decide and apply) are trivially testable
- Eventual consistency means assertions about state need timeout/poll patterns
- Tests are reproducible by construction: feed in events, get the same output

---

## The Given-When-Then Pattern

- **Given**: a sequence of events that already happened to the aggregate
- **When**: a command is dispatched
- **Then**: a specific sequence of new events is produced (or a specific failure)
- Maps directly onto how event-sourced aggregates work
- The same scaffold works for hundreds of test cases

---

## Given-When-Then Visualized

![given_when_then](svg/courses/architecting/cqrs-and-event-sourcing/09_testing_cqrs_es_systems/given_when_then.svg)

---

## A Concrete Test

```python
def test_placing_an_order_emits_OrderPlaced():
    # Given
    history = []  # nothing has happened to this aggregate yet

    # When
    cmd = PlaceOrder(order_id=OrderId("42"),
                     customer_id=CustomerId("c1"),
                     items=[item("sku-1", 1)])
    new_events = handle_place_order(history, cmd)

    # Then
    assert new_events == [
        OrderPlaced(order_id=OrderId("42"),
                    customer_id=CustomerId("c1"),
                    items=[item("sku-1", 1)])
    ]
```

- Pure: no database, no clock, no broker
- Fast: thousands of tests in seconds
- Stable: events are values; equality just works

---

## Testing Failure Cases

```python
def test_placing_an_already_placed_order_is_rejected():
    history = [
        OrderPlaced(order_id=OrderId("42"), ...),
    ]
    cmd = PlaceOrder(order_id=OrderId("42"), ...)

    with pytest.raises(OrderAlreadyPlaced):
        handle_place_order(history, cmd)
```

- Same shape; assertion is on the exception
- Domain exceptions are the negative space of the event set
- Cover both: events emitted on success, exception on failure

---

## Testing the Apply Method

```python
def test_apply_OrderPlaced_sets_status_to_placed():
    order = Order.empty(OrderId("42"))
    order.apply(OrderPlaced(order_id=OrderId("42"), items=[item("a", 1)]))
    assert order.status == "placed"
    assert len(order.items) == 1
```

- The apply method is a pure state mutation
- Test each event handler in isolation
- These are tiny, fast, and catch state-shape regressions early

---

## Testing Aggregates: The Whole Picture

```python
def test_full_lifecycle():
    history = [OrderPlaced(...), ItemShipped(...)]
    cmd = MarkDelivered(...)

    new_events = handle(history, cmd)

    assert new_events == [OrderDelivered(...)]
```

- The handler is `(history, cmd) -> events_or_exception`
- No I/O, no time, no globals
- Pair every command with at least one happy-path and one failure test

---

## Property-Based Testing

```python
@given(st.lists(any_event_for_order(), min_size=0, max_size=20))
def test_replay_is_deterministic(events):
    a = Order.empty()
    b = Order.empty()
    for e in events:
        a.apply(e)
        b.apply(e)
    assert a == b
```

- Generate sequences of events; assert invariants
- "Replaying the same events on a fresh aggregate gives the same state"
- Catches edge cases that example-based tests miss

---

## Testing Projections

```python
def test_OrderSummaryProjection_handles_OrderPlaced():
    db = InMemoryDB()
    proj = OrderSummaryProjection(db)

    proj.handle(OrderPlaced(order_id="42", customer="c1",
                            items=[item("a", 50)]))

    assert db.fetch_one("SELECT * FROM order_summary WHERE order_id='42'") == {
        "order_id": "42", "customer_id": "c1", "total": 50, "status": "placed",
    }
```

- Feed events; assert read model rows
- An in-memory database keeps tests fast
- The same projection code is used in production and in test

---

## Replay Scenario Tests

- Build a list of events that represents an interesting scenario
- Run the projection over them
- Assert the resulting read model state
- Run on the same events with a different starting checkpoint to test resumability

---

## Replay Scenarios

![replay_scenarios](svg/courses/architecting/cqrs-and-event-sourcing/09_testing_cqrs_es_systems/replay_scenarios.svg)

---

## Idempotency Tests

```python
def test_projection_is_idempotent():
    proj = OrderSummaryProjection(db)
    e = OrderPlaced(...)

    proj.handle(e)
    proj.handle(e)  # delivered twice

    rows = db.fetch_all("SELECT * FROM order_summary")
    assert len(rows) == 1  # only one row, despite two handle calls
```

- Replay simulates at-least-once delivery
- The projection must produce the same state regardless of duplicate events
- A required test for any production projection

---

## Out-of-Order Event Tests

```python
def test_projection_handles_events_out_of_order():
    proj = OrderSummaryProjection(db)
    proj.handle(OrderShipped(order_id="42"))  # arrives first
    proj.handle(OrderPlaced(order_id="42"))   # arrives second
    # Assert the final state is correct regardless of order
```

- Cross-stream projections may receive events out of order
- Test handlers tolerate it (or document the assumption that they don't)

---

## Integration Tests: Command Pipeline

```python
def test_command_pipeline_end_to_end(db, store, bus):
    bus.send(PlaceOrder(order_id="42", ...))

    # The events should be in the store
    events = store.read_stream("order-42")
    assert events == [OrderPlaced(order_id="42", ...)]

    # The projection should have produced a read model row
    wait_until(lambda: db.fetch_one("SELECT * FROM order_summary WHERE order_id='42'"))
```

- Real event store, real database, real projection
- Slower than unit tests; cover the wiring
- Use a small docker-compose for the supporting services

---

## Integration Tests: Query Pipeline

```python
def test_query_pipeline_end_to_end(db, queries):
    db.execute("INSERT INTO order_summary VALUES (...)")  # seed read model

    result = queries.execute(GetOrderSummary(order_id="42"))

    assert result.order_id == "42"
    assert result.total == 95
```

- The query path is simpler — no append, no projection
- Seed the read model directly; assert the result of the handler
- Authorization tests fit naturally here

---

## Wait-Until for Eventual Consistency

```python
def wait_until(predicate, *, timeout=5.0, interval=0.05):
    deadline = time.time() + timeout
    while time.time() < deadline:
        if predicate():
            return
        time.sleep(interval)
    raise AssertionError("predicate never became true")
```

- Bounded wait; never an infinite loop
- The interval is short enough to be fast on the happy path
- The timeout is generous enough to not flap under CI load

---

## Consumer-Driven Contract Tests

- A producer publishes integration events; multiple consumers depend on them
- Each consumer specifies what it requires from the event schema
- The producer's CI runs these contracts on every change
- Breaking a contract fails the producer's build, not the consumer's runtime
- Tools: Pact, Spring Cloud Contract

---

## Pact Flow

![pact_flow](svg/courses/architecting/cqrs-and-event-sourcing/09_testing_cqrs_es_systems/pact_flow.svg)

---

## A Pact-Style Test

```python
# Consumer side: define what we expect
def test_consumer_expects_OrderPlaced():
    pact.given("an order has been placed").upon_receiving("OrderPlaced") \
        .will_respond_with({"order_id": "...", "customer_id": "...",
                            "total": 95.0})

# This generates a pact file the producer must satisfy
```

- The consumer states its expectation in code
- The producer's tests verify they meet every consumer's expectation
- Adding a new field is safe; removing one breaks the build

---

## Test Data and Event Fixtures

- A library of named event sequences that represent canonical scenarios
- "An order placed but not yet shipped"
- "An order delivered last week"
- "A customer in good standing"
- Reuse across tests; the names communicate intent

---

## Fixture Builders

```python
def order_placed(order_id="42", customer_id="c1", items=None):
    return OrderPlaced(
        order_id=OrderId(order_id),
        customer_id=CustomerId(customer_id),
        items=items or [item("sku-1", 1)],
        ...
    )

def shipped_order(order_id="42"):
    return [order_placed(order_id), ItemShipped(order_id, ...)]
```

- Helpers with sensible defaults
- Tests stay readable: "given a shipped order, when..."
- Avoids large copy-paste of event payloads in every test

---

## Snapshot Tests for Read Models

- Take a known event sequence
- Project it
- Snapshot the resulting database state (json or SQL dump)
- Diff against a stored "golden" snapshot
- Re-run after intentional changes; review the diff before accepting

---

## Snapshot Test Trade-Offs

- Catches unintentional output changes immediately
- The "golden" file becomes maintenance overhead
- Best for stable read models; bad for highly evolving ones
- Pair with example-based tests for surgical assertions

---

## Common Pitfalls

- **Testing through the database**: slow and brittle; prefer pure handler tests
- **Real-time clocks in tests**: events have timestamps; inject a fake clock
- **Sleeping instead of polling**: sleeps are flaky; bounded polling is robust
- **Mocking the event store**: the contract is small; use a real in-memory implementation
- **Coupling tests to read model schema**: prefer asserting on rows by column name

---

## A Reasonable Test Pyramid

- **Many** unit tests for handlers (`given/when/then` over events)
- **Many** unit tests for `apply` methods (state mutation)
- **Some** unit tests for projections with in-memory DB
- **Some** integration tests for the command + projection pipeline
- **Few** end-to-end tests for full user journeys
- **Always-on** consumer-driven contracts for integration events

---

## Test Pyramid

![test_pyramid](svg/courses/architecting/cqrs-and-event-sourcing/09_testing_cqrs_es_systems/test_pyramid.svg)

---

## Course Recap

- Chapter 1: CQRS — separate read and write models
- Chapter 2: Event Sourcing — events as the source of truth
- Chapters 3-4: write side and read side
- Chapter 5: event store choices
- Chapter 6: projections and eventual consistency
- Chapter 7: snapshots
- Chapter 8: DDD, microservices, and integration
- Chapter 9: testing the whole thing

---

## Where to Go From Here

- Pick a small bounded context in your system
- Implement CQRS without ES first; measure
- Add ES if events become the natural model
- Build one read model at a time; rebuild often
- Treat operational tooling (monitoring, replay) as first-class from day one
- Read the source: Greg Young's talks, Vaughn Vernon's books, Adam Dymitruk's posts

---

## Summary

- Tests follow the system: events in, events out
- Handler tests are pure; projection tests use in-memory storage
- Eventual consistency means polling, not sleeping
- Consumer-driven contracts protect integration event schemas
- The pyramid stays similar: many small tests, fewer large ones
- A well-tested CQRS/ES system is one of the most refactor-friendly architectures around
