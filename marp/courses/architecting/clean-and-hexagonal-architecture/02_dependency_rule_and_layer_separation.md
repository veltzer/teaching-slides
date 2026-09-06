---
tags:
  - architecture:clean-architecture
level: intermediate
category: architecture
audience:
  - audiences:developers

---

# Dependency Rule and Layer Separation

---

## Dependency Rule

![dependency_rule](svg/courses/architecting/clean-and-hexagonal-architecture/02_dependency_rule_and_layer_separation/dependency_rule.svg)

---

## Four Layers

![four_layers](svg/courses/architecting/clean-and-hexagonal-architecture/02_dependency_rule_and_layer_separation/four_layers.svg)

---

## What This Chapter Covers

- The dependency rule, precisely
- The four layers in detail
- The "abstraction" boundary
- Inversion of control
- Compile-time vs runtime dependencies

---

## The Rule, Stated

- Outer layers depend on inner; never the reverse
- "Outer" = closer to the world (UI, DB)
- "Inner" = closer to the domain
- Dependencies point inward

---

## Four Layers

- **Entities**: enterprise-wide business rules
- **Use Cases**: application-specific business rules
- **Interface Adapters**: presenters, controllers, gateways
- **Frameworks & Drivers**: web, DB, UI

---

## Entities

- Pure business objects
- Methods that express domain rules
- No framework annotations
- No DB knowledge
- Reusable across applications

---

## Use Cases

- Application-specific behaviours
- Orchestrate entities
- Define input / output ports
- Independent of UI / DB / external services
- "PlaceOrderUseCase, RegisterUserUseCase"

---

## Interface Adapters

- Transform between use case and outer layer
- Controllers (web framework &#8594; use case)
- Presenters (use case &#8594; view model)
- Gateways (use case &#8594; DB / API)
- Glue code

---

## Frameworks And Drivers

- Spring, Express, Django
- Postgres, MongoDB
- Browser, mobile UI
- The replaceable parts

---

## Inversion Of Control

- Inner layer defines an interface
- Outer layer implements it
- Outer "plugs in" to inner
- The dependency arrow inverts at the abstraction boundary

---

## Compile-Time vs Runtime

- Compile-time: imports, types
- Runtime: actual instances passed in
- Outer module imports inner abstractions; inner doesn't import outer
- DI wires them at startup

---

## A Concrete Example

- Use case: `PlaceOrder` calls `OrderRepository.save(order)`
- `OrderRepository`: interface in the use case layer
- `PostgresOrderRepository`: implementation in adapter layer
- DI container wires them

---

## What Crosses The Boundary

- Inputs / outputs as plain data structures
- DTOs designed in the use-case layer
- Don't pass framework objects into use cases
- Don't return ORM entities from use cases

---

## Layer Boundaries In Code

- Folder structure: `domain/`, `usecases/`, `adapters/`, `infrastructure/`
- Or: separate modules / packages
- Reviewers check: no `infrastructure` import in `domain`
- Linters can enforce

---

## Tools To Enforce

- ArchUnit (Java): test layer rules
- Custom lint rules in TS / Python
- Code review discipline
- Documentation in the team's style guide

---

## Common Mistakes

- Spring annotations on entities (couples to Spring)
- Returning ORM entities from use cases
- Use cases that import HTTP request types
- "Just one little dependency" — they accumulate
- Layers that are file-system-deep but compile-time-thin
