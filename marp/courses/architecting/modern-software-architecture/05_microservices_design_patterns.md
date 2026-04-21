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
# Microservices Design Patterns

---
## Why Design Patterns?

- Microservices introduce new categories of distributed problems
- Patterns provide proven solutions to recurring challenges
- They create a shared vocabulary across teams
- Choosing the right patterns prevents costly mistakes

---
## Pattern Categories

![pattern_categories](svg/courses/architecting/modern-software-architecture/05_microservices_design_patterns/pattern_categories.svg)

---
## API Gateway Pattern

- A single entry point for all client requests
- Routes requests to the appropriate backend service
- Handles cross-cutting concerns: authentication, rate limiting, logging
- Simplifies the client by hiding the service topology

---
## API Gateway Architecture

![api_gateway_architecture](svg/courses/architecting/modern-software-architecture/05_microservices_design_patterns/api_gateway_architecture.svg)

---
## API Gateway Flow

![api_gateway_pattern](svg/courses/architecting/modern-software-architecture/05_microservices_design_patterns/api_gateway_pattern.svg)

---
## API Gateway Responsibilities

- Request routing and load balancing
- Authentication and authorization
- Rate limiting and throttling
- Request and response transformation
- Caching of common responses
- SSL termination

---
## API Gateway Pros and Cons

- Pros:
    - Single entry point simplifies client code
    - Centralizes cross-cutting concerns
    - Decouples clients from service topology changes
    - Enables monitoring and analytics at the edge
- Cons:
    - Can become a single point of failure
    - Adds latency for every request
    - Risk of becoming a "god" component with too much logic

---
## Popular API Gateway Tools

- `Kong` - open-source, plugin-based, built on `Nginx`
- `AWS API Gateway` - managed service with Lambda integration
- `Envoy` - high-performance proxy used in service meshes
- `Traefik` - cloud-native reverse proxy with auto-discovery
- `NGINX` - widely used as both gateway and load balancer

---
## Backend for Frontend (BFF) Pattern

- A dedicated API gateway for each type of client
- Each BFF tailors its API to the specific needs of its frontend
- Avoids one-size-fits-all APIs that serve no client well
- Each frontend team owns its corresponding BFF

---
## BFF Architecture

![bff_architecture](svg/courses/architecting/modern-software-architecture/05_microservices_design_patterns/bff_architecture.svg)

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

![client_side_service_discovery](svg/courses/architecting/modern-software-architecture/05_microservices_design_patterns/client_side_service_discovery.svg)

---
## Client-Side Discovery Details

- Client queries the service registry directly
- Client performs load balancing
- Examples: `Netflix Eureka` with `Ribbon`

---
## Client-Side Service Discovery Diagram

![client_side_service_discovery](svg/courses/architecting/modern-software-architecture/05_microservices_design_patterns/client_side_service_discovery.svg)

---
## Server-Side Discovery Details

- Load balancer queries the registry
- Client does not need to know about discovery
- Examples: `AWS ALB`, `Kubernetes Services`

---
## Server-Side Service Discovery Diagram

![server_side_service_discovery](svg/courses/architecting/modern-software-architecture/05_microservices_design_patterns/server_side_service_discovery.svg)

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
## Database per Service Pattern

- Each microservice owns its private database
- No direct database access between services
- Services communicate through APIs or events, not shared tables
- Enables independent schema evolution and technology choices

---
## Database per Service Diagram

![database_per_service_diagram](svg/courses/architecting/modern-software-architecture/05_microservices_design_patterns/database_per_service_diagram.svg)

---
## Database per Service Pros and Cons

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
## The Saga Pattern

- A sequence of local transactions across multiple services
- Each service performs its transaction and publishes an event
- If one step fails, compensating transactions undo previous steps
- Two coordination approaches: choreography and orchestration

---
## Saga: Choreography

![saga_choreography](svg/courses/architecting/modern-software-architecture/05_microservices_design_patterns/saga_choreography.svg)

---
## Saga: Orchestration

![saga_orchestration](svg/courses/architecting/modern-software-architecture/05_microservices_design_patterns/saga_orchestration.svg)

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

![compensation_example](svg/courses/architecting/modern-software-architecture/05_microservices_design_patterns/compensation_example.svg)

---
## CQRS Pattern

- `Command Query Responsibility Segregation`
- Separates the read model from the write model
- Commands change state; queries read state
- Each side can be optimized independently

---
## CQRS Architecture

![cqrs_architecture](svg/courses/architecting/modern-software-architecture/05_microservices_design_patterns/cqrs_architecture.svg)

---
## CQRS Benefits

- Read and write models can use different data stores
- Read side can be denormalized for fast queries
- Write side can enforce complex business rules
- Each side scales independently based on load
- Enables event sourcing on the write side

---
## When to Use CQRS

- Read and write workloads have very different characteristics
- Complex domain logic that benefits from separate models
- High read-to-write ratio where reads need optimization
- When combined with event sourcing for audit trails
- Not suitable for simple `CRUD` applications

---
## Event Sourcing

- Store state as a sequence of events rather than current state
- The current state is derived by replaying all events
- Events are immutable and append-only
- Provides a complete audit trail and history of changes

---
## Event Sourcing Flow

![event_sourcing_flow](svg/courses/architecting/modern-software-architecture/05_microservices_design_patterns/event_sourcing_flow.svg)

---
## Event Store Example

| Sequence | Event Type | Data |
|----------|-----------|------|
| 1 | `OrderCreated` | `{orderId: 123, customer: "Alice"}` |
| 2 | `ItemAdded` | `{orderId: 123, product: "Widget", qty: 2}` |
| 3 | `ItemAdded` | `{orderId: 123, product: "Gadget", qty: 1}` |
| 4 | `OrderConfirmed` | `{orderId: 123, total: 149.97}` |

---
## Event Sourcing Pros and Cons

- Pros:
    - Complete audit trail of every change
    - Can reconstruct state at any point in time
    - Natural fit with CQRS and event-driven architecture
    - Enables temporal queries and debugging
- Cons:
    - Event schema evolution is challenging
    - Replaying events can be slow for long-lived aggregates
    - Increased storage requirements
    - Higher complexity for developers unfamiliar with the pattern

---
## CQRS + Event Sourcing Combined

![cqrs_event_sourcing_combined](svg/courses/architecting/modern-software-architecture/05_microservices_design_patterns/cqrs_event_sourcing_combined.svg)

---
## Strangler Fig Pattern

- A migration strategy for incrementally replacing a monolith
- New functionality is built as microservices alongside the monolith
- A routing layer gradually redirects traffic from old to new
- The monolith shrinks over time until it can be decommissioned

---
## Strangler Fig Diagram

![strangler_fig_diagram](svg/courses/architecting/modern-software-architecture/05_microservices_design_patterns/strangler_fig_diagram.svg)

---
## Summary

- The `API Gateway` centralizes routing and cross-cutting concerns
- `BFF` provides client-specific APIs for different frontends
- `Service Discovery` enables dynamic location of service instances
- `Database per Service` ensures loose coupling at the data layer
- The `Saga` pattern manages distributed transactions through compensation
- `CQRS` separates read and write models for independent optimization
- `Event Sourcing` stores state as an immutable sequence of events
- The `Strangler Fig` pattern enables safe migration from monoliths
