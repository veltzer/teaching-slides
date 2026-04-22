---
tags:
  - languages:c++
level: advanced
category: embedded
audience:
  - audiences:embedded-engineers
  - audiences:developers

---
# Templates and Generic Programming

---

## Chapter Overview

1. Template basics and syntax
1. Two meanings of typename
1. Accessing names in template base classes
1. Parameter-independent code
1. Traits and template metaprogramming

---

## Why Templates?

![why_templates](svg/courses/embedded/effective-real-time-embedded-c-and-c++/16_templates_and_generic_programming/why_templates.svg)

---

## Function Templates

```cpp
// Basic function template
template<typename T>
T max(T a, T b) {
    return (a > b) ? a : b;
}

// Multiple template parameters
template<typename T, typename U>
auto max(T a, U b) -> decltype(a > b ? a : b) {
    return (a > b) ? a : b;
}

// Non-type template parameters
template<typename T, size_t N>
size_t arraySize(T (&)[N]) {
    return N;
}

// Usage
int x = max(10, 20);           // T = int
double y = max(3.14, 2.71);    // T = double
auto z = max(10, 3.14);        // T = int, U = double

int arr[50];
size_t size = arraySize(arr);  // N = 50
```

---

## Class Templates

```cpp
// Basic class template
template<typename T, size_t SIZE>
class FixedArray {
private:
    T data[SIZE];

public:
    T& operator[](size_t index) {
        return data[index];
    }

    const T& operator[](size_t index) const {
        return data[index];
    }

    constexpr size_t size() const { return SIZE; }

    T* begin() { return data; }
    T* end() { return data + SIZE; }
};

// Usage
FixedArray<int, 10> intArray;
FixedArray<float, 20> floatArray;
```

---

## Template Specialization

```cpp
// Primary template
template<typename T>
class Serializer {
public:
    void serialize(const T& obj) {
        // Generic implementation
        write(&obj, sizeof(T));
    }
};

// Full specialization for bool
template<>
class Serializer<bool> {
public:
    void serialize(const bool& value) {
        uint8_t byte = value ? 1 : 0;
        write(&byte, 1);
    }
};

// Partial specialization for pointers
template<typename T>
class Serializer<T*> {
public:
    void serialize(T* const& ptr) {
        if (ptr) {
            writeByte(1);  // Non-null marker
            Serializer<T>().serialize(*ptr);
        } else {
            writeByte(0);  // Null marker
        }
    }
};
```

---

## Two Meanings of typename

```cpp
// Meaning 1: Template parameter
template<typename T>  // Can use 'class' here too
class Container {
    T value;
};

// Meaning 2: Dependent type names
template<typename T>
class MyClass {
    // Without typename, compiler assumes T::iterator is a value
    typename T::iterator iter;  // Tell compiler it's a type

    void process() {
        // Dependent name in local variable
        typename T::value_type val;

        // Dependent name in cast
        val = static_cast<typename T::value_type>(42);
    }
};

// Rule: Use typename for dependent type names
// except in base class lists and member initializer lists
```

---

## Dependent Names

```cpp
template<typename T>
class Derived : public Base<T> {  // No typename needed
public:
    Derived() : Base<T>() {}      // No typename needed

    void foo() {
        // Dependent names need disambiguation
        typename T::SubType* ptr;  // typename required

        // Template dependent names
        T::template foo<int>();    // template keyword required

        // Both typename and template
        typename T::template Nested<int>::type val;
    }
};

// When to use typename:
// 1. T::something when 'something' is a type
// 2. Not needed in base class lists
// 3. Not needed in member initializer lists
// 4. Not needed for non-dependent names
```

---

## Accessing Base Class Names

```cpp
// Problem: Names in dependent base classes are hidden
template<typename T>
class Base {
public:
    void foo() { }
    static int value;
};

template<typename T>
class Derived : public Base<T> {
public:
    void bar() {
        // foo();           // Error! Name not found
        // value = 42;      // Error! Name not found

        // Solution 1: Use this->
        this->foo();

        // Solution 2: Use Base<T>::
        Base<T>::foo();
        Base<T>::value = 42;

        // Solution 3: Using declaration
        using Base<T>::foo;
        foo();  // Now OK
    }
};
```

---

## Template Template Parameters

```cpp
// Container that accepts another template as parameter
template<
    typename T,
    template<typename, typename> class Container = std::vector
>
class Stack {
private:
    Container<T, std::allocator<T>> items;

public:
    void push(const T& item) {
        items.push_back(item);
    }

    T pop() {
        T item = items.back();
        items.pop_back();
        return item;
    }
};

// Usage
Stack<int, std::vector> vecStack;
Stack<int, std::deque> dequeStack;
```

---

## Variadic Templates

```cpp
// Function with variable number of arguments
template<typename... Args>
void print(Args... args) {
    ((std::cout << args << " "), ...);  // C++17 fold expression
}

// Recursive approach (pre-C++17)
template<typename First, typename... Rest>
void printRecursive(First first, Rest... rest) {
    std::cout << first << " ";
    if constexpr (sizeof...(rest) > 0) {
        printRecursive(rest...);
    }
}

// Sizeof... operator
template<typename... Types>
class Tuple {
    static constexpr size_t size = sizeof...(Types);
};

// Usage
print(1, 2.5, "hello", 'c');  // Any number of args
```

---

## SFINAE (Substitution Failure Is Not An Error)

```cpp
// Enable function only for integral types
template<typename T>
typename std::enable_if<std::is_integral<T>::value, T>::type
increment(T value) {
    return value + 1;
}

// Modern C++: using enable_if_t
template<typename T>
std::enable_if_t<std::is_floating_point_v<T>, T>
halve(T value) {
    return value / 2;
}

// Using SFINAE for overload resolution
template<typename T>
auto serialize(T value)
    -> decltype(value.serialize(), void()) {
    value.serialize();  // Has serialize method
}

template<typename T>
auto serialize(T value)
    -> decltype(std::to_string(value), void()) {
    write(std::to_string(value));  // Convertible to string
}
```

---

## Concepts (C++20)

```cpp
// Define a concept
template<typename T>
concept Serializable = requires(T t) {
    { t.serialize() } -> std::same_as<void>;
    { t.size() } -> std::convertible_to<size_t>;
};

// Use concept to constrain template
template<Serializable T>
void save(const T& object) {
    object.serialize();
}

// Multiple constraints
template<typename T>
concept Numeric = std::is_arithmetic_v<T> &&
                  !std::is_same_v<T, bool>;

template<Numeric T>
T average(T a, T b) {
    return (a + b) / 2;
}

// Requires clause
template<typename T>
    requires std::is_pointer_v<T>
void process(T ptr) {
    if (ptr) { /* ... */ }
}
```

---

## Parameter-Independent Code

```cpp
// BAD: Code bloat - duplicated for each T
template<typename T>
class BadVector {
    T* data;
    size_t size;
public:
    void clear() {
        for (size_t i = 0; i < size; ++i) {
            data[i].~T();  // Destructor call depends on T
        }
        size = 0;
    }
};

```

---

## Parameter-Independent Code: Refactored

```cpp
// GOOD: Factor out type-independent code
class VectorBase {
protected:
    void* data;
    size_t size;
    size_t capacity;

    void clearImpl(void (*destructor)(void*)) {
        // Type-independent implementation
        for (size_t i = 0; i < size; ++i) {
            destructor(static_cast<char*>(data) + i * elemSize);
        }
        size = 0;
    }
};

template<typename T>
class GoodVector : private VectorBase {
    static void destroyElement(void* elem) {
        static_cast<T*>(elem)->~T();
    }
public:
    void clear() {
        clearImpl(&destroyElement);
    }
};
```

---

## Type Traits

```cpp
// Basic type traits
template<typename T>
struct is_pointer {
    static constexpr bool value = false;
};

template<typename T>
struct is_pointer<T*> {
    static constexpr bool value = true;
};

// Remove qualifiers
template<typename T>
struct remove_const {
    using type = T;
};

template<typename T>
struct remove_const<const T> {
    using type = T;
};

// Conditional type selection
template<bool Condition, typename TrueType, typename FalseType>
struct conditional {
    using type = TrueType;
};

template<typename TrueType, typename FalseType>
struct conditional<false, TrueType, FalseType> {
    using type = FalseType;
};

// Usage
using Type = conditional<sizeof(int) == 4, int32_t, int64_t>::type;
```

---

## Custom Traits

```cpp
// Detect if type has a method
template<typename T, typename = void>
struct has_serialize : std::false_type {};

template<typename T>
struct has_serialize<T,
    std::void_t<decltype(std::declval<T>().serialize())>
> : std::true_type {};

// Detect if type is iterable
template<typename T, typename = void>
struct is_iterable : std::false_type {};

template<typename T>
struct is_iterable<T,
    std::void_t<
        decltype(std::begin(std::declval<T>())),
        decltype(std::end(std::declval<T>()))
    >
> : std::true_type {};

// Usage
template<typename T>
void process(const T& obj) {
    if constexpr (has_serialize<T>::value) {
        obj.serialize();
    } else {
        defaultSerialize(obj);
    }
}
```

---

## Template Metaprogramming

```cpp
// Compile-time factorial
template<int N>
struct Factorial {
    static constexpr int value = N * Factorial<N-1>::value;
};

template<>
struct Factorial<0> {
    static constexpr int value = 1;
};

// Compile-time Fibonacci
template<int N>
struct Fibonacci {
    static constexpr int value =
        Fibonacci<N-1>::value + Fibonacci<N-2>::value;
};

template<>
struct Fibonacci<0> {
    static constexpr int value = 0;
};

template<>
struct Fibonacci<1> {
    static constexpr int value = 1;
};

// Usage
constexpr int fact5 = Factorial<5>::value;  // 120
constexpr int fib10 = Fibonacci<10>::value; // 55
```

---

## Compile-Time Utilities

```cpp
// Type list manipulation
template<typename... Types>
struct TypeList {};

// Get Nth type
template<size_t N, typename... Types>
struct GetType;

template<size_t N, typename Head, typename... Tail>
struct GetType<N, Head, Tail...> {
    using type = typename GetType<N-1, Tail...>::type;
};

template<typename Head, typename... Tail>
struct GetType<0, Head, Tail...> {
    using type = Head;
};

// Count types matching predicate
template<template<typename> class Pred, typename... Types>
struct CountIf;

template<template<typename> class Pred>
struct CountIf<Pred> {
    static constexpr size_t value = 0;
};

template<template<typename> class Pred,
         typename Head, typename... Tail>
struct CountIf<Pred, Head, Tail...> {
    static constexpr size_t value =
        Pred<Head>::value + CountIf<Pred, Tail...>::value;
};
```

---

## Expression Templates

```cpp
// Lazy evaluation with expression templates
template<typename L, typename R>
struct AddExpr {
    const L& left;
    const R& right;

    AddExpr(const L& l, const R& r) : left(l), right(r) {}

    auto operator[](size_t i) const {
        return left[i] + right[i];
    }
};

template<typename T, size_t N>
class Vector {
    T data[N];
public:
    T operator[](size_t i) const { return data[i]; }
    T& operator[](size_t i) { return data[i]; }

    template<typename Expr>
    Vector& operator=(const Expr& expr) {
        for (size_t i = 0; i < N; ++i) {
            data[i] = expr[i];
        }
        return *this;
    }
};

template<typename L, typename R>
AddExpr<L, R> operator+(const L& l, const R& r) {
    return AddExpr<L, R>(l, r);
}

// Usage: No temporary vectors created
Vector<float, 100> a, b, c, d;
d = a + b + c;  // Single loop, no temporaries
```

---

## CRTP (Curiously Recurring Template Pattern)

```cpp
// Static polymorphism
template<typename Derived>
class Comparable {
public:
    bool operator!=(const Derived& other) const {
        return !static_cast<const Derived*>(this)->operator==(other);
    }

    bool operator>(const Derived& other) const {
        return other < *static_cast<const Derived*>(this);
    }

    bool operator<=(const Derived& other) const {
        return !(other < *static_cast<const Derived*>(this));
    }

    bool operator>=(const Derived& other) const {
        return !(*static_cast<const Derived*>(this) < other);
    }
};

// Usage
class Temperature : public Comparable<Temperature> {
    float value;
public:
    explicit Temperature(float v) : value(v) {}

    bool operator==(const Temperature& other) const {
        return value == other.value;
    }

    bool operator<(const Temperature& other) const {
        return value < other.value;
    }
};
```

---

## Policy-Based Design

```cpp
// Policies as template parameters
template<typename T>
struct HeapStorage {
    static T* allocate(size_t n) {
        return new T[n];
    }

    static void deallocate(T* ptr) {
        delete[] ptr;
    }
};

template<typename T, size_t N>
struct StackStorage {
    static T buffer[N];

    static T* allocate(size_t n) {
        return (n <= N) ? buffer : nullptr;
    }

    static void deallocate(T*) {
        // No-op for stack storage
    }
};
```

---

## Policy-Based Design: `SmartArray`

```cpp
template<
    typename T,
    template<typename> class StoragePolicy = HeapStorage
>
class SmartArray {
    T* data;
    size_t size;

public:
    explicit SmartArray(size_t n)
        : data(StoragePolicy<T>::allocate(n)), size(n) {}

    ~SmartArray() {
        StoragePolicy<T>::deallocate(data);
    }
};
```

---

## Tag Dispatching

```cpp
// Tags for compile-time dispatch
struct random_access_iterator_tag {};
struct forward_iterator_tag {};

template<typename Iterator>
void advanceImpl(Iterator& it, int n, random_access_iterator_tag) {
    it += n;  // O(1) for random access
}

template<typename Iterator>
void advanceImpl(Iterator& it, int n, forward_iterator_tag) {
    for (int i = 0; i < n; ++i) {
        ++it;  // O(n) for forward only
    }
}

template<typename Iterator>
void advance(Iterator& it, int n) {
    using category = typename Iterator::iterator_category;
    advanceImpl(it, n, category{});
}

// Iterator with tag
template<typename T>
class MyIterator {
public:
    using iterator_category = random_access_iterator_tag;
    // ... rest of iterator implementation
};
```

---

## Template Instantiation Control

```cpp
// Explicit instantiation declaration (extern template)
extern template class std::vector<int>;  // Don't instantiate here

// Explicit instantiation definition
template class MyTemplate<int>;  // Instantiate here

// Control instantiation location
// In header:
template<typename T>
class BigTemplate {
    // ... lots of code
};

// Declare common instantiations
extern template class BigTemplate<int>;
extern template class BigTemplate<float>;

// In one .cpp file:
template class BigTemplate<int>;
template class BigTemplate<float>;
```

---

## Fold Expressions (C++17)

```cpp
// Unary fold
template<typename... Args>
auto sum(Args... args) {
    return (args + ...);  // Right fold: arg1 + (arg2 + ... + argN)
}

// Binary fold
template<typename... Args>
void printAll(Args... args) {
    ((std::cout << args << " "), ...);  // Left fold with comma
}

// Fold with operator&&
template<typename... Args>
bool allTrue(Args... args) {
    return (args && ...);  // true if all are true
}

// Fold with operator||
template<typename T, typename... Args>
bool anyOf(T value, Args... args) {
    return ((value == args) || ...);
}

// Usage
int total = sum(1, 2, 3, 4, 5);  // 15
bool found = anyOf(5, 1, 3, 5, 7);  // true
```

---

## if constexpr (C++17)

```cpp
// Compile-time conditional compilation
template<typename T>
auto processValue(T value) {
    if constexpr (std::is_integral_v<T>) {
        return value * 2;  // Integer processing
    }
    else if constexpr (std::is_floating_point_v<T>) {
        return value / 2;  // Float processing
    }
    else if constexpr (std::is_pointer_v<T>) {
        return value ? *value : T{};  // Pointer processing
    }
    else {
        return value;  // Default
    }
}

// Recursive template with if constexpr
template<typename Tuple, size_t... Is>
void printTupleImpl(const Tuple& t, std::index_sequence<Is...>) {
    ((std::cout << std::get<Is>(t) << " "), ...);
}

template<typename... Types>
void printTuple(const std::tuple<Types...>& t) {
    if constexpr (sizeof...(Types) > 0) {
        printTupleImpl(t, std::index_sequence_for<Types...>{});
    }
}
```

---

## Template Lambdas

```cpp
// Generic lambdas (C++14)
auto genericLambda = [](auto x, auto y) {
    return x + y;
};

// Template lambdas (C++20)
auto templateLambda = []<typename T>(T x, T y) {
    return x + y;
};

// Constrained template lambdas
auto constrainedLambda = []<typename T>
    requires std::is_arithmetic_v<T>
(T x, T y) {
    return x + y;
};

// Perfect forwarding in lambdas
auto forwardingLambda = []<typename... Args>
(Args&&... args) {
    return process(std::forward<Args>(args)...);
};

// Usage
int sum = genericLambda(5, 3);
double result = templateLambda(3.14, 2.71);
```

---

## Common Template Pitfalls

```cpp
// Pitfall 1: Dependent name lookup
template<typename T>
void bad() {
    T::type x;  // Error: needs typename
}

// Pitfall 2: Template argument deduction
template<typename T>
void func(T t, T u) {}

func(1, 1.0);  // Error: T can't be both int and double

// Pitfall 3: Code bloat
template<typename T>
class BigClass {
    // 1000 lines of code
};  // Instantiated for each T

// Pitfall 4: Point of instantiation
template<typename T>
void foo() {
    bar<T>();  // bar must be visible here
}
```

---

## Best Practices

1. **Use concepts** to constrain templates
1. **Factor out** type-independent code
1. **Minimize** template instantiations
1. **Document** template requirements
1. **Test** with multiple types
1. **Profile** for code bloat

---

## Template Debugging

```cpp
// Static assertions for debugging
template<typename T>
class Container {
    static_assert(std::is_default_constructible_v<T>,
                  "T must be default constructible");

    static_assert(sizeof(T) <= 1024,
                  "T is too large for this container");
};

// Concept error messages
template<typename T>
concept Sortable = requires(T a, T b) {
    { a < b } -> std::convertible_to<bool>;
};

template<Sortable T>
void sort(std::vector<T>& vec);  // Clear error if T not Sortable

// Type printing for debugging
template<typename T>
void printType() {
    std::cout << __PRETTY_FUNCTION__ << '\n';
}
```

---

## Summary

1. Templates enable generic, type-safe programming
1. Understand dependent names and typename usage
1. Use traits for compile-time type manipulation
1. SFINAE and concepts control template instantiation
1. Metaprogramming enables compile-time computation

---

## Key Takeaways

1. **Templates** provide zero-overhead abstraction
1. **typename** disambiguates dependent names
1. **Traits** enable compile-time decisions
1. **CRTP** provides static polymorphism
1. **Concepts** improve error messages
