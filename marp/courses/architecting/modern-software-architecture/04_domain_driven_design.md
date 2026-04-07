# Domain-Driven Design

---
## What Is Domain-Driven Design?

- An approach to software development that centers on the business domain
- Introduced by Eric Evans in his 2003 book "Domain-Driven Design"
- Bridges the gap between domain experts and developers
- Focuses on creating a shared understanding of the problem space

---
## Why DDD Matters for Modern Architecture

- Provides a principled way to decompose systems into services
- Aligns software boundaries with business boundaries
- Reduces miscommunication between technical and business teams
- Scales well as systems and organizations grow

---
## Strategic vs Tactical Design

![strategic_vs_tactical_design](/out/mermaid/courses/architecting/modern-software-architecture/04_domain_driven_design/strategic_vs_tactical_design.svg)

---
## The Ubiquitous Language

- A shared vocabulary between developers and domain experts
- Used consistently in code, documentation, and conversation
- Eliminates translation layers between business and technical language
- Each `Bounded Context` has its own ubiquitous language

---
## Building the Ubiquitous Language

- Collaborate with domain experts through workshops and interviews
- Document key terms in a glossary accessible to everyone
- Reflect domain terms directly in class names, method names, and variables
- Revise the language as understanding of the domain deepens

---
## Ubiquitous Language Example

- Domain expert says: "A customer places an order with line items"
- Code should reflect this directly:

```python
class Customer:
    def place_order(self, line_items):
        order = Order(customer=self,
                      items=line_items)
        return order
```

- Avoid technical jargon that domain experts do not recognize

---
## Bounded Contexts Defined

- A boundary within which a particular domain model applies
- Each context has its own ubiquitous language and model
- The same real-world concept may have different representations in different contexts
- Boundaries are explicit and enforced

---
## Bounded Context Example

![bounded_context_example](/out/mermaid/courses/architecting/modern-software-architecture/04_domain_driven_design/bounded_context_example.svg)

---
## Why Bounded Contexts Matter

- Prevent model pollution from trying to create a single universal model
- Allow teams to work independently within their context
- Each context can evolve its model without breaking others
- Map naturally to microservice boundaries

---
## Context Mapping

- Describes the relationships between `Bounded Contexts`
- Defines how contexts integrate and share data
- Makes dependencies and power dynamics explicit
- Documented in a Context Map diagram

---
## Context Map Patterns

- `Shared Kernel` - two contexts share a subset of the model
- `Customer-Supplier` - upstream context provides data, downstream consumes
- `Conformist` - downstream adopts the upstream model as-is
- `Anti-Corruption Layer` - downstream translates upstream concepts
- `Open Host Service` - context exposes a well-defined protocol
- `Published Language` - a shared format for exchanging data

---
## Context Map Diagram

![context_map_diagram](/out/mermaid/courses/architecting/modern-software-architecture/04_domain_driven_design/context_map_diagram.svg)

---
## Anti-Corruption Layer (ACL)

- A translation layer that protects a context from external model changes
- Converts external data formats into the internal domain model
- Prevents foreign concepts from leaking into the domain
- Essential when integrating with legacy systems or third-party APIs

---
## ACL Architecture

![acl_architecture](/out/mermaid/courses/architecting/modern-software-architecture/04_domain_driven_design/acl_architecture.svg)

---
## Entities

- Objects defined by their identity, not their attributes
- Have a unique identifier that persists across state changes
- Mutable: their attributes can change over time
- Examples: `User`, `Order`, `Product`, `Account`

---
## Entity Example

```python
class Order:
    def __init__(self, order_id, customer_id):
        self.order_id = order_id
        self.customer_id = customer_id
        self.items = []
        self.status = "created"

    def add_item(self, product, quantity):
        self.items.append(
            LineItem(product, quantity))

    def __eq__(self, other):
        return self.order_id == other.order_id
```

---
## Value Objects

- Objects defined by their attributes, not by identity
- Immutable: once created, they do not change
- Two value objects with the same attributes are equal
- Examples: `Money`, `Address`, `DateRange`, `Email`

---
## Value Object Example

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Money:
    amount: float
    currency: str

    def add(self, other):
        if self.currency != other.currency:
            raise ValueError("Currency mismatch")
        return Money(
            self.amount + other.amount,
            self.currency)
```

---
## Entity vs Value Object

| Aspect | Entity | Value Object |
|--------|--------|-------------|
| Identity | Has unique ID | No identity |
| Equality | By ID | By attributes |
| Mutability | Mutable | Immutable |
| Lifecycle | Tracked | Replaceable |
| Example | `Order #123` | `$49.99 USD` |

---
## Aggregates

- A cluster of related entities and value objects treated as a single unit
- Has a root entity called the `Aggregate Root`
- All external access goes through the aggregate root
- Defines a consistency boundary for transactions

---
## Aggregate Structure

![aggregate_structure](/out/mermaid/courses/architecting/modern-software-architecture/04_domain_driven_design/aggregate_structure.svg)

---
## Aggregate Design Rules

- Only the aggregate root has a global identity
- External objects can only reference the aggregate root
- Changes within the aggregate are transactionally consistent
- Keep aggregates small to reduce contention
- Reference other aggregates by ID, not by object reference

---
## Domain Services

- Operations that do not naturally belong to any entity or value object
- Stateless: they operate on domain objects but hold no state themselves
- Named using verbs from the ubiquitous language
- Example: `TransferMoney`, `CalculateShipping`, `ValidateOrder`

---
## Domain Service Example

```python
class PricingService:
    def calculate_order_total(self, order,
                              discounts):
        subtotal = sum(
            item.price * item.quantity
            for item in order.items)
        discount = discounts.apply(subtotal)
        tax = self._calculate_tax(
            subtotal - discount)
        return Money(
            subtotal - discount + tax,
            "USD")
```

---
## Application Services

- Orchestrate domain objects to fulfill use cases
- Do not contain business logic themselves
- Handle cross-cutting concerns: transactions, authorization, logging
- Act as the entry point from the outside world into the domain

---
## Application Service Example

```python
class PlaceOrderService:
    def __init__(self, order_repo,
                 pricing_service,
                 event_publisher):
        self.order_repo = order_repo
        self.pricing = pricing_service
        self.events = event_publisher

    def execute(self, command):
        order = Order(command.customer_id)
        for item in command.items:
            order.add_item(item.product,
                           item.quantity)
        self.order_repo.save(order)
        self.events.publish(
            OrderPlaced(order.order_id))
```

---
## Repositories

- Provide a collection-like interface for accessing aggregates
- Abstract the persistence mechanism from the domain
- One repository per aggregate root
- Methods: `find_by_id`, `save`, `delete`

---
## Domain Events

- Record that something significant happened in the domain
- Named in the past tense: `OrderPlaced`, `PaymentReceived`
- Immutable facts that can be published to other contexts
- Enable loose coupling between aggregates and bounded contexts

---
## Domain Event Flow

![domain_event_flow](/out/mermaid/courses/architecting/modern-software-architecture/04_domain_driven_design/domain_event_flow.svg)

---
## Mapping Domains to Microservices

- Each `Bounded Context` is a candidate for a microservice
- Not every context needs its own service; some can be combined
- Use context maps to identify integration points between services
- The ubiquitous language of each context guides the service API

---
## Decomposition Strategy

![decomposition_strategy](/out/mermaid/courses/architecting/modern-software-architecture/04_domain_driven_design/decomposition_strategy.svg)

---
## Subdomain Types

- Core Domain: the primary competitive advantage of the business
    - Invest the most effort here; build custom solutions
- Supporting Subdomain: necessary but not a differentiator
    - Can be outsourced or built with less sophistication
- Generic Subdomain: common across many businesses
    - Use off-the-shelf products (authentication, email)

---
## Event Storming

- A collaborative workshop technique for discovering domain events
- Participants include developers, domain experts, and stakeholders
- Uses sticky notes on a large wall or digital board
- Outputs: domain events, commands, aggregates, and bounded contexts

---
## Event Storming Flow

![event_storming_flow](/out/mermaid/courses/architecting/modern-software-architecture/04_domain_driven_design/event_storming_flow.svg)

---
## Common DDD Pitfalls

- Creating a single model that tries to represent everything
- Ignoring the ubiquitous language and using technical jargon
- Making aggregates too large, causing performance problems
- Skipping strategic design and jumping to tactical patterns
- Treating DDD as a technology rather than a design philosophy

---
## DDD and Microservices Alignment

- Bounded Contexts define service boundaries
- Ubiquitous Language shapes each service's API
- Context Maps reveal integration patterns between services
- Aggregates define the unit of deployment and consistency
- Domain Events become the integration mechanism between services

---
## Summary

- DDD provides a framework for modeling complex business domains
- Strategic design (Bounded Contexts, Context Maps) defines the big picture
- Tactical design (Entities, Value Objects, Aggregates) defines the internals
- The Ubiquitous Language ensures alignment between business and code
- Bounded Contexts map naturally to microservice boundaries
- Event Storming is an effective technique for domain discovery
