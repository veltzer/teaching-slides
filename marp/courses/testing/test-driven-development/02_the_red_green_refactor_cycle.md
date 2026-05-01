---
tags:
  - practices:tdd
level: intermediate
category: testing
audience:
  - audiences:developers

---
# The Red-Green-Refactor Cycle

---
## What This Chapter Covers

- Writing the first failing test
- Making the test pass with minimal code
- Refactoring for clean design
- Iterating through the cycle
- Triangulation and generalisation
- Step size: baby vs large

---
## Red: Write A Failing Test

- Pick the smallest possible behaviour to add
- Write the test
- Run it
- Confirm it fails — and *why* it fails
- A test that passes immediately tells you nothing

---
## Why The Failure Matters

- Confirms the test is actually testing something
- Tests that always pass = useless tests
- A green test for code that doesn't exist is suspicious
- Failure messages should be informative
- Treat the failure as feedback

---
## Green: Make It Pass

- Write the *minimum* code to pass
- Don't generalise yet
- Don't add features the test didn't ask for
- "Fake it till you make it" is allowed
- Speed over elegance for now

---
## "Fake It Till You Make It"

- Test: `add(2, 3) == 5`. Code: `return 5`.
- Yes, that passes
- Not the final code; just a step
- Triangulation will force the general solution
- Trains you to take small steps

---
## Refactor: Improve Without Breaking

- Tests still pass after each refactor
- One refactor at a time
- Run tests between each
- Common refactors: extract method, rename, move, inline
- Don't add features in the refactor step

---
## A Cycle in Practice

```python
# RED
def test_add():
    assert add(2, 3) == 5  # fails: NameError

# GREEN
def add(a, b):
    return 5              # passes (cheating)

# RED again (triangulation)
def test_add_other():
    assert add(1, 1) == 2  # fails

# GREEN
def add(a, b):
    return a + b           # passes both

# REFACTOR
# already clean; nothing to do
```

---
## When To Refactor

- After every green
- Before adding the next feature
- The "boy scout rule": leave code cleaner than you found it
- Refactoring is part of the cycle, not optional
- Skip it and tech debt accumulates

---
## When NOT To Refactor

- When you're about to throw away the code
- When the design is going to change anyway in the next test
- When you're under tight time pressure (note for later)
- When the refactor doesn't improve the design
- When tests don't cover the behaviour

---
## Cycle Times

- Per cycle: 1-5 minutes typical
- Failed tests should fail in seconds
- Test suite should run in seconds
- Slow tests break the rhythm
- Investment in fast tests pays back many times

---
## Step Size: Baby

- New domain, unfamiliar territory
- Hard problem
- Working with a partner / pair-programming
- When tests are slow (each cycle costs more)
- When confidence is low

---
## Step Size: Big

- Familiar domain
- Easy problem
- Working alone, in flow
- Fast tests
- High confidence

---
## When You Get Stuck

- Tests not passing? Write a *smaller* test
- Tests too complex? The design is fighting you
- "I don't know what to test next" — pick the next user-facing behaviour
- Stuck means: take smaller steps
- Don't push through; back up

---
## Generalisation

- After triangulation, generalise the implementation
- "Both tests pass with `return a + b`" — the general form
- Sometimes obvious; sometimes the third or fourth test forces it
- Don't generalise too soon (premature design)
- Don't avoid generalising (technical debt)

---
## Tracking Progress

- A list of tests-to-write
- Cross out each as you implement
- New tests come up; add them
- The list shapes your priorities
- An informal but powerful habit

---
## Cycle Discipline

- Every cycle: red, green, refactor
- Don't skip refactor (the design rots)
- Don't skip red (tests become coverage theatre)
- Don't skip green (just write tests; never solving the problem)
- Discipline pays off over months and years

---
## Common Cycle Mistakes

- Writing multiple tests at once (lose feedback)
- Writing more code than the test demands
- Skipping refactor "this time"
- Tests that pass for the wrong reason
- "Just one more feature before the next test"
