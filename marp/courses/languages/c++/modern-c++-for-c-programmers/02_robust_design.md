# Robust Design

---

## Single Responsibility Principle

![single_responsibility](svg/courses/languages/c++/modern-c++-for-c-programmers/02_robust_design/single_responsibility.svg)

---

## Single Responsibility Principle Detail

- Each class should have only one reason to change
- Focus on solving one problem well
- Benefits:
    - Easier to understand and maintain
    - More testable and reusable
    - Lower coupling between components

---

## Single Responsibility Principle (cont.)

Bad approach:
```cpp
class UserManager {
public:
    void createUser(const std::string& username);
    void deleteUser(const std::string& username);
    void saveUserToDatabase(const User& user);
    void loadUserFromDatabase(const std::string& username);
    void validateUserCredentials(const std::string& username, const std::string& password);
    void sendPasswordResetEmail(const std::string& email);
};
```

Better approach:
```cpp
class UserManager {
public:
    void createUser(const std::string& username);
    void deleteUser(const std::string& username);
};

class UserRepository {
public:
    void saveUser(const User& user);
    User loadUser(const std::string& username);
};

class UserAuthenticator {
public:
    bool validateCredentials(const std::string& username, const std::string& password);
};

class EmailService {
public:
    void sendPasswordResetEmail(const std::string& email);
};
```

---

## Reducing Complexity

- Complexity leads to bugs and maintenance issues
- Strategies:
    - Limit function and class size
    - Reduce nesting depth
    - Minimize number of parameters
    - Avoid magic numbers/strings

---

## Reducing Complexity: Example

Before:
```cpp
void processOrder(Order* o, bool applyDiscount, int discountType,
                 double discountValue, bool calculateTax,
                 double taxRate, bool express) {
    double total = 0;
    for (int i = 0; i < o->itemCount; i++) {
        total += o->items[i].price * o->items[i].quantity;
    }
    if (applyDiscount) {
        if (discountType == 0) {
            total -= discountValue;
        } else if (discountType == 1) {
            total = total * (1 - discountValue / 100);
        } else {
            // More discount types...
        }
    }
    if (calculateTax) {
        total = total * (1 + taxRate / 100);
    }
    if (express) {
        total += 15.99;
    }
    o->total = total;
}
```

---

## Reducing Complexity: Example (cont.)

After:
```cpp
enum class DiscountType { Fixed, Percentage };

struct DiscountOptions {
    bool apply = false;
    DiscountType type = DiscountType::Percentage;
    double value = 0;
};

struct ShippingOptions {
    bool express = false;
    double expressCost = 15.99;
};

struct TaxOptions {
    bool apply = false;
    double rate = 0;
};

double calculateOrderSubtotal(const Order& order) {
    return std::accumulate(order.items.begin(), order.items.end(), 0.0,
        [](double sum, const OrderItem& item) {
            return sum + item.price * item.quantity;
        });
}

double applyDiscount(double amount, const DiscountOptions& discount) {
    if (!discount.apply) return amount;
    if (discount.type == DiscountType::Fixed) {
        return amount - discount.value;
    } else {
        return amount * (1 - discount.value / 100);
    }
}

double applyTax(double amount, const TaxOptions& tax) {
    if (!tax.apply) return amount;
    return amount * (1 + tax.rate / 100);
}

double applyShipping(double amount, const ShippingOptions& shipping) {
    if (shipping.express) {
        return amount + shipping.expressCost;
    }
    return amount;
}

void processOrder(Order& order,
                 const DiscountOptions& discount,
                 const TaxOptions& tax,
                 const ShippingOptions& shipping) {
    double total = calculateOrderSubtotal(order);
    total = applyDiscount(total, discount);
    total = applyTax(total, tax);
    total = applyShipping(total, shipping);
    order.total = total;
}
```

---

## Encapsulation

- Hide implementation details behind well-defined interfaces
- Restrict direct access to object's state
- Benefits:
    - Maintains invariants
    - Enables internal implementation changes
    - Prevents misuse of data

---

## Encapsulation: Example

```cpp
// Poor encapsulation
class Account {
public:
    double balance;
    std::vector<Transaction> transactions;

    void deposit(double amount) {
        balance += amount;
        transactions.push_back({amount, "deposit"});
    }
};

// Client code can easily break invariants
Account acc;
acc.balance = 1000000; // Bypassing normal deposit logic
acc.transactions.clear(); // Destroying transaction history

// Good encapsulation
class Account {
private:
    double balance;
    std::vector<Transaction> transactions;

public:
    void deposit(double amount) {
        if (amount <= 0) throw std::invalid_argument("Deposit must be positive");
        balance += amount;
        transactions.push_back({amount, "deposit"});
    }

    double getBalance() const { return balance; }

    std::vector<Transaction> getTransactionHistory() const {
        return transactions;
    }
};
```

---

## Keeping Header Files Clean

- Headers should contain only what's necessary
- Minimize dependencies between headers
- Use forward declarations when possible
- Employ include guards or `#pragma once`

---

## Keeping Header Files Clean: Example

Before:
```cpp
// customer.h
#include <string>
#include <vector>
#include "address.h"
#include "order.h"
#include "product.h"
#include "payment.h"

class Customer {
public:
    Customer(const std::string& name);
    void placeOrder(const std::vector<Product>& products);
    void updateAddress(const Address& address);
    void makePayment(const Payment& payment);

private:
    std::string name;
    Address address;
    std::vector<Order> orders;
};
```

---

## Keeping Header Files Clean: Example (cont.)

After:
```cpp
// customer.h
#pragma once
#include <string>
#include <vector>

// Forward declarations
class Address;
class Order;
class Product;
class Payment;

class Customer {
public:
    Customer(const std::string& name);
    void placeOrder(const std::vector<Product>& products);
    void updateAddress(const Address& address);
    void makePayment(const Payment& payment);

private:
    std::string name;
    Address* address;  // Use pointer to avoid including Address header
    std::vector<Order> orders;
};

// customer.cpp
#include "customer.h"
#include "address.h"
#include "order.h"
#include "product.h"
#include "payment.h"

// Implementation...
```

---

## Conditional Compilation

- Compile different code based on conditions
- Common uses:
    - Platform-specific code
    - Debug vs. release builds
    - Feature toggles
    - Preventing multiple inclusions (include guards)

---

## Conditional Compilation: Example

```cpp
#ifdef _WIN32
    #include <windows.h>
    void sleep(unsigned milliseconds) {
        Sleep(milliseconds);
    }
#elif defined(__APPLE__) || defined(__linux__)
    #include <unistd.h>
    void sleep(unsigned milliseconds) {
        usleep(milliseconds * 1000);
    }
#else
    #error "Unsupported platform"
#endif

// Debug-only logging
#ifdef DEBUG
    #define LOG(msg) std::cout << "[DEBUG] " << msg << std::endl
#else
    #define LOG(msg)
#endif

// Include guard example
#ifndef MYHEADER_H
#define MYHEADER_H
// Header content here
#endif
```

---

## Coding Style

- Consistency is key
- Style affects maintainability and readability
- Common considerations:
    - Naming conventions
    - Indentation and braces
    - Comments and documentation
    - File organization

---

## Coding Style: Naming Conventions

Different styles:
```cpp
// Snake case (common for variables and functions in C++)
int items_count = 0;
double calculate_total_price();

// Camel case (common in some C++ codebases)
int itemsCount = 0;
double calculateTotalPrice();

// Pascal case (common for class names)
class OrderProcessor {
    // ...
};

// All caps for macros and constants
#define MAX_BUFFER_SIZE 1024
const int MAX_RETRY_COUNT = 3;
```

Style consistency:
```cpp
// Inconsistent - hard to read and maintain
int itemsCount = 0;
double calculate_total_price();
class orderProcessor {};
```

---

## Coding Style: Class Organization

```cpp
class Customer {
public:
    // Constructors, destructors
    Customer();
    ~Customer();

    // Core behavior
    void placeOrder(const Order& order);

    // Accessors/mutators
    std::string getName() const;
    void setAddress(const Address& address);

    // Static methods
    static Customer createGuestCustomer();

private:
    // Private helpers
    void validateOrder(const Order& order);
    void updateLoyaltyPoints(const Order& order);

    // Member variables
    std::string name;
    Address address;
    int loyaltyPoints;
};
```

---

## C++ 11 Game-Changers

Modern C++ features that improve robustness:
1. Smart pointers (`unique_ptr`, `shared_ptr`)
1. Move semantics
1. Lambda expressions
1. `auto` type deduction
1. Range-based for loops
1. `nullptr` keyword
1. Strongly-typed enums
1. `constexpr`

---

## Smart Pointers

- Resource management through RAII
- `unique_ptr`: Exclusive ownership
- `shared_ptr`: Shared ownership with reference counting
- `weak_ptr`: Non-owning reference to `shared_ptr`
- Eliminate manual memory management

```cpp
// Before C++11
void legacyCode() {
    Resource* res = new Resource();
    // Use res
    delete res; // Easy to forget or have early returns
}

// Modern C++
void modernCode() {
    auto res = std::make_unique<Resource>();
    // Use res
} // Automatically deleted when out of scope

// Shared ownership
std::shared_ptr<Document> doc = std::make_shared<Document>();
processDocument(doc); // Both functions can access and modify
saveDocument(doc);    // No need to worry about lifetime
```

---

## Move Semantics

- Efficiently transfer resources instead of copying
- Uses rvalue references (`&&`)
- Enabled by move constructors and move assignment operators
- Eliminates unnecessary copies

```cpp
std::vector<int> createLargeVector() {
    std::vector<int> result(1000000, 42);
    return result; // Move semantics allow this to be efficient
}

void processVector() {
    // Before C++11: Copy constructed (inefficient)
    // After C++11: Move constructed (efficient)
    std::vector<int> v = createLargeVector();

    // Explicitly moving an lvalue
    std::vector<int> v2;
    v2 = std::move(v); // v is now in a valid but unspecified state

    // v is "empty" after being moved from
    std::cout << "v size: " << v.size() << std::endl; // Likely 0
}
```

---

## Lambda Expressions

- Inline anonymous functions
- Syntax

```cpp
[capture](parameters) -> return_type { body }
```

- Enable functional programming patterns
- Great for customizing algorithms

```cpp
std::vector<int> numbers = {1, 2, 3, 4, 5};

// Find first even number
auto it = std::find_if(numbers.begin(), numbers.end(),
    [](int n) { return n % 2 == 0; });

// Sort by absolute value
std::sort(numbers.begin(), numbers.end(),
    [](int a, int b) { return std::abs(a) < std::abs(b); });

// Capture variables from surrounding scope
int threshold = 3;
auto largeEnough = std::all_of(numbers.begin(), numbers.end(),
    [threshold](int n) { return n >= threshold; });

// Mutable lambda
int sum = 0;
std::for_each(numbers.begin(), numbers.end(),
    [&sum](int n) { sum += n; });
```

---

## Type Deduction with `auto`

- Let compiler deduce types
- Improves maintainability when types are complex
- Works with variables, functions, and lambdas

```cpp
// Without auto
std::map<std::string, std::vector<int>>::iterator it = myMap.begin();
for (; it != myMap.end(); ++it) {
    // ...
}

// With auto
auto it = myMap.begin();
for (; it != myMap.end(); ++it) {
    // ...
}

// Even better with range-based for
for (const auto& pair : myMap) {
    // pair.first is the key, pair.second is the value
}

// Return type deduction (C++14)
auto multiply(int x, int y) {
    return x * y;
}
```

---

## Range-Based For Loops

- Simplified iteration over containers
- Works with arrays, STL containers, and any type with begin()/end()
- More readable and less error-prone

```cpp
std::vector<int> numbers = {1, 2, 3, 4, 5};

// Old way
for (std::vector<int>::iterator it = numbers.begin();
     it != numbers.end(); ++it) {
    std::cout << *it << std::endl;
}

// Range-based for
for (int num : numbers) {
    std::cout << num << std::endl;
}

// With auto and reference to avoid copying
for (const auto& num : numbers) {
    std::cout << num << std::endl;
}

// Works with arrays
int arr[] = {1, 2, 3, 4, 5};
for (int val : arr) {
    // ...
}
```

---

## `nullptr` Instead of `NULL`

- Type-safe pointer literal
- Avoids ambiguity with integer 0
- Resolves function overload issues

```cpp
// Problem with NULL
void foo(int x) {
    std::cout << "int version" << std::endl;
}

void foo(char* x) {
    std::cout << "pointer version" << std::endl;
}

int main() {
    foo(NULL); // Calls foo(int) because NULL is typically 0
    foo(nullptr); // Calls foo(char*) as expected

    // Clear pointer usage
    int* ptr = nullptr;
    if (ptr == nullptr) {
        // Safe comparison
    }

    return 0;
}
```

---

## Strongly-Typed Enums

- Scoped enumerations with `enum class`
- Type-safe, prevents implicit conversion to int
- Can specify underlying type

```cpp
// C-style enum - global namespace pollution
enum Color { RED, GREEN, BLUE };
enum TrafficLight { RED_LIGHT, YELLOW, GREEN_LIGHT };
// Error: RED redefined

// Modern enum class
enum class Color { Red, Green, Blue };
enum class TrafficLight { Red, Yellow, Green };

void useColors() {
    // C-style enum issues
    Color c1 = RED;
    if (c1 == 0) { } // Implicit conversion - bug prone

    // enum class benefits
    Color c2 = Color::Red;
    // if (c2 == 0) { } // Error - no implicit conversion
    if (c2 == Color::Red) { } // OK

    // Specify underlying type
    enum class Status : uint8_t {
        OK = 0,
        Error = 1,
        Unknown = 255
    };
}
```

---

## `constexpr`

- Enables compile-time computation
- Improved performance
- Guarantees compile-time evaluation when possible

```cpp
// C++03 - compile-time constants
const int square1(int x) {
    return x * x;
}
// Not usable in constant expressions despite being const

// C++11 - constexpr enables compile-time evaluation
constexpr int square2(int x) {
    return x * x;
}

// Usage
int arr[square2(3)]; // OK - evaluated at compile time
// int arr2[square1(3)]; // Error

// C++14 - more complex constexpr functions
constexpr int factorial(int n) {
    return (n <= 1) ? 1 : n * factorial(n - 1);
}

constexpr int fact5 = factorial(5); // Computed at compile time
```

---

## Best Practices for Error Handling

- Be explicit about error conditions
- Use exceptions for exceptional conditions
- Return values or optional for expected failures
- Consider using expected/outcome for complex error handling

---

## Error Handling: Example

```cpp
// Using return codes (C-style)
int divideNumbers(int a, int b, int* result) {
    if (b == 0) {
        return -1; // Error code
    }
    *result = a / b;
    return 0; // Success
}

// Using exceptions
int divideNumbers(int a, int b) {
    if (b == 0) {
        throw std::invalid_argument("Division by zero");
    }
    return a / b;
}

// Using std::optional (C++17)
std::optional<int> divideNumbers(int a, int b) {
    if (b == 0) {
        return std::nullopt;
    }
    return a / b;
}

// Usage with std::optional
auto result = divideNumbers(10, 0);
if (result) {
    std::cout << "Result: " << *result << std::endl;
} else {
    std::cout << "Division failed" << std::endl;
}
```

---

## Resource Management Best Practices

- Use RAII (Resource Acquisition Is Initialization)
- Prefer smart pointers over raw pointers
- Implement proper copy/move semantics
- Use standard containers instead of raw arrays

---

## Resource Management: RAII Example

```cpp
// Manual resource management (error-prone)
void processFileManual(const std::string& filename) {
    FILE* file = fopen(filename.c_str(), "r");
    if (!file) {
        throw std::runtime_error("Could not open file");
    }

    // If an exception occurs here, file is never closed
    char buffer[1024];
    size_t bytesRead = fread(buffer, 1, sizeof(buffer), file);

    // Process data...

    fclose(file); // Might never be reached
}

// RAII approach
class FileHandle {
private:
    FILE* file;

public:
    FileHandle(const std::string& filename) {
        file = fopen(filename.c_str(), "r");
        if (!file) {
            throw std::runtime_error("Could not open file");
        }
    }

    ~FileHandle() {
        if (file) {
            fclose(file);
        }
    }

    FILE* get() { return file; }
};

void processFileRAII(const std::string& filename) {
    FileHandle file(filename);

    // Even if an exception occurs, FileHandle's destructor will close the file
    char buffer[1024];
    size_t bytesRead = fread(buffer, 1, sizeof(buffer), file.get());

    // Process data...
}
```

---

## Defensive Programming

- Validate inputs and preconditions
- Design by contract (preconditions, postconditions, invariants)
- Fail fast and explicitly
- Use assertions for debugging

---

## Defensive Programming: Example

```cpp
class Vector {
private:
    int* data;
    size_t size;

public:
    // Constructor with input validation
    Vector(size_t initialSize) {
        if (initialSize > 1000000) {
            throw std::invalid_argument("Initial size too large");
        }

        size = initialSize;
        data = new int[size]();
    }

    // Bounds checking accessor
    int& at(size_t index) {
        if (index >= size) {
            throw std::out_of_range("Index out of bounds");
        }
        return data[index];
    }

    // Const version
    const int& at(size_t index) const {
        if (index >= size) {
            throw std::out_of_range("Index out of bounds");
        }
        return data[index];
    }

    // Debug assertion to validate internal state
    void checkInvariant() const {
        assert(data != nullptr && "Data pointer should never be null");
        assert(size > 0 && "Size should be positive");
    }

    // Destructor
    ~Vector() {
        delete[] data;
    }
};
```

---

## Testing Strategies

- Unit testing individual components
- Integration testing component interactions
- Test-driven development (TDD)
- Continuous integration
- Fuzzing and property-based testing

---

## Testing: Example with Google Test

```cpp
#include <gtest/gtest.h>
#include "math_utils.h"

// Simple test
TEST(MathTest, AdditionWorks) {
    EXPECT_EQ(add(2, 3), 5);
    EXPECT_EQ(add(-2, 3), 1);
    EXPECT_EQ(add(0, 0), 0);
}

// Parameterized test
class FactorialTest : public ::testing::TestWithParam<std::pair<int, int>> {};

TEST_P(FactorialTest, ComputesCorrectValues) {
    auto param = GetParam();
    int input = param.first;
    int expected = param.second;
    EXPECT_EQ(factorial(input), expected);
}

INSTANTIATE_TEST_SUITE_P(
    FactorialValues,
    FactorialTest,
    ::testing::Values(
        std::make_pair(0, 1),
        std::make_pair(1, 1),
        std::make_pair(2, 2),
        std::make_pair(3, 6),
        std::make_pair(4, 24),
        std::make_pair(5, 120)
    )
);

// Fixture for more complex testing
class VectorTest : public ::testing::Test {
protected:
    void SetUp() override {
        // Initialize before each test
        vec.push_back(1);
        vec.push_back(2);
        vec.push_back(3);
    }

    void TearDown() override {
        // Clean up after each test
    }

    std::vector<int> vec;
};

TEST_F(VectorTest, Size) {
    EXPECT_EQ(vec.size(), 3);
}

TEST_F(VectorTest, ContainsElements) {
    EXPECT_EQ(vec[0], 1);
    EXPECT_EQ(vec[1], 2);
    EXPECT_EQ(vec[2], 3);
}
```

---

## Profiling and Optimization

- Measure before optimizing
- Focus on bottlenecks (80/20 rule)
- Common tools:
    - Valgrind for memory analysis
    - gprof/perf for CPU profiling
    - Intel VTune and AMD CodeXL

---

## Profiling: Example Approach

```cpp
#include <chrono>

// Simple timing wrapper
template<typename Func>
auto timeFunction(Func&& func) {
    auto start = std::chrono::high_resolution_clock::now();

    // Call the function
    std::forward<Func>(func)();

    auto end = std::chrono::high_resolution_clock::now();
    return std::chrono::duration_cast<std::chrono::microseconds>(end - start).count();
}

// Usage
void optimizationExample() {
    std::vector<int> data(1000000);
    std::iota(data.begin(), data.end(), 0); // Fill with values 0..999999

    // Time the unoptimized version
    auto time1 = timeFunction([&data]() {
        long long sum = 0;
        for (const auto& val : data) {
            sum += val;
        }
        return sum;
    });

    // Time a more optimized version
    auto time2 = timeFunction([&data]() {
        return std::accumulate(data.begin(), data.end(), 0LL);
    });

    std::cout << "Manual loop: " << time1 << " μs\n";
    std::cout << "std::accumulate: " << time2 << " μs\n";
}
```

---

## Summary: Robust Design

- Apply Single Responsibility Principle
- Reduce complexity through decomposition
- Use encapsulation to maintain invariants
- Write clean, maintainable code
- Leverage modern C++ features
- Handle errors explicitly and consistently
- Manage resources through RAII
- Practice defensive programming
- Test thoroughly
- Profile before optimizing

---

## Lab Exercises

1. Refactor a complex function to reduce its complexity
1. Convert C-style memory management to use smart pointers
1. Apply lambda expressions to simplify algorithm usage
1. Create an RAII wrapper for a resource (file, mutex, etc.)
1. Write unit tests for a class using a testing framework
