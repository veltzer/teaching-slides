---
tags:
  - concepts:clean-code
  - concepts:refactoring
level: intermediate
category: design-patterns
audience:
  - audiences:developers

---

# Advanced Clean Code Techniques

---

## What This Chapter Covers

- Error handling patterns
- Avoiding deep nesting
- DRY: when it helps and when it hurts
- YAGNI and over-engineering
- Code metrics worth tracking
- Approaching legacy code

---

## Error Handling: Two Schools

- **Exceptions**: errors are flow-changing events (Java, Python, C#)
- **Errors as values**: errors are returned (Go, Rust)
- Both can produce clean code; both can produce a mess
- The trick is *consistency* within a codebase
- Pick one and apply it everywhere

---

## Exception Patterns

- Throw exceptions for *exceptional* conditions, not control flow
- Catch only what you can handle
- Don't catch a broad `Exception` and ignore it
- Add context as you re-throw: chain exceptions instead of swallowing
- Log at the boundary, not at every layer

---

## Errors as Values

```go
result, err := db.Save(order)
if err != nil {
    return fmt.Errorf("save order: %w", err)
}
```

- Every fallible call returns an error
- Caller decides how to handle it
- More verbose, more explicit, no surprises in control flow
- Wrap errors with context as they propagate

---

## Avoiding Deep Nesting

```python
# painful
def process(req):
    if req.is_valid():
        if req.user.has_permission("write"):
            if req.body:
                # actual work
                pass
```

- Three levels of nesting before any work
- Hard to read, hard to test, hard to change
- Each `if` should ideally be a guard or an early return

---

## Refactor: Early Returns

```python
def process(req):
    if not req.is_valid():
        return error("invalid")
    if not req.user.has_permission("write"):
        return error("forbidden")
    if not req.body:
        return error("empty")

    # actual work, at the top level
```

- Failure cases handled and dismissed up front
- Happy path lives at the lowest indentation
- Readable top to bottom

---

## DRY: Don't Repeat Yourself

- Don't duplicate *knowledge* — the same fact in two places
- Single business rule should live in one function
- Single magic value should live in one constant
- *Coincidental* duplication is fine — two pieces of code that *happen* to look alike but mean different things
- The wrong DRY couples unrelated things; the right DRY decouples them

---

## DRY Done Wrong

```python
# trying too hard
def safe_divide(a, b):
    return a / b if b != 0 else 0

result = safe_divide(x, y)
```

- The "safety" was needed *once*; everywhere else uses the helper without thinking
- Hides the real assumption ("divide by zero is fine, returns 0")
- Forces every caller to know about the helper
- Sometimes inline is clearer

---

## KISS: Keep It Simple

- Resist the urge to add cleverness
- Two simple solutions beat one complicated one
- Frameworks added "in case we need them" rarely pay back
- A junior developer should be able to follow your code
- Simple isn't easy — it takes work to *strip down* to the essentials

---

## YAGNI: You Aren't Gonna Need It

- Don't add a feature until it's actually needed
- Don't add a configuration option until two real configurations exist
- Don't add a plugin point until the second plugin shows up
- Speculative flexibility is the most common form of waste
- When the need arrives, *then* add — informed by what's actually needed

---

## Cyclomatic Complexity

- Counts the number of independent execution paths through a function
- Each `if`, `for`, `while`, `case` adds 1
- Above ~10, the function is hard to test thoroughly
- Above ~20, something is wrong with the design
- Tools (radon, SonarQube, ESLint) report it for free

---

## Code Coverage

- The percentage of code lines (or branches) executed by tests
- Useful as a *floor*, not a goal
- 80% coverage is a reasonable target for most teams
- 100% coverage doesn't mean bug-free — it means nothing was *uncovered*
- Coverage on dead code is fake comfort

---

## Maintainability Index

- A composite score of complexity, comment density, and code volume
- Various tools compute it (Visual Studio, SonarQube, radon)
- Useful as a relative measure across files
- Useful as a trend line over time
- Don't game it; use it to find the worst-offending files

---

## Reading Legacy Code

- Start with the tests — they document intent
- If there are no tests, *write characterisation tests* before changing anything
- Read the git log — what change happened and why?
- Resist the urge to refactor everything at once
- The boy scout rule: leave it cleaner than you found it

---

## The Strangler Fig Pattern

- Wrap legacy code in a new interface
- Move callers to the new interface
- Replace the legacy implementation behind the interface, piece by piece
- When all callers use the new interface, delete the legacy
- Refactoring without big-bang risk

---

## Refactoring with Tests

- Refactoring without tests is gambling
- Even small renames break things in ways the compiler doesn't catch
- Tests are the safety net that lets you move quickly
- A team without tests refactors slowly out of fear
- Add tests *before* refactoring; refactor *with* tests as your sensor

---

## A Sustainable Pace

- Clean code is built incrementally, every commit
- Don't schedule "refactoring sprints"; refactor as you go
- The boy scout rule applied daily beats heroic cleanups
- Saying "no" to features is part of clean-code discipline
- Quality is a long game

---

## Course Wrap-Up

- SOLID is heuristics, not commandments
- Apply them when you smell trouble
- Clean code is a discipline, not a checklist
- Good naming, small functions, focused classes — these compound
- The team that takes the time to read each other's code writes the cleanest code

---

## Refactoring Workflow

![refactoring_steps](svg/courses/principles/solid-clean-code/08_advanced_clean_code_techniques/refactoring_steps.svg)

---

## Levels of Duplication

![dry_levels](svg/courses/principles/solid-clean-code/08_advanced_clean_code_techniques/dry_levels.svg)
