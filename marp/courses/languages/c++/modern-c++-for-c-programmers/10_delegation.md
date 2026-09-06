# Delegation Techniques

## What is Delegation?

Delegation is a fundamental design principle where one object hands off responsibility for a task to another object

Key benefits:
- **Separation of concerns** - each class has a single responsibility
- **Flexibility** - can change behavior without modifying client code
- **Reusability** - delegated components can be reused in different contexts
- **Maintainability** - easier to test and debug isolated components

---

## Delegation Principles

Core principles that guide effective delegation:

1. **Single Responsibility** - each class should have one reason to change
1. **Loose Coupling** - minimize dependencies between components
1. **High Cohesion** - related functionality should be grouped together
1. **Favor Composition over Inheritance** - build complex behavior by combining simpler components

---

## Types of Delegation

C++ provides several mechanisms for delegation:

```cpp
// Composition - "has-a" relationship
class Engine { /* ... */ };
class Car {
    Engine engine;  // Car has an Engine
};

// Inheritance - "is-a" relationship
class Vehicle { /* ... */ };
class Car : public Vehicle {  // Car is a Vehicle
    /* ... */
};
```

---

## Composition

Composition represents a "has-a" relationship where objects contain other objects

```cpp
class Logger {
public:
    void log(const std::string& message) {
        std::cout << "[LOG] " << message << std::endl;
    }
};

class DatabaseManager {
private:
    Logger logger;  // Composition

public:
    void saveData(const std::string& data) {
        logger.log("Saving data: " + data);
        // Database save logic here
        logger.log("Data saved successfully");
    }
};
```

---

## Advantages of Composition

Composition offers several key advantages:

- **Runtime flexibility** - can change behavior at runtime
- **Multiple inheritance alternative** - avoid diamond problem
- **Clear ownership** - explicit lifetime management
- **Easy testing** - can inject mock objects

```cpp
class TextProcessor {
private:
    std::unique_ptr<Formatter> formatter;
    std::unique_ptr<Validator> validator;

public:
    void setFormatter(std::unique_ptr<Formatter> f) {
        formatter = std::move(f);
    }

    void process(const std::string& text) {
        if (validator->isValid(text)) {
            formatter->format(text);
        }
    }
};
```

---

## Composition Example: Graphics System

```cpp
class Point {
    double x, y;
public:
    Point(double x, double y) : x(x), y(y) {}
    double getX() const { return x; }
    double getY() const { return y; }
};

class Color {
    int r, g, b;
public:
    Color(int r, int g, int b) : r(r), g(g), b(b) {}
    std::string toString() const {
        return "rgb(" + std::to_string(r) + "," +
               std::to_string(g) + "," + std::to_string(b) + ")";
    }
};

class Shape {
protected:
    Point position;
    Color color;

public:
    Shape(Point pos, Color col) : position(pos), color(col) {}
    virtual void draw() const = 0;
};
```

---

## Adapter Pattern

The Adapter pattern allows incompatible interfaces to work together

```cpp
// Third-party library with incompatible interface
class LegacyPrinter {
public:
    void printDocument(const char* text) {
        std::cout << "Legacy: " << text << std::endl;
    }
};

// Our modern interface
class ModernPrinter {
public:
    virtual void print(const std::string& document) = 0;
};

// Adapter bridges the gap
class PrinterAdapter : public ModernPrinter {
private:
    LegacyPrinter* legacyPrinter;

public:
    PrinterAdapter(LegacyPrinter* printer) : legacyPrinter(printer) {}

    void print(const std::string& document) override {
        legacyPrinter->printDocument(document.c_str());
    }
};
```

---

## Object Adapter vs Class Adapter

**Object Adapter** (preferred in C++):
```cpp
class ObjectAdapter : public Target {
private:
    Adaptee* adaptee;  // Composition
public:
    ObjectAdapter(Adaptee* a) : adaptee(a) {}
    void request() override {
        adaptee->specificRequest();
    }
};
```

**Class Adapter** (using multiple inheritance):
```cpp
class ClassAdapter : public Target, private Adaptee {
public:
    void request() override {
        specificRequest();  // Direct call to inherited method
    }
};
```

---

## Adapter Pattern Example: File System

```cpp
class WindowsFileSystem {
public:
    void openFile(const char* filename) {
        std::cout << "Windows: Opening " << filename << std::endl;
    }
};

class UnixFileSystem {
public:
    void open_file(const std::string& name) {
        std::cout << "Unix: Opening " << name << std::endl;
    }
};

class FileSystemInterface {
public:
    virtual void openFile(const std::string& filename) = 0;
};

class WindowsAdapter : public FileSystemInterface {
private:
    WindowsFileSystem* windowsFS;
public:
    WindowsAdapter(WindowsFileSystem* fs) : windowsFS(fs) {}
    void openFile(const std::string& filename) override {
        windowsFS->openFile(filename.c_str());
    }
};
```

---

## Inheritance Basics

Inheritance models "is-a" relationships:

```cpp
class Animal {
protected:
    std::string name;

public:
    Animal(const std::string& n) : name(n) {}
    virtual void makeSound() const = 0;
    virtual ~Animal() = default;
};

class Dog : public Animal {
public:
    Dog(const std::string& n) : Animal(n) {}
    void makeSound() const override {
        std::cout << name << " says: Woof!" << std::endl;
    }
};

class Cat : public Animal {
public:
    Cat(const std::string& n) : Animal(n) {}
    void makeSound() const override {
        std::cout << name << " says: Meow!" << std::endl;
    }
};
```

---

## Public vs Protected vs Private Inheritance

```cpp
class Base {
public:
    void publicMethod() {}
protected:
    void protectedMethod() {}
private:
    void privateMethod() {}
};

class PublicDerived : public Base {
    // publicMethod() is public
    // protectedMethod() is protected
    // privateMethod() is not accessible
};

class ProtectedDerived : protected Base {
    // publicMethod() is protected
    // protectedMethod() is protected
    // privateMethod() is not accessible
};

class PrivateDerived : private Base {
    // publicMethod() is private
    // protectedMethod() is private
    // privateMethod() is not accessible
};
```

---

## When to Use Each Inheritance Type

**Public Inheritance** - "is-a" relationship:
```cpp
class Vehicle {};
class Car : public Vehicle {};  // Car IS-A Vehicle
```

**Protected Inheritance** - rarely used, controlled "is-a":
```cpp
class TimerImplementation {};
class Timer : protected TimerImplementation {};
```

**Private Inheritance** - "implemented-in-terms-of":
```cpp
class Timer {};
class Widget : private Timer {  // Widget implemented using Timer
public:
    void doSomething() {
        // Can use Timer's protected/public members
    }
};
```

---

## Multiple Inheritance

C++ allows a class to inherit from multiple base classes:

```cpp
class Flyable {
public:
    virtual void fly() = 0;
};

class Swimmable {
public:
    virtual void swim() = 0;
};

class Duck : public Flyable, public Swimmable {
public:
    void fly() override {
        std::cout << "Duck is flying" << std::endl;
    }

    void swim() override {
        std::cout << "Duck is swimming" << std::endl;
    }
};
```

---

## Multiple Inheritance Benefits

Multiple inheritance can be powerful when used correctly:

```cpp
class Drawable {
public:
    virtual void draw() const = 0;
};

class Clickable {
public:
    virtual void onClick() = 0;
};

class Button : public Drawable, public Clickable {
private:
    std::string text;

public:
    Button(const std::string& t) : text(t) {}

    void draw() const override {
        std::cout << "Drawing button: " << text << std::endl;
    }

    void onClick() override {
        std::cout << "Button clicked: " << text << std::endl;
    }
};
```

---

## The Diamond Problem: Overview

Multiple inheritance can lead to ambiguity.

---

## The Diamond Problem

![the_diamond_problem](svg/courses/languages/c++/modern-c++-for-c-programmers/10_delegation/the_diamond_problem.svg)

---

## The Diamond Problem (cont.)

```cpp
class Base {
public:
    void method() { std::cout << "Base::method" << std::endl; }
};

class Left : public Base {};
class Right : public Base {};

class Derived : public Left, public Right {
    // Ambiguous! Which Base::method?
    // void test() { method(); }  // ERROR: ambiguous
};
```

---

## Resolving Diamond Problem

Use scope resolution or virtual inheritance:

```cpp
class Derived : public Left, public Right {
public:
    void test() {
        Left::method();   // Explicitly call Left's version
        Right::method();  // Explicitly call Right's version
    }
};

// Or use virtual inheritance
class Left : virtual public Base {};
class Right : virtual public Base {};
class Derived : public Left, public Right {
    // Now only one Base subobject exists
public:
    void test() {
        method();  // No ambiguity
    }
};
```

---

## Virtual Inheritance

Virtual inheritance ensures only one instance of base class:

```cpp
class Animal {
protected:
    std::string name;
public:
    Animal(const std::string& n) : name(n) {}
};

class Mammal : virtual public Animal {
public:
    Mammal(const std::string& n) : Animal(n) {}
};

class Carnivore : virtual public Animal {
public:
    Carnivore(const std::string& n) : Animal(n) {}
};

class Dog : public Mammal, public Carnivore {
public:
    Dog(const std::string& n) : Animal(n), Mammal(n), Carnivore(n) {}
    // Only one Animal subobject
};
```

---

## Virtual Inheritance Constructor Rules

With virtual inheritance, most derived class calls virtual base constructor:

```cpp
class Base {
public:
    Base(int value) { std::cout << "Base: " << value << std::endl; }
};

class Middle1 : virtual public Base {
public:
    Middle1(int value) : Base(value) {}
};

class Middle2 : virtual public Base {
public:
    Middle2(int value) : Base(value) {}
};

class Derived : public Middle1, public Middle2 {
public:
    // Must call Base constructor directly
    Derived(int value) : Base(value), Middle1(value), Middle2(value) {}
};
```

---

## Name Hiding in Inheritance

Derived class names hide base class names:

```cpp
class Base {
public:
    void func() { std::cout << "Base::func()" << std::endl; }
    void func(int x) { std::cout << "Base::func(int)" << std::endl; }
};

class Derived : public Base {
public:
    void func() { std::cout << "Derived::func()" << std::endl; }
    // Base::func(int) is hidden!
};

void test() {
    Derived d;
    d.func();      // Calls Derived::func()
    // d.func(5);  // ERROR: no matching function
    d.Base::func(5);  // OK: explicit qualification
}
```

---

## Bringing Base Names into Scope

Use `using` declarations to bring hidden names back:

```cpp
class Base {
public:
    void func() { std::cout << "Base::func()" << std::endl; }
    void func(int x) { std::cout << "Base::func(int)" << std::endl; }
    void func(double x) { std::cout << "Base::func(double)" << std::endl; }
};

class Derived : public Base {
public:
    using Base::func;  // Bring all Base::func overloads into scope

    void func() { std::cout << "Derived::func()" << std::endl; }
    // Now Base::func(int) and Base::func(double) are also accessible
};

void test() {
    Derived d;
    d.func();      // Derived::func()
    d.func(5);     // Base::func(int)
    d.func(3.14);  // Base::func(double)
}
```

---

## Interface Classes

Pure abstract classes define contracts:

```cpp
class IDrawable {
public:
    virtual ~IDrawable() = default;
    virtual void draw() const = 0;
    virtual void move(int x, int y) = 0;
};

class ISerializable {
public:
    virtual ~ISerializable() = default;
    virtual std::string serialize() const = 0;
    virtual void deserialize(const std::string& data) = 0;
};

class Shape : public IDrawable, public ISerializable {
    // Must implement all pure virtual functions
};
```

---

## Interface Segregation Principle

Keep interfaces small and focused:

```cpp
// Bad: Fat interface
class IWorker {
public:
    virtual void work() = 0;
    virtual void eat() = 0;
    virtual void sleep() = 0;
};

// Good: Segregated interfaces
class IWorkable {
public:
    virtual void work() = 0;
};

class IFeedable {
public:
    virtual void eat() = 0;
};

class ISleepable {
public:
    virtual void sleep() = 0;
};

class Human : public IWorkable, public IFeedable, public ISleepable {
    // Implements all interfaces
};

class Robot : public IWorkable {
    // Only implements what makes sense
};
```

---

## Nested Classes

Classes can be defined inside other classes:

```cpp
class OuterClass {
private:
    int outerData;

public:
    class InnerClass {
    private:
        int innerData;

    public:
        InnerClass(int data) : innerData(data) {}

        void accessOuter(OuterClass& outer) {
            // Can access private members of outer class
            outer.outerData = 42;
        }
    };

    InnerClass createInner(int data) {
        return InnerClass(data);
    }
};
```

---

## Nested Class Access Rules

Nested classes have special access privileges:

```cpp
class Container {
private:
    static int staticData;
    int instanceData;

    class Iterator {
    public:
        Iterator(Container* container) : container(container) {}

        void process() {
            // Can access private static members
            staticData = 100;

            // Can access private instance members through pointer
            container->instanceData = 200;
        }

    private:
        Container* container;
    };

public:
    Iterator begin() { return Iterator(this); }
};
```

---

## Pimpl Idiom with Nested Classes

Use nested classes for implementation hiding:

```cpp
// Header file
class Widget {
public:
    Widget();
    ~Widget();
    void doSomething();

private:
    class Impl;
    std::unique_ptr<Impl> pImpl;
};

// Implementation file
class Widget::Impl {
public:
    void doSomething() {
        // Complex implementation details hidden
        std::cout << "Widget doing something complex" << std::endl;
    }

private:
    // Private implementation details
    std::vector<int> data;
    std::string config;
};

Widget::Widget() : pImpl(std::make_unique<Impl>()) {}
Widget::~Widget() = default;
void Widget::doSomething() { pImpl->doSomething(); }
```

---

## Friend Classes and Functions

Friends can access private members:

```cpp
class BankAccount {
private:
    double balance;

    friend class BankManager;  // Friend class
    friend void auditAccount(const BankAccount& account);  // Friend function

public:
    BankAccount(double initial) : balance(initial) {}
};

class BankManager {
public:
    void transferFunds(BankAccount& from, BankAccount& to, double amount) {
        if (from.balance >= amount) {  // Can access private balance
            from.balance -= amount;
            to.balance += amount;
        }
    }
};

void auditAccount(const BankAccount& account) {
    std::cout << "Account balance: " << account.balance << std::endl;
}
```

---

## Policy-Based Design

Use templates for compile-time delegation:

```cpp
template<typename StoragePolicy>
class SmartPointer : private StoragePolicy {
public:
    template<typename... Args>
    SmartPointer(Args&&... args) : StoragePolicy(std::forward<Args>(args)...) {}

    auto get() -> decltype(StoragePolicy::get()) {
        return StoragePolicy::get();
    }

    void reset() {
        StoragePolicy::reset();
    }
};

class ArrayStorage {
private:
    std::unique_ptr<int[]> ptr;
    size_t size;

public:
    ArrayStorage(size_t s) : ptr(std::make_unique<int[]>(s)), size(s) {}
    int* get() { return ptr.get(); }
    void reset() { ptr.reset(); }
};

using ArrayPtr = SmartPointer<ArrayStorage>;
```

---

## Delegation vs Inheritance Guidelines

**Use Composition When:**
- You need runtime flexibility
- You want to avoid inheritance hierarchies
- You need to combine behaviors from multiple sources
- You want clear ownership semantics

**Use Inheritance When:**
- You have a clear "is-a" relationship
- You need polymorphic behavior
- You want to provide a common interface
- You're extending existing functionality

---

## Mixin Pattern

Mixins provide reusable functionality:

```cpp
template<typename Derived>
class Comparable {
public:
    bool operator!=(const Derived& other) const {
        return !static_cast<const Derived&>(*this).operator==(other);
    }

    bool operator<=(const Derived& other) const {
        const auto& self = static_cast<const Derived&>(*this);
        return self < other || self == other;
    }

    bool operator>(const Derived& other) const {
        return !static_cast<const Derived&>(*this).operator<=(other);
    }

    bool operator>=(const Derived& other) const {
        return !static_cast<const Derived&>(*this).operator<(other);
    }
};
```

---

## Mixin Pattern: Usage Example

```cpp
class Number : public Comparable<Number> {
private:
    int value;

public:
    Number(int v) : value(v) {}

    bool operator==(const Number& other) const {
        return value == other.value;
    }

    bool operator<(const Number& other) const {
        return value < other.value;
    }

    // Gets !=, <=, >, >= for free from Comparable
};
```

---

## CRTP (Curiously Recurring Template Pattern)

Static polymorphism through templates:

```cpp
template<typename Derived>
class Base {
public:
    void interface() {
        static_cast<Derived*>(this)->implementation();
    }

    void commonMethod() {
        std::cout << "Common functionality" << std::endl;
    }
};

class Derived1 : public Base<Derived1> {
public:
    void implementation() {
        std::cout << "Derived1 implementation" << std::endl;
    }
};

class Derived2 : public Base<Derived2> {
public:
    void implementation() {
        std::cout << "Derived2 implementation" << std::endl;
    }
};

template<typename T>
void useBase(Base<T>& obj) {
    obj.interface();      // Calls derived implementation
    obj.commonMethod();   // Calls base implementation
}
```

---

## Delegation Best Practices

1. **Prefer composition over inheritance** for flexibility
1. **Use inheritance for "is-a" relationships** with polymorphism
1. **Keep interfaces small and focused** (Interface Segregation)
1. **Avoid deep inheritance hierarchies** (prefer flat, wide designs)
1. **Use virtual inheritance carefully** (performance implications)
1. **Make destructors virtual** in base classes
1. **Use RAII** for resource management in delegated objects

---

## Common Delegation Patterns Summary

**Composition**: Object contains other objects
**Adapter**: Bridge incompatible interfaces
**Inheritance**: "Is-a" relationships with polymorphism
**Multiple Inheritance**: Inherit from multiple base classes
**Virtual Inheritance**: Solve diamond problem
**Interface Classes**: Define contracts
**Nested Classes**: Helper classes with special access
**Policy-Based Design**: Compile-time delegation
**Mixins/CRTP**: Add functionality through inheritance

---

## Practical Example: Event System

```cpp
class IEventHandler {
public:
    virtual ~IEventHandler() = default;
    virtual void handleEvent(const std::string& event) = 0;
};

class EventManager {
private:
    std::vector<std::unique_ptr<IEventHandler>> handlers;

public:
    void addHandler(std::unique_ptr<IEventHandler> handler) {
        handlers.push_back(std::move(handler));
    }

    void fireEvent(const std::string& event) {
        for (auto& handler : handlers) {
            handler->handleEvent(event);
        }
    }
};

class LoggingHandler : public IEventHandler {
public:
    void handleEvent(const std::string& event) override {
        std::cout << "LOG: " << event << std::endl;
    }
};

class EmailHandler : public IEventHandler {
public:
    void handleEvent(const std::string& event) override {
        std::cout << "EMAIL: Sending notification for " << event << std::endl;
    }
};
```

---

## Performance Considerations

**Virtual Function Calls:**
- Small overhead due to vtable lookup
- Modern CPUs predict virtual calls well
- Consider CRTP for zero-overhead static polymorphism

**Multiple Inheritance:**
- Potential for larger object sizes
- Virtual inheritance has additional overhead
- Use judiciously and profile when performance matters

**Composition:**
- Additional indirection for delegated calls
- Can be optimized away by compiler
- Consider inlining for small, frequently called functions

---

## Testing Delegated Designs

Delegation makes testing easier:

```cpp
class MockLogger : public ILogger {
private:
    std::vector<std::string> messages;

public:
    void log(const std::string& message) override {
        messages.push_back(message);
    }

    const std::vector<std::string>& getMessages() const {
        return messages;
    }

    void clear() { messages.clear(); }
};

// In tests
TEST(DatabaseManager, LogsOperations) {
    auto mockLogger = std::make_unique<MockLogger>();
    auto* loggerPtr = mockLogger.get();

    DatabaseManager db(std::move(mockLogger));
    db.saveData("test data");

    EXPECT_EQ(loggerPtr->getMessages().size(), 2);
    EXPECT_EQ(loggerPtr->getMessages()[0], "Saving data: test data");
    EXPECT_EQ(loggerPtr->getMessages()[1], "Data saved successfully");
}
```
