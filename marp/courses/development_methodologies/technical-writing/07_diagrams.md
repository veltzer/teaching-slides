---
tags:
  - practices:technical-writing
  - practices:diagrams
level: beginner
category: methodology
audience:
  - audiences:developers

---

# Diagrams

---

## When Diagrams Earn Their Place

![diagram_purposes](svg/courses/development_methodologies/technical-writing/07_diagrams/diagram_purposes.svg)

---

## Diagram Types

![diagram_types](svg/courses/development_methodologies/technical-writing/07_diagrams/diagram_types.svg)

---

## What This Chapter Covers

- When and how to use diagrams
- Mermaid diagrams
- PlantUML
- Architecture diagrams
- Sequence diagrams
- Diagram-as-code workflows

---

## Why Diagrams Help

- Some concepts are inherently visual
- A flow with 5 steps is easier as a diagram than a paragraph
- Topology, hierarchy, and process: all visual by nature
- A picture *can* be worth 1000 words — when it's the right picture
- Done badly, diagrams confuse more than they clarify

---

## When To Use a Diagram

- Showing relationships between many things
- Explaining a sequence of events
- Mapping a topology (network, system)
- Comparing two structures side by side
- When prose is taking too many words

---

## When Not To Use a Diagram

- A single concept (use prose or a list)
- Numerical data (use a chart or table)
- Code examples (use a code block)
- When the diagram will go stale
- When you can't explain it in words first

---

## Diagram-as-Code

- Diagrams written as text (Mermaid, PlantUML)
- Versioned in git
- Diff-friendly
- Render automatically in CI / doc sites
- The modern default for technical docs

---

## Mermaid

```misc
flowchart LR
  A[Start] --> B{Decision}
  B -->|Yes| C[Action 1]
  B -->|No|  D[Action 2]
  C --> E[End]
  D --> E
```

- Markdown-friendly
- Renders in GitHub, GitLab, most static sites
- Many diagram types: flowchart, sequence, class, state, ER, gantt
- The most-deployed diagram tool today

---

## Mermaid Diagram Types

- `flowchart`: boxes and arrows
- `sequenceDiagram`: actors exchanging messages over time
- `classDiagram`: UML class diagrams
- `stateDiagram`: state machines
- `erDiagram`: entity-relationship
- `gantt`: project timelines

---

## PlantUML

```misc
@startuml
participant User
participant Server
participant DB

User -> Server: GET /orders
Server -> DB: SELECT * FROM orders
DB --> Server: rows
Server --> User: JSON
@enduml
```

- Older than Mermaid; more features
- Java-based renderer
- Great for UML
- Less integrated with modern doc sites

---

## Architecture Diagrams

- Show major components and their relationships
- Box for each service / module
- Arrows for the direction of dependency or data flow
- Group with rectangles or color
- Less is more: 5-10 boxes, not 50

---

## C4 Model

- A specific approach to architecture diagrams
- Four levels: Context, Container, Component, Code
- Each level zooms in
- Different audience for each level
- Tools: Structurizr, Mermaid (`C4Context` syntax)

---

## Sequence Diagrams

- Time flows top to bottom
- Actors arranged left to right
- Arrows show messages
- Reveals timing and order
- Excellent for explaining APIs and protocols

---

## A Sample Sequence

```misc
sequenceDiagram
  Client->>Auth: POST /login
  Auth->>Database: lookup user
  Database-->>Auth: user record
  Auth->>Auth: verify password
  Auth-->>Client: token
  Client->>API: GET /resource (with token)
```

- Each line is one interaction
- Solid arrow: request; dashed: response
- Self-loops for internal work

---

## Network Diagrams

- Boxes for hosts / services
- Lines for connections
- Annotations for ports, protocols
- Use grouping for VPCs, subnets, regions
- Avoid clutter; one concept per diagram

---

## State Machines

```misc
stateDiagram-v2
  [*] --> Idle
  Idle --> Loading: fetch()
  Loading --> Ready: success
  Loading --> Error: failure
  Ready --> Idle: reset()
  Error --> Idle: retry()
```

- States as nodes
- Transitions as arrows
- Initial / final states marked
- Useful for workflows and protocols

---

## Diagram Aesthetics

- One reading direction: left-to-right or top-to-bottom
- Consistent shapes for like things
- Limited color palette
- Labels on every line
- White space is part of the design

---

## Where Diagrams Live

- Inline in markdown (Mermaid)
- As image files (SVG preferred over PNG)
- In separate diagram files (PlantUML, Excalidraw, draw.io)
- Versioned alongside the code
- Generate to image in CI; commit the source

---

## Maintaining Diagrams

- Diagrams rot just like code
- "This diagram is from 2019" — easy to spot, hard to fix
- Date diagrams; review periodically
- Auto-generate where possible (DB schema, dependency graph)
- Stale diagrams mislead more than they help

---

## Common Diagram Mistakes

- Too many boxes; everything connected to everything
- 14 colors for 14 categories
- No legend
- Diagram says one thing, prose says another
- A binary asset that can't be diffed in a PR
