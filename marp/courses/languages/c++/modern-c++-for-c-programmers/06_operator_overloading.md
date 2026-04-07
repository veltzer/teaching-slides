# Operator Overloading

---

## What is Operator Overloading?

Operator overloading allows you to define how operators work with user-defined types (classes and structs).

Instead of writing:
```cpp
Vector result = vector1.add(vector2);
```

You can write:
```cpp
Vector result = vector1 + vector2;
```

---

## Why Use Operator Overloading?

1. **Natural syntax** - makes code more intuitive
1. **Consistency** - follows mathematical conventions
1. **Readability** - cleaner, more expressive code
1. **Integration** - works seamlessly with STL algorithms

---

## Basic Syntax

Two ways to overload operators:

**Member function:**
```cpp
class MyClass {
    ReturnType operator+(const MyClass& other) const;
};
```

**Non-member function:**
```cpp
ReturnType operator+(const MyClass& left, const MyClass& right);
```

---

## Overloadable Operators

![overloadable_operators](svg/courses/languages/c++/modern-c++-for-c-programmers/06_operator_overloading/overloadable_operators.svg)

---

## Non-Overloadable Operators

These operators **cannot** be overloaded:

- `::` (scope resolution)
- `.` (member access)
- `.*` (pointer-to-member)
- `?:` (ternary conditional)
- `sizeof`
- `typeid`

---

## Simple Example: Complex Numbers

```cpp
class Complex {
private:
    double real, imag;
public:
    Complex(double r = 0, double i = 0) : real(r), imag(i) {}

    // Addition operator
    Complex operator+(const Complex& other) const {
        return Complex(real + other.real, imag + other.imag);
    }

    void print() const {
        std::cout << real << " + " << imag << "i\n";
    }
};
```

---

## Using the Complex Class

```cpp
int main() {
    Complex c1(3, 4);    // 3 + 4i
    Complex c2(1, 2);    // 1 + 2i

    Complex c3 = c1 + c2;  // Uses operator+
    c3.print();            // Output: 4 + 6i

    return 0;
}
```

---

## Member vs Non-Member Functions

**Member function approach:**
```cpp
class Vector {
    Vector operator+(const Vector& other) const;
    // 'this' is the left operand
    // 'other' is the right operand
};
```

**Non-member function approach:**
```cpp
Vector operator+(const Vector& left, const Vector& right);
// Both operands are parameters
```

---

## When to Use Each Approach

**Use member functions for:**
- Operators that modify the object (`+=`, `-=`, `++`, `--`)
- Operators where left operand is always your class type

**Use non-member functions for:**
- Symmetric operators (`+`, `-`, `*`, `/`)
- When left operand might be a different type
- Better encapsulation (can be friends if needed)

---

## Arithmetic Operators Example

```cpp
class Vector2D {
private:
    double x, y;
public:
    Vector2D(double x = 0, double y = 0) : x(x), y(y) {}

    // Member function for +=
    Vector2D& operator+=(const Vector2D& other) {
        x += other.x;
        y += other.y;
        return *this;
    }

    double getX() const { return x; }
    double getY() const { return y; }
};
```

---

## Non-Member Arithmetic Operators

```cpp
// Non-member function for +
Vector2D operator+(const Vector2D& left, const Vector2D& right) {
    Vector2D result = left;  // Copy left operand
    result += right;         // Use += operator
    return result;
}

// Non-member function for -
Vector2D operator-(const Vector2D& left, const Vector2D& right) {
    return Vector2D(left.getX() - right.getX(),
                    left.getY() - right.getY());
}
```

---

## Comparison Operators

```cpp
class Point {
private:
    int x, y;
public:
    Point(int x = 0, int y = 0) : x(x), y(y) {}

    bool operator==(const Point& other) const {
        return x == other.x && y == other.y;
    }

    bool operator!=(const Point& other) const {
        return !(*this == other);  // Reuse == operator
    }

    int getX() const { return x; }
    int getY() const { return y; }
};
```

---

## Ordering Operators

```cpp
bool operator<(const Point& left, const Point& right) {
    if (left.getX() != right.getX()) {
        return left.getX() < right.getX();
    }
    return left.getY() < right.getY();
}

bool operator<=(const Point& left, const Point& right) {
    return left < right || left == right;
}

bool operator>(const Point& left, const Point& right) {
    return !(left <= right);
}

bool operator>=(const Point& left, const Point& right) {
    return !(left < right);
}
```

---

## C++20 Three-Way Comparison

```cpp
#include <compare>

class Point {
private:
    int x, y;
public:
    Point(int x = 0, int y = 0) : x(x), y(y) {}

    // Spaceship operator - generates all comparisons
    auto operator<=>(const Point& other) const {
        if (auto cmp = x <=> other.x; cmp != 0) {
            return cmp;
        }
        return y <=> other.y;
    }

    bool operator==(const Point& other) const = default;
};
```

---

## Stream Operators

```cpp
class Point {
private:
    int x, y;
public:
    Point(int x = 0, int y = 0) : x(x), y(y) {}

    // Friend functions for stream operators
    friend std::ostream& operator<<(std::ostream& os, const Point& p);
    friend std::istream& operator>>(std::istream& is, Point& p);

    int getX() const { return x; }
    int getY() const { return y; }
};
```

---

## Stream Operator Implementation

```cpp
std::ostream& operator<<(std::ostream& os, const Point& p) {
    os << "(" << p.x << ", " << p.y << ")";
    return os;
}

std::istream& operator>>(std::istream& is, Point& p) {
    char lparen, comma, rparen;
    is >> lparen >> p.x >> comma >> p.y >> rparen;
    return is;
}

// Usage:
Point p(3, 4);
std::cout << p;        // Output: (3, 4)
std::cin >> p;         // Input: (5, 6)
```

---

## Increment and Decrement Operators

```cpp
class Counter {
private:
    int value;
public:
    Counter(int v = 0) : value(v) {}

    // Pre-increment: ++counter
    Counter& operator++() {
        ++value;
        return *this;
    }

    // Post-increment: counter++
    Counter operator++(int) {
        Counter temp(*this);
        ++value;
        return temp;
    }

    int getValue() const { return value; }
};
```

---

## Subscript Operator

```cpp
class Array {
private:
    int* data;
    size_t size;
public:
    Array(size_t s) : size(s), data(new int[s]) {}
    ~Array() { delete[] data; }

    // Non-const version
    int& operator[](size_t index) {
        return data[index];
    }

    // Const version
    const int& operator[](size_t index) const {
        return data[index];
    }
};
```

---

## Function Call Operator

```cpp
class Multiplier {
private:
    int factor;
public:
    Multiplier(int f) : factor(f) {}

    // Function call operator
    int operator()(int value) const {
        return value * factor;
    }
};

// Usage:
Multiplier times2(2);
int result = times2(5);  // result = 10
```

---

## Assignment Operators

```cpp
class String {
private:
    char* data;
    size_t length;
public:
    // Copy assignment
    String& operator=(const String& other) {
        if (this != &other) {  // Self-assignment check
            delete[] data;
            length = other.length;
            data = new char[length + 1];
            std::strcpy(data, other.data);
        }
        return *this;
    }

    // Move assignment
    String& operator=(String&& other) noexcept {
        if (this != &other) {
            delete[] data;
            data = other.data;
            length = other.length;
            other.data = nullptr;
            other.length = 0;
        }
        return *this;
    }
};
```

---

## Compound Assignment Operators

```cpp
class Matrix {
private:
    std::vector<std::vector<int>> data;
public:
    Matrix& operator+=(const Matrix& other) {
        for (size_t i = 0; i < data.size(); ++i) {
            for (size_t j = 0; j < data[i].size(); ++j) {
                data[i][j] += other.data[i][j];
            }
        }
        return *this;
    }

    Matrix& operator*=(int scalar) {
        for (auto& row : data) {
            for (auto& element : row) {
                element *= scalar;
            }
        }
        return *this;
    }
};
```

---

## Best Practices

1. **Maintain consistency** with built-in types
1. **Return appropriate types**:
    - `operator+` returns by value
    - `operator+=` returns by reference
1. **Implement related operators together**
1. **Use const appropriately**
1. **Consider both member and non-member versions**

---

## Return Type Guidelines

![return_type_guidelines](svg/courses/languages/c++/modern-c++-for-c-programmers/06_operator_overloading/return_type_guidelines.svg)

---

## Common Mistakes

1. **Not returning reference from assignment operators**
```cpp
// Wrong:
MyClass operator=(const MyClass& other);

// Correct:
MyClass& operator=(const MyClass& other);
```

1. **Forgetting const correctness**
```cpp
// Wrong:
bool operator==(MyClass& other);

// Correct:
bool operator==(const MyClass& other) const;
```

---

## More Common Mistakes

1. **Not checking for self-assignment**
```cpp
MyClass& operator=(const MyClass& other) {
    if (this == &other) return *this;  // Important!
    // ... rest of assignment
    return *this;
}
```

1. **Inconsistent operator relationships**
```cpp
// If you implement ==, also implement !=
// If you implement <, consider implementing >, <=, >=
```

---

## Smart Pointer Example

```cpp
template<typename T>
class SmartPtr {
private:
    T* ptr;
public:
    explicit SmartPtr(T* p = nullptr) : ptr(p) {}
    ~SmartPtr() { delete ptr; }

    // Dereference operators
    T& operator*() const { return *ptr; }
    T* operator->() const { return ptr; }

    // Boolean conversion
    explicit operator bool() const { return ptr != nullptr; }

    // Comparison with nullptr
    bool operator==(std::nullptr_t) const { return ptr == nullptr; }
    bool operator!=(std::nullptr_t) const { return ptr != nullptr; }
};
```

---

## Using the Smart Pointer

```cpp
class Person {
public:
    std::string name;
    void sayHello() { std::cout << "Hello from " << name << std::endl; }
};

int main() {
    SmartPtr<Person> p(new Person);
    p->name = "Alice";
    p->sayHello();

    if (p) {  // Uses operator bool()
        std::cout << "Pointer is valid\n";
    }

    return 0;
}
```

---

## Type Conversion Operators

```cpp
class Temperature {
private:
    double celsius;
public:
    Temperature(double c) : celsius(c) {}

    // Conversion to double (Fahrenheit)
    operator double() const {
        return celsius * 9.0 / 5.0 + 32.0;
    }

    // Explicit conversion to int
    explicit operator int() const {
        return static_cast<int>(celsius);
    }
};
```

---

## Using Conversion Operators

```cpp
int main() {
    Temperature temp(25.0);  // 25°C

    double fahrenheit = temp;  // Implicit conversion: 77°F
    int rounded = static_cast<int>(temp);  // Explicit: 25

    std::cout << "Fahrenheit: " << fahrenheit << std::endl;
    std::cout << "Rounded: " << rounded << std::endl;

    return 0;
}
```

---

## Operator Precedence

Overloaded operators maintain the same precedence as built-in operators:

1. `::` (highest)
1. `()` `[]` `->` `.`
1. `!` `~` `++` `--` (unary)
1. `*` `/` `%`
1. `+` `-`
1. `<<` `>>`
1. `<` `<=` `>` `>=`
1. `==` `!=`
1. `&` (bitwise AND)
1. `^` (XOR)
1. `|` (bitwise OR)
1. `=` `+=` `-=` (lowest)

---

## Friend Functions

```cpp
class Rational {
private:
    int numerator, denominator;
public:
    Rational(int n = 0, int d = 1) : numerator(n), denominator(d) {}

    // Friend function can access private members
    friend Rational operator+(const Rational& left, const Rational& right);
    friend std::ostream& operator<<(std::ostream& os, const Rational& r);
};

Rational operator+(const Rational& left, const Rational& right) {
    return Rational(left.numerator * right.denominator +
                   right.numerator * left.denominator,
                   left.denominator * right.denominator);
}
```

---

## Symmetric Operations

```cpp
class Number {
private:
    int value;
public:
    Number(int v) : value(v) {}

    // Member function - only works for Number + int
    Number operator+(int other) const {
        return Number(value + other);
    }

    // Friend function - works for both Number + int and int + Number
    friend Number operator*(const Number& left, int right);
    friend Number operator*(int left, const Number& right);
};

Number operator*(const Number& left, int right) {
    return Number(left.value * right);
}

Number operator*(int left, const Number& right) {
    return Number(left * right.value);
}
```

---

## Template Operator Overloading

```cpp
template<typename T>
class Vector {
private:
    std::vector<T> data;
public:
    Vector(std::initializer_list<T> init) : data(init) {}

    Vector operator+(const Vector& other) const {
        Vector result;
        result.data.resize(std::max(data.size(), other.data.size()));

        for (size_t i = 0; i < result.data.size(); ++i) {
            T left_val = (i < data.size()) ? data[i] : T{};
            T right_val = (i < other.data.size()) ? other.data[i] : T{};
            result.data[i] = left_val + right_val;
        }

        return result;
    }
};
```

---

## STL Integration

```cpp
class Point {
private:
    int x, y;
public:
    Point(int x = 0, int y = 0) : x(x), y(y) {}

    bool operator<(const Point& other) const {
        return (x < other.x) || (x == other.x && y < other.y);
    }

    bool operator==(const Point& other) const {
        return x == other.x && y == other.y;
    }
};

// Now Point can be used in STL containers
std::set<Point> points;
std::map<Point, std::string> point_names;
std::sort(point_vector.begin(), point_vector.end());
```

---

## Overloading New and Delete

```cpp
class MyClass {
public:
    // Global new/delete overload
    static void* operator new(size_t size) {
        std::cout << "Allocating " << size << " bytes\n";
        return std::malloc(size);
    }

    static void operator delete(void* ptr) {
        std::cout << "Deallocating memory\n";
        std::free(ptr);
    }

    // Array versions
    static void* operator new[](size_t size) {
        return std::malloc(size);
    }

    static void operator delete[](void* ptr) {
        std::free(ptr);
    }
};
```

---

## Performance Considerations

1. **Return by value for temporary results**
    - Compiler optimizations handle this efficiently
1. **Return by reference for assignment operators**
    - Avoids unnecessary copies
1. **Use const references for parameters**
    - Prevents copying large objects
1. **Consider move semantics**
    - Implement move versions for efficiency

---

## Move Semantics with Operators

```cpp
class String {
private:
    char* data;
    size_t length;
public:
    // Move constructor
    String(String&& other) noexcept
        : data(other.data), length(other.length) {
        other.data = nullptr;
        other.length = 0;
    }

    // Move assignment
    String& operator=(String&& other) noexcept {
        if (this != &other) {
            delete[] data;
            data = other.data;
            length = other.length;
            other.data = nullptr;
            other.length = 0;
        }
        return *this;
    }
};
```

---

## Real-World Example: Matrix Class

```cpp
class Matrix {
private:
    std::vector<std::vector<double>> data;
    size_t rows, cols;
public:
    Matrix(size_t r, size_t c) : rows(r), cols(c),
           data(r, std::vector<double>(c, 0.0)) {}

    // Subscript operator
    std::vector<double>& operator[](size_t row) { return data[row]; }
    const std::vector<double>& operator[](size_t row) const { return data[row]; }

    // Matrix addition
    Matrix operator+(const Matrix& other) const {
        Matrix result(rows, cols);
        for (size_t i = 0; i < rows; ++i) {
            for (size_t j = 0; j < cols; ++j) {
                result[i][j] = data[i][j] + other[i][j];
            }
        }
        return result;
    }
};
```

---

## Matrix Class Continued

```cpp
    // Matrix multiplication
    Matrix operator*(const Matrix& other) const {
        Matrix result(rows, other.cols);
        for (size_t i = 0; i < rows; ++i) {
            for (size_t j = 0; j < other.cols; ++j) {
                for (size_t k = 0; k < cols; ++k) {
                    result[i][j] += data[i][k] * other[k][j];
                }
            }
        }
        return result;
    }

    // Stream output
    friend std::ostream& operator<<(std::ostream& os, const Matrix& m) {
        for (const auto& row : m.data) {
            for (double val : row) {
                os << val << " ";
            }
            os << "\n";
        }
        return os;
    }
```

---

## Using the Matrix Class

```cpp
int main() {
    Matrix m1(2, 2);
    Matrix m2(2, 2);

    // Fill matrices
    m1[0][0] = 1; m1[0][1] = 2;
    m1[1][0] = 3; m1[1][1] = 4;

    m2[0][0] = 5; m2[0][1] = 6;
    m2[1][0] = 7; m2[1][1] = 8;

    Matrix sum = m1 + m2;      // Matrix addition
    Matrix product = m1 * m2;  // Matrix multiplication

    std::cout << "Sum:\n" << sum;
    std::cout << "Product:\n" << product;

    return 0;
}
```

---

## Testing Your Operators

```cpp
void testComplexOperators() {
    Complex c1(3, 4);
    Complex c2(1, 2);

    // Test arithmetic
    Complex sum = c1 + c2;
    assert(sum.real() == 4 && sum.imag() == 6);

    // Test assignment
    Complex c3;
    c3 = c1;
    assert(c3 == c1);

    // Test comparison
    assert(c1 != c2);
    assert(c1 == Complex(3, 4));

    std::cout << "All tests passed!\n";
}
```

---

## Debugging Operator Overloads

1. **Add debug output** to see which operators are called
1. **Test edge cases** like self-assignment
1. **Check const correctness** - const objects should work
1. **Verify return types** match expectations
1. **Test with STL containers** to ensure compatibility

---

## Summary

Operator overloading allows you to:
- Create intuitive interfaces for custom types
- Integrate seamlessly with C++ features
- Write more expressive and readable code
- Follow mathematical and logical conventions

Remember to follow established conventions and maintain consistency with built-in types.
