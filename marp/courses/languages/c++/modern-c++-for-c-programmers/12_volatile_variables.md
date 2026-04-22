# Volatile Variables

## What is Volatile?

The `volatile` keyword tells the compiler that a variable's value may change at any time without any action being taken by the code

**Key characteristics:**
- Prevents compiler optimizations that assume the value doesn't change
- Forces the compiler to read from memory every time
- Does NOT provide thread synchronization
- Essential for hardware programming and memory-mapped I/O

**Common misconceptions:** volatile is NOT for thread safety in modern C++

---

## When to Use Volatile

Volatile should be used in specific scenarios:

1. **Memory-mapped I/O** - hardware registers
1. **Signal handlers** - variables modified by signal handlers
1. **Setjmp/longjmp** - variables that need to survive longjmp
1. **Memory-mapped hardware** - device drivers and embedded systems

```cpp
// Hardware register example
volatile uint32_t* const TIMER_CONTROL =
    reinterpret_cast<volatile uint32_t*>(0x40000000);

volatile uint32_t* const TIMER_VALUE =
    reinterpret_cast<volatile uint32_t*>(0x40000004);

void startTimer() {
    *TIMER_CONTROL = 1;  // Start timer

    // Wait for timer to reach target value
    while (*TIMER_VALUE < 1000) {
        // volatile ensures we read from hardware each time
    }
}
```

---

## Volatile vs Non-Volatile Behavior

Understanding compiler optimizations with and without volatile:

```cpp
// Without volatile - compiler may optimize
int normalVar = 0;

void busyWait() {
    while (normalVar == 0) {
        // Compiler might optimize this to infinite loop
        // thinking normalVar never changes
    }
}

// With volatile - compiler cannot optimize
volatile int volatileVar = 0;

void properWait() {
    while (volatileVar == 0) {
        // Compiler must read from memory each iteration
        // Cannot assume the value stays the same
    }
}

// Signal handler that modifies the variable
void signalHandler(int) {
    volatileVar = 1;  // This change will be visible in properWait()
}
```

---

## Memory-Mapped I/O Fundamentals

Memory-mapped I/O maps hardware registers to memory addresses:

```cpp
// Example: Simple GPIO controller
struct GPIORegisters {
    volatile uint32_t direction;    // 0x0: Pin direction (0=input, 1=output)
    volatile uint32_t outputData;   // 0x4: Output data register
    volatile uint32_t inputData;    // 0x8: Input data register (read-only)
    volatile uint32_t interrupt;    // 0xC: Interrupt status
};

class GPIOController {
private:
    volatile GPIORegisters* registers;

public:
    GPIOController(uintptr_t baseAddress)
        : registers(reinterpret_cast<volatile GPIORegisters*>(baseAddress)) {}

    void setPinDirection(int pin, bool output) {
        if (output) {
            registers->direction |= (1U << pin);   // Set bit
        } else {
            registers->direction &= ~(1U << pin);  // Clear bit
        }
    }

    void writePin(int pin, bool value) {
        if (value) {
            registers->outputData |= (1U << pin);
        } else {
            registers->outputData &= ~(1U << pin);
        }
    }

    bool readPin(int pin) const {
        return (registers->inputData & (1U << pin)) != 0;
    }
};
```

---

## Hardware Register Access Patterns

Common patterns for accessing hardware registers:

```cpp
// Read-modify-write operations
class TimerController {
private:
    volatile uint32_t* const control;
    volatile uint32_t* const prescaler;
    volatile uint32_t* const counter;

public:
    TimerController(uintptr_t base)
        : control(reinterpret_cast<volatile uint32_t*>(base))
        , prescaler(reinterpret_cast<volatile uint32_t*>(base + 4))
        , counter(reinterpret_cast<volatile uint32_t*>(base + 8)) {}

    void enableTimer(bool enable) {
        if (enable) {
            *control |= 0x01;   // Set enable bit
        } else {
            *control &= ~0x01;  // Clear enable bit
        }
    }

    void setPrescaler(uint16_t value) {
        // Clear prescaler bits and set new value
        *prescaler = (*prescaler & 0xFFFF0000) | value;
    }

    uint32_t getCurrentCount() const {
        return *counter;  // Read current counter value
    }

    void resetCounter() {
        *counter = 0;  // Reset counter to zero
    }
};
```

---

## Bit Manipulation with Volatile: Class

Safe bit manipulation techniques for hardware registers:

```cpp
class VolatileBits {
public:
    static void setBit(volatile uint32_t& reg, int bit) {
        reg |= (1U << bit);
    }

    static void clearBit(volatile uint32_t& reg, int bit) {
        reg &= ~(1U << bit);
    }

    static void toggleBit(volatile uint32_t& reg, int bit) {
        reg ^= (1U << bit);
    }

    static bool testBit(volatile uint32_t& reg, int bit) {
        return (reg & (1U << bit)) != 0;
    }

    static void modifyBits(volatile uint32_t& reg, uint32_t mask, uint32_t value) {
        reg = (reg & ~mask) | (value & mask);
    }
};
```

---

## Bit Manipulation with Volatile: Example

```cpp
void configureUART() {
    volatile uint32_t* const UART_CONTROL =
        reinterpret_cast<volatile uint32_t*>(0x50000000);

    VolatileBits::modifyBits(*UART_CONTROL, 0xFF, 0x83);

    VolatileBits::setBit(*UART_CONTROL, 3);

    VolatileBits::setBit(*UART_CONTROL, 2);
}
```

---

## Placement New Basics

Placement new constructs objects at specific memory locations:

```cpp
#include <new>  // For placement new

class Widget {
private:
    int value;

public:
    Widget(int v) : value(v) {
        std::cout << "Widget constructed with value " << v
                  << " at address " << this << std::endl;
    }

    ~Widget() {
        std::cout << "Widget destroyed at address " << this << std::endl;
    }

    int getValue() const { return value; }
};

void demonstratePlacementNew() {
    // Allocate raw memory
    char buffer[sizeof(Widget)];

    // Construct object at specific location
    Widget* widget = new(buffer) Widget(42);

    std::cout << "Widget value: " << widget->getValue() << std::endl;

    // Must manually call destructor
    widget->~Widget();

    // No delete needed - memory is on stack
}
```

---

## Placement New with Alignment: Class

Ensuring proper alignment for placement new:

```cpp
#include <memory>
#include <type_traits>

template<typename T>
class AlignedStorage {
private:
    alignas(T) char storage[sizeof(T)];
    bool constructed = false;

public:
    template<typename... Args>
    T* construct(Args&&... args) {
        if (constructed) {
            throw std::runtime_error("Object already constructed");
        }

        T* obj = new(storage) T(std::forward<Args>(args)...);
        constructed = true;
        return obj;
    }

    void destroy() {
        if (constructed) {
            reinterpret_cast<T*>(storage)->~T();
            constructed = false;
        }
    }
```

---

## Placement New with Alignment: Accessors

```cpp
    T* get() {
        return constructed ? reinterpret_cast<T*>(storage) : nullptr;
    }

    const T* get() const {
        return constructed ? reinterpret_cast<const T*>(storage) : nullptr;
    }

    ~AlignedStorage() {
        destroy();
    }
};

void demonstrateAlignedStorage() {
    AlignedStorage<Widget> storage;

    Widget* widget = storage.construct(100);
    std::cout << "Value: " << widget->getValue() << std::endl;
}
```

---

## Custom New/Delete: Class Setup

Overloading new and delete for specific classes:

```cpp
class MemoryTrackedClass {
private:
    static size_t allocatedCount;
    static size_t totalAllocated;
    int data;

public:
    MemoryTrackedClass(int value) : data(value) {
        std::cout << "MemoryTrackedClass constructed: " << value << std::endl;
    }

    ~MemoryTrackedClass() {
        std::cout << "MemoryTrackedClass destroyed" << std::endl;
    }
```

---

## Custom New/Delete: Operators

```cpp
    static void* operator new(size_t size) {
        std::cout << "Custom new called, size: " << size << std::endl;

        void* ptr = std::malloc(size);
        if (!ptr) {
            throw std::bad_alloc();
        }

        ++allocatedCount;
        totalAllocated += size;

        return ptr;
    }

    static void operator delete(void* ptr, size_t size) {
        std::cout << "Custom delete called, size: " << size << std::endl;

        if (ptr) {
            --allocatedCount;
            totalAllocated -= size;
            std::free(ptr);
        }
    }
```

---

## Custom New/Delete: Array Operators

```cpp
    static void* operator new[](size_t size) {
        std::cout << "Custom new[] called, size: " << size << std::endl;
        return std::malloc(size);
    }

    static void operator delete[](void* ptr, size_t size) {
        std::cout << "Custom delete[] called, size: " << size << std::endl;
        std::free(ptr);
    }

    static void printStats() {
        std::cout << "Allocated objects: " << allocatedCount
                  << ", Total memory: " << totalAllocated << " bytes" << std::endl;
    }
};

size_t MemoryTrackedClass::allocatedCount = 0;
size_t MemoryTrackedClass::totalAllocated = 0;
```

---

## Placement New for Hardware: Controller Class

Using placement new with memory-mapped hardware:

```cpp
constexpr uintptr_t DEVICE_MEMORY_BASE = 0x80000000;
constexpr size_t DEVICE_MEMORY_SIZE = 4096;

class DeviceController {
private:
    volatile uint32_t command;
    volatile uint32_t status;
    volatile uint32_t data[10];

public:
    DeviceController() : command(0), status(0) {
        for (int i = 0; i < 10; ++i) {
            data[i] = 0;
        }
        std::cout << "DeviceController initialized at " << this << std::endl;
    }

    void sendCommand(uint32_t cmd) {
        command = cmd;
    }
```

---

## Placement New for Hardware: Methods

```cpp
    uint32_t getStatus() const {
        return status;
    }

    void writeData(int index, uint32_t value) {
        if (index >= 0 && index < 10) {
            data[index] = value;
        }
    }

    uint32_t readData(int index) const {
        return (index >= 0 && index < 10) ? data[index] : 0;
    }
};

DeviceController* initializeDevice() {
    void* deviceMemory = reinterpret_cast<void*>(DEVICE_MEMORY_BASE);

    DeviceController* controller = new(deviceMemory) DeviceController();

    return controller;
}
```

---

## Memory Pool: Storage and Lookup

Creating efficient memory pools:

```cpp
template<typename T, size_t PoolSize>
class MemoryPool {
private:
    alignas(T) char storage[PoolSize * sizeof(T)];
    std::bitset<PoolSize> used;
    size_t nextFree = 0;

    size_t findFreeSlot() {
        for (size_t i = 0; i < PoolSize; ++i) {
            size_t index = (nextFree + i) % PoolSize;
            if (!used[index]) {
                return index;
            }
        }
        throw std::bad_alloc();
    }
```

---

## Memory Pool: Allocation

```cpp
public:
    template<typename... Args>
    T* allocate(Args&&... args) {
        size_t index = findFreeSlot();
        used[index] = true;
        nextFree = (index + 1) % PoolSize;

        T* ptr = reinterpret_cast<T*>(storage + index * sizeof(T));
        return new(ptr) T(std::forward<Args>(args)...);
    }

    void deallocate(T* ptr) {
        if (!ptr) return;

        char* charPtr = reinterpret_cast<char*>(ptr);
        size_t index = (charPtr - storage) / sizeof(T);

        if (index < PoolSize && used[index]) {
            ptr->~T();
            used[index] = false;
            nextFree = index;
        }
    }

    size_t capacity() const { return PoolSize; }
    size_t size() const { return used.count(); }
    bool empty() const { return used.none(); }
    bool full() const { return used.all(); }
};
```

---

## Memory Pool: Usage Example

```cpp
void demonstrateMemoryPool() {
    MemoryPool<Widget, 10> pool;

    std::vector<Widget*> widgets;

    for (int i = 0; i < 5; ++i) {
        widgets.push_back(pool.allocate(i * 10));
    }

    std::cout << "Pool size: " << pool.size() << std::endl;

    for (Widget* widget : widgets) {
        pool.deallocate(widget);
    }

    std::cout << "Pool size after deallocation: " << pool.size() << std::endl;
}
```

---

## Allocating Without Exceptions: Scalar

Using nothrow new for exception-free allocation:

```cpp
#include <new>

class SafeAllocator {
public:
    template<typename T, typename... Args>
    static T* allocate(Args&&... args) {
        void* memory = operator new(sizeof(T), std::nothrow);

        if (!memory) {
            return nullptr;
        }

        try {
            return new(memory) T(std::forward<Args>(args)...);
        } catch (...) {
            operator delete(memory, std::nothrow);
            return nullptr;
        }
    }

    template<typename T>
    static void deallocate(T* ptr) {
        if (ptr) {
            ptr->~T();
            operator delete(ptr, std::nothrow);
        }
    }
```

---

## Allocating Without Exceptions: Array Allocate

```cpp
    template<typename T>
    static T* allocateArray(size_t count) {
        if (count == 0) return nullptr;

        size_t totalSize = count * sizeof(T);

        void* memory = operator new(totalSize, std::nothrow);
        if (!memory) {
            return nullptr;
        }

        T* array = static_cast<T*>(memory);
        size_t constructed = 0;

        try {
            for (size_t i = 0; i < count; ++i) {
                new(array + i) T();
                ++constructed;
            }
            return array;
        } catch (...) {
            for (size_t i = 0; i < constructed; ++i) {
                array[i].~T();
            }
            operator delete(memory, std::nothrow);
            return nullptr;
        }
    }
```

---

## Allocating Without Exceptions: Array Deallocate

```cpp
    template<typename T>
    static void deallocateArray(T* array, size_t count) {
        if (array) {
            for (size_t i = count; i > 0; --i) {
                array[i - 1].~T();
            }
            operator delete(array, std::nothrow);
        }
    }
};
```

---

## Memory-Mapped File: Class Members

Using memory mapping for file I/O:

```cpp
#ifdef _WIN32
#include <windows.h>
#else
#include <sys/mman.h>
#include <fcntl.h>
#include <unistd.h>
#endif

class MemoryMappedFile {
private:
    void* mappedMemory = nullptr;
    size_t fileSize = 0;

#ifdef _WIN32
    HANDLE fileHandle = INVALID_HANDLE_VALUE;
    HANDLE mappingHandle = INVALID_HANDLE_VALUE;
#else
    int fileDescriptor = -1;
#endif
};
```

---

## Memory-Mapped File: Open on Windows

```cpp
bool open(const std::string& filename) {
#ifdef _WIN32
    fileHandle = CreateFileA(filename.c_str(), GENERIC_READ | GENERIC_WRITE,
                            0, nullptr, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, nullptr);

    if (fileHandle == INVALID_HANDLE_VALUE) {
        return false;
    }

    LARGE_INTEGER size;
    if (!GetFileSizeEx(fileHandle, &size)) {
        close();
        return false;
    }
    fileSize = static_cast<size_t>(size.QuadPart);

    mappingHandle = CreateFileMappingA(fileHandle, nullptr, PAGE_READWRITE, 0, 0, nullptr);
    if (!mappingHandle) {
        close();
        return false;
    }

    mappedMemory = MapViewOfFile(mappingHandle, FILE_MAP_ALL_ACCESS, 0, 0, 0);
```

---

## Memory-Mapped File: Open on POSIX

```cpp
#else
    fileDescriptor = ::open(filename.c_str(), O_RDWR);
    if (fileDescriptor == -1) {
        return false;
    }

    struct stat st;
    if (fstat(fileDescriptor, &st) == -1) {
        close();
        return false;
    }
    fileSize = st.st_size;

    mappedMemory = mmap(nullptr, fileSize, PROT_READ | PROT_WRITE,
                       MAP_SHARED, fileDescriptor, 0);
    if (mappedMemory == MAP_FAILED) {
        mappedMemory = nullptr;
        close();
        return false;
    }
#endif
    return true;
}
```

---

## Memory-Mapped File: Close

```cpp
void close() {
    if (mappedMemory) {
#ifdef _WIN32
        UnmapViewOfFile(mappedMemory);
#else
        munmap(mappedMemory, fileSize);
#endif
        mappedMemory = nullptr;
    }

#ifdef _WIN32
    if (mappingHandle != INVALID_HANDLE_VALUE) {
        CloseHandle(mappingHandle);
        mappingHandle = INVALID_HANDLE_VALUE;
    }
    if (fileHandle != INVALID_HANDLE_VALUE) {
        CloseHandle(fileHandle);
        fileHandle = INVALID_HANDLE_VALUE;
    }
#else
    if (fileDescriptor != -1) {
        ::close(fileDescriptor);
        fileDescriptor = -1;
    }
#endif
}
```

---

## Memory-Mapped File: Accessors

```cpp
template<typename T>
T* getAs() {
    return static_cast<T*>(mappedMemory);
}

size_t size() const { return fileSize; }

~MemoryMappedFile() {
    close();
}
```

---

## Volatile and Atomic: Basics

Understanding the relationship between volatile and atomic:

```cpp
#include <atomic>

volatile int volatileCounter = 0;

void incrementVolatile() {
    ++volatileCounter;  // NOT atomic
}

std::atomic<int> atomicCounter{0};

void incrementAtomic() {
    ++atomicCounter;  // thread safe
}

struct HardwareRegister {
    volatile std::atomic<uint32_t> control;
    volatile std::atomic<uint32_t> status;

    void setControlBit(int bit) {
        uint32_t current = control.load();
        uint32_t newValue = current | (1U << bit);
        control.store(newValue);
    }

    bool isStatusBitSet(int bit) const {
        return (status.load() & (1U << bit)) != 0;
    }
};
```

---

## Volatile and Atomic: Hardware Interface

```cpp
class AtomicHardwareInterface {
private:
    volatile std::atomic<uint32_t>* const registerBase;

public:
    AtomicHardwareInterface(uintptr_t base)
        : registerBase(reinterpret_cast<volatile std::atomic<uint32_t>*>(base)) {}

    void writeRegister(size_t index, uint32_t value) {
        registerBase[index].store(value, std::memory_order_release);
    }

    uint32_t readRegister(size_t index) const {
        return registerBase[index].load(std::memory_order_acquire);
    }

    void setBits(size_t index, uint32_t mask) {
        registerBase[index].fetch_or(mask, std::memory_order_acq_rel);
    }

    void clearBits(size_t index, uint32_t mask) {
        registerBase[index].fetch_and(~mask, std::memory_order_acq_rel);
    }
};
```

---

## Volatile in Embedded: ISR Communication

Practical examples for embedded programming:

```cpp
volatile bool dataReady = false;
volatile uint8_t receivedData = 0;

extern "C" void UART_IRQHandler() {
    if (UART->STATUS & UART_RX_READY) {
        receivedData = UART->DATA;
        dataReady = true;
    }
}

void processData() {
    while (true) {
        if (dataReady) {
            uint8_t data = receivedData;
            dataReady = false;

            handleReceivedByte(data);
        }

        performOtherTasks();
    }
}

volatile uint32_t* const WATCHDOG_RESET =
    reinterpret_cast<volatile uint32_t*>(0x40002000);

void feedWatchdog() {
    *WATCHDOG_RESET = 0xDEADBEEF;
}
```

---

## Volatile in Embedded: Software SPI

```cpp
class SoftwareSPI {
private:
    volatile uint32_t* const gpioOut;
    volatile uint32_t* const gpioIn;
    const uint32_t clockPin;
    const uint32_t mosiPin;
    const uint32_t misoPin;

public:
    SoftwareSPI(volatile uint32_t* out, volatile uint32_t* in,
                uint32_t clk, uint32_t mosi, uint32_t miso)
        : gpioOut(out), gpioIn(in), clockPin(clk), mosiPin(mosi), misoPin(miso) {}

    uint8_t transfer(uint8_t data) {
        uint8_t received = 0;

        for (int bit = 7; bit >= 0; --bit) {
            if (data & (1 << bit)) {
                *gpioOut |= (1U << mosiPin);
            } else {
                *gpioOut &= ~(1U << mosiPin);
            }

            *gpioOut |= (1U << clockPin);

            if (*gpioIn & (1U << misoPin)) {
                received |= (1 << bit);
            }

            *gpioOut &= ~(1U << clockPin);
        }

        return received;
    }
};
```

---

## Debug and Release Behavior

Volatile behavior differences between debug and optimized builds:

```cpp
// Example showing optimization differences
class OptimizationDemo {
private:
    int normalVariable = 0;
    volatile int volatileVariable = 0;

public:
    void demonstrateOptimization() {
        // Normal variable - compiler may optimize
        std::cout << "Normal variable test:" << std::endl;
        auto start = std::chrono::high_resolution_clock::now();

        for (int i = 0; i < 1000000; ++i) {
            normalVariable = i;
            int temp = normalVariable;  // May be optimized away
            (void)temp;  // Suppress unused warning
        }

        auto end = std::chrono::high_resolution_clock::now();
        auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
        std::cout << "Normal variable time: " << duration.count() << " microseconds" << std::endl;

        // Volatile variable - no optimization
        std::cout << "Volatile variable test:" << std::endl;
        start = std::chrono::high_resolution_clock::now();

        for (int i = 0; i < 1000000; ++i) {
            volatileVariable = i;
            int temp = volatileVariable;  // Must read from memory
            (void)temp;
        }

        end = std::chrono::high_resolution_clock::now();
        duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
        std::cout << "Volatile variable time: " << duration.count() << " microseconds" << std::endl;
    }
};
```

---

## Memory Barriers and Volatile: Compiler Only

Understanding memory ordering with volatile:

```cpp
class MemoryOrderingExample {
private:
    volatile int flag = 0;
    volatile int data = 0;

public:
    void writer() {
        data = 42;
        flag = 1;
        // Compiler won't reorder, but CPU might
    }

    int reader() {
        while (flag == 0) {
        }
        return data;
    }
};
```

---

## Memory Barriers and Volatile: Atomic

```cpp
class ProperMemoryOrdering {
private:
    std::atomic<int> flag{0};
    std::atomic<int> data{0};

public:
    void writer() {
        data.store(42, std::memory_order_relaxed);
        flag.store(1, std::memory_order_release);
    }

    int reader() {
        while (flag.load(std::memory_order_acquire) == 0) {
        }
        return data.load(std::memory_order_relaxed);
    }
};
```

---

## Device Driver Example: Class Definition

Complete example of a simple device driver:

```cpp
class LEDDriver {
private:
    struct LEDRegisters {
        volatile uint32_t control;
        volatile uint32_t brightness;
        volatile uint32_t pattern;
        volatile uint32_t timing;
    };

    volatile LEDRegisters* const registers;
    static constexpr uint32_t LED_ENABLE = 0x01;
    static constexpr uint32_t LED_BLINK = 0x02;
    static constexpr uint32_t LED_AUTO_PATTERN = 0x04;

public:
    LEDDriver(uintptr_t baseAddress)
        : registers(reinterpret_cast<volatile LEDRegisters*>(baseAddress)) {
        registers->control = 0;
        registers->brightness = 0;
        registers->pattern = 0;
        registers->timing = 1000;
    }
```

---

## Device Driver Example: Enable and Brightness

```cpp
    void enable(bool enabled) {
        if (enabled) {
            registers->control |= LED_ENABLE;
        } else {
            registers->control &= ~LED_ENABLE;
        }
    }

    void setBrightness(uint8_t level) {
        registers->brightness = level;
    }

    void setBlinkMode(bool blink) {
        if (blink) {
            registers->control |= LED_BLINK;
        } else {
            registers->control &= ~LED_BLINK;
        }
    }

    void setPattern(uint32_t pattern) {
        registers->pattern = pattern;
        registers->control |= LED_AUTO_PATTERN;
    }

    void setTiming(uint32_t milliseconds) {
        registers->timing = milliseconds;
    }
```

---

## Device Driver Example: High-Level Methods

```cpp
    uint32_t getStatus() const {
        return registers->control;
    }

    void turnOn() {
        setBrightness(255);
        enable(true);
    }

    void turnOff() {
        setBrightness(0);
        enable(false);
    }

    void startBlinking(uint32_t intervalMs) {
        setTiming(intervalMs);
        setBlinkMode(true);
        enable(true);
    }
};

void initializeLEDs() {
    LEDDriver statusLED(0x40001000);

    statusLED.turnOn();

    LEDDriver activityLED(0x40001100);
    activityLED.setPattern(0xAAAAAAAA);
    activityLED.startBlinking(500);
}
```

---

## Custom Allocators: `StackAllocator`

Creating specialized allocators for different memory regions:

```cpp
template<size_t Size>
class StackAllocator {
private:
    alignas(std::max_align_t) char storage[Size];
    char* current;
    char* end;

public:
    StackAllocator() : current(storage), end(storage + Size) {}

    template<typename T>
    T* allocate(size_t count = 1) {
        size_t bytes = count * sizeof(T);
        size_t alignment = alignof(T);

        char* aligned = reinterpret_cast<char*>(
            (reinterpret_cast<uintptr_t>(current) + alignment - 1) & ~(alignment - 1)
        );

        if (aligned + bytes > end) {
            throw std::bad_alloc();
        }

        current = aligned + bytes;
        return reinterpret_cast<T*>(aligned);
    }
```

---

## Custom Allocators: `StackAllocator` Methods

```cpp
    template<typename T, typename... Args>
    T* construct(Args&&... args) {
        T* ptr = allocate<T>();
        return new(ptr) T(std::forward<Args>(args)...);
    }

    void reset() {
        current = storage;
    }

    size_t bytesUsed() const {
        return current - storage;
    }

    size_t bytesAvailable() const {
        return end - current;
    }
};
```

---

## Custom Allocators: PoolAllocator Storage

```cpp
template<typename T, size_t PoolSize>
class PoolAllocator {
private:
    struct Block {
        alignas(T) char data[sizeof(T)];
        Block* next;
    };

    Block storage[PoolSize];
    Block* freeList;

public:
    PoolAllocator() {
        freeList = &storage[0];
        for (size_t i = 0; i < PoolSize - 1; ++i) {
            storage[i].next = &storage[i + 1];
        }
        storage[PoolSize - 1].next = nullptr;
    }
```

---

## Custom Allocators: PoolAllocator Allocate

```cpp
    T* allocate() {
        if (!freeList) {
            throw std::bad_alloc();
        }

        Block* block = freeList;
        freeList = freeList->next;

        return reinterpret_cast<T*>(block);
    }

    void deallocate(T* ptr) {
        if (!ptr) return;

        Block* block = reinterpret_cast<Block*>(ptr);
        block->next = freeList;
        freeList = block;
    }
```

---

## Custom Allocators: PoolAllocator Construct

```cpp
    template<typename... Args>
    T* construct(Args&&... args) {
        T* ptr = allocate();
        try {
            return new(ptr) T(std::forward<Args>(args)...);
        } catch (...) {
            deallocate(ptr);
            throw;
        }
    }

    void destroy(T* ptr) {
        if (ptr) {
            ptr->~T();
            deallocate(ptr);
        }
    }

    size_t capacity() const { return PoolSize; }
};
```

---

## Custom Allocators: Demo

```cpp
void demonstrateCustomAllocators() {
    StackAllocator<1024> stackAlloc;
    PoolAllocator<Widget, 10> poolAlloc;

    auto* stackWidget = stackAlloc.construct<Widget>(42);
    std::cout << "Stack widget: " << stackWidget->getValue() << std::endl;

    auto* poolWidget = poolAlloc.construct(100);
    std::cout << "Pool widget: " << poolWidget->getValue() << std::endl;

    stackWidget->~Widget();
    poolAlloc.destroy(poolWidget);

    stackAlloc.reset();
}
```

---

## Compiler Intrinsics: Memory Barrier

Using compiler-specific features with volatile:

```cpp
class CompilerSpecific {
public:
    static void memoryBarrier() {
#if defined(_MSC_VER)
        _ReadWriteBarrier();
#elif defined(__GNUC__)
        __asm__ __volatile__("" ::: "memory");
#else
        std::atomic_thread_fence(std::memory_order_seq_cst);
#endif
    }

    template<typename T>
    static void doNotOptimize(const T& value) {
#if defined(__GNUC__)
        __asm__ __volatile__("" : : "r,m"(value) : "memory");
#elif defined(_MSC_VER)
        volatile T* volatile_ptr = const_cast<volatile T*>(&value);
        (void)volatile_ptr;
        _ReadWriteBarrier();
#else
        volatile auto copy = value;
        (void)copy;
#endif
    }
```

---

## Compiler Intrinsics: Cache Flush

```cpp
    static void flushCache(void* address, size_t size) {
#if defined(_MSC_VER) && defined(_M_X64)
        for (char* ptr = static_cast<char*>(address);
             ptr < static_cast<char*>(address) + size;
             ptr += 64) {
            _mm_clflush(ptr);
        }
#elif defined(__GNUC__) && (defined(__x86_64__) || defined(__i386__))
        for (char* ptr = static_cast<char*>(address);
             ptr < static_cast<char*>(address) + size;
             ptr += 64) {
            __builtin_ia32_clflush(ptr);
        }
#endif
    }
};
```

---

## Compiler Intrinsics: Performance Counter

```cpp
class PerformanceCounter {
private:
    volatile uint64_t* const counterRegister;

public:
    PerformanceCounter(uintptr_t address)
        : counterRegister(reinterpret_cast<volatile uint64_t*>(address)) {}

    uint64_t readCounter() const {
        return *counterRegister;
    }

    static uint64_t getCPUTimestamp() {
#if defined(_MSC_VER) && defined(_M_X64)
        return __rdtsc();
#elif defined(__GNUC__) && (defined(__x86_64__) || defined(__i386__))
        uint32_t low, high;
        __asm__ __volatile__("rdtsc" : "=a"(low), "=d"(high));
        return (static_cast<uint64_t>(high) << 32) | low;
#else
        return std::chrono::high_resolution_clock::now().time_since_epoch().count();
#endif
    }
};
```

---

## Error Handling with Hardware: Types

Robust error handling for hardware operations:

```cpp
enum class HardwareError {
    Success,
    Timeout,
    DeviceNotReady,
    InvalidParameter,
    HardwareFailure,
    CommunicationError
};

class HardwareDevice {
private:
    volatile uint32_t* const controlReg;
    volatile uint32_t* const statusReg;
    volatile uint32_t* const dataReg;

    static constexpr uint32_t STATUS_READY = 0x01;
    static constexpr uint32_t STATUS_ERROR = 0x02;
    static constexpr uint32_t STATUS_BUSY = 0x04;

    static constexpr uint32_t CONTROL_ENABLE = 0x01;
    static constexpr uint32_t CONTROL_RESET = 0x80;

public:
    HardwareDevice(uintptr_t baseAddress)
        : controlReg(reinterpret_cast<volatile uint32_t*>(baseAddress))
        , statusReg(reinterpret_cast<volatile uint32_t*>(baseAddress + 4))
        , dataReg(reinterpret_cast<volatile uint32_t*>(baseAddress + 8)) {}
```

---

## Error Handling with Hardware: Initialize

```cpp
    HardwareError initialize() {
        *controlReg = CONTROL_RESET;

        auto timeout = std::chrono::steady_clock::now() + std::chrono::milliseconds(100);
        while ((*statusReg & STATUS_BUSY) && std::chrono::steady_clock::now() < timeout) {
            std::this_thread::sleep_for(std::chrono::microseconds(10));
        }

        if (*statusReg & STATUS_BUSY) {
            return HardwareError::Timeout;
        }

        if (*statusReg & STATUS_ERROR) {
            return HardwareError::HardwareFailure;
        }

        *controlReg = CONTROL_ENABLE;

        if (!(*statusReg & STATUS_READY)) {
            return HardwareError::DeviceNotReady;
        }

        return HardwareError::Success;
    }
```

---

## Error Handling with Hardware: Write

```cpp
    HardwareError writeData(uint32_t data) {
        if (!(*statusReg & STATUS_READY)) {
            return HardwareError::DeviceNotReady;
        }

        if (*statusReg & STATUS_ERROR) {
            return HardwareError::HardwareFailure;
        }

        *dataReg = data;

        auto timeout = std::chrono::steady_clock::now() + std::chrono::milliseconds(10);
        while ((*statusReg & STATUS_BUSY) && std::chrono::steady_clock::now() < timeout) {
            std::this_thread::sleep_for(std::chrono::microseconds(1));
        }

        if (*statusReg & STATUS_BUSY) {
            return HardwareError::Timeout;
        }

        if (*statusReg & STATUS_ERROR) {
            return HardwareError::CommunicationError;
        }

        return HardwareError::Success;
    }
```

---

## Error Handling with Hardware: Read

```cpp
    std::pair<HardwareError, uint32_t> readData() {
        if (!(*statusReg & STATUS_READY)) {
            return {HardwareError::DeviceNotReady, 0};
        }

        if (*statusReg & STATUS_ERROR) {
            return {HardwareError::HardwareFailure, 0};
        }

        uint32_t data = *dataReg;

        if (*statusReg & STATUS_ERROR) {
            return {HardwareError::CommunicationError, 0};
        }

        return {HardwareError::Success, data};
    }

    const char* errorToString(HardwareError error) const {
        switch (error) {
            case HardwareError::Success: return "Success";
            case HardwareError::Timeout: return "Operation timed out";
            case HardwareError::DeviceNotReady: return "Device not ready";
            case HardwareError::InvalidParameter: return "Invalid parameter";
            case HardwareError::HardwareFailure: return "Hardware failure";
            case HardwareError::CommunicationError: return "Communication error";
            default: return "Unknown error";
        }
    }
};
```

---

## RAII for Hardware: `HardwareResource`

Using RAII to manage hardware resources safely:

```cpp
class HardwareResource {
private:
    volatile uint32_t* const baseAddress;
    bool acquired = false;

public:
    explicit HardwareResource(uintptr_t address)
        : baseAddress(reinterpret_cast<volatile uint32_t*>(address)) {
        acquire();
    }

    ~HardwareResource() {
        release();
    }

    HardwareResource(const HardwareResource&) = delete;
    HardwareResource& operator=(const HardwareResource&) = delete;
    HardwareResource(HardwareResource&&) = delete;
    HardwareResource& operator=(HardwareResource&&) = delete;
```

---

## RAII for Hardware: Resource Methods

```cpp
    void acquire() {
        if (!acquired) {
            baseAddress[0] = 0x12345678;
            acquired = true;
        }
    }

    void release() {
        if (acquired) {
            baseAddress[0] = 0x87654321;
            acquired = false;
        }
    }

    volatile uint32_t* get() const {
        return acquired ? baseAddress : nullptr;
    }

    bool isAcquired() const {
        return acquired;
    }
};
```

---

## RAII for Hardware: `ScopedHardwareLock`

```cpp
class ScopedHardwareLock {
private:
    volatile uint32_t* const lockRegister;
    bool locked = false;

public:
    explicit ScopedHardwareLock(volatile uint32_t* reg) : lockRegister(reg) {
        auto timeout = std::chrono::steady_clock::now() + std::chrono::milliseconds(100);

        while (std::chrono::steady_clock::now() < timeout) {
            uint32_t expected = 0;
            if (*lockRegister == 0) {
                *lockRegister = 1;
                if (*lockRegister == 1) {
                    locked = true;
                    break;
                }
            }
            std::this_thread::sleep_for(std::chrono::microseconds(10));
        }

        if (!locked) {
            throw std::runtime_error("Failed to acquire hardware lock");
        }
    }

    ~ScopedHardwareLock() {
        if (locked) {
            *lockRegister = 0;
        }
    }

    ScopedHardwareLock(const ScopedHardwareLock&) = delete;
    ScopedHardwareLock& operator=(const ScopedHardwareLock&) = delete;
};
```

---

## RAII for Hardware: Usage

```cpp
void useHardwareResource() {
    try {
        HardwareResource resource(0x40000000);

        volatile uint32_t* hw = resource.get();
        if (hw) {
            hw[1] = 0xDEADBEEF;
            uint32_t result = hw[2];

            {
                ScopedHardwareLock lock(&hw[3]);
                hw[4] = result * 2;
            }
        }
    } catch (const std::exception& e) {
        std::cerr << "Hardware error: " << e.what() << std::endl;
    }
}
```

---

## Best Practices for Volatile

Guidelines for using volatile effectively:

**Do Use Volatile For:**
- Memory-mapped hardware registers
- Variables modified by signal handlers
- Variables accessed by setjmp/longjmp
- Communication with interrupt service routines

**Don't Use Volatile For:**
- Thread synchronization (use atomic instead)
- General multi-threading (use std::atomic)
- Performance optimization (it prevents optimizations)
- Cache coherency (use proper memory barriers)

```cpp
// Good: Hardware register access
volatile uint32_t* const TIMER_REG =
    reinterpret_cast<volatile uint32_t*>(0x40000000);

void configureTimer() {
    *TIMER_REG = 0x12345678;  // Correct use of volatile
}

// Bad: Thread synchronization
volatile bool flag = false;  // DON'T do this for threading

void badThreadSync() {
    // This is NOT thread-safe!
    while (!flag) {
        // Busy wait - volatile doesn't provide synchronization
    }
}

// Good: Thread synchronization
std::atomic<bool> atomicFlag{false};

void goodThreadSync() {
    while (!atomicFlag.load()) {
        // Properly synchronized
    }
}
```

---

## Debugging Volatile: `DebugVolatile`

Techniques for debugging volatile-related issues:

```cpp
class DebugVolatile {
private:
    volatile uint32_t debugRegister;

public:
    DebugVolatile(uint32_t initial = 0) : debugRegister(initial) {}

    void write(uint32_t value) {
        std::cout << "Writing " << std::hex << value
                  << " to address " << &debugRegister << std::endl;
        debugRegister = value;
    }

    uint32_t read() const {
        uint32_t value = debugRegister;
        std::cout << "Read " << std::hex << value
                  << " from address " << &debugRegister << std::endl;
        return value;
    }

    void dump() const {
        std::cout << "Volatile register at " << &debugRegister
                  << " contains " << std::hex << debugRegister << std::endl;
    }
};
```

---

## Debugging Volatile: `VolatileTracer` Class

```cpp
template<typename T>
class VolatileTracer {
private:
    volatile T value;
    mutable std::atomic<size_t> readCount{0};
    mutable std::atomic<size_t> writeCount{0};

public:
    VolatileTracer(T initial = T{}) : value(initial) {}

    VolatileTracer& operator=(const T& newValue) {
        value = newValue;
        writeCount.fetch_add(1);
        return *this;
    }

    operator T() const {
        readCount.fetch_add(1);
        return value;
    }

    void printStats() const {
        std::cout << "Reads: " << readCount.load()
                  << ", Writes: " << writeCount.load() << std::endl;
    }

    void resetStats() {
        readCount.store(0);
        writeCount.store(0);
    }
};
```

---

## Debugging Volatile: Tracer Usage

```cpp
void demonstrateDebugging() {
    VolatileTracer<uint32_t> traced(0x12345678);

    traced = 0xDEADBEEF;
    uint32_t value1 = traced;
    uint32_t value2 = traced;
    traced = 0xCAFEBABE;

    traced.printStats();
}
```

---

## Performance Implications: Setup

Understanding the performance cost of volatile:

```cpp
class PerformanceTest {
public:
    static void benchmarkVolatile() {
        const size_t iterations = 10000000;

        int normalVar = 0;
        auto start = std::chrono::high_resolution_clock::now();

        for (size_t i = 0; i < iterations; ++i) {
            normalVar = i;
            int temp = normalVar;
            CompilerSpecific::doNotOptimize(temp);
        }

        auto end = std::chrono::high_resolution_clock::now();
        auto normalTime = std::chrono::duration_cast<std::chrono::nanoseconds>(end - start);
```

---

## Performance Implications: Volatile Test

```cpp
        volatile int volatileVar = 0;
        start = std::chrono::high_resolution_clock::now();

        for (size_t i = 0; i < iterations; ++i) {
            volatileVar = i;
            int temp = volatileVar;
            (void)temp;
        }

        end = std::chrono::high_resolution_clock::now();
        auto volatileTime = std::chrono::duration_cast<std::chrono::nanoseconds>(end - start);

        std::cout << "Normal variable: " << normalTime.count() << " ns" << std::endl;
        std::cout << "Volatile variable: " << volatileTime.count() << " ns" << std::endl;
        std::cout << "Overhead: " << (volatileTime.count() - normalTime.count()) << " ns" << std::endl;
        std::cout << "Slowdown factor: " << static_cast<double>(volatileTime.count()) / normalTime.count() << "x" << std::endl;
    }
};
```

---

## Performance Implications: Cache Effects Setup

```cpp
class CacheEffectsDemo {
private:
    static constexpr size_t ARRAY_SIZE = 1024 * 1024;

public:
    static void demonstrateCacheEffects() {
        std::vector<int> normalArray(ARRAY_SIZE, 42);

        volatile int* volatileArray = new volatile int[ARRAY_SIZE];
        for (size_t i = 0; i < ARRAY_SIZE; ++i) {
            volatileArray[i] = 42;
        }
```

---

## Performance Implications: Cache Timing

```cpp
        auto testNormal = [&]() {
            auto start = std::chrono::high_resolution_clock::now();
            long long sum = 0;
            for (size_t i = 0; i < ARRAY_SIZE; ++i) {
                sum += normalArray[i];
            }
            auto end = std::chrono::high_resolution_clock::now();
            CompilerSpecific::doNotOptimize(sum);
            return std::chrono::duration_cast<std::chrono::microseconds>(end - start);
        };

        auto testVolatile = [&]() {
            auto start = std::chrono::high_resolution_clock::now();
            long long sum = 0;
            for (size_t i = 0; i < ARRAY_SIZE; ++i) {
                sum += volatileArray[i];
            }
            auto end = std::chrono::high_resolution_clock::now();
            return std::chrono::duration_cast<std::chrono::microseconds>(end - start);
        };

        auto normalTime = testNormal();
        auto volatileTime = testVolatile();

        std::cout << "Normal array sum: " << normalTime.count() << " μs" << std::endl;
        std::cout << "Volatile array sum: " << volatileTime.count() << " μs" << std::endl;

        delete[] volatileArray;
    }
};
```

---

## Modern Alternatives: `ModernSignaling`

C++11+ alternatives for common volatile use cases:

```cpp
class ModernSignaling {
private:
    std::atomic<bool> stopRequested{false};
    std::atomic<int> dataReady{0};

public:
    void requestStop() {
        stopRequested.store(true, std::memory_order_relaxed);
    }

    bool shouldStop() const {
        return stopRequested.load(std::memory_order_relaxed);
    }

    void signalDataReady(int count) {
        dataReady.store(count, std::memory_order_release);
    }

    int getDataReadyCount() const {
        return dataReady.load(std::memory_order_acquire);
    }
};
```

---

## Modern Alternatives: `AtomicHardwareRegister`

```cpp
class AtomicHardwareRegister {
private:
    std::atomic<uint32_t>* const hwRegister;

public:
    AtomicHardwareRegister(uintptr_t address)
        : hwRegister(reinterpret_cast<std::atomic<uint32_t>*>(address)) {}

    void write(uint32_t value) {
        hwRegister->store(value, std::memory_order_relaxed);
    }

    uint32_t read() const {
        return hwRegister->load(std::memory_order_relaxed);
    }

    void setBits(uint32_t mask) {
        hwRegister->fetch_or(mask, std::memory_order_relaxed);
    }

    void clearBits(uint32_t mask) {
        hwRegister->fetch_and(~mask, std::memory_order_relaxed);
    }

    bool testAndSet(uint32_t mask) {
        uint32_t old = hwRegister->fetch_or(mask, std::memory_order_relaxed);
        return (old & mask) != 0;
    }
};
```

---

## Modern Alternatives: `LockFreeQueue` Nodes

```cpp
class LockFreeQueue {
private:
    struct Node {
        std::atomic<int> data{0};
        std::atomic<Node*> next{nullptr};
    };

    std::atomic<Node*> head{nullptr};
    std::atomic<Node*> tail{nullptr};

public:
    LockFreeQueue() {
        Node* dummy = new Node;
        head.store(dummy);
        tail.store(dummy);
    }
```

---

## Modern Alternatives: `LockFreeQueue` Operations

```cpp
    void enqueue(int value) {
        Node* newNode = new Node;
        newNode->data.store(value);

        Node* prevTail = tail.exchange(newNode);
        prevTail->next.store(newNode);
    }

    bool dequeue(int& result) {
        Node* head_node = head.load();
        Node* next = head_node->next.load();

        if (next == nullptr) {
            return false;
        }

        result = next->data.load();
        head.store(next);
        delete head_node;
        return true;
    }

    ~LockFreeQueue() {
        while (head.load() != nullptr) {
            Node* old_head = head.load();
            head.store(old_head->next);
            delete old_head;
        }
    }
};
```

---

## Summary and Best Practices

**Volatile Summary:**
- Use for hardware registers and memory-mapped I/O
- Prevents compiler optimizations, not CPU reordering
- Does NOT provide thread synchronization
- Has performance implications due to prevented optimizations

**Key Guidelines:**
1. **Use volatile for hardware programming** - memory-mapped registers
1. **Use atomic for thread synchronization** - not volatile
1. **Combine with placement new** for hardware object construction
1. **Use RAII** for hardware resource management
1. **Handle errors gracefully** with timeout and retry logic
1. **Profile performance impact** of volatile access patterns

**Modern C++ Approach:**
- Prefer `std::atomic` over volatile for thread safety
- Use memory ordering specifications for performance
- Apply RAII principles to hardware resource management
- Leverage custom allocators for specialized memory regions
