# Small Scale Design patterns

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

![interaction_diagram](/mermaid/courses/architecting/architecting/12_small_scale_design_patterns/interaction_diagram.mmd)

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

![interpreter_diagram](/mermaid/courses/architecting/architecting/12_small_scale_design_patterns/interpreter_diagram.mmd)

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

![repository_pattern_diagram](/mermaid/courses/architecting/architecting/12_small_scale_design_patterns/repository_pattern_diagram.mmd)

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

![command_pattern_diagram](/mermaid/courses/architecting/architecting/12_small_scale_design_patterns/command_pattern_diagram.mmd)

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

![decorator_pattern_diagram](/mermaid/courses/architecting/architecting/12_small_scale_design_patterns/decorator_pattern_diagram.mmd)

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

![facade_pattern_diagram](/mermaid/courses/architecting/architecting/12_small_scale_design_patterns/facade_pattern_diagram.mmd)

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
