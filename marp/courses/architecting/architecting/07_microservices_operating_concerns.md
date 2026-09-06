---
tags:
  - concepts:architecture
  - concepts:microservices
  - concepts:design-patterns
level: advanced
category: architecture
audience:
  - audiences:developers
  - audiences:architects

---

# Microservices Operating Concerns

---

## Scope of This Chapter

- This chapter assumes you know the named patterns from the Architecture Patterns course
- API Gateway, BFF, Saga, Strangler Fig, Database per Service — definitions live there
- Here we focus on what those patterns demand at runtime
- Distributed transactions, service discovery, load balancing, anti-patterns
- CQRS and Event Sourcing definitions live in the Architecture Patterns course (ch 04); their event-streaming operating concerns are covered in ch 19 of this course

---

## Pattern Categories

![pattern_categories](svg/courses/architecting/architecting/07_microservices_operating_concerns/pattern_categories.svg)

---

## API Gateway in Practice

- Routing rules that survive service refactoring
- Authentication and rate limiting consolidated in one place
- Cross-cutting concerns belong here, not in every service
- The gateway becomes a critical operational component

---

## API Gateway Responsibilities

- Request routing and load balancing
- Authentication and authorization
- Rate limiting and quota enforcement
- Request and response transformation
- Logging, metrics, and tracing
- SSL termination

---

## Popular API Gateway Tools

- `Kong` - open source gateway built on `Nginx`
- `AWS API Gateway` - managed service tightly integrated with `Lambda`
- `Envoy` - service proxy used heavily in service meshes
- `Traefik` - dynamic gateway with native `Kubernetes` support

---

## BFF vs Single API Gateway

| Aspect | Single Gateway | BFF |
|--------|---------------|-----|
| Clients | All clients | One per client type |
| Ownership | Platform team | Frontend teams |
| API shape | Generic | Client-specific |
| Complexity | Lower initially | Higher but more maintainable |
| Coupling | Clients adapt to API | API adapts to clients |

---

## Service Discovery

- The mechanism by which services find each other's network locations
- Necessary because service instances are dynamic in cloud environments
- Instances scale up, scale down, and move across hosts
- Without discovery, services would need hardcoded addresses

---

## Client-Side Service Discovery

![client_side_service_discovery](svg/courses/architecting/architecting/07_microservices_operating_concerns/client_side_service_discovery.svg)

---

## Client-Side Discovery Details

- Client queries the service registry directly
- Client performs load balancing
- Examples: `Netflix Eureka` with `Ribbon`
- Trade-off: more logic in every client; one fewer hop on the data path

---

## Server-Side Service Discovery

![server_side_service_discovery](svg/courses/architecting/architecting/07_microservices_operating_concerns/server_side_service_discovery.svg)

---

## Server-Side Discovery Details

- Load balancer queries the registry
- Client does not need to know about discovery
- Examples: `AWS ALB`, `Kubernetes Services`
- Trade-off: extra network hop; clients stay simple

---

## Service Registry Tools

- `Consul` - service discovery with health checking and KV store
- `etcd` - distributed key-value store used by `Kubernetes`
- `ZooKeeper` - coordination service for distributed systems
- `Kubernetes DNS` - built-in service discovery via DNS names

---

## Load Balancing Strategies

- Round Robin: distribute requests evenly across instances
- Least Connections: send to the instance with fewest active connections
- Weighted: assign different weights based on instance capacity
- IP Hash: route based on client IP for session affinity
- Random: simple random selection among healthy instances

---

## Database per Service in Practice

- Each microservice owns its private database
- No direct database access between services
- Services communicate through APIs or events, not shared tables
- Enables independent schema evolution and technology choices

---

## Database per Service Trade-Offs

- Pros:
    - Loose coupling between services
    - Independent scaling of databases
    - Freedom to choose the best database technology per service
    - Schema changes do not affect other services
- Cons:
    - Cross-service queries are complex
    - Maintaining data consistency is harder
    - More databases to operate and monitor

---

## Shared Database Anti-Pattern

- Multiple services access the same database
- Changes to the schema require coordinating multiple teams
- Creates tight coupling that defeats the purpose of microservices
- Acceptable only as a transitional step during migration from monolith

---

## Distributed Transactions Problem

- A single business operation may span multiple services
- Traditional `ACID` transactions do not work across service boundaries
- Two-Phase Commit (`2PC`) is slow and reduces availability
- The Saga pattern provides an alternative approach

---

## Saga in Practice

- A sequence of local transactions across multiple services
- Each service performs its transaction and publishes an event
- If one step fails, compensating transactions undo previous steps
- Two coordination approaches: choreography and orchestration

---

## Saga: Choreography

![saga_choreography](svg/courses/architecting/architecting/07_microservices_operating_concerns/saga_choreography.svg)

---

## Saga: Orchestration

![saga_orchestration](svg/courses/architecting/architecting/07_microservices_operating_concerns/saga_orchestration.svg)

---

## Choreography vs Orchestration

| Aspect | Choreography | Orchestration |
|--------|-------------|---------------|
| Coupling | Loosely coupled | Central coordinator |
| Visibility | Hard to trace flow | Clear workflow |
| Complexity | Distributed logic | Centralized logic |
| Scalability | Better | Coordinator is bottleneck |
| Use case | Simple workflows | Complex business processes |

---

## Compensating Transactions

- The "undo" mechanism for saga steps that succeeded before a failure
- Each step defines a compensating action (e.g., refund payment, release stock)
- Compensations must be idempotent
- Not all actions can be perfectly undone (e.g., sending an email)

---

## Compensation Example

![compensation_example](svg/courses/architecting/architecting/07_microservices_operating_concerns/compensation_example.svg)

---

## Strangler Fig in Practice

- A migration strategy for incrementally replacing a monolith
- New functionality is built as microservices alongside the monolith
- A routing layer gradually redirects traffic from old to new
- The monolith shrinks over time until it can be decommissioned

---

## Strangler Fig Diagram

![strangler_fig_diagram](svg/courses/architecting/architecting/07_microservices_operating_concerns/strangler_fig_diagram.svg)

---

## Summary

- API Gateway and BFF concentrate cross-cutting concerns where they belong
- Service Discovery and load balancing keep dynamic environments routable
- Database per Service trades easy joins for service autonomy
- Distributed transactions are not free — Saga makes them tractable through compensation
- Strangler Fig is the safest path out of a monolith
- CQRS and Event Sourcing operating concerns are covered in ch 19 (Event Streaming)
