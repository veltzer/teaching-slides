---
tags:
  - concepts:domain-driven-design
  - practices:facilitation
level: advanced
category: architecture
audience:
  - audiences:architects
  - audiences:developers

---
# Event Storming and Domain Discovery

---
## What Event Storming Is

- A workshop technique for exploring complex business domains
- Created by Alberto Brandolini (~2013)
- Whiteboard or sticky notes; the whole team participates
- Output: a shared understanding of how the domain works

---
## Why Event Storming

- Domain experts and developers often talk past each other
- A workshop with concrete events forces alignment
- The result is faster than weeks of interviews
- Every participant leaves with the same picture

---
## What You Need

- A long wall (physical or virtual)
- Sticky notes in different colors (orange, blue, yellow, pink, purple)
- Markers
- Domain experts, developers, anyone with relevant knowledge
- A facilitator

---
## Sticky Note Colors (Conventional)

- **Orange**: domain events (past tense: "OrderPlaced")
- **Blue**: commands (imperative: "PlaceOrder")
- **Yellow**: aggregates (the things that handle commands and emit events)
- **Pink**: external systems and people
- **Purple**: policies and process managers

---
## Three Levels of Event Storming

- **Big Picture**: explore the whole domain; broad strokes
- **Process Modeling**: drill into specific business processes
- **Software Design**: identify aggregates, commands, events for implementation
- Each level builds on the previous

---
## Big Picture Storming

- Goal: understand the domain end-to-end
- Participants brainstorm domain events as orange sticky notes
- Place them on a timeline left to right
- Cluster events that belong together
- Identify pain points, unknowns, hot spots

---
## Process Modeling Storming

- Pick one process from the big picture
- Add commands (blue) that cause events
- Add aggregates (yellow) that handle commands and emit events
- Add policies (purple) that react to events and trigger commands
- The flow becomes visible

---
## Software Design Storming

- Closest to implementation
- Refine aggregates: what data, what invariants, what boundaries
- Identify bounded contexts from event clusters
- Output: a starting point for code

---
## Running an Event Storming

- 2-4 hours per session
- Start with "what events happen?" — silent brainstorm
- Place events on the timeline
- Gradually add commands, aggregates, policies
- Frequent stand-back-and-discuss moments

---
## Hot Spots

- Areas of the timeline where the team disagrees or is confused
- Mark them explicitly (red sticky)
- These are the places to dig deeper
- Often: the most valuable parts of the workshop

---
## Pivotal Events

- Events that mark major transitions in the domain
- "OrderShipped" might be pivotal: many things change after it
- Use them to identify bounded context boundaries
- Often a clue to good service decomposition

---
## Outcomes of Event Storming

- A shared model in everyone's head
- A set of bounded contexts
- A list of aggregates and their commands/events
- A list of integration points and policies
- A photo or digital archive of the workshop board

---
## When to Run an Event Storming

- Starting a new project
- Onboarding new team members
- Major refactoring of an existing system
- Resolving disagreements about how the domain works
- Periodic alignment as understanding evolves

---
## Common Mistakes

- Letting one expert dominate the workshop
- Skipping silent brainstorm — events come too narrow
- Going to software-level detail too early
- Treating the output as final rather than a snapshot

---
## After the Workshop

- Capture the board (photo or digital tool)
- Write a short narrative of the process
- Identify follow-up questions
- Schedule another session if hot spots are unresolved

---
## Tools

- Physical: real walls, paper, stickies
- Digital: Miro, Mural, EventStorming.com
- Hybrid: works but loses some energy
- The output matters more than the medium

---
## Domain Storytelling: A Cousin

- Similar workshop technique
- Focuses on user stories: "Customer does X, system responds Y"
- Complementary to event storming
- Use both in different contexts

---
## Anti-Patterns

- Workshop without a domain expert
- Workshop without a developer
- Treating it as a one-time event rather than a recurring practice
- No follow-through into code

---
## Summary

- Event storming is a fast, collaborative way to explore a domain
- Three levels: big picture, process modeling, software design
- Use sticky-note colors as conventions, not laws
- Hot spots and pivotal events guide later design
- Output: shared understanding plus a starting model for implementation
