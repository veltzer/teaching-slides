# Design Patterns

---

## What are Design Patterns?

Design patterns are reusable solutions to commonly occurring problems in software design

Key benefits:
1. **Proven solutions** - tested and refined over time
1. **Common vocabulary** - shared language for developers
1. **Design quality** - promote loose coupling and high cohesion
1. **Code reusability** - abstract solutions applicable to many contexts

```cpp
// Pattern provides structure, not just code
class SortStrategy {
public:
    virtual ~SortStrategy() = default;
    virtual void sort(std::vector<int>& data) = 0;
    virtual std::string getName() const = 0;
};

class BubbleSort : public SortStrategy {
public:
    void sort(std::vector<int>& data) override {
        std::cout << "Performing bubble sort" << std::endl;
        // Bubble sort implementation
        for (size_t i = 0; i < data.size(); ++i) {
            for (size_t j = 0; j < data.size() - 1 - i; ++j) {
                if (data[j] > data[j + 1]) {
                    std::swap(data[j], data[j + 1]);
                }
            }
        }
    }

    std::string getName() const override { return "Bubble Sort"; }
};

class QuickSort : public SortStrategy {
public:
    void sort(std::vector<int>& data) override {
        std::cout << "Performing quick sort" << std::endl;
        quickSort(data, 0, data.size() - 1);
    }

    std::string getName() const override { return "Quick Sort"; }

private:
    void quickSort(std::vector<int>& arr, int low, int high) {
        if (low < high) {
            int pi = partition(arr, low, high);
            quickSort(arr, low, pi - 1);
            quickSort(arr, pi + 1, high);
        }
    }

    int partition(std::vector<int>& arr, int low, int high) {
        int pivot = arr[high];
        int i = low - 1;
        for (int j = low; j < high; ++j) {
            if (arr[j] < pivot) {
                ++i;
                std::swap(arr[i], arr[j]);
            }
        }
        std::swap(arr[i + 1], arr[high]);
        return i + 1;
    }
};

class SortContext {
private:
    std::unique_ptr<SortStrategy> strategy;

public:
    void setStrategy(std::unique_ptr<SortStrategy> newStrategy) {
        strategy = std::move(newStrategy);
    }

    void performSort(std::vector<int>& data) {
        if (strategy) {
            std::cout << "Using " << strategy->getName() << std::endl;
            strategy->sort(data);
        }
    }
};
```

---

## Pattern Categories

![pattern_categories](/svg/courses/languages/c++/modern-c++-for-c-programmers/16_design_patterns/pattern_categories.svg)

Different patterns solve different types of problems

---

## CREATIONAL PATTERNS

---

## Factory Pattern

Encapsulate object creation logic

```cpp
enum class DatabaseType { MySQL, PostgreSQL, SQLite };

class Database {
public:
    virtual ~Database() = default;
    virtual void connect(const std::string& connectionString) = 0;
    virtual void execute(const std::string& query) = 0;
};

class MySQLDatabase : public Database {
public:
    void connect(const std::string& connectionString) override {
        std::cout << "Connecting to MySQL: " << connectionString << std::endl;
    }

    void execute(const std::string& query) override {
        std::cout << "MySQL executing: " << query << std::endl;
    }
};

class PostgreSQLDatabase : public Database {
public:
    void connect(const std::string& connectionString) override {
        std::cout << "Connecting to PostgreSQL: " << connectionString << std::endl;
    }

    void execute(const std::string& query) override {
        std::cout << "PostgreSQL executing: " << query << std::endl;
    }
};

class SQLiteDatabase : public Database {
public:
    void connect(const std::string& connectionString) override {
        std::cout << "Connecting to SQLite: " << connectionString << std::endl;
    }

    void execute(const std::string& query) override {
        std::cout << "SQLite executing: " << query << std::endl;
    }
};
```

---

## Factory Implementation

```cpp
class DatabaseFactory {
public:
    static std::unique_ptr<Database> createDatabase(DatabaseType type) {
        switch (type) {
            case DatabaseType::MySQL:
                return std::make_unique<MySQLDatabase>();
            case DatabaseType::PostgreSQL:
                return std::make_unique<PostgreSQLDatabase>();
            case DatabaseType::SQLite:
                return std::make_unique<SQLiteDatabase>();
            default:
                throw std::invalid_argument("Unknown database type");
        }
    }

    // Factory with configuration
    static std::unique_ptr<Database> createDatabase(const std::string& config) {
        if (config.find("mysql") != std::string::npos) {
            return createDatabase(DatabaseType::MySQL);
        } else if (config.find("postgresql") != std::string::npos) {
            return createDatabase(DatabaseType::PostgreSQL);
        } else if (config.find("sqlite") != std::string::npos) {
            return createDatabase(DatabaseType::SQLite);
        } else {
            throw std::invalid_argument("Cannot determine database type from config");
        }
    }
};

// Usage
void demonstrateFactory() {
    auto db1 = DatabaseFactory::createDatabase(DatabaseType::MySQL);
    auto db2 = DatabaseFactory::createDatabase("postgresql://localhost:5432");

    db1->connect("mysql://localhost:3306");
    db2->connect("postgresql://localhost:5432");
}
```

---

## Abstract Factory Pattern

Create families of related objects

```cpp
// Abstract products
class Button {
public:
    virtual ~Button() = default;
    virtual void render() = 0;
    virtual void onClick() = 0;
};

class TextField {
public:
    virtual ~TextField() = default;
    virtual void render() = 0;
    virtual void onTextChange() = 0;
};

// Concrete products for Windows
class WindowsButton : public Button {
public:
    void render() override {
        std::cout << "Rendering Windows button" << std::endl;
    }

    void onClick() override {
        std::cout << "Windows button clicked" << std::endl;
    }
};

class WindowsTextField : public TextField {
public:
    void render() override {
        std::cout << "Rendering Windows text field" << std::endl;
    }

    void onTextChange() override {
        std::cout << "Windows text field changed" << std::endl;
    }
};

// Concrete products for macOS
class MacButton : public Button {
public:
    void render() override {
        std::cout << "Rendering Mac button" << std::endl;
    }

    void onClick() override {
        std::cout << "Mac button clicked" << std::endl;
    }
};

class MacTextField : public TextField {
public:
    void render() override {
        std::cout << "Rendering Mac text field" << std::endl;
    }

    void onTextChange() override {
        std::cout << "Mac text field changed" << std::endl;
    }
};
```

---

## Abstract Factory Implementation

```cpp
// Abstract factory
class GUIFactory {
public:
    virtual ~GUIFactory() = default;
    virtual std::unique_ptr<Button> createButton() = 0;
    virtual std::unique_ptr<TextField> createTextField() = 0;
};

// Concrete factories
class WindowsFactory : public GUIFactory {
public:
    std::unique_ptr<Button> createButton() override {
        return std::make_unique<WindowsButton>();
    }

    std::unique_ptr<TextField> createTextField() override {
        return std::make_unique<WindowsTextField>();
    }
};

class MacFactory : public GUIFactory {
public:
    std::unique_ptr<Button> createButton() override {
        return std::make_unique<MacButton>();
    }

    std::unique_ptr<TextField> createTextField() override {
        return std::make_unique<MacTextField>();
    }
};

// Client code
class Application {
private:
    std::unique_ptr<GUIFactory> factory;
    std::unique_ptr<Button> button;
    std::unique_ptr<TextField> textField;

public:
    Application(std::unique_ptr<GUIFactory> f) : factory(std::move(f)) {
        button = factory->createButton();
        textField = factory->createTextField();
    }

    void render() {
        button->render();
        textField->render();
    }
};
```

---

## Builder Pattern

Construct complex objects step by step

```cpp
class Computer {
private:
    std::string cpu, gpu, ram, storage;
public:
    void setCPU(const std::string& c) { cpu = c; }
    void setGPU(const std::string& g) { gpu = g; }
    void setRAM(const std::string& r) { ram = r; }
    void setStorage(const std::string& s) { storage = s; }

    void display() const {
        std::cout << "Computer: CPU=" << cpu << ", GPU=" << gpu
                  << ", RAM=" << ram << ", Storage=" << storage << std::endl;
    }
};

class ComputerBuilder {
private:
    std::unique_ptr<Computer> computer = std::make_unique<Computer>();
public:
    ComputerBuilder& withCPU(const std::string& cpu) {
        computer->setCPU(cpu);
        return *this;
    }

    ComputerBuilder& withGPU(const std::string& gpu) {
        computer->setGPU(gpu);
        return *this;
    }

    ComputerBuilder& withRAM(const std::string& ram) {
        computer->setRAM(ram);
        return *this;
    }

    ComputerBuilder& withStorage(const std::string& storage) {
        computer->setStorage(storage);
        return *this;
    }

    std::unique_ptr<Computer> build() {
        return std::move(computer);
    }
};

// Usage
auto pc = ComputerBuilder()
    .withCPU("Intel i7")
    .withGPU("RTX 4080")
    .withRAM("32GB")
    .withStorage("1TB SSD")
    .build();
```

---

## Prototype Pattern

Clone objects instead of creating new ones

```cpp
class Prototype {
public:
    virtual ~Prototype() = default;
    virtual std::unique_ptr<Prototype> clone() const = 0;
    virtual void display() const = 0;
};

class ConcretePrototype : public Prototype {
private:
    std::string data;
    int value;
public:
    ConcretePrototype(const std::string& d, int v) : data(d), value(v) {}

    std::unique_ptr<Prototype> clone() const override {
        return std::make_unique<ConcretePrototype>(*this);
    }

    void display() const override {
        std::cout << "Data: " << data << ", Value: " << value << std::endl;
    }

    void setData(const std::string& d) { data = d; }
};

class PrototypeManager {
private:
    std::map<std::string, std::unique_ptr<Prototype>> prototypes;
public:
    void registerPrototype(const std::string& key, std::unique_ptr<Prototype> proto) {
        prototypes[key] = std::move(proto);
    }

    std::unique_ptr<Prototype> create(const std::string& key) {
        auto it = prototypes.find(key);
        if (it != prototypes.end()) {
            return it->second->clone();
        }
        return nullptr;
    }
};
```

---

## Singleton Pattern

Ensure only one instance of a class exists

```cpp
class Singleton {
private:
    static std::unique_ptr<Singleton> instance;
    static std::once_flag init_flag;

    // Private constructor
    Singleton() {
        std::cout << "Singleton instance created" << std::endl;
    }

public:
    // Delete copy constructor and assignment operator
    Singleton(const Singleton&) = delete;
    Singleton& operator=(const Singleton&) = delete;

    static Singleton& getInstance() {
        std::call_once(init_flag, []() {
            instance = std::unique_ptr<Singleton>(new Singleton());
        });
        return *instance;
    }

    void doSomething() {
        std::cout << "Singleton doing work" << std::endl;
    }
};

// Static member definitions
std::unique_ptr<Singleton> Singleton::instance = nullptr;
std::once_flag Singleton::init_flag;

// Modern C++11 thread-safe singleton (Meyer's Singleton)
class ModernSingleton {
private:
    ModernSingleton() {
        std::cout << "Modern singleton created" << std::endl;
    }

public:
    ModernSingleton(const ModernSingleton&) = delete;
    ModernSingleton& operator=(const ModernSingleton&) = delete;

    static ModernSingleton& getInstance() {
        static ModernSingleton instance;  // Thread-safe since C++11
        return instance;
    }

    void doSomething() {
        std::cout << "Modern singleton doing work" << std::endl;
    }
};
```

---

## Alternatives to Singleton

Better design alternatives to the singleton pattern:

```cpp
// 1. Dependency Injection
class Logger {
public:
    virtual ~Logger() = default;
    virtual void log(const std::string& message) = 0;
};

class FileLogger : public Logger {
public:
    void log(const std::string& message) override {
        std::cout << "File: " << message << std::endl;
    }
};

class Service {
private:
    Logger& logger;  // Dependency injected

public:
    Service(Logger& log) : logger(log) {}

    void doWork() {
        logger.log("Work performed");
    }
};

// 2. Static/Global instance management
class ResourceManager {
private:
    static std::unique_ptr<ResourceManager> globalInstance;

public:
    static void initialize() {
        if (!globalInstance) {
            globalInstance = std::make_unique<ResourceManager>();
        }
    }

    static ResourceManager& get() {
        if (!globalInstance) {
            throw std::runtime_error("ResourceManager not initialized");
        }
        return *globalInstance;
    }

    static void shutdown() {
        globalInstance.reset();
    }
};

// 3. Monostate pattern - shared state, multiple instances
class Monostate {
private:
    static int sharedState;

public:
    int getState() const { return sharedState; }
    void setState(int value) { sharedState = value; }
};

int Monostate::sharedState = 0;
```

---

## STRUCTURAL PATTERNS

---

## Adapter Pattern

Make incompatible interfaces work together

```cpp
// Existing class with incompatible interface
class LegacyPrinter {
public:
    void printOldFormat(const std::string& text) {
        std::cout << "Legacy: " << text << std::endl;
    }
};

// Target interface we want to use
class ModernPrinter {
public:
    virtual ~ModernPrinter() = default;
    virtual void print(const std::string& text) = 0;
};

// Adapter makes LegacyPrinter compatible with ModernPrinter
class PrinterAdapter : public ModernPrinter {
private:
    LegacyPrinter legacyPrinter;
public:
    void print(const std::string& text) override {
        legacyPrinter.printOldFormat(text);  // Adapt the call
    }
};

// Object adapter version
class ObjectPrinterAdapter : public ModernPrinter {
private:
    std::unique_ptr<LegacyPrinter> legacyPrinter;
public:
    ObjectPrinterAdapter(std::unique_ptr<LegacyPrinter> printer)
        : legacyPrinter(std::move(printer)) {}

    void print(const std::string& text) override {
        legacyPrinter->printOldFormat(text);
    }
};
```

---

## Bridge Pattern

Separate abstraction from implementation to vary them independently

```cpp
// Implementation interface
class DrawingAPI {
public:
    virtual ~DrawingAPI() = default;
    virtual void drawCircle(double x, double y, double radius) = 0;
    virtual void drawLine(double x1, double y1, double x2, double y2) = 0;
};

// Concrete implementations
class OpenGLDrawing : public DrawingAPI {
public:
    void drawCircle(double x, double y, double radius) override {
        std::cout << "OpenGL: Circle at (" << x << "," << y
                  << ") radius " << radius << std::endl;
    }

    void drawLine(double x1, double y1, double x2, double y2) override {
        std::cout << "OpenGL: Line from (" << x1 << "," << y1
                  << ") to (" << x2 << "," << y2 << ")" << std::endl;
    }
};

class DirectXDrawing : public DrawingAPI {
public:
    void drawCircle(double x, double y, double radius) override {
        std::cout << "DirectX: Circle at (" << x << "," << y
                  << ") radius " << radius << std::endl;
    }

    void drawLine(double x1, double y1, double x2, double y2) override {
        std::cout << "DirectX: Line from (" << x1 << "," << y1
                  << ") to (" << x2 << "," << y2 << ")" << std::endl;
    }
};
```

---

## Bridge Abstraction

```cpp
// Abstraction
class Shape {
protected:
    std::unique_ptr<DrawingAPI> drawingAPI;

public:
    Shape(std::unique_ptr<DrawingAPI> api) : drawingAPI(std::move(api)) {}
    virtual ~Shape() = default;
    virtual void draw() = 0;
    virtual void resize(double factor) = 0;
};

// Refined abstractions
class Circle : public Shape {
private:
    double x, y, radius;

public:
    Circle(double x, double y, double radius, std::unique_ptr<DrawingAPI> api)
        : Shape(std::move(api)), x(x), y(y), radius(radius) {}

    void draw() override {
        drawingAPI->drawCircle(x, y, radius);
    }

    void resize(double factor) override {
        radius *= factor;
    }
};

class Line : public Shape {
private:
    double x1, y1, x2, y2;

public:
    Line(double x1, double y1, double x2, double y2, std::unique_ptr<DrawingAPI> api)
        : Shape(std::move(api)), x1(x1), y1(y1), x2(x2), y2(y2) {}

    void draw() override {
        drawingAPI->drawLine(x1, y1, x2, y2);
    }

    void resize(double factor) override {
        // Scale the line endpoints
        x2 = x1 + (x2 - x1) * factor;
        y2 = y1 + (y2 - y1) * factor;
    }
};
```

---

## Composite Pattern

Compose objects into tree structures to represent part-whole hierarchies

```cpp
class Component {
public:
    virtual ~Component() = default;
    virtual void operation() = 0;
    virtual void add(std::unique_ptr<Component> component) {
        throw std::runtime_error("Operation not supported");
    }
    virtual void remove(Component* component) {
        throw std::runtime_error("Operation not supported");
    }
    virtual Component* getChild(size_t index) {
        throw std::runtime_error("Operation not supported");
    }
};

class Leaf : public Component {
private:
    std::string name;
public:
    Leaf(const std::string& n) : name(n) {}

    void operation() override {
        std::cout << "Leaf " << name << " operation" << std::endl;
    }
};
```

---

## Composite Implementation

```cpp
class Composite : public Component {
private:
    std::vector<std::unique_ptr<Component>> children;
    std::string name;

public:
    Composite(const std::string& n) : name(n) {}

    void operation() override {
        std::cout << "Composite " << name << " operation:" << std::endl;
        for (auto& child : children) {
            child->operation();
        }
    }

    void add(std::unique_ptr<Component> component) override {
        children.push_back(std::move(component));
    }

    void remove(Component* component) override {
        children.erase(
            std::remove_if(children.begin(), children.end(),
                [component](const std::unique_ptr<Component>& ptr) {
                    return ptr.get() == component;
                }),
            children.end()
        );
    }

    Component* getChild(size_t index) override {
        if (index < children.size()) {
            return children[index].get();
        }
        return nullptr;
    }
};
```

---

## Composite Usage Example

Building hierarchical structures with uniform interface:

```cpp
void demonstrateComposite() {
    // Create individual leaves
    auto leaf1 = std::make_unique<Leaf>("A");
    auto leaf2 = std::make_unique<Leaf>("B");
    auto leaf3 = std::make_unique<Leaf>("C");

    // Create composites
    auto composite1 = std::make_unique<Composite>("Group1");
    auto composite2 = std::make_unique<Composite>("Group2");

    // Build hierarchy
    composite1->add(std::move(leaf1));
    composite1->add(std::move(leaf2));

    composite2->add(std::move(leaf3));
    composite2->add(std::move(composite1));  // Nest composites

    // Uniform interface - treat leaf and composite the same
    composite2->operation();  // Recursively calls all children
}
```

---

## Decorator Pattern

Add behavior to objects dynamically

```cpp
class Coffee {
public:
    virtual ~Coffee() = default;
    virtual double cost() = 0;
    virtual std::string description() = 0;
};

class SimpleCoffee : public Coffee {
public:
    double cost() override { return 2.0; }
    std::string description() override { return "Simple coffee"; }
};

class CoffeeDecorator : public Coffee {
protected:
    std::unique_ptr<Coffee> coffee;
public:
    CoffeeDecorator(std::unique_ptr<Coffee> c) : coffee(std::move(c)) {}
};

class MilkDecorator : public CoffeeDecorator {
public:
    MilkDecorator(std::unique_ptr<Coffee> c) : CoffeeDecorator(std::move(c)) {}

    double cost() override { return coffee->cost() + 0.5; }
    std::string description() override { return coffee->description() + ", milk"; }
};

class SugarDecorator : public CoffeeDecorator {
public:
    SugarDecorator(std::unique_ptr<Coffee> c) : CoffeeDecorator(std::move(c)) {}

    double cost() override { return coffee->cost() + 0.2; }
    std::string description() override { return coffee->description() + ", sugar"; }
};

// Usage
auto coffee = std::make_unique<SugarDecorator>(
    std::make_unique<MilkDecorator>(
        std::make_unique<SimpleCoffee>()));
```

---

## Facade Pattern

Provide simplified interface to complex subsystem

```cpp
// Complex subsystem
class CPU {
public:
    void freeze() { std::cout << "CPU frozen\n"; }
    void jump(long position) { std::cout << "CPU jump to " << position << "\n"; }
    void execute() { std::cout << "CPU executing\n"; }
};

class Memory {
public:
    void load(long position, const std::string& data) {
        std::cout << "Memory loaded at " << position << ": " << data << "\n";
    }
};

class HardDrive {
public:
    std::string read(long lba, int size) {
        std::cout << "HD reading " << size << " bytes from " << lba << "\n";
        return "boot_data";
    }
};

// Facade provides simple interface
class ComputerFacade {
private:
    CPU cpu;
    Memory memory;
    HardDrive hardDrive;

public:
    void start() {
        std::cout << "Starting computer...\n";
        cpu.freeze();
        memory.load(0, hardDrive.read(0, 1024));
        cpu.jump(0);
        cpu.execute();
        std::cout << "Computer started!\n";
    }
};

// Client uses simple interface
ComputerFacade computer;
computer.start();  // Much simpler than calling each component
```

---

## Proxy Pattern

Provide a placeholder/surrogate to control access to another object

```cpp
class Image {
public:
    virtual ~Image() = default;
    virtual void display() = 0;
    virtual void load() = 0;
};

class RealImage : public Image {
private:
    std::string filename;
    bool loaded = false;

public:
    RealImage(const std::string& file) : filename(file) {}

    void load() override {
        if (!loaded) {
            std::cout << "Loading image: " << filename << std::endl;
            // Simulate expensive loading operation
            std::this_thread::sleep_for(std::chrono::milliseconds(100));
            loaded = true;
        }
    }

    void display() override {
        if (!loaded) load();
        std::cout << "Displaying image: " << filename << std::endl;
    }
};
```

---

## Proxy Implementation

```cpp
class ImageProxy : public Image {
private:
    std::string filename;
    mutable std::unique_ptr<RealImage> realImage;  // Lazy initialization

public:
    ImageProxy(const std::string& file) : filename(file) {}

    void load() override {
        if (!realImage) {
            realImage = std::make_unique<RealImage>(filename);
        }
        realImage->load();
    }

    void display() override {
        if (!realImage) {
            realImage = std::make_unique<RealImage>(filename);
        }
        realImage->display();
    }
};

// Usage
void demonstrateProxy() {
    std::vector<std::unique_ptr<Image>> images;
    images.push_back(std::make_unique<ImageProxy>("photo1.jpg"));
    images.push_back(std::make_unique<ImageProxy>("photo2.jpg"));
    images.push_back(std::make_unique<ImageProxy>("photo3.jpg"));

    // Images not loaded yet - fast creation
    std::cout << "Images created" << std::endl;

    // Only load when actually displayed
    images[1]->display();  // Only photo2.jpg is loaded
}
```

---

## Cheshire Cat Pattern (Pimpl)

Hide implementation details by moving them to a separate class

```cpp
// Widget.h - Public interface
class Widget {
public:
    Widget();
    ~Widget();

    // Copy operations
    Widget(const Widget& other);
    Widget& operator=(const Widget& other);

    // Move operations
    Widget(Widget&& other) noexcept;
    Widget& operator=(Widget&& other) noexcept;

    void doSomething();
    void configure(const std::string& config);

private:
    class Impl;  // Forward declaration
    std::unique_ptr<Impl> pImpl;  // Pointer to implementation
};
```

---

## Cheshire Cat Implementation

```cpp
// Widget.cpp - Implementation hidden from clients
class Widget::Impl {
public:
    void doSomething() {
        // Complex implementation details
        processData();
        updateState();
    }

    void configure(const std::string& config) {
        configuration = config;
        parseConfiguration();
    }

private:
    std::string configuration;
    std::vector<int> data;
    std::map<std::string, std::string> settings;

    void processData() { /* complex logic */ }
    void updateState() { /* internal state management */ }
    void parseConfiguration() { /* parsing logic */ }
};

// Widget methods delegate to implementation
Widget::Widget() : pImpl(std::make_unique<Impl>()) {}
Widget::~Widget() = default;  // unique_ptr handles cleanup

void Widget::doSomething() { pImpl->doSomething(); }
void Widget::configure(const std::string& config) { pImpl->configure(config); }
```

---

## Bridge vs Cheshire Cat

![bridge_vs_cheshire_cat](/svg/courses/languages/c++/modern-c++-for-c-programmers/16_design_patterns/bridge_vs_cheshire_cat.svg)

Choose based on whether you need runtime flexibility or compilation benefits

---

## BEHAVIORAL PATTERNS

---

## Observer Pattern

Define one-to-many dependency between objects

```cpp
class Observer {
public:
    virtual ~Observer() = default;
    virtual void update(const std::string& message) = 0;
};

class Subject {
private:
    std::vector<Observer*> observers;
    std::string state;

public:
    void attach(Observer* observer) {
        observers.push_back(observer);
    }

    void detach(Observer* observer) {
        observers.erase(
            std::remove(observers.begin(), observers.end(), observer),
            observers.end()
        );
    }

    void notify() {
        for (auto* observer : observers) {
            observer->update(state);
        }
    }

    void setState(const std::string& newState) {
        state = newState;
        notify();
    }

    const std::string& getState() const { return state; }
};

class ConcreteObserver : public Observer {
private:
    std::string name;

public:
    ConcreteObserver(const std::string& n) : name(n) {}

    void update(const std::string& message) override {
        std::cout << name << " received update: " << message << std::endl;
    }
};
```

---

## Modern Observer with std::function

```cpp
#include <functional>

class ModernSubject {
private:
    std::vector<std::function<void(const std::string&)>> observers;
    std::string state;

public:
    // Return handle for unsubscribing
    size_t subscribe(std::function<void(const std::string&)> callback) {
        observers.push_back(callback);
        return observers.size() - 1;
    }

    void unsubscribe(size_t handle) {
        if (handle < observers.size()) {
            observers.erase(observers.begin() + handle);
        }
    }

    void notify() {
        for (const auto& observer : observers) {
            observer(state);
        }
    }

    void setState(const std::string& newState) {
        state = newState;
        notify();
    }
};

// Usage with lambdas
void demonstrateModernObserver() {
    ModernSubject subject;

    auto handle1 = subject.subscribe([](const std::string& msg) {
        std::cout << "Lambda observer 1: " << msg << std::endl;
    });

    auto handle2 = subject.subscribe([](const std::string& msg) {
        std::cout << "Lambda observer 2: " << msg << std::endl;
    });

    subject.setState("Hello World");  // Both observers notified
    subject.unsubscribe(handle1);
    subject.setState("Second message");  // Only observer 2 notified
}
```

---

## Strategy Pattern

Define family of algorithms and make them interchangeable

```cpp
class SortStrategy {
public:
    virtual ~SortStrategy() = default;
    virtual void sort(std::vector<int>& data) = 0;
    virtual std::string getName() const = 0;
};

class BubbleSort : public SortStrategy {
public:
    void sort(std::vector<int>& data) override {
        std::cout << "Performing bubble sort" << std::endl;
        // Bubble sort implementation
        for (size_t i = 0; i < data.size(); ++i) {
            for (size_t j = 0; j < data.size() - 1 - i; ++j) {
                if (data[j] > data[j + 1]) {
                    std::swap(data[j], data[j + 1]);
                }
            }
        }
    }

    std::string getName() const override { return "Bubble Sort"; }
};

class QuickSort : public SortStrategy {
public:
    void sort(std::vector<int>& data) override {
        std::cout << "Performing quick sort" << std::endl;
        quickSort(data, 0, data.size() - 1);
    }

    std::string getName() const override { return "Quick Sort"; }

private:
    void quickSort(std::vector<int>& arr, int low, int high) {
        if (low < high) {
            int pi = partition(arr, low, high);
            quickSort(arr, low, pi - 1);
            quickSort(arr, pi + 1, high);
        }
    }

    int partition(std::vector<int>& arr, int low, int high) {
        int pivot = arr[high];
        int i = low - 1;
        for (int j = low; j < high; ++j) {
            if (arr[j] < pivot) {
                ++i;
                std::swap(arr[i], arr[j]);
            }
        }
        std::swap(arr[i + 1], arr[high]);
        return i + 1;
    }
};

class SortContext {
private:
    std::unique_ptr<SortStrategy> strategy;

public:
    void setStrategy(std::unique_ptr<SortStrategy> newStrategy) {
        strategy = std::move(newStrategy);
    }

    void performSort(std::vector<int>& data) {
        if (strategy) {
            std::cout << "Using " << strategy->getName() << std::endl;
            strategy->sort(data);
        }
    }
};
```

---

## Command Pattern

Encapsulate requests as objects

```cpp
class Command {
public:
    virtual ~Command() = default;
    virtual void execute() = 0;
    virtual void undo() = 0;
};

class Light {
private:
    bool isOn = false;

public:
    void turnOn() {
        isOn = true;
        std::cout << "Light is ON" << std::endl;
    }

    void turnOff() {
        isOn = false;
        std::cout << "Light is OFF" << std::endl;
    }

    bool getState() const { return isOn; }
};

class LightOnCommand : public Command {
private:
    Light& light;

public:
    LightOnCommand(Light& l) : light(l) {}

    void execute() override {
        light.turnOn();
    }

    void undo() override {
        light.turnOff();
    }
};

class LightOffCommand : public Command {
private:
    Light& light;

public:
    LightOffCommand(Light& l) : light(l) {}

    void execute() override {
        light.turnOff();
    }

    void undo() override {
        light.turnOn();
    }
};
```

---

## Command Invoker

```cpp
class RemoteControl {
private:
    std::vector<std::unique_ptr<Command>> commands;
    std::stack<std::unique_ptr<Command>> history;

public:
    void setCommand(size_t slot, std::unique_ptr<Command> command) {
        if (slot >= commands.size()) {
            commands.resize(slot + 1);
        }
        commands[slot] = std::move(command);
    }

    void pressButton(size_t slot) {
        if (slot < commands.size() && commands[slot]) {
            commands[slot]->execute();

            // Clone command for undo (simplified)
            if (auto* lightOn = dynamic_cast<LightOnCommand*>(commands[slot].get())) {
                // In real implementation, you'd need proper cloning
            }
        }
    }

    void undo() {
        if (!history.empty()) {
            auto command = std::move(history.top());
            history.pop();
            command->undo();
        }
    }
};

// Macro command - composite pattern with commands
class MacroCommand : public Command {
private:
    std::vector<std::unique_ptr<Command>> commands;

public:
    void addCommand(std::unique_ptr<Command> command) {
        commands.push_back(std::move(command));
    }

    void execute() override {
        for (auto& command : commands) {
            command->execute();
        }
    }

    void undo() override {
        // Undo in reverse order
        for (auto it = commands.rbegin(); it != commands.rend(); ++it) {
            (*it)->undo();
        }
    }
};
```

---

## Template Method Pattern

Define algorithm skeleton, let subclasses override specific steps

```cpp
class DataProcessor {
public:
    // Template method - defines the algorithm structure
    void processData() {
        loadData();
        if (validateData()) {
            transformData();
            saveData();
        } else {
            handleValidationError();
        }
        cleanup();
    }

protected:
    // Steps to be implemented by subclasses
    virtual void loadData() = 0;
    virtual bool validateData() = 0;
    virtual void transformData() = 0;
    virtual void saveData() = 0;

    // Hook methods - optional override
    virtual void handleValidationError() {
        std::cout << "Validation failed - using default error handling" << std::endl;
    }

    virtual void cleanup() {
        std::cout << "Default cleanup performed" << std::endl;
    }
};

class CSVProcessor : public DataProcessor {
private:
    std::vector<std::string> data;

protected:
    void loadData() override {
        std::cout << "Loading CSV data" << std::endl;
        data = {"row1", "row2", "row3"};  // Simplified
    }

    bool validateData() override {
        std::cout << "Validating CSV data" << std::endl;
        return !data.empty();
    }

    void transformData() override {
        std::cout << "Transforming CSV data" << std::endl;
        for (auto& row : data) {
            row = "processed_" + row;
        }
    }

    void saveData() override {
        std::cout << "Saving processed CSV data" << std::endl;
        for (const auto& row : data) {
            std::cout << "  " << row << std::endl;
        }
    }

    void cleanup() override {
        std::cout << "CSV-specific cleanup" << std::endl;
        data.clear();
    }
};
```

---

## State Pattern

Allow object to alter behavior when internal state changes

```cpp
class State {
public:
    virtual ~State() = default;
    virtual void handle() = 0;
    virtual std::string getName() const = 0;
};

class ConcreteStateA : public State {
public:
    void handle() override {
        std::cout << "Handling in State A" << std::endl;
    }

    std::string getName() const override { return "State A"; }
};

class ConcreteStateB : public State {
public:
    void handle() override {
        std::cout << "Handling in State B" << std::endl;
    }

    std::string getName() const override { return "State B"; }
};

class Context {
private:
    std::unique_ptr<State> state;

public:
    Context(std::unique_ptr<State> s) : state(std::move(s)) {}

    void setState(std::unique_ptr<State> s) {
        std::cout << "Transitioning to " << s->getName() << std::endl;
        state = std::move(s);
    }

    void request() {
        std::cout << "Current state: " << state->getName() << std::endl;
        state->handle();
    }
};

// Usage
Context context(std::make_unique<ConcreteStateA>());
context.request();  // "Handling in State A"
context.setState(std::make_unique<ConcreteStateB>());
context.request();  // "Handling in State B"
```

---

## Chain of Responsibility Pattern

Pass requests along chain of handlers

```cpp
class Handler {
protected:
    std::unique_ptr<Handler> nextHandler;

public:
    void setNext(std::unique_ptr<Handler> handler) {
        nextHandler = std::move(handler);
    }

    virtual void handleRequest(int request) {
        if (nextHandler) {
            nextHandler->handleRequest(request);
        } else {
            std::cout << "No handler could process request " << request << std::endl;
        }
    }
};

class ConcreteHandlerA : public Handler {
public:
    void handleRequest(int request) override {
        if (request < 10) {
            std::cout << "Handler A processed request " << request << std::endl;
        } else {
            std::cout << "Handler A cannot handle " << request << ", passing on" << std::endl;
            Handler::handleRequest(request);
        }
    }
};

class ConcreteHandlerB : public Handler {
public:
    void handleRequest(int request) override {
        if (request >= 10 && request < 20) {
            std::cout << "Handler B processed request " << request << std::endl;
        } else {
            std::cout << "Handler B cannot handle " << request << ", passing on" << std::endl;
            Handler::handleRequest(request);
        }
    }
};

class ConcreteHandlerC : public Handler {
public:
    void handleRequest(int request) override {
        if (request >= 20) {
            std::cout << "Handler C processed request " << request << std::endl;
        } else {
            Handler::handleRequest(request);
        }
    }
};
```

---

## Visitor Pattern

Separate operations from object structure

```cpp
// Forward declarations
class Circle;
class Rectangle;
class Triangle;

class ShapeVisitor {
public:
    virtual ~ShapeVisitor() = default;
    virtual void visit(Circle& circle) = 0;
    virtual void visit(Rectangle& rectangle) = 0;
    virtual void visit(Triangle& triangle) = 0;
};

class Shape {
public:
    virtual ~Shape() = default;
    virtual void accept(ShapeVisitor& visitor) = 0;
};

class Circle : public Shape {
private:
    double radius;

public:
    Circle(double r) : radius(r) {}

    void accept(ShapeVisitor& visitor) override {
        visitor.visit(*this);
    }

    double getRadius() const { return radius; }
};

class Rectangle : public Shape {
private:
    double width, height;

public:
    Rectangle(double w, double h) : width(w), height(h) {}

    void accept(ShapeVisitor& visitor) override {
        visitor.visit(*this);
    }

    double getWidth() const { return width; }
    double getHeight() const { return height; }
};

class Triangle : public Shape {
private:
    double base, height;

public:
    Triangle(double b, double h) : base(b), height(h) {}

    void accept(ShapeVisitor& visitor) override {
        visitor.visit(*this);
    }

    double getBase() const { return base; }
    double getHeight() const { return height; }
};
```

---

## Visitor Implementations

```cpp
class AreaCalculator : public ShapeVisitor {
private:
    double totalArea = 0;

public:
    void visit(Circle& circle) override {
        double area = 3.14159 * circle.getRadius() * circle.getRadius();
        totalArea += area;
        std::cout << "Circle area: " << area << std::endl;
    }

    void visit(Rectangle& rectangle) override {
        double area = rectangle.getWidth() * rectangle.getHeight();
        totalArea += area;
        std::cout << "Rectangle area: " << area << std::endl;
    }

    void visit(Triangle& triangle) override {
        double area = 0.5 * triangle.getBase() * triangle.getHeight();
        totalArea += area;
        std::cout << "Triangle area: " << area << std::endl;
    }

    double getTotalArea() const { return totalArea; }
};

class DrawingVisitor : public ShapeVisitor {
public:
    void visit(Circle& circle) override {
        std::cout << "Drawing circle with radius " << circle.getRadius() << std::endl;
    }

    void visit(Rectangle& rectangle) override {
        std::cout << "Drawing rectangle " << rectangle.getWidth()
                  << "x" << rectangle.getHeight() << std::endl;
    }

    void visit(Triangle& triangle) override {
        std::cout << "Drawing triangle with base " << triangle.getBase()
                  << " and height " << triangle.getHeight() << std::endl;
    }
};

// Usage
void demonstrateVisitor() {
    std::vector<std::unique_ptr<Shape>> shapes;
    shapes.push_back(std::make_unique<Circle>(5.0));
    shapes.push_back(std::make_unique<Rectangle>(4.0, 6.0));
    shapes.push_back(std::make_unique<Triangle>(3.0, 8.0));

    AreaCalculator areaCalc;
    DrawingVisitor drawer;

    for (auto& shape : shapes) {
        shape->accept(areaCalc);
        shape->accept(drawer);
    }

    std::cout << "Total area: " << areaCalc.getTotalArea() << std::endl;
}
```

---

## Iterator Pattern

Provide way to access elements sequentially

```cpp
template<typename T>
class Iterator {
public:
    virtual ~Iterator() = default;
    virtual bool hasNext() = 0;
    virtual T next() = 0;
};

template<typename T>
class ConcreteIterator : public Iterator<T> {
private:
    std::vector<T>& collection;
    size_t position = 0;

public:
    ConcreteIterator(std::vector<T>& coll) : collection(coll) {}

    bool hasNext() override {
        return position < collection.size();
    }

    T next() override {
        if (!hasNext()) {
            throw std::out_of_range("No more elements");
        }
        return collection[position++];
    }
};

template<typename T>
class Collection {
private:
    std::vector<T> items;

public:
    void add(const T& item) { items.push_back(item); }

    std::unique_ptr<Iterator<T>> createIterator() {
        return std::make_unique<ConcreteIterator<T>>(items);
    }

    // Modern approach - return standard iterators
    auto begin() { return items.begin(); }
    auto end() { return items.end(); }
};
```

---

## Mediator Pattern

Define how objects interact through a mediator

```cpp
class Mediator {
public:
    virtual ~Mediator() = default;
    virtual void notify(const std::string& sender, const std::string& event) = 0;
};

class Component {
protected:
    Mediator* mediator;

public:
    Component(Mediator* m) : mediator(m) {}
    virtual ~Component() = default;
};

class Button : public Component {
private:
    std::string name;

public:
    Button(const std::string& n, Mediator* m) : Component(m), name(n) {}

    void click() {
        std::cout << "Button " << name << " clicked" << std::endl;
        mediator->notify(name, "click");
    }
};

class TextField : public Component {
private:
    std::string name;
    std::string text;

public:
    TextField(const std::string& n, Mediator* m) : Component(m), name(n) {}

    void setText(const std::string& t) {
        text = t;
        std::cout << "TextField " << name << " text changed to: " << text << std::endl;
        mediator->notify(name, "textChanged");
    }

    const std::string& getText() const { return text; }
};

class Dialog : public Mediator {
private:
    std::unique_ptr<Button> submitButton;
    std::unique_ptr<TextField> textField;

public:
    Dialog() {
        submitButton = std::make_unique<Button>("Submit", this);
        textField = std::make_unique<TextField>("Input", this);
    }

    void notify(const std::string& sender, const std::string& event) override {
        if (sender == "Submit" && event == "click") {
            std::cout << "Dialog: Processing form submission with text: "
                      << textField->getText() << std::endl;
        } else if (sender == "Input" && event == "textChanged") {
            std::cout << "Dialog: Text field updated" << std::endl;
        }
    }

    Button* getSubmitButton() { return submitButton.get(); }
    TextField* getTextField() { return textField.get(); }
};
```

---

## Memento Pattern

Capture and restore object state

```cpp
class Memento {
private:
    std::string state;
    std::chrono::system_clock::time_point timestamp;
    friend class Originator;

public:
    Memento(const std::string& s) : state(s), timestamp(std::chrono::system_clock::now()) {}

    std::string getTimestamp() const {
        auto time_t = std::chrono::system_clock::to_time_t(timestamp);
        return std::ctime(&time_t);
    }
};

class Originator {
private:
    std::string state;

public:
    void setState(const std::string& s) {
        std::cout << "Setting state to: " << s << std::endl;
        state = s;
    }

    std::string getState() const { return state; }

    std::unique_ptr<Memento> createMemento() {
        std::cout << "Creating memento with state: " << state << std::endl;
        return std::make_unique<Memento>(state);
    }

    void restoreFromMemento(const Memento& memento) {
        state = memento.state;
        std::cout << "Restored state to: " << state << std::endl;
    }
};

class Caretaker {
private:
    std::vector<std::unique_ptr<Memento>> mementos;

public:
    void addMemento(std::unique_ptr<Memento> memento) {
        std::cout << "Caretaker: Storing memento" << std::endl;
        mementos.push_back(std::move(memento));
    }

    Memento* getMemento(size_t index) {
        if (index < mementos.size()) {
            std::cout << "Caretaker: Retrieving memento " << index << std::endl;
            return mementos[index].get();
        }
        return nullptr;
    }

    size_t size() const { return mementos.size(); }
};
```

---

## Null Object Pattern

Provide a default object that does nothing to eliminate null checks

```cpp
class Logger {
public:
    virtual ~Logger() = default;
    virtual void log(const std::string& message) = 0;
    virtual void error(const std::string& message) = 0;
};

class FileLogger : public Logger {
private:
    std::ofstream file;

public:
    FileLogger(const std::string& filename) : file(filename) {}

    void log(const std::string& message) override {
        file << "[LOG] " << message << std::endl;
    }

    void error(const std::string& message) override {
        file << "[ERROR] " << message << std::endl;
    }
};

class NullLogger : public Logger {
public:
    void log(const std::string& message) override {
        // Do nothing - null object behavior
    }

    void error(const std::string& message) override {
        // Do nothing - null object behavior
    }
};

class Service {
private:
    std::unique_ptr<Logger> logger;

public:
    Service(std::unique_ptr<Logger> log = std::make_unique<NullLogger>())
        : logger(std::move(log)) {}

    void processRequest() {
        logger->log("Processing request");  // No null check needed!

        try {
            // Do some work
            doWork();
            logger->log("Request processed successfully");
        } catch (const std::exception& e) {
            logger->error("Request failed: " + std::string(e.what()));
        }
    }

private:
    void doWork() {
        // Implementation
    }
};
```

---

## Modern C++ Pattern Enhancements

Using modern C++ features to improve patterns:

```cpp
// Lambda-based Strategy
class ModernSortContext {
private:
    std::function<void(std::vector<int>&)> sortFunction;

public:
    void setStrategy(std::function<void(std::vector<int>&)> func) {
        sortFunction = func;
    }

    void sort(std::vector<int>& data) {
        if (sortFunction) {
            sortFunction(data);
        }
    }
};

// Usage with lambdas
void demonstrateModernStrategy() {
    ModernSortContext context;

    // Set strategy using lambda
    context.setStrategy([](std::vector<int>& data) {
        std::sort(data.begin(), data.end());
    });

    std::vector<int> numbers = {3, 1, 4, 1, 5, 9, 2, 6};
    context.sort(numbers);
}

// Template-based Factory
template<typename Base, typename... Args>
class GenericFactory {
private:
    std::map<std::string, std::function<std::unique_ptr<Base>(Args...)>> creators;

public:
    template<typename Derived>
    void registerType(const std::string& name) {
        creators[name] = [](Args... args) {
            return std::make_unique<Derived>(std::forward<Args>(args)...);
        };
    }

    std::unique_ptr<Base> create(const std::string& name, Args... args) {
        auto it = creators.find(name);
        if (it != creators.end()) {
            return it->second(std::forward<Args>(args)...);
        }
        return nullptr;
    }
};
```

---

## When to Use Each Pattern

![when_to_use_each_pattern](/svg/courses/languages/c++/modern-c++-for-c-programmers/16_design_patterns/when_to_use_each_pattern.svg)

Choose patterns based on actual problems, not theoretical perfection

---

## Pattern Combinations

Patterns often work together to solve complex problems:

```cpp
// Factory + Strategy + Template Method
class SortingFactory {
public:
    static std::unique_ptr<SortStrategy> createSorter(const std::string& type) {
        if (type == "bubble") {
            return std::make_unique<BubbleSort>();
        } else if (type == "quick") {
            return std::make_unique<QuickSort>();
        }
        throw std::invalid_argument("Unknown sort type");
    }
};

// Observer + Command for undo/redo system
class UndoRedoManager : public Subject {
private:
    std::stack<std::unique_ptr<Command>> undoStack;
    std::stack<std::unique_ptr<Command>> redoStack;

public:
    void executeCommand(std::unique_ptr<Command> command) {
        command->execute();
        undoStack.push(std::move(command));

        // Clear redo stack when new command executed
        while (!redoStack.empty()) {
            redoStack.pop();
        }

        setState("Command executed");  // Notify observers
    }

    void undo() {
        if (!undoStack.empty()) {
            auto command = std::move(undoStack.top());
            undoStack.pop();
            command->undo();
            redoStack.push(std::move(command));
            setState("Command undone");
        }
    }

    void redo() {
        if (!redoStack.empty()) {
            auto command = std::move(redoStack.top());
            redoStack.pop();
            command->execute();
            undoStack.push(std::move(command));
            setState("Command redone");
        }
    }
};

// Composite + Visitor for complex hierarchies
class DocumentElement : public Component {
public:
    virtual void accept(ShapeVisitor& visitor) = 0;
};

class Paragraph : public DocumentElement {
private:
    std::string text;
public:
    Paragraph(const std::string& t) : text(t) {}

    void operation() override {
        std::cout << "Paragraph: " << text << std::endl;
    }

    void accept(ShapeVisitor& visitor) override {
        // visitor.visit(*this); // Would need appropriate visitor interface
    }
};
```

---

## Proxy Pattern Variations

![proxy_pattern_variations](/svg/courses/languages/c++/modern-c++-for-c-programmers/16_design_patterns/proxy_pattern_variations.svg)

Different proxy types serve different purposes

---

## Lazy Initialization Pattern

Defer expensive object creation until actually needed

```cpp
template<typename T>
class Lazy {
private:
    mutable std::optional<T> value;
    std::function<T()> factory;

public:
    template<typename F>
    Lazy(F&& f) : factory(std::forward<F>(f)) {}

    const T& get() const {
        if (!value.has_value()) {
            value = factory();
        }
        return value.value();
    }

    const T& operator*() const { return get(); }
    const T* operator->() const { return &get(); }

    bool isInitialized() const { return value.has_value(); }

    void reset() { value.reset(); }
};

// Usage
class ExpensiveResource {
public:
    ExpensiveResource() {
        std::cout << "Creating expensive resource..." << std::endl;
        // Simulate expensive initialization
    }

    void doWork() {
        std::cout << "Working..." << std::endl;
    }
};

Lazy<ExpensiveResource> resource([]() { return ExpensiveResource(); });
// Not created yet!

// Only created when first accessed
resource->doWork();  // Now it's created and used
```

---

## Dependency Inversion Principle

Depend on abstractions, not concretions

```cpp
// Bad: High-level module depends on low-level module
class EmailService {  // Low-level
public:
    void sendEmail(const std::string& to, const std::string& message) {
        std::cout << "Sending email to " << to << ": " << message << std::endl;
    }
};

class NotificationManager {  // High-level
private:
    EmailService emailService;  // Direct dependency!

public:
    void notifyUser(const std::string& user, const std::string& message) {
        emailService.sendEmail(user, message);  // Tightly coupled
    }
};

// Good: Both depend on abstraction
class NotificationService {  // Abstraction
public:
    virtual ~NotificationService() = default;
    virtual void notify(const std::string& recipient, const std::string& message) = 0;
};

class EmailNotification : public NotificationService {
public:
    void notify(const std::string& recipient, const std::string& message) override {
        std::cout << "Email to " << recipient << ": " << message << std::endl;
    }
};

class SMSNotification : public NotificationService {
public:
    void notify(const std::string& recipient, const std::string& message) override {
        std::cout << "SMS to " << recipient << ": " << message << std::endl;
    }
};
```

---

## Dependency Injection

Provide dependencies from the outside rather than creating them internally

```cpp
class ImprovedNotificationManager {
private:
    std::vector<std::unique_ptr<NotificationService>> services;

public:
    // Constructor injection
    ImprovedNotificationManager(std::vector<std::unique_ptr<NotificationService>> svc)
        : services(std::move(svc)) {}

    // Setter injection
    void addNotificationService(std::unique_ptr<NotificationService> service) {
        services.push_back(std::move(service));
    }

    void notifyUser(const std::string& user, const std::string& message) {
        for (auto& service : services) {
            service->notify(user, message);  // Polymorphic call
        }
    }
};

// Usage
auto createNotificationManager() {
    std::vector<std::unique_ptr<NotificationService>> services;
    services.push_back(std::make_unique<EmailNotification>());
    services.push_back(std::make_unique<SMSNotification>());

    return std::make_unique<ImprovedNotificationManager>(std::move(services));
}
```

---

## SOLID Principles & Patterns

How design patterns support SOLID principles:

```cpp
// Single Responsibility Principle - each pattern has one job
class FileReader {  // Only reads files
public:
    std::string readFile(const std::string& filename) {
        // File reading logic
        return "file_content";
    }
};

class DataProcessor {  // Only processes data
public:
    std::string processData(const std::string& data) {
        return "processed_" + data;
    }
};

// Open/Closed Principle - Strategy pattern enables extension
class PaymentProcessor {
private:
    std::unique_ptr<PaymentStrategy> strategy;
public:
    void setStrategy(std::unique_ptr<PaymentStrategy> s) { strategy = std::move(s); }
    void processPayment(double amount) { strategy->pay(amount); }
};

// Add new payment methods without modifying existing code
class CreditCardPayment : public PaymentStrategy {
public:
    void pay(double amount) override {
        std::cout << "Paid $" << amount << " with credit card" << std::endl;
    }
};

// Liskov Substitution Principle - polymorphic substitution
void processShapes(std::vector<std::unique_ptr<Shape>>& shapes) {
    for (auto& shape : shapes) {
        shape->draw();  // Works with any Shape subclass
    }
}

// Interface Segregation Principle - focused interfaces
class Printable {
public:
    virtual void print() = 0;
};

class Scannable {
public:
    virtual void scan() = 0;
};

class Printer : public Printable {
public:
    void print() override { std::cout << "Printing..." << std::endl; }
};

// Dependency Inversion Principle - depend on abstractions
class DocumentService {
private:
    std::unique_ptr<Printable> printer;  // Depends on abstraction
public:
    DocumentService(std::unique_ptr<Printable> p) : printer(std::move(p)) {}
    void printDocument() { printer->print(); }
};
```

---

## Anti-Patterns to Avoid

Common misuses and problems with design patterns:

```cpp
// Anti-pattern: Pattern overuse
class OverEngineeredHelloWorld {
private:
    std::unique_ptr<MessageStrategy> strategy;
    std::unique_ptr<OutputFactory> factory;
    std::unique_ptr<MessageBuilder> builder;
public:
    // 50 lines of code to print "Hello World"
    void display() {
        auto message = builder->withGreeting("Hello")
                             ->withTarget("World")
                             ->build();
        auto output = factory->createOutput("console");
        strategy->setOutput(std::move(output));
        strategy->displayMessage(message);
    }
};

// Better: Simple solution
void printHelloWorld() {
    std::cout << "Hello World" << std::endl;
}

// Anti-pattern: God Object (violates SRP)
class GodClass {
public:
    void readFile() { /* ... */ }
    void processData() { /* ... */ }
    void saveToDatabase() { /* ... */ }
    void sendEmail() { /* ... */ }
    void generateReport() { /* ... */ }
    void validateInput() { /* ... */ }
    // ... 50 more methods
};

// Better: Single responsibility classes
class FileReader { public: std::string read(const std::string& file); };
class DataProcessor { public: std::string process(const std::string& data); };
class DatabaseSaver { public: void save(const std::string& data); };

// Anti-pattern: Singleton abuse
class GlobalState : public Singleton<GlobalState> {
public:
    std::map<std::string, std::string> config;
    std::vector<std::string> userData;
    DatabaseConnection* db;
    // Everything is global - hard to test and maintain
};

// Better: Dependency injection
class ConfigService {
private:
    std::map<std::string, std::string> config;
public:
    std::string getValue(const std::string& key) { return config[key]; }
};
```

---

## Testing with Design Patterns

How patterns improve testability:

```cpp
// Testable design using dependency injection
class OrderService {
private:
    std::unique_ptr<PaymentProcessor> paymentProcessor;
    std::unique_ptr<EmailService> emailService;
    std::unique_ptr<InventoryService> inventoryService;

public:
    OrderService(std::unique_ptr<PaymentProcessor> payment,
                std::unique_ptr<EmailService> email,
                std::unique_ptr<InventoryService> inventory)
        : paymentProcessor(std::move(payment))
        , emailService(std::move(email))
        , inventoryService(std::move(inventory)) {}

    bool processOrder(const Order& order) {
        if (!inventoryService->isAvailable(order.productId)) {
            return false;
        }

        if (!paymentProcessor->processPayment(order.amount)) {
            return false;
        }

        inventoryService->reserve(order.productId);
        emailService->sendConfirmation(order.customerEmail);
        return true;
    }
};

// Mock implementations for testing
class MockPaymentProcessor : public PaymentProcessor {
public:
    bool processPayment(double amount) override {
        return amount > 0;  // Simple test logic
    }
};

class MockEmailService : public EmailService {
public:
    void sendConfirmation(const std::string& email) override {
        sentEmails.push_back(email);
    }

    std::vector<std::string> sentEmails;
};

// Test becomes easy
void testOrderProcessing() {
    auto mockPayment = std::make_unique<MockPaymentProcessor>();
    auto mockEmail = std::make_unique<MockEmailService>();
    auto mockInventory = std::make_unique<MockInventoryService>();

    OrderService service(std::move(mockPayment),
                        std::move(mockEmail),
                        std::move(mockInventory));

    Order order{"product123", 99.99, "customer@example.com"};
    bool result = service.processOrder(order);

    assert(result == true);
    assert(mockEmail->sentEmails.size() == 1);
}
```

---

## Pattern Evolution in Modern C++

How C++11/14/17/20 features change pattern implementation:

```cpp
// C++11: Move semantics and smart pointers
class ModernFactory {
public:
    template<typename T, typename... Args>
    static std::unique_ptr<T> create(Args&&... args) {
        return std::make_unique<T>(std::forward<Args>(args)...);
    }
};

// C++14: Generic lambdas
auto createStrategy = [](auto&& algorithm) {
    return [algorithm = std::forward<decltype(algorithm)>(algorithm)](auto& data) {
        algorithm(data);
    };
};

// C++17: std::variant for type-safe unions
using Command = std::variant<MoveCommand, RotateCommand, ScaleCommand>;

class CommandProcessor {
public:
    void execute(const Command& cmd) {
        std::visit([](const auto& command) {
            command.execute();
        }, cmd);
    }
};

// C++20: Concepts for better template constraints
template<typename T>
concept Observable = requires(T t) {
    t.attach(std::declval<Observer*>());
    t.detach(std::declval<Observer*>());
    t.notify();
};

template<Observable T>
class ObserverManager {
    T& subject;
public:
    ObserverManager(T& s) : subject(s) {}
    // Guaranteed to work with Observable types
};

// C++20: Coroutines for async patterns
class AsyncCommand {
public:
    std::future<void> executeAsync() {
        co_await std::this_thread::sleep_for(std::chrono::milliseconds(100));
        // Async execution logic
        co_return;
    }
};
```

---

## Performance Considerations

When patterns help or hurt performance:

```cpp
// Virtual function overhead in patterns
class Shape {  // Virtual dispatch cost
public:
    virtual void draw() = 0;  // Runtime cost
    virtual double area() = 0;
};

// Template-based alternative for compile-time polymorphism
template<typename ShapeType>
class DrawingContext {
public:
    void drawShape(const ShapeType& shape) {
        shape.draw();  // No virtual dispatch - inlined
    }
};

// Memory overhead considerations
class HeavyweightFlyweight {
private:
    // Large intrinsic state
    std::array<double, 1000> sharedData;
public:
    void operation(const ExtrinsicState& state) {
        // Use shared data with extrinsic state
    }
};

// Smart pointer overhead
class PerformanceCriticalClass {
private:
    // std::unique_ptr<Impl> pImpl;  // Indirection cost
    Impl impl;  // Direct storage when appropriate
public:
    void hotPath() {
        impl.criticalOperation();  // No indirection
    }
};

// Pattern selection based on usage
class OptimizedContainer {
public:
    // Strategy pattern for occasional changes
    void setSortStrategy(std::unique_ptr<SortStrategy> strategy) {
        sortStrategy = std::move(strategy);
    }

    // Template specialization for frequent operations
    template<typename Compare>
    void fastSort(Compare comp) {
        std::sort(data.begin(), data.end(), comp);  // Inlined
    }
};
```

---

## Summary

Design Patterns in Modern C++:

**Key Principles:**
1. **Solve actual problems** - don't over-engineer
2. **Common vocabulary** - communicate design intent clearly
3. **Proven solutions** - tested and refined over time
4. **SOLID principles** - patterns support good design principles
5. **Modern C++** enhances pattern implementation

**Pattern Categories:**
- **Creational (5 patterns)**: Factory, Abstract Factory, Builder, Prototype, Singleton
- **Structural (6 patterns)**: Adapter, Bridge, Composite, Decorator, Facade, Proxy
- **Behavioral (11 patterns)**: Observer, Strategy, Command, Template Method, State, Chain of Responsibility, Visitor, Iterator, Mediator, Memento, Null Object

**Modern Enhancements:**
- Smart pointers for automatic memory management
- Lambdas for functional and callback patterns
- Templates for compile-time polymorphism
- Move semantics for efficient object transfer
- Concepts for better template constraints (C++20)

**Best Practices:**
- Choose patterns based on actual requirements
- Combine patterns when solving complex problems
- Prefer composition over inheritance
- Use modern C++ features to simplify implementation
- Focus on testability and maintainability
- Avoid anti-patterns and over-engineering

**Remember:**
Patterns are tools, not goals. Use them when they genuinely improve your design, code clarity, and maintainability. Start simple and add patterns when complexity demands structure.
