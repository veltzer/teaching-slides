---
tags:
  - practices:tdd
  - practices:advanced
level: intermediate
category: testing
audience:
  - audiences:developers
  - audiences:architects

---
# Advanced TDD Practices

---
## What This Chapter Covers

- Outside-in vs inside-out TDD
- London school vs Detroit school
- Property-based testing and TDD
- Acceptance TDD (ATDD)
- Continuous integration and TDD
- Code review for test quality

---
## Outside-In TDD

- Start at the user-facing layer
- Write a failing acceptance test
- Drill down: write failing unit tests as you discover collaborators
- Also called "double-loop TDD"
- Common in BDD-style work

---
## Advanced Tools

![advanced_tdd](svg/courses/testing/test-driven-development/10_advanced_tdd_practices/advanced_tdd.svg)

---
## Inside-Out TDD

- Start at the lowest level (a class, a function)
- Build outward as needs emerge
- Discover the architecture as you go
- The classic Beck-style TDD
- Common in functional / library code

---
## When To Use Each

- Outside-in: feature-driven work; clear user goals
- Inside-out: foundational work; library design
- Most teams blend both depending on the task
- Don't dogmatise; use what fits

---
## London School TDD

- Heavy use of mocks
- Test interactions between objects
- "Tell, don't ask" object communication
- Tests as specifications of object behaviour
- Originated in London (XtC)

---
## Detroit / Chicago School TDD

- Use real objects where practical
- Test state, not interactions
- Mocks only at boundaries
- Tests as specifications of system behaviour
- Originated in the US (Beck, Jeffries)

---
## Picking A School

- Mostly preference; both work
- London tests fail more often on refactors (more brittle)
- Detroit tests give more confidence in real behaviour
- Mock-heavy codebases tend toward London naturally
- Object-state-rich codebases lean Detroit

---
## Property-Based Testing

- Define properties (invariants) that should hold
- Framework generates many random inputs
- Tries to find an input that violates the property
- Shrinks failures to minimal counterexamples
- Hypothesis (Python), QuickCheck (Haskell), fast-check (JS)

---
## Property-Based + TDD

- Use property-based for general properties
- Use example-based for specific cases
- Mix freely
- Property tests catch what examples miss
- Especially powerful for parsers, protocols, math

---
## Acceptance TDD (ATDD)

- Write the acceptance criteria as tests *first*
- Done together by stakeholders, testers, devs
- Fail in the beginning; pass when feature complete
- The feature is "done" when its ATDD tests pass
- Closely related to BDD

---
## ATDD Workflow

- Three Amigos meeting: business + dev + tester
- Write the scenarios as Gherkin
- Devs implement step definitions
- TDD inside to make them pass
- Done when scenarios green and stakeholder accepts

---
## Continuous Integration and TDD

- TDD without CI: half the value
- CI runs all tests on every push
- Fast feedback on integration failures
- TDD + CI = hard to push broken code
- The feedback loop the discipline depends on

---
## Speed Of CI Matters

- Slow CI &#8594; people skip it
- Aim: under 10 minutes for unit + integration
- Parallelise; cache aggressively; optimise often
- Slow tests get retried, ignored, or worked-around
- Your CI speed is your TDD speed

---
## TDD And Code Review

- Reviewers should check: tests exist, tests are good
- A failing test for a fix is the strongest signal
- Watch for: tests that always pass (no real assertion)
- Watch for: low-quality tests with high coverage
- Test quality matters more than quantity

---
## Mutation Testing

- Tools introduce small mutations to the production code
- Run tests; should fail
- "Surviving mutants" = tests didn't catch the mutation = weak tests
- Tools: PIT (Java), Stryker (JS), mutmut (Python)
- A way to grade your test suite

---
## Why Mutation Testing

- Coverage tells you what was *executed*
- Mutation tells you what was *checked*
- Different metric; harder to game
- Slow; run periodically rather than every commit
- A revelation if you've never tried it

---
## Test Smells

- Long setup
- Test depends on another test
- Test does too many things
- Test name vague
- Test assertions buried in helpers
- Each is a flag for refactoring

---
## Refactoring Tests

- Tests are code; they need maintenance too
- Apply TDD principles to test code
- Extract helpers, name things well, keep them small
- Don't tolerate test smells
- A clean test suite makes TDD enjoyable

---
## When TDD Gets Hard

- The design is wrong; tests fight you
- Listen to the tests
- "This is hard to test" usually means "this is poorly designed"
- Refactor toward testability; refactor toward simplicity
- TDD is a design pressure

---
## TDD Habits That Compound

- Test first; *every* time
- Run tests after every change
- Refactor in green
- One commit per cycle
- After a year of practice, it feels natural
- After two years, you can't imagine working without it

---
## Course Wrap-Up

- TDD is a design discipline, not a testing technique
- Red-green-refactor; tiny cycles; constant feedback
- Test doubles, mocks, fakes — pick the right tool
- BDD adds stakeholder visibility
- Architecture matters: pyramid, fast unit tests, real CI
- Refactoring with tests is what keeps codebases alive
- Practice makes the difference; many engineers know about TDD; few do it
