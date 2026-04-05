# Portable Integers and Robust Constructors

## The Integer Size Problem

C++ integer types have implementation-defined sizes, making portable code challenging

**Standard guarantees (minimum sizes):**
- `char` ≥ 8 bits
- `short` ≥ 16 bits
- `int` ≥ 16 bits
- `long` ≥ 32 bits
- `long long` ≥ 64 bits (C++11)

**Reality varies by platform:**
- 32-bit systems: `int` = 32 bits, `long` = 32 bits
- 64-bit Windows: `int` = 32 bits, `long` = 32 bits
- 64-bit Unix/Linux: `int` = 32 bits, `long` = 64 bits

---

## Language Specification for Integers

Understanding what the standard guarantees:

```cpp
#include <limits>
#include <climits>

void exploreIntegerSizes() {
    std::cout << "sizeof(char): " << sizeof(char) << " bytes" << std::endl;
    std::cout << "sizeof(short): " << sizeof(short) << " bytes" << std::endl;
    std::cout << "sizeof(int): " << sizeof(int) << " bytes" << std::endl;
    std::cout << "sizeof(long): " << sizeof(long) << " bytes" << std::endl;
    std::cout << "sizeof(long long): " << sizeof(long long) << " bytes" << std::endl;

    std::cout << "\nValue ranges:" << std::endl;
    std::cout << "INT_MIN: " << INT_MIN << std::endl;
    std::cout << "INT_MAX: " << INT_MAX << std::endl;
    std::cout << "LONG_MIN: " << LONG_MIN << std::endl;
    std::cout << "LONG_MAX: " << LONG_MAX << std::endl;

    std::cout << "\nUsing numeric_limits:" << std::endl;
    std::cout << "int max: " << std::numeric_limits<int>::max() << std::endl;
    std::cout << "int min: " << std::numeric_limits<int>::min() << std::endl;
}
```

---

## Discovering Integer Size at Runtime

Checking sizes and capabilities at runtime:

```cpp
#include <iostream>
#include <limits>
#include <type_traits>

template<typename T>
void analyzeIntegerType(const std::string& typeName) {
    std::cout << "\n=== " << typeName << " ===" << std::endl;
    std::cout << "Size: " << sizeof(T) << " bytes" << std::endl;
    std::cout << "Bits: " << sizeof(T) * 8 << std::endl;
    std::cout << "Signed: " << std::boolalpha << std::is_signed_v<T> << std::endl;
    std::cout << "Min: " << std::numeric_limits<T>::min() << std::endl;
    std::cout << "Max: " << std::numeric_limits<T>::max() << std::endl;

    if constexpr (std::is_integral_v<T>) {
        std::cout << "Is exact: " << std::numeric_limits<T>::is_exact << std::endl;
        std::cout << "Digits: " << std::numeric_limits<T>::digits << std::endl;
    }
}

void discoverPlatformSizes() {
    analyzeIntegerType<char>("char");
    analyzeIntegerType<short>("short");
    analyzeIntegerType<int>("int");
    analyzeIntegerType<long>("long");
    analyzeIntegerType<long long>("long long");
    analyzeIntegerType<size_t>("size_t");
    analyzeIntegerType<ptrdiff_t>("ptrdiff_t");
}
```

---

## Fixed-Width Integer Types (C++11)

Use `<cstdint>` for guaranteed sizes:

```cpp
#include <cstdint>

void demonstrateFixedWidthTypes() {
    // Exact width types (may not be available on all platforms)
    int8_t   i8  = 127;      // Exactly 8 bits
    int16_t  i16 = 32767;    // Exactly 16 bits
    int32_t  i32 = 2147483647; // Exactly 32 bits
    int64_t  i64 = 9223372036854775807LL; // Exactly 64 bits

    uint8_t  u8  = 255;      // Unsigned 8 bits
    uint16_t u16 = 65535;    // Unsigned 16 bits
    uint32_t u32 = 4294967295U; // Unsigned 32 bits
    uint64_t u64 = 18446744073709551615ULL; // Unsigned 64 bits

    // Minimum width types (guaranteed to be at least N bits)
    int_least8_t  least8  = 100;
    int_least16_t least16 = 1000;
    int_least32_t least32 = 100000;
    int_least64_t least64 = 1000000000LL;

    // Fastest types (fastest type with at least N bits)
    int_fast8_t  fast8  = 42;
    int_fast16_t fast16 = 1000;
    int_fast32_t fast32 = 100000;
    int_fast64_t fast64 = 1000000000LL;

    // Pointer-sized integers
    intptr_t  ptr_int = reinterpret_cast<intptr_t>(&i32);
    uintptr_t ptr_uint = reinterpret_cast<uintptr_t>(&u32);

    // Maximum width types
    intmax_t  max_int = 123456789012345LL;
    uintmax_t max_uint = 123456789012345ULL;
}
```

---

## Choosing the Right Integer Type

Guidelines for selecting appropriate integer types:

```cpp
// For array indices and sizes
void arrayOperations() {
    std::vector<int> data(100);

    // Good: Use size_t for indices and sizes
    for (size_t i = 0; i < data.size(); ++i) {
        data[i] = static_cast<int>(i);
    }

    // Better: Use auto with range-based for
    for (auto& value : data) {
        value *= 2;
    }
}

// For specific bit requirements
class BitFlags {
private:
    uint32_t flags = 0;  // Exactly 32 bits needed

public:
    void setFlag(uint8_t position) {  // Position 0-31
        if (position < 32) {
            flags |= (1U << position);
        }
    }

    bool isFlagSet(uint8_t position) const {
        return position < 32 && (flags & (1U << position)) != 0;
    }
};

// For performance-critical code
void performanceCritical() {
    // Use fastest types for inner loops
    int_fast32_t accumulator = 0;

    for (int_fast32_t i = 0; i < 1000000; ++i) {
        accumulator += i;
    }
}

// For interfacing with C APIs
extern "C" {
    // C function expecting specific types
    void c_function(int32_t value, uint16_t flags);
}

void callCFunction() {
    int32_t value = 42;
    uint16_t flags = 0x1234;
    c_function(value, flags);  // Exact types guaranteed
}
```

---

## Template Classes for Integer Handling

Creating flexible integer handling with templates:

```cpp
template<typename IntType>
class SafeInteger {
private:
    IntType value;

    static_assert(std::is_integral_v<IntType>, "IntType must be an integer type");

public:
    explicit SafeInteger(IntType val = 0) : value(val) {}

    // Safe addition with overflow checking
    SafeInteger operator+(const SafeInteger& other) const {
        if (value > 0 && other.value > std::numeric_limits<IntType>::max() - value) {
            throw std::overflow_error("Addition overflow");
        }
        if (value < 0 && other.value < std::numeric_limits<IntType>::min() - value) {
            throw std::underflow_error("Addition underflow");
        }
        return SafeInteger(value + other.value);
    }

    // Safe multiplication
    SafeInteger operator*(const SafeInteger& other) const {
        if (value != 0 && other.value != 0) {
            if (value > std::numeric_limits<IntType>::max() / other.value ||
                value < std::numeric_limits<IntType>::min() / other.value) {
                throw std::overflow_error("Multiplication overflow");
            }
        }
        return SafeInteger(value * other.value);
    }

    // Conversion operator
    operator IntType() const { return value; }

    // Get the underlying value
    IntType get() const { return value; }

    // Type information
    static constexpr size_t bitWidth() {
        return sizeof(IntType) * 8;
    }

    static constexpr IntType minValue() {
        return std::numeric_limits<IntType>::min();
    }

    static constexpr IntType maxValue() {
        return std::numeric_limits<IntType>::max();
    }
};

// Usage examples
void demonstrateSafeInteger() {
    SafeInteger<int32_t> a(1000000);
    SafeInteger<int32_t> b(2000);

    try {
        auto result = a * b;  // Safe multiplication
        std::cout << "Result: " << result.get() << std::endl;
    } catch (const std::exception& e) {
        std::cout << "Error: " << e.what() << std::endl;
    }

    std::cout << "Bit width: " << SafeInteger<int16_t>::bitWidth() << std::endl;
    std::cout << "Max value: " << SafeInteger<int16_t>::maxValue() << std::endl;
}
```

---

## Template Class Specialization

Specializing templates for specific integer types:

```cpp
// Primary template
template<typename T>
class IntegerTraits {
public:
    static constexpr bool isSigned = std::is_signed_v<T>;
    static constexpr size_t bitWidth = sizeof(T) * 8;
    static constexpr const char* typeName = "unknown";
};

// Specializations for specific types
template<>
class IntegerTraits<int8_t> {
public:
    static constexpr bool isSigned = true;
    static constexpr size_t bitWidth = 8;
    static constexpr const char* typeName = "int8_t";

    static int8_t safeCast(long long value) {
        if (value < -128 || value > 127) {
            throw std::out_of_range("Value out of range for int8_t");
        }
        return static_cast<int8_t>(value);
    }
};

template<>
class IntegerTraits<uint32_t> {
public:
    static constexpr bool isSigned = false;
    static constexpr size_t bitWidth = 32;
    static constexpr const char* typeName = "uint32_t";

    static uint32_t safeCast(unsigned long long value) {
        if (value > 0xFFFFFFFFULL) {
            throw std::out_of_range("Value out of range for uint32_t");
        }
        return static_cast<uint32_t>(value);
    }
};

// Template function using traits
template<typename T>
void printIntegerInfo() {
    std::cout << "Type: " << IntegerTraits<T>::typeName << std::endl;
    std::cout << "Signed: " << IntegerTraits<T>::isSigned << std::endl;
    std::cout << "Bit width: " << IntegerTraits<T>::bitWidth << std::endl;
}

void demonstrateTraits() {
    printIntegerInfo<int8_t>();
    printIntegerInfo<uint32_t>();

    try {
        auto value = IntegerTraits<int8_t>::safeCast(200);  // Will throw
    } catch (const std::exception& e) {
        std::cout << "Caught: " << e.what() << std::endl;
    }
}
```

---

## Template Class Aliasing

Using alias templates for convenience:

```cpp
// Alias templates for common integer types
template<size_t Bits>
using SignedInt = std::conditional_t<
    Bits <= 8, int8_t,
    std::conditional_t<
        Bits <= 16, int16_t,
        std::conditional_t<
            Bits <= 32, int32_t,
            int64_t
        >
    >
>;

template<size_t Bits>
using UnsignedInt = std::conditional_t<
    Bits <= 8, uint8_t,
    std::conditional_t<
        Bits <= 16, uint16_t,
        std::conditional_t<
            Bits <= 32, uint32_t,
            uint64_t
        >
    >
>;

// Platform-specific aliases
using PlatformInt = int;  // Native int size
using FastInt = int_fast32_t;  // Fast 32-bit operations
using PointerInt = intptr_t;   // Pointer-sized integer

// Application-specific aliases
using UserID = uint32_t;       // User identifier
using Timestamp = uint64_t;    // Unix timestamp
using FileSize = uint64_t;     // File size in bytes
using ProcessID = uint32_t;    // Process identifier

// Container size aliases
template<typename Container>
using ContainerSize = typename Container::size_type;

// Usage examples
void demonstrateAliases() {
    SignedInt<12> small_int = 42;     // Becomes int16_t
    UnsignedInt<24> medium_int = 100; // Becomes uint32_t

    UserID user = 12345;
    Timestamp now = 1640995200;  // 2022-01-01 00:00:00 UTC
    FileSize size = 1024 * 1024; // 1 MB

    std::vector<int> data{1, 2, 3, 4, 5};
    ContainerSize<decltype(data)> count = data.size();

    std::cout << "User: " << user << std::endl;
    std::cout << "Timestamp: " << now << std::endl;
    std::cout << "File size: " << size << " bytes" << std::endl;
    std::cout << "Data count: " << count << std::endl;
}
```

---

## Single Point of Maintenance for Constructors

Using delegating constructors to reduce code duplication:

```cpp
class Rectangle {
private:
    double width, height;
    std::string name;

    // Private validation method
    void validate() {
        if (width <= 0 || height <= 0) {
            throw std::invalid_argument("Width and height must be positive");
        }
    }

public:
    // Primary constructor - all initialization logic here
    Rectangle(double w, double h, const std::string& n)
        : width(w), height(h), name(n) {
        validate();
        std::cout << "Rectangle '" << name << "' created: "
                  << width << " x " << height << std::endl;
    }

    // Delegating constructors
    Rectangle(double w, double h) : Rectangle(w, h, "unnamed") {}

    Rectangle(double side) : Rectangle(side, side, "square") {}

    Rectangle() : Rectangle(1.0, 1.0, "unit rectangle") {}

    // Copy constructor
    Rectangle(const Rectangle& other)
        : Rectangle(other.width, other.height, other.name + " (copy)") {}

    // Methods
    double area() const { return width * height; }
    double perimeter() const { return 2 * (width + height); }

    const std::string& getName() const { return name; }
    double getWidth() const { return width; }
    double getHeight() const { return height; }
};

void demonstrateDelegatingConstructors() {
    try {
        Rectangle r1;                    // Uses default values
        Rectangle r2(5.0);              // Square
        Rectangle r3(3.0, 4.0);         // Rectangle with default name
        Rectangle r4(2.0, 6.0, "door"); // Full specification
        Rectangle r5(r4);               // Copy constructor

        std::cout << "r4 area: " << r4.area() << std::endl;
    } catch (const std::exception& e) {
        std::cout << "Error: " << e.what() << std::endl;
    }
}
```

---

## Argument Range Checking

Implementing robust parameter validation:

```cpp
template<typename T>
class RangeValidator {
private:
    T minValue, maxValue;

public:
    RangeValidator(T min_val, T max_val) : minValue(min_val), maxValue(max_val) {
        if (min_val > max_val) {
            throw std::invalid_argument("Minimum value cannot be greater than maximum");
        }
    }

    T validate(T value, const std::string& paramName = "parameter") const {
        if (value < minValue || value > maxValue) {
            throw std::out_of_range(paramName + " value " + std::to_string(value) +
                                   " is outside valid range [" + std::to_string(minValue) +
                                   ", " + std::to_string(maxValue) + "]");
        }
        return value;
    }

    bool isValid(T value) const {
        return value >= minValue && value <= maxValue;
    }

    T clamp(T value) const {
        return std::clamp(value, minValue, maxValue);
    }
};

class BankAccount {
private:
    uint32_t accountNumber;
    int64_t balanceCents;  // Store as cents to avoid floating point issues
    std::string ownerName;

    static RangeValidator<uint32_t> accountValidator;
    static RangeValidator<int64_t> balanceValidator;

public:
    BankAccount(uint32_t account, int64_t initial_balance, const std::string& owner)
        : accountNumber(accountValidator.validate(account, "Account number"))
        , balanceCents(balanceValidator.validate(initial_balance, "Initial balance"))
        , ownerName(validateName(owner)) {

        std::cout << "Account created for " << ownerName
                  << " with balance $" << (balanceCents / 100.0) << std::endl;
    }

    // Convenience constructor with validation
    BankAccount(uint32_t account, double initial_dollars, const std::string& owner)
        : BankAccount(account, static_cast<int64_t>(initial_dollars * 100), owner) {}

    void deposit(int64_t cents) {
        cents = balanceValidator.validate(cents, "Deposit amount");
        if (cents <= 0) {
            throw std::invalid_argument("Deposit amount must be positive");
        }

        // Check for overflow
        if (balanceCents > balanceValidator.validate(
            std::numeric_limits<int64_t>::max() - cents, "New balance")) {
            throw std::overflow_error("Deposit would cause balance overflow");
        }

        balanceCents += cents;
    }

    void withdraw(int64_t cents) {
        cents = balanceValidator.validate(cents, "Withdrawal amount");
        if (cents <= 0) {
            throw std::invalid_argument("Withdrawal amount must be positive");
        }
        if (cents > balanceCents) {
            throw std::insufficient_funds("Insufficient funds for withdrawal");
        }

        balanceCents -= cents;
    }

    double getBalance() const { return balanceCents / 100.0; }
    uint32_t getAccountNumber() const { return accountNumber; }
    const std::string& getOwnerName() const { return ownerName; }

private:
    std::string validateName(const std::string& name) {
        if (name.empty() || name.length() > 100) {
            throw std::invalid_argument("Owner name must be 1-100 characters");
        }
        if (std::all_of(name.begin(), name.end(), ::isspace)) {
            throw std::invalid_argument("Owner name cannot be only whitespace");
        }
        return name;
    }

    class insufficient_funds : public std::runtime_error {
    public:
        explicit insufficient_funds(const std::string& msg) : std::runtime_error(msg) {}
    };
};

// Static member definitions
RangeValidator<uint32_t> BankAccount::accountValidator(1000, 9999999);
RangeValidator<int64_t> BankAccount::balanceValidator(-100000000, 100000000000);  // -$1M to $1B
```

---

## Custom Literals (C++11)

Creating user-defined literals for intuitive initialization:

```cpp
// Literals for different integer bases
constexpr uint64_t operator"" _KB(unsigned long long value) {
    return value * 1024;
}

constexpr uint64_t operator"" _MB(unsigned long long value) {
    return value * 1024 * 1024;
}

constexpr uint64_t operator"" _GB(unsigned long long value) {
    return value * 1024 * 1024 * 1024;
}

// Literals for time durations (extending std::chrono)
constexpr std::chrono::milliseconds operator"" _ms(unsigned long long value) {
    return std::chrono::milliseconds(value);
}

constexpr std::chrono::seconds operator"" _s(unsigned long long value) {
    return std::chrono::seconds(value);
}

// Binary literal helper
constexpr uint64_t operator"" _binary(const char* str) {
    uint64_t result = 0;
    while (*str) {
        if (*str == '0' || *str == '1') {
            result = result * 2 + (*str - '0');
        }
        ++str;
    }
    return result;
}

// Hexadecimal with type safety
template<typename T>
struct HexValue {
    T value;
    explicit HexValue(T v) : value(v) {}
    operator T() const { return value; }
};

HexValue<uint32_t> operator"" _hex32(const char* str, size_t) {
    return HexValue<uint32_t>(std::stoul(str, nullptr, 16));
}

HexValue<uint64_t> operator"" _hex64(const char* str, size_t) {
    return HexValue<uint64_t>(std::stoull(str, nullptr, 16));
}

// Usage examples
void demonstrateCustomLiterals() {
    // Memory sizes
    auto fileSize = 500_MB;
    auto cacheSize = 64_KB;
    auto maxMemory = 4_GB;

    std::cout << "File size: " << fileSize << " bytes" << std::endl;
    std::cout << "Cache size: " << cacheSize << " bytes" << std::endl;
    std::cout << "Max memory: " << maxMemory << " bytes" << std::endl;

    // Time durations
    auto timeout = 30_s;
    auto interval = 100_ms;

    std::cout << "Timeout: " << timeout.count() << " seconds" << std::endl;
    std::cout << "Interval: " << interval.count() << " milliseconds" << std::endl;

    // Binary values
    auto flags = "10110101"_binary;
    std::cout << "Binary flags: " << std::hex << flags << std::dec << std::endl;

    // Hexadecimal values
    uint32_t address = "DEADBEEF"_hex32;
    uint64_t bigValue = "123456789ABCDEF0"_hex64;

    std::cout << "Address: 0x" << std::hex << address << std::dec << std::endl;
    std::cout << "Big value: 0x" << std::hex << bigValue << std::dec << std::endl;
}
```

---

## Template Parameter Deduction

Understanding how templates deduce types automatically:

```cpp
// Function template with type deduction
template<typename T>
T maximum(T a, T b) {
    return (a > b) ? a : b;
}

// Template with multiple parameters
template<typename T, typename U>
auto add(T a, U b) -> decltype(a + b) {
    return a + b;
}

// C++14 auto return type deduction
template<typename T, typename U>
auto multiply(T a, U b) {
    return a * b;
}

// Template with non-type parameters
template<typename T, size_t N>
class FixedArray {
private:
    T data[N];

public:
    FixedArray() = default;

    T& operator[](size_t index) {
        if (index >= N) {
            throw std::out_of_range("Index out of bounds");
        }
        return data[index];
    }

    const T& operator[](size_t index) const {
        if (index >= N) {
            throw std::out_of_range("Index out of bounds");
        }
        return data[index];
    }

    constexpr size_t size() const { return N; }

    // Iterator support
    T* begin() { return data; }
    T* end() { return data + N; }
    const T* begin() const { return data; }
    const T* end() const { return data + N; }
};

// Template argument deduction guides (C++17)
template<typename T, typename... Args>
FixedArray(T, Args...) -> FixedArray<T, 1 + sizeof...(Args)>;

void demonstrateDeduction() {
    // Type deduction in action
    auto result1 = maximum(5, 10);        // T deduced as int
    auto result2 = maximum(3.14, 2.71);   // T deduced as double

    // Mixed type operations
    auto result3 = add(5, 3.14);          // int + double = double
    auto result4 = multiply(2, 3.5f);     // int * float = float

    // Array with deduced size
    FixedArray<int, 5> array1;
    array1[0] = 10;
    array1[4] = 50;

    // C++17 deduction guide (if available)
#if __cpp_deduction_guides >= 201606
    FixedArray array2{1, 2, 3, 4, 5};  // Deduced as FixedArray<int, 5>
#endif

    std::cout << "Maximum of 5 and 10: " << result1 << std::endl;
    std::cout << "Maximum of 3.14 and 2.71: " << result2 << std::endl;
    std::cout << "5 + 3.14 = " << result3 << std::endl;
    std::cout << "2 * 3.5f = " << result4 << std::endl;
}
```

---

## Template Functions with Non-Argument Type Parameters

Templates with explicit type parameters:

```cpp
// Template with explicit type parameter
template<typename ReturnType, typename InputType>
ReturnType safe_cast(InputType value) {
    if constexpr (std::is_integral_v<InputType> && std::is_integral_v<ReturnType>) {
        // Integer to integer conversion
        if (value < std::numeric_limits<ReturnType>::min() ||
            value > std::numeric_limits<ReturnType>::max()) {
            throw std::out_of_range("Value out of range for target type");
        }
    } else if constexpr (std::is_floating_point_v<InputType> && std::is_integral_v<ReturnType>) {
        // Float to integer conversion
        if (std::isnan(value) || std::isinf(value)) {
            throw std::invalid_argument("Cannot convert NaN or infinity to integer");
        }
        if (value < std::numeric_limits<ReturnType>::min() ||
            value > std::numeric_limits<ReturnType>::max()) {
            throw std::out_of_range("Value out of range for target type");
        }
    }

    return static_cast<ReturnType>(value);
}

// Template with size parameter
template<size_t BitWidth>
struct IntegerSelector {
    using type = std::conditional_t<
        BitWidth <= 8, uint8_t,
        std::conditional_t<
            BitWidth <= 16, uint16_t,
            std::conditional_t<
                BitWidth <= 32, uint32_t,
                uint64_t
            >
        >
    >;
};

template<size_t BitWidth>
using integer_t = typename IntegerSelector<BitWidth>::type;

// Template function using size parameter
template<size_t Bits>
integer_t<Bits> createMask() {
    static_assert(Bits <= 64, "Cannot create mask with more than 64 bits");
    if constexpr (Bits == 64) {
        return ~integer_t<Bits>(0);
    } else {
        return (integer_t<Bits>(1) << Bits) - 1;
    }
}

// Template with value parameter
template<int Base>
constexpr long long power(int exponent) {
    static_assert(Base != 0, "Base cannot be zero");

    if (exponent == 0) return 1;
    if (exponent == 1) return Base;

    long long result = 1;
    int abs_exp = (exponent < 0) ? -exponent : exponent;

    for (int i = 0; i < abs_exp; ++i) {
        result *= Base;
    }

    return (exponent < 0) ? 1 / result : result;
}

void demonstrateNonArgumentParameters() {
    // Safe casting with explicit types
    try {
        auto result1 = safe_cast<int16_t>(42);        // int to int16_t
        auto result2 = safe_cast<uint8_t>(255);       // int to uint8_t
        auto result3 = safe_cast<int>(3.14);          // double to int

        std::cout << "Safe cast results: " << result1 << ", "
                  << static_cast<int>(result2) << ", " << result3 << std::endl;

        // This would throw an exception
        // auto bad_cast = safe_cast<uint8_t>(1000);

    } catch (const std::exception& e) {
        std::cout << "Conversion error: " << e.what() << std::endl;
    }

    // Using bit-width selector
    integer_t<12> small_int = 100;   // Becomes uint16_t
    integer_t<24> medium_int = 1000; // Becomes uint32_t
    integer_t<48> large_int = 10000; // Becomes uint64_t

    // Creating masks
    auto mask8 = createMask<8>();    // 0xFF
    auto mask16 = createMask<16>();  // 0xFFFF
    auto mask32 = createMask<32>();  // 0xFFFFFFFF

    std::cout << "8-bit mask: 0x" << std::hex << static_cast<int>(mask8) << std::dec << std::endl;
    std::cout << "16-bit mask: 0x" << std::hex << mask16 << std::dec << std::endl;
    std::cout << "32-bit mask: 0x" << std::hex << mask32 << std::dec << std::endl;

    // Compile-time power calculations
    constexpr auto power2_10 = power<2>(10);  // 1024
    constexpr auto power10_3 = power<10>(3);  // 1000

    std::cout << "2^10 = " << power2_10 << std::endl;
    std::cout << "10^3 = " << power10_3 << std::endl;
}
```

---

## Template Function Overloading

Overloading template functions with different constraints:

```cpp
#include <type_traits>
#include <iostream>
#include <string>

// Primary template for general types
template<typename T>
void process(T value) {
    std::cout << "Processing general type: " << value << std::endl;
}

// Specialization for integral types
template<typename T>
typename std::enable_if_t<std::is_integral_v<T>>
process(T value) {
    std::cout << "Processing integer: " << value
              << " (bits: " << sizeof(T) * 8 << ")" << std::endl;
}

// Specialization for floating point types
template<typename T>
typename std::enable_if_t<std::is_floating_point_v<T>>
process(T value) {
    std::cout << "Processing floating point: " << std::fixed << value
              << " (precision: " << (sizeof(T) == 4 ? "single" : "double") << ")" << std::endl;
}

// C++17 constexpr if version (cleaner)
template<typename T>
void process_modern(T value) {
    if constexpr (std::is_integral_v<T>) {
        std::cout << "Processing integer: " << value
                  << " (bits: " << sizeof(T) * 8 << ")" << std::endl;
    } else if constexpr (std::is_floating_point_v<T>) {
        std::cout << "Processing floating point: " << std::fixed << value
                  << " (precision: " << (sizeof(T) == 4 ? "single" : "double") << ")" << std::endl;
    } else {
        std::cout << "Processing other type: " << value << std::endl;
    }
}

// Function overloading with different parameter counts
template<typename T>
T safe_add(T a) {
    return a;
}

template<typename T>
T safe_add(T a, T b) {
    // Check for overflow
    if constexpr (std::is_integral_v<T> && std::is_signed_v<T>) {
        if (a > 0 && b > std::numeric_limits<T>::max() - a) {
            throw std::overflow_error("Addition overflow");
        }
        if (a < 0 && b < std::numeric_limits<T>::min() - a) {
            throw std::underflow_error("Addition underflow");
        }
    }
    return a + b;
}

template<typename T, typename... Args>
T safe_add(T first, Args... rest) {
    return safe_add(first, safe_add(rest...));
}

// SFINAE-based overloading
template<typename Container>
auto size_helper(const Container& c, int) -> decltype(c.size()) {
    return c.size();  // Use member function if available
}

template<typename Container>
auto size_helper(const Container& c, long) -> decltype(std::distance(std::begin(c), std::end(c))) {
    return std::distance(std::begin(c), std::end(c));  // Fallback to iterator distance
}

template<typename Container>
auto get_size(const Container& c) {
    return size_helper(c, 0);  // int preferred over long
}

void demonstrateTemplateOverloading() {
    // Type-based overloading
    process(42);        // Integer version
    process(3.14);      // Floating point version
    process("hello");   // General version

    std::cout << "\nModern version:" << std::endl;
    process_modern(42);
    process_modern(3.14f);
    process_modern(std::string("hello"));

    // Variadic template overloading
    try {
        auto result1 = safe_add(5);
        auto result2 = safe_add(10, 20);
        auto result3 = safe_add(1, 2, 3, 4, 5);

        std::cout << "\nSafe add results: " << result1 << ", "
                  << result2 << ", " << result3 << std::endl;
    } catch (const std::exception& e) {
        std::cout << "Error: " << e.what() << std::endl;
    }

    // SFINAE-based size detection
    std::vector<int> vec{1, 2, 3, 4, 5};
    int array[] = {1, 2, 3};

    std::cout << "Vector size: " << get_size(vec) << std::endl;
    std::cout << "Array size: " << get_size(array) << std::endl;
}
```

---

## Template Specialization

Full and partial template specialization:

```cpp
// Primary template
template<typename T, size_t N>
class StaticArray {
private:
    T data[N];

public:
    StaticArray() = default;

    T& operator[](size_t index) { return data[index]; }
    const T& operator[](size_t index) const { return data[index]; }

    constexpr size_t size() const { return N; }

    void fill(const T& value) {
        for (size_t i = 0; i < N; ++i) {
            data[i] = value;
        }
    }

    void print() const {
        std::cout << "StaticArray<" << typeid(T).name() << ", " << N << ">: ";
        for (size_t i = 0; i < N; ++i) {
            std::cout << data[i] << " ";
        }
        std::cout << std::endl;
    }
};

// Full specialization for bool
template<size_t N>
class StaticArray<bool, N> {
private:
    uint8_t data[(N + 7) / 8];  // Pack bits

public:
    StaticArray() { std::memset(data, 0, sizeof(data)); }

    class BitReference {
    private:
        uint8_t* byte;
        size_t bit_pos;

    public:
        BitReference(uint8_t* b, size_t pos) : byte(b), bit_pos(pos) {}

        BitReference& operator=(bool value) {
            if (value) {
                *byte |= (1 << bit_pos);
            } else {
                *byte &= ~(1 << bit_pos);
            }
            return *this;
        }

        operator bool() const {
            return (*byte & (1 << bit_pos)) != 0;
        }
    };

    BitReference operator[](size_t index) {
        return BitReference(&data[index / 8], index % 8);
    }

    bool operator[](size_t index) const {
        return (data[index / 8] & (1 << (index % 8))) != 0;
    }

    constexpr size_t size() const { return N; }

    void fill(bool value) {
        uint8_t fill_byte = value ? 0xFF : 0x00;
        std::memset(data, fill_byte, sizeof(data));
    }

    void print() const {
        std::cout << "StaticArray<bool, " << N << ">: ";
        for (size_t i = 0; i < N; ++i) {
            std::cout << ((*this)[i] ? '1' : '0') << " ";
        }
        std::cout << std::endl;
    }
};

// Partial specialization for pointers
template<typename T, size_t N>
class StaticArray<T*, N> {
private:
    T* data[N];

public:
    StaticArray() { std::fill(data, data + N, nullptr); }

    T*& operator[](size_t index) { return data[index]; }
    T* const& operator[](size_t index) const { return data[index]; }

    constexpr size_t size() const { return N; }

    void fill(T* value) {
        std::fill(data, data + N, value);
    }

    size_t count_non_null() const {
        return std::count_if(data, data + N, [](T* ptr) { return ptr != nullptr; });
    }

    void print() const {
        std::cout << "StaticArray<" << typeid(T).name() << "*, " << N << ">: ";
        for (size_t i = 0; i < N; ++i) {
            if (data[i]) {
                std::cout << data[i] << " ";
            } else {
                std::cout << "null ";
            }
        }
        std::cout << std::endl;
    }
};

// Template specialization for specific size
template<typename T>
class StaticArray<T, 1> {
private:
    T value;

public:
    StaticArray() = default;
    explicit StaticArray(const T& val) : value(val) {}

    T& operator[](size_t index) {
        if (index != 0) throw std::out_of_range("Index must be 0");
        return value;
    }

    const T& operator[](size_t index) const {
        if (index != 0) throw std::out_of_range("Index must be 0");
        return value;
    }

    constexpr size_t size() const { return 1; }

    void fill(const T& val) { value = val; }

    // Additional operations for single-element arrays
    operator T&() { return value; }
    operator const T&() const { return value; }

    void print() const {
        std::cout << "StaticArray<" << typeid(T).name() << ", 1>: " << value << std::endl;
    }
};

void demonstrateSpecialization() {
    // Regular array
    StaticArray<int, 5> intArray;
    intArray.fill(42);
    intArray[2] = 100;
    intArray.print();

    // Bool specialization (bit-packed)
    StaticArray<bool, 10> boolArray;
    boolArray.fill(false);
    boolArray[0] = true;
    boolArray[3] = true;
    boolArray[7] = true;
    boolArray.print();

    // Pointer specialization
    StaticArray<int*, 3> ptrArray;
    int x = 10, y = 20;
    ptrArray[0] = &x;
    ptrArray[2] = &y;
    std::cout << "Non-null pointers: " << ptrArray.count_non_null() << std::endl;
    ptrArray.print();

    // Single-element specialization
    StaticArray<double, 1> singleArray(3.14159);
    double value = singleArray;  // Implicit conversion
    std::cout << "Single value: " << value << std::endl;
    singleArray.print();
}
```

---

## Template Instantiation and Linkage

Understanding template instantiation and ODR issues:

```cpp
// Template declaration in header
template<typename T>
class Calculator {
public:
    T add(T a, T b) { return a + b; }
    T multiply(T a, T b) { return a * b; }

    // Inline function - defined in header
    T subtract(T a, T b) { return a - b; }
};

// Explicit template instantiation declaration
extern template class Calculator<int>;
extern template class Calculator<double>;

// Function template
template<typename T>
T power(T base, int exponent) {
    T result = T(1);
    for (int i = 0; i < exponent; ++i) {
        result *= base;
    }
    return result;
}

// Explicit instantiation declaration
extern template int power<int>(int, int);
extern template double power<double>(double, int);

// Template with static member
template<typename T>
class Counter {
private:
    static int count;

public:
    Counter() { ++count; }
    ~Counter() { --count; }

    static int getCount() { return count; }
};

// Static member definition template
template<typename T>
int Counter<T>::count = 0;

// Explicit instantiation of static member
template int Counter<int>::count;
template int Counter<double>::count;

// Template linkage demonstration
void demonstrateInstantiation() {
    // These will use the explicitly instantiated versions
    Calculator<int> intCalc;
    Calculator<double> doubleCalc;

    auto result1 = intCalc.add(5, 3);
    auto result2 = doubleCalc.multiply(2.5, 4.0);

    // Function template usage
    auto result3 = power(2, 10);      // Uses explicit instantiation
    auto result4 = power(1.5, 3);     // Uses explicit instantiation

    // Counter usage
    Counter<int> c1, c2, c3;
    Counter<double> d1, d2;

    std::cout << "Int calculators: " << result1 << std::endl;
    std::cout << "Double calculators: " << result2 << std::endl;
    std::cout << "Power results: " << result3 << ", " << result4 << std::endl;
    std::cout << "Int counters: " << Counter<int>::getCount() << std::endl;
    std::cout << "Double counters: " << Counter<double>::getCount() << std::endl;
}

// Template with friend function
template<typename T>
class Point {
private:
    T x, y;

public:
    Point(T x_val, T y_val) : x(x_val), y(y_val) {}

    // Friend function template
    template<typename U>
    friend std::ostream& operator<<(std::ostream& os, const Point<U>& point);

    // Non-template friend (one friend per instantiation)
    friend Point operator+(const Point& lhs, const Point& rhs) {
        return Point(lhs.x + rhs.x, lhs.y + rhs.y);
    }

    T getX() const { return x; }
    T getY() const { return y; }
};

// Friend function definition
template<typename T>
std::ostream& operator<<(std::ostream& os, const Point<T>& point) {
    return os << "(" << point.x << ", " << point.y << ")";
}

void demonstrateTemplateFriends() {
    Point<int> p1(3, 4);
    Point<int> p2(1, 2);
    Point<int> p3 = p1 + p2;  // Uses friend operator+

    std::cout << "Point arithmetic: " << p1 << " + " << p2 << " = " << p3 << std::endl;
}
```

---

## Namespaces for Organization

Using namespaces to organize template code:

```cpp
namespace math {
    namespace detail {
        // Internal implementation details
        template<typename T>
        constexpr bool is_power_of_two(T value) {
            return value > 0 && (value & (value - 1)) == 0;
        }

        template<typename T>
        T gcd_impl(T a, T b) {
            while (b != 0) {
                T temp = b;
                b = a % b;
                a = temp;
            }
            return a;
        }
    }

    // Public interface
    template<typename T>
    class Fraction {
    private:
        T numerator, denominator;

        void simplify() {
            T g = detail::gcd_impl(numerator, denominator);
            numerator /= g;
            denominator /= g;

            if (denominator < 0) {
                numerator = -numerator;
                denominator = -denominator;
            }
        }

    public:
        Fraction(T num = 0, T den = 1) : numerator(num), denominator(den) {
            if (denominator == 0) {
                throw std::invalid_argument("Denominator cannot be zero");
            }
            simplify();
        }

        Fraction operator+(const Fraction& other) const {
            return Fraction(numerator * other.denominator + other.numerator * denominator,
                           denominator * other.denominator);
        }

        Fraction operator*(const Fraction& other) const {
            return Fraction(numerator * other.numerator,
                           denominator * other.denominator);
        }

        bool operator==(const Fraction& other) const {
            return numerator == other.numerator && denominator == other.denominator;
        }

        double toDouble() const {
            return static_cast<double>(numerator) / denominator;
        }

        T getNumerator() const { return numerator; }
        T getDenominator() const { return denominator; }
    };

    template<typename T>
    T gcd(T a, T b) {
        return detail::gcd_impl(std::abs(a), std::abs(b));
    }

    template<typename T>
    T lcm(T a, T b) {
        return (a * b) / gcd(a, b);
    }

    // Constants namespace
    namespace constants {
        template<typename T>
        constexpr T pi = T(3.14159265358979323846);

        template<typename T>
        constexpr T e = T(2.71828182845904523536);

        template<typename T>
        constexpr T sqrt2 = T(1.41421356237309504880);
    }
}

namespace containers {
    template<typename T, size_t Capacity>
    class CircularBuffer {
    private:
        std::array<T, Capacity> buffer;
        size_t head = 0;
        size_t tail = 0;
        size_t count = 0;

    public:
        bool push(const T& item) {
            if (count == Capacity) {
                return false;  // Buffer full
            }

            buffer[tail] = item;
            tail = (tail + 1) % Capacity;
            ++count;
            return true;
        }

        bool pop(T& item) {
            if (count == 0) {
                return false;  // Buffer empty
            }

            item = buffer[head];
            head = (head + 1) % Capacity;
            --count;
            return true;
        }

        bool empty() const { return count == 0; }
        bool full() const { return count == Capacity; }
        size_t size() const { return count; }
        constexpr size_t capacity() const { return Capacity; }
    };

    // Alias for common buffer sizes
    template<typename T>
    using SmallBuffer = CircularBuffer<T, 16>;

    template<typename T>
    using MediumBuffer = CircularBuffer<T, 256>;

    template<typename T>
    using LargeBuffer = CircularBuffer<T, 4096>;
}

void demonstrateNamespaces() {
    // Using math namespace
    math::Fraction<int> f1(1, 2);
    math::Fraction<int> f2(1, 3);
    auto f3 = f1 + f2;

    std::cout << "Fraction arithmetic: 1/2 + 1/3 = "
              << f3.getNumerator() << "/" << f3.getDenominator()
              << " = " << f3.toDouble() << std::endl;

    auto gcd_result = math::gcd(48, 18);
    auto lcm_result = math::lcm(48, 18);

    std::cout << "GCD(48, 18) = " << gcd_result << std::endl;
    std::cout << "LCM(48, 18) = " << lcm_result << std::endl;

    // Using constants
    auto circle_area = math::constants::pi<double> * 5.0 * 5.0;
    std::cout << "Circle area (r=5): " << circle_area << std::endl;

    // Using containers namespace
    containers::SmallBuffer<int> buffer;

    // Fill buffer
    for (int i = 0; i < 20; ++i) {
        if (!buffer.push(i)) {
            std::cout << "Buffer full at item " << i << std::endl;
            break;
        }
    }

    // Empty buffer
    int value;
    while (buffer.pop(value)) {
        std::cout << value << " ";
    }
    std::cout << std::endl;
}
```

---

## Namespace Aliases and Using Declarations

Managing complex namespace hierarchies:

```cpp
namespace company {
    namespace graphics {
        namespace rendering {
            namespace opengl {
                class Renderer {
                public:
                    void render() {
                        std::cout << "OpenGL rendering" << std::endl;
                    }

                    void setViewport(int width, int height) {
                        std::cout << "Setting viewport: " << width << "x" << height << std::endl;
                    }
                };

                class Texture {
                public:
                    void bind() {
                        std::cout << "Binding OpenGL texture" << std::endl;
                    }
                };
            }

            namespace vulkan {
                class Renderer {
                public:
                    void render() {
                        std::cout << "Vulkan rendering" << std::endl;
                    }

                    void setViewport(int width, int height) {
                        std::cout << "Setting Vulkan viewport: " << width << "x" << height << std::endl;
                    }
                };

                class Texture {
                public:
                    void bind() {
                        std::cout << "Binding Vulkan texture" << std::endl;
                    }
                };
            }
        }

        namespace math {
            template<typename T>
            struct Vector3 {
                T x, y, z;

                Vector3(T x_val = T{}, T y_val = T{}, T z_val = T{})
                    : x(x_val), y(y_val), z(z_val) {}

                Vector3 operator+(const Vector3& other) const {
                    return Vector3(x + other.x, y + other.y, z + other.z);
                }

                T dot(const Vector3& other) const {
                    return x * other.x + y * other.y + z * other.z;
                }
            };

            using Vector3f = Vector3<float>;
            using Vector3d = Vector3<double>;
            using Vector3i = Vector3<int>;
        }
    }
}

void demonstrateNamespaceAliases() {
    // Namespace aliases for convenience
    namespace gl = company::graphics::rendering::opengl;
    namespace vk = company::graphics::rendering::vulkan;
    namespace gmath = company::graphics::math;

    // Using specific types
    using OpenGLRenderer = company::graphics::rendering::opengl::Renderer;
    using Vec3f = company::graphics::math::Vector3f;

    // Usage with aliases
    gl::Renderer glRenderer;
    gl::Texture glTexture;

    vk::Renderer vkRenderer;
    vk::Texture vkTexture;

    glRenderer.render();
    glRenderer.setViewport(1920, 1080);
    glTexture.bind();

    vkRenderer.render();
    vkRenderer.setViewport(1920, 1080);
    vkTexture.bind();

    // Math operations
    Vec3f v1(1.0f, 2.0f, 3.0f);
    Vec3f v2(4.0f, 5.0f, 6.0f);
    auto v3 = v1 + v2;
    auto dot_product = v1.dot(v2);

    std::cout << "Vector sum: (" << v3.x << ", " << v3.y << ", " << v3.z << ")" << std::endl;
    std::cout << "Dot product: " << dot_product << std::endl;
}

// ADL (Argument-Dependent Lookup) demonstration
namespace custom {
    template<typename T>
    class SmartPointer {
    private:
        T* ptr;

    public:
        explicit SmartPointer(T* p = nullptr) : ptr(p) {}
        ~SmartPointer() { delete ptr; }

        SmartPointer(const SmartPointer&) = delete;
        SmartPointer& operator=(const SmartPointer&) = delete;

        SmartPointer(SmartPointer&& other) noexcept : ptr(other.ptr) {
            other.ptr = nullptr;
        }

        SmartPointer& operator=(SmartPointer&& other) noexcept {
            if (this != &other) {
                delete ptr;
                ptr = other.ptr;
                other.ptr = nullptr;
            }
            return *this;
        }

        T* get() const { return ptr; }
        T& operator*() const { return *ptr; }
        T* operator->() const { return ptr; }
        explicit operator bool() const { return ptr != nullptr; }
    };

    // Free function in same namespace (ADL will find this)
    template<typename T>
    void swap(SmartPointer<T>& a, SmartPointer<T>& b) {
        std::cout << "Using custom swap for SmartPointer" << std::endl;
        // Implement efficient swap
        T* temp = a.ptr;
        a.ptr = b.ptr;
        b.ptr = temp;
    }

    template<typename T, typename... Args>
    SmartPointer<T> make_smart(Args&&... args) {
        return SmartPointer<T>(new T(std::forward<Args>(args)...));
    }
}

void demonstrateADL() {
    auto ptr1 = custom::make_smart<int>(42);
    auto ptr2 = custom::make_smart<int>(100);

    std::cout << "Before swap: " << *ptr1 << ", " << *ptr2 << std::endl;

    // ADL finds custom::swap due to argument types
    swap(ptr1, ptr2);  // No need for custom:: prefix

    std::cout << "After swap: " << *ptr1 << ", " << *ptr2 << std::endl;
}
```

---

## Best Practices Summary

**Portable Integer Guidelines:**
1. **Use fixed-width types** (`int32_t`, `uint64_t`) when exact size matters
1. **Use size_t** for array indices and container sizes
1. **Use appropriate fastest types** for performance-critical loops
1. **Validate ranges** in constructors and setter functions
1. **Use delegating constructors** to centralize initialization logic

**Template Best Practices:**
1. **Constrain templates** with SFINAE or concepts (C++20)
1. **Provide clear error messages** with static_assert
1. **Use explicit instantiation** to control compilation units
1. **Organize with namespaces** to avoid naming conflicts
1. **Document template requirements** clearly

**Constructor Design:**
1. **Single point of maintenance** through delegation
1. **Validate all parameters** with appropriate error handling
1. **Use custom literals** for intuitive initialization
1. **Provide multiple convenient constructors** with delegation
