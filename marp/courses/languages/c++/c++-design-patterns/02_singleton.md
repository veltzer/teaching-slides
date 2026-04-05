# Singleton Pattern

---

## Intent

- Ensure a class has only one instance
- Provide a global point of access to that instance
- Control shared resource access (e.g., database connection, configuration, logging)

---

## Classic Singleton (Pre-C++11)

```cpp
class Singleton {
private:
    static Singleton* instance;
    Singleton() = default;
    Singleton(const Singleton&) = delete;
    Singleton& operator=(const Singleton&) = delete;

public:
    static Singleton* getInstance() {
        if (instance == nullptr) {
            instance = new Singleton();
        }
        return instance;
    }
};

Singleton* Singleton::instance = nullptr;
```

**Problem**: Not thread-safe

---

## Singleton Structure

<svg width="400" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="100" y="20" width="200" height="160" fill="#e3f2fd" stroke="#1976d2" stroke-width="2" rx="4"/>
  <text x="200" y="45" text-anchor="middle" font-size="14" font-weight="bold">Singleton</text>
  <line x1="100" y1="55" x2="300" y2="55" stroke="#1976d2" stroke-width="1"/>
  <text x="115" y="75" font-size="11">- instance: Singleton</text>
  <text x="115" y="93" font-size="11">- data...</text>
  <line x1="100" y1="100" x2="300" y2="100" stroke="#1976d2" stroke-width="1"/>
  <text x="115" y="120" font-size="11">- Singleton()</text>
  <text x="115" y="138" font-size="11">+ getInstance(): Singleton&amp;</text>
  <text x="115" y="156" font-size="11">+ doSomething()</text>
</svg>

---

## Meyers' Singleton (Modern C++)

```cpp
class Singleton {
private:
    Singleton() = default;
    ~Singleton() = default;
    Singleton(const Singleton&) = delete;
    Singleton& operator=(const Singleton&) = delete;

public:
    static Singleton& getInstance() {
        static Singleton instance;
        return instance;
    }

    void doSomething() {
        // business logic
    }
};
```

- Thread-safe since C++11 (static local initialization is guaranteed thread-safe)
- No manual memory management
- Lazy initialization

---

## Singleton with Configuration

```cpp
class AppConfig {
private:
    std::unordered_map<std::string, std::string> settings;

    AppConfig() {
        // Load defaults
        settings["log_level"] = "INFO";
        settings["max_connections"] = "100";
    }

public:
    AppConfig(const AppConfig&) = delete;
    AppConfig& operator=(const AppConfig&) = delete;

    static AppConfig& getInstance() {
        static AppConfig instance;
        return instance;
    }

    std::string get(const std::string& key) const {
        auto it = settings.find(key);
        return it != settings.end() ? it->second : "";
    }

    void set(const std::string& key, const std::string& value) {
        settings[key] = value;
    }
};
```

---

## Thread-Safe Singleton with Mutex

```cpp
class ThreadSafeRegistry {
private:
    std::unordered_map<std::string, std::shared_ptr<void>> services;
    mutable std::mutex mtx;

    ThreadSafeRegistry() = default;

public:
    ThreadSafeRegistry(const ThreadSafeRegistry&) = delete;
    ThreadSafeRegistry& operator=(const ThreadSafeRegistry&) = delete;

    static ThreadSafeRegistry& getInstance() {
        static ThreadSafeRegistry instance;
        return instance;
    }

    template<typename T>
    void registerService(const std::string& name, std::shared_ptr<T> svc) {
        std::lock_guard<std::mutex> lock(mtx);
        services[name] = svc;
    }

    template<typename T>
    std::shared_ptr<T> getService(const std::string& name) {
        std::lock_guard<std::mutex> lock(mtx);
        auto it = services.find(name);
        return it != services.end()
            ? std::static_pointer_cast<T>(it->second) : nullptr;
    }
};
```

---

## Singleton: When to Use and When to Avoid

**Use when:**

- Exactly one instance must coordinate actions across the system
- Shared resources like thread pools, caches, or configuration

**Avoid when:**

- It's just a convenient global — prefer dependency injection
- Testing becomes difficult due to tight coupling
- Multiple instances might be needed in the future

**Alternatives:**

- Dependency injection
- Passing instances explicitly
- Monostate pattern (shared static state, multiple instances)

---

## Singleton vs Static Class

| Aspect | Singleton | Static Class |
|--------|-----------|-------------|
| Polymorphism | Yes | No |
| Lazy initialization | Yes | No |
| Interface implementation | Yes | No |
| Lifetime control | Yes | No |
| Testing/mocking | Easier | Harder |
| Memory | Heap or static | Static only |

Prefer Singleton when you need polymorphism or controlled initialization order
