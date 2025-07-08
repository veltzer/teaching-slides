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

---

## Singleton Pattern

Ensure only one instance of a class exists

```cpp
class Singleton {
private:
    static std::unique_ptr<Singleton> instance;
    static std::once_flag initFlag;

    // Private constructor
    Singleton() {
        std::cout << "Singleton instance created" << std::endl;
    }

public:
    // Delete copy constructor and assignment operator
    Singleton(const Singleton&) = delete;
    Singleton& operator=(const Singleton&) = delete;

    static Singleton& getInstance() {
        std::call_once(initFlag, []() {
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
std::once_flag Singleton::initFlag;

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

## When to Use Each Pattern

<svg width="550" height="300" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="30" width="450" height="40" fill="#e3f2fd" stroke="#1976d2" stroke-width="2"/>
  <text x="275" y="55" text-anchor="middle" font-size="14">Pattern Selection Guide</text>

  <rect x="50" y="90" width="120" height="80" fill="#e8f5e8" stroke="#4caf50" stroke-width="2"/>
  <text x="110" y="115" text-anchor="middle" font-size="11">Creational</text>
  <text x="110" y="135" text-anchor="middle" font-size="9">Complex object creation</text>
  <text x="110" y="150" text-anchor="middle" font-size="9">Hide implementation</text>
  <text x="110" y="165" text-anchor="middle" font-size="9">Configurable creation</text>

  <rect x="190" y="90" width="120" height="80" fill="#fff3e0" stroke="#f57c00" stroke-width="2"/>
  <text x="250" y="115" text-anchor="middle" font-size="11">Structural</text>
  <text x="250" y="135" text-anchor="middle" font-size="9">Object composition</text>
  <text x="250" y="150" text-anchor="middle" font-size="9">Interface adaptation</text>
  <text x="250" y="165" text-anchor="middle" font-size="9">Hierarchies</text>

  <rect x="330" y="90" width="120" height="80" fill="#f3e5f5" stroke="#7b1fa2" stroke-width="2"/>
  <text x="390" y="115" text-anchor="middle" font-size="11">Behavioral</text>
  <text x="390" y="135" text-anchor="middle" font-size="9">Object interaction</text>
  <text x="390" y="150" text-anchor="middle" font-size="9">Algorithm variation</text>
  <text x="390" y="165" text-anchor="middle" font-size="9">Communication</text>

  <rect x="50" y="190" width="150" height="60" fill="#ffebee" stroke="#d32f2f" stroke-width="2"/>
  <text x="125" y="215" text-anchor="middle" font-size="11">Avoid Over-engineering</text>
  <text x="125" y="235" text-anchor="middle" font-size="9">Simple solutions first</text>

  <rect x="220" y="190" width="150" height="60" fill="#e8f5e8" stroke="#4caf50" stroke-width="2"/>
  <text x="295" y="215" text-anchor="middle" font-size="11">Know When to Apply</text>
  <text x="295" y="235" text-anchor="middle" font-size="9">Solve actual problems</text>

  <rect x="390" y="190" width="150" height="60" fill="#e3f2fd" stroke="#1976d2" stroke-width="2"/>
  <text x="465" y="215" text-anchor="middle" font-size="11">Modern C++ Features</text>
  <text x="465" y="235" text-anchor="middle" font-size="9">Smart pointers, lambdas</text>
</svg>

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
```

---

## Modern C++ and Patterns

How modern C++ features enhance pattern implementation:

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

## Summary

Design Patterns in Modern C++:

1. **Proven solutions** to recurring design problems
1. **Common vocabulary** for communicating design decisions
1. **Structural patterns** help organize object relationships
1. **Creational patterns** manage object instantiation complexity
1. **Behavioral patterns** define object interaction protocols
1. **Modern C++ features** (smart pointers, lambdas, templates) enhance pattern implementation
1. **Combine patterns** to solve complex problems
1. **Apply judiciously** - solve actual problems, not theoretical ones

Patterns are tools, not goals. Use them when they genuinely improve your design.

Pattern
1. Intent: What problem does it solve?
1. Structure: How are classes/objects organized?
1. Participants: What roles do classes play?
1. Consequences: What are the trade-offs?

---

## Pattern Categories

<svg width="550" height="250" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="150" height="150" fill="#e3f2fd" stroke="#1976d2" stroke-width="2"/>
  <text x="125" y="75" text-anchor="middle" font-size="14">Creational</text>
  <text x="125" y="100" text-anchor="middle" font-size="11">Object creation</text>
  <text x="125" y="120" text-anchor="middle" font-size="10">• Factory</text>
  <text x="125" y="140" text-anchor="middle" font-size="10">• Singleton</text>
  <text x="125" y="160" text-anchor="middle" font-size="10">• Builder</text>
  <text x="125" y="180" text-anchor="middle" font-size="10">• Prototype</text>

  <rect x="220" y="50" width="150" height="150" fill="#e8f5e8" stroke="#4caf50" stroke-width="2"/>
  <text x="295" y="75" text-anchor="middle" font-size="14">Structural</text>
  <text x="295" y="100" text-anchor="middle" font-size="11">Object composition</text>
  <text x="295" y="120" text-anchor="middle" font-size="10">• Composite</text>
  <text x="295" y="140" text-anchor="middle" font-size="10">• Bridge</text>
  <text x="295" y="160" text-anchor="middle" font-size="10">• Proxy</text>
  <text x="295" y="180" text-anchor="middle" font-size="10">• Adapter</text>

  <rect x="390" y="50" width="150" height="150" fill="#fff3e0" stroke="#f57c00" stroke-width="2"/>
  <text x="465" y="75" text-anchor="middle" font-size="14">Behavioral</text>
  <text x="465" y="100" text-anchor="middle" font-size="11">Object interaction</text>
  <text x="465" y="120" text-anchor="middle" font-size="10">• Observer</text>
  <text x="465" y="140" text-anchor="middle" font-size="10">• Strategy</text>
  <text x="465" y="160" text-anchor="middle" font-size="10">• Command</text>
  <text x="465" y="180" text-anchor="middle" font-size="10">• Visitor</text>
</svg>

Different patterns solve different types of problems

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
public:
    void operation() override {
        std::cout << "Leaf operation" << std::endl;
    }
};
```

---

## Composite Implementation

```cpp
class Composite : public Component {
private:
    std::vector<std::unique_ptr<Component>> children;

public:
    void operation() override {
        std::cout << "Composite operation:" << std::endl;
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
    auto leaf1 = std::make_unique<Leaf>();
    auto leaf2 = std::make_unique<Leaf>();
    auto leaf3 = std::make_unique<Leaf>();

    // Create composites
    auto composite1 = std::make_unique<Composite>();
    auto composite2 = std::make_unique<Composite>();

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

## Cheshire Cat Benefits

<svg width="500" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="30" width="180" height="140" fill="#e8f5e8" stroke="#4caf50" stroke-width="2"/>
  <text x="140" y="55" text-anchor="middle" font-size="14">Benefits</text>
  <text x="140" y="80" text-anchor="middle" font-size="11">Compilation firewall</text>
  <text x="140" y="100" text-anchor="middle" font-size="11">Binary compatibility</text>
  <text x="140" y="120" text-anchor="middle" font-size="11">Hide dependencies</text>
  <text x="140" y="140" text-anchor="middle" font-size="11">Reduce header size</text>
  <text x="140" y="160" text-anchor="middle" font-size="11">Implementation freedom</text>

  <rect x="270" y="30" width="180" height="140" fill="#ffebee" stroke="#d32f2f" stroke-width="2"/>
  <text x="360" y="55" text-anchor="middle" font-size="14">Costs</text>
  <text x="360" y="80" text-anchor="middle" font-size="11">Extra indirection</text>
  <text x="360" y="100" text-anchor="middle" font-size="11">Memory overhead</text>
  <text x="360" y="120" text-anchor="middle" font-size="11">More complex code</text>
  <text x="360" y="140" text-anchor="middle" font-size="11">Lost inlining</text>
  <text x="360" y="160" text-anchor="middle" font-size="11">Harder debugging</text>
</svg>

Use when interface stability and compilation speed matter

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

## Bridge vs Cheshire Cat

<svg width="550" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="30" width="200" height="140" fill="#e3f2fd" stroke="#1976d2" stroke-width="2"/>
  <text x="150" y="55" text-anchor="middle" font-size="14">Bridge Pattern</text>
  <text x="150" y="80" text-anchor="middle" font-size="11">Multiple implementations</text>
  <text x="150" y="100" text-anchor="middle" font-size="11">Runtime selection</text>
  <text x="150" y="120" text-anchor="middle" font-size="11">Varies independently</text>
  <text x="150" y="140" text-anchor="middle" font-size="11">Platform abstraction</text>
  <text x="150" y="160" text-anchor="middle" font-size="11">Strategy-like</text>

  <rect x="300" y="30" width="200" height="140" fill="#e8f5e8" stroke="#4caf50" stroke-width="2"/>
  <text x="400" y="55" text-anchor="middle" font-size="14">Cheshire Cat</text>
  <text x="400" y="80" text-anchor="middle" font-size="11">Single implementation</text>
  <text x="400" y="100" text-anchor="middle" font-size="11">Compile-time hiding</text>
  <text x="400" y="120" text-anchor="middle" font-size="11">Hide complexity</text>
  <text x="400" y="140" text-anchor="middle" font-size="11">Compilation firewall</text>
  <text x="400" y="160" text-anchor="middle" font-size="11">Performance-focused</text>
</svg>

Choose based on whether you need runtime flexibility or compilation benefits

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
```

---

## Null Object Usage

```cpp
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

// Usage
Service service1;  // Uses NullLogger by default
Service service2(std::make_unique<FileLogger>("app.log"));  // Uses FileLogger
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

## Proxy Pattern Variations

<svg width="550" height="250" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="120" height="80" fill="#e3f2fd" stroke="#1976d2" stroke-width="2"/>
  <text x="110" y="75" text-anchor="middle" font-size="12">Virtual Proxy</text>
  <text x="110" y="95" text-anchor="middle" font-size="10">Lazy loading</text>
  <text x="110" y="110" text-anchor="middle" font-size="10">Expensive objects</text>

  <rect x="190" y="50" width="120" height="80" fill="#e8f5e8" stroke="#4caf50" stroke-width="2"/>
  <text x="250" y="75" text-anchor="middle" font-size="12">Protection Proxy</text>
  <text x="250" y="95" text-anchor="middle" font-size="10">Access control</text>
  <text x="250" y="110" text-anchor="middle" font-size="10">Security checks</text>

  <rect x="330" y="50" width="120" height="80" fill="#fff3e0" stroke="#f57c00" stroke-width="2"/>
  <text x="390" y="75" text-anchor="middle" font-size="12">Remote Proxy</text>
  <text x="390" y="95" text-anchor="middle" font-size="10">Network objects</text>
  <text x="390" y="110" text-anchor="middle" font-size="10">Distributed systems</text>

  <rect x="120" y="150" width="120" height="80" fill="#f3e5f5" stroke="#7b1fa2" stroke-width="2"/>
  <text x="180" y="175" text-anchor="middle" font-size="12">Smart Proxy</text>
  <text x="180" y="195" text-anchor="middle" font-size="10">Reference counting</text>
  <text x="180" y="210" text-anchor="middle" font-size="10">Thread safety</text>

  <rect x="260" y="150" width="120" height="80" fill="#ffebee" stroke="#d32f2f" stroke-width="2"/>
  <text x="320" y="175" text-anchor="middle" font-size="12">Cache Proxy</text>
  <text x="320" y="195" text-anchor="middle" font-size="10">Result caching</text>
  <text x="320" y="210" text-anchor="middle" font-size="10">Performance</text>
</svg>

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

## Factory Pattern

Encapsulate object creation logic

```cpp
enum class DatabaseType {
    MySQL,
    PostgreSQL,
    SQLite
};

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

## Strategy Pattern

Define a family of algorithms and make them interchangeable

```cpp
class
