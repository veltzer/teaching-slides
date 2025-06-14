# Templates

---

## What are Templates?

Templates are C++ features that allow you to write generic code that works with different types.

Instead of writing separate functions for each type:
```cpp
int max(int a, int b) { return a > b ? a : b; }
double max(double a, double b) { return a > b ? a : b; }
string max(string a, string b) { return a > b ? a : b; }
```

Write one template:
```cpp
template<typename T>
T max(T a, T b) { return a > b ? a : b; }
```

---

## Why Use Templates?

1. **Code reuse** - write once, use with many types
1. **Type safety** - compile-time type checking
1. **Performance** - no runtime overhead
1. **Flexibility** - works with user-defined types
1. **STL foundation** - containers, algorithms, iterators

---

## Template Categories

<svg width="600" height="300" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="200" height="80" fill="#e6f3ff" stroke="#0066cc"/>
  <text x="150" y="75" text-anchor="middle" font-size="16" font-weight="bold">Function Templates</text>
  <text x="150" y="95" text-anchor="middle" font-size="12">Generic functions</text>
  <text x="150" y="110" text-anchor="middle" font-size="12">Template parameters</text>

  <rect x="350" y="50" width="200" height="80" fill="#ffe6e6" stroke="#cc0000"/>
  <text x="450" y="75" text-anchor="middle" font-size="16" font-weight="bold">Class Templates</text>
  <text x="450" y="95" text-anchor="middle" font-size="12">Generic classes</text>
  <text x="450" y="110" text-anchor="middle" font-size="12">Container classes</text>

  <rect x="50" y="170" width="200" height="80" fill="#e6ffe6" stroke="#00cc00"/>
  <text x="150" y="195" text-anchor="middle" font-size="16" font-weight="bold">Variable Templates</text>
  <text x="150" y="215" text-anchor="middle" font-size="12">Generic variables</text>
  <text x="150" y="230" text-anchor="middle" font-size="12">(C++14)</text>

  <rect x="350" y="170" width="200" height="80" fill="#fff0e6" stroke="#ff6600"/>
  <text x="450" y="195" text-anchor="middle" font-size="16" font-weight="bold">Alias Templates</text>
  <text x="450" y="215" text-anchor="middle" font-size="12">Template typedefs</text>
  <text x="450" y="230" text-anchor="middle" font-size="12">(C++11)</text>
</svg>

---

## Function Template Syntax

```cpp
template<typename T>
T functionName(T parameter) {
    // Function body using type T
    return result;
}

// Alternative syntax (equivalent)
template<class T>
T functionName(T parameter) {
    return result;
}
```

**Note:** `typename` and `class` are interchangeable in template parameters.

---

## Simple Function Template Example

```cpp
template<typename T>
T add(T a, T b) {
    return a + b;
}

int main() {
    int result1 = add(5, 3);           // T = int
    double result2 = add(2.5, 1.7);    // T = double
    string result3 = add("Hello", " World");  // T = string

    std::cout << result1 << std::endl;  // 8
    std::cout << result2 << std::endl;  // 4.2
    std::cout << result3 << std::endl;  // Hello World

    return 0;
}
```

---

## Template Instantiation

<svg width="600" height="400" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="20" width="500" height="60" fill="#f0f0f0" stroke="#333"/>
  <text x="300" y="40" text-anchor="middle" font-size="14" font-weight="bold">Template Definition</text>
  <text x="300" y="60" text-anchor="middle" font-size="12">template&lt;typename T&gt; T max(T a, T b)</text>

  <line x1="300" y1="80" x2="300" y2="120" stroke="#333" marker-end="url(#arrowhead)"/>

  <rect x="50" y="140" width="150" height="80" fill="#e6f3ff" stroke="#0066cc"/>
  <text x="125" y="160" text-anchor="middle" font-size="12" font-weight="bold">Call: max(5, 3)</text>
  <text x="125" y="180" text-anchor="middle" font-size="12">Instantiate:</text>
  <text x="125" y="200" text-anchor="middle" font-size="12">int max(int, int)</text>

  <rect x="225" y="140" width="150" height="80" fill="#ffe6e6" stroke="#cc0000"/>
  <text x="300" y="160" text-anchor="middle" font-size="12" font-weight="bold">Call: max(2.5, 1.7)</text>
  <text x="300" y="180" text-anchor="middle" font-size="12">Instantiate:</text>
  <text x="300" y="200" text-anchor="middle" font-size="12">double max(double, double)</text>

  <rect x="400" y="140" width="150" height="80" fill="#e6ffe6" stroke="#00cc00"/>
  <text x="475" y="160" text-anchor="middle" font-size="12" font-weight="bold">Call: max(s1, s2)</text>
  <text x="475" y="180" text-anchor="middle" font-size="12">Instantiate:</text>
  <text x="475" y="200" text-anchor="middle" font-size="12">string max(string, string)</text>

  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Multiple Template Parameters

```cpp
template<typename T, typename U>
auto multiply(T a, U b) -> decltype(a * b) {
    return a * b;
}

// C++14 and later - auto return type deduction
template<typename T, typename U>
auto multiply(T a, U b) {
    return a * b;
}

int main() {
    auto result1 = multiply(5, 2.5);      // int * double = double
    auto result2 = multiply(3.14, 2);     // double * int = double

    std::cout << result1 << std::endl;    // 12.5
    std::cout << result2 << std::endl;    // 6.28

    return 0;
}
```

---

## Template Argument Deduction

```cpp
template<typename T>
void printValue(T value) {
    std::cout << "Value: " << value << std::endl;
}

int main() {
    // Automatic deduction
    printValue(42);        // T deduced as int
    printValue(3.14);      // T deduced as double
    printValue("Hello");   // T deduced as const char*

    // Explicit specification
    printValue<std::string>("Hello");  // T explicitly set to string
    printValue<double>(42);            // T explicitly set to double

    return 0;
}
```

---

## Template Specialization

Sometimes you need different behavior for specific types:

```cpp
template<typename T>
void print(T value) {
    std::cout << "Generic: " << value << std::endl;
}

// Full specialization for bool
template<>
void print<bool>(bool value) {
    std::cout << "Boolean: " << (value ? "true" : "false") << std::endl;
}

int main() {
    print(42);      // Uses generic version
    print(3.14);    // Uses generic version
    print(true);    // Uses specialized version

    return 0;
}
```

---

## Class Templates

```cpp
template<typename T>
class Stack {
private:
    std::vector<T> elements;
public:
    void push(const T& element) {
        elements.push_back(element);
    }

    T pop() {
        if (elements.empty()) {
            throw std::runtime_error("Stack is empty");
        }
        T top = elements.back();
        elements.pop_back();
        return top;
    }

    bool empty() const {
        return elements.empty();
    }

    size_t size() const {
        return elements.size();
    }
};
```

---

## Using Class Templates

```cpp
int main() {
    // Must specify template argument for class templates
    Stack<int> intStack;
    Stack<std::string> stringStack;

    // Using int stack
    intStack.push(10);
    intStack.push(20);
    intStack.push(30);

    while (!intStack.empty()) {
        std::cout << intStack.pop() << " ";
    }
    std::cout << std::endl;  // Output: 30 20 10

    // Using string stack
    stringStack.push("First");
    stringStack.push("Second");
    std::cout << stringStack.pop() << std::endl;  // Output: Second

    return 0;
}
```

---

## Template Parameters Types

1. **Type parameters** - most common
1. **Non-type parameters** - values known at compile time
1. **Template template parameters** - templates as parameters

```cpp
// Type parameter
template<typename T>
class Container { };

// Non-type parameter
template<int Size>
class FixedArray {
    int data[Size];
};

// Template template parameter
template<template<typename> class Container>
class Adapter { };
```

---

## Non-Type Template Parameters

```cpp
template<typename T, int Size>
class Array {
private:
    T data[Size];
public:
    T& operator[](int index) {
        return data[index];
    }

    const T& operator[](int index) const {
        return data[index];
    }

    constexpr int size() const {
        return Size;
    }
};

int main() {
    Array<int, 10> arr1;    // Array of 10 integers
    Array<double, 5> arr2;  // Array of 5 doubles

    arr1[0] = 100;
    std::cout << "Array size: " << arr1.size() << std::endl;

    return 0;
}
```

---

## Default Template Arguments

```cpp
template<typename T = int, int Size = 10>
class Buffer {
private:
    T data[Size];
public:
    void set(int index, const T& value) {
        if (index >= 0 && index < Size) {
            data[index] = value;
        }
    }

    T get(int index) const {
        return (index >= 0 && index < Size) ? data[index] : T{};
    }
};

int main() {
    Buffer<> buf1;              // Buffer<int, 10>
    Buffer<double> buf2;        // Buffer<double, 10>
    Buffer<char, 20> buf3;      // Buffer<char, 20>

    return 0;
}
```

---

## Template Member Functions

```cpp
class Printer {
public:
    template<typename T>
    void print(const T& value) {
        std::cout << "Printing: " << value << std::endl;
    }

    template<typename T>
    void printArray(const T* arr, int size) {
        for (int i = 0; i < size; ++i) {
            std::cout << arr[i] << " ";
        }
        std::cout << std::endl;
    }
};

int main() {
    Printer p;
    p.print(42);
    p.print("Hello");

    int arr[] = {1, 2, 3, 4, 5};
    p.printArray(arr, 5);

    return 0;
}
```

---

## Class Template Specialization

```cpp
template<typename T>
class Vector {
private:
    T* data;
    size_t size;
public:
    // General implementation
    void add(const T& element) {
        // Add element to vector
    }
};

// Specialization for bool - uses bit packing
template<>
class Vector<bool> {
private:
    unsigned char* data;
    size_t size;
public:
    void add(bool element) {
        // Specialized implementation for bool
        // Uses bit manipulation for space efficiency
    }
};
```

---

## Partial Template Specialization

```cpp
// Primary template
template<typename T, typename U>
class Pair {
public:
    T first;
    U second;
    void print() {
        std::cout << "Generic pair: " << first << ", " << second << std::endl;
    }
};

// Partial specialization - both types are the same
template<typename T>
class Pair<T, T> {
public:
    T first;
    T second;
    void print() {
        std::cout << "Same type pair: " << first << ", " << second << std::endl;
    }
};

// Partial specialization - second type is pointer
template<typename T, typename U>
class Pair<T, U*> {
public:
    T first;
    U* second;
    void print() {
        std::cout << "Pointer pair: " << first << ", " << *second << std::endl;
    }
};
```

---

## Template Type Deduction

```cpp
template<typename T>
void func(T param) { }

template<typename T>
void func2(T& param) { }

template<typename T>
void func3(const T& param) { }

int main() {
    int x = 42;
    const int cx = x;
    const int& rx = x;

    func(x);    // T = int, param type = int
    func(cx);   // T = int, param type = int (const dropped)
    func(rx);   // T = int, param type = int (const and & dropped)

    func2(x);   // T = int, param type = int&
    func2(cx);  // T = const int, param type = const int&
    func2(rx);  // T = const int, param type = const int&

    return 0;
}
```

---

## Function Template Overloading

```cpp
template<typename T>
void process(T value) {
    std::cout << "Generic version: " << value << std::endl;
}

template<typename T>
void process(T* ptr) {
    std::cout << "Pointer version: " << *ptr << std::endl;
}

// Non-template function
void process(int value) {
    std::cout << "Non-template int version: " << value << std::endl;
}

int main() {
    int x = 42;
    int* px = &x;
    double d = 3.14;

    process(x);   // Calls non-template version (exact match preferred)
    process(px);  // Calls pointer template version
    process(d);   // Calls generic template version

    return 0;
}
```

---

## Template Constraints (C++20 Concepts)

```cpp
#include <concepts>

// Concept definition
template<typename T>
concept Addable = requires(T a, T b) {
    a + b;  // T must support addition
};

template<typename T>
concept Printable = requires(T t) {
    std::cout << t;  // T must be printable
};

// Constrained template
template<Addable T>
T add(T a, T b) {
    return a + b;
}

// Multiple constraints
template<typename T>
requires Addable<T> && Printable<T>
void addAndPrint(T a, T b) {
    T result = a + b;
    std::cout << "Result: " << result << std::endl;
}
```

---

## SFINAE (Substitution Failure Is Not An Error)

```cpp
#include <type_traits>

// Enable if T is integral
template<typename T>
typename std::enable_if<std::is_integral<T>::value, void>::type
processNumber(T value) {
    std::cout << "Processing integer: " << value << std::endl;
}

// Enable if T is floating point
template<typename T>
typename std::enable_if<std::is_floating_point<T>::value, void>::type
processNumber(T value) {
    std::cout << "Processing float: " << value << std::endl;
}

int main() {
    processNumber(42);      // Calls integer version
    processNumber(3.14);    // Calls floating point version
    // processNumber("hi");  // Compilation error - no matching function

    return 0;
}
```

---

## Template Metaprogramming

```cpp
// Compile-time factorial calculation
template<int N>
struct Factorial {
    static constexpr int value = N * Factorial<N - 1>::value;
};

// Specialization for base case
template<>
struct Factorial<0> {
    static constexpr int value = 1;
};

// Type selection based on condition
template<bool Condition, typename TrueType, typename FalseType>
struct Conditional {
    using type = TrueType;
};

template<typename TrueType, typename FalseType>
struct Conditional<false, TrueType, FalseType> {
    using type = FalseType;
};

int main() {
    constexpr int fact5 = Factorial<5>::value;  // 120
    std::cout << "5! = " << fact5 << std::endl;

    using SelectedType = Conditional<true, int, double>::type;  // int

    return 0;
}
```

---

## Variadic Templates

```cpp
// Base case - no arguments
void print() {
    std::cout << std::endl;
}

// Recursive case - at least one argument
template<typename T, typename... Args>
void print(T first, Args... rest) {
    std::cout << first << " ";
    print(rest...);  // Recursive call with remaining arguments
}

int main() {
    print(1, 2.5, "hello", 'x');  // Output: 1 2.5 hello x
    print("Just one argument");    // Output: Just one argument
    print();                       // Output: (just newline)

    return 0;
}
```

---

## Variadic Template Example: Tuple

```cpp
template<typename... Types>
class Tuple;

// Base case - empty tuple
template<>
class Tuple<> { };

// Recursive case
template<typename Head, typename... Tail>
class Tuple<Head, Tail...> : private Tuple<Tail...> {
private:
    Head head;
public:
    Tuple(Head h, Tail... t) : Tuple<Tail...>(t...), head(h) { }

    Head getHead() const { return head; }
    Tuple<Tail...> getTail() const { return *this; }
};

int main() {
    Tuple<int, double, std::string> t(42, 3.14, "hello");
    std::cout << t.getHead() << std::endl;  // 42

    return 0;
}
```

---

## Perfect Forwarding

```cpp
template<typename T>
void wrapper(T&& arg) {
    // Forward arg to another function
    process(std::forward<T>(arg));
}

void process(int& x) {
    std::cout << "Processing lvalue: " << x << std::endl;
}

void process(int&& x) {
    std::cout << "Processing rvalue: " << x << std::endl;
}

int main() {
    int x = 42;
    wrapper(x);        // Forwards as lvalue
    wrapper(100);      // Forwards as rvalue

    return 0;
}
```

---

## Template Alias (C++11)

```cpp
// Traditional typedef
typedef std::vector<std::string> StringVector;

// Template alias - more flexible
template<typename T>
using Vector = std::vector<T>;

template<typename Key, typename Value>
using Dictionary = std::map<Key, Value>;

// Alias for complex types
template<typename T>
using SharedPtr = std::shared_ptr<T>;

int main() {
    Vector<int> numbers = {1, 2, 3, 4, 5};
    Dictionary<std::string, int> ages = {
        {"Alice", 25}, {"Bob", 30}
    };
    SharedPtr<int> ptr = std::make_shared<int>(42);

    return 0;
}
```

---

## Variable Templates (C++14)

```cpp
// Variable template
template<typename T>
constexpr T pi = T(3.1415926535897932385);

// Variable template with non-type parameter
template<int N>
constexpr int factorial = N * factorial<N - 1>;

// Specialization for base case
template<>
constexpr int factorial<0> = 1;

int main() {
    std::cout << "Pi as float: " << pi<float> << std::endl;
    std::cout << "Pi as double: " << pi<double> << std::endl;
    std::cout << "5! = " << factorial<5> << std::endl;  // 120

    return 0;
}
```

---

## Template Template Parameters

```cpp
template<template<typename> class Container>
class Stack {
private:
    Container<int> data;
public:
    void push(int value) {
        // Implementation depends on Container interface
    }

    int pop() {
        // Implementation depends on Container interface
    }
};

// Usage with different container types
int main() {
    Stack<std::vector> vectorStack;    // Uses std::vector internally
    Stack<std::list> listStack;       // Uses std::list internally
    Stack<std::deque> dequeStack;     // Uses std::deque internally

    return 0;
}
```

---

## Template Compilation Model

<svg width="600" height="400" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="150" height="80" fill="#e6f3ff" stroke="#0066cc"/>
  <text x="125" y="75" text-anchor="middle" font-size="14" font-weight="bold">Template</text>
  <text x="125" y="95" text-anchor="middle" font-size="14" font-weight="bold">Definition</text>
  <text x="125" y="115" text-anchor="middle" font-size="12">header.h</text>

  <rect x="250" y="50" width="150" height="80" fill="#ffe6e6" stroke="#cc0000"/>
  <text x="325" y="75" text-anchor="middle" font-size="14" font-weight="bold">Template</text>
  <text x="325" y="95" text-anchor="middle" font-size="14" font-weight="bold">Usage</text>
  <text x="325" y="115" text-anchor="middle" font-size="12">main.cpp</text>

  <rect x="450" y="50" width="150" height="80" fill="#e6ffe6" stroke="#00cc00"/>
  <text x="525" y="75" text-anchor="middle" font-size="14" font-weight="bold">Instantiated</text>
  <text x="525" y="95" text-anchor="middle" font-size="14" font-weight="bold">Code</text>
  <text x="525" y="115" text-anchor="middle" font-size="12">object file</text>

  <line x1="200" y1="90" x2="250" y2="90" stroke="#333" marker-end="url(#arrowhead)"/>
  <line x1="400" y1="90" x2="450" y2="90" stroke="#333" marker-end="url(#arrowhead)"/>

  <text x="225" y="85" text-anchor="middle" font-size="10">include</text>
  <text x="425" y="85" text-anchor="middle" font-size="10">instantiate</text>

  <rect x="150" y="200" width="300" height="150" fill="#f9f9f9" stroke="#666"/>
  <text x="300" y="220" text-anchor="middle" font-size="14" font-weight="bold">Template must be visible at point of use</text>
  <text x="300" y="245" text-anchor="middle" font-size="12">• Usually defined in header files</text>
  <text x="300" y="265" text-anchor="middle" font-size="12">• Cannot separate declaration/definition</text>
  <text x="300" y="285" text-anchor="middle" font-size="12">• Instantiation happens at compile time</text>
  <text x="300" y="305" text-anchor="middle" font-size="12">• Each instantiation creates new code</text>
  <text x="300" y="325" text-anchor="middle" font-size="12">• Can lead to code bloat</text>

  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Template Error Messages

Common template errors and solutions:

```cpp
template<typename T>
void func(T value) {
    value.someMethod();  // Error if T doesn't have someMethod
}

// Better approach with concepts (C++20)
template<typename T>
concept HasSomeMethod = requires(T t) {
    t.someMethod();
};

template<HasSomeMethod T>
void func(T value) {
    value.someMethod();
}
```

---

## Template Best Practices

1. **Keep templates simple** - complex templates are hard to debug
1. **Use concepts** (C++20) or SFINAE for constraints
1. **Provide clear error messages** with static_assert
1. **Document template requirements** clearly
1. **Prefer function templates over macros**
1. **Use template aliases** for complex types
1. **Be careful with template instantiation** - can cause code bloat

---

## Template Debugging Tips

```cpp
template<typename T>
void debugTemplate(T value) {
    // Print type information
    std::cout << "Type: " << typeid(T).name() << std::endl;

    // Static assertions for debugging
    static_assert(std::is_arithmetic_v<T>, "T must be arithmetic");

    // Conditional compilation for debugging
    #ifdef DEBUG_TEMPLATES
    std::cout << "Debug: processing value " << value << std::endl;
    #endif

    // Process value
    std::cout << "Value: " << value << std::endl;
}
```

---

## Common Template Patterns

1. **RAII wrapper templates**
1. **Policy-based design**
1. **Template method pattern**
1. **Curiously Recurring Template Pattern (CRTP)**
1. **Expression templates**
1. **Template factories**

---

## CRTP Example

```cpp
template<typename Derived>
class Base {
public:
    void interface() {
        static_cast<Derived*>(this)->implementation();
    }

    static void static_interface() {
        Derived::static_implementation();
    }
};

class Derived : public Base<Derived> {
public:
    void implementation() {
        std::cout << "Derived implementation" << std::endl;
    }

    static void static_implementation() {
        std::cout << "Derived static implementation" << std::endl;
    }
};

int main() {
    Derived d;
    d.interface();  // Calls Derived::implementation
    Derived::static_interface();  // Calls Derived::static_implementation

    return 0;
}
```

---

## Template Performance

Templates can affect performance in several ways:

**Positive impacts:**
- Zero runtime overhead
- Compile-time optimizations
- Inlining opportunities

**Potential negatives:**
- Code bloat from multiple instantiations
- Longer compilation times
- Larger executable size

---

## Template Instantiation Control

```cpp
// Explicit instantiation declaration (suppress automatic instantiation)
extern template class std::vector<int>;

// Explicit instantiation definition (force instantiation)
template class std::vector<int>;

// Explicit instantiation of function
template void func<int>(int);

// In implementation file:
template<typename T>
void func(T value) {
    // Implementation
}

// Explicit instantiation for specific types
template void func<int>(int);
template void func<double>(double);
```

---

## Real-World Example: Generic Container

```cpp
template<typename T, typename Allocator = std::allocator<T>>
class SimpleVector {
private:
    T* data;
    size_t capacity;
    size_t count;
    Allocator alloc;

public:
    SimpleVector() : data(nullptr), capacity(0), count(0) {}

    ~SimpleVector() {
        clear();
        if (data) {
            alloc.deallocate(data, capacity);
        }
    }

    void push_back(const T& value) {
        if (count >= capacity) {
            reserve(capacity == 0 ? 1 : capacity * 2);
        }
        alloc.construct(data + count, value);
        ++count;
    }

    T& operator[](size_t index) { return data[index]; }
    const T& operator[](size_t index) const { return data[index]; }

    size_t size() const { return count; }
    bool empty() const { return count == 0; }
};
```

---

## Template Library Design

When designing template libraries:

1. **Make common cases easy**
1. **Provide sensible defaults**
1. **Use policy-based design** for customization
1. **Provide type traits** for introspection
1. **Document requirements** clearly
1. **Test with various types**
1. **Consider compilation time**

---

## Templates and the STL

The Standard Template Library heavily uses templates:

```cpp
// Containers are class templates
std::vector<int> numbers;
std::map<std::string, int> dictionary;

// Algorithms are function templates
std::sort(numbers.begin(), numbers.end());
std::find(numbers.begin(), numbers.end(), 42);

// Iterators are template-based
std::vector<int>::iterator it = numbers.begin();
auto it2 = numbers.begin();  // Type deduction

// Function objects and lambdas
std::sort(numbers.begin(), numbers.end(),
          [](int a, int b) { return a > b; });
```

---

## Template Error Prevention

```cpp
template<typename T>
class SafeArray {
private:
    T* data;
    size_t size;
public:
    SafeArray(size_t s) : size(s) {
        static_assert(std::is_default_constructible_v<T>,
                     "T must be default constructible");
        static_assert(!std::is_pointer_v<T>,
                     "Use smart pointers instead of raw pointers");
        data = new T[size]();
    }

    ~SafeArray() { delete[] data; }

    T& at(size_t index) {
        if (index >= size) {
            throw std::out_of_range("Index out of range");
        }
        return data[index];
    }
};
```

---

## Template Argument Deduction Guides (C++17)

```cpp
template<typename T>
class Vector {
private:
    T* data;
    size_t size;
public:
    Vector(std::initializer_list<T> list) {
        size = list.size();
        data = new T[size];
        std::copy(list.begin(), list.end(), data);
    }

    template<typename Iterator>
    Vector(Iterator first, Iterator last) {
        size = std::distance(first, last);
        data = new T[size];
        std::copy(first, last, data);
    }
};

// Deduction guides
template<typename T>
Vector(std::initializer_list<T>) -> Vector<T>;

template<typename Iterator>
Vector(Iterator, Iterator) -> Vector<typename std::iterator_traits<Iterator>::value_type>;

// Usage
Vector v1{1, 2, 3, 4, 5};  // Deduced as Vector<int>
std::vector<double> source = {1.1, 2.2, 3.3};
Vector v2(source.begin(), source.end());  // Deduced as Vector<double>
```

---

## Advanced Template Techniques

```cpp
// Tag dispatching
struct input_iterator_tag {};
struct forward_iterator_tag : input_iterator_tag {};
struct bidirectional_iterator_tag : forward_iterator_tag {};
struct random_access_iterator_tag : bidirectional_iterator_tag {};

template<typename Iterator>
void advance_impl(Iterator& it, int n, input_iterator_tag) {
    for (int i = 0; i < n; ++i) ++it;
}

template<typename Iterator>
void advance_impl(Iterator& it, int n, random_access_iterator_tag) {
    it += n;  // O(1) for random access iterators
}

template<typename Iterator>
void advance(Iterator& it, int n) {
    using category = typename std::iterator_traits<Iterator>::iterator_category;
    advance_impl(it, n, category{});
}
```

---

## Template Metaprogramming: Type Lists

```cpp
template<typename... Types>
struct TypeList {};

// Get size of type list
template<typename List>
struct Size;

template<typename... Types>
struct Size<TypeList<Types...>> {
    static constexpr size_t value = sizeof...(Types);
};

// Get type at index
template<size_t Index, typename List>
struct TypeAt;

template<size_t Index, typename Head, typename... Tail>
struct TypeAt<Index, TypeList<Head, Tail...>> {
    using type = typename TypeAt<Index - 1, TypeList<Tail...>>::type;
};

template<typename Head, typename... Tail>
struct TypeAt<0, TypeList<Head, Tail...>> {
    using type = Head;
};

// Usage
using MyTypes = TypeList<int, double, std::string>;
constexpr size_t count = Size<MyTypes>::value;  // 3
using SecondType = TypeAt<1, MyTypes>::type;    // double
```

---

## Fold Expressions (C++17)

```cpp
// Variadic template with fold expressions
template<typename... Args>
auto sum(Args... args) {
    return (args + ...);  // Unary right fold: ((a + b) + c) + d
}

template<typename... Args>
auto multiply(Args... args) {
    return (args * ...);  // Unary right fold
}

template<typename... Args>
void print(Args... args) {
    ((std::cout << args << " "), ...);  // Binary fold with comma operator
    std::cout << std::endl;
}

template<typename... Args>
bool all_true(Args... args) {
    return (args && ...);  // Logical AND fold
}

int main() {
    std::cout << sum(1, 2, 3, 4, 5) << std::endl;     // 15
    std::cout << multiply(2, 3, 4) << std::endl;       // 24
    print("Hello", 42, 3.14, "World");                // Hello 42 3.14 World
    std::cout << all_true(true, true, false) << std::endl; // false

    return 0;
}
```

---

## Template Specialization for Optimization

```cpp
// Generic implementation
template<typename T>
void copy_array(T* dest, const T* src, size_t count) {
    for (size_t i = 0; i < count; ++i) {
        dest[i] = src[i];
    }
}

// Optimized specialization for trivially copyable types
template<>
void copy_array<char>(char* dest, const char* src, size_t count) {
    std::memcpy(dest, src, count);
}

// Partial specialization for pointers
template<typename T>
void copy_array<T*>(T** dest, T* const* src, size_t count) {
    // Specialized handling for arrays of pointers
    for (size_t i = 0; i < count; ++i) {
        dest[i] = src[i];  // Shallow copy for pointers
    }
}
```

---

## Template Design Patterns

**Policy-Based Design:**
```cpp
template<typename T, typename ComparePolicy = std::less<T>>
class SortedContainer {
private:
    std::vector<T> data;
    ComparePolicy compare;
public:
    void insert(const T& value) {
        auto pos = std::lower_bound(data.begin(), data.end(), value, compare);
        data.insert(pos, value);
    }
    bool contains(const T& value) const {
        auto pos = std::lower_bound(data.begin(), data.end(), value, compare);
        return pos != data.end() && !compare(value, *pos) && !compare(*pos, value);
    }
};

// Usage with different policies
SortedContainer<int> ascending;                    // Default std::less
SortedContainer<int, std::greater<int>> descending; // Descending order
```

---

## Expression Templates

```cpp
template<typename Expr>
class VectorExpression {
public:
    double operator[](size_t i) const {
        return static_cast<const Expr&>(*this)[i];
    }

    size_t size() const {
        return static_cast<const Expr&>(*this).size();
    }
};

class Vector : public VectorExpression<Vector> {
private:
    std::vector<double> data;
public:
    Vector(size_t size) : data(size) {}

    double& operator[](size_t i) { return data[i]; }
    double operator[](size_t i) const { return data[i]; }
    size_t size() const { return data.size(); }

    template<typename Expr>
    Vector& operator=(const VectorExpression<Expr>& expr) {
        for (size_t i = 0; i < size(); ++i) {
            data[i] = expr[i];
        }
        return *this;
    }
};

template<typename LHS, typename RHS>
class VectorAdd : public VectorExpression<VectorAdd<LHS, RHS>> {
private:
    const LHS& lhs;
    const RHS& rhs;
public:
    VectorAdd(const LHS& l, const RHS& r) : lhs(l), rhs(r) {}

    double operator[](size_t i) const {
        return lhs[i] + rhs[i];
    }

    size_t size() const { return lhs.size(); }
};

template<typename LHS, typename RHS>
VectorAdd<LHS, RHS> operator+(const VectorExpression<LHS>& lhs,
                             const VectorExpression<RHS>& rhs) {
    return VectorAdd<LHS, RHS>(static_cast<const LHS&>(lhs),
                               static_cast<const RHS&>(rhs));
}
```

---

## Template Testing Strategies

```cpp
// Test with different types
template<typename T>
void test_container() {
    Container<T> c;

    // Test basic operations
    c.push_back(T{});
    assert(c.size() == 1);
    assert(!c.empty());

    // Test with specific values for this type
    if constexpr (std::is_same_v<T, int>) {
        c.push_back(42);
        assert(c.back() == 42);
    } else if constexpr (std::is_same_v<T, std::string>) {
        c.push_back("hello");
        assert(c.back() == "hello");
    }
}

int main() {
    test_container<int>();
    test_container<double>();
    test_container<std::string>();
    test_container<std::vector<int>>();

    std::cout << "All tests passed!" << std::endl;

    return 0;
}
```

---

## Template Compilation Optimization

```cpp
// Use forward declarations to reduce compilation time
template<typename T>
class ForwardDeclared;

// Prefer type aliases over nested typedefs
template<typename T>
using ValueType = typename T::value_type;

// Use extern templates to control instantiation
extern template class std::vector<int>;
extern template class std::map<std::string, int>;

// Minimize template depth to reduce compile time
template<typename T>
struct SimpleTraits {
    using type = T;
    static constexpr bool is_pod = std::is_pod_v<T>;
};

// Instead of deeply nested template recursion
```

---

## Common Template Pitfalls

1. **Template bloat** - excessive instantiations
1. **Compilation time** - complex templates slow builds
1. **Error messages** - hard to understand template errors
1. **Name lookup** - two-phase lookup complications
1. **Template recursion** - infinite recursion
1. **Specialization ambiguity** - unclear which version to use

---

## Template Debugging Techniques

```cpp
// Print template instantiation information
template<typename T>
void debug_type() {
    std::cout << "Type: " << typeid(T).name() << std::endl;
    std::cout << "Size: " << sizeof(T) << std::endl;
    std::cout << "Is integral: " << std::is_integral_v<T> << std::endl;
    std::cout << "Is pointer: " << std::is_pointer_v<T> << std::endl;
}

// Use static_assert for compile-time checks
template<typename T>
void constrained_function(T value) {
    static_assert(std::is_arithmetic_v<T>,
                  "T must be an arithmetic type");
    static_assert(sizeof(T) >= 4,
                  "T must be at least 4 bytes");

    // Function implementation
}

// Compiler-specific template debugging
#ifdef __GNUC__
    #pragma GCC diagnostic push
    #pragma GCC diagnostic error "-Wtemplate-backtrace-limit=0"
#endif
```

---

## Summary

Templates are a powerful C++ feature that enable:

1. **Generic programming** - write code once, use with many types
1. **Type safety** - compile-time type checking
1. **Performance** - zero runtime overhead
1. **STL foundation** - containers, algorithms, iterators
1. **Metaprogramming** - compile-time computation

Key concepts: function templates, class templates, specialization, SFINAE, variadic templates, and concepts (C++20).

Templates make C++ code more reusable, efficient, and type-safe while maintaining performance.
