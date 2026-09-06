---
tags:
  - architecture:clean-architecture
  - architecture:adapters
level: intermediate
category: architecture
audience:
  - audiences:developers

---

# Interface Adapters

---

## Adapter Roles

![adapter_roles](svg/courses/architecting/clean-and-hexagonal-architecture/04_interface_adapters/adapter_roles.svg)

---

## What This Chapter Covers

- The role of adapters
- Controllers
- Presenters
- Gateways / repositories
- View models
- DTOs

---

## What An Adapter Is

- Translates between layers
- Outer to inner: parse input
- Inner to outer: format output
- Lives in its own layer
- Replaceable

---

## Adapter Roles

![adapter_pattern](svg/courses/architecting/clean-and-hexagonal-architecture/04_interface_adapters/adapter_pattern.svg)

---

## Controllers

- Receive HTTP request
- Validate, parse
- Build use case input
- Call use case
- Return HTTP response
- Thin

---

## Controller Example

```python
@app.post("/orders")
def place_order(request):
    body = request.json()
    items = [Item(p['id'], p['qty']) for p in body['items']]
    use_case = PlaceOrderUseCase(...)
    order = use_case.execute(body['customer_id'], items)
    return {"order_id": order.id}, 201
```

---

## Presenters

- Format use case output for the view
- ViewModel: "Order #42 placed; total $99.99"
- Domain model untouched
- Controller depends on presenter; presenter depends on use case

---

## Gateways

- Implement output ports
- Database access
- External API calls
- Plug-in for the use case

---

## Repository Example

```python
class PostgresOrderRepository(OrderRepository):
    def __init__(self, conn):
        self.conn = conn

    def save(self, order):
        self.conn.execute(
            "INSERT INTO orders (id, customer_id) VALUES (%s, %s)",
            (order.id, order.customer_id)
        )
```

- Implements the interface in the use case layer

---

## DTOs

- Data Transfer Objects
- Plain data; no behaviour
- Cross layer boundaries
- Different from entities (entities have behaviour)
- Define per-direction (input DTO, output DTO)

---

## When To Use DTOs

- Use cases input / output: DTOs
- API request / response: DTOs (controllers map)
- Repository methods: entities directly (or DTOs)
- More layers = more DTOs = more mapping
- Pragmatically: minimise

---

## View Models

- For UI rendering
- Computed display fields
- "$99.99" instead of `99.99` `USD`
- Not the domain entity
- Built by presenters

---

## Avoiding Anaemic Layers

- Each layer has a real role
- Controllers: protocol translation
- Use cases: business orchestration
- Adapters: technology integration
- If a layer is pure pass-through, consider merging

---

## Adapter Naming

- Suffix with the technology: `PostgresOrderRepository`
- Or: prefix with the use: `OrderApiController`
- Don't name by the interface alone (`OrderRepository` is the *interface*)
- Names reveal layer membership

---

## Multi-Adapter Setups

- One use case; many adapters
- `OrderRepository` &#8594; Postgres in prod, in-memory in tests
- DI container picks
- Same use case; different deployment

---

## Adapters For Cross-Cutting

- Logging, metrics, tracing: adapters or middleware
- Don't put in use cases (they're for business logic)
- Decorator pattern: wrap use cases with cross-cutting
- Or: aspect-oriented (Spring) where appropriate

---

## Common Mistakes

- Controllers with business logic
- Use cases imported into controllers via concrete class (skip the interface)
- Repository returning ORM entity directly (leak)
- DTOs proliferate (one per layer-pair, plus mappers everywhere)
- "Slim controller" that's actually a fat use case in disguise
