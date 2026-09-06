---
tags:
  - concepts:oop
  - concepts:abstraction
level: beginner
category: design-patterns
audience:
  - audiences:developers

---

# Abstraction

---

## What This Chapter Covers

- What abstraction is, distinct from encapsulation
- Abstract classes
- Interfaces
- Abstract methods
- Contracts and protocols
- Designing for abstraction

---

## Abstraction vs Encapsulation

- **Encapsulation**: hide *internal state* behind methods
- **Abstraction**: hide *the kind of thing* behind a contract
- Encapsulation is about access; abstraction is about identity
- "I don't need to know how Logger works" = encapsulation
- "I don't need to know whether this is a FileLogger or NetLogger" = abstraction

---

## Levels

![abstraction_levels](svg/courses/principles/object-oriented-programming/06_abstraction/abstraction_levels.svg)

---

## Interface Versus Abstract Class

![interface_versus_class](svg/courses/principles/object-oriented-programming/06_abstraction/interface_versus_class.svg)

---

## Abstract Classes

- A class that *cannot* be instantiated directly
- Defines some methods, leaves others to subclasses
- Used as a partial implementation
- Java: `abstract class`; Python: `abc.ABC`
- A subclass either implements the missing methods or is itself abstract

---

## Abstract Class in Python

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self): ...

    def describe(self):
        return f"shape with area {self.area():.2f}"
```

- `Shape` cannot be instantiated
- Subclasses must implement `area`
- `describe` is shared across subclasses for free
- A common pattern for "template + customisation point"

---

## Abstract Class in Java

```java
public abstract class Shape {
    public abstract double area();

    public String describe() {
        return "shape with area " + area();
    }
}
```

- `abstract` on the class and on the unimplemented method
- Subclasses must override `area` or be `abstract` themselves
- Same pattern as the Python version

---

## Interfaces

- Pure contract: method signatures, no implementation
- A class can implement many interfaces (Java, C#)
- Express "is capable of" rather than "is a kind of"
- Examples: `Comparable`, `Iterable`, `Closeable`
- Modern Java added default methods, blurring abstract class vs interface

---

## Java Interface Example

```java
public interface Comparable<T> {
    int compareTo(T other);
}

public class Version implements Comparable<Version> {
    @Override
    public int compareTo(Version other) {
        // ...
    }
}
```

---

## Python Protocols

```python
from typing import Protocol

class Drawable(Protocol):
    def draw(self) -> None: ...

def render(item: Drawable) -> None:
    item.draw()
```

- Structural typing: anything with a `draw()` method matches
- Type checker (mypy) verifies; runtime doesn't enforce
- Python's answer to interfaces without inheritance
- Closely matches duck typing while giving type safety

---

## Abstract Method Default Behaviour

- Calling an abstract method via the abstract class fails
- Java: compile error
- Python: `TypeError` at instantiation if you try to instantiate the abstract class
- This is by design — the contract is "subclasses provide this"
- Forces the developer to think about the customisation points

---

## Designing for Abstraction

- What does the *consumer* need? That's the interface
- Don't design the interface around how *implementations* work
- Keep interfaces small — each method is a constraint on every implementer
- Name methods for *what* they do, not *how*
- A good interface predicts how it'll be used; a bad one mirrors one implementation

---

## The Right Number of Methods

- One method: "Functional interface" — Strategy, Comparator, Runnable
- Two to five: typical service interface — Repository, Validator
- Five to ten: getting bigger; consider splitting (Interface Segregation)
- More than ten: probably too broad — it's likely two interfaces in disguise

---

## Layered Abstraction

- High-level: business operations (`OrderService.placeOrder`)
- Mid-level: domain operations (`PaymentGateway.charge`)
- Low-level: infrastructure (`HttpClient.post`)
- Each layer talks to the next via abstractions
- This is what makes the lower layers replaceable

---

## Abstraction and Testing

- Replace expensive collaborators with fakes via the abstraction
- Test the consumer in isolation
- Mocks, stubs, fakes — all rely on the consumer talking to an interface, not a concrete class
- Excessive mocking is a smell — sometimes the abstraction is wrong

---

## Premature Abstraction

- Adding a `Persistable` interface "in case we add another database"
- Adding a `Notifier` interface "in case we add SMS"
- Costs: extra files, extra mental overhead, harder navigation
- Benefit: zero, until the second implementation actually arrives
- Better: refactor when the second implementation appears

---

## Common Mistakes

- One interface per class with one implementation each — code "Hungarian"
- Abstract methods that immediately throw or return null — useless contract
- Interfaces that leak implementation details (e.g., expose internal types)
- Splitting an obvious cohesive class into many tiny interfaces because "abstraction is good"
- An abstract base class with state — usually wants to be composition instead
