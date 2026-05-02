---
tags:
  - concepts:oop
  - concepts:composition
  - concepts:inheritance
level: beginner
category: design-patterns
audience:
  - audiences:developers

---
# Composition vs Inheritance

---
## What This Chapter Covers

- "Has-a" vs "is-a" relationships
- Delegation patterns
- Why "favour composition" became a maxim
- Mixins and traits
- Refactoring inheritance to composition
- A practical decision guide

---
## Has-A vs Is-A

- **Is-a**: a Dog *is an* Animal &#8594; inheritance candidate
- **Has-a**: a Car *has an* Engine &#8594; composition
- "Is-a" is rarer than it looks — many things that *seem* "is-a" are actually "behaves-like"
- "Has-a" is the safer default
- When in doubt: it's probably has-a

---
## Side by Side

![composition_over_inheritance](svg/courses/principles/object-oriented-programming/07_composition_vs_inheritance/composition_over_inheritance.svg)

---
## Composition: A First Example

```python
class Engine:
    def start(self): ...

class Car:
    def __init__(self, engine):
        self._engine = engine

    def start(self):
        self._engine.start()
```

- `Car` *holds* an `Engine`, doesn't extend it
- The Engine can be swapped at construction time
- Easy to test: pass a fake Engine

---
## The Same Idea With Inheritance (Don't)

```python
class Car(Engine):
    pass
```

- Conceptually wrong: a Car is not a kind of Engine
- Inherits everything Engine has, including state
- Can't swap engines without changing the Car class
- Probably a chain of inheritance hacks ahead

---
## Delegation

- An object holds another object and *delegates* method calls to it
- Looks like inheritance from the outside (same method names)
- Behaves better: you control which calls are forwarded, can add behaviour
- Adapter, Decorator, Proxy patterns are all flavours of delegation
- The verbose-but-explicit option

---
## "Favour Composition Over Inheritance"

- A guideline from *Design Patterns* (Gang of Four, 1994)
- Inheritance couples subclass tightly to superclass implementation
- Composition couples to a *contract* (the interface)
- Composition is more flexible, easier to test, easier to refactor
- Not a hard rule — inheritance has uses — but the right default

---
## Mixins

- Small classes that add a *capability*, not an identity
- Composed via multiple inheritance in Python, traits in Scala/Rust
- Example: `Comparable`, `Serializable`, `LoggingMixin`
- Each mixin is independent; objects pick what they need
- Used carefully, mixins are composition with inheritance syntax

---
## A Mixin in Python

```python
class TimestampMixin:
    def __init__(self):
        self.created_at = datetime.utcnow()

class Article(TimestampMixin):
    def __init__(self, title):
        super().__init__()
        self.title = title
```

- The Article gets a `created_at` for free
- The mixin doesn't define identity, just a capability
- Order of base classes matters — uses Python's MRO

---
## Refactoring Inheritance to Composition

- Find the inherited methods you actually use
- Extract them into a helper class
- Hold the helper as a field
- Forward calls (delegate) where needed
- Remove the inheritance link

---
## A Refactoring Example

Before:
```python
class FileWriter(BaseLogger):
    def log(self, msg):
        self.write(self.format(msg))
```

After:
```python
class FileWriter:
    def __init__(self, formatter):
        self._formatter = formatter

    def log(self, msg):
        self._write(self._formatter.format(msg))
```

- Decoupled from the BaseLogger hierarchy
- Formatter is now swappable

---
## When Inheritance Is the Right Choice

- The relationship really is "is-a" in the domain
- Subclasses won't violate the parent's contract
- The base class was *designed* for inheritance
- The base class is in your codebase — you control its evolution
- You're using a framework that requires extending a base class

---
## When Composition Is the Right Choice

- You want code reuse without identity
- You want to be able to swap implementations
- You want to mix multiple capabilities
- You want to test the consumer in isolation
- You're not sure (most cases) — start here

---
## Quick Decision Guide

- "Is this thing a *kind of* the other?" &#8594; consider inheritance
- "Does this thing *use* or *have* the other?" &#8594; composition
- "Will I need to swap implementations?" &#8594; composition
- "Is the thing on the right a stable, well-designed base class?" &#8594; inheritance OK
- "Does the relationship feel forced?" &#8594; composition

---
## A Practical Pattern: Strategy

```python
class SortStrategy(Protocol):
    def sort(self, items: list) -> list: ...

class Catalog:
    def __init__(self, strategy: SortStrategy):
        self._strategy = strategy

    def list_products(self):
        return self._strategy.sort(self._products)
```

- The varying behaviour (how to sort) is *injected*
- Add new strategies without touching `Catalog`
- Test with a stub strategy
- Pure composition, zero inheritance

---
## Common Mistakes

- Reaching for inheritance because two classes share a method name
- Building a hierarchy three levels deep before noticing the smell
- Mixin chains that are hard to follow
- Composition without depending on an abstraction (just hardcoding the helper class)
- Reflexively rewriting all inheritance into composition — both are tools
