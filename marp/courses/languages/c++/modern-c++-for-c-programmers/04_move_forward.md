# Move and Forward

---

## R-Value References

- New reference type introduced in C++11
- Denoted by double ampersand: `T&&`
- References to temporary objects (r-values)
- Key enabler for move semantics
- Distinguishes between temporary and persistent objects

---

## L-Values vs R-Values

- L-value: Has identity and can appear on left side of assignment
- R-value: Temporary value, can only appear on right side of assignment

```cpp
int x = 10;      // x is an l-value
int y = x + 20;  // (x + 20) is an r-value

// L-value examples
int a;           // a is an l-value
int& ref = a;    // ref is an l-value reference
a = 5;           // a can be assigned to

// R-value examples
int b = 5 + 3;   // (5 + 3) is an r-value
// (5 + 3) = 10; // Error: cannot assign to an r-value
int&& rref = 5;  // rref is an r-value reference
```

---

## R-Value Reference Rules

- R-value references bind to r-values (temporaries)
- L-value references to const can also bind to r-values
- Named r-value references behave like l-values

```cpp
// R-value reference binds to temporary
int&& rref1 = 42;  // OK

// L-value reference cannot bind to r-value (except const)
// int& ref1 = 42;  // Error
const int& ref2 = 42;  // OK - const& can bind to r-value

// An r-value reference variable is itself an l-value
int&& rref2 = rref1;  // Error: rref1 is an l-value despite its type
```

---

## Move Rather than Copy

- Traditional copy operations duplicate resources
- Moving "steals" resources from source object
- Much more efficient for resource-managing classes
- Leaves source in a valid but unspecified state

---

## Move Constructor: Example

```cpp
class Vector {
private:
    int* data;
    size_t size;

public:
    // Regular constructor
    Vector(size_t sz) : size(sz) {
        data = new int[size]();
        std::cout << "Regular constructor" << std::endl;
    }

    // Copy constructor
    Vector(const Vector& other) : size(other.size) {
        data = new int[size];
        std::copy(other.data, other.data + size, data);
        std::cout << "Copy constructor" << std::endl;
    }

    // Move constructor
    Vector(Vector&& other) noexcept : data(other.data), size(other.size) {
        // Take ownership of resources
        other.data = nullptr; // Leave source in valid state
        other.size = 0;
        std::cout << "Move constructor" << std::endl;
    }

    // Destructor
    ~Vector() {
        delete[] data;
    }
};
```

---

## Move Assignment Operator: Example

```cpp
class Vector {
    // Previous members...

    // Move assignment operator
    Vector& operator=(Vector&& other) noexcept {
        if (this != &other) {
            // Release current resources
            delete[] data;

            // Steal resources from other
            data = other.data;
            size = other.size;

            // Leave other in valid state
            other.data = nullptr;
            other.size = 0;
        }
        std::cout << "Move assignment" << std::endl;
        return *this;
    }
};

// Usage
Vector createVector(size_t size) {
    return Vector(size); // Return value is an r-value
}

void useVector() {
    Vector v1(100);                // Regular constructor
    Vector v2 = v1;                // Copy constructor
    Vector v3 = createVector(200); // Move constructor

    v1 = v2;                       // Copy assignment
    v1 = createVector(300);        // Move assignment
}
```

---

## Move Semantics Benefits

- Eliminates unnecessary deep copies
- Dramatically improves performance for large objects
- Enables efficient return-by-value
- Essential for move-only types (unique_ptr, ifstream, etc.)

```cpp
void performanceExample() {
    std::vector<std::string> v1;

    // Fill vector with large strings
    for (int i = 0; i < 1000; ++i) {
        v1.push_back(std::string(10000, 'x'));
    }

    // Without move semantics: ~1000 deep copies
    // With move semantics: ~1000 moves (much faster)
    std::vector<std::string> v2 = std::move(v1);

    // v1 is now in a valid but unspecified state
    std::cout << "v1 size after move: " << v1.size() << std::endl;
}
```

---

## Compiler Synthesized Member Functions

In C++11, compiler can synthesize:
1. Default constructor
1. Destructor
1. Copy constructor
1. Copy assignment operator
1. Move constructor
1. Move assignment operator

Default behavior:
- Performs memberwise copy/move for each member
- Calls base class copy/move operations

---

## Default and Delete Specifiers

```cpp
class DefaultedMembers {
public:
    // Request compiler-generated versions
    DefaultedMembers() = default;
    DefaultedMembers(const DefaultedMembers&) = default;
    DefaultedMembers(DefaultedMembers&&) = default;
    DefaultedMembers& operator=(const DefaultedMembers&) = default;
    DefaultedMembers& operator=(DefaultedMembers&&) = default;
    ~DefaultedMembers() = default;
};

class DeletedMembers {
public:
    DeletedMembers() = default;

    // Prevent copying
    DeletedMembers(const DeletedMembers&) = delete;
    DeletedMembers& operator=(const DeletedMembers&) = delete;

    // Allow moving
    DeletedMembers(DeletedMembers&&) = default;
    DeletedMembers& operator=(DeletedMembers&&) = default;
};
```

---

## Special Member Function Generation Rules

- Default constructor: Generated if no user-declared constructors
- Destructor: Generated if not user-declared
- Copy operations:
    - Not generated if user-declared move operations
    - Generated if not user-declared and no user-declared move operations
- Move operations:
    - Not generated if user-declared copy operations, destructor, or move operations
    - Generated if not user-declared and all copy/move/destructor not user-declared

---

## Rule of Three / Five / Zero

- Rule of Three (pre-C++11):
    - If you need to define any of destructor, copy constructor, copy assignment, you should define all three
- Rule of Five (C++11):
    - If you need custom destructor, add copy/move constructors and copy/move assignment
- Rule of Zero:
    - Prefer to define no custom copy/move/destructor if possible
    - Let compiler handle special functions

---

## Rule of Three Example

```cpp
class ResourceManager {
private:
    Resource* resource;

public:
    ResourceManager() : resource(new Resource()) {}

    // Rule of Three: Define all or none
    ~ResourceManager() {
        delete resource;
    }

    ResourceManager(const ResourceManager& other) :
        resource(new Resource(*other.resource)) {}

    ResourceManager& operator=(const ResourceManager& other) {
        if (this != &other) {
            delete resource;
            resource = new Resource(*other.resource);
        }
        return *this;
    }
};
```

---

## Rule of Five Example

```cpp
class ResourceManager {
private:
    Resource* resource;

public:
    ResourceManager() : resource(new Resource()) {}

    // Rule of Five: Define all or none
    ~ResourceManager() {
        delete resource;
    }

    // Copy operations
    ResourceManager(const ResourceManager& other) :
        resource(new Resource(*other.resource)) {}

    ResourceManager& operator=(const ResourceManager& other) {
        if (this != &other) {
            delete resource;
            resource = new Resource(*other.resource);
        }
        return *this;
    }

    // Move operations
    ResourceManager(ResourceManager&& other) noexcept :
        resource(other.resource) {
        other.resource = nullptr;
    }

    ResourceManager& operator=(ResourceManager&& other) noexcept {
        if (this != &other) {
            delete resource;
            resource = other.resource;
            other.resource = nullptr;
        }
        return *this;
    }
};
```

---

## Rule of Zero Example

```cpp
class SmartResourceManager {
private:
    std::unique_ptr<Resource> resource;

public:
    SmartResourceManager() : resource(std::make_unique<Resource>()) {}

    // No need to declare any special functions!
    // The compiler correctly handles:
    // - Destructor (calls unique_ptr destructor)
    // - Move constructor/assignment (moves unique_ptr)
    // - Copy operations are implicitly deleted (unique_ptr is move-only)
};

class CopyableResourceManager {
private:
    std::shared_ptr<Resource> resource;

public:
    CopyableResourceManager() : resource(std::make_shared<Resource>()) {}

    // No need to declare any special functions!
    // - Destructor (calls shared_ptr destructor)
    // - Move constructor/assignment (moves shared_ptr)
    // - Copy constructor/assignment (copies shared_ptr, not Resource)
};
```

---

## `std::swap`

- Generic algorithm to exchange values
- Standard way to implement copy-and-swap idiom
- Optimized for move semantics in C++11

```cpp
// Basic usage
int a = 5, b = 10;
std::swap(a, b); // Now a=10, b=5

// Custom swap implementation
class Widget {
    // ... member variables and functions

    friend void swap(Widget& a, Widget& b) noexcept {
        using std::swap;

        // Swap each member
        swap(a.m_data, b.m_data);
        swap(a.m_size, b.m_size);
        // etc.
    }
};

// Using swap for copy-and-swap idiom
Widget& Widget::operator=(Widget other) { // Other is a copy
    swap(*this, other);
    return *this;
}
```

---

## `std::move`

- Not actually a move operation
- Casts an expression to an r-value reference (enables moving)
- Doesn't move anything by itself
- Indicates that an object can be "moved from"

```cpp
std::string s1 = "Hello";
std::string s2 = "World";

// Without std::move - performs a copy
s2 = s1;
std::cout << "s1 after copy: " << s1 << std::endl;
// s1 still contains "Hello"

// With std::move - performs a move
s1 = "Hello again";
s2 = std::move(s1);
std::cout << "s1 after move: " << s1 << std::endl;
// s1 is in a valid but unspecified state (likely empty)
```

---

## `std::move` Implementation

```cpp
// Simplified implementation of std::move
template<typename T>
typename std::remove_reference<T>::type&& move(T&& param) {
    using ReturnType = typename std::remove_reference<T>::type&&;
    return static_cast<ReturnType>(param);
}

// Usage
std::string s1 = "Hello";
std::string s2 = std::move(s1); // s1 is moved into s2
```

---

## `std::forward`

- "Perfect forwarding" of arguments
- Preserves value category (l-value/r-value) of arguments
- Works with universal references (T&&)
- Conditionally casts to r-value only if original argument was an r-value

---

## Universal References

```cpp
// Regular r-value reference
void f(Widget&& w);

// Universal reference - template parameter deduction involved
template<typename T>
void g(T&& param); // "&&" here is NOT necessarily an r-value reference

// Usage
Widget w;
f(w);              // Error: cannot bind l-value to r-value reference
g(w);              // OK: T deduced as Widget&, so param is Widget&
g(Widget());       // OK: T deduced as Widget, so param is Widget&&
```

---

## Reference Collapsing Rules

When forming a reference to a reference, the following rules apply:
- T& & becomes T&
- T& && becomes T&
- T&& & becomes T&
- T&& && becomes T&&

This is key to understanding how universal references work:
```cpp
template<typename T>
void f(T&& param) {
    // If called with l-value:
    //   T = X&, param type = X& && = X&
    // If called with r-value:
    //   T = X, param type = X&&
}
```

---

## Perfect Forwarding: The Problem

```cpp
// We want to forward arguments exactly as received
template<typename T>
void wrapper(T&& arg) {
    // Problem: arg is always an l-value here (it has a name)
    foo(arg); // Will always call foo(T&) even if original was r-value
}

// Desired behavior:
// wrapper(lvalue) -> foo(lvalue)
// wrapper(rvalue) -> foo(rvalue)
```

---

## Perfect Forwarding: The Solution

```cpp
template<typename T, typename... Args>
std::unique_ptr<T> make_unique(Args&&... args) {
    // Perfect forwarding preserves value category
    return std::unique_ptr<T>(new T(std::forward<Args>(args)...));
}

// Usage
class Widget {
public:
    Widget(int x, std::string s) {}
};

int main() {
    int i = 42;
    std::string s = "text";

    // Works with l-values
    auto w1 = make_unique<Widget>(i, s);

    // Works with r-values too
    auto w2 = make_unique<Widget>(42, std::string("text"));

    // Works with mixed l-values and r-values
    auto w3 = make_unique<Widget>(i, std::string("text"));
}
```

---

## `std::forward` Implementation

```cpp
// Simplified implementation of std::forward
template<typename T>
T&& forward(typename std::remove_reference<T>::type& param) {
    return static_cast<T&&>(param);
}

template<typename T>
T&& forward(typename std::remove_reference<T>::type&& param) {
    static_assert(!std::is_lvalue_reference<T>::value,
                  "Cannot forward an r-value as an l-value");
    return static_cast<T&&>(param);
}

// Usage in template function
template<typename T, typename Arg>
void wrapper(Arg&& arg) {
    // Forward arg as the original value category
    f<T>(std::forward<Arg>(arg));
}
```

---

## Move Semantics Best Practices

1. Make move operations `noexcept`
1. Leave moved-from objects in a valid state
1. Don't assume anything about the state of moved-from objects
1. Return by value, let compiler optimize with RVO
1. Follow the Rule of Zero when possible
1. Use `std::move` for the last use of an object
1. Never use `std::move` on function return values

---

## Move Semantics: Best Practices Example

```cpp
class Widget {
private:
    std::unique_ptr<int[]> data;
    size_t size;

public:
    // Constructor allocates resources
    Widget(size_t n) : size(n), data(std::make_unique<int[]>(n)) {}

    // Move constructor marked noexcept - important for containers!
    Widget(Widget&& other) noexcept
        : data(std::move(other.data)), size(other.size) {
        other.size = 0; // Leave in valid state
    }

    // Move assignment also marked noexcept
    Widget& operator=(Widget&& other) noexcept {
        if (this != &other) {
            data = std::move(other.data);
            size = other.size;
            other.size = 0; // Leave in valid state
        }
        return *this;
    }

    // Use Widget - safe even for moved-from objects
    bool isEmpty() const { return size == 0 || data == nullptr; }
};
```

---

## Moving Only When Necessary

```cpp
void process(const std::string& lvalArg, std::string&& rvalArg) {
    // lvalArg is always an l-value - don't move from it!
    std::string s1 = lvalArg;      // copy

    // rvalArg is an l-value despite its type - must use std::move
    std::string s2 = rvalArg;      // copy!
    std::string s3 = std::move(rvalArg); // move

    // Last use of local variables - can move from them
    std::vector<std::string> v;
    v.push_back(s1);               // copy
    v.push_back(std::move(s2));    // move - s2 no longer needed

    // Don't move from function parameters unless they're r-value references
}
```

---

## Returning Values and RVO

```cpp
// Don't use std::move on return values!
Widget createWidget() {
    Widget w;
    // ... initialize w
    return w; // Don't write: return std::move(w);
}

// The compiler can use RVO to eliminate the copy/move
// Adding std::move actually disables this optimization!

// For returning parameters, do use std::move
Widget transformWidget(Widget w) {
    // ... transform w
    return std::move(w); // Parameter is already an object - move is appropriate
}
```

---

## Move-Only Types

- Types that can be moved but not copied
- Implemented by deleting copy operations
- Examples: `std::unique_ptr`, `std::future`, `std::thread`

```cpp
class MoveOnly {
public:
    MoveOnly() = default;

    // Delete copy operations
    MoveOnly(const MoveOnly&) = delete;
    MoveOnly& operator=(const MoveOnly&) = delete;

    // Enable move operations
    MoveOnly(MoveOnly&&) = default;
    MoveOnly& operator=(MoveOnly&&) = default;
};

void useMoveOnly() {
    MoveOnly m1;
    // MoveOnly m2 = m1;     // Error: copy constructor is deleted
    MoveOnly m3 = std::move(m1); // OK: uses move constructor
}
```

---

## Implementing Move for Classes with References/const Members

```cpp
class WidgetWithReference {
private:
    int& refMember;
    const int constMember;

public:
    WidgetWithReference(int& ref, int c)
        : refMember(ref), constMember(c) {}

    // Move not implicitly generated for classes with references
    WidgetWithReference(WidgetWithReference&& other)
        : refMember(other.refMember), constMember(other.constMember) {
        // Can't reset refMember or constMember, but we can still move
    }

    WidgetWithReference& operator=(WidgetWithReference&& other) {
        // Can't reassign refMember or constMember
        // Consider making class move-only but not assignable
        return *this;
    }
};
```

---

## Perfect Forwarding Constructor

```cpp
class Person {
private:
    std::string name;
    int age;

public:
    // Perfect forwarding constructor
    template<typename T1, typename T2>
    Person(T1&& n, T2&& a)
        : name(std::forward<T1>(n)), age(std::forward<T2>(a)) {}

    // Copy and move operations
    Person(const Person&) = default;
    Person(Person&&) = default;
    Person& operator=(const Person&) = default;
    Person& operator=(Person&&) = default;
};

// Usage
std::string name = "John";
Person p1(name, 30);               // name copied, 30 used directly
Person p2(std::string("Jane"), 25); // string moved, 25 used directly
Person p3(std::move(name), 35);    // name moved, 35 used directly
```

---

## Variadic Templates and Perfect Forwarding

```cpp
// Forward all arguments to a constructor
template<typename T, typename... Args>
std::unique_ptr<T> make_unique(Args&&... args) {
    return std::unique_ptr<T>(new T(std::forward<Args>(args)...));
}

// Forward all arguments to a function
template<typename F, typename... Args>
auto invoke(F&& f, Args&&... args)
    -> decltype(std::forward<F>(f)(std::forward<Args>(args)...)) {
    return std::forward<F>(f)(std::forward<Args>(args)...);
}

// Usage
auto ptr = make_unique<Widget>(42, "Hello", 3.14);

auto result = invoke([](int x, int y) { return x + y; }, 5, 10);
```

---

## Summary: Move and Forward

- R-value references enable efficient resource transfer
- Move semantics eliminate unnecessary copies
- Perfect forwarding preserves value categories
- `std::move` casts to r-value reference
- `std::forward` conditionally casts based on original value category
- Rule of Zero/Three/Five guide special member function implementation
- Move-only types prevent unwanted copying
- Modern C++ emphasizes move semantics for efficiency

---

## Lab Exercises

1. Implement a simple string class with move semantics
1. Create a move-only resource wrapper class
1. Write a function template that perfectly forwards its arguments
1. Benchmark the performance difference between copying and moving large objects
1. Convert a class to follow the Rule of Zero using standard library components
