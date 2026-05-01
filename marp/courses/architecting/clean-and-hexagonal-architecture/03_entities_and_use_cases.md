---
tags:
  - architecture:clean-architecture
  - architecture:domain
level: intermediate
category: architecture
audience:
  - audiences:developers

---
# Entities and Use Cases

---
## What This Chapter Covers

- What an entity is
- Domain rules in entities
- What a use case is
- Input/output ports
- Use case structure
- A worked example

---
## What An Entity Is

- A business object with identity
- Encapsulates rules that apply *regardless of the application*
- "An order has at least one line item"
- "An employee's salary cannot be negative"
- Pure code; no framework

---
## Entity Example

```python
class Order:
    def __init__(self, id, customer_id):
        self.id = id
        self.customer_id = customer_id
        self.items = []

    def add_item(self, item):
        if item.quantity <= 0:
            raise ValueError("quantity must be positive")
        self.items.append(item)

    def total(self):
        return sum(i.subtotal() for i in self.items)
```

---
## What A Use Case Is

- Application-specific operation
- "Place an order"
- "Cancel an order"
- "List a customer's orders"
- Each one is a separate class / function

---
## Use Case Example

```python
class PlaceOrderUseCase:
    def __init__(self, order_repo, payment_gateway, mailer):
        self._order_repo = order_repo
        self._payment_gateway = payment_gateway
        self._mailer = mailer

    def execute(self, customer_id, items):
        order = Order(uuid4(), customer_id)
        for item in items:
            order.add_item(item)
        self._payment_gateway.charge(customer_id, order.total())
        self._order_repo.save(order)
        self._mailer.send_confirmation(order)
        return order
```

---
## Input Ports

- The use case's method signatures
- "PlaceOrderUseCase.execute(customer_id, items) &#8594; Order"
- Plain types; not HTTP or framework
- Other layers depend on these

---
## Output Ports

- Interfaces the use case calls
- `OrderRepository`, `PaymentGateway`, `Mailer`
- Defined in the use case layer
- Implemented in the adapter layer

---
## Use Case Granularity

- One use case per business operation
- Don't merge unrelated operations
- A use case is small; one method usually
- "ServiceClass" with 30 methods is a smell

---
## Use Case Composition

- Complex operations = orchestrate multiple use cases
- Or: one use case calls another
- Either works; pick consistency
- The orchestration belongs in another use case, not the controller

---
## Pure Functions vs Classes

- Use case can be a function
- "PlaceOrder is a function from (deps, input) to output"
- Functional approach: clean, testable
- OO approach: more familiar to many teams
- Both fit clean architecture

---
## Domain Events

- Use case publishes events: "OrderPlaced"
- Other use cases subscribe
- Decouples cross-domain interactions
- Often combined with event sourcing

---
## A Test For A Use Case

- No HTTP / DB / framework in test
- Inject fakes for ports
- Call execute(); assert on returned value and fake state
- Fast; deterministic
- The TDD-friendly way to build domains

---
## Common Mistakes

- Use cases that take HTTP request objects as input
- Entities that have ORM annotations
- "Service" class with many unrelated methods
- Use case that doesn't define its own interfaces
- Entities that depend on use cases (reverse direction)
