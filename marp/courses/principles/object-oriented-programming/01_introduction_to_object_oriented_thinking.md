---
tags:
  - concepts:oop
level: beginner
category: design-patterns
audience:
  - audiences:developers

---
# Introduction to Object-Oriented Thinking

---
## What This Chapter Covers

- The procedural model and where it breaks down
- The object model: state and behaviour together
- Modelling the world as objects
- Why OOP became dominant
- A short tour of OOP's history

---
## The Procedural Model

- Code is organised as functions that operate on data
- Data is mostly inert — passed around as arguments and return values
- Examples: classic C, Pascal, early Fortran
- Works well for small programs and well-defined algorithms
- Breaks down at scale: which function modifies which data?

---
## The Object Model

- An object bundles *state* (data) with *behaviour* (functions that operate on it)
- A small set of well-named methods is the contract
- Internal data is hidden; clients only see methods
- A program becomes a collection of objects exchanging messages
- Easier to reason about *who can change what*

---
## Two Senses of "Object"

- The word "object" gets reused; pin it down:
- **Class**: the blueprint — definition, code, methods
- **Object** (instance): a specific thing built from a class
- Class = "Dog"; objects = "Rex", "Lassie", "Buddy"
- All objects of one class share the same methods, but each has its own state

---
## Objects and Messages

- Calling a method is sometimes called "sending a message"
- `dog.bark()` &#8594; "send the bark message to the dog object"
- Smalltalk-style: literally everything is a message send
- Java/C# style: looks like calling a function on an object
- The mental model is the same; the syntax differs

---
## Modelling the World

- A logging system has Loggers, Formatters, Appenders
- An e-commerce site has Customers, Orders, Products, Carts
- Each maps to a class with state and behaviour
- The mapping isn't one-to-one with reality — it's a *useful abstraction*
- A "Customer" object isn't a person; it's the parts of a person the system cares about

---
## Why OOP Won

- Bigger codebases became common in the 1990s
- Procedural code rotted under that scale
- OOP gave teams a way to localise change (encapsulation)
- It let large libraries be reused (inheritance, polymorphism)
- Languages with first-class OOP (Java, C#) shipped at the right moment

---
## A Brief History

- 1967: Simula 67 introduced classes and objects
- 1972: Smalltalk took the idea to extremes — pure object model
- 1985: C++ added objects to C, kept performance
- 1995: Java promised "write once, run anywhere"
- 2000s: C#, Python, Ruby — each with their own flavour of OOP

---
## The OOP Pillars

- **Encapsulation**: hide data behind methods
- **Inheritance**: derive specialised classes from general ones
- **Polymorphism**: treat different types uniformly through a common interface
- **Abstraction**: expose what an object does, hide how
- These four concepts structure the rest of this course

---
## OOP Is Not the Only Way

- Functional programming (Haskell, Clojure): values + functions, no mutable objects
- Procedural (C, Go): functions + structs, no inheritance
- Logic programming (Prolog): rules and unification
- Modern languages mix paradigms — Python and Scala are multi-paradigm
- OOP is *a* tool; not the only tool

---
## When OOP Helps

- Domain has clear "things" with state and behaviour
- Code lives long, evolves over years, has many maintainers
- Polymorphism cleanly models a "kind of" relationship
- Multiple implementations of the same contract exist
- A team is large enough that encapsulation matters

---
## When OOP Hurts

- Pure data transformation (use pipelines)
- Algorithms with no state (use functions)
- Performance-critical loops (object overhead can matter)
- Domains with no obvious "things" — forcing classes on them adds noise
- Teams that misuse inheritance — the topic of a later chapter

---
## What's Next

- Classes and objects in concrete code
- Encapsulation, the most foundational pillar
- Inheritance and polymorphism — the powerful and the dangerous
- Abstraction, composition, design by contract
- SOLID, UML, and how to think about OOP in practice
