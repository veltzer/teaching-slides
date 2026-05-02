---
tags:
  - concepts:microservices
  - practices:ddd
level: intermediate
category: architecture
audience:
  - audiences:architects

---
# Service Boundaries and Bounded Contexts

---
## Bounded Context

- A boundary within which a particular domain model applies
- Inside the boundary: one set of terms, one model, one consistency
- Outside the boundary: different terms, different model
- The unit of "this is one service's responsibility"

---
## Why Bounded Contexts

- Without them, every concept ends up "global" — `User` means everything to everyone
- With them, `User` means one specific thing in this context
- Different contexts can have different fields, different rules for the same name
- Translation happens at the boundary (anti-corruption layer)

---
## Drawing Boundaries

![boundary_choices](svg/courses/architecting/microservices-architecture/04_boundaries/boundary_choices.svg)

---
## A Concrete Example

- In Sales context: `Customer` has order history, lifetime value
- In Shipping context: `Customer` has delivery addresses, signature requirements
- In Billing context: `Customer` has payment methods, credit limit
- Three different `Customer`s; three different services

---
## Ubiquitous Language

- Each bounded context has its own vocabulary
- Inside a context: domain experts and developers speak the same language
- Across contexts: translate at the boundary
- Code, conversations, documentation all use the context's language

---
## Context Mapping

- Document how bounded contexts relate
- Customer-Supplier: one context's output is another's input
- Conformist: one context adopts another's model wholesale
- Anti-Corruption Layer: one context translates the other's model
- Shared Kernel: two contexts share a small common model

---
## Identifying Boundaries

- Talk to domain experts; they often have the boundaries in their language
- Look for terms that mean different things in different conversations
- Look for "we don't really care about that here" moments
- Boundaries follow conceptual clarity, not technical preference

---
## Strategic vs Tactical Design

- Strategic: identify bounded contexts, their relationships, the big picture
- Tactical: aggregates, entities, value objects, domain events within a context
- Strategic design comes first; tactical comes second
- Tactical is where most engineers start; strategic is what architects own

---
## Bounded Context = Service?

- Often yes — a bounded context becomes a microservice
- Sometimes no — multiple bounded contexts can fit in one service if they share a team
- Sometimes one bounded context is multiple services (rare; usually a smell)
- Use the bounded context as the default service boundary

---
## Anti-Corruption Layer

- A translator at the boundary between bounded contexts
- Maps incoming concepts to your context's language
- Prevents another context's vocabulary from polluting yours
- Often a thin module per integration

---
## Aggregates

- Within a service, group entities that must stay consistent
- The aggregate root is the entry point
- Commands target aggregates; aggregates produce events
- Each aggregate is a small consistency boundary

---
## Aggregates and Service Boundaries

- An aggregate lives entirely within one service
- A transaction covers one aggregate
- Multi-aggregate workflows use sagas (separate course)
- Cross-service workflows are coordinated, not transactional

---
## Domain Events

- A meaningful business fact, in the past tense
- "OrderPlaced", "ShipmentDelivered"
- Aggregates emit events when their state changes
- Other services can subscribe and react

---
## Integration Events vs Domain Events

- Domain event: internal to a bounded context — fine-grained
- Integration event: published across context boundaries — coarse-grained
- The integration event is a public contract; the domain event is private
- Usually a small subset of domain events become integration events

---
## When Boundaries Are Wrong

- Lots of cross-service synchronous calls
- A single change touches many services
- Stuck workflows because one service is down
- These all suggest the boundary is in the wrong place

---
## Refactoring Boundaries

- Hard but possible
- Move a capability from service A to service B by extracting first, then deleting from A
- Or: merge two services that should have been one
- Plan for this; the first cut is rarely final

---
## Summary

- Bounded contexts are the conceptual unit
- A service usually = a bounded context
- Each context has its own vocabulary, model, consistency
- Translate at the boundary (ACL)
- Refactor boundaries as understanding grows
