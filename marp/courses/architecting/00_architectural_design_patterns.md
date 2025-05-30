# Client-Server Pattern
---
## Overview

- Separates the system into two applications:
    - Client: Requests services, can be "thin" or "thick"
    - Server: Provides services, often manages resources
- Client and server have different lifecycles but communicate via requests/responses
---
## Component Roles

- Client
    - Initiates requests to the server
    - Waits for and receives server responses
    - Usually interacts directly with end users
- Server
    - Listens for client requests
    - Processes requests and sends responses back
    - May validate requests and authorize access
    - Often manages shared resources
---
## Communication Diagram

![0](../../../out/mermaid/marp/courses/architecting/XX_architectural_design_patterns.md/0.png)

---

## Pros and Cons

Pros:
- Centralized control and management of resources
- Supports many clients with different capabilities
- Easy to add new clients without changing the server
- Clients and servers can evolve independently

Cons:
- Server can be a single point of failure
- Potential performance bottlenecks at the server
- Limited offline capability for thin clients
- Security and scalability can be challenging

---

## When to Use

- Resources need to be centrally managed
- Many clients need to access the same data or services
- Clients may have different capabilities or technical stacks
- System must support changing client-side platforms
- Processing can be offloaded from clients to server

---
## Broker Pattern

- A broker component coordinates communication between clients and servers
- Clients request services from the broker, not directly from servers
- Servers register their services with the broker and wait for requests
- Broker decouples clients from servers and provides additional services

---

## Broker Component Roles

- Broker
    - Maintains a registry of available services and their locations
    - Receives client requests and forwards them to appropriate servers
    - May provide additional services like logging, security, or transaction management
- Client
    - Requests services from the broker using a common interface
    - Does not need to know the location or implementation details of servers
- Server
    - Registers its services with the broker
    - Receives requests from the broker and sends responses back
    - Does not interact directly with clients

---

## Broker Interaction Diagram

![1](../../../out/mermaid/marp/courses/architecting/XX_architectural_design_patterns.md/1.png)

---
## Broker Pros and Cons

Pros:
- Decouples clients from servers
- Enables location transparency and platform independence
- Supports dynamic registration and discovery of services
- Can provide additional services and optimizations

Cons:
- Broker can become a performance bottleneck or single point of failure
- Added complexity from the broker component and interactions
- Potential latency overhead from indirection through broker
- Clients and servers must agree on a common broker interface

---

## Broker When to Use

- Clients need to access multiple services in a uniform way
- Services need to be decoupled from clients for flexibility
- Dynamic registration and discovery of services is required
- Additional services like logging or security need to be centralized
- Platform and language independence between clients and servers is desired

---

## Peer-to-Peer Pattern

- Distributes tasks or workloads between equally privileged participants (peers)
- Peers are both consumers and suppliers of resources
- Peers can act as clients, servers, or both
- Decentralized model without the need for central coordination
---
## Peer-to-Peer Roles

- Peer
    - Participates in the network both as a consumer and supplier of resources
    - Can act as a client by requesting services from other peers
    - Can act as a server by providing services to other peers
    - May have different capabilities or responsibilities
- Connection
    - Logical link between two peers that enables communication
    - Can be direct or indirect (e.g., through other peers)
    - Can be persistent or created on-demand

---

## Peer-to-Peer Diagram

![2](../../../out/mermaid/marp/courses/architecting/XX_architectural_design_patterns.md/2.png)

---
## Peer-to-Peer Pros and Cons

Pros:
- Eliminates the need for central servers or authorities
- Can increase robustness and availability through redundancy
- Enables collaborative resource sharing and aggregation
- Supports scalability by distributing load among peers

Cons:
- Complexity of peer discovery and communication
- Potential security and trust issues between peers
- Performance can be unpredictable and depends on peer capabilities
- Harder to ensure data consistency and integrity across peers

---

## Peer-to-Peer When to Use

- Resources are distributed among multiple participants
- Centralized control or single points of failure need to be avoided
- Collaborative resource sharing or aggregation is desired
- Scalability and load balancing can be achieved through peer distribution
- Participants are willing to contribute resources as well as consume them
---
## Event Bus Pattern

- Components communicate through a central event dispatcher (bus)
- Publishers send events to the bus without knowing the subscribers
- Subscribers register interest in specific events and are notified by the bus
- Decouples publishers from subscribers and enables event-driven architecture
---
## Event Bus Roles

- Event Bus
    - Central communication channel for events
    - Receives events from publishers and dispatches them to subscribers
    - Can provide additional services like event filtering, transformation, or persistence
- Publisher
    - Sends events to the event bus
    - Does not need to know or depend on the subscribers
    - Can publish different types of events
- Subscriber
    - Registers interest in specific events with the event bus
    - Receives and handles events dispatched by the bus
    - Can subscribe to different types of events

---

## Event Bus Interaction Diagram

![3](../../../out/mermaid/marp/courses/architecting/XX_architectural_design_patterns.md/3.png)

---

## Event Bus Pros and Cons

Pros:
- Decouples publishers from subscribers
- Enables event-driven and reactive architectures
- Supports dynamic and flexible event routing
- Can scale publishers and subscribers independently

Cons:
- Introduces additional complexity and potential performance overhead
- Event bus can become a bottleneck or single point of failure
- Subscribers need to carefully handle event ordering and duplicates
- Debugging and tracing event flows can be challenging

---

## Event Bus When to Use

- Publishers need to broadcast events without knowing the subscribers
- Subscribers need to dynamically register interest in specific events
- Event-driven communication and reactive processing are required
- Flexibility and extensibility in event routing and handling are desired
- Loose coupling and independent scalability of components are important

---
## Microservices Pattern

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

![4](../../../out/mermaid/marp/courses/architecting/XX_architectural_design_patterns.md/4.png)

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
## Service-Oriented Architecture (SOA) Pattern

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

![5](../../../out/mermaid/marp/courses/architecting/XX_architectural_design_patterns.md/5.png)

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
## Event-Driven Architecture (EDA) Pattern

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

![6](../../../out/mermaid/marp/courses/architecting/XX_architectural_design_patterns.md/6.png)

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
## Domain-Driven Design (DDD) Pattern

- An approach to software development that focuses on modeling the business domain
- Emphasizes collaboration between domain experts and developers to create a shared understanding
- Aims to align the software design with the business domain and its terminology
- Provides a set of principles and practices for building complex, domain-centric applications

---

## DDD Key Concepts

- Bounded Context
    - A specific responsibility with explicit boundaries within the domain model
    - Defines the context in which a model applies and the boundaries of its applicability
- Ubiquitous Language
    - A common language used by domain experts and developers to discuss and model the domain
    - Ensures a shared understanding and consistency between the business and the software
- Entity
    - An object with a unique identity that remains constant throughout its lifecycle
    - Represents a domain concept that is defined by its identity rather than its attributes
- Value Object
    - An immutable object that represents a descriptive aspect of the domain with no identity
    - Defined by its attributes and can be freely shared and replaced
- Aggregate
    - A cluster of related entities and value objects that are treated as a single unit
    - Defines a consistency boundary and enforces invariants within the aggregate

---

## DDD Architecture Diagram

![7](../../../out/mermaid/marp/courses/architecting/XX_architectural_design_patterns.md/7.png)

---
## DDD Pros and Cons

Pros:
- Aligns the software design with the business domain and its language
- Promotes a shared understanding between domain experts and developers
- Encourages modular and maintainable design based on domain concepts
- Facilitates the creation of expressive and rich domain models
- Supports the evolution of the domain model as the business requirements change

Cons:
- Requires a significant investment in domain modeling and collaboration with domain experts
- Can lead to increased complexity and learning curve for developers
- May introduce overhead in terms of mapping between domain models and persistence models
- Requires a deep understanding of DDD principles and practices
- May not be suitable for simple or CRUD-based applications

---

## DDD When to Use

- When building complex, domain-centric applications with rich business logic
- When the business domain is complex and requires a deep understanding and modeling
- When collaboration between domain experts and developers is critical for success
- When the application needs to be maintainable, extensible, and aligned with the business domain
- When the domain model is expected to evolve over time based on changing business requirements

---
## Command Query Responsibility Segregation (CQRS) Pattern

- Separates the read and write operations of an application into separate models
- Commands (write operations) modify the state of the system but do not return data
- Queries (read operations) return data but do not modify the state of the system
- Allows optimizing read and write operations independently based on their specific requirements
- Often used in combination with Event Sourcing for maintaining the write model

---

## CQRS Key Concepts

- Command
    - An operation that modifies the state of the system
    - Represents a request to perform an action or a change
    - Typically follows the Command pattern and encapsulates the action and its parameters
- Query
    - An operation that retrieves data from the system
    - Represents a request for information without modifying the state
    - Often uses a simplified read model optimized for querying
- Command Model
    - Represents the write model of the system
    - Responsible for handling commands and modifying the state
    - Focused on the behavior and the business rules of the system
- Query Model
    - Represents the read model of the system
    - Responsible for handling queries and returning data
    - Optimized for querying and presentation purposes
- Event Sourcing
    - A complementary pattern often used with CQRS
    - Persists the state changes as a sequence of events
    - Allows reconstructing the current state by replaying the events

---

## CQRS Architecture Diagram

![8](../../../out/mermaid/marp/courses/architecting/XX_architectural_design_patterns.md/8.png)

---

## CQRS Pros and Cons

Pros:
- Allows optimizing read and write operations independently
- Supports scalability and performance by separating concerns
- Enables using different data models for reads and writes
- Facilitates implementing complex querying and reporting requirements
- Can improve system maintainability and evolution over time

Cons:
- Introduces complexity in terms of maintaining multiple models
- Requires careful consideration of eventual consistency and synchronization
- May lead to increased development and maintenance efforts
- Requires additional infrastructure and tooling for event sourcing and synchronization
- Can be overkill for simple CRUD-based applications

---

## CQRS When to Use

- When the application has different scalability and performance requirements for reads and writes
- When the read and write models have different data representations and querying needs
- When the application requires complex querying, reporting, or data analysis capabilities
- When the system needs to handle high write volumes and eventual consistency is acceptable
- When using Event Sourcing to maintain the write model and reconstruct the state

---
## Event Sourcing Pattern

- Persists the state of a system as a sequence of events
- Events represent the changes that have occurred in the system over time
- The current state can be reconstructed by replaying the events in order
- Provides a complete audit trail and enables temporal queries and debugging
- Often used in combination with CQRS for separating read and write models

---

## Event Sourcing Key Concepts

- Event
    - Represents a significant change or action that has occurred in the system
    - Contains the relevant data associated with the change
    - Immutable and stored in chronological order
- Event Store
    - A storage mechanism optimized for storing and retrieving events
    - Provides an append-only log of events
    - Supports efficient retrieval of events based on criteria such as time or aggregate ID
- Aggregate
    - A domain object or entity that encapsulates state and behavior
    - Represents a consistency boundary and maintains invariants
    - Reconstructed by replaying the events associated with its ID
- Projection
    - A derived view or representation of the system state
    - Created by processing the events and applying the changes to a read model
    - Can be optimized for querying and presentation purposes
---

## Event Sourcing Architecture Diagram

![9](../../../out/mermaid/marp/courses/architecting/XX_architectural_design_patterns.md/9.png)

---
## Event Sourcing Pros and Cons

Pros:
- Provides a complete audit trail and history of changes
- Enables temporal queries and debugging by replaying events
- Supports flexible querying and reporting by creating projections
- Facilitates implementing undo/redo functionality and state reconstruction
- Can improve scalability and performance when combined with CQRS

Cons:
- Introduces complexity in terms of event modeling and handling
- Requires careful consideration of event schema evolution and versioning
- May lead to increased storage requirements for storing events
- Requires additional processing to reconstruct the current state from events
- Can be challenging to implement queries that span multiple aggregates
---
## Event Sourcing When to Use

- When a complete audit trail and history of changes are required
- When temporal queries and debugging are important for the system
- When the ability to rebuild the state from events is valuable
- When flexible querying and reporting requirements exist
- When using CQRS to separate read and write models and optimize performance
- When the domain involves complex business rules and state transitions
---
## Serverless Architecture Pattern

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

![10](../../../out/mermaid/marp/courses/architecting/XX_architectural_design_patterns.md/10.png)

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
## Space-Based Architecture Pattern

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

![11](../../../out/mermaid/marp/courses/architecting/XX_architectural_design_patterns.md/11.png)

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
## Hexagonal Architecture (Ports and Adapters) Pattern

- Also known as the Ports and Adapters pattern
- Focuses on creating loosely coupled application components
- Separates the core business logic from external dependencies
- Defines ports (interfaces) for interaction with the outside world
- Uses adapters to connect the ports to specific technologies or services
- Promotes testability, maintainability, and flexibility
---

## Hexagonal Architecture Key Concepts

- Domain
    - Represents the core business logic and rules of the application
    - Independent of external dependencies and technologies
    - Contains the domain model, services, and use cases
- Ports
    - Interfaces that define the communication contracts between the domain and the outside world
    - Divided into two types: inbound ports (API) and outbound ports (SPI)
    - Inbound ports handle requests from the outside and delegate to the domain
    - Outbound ports define the dependencies and services required by the domain
- Adapters
    - Implementations that connect the ports to specific technologies or services
    - Adapt the external dependencies to the interfaces defined by the ports
    - Can be swapped or replaced without modifying the domain
- Dependency Inversion
    - The domain depends on abstractions (ports) rather than concrete implementations
    - Allows the domain to remain independent and decoupled from external dependencies

---

## Hexagonal Architecture Diagram

![12](../../../out/mermaid/marp/courses/architecting/XX_architectural_design_patterns.md/12.png)

---
## Hexagonal Architecture Pros and Cons

Pros:
- Promotes loose coupling and separation of concerns
- Improves testability by isolating the domain from external dependencies
- Enhances maintainability and flexibility by allowing easy replacement of adapters
- Enables parallel development of the domain and adapters
- Supports evolutionary architecture and incremental development

Cons:
- Introduces additional complexity and indirection
- Requires upfront design and definition of ports and adapters
- May lead to increased development effort and code duplication
- Can be overkill for simple or small-scale applications
- Requires discipline and consistency in following the pattern

---

## Hexagonal Architecture When to Use

- When building complex applications with multiple external dependencies
- When the domain logic needs to be independent and decoupled from infrastructure concerns
- When testability and maintainability are critical requirements
- When the application needs to support multiple user interfaces or delivery mechanisms
- When the application is expected to evolve and adapt to changing requirements
- When a modular and loosely coupled architecture is desired

---
## Clean Architecture Pattern

- Promotes separation of concerns and dependency inversion
- Divides the system into concentric layers with clear boundaries
- Inner layers contain the core business logic and domain entities
- Outer layers handle infrastructure, frameworks, and external dependencies
- Dependencies point inward, with inner layers being independent of outer layers
- Emphasizes maintainability, testability, and flexibility

---
## Clean Architecture Key Concepts

- Entities
    - Represent the core business objects and rules
    - Encapsulate the most general and high-level rules of the system
    - Should be independent of any external framework or infrastructure
- Use Cases
    - Contain the application-specific business rules and logic
    - Orchestrate the flow of data to and from the entities
    - Should not be affected by changes in external layers
- Interface Adapters
    - Convert data from the format most convenient for the use cases and entities to the format most convenient for the external layers
    - Include presenters, views, and controllers
    - Adapt the data to the needs of the specific framework or protocol
- Frameworks and Drivers
    - Represent the outermost layer of the system
    - Include frameworks, databases, UI, and other external dependencies
    - Should be easily replaceable without affecting the inner layers

---

## Architecture Diagram

![13](../../../out/mermaid/marp/courses/architecting/XX_architectural_design_patterns.md/13.png)

---
## Pros and Cons

Pros:
- Promotes separation of concerns and modularity
- Enhances testability by isolating the core logic from external dependencies
- Improves maintainability by reducing the impact of changes in outer layers
- Supports flexibility and interchangeability of frameworks and drivers
- Enables parallel development of different layers

Cons:
- Can introduce additional complexity and abstraction layers
- Requires strict adherence to the dependency rule and architecture boundaries
- May lead to increased development effort and code duplication
- Can be overkill for small or simple applications
- Requires a good understanding of the principles and patterns involved
---
## When to Use

- When building large and complex applications with multiple external dependencies
- When the core business logic needs to be independent and protected from changes in external layers
- When testability and maintainability are critical concerns
- When the application needs to support multiple user interfaces or delivery mechanisms
- When the system is expected to evolve and adapt to changing requirements over time
- When a clear separation of responsibilities and concerns is desired
---
## Onion Architecture Pattern

- Organizes the application into concentric layers
- Innermost layer contains the domain model and core business logic
- Outer layers depend on inner layers but not vice versa
- Promotes separation of concerns and dependency inversion
- Aims to make the application more maintainable, testable, and adaptable
---
## Onion Architecture Key Concepts

- Domain Model
    - Represents the core business entities, rules, and logic
    - Located at the center of the architecture
    - Independent of any external dependencies or frameworks
- Domain Services
    - Implement the use cases and business logic that operate on the domain model
    - Depend only on the domain model and other domain services
- Application Services
    - Coordinate the interaction between the domain layer and the external layers
    - Depend on the domain model and domain services
    - Adapt the data from the domain to the needs of the outer layers
- Infrastructure
    - Contains the implementations of external dependencies and frameworks
    - Includes databases, UI frameworks, web services, etc.
    - Depends on the application services and adapts to their interfaces
---
## Onion Architecture Diagram

![14](../../../out/mermaid/marp/courses/architecting/XX_architectural_design_patterns.md/14.png)

---
## Onion Architecture Pros and Cons

Pros:
- Promotes a clear separation of concerns and modularity
- Enables the domain model to be independent of external dependencies
- Makes the application more testable by isolating the core logic
- Allows for easier maintenance and evolution of the system
- Supports the substitution of external frameworks and technologies

Cons:
- Can introduce additional layers of abstraction and complexity
- Requires a good understanding of the principles and patterns involved
- May lead to increased development effort and code duplication
- Can be overkill for small or simple applications
- Requires discipline and consistency in following the architecture guidelines

---
## Onion Architecture When to Use

- When building applications with complex business logic and domain rules
- When the core domain needs to be protected from changes in external dependencies
- When testability and maintainability are key requirements
- When the application needs to be adaptable to changing frameworks and technologies
- When a clear separation of concerns and modularity is desired
- When the application is expected to grow and evolve over time

---

## Microkernel Architecture Pattern

- Separates the core system functionality (microkernel) from extended functionality (plugins)
- The microkernel provides minimal and generic functionality
- Plugins are independent components that add specific features and capabilities
- Plugins communicate with the microkernel through well-defined interfaces
- Promotes extensibility, flexibility, and modularity

---

## Microkernel Key Concepts

- Microkernel
    - Represents the core and minimal functionality of the system
    - Provides the basic services and abstractions for plugins to build upon
    - Responsible for managing the communication between plugins
    - Remains stable and unchanged as plugins are added or modified
- Plugins
    - Independent components that add specific features and capabilities to the system
    - Extend the functionality of the microkernel without modifying it
    - Communicate with the microkernel and other plugins through well-defined interfaces
    - Can be added, removed, or updated without affecting the microkernel or other plugins
- Contracts
    - Define the interfaces and communication protocols between the microkernel and plugins
    - Specify the responsibilities and expectations of both the microkernel and plugins
    - Ensure the compatibility and interoperability of plugins with the microkernel

---
## Microkernel Architecture Diagram

![15](../../../out/mermaid/marp/courses/architecting/XX_architectural_design_patterns.md/15.png)

---
## Microkernel Pros and Cons

Pros:
- Promotes extensibility and flexibility by allowing the addition of new features through plugins
- Enables the system to be customized and adapted to specific needs
- Facilitates the development and deployment of plugins independently of the microkernel
- Improves maintainability by keeping the microkernel stable and separate from plugins
- Supports the reuse and sharing of plugins across different systems

Cons:
- Increases the overall complexity of the system due to the separation of concerns
- Requires careful design and definition of contracts between the microkernel and plugins
- May introduce performance overhead due to the communication between the microkernel and plugins
- Can lead to a proliferation of plugins and potential compatibility issues
- Requires effective management and coordination of plugins and their dependencies

---

## Microkernel When to Use

- When the system needs to be highly extensible and customizable
- When the core functionality of the system is relatively stable and generic
- When the system needs to support the addition of new features and capabilities over time
- When the development and deployment of features need to be independent of the core system
- When the system needs to be adapted to different contexts or environments
- When the system benefits from the reuse and sharing of plugins across multiple instances

---
## Publish-Subscribe Pattern

- Defines a messaging pattern for communication between publishers and subscribers
- Publishers send messages to a message broker or event bus
- Subscribers register their interest in specific topics or message types
- The message broker delivers the messages to all interested subscribers
- Enables loose coupling and asynchronous communication between components

---

## Publish-Subscribe Key Concepts

- Publisher
    - A component that sends messages to the message broker
    - Publishes messages without knowledge of the subscribers
    - Can publish messages to multiple topics or channels
- Subscriber
    - A component that registers interest in specific topics or message types
    - Receives messages from the message broker based on its subscriptions
    - Can subscribe to multiple topics or channels
- Message Broker
    - A central component that receives messages from publishers and delivers them to subscribers
    - Maintains a registry of subscriptions and their associated subscribers
    - Can perform message filtering, transformation, and routing based on topic or message type
- Topic or Channel
    - A logical grouping or category of messages
    - Used by publishers to organize and categorize messages
    - Used by subscribers to express their interest in specific types of messages

---

## Publish-Subscribe Diagram

![16](../../../out/mermaid/marp/courses/architecting/XX_architectural_design_patterns.md/16.png)

---

## Publish-Subscribe Pros and Cons

Pros:
- Enables loose coupling between publishers and subscribers
- Supports asynchronous communication and independent scalability of components
- Allows for dynamic registration and deregistration of subscribers
- Facilitates event-driven architectures and reactive systems
- Provides flexibility in message routing and filtering based on topics or message types

Cons:
- Introduces additional complexity and potential performance overhead due to the message broker
- Requires careful design and management of topics and subscriptions to avoid message flooding
- Can lead to increased latency due to the indirection through the message broker
- Requires reliable message delivery and handling of failures in the message broker
- May not be suitable for scenarios requiring strict message ordering or real-time processing

---

## Publish-Subscribe When to Use

- When loose coupling and asynchronous communication between components are desired
- When the system needs to support dynamic registration and deregistration of subscribers
- When the system benefits from event-driven architectures and reactive processing
- When the scalability and independent evolution of publishers and subscribers are important
- When the system needs to handle a high volume of messages and perform message routing and filtering
- When the system can tolerate some level of latency and eventual consistency in message delivery

---
## Monolithic Architecture Pattern

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

![17](../../../out/mermaid/marp/courses/architecting/XX_architectural_design_patterns.md/17.png)

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
## Modular Monolith Pattern

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

![18](../../../out/mermaid/marp/courses/architecting/XX_architectural_design_patterns.md/18.png)

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
## Share-Nothing Architecture Pattern

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

![19](../../../out/mermaid/marp/courses/architecting/XX_architectural_design_patterns.md/19.png)

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
## Circuit Breaker Pattern

- Prevents cascading failures in distributed systems
- Allows graceful degradation and faster recovery
- Monitors for failures and "trips" to prevent further calls
- Provides fallback mechanisms and automatic recovery
---
## Circuit Breaker Pattern Diagram

![20](../../../out/mermaid/marp/courses/architecting/XX_architectural_design_patterns.md/20.png)

---
## Pros and Cons

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
## When to Use

- In microservices architectures
- Systems with critical external dependencies
- High-traffic applications prone to failures
- When implementing fault-tolerant systems
- In scenarios requiring rapid failure detection and recovery
---
## Saga Pattern

- Manages data consistency across microservices in distributed transaction scenarios
- Breaks down long-lived transactions into a sequence of local transactions
- Each local transaction updates the database and publishes an event
- Subsequent steps are triggered by these events
- Provides compensating transactions for rollback
---
## Saga Pattern Diagram

![21](../../../out/mermaid/marp/courses/architecting/XX_architectural_design_patterns.md/21.png)

---
## Pros and Cons

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
## When to Use

- In microservices architectures with distributed transactions
- When dealing with long-lived, multi-step business processes
- In systems requiring complex failure recovery mechanisms
- When strong consistency is not immediately required
- In scenarios where traditional two-phase commit is not feasible
---
## Bulkhead Pattern

- Isolates elements of an application into pools so that if one fails, the others will continue to function
- Named after the sectioned partitions (bulkheads) of a ship's hull
- Prevents cascading failures across services
- Enables fault tolerance and graceful degradation
---
## Bulkhead Pattern Diagram

![22](../../../out/mermaid/marp/courses/architecting/XX_architectural_design_patterns.md/22.png)

---
## Bulkhead Pattern Pros and Cons

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
## Bulkhead Pattern When to Use

- In microservices architectures to isolate services
- When dealing with third-party service integrations
- In systems with varying resource requirements across components
- To protect critical services from failure in non-critical ones
- In scenarios requiring different quality-of-service levels for different operations
---
## Strangler Fig Pattern

- Gradual migration strategy for rewriting or replacing legacy systems
- Incrementally creates a new system around the edges of the old
- Lets you migrate functionality piece by piece
- Named after strangler fig vines that grow around and replace their host trees
- Allows for coexistence of old and new systems during transition
---
## Strangler Fig Pattern Diagram

![23](../../../out/mermaid/marp/courses/architecting/XX_architectural_design_patterns.md/23.png)

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
## Backend for Frontend (BFF) Pattern

- Creates separate backend services for specific frontend applications or interfaces
- Tailors the API to the needs of each client type (e.g., mobile, web, desktop)
- Optimizes data transfer and aggregation for each client
- Improves performance and user experience
- Simplifies client-side logic by moving complexity to the BFF layer
---
## Backend for Frontend (BFF) Pattern Diagram

![24](../../../out/mermaid/marp/courses/architecting/XX_architectural_design_patterns.md/24.png)

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
## API Gateway Pattern

- Acts as a single entry point for all client requests
- Routes requests to appropriate microservices
- Aggregates responses from multiple services
- Handles cross-cutting concerns (authentication, logging, SSL termination)
- Can perform protocol translation and API composition
---
## API Gateway Pattern Diagram

![25](../../../out/mermaid/marp/courses/architecting/XX_architectural_design_patterns.md/25.png)

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
## Anti-Corruption Layer Pattern

- Acts as a facade between different subsystems or models
- Translates requests between incompatible domain models
- Protects the integrity of a new or refactored system from legacy influences
- Facilitates integration between systems with different semantics
- Enables gradual migration from legacy to new systems
- Originated from Domain-Driven Design principles

---

## Anti-Corruption Layer Pattern Diagram

![26](../../../out/mermaid/marp/courses/architecting/XX_architectural_design_patterns.md/26.png)

---
## Anti-Corruption Pros and Cons

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

## Anti-Corruption When to Use

- During large-scale system modernization or migration projects
- When integrating systems with fundamentally different domain models
- In scenarios where a new system must coexist with legacy systems
- To protect a well-designed domain model from external influence
- When gradually replacing a legacy system over time
- In situations where direct translation between two models is complex or undesirable
- To facilitate communication between bounded contexts in a microservices architecture
---

## Database per Service Pattern

- Each microservice has its own private database
- Ensures loose coupling between services
- Allows each service to choose the most appropriate database type
- Prevents services from accessing each other's data directly
- Supports the autonomy and independence of microservices
- Facilitates independent scaling and deployment of services

---

## Database per Service Pattern Diagram

![27](../../../out/mermaid/marp/courses/architecting/XX_architectural_design_patterns.md/27.png)

---

## Database per service Pros and Cons

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

## Database per service When to Use

- In microservices architectures to ensure service independence
- When different services have distinct data storage requirements
- To support independent scaling of services and their data stores
- In scenarios where data isolation and security are critical
- When evolving from a monolithic to a microservices architecture
- To enable independent development and deployment of services
- In systems where services need to be loosely coupled
- When different teams are responsible for different services and their data
---

## Geode Pattern

- Deploys a subset of application's services into satellite locations
- Brings services closer to end users to reduce latency
- Replicates data to local caches in each geode
- Improves performance and availability for distributed applications
- Helps comply with data sovereignty and regulations
- Allows for local processing while maintaining global consistency

---

## Geode Pattern Diagram

![28](../../../out/mermaid/marp/courses/architecting/XX_architectural_design_patterns.md/28.png)

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
## Kappa Architecture

- Simplifies Lambda Architecture by treating all data as streams
- Uses a single processing engine for both real-time and batch processing
- Relies on replayable logs or event sourcing for data storage
- Eliminates the need for separate batch and speed layers
- Aims to reduce complexity while maintaining scalability and fault-tolerance
---
## Kappa Architecture Diagram

![29](../../../out/mermaid/marp/courses/architecting/XX_architectural_design_patterns.md/29.png)

---
## Pros and Cons

Pros:
- Simplifies architecture by using a single processing path
- Reduces code duplication and maintenance overhead
- Allows easy reprocessing of data by replaying the event stream
- Provides consistency between "batch" and "real-time" results
- Typically easier to reason about and debug

Cons:
- May require more storage for maintaining a long-term log
- Can be less efficient for certain types of batch processing
- Relies heavily on the scalability of the stream processing system
- May not be suitable for all types of data or processing requirements
- Can be challenging to implement for systems not designed with event sourcing in mind
---
## When to Use

- When your data can be naturally represented as a series of events or changes
- In systems where the distinction between batch and real-time processing is blurred
- When you need to frequently reprocess historical data
- For applications built around event sourcing and CQRS principles
- When you want to simplify your architecture and reduce maintenance overhead
- In scenarios where consistency between historical and real-time views is crucial
- When your use case allows for incremental processing of all data
---
## Lambda Architecture

- Combines batch and stream processing methods
- Designed to handle massive quantities of data
- Provides comprehensive and accurate views of batch data
- Offers real-time views of online data
- Aims to balance latency, throughput, and fault-tolerance
---
## Lambda Architecture Diagram

![30](../../../out/mermaid/marp/courses/architecting/XX_architectural_design_patterns.md/30.png)

---
## Pros and Cons

Pros:
- Handles both real-time and batch processing
- Provides fault tolerance and scalability
- Allows reprocessing of data in batch layer
- Supports complex analytics on large datasets
- Enables correction of errors in real-time layer through batch processing

Cons:
- Increased complexity in system architecture
- Requires maintaining two separate systems for batch and speed layers
- May lead to increased operational and development costs
- Potential for data inconsistency between batch and speed layers
- Batch processing introduces latency in data availability
---
## When to Use

- For systems requiring both batch and real-time data processing
- When dealing with large-scale data that needs both historical and real-time analysis
- In scenarios where data accuracy is crucial, but low-latency views are also needed
- For applications that can tolerate some degree of eventual consistency
- When building systems that need to handle both incremental and reprocessing computations
- In use cases where you need to balance between accuracy (batch layer) and speed (real-time layer)
---
## Mesh Architecture

- Decentralized networking approach for microservices
- Provides service-to-service communication without a central gateway
- Uses a lightweight proxy (sidecar) alongside each service instance
- Manages routing, load balancing, and security at the service level
- Enables fine-grained control over network behavior and observability
---
## Mesh Architecture Diagram

![31](../../../out/mermaid/marp/courses/architecting/XX_architectural_design_patterns.md/31.png)

---
## Mesh Architecture Pros and Cons

Pros:
- Improves reliability and fault tolerance
- Enhances observability with detailed metrics and tracing
- Provides consistent security policies across services
- Enables advanced traffic management (e.g., canary releases, A/B testing)
- Reduces the complexity of individual microservices

Cons:
- Increases overall system complexity
- Can introduce latency due to proxy communication
- Requires additional resources for sidecar proxies
- May have a steep learning curve for teams
- Can be overkill for smaller or simpler microservices architectures
---
## Mesh Architecture When to Use

- In large-scale microservices architectures
- When you need fine-grained control over service-to-service communication
- For systems requiring advanced traffic management and load balancing
- When implementing consistent security policies across services is crucial
- In environments where detailed observability and monitoring are necessary
- For gradual adoption of microservices in a hybrid architecture
- When you want to offload common networking concerns from application code
---
## Sharded Architecture Pattern

- Horizontally partitions data across multiple databases or 'shards'
- Each shard contains a subset of the data, determined by a shard key
- Improves scalability and performance for large-scale distributed databases
- Allows for parallel processing of queries across multiple shards
- Enables handling of larger datasets than can fit on a single server
---
## Sharded Architecture Diagram

![32](../../../out/mermaid/marp/courses/architecting/XX_architectural_design_patterns.md/32.png)

---
## Sharded Pros and Cons

Pros:
- Improves scalability for large datasets
- Enhances query performance through parallelization
- Allows for better resource utilization
- Provides fault isolation (issues in one shard don't affect others)
- Enables geographic distribution of data

Cons:
- Increases complexity in data management and application logic
- Can lead to data distribution skew if shard key is poorly chosen
- Makes it challenging to perform queries across multiple shards
- Complicates data consistency and transaction management
- Can make resharding (rebalancing data across shards) difficult
---
## Sharded When to Use

- When dealing with very large datasets that exceed single server capacity
- In systems requiring high throughput for read and write operations
- When you need to scale out database resources horizontally
- For applications with clear data partitioning strategies
- In scenarios where data can be naturally segmented (e.g., by customer, region, or time)
- When you need to improve performance by reducing contention and increasing cache efficiency
---
## Throttling Pattern

- Controls the rate at which requests are processed or resources are consumed
- Prevents system overload and ensures fair resource allocation
- Can be applied at various levels: user, service, or system-wide
- Implements strategies like fixed window, sliding window, or token bucket algorithms
- Helps maintain system stability and responsiveness under high load
---
## Throttling Pattern Diagram

![33](../../../out/mermaid/marp/courses/architecting/XX_architectural_design_patterns.md/33.png)

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
