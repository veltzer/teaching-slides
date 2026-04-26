---
tags:
  - architecture:saga
  - practices:testing
level: advanced
category: architecture
audience:
  - audiences:architects
  - audiences:developers

---
# Testing and Debugging Sagas

---
## What This Chapter Covers

- Unit-testing orchestrators and choreography handlers
- Simulating failure scenarios
- Integration testing with real brokers
- Contract tests between participants
- Distributed tracing for visibility
- Saga monitoring and alerts
- Common anti-patterns
- Production debugging

---
## Why Sagas Need Special Test Discipline

- Failure paths are easy to forget — they only run when something breaks
- Distributed coordination is hard to reason about manually
- Production bugs surface as stuck sagas with no obvious cause
- Test rigor up front saves on-call pages later

---
## Unit Testing the Orchestrator

- The orchestrator is a pure state machine — perfect for unit tests
- Given a state and an event, assert the next state and emitted commands
- No real services, no real broker
- Fast, deterministic, comprehensive

---
## Orchestrator Test Pattern

```python
def test_payment_failed_triggers_compensation():
    saga = OrderSaga.start("42", items=[item("a", 1)])
    saga.handle(InventoryReserved("42"))

    saga.handle(PaymentFailed("42", reason="insufficient_funds"))

    assert saga.status == "compensating"
    assert saga.last_command == ReleaseInventory("42")
```

- Given: starting state and history
- When: an event arrives
- Then: state transition and emitted command(s)

---
## Simulating Failure Scenarios

- Test every step's failure
- Test every retry threshold
- Test every timeout
- Test failures during compensation
- Test halted-saga path

---
## Failure Test Coverage Matrix

| Step | Success | Transient fail | Permanent fail | Timeout |
|---|---|---|---|---|
| Reserve inventory | ✓ | ✓ | ✓ | ✓ |
| Capture payment | ✓ | ✓ | ✓ | ✓ |
| Schedule shipment | ✓ | ✓ | ✓ | ✓ |
| (compensations) | ✓ | ✓ | ✓ (halted) | ✓ |

- Each cell is at least one test
- Comprehensive but not heroic — most are 5-line assertions

---
## Choreography Unit Tests

- Each participant is its own unit
- Given an inbound event, assert the local action and the outbound event
- No orchestrator, but the same `given/when/then` pattern
- Test both forward and reactive-compensation handlers

---
## Choreography Handler Test

```python
def test_inventory_reacts_to_OrderCancelled():
    inventory = InventoryService(db)
    db.reservations.add(Reservation(order_id="42", sku="a", qty=1))

    inventory.handle(OrderCancelled(order_id="42"))

    assert db.reservations.find("42").released is True
    assert outbox.last == InventoryReleased(order_id="42")
```

---
## Integration Tests

- Spin up a real broker (Kafka, NATS, RabbitMQ) in a container
- Spin up the participants in containers or as test processes
- Run the saga end-to-end
- Assert the final state across services

---
## Integration Test Anatomy

```python
def test_order_saga_end_to_end(broker, services):
    services.sales.send(PlaceOrder(order_id="42", ...))

    wait_until(lambda: services.shipping.has("42"))

    assert services.inventory.reserved("42") is True
    assert services.payment.captured("42") == amount
```

- Slow but thorough
- A few of these per saga is plenty
- Run on every CI build, not on every commit

---
## Contract Testing Between Participants

- Each participant publishes events; others consume them
- Schemas are contracts
- Pact-style tests verify producers haven't broken consumers
- Schema registries enforce compatibility at deploy time

---
## A Producer Contract Test

```python
def test_OrderPlaced_contract():
    event = sales.publish_OrderPlaced(order_id="42", customer="c1")

    # Verifies the event matches the schema downstream consumers expect
    pact.assert_matches(event, "OrderPlaced", version="v2")
```

- Lightweight; fast
- Run on producer's CI; fails if a consumer's contract is broken

---
## Distributed Tracing

- Every saga step crosses a service boundary
- A trace ties together the spans across services
- Open standard: OpenTelemetry
- Backends: Jaeger, Tempo, Zipkin

---
## Saga Visibility Stack

![saga_visibility](svg/courses/architecting/saga-pattern/06_testing_and_debugging_sagas/saga_visibility.svg)

---
## Trace Propagation

- Each event carries a trace id and span id
- Each participant continues the trace from the inbound event
- Each command/response is a span
- The full saga is one trace tree

---
## Useful Trace Annotations

- `saga_id` (= correlation id)
- `step_name`
- `attempt_number`
- `is_compensation`
- `participant`
- A search by `saga_id` returns the entire flow

---
## Saga Monitoring Dashboards

- Number of in-flight sagas, by status
- Average and P99 saga duration
- Compensation rate (how often we fail)
- Halted saga count (alert)
- Per-step failure rate

---
## Alerts to Set Up

- Halted sagas exist (operator action required)
- Saga duration P99 exceeds threshold
- Compensation rate exceeds baseline
- Specific step's failure rate exceeds threshold
- Stuck saga: no progress for N minutes

---
## A Sample Alert

```yaml
- alert: SagaHaltedRequiresIntervention
  expr: |
    sum(saga_status{state="requires_intervention"}) > 0
  for: 5m
  labels:
    severity: page
  annotations:
    summary: "Saga halted; manual review needed"
    runbook: "https://wiki/runbooks/saga-halted"
```

- Halted sagas are a real condition; pages are appropriate

---
## Anti-Patterns That Hurt at Test Time

- **Long sagas**: a 30-step saga is hard to test exhaustively — split it
- **Missing compensations**: only discovered during failure tests
- **State explosion**: the orchestrator's state machine has thousands of states — model with sub-sagas
- **Implicit ordering**: tests pass in dev, fail in prod due to event-order assumptions
- **Hidden side effects**: compensations that touch unrelated systems

---
## Production Debugging: First Steps

- Find the saga id (correlation id) from the trigger
- Query the saga state store: where is it stuck?
- Query the trace by saga id: what was the last successful step?
- Query the participant's logs for that step
- Decide: retry, manual completion, or compensation

---
## Replaying Events

- For event-sourced orchestrators: replay events to reconstruct the saga
- For workflow-engine sagas: use the engine's history feature
- Always non-destructive — replay does not re-trigger side effects unless explicitly requested
- Useful for "why did this saga go this way?" forensic work

---
## Manual Saga Intervention

- Some halted sagas need a human in the loop
- Examples: customer reaches max retries on payment; goods damaged in transit
- The saga state machine should expose admin operations
- Operations should be auditable: who did what, when, why

---
## Admin Operations

- `RetryStep`: try the failing step again
- `SkipStep`: mark as completed; useful when the action was done out of band
- `ForceCompensate`: trigger compensation despite being past the pivot
- `MarkResolved`: close the saga without running anything else
- All require justification stored in the audit log

---
## Common Anti-Patterns Recap

- **Sagas as cargo-cult**: using a saga where a local transaction would do
- **Saga aggregates that grow without bound**: split into sub-sagas
- **Compensations as afterthoughts**: design them with the forward steps
- **No correlation id**: cannot debug; cannot monitor
- **No idempotency**: at-least-once delivery turns into double-charges
- **No timeouts**: silent saga death

---
## A Reasonable Production Setup

- Event store / message broker with durable subscriptions
- Per-saga correlation id propagation
- Distributed tracing (OpenTelemetry → Jaeger)
- Per-saga state store with admin UI
- Dashboards: status counts, durations, compensation rate, halted sagas
- Runbook for halted sagas; on-call rotation for halts

---
## Where to Go From Here

- Pick one cross-service workflow in your system
- Make it a saga — orchestration if you want visibility, choreography if you want autonomy
- Define every step's compensation alongside the step
- Wire up correlation IDs and a saga timeline projection
- Build the dashboard before the saga goes live

---
## Course Recap

- Chapter 1: distributed transactions, why 2PC fails, eventual consistency contract
- Chapter 2: saga fundamentals
- Chapter 3: choreography
- Chapter 4: orchestration
- Chapter 5: compensations and pivots
- Chapter 6: testing, debugging, monitoring

---
## Summary

- Unit-test orchestrators as state machines; choreography handlers as event functions
- Cover failure paths with the same rigor as happy paths
- Distributed tracing turns "where is order 42?" into a search query
- Halted sagas are first-class operational events; alerts and runbooks are mandatory
- Sagas are tractable when treated as a domain concept — not as a clever trick
