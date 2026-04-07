# Statics and Globals

## Understanding Storage Classes

Storage classes determine the lifetime, scope, and linkage of variables in C++

**Four main storage classes:**
- **Automatic** - local variables (default)
- **Static** - persists for program duration
- **Dynamic** - heap allocated with new/delete
- **Thread-local** - per-thread storage (C++11)

Each storage class has different initialization, destruction, and visibility rules

---

## Storage Class Overview

```cpp
// Automatic storage (stack)
void function() {
    int local = 42;  // Created when function called
}                    // Destroyed when function exits

// Static storage (data segment)
static int staticVar = 100;  // Initialized once, lives until program ends

// Dynamic storage (heap)
int* dynamic = new int(200);  // Explicit allocation
delete dynamic;               // Explicit deallocation

// Thread-local storage (C++11)
thread_local int tlsVar = 300;  // One instance per thread
```

---

## Static Local Variables

Static local variables retain their value between function calls:

```cpp
int getNextId() {
    static int counter = 0;  // Initialized only once
    return ++counter;
}

void demonstrateStaticLocal() {
    std::cout << getNextId() << std::endl;  // 1
    std::cout << getNextId() << std::endl;  // 2
    std::cout << getNextId() << std::endl;  // 3

    // counter retains its value between calls
}

// Thread-safe since C++11
int getThreadSafeId() {
    static int counter = 0;
    static std::mutex mtx;

    std::lock_guard<std::mutex> lock(mtx);
    return ++counter;
}
```

---

## Static Local Initialization

Static locals are initialized on first use (lazy initialization):

```cpp
class Logger {
public:
    Logger() { std::cout << "Logger created" << std::endl; }
    void log(const std::string& msg) {
        std::cout << "[LOG] " << msg << std::endl;
    }
};

Logger& getLogger() {
    static Logger instance;  // Created on first call
    return instance;         // Destroyed at program exit
}

void example() {
    std::cout << "Before first call" << std::endl;
    getLogger().log("First message");   // Logger created here
    getLogger().log("Second message");  // Uses existing instance
}
```

---

## Static Class Members

Static members belong to the class, not to any specific instance:

```cpp
class BankAccount {
private:
    static double interestRate;  // Shared by all instances
    static int nextAccountId;    // Shared counter

    int accountId;
    double balance;

public:
    BankAccount(double initialBalance)
        : accountId(++nextAccountId), balance(initialBalance) {}

    static void setInterestRate(double rate) {
        interestRate = rate;  // No 'this' pointer in static methods
    }

    static double getInterestRate() {
        return interestRate;
    }

    double calculateInterest() const {
        return balance * interestRate;  // Access static from non-static
    }

    int getId() const { return accountId; }
};
```

---

## Static Member Definition

Static data members must be defined outside the class:

```cpp
// In header file (.h)
class Counter {
private:
    static int count;

public:
    Counter() { ++count; }
    ~Counter() { --count; }
    static int getCount() { return count; }
};

// In source file (.cpp)
int Counter::count = 0;  // Definition and initialization

// Usage
void example() {
    std::cout << Counter::getCount() << std::endl;  // 0

    Counter c1;
    std::cout << Counter::getCount() << std::endl;  // 1

    {
        Counter c2, c3;
        std::cout << Counter::getCount() << std::endl;  // 3
    }  // c2 and c3 destroyed

    std::cout << Counter::getCount() << std::endl;  // 1
}
```

---

## Inline Static Members (C++17)

C++17 allows inline static data members:

```cpp
class ModernCounter {
private:
    inline static int count = 0;  // Definition in class (C++17)

public:
    ModernCounter() { ++count; }
    ~ModernCounter() { --count; }
    static int getCount() { return count; }
};

// No separate definition needed!

class Configuration {
public:
    inline static std::string appName = "MyApp";
    inline static int version = 1;
    inline static bool debugMode = false;

    // Complex types work too
    inline static std::vector<std::string> supportedFormats = {
        "json", "xml", "yaml"
    };
};
```

---

## Stateless Classes

Classes that contain only static members and functions:

```cpp
class MathUtils {
public:
    static double pi() { return 3.14159265359; }
    static double e()  { return 2.71828182846; }

    static double toDegrees(double radians) {
        return radians * 180.0 / pi();
    }

    static double toRadians(double degrees) {
        return degrees * pi() / 180.0;
    }

    static double power(double base, int exponent) {
        double result = 1.0;
        for (int i = 0; i < exponent; ++i) {
            result *= base;
        }
        return result;
    }

    // Private constructor prevents instantiation
private:
    MathUtils() = delete;
    MathUtils(const MathUtils&) = delete;
    MathUtils& operator=(const MathUtils&) = delete;
};
```

---

## Static vs Namespace Functions

Stateless classes vs namespaces for utility functions:

```cpp
// Stateless class approach
class StringUtils {
public:
    static std::string toUpper(const std::string& str);
    static std::string toLower(const std::string& str);
    static bool startsWith(const std::string& str, const std::string& prefix);
private:
    StringUtils() = delete;
};

// Namespace approach (often preferred)
namespace string_utils {
    std::string toUpper(const std::string& str);
    std::string toLower(const std::string& str);
    bool startsWith(const std::string& str, const std::string& prefix);
}

// Usage comparison
void example() {
    std::string text = "Hello World";

    // Class approach
    auto upper1 = StringUtils::toUpper(text);

    // Namespace approach
    auto upper2 = string_utils::toUpper(text);
}
```

---

## Global Variables Problems

Global variables can cause numerous issues:

```cpp
// Global variables - problematic
int globalCounter = 0;
std::string globalConfig = "default";
std::vector<int> globalData;

void function1() {
    globalCounter++;  // Who else modifies this?
    globalData.push_back(globalCounter);
}

void function2() {
    globalCounter *= 2;  // Unexpected side effect!
    globalConfig = "modified";
}

// Problems:
// 1. Hard to track who modifies globals
// 2. Makes testing difficult
// 3. Order of initialization issues
// 4. Thread safety concerns
// 5. Tight coupling between modules
```

---

## Static Initialization Order Fiasco

Global static objects can have undefined initialization order:

```cpp
// File1.cpp
class Logger {
public:
    Logger() { std::cout << "Logger initialized" << std::endl; }
    void log(const std::string& msg) { /* ... */ }
};

Logger globalLogger;  // When is this initialized?

// File2.cpp
class Database {
public:
    Database() {
        globalLogger.log("Database initialized");  // DANGER!
        // globalLogger might not be initialized yet!
    }
};

Database globalDB;  // Order with globalLogger is undefined!
```

---

## Solving Initialization Order Issues

Use functions to control initialization order:

```cpp
// File1.cpp
Logger& getLogger() {
    static Logger instance;  // Initialized on first use
    return instance;
}

// File2.cpp
Database& getDatabase() {
    static Database instance;
    return instance;
}

Database::Database() {
    getLogger().log("Database initialized");  // Safe!
    // Logger is guaranteed to be initialized
}

// Usage
void someFunction() {
    getDatabase().query("SELECT * FROM users");
    // Both Logger and Database are properly initialized
}
```

---

## Safe Global Variables

Make globals safe through encapsulation:

```cpp
class ApplicationConfig {
private:
    std::string appName = "DefaultApp";
    int version = 1;
    bool debugMode = false;
    mutable std::mutex configMutex;

    ApplicationConfig() = default;  // Private constructor

public:
    // Non-copyable, non-movable
    ApplicationConfig(const ApplicationConfig&) = delete;
    ApplicationConfig& operator=(const ApplicationConfig&) = delete;

    static ApplicationConfig& getInstance() {
        static ApplicationConfig instance;
        return instance;
    }

    void setAppName(const std::string& name) {
        std::lock_guard<std::mutex> lock(configMutex);
        appName = name;
    }

    std::string getAppName() const {
        std::lock_guard<std::mutex> lock(configMutex);
        return appName;
    }

    void setDebugMode(bool debug) {
        std::lock_guard<std::mutex> lock(configMutex);
        debugMode = debug;
    }

    bool isDebugMode() const {
        std::lock_guard<std::mutex> lock(configMutex);
        return debugMode;
    }
};
```

---

## The Singleton Pattern

Singleton ensures only one instance of a class exists:

```cpp
class Singleton {
private:
    Singleton() = default;

public:
    // Delete copy constructor and assignment
    Singleton(const Singleton&) = delete;
    Singleton& operator=(const Singleton&) = delete;

    // Delete move constructor and assignment
    Singleton(Singleton&&) = delete;
    Singleton& operator=(Singleton&&) = delete;

    static Singleton& getInstance() {
        static Singleton instance;  // Thread-safe since C++11
        return instance;
    }

    void doSomething() {
        std::cout << "Singleton doing work" << std::endl;
    }
};

// Usage
void example() {
    auto& singleton = Singleton::getInstance();
    singleton.doSomething();

    // auto copy = singleton;  // ERROR: deleted copy constructor
}
```

---

## Thread-Safe Singleton (Pre-C++11)

Before C++11, manual synchronization was needed:

```cpp
class ThreadSafeSingleton {
private:
    static ThreadSafeSingleton* instance;
    static std::mutex instanceMutex;

    ThreadSafeSingleton() = default;

public:
    ThreadSafeSingleton(const ThreadSafeSingleton&) = delete;
    ThreadSafeSingleton& operator=(const ThreadSafeSingleton&) = delete;

    static ThreadSafeSingleton& getInstance() {
        // Double-checked locking pattern
        if (instance == nullptr) {
            std::lock_guard<std::mutex> lock(instanceMutex);
            if (instance == nullptr) {
                instance = new ThreadSafeSingleton();
            }
        }
        return *instance;
    }

    void doWork() { /* ... */ }
};

// Static member definitions
ThreadSafeSingleton* ThreadSafeSingleton::instance = nullptr;
std::mutex ThreadSafeSingleton::instanceMutex;
```

---

## Singleton with Parameters

Singletons with initialization parameters:

```cpp
class ConfigurableSingleton {
private:
    std::string config;
    bool initialized = false;

    ConfigurableSingleton() = default;

public:
    ConfigurableSingleton(const ConfigurableSingleton&) = delete;
    ConfigurableSingleton& operator=(const ConfigurableSingleton&) = delete;

    static ConfigurableSingleton& getInstance() {
        static ConfigurableSingleton instance;
        return instance;
    }

    void initialize(const std::string& configuration) {
        if (initialized) {
            throw std::runtime_error("Already initialized");
        }
        config = configuration;
        initialized = true;
    }

    const std::string& getConfig() const {
        if (!initialized) {
            throw std::runtime_error("Not initialized");
        }
        return config;
    }
};

// Usage
void initializeApp() {
    ConfigurableSingleton::getInstance().initialize("production");
}

void useApp() {
    auto config = ConfigurableSingleton::getInstance().getConfig();
    std::cout << "Config: " << config << std::endl;
}
```

---

## Singleton Registry Pattern

Manage multiple named singletons:

```cpp
template<typename T>
class SingletonRegistry {
private:
    static std::unordered_map<std::string, std::unique_ptr<T>> instances;
    static std::mutex registryMutex;

public:
    template<typename... Args>
    static T& getInstance(const std::string& name, Args&&... args) {
        std::lock_guard<std::mutex> lock(registryMutex);

        auto it = instances.find(name);
        if (it == instances.end()) {
            instances[name] = std::make_unique<T>(std::forward<Args>(args)...);
        }

        return *instances[name];
    }

    static bool exists(const std::string& name) {
        std::lock_guard<std::mutex> lock(registryMutex);
        return instances.find(name) != instances.end();
    }

    static void remove(const std::string& name) {
        std::lock_guard<std::mutex> lock(registryMutex);
        instances.erase(name);
    }
};

template<typename T>
std::unordered_map<std::string, std::unique_ptr<T>> SingletonRegistry<T>::instances;

template<typename T>
std::mutex SingletonRegistry<T>::registryMutex;
```

---

## Problems with Singleton

Singleton pattern has several drawbacks:

**Testing Issues:**
```cpp
class DatabaseSingleton {
    // Hard to mock for testing
    // Global state affects test isolation
public:
    void saveUser(const User& user) { /* real database */ }
};

// Better: Dependency injection
class UserService {
private:
    IDatabase* database;  // Interface for easy mocking

public:
    UserService(IDatabase* db) : database(db) {}
    void saveUser(const User& user) { database->save(user); }
};
```

**Hidden Dependencies:**
```cpp
void processOrder(const Order& order) {
    // Hidden dependency on Logger singleton
    Logger::getInstance().log("Processing order");
    // Better: explicit dependency
    // void processOrder(const Order& order, ILogger& logger)
}
```

---

## Alternatives to Singleton

Consider these alternatives before using Singleton:

**Dependency Injection:**
```cpp
class Application {
private:
    std::unique_ptr<ILogger> logger;
    std::unique_ptr<IDatabase> database;

public:
    Application(std::unique_ptr<ILogger> logger,
                std::unique_ptr<IDatabase> database)
        : logger(std::move(logger)), database(std::move(database)) {}
    void run() {
        logger->log("Application starting");
        // Use injected dependencies
    }
};
```

**Factory Pattern:**
```cpp
class ServiceFactory {
public:
    static std::unique_ptr<ILogger> createLogger() {
        return std::make_unique<FileLogger>("app.log");
    }
    static std::unique_ptr<IDatabase> createDatabase() {
        return std::make_unique<SqliteDatabase>("app.db");
    }
};
```

---

## Global Access Without Globals

Provide global-like access without global state:

```cpp
class ServiceLocator {
private:
    std::unordered_map<std::string, std::any> services;

public:
    template<typename T>
    void registerService(const std::string& name, std::unique_ptr<T> service) {
        services[name] = std::move(service);
    }

    template<typename T>
    T& getService(const std::string& name) {
        auto it = services.find(name);
        if (it == services.end()) {
            throw std::runtime_error("Service not found: " + name);
        }

        return *std::any_cast<std::unique_ptr<T>&>(it->second);
    }
};

// Usage
void setupServices(ServiceLocator& locator) {
    locator.registerService<ILogger>("logger",
        std::make_unique<FileLogger>("app.log"));
    locator.registerService<IDatabase>("database",
        std::make_unique<SqliteDatabase>("app.db"));
}

void useServices(ServiceLocator& locator) {
    auto& logger = locator.getService<ILogger>("logger");
    logger.log("Using service locator");
}
```

---

## RAII and Static Resources

Use RAII to manage static resources safely:

```cpp
class FileManager {
private:
    std::string filename;
    std::fstream file;

public:
    FileManager(const std::string& name) : filename(name) {
        file.open(filename, std::ios::in | std::ios::out | std::ios::app);
        if (!file.is_open()) {
            throw std::runtime_error("Cannot open file: " + filename);
        }
    }

    ~FileManager() {
        if (file.is_open()) {
            file.close();
        }
    }

    void write(const std::string& data) {
        file << data << std::endl;
        file.flush();
    }
};

FileManager& getLogFile() {
    static FileManager logFile("application.log");
    return logFile;  // Automatically cleaned up at program exit
}
```

---

## Thread-Local Storage

Each thread gets its own instance:

```cpp
class ThreadLocalLogger {
private:
    thread_local static std::unique_ptr<ThreadLocalLogger> instance;
    std::ostringstream buffer;
    std::thread::id threadId;

    ThreadLocalLogger() : threadId(std::this_thread::get_id()) {}

public:
    static ThreadLocalLogger& getInstance() {
        if (!instance) {
            instance = std::unique_ptr<ThreadLocalLogger>(new ThreadLocalLogger());
        }
        return *instance;
    }

    void log(const std::string& message) {
        buffer << "[Thread " << threadId << "] " << message << std::endl;
    }

    std::string getLog() const {
        return buffer.str();
    }

    void clearLog() {
        buffer.str("");
        buffer.clear();
    }
};

thread_local std::unique_ptr<ThreadLocalLogger> ThreadLocalLogger::instance;
```

---

## Thread-Local Example

```cpp
void workerFunction(int workerId) {
    auto& logger = ThreadLocalLogger::getInstance();

    for (int i = 0; i < 5; ++i) {
        logger.log("Worker " + std::to_string(workerId) +
                  " iteration " + std::to_string(i));
        std::this_thread::sleep_for(std::chrono::milliseconds(100));
    }

    std::cout << "Worker " << workerId << " log:\n"
              << logger.getLog() << std::endl;
}

void demonstrateThreadLocal() {
    std::vector<std::thread> threads;

    for (int i = 0; i < 3; ++i) {
        threads.emplace_back(workerFunction, i);
    }

    for (auto& t : threads) {
        t.join();
    }

    // Each thread has its own logger instance
}
```

---

## Static Analysis and Global State

Tools to analyze global state usage:

```cpp
// Use static analysis tools to find:

// 1. Global variables
int globalVar = 42;  // Flag: global variable

// 2. Singleton usage
auto& singleton = MySingleton::getInstance();  // Flag: singleton access

// 3. Static local variables
int getCounter() {
    static int count = 0;  // Flag: static local
    return ++count;
}

// 4. Thread-local variables
thread_local int tlsVar = 0;  // Flag: thread-local storage

// Consider tools like:
// - clang-static-analyzer
// - PVS-Studio
// - SonarQube
// - Custom linting rules
```

---

## Global State in Libraries

Best practices for library design:

```cpp
// Bad: Library with global state
namespace BadLibrary {
    static Config globalConfig;

    void initialize(const Config& config) {
        globalConfig = config;  // Global state!
    }

    void doWork() {
        // Uses global config
    }
}

// Good: Stateless library
namespace GoodLibrary {
    class Context {
    private:
        Config config;

    public:
        Context(const Config& cfg) : config(cfg) {}
        void doWork() { /* Use this->config */ }
    };

    std::unique_ptr<Context> createContext(const Config& config) {
        return std::make_unique<Context>(config);
    }
}
```

---

## Memory Layout of Static Variables

Understanding where static variables are stored:

```xml
![memory_layout_of_static_variables](../../../../../svg/courses/languages/c++/modern-c++-for-c-programmers/11_statics_and_globals/memory_layout_of_static_variables.svg)
```

```cpp
static int initializedStatic = 42;    // .data segment
static int uninitializedStatic;       // .bss segment

void function() {
    static int localStatic = 100;     // .data segment
    int localVar = 200;               // Stack
    int* heapVar = new int(300);      // Heap
}
```

---

## Performance Implications

Static variables have performance characteristics:

**Advantages:**
- No allocation/deallocation overhead
- CPU cache friendly (predictable memory location)
- No constructor/destructor calls for POD types

**Disadvantages:**
- Thread synchronization overhead for shared access
- Increased memory usage (exists for program lifetime)
- Potential cache line contention in multi-threaded code

```cpp
// Cache-friendly access
static std::array<int, 1000> staticArray = {};

void processData() {
    // Array is always in same memory location
    // Good for CPU cache prediction
    for (int& value : staticArray) {
        value *= 2;
    }
}
```

---

## Debugging Static Variables

Techniques for debugging static variable issues:

```cpp
class DebuggableCounter {
private:
    static int count;
    static bool debugMode;

public:
    static void enableDebug(bool enable = true) {
        debugMode = enable;
    }

    DebuggableCounter() {
        ++count;
        if (debugMode) {
            std::cout << "Counter created, total: " << count
                      << " at " << this << std::endl;
        }
    }

    ~DebuggableCounter() {
        --count;
        if (debugMode) {
            std::cout << "Counter destroyed, remaining: " << count
                      << " was at " << this << std::endl;
        }
    }

    static int getCount() { return count; }
};

// Usage
int main() {
    DebuggableCounter::enableDebug();
    // Now you can track all creations/destructions
}
```

---

## Best Practices Summary

**Do:**
- Use static local variables for lazy initialization
- Prefer dependency injection over singletons
- Use thread_local for per-thread data
- Make static members const when possible
- Use RAII for static resource management

**Don't:**
- Create global variables for mutable state
- Use singleton as a global variable replacement
- Rely on static initialization order between translation units
- Forget thread safety for shared static data
- Use static members for utility functions (prefer namespaces)

---

## Refactoring Global State

Transform global state into better designs:

```cpp
// Before: Global state
static Database* globalDB = nullptr;
static Logger* globalLogger = nullptr;

void processUser(const User& user) {
    globalLogger->log("Processing user");
    globalDB->save(user);
}

// After: Dependency injection
class UserProcessor {
private:
    IDatabase& database;
    ILogger& logger;

public:
    UserProcessor(IDatabase& db, ILogger& log)
        : database(db), logger(log) {}

    void process(const User& user) {
        logger.log("Processing user");
        database.save(user);
    }
};

// Usage
void main() {
    FileLogger logger("app.log");
    SqliteDatabase database("users.db");

    UserProcessor processor(database, logger);
    processor.process(user);
}
```

---

## Modern C++ Static Features

C++11/14/17/20 improvements for static storage:

```cpp
// C++11: Thread-safe static initialization
Logger& getLogger() {
    static Logger instance;  // Thread-safe initialization
    return instance;
}

// C++17: Inline static variables
class Config {
public:
    inline static std::string appName = "MyApp";
    inline static std::vector<std::string> modules = {"core", "ui"};
};

// C++20: Constexpr and constinit
constexpr int compileTimeValue = 42;
constinit static int runtimeValue = getInitialValue();

// C++20: Static lambdas
auto getProcessor() {
    static auto processor = [](int x) { return x * 2; };
    return processor;
}
```

---

## Testing Strategies

Strategies for testing code with static state:

```cpp
// Testable singleton with reset capability
class TestableSingleton {
private:
    static std::unique_ptr<TestableSingleton> instance;
    int value = 0;

public:
    static TestableSingleton& getInstance() {
        if (!instance) {
            instance = std::make_unique<TestableSingleton>();
        }
        return *instance;
    }

    static void resetForTesting() {
        instance.reset();
    }

    void setValue(int v) { value = v; }
    int getValue() const { return value; }
};

// Test fixture
class SingletonTest : public ::testing::Test {
protected:
    void SetUp() override {
        TestableSingleton::resetForTesting();
    }

    void TearDown() override {
        TestableSingleton::resetForTesting();
    }
};

TEST_F(SingletonTest, ValuePersistence) {
    auto& s1 = TestableSingleton::getInstance();
    s1.setValue(42);

    auto& s2 = TestableSingleton::getInstance();
    EXPECT_EQ(s2.getValue(), 42);
}
```

---

## Static Polymorphism

Use static members for compile-time polymorphism:

```cpp
template<typename Derived>
class StaticInterface {
public:
    void doWork() {
        static_cast<Derived*>(this)->doWorkImpl();
    }

    static std::string getTypeName() {
        return Derived::getTypeNameImpl();
    }
};

class ConcreteA : public StaticInterface<ConcreteA> {
public:
    void doWorkImpl() {
        std::cout << "ConcreteA working" << std::endl;
    }

    static std::string getTypeNameImpl() {
        return "ConcreteA";
    }
};

class ConcreteB : public StaticInterface<ConcreteB> {
public:
    void doWorkImpl() {
        std::cout << "ConcreteB working" << std::endl;
    }

    static std::string getTypeNameImpl() {
        return "ConcreteB";
    }
};

// Usage
template<typename T>
void useInterface() {
    std::cout << "Working with: " << T::getTypeName() << std::endl;
    T instance;
    instance.doWork();
}
```
