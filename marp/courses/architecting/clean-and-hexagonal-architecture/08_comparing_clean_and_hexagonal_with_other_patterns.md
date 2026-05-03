---
tags:
  - architecture:clean-architecture
  - architecture:patterns
level: intermediate
category: architecture
audience:
  - audiences:architects

---
# Comparing Clean and Hexagonal with Other Patterns

---
## Related Patterns

![related_patterns](svg/courses/architecting/clean-and-hexagonal-architecture/08_comparing_clean_and_hexagonal_with_other_patterns/related_patterns.svg)

---
## What This Chapter Covers

- Clean vs Hexagonal
- Onion Architecture
- DDD
- Layered (3-tier)
- MVC / MVP / MVVM
- When to use which

---
## Clean vs Hexagonal

- Both: domain at the centre, dependencies inward
- Clean: layered (rings)
- Hexagonal: ports on edges
- Same idea; different visual / vocabulary
- Pick whichever your team prefers

---
## Patterns Side by Side

![pattern_comparison](svg/courses/architecting/clean-and-hexagonal-architecture/08_comparing_clean_and_hexagonal_with_other_patterns/pattern_comparison.svg)

---
## Onion Architecture

- Same idea: layers, dependencies inward
- Predates Clean Architecture
- Jeffrey Palermo (2008)
- Effectively the same as Clean
- Naming convergence: pick one in the team

---
## DDD (Domain-Driven Design)

- Eric Evans (2003)
- About the *modelling*; not the layering
- Bounded contexts, aggregates, value objects
- Often combined with Clean / Hexagonal
- Complementary; not alternative

---
## DDD + Clean

- DDD models the domain
- Clean structures the code
- Aggregates are entities; use cases manipulate them
- Common pairing in serious enterprise codebases

---
## Layered (3-Tier)

- Presentation, Business, Data
- Older; pre-dates Clean
- Often: Business depends on Data (wrong direction)
- Clean fixes: Data depends on Business (interfaces)

---
## MVC

- Model, View, Controller
- Originally a UI pattern (Smalltalk)
- Often misapplied: model knows everything
- Clean: replace MVC's model with full layered architecture

---
## MVP / MVVM

- UI patterns, related to MVC
- Move logic out of the view
- Don't replace Clean; complement it
- Use within the UI / adapter layer

---
## CQRS

- Command Query Responsibility Segregation
- Separate read and write models
- Often combined with Clean / Hexagonal
- Two sets of use cases (commands and queries)
- Pairs naturally; not required

---
## Event Sourcing

- Storage of events; current state derived
- Often combined with CQRS
- Clean architecture organises the rest
- Events live in the domain layer

---
## Microservices

- Distribution choice; orthogonal to internal architecture
- Each service can be Clean / Hexagonal internally
- Or: monolith with Clean architecture
- Don't conflate these decisions

---
## When To Use Each

- Clean / Hexagonal: long-lived domains, complex logic
- MVC: simple web UIs
- DDD: rich domain modelling
- 3-Tier: simple CRUD, especially legacy
- Serverless / functions: per-function structure usually flat

---
## Hybrid

- Clean Architecture + DDD: common
- Clean + CQRS: common at scale
- Clean inside microservices: common
- The patterns complement; don't compete

---
## Picking By Team

- Match the pattern to the team's discipline
- Junior team: simpler patterns
- Senior team: invest in Clean
- Pick the simplest that meets the longevity goal

---
## Common Pattern Mistakes

- Pattern as religion
- Adopting Clean for a 100-line script
- Mixing layers naively (3-tier with framework on top)
- Ignoring DDD modelling; just laying code
- "We chose pattern X" without team buy-in

---
## Course Wrap-Up

- Domain at the centre is the universal idea
- Dependencies always point inward
- Layers / ports / adapters: structural details
- Testing benefits from the discipline
- DI is the wiring mechanism
- Pick by longevity and complexity; not by trend
