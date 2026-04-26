---
tags:
  - concepts:domain-driven-design
  - practices:refactoring
level: advanced
category: architecture
audience:
  - audiences:architects
  - audiences:developers

---
# Refactoring Toward Deeper Insight

---
## What This Chapter Is About

- DDD is iterative; the first model is rarely the right one
- "Refactoring toward deeper insight" is Eric Evans' phrase for evolving the model as understanding grows
- This is a discipline, not a one-time activity
- The mature DDD team refactors the model continuously

---
## Why Models Drift

- Initial understanding is incomplete
- New requirements expose hidden concepts
- The domain itself changes over time
- The model that fit yesterday may not fit today

---
## Signs of a Drifting Model

- Names don't match how the business talks anymore
- "We have to ask the senior dev because the model is in his head"
- New features require workarounds because the model doesn't support them
- The codebase has more `if special_case` than business logic

---
## Three Levels of Refactoring

- **Code-level**: rename, extract method, simplify (the standard refactorings)
- **Model-level**: introduce new concepts, split aggregates, redraw boundaries
- **Strategic-level**: change bounded contexts, split or merge services
- All three apply; DDD emphasizes the latter two

---
## Continuous Refactoring as Discipline

- Refactoring isn't a project; it's a daily practice
- Every commit is an opportunity to make the model clearer
- The team commits to keeping the model healthy
- Without this discipline, models decay

---
## Listening for the Domain

- Conversations with domain experts surface new concepts
- A new term that hasn't been explicit before
- A familiar term that means something different in a new context
- These are signals to refactor

---
## Concept Mining

- Look in the code for repeated patterns
- "We always do X right after Y" — extract a domain concept for "X-after-Y"
- "Five fields always travel together" — make them a value object
- The implicit becomes explicit

---
## Discovery Through Implementation

- Sometimes you only see the right model after writing the wrong one
- The first attempt teaches you what the model should be
- The second attempt is the refactor
- Plan for it; don't expect to nail the model on day one

---
## Pivoting on a Pivotal Concept

- Sometimes a single new concept reorganizes everything
- "We're not really tracking orders; we're tracking commitments"
- The new concept fits better; rebuild around it
- These are rare but transformative

---
## Splitting an Aggregate

- An aggregate that's grown too big and slow
- Find the natural seam: which entities really need to be in the same transaction?
- Split: each becomes its own aggregate
- Cross-aggregate operations become process managers (or sagas)

---
## Merging Aggregates

- Two aggregates that always change together
- Constant cross-aggregate coordination is a smell
- Merge them; one consistency boundary
- Less common than splitting, but real

---
## Redrawing Bounded Contexts

- Two contexts that always exchange the same data
- Their integration is more code than their independence saves
- Reconsider the boundary
- Sometimes the right answer is one bigger context

---
## When to Stop Refactoring

- The model is clear, the team agrees, the names match the business
- The cost of further refinement exceeds the benefit
- Stop until the next signal arrives
- "Refactor when you feel friction" is a useful heuristic

---
## Resistance to Refactoring

- "We don't have time to refactor"
- "It works, why change it?"
- "Senior management won't approve"
- All real; all overcome by tying refactoring to feature velocity

---
## Tying Refactoring to Features

- "This feature is hard because the model is wrong"
- "Refactoring will make this and the next three features easier"
- Bundle refactoring with feature work, not as separate sprints
- The business sees velocity; the team sees a healthy model

---
## Strategic Refactoring

- Bounded context boundaries change
- Two services merge or split
- Major: takes weeks-months; coordinate carefully
- Apply the strangler fig pattern: build new alongside, migrate gradually

---
## Watch for Hot Spots

- Areas of the codebase with frequent bugs
- Areas where every change is risky
- Areas the team avoids
- These are model-drift indicators

---
## Tools to Help

- Event storming workshops to re-explore the domain
- ADRs (Architecture Decision Records) to document why
- Static analysis to find patterns ripe for extraction
- Tests as a safety net for refactoring

---
## Anti-Patterns

- Refactoring in a separate branch that lives forever
- "Big rewrite" instead of incremental refactoring
- Refactoring without test coverage
- Refactoring that doesn't reflect the actual domain — just rearranging

---
## Course Recap

- Chapter 1: strategic design — bounded contexts, ubiquitous language
- Chapter 2: event storming for discovery
- Chapter 3: tactical building blocks
- Chapter 4: CQRS and event sourcing
- Chapter 5: sagas and process managers
- Chapter 6: hexagonal architecture and microservices
- Chapter 7: refactoring as discipline

---
## Where to Go From Here

- Pick one bounded context in your system
- Run an event storming on it
- Identify the aggregates, refine the language
- Refactor the code to match
- Repeat for the next context

---
## Recommended Reading

- Eric Evans, "Domain-Driven Design" (the original "blue book")
- Vaughn Vernon, "Implementing Domain-Driven Design" (the "red book")
- Vaughn Vernon, "Domain-Driven Design Distilled" (short intro)
- Alberto Brandolini's writing on event storming

---
## Summary

- DDD is iterative; refactoring is part of the practice
- Watch for model drift; refactor when you feel friction
- Tie refactoring to features for visible value
- Strategic refactoring (boundaries) is real but gradual
- The mature team treats the model as a living artifact
