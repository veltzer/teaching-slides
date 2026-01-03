# Small Scale Design patterns

<!-- Add Mermaid.js support -->
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
<script>
  mermaid.initialize({ startOnLoad: true });
</script>

## Model-View-Controller (MVC) Pattern

---

## Overview

- Separates the application into three main components: Model, View, and Controller
- Model represents the data and business logic
- View presents the data to the user and handles user interaction
- Controller mediates between Model and View, handling input and updating state

---

## Component Roles

- Model
    - Represents the data and business logic of the application
    - Independent of the user interface and presentation
    - Notifies the View when data changes
- View
    - Presents the data to the user and handles user interaction
    - Receives updates from the Model and renders the data
    - Sends user input to the Controller
- Controller
    - Receives user input from the View and translates it into actions
    - Updates the Model based on the actions
    - Selects the appropriate View for presenting the updated data

---

## Interaction Diagram

<div class="mermaid">
graph TB
    U[User] -->|Input| V[View]
    V -->|User Events| C[Controller]
    C -->|Update| M[Model]
    M -->|Notify Changes| V
    C -->|Select View| V
    M -->|Business Logic| M

    style U fill:#fff3e0
    style V fill:#e3f2fd
    style C fill:#f3e5f5
    style M fill:#e8f5e9
</div>

---

## Pros and Cons

Pros:
- Separates concerns and responsibilities between components
- Enables independent development and testing of components
- Supports multiple Views for the same Model
- Facilitates code reuse and maintainability

Cons:
- Can lead to increased complexity and indirection
- Tight coupling between View and Controller can occur
- Potential for excessive updates and notifications between components
- May not be suitable for simple or highly interactive applications

---

## When to Use

- Application has a complex user interface with multiple Views
- Data model and business logic need to be independent of the presentation
- Multiple developers or teams are working on different components
- Application requires flexibility in adding or modifying Views
- Testing and maintainability are important considerations

---

## Interpreter Pattern

- Defines a representation for a grammar and an interpreter to interpret sentences in the language
- Provides a way to evaluate language grammar or expressions
- Defines classes for each grammar rule, which can interpret expressions
- Useful for simple languages, query languages, or configurations

---

## Interpreter Component Roles

- Abstract Expression
    - Declares an abstract interpret operation that is common to all nodes in the abstract syntax tree
- Terminal Expression
    - Implements an interpret operation associated with terminal symbols in the grammar
    - No recursion since it is a leaf node
- Non-terminal Expression
    - Implements an interpret operation for non-terminal symbols in the grammar
    - Recursively calls interpret on its child nodes
- Context
    - Contains information that is global to the interpreter
    - Accessed and manipulated by the expression nodes during interpretation

---

## Interpreter Diagram

<div class="mermaid">
graph TB
    subgraph "Abstract Syntax Tree"
        AE[Abstract Expression]
        AE --> TE[Terminal Expression]
        AE --> NTE[Non-Terminal Expression]
        NTE --> NTE1[Non-Terminal 1]
        NTE --> TE2[Terminal 2]
    end

    C[Context] -.->|Global Info| AE
    C -.->|Variables| TE
    C -.->|State| NTE

    style AE fill:#e3f2fd
    style TE fill:#f3e5f5
    style C fill:#e8f5e9
</div>

---

## Interpreter Pros and Cons

Pros:
- Provides a way to interpret a language or grammar
- Easy to change and extend the grammar by adding new expression classes
- Enables adding new ways to interpret expressions
- Supports recursive traversal of complex structures

Cons:
- Complex grammars can lead to a large number of expression classes
- Inefficient for complex grammars or large expressions
- Interpreter design pattern can be overkill for simple expressions
- Interpreter classes are tightly coupled to the grammar

---

## Interpreter When to Use

- When there is a language to interpret and the grammar is simple
- When the efficiency is not a critical concern
- When the grammar is likely to change and needs to be extended easily
- When the abstract syntax tree representation is not too complex

---

## Repository Pattern

- Mediates between the domain and data mapping layers
- Provides an abstraction of data for the domain layer
- Decouples the application from persistence frameworks
- Centralizes data access logic

---

## Repository Pattern Diagram

<div class="mermaid">
graph TB
    subgraph "Domain Layer"
        BS[Business Service]
        DE[Domain Entity]
    end

    subgraph "Repository Layer"
        IR[IRepository Interface]
        CR[Concrete Repository]
    end

    subgraph "Data Layer"
        DB[Database]
        API[External API]
        FS[File System]
    end

    BS --> IR
    IR --> CR
    CR --> DB
    CR --> API
    CR --> FS
    DE <--> CR

    style BS fill:#e3f2fd
    style IR fill:#f3e5f5
    style DB fill:#e8f5e9
</div>

---

## Repository Pros and Cons

Pros:
- Separation of concerns
- Improved testability
- Flexibility in data source
- Centralized data access logic

Cons:
- Additional layer of abstraction
- Potential for over-engineering in simple applications
- Learning curve for developers new to the pattern

---

## Repository When to Use

- Large-scale applications with complex domain models
- Projects requiring database independence
- Systems needing improved testability of data access code
- When anticipating future changes in data storage mechanisms
- In domain-driven design (DDD) architectures
---

## Repository Command Pattern

- Encapsulates a request as an object
- Decouples the object that invokes the operation from the one that knows how to perform it
- Allows parameterization of clients with different requests
- Supports undoable operations
- Enables queueing and logging of requests

---

## Command Pattern Diagram

<div class="mermaid">
graph LR
    I[Invoker] --> IC[ICommand]
    IC --> CC1[ConcreteCommand 1]
    IC --> CC2[ConcreteCommand 2]
    IC --> CC3[ConcreteCommand 3]

    CC1 --> R1[Receiver 1]
    CC2 --> R2[Receiver 2]
    CC3 --> R3[Receiver 3]

    C[Client] -.->|Creates| CC1
    C -.->|Configures| I

    style I fill:#e3f2fd
    style IC fill:#f3e5f5
    style R1 fill:#e8f5e9
</div>

---

## Command Pros and Cons

Pros:
- Decouples the sender and receiver of a request
- Allows for extensibility: new commands can be added without changing existing code
- Supports undo/redo functionality
- Enables composition of commands (Macro Commands)
- Simplifies implementation of transactional systems

Cons:
- Can lead to a high number of small, similar command classes
- May introduce unnecessary complexity for simple applications
- Can be overkill for applications with simple, straightforward operations
- Might slightly increase memory usage due to object creation

---

## Command When to Use

- When you need to parameterize objects with operations
- To implement undo/redo functionality
- For queueing, scheduling, or executing requests at different times
- In GUI systems for handling menu actions or button clicks
- To implement transactional behavior and rollback mechanisms
- When you need to structure a system around high-level operations built on primitive operations
---

## Decorator Pattern

- Allows behavior to be added to an individual object, dynamically, without affecting the behavior of other objects from the same class
- Provides a flexible alternative to subclassing for extending functionality
- Adheres to the Open/Closed Principle: open for extension, closed for modification
- Composes objects in a recursive manner
- Allows for a stack of behaviors that can be configured at runtime

---

## Decorator Pattern Diagram

<div class="mermaid">
graph TB
    IC[IComponent]
    IC --> CC[ConcreteComponent]
    IC --> D[Decorator]

    D --> CD1[ConcreteDecorator A]
    D --> CD2[ConcreteDecorator B]
    D --> CD3[ConcreteDecorator C]

    D -.->|Wraps| IC

    CD1 -.->|Adds Feature A| CC
    CD2 -.->|Adds Feature B| CC
    CD3 -.->|Adds Feature C| CC

    style IC fill:#e3f2fd
    style D fill:#f3e5f5
    style CC fill:#e8f5e9
</div>

---

## Decorator Pros and Cons

Pros:
- Extends an object's behavior without making a new subclass
- Adds responsibilities dynamically at runtime
- Combines multiple behaviors using multiple decorators
- Follows Single Responsibility Principle by dividing functionality into classes
- Allows for a "pay as you go" approach to adding features

Cons:
- Can result in many small objects in the design, making it harder to learn and debug
- Can be complex for developers unfamiliar with the pattern
- Decorators and their components aren't identical, so shouldn't be used where object identity is important
- Can sometimes lead to excessive layering if overused

---

## Decorator When to Use

- When you need to add responsibilities to objects dynamically without affecting other objects
- When extension by subclassing is impractical or impossible
- To avoid a class hierarchy explosion when many independent extensions are possible
- When you want to add functionality that can be withdrawn easily
- In systems where you need a stack of behaviors that can be composed at runtime
- When applying the Open/Closed principle in your design
---

## Facade Pattern

- Provides a simplified interface to a complex subsystem
- Acts as a front-facing interface masking more complex underlying or structural code
- Defines a higher-level interface that makes the subsystem easier to use
- Doesn't encapsulate the subsystem but provides a simplified view of it
- Decouples the client implementation from the complex subsystem

---

## Facade Pattern Diagram

<div class="mermaid">
graph LR
    C[Client] --> F[Facade]

    subgraph "Complex Subsystem"
        F --> S1[Subsystem 1]
        F --> S2[Subsystem 2]
        F --> S3[Subsystem 3]
        F --> S4[Subsystem 4]

        S1 -.-> S2
        S2 -.-> S3
        S3 -.-> S4
        S4 -.-> S1
    end

    style C fill:#e3f2fd
    style F fill:#f3e5f5
    style S1 fill:#e8f5e9
</div>

---

## Facade Pros and Cons

Pros:
- Simplifies the interface for a complex system
- Decouples client code from subsystem code
- Promotes loose coupling between subsystems and its clients
- Can layer facades to compose complex systems
- Shields clients from subsystem components, reducing dependencies

Cons:
- Can become a "god object" coupled to all classes of an app
- May introduce an additional level of indirection, affecting performance
- Might hide useful lower-level functionality from clients
- Can violate the principle of least knowledge by exposing internal functions

---

## Facade When to Use

- When you need to provide a simple interface to a complex subsystem
- To decompose a subsystem into separate layers
- When there are many dependencies between clients and the implementation classes of an abstraction
- To structure a subsystem into layers, using facades to define entry points to each level
- When you want to minimize coupling between subsystems
- To wrap a poorly designed collection of APIs with a single well-designed API
