---
tags:
  - concepts:architecture
  - concepts:design-patterns
  - concepts:resiliency
  - concepts:microservices
level: intermediate
category: architecture
audience:
  - audiences:developers
  - audiences:architects

---
# Resiliency & Cross-Cutting Patterns

---
## Pattern Index

- Resiliency: Circuit Breaker, Bulkhead, Saga, Throttling
- Integration: API Gateway, Backend for Frontend, Anti-Corruption Layer
- Modernization: Strangler Fig
- Microservice support: Database per Service, Geode
- Operational: Ambassador, Sidecar, Valet Key

---
## Circuit Breaker Overview

- Prevents cascading failures in distributed systems
- Allows graceful degradation and faster recovery
- Monitors for failures and "trips" to prevent further calls
- Provides fallback mechanisms and automatic recovery

---
## Circuit Breaker Pattern Diagram

![circuit_breaker_pattern_diagram](svg/courses/architecting/architecture-patterns/06_resiliency_and_cross_cutting_patterns/circuit_breaker_pattern_diagram.svg)

---
## Circuit Breaker Pros and Cons

Pros:
- Prevents system overload
- Improves system resilience
- Enables fast failure detection
- Allows for graceful degradation

Cons:
- Adds complexity to the system
- Requires careful configuration
- May mask underlying issues if not monitored
- Can lead to reduced functionality during outages

---
## Circuit Breaker When to Use

- In microservices architectures
- Systems with critical external dependencies
- High-traffic applications prone to failures
- When implementing fault-tolerant systems
- In scenarios requiring rapid failure detection and recovery

---
## Bulkhead Overview

- Isolates elements of an application into pools so that if one fails, the others will continue to function
- Named after the sectioned partitions (bulkheads) of a ship's hull
- Prevents cascading failures across services
- Enables fault tolerance and graceful degradation

---
## Bulkhead Pattern Diagram

![bulkhead_pattern_diagram](svg/courses/architecting/architecture-patterns/06_resiliency_and_cross_cutting_patterns/bulkhead_pattern_diagram.svg)

---
## Bulkhead Pros and Cons

Pros:
- Isolates failures, preventing system-wide cascading failures
- Improves resilience and fault tolerance
- Allows for better resource allocation and management
- Enables different scaling strategies for different components

Cons:
- Can increase system complexity
- May lead to underutilization of resources if not properly configured
- Requires careful capacity planning
- Can be challenging to implement in legacy systems

---
## Bulkhead When to Use

- In microservices architectures to isolate services
- When dealing with third-party service integrations
- In systems with varying resource requirements across components
- To protect critical services from failure in non-critical ones
- In scenarios requiring different quality-of-service levels for different operations

---
## Saga Overview

- Manages data consistency across microservices in distributed transaction scenarios
- Breaks down long-lived transactions into a sequence of local transactions
- Each local transaction updates the database and publishes an event
- Subsequent steps are triggered by these events
- Provides compensating transactions for rollback

---
## Saga Pattern Diagram

![saga_pattern_diagram](svg/courses/architecting/architecture-patterns/06_resiliency_and_cross_cutting_patterns/saga_pattern_diagram.svg)

---
## Saga Pros and Cons

Pros:
- Maintains data consistency across services
- Supports long-lived transactions
- Improves system resilience
- Allows for complex failure recovery

Cons:
- Increases complexity in business logic
- Requires careful design of compensating actions
- Can be challenging to debug and test
- May introduce eventual consistency

---
## Saga When to Use

- In microservices architectures with distributed transactions
- When dealing with long-lived, multi-step business processes
- In systems requiring complex failure recovery mechanisms
- When strong consistency is not immediately required
- In scenarios where traditional two-phase commit is not feasible

---
## Throttling Overview

- Controls the rate at which requests are processed or resources are consumed
- Prevents system overload and ensures fair resource allocation
- Can be applied at various levels: user, service, or system-wide
- Implements strategies like fixed window, sliding window, or token bucket algorithms
- Helps maintain system stability and responsiveness under high load

---
## Throttling Pattern Diagram

![throttling_pattern_diagram](svg/courses/architecting/architecture-patterns/06_resiliency_and_cross_cutting_patterns/throttling_pattern_diagram.svg)

---
## Throttling Pros and Cons

Pros:
- Prevents system overload and improves stability
- Ensures fair resource allocation among clients
- Protects against certain types of DoS attacks
- Can prioritize critical operations under high load
- Helps in capacity planning and resource management

Cons:
- May degrade user experience if not carefully implemented
- Can be complex to configure and fine-tune
- Might introduce additional latency
- Can be challenging to implement in distributed systems
- May require additional infrastructure for rate limiting

---
## Throttling When to Use

- In public-facing APIs to prevent abuse
- When dealing with limited backend resources
- In systems with varying levels of service (e.g., free vs. premium tiers)
- To protect dependent services from cascading failures
- When implementing fair use policies
- In scenarios where certain clients might monopolize resources
- To manage traffic spikes and ensure system stability

---
## API Gateway Overview

- Acts as a single entry point for all client requests
- Routes requests to appropriate microservices
- Aggregates responses from multiple services
- Handles cross-cutting concerns (authentication, logging, SSL termination)
- Can perform protocol translation and API composition

---
## API Gateway Pattern Diagram

![api_gateway_pattern_diagram](svg/courses/architecting/architecture-patterns/06_resiliency_and_cross_cutting_patterns/api_gateway_pattern_diagram.svg)

---
## API Gateway Pros and Cons

Pros:
- Centralizes cross-cutting concerns
- Simplifies client-side code
- Enables microservice refactoring without affecting clients
- Can improve security and performance
- Allows for API composition and transformation

Cons:
- Can become a single point of failure
- May introduce additional latency
- Can become a development bottleneck
- Requires careful management to avoid becoming too complex
- May require significant infrastructure investment

---
## API Gateway When to Use

- In microservices architectures to provide a unified entry point
- When clients need to access multiple services in a single request
- To shield internal system architecture from external clients
- When implementing consistent security policies across APIs
- To handle differences between client protocols and internal services
- For gradually migrating from a monolith to microservices

---
## Backend for Frontend (BFF) Overview

- Creates separate backend services for specific frontend applications or interfaces
- Tailors the API to the needs of each client type (e.g., mobile, web, desktop)
- Optimizes data transfer and aggregation for each client
- Improves performance and user experience
- Simplifies client-side logic by moving complexity to the BFF layer

---
## BFF Pattern Diagram

![backend_for_frontend_bff_pattern_diagram](svg/courses/architecting/architecture-patterns/06_resiliency_and_cross_cutting_patterns/backend_for_frontend_bff_pattern_diagram.svg)

---
## BFF Pros and Cons

Pros:
- Optimizes API for each client type
- Improves performance by reducing data transfer
- Simplifies client-side code
- Allows independent evolution of client-specific APIs
- Can handle client-specific authentication and authorization

Cons:
- Increases overall system complexity
- Can lead to code duplication across BFFs
- Requires additional development and maintenance effort
- May result in inconsistencies between different client experiences
- Can become a bottleneck if not properly designed

---
## BFF When to Use

- When supporting multiple client types with different needs (e.g., web, mobile, IoT)
- In microservices architectures to aggregate data from multiple services
- When optimizing for mobile performance is crucial
- To simplify complex client-side logic in large applications
- When different clients require different data shapes or operations

---
## Anti-Corruption Layer (ACL) Overview

- Acts as a facade between different subsystems or models
- Translates requests between incompatible domain models
- Protects the integrity of a new or refactored system from legacy influences
- Facilitates integration between systems with different semantics
- Enables gradual migration from legacy to new systems
- Originated from Domain-Driven Design principles

---
## ACL Pattern Diagram

![anti_corruption_layer_pattern_diagram](svg/courses/architecting/architecture-patterns/06_resiliency_and_cross_cutting_patterns/anti_corruption_layer_pattern_diagram.svg)

---
## ACL Pros and Cons

Pros:
- Isolates and protects the new system from legacy complexities
- Facilitates incremental migration and modernization
- Improves maintainability by centralizing integration logic
- Allows for independent evolution of connected systems
- Reduces the risk of corrupting the new system's domain model

Cons:
- Adds an extra layer of complexity to the overall architecture
- Can introduce performance overhead due to additional translations
- Requires effort to design, implement, and maintain the translation layer
- May become a bottleneck if not properly designed and scaled
- Can be challenging to keep in sync with changes in connected systems

---
## ACL When to Use

- During large-scale system modernization or migration projects
- When integrating systems with fundamentally different domain models
- In scenarios where a new system must coexist with legacy systems
- To protect a well-designed domain model from external influence
- When gradually replacing a legacy system over time
- In situations where direct translation between two models is complex or undesirable
- To facilitate communication between bounded contexts in a microservices architecture

---
## Strangler Fig Overview

- Gradual migration strategy for rewriting or replacing legacy systems
- Incrementally creates a new system around the edges of the old
- Lets you migrate functionality piece by piece
- Named after strangler fig vines that grow around and replace their host trees
- Allows for coexistence of old and new systems during transition

---
## Strangler Fig Pattern Diagram

![strangler_fig_pattern_diagram](svg/courses/architecting/architecture-patterns/06_resiliency_and_cross_cutting_patterns/strangler_fig_pattern_diagram.svg)

---
## Strangler Fig Pros and Cons

Pros:
- Reduces risk of big-bang rewrite
- Allows for incremental migration and value delivery
- Enables easier rollback if issues arise
- Provides opportunity to learn and adjust during migration

Cons:
- Can be slower than a full rewrite
- Requires careful planning and coordination
- May introduce temporary complexity during transition
- Can be challenging to maintain consistency between old and new systems

---
## Strangler Fig When to Use

- When migrating large, mission-critical legacy systems
- In scenarios where a big-bang rewrite is too risky
- When needing to deliver value incrementally during system modernization
- In situations requiring minimal disruption to existing services
- When the existing system is too large or complex for a single, complete rewrite

---
## Database per Service Overview

- Each microservice has its own private database
- Ensures loose coupling between services
- Allows each service to choose the most appropriate database type
- Prevents services from accessing each other's data directly
- Supports the autonomy and independence of microservices
- Facilitates independent scaling and deployment of services

---
## Database per Service Pattern Diagram

![database_per_service_pattern_diagram](svg/courses/architecting/architecture-patterns/06_resiliency_and_cross_cutting_patterns/database_per_service_pattern_diagram.svg)

---
## Database per Service Pros and Cons

Pros:
- Supports service autonomy and independent deployment
- Allows for choosing the best database type for each service
- Improves scalability and performance through focused optimization
- Enhances data security by isolating data access
- Facilitates easier schema changes and database upgrades

Cons:
- Increases complexity in data management and consistency
- Can lead to data duplication across services
- Makes it challenging to perform queries across multiple services
- May increase infrastructure and operational costs
- Requires careful handling of distributed transactions

---
## Database per Service When to Use

- In microservices architectures to ensure service independence
- When different services have distinct data storage requirements
- To support independent scaling of services and their data stores
- In scenarios where data isolation and security are critical
- When evolving from a monolithic to a microservices architecture
- To enable independent development and deployment of services
- In systems where services need to be loosely coupled
- When different teams are responsible for different services and their data

---
## Geode Overview

- Deploys a subset of application's services into satellite locations
- Brings services closer to end users to reduce latency
- Replicates data to local caches in each geode
- Improves performance and availability for distributed applications
- Helps comply with data sovereignty and regulations
- Allows for local processing while maintaining global consistency

---
## Geode Pattern Diagram

![geode_pattern_diagram](svg/courses/architecting/architecture-patterns/06_resiliency_and_cross_cutting_patterns/geode_pattern_diagram.svg)

---
## Geode Pros and Cons

Pros:
- Reduces latency for geographically distributed users
- Improves application responsiveness and user experience
- Enables better scalability and load distribution
- Facilitates compliance with data residency requirements
- Enhances fault tolerance and availability

Cons:
- Increases overall system complexity
- Can be challenging to maintain data consistency across geodes
- Requires careful management of data replication and synchronization
- May increase operational costs due to distributed infrastructure
- Can complicate deployment and versioning processes

---
## Geode When to Use

- For globally distributed applications with users across different regions
- When low latency is critical for application performance
- To comply with data sovereignty and local regulatory requirements
- In scenarios where you need to process data locally while maintaining global consistency
- For applications that benefit from bringing compute closer to the data and users
- When you need to improve availability and fault tolerance across geographic regions
- In large-scale systems where global deployment is necessary but challenging

---
## Ambassador Overview

- Provides a proxy service for connecting to external services or resources
- Offloads common client connectivity tasks from the main application
- Acts as a single point of contact for managing service dependencies
- Can handle network request retries, monitoring, logging, and security
- Simplifies the main application by abstracting connection complexities

---
## Ambassador Pattern Diagram

![ambassador_pattern_diagram](svg/courses/architecting/architecture-patterns/06_resiliency_and_cross_cutting_patterns/ambassador_pattern_diagram.svg)

---
## Ambassador Pros and Cons

Pros:
- Simplifies client application by offloading connectivity concerns
- Provides a consistent interface to diverse external services
- Improves application resilience through built-in retry and circuit breaking
- Enables easier updates to service communication without changing the main application
- Facilitates implementation of cross-cutting concerns like logging and monitoring

Cons:
- Adds an extra network hop, potentially increasing latency
- Increases overall system complexity
- Can become a single point of failure if not properly managed
- May require additional resources and maintenance
- Can complicate local development and testing scenarios

---
## Ambassador When to Use

- In microservices architectures to manage inter-service communication
- When connecting to external services with complex protocols or authentication
- To implement retry logic and circuit breaking for improved resilience
- In polyglot environments where services are written in different languages
- To standardize and simplify access to a variety of backend services
- When you need to add features like logging or monitoring without modifying the main application
- In scenarios where you want to shield the main application from the complexities of service discovery

---
## Sidecar Overview

- Deploys components of an application as a separate process or container
- Attaches and co-locates the sidecar with a parent application
- Extends and enhances the functionality of the main application
- Provides a way to access features or services in a language-agnostic way
- Common uses include logging, monitoring, security, and network services

---
## Sidecar Pattern Diagram

![sidecar_pattern_diagram](svg/courses/architecting/architecture-patterns/06_resiliency_and_cross_cutting_patterns/sidecar_pattern_diagram.svg)

---
## Sidecar Pros and Cons

Pros:
- Separation of concerns between core functionality and peripheral tasks
- Language-agnostic way to extend application capabilities
- Easier to develop, test, and maintain components independently
- Allows for standardization of cross-cutting concerns across different services
- Enables updating or replacing the sidecar without modifying the main application

Cons:
- Increases overall system complexity
- Can introduce additional resource overhead
- Potential latency in communication between application and sidecar
- May complicate deployment and orchestration processes
- Can lead to version compatibility issues between application and sidecar

---
## Sidecar When to Use

- In microservices architectures to handle cross-cutting concerns
- When you need to add features to an application without modifying its code
- For implementing service mesh functionalities (e.g., service discovery, load balancing)
- To standardize monitoring, logging, or security across diverse applications
- When you want to offload peripheral tasks from the main application
- In polyglot environments where services are written in different languages
- To extend the functionality of legacy applications without modifying them

---
## Valet Key Overview

- Provides clients with restricted direct access to a specific resource
- Uses a token or key with limited privileges and validity period
- Offloads data transfer from the application to a separate data store
- Improves scalability by reducing load on the main application server
- Enhances security by limiting the scope and duration of access
- Often used for operations like uploads/downloads in cloud storage

---
## Valet Key Pattern Diagram

![valet_key_pattern_diagram](svg/courses/architecting/architecture-patterns/06_resiliency_and_cross_cutting_patterns/valet_key_pattern_diagram.svg)

---
## Valet Key Pros and Cons

Pros:
- Reduces load on application servers
- Improves performance for large data transfers
- Enhances security through limited-scope access
- Simplifies client-side implementation for resource access
- Allows fine-grained control over resource permissions

Cons:
- Increases complexity in managing and securing access tokens
- Requires careful implementation to prevent token misuse
- May need additional infrastructure for token generation/validation
- Can be challenging to revoke access before token expiration
- Might not be suitable for frequently changing or sensitive data

---
## Valet Key When to Use

- In cloud-based applications for managing access to storage services
- When handling large file uploads or downloads
- To offload data transfer operations from application servers
- In scenarios requiring temporary, limited access to resources
- For improving scalability in systems with heavy resource access
- When implementing fine-grained access control to shared resources
- In multi-tenant systems to securely manage resource access across tenants

---
## Summary

- Resiliency: Circuit Breaker stops cascades, Bulkhead isolates pools, Saga gives distributed transactions, Throttling enforces rate limits
- Integration: API Gateway is one front door for many services, BFF tailors per client, ACL translates between models
- Modernization: Strangler Fig replaces legacy systems incrementally
- Microservice support: Database per Service enforces autonomy, Geode brings services close to users
- Operational: Ambassador proxies outbound calls, Sidecar adds cross-cutting concerns out-of-process, Valet Key delegates direct resource access via short-lived tokens
- These patterns are usually combined — a typical microservices system uses many at once
