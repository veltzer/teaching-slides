---
tags:
  - concepts:design-patterns
level: intermediate
category: design-patterns
audience:
  - audiences:developers

---
# Overview

---
## What This Chapter Covers

- What design patterns are
- Where they came from
- How they differ from principles like SOLID
- The vocabulary they give a team
- Patterns and language
- A short tour of how to read pattern descriptions

---
## What a Design Pattern Is

- A *named* solution to a *recurring* design problem
- Templates with a problem, a solution, and known consequences
- Not code you copy — a structure you adapt to your context
- Not a library — a way of organising classes and their interactions
- Once a team shares the vocabulary, designs become discussable in shorthand

---
## A Brief History

- Christopher Alexander used "patterns" for architecture in the 1970s
- Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides — the "Gang of Four"
- 1994 book *Design Patterns: Elements of Reusable Object-Oriented Software*
- 23 patterns split into Creational, Structural, Behavioural
- These 23 are still the canonical "design patterns" in conversation

---
## Patterns vs Principles

- **Principles** (SOLID, DRY, KISS): general guidance, language-agnostic, "what to aim for"
- **Patterns** (Singleton, Factory, Observer): specific structures, "how to organise"
- Principles tell you the destination; patterns are sometimes the route
- Patterns *embody* principles when applied well
- A team needs both

---
## What Patterns Are Not

- A complete solution you drop in
- A guarantee of good design — applied wrong, they create complexity
- A required toolkit — many programs need none
- A replacement for thinking about your specific problem
- A topic for showing off; choose patterns based on need

---
## Why Learn Them

- Vocabulary: "let's use the Strategy here" beats a 10-minute explanation
- Recognition: spot when you've reinvented one and can use the proven version
- Trade-off awareness: each pattern has known costs documented over decades
- Reading: understand other people's code that uses them
- Discipline: standard structure beats ad-hoc invention every time

---
## Pattern Categories

![categories](svg/courses/design_patterns/design-patterns/01_overview/categories.svg)

---
## Reading a Pattern Description

- **Intent**: one sentence — what problem the pattern solves
- **Motivation**: a small story showing the problem
- **Structure**: a class diagram of the participants
- **Participants**: each class's role
- **Consequences**: what you gain, what you give up
- **Implementation**: language-specific notes

---
## Patterns and Language

- The Gang of Four book uses C++ and Smalltalk
- Many patterns are *trivial* in dynamic / functional languages
- Strategy in C++ &#8594; pass an object; in Python &#8594; pass a function
- Visitor in Java &#8594; double dispatch; in Haskell &#8594; pattern matching
- Read patterns as ideas, not as Java idioms

---
## Patterns vs Anti-Patterns

- **Pattern**: a *recommended* solution to a recurring problem
- **Anti-pattern**: a *common but harmful* response to a recurring problem
- Singleton can become an anti-pattern when used as a global variable
- God Object, Spaghetti Code, Magic Numbers — anti-patterns
- Knowing both makes you a better reviewer

---
## A Common Misuse

- Building a system *to* use patterns
- Looks impressive in a class diagram, costs in maintenance
- Patterns are *justified by problems*
- If there's no recurring problem, the pattern adds noise without value
- "Pattern fever" — a phase most developers go through, then recover from

---
## Choosing the Right Pattern

- Identify the *real* problem first
- Look at the patterns whose intent matches
- Read the consequences — what you give up
- Try the simplest one that addresses the problem
- Refactor *into* the pattern when needed; don't guess up front

---
## Learning Strategy

- Don't memorise all 23 at once
- Learn 4-5 you'll actually use (Strategy, Factory, Observer, Decorator, Template Method)
- Recognise the others when reading code
- Implement each pattern at least once in a small example
- Re-read the descriptions every few years — your understanding deepens

---
## Patterns Beyond GoF

- Architectural patterns: MVC, MVVM, Hexagonal, Clean
- Concurrency patterns: Producer-Consumer, Future, Reactor
- Distributed systems patterns: Saga, Circuit Breaker, Bulkhead
- Domain-Driven Design patterns: Aggregate, Entity, Value Object
- This course is the GoF foundation; the rest extend it

---
## What's Next

- Five Creational patterns: making objects with intent
- Seven Structural patterns: composing objects without rigidity
- Eleven Behavioural patterns: how objects share work
- Worked examples in Python and Java
- For each: when to reach for it, and when not to
