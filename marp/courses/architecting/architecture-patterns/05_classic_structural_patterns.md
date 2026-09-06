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

# Classic Structural Patterns

---

## Layered Overview

- Partitions the system into layers, each with a specific role and responsibility
- Common layers: Presentation, Application, Business Logic, Data Access
- Adjacent layers communicate via well-defined interfaces

---

## Layer Responsibilities

- Presentation Layer
    - User interface and user interaction
    - Displays information to the user and interprets user commands
- Application Layer
    - Coordinates application activity
    - Doesn't contain business logic
    - Delegates to business logic layer
- Business Logic Layer
    - Core functionality and business rules
    - Independent of other layers
- Data Access Layer
    - Provides persistence for the business layer
    - Abstracts the actual database or external services

---

## Layered Diagram

![layer_diagram](svg/courses/architecting/architecture-patterns/05_classic_structural_patterns/layer_diagram.svg)

---

## Layered Pros and Cons

Pros:
- Separation of concerns and modularity
- Changes in one layer don't affect others
- Easy to understand and implement
- Supports incremental development

Cons:
- Potential for tight coupling between layers
- Performance overhead from layer-to-layer communication
- Limited flexibility and scalability
- Can lead to monolithic applications over time

---

## Layered When to Use

- Business logic can be cleanly separated from presentation and data
- Multiple user interfaces need to reuse business logic
- Incremental development is desired
- Different teams will work on different layers

---

## Master-Slave Overview

- One component (the master) controls one or more other components (the slaves)
- Master assigns tasks to slaves and monitors their progress
- Slaves complete assigned tasks and report back to master
- Often used for parallel processing or redundancy
- Modern equivalents in the field: Leader-Worker (compute), Primary-Replica (databases)

---

## Master-Slave Component Roles

- Master
    - Decomposes task into smaller subtasks
    - Distributes subtasks to slaves
    - Monitors slave progress and health
    - Aggregates results from slaves
- Slave
    - Accepts tasks from master
    - Processes subtasks independently
    - Reports status and results to master
    - May be identical to each other

---

## Master-Slave Interaction Diagram

![interaction_diagram](svg/courses/architecting/architecture-patterns/05_classic_structural_patterns/interaction_diagram.svg)

---

## Master-Slave Pros and Cons

Pros:
- Enables parallel processing for better performance
- Supports scalability by adding more slaves
- Provides fault tolerance if slaves fail
- Simplifies slave implementation and testing

Cons:
- Master can be a single point of failure
- Added latency from master-slave communication
- Limited applicability outside parallel processing
- Slaves are not autonomous and rely on master

---

## Master-Slave When to Use

- Task can be decomposed into independent subtasks
- Processing can be done more efficiently in parallel
- Resource usage needs to be coordinated
- Fault tolerance and redundancy are required
- Slaves do not need to communicate with each other

---

## Pipe-Filter Overview

- Decomposes a task into a series of sequential steps (filters)
- Data flows through the steps via connectors (pipes)
- Each filter works independently, unaware of other filters
- Filters can be added, removed, or reordered as needed

---

## Pipe-Filter Component Roles

- Filter
    - Performs a specific processing step
    - Receives input data, processes it, and produces output
    - Does not know or interact with other filters
- Pipe
    - Connects the output of one filter to the input of the next
    - Passes data between filters
    - Can perform buffering, synchronization, or transformation
- Data
    - Flows through the pipes and is processed by the filters
    - Can be a stream of bytes, objects, or messages

---

## Pipe-Filter Diagram

![pipe_filter_diagram](svg/courses/architecting/architecture-patterns/05_classic_structural_patterns/pipe_filter_diagram.svg)

---

## Pipe-Filter Pros and Cons

Pros:
- Supports reuse and late binding of filters
- Easy to understand and maintain individual filters
- Flexible and adaptable to changing requirements
- Naturally fits batch processing scenarios

Cons:
- Not suitable for interactive or request-response interactions
- Error handling and recovery can be complex
- Potential performance overhead from data flow between filters
- Overall pipeline can be harder to understand and debug

---

## Pipe-Filter When to Use

- Processing can be divided into a sequence of independent steps
- Reuse and late composition of steps is desired
- Multiple sources need to be processed in the same way
- Output of one step is input for the next step
- Little or no user interaction is required during processing

---

## Blackboard Overview

- Coordinates a group of loosely coupled, independent Knowledge Sources (KSs)
- KSs work collaboratively to solve a problem using a shared data structure (Blackboard)
- Each KS contributes a piece of the solution based on its specialized knowledge
- Control component manages the activation and scheduling of KSs

---

## Blackboard Component Roles

- Blackboard
    - Shared data structure that holds the problem state and partial solutions
    - Accessible by all Knowledge Sources for reading and writing
    - Organized into hierarchical levels of abstraction
- Knowledge Source (KS)
    - Independent module that encapsulates a specific piece of knowledge or expertise
    - Reads data from the Blackboard, processes it, and writes results back
    - Triggered by changes in the Blackboard or by the Control component
- Control
    - Manages the activation and scheduling of Knowledge Sources
    - Monitors the Blackboard for changes and selects appropriate KSs to activate
    - Can implement different strategies for KS activation and conflict resolution

---

## Blackboard Interaction Diagram

![blackboard_interaction_diagram](svg/courses/architecting/architecture-patterns/05_classic_structural_patterns/blackboard_interaction_diagram.svg)

---

## Blackboard Pros and Cons

Pros:
- Enables collaboration among independent, heterogeneous Knowledge Sources
- Supports incremental and opportunistic problem solving
- Provides flexibility in adding or modifying Knowledge Sources
- Allows for multiple control strategies and conflict resolution mechanisms

Cons:
- Can lead to complex interactions and dependencies between Knowledge Sources
- Performance may depend on the efficiency of the Blackboard and Control components
- Debugging and tracing the problem-solving process can be challenging
- May require careful design and partitioning of the problem space and knowledge

---

## Blackboard When to Use

- Problem can be decomposed into loosely coupled subproblems
- Multiple, independent sources of knowledge need to collaborate
- Incremental and opportunistic problem solving is desired
- Flexibility in adding or modifying knowledge sources is required
- Complex control strategies and conflict resolution mechanisms are needed

---

## Summary

- Layered organizes a single application into stacked horizontal slices
- Master-Slave centralizes control of parallel work under one coordinator
- Pipe-Filter chains independent stages with data flowing one direction
- Blackboard lets multiple specialists collaborate via shared state with a controller
- These are the oldest entries in the catalog — most modern systems still use one or more
