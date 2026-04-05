# Microservices Design Patterns

<!-- Add Mermaid.js support -->
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
<script>
  mermaid.initialize({ startOnLoad: true });
</script>

---
## Why Design Patterns?

- Microservices introduce new categories of distributed problems
- Patterns provide proven solutions to recurring challenges
- They create a shared vocabulary across teams
- Choosing the right patterns prevents costly mistakes

---
## Pattern Categories

<div class="mermaid">
graph TD
    P[Microservices Patterns]
    P --> R[Routing Patterns]
    P --> D[Data Patterns]
    P --> C[Communication Patterns]
    P --> T[Transaction Patterns]
    R --> AG[API Gateway]
    R --> BFF[Backend for Frontend]
    R --> SD[Service Discovery]
    D --> DPS[Database per Service]
    D --> CQRS2[CQRS]
    D --> ES[Event Sourcing]
    T --> SG[Saga]
</div>

---
## API Gateway Pattern

- A single entry point for all client requests
- Routes requests to the appropriate backend service
- Handles cross-cutting concerns: authentication, rate limiting, logging
- Simplifies the client by hiding the service topology

---
## API Gateway Architecture

<div class="mermaid">
graph TD
    C1[Web App] --> GW[API Gateway]
    C2[Mobile App] --> GW
    C3[Third Party] --> GW
    GW --> S1[User Service]
    GW --> S2[Order Service]
    GW --> S3[Product Service]
    GW --> S4[Payment Service]
</div>

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

<div class="mermaid">
graph TD
    WEB[Web Application] --> BFF_W[Web BFF]
    MOB[Mobile Application] --> BFF_M[Mobile BFF]
    IOT[IoT Device] --> BFF_I[IoT BFF]
    BFF_W --> S1[User Service]
    BFF_W --> S2[Order Service]
    BFF_M --> S1
    BFF_M --> S3[Notification Service]
    BFF_I --> S4[Telemetry Service]
</div>

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

<div class="mermaid">
sequenceDiagram
    participant Client
    participant Registry
    participant Service A
    participant Service B
    Client->>Registry: Query for Service X
    Registry-->>Client: [Service A:8080, Service B:8081]
    Client->>Service A: Direct request
</div>

- Client queries the service registry directly
- Client performs load balancing
- Examples: `Netflix Eureka` with `Ribbon`

---
## Server-Side Service Discovery

<div class="mermaid">
sequenceDiagram
    participant Client
    participant Load Balancer
    participant Registry
    participant Service
    Client->>Load Balancer: Request for Service X
    Load Balancer->>Registry: Lookup Service X
    Registry-->>Load Balancer: [instances]
    Load Balancer->>Service: Forward request
    Service-->>Load Balancer: Response
    Load Balancer-->>Client: Response
</div>

- Load balancer queries the registry
- Client does not need to know about discovery
- Examples: `AWS ALB`, `Kubernetes Services`

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

<div class="mermaid">
graph TD
    S1[Order Service] --> DB1[(Orders DB - PostgreSQL)]
    S2[Product Service] --> DB2[(Products DB - MongoDB)]
    S3[Analytics Service] --> DB3[(Analytics DB - ClickHouse)]
    S1 -->|API Call| S2
    S1 -->|Event| S3
</div>

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

<div class="mermaid">
sequenceDiagram
    participant Order
    participant Payment
    participant Inventory
    participant Shipping
    Order->>Order: Create Order
    Order->>Payment: OrderCreated
    Payment->>Payment: Process Payment
    Payment->>Inventory: PaymentCompleted
    Inventory->>Inventory: Reserve Stock
    Inventory->>Shipping: StockReserved
    Shipping->>Shipping: Schedule Delivery
</div>

---
## Saga: Orchestration

<div class="mermaid">
sequenceDiagram
    participant Orchestrator
    participant Order
    participant Payment
    participant Inventory
    Orchestrator->>Order: Create Order
    Order-->>Orchestrator: Order Created
    Orchestrator->>Payment: Process Payment
    Payment-->>Orchestrator: Payment OK
    Orchestrator->>Inventory: Reserve Stock
    Inventory-->>Orchestrator: Stock Reserved
</div>

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

<div class="mermaid">
graph LR
    A[Create Order] -->|Success| B[Process Payment]
    B -->|Success| C[Reserve Stock]
    C -->|FAILURE| D[Refund Payment]
    D --> E[Cancel Order]
</div>

---
## CQRS Pattern

- `Command Query Responsibility Segregation`
- Separates the read model from the write model
- Commands change state; queries read state
- Each side can be optimized independently

---
## CQRS Architecture

<div class="mermaid">
graph TD
    C[Client] -->|Commands| CS[Command Service]
    C -->|Queries| QS[Query Service]
    CS --> WDB[(Write Database)]
    WDB -->|Sync/Events| RDB[(Read Database)]
    QS --> RDB
</div>

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

<div class="mermaid">
sequenceDiagram
    participant Client
    participant Service
    participant Event Store
    Client->>Service: Place Order
    Service->>Event Store: Append OrderCreated
    Client->>Service: Add Item
    Service->>Event Store: Append ItemAdded
    Client->>Service: Get Order
    Service->>Event Store: Read Events
    Event Store-->>Service: [OrderCreated, ItemAdded]
    Service->>Service: Replay to build state
    Service-->>Client: Current Order State
</div>

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

<div class="mermaid">
graph TD
    CMD[Command] --> CH[Command Handler]
    CH --> ES[(Event Store)]
    ES -->|Publish Events| EP[Event Projector]
    EP --> RM[(Read Model DB)]
    Q[Query] --> QH[Query Handler]
    QH --> RM
</div>

---
## Strangler Fig Pattern

- A migration strategy for incrementally replacing a monolith
- New functionality is built as microservices alongside the monolith
- A routing layer gradually redirects traffic from old to new
- The monolith shrinks over time until it can be decommissioned

---
## Strangler Fig Diagram

<div class="mermaid">
graph TD
    R[Router / Proxy] --> M[Monolith]
    R --> S1[New Service A]
    R --> S2[New Service B]
    M -.->|Migrate Feature C| S3[Future Service C]
    style M fill:#ffcccc
    style S1 fill:#ccffcc
    style S2 fill:#ccffcc
</div>

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
