# Modern C++ for C Programmers
## Chapter 9: Bitfields and Unions

---

## Chapter Overview

**Topics Covered:**
- Bitfields for memory-efficient storage
- Anonymous unions
- Endianness and portability issues
- Creating portable bitfield implementations
- Template parameter checking
- Type traits and static assertions
- Modern alternatives to bitfields

---

## What Are Bitfields?

Bitfields allow you to specify the exact number of bits for struct/class members:

```cpp
struct StatusFlags {
    unsigned int isActive : 1;      // 1 bit
    unsigned int isVisible : 1;     // 1 bit
    unsigned int priority : 3;      // 3 bits (0-7)
    unsigned int category : 4;      // 4 bits (0-15)
    unsigned int reserved : 23;     // 23 bits
    // Total: 32 bits (4 bytes)
};
```

**Benefits:**
- Memory efficient
- Natural bit manipulation
- Self-documenting code

---

## Bitfield Memory Layout

![bitfield_memory_layout](/svg/courses/languages/c++/modern-c++-for-c-programmers/09_bitfields_unions/bitfield_memory_layout.svg)

---

## Basic Bitfield Usage

```cpp
struct NetworkPacketHeader {
    unsigned int version : 4;        // IP version (4 or 6)
    unsigned int headerLength : 4;   // Header length
    unsigned int typeOfService : 8;  // Type of service
    unsigned int totalLength : 16;   // Total packet length
};

void processPacket() {
    NetworkPacketHeader header = {};

    header.version = 4;
    header.headerLength = 5;
    header.typeOfService = 0;
    header.totalLength = 1500;

    std::cout << "Version: " << header.version << '\n';
    std::cout << "Header size: " << header.headerLength * 4 << " bytes\n";
}
```

---

## Bitfield Types and Constraints

**Allowed Types:**
- `int`, `unsigned int`
- `signed int`
- `bool`
- Enumeration types
- Implementation-defined integral types

**Constraints:**
- Cannot take address of bitfield
- Cannot create references to bitfields
- Cannot create arrays of bitfields
- Cannot use `sizeof` on bitfields

---

## Bitfield Limitations

```cpp
struct BitfieldExample {
    unsigned int flag : 1;
    unsigned int count : 7;
};

void demonstrateLimitations() {
    BitfieldExample bf;

    // These operations are NOT allowed:
    // &bf.flag;           // Cannot take address
    // int& ref = bf.flag; // Cannot create reference
    // sizeof(bf.flag);    // Cannot get size

    // These operations ARE allowed:
    bf.flag = 1;                    // Assignment
    int value = bf.flag;            // Reading
    bool isSet = (bf.flag != 0);    // Comparison
}
```

---

## Anonymous Unions

```cpp
struct Coordinate {
    union {
        struct { float x, y, z; };      // Named access
        struct { float r, g, b; };      // Color interpretation
        float data[3];                  // Array access
    };

    Coordinate(float x, float y, float z) : x(x), y(y), z(z) {}
};

void useCoordinate() {
    Coordinate point(1.0f, 2.0f, 3.0f);

    std::cout << "Position: " << point.x << ", " << point.y << ", " << point.z << '\n';
    std::cout << "Color: " << point.r << ", " << point.g << ", " << point.b << '\n';
    std::cout << "Array[0]: " << point.data[0] << '\n';
}
```

---

## Tagged Unions (Discriminated Unions)

```cpp
enum class DataType {
    Integer,
    Float,
    String
};

struct Variant {
    DataType type;

    union {
        int intValue;
        float floatValue;
        char stringValue[32];
    };

    Variant(int val) : type(DataType::Integer), intValue(val) {}
    Variant(float val) : type(DataType::Float), floatValue(val) {}
    Variant(const char* val) : type(DataType::String) {
        std::strncpy(stringValue, val, sizeof(stringValue) - 1);
        stringValue[sizeof(stringValue) - 1] = '\0';
    }
};
```

---

## Modern Alternative: std::variant

```cpp
#include <variant>
#include <string>

using ModernVariant = std::variant<int, float, std::string>;

void useModernVariant() {
    ModernVariant var = 42;

    // Type-safe access
    if (std::holds_alternative<int>(var)) {
        std::cout << "Integer: " << std::get<int>(var) << '\n';
    }

    // Visitor pattern
    std::visit([](const auto& value) {
        std::cout << "Value: " << value << '\n';
    }, var);

    // Exception-safe access
    try {
        float f = std::get<float>(var);  // Throws if wrong type
    }
    catch (const std::bad_variant_access& e) {
        std::cout << "Wrong type access\n";
    }
}
```

---

## Endianness Issues

![endianness_issues](/svg/courses/languages/c++/modern-c++-for-c-programmers/09_bitfields_unions/endianness_issues.svg)

---

## Bitfield Portability Problems

```cpp
struct ProblematicBitfield {
    unsigned int flag1 : 1;
    unsigned int flag2 : 1;
    unsigned int value : 6;
};

void demonstratePortabilityIssues() {
    ProblematicBitfield bf = {};
    bf.flag1 = 1;
    bf.value = 42;

    // Problems:
    // 1. Bit order within byte is implementation-defined
    // 2. Allocation order is implementation-defined
    // 3. Alignment and padding are implementation-defined

    // This code may behave differently on different platforms!
    unsigned char* bytes = reinterpret_cast<unsigned char*>(&bf);
    std::cout << "Byte 0: 0x" << std::hex << static_cast<int>(bytes[0]) << '\n';
}
```

---

## Detecting Endianness

```cpp
constexpr bool isLittleEndian() {
    constexpr uint32_t test = 0x01234567;
    return reinterpret_cast<const uint8_t*>(&test)[0] == 0x67;
}

constexpr bool isBigEndian() {
    return !isLittleEndian();
}

void checkEndianness() {
    if constexpr (isLittleEndian()) {
        std::cout << "System is little endian\n";
    } else {
        std::cout << "System is big endian\n";
    }
}
```

---

## Creating Portable Bitfields

```cpp
#include <cstdint>

class PortableBitfield {
private:
    uint32_t data;

public:
    // Explicit bit manipulation for portability
    void setFlag1(bool value) {
        if (value) {
            data |= 0x01;  // Set bit 0
        } else {
            data &= ~0x01; // Clear bit 0
        }
    }

    bool getFlag1() const {
        return (data & 0x01) != 0;
    }

    void setValue(uint8_t value) {
        data = (data & 0x03) | ((value & 0x3F) << 2);  // Bits 2-7
    }

    uint8_t getValue() const {
        return (data >> 2) & 0x3F;
    }
};
```

---

## Template-Based Portable Bitfield

```cpp
template<typename T, size_t Offset, size_t Width>
class BitfieldMember {
private:
    static_assert(Offset + Width <= sizeof(T) * 8, "Bitfield out of range");
    static_assert(Width > 0, "Width must be positive");

    static constexpr T mask = ((T(1) << Width) - 1) << Offset;

    T& data;

public:
    BitfieldMember(T& storage) : data(storage) {}

    BitfieldMember& operator=(T value) {
        data = (data & ~mask) | ((value << Offset) & mask);
        return *this;
    }

    operator T() const {
        return (data & mask) >> Offset;
    }
};
```

---

## Using Template Bitfield

```cpp
class NetworkHeader {
private:
    uint32_t headerData = 0;

public:
    BitfieldMember<uint32_t, 0, 4> version{headerData};
    BitfieldMember<uint32_t, 4, 4> headerLength{headerData};
    BitfieldMember<uint32_t, 8, 8> typeOfService{headerData};
    BitfieldMember<uint32_t, 16, 16> totalLength{headerData};

    void serialize(std::ostream& out) const {
        uint32_t networkOrder = htonl(headerData);
        out.write(reinterpret_cast<const char*>(&networkOrder), sizeof(networkOrder));
    }
};

void useNetworkHeader() {
    NetworkHeader header;
    header.version = 4;
    header.headerLength = 5;
    header.totalLength = 1500;
}
```

---

## Template Parameter Checking

```cpp
template<typename T>
constexpr bool is_integral_v = std::is_integral<T>::value;

template<typename T>
constexpr bool is_unsigned_v = std::is_unsigned<T>::value;

template<typename T, size_t Bits>
class CheckedBitfield {
    static_assert(is_integral_v<T>, "T must be an integral type");
    static_assert(is_unsigned_v<T>, "T must be unsigned for bitfields");
    static_assert(Bits <= sizeof(T) * 8, "Too many bits for type T");
    static_assert(Bits > 0, "Must have at least one bit");

    T data : Bits;

public:
    CheckedBitfield() : data(0) {}
    CheckedBitfield(T value) : data(value) {}

    operator T() const { return data; }
    CheckedBitfield& operator=(T value) {
        data = value;
        return *this;
    }
};
```

---

## Type Traits for Bitfields

```cpp
#include <type_traits>

// Check if type is suitable for bitfields
template<typename T>
struct is_bitfield_compatible {
    static constexpr bool value =
        std::is_integral_v<T> &&
        !std::is_same_v<T, bool> &&  // bool has special rules
        sizeof(T) <= sizeof(unsigned long long);
};

template<typename T>
constexpr bool is_bitfield_compatible_v = is_bitfield_compatible<T>::value;

// Check if value fits in specified bits
template<typename T, size_t Bits>
constexpr bool value_fits_in_bits(T value) {
    if constexpr (std::is_signed_v<T>) {
        constexpr T max_val = (T(1) << (Bits - 1)) - 1;
        constexpr T min_val = -(T(1) << (Bits - 1));
        return value >= min_val && value <= max_val;
    } else {
        constexpr T max_val = (T(1) << Bits) - 1;
        return value <= max_val;
    }
}
```

---

## Static Assertions

```cpp
template<typename T, size_t Bits>
class ValidatedBitfield {
    // Compile-time validation
    static_assert(is_bitfield_compatible_v<T>,
                  "Type not suitable for bitfields");
    static_assert(Bits > 0,
                  "Bitfield must have at least one bit");
    static_assert(Bits <= sizeof(T) * 8,
                  "Too many bits for the specified type");

private:
    T value : Bits;

public:
    explicit ValidatedBitfield(T val = 0) {
        static_assert(value_fits_in_bits<T, Bits>(0),
                      "Default value validation");
        value = val;
    }

    void set(T val) {
        // Runtime validation for dynamic values
        if (!value_fits_in_bits<T, Bits>(val)) {
            throw std::out_of_range("Value doesn't fit in bitfield");
        }
        value = val;
    }

    T get() const { return value; }
};
```

---

## Advanced Static Assertions

```cpp
// Custom assertion messages
#define STATIC_ASSERT_MSG(condition, message) \
    static_assert(condition, message)

template<size_t N>
struct ensure_power_of_two {
    STATIC_ASSERT_MSG((N & (N - 1)) == 0 && N > 0,
                      "Size must be a power of two");
    static constexpr size_t value = N;
};

template<typename T>
class AlignedBitfield {
    // Ensure proper alignment
    STATIC_ASSERT_MSG(alignof(T) >= sizeof(T),
                      "Type must be naturally aligned");
    STATIC_ASSERT_MSG(std::is_trivially_copyable_v<T>,
                      "Type must be trivially copyable");

    T data;

public:
    static constexpr size_t alignment = alignof(T);
    static constexpr size_t size = sizeof(T);
};
```

---

## Bitfield Performance Considerations

```cpp
// Efficient bitfield operations
class OptimizedFlags {
private:
    uint32_t flags = 0;

public:
    // Batch operations are more efficient
    void setFlags(uint32_t mask, bool value) {
        if (value) {
            flags |= mask;   // Set multiple bits
        } else {
            flags &= ~mask;  // Clear multiple bits
        }
    }

    bool testFlags(uint32_t mask) const {
        return (flags & mask) == mask;  // Test multiple bits
    }

    // Single bit operations
    void setFlag(size_t bit) { flags |= (1u << bit); }
    void clearFlag(size_t bit) { flags &= ~(1u << bit); }
    bool testFlag(size_t bit) const { return flags & (1u << bit); }
    void toggleFlag(size_t bit) { flags ^= (1u << bit); }
};
```

---

## Bitwise Operations Reference

![bitwise_operations_reference](/svg/courses/languages/c++/modern-c++-for-c-programmers/09_bitfields_unions/bitwise_operations_reference.svg)

---

## Bit Manipulation Examples

```cpp
class BitManipulation {
public:
    // Set the nth bit
    static uint32_t setBit(uint32_t value, int n) {
        return value | (1u << n);
    }

    // Clear the nth bit
    static uint32_t clearBit(uint32_t value, int n) {
        return value & ~(1u << n);
    }

    // Toggle the nth bit
    static uint32_t toggleBit(uint32_t value, int n) {
        return value ^ (1u << n);
    }

    // Test the nth bit
    static bool testBit(uint32_t value, int n) {
        return (value & (1u << n)) != 0;
    }

    // Count set bits (population count)
    static int popCount(uint32_t value) {
        return __builtin_popcount(value);  // GCC/Clang builtin
    }
};
```

---

## Modern Bit Manipulation

```cpp
#include <bit>  // C++20

void modernBitOps() {
    uint32_t value = 0b10110100;

    // C++20 bit operations
    auto count = std::popcount(value);           // Count set bits
    auto leading = std::countl_zero(value);      // Leading zeros
    auto trailing = std::countr_zero(value);     // Trailing zeros

    // Bit rotation
    auto rotated_left = std::rotl(value, 3);     // Rotate left
    auto rotated_right = std::rotr(value, 3);    // Rotate right

    // Power of 2 operations
    bool is_pow2 = std::has_single_bit(value);   // Is power of 2?
    auto next_pow2 = std::bit_ceil(value);       // Next power of 2
    auto prev_pow2 = std::bit_floor(value);      // Previous power of 2

    std::cout << "Count: " << count << '\n';
    std::cout << "Is power of 2: " << is_pow2 << '\n';
}
```

---

## Endian-Safe Serialization

```cpp
#include <bit>

class EndianSafeSerializer {
public:
    template<typename T>
    static void writeValue(std::ostream& out, T value) {
        static_assert(std::is_trivially_copyable_v<T>);

        if constexpr (std::endian::native == std::endian::little) {
            // Convert to big endian for network byte order
            value = byteSwap(value);
        }

        out.write(reinterpret_cast<const char*>(&value), sizeof(value));
    }

    template<typename T>
    static T readValue(std::istream& in) {
        T value;
        in.read(reinterpret_cast<char*>(&value), sizeof(value));

        if constexpr (std::endian::native == std::endian::little) {
            value = byteSwap(value);
        }

        return value;
    }

private:
    template<typename T>
    static T byteSwap(T value) {
        if constexpr (sizeof(T) == 2) {
            return __builtin_bswap16(value);
        } else if constexpr (sizeof(T) == 4) {
            return __builtin_bswap32(value);
        } else if constexpr (sizeof(T) == 8) {
            return __builtin_bswap64(value);
        }
        return value;
    }
};
```

---

## Union with Constructors (C++11+)

```cpp
union ModernUnion {
    int intValue;
    float floatValue;
    std::string stringValue;  // Non-trivial type allowed in C++11+

    ModernUnion() : intValue(0) {}

    ModernUnion(int i) : intValue(i) {}
    ModernUnion(float f) : floatValue(f) {}
    ModernUnion(const std::string& s) : stringValue(s) {}

    // Must provide destructor when non-trivial types are present
    ~ModernUnion() {
        // Need to know which member is active!
        // This is why std::variant is preferred
    }
};
```

---

## Bitfield Alternatives: std::bitset

```cpp
#include <bitset>

void useBitset() {
    std::bitset<32> flags;

    // Set individual bits
    flags[0] = true;    // Set bit 0
    flags[5] = true;    // Set bit 5

    // Bitwise operations
    flags |= 0b1100;    // Set bits 2 and 3
    flags &= 0xFF;      // Mask to lower 8 bits

    // Query operations
    bool isSet = flags[0];
    size_t count = flags.count();    // Number of set bits
    bool any = flags.any();          // Any bits set?
    bool all = flags.all();          // All bits set?

    // String conversion
    std::string str = flags.to_string();
    unsigned long val = flags.to_ulong();

    std::cout << "Flags: " << flags << '\n';
    std::cout << "Count: " << count << '\n';
}
```

---

## Packed Structures

```cpp
// Force tight packing (compiler-specific)
#pragma pack(push, 1)
struct PackedStruct {
    uint8_t  byte1;      // 1 byte
    uint32_t dword;      // 4 bytes
    uint16_t word;       // 2 bytes
    uint8_t  byte2;      // 1 byte
    // Total: 8 bytes (no padding)
};
#pragma pack(pop)

// Portable alternative using alignas
struct alignas(1) PortablePackedStruct {
    uint8_t  byte1;
    uint32_t dword;
    uint16_t word;
    uint8_t  byte2;
};

static_assert(sizeof(PackedStruct) == 8);
static_assert(sizeof(PortablePackedStruct) == 8);
```

---

## Memory-Mapped I/O with Bitfields

```cpp
// Memory-mapped hardware register
struct volatile HardwareRegister {
    volatile unsigned int enable : 1;
    volatile unsigned int mode : 3;
    volatile unsigned int status : 4;
    volatile unsigned int reserved : 24;
};

class HardwareController {
private:
    HardwareRegister* reg;

public:
    HardwareController(void* address)
        : reg(static_cast<HardwareRegister*>(address)) {}

    void enable() {
        reg->enable = 1;
    }

    void setMode(unsigned int mode) {
        if (mode < 8) {  // 3 bits = max value 7
            reg->mode = mode;
        }
    }

    unsigned int getStatus() const {
        return reg->status;
    }
};
```

---

## Best Practices for Bitfields

**Do:**
- Use for space-critical applications
- Document bit layouts clearly
- Consider endianness for serialization
- Use template validation
- Prefer standard integers for bitfield types

**Don't:**
- Rely on implementation-defined behavior
- Mix signed and unsigned bitfields
- Use for performance-critical bit manipulation
- Take addresses of bitfield members
- Assume specific memory layout

---

## Performance Comparison

```cpp
#include <chrono>

void performanceTest() {
    const size_t iterations = 10000000;

    // Bitfield test
    struct BitfieldStruct {
        unsigned int flag : 1;
        unsigned int value : 7;
    } bf = {};

    auto start = std::chrono::high_resolution_clock::now();
    for (size_t i = 0; i < iterations; ++i) {
        bf.flag = i & 1;
        bf.value = i & 0x7F;
    }
    auto bitfield_time = std::chrono::high_resolution_clock::now() - start;

    // Manual bit manipulation test
    uint8_t manual = 0;
    start = std::chrono::high_resolution_clock::now();
    for (size_t i = 0; i < iterations; ++i) {
        manual = (manual & 0x01) | ((i & 0x7F) << 1);
    }
    auto manual_time = std::chrono::high_resolution_clock::now() - start;

    std::cout << "Bitfield: " << bitfield_time.count() << "ns\n";
    std::cout << "Manual: " << manual_time.count() << "ns\n";
}
```

---

## Modern Alternatives Summary

**Instead of traditional bitfields, consider:**

```cpp
// 1. std::bitset for flag collections
std::bitset<32> flags;

// 2. std::variant for discriminated unions
std::variant<int, float, std::string> value;

// 3. Template-based type-safe bitfields
BitfieldMember<uint32_t, 0, 8> field;

// 4. Bit manipulation functions
constexpr uint32_t setBits(uint32_t value, uint32_t mask) {
    return value | mask;
}

// 5. Scoped enums for flags
enum class FilePermissions : uint32_t {
    None = 0,
    Read = 1 << 0,
    Write = 1 << 1,
    Execute = 1 << 2,
    All = Read | Write | Execute
};

// Enable bitwise operations
FilePermissions operator|(FilePermissions a, FilePermissions b) {
    return static_cast<FilePermissions>(
        static_cast<uint32_t>(a) | static_cast<uint32_t>(b)
    );
}
```

---

## Type-Safe Flag Enums

```cpp
template<typename Enum>
class Flags {
private:
    using underlying_type = std::underlying_type_t<Enum>;
    underlying_type value;

public:
    constexpr Flags() : value(0) {}
    constexpr Flags(Enum e) : value(static_cast<underlying_type>(e)) {}

    constexpr Flags operator|(Flags other) const {
        return Flags(static_cast<Enum>(value | other.value));
    }

    constexpr Flags operator&(Flags other) const {
        return Flags(static_cast<Enum>(value & other.value));
    }

    constexpr bool test(Enum flag) const {
        return (value & static_cast<underlying_type>(flag)) != 0;
    }

    constexpr void set(Enum flag) {
        value |= static_cast<underlying_type>(flag);
    }

    constexpr void clear(Enum flag) {
        value &= ~static_cast<underlying_type>(flag);
    }
};

using FileFlags = Flags<FilePermissions>;
```

---

## Bit Field Register Template

```cpp
template<typename T, T Address>
class MemoryMappedRegister {
private:
    volatile T* const reg_ptr = reinterpret_cast<volatile T*>(Address);

public:
    // Read the entire register
    T read() const {
        return *reg_ptr;
    }

    // Write the entire register
    void write(T value) {
        *reg_ptr = value;
    }

    // Read specific bits
    template<size_t Offset, size_t Width>
    T readField() const {
        static_assert(Offset + Width <= sizeof(T) * 8);
        constexpr T mask = ((T(1) << Width) - 1) << Offset;
        return (*reg_ptr & mask) >> Offset;
    }

    // Write specific bits
    template<size_t Offset, size_t Width>
    void writeField(T value) {
        static_assert(Offset + Width <= sizeof(T) * 8);
        constexpr T mask = ((T(1) << Width) - 1) << Offset;
        T current = *reg_ptr;
        *reg_ptr = (current & ~mask) | ((value << Offset) & mask);
    }

    // Set specific bits
    template<size_t Offset, size_t Width>
    void setBits() {
        constexpr T mask = ((T(1) << Width) - 1) << Offset;
        *reg_ptr |= mask;
    }

    // Clear specific bits
    template<size_t Offset, size_t Width>
    void clearBits() {
        constexpr T mask = ((T(1) << Width) - 1) << Offset;
        *reg_ptr &= ~mask;
    }
};
```

---

## Hardware Register Example

```cpp
// Define hardware registers
constexpr uint32_t CONTROL_REG_ADDR = 0x40000000;
constexpr uint32_t STATUS_REG_ADDR  = 0x40000004;

using ControlRegister = MemoryMappedRegister<uint32_t, CONTROL_REG_ADDR>;
using StatusRegister = MemoryMappedRegister<uint32_t, STATUS_REG_ADDR>;

class HardwareDevice {
private:
    ControlRegister control;
    StatusRegister status;

public:
    void initialize() {
        // Set enable bit (bit 0)
        control.setBits<0, 1>();

        // Set mode to 3 (bits 1-3)
        control.writeField<1, 3>(3);

        // Clear interrupt flag (bit 7)
        control.clearBits<7, 1>();
    }

    bool isReady() const {
        // Check ready bit (bit 0) in status register
        return status.readField<0, 1>() != 0;
    }

    uint8_t getErrorCode() const {
        // Read error code (bits 8-15) from status register
        return static_cast<uint8_t>(status.readField<8, 8>());
    }
};
```

---

## Compile-Time Bit Manipulation

```cpp
template<typename T>
class constexpr_bitfield {
private:
    T data = 0;

public:
    constexpr constexpr_bitfield() = default;
    constexpr constexpr_bitfield(T value) : data(value) {}

    template<size_t Offset, size_t Width>
    constexpr T get() const {
        static_assert(Offset + Width <= sizeof(T) * 8);
        constexpr T mask = ((T(1) << Width) - 1);
        return (data >> Offset) & mask;
    }

    template<size_t Offset, size_t Width>
    constexpr constexpr_bitfield set(T value) const {
        static_assert(Offset + Width <= sizeof(T) * 8);
        constexpr T mask = ((T(1) << Width) - 1) << Offset;
        return constexpr_bitfield((data & ~mask) | ((value << Offset) & mask));
    }

    constexpr T value() const { return data; }
};

// Compile-time usage
constexpr auto config = constexpr_bitfield<uint32_t>()
    .set<0, 1>(1)    // Enable bit
    .set<1, 3>(5)    // Mode = 5
    .set<8, 8>(42);  // Value = 42

static_assert(config.get<0, 1>() == 1);
static_assert(config.get<1, 3>() == 5);
static_assert(config.get<8, 8>() == 42);
```

---

## Cross-Platform Serialization

```cpp
#include <array>

class CrossPlatformBitfield {
private:
    std::array<uint8_t, 4> bytes = {};

public:
    // Platform-independent bit access
    void setBit(size_t bit, bool value) {
        if (bit >= 32) return;

        size_t byte_index = bit / 8;
        size_t bit_index = bit % 8;

        if (value) {
            bytes[byte_index] |= (1u << bit_index);
        } else {
            bytes[byte_index] &= ~(1u << bit_index);
        }
    }

    bool getBit(size_t bit) const {
        if (bit >= 32) return false;

        size_t byte_index = bit / 8;
        size_t bit_index = bit % 8;

        return (bytes[byte_index] & (1u << bit_index)) != 0;
    }

    void setField(size_t offset, size_t width, uint32_t value) {
        // Clear existing bits
        for (size_t i = 0; i < width; ++i) {
            setBit(offset + i, false);
        }

        // Set new bits
        for (size_t i = 0; i < width; ++i) {
            setBit(offset + i, (value & (1u << i)) != 0);
        }
    }

    uint32_t getField(size_t offset, size_t width) const {
        uint32_t result = 0;
        for (size_t i = 0; i < width; ++i) {
            if (getBit(offset + i)) {
                result |= (1u << i);
            }
        }
        return result;
    }

    // Serialization
    const std::array<uint8_t, 4>& toBytes() const { return bytes; }
    void fromBytes(const std::array<uint8_t, 4>& data) { bytes = data; }
};
```

---

## SIMD-Friendly Bit Operations

```cpp
#include <immintrin.h>  // Intel intrinsics

class SIMDBitOperations {
public:
    // Parallel bit count using SIMD
    static std::array<int, 4> parallelPopcount(const std::array<uint32_t, 4>& values) {
        __m128i vec = _mm_loadu_si128(reinterpret_cast<const __m128i*>(values.data()));

        std::array<int, 4> result;
        for (int i = 0; i < 4; ++i) {
            result[i] = _mm_popcnt_u32(values[i]);
        }

        return result;
    }

    // Parallel bit reversal
    static std::array<uint32_t, 4> parallelBitReverse(const std::array<uint32_t, 4>& values) {
        std::array<uint32_t, 4> result;

        for (int i = 0; i < 4; ++i) {
            uint32_t val = values[i];
            // Bit reversal algorithm
            val = ((val & 0xAAAAAAAA) >> 1) | ((val & 0x55555555) << 1);
            val = ((val & 0xCCCCCCCC) >> 2) | ((val & 0x33333333) << 2);
            val = ((val & 0xF0F0F0F0) >> 4) | ((val & 0x0F0F0F0F) << 4);
            val = ((val & 0xFF00FF00) >> 8) | ((val & 0x00FF00FF) << 8);
            val = (val >> 16) | (val << 16);
            result[i] = val;
        }

        return result;
    }
};
```

---

## Union with Smart Pointer Management

```cpp
#include <memory>
#include <typeinfo>

class TypeSafeUnion {
private:
    enum class Type { Int, Float, String, None } type = Type::None;

    union Storage {
        int intValue;
        float floatValue;
        std::unique_ptr<std::string> stringPtr;

        Storage() {}
        ~Storage() {}
    } storage;

public:
    TypeSafeUnion() = default;

    TypeSafeUnion(int value) : type(Type::Int) {
        storage.intValue = value;
    }

    TypeSafeUnion(float value) : type(Type::Float) {
        storage.floatValue = value;
    }

    TypeSafeUnion(const std::string& value) : type(Type::String) {
        new(&storage.stringPtr) std::unique_ptr<std::string>(
            std::make_unique<std::string>(value)
        );
    }

    ~TypeSafeUnion() {
        clear();
    }

    TypeSafeUnion(const TypeSafeUnion& other) {
        *this = other;
    }

    TypeSafeUnion& operator=(const TypeSafeUnion& other) {
        if (this != &other) {
            clear();
            type = other.type;

            switch (type) {
                case Type::Int:
                    storage.intValue = other.storage.intValue;
                    break;
                case Type::Float:
                    storage.floatValue = other.storage.floatValue;
                    break;
                case Type::String:
                    new(&storage.stringPtr) std::unique_ptr<std::string>(
                        std::make_unique<std::string>(*other.storage.stringPtr)
                    );
                    break;
                case Type::None:
                    break;
            }
        }
        return *this;
    }

private:
    void clear() {
        if (type == Type::String) {
            storage.stringPtr.~unique_ptr();
        }
        type = Type::None;
    }

public:
    template<typename T>
    T get() const {
        if constexpr (std::is_same_v<T, int>) {
            if (type != Type::Int) throw std::bad_cast();
            return storage.intValue;
        } else if constexpr (std::is_same_v<T, float>) {
            if (type != Type::Float) throw std::bad_cast();
            return storage.floatValue;
        } else if constexpr (std::is_same_v<T, std::string>) {
            if (type != Type::String) throw std::bad_cast();
            return *storage.stringPtr;
        }
    }
};
```

---

## Bit-Packed Data Structures

```cpp
// Compact representation of date
class PackedDate {
private:
    uint32_t data;  // year(12) + month(4) + day(5) + padding(11) = 32 bits

public:
    PackedDate(uint16_t year, uint8_t month, uint8_t day) {
        data = 0;
        setYear(year);
        setMonth(month);
        setDay(day);
    }

    uint16_t getYear() const { return (data >> 20) & 0xFFF; }    // 12 bits
    uint8_t getMonth() const { return (data >> 16) & 0xF; }     // 4 bits
    uint8_t getDay() const { return (data >> 11) & 0x1F; }      // 5 bits

    void setYear(uint16_t year) {
        if (year > 4095) throw std::out_of_range("Year too large");
        data = (data & 0x000FFFFF) | ((uint32_t(year) & 0xFFF) << 20);
    }

    void setMonth(uint8_t month) {
        if (month == 0 || month > 12) throw std::out_of_range("Invalid month");
        data = (data & 0xFFF0FFFF) | ((uint32_t(month) & 0xF) << 16);
    }

    void setDay(uint8_t day) {
        if (day == 0 || day > 31) throw std::out_of_range("Invalid day");
        data = (data & 0xFFFF07FF) | ((uint32_t(day) & 0x1F) << 11);
    }

    // Efficient comparison
    bool operator<(const PackedDate& other) const {
        return data < other.data;
    }

    bool operator==(const PackedDate& other) const {
        return (data & 0xFFFFF800) == (other.data & 0xFFFFF800);
    }
};
```

---

## Debugging Bitfields

```cpp
class DebuggableBitfield {
private:
    uint32_t data = 0;

public:
    void dump() const {
        std::cout << "Bitfield value: 0x" << std::hex << data << std::dec << '\n';
        std::cout << "Binary: ";
        for (int i = 31; i >= 0; --i) {
            std::cout << ((data >> i) & 1);
            if (i % 4 == 0) std::cout << ' ';
        }
        std::cout << '\n';
    }

    void dumpField(const std::string& name, size_t offset, size_t width) const {
        uint32_t mask = ((1u << width) - 1) << offset;
        uint32_t value = (data & mask) >> offset;

        std::cout << name << ": " << value
                  << " (bits " << offset << "-" << (offset + width - 1) << ")\n";
    }

    // Test specific bit patterns
    bool matchesPattern(uint32_t pattern, uint32_t mask) const {
        return (data & mask) == (pattern & mask);
    }
};

// Usage
void debugExample() {
    DebuggableBitfield bf;
    // ... set some fields ...

    bf.dump();
    bf.dumpField("Enable", 0, 1);
    bf.dumpField("Mode", 1, 3);
    bf.dumpField("Priority", 4, 4);

    // Check for specific patterns
    if (bf.matchesPattern(0x1, 0x1)) {
        std::cout << "Device is enabled\n";
    }
}
```

---

## Summary

**Bitfields and Unions in Modern C++:**

- **Bitfields**: Memory-efficient for flags and small values
- **Unions**: Type-unsafe but memory-efficient alternatives
- **Portability**: Major concern across platforms
- **Modern alternatives**: `std::variant`, `std::bitset`, template solutions

**Best Practices:**
- Use standard alternatives when possible
- Consider endianness for serialization
- Validate with static assertions
- Document bit layouts clearly
- Test on target platforms

**Performance**: Good for memory, consider CPU cache effects

**Modern C++**: Provides better type-safe alternatives to traditional bitfields and unions.
