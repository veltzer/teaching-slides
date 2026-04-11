# Modern C++ for C programmers

---

## An Overview of OO Programming and C++

- C++ extends C with object-oriented capabilities
- Combines efficiency of low-level programming with high-level abstractions
- Key OOP concepts in C++:
    - Encapsulation: Bundling data with methods that operate on that data
    - Inheritance: Creating new classes based on existing ones
    - Polymorphism: Treating objects of different types through a common interface

---

## An Overview of OO Programming and C++ (cont.)

```cpp
// C-style programming
float radius = 5.0;
float area = 3.14159 * radius * radius;

// Object-oriented approach
class Circle {
private:
    float radius;
public:
    Circle(float r) : radius(r) {}
    float area() const { return 3.14159 * radius * radius; }
};

Circle c(5.0);
float area = c.area();
```

---

## The Class Approach

- Classes are the primary mechanism for encapsulation in C++
- Components:
    - Data members (attributes)
    - Member functions (methods)
    - Access specifiers (public, private, protected)

---

## The Class Approach (cont.)

```cpp
class BankAccount {
private:
    double balance;
    std::string accountNumber;

public:
    // Constructor
    BankAccount(std::string accNum, double initialBalance = 0.0)
        : accountNumber(accNum), balance(initialBalance) {}

    void deposit(double amount) {
        if (amount > 0) balance += amount;
    }

    bool withdraw(double amount) {
        if (amount > 0 && balance >= amount) {
            balance -= amount;
            return true;
        }
        return false;
    }

    double getBalance() const { return balance; }
};
```

---

## Efficiency and Integrity Issues

- C++ designed to minimize runtime overhead
- No automatic garbage collection
- Manual memory management with `new` and `delete`
- Resource management patterns:
    - RAII (Resource Acquisition Is Initialization)
    - Smart pointers
    - Move semantics (C++11)

---

## Efficiency and Integrity Issues (cont.)

Common issues:
- Memory leaks
- Dangling pointers
- Double deletion
- Buffer overflows

```cpp
// Potential memory leak if exception occurs between new and delete
void riskyFunction() {
    Resource* res = new Resource();
    // If code here throws an exception, res is never deleted
    delete res;
}

// RAII approach prevents leaks
void safeFunction() {
    std::unique_ptr<Resource> res(new Resource());
    // If exception occurs, res is automatically deleted
}
```

---

## Composite Classes

- Object composition: building complex objects from simpler ones
- "Has-a" relationship
- Promotes code reuse without inheritance complexity

---

## Composite Classes (cont.)

```cpp
class Engine {
private:
    int horsepower;
public:
    Engine(int hp) : horsepower(hp) {}
    void start() { /* Implementation */ }
};

class Wheel {
public:
    void rotate() { /* Implementation */ }
};

class Car {
private:
    Engine engine;
    Wheel wheels[4];
    std::string model;
public:
    Car(std::string m, int hp) : model(m), engine(hp) {}
    void drive() {
        engine.start();
        for (auto& wheel : wheels) wheel.rotate();
    }
};
```

---

## Associative Classes

- Objects that maintain relationships with other objects
- Implementations:
    - Raw pointers (risky)
    - References (non-reassignable)
    - Smart pointers (safe)

---

## Associative Classes (cont.)

```cpp
class Department {
public:
    std::string name;
    Department(std::string n) : name(n) {}
};

class Employee {
private:
    std::string name;
    std::shared_ptr<Department> department; // Association
public:
    Employee(std::string n, std::shared_ptr<Department> d)
        : name(n), department(d) {}

    void transferTo(std::shared_ptr<Department> newDept) {
        department = newDept;
    }

    std::string getDepartmentName() const {
        return department ? department->name : "Unassigned";
    }
};
```

---

## Operator Overloading

- Define custom behavior for C++ operators
- Makes user-defined types behave like built-in types
- Improves code readability when used appropriately

---

## Operator Overloading (cont.)

```cpp
class Complex {
private:
    double real;
    double imag;

public:
    Complex(double r = 0, double i = 0) : real(r), imag(i) {}

    // Operator overloading as member function
    Complex operator+(const Complex& other) const {
        return Complex(real + other.real, imag + other.imag);
    }

    // Operator overloading as non-member function
    friend std::ostream& operator<<(std::ostream& os, const Complex& c) {
        os << c.real;
        if (c.imag >= 0) os << '+';
        os << c.imag << 'i';
        return os;
    }
};
```

---

## Class Properties

- Special member functions
- Access control
- Static members
- Const members and member functions

---

## Class Properties: Special Member Functions

1. Constructor: Initializes objects
1. Destructor: Cleans up resources
1. Copy constructor: Creates new object as copy of existing one
1. Copy assignment operator: Assigns one object to another
1. Move constructor (C++11): Transfers resources from one object to another
1. Move assignment operator (C++11): Transfers resources during assignment

---

## Class Properties: Static Members

```cpp
class Counter {
private:
    int id;
    static int nextId; // Declaration of static member

public:
    Counter() : id(nextId++) {}

    static int getCount() { // Static member function
        return nextId;
    }

    int getId() const { return id; }
};

// Definition of static member (outside class)
int Counter::nextId = 0;

// Usage
Counter c1, c2, c3;
std::cout << "Total count: " << Counter::getCount() << std::endl; // Outputs 3
```

---

## Class Properties: Const Correctness

```cpp
class Temperature {
private:
    double celsius;

public:
    Temperature(double c) : celsius(c) {}

    // Const member function - can be called on const objects
    double getCelsius() const {
        return celsius;
    }

    double getFahrenheit() const {
        return celsius * 9.0/5.0 + 32.0;
    }

    // Non-const member function - cannot be called on const objects
    void setCelsius(double c) {
        celsius = c;
    }
};

const Temperature freezing(0);
double c = freezing.getCelsius();    // OK - const method
// freezing.setCelsius(10);          // Error - can't modify const object
```

---

## Inheritance

- "Is-a" relationship between classes
- Base class (parent) and derived class (child)
- Types:
    - Public inheritance: "is-a" relationship
    - Protected inheritance: implementation inheritance
    - Private inheritance: implementation detail

---

## Inheritance (cont.)

```cpp
class Shape {
protected:
    int x, y;

public:
    Shape(int x0 = 0, int y0 = 0) : x(x0), y(y0) {}

    virtual void draw() const {
        std::cout << "Drawing shape at (" << x << "," << y << ")" << std::endl;
    }

    virtual double area() const {
        return 0;
    }
};

class Circle : public Shape {
private:
    double radius;

public:
    Circle(int x0, int y0, double r) : Shape(x0, y0), radius(r) {}

    void draw() const override {
        std::cout << "Drawing circle at (" << x << "," << y
                  << ") with radius " << radius << std::endl;
    }

    double area() const override {
        return 3.14159 * radius * radius;
    }
};
```

---

## Polymorphism

- Multiple forms of a single interface
- Implemented via virtual functions in C++
- Enables runtime binding of function calls
- Foundation of extensible OO designs

---

## Polymorphism (cont.)

```cpp
class Animal {
public:
    virtual void makeSound() const {
        std::cout << "..." << std::endl;
    }

    virtual ~Animal() {}  // Virtual destructor essential for polymorphic classes
};

class Dog : public Animal {
public:
    void makeSound() const override {
        std::cout << "Woof!" << std::endl;
    }
};

class Cat : public Animal {
public:
    void makeSound() const override {
        std::cout << "Meow!" << std::endl;
    }
};

// Polymorphic usage
void animalConcert(const Animal& animal) {
    animal.makeSound();
}

Dog dog;
Cat cat;
animalConcert(dog);  // Outputs: Woof!
animalConcert(cat);  // Outputs: Meow!
```

---

## Runtime Type Information (RTTI)

- Mechanisms to identify object type at runtime
- Components:
    - `dynamic_cast`: Safe downcasting in inheritance hierarchies
    - `typeid`: Returns type information of an expression
    - `type_info`: Holds type information

---

## RTTI Example

```cpp
void processAnimal(Animal* animal) {
    // Base class usage
    animal->makeSound();

    // Attempt to downcast
    if (Dog* dog = dynamic_cast<Dog*>(animal)) {
        // Dog-specific operations
        std::cout << "It's a dog!" << std::endl;
    }
    else if (Cat* cat = dynamic_cast<Cat*>(animal)) {
        // Cat-specific operations
        std::cout << "It's a cat!" << std::endl;
    }

    // Using typeid
    if (typeid(*animal) == typeid(Dog)) {
        std::cout << "Confirmed as Dog type" << std::endl;
    }
}
```

---

## Abstract Classes and Interfaces

- Abstract class: Contains at least one pure virtual function
- Interface: Only pure virtual functions (no implementation)
- Used to define contracts that derived classes must implement

---

## Abstract Classes Example

```cpp
class Drawable {  // Abstract class / Interface
public:
    virtual void draw() const = 0;  // Pure virtual function
    virtual ~Drawable() {}
};

class Rectangle : public Shape, public Drawable {
private:
    int width, height;

public:
    Rectangle(int x0, int y0, int w, int h)
        : Shape(x0, y0), width(w), height(h) {}

    void draw() const override {
        std::cout << "Drawing rectangle at (" << x << "," << y
                  << ") with width " << width
                  << " and height " << height << std::endl;
    }

    double area() const override {
        return width * height;
    }
};

// Cannot instantiate abstract classes
// Drawable d;  // Error
// Can use pointers/references to abstract types
Drawable* d = new Rectangle(10, 20, 30, 40);
d->draw();
delete d;
```

---

## Exception Handling Basics

- Mechanism for handling runtime errors
- Components:
    - `try`: Code that might throw an exception
    - `catch`: Handlers for exceptions
    - `throw`: Raises an exception

---

## Exception Handling Example

```cpp
class DivideByZeroException : public std::exception {
public:
    const char* what() const noexcept override {
        return "Division by zero attempted";
    }
};

double safeDivide(double numerator, double denominator) {
    if (denominator == 0) {
        throw DivideByZeroException();
    }
    return numerator / denominator;
}

try {
    double result = safeDivide(10, 0);
    std::cout << "Result: " << result << std::endl;
} catch (const DivideByZeroException& e) {
    std::cerr << "Error: " << e.what() << std::endl;
} catch (const std::exception& e) {
    std::cerr << "Standard exception: " << e.what() << std::endl;
} catch (...) {
    std::cerr << "Unknown exception occurred" << std::endl;
}
```

---

## Templates Basics

- Generic programming mechanism
- Enables type-independent code
- Compile-time polymorphism
- Function templates and class templates

---

## Template Examples

```cpp
// Function template
template<typename T>
T max(T a, T b) {
    return (a > b) ? a : b;
}

// Usage
int maxInt = max<int>(10, 20);      // 20
double maxDouble = max(3.14, 2.71); // 3.14 (type deduced)

// Class template
template<typename T, int Size = 10>
class Array {
private:
    T data[Size];

public:
    T& operator[](int index) {
        if (index < 0 || index >= Size) {
            throw std::out_of_range("Index out of bounds");
        }
        return data[index];
    }

    int size() const {
        return Size;
    }
};

// Usage
Array<int, 5> smallArray;
Array<double> defaultArray; // Size = 10
```

---

## Standard Template Library (STL) Overview

- Collection of container classes, algorithms, and iterators
- Promotes code reuse and efficiency
- Main components:
    - Containers: store collections of objects
    - Algorithms: process data in containers
    - Iterators: provide access to container elements
    - Function objects: customize algorithm behavior

---

## STL Containers Overview

- Sequence containers:
    - `vector`: Dynamic array
    - `list`: Doubly-linked list
    - `deque`: Double-ended queue
- Associative containers:
    - `set`: Collection of unique keys
    - `map`: Collection of key-value pairs
- Container adaptors:
    - `stack`: LIFO data structure
    - `queue`: FIFO data structure
    - `priority_queue`: Priority-based queue

---

## STL Algorithms Overview

```cpp
#include <vector>
#include <algorithm>
#include <iostream>

int main() {
    std::vector<int> numbers = {5, 2, 8, 1, 9};

    // Finding an element
    auto it = std::find(numbers.begin(), numbers.end(), 8);
    if (it != numbers.end()) {
        std::cout << "Found 8 at position " << (it - numbers.begin()) << std::endl;
    }

    // Sorting
    std::sort(numbers.begin(), numbers.end());

    // Applying a function to each element
    std::for_each(numbers.begin(), numbers.end(), [](int n) {
        std::cout << n << " ";
    });

    return 0;
}
```

---

## Summary: C++ Refresher

- C++ combines procedural and object-oriented paradigms
- Classes provide encapsulation of data and behavior
- Inheritance creates "is-a" relationships
- Polymorphism enables runtime flexibility
- Templates support generic programming
- STL provides ready-to-use containers and algorithms
- Modern C++ emphasizes safety and expressiveness

---

## Lab Exercises

1. Create a `Person` class with appropriate attributes and methods
1. Implement a class hierarchy for shapes with polymorphic area calculation
1. Create a templated container class with basic operations
1. Solve a problem using STL containers and algorithms
1. Implement a simple resource management class following RAII principles
