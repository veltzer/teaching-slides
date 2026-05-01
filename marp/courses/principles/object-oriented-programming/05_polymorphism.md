---
tags:
  - concepts:oop
  - concepts:polymorphism
level: beginner
category: design-patterns
audience:
  - audiences:developers

---
# Polymorphism

---
## What This Chapter Covers

- What polymorphism actually means
- Subtype polymorphism (the OOP kind)
- Method overriding and dynamic dispatch
- Compile-time vs runtime polymorphism
- Duck typing in Python
- Why polymorphism is the real point of OOP

---
## What "Polymorphism" Means

- Greek: "many forms"
- The *same* method call can do different things depending on the object
- Example: `shape.area()` returns the right value whether `shape` is a Circle or a Rectangle
- The caller doesn't care which class — only that there's an `area()` method
- The discipline of programming to a common contract

---
## A First Example

```python
class Shape:
    def area(self): raise NotImplementedError

class Circle(Shape):
    def __init__(self, r): self.r = r
    def area(self): return 3.14159 * self.r ** 2

class Rectangle(Shape):
    def __init__(self, w, h): self.w, self.h = w, h
    def area(self): return self.w * self.h

shapes = [Circle(5), Rectangle(3, 4)]
total = sum(s.area() for s in shapes)
```

---
## Why This Matters

- The caller has no `if isinstance(...)` chain
- Adding a new shape (Triangle) doesn't touch `total` calculation
- The decision of *which area() to run* is made at runtime
- The data dictates the behaviour, not a switch statement
- Open/closed principle in action

---
## Dynamic Dispatch

- The runtime looks up the method based on the object's *actual type*
- The variable's *declared type* doesn't decide
- Java: `Shape s = new Circle(5); s.area();` &#8594; calls Circle.area
- Python: every method call is a dynamic lookup; trivial to make polymorphic
- C++: marked `virtual` to enable dynamic dispatch; non-virtual is static

---
## Compile-Time Polymorphism

- Method *overloading*: same name, different parameter lists
- Resolved at compile time based on the argument types
- Java: yes (with overload resolution rules)
- Python: no (can simulate with `singledispatch` or default args)
- Easier to misuse than overriding — readers can't tell which version is called

---
## Overloading vs Overriding

- **Overloading**: same name, different *parameter lists*, same class
- **Overriding**: same name, *same* parameter list, different class
- Overloading is a syntactic convenience
- Overriding is the OOP feature that gives you polymorphism
- Java has both; Python only really has overriding

---
## Duck Typing

> "If it walks like a duck and quacks like a duck, it's a duck."

- Python doesn't check what type something *is*; it checks whether it has the methods being called
- No need for a shared base class or interface
- `def render(thing): thing.draw()` works for anything with a `draw` method
- Simpler than declaring interfaces; harder to verify statically
- Type hints + protocols (PEP 544) get you back some of the safety

---
## Interfaces as Polymorphism's Vehicle

```java
public interface Shape {
    double area();
}

public class Circle implements Shape { ... }
public class Rectangle implements Shape { ... }
```

- The interface declares the contract
- Each implementer fulfils it
- Code that consumes `Shape` works with any current or future implementation
- Java's preferred shape for polymorphism

---
## Polymorphism Without Inheritance

- Strategy pattern: pass a function (or a function object) instead
- C++/Rust function templates: parametric polymorphism
- Trait-based dispatch in Rust, type classes in Haskell
- All achieve "varied behaviour through a common shape" without inheritance
- OOP's polymorphism is one of several techniques

---
## A Practical Example

```python
def total_area(shapes):
    return sum(s.area() for s in shapes)
```

- Works for any list of objects with an `area()` method
- Future shapes need no change to `total_area`
- Compare with the procedural version that switched on `shape_type`
- This is the daily payoff of polymorphism

---
## When Polymorphism Helps

- Multiple things implement the same operation differently
- You want callers to be ignorant of which implementation
- New implementations are added over time
- Testing benefits from substitution (mocks, fakes)

---
## When Polymorphism Hurts

- Only one implementation exists today and probably ever
- The varied behaviour is one branch in a single function — leave it
- Forcing an interface on stable, single-implementation code adds noise
- Premature polymorphism is a flavour of premature abstraction

---
## Common Mistakes

- A subclass that overrides a method to do nothing or throw — violates substitutability
- Public methods that change behaviour based on `isinstance` checks (anti-pattern)
- Many narrow interfaces, each with one implementation
- Forgetting `@Override` in Java — typo &#8594; "new method" instead of "override"
- Overloading where polymorphism would be clearer
