# Strong Primitive Types

---

## Mission Statement for a New Design

- Create type-safe, self-validating primitive types
- Prevent common errors through compile-time type checking
- Make illegal states unrepresentable
- Provide clear semantics and intention-revealing interfaces
- Enable natural, intuitive usage with appropriate operators

---

## Problems with Built-in Primitive Types

```cpp
// Primitive types allow invalid states
int age = -30;     // Negative age is meaningless
bool isDone = 42;  // Any non-zero value becomes true

// Semantic confusion
void sendPayment(int dollars, int cents);

// Easy to mix arguments
sendPayment(50, 75);  // OK - $50.75
sendPayment(75, 50);  // Oops - $75.50

// Implicit conversions lead to mistakes
double calculateTax(double price, double rate) {
    return price * rate;
}

// Is rate 0.08 (8%) or 8 (800%)?
double tax = calculateTax(100.0, 8);
```

---

## Standard Libraries for Time and Date

- C++11 introduces `<chrono>` for duration and time point
- C++20 adds `<date>` for calendar types (C++20, not covered here)

```cpp
#include <chrono>
#include <iostream>

void chronoExample() {
    using namespace std::chrono;

    // Strongly typed durations
    hours h(1);
    minutes m = h;      // Implicit conversion to smaller units
    seconds s1 = h;     // 3600 seconds
    seconds s2 = m;     // 60 seconds

    // Cannot implicitly convert to larger units
    // hours badH = m;  // Error
    hours goodH = duration_cast<hours>(m); // OK with explicit cast

    // Arithmetic works as expected
    auto total = h + m + s1;  // Result is in smallest unit (seconds)

    std::cout << "1 hour + 1 minute + 1 second = "
              << total.count() << " seconds" << std::endl;

    // Time points
    system_clock::time_point now = system_clock::now();
    system_clock::time_point later = now + hours(5) + minutes(30);

    // Duration between time points
    auto diff = later - now;
    std::cout << "Difference: "
              << duration_cast<minutes>(diff).count()
              << " minutes" << std::endl;
}
```

---

## Creating Strongly Typed Primitive Types

Goals for custom primitive types:
1. 1. 1. Type safety - prevent mixing with other types
1. 1. 1. Range validation - ensure values are within valid range
1. 1. 1. Self-documenting - clear semantics through type names
1. 1. 1. Natural usage - appropriate operators and conversions
1. 1. 1. Efficient - minimal runtime overhead

---

## Basic Strong Type Example

```cpp
class Percent {
private:
    double value;

public:
    explicit Percent(double val) {
        if (val < 0.0 || val > 100.0) {
            throw std::out_of_range("Percent value must be between 0 and 100");
        }
        value = val;
    }

    double getValue() const { return value; }

    // Optional: conversion back to double
    explicit operator double() const { return value; }
};

void usePercent() {
    Percent taxRate(8.5);                  // OK
    // Percent invalidRate(150.0);         // Exception
    // double d = taxRate;                 // Error: implicit conversion disabled
    double d = static_cast<double>(taxRate); // OK: explicit conversion

    // Without operators, usage is awkward
    double price = 100.0;
    double tax = price * (taxRate.getValue() / 100.0);
}
```

---

## Strong Type with Operators

```cpp
class Percent {
private:
    double value;

public:
    explicit Percent(double val) : value(val) {
        if (val < 0.0 || val > 100.0) {
            throw std::out_of_range("Percent value must be between 0 and 100");
        }
    }

    double getValue() const { return value; }

    // Arithmetic operators
    Percent operator+(const Percent& other) const {
        return Percent(value + other.value);
    }

    Percent operator-(const Percent& other) const {
        return Percent(value - other.value);
    }

    // Comparison operators
    bool operator==(const Percent& other) const {
        return value == other.value;
    }

    bool operator<(const Percent& other) const {
        return value < other.value;
    }

    // Apply percentage to a value
    template<typename T>
    T operator*(T base) const {
        return base * (value / 100.0);
    }
};

// Free function to apply percentage from right
template<typename T>
T operator*(T base, const Percent& p) {
    return p * base;
}
```

---

## Strong Money Type

```cpp
class Money {
private:
    int64_t cents; // Store money as whole cents to avoid floating-point issues

public:
    // Constructor from dollars and cents
    Money(int dollars, int cents = 0) : cents(dollars * 100LL + cents) {
        if (cents < 0 || cents >= 100) {
            throw std::out_of_range("Cents must be between 0 and 99");
        }
    }

    // Constructor from a decimal amount
    explicit Money(double amount) : cents(static_cast<int64_t>(amount * 100.0 + 0.5)) {}

    // Getters
    int getDollars() const { return static_cast<int>(cents / 100); }
    int getCents() const { return static_cast<int>(cents % 100); }
    double getAmount() const { return cents / 100.0; }

    // Arithmetic operators
    Money operator+(const Money& other) const {
        Money result(0);
        result.cents = cents + other.cents;
        return result;
    }

    Money operator-(const Money& other) const {
        Money result(0);
        result.cents = cents - other.cents;
        return result;
    }

    // Scale by a factor
    Money operator*(double factor) const {
        Money result(0);
        result.cents = static_cast<int64_t>(cents * factor + 0.5);
        return result;
    }
};

// Free function for scaling
Money operator*(double factor, const Money& money) {
    return money * factor;
}
```

---

## Using Strong Types with Standard Algorithms

```cpp
void algorithmExample() {
    std::vector<Percent> taxRates = {
        Percent(7.5), Percent(8.25), Percent(6.0), Percent(9.0)
    };

    // Find minimum tax rate
    auto minRate = std::min_element(
        taxRates.begin(), taxRates.end(),
        [](const Percent& a, const Percent& b) {
            return a.getValue() < b.getValue();
        }
    );

    std::cout << "Minimum tax rate: " << minRate->getValue() << "%" << std::endl;

    // Sort tax rates
    std::sort(taxRates.begin(), taxRates.end());

    // Calculate average using standard algorithm
    double sum = std::accumulate(
        taxRates.begin(), taxRates.end(),
        0.0,
        [](double acc, const Percent& p) {
            return acc + p.getValue();
        }
    );

    double average = sum / taxRates.size();
    std::cout << "Average tax rate: " << average << "%" << std::endl;
}
```

---

## Class Definition Organization

Best practices for organizing class definitions:

```cpp
class Temperature {
public:
    // 1. Type aliases and enums first
    enum class Scale { Celsius, Fahrenheit, Kelvin };

    // 2. Constructors and assignment operators
    explicit Temperature(double val, Scale s = Scale::Celsius);
    Temperature(const Temperature& other) = default;
    Temperature& operator=(const Temperature& other) = default;
    Temperature(Temperature&& other) noexcept = default;
    Temperature& operator=(Temperature&& other) noexcept = default;
    ~Temperature() = default;

    // 3. Core functionality
    double getValue(Scale scale = Scale::Celsius) const;
    void setValue(double val, Scale scale = Scale::Celsius);

    // 4. Operators
    Temperature operator+(const Temperature& other) const;
    Temperature operator-(const Temperature& other) const;
    bool operator==(const Temperature& other) const;
    bool operator<(const Temperature& other) const;

private:
    // 5. Private implementation details
    double celsiusValue;

    // 6. Private helper methods
    double convertToCelsius(double val, Scale fromScale) const;
    double convertFromCelsius(double val, Scale toScale) const;
};
```

---

## Building a Strong Temperature Type

```cpp
class Temperature {
private:
    double kelvin; // Store in Kelvin internally for scientific consistency

    // Valid temperature range (0 Kelvin to practical upper limit)
    static constexpr double MIN_KELVIN = 0.0;
    static constexpr double MAX_KELVIN = 1.0e6; // Arbitrary high value

public:
    enum class Scale { Celsius, Fahrenheit, Kelvin };

    // Constructors with validation
    explicit Temperature(double val, Scale scale = Scale::Celsius) {
        setTemperature(val, scale);
    }

    // Setters with validation
    void setTemperature(double val, Scale scale = Scale::Celsius) {
        switch (scale) {
            case Scale::Celsius:
                kelvin = val + 273.15;
                break;
            case Scale::Fahrenheit:
                kelvin = (val + 459.67) * 5.0 / 9.0;
                break;
            case Scale::Kelvin:
                kelvin = val;
                break;
        }

        if (kelvin < MIN_KELVIN || kelvin > MAX_KELVIN) {
            throw std::out_of_range("Temperature out of valid range");
        }
    }

    // Getters
    double getCelsius() const { return kelvin - 273.15; }
    double getFahrenheit() const { return kelvin * 9.0 / 5.0 - 459.67; }
    double getKelvin() const { return kelvin; }

    double get(Scale scale) const {
        switch (scale) {
            case Scale::Celsius: return getCelsius();
            case Scale::Fahrenheit: return getFahrenheit();
            case Scale::Kelvin: return getKelvin();
            default: throw std::invalid_argument("Invalid scale");
        }
    }
};
```

---

## Adding Operators to Temperature Class

```cpp
class Temperature {
    // Previous members...

public:
    // Arithmetic operators
    Temperature operator+(const Temperature& other) const {
        return Temperature(kelvin + other.kelvin, Scale::Kelvin);
    }

    Temperature operator-(const Temperature& other) const {
        return Temperature(kelvin - other.kelvin, Scale::Kelvin);
    }

    // Scaling
    Temperature operator*(double factor) const {
        return Temperature(kelvin * factor, Scale::Kelvin);
    }

    // Comparison operators
    bool operator==(const Temperature& other) const {
        // Consider floating-point epsilon for equality
        const double epsilon = 1e-9;
        return std::abs(kelvin - other.kelvin) < epsilon;
    }

    bool operator!=(const Temperature& other) const {
        return !(*this == other);
    }

    bool operator<(const Temperature& other) const {
        return kelvin < other.kelvin;
    }

    bool operator>(const Temperature& other) const {
        return other < *this;
    }

    bool operator<=(const Temperature& other) const {
        return !(other < *this);
    }

    bool operator>=(const Temperature& other) const {
        return !(*this < other);
    }
};

// Free function for scaling
Temperature operator*(double factor, const Temperature& temp) {
    return temp * factor;
}
```

---

## Strong ID Types

```cpp
// Generic ID type
template<typename Tag, typename ValueType = int>
class StrongId {
private:
    ValueType value;

public:
    explicit StrongId(ValueType val) : value(val) {}

    ValueType getValue() const { return value; }

    // Comparison operators
    bool operator==(const StrongId& other) const {
        return value == other.value;
    }

    bool operator!=(const StrongId& other) const {
        return !(*this == other);
    }

    bool operator<(const StrongId& other) const {
        return value < other.value;
    }

    // Optional: Increment/decrement for generating sequential IDs
    StrongId& operator++() {
        ++value;
        return *this;
    }

    StrongId operator++(int) {
        StrongId temp = *this;
        ++*this;
        return temp;
    }
};

// Usage
struct UserTag {}; // Empty tag for type differentiation
struct ProductTag {};

using UserId = StrongId<UserTag>;
using ProductId = StrongId<ProductTag>;

void processUser(UserId id) {
    // Process user
}

void useStrongIds() {
    UserId user1(1);
    UserId user2(2);
    ProductId product1(1);

    processUser(user1);  // OK
    // processUser(product1);  // Error: different types

    if (user1 < user2) { /* Compare users */ }
    // if (user1 < product1) { /* Error: incompatible types */ }
}
```

---

## Physical Quantity Types

```cpp
// Simple physical quantity with unit checking
template<int M, int KG, int S>
class Quantity {
private:
    double value;

public:
    explicit Quantity(double val) : value(val) {}

    double getValue() const { return value; }

    // Addition and subtraction only with same units
    Quantity operator+(const Quantity& other) const {
        return Quantity(value + other.value);
    }

    Quantity operator-(const Quantity& other) const {
        return Quantity(value - other.value);
    }

    // Multiplication by scalar
    Quantity operator*(double scalar) const {
        return Quantity(value * scalar);
    }

    // Division by scalar
    Quantity operator/(double scalar) const {
        return Quantity(value / scalar);
    }

    // Multiplication with another quantity
    template<int M2, int KG2, int S2>
    Quantity<M+M2, KG+KG2, S+S2> operator*(const Quantity<M2, KG2, S2>& other) const {
        return Quantity<M+M2, KG+KG2, S+S2>(value * other.getValue());
    }

    // Division by another quantity
    template<int M2, int KG2, int S2>
    Quantity<M-M2, KG-KG2, S-S2> operator/(const Quantity<M2, KG2, S2>& other) const {
        return Quantity<M-M2, KG-KG2, S-S2>(value / other.getValue());
    }
};

// Type aliases for common quantities
using Length = Quantity<1, 0, 0>;   // meters
using Mass = Quantity<0, 1, 0>;     // kilograms
using Time = Quantity<0, 0, 1>;     // seconds
using Velocity = Quantity<1, 0, -1>; // meters/second
using Acceleration = Quantity<1, 0, -2>; // meters/second²
using Force = Quantity<1, 1, -2>;   // newtons (kg·m/s²)
```

---

## Using Physical Quantity Types

```cpp
void physicsCalculations() {
    // Create base quantities
    Length distance(100.0);           // 100 meters
    Time time(10.0);                  // 10 seconds
    Mass mass(5.0);                   // 5 kilograms

    // Derived quantities through operations
    Velocity velocity = distance / time;  // 10 m/s
    std::cout << "Velocity: " << velocity.getValue() << " m/s" << std::endl;

    Acceleration accel = velocity / time; // 1 m/s²
    std::cout << "Acceleration: " << accel.getValue() << " m/s²" << std::endl;

    Force force = mass * accel;        // 5 N
    std::cout << "Force: " << force.getValue() << " N" << std::endl;

    // Static type checking prevents errors
    // Velocity invalid = distance + time;  // Error: incompatible units
    // Force badForce = mass * velocity;    // Error: wrong units

    // Scaling is allowed
    Length doubleDistance = distance * 2.0;  // 200 meters
}
```

---

## Tag Dispatch for Unit Conversion

```cpp
// Tags for different length units
struct MeterTag {};
struct FootTag {};
struct InchTag {};

class Length {
private:
    double meters; // Always store in base unit (meters)

public:
    // Base constructor
    explicit Length(double value, MeterTag) : meters(value) {}

    // Tagged constructors for different units
    explicit Length(double value, FootTag) : meters(value * 0.3048) {}
    explicit Length(double value, InchTag) : meters(value * 0.0254) {}

    // Static factory methods for better readability
    static Length fromMeters(double value) { return Length(value, MeterTag{}); }
    static Length fromFeet(double value) { return Length(value, FootTag{}); }
    static Length fromInches(double value) { return Length(value, InchTag{}); }

    // Getters in different units
    double toMeters() const { return meters; }
    double toFeet() const { return meters / 0.3048; }
    double toInches() const { return meters / 0.0254; }
};

void useTagDispatch() {
    Length height = Length::fromFeet(6.2);
    std::cout << "Height in meters: " << height.toMeters() << std::endl;
    std::cout << "Height in inches: " << height.toInches() << std::endl;
}
```

---

## Named Parameter Idiom

```cpp
class Circle {
public:
    class Builder {
    private:
        double radius_ = 1.0;
        double x_ = 0.0;
        double y_ = 0.0;

    public:
        Builder& radius(double r) {
            if (r <= 0) throw std::invalid_argument("Radius must be positive");
            radius_ = r;
            return *this;
        }

        Builder& centerX(double x) {
            x_ = x;
            return *this;
        }

        Builder& centerY(double y) {
            y_ = y;
            return *this;
        }

        Circle build() const {
            return Circle(radius_, x_, y_);
        }
    };

    static Builder create() {
        return Builder();
    }

    double area() const {
        return 3.14159 * radius_ * radius_;
    }

private:
    double radius_;
    double x_;
    double y_;

    Circle(double r, double x, double y)
        : radius_(r), x_(x), y_(y) {}
};

// Usage
void useNamedParameters() {
    // Clear, self-documenting initialization
    Circle c = Circle::create()
        .radius(2.5)
        .centerX(10.0)
        .centerY(20.0)
        .build();

    std::cout << "Circle area: " << c.area() << std::endl;
}
```

---

## Custom Literals

```cpp
// User-defined literals for units (C++11)
namespace Units {

// Temperature literals
constexpr Temperature operator""_C(long double celsius) {
    return Temperature(static_cast<double>(celsius), Temperature::Scale::Celsius);
}

constexpr Temperature operator""_F(long double fahrenheit) {
    return Temperature(static_cast<double>(fahrenheit), Temperature::Scale::Fahrenheit);
}

constexpr Temperature operator""_K(long double kelvin) {
    return Temperature(static_cast<double>(kelvin), Temperature::Scale::Kelvin);
}

// Length literals
constexpr Length operator""_m(long double value) {
    return Length::fromMeters(static_cast<double>(value));
}

constexpr Length operator""_ft(long double value) {
    return Length::fromFeet(static_cast<double>(value));
}

constexpr Length operator""_in(long double value) {
    return Length::fromInches(static_cast<double>(value));
}

// Time literals
constexpr Time operator""_s(long double value) {
    return Time(static_cast<double>(value));
}

constexpr Time operator""_min(long double value) {
    return Time(static_cast<double>(value * 60.0));
}

constexpr Time operator""_h(long double value) {
    return Time(static_cast<double>(value * 3600.0));
}

} // namespace Units

// Usage
void useCustomLiterals() {
    using namespace Units;

    auto boiling = 100.0_C;
    auto freezing = 32.0_F;
    auto absoluteZero = 0.0_K;

    auto height = 1.8_m;
    auto distance = 26.2_ft;

    auto lapTime = 65.3_s;
    auto cookingTime = 25.0_min;

    std::cout << "Boiling point in F: " << boiling.getFahrenheit() << std::endl;
    std::cout << "Height in inches: " << height.toInches() << std::endl;
    std::cout << "Cooking time in seconds: " << cookingTime.getValue() << std::endl;
}
```

---

## Non-Empty Base Class Optimization

```cpp
// Empty tag class for type differentiation
struct UserIdTag {};

// Basic strong ID template - potentially wastes space
template<typename Tag>
class BasicStrongId {
private:
    int value;
    Tag tag; // Empty member but still takes space in some implementations

public:
    explicit BasicStrongId(int val) : value(val) {}
    int getValue() const { return value; }
};

// Optimized version using empty base class optimization
template<typename Tag>
class OptimizedStrongId : private Tag { // Inherit privately from tag
private:
    int value;

public:
    explicit OptimizedStrongId(int val) : value(val) {}
    int getValue() const { return value; }
};

// Usage
void sizeComparison() {
    std::cout << "Size of BasicStrongId: "
              << sizeof(BasicStrongId<UserIdTag>) << " bytes" << std::endl;

    std::cout << "Size of OptimizedStrongId: "
              << sizeof(OptimizedStrongId<UserIdTag>) << " bytes" << std::endl;
}
```

---

## CRTP for Strong Types

```cpp
// Base template with common operations
template<typename Derived>
class StrongTypeBase {
public:
    // Comparison operators
    bool operator==(const Derived& other) const {
        const Derived& self = static_cast<const Derived&>(*this);
        return self.getValue() == other.getValue();
    }

    bool operator!=(const Derived& other) const {
        return !(*this == other);
    }

    bool operator<(const Derived& other) const {
        const Derived& self = static_cast<const Derived&>(*this);
        return self.getValue() < other.getValue();
    }

    bool operator>(const Derived& other) const {
        return static_cast<const Derived&>(*this) > other;
    }
};

// Strong type implementation with CRTP
template<typename Tag, typename ValueType>
class StrongTypeCRTP : public StrongTypeBase<StrongTypeCRTP<Tag, ValueType>> {
private:
    ValueType value;

public:
    explicit StrongTypeCRTP(ValueType val) : value(val) {}
    ValueType getValue() const { return value; }
};

// Usage
struct EmployeeIdTag {};
struct DepartmentIdTag {};

using EmployeeId = StrongTypeCRTP<EmployeeIdTag, int>;
using DepartmentId = StrongTypeCRTP<DepartmentIdTag, int>;

void useCRTPTypes() {
    EmployeeId e1(101);
    EmployeeId e2(102);

    if (e1 < e2) {
        std::cout << "Employee 1 has lower ID" << std::endl;
    }

    // Type safety maintained
    // if (e1 < DepartmentId(1)) { /* Error: incompatible types */ }
}
```

---

## Preventing Implicit Conversions Between Similar Types

```cpp
// Type trait to determine if types are "similar" strong types
template<typename T, typename U>
struct AreSimilarStrongTypes : std::false_type {};

// Tag types for different distances
struct MilesTag {};
struct KilometersTag {};

// Strong types for different distance units
template<typename Tag>
class Distance {
private:
    double value;

public:
    explicit Distance(double val) : value(val) {}
    double getValue() const { return value; }

    // Conversion constructor with SFINAE to prevent conversions
    // between different strong types
    template<typename OtherTag,
            typename = std::enable_if_t<!AreSimilarStrongTypes<Tag, OtherTag>::value>>
    explicit Distance(const Distance<OtherTag>& other);
};

// Specialization for miles to kilometers
template<>
template<>
Distance<KilometersTag>::Distance(const Distance<MilesTag>& miles)
    : value(miles.getValue() * 1.60934) {}

// Specialization for kilometers to miles
template<>
template<>
Distance<MilesTag>::Distance(const Distance<KilometersTag>& km)
    : value(km.getValue() / 1.60934) {}

// Usage
void preventImplicitConversions() {
    Distance<MilesTag> miles(100.0);

    // Explicit conversion required
    Distance<KilometersTag> km(miles); // Error if not explicit

    std::cout << miles.getValue() << " miles = "
              << km.getValue() << " kilometers" << std::endl;
}
```

---

## Summary: Strong Primitive Types

- Create self-documenting, type-safe primitive types
- Enforce valid ranges and semantics at compile time
- Prevent accidental mixing of incompatible units
- Use templates and CRTP for code reuse
- Consider tagged constructors for unit conversions
- Implement appropriate operators for natural usage
- Use custom literals for intuitive instantiation
- Prefer strong typing over raw primitives in domain logic

---

## Lab Exercises

1. 1. 1. Create a strong `EmailAddress` type with validation
1. 1. 1. Implement a unit-safe `Velocity` class with operators
1. 1. 1. Design a template for creating strong ID types
1. 1. 1. Create a money type with proper rounding semantics
1. 1. 1. Implement a physical quantity system with dimensional analysis
