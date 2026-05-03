---
tags:
  - concepts:solid
  - concepts:lsp
level: intermediate
category: design-patterns
audience:
  - audiences:developers

---
# Liskov Substitution Principle (LSP)

---
## With vs Without LSP

![lsp](svg/courses/principles/solid-clean-code/04_liskov_substitution_principle/lsp.svg)

---
## What This Chapter Covers

- Barbara Liskov's original formulation
- Behavioural subtyping in plain language
- The classic Square/Rectangle violation
- Other common violations
- Designing inheritance hierarchies that satisfy LSP

---
## The Principle, Stated Carefully

- "Subtypes must be substitutable for their base types"
- Anywhere `Base` works, any `Derived` should also work — *with the same observable behaviour*
- It's a *behavioural* contract, not just syntactic
- Originally from Barbara Liskov's 1987 keynote
- Reformulated by Robert Martin into the SOLID L

---
## What "Substitutable" Means

- Caller has a `Base` reference
- Caller invokes any method declared on `Base`
- The result must satisfy what `Base`'s contract promised
- The caller doesn't care which `Derived` it actually got
- If it does care, the hierarchy is wrong

---
## The Classic Violation

```python
class Rectangle:
    def __init__(self, w, h):
        self.w, self.h = w, h
    def set_width(self, w): self.w = w
    def set_height(self, h): self.h = h
    def area(self): return self.w * self.h

class Square(Rectangle):
    def set_width(self, w):
        self.w = self.h = w
    def set_height(self, h):
        self.w = self.h = h
```

---
## Why Square/Rectangle Breaks LSP

```python
def test_resize(r: Rectangle):
    r.set_width(5)
    r.set_height(3)
    assert r.area() == 15  # passes for Rectangle, fails for Square
```

- The test relies on a *Rectangle* contract: width and height are independent
- A `Square` violates that contract
- Hence Square is *not* a Liskov-valid subtype of Rectangle, despite the math
- "Square is a kind of Rectangle" works in geometry, not in mutable OOP

---
## Fixing It

- Don't subclass: `Square` and `Rectangle` are sibling shapes
- Pull up an immutable abstract `Shape` with `area()`
- Let neither inherit from the other
- Or: design both as immutable — `setWidth` returns a *new* shape
- Most violations get fixed by removing inheritance

---
## Other Common Violations

- **Throwing on inherited methods**: subclass refuses to do what base allowed
- **Strengthening preconditions**: subclass requires more than base
- **Weakening postconditions**: subclass delivers less than base
- **Side effects** that base didn't have
- **Type narrowing** — subclass returns a more specific type but the consumer relied on the base type's interface

---
## Violations At A Glance

![lsp_violations](svg/courses/principles/solid-clean-code/04_liskov_substitution_principle/lsp_violations.svg)

---
## Throwing on Inherited Methods

```python
class ReadOnlyList(List):
    def append(self, item):
        raise NotImplementedError("read-only")
```

- Any code that takes a `List` and calls `append` will crash on `ReadOnlyList`
- The hierarchy is wrong: ReadOnlyList is not a kind of List
- Fix: separate `ReadableList` and `MutableList` interfaces

---
## Strengthened Preconditions

```python
class Connection:
    def send(self, data: bytes): ...

class TLSConnection(Connection):
    def send(self, data: bytes):
        if not self.handshake_done:
            raise RuntimeError("must handshake first")
        ...
```

- Caller treats it as a `Connection` and calls `send`
- TLS variant adds a precondition the base didn't have
- Anyone who works with `Connection` is now broken when handed TLS
- Fix: do the handshake in the constructor, or expose a different type

---
## Behavioural Contracts

- A subtype must *honour* the base type's contract — not just match its signatures
- Document the contract: preconditions, postconditions, invariants
- LSP is a *behavioural* check, not a compiler check
- A class that compiles is not necessarily Liskov-valid
- Tests that exercise the base's contract on a subtype catch this

---
## Practical Tests

- Write tests against the *base type*
- Run them against every subtype
- All pass &#8594; LSP is intact
- Any fail &#8594; either fix the subtype or remove it from the hierarchy
- This is a low-cost discipline that prevents whole categories of bugs

---
## When LSP Is Hard

- Frameworks force you to extend a base class with awkward methods
- Override only what's needed; let the rest delegate to the base
- Sometimes the cleanest answer is: don't extend, wrap
- Wrapping (composition) gives you a fresh contract you control

---
## LSP Without Inheritance

- Same problem appears with interfaces and structural types
- A class implementing `Iterable` that throws on `next()` violates the contract
- A function that takes `Callable` but assumes a specific arity violates it
- LSP is really about *contracts*, not the inheritance keyword
- Apply the same thinking everywhere subtyping happens

---
## A Useful Heuristic

- If you find yourself overriding a method to do nothing, throw, or return null — your subtype probably violates LSP
- If the subtype needs to *expand* the base's permissive behaviour, fine
- If the subtype needs to *restrict* it, the hierarchy is wrong
- Subtypes should *strengthen* postconditions and *weaken* preconditions

---
## LSP and Other Principles

- OCP requires substitutable subtypes — without LSP, OCP breaks at runtime
- ISP reduces the surface area where LSP can be violated
- DbC formalises what LSP requires
- LSP without DbC is wishful thinking — write down the contracts

---
## Common Mistakes

- Inheriting "to reuse code" when there's no real "is-a" relationship
- Overriding methods to throw or return early
- Adding subclass-only state that breaks base assumptions
- Not testing the base contract against every subtype
- Treating LSP as a compile-time check rather than a behavioural one
