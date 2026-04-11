---
tags:
  - languages:c++
  - design-patterns:raii
level: advanced
category: embedded
audience:
  - audiences:embedded-engineers
  - audiences:developers
---
# C++ Resource Management

---

## Chapter Overview

1. Managing contained members
1. The Rule of Three/Five/Zero
1. Smart pointers for embedded
1. Resource managing classes
1. Move semantics optimization

---

## RAII Principle

![raii_principle](svg/courses/embedded/effective-real-time-embedded-c-and-c++/15_resource_management/raii_principle.svg)

---

## Basic Resource Management

```cpp
// Manual resource management (BAD)
void processFile() {
    FILE* file = fopen("data.txt", "r");
    if (!file) return;

    char* buffer = (char*)malloc(1024);
    if (!buffer) {
        fclose(file);  // Easy to forget!
        return;
    }

    // Process...
    if (error_condition) {
        free(buffer);
        fclose(file);  // Duplicate cleanup
        return;
    }

    free(buffer);
    fclose(file);
}

// RAII approach (GOOD)
class FileHandle {
private:
    FILE* file;

public:
    explicit FileHandle(const char* name, const char* mode)
        : file(fopen(name, mode)) {}

    ~FileHandle() {
        if (file) fclose(file);
    }

    operator FILE*() { return file; }
    bool isValid() const { return file != nullptr; }
};
```

---

## Managing Contained Members

```cpp
class UartDriver {
private:
    DmaChannel txDma;
    DmaChannel rxDma;
    CircularBuffer<256> txBuffer;
    CircularBuffer<256> rxBuffer;
    const uint32_t baseAddress;

public:
    // Constructor initializes all members
    UartDriver(uint32_t addr, uint8_t txDmaNum, uint8_t rxDmaNum)
        : txDma(txDmaNum)           // Initialize in order
        , rxDma(rxDmaNum)           // of declaration
        , txBuffer()                // Default construct
        , rxBuffer()
        , baseAddress(addr) {       // const must be initialized

        // Additional setup
        configureUart();
    }

    // Destructor automatically calls member destructors
    // in reverse order of construction
};
```

---

## Rule of Three

```cpp
// If you define any of these, define all three:
// 1. Destructor
// 2. Copy constructor
// 3. Copy assignment operator

class Buffer {
private:
    uint8_t* data;
    size_t size;

public:
    // Constructor
    explicit Buffer(size_t s)
        : data(new uint8_t[s]), size(s) {}

    // 1. Destructor
    ~Buffer() {
        delete[] data;
    }

    // 2. Copy constructor
    Buffer(const Buffer& other)
        : data(new uint8_t[other.size]), size(other.size) {
        std::memcpy(data, other.data, size);
    }

    // 3. Copy assignment operator
    Buffer& operator=(const Buffer& other) {
        if (this != &other) {
            delete[] data;
            size = other.size;
            data = new uint8_t[size];
            std::memcpy(data, other.data, size);
        }
        return *this;
    }
};
```

---

## Copy-and-Swap Idiom

```cpp
class Buffer {
private:
    uint8_t* data;
    size_t size;

    // Private swap function
    void swap(Buffer& other) noexcept {
        std::swap(data, other.data);
        std::swap(size, other.size);
    }

public:
    // Copy assignment using copy-and-swap
    Buffer& operator=(Buffer other) {  // Pass by value
        swap(other);  // Swap with temporary
        return *this;  // Old data destroyed with temporary
    }

    // Strong exception guarantee
    // Self-assignment safe
    // Reuses copy constructor logic
};
```

---

## Rule of Five (C++11)

```cpp
// Add move semantics for performance
class Buffer {
private:
    uint8_t* data;
    size_t size;

public:
    // Constructor
    explicit Buffer(size_t s)
        : data(new uint8_t[s]), size(s) {}

    // 1. Destructor
    ~Buffer() { delete[] data; }

    // 2. Copy constructor
    Buffer(const Buffer& other);

    // 3. Copy assignment
    Buffer& operator=(const Buffer& other);

    // 4. Move constructor
    Buffer(Buffer&& other) noexcept
        : data(other.data), size(other.size) {
        other.data = nullptr;
        other.size = 0;
    }

    // 5. Move assignment
    Buffer& operator=(Buffer&& other) noexcept {
        if (this != &other) {
            delete[] data;
            data = other.data;
            size = other.size;
            other.data = nullptr;
            other.size = 0;
        }
        return *this;
    }
};
```

---

## Rule of Zero

```cpp
// Prefer Rule of Zero - let compiler generate everything
class SerialPort {
private:
    // Use RAII types that manage themselves
    FileDescriptor fd;
    std::array<uint8_t, 256> rxBuffer;
    std::array<uint8_t, 256> txBuffer;
    Config config;

public:
    SerialPort(const char* device, const Config& cfg)
        : fd(device), config(cfg) {
        configure();
    }

    // No explicit destructor needed
    // No explicit copy/move operations needed
    // Compiler generates correct defaults
};

// BUT: If any member is not copyable/movable,
// the class becomes non-copyable/movable
```

---

## Deleted Functions

```cpp
// Explicitly prevent operations
class Singleton {
private:
    static Singleton* instance;

    Singleton() = default;

public:
    // Delete copy operations
    Singleton(const Singleton&) = delete;
    Singleton& operator=(const Singleton&) = delete;

    // Delete move operations
    Singleton(Singleton&&) = delete;
    Singleton& operator=(Singleton&&) = delete;

    static Singleton& getInstance() {
        if (!instance) {
            instance = new Singleton();
        }
        return *instance;
    }
};

// Usage
auto& s1 = Singleton::getInstance();
// auto s2 = s1;  // Error: copy deleted
```

---

## Smart Pointers for Embedded

```cpp
// Unique ownership without heap allocation
template<typename T>
class StaticUnique {
private:
    alignas(T) uint8_t storage[sizeof(T)];
    bool initialized{false};

public:
    template<typename... Args>
    void emplace(Args&&... args) {
        if (initialized) {
            get()->~T();
        }
        new(storage) T(std::forward<Args>(args)...);
        initialized = true;
    }

    ~StaticUnique() {
        if (initialized) {
            get()->~T();
        }
    }

    T* get() {
        return initialized ?
            reinterpret_cast<T*>(storage) : nullptr;
    }

    T* operator->() { return get(); }
    T& operator*() { return *get(); }
};
```

---

## Reference Counting

```cpp
// Simple intrusive reference counting
class RefCounted {
private:
    mutable uint32_t refCount{0};

public:
    void addRef() const { ++refCount; }

    void release() const {
        if (--refCount == 0) {
            delete this;
        }
    }

protected:
    virtual ~RefCounted() = default;
};

template<typename T>
class IntrusivePtr {
private:
    T* ptr{nullptr};

public:
    explicit IntrusivePtr(T* p = nullptr) : ptr(p) {
        if (ptr) ptr->addRef();
    }

    ~IntrusivePtr() {
        if (ptr) ptr->release();
    }

    IntrusivePtr(const IntrusivePtr& other)
        : ptr(other.ptr) {
        if (ptr) ptr->addRef();
    }

    IntrusivePtr& operator=(const IntrusivePtr& other) {
        if (ptr != other.ptr) {
            if (ptr) ptr->release();
            ptr = other.ptr;
            if (ptr) ptr->addRef();
        }
        return *this;
    }

    T* operator->() const { return ptr; }
    T& operator*() const { return *ptr; }
};
```

---

## Custom Deleters

```cpp
// Resource cleanup without heap allocation
template<typename T, typename Deleter>
class UniqueResource {
private:
    T resource;
    Deleter deleter;
    bool owned{true};

public:
    UniqueResource(T res, Deleter del)
        : resource(res), deleter(del) {}

    ~UniqueResource() {
        if (owned) deleter(resource);
    }

    // Move only
    UniqueResource(UniqueResource&& other) noexcept
        : resource(std::move(other.resource))
        , deleter(std::move(other.deleter))
        , owned(other.owned) {
        other.owned = false;
    }

    T& get() { return resource; }
    T release() { owned = false; return resource; }
};

// Usage
auto spi = UniqueResource(
    SPI1,
    [](SPI_TypeDef* s) { s->CR1 &= ~SPI_CR1_SPE; }
);
```

---

## Memory Pool with RAII

```cpp
template<typename T, size_t N>
class MemoryPool {
private:
    struct Block {
        alignas(T) uint8_t data[sizeof(T)];
        bool used{false};
    };

    std::array<Block, N> blocks;

public:
    class Ptr {
    private:
        T* ptr{nullptr};
        MemoryPool* pool{nullptr};

    public:
        Ptr() = default;
        Ptr(T* p, MemoryPool* mp) : ptr(p), pool(mp) {}

        ~Ptr() {
            if (ptr && pool) {
                pool->deallocate(ptr);
            }
        }

        // Move only
        Ptr(Ptr&& other) noexcept
            : ptr(other.ptr), pool(other.pool) {
            other.ptr = nullptr;
            other.pool = nullptr;
        }

        T* operator->() { return ptr; }
        T& operator*() { return *ptr; }
    };

    template<typename... Args>
    Ptr allocate(Args&&... args) {
        for (auto& block : blocks) {
            if (!block.used) {
                block.used = true;
                T* obj = new(block.data) T(std::forward<Args>(args)...);
                return Ptr(obj, this);
            }
        }
        return Ptr();  // Allocation failed
    }

private:
    void deallocate(T* ptr) {
        ptr->~T();
        // Find and mark block as free
        auto addr = reinterpret_cast<uint8_t*>(ptr);
        for (auto& block : blocks) {
            if (block.data == addr) {
                block.used = false;
                break;
            }
        }
    }
};
```

---

## Scope Guards

```cpp
// Execute action on scope exit
template<typename F>
class ScopeGuard {
private:
    F func;
    bool active{true};

public:
    explicit ScopeGuard(F f) : func(std::move(f)) {}

    ~ScopeGuard() {
        if (active) func();
    }

    void dismiss() { active = false; }

    // Non-copyable
    ScopeGuard(const ScopeGuard&) = delete;
    ScopeGuard& operator=(const ScopeGuard&) = delete;
};

// Helper function
template<typename F>
auto makeScopeGuard(F&& f) {
    return ScopeGuard<std::decay_t<F>>(std::forward<F>(f));
}

// Usage
void processData() {
    acquireResource();
    auto guard = makeScopeGuard([]{ releaseResource(); });

    // Process...
    if (error) return;  // Resource automatically released

    // Success path
    guard.dismiss();  // Don't release
    // Manual release with different parameters
}
```

---

## Lock Guards

```cpp
// Mutex wrapper with RAII
class Mutex {
private:
    volatile uint32_t locked{0};

public:
    void lock() {
        while (__atomic_test_and_set(&locked, __ATOMIC_ACQUIRE)) {
            __WFE();  // Wait for event
        }
    }

    void unlock() {
        __atomic_clear(&locked, __ATOMIC_RELEASE);
        __SEV();  // Send event
    }

    bool tryLock() {
        return !__atomic_test_and_set(&locked, __ATOMIC_ACQUIRE);
    }
};

// RAII lock guard
template<typename Mutex>
class LockGuard {
private:
    Mutex& mutex;

public:
    explicit LockGuard(Mutex& m) : mutex(m) {
        mutex.lock();
    }

    ~LockGuard() {
        mutex.unlock();
    }

    // Non-copyable, non-movable
    LockGuard(const LockGuard&) = delete;
    LockGuard& operator=(const LockGuard&) = delete;
};

// Usage
Mutex dataMutex;
void updateData() {
    LockGuard<Mutex> lock(dataMutex);
    // Critical section
}  // Automatically unlocked
```

---

## String Management

```cpp
// Fixed-capacity string with SSO
template<size_t N>
class FixedString {
private:
    char buffer[N];
    size_t length{0};

public:
    FixedString() { buffer[0] = '\0'; }

    FixedString(const char* str) {
        length = 0;
        while (str[length] && length < N - 1) {
            buffer[length] = str[length];
            length++;
        }
        buffer[length] = '\0';
    }

    FixedString(const FixedString& other) = default;
    FixedString& operator=(const FixedString& other) = default;

    // String operations
    FixedString& operator+=(const char* str) {
        size_t i = 0;
        while (str[i] && length < N - 1) {
            buffer[length++] = str[i++];
        }
        buffer[length] = '\0';
        return *this;
    }

    const char* c_str() const { return buffer; }
    size_t size() const { return length; }
    size_t capacity() const { return N - 1; }
};

// Usage
FixedString<64> message("Error: ");
message += "Sensor timeout";
```

---

## Container Resource Management

```cpp
// Vector with inline storage
template<typename T, size_t N>
class InlineVector {
private:
    alignas(T) uint8_t storage[N * sizeof(T)];
    size_t count{0};

public:
    ~InlineVector() {
        clear();
    }

    void push_back(const T& value) {
        if (count < N) {
            new(&storage[count * sizeof(T)]) T(value);
            ++count;
        }
    }

    void push_back(T&& value) {
        if (count < N) {
            new(&storage[count * sizeof(T)]) T(std::move(value));
            ++count;
        }
    }

    template<typename... Args>
    void emplace_back(Args&&... args) {
        if (count < N) {
            new(&storage[count * sizeof(T)]) T(std::forward<Args>(args)...);
            ++count;
        }
    }

    void clear() {
        for (size_t i = 0; i < count; ++i) {
            reinterpret_cast<T*>(&storage[i * sizeof(T)])->~T();
        }
        count = 0;
    }

    T& operator[](size_t i) {
        return *reinterpret_cast<T*>(&storage[i * sizeof(T)]);
    }
};
```

---

## Perfect Forwarding

```cpp
// Resource factory with perfect forwarding
class ResourceManager {
private:
    struct Resource {
        uint32_t id;
        uint8_t* data;
        size_t size;

        Resource(uint32_t i, size_t s)
            : id(i), data(new uint8_t[s]), size(s) {}

        ~Resource() { delete[] data; }

        // Move constructor
        Resource(Resource&& other) noexcept
            : id(other.id), data(other.data), size(other.size) {
            other.data = nullptr;
        }
    };

    std::array<Resource*, 10> resources{nullptr};

public:
    template<typename... Args>
    Resource* create(size_t slot, Args&&... args) {
        if (slot >= resources.size()) return nullptr;

        delete resources[slot];  // Clean up old
        resources[slot] = new Resource(std::forward<Args>(args)...);
        return resources[slot];
    }

    ~ResourceManager() {
        for (auto* res : resources) {
            delete res;
        }
    }
};
```

---

## Move Semantics Optimization

```cpp
// Efficient buffer swapping
class DataBuffer {
private:
    uint8_t* data;
    size_t size;
    size_t capacity;

public:
    // Move constructor - O(1)
    DataBuffer(DataBuffer&& other) noexcept
        : data(other.data)
        , size(other.size)
        , capacity(other.capacity) {
        other.data = nullptr;
        other.size = 0;
        other.capacity = 0;
    }

    // Move assignment with swap
    DataBuffer& operator=(DataBuffer&& other) noexcept {
        swap(other);
        return *this;
    }

    void swap(DataBuffer& other) noexcept {
        std::swap(data, other.data);
        std::swap(size, other.size);
        std::swap(capacity, other.capacity);
    }
};

// Enable ADL
void swap(DataBuffer& a, DataBuffer& b) noexcept {
    a.swap(b);
}
```

---

## Copy Elision

```cpp
// Return Value Optimization (RVO)
class Matrix {
private:
    float data[16];

public:
    Matrix() = default;

    // Named RVO
    static Matrix identity() {
        Matrix m;
        for (int i = 0; i < 4; ++i) {
            m.data[i * 4 + i] = 1.0f;
        }
        return m;  // NRVO applies
    }

    // Guaranteed copy elision (C++17)
    static Matrix multiply(const Matrix& a, const Matrix& b) {
        return Matrix(a, b);  // Direct construction
    }

private:
    Matrix(const Matrix& a, const Matrix& b) {
        // Multiply matrices
    }
};

// Usage - no copies
Matrix m = Matrix::identity();
```

---

## Resource Pools

```cpp
// Type-erased resource pool
class ResourcePool {
private:
    struct ResourceBase {
        virtual ~ResourceBase() = default;
        virtual void reset() = 0;
    };

    template<typename T>
    struct Resource : ResourceBase {
        T object;
        bool inUse{false};

        template<typename... Args>
        Resource(Args&&... args)
            : object(std::forward<Args>(args)...) {}

        void reset() override {
            object.reset();
            inUse = false;
        }
    };

    std::array<std::unique_ptr<ResourceBase>, 32> pool;

public:
    template<typename T, typename... Args>
    T* acquire(Args&&... args) {
        // Find existing free resource
        for (auto& res : pool) {
            if (res && !static_cast<Resource<T>*>(res.get())->inUse) {
                auto* r = static_cast<Resource<T>*>(res.get());
                r->inUse = true;
                return &r->object;
            }
        }

        // Create new resource
        for (auto& res : pool) {
            if (!res) {
                res = std::make_unique<Resource<T>>(
                    std::forward<Args>(args)...);
                return &static_cast<Resource<T>*>(res.get())->object;
            }
        }

        return nullptr;  // Pool full
    }
};
```

---

## Exception Safety Levels

```cpp
// Strong exception guarantee example
template<typename T>
class SafeVector {
private:
    T* data{nullptr};
    size_t size{0};
    size_t capacity{0};

    void swap(SafeVector& other) noexcept {
        std::swap(data, other.data);
        std::swap(size, other.size);
        std::swap(capacity, other.capacity);
    }

public:
    void push_back(const T& value) {
        if (size == capacity) {
            // Strong guarantee - create new buffer first
            size_t newCap = capacity ? capacity * 2 : 1;
            T* newData = new T[newCap];

            // Copy construct elements
            size_t i = 0;
            try {
                for (; i < size; ++i) {
                    new(&newData[i]) T(data[i]);
                }
                new(&newData[size]) T(value);
            } catch (...) {
                // Clean up on exception
                while (i > 0) {
                    newData[--i].~T();
                }
                delete[] newData;
                throw;
            }

            // Success - swap buffers
            SafeVector temp;
            temp.data = newData;
            temp.size = size + 1;
            temp.capacity = newCap;
            swap(temp);
        } else {
            // Simple case
            new(&data[size]) T(value);
            ++size;
        }
    }
};
```

---

## noexcept and Move Operations

```cpp
// Optimize with noexcept
class Buffer {
private:
    uint8_t* data;
    size_t size;

public:
    // Move constructor should be noexcept
    Buffer(Buffer&& other) noexcept
        : data(std::exchange(other.data, nullptr))
        , size(std::exchange(other.size, 0)) {}

    // Move assignment should be noexcept
    Buffer& operator=(Buffer&& other) noexcept {
        if (this != &other) {
            delete[] data;
            data = std::exchange(other.data, nullptr);
            size = std::exchange(other.size, 0);
        }
        return *this;
    }

    // Swap should be noexcept
    void swap(Buffer& other) noexcept {
        std::swap(data, other.data);
        std::swap(size, other.size);
    }
};

// Check if operations are noexcept
static_assert(std::is_nothrow_move_constructible_v<Buffer>);
static_assert(std::is_nothrow_move_assignable_v<Buffer>);
```

---

## Resource Lifetime Tracking

```cpp
// Debug resource tracking
#ifdef DEBUG
class ResourceTracker {
private:
    static inline std::array<const char*, 100> resources;
    static inline size_t count{0};

public:
    static void track(const char* name) {
        if (count < resources.size()) {
            resources[count++] = name;
        }
    }

    static void untrack(const char* name) {
        for (size_t i = 0; i < count; ++i) {
            if (resources[i] == name) {
                resources[i] = resources[--count];
                return;
            }
        }
    }

    static void report() {
        if (count > 0) {
            printf("Leaked resources:\n");
            for (size_t i = 0; i < count; ++i) {
                printf("  %s\n", resources[i]);
            }
        }
    }
};

#define TRACK_RESOURCE(name) ResourceTracker::track(name)
#define UNTRACK_RESOURCE(name) ResourceTracker::untrack(name)
#else
#define TRACK_RESOURCE(name)
#define UNTRACK_RESOURCE(name)
#endif
```

---

## Best Practices

1. **Use RAII** for all resources
1. **Follow Rule of Zero** when possible
1. **Make move operations noexcept**
1. **Avoid naked new/delete**
1. **Use smart pointers** appropriately
1. **Design for exception safety**

---

## Common Pitfalls

```cpp
// BAD: Exception unsafe
class Bad {
    int* p1;
    int* p2;
public:
    Bad() : p1(new int), p2(new int) {}  // Leak if p2 throws
};

// GOOD: Exception safe
class Good {
    std::unique_ptr<int> p1;
    std::unique_ptr<int> p2;
public:
    Good() : p1(std::make_unique<int>()),
             p2(std::make_unique<int>()) {}  // Safe
};

// BAD: Self-assignment unsafe
Bad& operator=(const Bad& other) {
    delete p1;  // Oops if this == &other
    p1 = new int(*other.p1);
    return *this;
}
```

---

## Summary

1. RAII ensures automatic resource management
1. Rule of Three/Five/Zero guides class design
1. Smart pointers prevent memory leaks
1. Move semantics enable efficient transfers
1. Exception safety requires careful design

---

## Key Takeaways

1. **Constructor acquires**, destructor releases
1. **Compiler-generated** functions often sufficient
1. **Smart pointers** manage ownership
1. **noexcept** enables optimizations
1. **Test** resource management thoroughly
