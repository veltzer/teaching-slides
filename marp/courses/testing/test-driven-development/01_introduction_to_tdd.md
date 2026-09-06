---
tags:
  - practices:tdd
level: intermediate
category: testing
audience:
  - audiences:developers

---

# Introduction to TDD

---

## What This Chapter Covers

- What TDD is, in one sentence
- A short history
- The red-green-refactor cycle
- Benefits and trade-offs
- TDD vs test-after development
- When to use TDD; when not to

---

## The Cycle

![red_green_refactor](svg/courses/testing/test-driven-development/01_introduction_to_tdd/red_green_refactor.svg)

---

## TDD Benefits

![tdd_benefits](svg/courses/testing/test-driven-development/01_introduction_to_tdd/tdd_benefits.svg)

---

## What TDD Is

- Write a failing test first
- Write the smallest code that passes the test
- Refactor with the test as a safety net
- Repeat
- Each step is small; the rhythm is the point

---

## A Short History

- Test-first ideas appeared in early software (NASA, defence)
- Kent Beck popularised TDD with Extreme Programming (late 1990s)
- His book *Test-Driven Development By Example* (2003) is canonical
- The discipline spread; the practice less so
- Many teams "do TDD" sporadically; few do it continuously

---

## The Red-Green-Refactor Cycle

- **Red**: write a failing test
- **Green**: write the minimum code to pass
- **Refactor**: improve the design without changing behaviour
- Cycle measured in *minutes*, not hours
- Run the test suite hundreds of times a day

---

## Benefits

- Built-in test coverage
- Forces design pressure (untestable code = redesign)
- Catches regressions immediately
- Documentation by example (tests show usage)
- Confidence to refactor

---

## Trade-Offs

- Slower in the short term
- Hard to apply to discovery-phase code
- Hard to apply to UI / integration boundaries
- Requires discipline; easy to slip
- Some types of code resist (algorithmically complex, throwaway scripts)

---

## TDD vs Test-After

- Test-after: write code; then write tests
- Tests-after produce coverage, not design
- TDD's value is the *design* feedback, not the tests
- Test-after is still better than no tests
- Both have a place; pick deliberately

---

## When TDD Wins

- Small, focused units (functions, classes)
- Clear inputs and outputs
- Pure logic, deterministic
- New code in a familiar domain
- Bug fixes (write a failing test for the bug, then fix)

---

## When TDD Loses

- Exploratory work where you don't yet know the design
- UI prototypes
- Integration code that depends on external systems
- Algorithmic research where the spec is unclear
- One-off scripts you'll throw away

---

## Where TDD Pays Off

![when_tdd_wins](svg/courses/testing/test-driven-development/01_introduction_to_tdd/when_tdd_wins.svg)

---

## TDD Is Not Testing

- Testing is verifying correctness; TDD is a *design* method
- The tests are a side effect; the design is the goal
- Stop calling it "test-first" and call it "design-first"
- This reframe helps people get past "I know how to test"
- It's about the rhythm, not the artifact

---

## A Simple Example

- Write a test: `assert add(2, 3) == 5`
- Run it: fails (no `add` function)
- Write the code: `def add(a, b): return a + b`
- Run it: passes
- Refactor (nothing to refactor here): done
- Cycle complete in 30 seconds

---

## Triangulation

- Sometimes you write the simplest code that passes the *first* test
- It's wrong for the general case
- Add a *second* test that exposes the limitation
- Now you must generalise
- Triangulation forces correctness

---

## Triangulation Example

- Test 1: `add(2, 3) == 5`. Code: `return 5`. Passes.
- Test 2: `add(1, 1) == 2`. Code: `return a + b`. Both pass.
- The naive `return 5` was forced out by the second test
- Toy example; real problems benefit similarly

---

## Triangulation Strategy

![triangulation](svg/courses/testing/test-driven-development/01_introduction_to_tdd/triangulation.svg)

---

## TDD Doesn't Mean Tiny Steps

- Beck's book emphasises baby steps
- Modern practitioners take bigger steps when confident
- Steps should match your *certainty*
- Confused: small steps. Confident: bigger.
- Calibrate over time

---

## Common Misconceptions

- "TDD slows me down" — true short-term, false long-term
- "I do TDD; my tests run after my code" — that's test-after
- "TDD = high coverage" — coverage is a side effect
- "TDD prevents bugs" — reduces them; doesn't eliminate
- "TDD is dogma" — pragmatism still applies

---

## What's Next

- The red-green-refactor cycle in depth
- Unit testing foundations
- Test doubles, mocks, stubs
- BDD: a different lens
- Test architecture
- Refactoring with tests
