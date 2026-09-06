# Polymorphism

---

## What is Polymorphism?

Polymorphism allows objects of different types to be treated as objects of a common base type

Key benefits:
1. Code reusability and flexibility
1. Runtime behavior selection
1. Clean separation of interface and implementation

```cpp
class Shape {
public:
    virtual void draw() = 0;
    virtual ~Shape() = default;
};

Shape* shapes[] = {new Circle(), new Rectangle()};
for(auto* shape : shapes) {
    shape->draw(); // Calls appropriate implementation
}
```

---

## Abstract Base Classes

Abstract base classes define interfaces that derived classes must implement

```cpp
class Animal {
public:
    virtual void makeSound() = 0;  // Pure virtual function
    virtual void move() = 0;
    virtual ~Animal() = default;   // Virtual destructor

protected:
    std::string name;              // Common data
};

class Dog : public Animal {
public:
    void makeSound() override { std::cout << "Woof!\n"; }
    void move() override { std::cout << "Running\n"; }
};
```

---

## Pure Virtual Functions

Pure virtual functions make a class abstract and must be overridden

```cpp
class Database {
public:
    // Pure virtual functions
    virtual bool connect(const std::string& url) = 0;
    virtual void execute(const std::string& query) = 0;
    virtual void close() = 0;

    // Can have non-pure virtual functions
    virtual void logQuery(const std::string& query) {
        std::cout << "Executing: " << query << std::endl;
    }
};
```

Cannot instantiate abstract classes:
```cpp
Database db;        // Error: cannot instantiate abstract class
Database* db = new MySQLDatabase();  // OK: concrete implementation
```

---

## Benefits of Polymorphism

![benefits_of_polymorphism](svg/courses/languages/c++/modern-c++-for-c-programmers/14_polymorphism/benefits_of_polymorphism.svg)

---

## Benefits of Polymorphism: Details

1. Write once, use with multiple types
1. Easy to add new implementations
1. Loose coupling between components
1. Enhanced testing through mocking

---

## Cost of Polymorphism

Virtual function calls have runtime overhead:

```cpp
class Base {
public:
    virtual void func() { /* implementation */ }  // Virtual call
    void nonVirtual() { /* implementation */ }     // Direct call
};
```

Performance considerations:
1. Virtual table lookup (vtable)
1. Indirect function call
1. Prevents some compiler optimizations
1. Memory overhead for vtable pointer

**Rule**: Use polymorphism when flexibility outweighs performance costs

---

## Virtual Function Mechanics: Overview

Each object with virtual functions contains a pointer to its class's virtual table

---

## Virtual Function Mechanics

![virtual_function_mechanics](svg/courses/languages/c++/modern-c++-for-c-programmers/14_polymorphism/virtual_function_mechanics.svg)

---

## Template Method Pattern

Define algorithm structure in base class, let derived classes implement steps

```cpp
class DataProcessor {
public:
    void process() {
        loadData();
        validateData();
        transformData();
        saveData();
    }

protected:
    virtual void loadData() = 0;
    virtual void validateData() = 0;
    virtual void transformData() = 0;
    virtual void saveData() = 0;
};

class CSVProcessor : public DataProcessor {
protected:
    void loadData() override { /* CSV specific loading */ }
    void validateData() override { /* CSV validation */ }
    // ... other implementations
};
```

---

## Template Method Benefits

![template_method_benefits](svg/courses/languages/c++/modern-c++-for-c-programmers/14_polymorphism/template_method_benefits.svg)

---

## Template Method Benefits: Details

1. Eliminates code duplication
1. Enforces consistent algorithm structure
1. Allows customization of specific steps
1. Easy to add new implementations

---

## Smart References

Smart references wrap raw pointers with additional behavior

```cpp
template<typename T>
class SmartReference {
private:
    T* ptr;

public:
    SmartReference(T* p) : ptr(p) {}

    T& operator*() {
        if (!ptr) throw std::runtime_error("Null reference");
        return *ptr;
    }

    T* operator->() {
        if (!ptr) throw std::runtime_error("Null reference");
        return ptr;
    }

    operator bool() const { return ptr != nullptr; }
};
```

---

## Smart Reference Use Cases

Smart references add safety and functionality:

```cpp
class LoggingReference {
    Shape* shape;
public:
    LoggingReference(Shape* s) : shape(s) {}

    Shape* operator->() {
        std::cout << "Accessing shape at " << shape << std::endl;
        return shape;
    }

    Shape& operator*() {
        std::cout << "Dereferencing shape" << std::endl;
        return *shape;
    }
};

LoggingReference ref(new Circle());
ref->draw();  // Logs access then calls Circle::draw()
```

---

## Templated Outward Conversions

Allow safe conversions from derived to base types in templates

```cpp
template<typename T>
class SmartPtr {
    T* ptr;

public:
    SmartPtr(T* p) : ptr(p) {}

    // Templated conversion constructor
    template<typename U>
    SmartPtr(const SmartPtr<U>& other) : ptr(other.get()) {
        static_assert(std::is_convertible_v<U*, T*>,
                     "Invalid conversion");
    }

    T* get() const { return ptr; }
};

SmartPtr<Circle> circle(new Circle());
SmartPtr<Shape> shape = circle;  // Safe upcast
```

---

## Conversion Safety

![conversion_safety](svg/courses/languages/c++/modern-c++-for-c-programmers/14_polymorphism/conversion_safety.svg)

---

## Conversion Safety: Overview

Upward conversions (derived to base) are always safe
Sideways conversions require runtime checks

---

## Curiously Recurring Template Pattern (CRTP)

A class derives from a template instantiation of itself

```cpp
template<typename Derived>
class Base {
public:
    void interface() {
        static_cast<Derived*>(this)->implementation();
    }

    void commonFunction() {
        // Common functionality for all derived classes
    }
};

class Concrete : public Base<Concrete> {
public:
    void implementation() {
        std::cout << "Concrete implementation" << std::endl;
    }
};
```

---

## CRTP Benefits

CRTP provides compile-time polymorphism:

```cpp
template<typename T>
class Counter {
protected:
    static int count;

public:
    Counter() { ++count; }
    Counter(const Counter&) { ++count; }
    ~Counter() { --count; }

    static int getCount() { return count; }
};

template<typename T>
int Counter<T>::count = 0;

class MyClass : public Counter<MyClass> {
    // Each derived class gets its own counter
};
```

**Advantages**: No virtual function overhead, type safety at compile time

---

## CRTP vs Virtual Functions: Overview

Choose based on requirements: flexibility vs performance

---

## CRTP vs Virtual Functions

![crtp_vs_virtual_functions](svg/courses/languages/c++/modern-c++-for-c-programmers/14_polymorphism/crtp_vs_virtual_functions.svg)

---

## Downcasting

Converting from base pointer to derived pointer

```cpp
class Shape {
public:
    virtual ~Shape() = default;
    virtual void draw() = 0;
};

class Circle : public Shape {
public:
    void draw() override { /* draw circle */ }
    void setRadius(double r) { radius = r; }
private:
    double radius;
};

// Safe downcasting with dynamic_cast
Shape* shape = new Circle();
Circle* circle = dynamic_cast<Circle*>(shape);
if (circle) {
    circle->setRadius(5.0);  // Safe to call Circle-specific method
}
```

---

## Dynamic Cast Safety

`dynamic_cast` provides runtime type checking:

```cpp
void processShape(Shape* shape) {
    // Try to downcast to specific types
    if (Circle* circle = dynamic_cast<Circle*>(shape)) {
        circle->setRadius(10.0);
        std::cout << "Processing circle\n";
    }
    else if (Rectangle* rect = dynamic_cast<Rectangle*>(shape)) {
        rect->setWidth(20.0);
        std::cout << "Processing rectangle\n";
    }
    else {
        std::cout << "Unknown shape type\n";
    }
}
```

**Important**: Only works with polymorphic types (classes with virtual functions)

---

## Static vs Dynamic Cast: Overview

Use `dynamic_cast` for safe downcasting, `static_cast` when you're certain

---

## Static vs Dynamic Cast

![static_vs_dynamic_cast](svg/courses/languages/c++/modern-c++-for-c-programmers/14_polymorphism/static_vs_dynamic_cast.svg)

---

## Visitor Pattern Alternative

Instead of downcasting, use the visitor pattern:

```cpp
class ShapeVisitor {
public:
    virtual void visit(Circle& circle) = 0;
    virtual void visit(Rectangle& rectangle) = 0;
    virtual ~ShapeVisitor() = default;
};

class Shape {
public:
    virtual void accept(ShapeVisitor& visitor) = 0;
    virtual ~Shape() = default;
};

class Circle : public Shape {
public:
    void accept(ShapeVisitor& visitor) override {
        visitor.visit(*this);
    }
    double getRadius() const { return radius; }
private:
    double radius;
};
```

---

## Visitor Pattern Implementation

```cpp
class AreaCalculator : public ShapeVisitor {
private:
    double totalArea = 0;

public:
    void visit(Circle& circle) override {
        totalArea += 3.14159 * circle.getRadius() * circle.getRadius();
    }

    void visit(Rectangle& rect) override {
        totalArea += rect.getWidth() * rect.getHeight();
    }

    double getTotalArea() const { return totalArea; }
};

// Usage
std::vector<std::unique_ptr<Shape>> shapes;
shapes.push_back(std::make_unique<Circle>());
shapes.push_back(std::make_unique<Rectangle>());

AreaCalculator calculator;
for (auto& shape : shapes) {
    shape->accept(calculator);
}
```

---

## Multiple Inheritance Polymorphism

A class can implement multiple interfaces:

```cpp
class Drawable {
public:
    virtual void draw() = 0;
    virtual ~Drawable() = default;
};

class Movable {
public:
    virtual void move(int x, int y) = 0;
    virtual ~Movable() = default;
};

class Sprite : public Drawable, public Movable {
public:
    void draw() override { /* drawing code */ }
    void move(int x, int y) override { /* movement code */ }
};
```

---

## Interface Segregation

Design specific interfaces rather than monolithic ones:

```cpp
// Poor design - fat interface
class MediaPlayer {
public:
    virtual void playAudio() = 0;
    virtual void playVideo() = 0;
    virtual void recordAudio() = 0;
    virtual void recordVideo() = 0;
};

// Better design - segregated interfaces
class AudioPlayer {
public:
    virtual void playAudio() = 0;
    virtual ~AudioPlayer() = default;
};

class AudioRecorder {
public:
    virtual void recordAudio() = 0;
    virtual ~AudioRecorder() = default;
};
```

---

## Polymorphic Containers

Store different types in the same container:

```cpp
#include <vector>
#include <memory>

class Animal {
public:
    virtual void makeSound() = 0;
    virtual ~Animal() = default;
};

class Dog : public Animal {
public:
    void makeSound() override { std::cout << "Woof!" << std::endl; }
};

class Cat : public Animal {
public:
    void makeSound() override { std::cout << "Meow!" << std::endl; }
};

std::vector<std::unique_ptr<Animal>> animals;
animals.push_back(std::make_unique<Dog>());
animals.push_back(std::make_unique<Cat>());

for (const auto& animal : animals) {
    animal->makeSound();  // Polymorphic call
}
```

---

## Type Erasure

Hide implementation details while maintaining polymorphic behavior:

```cpp
class Any {
private:
    struct Concept {
        virtual ~Concept() = default;
        virtual std::unique_ptr<Concept> clone() const = 0;
    };

    template<typename T>
    struct Model : Concept {
        T data;
        Model(T value) : data(std::move(value)) {}
        std::unique_ptr<Concept> clone() const override {
            return std::make_unique<Model<T>>(data);
        }
    };

    std::unique_ptr<Concept> ptr;

public:
    template<typename T>
    Any(T value) : ptr(std::make_unique<Model<T>>(std::move(value))) {}
};
```

---

## Function Objects and Polymorphism

Combine function objects with polymorphism:

```cpp
class Operation {
public:
    virtual double operator()(double a, double b) = 0;
    virtual ~Operation() = default;
};

class Add : public Operation {
public:
    double operator()(double a, double b) override {
        return a + b;
    }
};

class Multiply : public Operation {
public:
    double operator()(double a, double b) override {
        return a * b;
    }
};

double calculate(Operation& op, double x, double y) {
    return op(x, y);  // Polymorphic function call
}
```

---

## Performance Considerations: Overview

Consider performance vs flexibility trade-offs in critical code paths

---

## Performance Considerations

![performance_considerations](svg/courses/languages/c++/modern-c++-for-c-programmers/14_polymorphism/performance_considerations.svg)

---

## When to Use Polymorphism

Use polymorphism when:

1. **Multiple implementations** of the same interface exist
1. **Runtime type selection** is needed
1. **Extensibility** is important
1. **Code reuse** across different types is beneficial

Avoid when:
1. **Performance** is critical and overhead matters
1. **Only one implementation** will ever exist
1. **Compile-time selection** is sufficient

---

## Polymorphism Best Practices

1. **Always provide virtual destructors** in base classes
1. **Use pure virtual functions** to enforce interface contracts
1. **Prefer composition** over inheritance when possible
1. **Keep interfaces small** and focused
1. **Use smart pointers** for automatic memory management
1. **Consider CRTP** for compile-time polymorphism
1. **Document virtual function contracts** clearly

```cpp
class Base {
public:
    virtual ~Base() = default;  // Essential for proper cleanup
    virtual void doSomething() = 0;
};
```

---

## Modern C++ and Polymorphism

C++11/14/17 improvements for polymorphic code:

```cpp
// Override keyword for safety
class Derived : public Base {
public:
    void doSomething() override;  // Compiler checks override
    void helper() final;          // Cannot be overridden further
};

// Auto with polymorphism
auto factory() -> std::unique_ptr<Base> {
    return std::make_unique<Derived>();
}

// Range-based for with polymorphism
for (const auto& item : polymorphicContainer) {
    item->virtualMethod();
}
```

---

## Summary

Polymorphism in Modern C++:

1. **Virtual functions** enable runtime polymorphism
1. **Abstract base classes** define contracts
1. **Template Method Pattern** reuses algorithm structure
1. **CRTP** provides compile-time polymorphism
1. **Smart pointers** manage polymorphic objects safely
1. **Dynamic casting** enables safe downcasting
1. **Performance trade-offs** must be considered

Polymorphism is a powerful tool for creating flexible, maintainable code when used appropriately.
