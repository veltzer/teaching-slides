---
tags:
  - practices:tdd
  - practices:refactoring
level: intermediate
category: testing
audience:
  - audiences:developers

---
# Refactoring With Tests

---
## What This Chapter Covers

- What refactoring is
- Why tests enable refactoring
- Common refactoring patterns
- The strangler pattern for legacy code
- Characterisation tests
- Continuous refactoring as part of TDD

---
## What Refactoring Is

- Changing the structure of code without changing behaviour
- Improvements: readability, modularity, performance
- Small, safe steps
- Tests verify behaviour preserved
- Coined / popularised by Martin Fowler

---
## Tests as Safety Net

![refactor_safety](svg/courses/testing/test-driven-development/08_refactoring_with_tests/refactor_safety.svg)

---
## Why Tests Matter

- Without tests: refactor by faith, hope it still works
- With tests: refactor; run tests; if green, behaviour preserved
- Tests are the safety net
- Refactoring without tests is gambling
- Even simple renames break things in subtle ways

---
## Common Refactoring Patterns

- **Extract Method**: pull a chunk of code into its own method
- **Inline Method**: opposite; merge a method back into its caller
- **Rename**: better names; safer with IDE support
- **Move Method**: a method belongs on another class
- **Extract Class**: a class is doing too much; split

---
## Extract Method

```python
# Before
def process(order):
    if order.total > 1000:
        order.discount = order.total * 0.1
    save(order)

# After
def process(order):
    apply_discount(order)
    save(order)

def apply_discount(order):
    if order.total > 1000:
        order.discount = order.total * 0.1
```

---
## Inline Method

```python
# Before
def get_rating(driver):
    return more_than_five_late_deliveries(driver) and 1 or 2

def more_than_five_late_deliveries(driver):
    return driver.late_deliveries > 5

# After (inline if it's only used once and is simpler inline)
def get_rating(driver):
    return (driver.late_deliveries > 5) and 1 or 2
```

---
## Rename

- The simplest, most underrated refactor
- IDEs do this safely
- Old name &#8594; new name everywhere
- A bad name fixed today saves hours next year
- Default to renaming when you understand a thing better

---
## Move Method

- A method that uses another class's data more than its own
- Move it to that class
- Reduces coupling
- "Feature envy" smell &#8594; this refactor

---
## Extract Class

- A class doing two things
- Split into two classes
- Each with focused responsibility
- Often follows: noticing methods that don't share state with others
- A SOLID-driven refactor (Single Responsibility)

---
## The Strangler Pattern

- For replacing legacy code
- Build the new alongside the old
- Migrate callers one at a time
- When all migrated, delete the old
- Coined by Martin Fowler; named after strangler-fig vines

---
## Characterisation Tests

- For untested legacy code
- Write tests that capture *current* behaviour
- "If I run this with X, I get Y" (whatever Y is)
- Now safe to refactor
- Working Effectively with Legacy Code (Feathers) is the canonical reference

---
## Working With Untested Code

- Don't change anything until you have tests
- Find a "seam" — a place where behaviour can be observed
- Write tests at that seam
- Refactor inside the seam
- Repeat: peeling layers, like a programming-archaeology dig

---
## Safe Refactoring Workflow

- Run all tests; ensure green
- Make one small change
- Run all tests; ensure still green
- Commit (or stash for now)
- Repeat

---
## When Tests Fail Mid-Refactor

- Don't power through
- The refactor introduced a behaviour change (probably)
- Revert the last step; try smaller
- Or: question whether the test was right
- Don't suppress tests to make them pass

---
## Continuous Refactoring

- Part of every cycle (TDD's third step)
- Tiny improvements add up
- The codebase gets better, not worse, over time
- Without it: tech debt accretes silently
- With it: the codebase stays workable for years

---
## When NOT To Refactor

- Tests are red
- Right before a deploy
- Code about to be deleted
- When the refactor doesn't actually improve anything
- Pick your moments; don't refactor everything

---
## Refactoring vs Adding Features

- Don't mix them
- Refactor first; commit; then add the feature; commit
- One PR per refactor
- Reviewers can see exactly what changed
- "Refactor + feature" PRs are nightmare to review

---
## Common Refactoring Mistakes

- Refactoring without tests
- Big-bang refactor over a week
- Refactoring + feature in one PR
- Renaming things to your personal preference
- Premature abstraction (refactoring to support a feature you don't need yet)
