---
tags:
  - concepts:oop
  - concepts:encapsulation
level: beginner
category: design-patterns
audience:
  - audiences:developers

---
# Encapsulation

---
## With vs Without

![encapsulation](svg/courses/principles/object-oriented-programming/03_encapsulation/encapsulation.svg)

---
## Access Modifiers

![access_modifiers](svg/courses/principles/object-oriented-programming/03_encapsulation/access_modifiers.svg)

---
## Why It Matters

![encapsulation_benefits](svg/courses/principles/object-oriented-programming/03_encapsulation/encapsulation_benefits.svg)

---
## What This Chapter Covers

- What encapsulation actually means
- Access modifiers
- Getters, setters, and properties
- The difference between "data hiding" and "information hiding"
- Designing clean interfaces
- Common mistakes

---
## What Encapsulation Is

- Bundling state with the behaviour that operates on it
- *Hiding* internal state behind a controlled interface
- Clients call methods, not poke at fields
- The class decides *how* its state changes
- Internal redesign doesn't break clients

---
## Why Hide Data?

- Direct field access spreads knowledge of representation everywhere
- Change the representation &#8594; change every place that touched the field
- Hiding the field behind methods isolates that change to one place
- Validation lives next to mutation
- Concurrency, lazy loading, computed values — all become possible

---
## Access Modifiers in Java

- `public`: visible everywhere
- `private`: visible only inside this class
- `protected`: visible inside this class and subclasses
- (default): visible inside the same package
- Use the most restrictive that works; widen later if needed

---
## "Access Modifiers" in Python

- Python has no enforced access control
- Convention: `_name` means "intended as private"
- `__name` triggers name mangling (rarely useful)
- The convention works when the team respects it
- "We're all consenting adults here"

---
## Getters and Setters

```java
private int age;

public int getAge() {
    return age;
}

public void setAge(int age) {
    if (age < 0) throw new IllegalArgumentException("negative age");
    this.age = age;
}
```

- Mediated access lets you validate, log, lock, lazy-compute
- Bare getter/setter pairs aren't much better than public fields
- Add them when there's a *reason*

---
## Properties in Python

```python
class Account:
    def __init__(self, balance):
        self._balance = balance

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, value):
        if value < 0:
            raise ValueError("negative balance")
        self._balance = value
```

- Looks like field access, runs methods underneath
- Lets you start with a public attribute and *promote* it later without breaking callers
- C# has the same idea built in

---
## Don't Just Mirror Fields

- A getter for every field, a setter for every field, no other methods = anemic class
- Better: ask the class to *do* something on your behalf
- `account.deposit(50)` over `account.setBalance(account.getBalance() + 50)`
- Methods that express *behaviour* are the point of OOP
- Bare data with bare accessors is just a struct in disguise

---
## Information Hiding vs Data Hiding

- **Data hiding**: keep fields private
- **Information hiding** (Parnas, 1972): hide *design decisions* that might change
- Hiding the implementation of a method is information hiding
- Hiding *which library* powers a service is information hiding
- Data hiding is the easy half; information hiding is the discipline

---
## Designing Clean Interfaces

- Few methods, each with a clear purpose
- Methods named for *what* they do, not *how*
- No public method that takes the class's own private representation as a parameter
- No leaks: if you return a mutable internal collection, return a copy
- Beware the temptation to add "convenience" methods that bloat the API

---
## Immutability

- The simplest encapsulation: no setters at all
- Construct the object fully, never change it
- All "modifications" return new instances
- Trivial to reason about, share across threads, cache
- Java records, Python frozen dataclasses, Kotlin data classes — language-level support

---
## Visibility in Practice

- Start with `private` for everything
- Promote to `protected` when a subclass legitimately needs it
- Promote to `public` only with a good reason
- Be especially conservative with mutable shared state
- Every public field is a future support ticket

---
## Encapsulation and Testing

- Tests should exercise the *interface*, not the internals
- Testing private methods is a smell — usually means they should be public on a different class
- White-box tests that assert on private state are brittle
- Refactor the class to expose the right behaviours, then test those

---
## Encapsulation and Concurrency

- Mutable state shared across threads needs coordination
- Encapsulation is what *makes* coordination possible
- Synchronisation lives inside the class, not at every call site
- Better: design out the mutability and avoid the problem
- Immutable objects are inherently thread-safe

---
## Common Mistakes

- Bare getter/setter for every field — defeats the purpose
- Methods that return references to mutable internal collections
- "Friend" workarounds (Java reflection, Python double-underscore poking) used in production code
- Public mutable static state
- A large class with public methods that operate on every internal field
