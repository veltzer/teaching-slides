---
tags:
  - concepts:architecture
  - concepts:design-patterns
level: intermediate
category: architecture
audience:
  - audiences:developers
  - audiences:architects

---
# Internal Code Architectures

---
## A Note on DDD

- Domain-Driven Design is not a code-organization pattern like Hexagonal or Onion
- It is a methodology for modeling the domain itself
- Strategic side: Bounded Contexts, Context Maps, Ubiquitous Language
- Tactical side: Entities, Value Objects, Aggregates, Domain Events, Repositories
- The patterns in this chapter (Hexagonal, Clean, Onion) are common implementation vehicles for DDD tactical patterns
- Full coverage: Architecting Software Systems course, ch 04 (Domain-Driven Design)
- This chapter focuses on patterns for organizing the code that implements your domain

---
## CQRS Overview

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

![cqrs_architecture_diagram](svg/courses/architecting/architecture-patterns/04_internal_code_architectures/cqrs_architecture_diagram.svg)

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
## Event Sourcing Overview

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

![event_sourcing_architecture_diagram](svg/courses/architecting/architecture-patterns/04_internal_code_architectures/event_sourcing_architecture_diagram.svg)

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
## Hexagonal Overview

- Also known as the Ports and Adapters pattern
- Focuses on creating loosely coupled application components
- Separates the core business logic from external dependencies
- Defines ports (interfaces) for interaction with the outside world
- Uses adapters to connect the ports to specific technologies or services
- Promotes testability, maintainability, and flexibility

---
## Hexagonal Key Concepts

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

![hexagonal_architecture_diagram](svg/courses/architecting/architecture-patterns/04_internal_code_architectures/hexagonal_architecture_diagram.svg)

---
## Hexagonal Pros and Cons

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
## Hexagonal When to Use

- When building complex applications with multiple external dependencies
- When the domain logic needs to be independent and decoupled from infrastructure concerns
- When testability and maintainability are critical requirements
- When the application needs to support multiple user interfaces or delivery mechanisms
- When the application is expected to evolve and adapt to changing requirements
- When a modular and loosely coupled architecture is desired

---
## Clean Architecture Overview

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
## Clean Architecture Diagram

![architecture_diagram](svg/courses/architecting/architecture-patterns/04_internal_code_architectures/architecture_diagram.svg)

---
## Clean Architecture Pros and Cons

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
## Clean Architecture When to Use

- When building large and complex applications with multiple external dependencies
- When the core business logic needs to be independent and protected from changes in external layers
- When testability and maintainability are critical concerns
- When the application needs to support multiple user interfaces or delivery mechanisms
- When the system is expected to evolve and adapt to changing requirements over time
- When a clear separation of responsibilities and concerns is desired

---
## Onion Overview

- Organizes the application into concentric layers
- Innermost layer contains the domain model and core business logic
- Outer layers depend on inner layers but not vice versa
- Promotes separation of concerns and dependency inversion
- Aims to make the application more maintainable, testable, and adaptable

---
## Onion Key Concepts

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

![onion_architecture_diagram](svg/courses/architecting/architecture-patterns/04_internal_code_architectures/onion_architecture_diagram.svg)

---
## Onion Pros and Cons

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
## Onion When to Use

- When building applications with complex business logic and domain rules
- When the core domain needs to be protected from changes in external dependencies
- When testability and maintainability are key requirements
- When the application needs to be adaptable to changing frameworks and technologies
- When a clear separation of concerns and modularity is desired
- When the application is expected to grow and evolve over time

---
## Microkernel Overview

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

![microkernel_architecture_diagram](svg/courses/architecting/architecture-patterns/04_internal_code_architectures/microkernel_architecture_diagram.svg)

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
## Summary

- CQRS splits read and write models when their requirements diverge
- Event Sourcing stores state as an append-only log of events for auditability and replay
- Hexagonal, Clean, and Onion are variants of the same idea: insulate domain logic from infrastructure via dependency inversion
- Microkernel decouples a stable core from variable plugins
- These patterns compose well: Hexagonal + CQRS + Event Sourcing is a common combination
- For DDD methodology see the Architecting Software Systems course
