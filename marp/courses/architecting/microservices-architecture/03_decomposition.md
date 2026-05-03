---
tags:
  - concepts:microservices
  - concepts:design-patterns
level: intermediate
category: architecture
audience:
  - audiences:architects

---
# Decomposition Strategies

---
## The Question

- Given a domain (existing or planned), how do you split it into services?
- Wrong split: services that constantly need to coordinate
- Right split: services that mostly stand alone
- This is the hardest microservices design problem

---
## Decomposition Strategies

![decomposition_strategies](svg/courses/architecting/microservices-architecture/03_decomposition/decomposition_strategies.svg)

---
## Strategy Choice Visualised

![strategy_choice](svg/courses/architecting/microservices-architecture/03_decomposition/strategy_choice.svg)

---
## Decompose by Business Capability

- Identify the business activities the system supports
- Each major capability becomes a service (or a small group)
- Examples: Order Management, Inventory, Billing, Notifications
- The names match how the business talks about itself

---
## Decompose by Subdomain

- DDD term for a conceptually distinct part of the domain
- Sales is a subdomain; Shipping is a subdomain; Reporting is a subdomain
- Each subdomain has its own model and language
- Subdomain ≈ bounded context (chapter 4)

---
## Decompose by Use Case

- Each major user-facing flow becomes a service
- "Place an order", "Cancel an order", "View inventory"
- Useful for early-stage decomposition; converges to capability-based later
- Risks: too many tiny services if every screen becomes one

---
## Don't Decompose by Layer

- "API service, business service, data service" is a distributed monolith
- Every change touches all three
- Latency is high; coupling is total
- The split should be vertical (by capability), not horizontal (by layer)

---
## Don't Decompose by Verb

- "Validation service", "Calculation service", "Notification service"
- These are technical concerns, not business capabilities
- Tend to become dumping grounds
- Verbs become methods within capability services

---
## Decompose by Data Ownership

- Identify the entities in the domain
- Group related entities that change together
- The owning service controls all writes to that group
- Reads can flow through APIs or denormalized projections

---
## A Working Example: E-Commerce

- Catalog: products, categories, search
- Cart: shopping cart contents
- Order: order placement and lifecycle
- Inventory: stock levels and reservations
- Payment: charges, refunds, methods
- Shipping: addresses, carriers, tracking
- Customer: profiles, addresses, preferences

---
## Granularity

- Too coarse: services that look like mini-monoliths
- Too fine: nano-services that constantly call each other
- Right size: a small team can own it; it has a clear capability
- Two pizzas team is a useful heuristic for ownership

---
## Cohesion vs Coupling

- High cohesion within a service: related things together
- Low coupling between services: minimal cross-service calls
- Hard goal: maximize one, minimize the other
- A bad decomposition makes both worse

---
## The Test: Independent Change

- Can a feature change be implemented in one service?
- If most changes touch multiple services, the boundaries are wrong
- Track this metric: average services touched per pull request
- Above 1.5: decomposition has issues

---
## The Test: Independent Failure

- If service X is down, what stops working?
- The answer should be a clear subset of the system
- If "everything stops" — services are too coupled
- Critical paths should depend on as few services as possible

---
## Evolutionary Architecture

- The first decomposition is rarely right
- Boundaries shift as the domain is better understood
- Plan for refactoring service boundaries
- Don't aim for perfect; aim for evolvable

---
## Anti-Patterns

- Decompose to match the database schema (one service per table)
- Decompose to match the team's skill silos ("Ruby team", "Go team")
- Decompose to match the deploy schedule ("daily release service")
- Decompose by who owns the existing code

---
## Summary

- Decompose by business capability or subdomain
- Vertical splits (by capability) beat horizontal (by layer)
- Right size = a team can own it end-to-end
- Test by independent change and independent failure
- Plan to refactor boundaries as understanding grows
