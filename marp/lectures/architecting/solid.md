---
tags:
- concepts:oop
- concepts:design-patterns
- concepts:architecture
level: intermediate
category: architecture
audience:
- audiences:developers
---
# SOLID Principles
## Understanding the Foundation of Object-Oriented Design
## Mark Veltzer
## [mark.veltzer@gmail.com](mailto:mark.veltzer@gmail.com)

---

![title](svg/lectures/architecting/solid/title.svg)

## Overview
1. Single Responsibility Principle (SRP)
1. Open/Closed Principle (OCP)
1. Liskov Substitution Principle (LSP)
1. Interface Segregation Principle (ISP)
1. Dependency Inversion Principle (DIP)
---
## Why SOLID?
- Maintainable code
- Easier testing
- Flexible architecture
- Reduced technical debt
- Better scalability
- Easier to understand and modify
---
## Single Responsibility Principle

> "A class should have one, and only one, reason to change."
> - Robert C. Martin

---
## SRP - Bad Example

```java
class Employee {
    private String name;
    private double salary;

    public void calculatePay() { /* ... */ }
    public void saveToDatabase() { /* ... */ }
    public void generateReport() { /* ... */ }
    public void sendEmail() { /* ... */ }
}
```

---
## SRP - Violation Visualization

![srp_violation_visualization](svg/lectures/architecting/solid/srp_violation_visualization.svg)

---
## SRP - Good Example

```java
class Employee {
    private String name;
    private double salary;
}

class PayrollCalculator {
    public void calculatePay(Employee employee) { /* ... */ }
}

class EmployeeRepository {
    public void save(Employee employee) { /* ... */ }
}

class ReportGenerator {
    public void generateReport(Employee employee) { /* ... */ }
}

class EmailService {
    public void sendEmail(String to, String content) { /* ... */ }
}
```

---
## SRP - Better Structure

![srp_better_structure](svg/lectures/architecting/solid/srp_better_structure.svg)

---
## Open/Closed Principle

> "Software entities should be open for extension, but closed for modification."
> - Bertrand Meyer

---
## OCP - Bad Example

```java
class Rectangle {
    private double width;
    private double height;
    // getters, setters
}

class AreaCalculator {
    public double calculateArea(Object shape) {
        if (shape instanceof Rectangle) {
            Rectangle rect = (Rectangle) shape;
            return rect.getWidth() * rect.getHeight();
        }
        else if (shape instanceof Circle) {
            Circle circle = (Circle) shape;
            return Math.PI * circle.getRadius() * circle.getRadius();
        }
        return 0;
    }
}
```

---
## OCP - Violation Visualization

![ocp_violation_visualization](svg/lectures/architecting/solid/ocp_violation_visualization.svg)

---
## OCP - Good Example

```java
interface Shape {
    double calculateArea();
}

class Rectangle implements Shape {
    private double width;
    private double height;

    public double calculateArea() {
        return width * height;
    }
}

class Circle implements Shape {
    private double radius;

    public double calculateArea() {
        return Math.PI * radius * radius;
    }
}
```

---
## OCP - Better Structure

![ocp_better_structure](svg/lectures/architecting/solid/ocp_better_structure.svg)

---
## Liskov Substitution Principle

> "Objects in a program should be replaceable with instances of their subtypes without altering the correctness of that program."
> - Barbara Liskov

---
## LSP - Bad Example

```java
class Bird {
    public void fly() {
        // Implementation
    }
}

class Penguin extends Bird {
    @Override
    public void fly() {
        throw new UnsupportedOperationException("Penguins can't fly!");
    }
}
```

---
## LSP - Violation Visualization

![lsp_violation_visualization](svg/lectures/architecting/solid/lsp_violation_visualization.svg)

---
## LSP - Good Example

```java
interface Bird {
    void move();
}

interface FlyingBird extends Bird {
    void fly();
}

class Sparrow implements FlyingBird {
    public void move() { /* ... */ }
    public void fly() { /* ... */ }
}

class Penguin implements Bird {
    public void move() { /* ... */ }
}
```

---
## LSP - Better Structure

![lsp_better_structure](svg/lectures/architecting/solid/lsp_better_structure.svg)

---
## Interface Segregation Principle

> "Clients should not be forced to depend upon interfaces that they do not use."
> - Robert C. Martin

---
## ISP - Bad Example

```java
interface Worker {
    void work();
    void eat();
    void sleep();
}

class Human implements Worker {
    public void work() { /* ... */ }
    public void eat() { /* ... */ }
    public void sleep() { /* ... */ }
}

class Robot implements Worker {
    public void work() { /* ... */ }
    public void eat() { throw new UnsupportedOperationException(); }
    public void sleep() { throw new UnsupportedOperationException(); }
}
```

---
## ISP - Violation Visualization

![isp_violation_visualization](svg/lectures/architecting/solid/isp_violation_visualization.svg)

---
## ISP - Good Example

```java
interface Workable {
    void work();
}

interface Eatable {
    void eat();
}

interface Sleepable {
    void sleep();
}

class Human implements Workable, Eatable, Sleepable {
    public void work() { /* ... */ }
    public void eat() { /* ... */ }
    public void sleep() { /* ... */ }
}

class Robot implements Workable {
    public void work() { /* ... */ }
}
```

---
## ISP - Better Structure

![isp_better_structure](svg/lectures/architecting/solid/isp_better_structure.svg)

---
## Dependency Inversion Principle

> "High-level modules should not depend on low-level modules. Both should depend on abstractions."
> - Robert C. Martin

---
## DIP - Bad Example

```java
class LightBulb {
    public void turnOn() { /* ... */ }
    public void turnOff() { /* ... */ }
}

class Switch {
    private LightBulb bulb;

    public Switch() {
        this.bulb = new LightBulb();
    }

    public void operate() {
        // Direct dependency on LightBulb implementation
        bulb.turnOn();
    }
}
```

---
## DIP - Violation Visualization

![dip_violation_visualization](svg/lectures/architecting/solid/dip_violation_visualization.svg)

---
## DIP - Good Example

```java
interface Switchable {
    void turnOn();
    void turnOff();
}

class LightBulb implements Switchable {
    public void turnOn() { /* ... */ }
    public void turnOff() { /* ... */ }
}

class Switch {
    private final Switchable device;

    public Switch(Switchable device) {
        this.device = device;
    }

    public void operate() {
        device.turnOn();
    }
}
```

---
## DIP - Better Structure

![dip_better_structure](svg/lectures/architecting/solid/dip_better_structure.svg)

---
## Real-World Example: E-commerce System

Let's see how SOLID principles work together in a real system.

---
## E-commerce System - Bad Design

```java
class Order {
    private List<Item> items;

    public void addItem(Item item) { /* ... */ }
    public void calculateTotal() { /* ... */ }
    public void processPayment() { /* ... */ }
    public void saveToDatabase() { /* ... */ }
    public void sendConfirmationEmail() { /* ... */ }
    public void generateInvoice() { /* ... */ }
}
```

---
## E-commerce - Bad Design Visualization

![e_commerce_bad_design_visualization](svg/lectures/architecting/solid/e_commerce_bad_design_visualization.svg)

---
## E-commerce System - SOLID Design

```java
interface OrderRepository {
    void save(Order order);
}

interface PaymentProcessor {
    void process(Order order);
}

interface NotificationService {
    void notify(Order order);
}

class Order {
    private List<Item> items;
    private final OrderCalculator calculator;

    public void addItem(Item item) { /* ... */ }
}

class OrderService {
    private final OrderRepository repository;
    private final PaymentProcessor paymentProcessor;
    private final NotificationService notificationService;

    public void processOrder(Order order) {
        paymentProcessor.process(order);
        repository.save(order);
        notificationService.notify(order);
    }
}
```

---
## E-commerce - SOLID Design Visualization

![e_commerce_solid_design_visualization](svg/lectures/architecting/solid/e_commerce_solid_design_visualization.svg)

---
## Benefits of SOLID in the E-commerce Example
1. Single Responsibility: Each class has one job
1. Open/Closed: New payment methods without changing existing code
1. Liskov Substitution: Different repository implementations are interchangeable
1. Interface Segregation: Clients depend only on methods they need
1. Dependency Inversion: High-level OrderService depends on abstractions
---
## Common SOLID Violations
1. God Classes
1. Tight Coupling
1. Inheritance Abuse
1. Large Interfaces
1. Concrete Dependencies
---
## How to Identify SOLID Violations
1. Multiple responsibilities in one class
1. Frequent changes to existing code
1. Inheritance breaking functionality
1. Unused interface methods
1. Direct instantiation of dependencies
---
## Refactoring Towards SOLID
1. Extract Class
1. Extract Interface
1. Dependency Injection
1. Interface Segregation
1. Abstract Factory Pattern
---
## Testing Benefits with SOLID
- Easier unit testing
- Better mock objects
- Isolated components
- Focused test cases
- Improved test coverage
---
## Best Practices
1. Keep classes small and focused
1. Use composition over inheritance
1. Program to interfaces
1. Inject dependencies
1. Follow the Law of Demeter
---
## Common Questions
1. When to break SOLID principles?
1. How to balance SOLID with pragmatism?
1. What about performance impact?
1. How to handle legacy code?
1. Where to start applying SOLID?
---
## Tools and Techniques
1. Static Code Analysis
1. Design Pattern Recognition
1. Dependency Injection Frameworks
1. Refactoring IDEs
1. Architecture Validation Tools
---
## Summary
SOLID Principles:
1. Single Responsibility
1. Open/Closed
1. Liskov Substitution
1. Interface Segregation
1. Dependency Inversion
---
## Additional Resources
1. Clean Code by Robert C. Martin
1. Design Patterns by Gang of Four
1. Refactoring by Martin Fowler
1. Online courses and tutorials
1. Community discussions
