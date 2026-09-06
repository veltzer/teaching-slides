---
tags:
  - concepts:oop
  - concepts:practice
level: beginner
category: design-patterns
audience:
  - audiences:developers

---

# OOP in Practice

---

## What This Chapter Covers

- Patterns that recur in real OOP code
- Refactoring procedural code to OOP
- Testing object-oriented code
- Common anti-patterns
- A short tour of where this knowledge lands you

---

## Common Patterns You'll See

- **Template Method**: base class defines the skeleton, subclasses fill in steps
- **Strategy**: behaviour passed in as an object
- **Observer**: subjects notify observers of events
- **Factory**: hide construction behind a method
- **Singleton**: exactly one instance (use sparingly)

---

## Smells to Watch For

![oop_smells](svg/courses/principles/object-oriented-programming/11_oop_in_practice/oop_smells.svg)

---

## Team Practices

![team_practices](svg/courses/principles/object-oriented-programming/11_oop_in_practice/team_practices.svg)

---

## Refactoring Procedural to OOP

- Find functions that always operate on the same dictionary or struct
- Extract that data into a class
- Move the functions into the class as methods
- Hide the now-internal data
- Replace direct field access with method calls

---

## Refactoring Example

Before:
```python
def start_engine(car):
    car['running'] = True

def stop_engine(car):
    car['running'] = False

car = {'running': False}
start_engine(car)
```

After:
```python
class Car:
    def __init__(self):
        self._running = False
    def start(self): self._running = True
    def stop(self): self._running = False

car = Car()
car.start()
```

---

## Testing OOP Code

- Test through the public interface — don't poke at private state
- One test class per production class is a reasonable starting point
- Use composition + dependency injection so collaborators can be replaced
- Mocks/stubs/fakes are tools — pick the lightest one that works
- Test the *contract*, not the implementation

---

## Test Doubles

- **Dummy**: passed but never used
- **Stub**: returns canned answers
- **Spy**: records what was called
- **Mock**: pre-programmed expectations and verification
- **Fake**: simplified working implementation (in-memory DB, etc.)

---

## When To Use Which

- A test that doesn't care about the collaborator: dummy
- A test that needs the collaborator to return something specific: stub
- A test that needs to *check* the collaborator was called: spy or mock
- A test that wants real-ish behaviour but lighter: fake
- Heavy use of mocks is a smell — usually means the design is too coupled

---

## OOP Anti-Patterns: God Object

- One class that does everything
- Knows too much, does too much, depends on too much
- Sometimes called "manager", "controller", "service" with no constraint
- Symptoms: 1000+ lines, 50+ methods, every change touches it
- Fix: extract cohesive responsibilities into smaller classes

---

## Anti-Pattern: Anaemic Domain Model

- Classes that are just data — getters and setters, no behaviour
- All the logic lives in "service" classes that operate on the data
- Looks OO from the outside, is procedural underneath
- Common in projects that started with "ORM-friendly" data classes
- Fix: move behaviour into the data class where it belongs

---

## Anti-Pattern: Yo-Yo Problem

- Inheritance hierarchy is so deep that finding behaviour requires hopping up and down the chain
- Reading any method requires keeping the whole hierarchy in your head
- Fix: flatten the hierarchy, extract behaviour into helpers

---

## Anti-Pattern: Inappropriate Intimacy

- Two classes know too much about each other's internals
- Often: A's methods constantly read and write B's fields
- Fix: move the methods to the class that owns the data

---

## Anti-Pattern: Telescoping Constructor

- A class with constructors taking 2, 3, 4, 5, 6 args
- Each new constructor calls the larger one with defaults
- Hard to read at the call site: `new Pizza("M", "thin", true, false, true, 12)`
- Fix: builder pattern, named arguments (Python, Kotlin)

---

## Modern OOP Conventions

- Classes are smaller than they used to be (one job each)
- Inheritance is shallower (composition where possible)
- Mutable state is rarer (immutability is preferred where reasonable)
- Interfaces are smaller (Interface Segregation)
- Dependencies are injected, not constructed inside

---

## OOP and Functional Programming

- Modern languages mix the two: Python, Scala, Kotlin, C#
- Use OOP for the "things with identity"
- Use FP for the data transformations
- Lambdas and method references are now everywhere — embrace them
- Pure functions inside encapsulated objects: best of both

---

## When NOT to Reach for OOP

- Single-purpose scripts — overkill
- Pure data transformations — functional pipelines are clearer
- Performance-critical inner loops — object overhead matters
- Plain old CLI utilities — argparse + functions
- Don't force a hierarchy where there isn't one

---

## What Comes Next

- **Design patterns**: standard solutions to recurring problems
- **Domain-Driven Design**: model the business in OO terms
- **Architecture patterns**: how to organise *systems* of objects
- **Refactoring**: a discipline of evolving code over time
- This course is the foundation; those are the next steps

---

## Course Wrap-Up

- OOP gives you a vocabulary for organising change-resistant code
- The four pillars are tools, not commandments
- Composition usually beats inheritance
- SOLID is heuristics, not laws — apply when you smell trouble
- The goal is *understandable* code that survives years of change
