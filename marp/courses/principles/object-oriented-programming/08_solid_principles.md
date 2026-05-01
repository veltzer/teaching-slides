---
tags:
  - concepts:oop
  - concepts:solid
level: beginner
category: design-patterns
audience:
  - audiences:developers

---
# SOLID Principles

---
## What This Chapter Covers

- Where SOLID came from
- All five principles, briefly
- A worked example for each
- How they relate to each other
- Common code smells that signal a violation

---
## Where SOLID Came From

- Five principles, each named by an existing OOP pioneer
- Compiled by Robert C. Martin (Uncle Bob) in the early 2000s
- The acronym SOLID was coined later
- They're not laws; they're heuristics that have proven useful
- Read in order, they reinforce each other

---
## SOLID at a Glance

![solid_overview](svg/courses/principles/object-oriented-programming/08_solid_principles/solid_overview.svg)

---
## S: Single Responsibility Principle

- A class should have *one reason to change*
- Not "one thing it does" — one *axis of variation*
- Example: a `User` class that handles auth *and* profile rendering has two reasons to change
- Refactor: split into `AuthService` and `ProfileRenderer`
- Tells you *when* to split a class

---
## SRP Smell

- Methods that have nothing in common with each other
- Most edits to a class only touch one cluster of methods
- The class name needs an "and" or "or" to describe it
- Tests for the class are themselves split into clusters
- The class file is over 500 lines

---
## O: Open/Closed Principle

- Classes should be *open for extension*, *closed for modification*
- You add new behaviour without editing existing code
- Achieved through polymorphism, strategy, plug-ins
- Example: a `PaymentProcessor` that takes a list of `PaymentMethod` strategies
- Adding crypto support means a new class, not editing the processor

---
## OCP Smell

- Long `if/elif` (or `switch`) chains that grow each release
- Every new feature requires editing the same central class
- "I have to update this in 4 places to add X"
- Bug-fix touches a class far from the feature being added
- The fix: extract the variation behind an interface

---
## L: Liskov Substitution Principle

- Subtypes must be substitutable for their base types
- Anywhere `Base` is expected, any `Derived` should work the same
- The classic violation: `Square extends Rectangle`
- Setting `setWidth(5)` on a Square must also change height — breaks code that expected independence
- The base class's *behavioural contract* must be honoured

---
## LSP Worked Example

```python
class Bird:
    def fly(self): ...

class Penguin(Bird):
    def fly(self):
        raise NotImplementedError("penguins don't fly")
```

- Penguin breaks any caller that depends on `Bird.fly` working
- The hierarchy is wrong — flying isn't intrinsic to *all* birds
- Fix: split into `Bird` and `FlyingBird`, or use composition

---
## I: Interface Segregation Principle

- Clients should not be forced to depend on methods they do not use
- A "fat" interface that bundles many capabilities forces every implementer to handle all of them
- Split into many small interfaces; clients depend on only what they need
- Java's `Iterable` is well-segregated; old AWT had nightmare-fat interfaces

---
## ISP Worked Example

```java
// Bad: every Worker must implement eat()
public interface Worker {
    void work();
    void eat();
}

// Good: separate
public interface Workable { void work(); }
public interface Feedable  { void eat(); }
```

- A robot worker now implements only `Workable`
- Clients depending on `Workable` don't see `eat`
- Each interface evolves independently

---
## D: Dependency Inversion Principle

- High-level modules shouldn't depend on low-level modules; both should depend on *abstractions*
- Abstractions shouldn't depend on details; details should depend on abstractions
- In practice: code to interfaces, not concrete classes
- Inject the concrete implementation from the outside
- Pairs naturally with dependency injection frameworks

---
## DIP Worked Example

Before (high-level depends on low-level):
```python
class OrderService:
    def __init__(self):
        self._db = PostgresDB()  # concrete
```

After (both depend on abstraction):
```python
class OrderService:
    def __init__(self, db: Database):  # abstract
        self._db = db
```

- Now `OrderService` works with any `Database` impl
- Easy to test with an in-memory fake

---
## How They Reinforce Each Other

- **S**RP gives you small focused classes
- **O**CP needs polymorphism &#8594; needs **L**SP to work safely
- **I**SP keeps the polymorphic interfaces small
- **D**IP makes those interfaces injectable
- Following one well usually pulls the others along

---
## SOLID Is Not Religion

- These are *heuristics*, not laws
- Bad: applying every principle to every class blindly
- Good: noticing a smell and *picking* the right principle to address it
- Bad SOLID code can be over-engineered, abstract for its own sake
- Aim for *understandable* code; SOLID is one tool

---
## Common Mistakes

- Splitting a class into 12 microclasses to "follow SRP" — now nothing makes sense
- Adding interfaces with one implementation "for OCP"
- Naming things `IFooFactory` because the book said so
- Overusing dependency injection until every class needs a container to construct
- Treating LSP as a syntactic check (does it compile?) rather than behavioural
