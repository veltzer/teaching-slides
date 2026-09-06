---
tags:
  - concepts:oop
  - concepts:inheritance
level: beginner
category: design-patterns
audience:
  - audiences:developers

---

# Inheritance

---

## What This Chapter Covers

- What inheritance is and what it gives you
- Method overriding
- Constructor chaining
- Single vs multiple inheritance
- The fragile base class problem
- When inheritance is the wrong tool

---

## What Inheritance Is

- A class can extend another, gaining its fields and methods
- The new class is the *subclass* (derived); the original is the *superclass* (base)
- Subclass can add new members, override existing ones
- Models an "is-a" relationship: a Dog *is an* Animal
- Common in libraries: extending base classes the framework provides

---

## Forms

![inheritance_kinds](svg/courses/principles/object-oriented-programming/04_inheritance/inheritance_kinds.svg)

---

## Liskov Substitution

![liskov_principle](svg/courses/principles/object-oriented-programming/04_inheritance/liskov_principle.svg)

---

## A First Example

```java
public class Animal {
    protected String name;
    public Animal(String name) { this.name = name; }
    public void speak() { System.out.println("..."); }
}

public class Dog extends Animal {
    public Dog(String name) { super(name); }
    @Override
    public void speak() { System.out.println(name + " says woof"); }
}
```

---

## Method Overriding

- Subclass redefines a method inherited from the superclass
- The new version runs whenever the method is called *through that subclass*
- Java requires `@Override` (good practice — catches typos)
- Python has no annotation; just define a method with the same name
- The pattern of using overriding for varied behaviour is *polymorphism* (next chapter)

---

## Constructor Chaining

- Subclass constructor must initialise the superclass first
- Java: `super(args)` as the first statement of a constructor
- Python: `super().__init__(args)` somewhere in `__init__`
- If you don't call it, you may get partial initialisation
- The superclass invariants must hold before the subclass adds its own state

---

## Calling Super Methods

```python
class TimedAnimal(Animal):
    def speak(self):
        start = time.time()
        super().speak()
        print(f"took {time.time() - start:.4f}s")
```

- `super()` calls the parent's version
- Useful when the subclass *extends* (not replaces) behaviour
- Pattern: pre-action, super call, post-action

---

## Single vs Multiple Inheritance

- Single inheritance: a class has at most one parent (Java, C#, Kotlin)
- Multiple inheritance: a class has many parents (Python, C++, Eiffel)
- Multiple inheritance brings power *and* the diamond problem
- Most languages compromise with interfaces (Java) or mixins (Python)
- Interfaces give "is-a" without bringing implementation

---

## The Diamond Problem

- Class B extends A; class C extends A; class D extends B and C
- Which `A` does D inherit?
- Languages resolve it differently: C++ uses virtual inheritance; Python uses MRO (method resolution order)
- The *human* confusion is the real problem
- Avoid by preferring composition or interfaces

---

## Interfaces as a Cheaper Alternative

```java
public interface Speaker {
    void speak();
}

public class Dog implements Speaker { ... }
public class Cat implements Speaker { ... }
```

- Pure contract, no implementation
- A class can implement many interfaces — no diamond problem
- Modern Java added default methods, blurring the line
- Interfaces give you polymorphism without inheritance

---

## The Fragile Base Class Problem

- Subclasses depend on the *implementation*, not just the interface, of the base
- Change the base &#8594; subclasses break in non-obvious ways
- Especially bad when the base is in a third-party library
- Documented in Joshua Bloch's *Effective Java*: "Design and document for inheritance, or prohibit it"
- Final classes (Java) and `@final` decorators are tools to prohibit it

---

## When Inheritance Is the Wrong Tool

- "Code reuse" is *not* a good reason — use composition
- "Customer is-a Person" — actually no, model what the system needs
- Forcing a hierarchy on essentially-flat data
- More than 2-3 levels deep — the chain becomes hard to reason about
- When a Liskov violation lurks (next chapter)

---

## Composition Over Inheritance

```python
class Logger:
    def log(self, msg): ...

class OrderService:
    def __init__(self, logger):
        self._logger = logger
```

- Hold a reference to the helper instead of inheriting from it
- Easier to swap implementations
- Easier to test (inject a mock)
- Forms the basis of the Strategy pattern

---

## Inheritance in Python

- Use `class Sub(Base):`
- Multiple inheritance with `class Sub(B1, B2):`
- MRO determines which `Base.__init__` runs
- Diamond resolved by C3 linearisation
- Most Python OO uses single inheritance + mixins

---

## Inheritance in Java

- Use `class Sub extends Base`
- Single inheritance only
- Implement many interfaces with `implements I1, I2`
- `final` class can't be extended; `final` method can't be overridden
- Modern Java: prefer composition + interfaces

---

## Practical Guideline

- First reach: composition
- Second reach: interfaces
- Third reach: inheritance, with a *single* base class
- Document inheritance contracts: what subclasses may rely on, what they must implement
- Keep hierarchies shallow

---

## Common Mistakes

- Inheritance for code reuse rather than for an "is-a" relationship
- Subclasses that violate the parent's contract (subclass `Square extends Rectangle` is the classic)
- Deep inheritance chains
- Calling overridable methods from the constructor
- Letting subclasses access mutable parent state directly
