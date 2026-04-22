# Const, Copying and Conversions

---

## Const Consistency

- `const` is a contract with users of your code
- Indicates that an object will not be modified
- Helps compiler catch accidental modifications
- Enables compiler optimizations
- Creates more readable and maintainable code

---

## Const Correctness

- Apply `const` whenever possible
- Start with everything `const` and remove as needed
- Common usages:
    - `const` variables that shouldn't change
    - `const` member functions that don't modify object state
    - `const` parameters that function won't modify
    - Return by `const` reference to prevent modification

---

## Const Variables

```cpp
// Non-constant - can be modified
int count = 42;
count = 43; // OK

// Constant - cannot be modified
const int MAX_USERS = 100;
// MAX_USERS = 101; // Error: assignment of read-only variable

// Constant pointer to non-constant data
int value = 10;
int* const ptr = &value;
*ptr = 20;      // OK - can modify the data
// ptr = &count; // Error - cannot modify the pointer

// Constant pointer to constant data
const int* const constPtr = &MAX_USERS;
// *constPtr = 101; // Error - cannot modify the data
// constPtr = &count; // Error - cannot modify the pointer
```

---

## Const Parameters

```cpp
// Passing by value
void processValue(int value) {
    value = value * 2; // Modifies local copy, not original
}

// Passing by reference - can modify original
void processReference(int& value) {
    value = value * 2; // Modifies original value
}

// Passing by const reference - cannot modify original
void processConstReference(const int& value) {
    // value = value * 2; // Error: assignment of read-only reference
    int result = value * 2; // OK - using the value
}

// Passing by const pointer - cannot modify what it points to
void processConstPointer(const int* ptr) {
    // *ptr = 100; // Error: assignment of read-only location
    int result = *ptr * 2; // OK - using the value
}
```

---

## Const Member Functions

```cpp
class Counter {
private:
    int count;
    mutable int accessCount; // Can be modified even in const methods

public:
    Counter() : count(0), accessCount(0) {}

    // Non-const method - can modify the object
    void increment() {
        ++count;
    }

    // Const method - cannot modify the object (except mutable members)
    int getCount() const {
        ++accessCount; // OK - mutable member
        // ++count;    // Error - cannot modify non-mutable member
        return count;
    }

    // Another const method
    int getAccessCount() const {
        return accessCount;
    }
};

void useCounter() {
    Counter c;
    c.increment(); // OK

    const Counter cc;
    // cc.increment(); // Error - cannot call non-const method on const object
    cc.getCount();     // OK - const method
}
```

---

## Const Overloading

```cpp
class Container {
private:
    std::vector<int> data;

public:
    // Non-const version - returns reference that can modify
    int& at(size_t index) {
        return data.at(index);
    }

    // Const version - returns const reference that cannot modify
    const int& at(size_t index) const {
        return data.at(index);
    }
};

void useContainer() {
    Container c;
    c.at(0) = 42;        // Uses non-const version, can modify

    const Container cc;
    // cc.at(0) = 42;     // Error - uses const version, cannot modify
    int value = cc.at(0); // OK - can read value
}
```

---

## Logical vs Physical Constness

Physical constness:
- Doesn't modify any bits within the object
- What the compiler enforces with `const`

Logical constness:
- Appears constant to external users
- May modify internal implementation details
- Implemented using `mutable` keyword

---

## The `mutable` Keyword

```cpp
class CachedCalculator {
private:
    int input;
    mutable bool calculated;
    mutable int cachedResult;

public:
    CachedCalculator(int in)
        : input(in), calculated(false), cachedResult(0) {}

    int getResult() const {
        if (!calculated) {
            cachedResult = performExpensiveCalculation(input);
            calculated = true;
        }
        return cachedResult;
    }

private:
    int performExpensiveCalculation(int value) const {
        // Complex calculation here
        return value * value;
    }
};

// Usage
void useCalculator() {
    const CachedCalculator calc(42);
    int result = calc.getResult(); // Works despite modifying internal state
}
```

---

## Const Iterator Example

```cpp
void printVector(const std::vector<int>& vec) {
    // Method 1: Range-based for loop with const
    for (const int& value : vec) {
        std::cout << value << " ";
    }
    std::cout << std::endl;

    // Method 2: const_iterator (pre-C++11)
    for (std::vector<int>::const_iterator it = vec.begin();
         it != vec.end(); ++it) {
        std::cout << *it << " ";
    }
    std::cout << std::endl;

    // Method 3: auto with const_iterator (C++11)
    for (auto it = vec.cbegin(); it != vec.cend(); ++it) {
        std::cout << *it << " ";
        // *it = 42; // Error: assignment of read-only location
    }
    std::cout << std::endl;
}
```

---

## C++ Casts Overview

C++ provides type-safe casting operators:
- `static_cast`: Compile-time checked conversions
- `dynamic_cast`: Runtime checked downcasting
- `const_cast`: Add/remove const or volatile
- `reinterpret_cast`: Reinterpret bit patterns (dangerous)

---

## The `static_cast` Keyword

```cpp
// Numeric conversions
double d = 3.14159;
int i = static_cast<int>(d); // Explicit conversion from double to int

// Pointer conversions up inheritance hierarchy (upcast)
class Base {};
class Derived : public Base {};

Derived* derived = new Derived();
Base* base = static_cast<Base*>(derived); // OK - upcast is safe

// Convertible types
class Seconds {
public:
    explicit Seconds(int s) : value(s) {}
    int value;
};

class Minutes {
public:
    explicit Minutes(int m) : value(m) {}
    // Conversion to Seconds
    explicit operator Seconds() const {
        return Seconds(value * 60);
    }
    int value;
};

Minutes m(2);
Seconds s = static_cast<Seconds>(m); // Uses conversion operator
```

---

## The `dynamic_cast` Keyword

```cpp
class Base {
public:
    virtual ~Base() {} // Polymorphic base class
};

class Derived1 : public Base {
public:
    void derived1Method() { std::cout << "Derived1" << std::endl; }
};

class Derived2 : public Base {
public:
    void derived2Method() { std::cout << "Derived2" << std::endl; }
};

void processObject(Base* obj) {
    // Try to cast to Derived1
    if (Derived1* d1 = dynamic_cast<Derived1*>(obj)) {
        d1->derived1Method();
    }
    // Try to cast to Derived2
    else if (Derived2* d2 = dynamic_cast<Derived2*>(obj)) {
        d2->derived2Method();
    }
    else {
        std::cout << "Unknown derived type" << std::endl;
    }
}
```

---

## `dynamic_cast`: Reference Version

```cpp
// Reference version (throws std::bad_cast if fails)
void processObjectRef(Base& obj) {
    try {
        Derived1& d1 = dynamic_cast<Derived1&>(obj);
        d1.derived1Method();
    }
    catch (const std::bad_cast&) {
        std::cout << "Not a Derived1 object" << std::endl;
    }
}
```

---

## The `const_cast` Keyword

```cpp
void legacyFunction(char* buffer, size_t size) {
    // Function that doesn't use const but doesn't modify buffer
    // ...
}

void modernFunction(const char* constBuffer, size_t size) {
    // Need to call legacy function that takes non-const
    char* buffer = const_cast<char*>(constBuffer);
    legacyFunction(buffer, size);
    // Dangerous if legacyFunction actually modifies buffer!
}

// Another example - mutable method outside class
class Widget {
private:
    int value;
public:
    Widget(int v) : value(v) {}
    int getValue() const { return value; }
};

// External function that "logically" doesn't modify the Widget
void logWidget(Widget& w) {
    std::cout << "Widget value: " << w.getValue() << std::endl;
}

void processWidget(const Widget& constW) {
    // Need to call function taking non-const
    Widget& w = const_cast<Widget&>(constW);
    logWidget(w); // OK if logWidget doesn't actually modify
}
```

---

## The `reinterpret_cast` Keyword

```cpp
// Converting between pointer types
int* p = new int(42);
char* c = reinterpret_cast<char*>(p); // Dangerous!

// Converting between pointers and integers
uintptr_t address = reinterpret_cast<uintptr_t>(p);
int* p2 = reinterpret_cast<int*>(address);

// Type punning - interpret one type as another
struct Data {
    int x;
    double y;
};

Data d = {42, 3.14};
char* bytes = reinterpret_cast<char*>(&d);
// Can now access d's memory byte by byte
// DANGEROUS - can cause alignment issues and undefined behavior

// Function pointer conversion
typedef void (*FuncA)();
typedef int (*FuncB)();

void funcA() {}
FuncB b = reinterpret_cast<FuncB>(funcA); // DANGEROUS!
```

---

## C-Style Cast vs C++ Casts

C-style cast:
```cpp
int i = 42;
double d = (double)i; // Old C-style cast
float* fp = (float*)&i; // Dangerous C-style cast
```

Problems with C-style casts:
- Hard to spot in code
- Can perform any combination of conversions
- Compiler won't warn about dangerous conversions

Advantages of C++ casts:
- More visible in code
- Express intent clearly
- More type-safe
- Easier to search for in code reviews

---

## Converting Constructors

- Allow implicit conversion from another type
- Can cause unexpected behavior if not controlled
- Use `explicit` keyword to prevent implicit conversions

---

## Converting Constructors: Example

```cpp
class String {
private:
    char* data;
    size_t length;

public:
    // Converting constructor - allows implicit conversion
    String(const char* str) {
        length = strlen(str);
        data = new char[length + 1];
        strcpy(data, str);
    }

    // Regular destructor
    ~String() {
        delete[] data;
    }
};

void processString(const String& str) {
    // Process string
}

// Usage
void useString() {
    String s("Hello"); // Direct initialization
    String s2 = "World"; // Copy initialization - implicit conversion

    processString("Converted"); // Implicit conversion from const char*
}
```

---

## The `explicit` Keyword

```cpp
class String {
private:
    char* data;
    size_t length;

public:
    // Explicit constructor - prevents implicit conversion
    explicit String(const char* str) {
        length = strlen(str);
        data = new char[length + 1];
        strcpy(data, str);
    }

    ~String() {
        delete[] data;
    }
};

void processString(const String& str) {
    // Process string
}

// Usage
void useString() {
    String s("Hello"); // Direct initialization - OK
    // String s2 = "World"; // Error - implicit conversion not allowed

    // processString("Converted"); // Error - implicit conversion not allowed
    processString(String("Converted")); // OK - explicit conversion
}
```

---

## User-Defined Conversion Operators

- Allow conversion from your class to another type
- Should be used carefully to avoid confusion
- Consider making them `explicit` as well

---

## User-Defined Conversion Operators: Example

```cpp
class Meters {
private:
    double value;

public:
    explicit Meters(double val) : value(val) {}

    // Conversion operator to double
    operator double() const {
        return value;
    }
};

class Feet {
private:
    double value;

public:
    explicit Feet(double val) : value(val) {}

    // Explicit conversion operator to Meters
    explicit operator Meters() const {
        return Meters(value * 0.3048);
    }
};

void useConversions() {
    Meters m(5.0);
    double d = m; // Implicit conversion to double

    Feet f(20.0);
    // Meters m2 = f; // Error - explicit conversion not allowed implicitly
    Meters m2 = static_cast<Meters>(f); // OK - explicit conversion
}
```

---

## Copy Construction and Assignment

- Copy constructor: Creates a new object as a copy of an existing one
- Copy assignment operator: Assigns one object's value to another
- Both are generated by the compiler if not provided
- Follow the Rule of Three/Five/Zero

---

## Copy Constructor: Example

```cpp
class Array {
private:
    int* data;
    size_t size;

public:
    // Regular constructor
    Array(size_t sz) : size(sz) {
        data = new int[size]();
    }

    // Copy constructor
    Array(const Array& other) : size(other.size) {
        data = new int[size];
        for (size_t i = 0; i < size; ++i) {
            data[i] = other.data[i];
        }
    }

    // Destructor
    ~Array() {
        delete[] data;
    }
};

// Usage
Array a1(10);
Array a2 = a1; // Calls copy constructor
Array a3(a1);  // Also calls copy constructor
```

---

## Copy Assignment Operator: Example

```cpp
class Array {
private:
    int* data;
    size_t size;

public:
    // Regular constructor
    Array(size_t sz) : size(sz) {
        data = new int[size]();
    }

    // Copy constructor
    Array(const Array& other) : size(other.size) {
        data = new int[size];
        for (size_t i = 0; i < size; ++i) {
            data[i] = other.data[i];
        }
    }
```

---

## Copy Assignment Operator: Implementation

```cpp
    // Copy assignment operator
    Array& operator=(const Array& other) {
        if (this != &other) { // Self-assignment check
            // Free old resources
            delete[] data;

            // Allocate new resources
            size = other.size;
            data = new int[size];

            // Copy data
            for (size_t i = 0; i < size; ++i) {
                data[i] = other.data[i];
            }
        }
        return *this;
    }

    // Destructor
    ~Array() {
        delete[] data;
    }
};

// Usage
Array a1(10);
Array a2(5);
a2 = a1; // Calls copy assignment operator
```

---

## Copy-and-Swap Idiom

- Safe and exception-friendly way to implement assignment
- Handles self-assignment automatically
- Provides strong exception guarantee

```cpp
class Array {
private:
    int* data;
    size_t size;

public:
    // Regular constructor
    Array(size_t sz) : size(sz) {
        data = new int[size]();
    }

    // Copy constructor
    Array(const Array& other) : size(other.size) {
        data = new int[size];
        for (size_t i = 0; i < size; ++i) {
            data[i] = other.data[i];
        }
    }
```

---

## Copy-and-Swap: Assignment and Swap

```cpp
    // Copy assignment operator using copy-and-swap
    Array& operator=(Array other) { // Pass by value (creates a copy)
        swap(*this, other); // Swap with the copy
        return *this;
        // The copy's destructor cleans up the old data
    }

    // Swap function
    friend void swap(Array& first, Array& second) noexcept {
        using std::swap;
        swap(first.data, second.data);
        swap(first.size, second.size);
    }

    // Destructor
    ~Array() {
        delete[] data;
    }
};
```

---

## Efficiency: Copy Elision

- Compiler optimization that eliminates unnecessary copying
- C++11 guarantees certain types of copy elision
- Return Value Optimization (RVO) is the most common form

---

## Return Value Optimization (RVO)

```cpp
class Heavy {
private:
    std::vector<int> data;

public:
    Heavy() {
        std::cout << "Constructor" << std::endl;
        data.resize(1000000, 42);
    }

    Heavy(const Heavy& other) : data(other.data) {
        std::cout << "Copy constructor" << std::endl;
    }

    ~Heavy() {
        std::cout << "Destructor" << std::endl;
    }
};

// Without RVO, this would create a temporary that gets copied
Heavy createHeavy() {
    return Heavy(); // With RVO, this constructs directly in the caller's stack
}

// Usage
void useHeavy() {
    Heavy h = createHeavy(); // Only one constructor call with RVO
    // Without RVO: Constructor, Copy constructor, Destructor
    // With RVO: Just Constructor
}
```

---

## Named Return Value Optimization (NRVO)

```cpp
Heavy createHeavyNamed() {
    Heavy result; // Named local variable
    // Do something with result
    return result; // NRVO can eliminate the copy here too
}

// When NRVO applies, this also results in just one constructor call
```

---

## Disabling Copy Operations

```cpp
class Uncopyable {
public:
    Uncopyable() = default;

    // Disable copying
    Uncopyable(const Uncopyable&) = delete;
    Uncopyable& operator=(const Uncopyable&) = delete;

    // Other methods...
};

// Alternative approach (pre-C++11)
class LegacyUncopyable {
private:
    // Private copy operations prevent public copying
    LegacyUncopyable(const LegacyUncopyable&);
    LegacyUncopyable& operator=(const LegacyUncopyable&);

public:
    LegacyUncopyable() {}
    // Other methods...
};

// Usage
Uncopyable u1;
// Uncopyable u2 = u1; // Error: copy constructor is deleted
Uncopyable u3;
// u3 = u1; // Error: copy assignment operator is deleted
```

---

## Summary: Const, Copying and Conversions

- Use `const` consistently to express your intent
- Understand when to use `mutable` for logical constness
- Use appropriate C++ casts instead of C-style casts
- Control conversions with `explicit` constructors and conversion operators
- Implement copy operations correctly for classes with resources
- Use copy-and-swap for safe, exception-friendly assignment
- Understand and leverage compiler optimizations like RVO
- Delete copy operations when copying doesn't make sense

---

## Lab Exercises

1. Implement a class with proper const member functions
1. Create a resource-managing class with correct copy semantics
1. Refactor code to use proper C++ casts instead of C-style casts
1. Implement a class with controlled conversion behavior
1. Measure the impact of copy elision on performance
