---
tags:
  - concepts:domain-driven-design
  - concepts:microservices
  - concepts:design-patterns
level: advanced
category: architecture
audience:
  - audiences:architects

---
# DDD With Microservices and Hexagonal Architecture

---
## DDD and Microservices

- Bounded context = service is the natural mapping
- Each service owns its model and its data
- Cross-context integration via events and APIs
- DDD provides the boundaries; microservices are the deployment

---
## Why The Match Works

- Both emphasize boundaries
- Both treat each unit as autonomous
- Both expect integration to be deliberate
- DDD without boundaries is fuzzy; microservices without DDD is arbitrary

---
## Bounded Context Per Service

- Default: one service per bounded context
- Some bounded contexts may be implemented as multiple services if scale demands
- Some small contexts may share a service if the team is small
- Use the bounded context as the starting point; adjust if needed

---
## Hexagonal Architecture

- Ports-and-adapters architecture by Alistair Cockburn
- The application core is in the center
- Ports (interfaces) define how the core talks to the outside
- Adapters implement the ports for specific technologies

---
## Why Hexagonal

- Isolates the domain from infrastructure
- Easy to swap databases, brokers, frameworks
- Domain code is testable without the infrastructure
- Aligns with DDD's "domain layer" concept

---
## The Layers (or Hexagon)

- **Domain**: aggregates, entities, value objects, domain events
- **Application**: command and query handlers, application services
- **Infrastructure**: databases, brokers, HTTP, third-party APIs
- The domain depends on nothing; everything depends on the domain

---
## Ports

- Interfaces declared in the domain or application layer
- "We need a way to save orders" → `OrderRepository` interface
- "We need to publish events" → `EventBus` interface
- The ports are the contracts; the adapters fulfill them

---
## Adapters

- Implementations of ports
- `PostgresOrderRepository` implements `OrderRepository`
- `KafkaEventBus` implements `EventBus`
- Live in the infrastructure layer; can be swapped without touching the domain

---
## Adapter Examples

- **Driving adapter**: HTTP controller that calls a command handler
- **Driven adapter**: a SQL repository that fulfills the repository port
- Driving = "calls in"; driven = "called by"
- Both are adapters; both fit the hexagon

---
## Onion Architecture

- A close cousin of hexagonal
- Concentric circles: domain at the center, infrastructure outside
- Same idea: domain depends on nothing
- Different visualization, same principle

---
## Clean Architecture

- Robert Martin's name for similar ideas
- Slightly different vocabulary (entities, use cases, controllers, gateways)
- Same direction of dependencies
- All three (hexagonal, onion, clean) are variations on a theme

---
## Why It Matters For Microservices

- Each microservice has its own hexagon
- The domain layer is shielded from HTTP and database choices
- Swapping technology per service doesn't ripple
- Testing the domain doesn't need a full stack

---
## A Service Layout

```tree
/src
  /domain         # entities, value objects, aggregates
  /application    # handlers, ports
  /infrastructure # adapters: db, http, broker
  /interfaces     # http controllers, message subscribers
```

- Dependencies point inward
- Domain has no `import` from infrastructure
- Application uses domain and ports; doesn't know adapters

---
## Cross-Service Integration

- Each service has its own ports for outgoing calls
- An adapter calls another service's API
- Anti-corruption layer maps the response into this service's terms
- The ACL is itself a port + adapter

---
## DDD Patterns That Don't Survive Service Boundaries

- Aggregate references across services — use IDs only
- Cross-aggregate transactions across services — use sagas
- Shared databases across services — never
- Each service's hexagon is sealed

---
## Microservices Anti-Patterns That DDD Catches

- Decompose by technical layer (data service, business service)
- Shared aggregates between services
- A "User Service" that owns User everywhere — should be per-context
- Services that mirror database tables 1:1

---
## When to Refactor Across Services

- If two services constantly call each other for the same data, the boundary may be wrong
- Move the boundary; merge if needed
- DDD's boundaries should match the actual coupling

---
## Bounded Contexts Within a Monolith

- Hexagonal architecture applies inside a monolith too
- Multiple bounded contexts can live in one deployable
- The boundaries are module boundaries; the discipline is the same
- Modular monolith is a valid endpoint

---
## When the Monolith Is Right

- Small team, small domain
- Operational maturity isn't there for distributed systems
- Bounded contexts are clear but not yet large enough to need separate teams
- Apply DDD inside; postpone microservices until the team and system demand it

---
## Where to Go Deeper

- The dedicated **Microservices Architecture** course covers:
    - Decomposition strategies
    - Service communication
    - Data management across services
    - Deployment, observability, scaling

---
## Summary

- Bounded context = service is the natural microservices mapping
- Hexagonal architecture isolates the domain from infrastructure
- Ports declare contracts; adapters implement them per technology
- DDD's boundaries should match microservice boundaries
- The same patterns apply in modular monoliths
