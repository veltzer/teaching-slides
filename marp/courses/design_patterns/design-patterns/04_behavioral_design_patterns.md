---
tags:
  - concepts:design-patterns
  - concepts:behavioural-patterns
level: intermediate
category: design-patterns
audience:
  - audiences:developers

---
# Behavioural Design Patterns

---
## What This Chapter Covers

- Eleven patterns about *how objects share work*
- Strategy, Observer, Iterator, Template Method, Command — the headline patterns
- Chain of Responsibility, State, Visitor — high-impact specialised tools
- Mediator, Memento, Interpreter — useful in narrower cases
- For each: intent, structure, code sketch, when to use

---
## The Headline Four

![behavioral_patterns](svg/courses/design_patterns/design-patterns/04_behavioral_design_patterns/behavioral_patterns.svg)

---
## Strategy

- *Intent*: encapsulate algorithms behind a common interface, switch them at runtime
- The classic "varying behaviour" pattern
- Sort with different comparators; price an order with different discount strategies
- In functional languages, often "just pass a function"
- Pairs with Open/Closed: new strategies don't change consumers

---
## Strategy in Code

```python
class Strategy(Protocol):
    def apply(self, x): ...

class CapStrategy:
    def apply(self, x): return min(x, 100)

class DoubleStrategy:
    def apply(self, x): return x * 2

def process(items, strategy):
    return [strategy.apply(x) for x in items]
```

- The consumer (`process`) doesn't know which strategy
- Add new strategies without touching `process`

---
## Observer

- *Intent*: when one object changes state, notify many dependents
- The **subject** maintains a list of **observers**, calls them on change
- Foundation of MVC, reactive systems, GUI event loops
- Spreadsheet "if cell A changes, recompute B, C, D" is Observer
- Easy to misuse: cyclic dependencies, surprise updates

---
## Observer in Code

```python
class Subject:
    def __init__(self):
        self._observers = []
    def attach(self, obs): self._observers.append(obs)
    def notify(self, event):
        for o in self._observers:
            o.update(event)

class LoggingObserver:
    def update(self, event): print("event:", event)
```

- Observers register at any time
- Subject knows nothing about specific observer types

---
## Iterator

- *Intent*: traverse a collection without exposing its internals
- Most languages now have iterators built in
- Python: `__iter__` and `__next__`; Java: `Iterator<T>`
- The pattern is interesting historically; less so as a deliberate design choice today
- Knowing it explains *why* `for x in collection:` works

---
## Template Method

- *Intent*: define the skeleton of an algorithm in a base class, let subclasses fill in steps
- The "skeleton method" calls a sequence of steps
- Some steps are concrete (shared), some are abstract (subclass fills in)
- The order is fixed in the base class
- Common in framework code where a base class drives the workflow

---
## Template Method in Code

```python
class Game(ABC):
    def play(self):                # the template
        self._initialize()
        while not self._over():
            self._take_turn()
        self._announce_winner()

    @abstractmethod
    def _initialize(self): ...
    @abstractmethod
    def _take_turn(self): ...
    @abstractmethod
    def _over(self): ...
    @abstractmethod
    def _announce_winner(self): ...
```

- `play()` is fixed for all games
- Subclasses fill in the steps — Chess, Monopoly, Checkers

---
## Command

- *Intent*: encapsulate a request as an object
- Can be queued, logged, undone, redone
- The classic implementation of "undo/redo" in editors
- The pattern decouples the *invoker* from the *receiver*
- In functional languages: a function or a closure

---
## Command in Code

```python
class Command(ABC):
    @abstractmethod
    def execute(self): ...
    @abstractmethod
    def undo(self): ...

class TypeText(Command):
    def __init__(self, doc, text):
        self._doc, self._text = doc, text
    def execute(self): self._doc.append(self._text)
    def undo(self):    self._doc.remove_last(len(self._text))

# Editor stores a stack of executed Commands; pop to undo
```

---
## Chain of Responsibility

- *Intent*: pass a request along a chain of handlers until one handles it
- Each handler decides: handle it or pass it on
- Used in HTTP middleware (Express, Flask), event bubbling, exception handling
- Decouples sender from a specific receiver
- Risk: requests fall off the end with no handler

---
## State

- *Intent*: an object behaves differently depending on its internal state
- Replace big `if state == X: ... elif state == Y: ...` chains with state-object dispatch
- The Context delegates to a State object; transitions swap the State
- Common in protocol implementations, game characters, UI workflow
- Cleaner than a switch, costs an extra class per state

---
## State in Code

```python
class State(ABC):
    @abstractmethod
    def insert_coin(self, machine): ...

class NoCoinState(State):
    def insert_coin(self, m):
        m.state = HasCoinState()
        print("coin accepted")

class HasCoinState(State):
    def insert_coin(self, m):
        print("already has coin")

class Machine:
    def __init__(self):
        self.state = NoCoinState()
    def insert_coin(self):
        self.state.insert_coin(self)
```

---
## Visitor

- *Intent*: separate an algorithm from the object structure it operates on
- Lets you add new operations to a fixed set of classes without modifying them
- Heavy use in compilers (visit each AST node type)
- The trade-off: easy to add operations, hard to add new types
- Often replaced by sum types + pattern matching in modern languages

---
## Mediator

- *Intent*: encapsulate how a set of objects interact, so they don't refer to each other directly
- The mediator becomes the only object that knows the network of relationships
- Air-traffic control: planes don't talk to planes; they talk to the tower
- Reduces N-to-N dependencies to N-to-1
- Risk: mediator becomes a god object

---
## Memento

- *Intent*: capture and externalise an object's internal state so it can be restored later
- Used for undo systems, save points, snapshots
- Without breaking encapsulation: only the originator can read the memento's state
- Often combined with Command for full undo/redo
- Modern equivalent: serialise to JSON, restore later

---
## Interpreter

- *Intent*: define a representation for a grammar plus an interpreter for it
- Each grammar rule is a class; the program is a tree of these
- Used to evaluate small DSLs, expression languages, query parsers
- Heavy machinery; only worth it for grammars you really do interpret
- For complex grammars, reach for a parser generator (ANTLR, Lark)

---
## Choosing Among Behavioural Patterns

- Vary an algorithm at runtime &#8594; Strategy
- One change &#8594; many reactions &#8594; Observer
- Fixed workflow with customisable steps &#8594; Template Method
- Encapsulate an action for queueing/undo &#8594; Command
- Pass a request through layers &#8594; Chain of Responsibility
- Behaviour depends on internal state &#8594; State
- New operations on a fixed type hierarchy &#8594; Visitor

---
## Course Wrap-Up

- 23 patterns is a *vocabulary*, not a checklist
- Most teams use 5-10 of them regularly; recognise the rest when reading code
- Patterns *embody* principles like SOLID, DRY, OCP
- Modern languages make some patterns trivial (Strategy = a function)
- Don't *use* patterns; *recognise* the problem first, then check whether a pattern fits
