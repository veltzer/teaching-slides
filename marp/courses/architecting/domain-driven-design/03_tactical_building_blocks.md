---
tags:
  - concepts:domain-driven-design
  - concepts:design-patterns
level: advanced
category: architecture
audience:
  - audiences:developers

---
# Tactical DDD Building Blocks

---
## What Tactical DDD Provides

- Concrete patterns for implementing the domain model in code
- Entities, value objects, aggregates, domain events, repositories, services
- The building blocks of the write side
- Strategic design defined the boundaries; tactical design fills them

---
## Aggregate

![aggregate](svg/courses/architecting/domain-driven-design/03_tactical_building_blocks/aggregate.svg)

---
## Building Blocks

![tactical_blocks](svg/courses/architecting/domain-driven-design/03_tactical_building_blocks/tactical_blocks.svg)

---
## Entities

- An object with identity that persists over time
- Two entities are different if their IDs differ, even if other fields match
- Examples: `User`, `Order`, `Product`
- Identity comes from the domain, not from the database

---
## Entity Identity

- The id is part of the entity, not metadata
- Often a UUID generated when the entity is created
- The id never changes
- Equality is by id, not by structural equality

---
## Value Objects

- An object defined by its attributes, not by an identity
- Two value objects are equal if their attributes are equal
- Immutable
- Examples: `Money`, `Address`, `DateRange`, `EmailAddress`

---
## Why Value Objects Matter

- "$100" and another "$100" are interchangeable — no identity
- Capturing them as types prevents misuse: you can't add money to a date
- Methods belong on the value object: `money.add(other)`, `address.is_in(country)`
- Reduces primitive obsession in the codebase

---
## Aggregates

- A cluster of entities and value objects treated as one unit
- An aggregate has a root entity (the aggregate root)
- Outside code talks to the root only
- Internal entities are not visible from outside

---
## Aggregate Boundaries

- Define the **consistency boundary**: invariants hold within an aggregate
- A transaction modifies one aggregate
- Cross-aggregate consistency is eventual
- This is the most important tactical decision

---
## Aggregate Root

- The entry point to the aggregate
- Holds references to internal entities
- Enforces invariants
- All commands target the root

---
## Aggregate Example

- `Order` is the aggregate root
- It contains `LineItem`s (entities) and `Address` (value object)
- `Order.add_line_item()` enforces "max 50 items"
- External code calls `order.add_line_item(...)`, not `line_item.set_quantity(...)`

---
## Aggregate Size

- Smaller is better
- Each aggregate is a unit of consistency and lock
- Big aggregates = lock contention, slow writes
- Most aggregates should fit on one screen

---
## Aggregate Rules

- Reference other aggregates by id, not by object reference
- Update one aggregate per transaction
- Invariants within: enforced by the root
- Invariants across: eventual consistency, sagas, process managers

---
## Domain Events

- A meaningful business fact that happened
- Past tense: `OrderPlaced`, `PaymentCaptured`, `ShipmentScheduled`
- Emitted by aggregates when their state changes
- Other parts of the system react to them

---
## Domain Event Anatomy

```python
@dataclass(frozen=True)
class OrderPlaced:
    order_id: OrderId
    customer_id: CustomerId
    items: list[LineItem]
    placed_at: datetime
```

- Immutable
- Carries enough data for subscribers to react
- Names the business fact in domain terms

---
## Repositories

- The persistence abstraction for aggregates
- "Save this order"; "find the order by id"
- Hides the database mechanics
- One repository per aggregate type

---
## Repository Sketch

```python
class OrderRepository:
    def save(self, order: Order) -> None: ...
    def find(self, order_id: OrderId) -> Order | None: ...
```

- Clean, narrow interface
- Implementation hits the database; client code doesn't care how

---
## Domain Services

- Operations that don't naturally belong to a single aggregate
- Stateless; encapsulate domain logic
- Example: `OrderPricingService.calculate(items, customer, region)`
- Use sparingly; prefer aggregate methods when possible

---
## Application Services

- Orchestrate use cases: load an aggregate, call domain methods, save
- Thin layer above the domain
- Don't put business rules here — put them in aggregates and domain services
- One application service method per use case

---
## Application Service Sketch

```python
class PlaceOrderHandler:
    def handle(self, cmd: PlaceOrder) -> None:
        order = self.repo.find(cmd.order_id) or Order.create(cmd.order_id)
        order.place(cmd.items, cmd.customer)
        self.repo.save(order)
        self.bus.publish(order.pull_pending_events())
```

---
## Factories

- Encapsulate the creation of complex aggregates
- Enforce that newly-created aggregates are valid
- Often a static method on the aggregate: `Order.create(...)`
- Or a separate factory class for very complex creation

---
## Specifications

- Encapsulate query criteria as objects
- `OrdersFromCustomer(customer_id).and(WithStatus("pending"))`
- Reusable, composable, testable
- Useful when you have many similar queries

---
## Anti-Corruption Layer (Tactical View)

- A translator between bounded contexts (strategic concept)
- In code: a class or module that maps external models to your domain
- Often in the infrastructure layer
- Keeps the domain layer free of external concerns

---
## Anti-Patterns

- **Anemic domain model**: aggregates with only getters and setters; logic in services
- **Smart UI, dumb domain**: business rules in controllers
- **Repository as DAO**: leaking SQL into the domain
- **Aggregates that span everything**: too coarse to manage
- **Cross-aggregate transactions**: should be sagas

---
## Summary

- Entities (with identity), value objects (without), aggregates (consistency boundary)
- Domain events emitted by aggregates
- Repositories for persistence
- Domain services for cross-aggregate logic; application services for orchestration
- The building blocks fit together; each has a precise role
