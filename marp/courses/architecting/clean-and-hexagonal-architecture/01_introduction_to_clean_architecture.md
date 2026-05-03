---
tags:
  - architecture:clean-architecture
level: intermediate
category: architecture
audience:
  - audiences:developers

---
# Introduction to Clean Architecture

---
## Goals of Clean Architecture

![clean_goals](svg/courses/architecting/clean-and-hexagonal-architecture/01_introduction/clean_goals.svg)

---
## What This Chapter Covers

- What clean architecture is
- Robert Martin's vision
- The dependency rule
- Why it matters
- Trade-offs

---
## What Clean Architecture Is

- An organising principle for code
- Domain / business logic at the centre
- Frameworks, DBs, UI at the outside
- Dependencies point inward
- Outer layers can change without affecting the core

---
## The Goals

- Independent of frameworks
- Testable without UI / DB
- Independent of UI
- Independent of DB
- Independent of any external agency

---
## The Dependency Rule

- Source code dependencies always point inward
- Inner layers know nothing about outer
- Outer layers depend on inner abstractions
- A SOLID-driven principle
- The crux of clean architecture

---
## The Onion Layers

- Entities (innermost)
- Use cases
- Interface adapters
- Frameworks and drivers (outermost)
- Each depends only on inner

---
## Why It Matters

- Testability: domain testable in isolation
- Maintainability: replace DB without touching domain
- Longevity: domain logic survives tech churn
- Onboarding: clear separation of concerns

---
## Comparison To Traditional MVC

- MVC: model knows DB, controller knows view
- Clean: domain knows nothing
- More layers; more files
- Higher discipline; longer-lived code

---
## When To Use

- Long-lived applications
- Complex domain logic
- Multiple delivery mechanisms (web + CLI + mobile)
- Multiple data stores
- Team with discipline to maintain layers

---
## When NOT To Use

- Simple CRUD apps
- Prototypes
- Teams that won't maintain the layering
- Cost > benefit for short-lived code

---
## Common Misconceptions

- "Clean = many files" — yes, but well-organised
- "Domain = no Spring annotations" — strict view; strict version
- "Always 4 layers" — guideline, not strict
- Adapt to context

---
## Trade-Offs

- Pro: testability, longevity, replaceability
- Con: more code, more abstraction
- Con: harder for newcomers
- Worth it past a threshold of complexity

---
## What's Next

- The dependency rule in detail
- Entities and use cases
- Interface adapters
- Hexagonal (ports and adapters)
- DI and testing
