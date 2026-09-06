---
tags:
  - concepts:architecture
  - concepts:design-patterns
  - concepts:microservices
level: intermediate
category: architecture
audience:
  - audiences:developers
  - audiences:architects

---

# System Architectures

---

## Monolithic Overview

- Combines all the functionality of an application into a single, unified codebase
- The application is deployed as a single, self-contained unit
- All components of the application run within the same process or container
- Communication between components is done through method invocations or function calls
- Suitable for small to medium-sized applications with a limited set of functionalities

---

## Monolithic Architecture Key Concepts

- Monolithic Codebase
    - All the code for the application is contained in a single codebase
    - The codebase includes the user interface, business logic, and data access layers
    - The components are tightly coupled and share the same dependencies
- Unified Deployment
    - The entire application is deployed as a single unit
    - Any changes to the application require redeploying the entire monolith
    - Scaling is achieved by running multiple instances of the monolith
- Shared Database
    - The application typically relies on a single, shared database
    - All components access the same database schema and tables
    - Data consistency and transactions are managed within the monolith

---

## Monolithic Architecture Diagram

![monolithic_architecture_diagram](svg/courses/architecting/architecture-patterns/03_system_architectures/monolithic_architecture_diagram.svg)

---

## Monolithic Architecture Pros and Cons

Pros:
- Simple development and deployment process
- Easier to understand and maintain for small to medium-sized applications
- Enables rapid development and iteration in the early stages of a project
- Provides good performance due to the tight coupling and shared memory space
- Simplifies testing and debugging as all components are within the same codebase

Cons:
- Becomes complex and difficult to maintain as the application grows in size and complexity
- Tight coupling between components makes it harder to modify or replace individual parts
- Scaling the application can be challenging as the entire monolith needs to be scaled
- Limited flexibility in terms of technology choices and independent deployment of components
- A single bug or failure can bring down the entire application

---

## Monolithic Architecture When to Use

- When building small to medium-sized applications with a limited set of functionalities
- When the application has a well-defined and stable domain model
- When rapid development and iteration are more important than long-term maintainability
- When the team is small and has a good understanding of the entire codebase
- When the application is not expected to scale significantly or require frequent updates
- When simplicity and ease of development are prioritized over flexibility and scalability

---

## Modular Monolith Overview

- Combines the simplicity of a monolithic architecture with the modularity of microservices
- Organizes the application into loosely coupled, independently deployable modules
- Modules encapsulate related functionality and have well-defined interfaces
- Modules can be developed, tested, and deployed separately
- Provides a balance between the simplicity of a monolith and the flexibility of microservices

---

## Modular Monolith Key Concepts

- Modules
    - Logical units of functionality within the monolith
    - Encapsulate related features, domain concepts, or business capabilities
    - Have well-defined interfaces and boundaries
    - Can be developed, tested, and maintained independently
- Module Interfaces
    - Define the contracts and communication channels between modules
    - Specify the input and output data structures and operations
    - Ensure loose coupling and encapsulation of module internals
- Shared Database
    - Modules typically share a single database
    - Each module owns a subset of the database tables or schemas
    - Modules access the database through well-defined data access layers
- Deployment
    - The entire application is still deployed as a single unit
    - Modules can be independently deployable if desired
    - Deployment can be automated and optimized for the modular structure

---

## Modular Monolith Architecture Diagram

![modular_monolith_architecture_diagram](svg/courses/architecting/architecture-patterns/03_system_architectures/modular_monolith_architecture_diagram.svg)

---

## Modular Monolith Pros and Cons

Pros:
- Provides a modular structure while maintaining the simplicity of a monolith
- Enables independent development, testing, and maintenance of modules
- Allows for incremental adoption and refactoring of legacy monoliths
- Reduces the complexity and overhead compared to microservices
- Simplifies deployment and operations compared to distributed systems

Cons:
- Modules are still tightly coupled within the monolith
- Limited scalability compared to microservices
- Shared database can become a bottleneck and cause tight coupling
- Requires discipline and governance to maintain module boundaries
- May not provide the same level of isolation and autonomy as microservices

---

## Modular Monolith When to Use

- When migrating from a monolithic architecture to a more modular structure
- When the application has a moderate level of complexity and size
- When independent development and maintenance of modules are desired
- When the benefits of microservices are not justified due to the added complexity
- When a balance between simplicity and modularity is needed
- When incremental adoption and refactoring of legacy systems are required

---

## Microservices Overview

- Structures an application as a collection of small, independent services
- Each service implements a specific business capability or functionality
- Services are loosely coupled and communicate via lightweight protocols (e.g., HTTP/REST)
- Enables developing, deploying, and scaling services independently

---

## Microservices Key Principles

- Single Responsibility Principle
    - Each service focuses on a single business capability or function
- Loose Coupling
    - Services are independent and can be developed, deployed, and scaled separately
- Encapsulation
    - Services hide their internal details and expose functionality through well-defined interfaces
- Autonomy
    - Services have control over their own data and can make decisions independently
- Resilience
    - Services are designed to handle failures gracefully and recover independently

---

## Microservices Architecture Diagram

![microservices_architecture_diagram](svg/courses/architecting/architecture-patterns/03_system_architectures/microservices_architecture_diagram.svg)

---

## Microservices Pros and Cons

Pros:
- Enables independent development, deployment, and scaling of services
- Supports technology diversity and using the right tool for the job
- Facilitates incremental adoption and migration from monolithic applications
- Improves fault isolation and resilience

Cons:
- Increases complexity in terms of distributed systems and service orchestration
- Requires careful design to avoid tight coupling and maintain data consistency
- Can lead to increased overhead in terms of communication and data serialization
- Debugging and tracing can be more challenging in a distributed environment

---

## Microservices When to Use

- When the application has a large and complex domain that can be decomposed into smaller, independent services
- When different parts of the application have different scalability, performance, or availability requirements
- When the application needs to support multiple platforms, devices, or user interfaces
- When the organization has multiple teams that can develop, deploy, and maintain services independently
- When incremental adoption and migration from a monolithic application is desired

---

## SOA Overview

- Structures an application as a collection of services that provide business functionality
- Services are loosely coupled, autonomous, and expose well-defined interfaces
- Services can be discovered, composed, and reused to create business processes
- Enables integration and interoperability between heterogeneous systems

---

## Service-Oriented Architecture Key Principles

- Service Contract
    - Services define a formal contract that specifies their interfaces, operations, and data models
- Loose Coupling
    - Services are independent and can be developed, deployed, and maintained separately
- Service Abstraction
    - Services hide their internal details and expose functionality through abstract interfaces
- Service Reusability
    - Services are designed to be reusable across multiple business processes and applications
- Service Composability
    - Services can be composed and orchestrated to create higher-level business processes
- Service Autonomy
    - Services have control over their own logic and resources

---

## Service-Oriented Architecture Diagram

![service_oriented_architecture_diagram](svg/courses/architecting/architecture-patterns/03_system_architectures/service_oriented_architecture_diagram.svg)

---

## Service-Oriented Architecture Pros and Cons

Pros:
- Enables integration and interoperability between heterogeneous systems
- Supports reuse of business functionality across multiple applications
- Facilitates loose coupling and independence of services
- Allows for flexible composition and orchestration of services
- Enables incremental adoption and migration from legacy systems

Cons:
- Requires significant upfront design and modeling of service contracts
- Can lead to increased complexity in terms of service governance and management
- May introduce performance overhead due to message serialization and transport
- Debugging and tracing can be challenging in a distributed service environment
- Requires a mature infrastructure and tooling for service discovery, composition, and monitoring

---

## Service-Oriented Architecture When to Use

- When the application needs to integrate and interoperate with multiple heterogeneous systems
- When the business functionality can be decomposed into reusable and composable services
- When loose coupling and independence of services are important for flexibility and maintainability
- When incremental adoption and migration from legacy systems is desired
- When a mature infrastructure and tooling for service management and governance are available

---

## EDA Overview

- Structures an application around the production, detection, and consumption of events
- Components are loosely coupled and interact through asynchronous event notifications
- Events represent significant changes in state or actions that have occurred
- Enables building reactive, real-time, and highly scalable systems

---

## Event-Driven Architecture Key Concepts

- Event
    - An occurrence or a state change that is significant for the system
    - Can be triggered by user actions, system state changes, or external stimuli
- Event Producer
    - A component that generates or publishes events to an event channel or broker
- Event Consumer
    - A component that subscribes to and consumes events from an event channel or broker
- Event Channel
    - A communication channel or broker that facilitates the exchange of events between producers and consumers
- Event Processing
    - The logic that is executed in response to receiving an event, such as updating state or triggering actions

---

## Event-Driven Architecture Diagram

![event_driven_architecture_diagram](svg/courses/architecting/architecture-patterns/03_system_architectures/event_driven_architecture_diagram.svg)

---

## Event-Driven Architecture Pros and Cons

Pros:
- Enables loose coupling and asynchronous communication between components
- Supports building reactive and real-time systems that can respond to events
- Facilitates scalability and flexibility, as producers and consumers can be added or removed independently
- Allows for event-driven workflows and complex event processing
- Enables integration with external systems and services through event-based interfaces

Cons:
- Can introduce complexity in terms of event management, routing, and consistency
- Requires careful design to ensure reliable event delivery and processing
- Debugging and tracing event flows can be challenging in a distributed system
- May require additional infrastructure and tooling for event storage, monitoring, and replay
- Can lead to increased latency and eventual consistency challenges

---

## Event-Driven Architecture When to Use

- When the application needs to react to real-time events and state changes
- When loose coupling and asynchronous communication between components are desired
- When the system needs to scale and handle high volumes of events and traffic
- When complex event processing and event-driven workflows are required
- When integration with external systems and services through event-based interfaces is necessary

---

## Serverless Overview

- Builds applications as a collection of small, independent, and stateless functions
- Functions are event-driven and executed in ephemeral containers managed by a platform
- Eliminates the need for server management and infrastructure provisioning
- Provides automatic scaling, high availability, and pay-per-use pricing model
- Enables rapid development, deployment, and iteration of application components

---

## Serverless Key Concepts

- Function
    - A small, independent unit of code that performs a specific task
    - Stateless and executed in response to events or triggers
    - Can be written in various programming languages supported by the platform
- Event
    - A trigger that causes the execution of a function
    - Can be HTTP requests, database changes, file uploads, scheduled jobs, etc.
- Serverless Platform
    - A cloud computing service that manages the execution environment for functions
    - Handles scaling, provisioning, and resource allocation automatically
    - Examples include AWS Lambda, Azure Functions, Google Cloud Functions
- API Gateway
    - An entry point for client requests to access serverless functions
    - Provides routing, authentication, throttling, and request/response transformation
- Stateless
    - Functions do not maintain persistent state between invocations
    - State is typically stored in external services like databases or object storage

---

## Serverless Architecture Diagram

![serverless_architecture_diagram](svg/courses/architecting/architecture-patterns/03_system_architectures/serverless_architecture_diagram.svg)

---

## Serverless Pros and Cons

Pros:
- Eliminates server management and infrastructure concerns
- Provides automatic scaling based on incoming requests or events
- Offers pay-per-use pricing, reducing costs for infrequently used functions
- Enables rapid development and deployment of small, focused functions
- Supports event-driven architectures and asynchronous processing

Cons:
- Limited control over the execution environment and performance
- Cold starts can introduce latency for infrequently invoked functions
- Vendor lock-in and dependency on the serverless platform
- Debugging and testing can be more challenging in a distributed environment
- May not be suitable for long-running or stateful processes

---

## Serverless When to Use

- When building event-driven and reactive applications
- When the application has unpredictable or highly variable workloads
- When rapid development and deployment of small, focused functions are desired
- When server management and infrastructure provisioning should be avoided
- When pay-per-use pricing and automatic scaling are beneficial
- When integrating with various cloud services and APIs

---

## Space-Based Overview

- Designed for highly scalable and distributed applications
- Focuses on data replication and partitioning across multiple nodes
- Supports high read and write throughput and low latency
- Utilizes in-memory data grids and distributed caching
- Enables linear scalability and fault tolerance

---

## Space-Based Key Concepts

- Processing Unit
    - A self-contained unit of deployment and scaling
    - Contains the application components and necessary resources
    - Can be replicated and distributed across multiple nodes
- In-Memory Data Grid
    - A distributed cache that stores data in memory across multiple nodes
    - Provides fast read and write access to data
    - Supports data replication and partitioning for scalability and fault tolerance
- Messaging Grid
    - A distributed messaging system for communication between processing units
    - Enables asynchronous and decoupled communication
    - Supports publish-subscribe and point-to-point messaging patterns
- Data Virtualization
    - Abstracts the physical location and distribution of data
    - Provides a unified view of data across multiple nodes and data sources
    - Enables transparent data access and querying

---

## Space-Based Architecture Diagram

![space_based_architecture_diagram](svg/courses/architecting/architecture-patterns/03_system_architectures/space_based_architecture_diagram.svg)

---

## Space-Based Pros and Cons

Pros:
- Enables high scalability and performance through data replication and partitioning
- Supports low latency and high throughput for read and write operations
- Provides fault tolerance and resilience through distributed processing units
- Enables linear scalability by adding more processing units and nodes
- Supports real-time data processing and analytics

Cons:
- Increases complexity in terms of data consistency and synchronization
- Requires careful design and configuration of data partitioning and replication
- May introduce overhead in terms of memory usage and network communication
- Requires specialized skills and knowledge for development and operations
- May not be suitable for applications with strong consistency requirements

---

## Space-Based When to Use

- When building highly scalable and distributed applications
- When low latency and high throughput are critical requirements
- When the application needs to handle a large volume of concurrent users and requests
- When real-time data processing and analytics are required
- When the application needs to be resilient and fault-tolerant
- When linear scalability is desired by adding more nodes and processing units

---

## Share-Nothing Overview

- Consists of independent nodes that do not share any resources (e.g., memory, storage)
- Each node is self-sufficient and operates independently
- Nodes communicate with each other through message passing or APIs
- Provides high scalability, fault tolerance, and performance
- Commonly used in distributed systems and big data processing

---

## Share-Nothing Key Concepts

- Independent Nodes
    - Each node operates independently and has its own resources (e.g., CPU, memory, storage)
    - Nodes do not share any resources directly with other nodes
    - Each node is responsible for its own data and processing
- Message Passing
    - Nodes communicate with each other through message passing or APIs
    - Messages are sent over a network to exchange data or coordinate tasks
    - Message passing enables loose coupling between nodes
- Distributed Data
    - Data is partitioned and distributed across the nodes
    - Each node manages its own subset of the data
    - Data distribution can be based on sharding, replication, or a combination of both
- Parallel Processing
    - Tasks are divided and processed in parallel across the nodes
    - Each node performs its assigned tasks independently
    - Results from individual nodes are aggregated to produce the final output

---

## Share-Nothing Architecture Diagram

![share_nothing_architecture_diagram](svg/courses/architecting/architecture-patterns/03_system_architectures/share_nothing_architecture_diagram.svg)

---

## Share-Nothing Pros and Cons

Pros:
- High scalability by adding more nodes to the system
- Improved performance through parallel processing and distributed data
- Fault tolerance and resilience as failures are isolated to individual nodes
- Flexibility in terms of technology choices and independent node upgrades
- Enables handling large volumes of data and processing-intensive tasks

Cons:
- Increased complexity in terms of system design and coordination between nodes
- Requires careful data partitioning and distribution strategies
- Message passing and network communication can introduce latency and overhead
- Difficult to maintain data consistency and handle distributed transactions
- Debugging and troubleshooting can be challenging in a distributed environment

---

## Share-Nothing When to Use

- When building large-scale, data-intensive applications that require high scalability
- When the system needs to handle a high volume of concurrent users or requests
- When the data and processing can be partitioned and distributed across multiple nodes
- When fault tolerance and resilience are critical requirements
- When the system benefits from parallel processing and distributed computing
- When flexibility and independent scaling of nodes are desired

---

## Summary

- Monolith and Modular Monolith are the simplest deployment shapes
- Microservices and SOA decompose the system into independently deployable services at different granularities
- EDA shifts the integration model from request-response to events
- Serverless removes server-management responsibility from the team
- Space-Based and Share-Nothing scale horizontally by partitioning state across nodes
- The right system architecture depends on team size, deployment cadence, and scale requirements
