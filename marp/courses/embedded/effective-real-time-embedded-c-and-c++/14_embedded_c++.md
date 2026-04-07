# Embedded C++

---

## Chapter Overview

1. C vs C++ in embedded systems
1. Benefits of embedded C++ (EC++)
1. Restrictions and guidelines
1. Memory and performance considerations
1. Best practices for embedded C++

---

## Why C++ in Embedded?

![why_c_in_embedded](svg/courses/embedded/effective-real-time-embedded-c-and-c++/14_embedded_c++/why_c_in_embedded.svg)

---

## C vs C++ Comparison

```cpp
// C approach
typedef struct {
    uint8_t* buffer;
    size_t size;
    size_t head;
    size_t tail;
} circular_buffer_t;

void cb_init(circular_buffer_t* cb, uint8_t* buf, size_t size);
bool cb_push(circular_buffer_t* cb, uint8_t data);
bool cb_pop(circular_buffer_t* cb, uint8_t* data);

// C++ approach
template<size_t SIZE>
class CircularBuffer {
private:
    uint8_t buffer[SIZE];
    size_t head{0};
    size_t tail{0};

public:
    constexpr size_t capacity() const { return SIZE; }
    bool push(uint8_t data);
    bool pop(uint8_t& data);
};
```

---

## Embedded C++ (EC++) Standard

Key restrictions for embedded use:
1. **No exceptions** - too much overhead
1. **No RTTI** - runtime type information
1. **Limited STL** - avoid dynamic allocation
1. **No multiple inheritance** - complexity
1. **Careful with templates** - code bloat

---

## Zero-Cost Abstractions

```cpp
// C++ pin abstraction with zero overhead
template<uint32_t PORT, uint16_t PIN>
class Pin {
public:
    static void setOutput() {
        reinterpret_cast<GPIO_TypeDef*>(PORT)->MODER |= (1 << (PIN * 2));
    }

    static void high() {
        reinterpret_cast<GPIO_TypeDef*>(PORT)->BSRR = (1 << PIN);
    }

    static void low() {
        reinterpret_cast<GPIO_TypeDef*>(PORT)->BSRR = (1 << (PIN + 16));
    }

    static bool read() {
        return reinterpret_cast<GPIO_TypeDef*>(PORT)->IDR & (1 << PIN);
    }
};

// Usage - all resolved at compile time
using LedPin = Pin<GPIOA_BASE, 5>;
LedPin::setOutput();
LedPin::high();
```

---

## Compile-Time Configuration

```cpp
// Template-based configuration
template<typename Config>
class Uart {
private:
    static constexpr auto uart = Config::uart;
    static constexpr auto baudrate = Config::baudrate;

public:
    static void init() {
        uart->CR1 = 0;
        uart->BRR = SystemCoreClock / baudrate;
        uart->CR1 = USART_CR1_TE | USART_CR1_RE | USART_CR1_UE;
    }

    static void send(uint8_t data) {
        while (!(uart->SR & USART_SR_TXE));
        uart->DR = data;
    }
};

// Configuration
struct UartConfig {
    static constexpr auto uart = USART1;
    static constexpr uint32_t baudrate = 115200;
};

using Serial = Uart<UartConfig>;
```

---

## Constexpr for Compile-Time

```cpp
// Compile-time calculations
template<uint32_t FREQ, uint32_t BAUD>
class BaudRateCalculator {
public:
    static constexpr uint32_t calculate() {
        return (FREQ + BAUD / 2) / BAUD;
    }

    static_assert(calculate() <= 0xFFFF, "Baud rate divider too large");
    static constexpr uint16_t value = calculate();
};

// Timer period calculation
template<uint32_t CLOCK_HZ, uint32_t PERIOD_US>
constexpr uint32_t calculateTimerPeriod() {
    constexpr uint32_t period = (CLOCK_HZ / 1'000'000) * PERIOD_US;
    static_assert(period > 0 && period <= 0xFFFF, "Invalid timer period");
    return period;
}

// Usage
constexpr auto TIMER_PERIOD = calculateTimerPeriod<84'000'000, 100>();
```

---

## RAII for Resource Management

```cpp
// Automatic resource management
class InterruptLock {
private:
    uint32_t primask;

public:
    InterruptLock() : primask(__get_PRIMASK()) {
        __disable_irq();
    }

    ~InterruptLock() {
        __set_PRIMASK(primask);
    }

    // Prevent copying
    InterruptLock(const InterruptLock&) = delete;
    InterruptLock& operator=(const InterruptLock&) = delete;
};

// Usage - automatically restored on scope exit
void criticalOperation() {
    InterruptLock lock;  // Interrupts disabled

    // Critical section
    modifySharedData();

}  // Interrupts automatically restored
```

---

## Static Polymorphism

```cpp
// CRTP - Curiously Recurring Template Pattern
template<typename Derived>
class Device {
public:
    void process() {
        static_cast<Derived*>(this)->processImpl();
    }

    void init() {
        static_cast<Derived*>(this)->initImpl();
    }
};

class Sensor : public Device<Sensor> {
public:
    void processImpl() {
        // Sensor-specific processing
        value = readAdc();
    }

    void initImpl() {
        // Sensor initialization
        configureAdc();
    }

private:
    uint16_t value;
};

// No virtual functions - all resolved at compile time
```

---

## Enum Classes for Type Safety

```cpp
// Type-safe enumerations
enum class GpioMode : uint8_t {
    Input = 0,
    Output = 1,
    Alternate = 2,
    Analog = 3
};

enum class PullType : uint8_t {
    None = 0,
    Up = 1,
    Down = 2
};

class Gpio {
public:
    static void setMode(GPIO_TypeDef* port, uint8_t pin,
                       GpioMode mode, PullType pull = PullType::None) {
        uint32_t modeVal = static_cast<uint32_t>(mode);
        uint32_t pullVal = static_cast<uint32_t>(pull);

        port->MODER &= ~(3U << (pin * 2));
        port->MODER |= (modeVal << (pin * 2));

        port->PUPDR &= ~(3U << (pin * 2));
        port->PUPDR |= (pullVal << (pin * 2));
    }
};

// Usage - type safe
Gpio::setMode(GPIOA, 5, GpioMode::Output);
// Gpio::setMode(GPIOA, 5, PullType::Up);  // Compile error!
```

---

## Inline Functions

```cpp
// Force inline for performance
class FastMath {
public:
    // Always inline
    [[gnu::always_inline]]
    static inline int32_t abs(int32_t x) {
        return (x ^ (x >> 31)) - (x >> 31);
    }

    // Compiler decides
    inline static uint32_t min(uint32_t a, uint32_t b) {
        return (a < b) ? a : b;
    }

    // Template automatically inline
    template<typename T>
    static T clamp(T value, T min, T max) {
        return (value < min) ? min : (value > max) ? max : value;
    }
};
```

---

## Placement New

```cpp
// Static memory allocation with constructors
template<typename T, size_t N>
class StaticPool {
private:
    alignas(T) uint8_t storage[N * sizeof(T)];
    T* objects[N];
    size_t allocated{0};

public:
    template<typename... Args>
    T* create(Args&&... args) {
        if (allocated >= N) return nullptr;

        void* ptr = &storage[allocated * sizeof(T)];
        T* obj = new(ptr) T(std::forward<Args>(args)...);
        objects[allocated++] = obj;

        return obj;
    }

    void destroy(T* obj) {
        obj->~T();  // Call destructor
        // Memory remains allocated in pool
    }
};

// Usage
StaticPool<Sensor, 10> sensorPool;
Sensor* s1 = sensorPool.create(ADC1, 0);
```

---

## Const Correctness

```cpp
class SensorData {
private:
    mutable uint32_t accessCount{0};
    float value;

public:
    // Const member function
    float getValue() const {
        accessCount++;  // Allowed due to mutable
        return value;
    }

    // Non-const member function
    void setValue(float v) {
        value = v;
    }

    // Return const reference
    const float& getValueRef() const {
        return value;
    }
};

// Const object
void processData(const SensorData& data) {
    float v = data.getValue();      // OK
    // data.setValue(10.0f);        // Error - const object
}
```

---

## Compile-Time Assertions

```cpp
// Static assertions for safety
template<typename T, size_t SIZE>
class Buffer {
    static_assert(SIZE > 0, "Buffer size must be greater than 0");
    static_assert(SIZE <= 1024, "Buffer size too large");
    static_assert(std::is_trivially_copyable_v<T>,
                  "Buffer type must be trivially copyable");

private:
    T data[SIZE];

public:
    constexpr size_t size() const { return SIZE; }
};

// Alignment checks
template<typename T>
class AlignedStorage {
    static_assert(alignof(T) <= 16, "Type alignment too large");
    alignas(16) T storage;
};
```

---

## Avoiding Dynamic Memory

```cpp
// Stack-based alternatives
template<size_t N>
class FixedString {
private:
    char data[N];
    size_t len{0};

public:
    FixedString() = default;

    FixedString(const char* str) {
        size_t i = 0;
        while (str[i] && i < N - 1) {
            data[i] = str[i];
            i++;
        }
        data[i] = '\0';
        len = i;
    }

    const char* c_str() const { return data; }
    size_t length() const { return len; }
};

// Usage - no heap allocation
FixedString<32> deviceName("Temperature Sensor");
```

---

## Reference vs Pointer

```cpp
// Prefer references for non-null parameters
class Device {
private:
    Uart& uart;  // Must be initialized, cannot be null
    Spi* spi;    // Optional, can be null

public:
    // Reference in constructor ensures non-null
    explicit Device(Uart& u, Spi* s = nullptr)
        : uart(u), spi(s) {}

    void sendData(const uint8_t& data) {
        uart.send(data);  // No null check needed

        if (spi) {        // Null check required
            spi->send(data);
        }
    }
};
```

---

## Namespace Organization

```cpp
// Organize code with namespaces
namespace HAL {
    namespace GPIO {
        void init(GPIO_TypeDef* port);
        void setPin(GPIO_TypeDef* port, uint8_t pin);
    }

    namespace UART {
        void init(USART_TypeDef* uart, uint32_t baud);
        void send(USART_TypeDef* uart, uint8_t data);
    }
}

// Avoid using namespace in headers
// In source files:
using namespace HAL::GPIO;  // OK in .cpp file

// Or use specific items
using HAL::UART::send;
```

---

## Function Objects

```cpp
// Lightweight function objects
template<typename T>
struct Less {
    constexpr bool operator()(const T& a, const T& b) const {
        return a < b;
    }
};

template<typename T, typename Compare = Less<T>>
class PriorityQueue {
private:
    T data[16];
    size_t count{0};
    Compare comp;

public:
    void push(const T& item) {
        // Use comparison function object
        size_t i = count;
        while (i > 0 && comp(data[(i-1)/2], item)) {
            data[i] = data[(i-1)/2];
            i = (i-1)/2;
        }
        data[i] = item;
        count++;
    }
};
```

---

## Bit Manipulation Classes

```cpp
// Type-safe bit manipulation
template<typename T, size_t POS, size_t LEN = 1>
class BitField {
private:
    T& reg;

public:
    explicit BitField(T& r) : reg(r) {}

    BitField& operator=(T value) {
        constexpr T mask = ((1U << LEN) - 1) << POS;
        reg = (reg & ~mask) | ((value << POS) & mask);
        return *this;
    }

    operator T() const {
        constexpr T mask = ((1U << LEN) - 1);
        return (reg >> POS) & mask;
    }
};

// Usage
struct TimerRegs {
    uint32_t CR1;
    uint32_t CR2;
};

BitField<uint32_t, 0, 1> enable(timer->CR1);    // Bit 0
BitField<uint32_t, 4, 2> mode(timer->CR1);      // Bits 4-5

enable = 1;        // Set bit 0
mode = 0b10;       // Set bits 4-5 to 10
```

---

## Avoiding Exceptions

```cpp
// Error handling without exceptions
template<typename T>
class Result {
private:
    union {
        T value;
        uint8_t dummy;  // For default construction
    };
    bool hasValue;

public:
    Result() : dummy{}, hasValue(false) {}
    Result(const T& v) : value(v), hasValue(true) {}

    bool isValid() const { return hasValue; }

    T& operator*() { return value; }
    const T& operator*() const { return value; }

    T* operator->() { return &value; }
    const T* operator->() const { return &value; }
};

// Usage
Result<int> divide(int a, int b) {
    if (b == 0) return {};  // Invalid result
    return a / b;
}

auto result = divide(10, 2);
if (result.isValid()) {
    int value = *result;
}
```

---

## Code Size Optimization

```cpp
// Minimize template instantiations
// Base class with non-template code
class UartBase {
protected:
    USART_TypeDef* uart;

    void sendByte(uint8_t data) {
        while (!(uart->SR & USART_SR_TXE));
        uart->DR = data;
    }

public:
    explicit UartBase(USART_TypeDef* u) : uart(u) {}
};

// Template class only for type-specific parts
template<typename T>
class TypedUart : public UartBase {
public:
    using UartBase::UartBase;

    void send(const T& data) {
        const uint8_t* bytes = reinterpret_cast<const uint8_t*>(&data);
        for (size_t i = 0; i < sizeof(T); ++i) {
            sendByte(bytes[i]);
        }
    }
};
```

---

## Link-Time Optimization

```cpp
// Help compiler optimize across translation units
// In header:
class Device {
public:
    void process();

    // Inline simple getters
    [[nodiscard]] inline uint32_t getId() const { return id; }

private:
    uint32_t id;
};

// Mark functions for optimization
[[gnu::hot]] void criticalPath();
[[gnu::cold]] void errorHandler();

// Whole program optimization
// Compile with: -flto
```

---

## Memory Placement

```cpp
// Control memory placement
class DmaBuffer {
private:
    // Place in specific section
    [[gnu::section(".dma_buffer")]]
    alignas(32) uint8_t buffer[1024];

public:
    uint8_t* data() { return buffer; }
    constexpr size_t size() const { return sizeof(buffer); }
};

// Place frequently used data together
struct [[gnu::packed]] ControlBlock {
    uint32_t status;
    uint32_t command;
    uint16_t count;
    uint16_t flags;
};
```

---

## Compile-Time Interfaces

```cpp
// Concept-like compile-time interface checking
template<typename T>
class SensorInterface {
private:
    // Check interface at compile time
    static void checkInterface() {
        T sensor;
        float v = sensor.read();         // Must have read()
        sensor.calibrate();              // Must have calibrate()
        bool r = sensor.isReady();       // Must have isReady()
        (void)v; (void)r;  // Avoid unused warnings
    }

public:
    SensorInterface() {
        // Verify interface in debug builds
        #ifdef DEBUG
        if (false) checkInterface();
        #endif
    }
};

// Implementation must satisfy interface
class TempSensor : public SensorInterface<TempSensor> {
public:
    float read() { return 25.0f; }
    void calibrate() { }
    bool isReady() { return true; }
};
```

---

## Performance Guidelines

1. **Prefer stack allocation** over heap
1. **Use templates** for compile-time polymorphism
1. **Inline** small functions
1. **Avoid** virtual functions in hot paths
1. **Minimize** template instantiations
1. **Profile** to verify optimizations

---

## Safety Guidelines

1. **No exceptions** - use error codes
1. **No dynamic_cast** - avoid RTTI
1. **Fixed-size containers** - no std::vector
1. **Const correctness** - immutable by default
1. **Static analysis** - use tools
1. **Defensive programming** - validate inputs

---

## Summary

1. C++ offers powerful abstractions for embedded
1. Zero-cost abstractions possible with care
1. RAII improves resource management
1. Templates enable compile-time optimization
1. Restrictions necessary for embedded use

---

## Key Takeaways

1. **Modern C++** features benefit embedded
1. **Compile-time** computation reduces runtime
1. **Type safety** prevents errors
1. **RAII** manages resources automatically
1. **Templates** enable reusable code
