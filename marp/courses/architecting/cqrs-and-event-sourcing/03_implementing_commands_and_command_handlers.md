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
# Implementing Commands and Command Handlers

---
## What This Chapter Covers

- Designing command objects
- Command handlers and the pipeline that runs them
- Aggregate roots: the home of write-side invariants
- Producing events from aggregates
- Failure modes, idempotency, and middleware

---
## A Command Is a Request

- Imperative name: `PlaceOrder`, `RefundPayment`, `ChangeAddress`
- Carries everything needed to validate and apply the change
- Carries identity so the operation can be made idempotent
- May fail; the failure is itself a meaningful response

---
## Command Object Design

```python
@dataclass(frozen=True)
class PlaceOrder:
    order_id: OrderId         # who is being acted on
    customer_id: CustomerId   # actor / context
    items: list[LineItem]     # payload
    expected_version: int = 0 # for optimistic concurrency
    correlation_id: UUID      # ties together a workflow
    issued_at: datetime       # when the user said "do it"
```

- Immutable
- Self-validating where possible (types do the work)
- Includes metadata, not just payload

---
## Command Validation: Two Layers

- **Structural**: shape, types, lengths, formats — fail fast before reaching the domain
- **Domain**: business rules that depend on the current aggregate state
- Structural validation lives in the API or DTO layer
- Domain validation lives in the aggregate itself

---
## Structural Validation Example

```python
def validate(cmd: PlaceOrder) -> list[str]:
    errors = []
    if not cmd.items:
        errors.append("at least one item is required")
    if any(item.quantity <= 0 for item in cmd.items):
        errors.append("quantities must be positive")
    if cmd.expected_version < 0:
        errors.append("expected_version must be non-negative")
    return errors
```

- Returns a list, not exceptions — multiple errors are normal
- Runs before any aggregate is loaded
- Fail-fast: if this fails, nothing else needs to happen

---
## Domain Validation Lives in the Aggregate

```python
class Order:
    def place(self, items: list[LineItem]) -> list[Event]:
        if self.status != "draft":
            raise OrderAlreadyPlaced(self.id)
        if not self._customer_in_good_standing():
            raise CustomerSuspended(self.customer_id)
        if self._would_exceed_credit_limit(items):
            raise CreditLimitExceeded(self.customer_id)
        return [OrderPlaced(order_id=self.id, items=items)]
```

- Raises domain-specific exceptions
- Never returns partial success
- Returns events on success, not state

---
## Aggregate Roots

- The unit of consistency in DDD
- Owns its invariants — no other code may violate them
- All commands targeting the aggregate go through the root
- Mutations are produced as events, not direct state changes

---
## Aggregate Lifecycle

![aggregate_lifecycle](svg/courses/architecting/cqrs-and-event-sourcing/03_implementing_commands_and_command_handlers/aggregate_lifecycle.svg)

---
## Loading an Aggregate

```python
def load_order(order_id: OrderId) -> Order:
    events = event_store.read_stream(f"order-{order_id}")
    order = Order.empty(order_id)
    for event in events:
        order.apply(event)
    return order
```

- Read all events for the stream
- Replay them onto a fresh aggregate
- Snapshots can short-circuit this for long streams (chapter 7)

---
## Saving an Aggregate

```python
def save_order(order: Order) -> None:
    new_events = order.pull_pending_events()
    event_store.append(
        stream=f"order-{order.id}",
        expected_version=order.loaded_version,
        events=new_events,
    )
```

- Append only the new events
- `expected_version` enforces optimistic concurrency
- A version mismatch is a `ConcurrencyConflict` — the command must be retried

---
## The Command Handler

```python
class PlaceOrderHandler:
    def __init__(self, event_store: EventStore):
        self._store = event_store

    def handle(self, cmd: PlaceOrder) -> None:
        events = read_stream(self._store, cmd.order_id)
        order = Order.empty(cmd.order_id)
        for event in events:
            order.apply(event)

        new_events = order.place(cmd.items)
        self._store.append(
            stream=f"order-{cmd.order_id}",
            expected_version=cmd.expected_version,
            events=new_events,
        )
```

- One handler per command type
- Loads, decides, saves — that's the whole shape

---
## The Generic Pattern

![command_handler_pipeline](svg/courses/architecting/cqrs-and-event-sourcing/03_implementing_commands_and_command_handlers/command_handler_pipeline.svg)

---
## Command Bus

- A dispatcher that routes commands to their handlers
- Registers handlers by command type
- Optional: applies middleware uniformly to every command

```python
class CommandBus:
    def __init__(self):
        self._handlers: dict[type, Handler] = {}

    def register(self, cmd_type: type, handler: Handler) -> None:
        self._handlers[cmd_type] = handler

    def send(self, cmd: Command) -> None:
        handler = self._handlers[type(cmd)]
        handler.handle(cmd)
```

---
## Middleware Pipelines

- Cross-cutting concerns shouldn't pollute every handler
- Wrap the bus with middleware: logging, metrics, validation, transactions, retries
- Each layer sees the command and decides whether to pass it on
- Order matters; the outer layer runs first on entry, last on exit

---
## Middleware Example

```python
class LoggingMiddleware:
    def __init__(self, inner: CommandBus):
        self._inner = inner

    def send(self, cmd: Command) -> None:
        log.info("command received", extra={"type": type(cmd).__name__})
        try:
            self._inner.send(cmd)
            log.info("command succeeded")
        except Exception as e:
            log.exception("command failed")
            raise

bus = LoggingMiddleware(MetricsMiddleware(ValidationMiddleware(CommandBus())))
```

---
## Common Middleware

- **Validation**: structural validation before reaching the handler
- **Logging**: every command in and out, with correlation id
- **Metrics**: per-command-type counters and latencies
- **Tracing**: open a span for each command
- **Authorization**: permission check based on actor in the command
- **Transactions**: open and close a unit-of-work
- **Retry**: on transient failures (concurrency conflicts, network errors)

---
## Idempotency Matters

- Networks lose responses; clients retry
- The same command may arrive twice
- Without idempotency, the user is charged twice, the order ships twice
- This is not optional in any production system

---
## Idempotency Through Command IDs

```python
@dataclass(frozen=True)
class PlaceOrder:
    command_id: UUID  # client-generated and stable across retries
    order_id: OrderId
    items: list[LineItem]
```

- Client generates `command_id` once and reuses it for retries
- Handler records `command_id` on success
- Subsequent attempts with the same `command_id` are no-ops or return the original result

---
## Idempotency Through Event Identity

- Each event carries a stable `event_id`
- Append rejects duplicate `event_id` for the same stream
- Retrying a command produces the same events; the second append is rejected
- Effective even when client-side `command_id` is missing

---
## Concurrency Conflicts

- Two clients try to modify the same aggregate at version `v`
- The first appends events, advancing the version
- The second's `expected_version` is now stale — the append fails
- The handler must retry: load fresh, decide again, append

---
## Retry on Conflict

```python
for attempt in range(3):
    try:
        handle(cmd)
        return
    except ConcurrencyConflict:
        if attempt == 2:
            raise
        # reload and retry
```

- Bounded retries
- Reload the aggregate each time — the conflict means state changed
- Re-decide based on the new state — the original decision may now be invalid

---
## Concurrency Conflict Resolution

![concurrency_conflict](svg/courses/architecting/cqrs-and-event-sourcing/03_implementing_commands_and_command_handlers/concurrency_conflict.svg)

---
## Producing Events: One vs Many

- A single command often produces a single event
- A command may produce zero events (idempotent re-application)
- A command may produce many events when the decision triggers cascading state
    - `PlaceOrder` could produce `OrderPlaced`, `InventoryReserved`, `LoyaltyAccrued`
- Treat the events as a unit: all are appended atomically or none are

---
## Atomicity of the Append

- The event store guarantees the append of a list of events is atomic
- Either all events are persisted or none are
- This is the boundary of consistency in an event-sourced system
- Side effects beyond the append (notifications, integrations) are eventually consistent

---
## Side Effects: The Hard Part

- An event in the log does not automatically reach external systems
- Sending an email, calling a third-party API, charging a card are side effects
- Side effects must be triggered by projections of the events, not by the handler
- This decouples the write path from the integration path

---
## Side Effects Belong in Subscribers

![side_effects_in_subscribers](svg/courses/architecting/cqrs-and-event-sourcing/03_implementing_commands_and_command_handlers/side_effects_in_subscribers.svg)

---
## Failure Modes

- **Validation failure**: shape is wrong; return errors before loading anything
- **Domain failure**: invariants would be violated; raise a domain exception
- **Concurrency conflict**: state changed under us; retry
- **Storage failure**: the event store is unavailable; the caller should retry later
- **Bug**: an assertion fires; do not swallow — let it crash and log

---
## Mapping Failures to Responses

- Validation failure → 400 Bad Request, with the list of issues
- Domain failure → 409 Conflict or 422 Unprocessable, with a domain code
- Concurrency conflict (after exhausting retries) → 503, retry-after
- Storage failure → 503, retry-after
- Bug → 500, alert on-call

---
## Authorization

- Belongs in middleware, not in the handler
- The actor information comes from the command's metadata (set by the API layer)
- Permissions are checked before the aggregate is loaded
- Domain rules are domain rules; permissions are permissions — keep them apart

---
## Command Handler Smells

- **Returning state**: handlers should return acknowledgement, not data
- **Mutating multiple aggregates**: each command operates on one aggregate
- **Reading from the read model**: the write path does not need read models
- **Side effects in the handler**: those go in subscribers
- **Skipping the aggregate**: every state change goes through the root

---
## One Command, One Aggregate

- A command operates on exactly one aggregate root
- Multi-aggregate workflows are coordinated by a process manager (chapter 8)
- This keeps the unit of consistency clear
- Cross-aggregate operations are explicit, not accidental

---
## Testing Command Handlers (Preview)

- Given a sequence of past events
- When a command is dispatched
- Then a specific sequence of new events is produced (or a specific failure)
- We cover this in detail in chapter 9

---
## Summary

- Commands are immutable requests, named imperatively, carrying identity for idempotency
- Validation has two layers: structural (before) and domain (in the aggregate)
- Aggregate roots own invariants and produce events on successful decisions
- Handlers load, decide, save — nothing more
- Cross-cutting concerns belong in middleware
- Concurrency conflicts are resolved by retry; side effects belong in subscribers
- One command, one aggregate, atomic append
