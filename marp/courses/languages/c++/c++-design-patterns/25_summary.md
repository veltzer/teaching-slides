---
tags:
  - languages:cpp
  - concepts:design-patterns
  - concepts:oop
  - practices:software-design
level: advanced
category: language
audience:
  - audiences:developers

---

# Design Patterns Summary

---

## Creational Patterns Overview

| Pattern | Purpose | Key Idea |
|---------|---------|----------|
| Singleton | One instance globally | Static local variable (Meyers') |
| Factory Method | Delegate creation to subclasses | Virtual creation method |
| Abstract Factory | Create families of related objects | Factory of factories |
| Builder | Construct complex objects step by step | Fluent interface |
| Prototype | Clone existing objects | `clone()` method |

---

## Structural Patterns Overview

| Pattern | Purpose | Key Idea |
|---------|---------|----------|
| Adapter | Make incompatible interfaces work together | Wrapper class |
| Bridge | Separate abstraction from implementation | Composition over inheritance |
| Composite | Treat groups and individuals uniformly | Tree structure |
| Decorator | Add behavior dynamically | Wrapping chain |
| Facade | Simplify complex subsystem | Unified interface |
| Flyweight | Share common state to save memory | Intrinsic vs extrinsic state |
| Proxy | Control access to an object | Surrogate with same interface |

---

## Behavioral Patterns Overview

| Pattern | Purpose | Key Idea |
|---------|---------|----------|
| Chain of Responsibility | Pass request along a chain | Linked handlers |
| Command | Encapsulate request as object | Undo/redo support |
| Interpreter | Evaluate language grammar | Expression tree |
| Iterator | Sequential access to elements | `begin()`/`end()` |
| Mediator | Centralize complex interactions | Hub-and-spoke |
| Memento | Save and restore state | Snapshot without exposing internals |
| Observer | Notify dependents of state changes | Publish-subscribe |
| State | Behavior varies by internal state | State objects |
| Strategy | Swap algorithms at runtime | Composition of behavior |
| Template Method | Define algorithm skeleton | Override steps via inheritance |
| Visitor | Add operations without modifying classes | Double dispatch |

---

## Pattern Selection Guide

![pattern_selection_guide](svg/courses/languages/c++/c++-design-patterns/25_summary/pattern_selection_guide.svg)

---

## Choosing the Right Pattern

Questions to ask:

1. **Is it about creating objects?** Look at Creational patterns
1. **Is it about organizing classes?** Look at Structural patterns
1. **Is it about communication between objects?** Look at Behavioral patterns
1. **Do I need flexibility at runtime?** Strategy, State, Command
1. **Do I need to extend without modifying?** Visitor, Decorator, Observer
1. **Do I need to simplify complexity?** Facade, Mediator, Chain of Responsibility

---

## Modern C++ Alternatives

Some patterns become simpler or unnecessary with modern C++ features:

- **Strategy** → `std::function` + lambdas
- **Observer** → `std::function` callbacks or signal/slot libraries
- **Command** → `std::function` with captures
- **Iterator** → Range-based for, C++20 Ranges
- **Visitor** → `std::variant` + `std::visit`
- **Singleton** → Meyers' Singleton (thread-safe since C++11)

The patterns remain valuable as design concepts even when their implementation is simplified by language features

---

## Anti-Patterns to Avoid

1. **Pattern overuse**: Not every problem needs a pattern
1. **Premature abstraction**: Add patterns when complexity warrants it
1. **Wrong pattern**: Understand the problem before choosing a solution
1. **Ignoring SOLID**: Patterns work best when SOLID principles are followed
1. **Copy-paste patterns**: Adapt to your specific context

**Remember**: Patterns are tools, not goals. The best code is the simplest code that solves the problem correctly.

---

## Further Reading

- "Design Patterns: Elements of Reusable Object-Oriented Software" — Gang of Four
- "Modern C++ Design" — Andrei Alexandrescu
- "Head First Design Patterns" — Freeman & Robson
- "Refactoring Guru" — refactoring.guru/design-patterns
- "C++ Core Guidelines" — isocpp.github.io/CppCoreGuidelines
