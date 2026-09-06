---
tags:
  - languages:c++
  - design-patterns:oop
level: advanced
category: embedded
audience:
  - audiences:embedded-engineers
  - audiences:developers

---

# Inheritance and OO Design

---

## Inheritance in C++

- Mechanism for deriving new classes from existing ones
- Promotes code reuse and extensibility
- Supports polymorphism through virtual functions

---

## Types of Inheritance

1. Single Inheritance
1. Multiple Inheritance
1. Multilevel Inheritance
1. Hierarchical Inheritance
1. Hybrid Inheritance

---

## Single Inheritance

- One base class and one derived class
- Simplest form of inheritance

```cpp
class Base {
public:
    void display();
};

class Derived : public Base {
    // inherits display()
};
```

---

## Multiple Inheritance

- A class can inherit from more than one base class
- Can lead to ambiguity (e.g., Diamond Problem)

```cpp
class A { };
class B { };
class C : public A, public B { };
```

---

## Diamond Problem

- Occurs in multiple inheritance when two base classes inherit from a common ancestor
- Resolved using **virtual inheritance**

```cpp
class A { };
class B : virtual public A { };
class C : virtual public A { };
class D : public B, public C { };
```

---

## Virtual Functions

- Enable **runtime polymorphism**
- Base class defines a virtual function
- Derived class overrides it

```cpp
class Base {
public:
    virtual void show();
};

class Derived : public Base {
public:
    void show() override;
};
```

---

## Abstract Classes

- A class with at least one **pure virtual function**
- Cannot be instantiated
- Used as **interfaces**

```cpp
class Interface {
public:
    virtual void draw() = 0;
};
```

---

## Interface Segregation Principle

- Clients should not be forced to depend on interfaces they do not use
- Split large interfaces into smaller, specific ones

---

## Liskov Substitution Principle

- Subtypes must be substitutable for their base types
- Derived classes should not violate expectations set by base classes

---

## Composition vs Inheritance

- **Inheritance**: "is-a" relationship
- **Composition**: "has-a" relationship
- Prefer composition for flexibility and maintainability

---

## Favor Composition Over Inheritance

- Reduces tight coupling
- Easier to test and modify
- Promotes reuse of behavior without inheriting unnecessary interface

---

## UML Diagram Example

![uml_diagram_example](svg/courses/embedded/effective-real-time-embedded-c-and-c++/13_object_oriented_design/uml_diagram_example.svg)

---

## OO Design in Embedded Systems

- OO design offers modularity, maintainability, and abstraction
- Encapsulation isolates hardware-specific code
- Reduces global state and improves testing

---

## Embedded System Constraints

- Limited memory and CPU resources
- Deterministic and predictable behavior required
- Overhead from dynamic allocation and virtual tables can be costly

---

## OO Best Practices for Embedded

1. Use static allocation where possible
1. Avoid unnecessary inheritance chains
1. Use interfaces for hardware abstraction
1. Minimize use of RTTI and exceptions

---

## Hardware Abstraction with Interfaces

- Define abstract classes for hardware components
- Implement platform-specific behavior in derived classes

```cpp
class ILED {
public:
    virtual void on() = 0;
    virtual void off() = 0;
};

class GpioLed : public ILED {
    void on() override { /* write to GPIO */ }
    void off() override { /* write to GPIO */ }
};
```

---

## Example: Sensor Abstraction

```cpp
class ISensor {
public:
    virtual int read() = 0;
};

class AdcSensor : public ISensor {
    int read() override {
        // ADC hardware read
        return 42;
    }
};
```

---

## Encapsulation in Embedded Systems

- Group related data and functions
- Protects system integrity
- Makes hardware drivers easier to reason about and test

---

## Class Design Guidelines

- Keep classes small and focused
- Favor interfaces over implementation inheritance
- Isolate hardware access through drivers and interfaces

---

## Virtual Destructors

- Always declare destructors `virtual` in base classes
- Ensures proper cleanup in polymorphic scenarios

```cpp
class Device {
public:
    virtual ~Device() {}
};
```

---

## Polymorphism Benefits in Embedded

- Simplifies interface use across different implementations
- Decouples system logic from hardware details
- Enables mock hardware for unit testing

---

## Real-World Use: Driver Abstraction

- A motor controller can have:
    - A generic interface `IMotor`
    - Implementations like `PwmMotor` or `StepMotor`
- Higher-level logic uses `IMotor` without knowing implementation

---

## Static Polymorphism (CRTP)

- Avoids vtable overhead
- Enables polymorphism at compile time

```cpp
template<typename Derived>
class SensorBase {
public:
    int read() {
        return static_cast<Derived*>(this)->readImpl();
    }
};

class TempSensor : public SensorBase<TempSensor> {
public:
    int readImpl() { return 25; }
};
```

---

## OO and RTOS Integration

- OO patterns fit well with RTOS tasks and handlers
- Interfaces encapsulate task logic
- Message passing can follow observer pattern

---

## State Machines with OO

- Represent states as classes
- Use inheritance and polymorphism to switch behaviors
- Clear separation of concerns

---

## Example: State Pattern

```cpp
class State {
public:
    virtual void handle() = 0;
};

class IdleState : public State {
    void handle() override { /* idle handling */ }
};

class ActiveState : public State {
    void handle() override { /* active handling */ }
};
```

---

## Design Pattern: Strategy

- Define interchangeable behaviors
- Change behavior at runtime without modifying class

```cpp
class CompressionStrategy {
public:
    virtual void compress() = 0;
};

class ZipStrategy : public CompressionStrategy {
    void compress() override { /* zip */ }
};

class Context {
    CompressionStrategy* strategy;
public:
    void execute() { strategy->compress(); }
};
```

---

## Summary

- Inheritance enables reuse and polymorphism
- Use inheritance judiciously in embedded systems
- Abstract interfaces provide clean separation
- Prefer composition and static allocation when possible
- OO design improves modularity, testability, and maintainability
- OO patterns like State and Strategy enhance clarity and flexibility

---

## SOLID Principles

![solid_principles](svg/courses/embedded/effective-real-time-embedded-c-and-c++/13_object_oriented_design/solid_principles.svg)

---

## Design Patterns

![design_patterns](svg/courses/embedded/effective-real-time-embedded-c-and-c++/13_object_oriented_design/design_patterns.svg)
