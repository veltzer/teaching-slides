---
tags:
  - concepts:design-patterns
  - concepts:creational-patterns
level: intermediate
category: design-patterns
audience:
  - audiences:developers

---

# Creational Design Patterns

---

## Patterns Overview

![creational_patterns](svg/courses/design_patterns/design-patterns/02_creational_design_patterns/creational_patterns.svg)

---

## What This Chapter Covers

- Five patterns that *create* objects with intent
- Singleton, Factory Method, Abstract Factory, Builder, Prototype
- For each: intent, structure, code, when to use, trade-offs
- A short worked example that uses two of them together

---

## Why Creational Patterns

- Object construction often does more than `new`
- It picks the right concrete type based on context
- It validates inputs and enforces invariants
- It manages shared resources or pools
- Pulling these concerns out of consumers makes the code cleaner

---

## Creational Patterns Compared

![factories_compared](svg/courses/design_patterns/design-patterns/02_creational_design_patterns/factories_compared.svg)

---

## Singleton

- *Intent*: ensure a class has exactly one instance, give global access
- Use for: configuration objects, logging, connection pools
- Misuse for: anything that benefits from being a regular instance
- The most overused pattern — start by *not* using it

---

## Singleton in Code

```python
class Logger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```

- Construct returns the same object every time
- Java equivalent: private constructor + static getInstance
- Modern preference: dependency injection over Singleton

---

## Singleton Trade-offs

- Pro: guaranteed single instance, easy access
- Con: hidden dependency — code that uses it has invisible coupling
- Con: hard to test — can't substitute it
- Con: bad with concurrency unless explicitly synchronised
- If you need shared state, an injected service is usually better

---

## Factory Method

- *Intent*: defer instantiation to subclasses
- The base class declares "make a Product" but doesn't pick which kind
- Subclasses override to pick the concrete Product
- Useful when a framework needs to create objects of types it doesn't know
- "Open for extension" without modifying the framework

---

## Factory Method in Code

```python
class Document(ABC):
    def open(self):
        pages = self._read_pages()  # subclass decides type
        ...
    @abstractmethod
    def _read_pages(self): ...

class PdfDocument(Document):
    def _read_pages(self): return [PdfPage(...) for ...]

class WordDocument(Document):
    def _read_pages(self): return [WordPage(...) for ...]
```

- `Document.open` doesn't know which Page type it gets
- Subclass picks; `open` runs the same way for both

---

## Abstract Factory

- *Intent*: create *families* of related objects without naming concrete classes
- One factory class makes many *kinds* of products
- Switch the factory &#8594; switch the whole family
- Cross-platform UI: a `MacFactory` makes Mac buttons + Mac windows; a `WinFactory` makes Win versions
- Heavyweight; consider Factory Method first

---

## Abstract Factory in Code

```python
class GuiFactory(ABC):
    @abstractmethod
    def create_button(self): ...
    @abstractmethod
    def create_window(self): ...

class MacFactory(GuiFactory):
    def create_button(self): return MacButton()
    def create_window(self): return MacWindow()

class WinFactory(GuiFactory):
    def create_button(self): return WinButton()
    def create_window(self): return WinWindow()
```

- Pass the right factory at startup
- The rest of the app uses the abstract `Button`, `Window`

---

## Builder

- *Intent*: construct a complex object step by step, separate construction from representation
- Useful when an object has many optional parameters
- Avoids the "telescoping constructor": `Pizza(small, thin, true, false, true, ...)`
- Often combined with a fluent interface

---

## Builder in Code

```python
class PizzaBuilder:
    def __init__(self): self._p = Pizza()
    def size(self, s):    self._p.size = s; return self
    def thin_crust(self): self._p.thin_crust = True; return self
    def cheese(self, c):  self._p.cheese = c; return self
    def build(self):      return self._p

p = PizzaBuilder().size("L").thin_crust().cheese("mozz").build()
```

- Each method returns `self` for chaining
- `build()` returns the finished product

---

## Builder Trade-offs

- Pro: readable construction of complex objects
- Pro: lets you build immutable objects step by step
- Con: more boilerplate than a simple constructor
- Con: builder and product can drift out of sync
- Modern languages with named arguments (Python, Kotlin) often skip Builder

---

## Prototype

- *Intent*: create new objects by *cloning* an existing one
- Useful when construction is expensive or complex
- The prototype carries default state; clone, then customise
- Languages with deep copy support (Python's `copy.deepcopy`) implement it almost trivially
- Common in games (clone a tree template, place 100 trees)

---

## Prototype in Code

```python
import copy

class Shape:
    def __init__(self, x, y, color):
        self.x, self.y, self.color = x, y, color
    def clone(self):
        return copy.deepcopy(self)

template = Shape(0, 0, "blue")
new = template.clone()
new.x, new.y = 100, 200
```

- The clone shares the *type* and initial state of the prototype
- Mutating the clone doesn't affect the original

---

## Worked Example: Logger With Factory

- A `LoggerFactory` decides whether to make a FileLogger or NetLogger
- Each Logger instance is itself a Singleton (one per category)
- The factory hides the construction logic
- Consumers just ask `LoggerFactory.get("orders")`
- Two patterns, well-applied, no surprises in the API

---

## Choosing Among Creational Patterns

- One instance forever &#8594; Singleton (or skip and inject a regular one)
- Subclass picks the concrete type &#8594; Factory Method
- Many related types selected together &#8594; Abstract Factory
- Many constructor arguments, varied combinations &#8594; Builder
- Expensive construction, customise from a template &#8594; Prototype

---

## Common Mistakes

- Singleton everywhere &#8594; effectively global mutable state
- Builder for objects with three fields &#8594; pure ceremony
- Abstract Factory with one concrete factory &#8594; defer until the second one exists
- Factory Method imitating Strategy &#8594; pick the right pattern for the intent
- Prototype + mutable shared state &#8594; clones change each other unexpectedly
