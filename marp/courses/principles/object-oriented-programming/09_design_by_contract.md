---
tags:
  - concepts:oop
  - concepts:contracts
level: beginner
category: design-patterns
audience:
  - audiences:developers

---

# Design by Contract

---

## What This Chapter Covers

- The idea: methods as contracts
- Preconditions, postconditions, invariants
- Defensive programming and its alternative
- Assertions vs validation
- Where DbC fits in modern languages

---

## The Contract Metaphor

- A method has obligations and promises, like a legal contract
- Caller's obligations: meet the **preconditions**
- Callee's promises: deliver the **postconditions**
- Class itself maintains **invariants** between method calls
- Coined by Bertrand Meyer for the Eiffel language (1980s)

---

## Three Clauses

![contract_clauses](svg/courses/principles/object-oriented-programming/09_design_by_contract/contract_clauses.svg)

---

## Preconditions

- What must be true *before* a method runs
- Example: `Stack.pop()` requires the stack be non-empty
- Caller is responsible for meeting them
- If the precondition is violated, behaviour is undefined
- Document them clearly; modern langs use type hints, asserts, or annotations

---

## Postconditions

- What the method *guarantees* after returning
- Example: after `Stack.push(x)`, `top()` returns `x` and `size` increased by 1
- Method is responsible for delivering them
- Failure to deliver = bug in the method
- Tests should cover the contract, not the implementation

---

## Invariants

- Conditions that must hold at *every visible state* of the object
- Example: an `Account` invariant — "balance &#8805; 0"
- Methods can violate the invariant temporarily *during* execution
- They must restore it before returning
- Construction must establish it; destruction can leave it in any state

---

## A Worked Example

```python
class BoundedQueue:
    def __init__(self, capacity):
        # invariant: 0 <= len(self._items) <= capacity
        self._capacity = capacity
        self._items = []

    def push(self, x):
        # precondition: len(self._items) < self._capacity
        # postcondition: len(self._items) == old(len) + 1
        assert len(self._items) < self._capacity
        self._items.append(x)
```

---

## Defensive Programming

- Every method validates *all* its inputs and protects against bad data
- Lots of repeated checks at every layer
- Result: noisy code, slow code, scattered error handling
- Often defends against impossible states
- The "everyone is suspicious of everyone" model

---

## Contract-Based Programming

- Each method states what it requires and what it delivers
- Validation happens *at the boundary* — once
- Internal methods trust their callers
- Failures of internal contracts are *bugs*, not user errors
- The "trust within the system, validate at the edge" model

---

## Assertions vs Validation

- **Assertions**: checks for *programmer errors* (something we believed was true wasn't)
- **Validation**: checks for *user errors* (untrusted input)
- Assertions can be disabled in production (Python `-O`, Java `-da`)
- Validation must always run
- Don't confuse the two — they have different audiences

---

## Where to Validate

- At the boundaries: API endpoints, message receivers, file readers
- Once data is past the boundary, treat it as trusted
- The middle of the system uses assertions for its own consistency
- Internal modules don't re-validate what the boundary already checked
- This dramatically simplifies internal code

---

## Failing Loudly

- A failed precondition is a bug in the caller
- A failed postcondition is a bug in the callee
- A failed invariant is a bug somewhere — class is corrupted
- *Crash early* is better than *limp along*
- Modern languages: throw, raise, panic — don't silently continue

---

## DbC in Mainstream Languages

- Eiffel: native syntax for `require`, `ensure`, `invariant`
- Java: JML (Java Modeling Language) — academic, rarely used
- C++: contracts proposed for C++23, then withdrawn
- Python: assertions + type hints + docstrings
- Most teams encode contracts in *tests* and naming

---

## DbC and Inheritance

- Subclasses can *weaken* preconditions (accept more)
- Subclasses can *strengthen* postconditions (deliver more)
- Subclasses cannot *strengthen* preconditions (would break callers)
- Subclasses cannot *weaken* postconditions (would break callers)
- This is exactly the Liskov Substitution Principle

---

## Practical Patterns

- Document contracts in docstrings or method comments
- Express preconditions as type hints where possible
- Use assertions for "this can't happen" checks
- Use named exceptions for documented error conditions
- Pair contract-style code with property-based testing

---

## Common Mistakes

- Defensive code at every layer — repeats checks pointlessly
- Catching `AssertionError` to "be robust" — defeats the point
- Throwing the same exception type for caller-error and runtime-error
- Documenting contracts only in your head
- Validating in three places, none of them the boundary
