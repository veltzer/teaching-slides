# Functional Abstraction

---

## Chapter Overview

1. Events and callbacks
1. The Command pattern
1. Functor Commands
1. Lambda, an alternatives to functors
1. Wrapping Traditional callbacks
1. Member function pointers
1. Function pointer adapters

---

## The Need for Functional Abstraction

- Decoupling code through callbacks
- Event-driven programming
- Delayed execution
- Customizable algorithms
- Plugin architectures

---

## Traditional C-Style Callbacks

```cpp
// Function pointer type
typedef void (*Callback)(int);

// Function that uses callback
void process(int data, Callback cb) {
    // Do some processing...
    cb(data * 2);
}

// Callback implementation
void myCallback(int value) {
    std::cout << "Result: " << value << std::endl;
}

process(42, myCallback);
```

---

## Limitations of Function Pointers

- No state capture
- Type safety issues
- Cannot use member functions directly
- No inline optimization opportunities
- Difficult syntax for complex signatures

---

## The Command Pattern

![the_command_pattern](/svg/courses/languages/c++/modern-c++-for-c-programmers/17_functional_abstraction/the_command_pattern.svg)

---

## Command Pattern Implementation

```cpp
class Command {
public:
    virtual ~Command() = default;
    virtual void execute() = 0;
};

class PrintCommand : public Command {
private:
    std::string message;
public:
    PrintCommand(const std::string& msg) : message(msg) {}
    void execute() override {
        std::cout << message << std::endl;
    }
};
```

---

## Command Pattern Usage

```cpp
class Button {
private:
    std::unique_ptr<Command> command;
public:
    void setCommand(std::unique_ptr<Command> cmd) {
        command = std::move(cmd);
    }

    void click() {
        if (command) {
            command->execute();
        }
    }
};

Button button;
button.setCommand(std::make_unique<PrintCommand>("Button clicked!"));
button.click();
```

---

## Functors (Function Objects)

```cpp
class Multiplier {
private:
    int factor;
public:
    Multiplier(int f) : factor(f) {}

    int operator()(int value) const {
        return value * factor;
    }
};

// Usage
Multiplier times3(3);
std::cout << times3(10) << std::endl;  // 30

std::vector<int> nums{1, 2, 3, 4, 5};
std::transform(nums.begin(), nums.end(), nums.begin(), times3);
```

---

## Advantages of Functors

- Can maintain state
- Type safe
- Can be inlined by compiler
- Work with STL algorithms
- Can have multiple operator() overloads

---

## Functor Templates

```cpp
template<typename T>
class Comparator {
private:
    bool ascending;
public:
    Comparator(bool asc = true) : ascending(asc) {}

    bool operator()(const T& a, const T& b) const {
        return ascending ? (a < b) : (a > b);
    }
};

std::vector<int> values{3, 1, 4, 1, 5, 9};
std::sort(values.begin(), values.end(), Comparator<int>(false));
```

---

## Lambda Expressions

```cpp
// Basic lambda
auto add = [](int a, int b) { return a + b; };
std::cout << add(3, 4) << std::endl;  // 7

// Lambda with capture
int multiplier = 10;
auto times = [multiplier](int x) { return x * multiplier; };
std::cout << times(5) << std::endl;  // 50
```

---

## Lambda Capture Modes

```cpp
int x = 10, y = 20;

// Capture by value
auto lambda1 = [x, y]() { return x + y; };

// Capture by reference
auto lambda2 = [&x, &y]() { x++; y++; return x + y; };

// Capture all by value
auto lambda3 = [=]() { return x + y; };

// Capture all by reference
auto lambda4 = [&]() { return x + y; };

// Mixed capture
auto lambda5 = [x, &y]() { y = x * 2; return y; };
```

---

## Mutable Lambdas

```cpp
int counter = 0;

// Error: cannot modify captured value
// auto inc1 = [counter]() { return ++counter; };

// OK: mutable lambda
auto inc2 = [counter]() mutable { return ++counter; };

std::cout << inc2() << std::endl;  // 1
std::cout << inc2() << std::endl;  // 2
std::cout << counter << std::endl; // 0 (original unchanged)
```

---

## Generic Lambdas (C++14)

```cpp
// Generic lambda
auto print = [](const auto& value) {
    std::cout << value << std::endl;
};

print(42);          // int
print(3.14);        // double
print("Hello");     // const char*

// Generic lambda with multiple parameters
auto multiply = [](auto a, auto b) { return a * b; };
```

---

## std::function

```cpp
#include <functional>

// std::function can hold any callable
std::function<int(int, int)> operation;

// Can hold function pointer
int add(int a, int b) { return a + b; }
operation = add;

// Can hold lambda
operation = [](int a, int b) { return a * b; };

// Can hold functor
struct Divider {
    int operator()(int a, int b) { return a / b; }
};
operation = Divider();
```

---

## std::function Performance

```cpp
class Calculator {
private:
    std::vector<std::function<double(double, double)>> operations;
public:
    void addOperation(std::function<double(double, double)> op) {
        operations.push_back(op);
    }

    std::vector<double> calculate(double a, double b) {
        std::vector<double> results;
        for (const auto& op : operations) {
            results.push_back(op(a, b));
        }
        return results;
    }
};
```

---

## Wrapping Traditional Callbacks

```cpp
// C-style callback API
typedef void (*EventHandler)(int code, void* userData);

void registerHandler(EventHandler handler, void* userData);

// C++ wrapper
class EventManager {
private:
    std::function<void(int)> callback;

    static void staticHandler(int code, void* userData) {
        auto* mgr = static_cast<EventManager*>(userData);
        mgr->callback(code);
    }
public:
    void setHandler(std::function<void(int)> cb) {
        callback = cb;
        registerHandler(staticHandler, this);
    }
};
```

---

## Member Function Pointers

```cpp
class Widget {
public:
    void show() { std::cout << "Showing widget\n"; }
    void hide() { std::cout << "Hiding widget\n"; }
    int getValue() const { return 42; }
};

// Member function pointer types
void (Widget::*action)() = &Widget::show;
int (Widget::*getter)() const = &Widget::getValue;

// Usage
Widget w;
(w.*action)();  // Call through object

Widget* pw = &w;
(pw->*action)(); // Call through pointer
```

---

## std::mem_fn

```cpp
#include <functional>

class Task {
public:
    void execute() { std::cout << "Executing task\n"; }
    bool isComplete() const { return false; }
};

// Convert member function to callable
auto exec = std::mem_fn(&Task::execute);
auto check = std::mem_fn(&Task::isComplete);

Task t;
exec(t);  // Calls t.execute()

std::vector<Task> tasks(5);
// Use with algorithms
std::for_each(tasks.begin(), tasks.end(), std::mem_fn(&Task::execute));
```

---

## std::bind

```cpp
void processData(int id, const std::string& name, double value) {
    std::cout << "ID: " << id << ", Name: " << name
              << ", Value: " << value << std::endl;
}

// Bind some parameters
auto processUser = std::bind(processData, 42, std::placeholders::_1, 3.14);
processUser("Alice");  // ID: 42, Name: Alice, Value: 3.14

// Bind member functions
Widget w;
auto showWidget = std::bind(&Widget::show, &w);
showWidget();  // Calls w.show()
```

---

## std::bind with Reordering

```cpp
void display(const std::string& prefix, int value, const std::string& suffix) {
    std::cout << prefix << value << suffix << std::endl;
}

// Reorder parameters
auto reordered = std::bind(display,
    std::placeholders::_2,  // second arg becomes prefix
    std::placeholders::_1,  // first arg becomes value
    std::placeholders::_3); // third arg becomes suffix

reordered(42, "Value: ", "!");  // Prints: Value: 42!
```

---

## Function Adapter Pattern

```cpp
template<typename Signature>
class FunctionAdapter;

template<typename R, typename... Args>
class FunctionAdapter<R(Args...)> {
private:
    std::function<R(Args...)> fn;
public:
    template<typename F>
    FunctionAdapter(F&& f) : fn(std::forward<F>(f)) {}

    R operator()(Args... args) const {
        // Add pre/post processing
        std::cout << "Calling function...\n";
        R result = fn(args...);
        std::cout << "Function completed.\n";
        return result;
    }
};
```

---

## Combining Techniques

```cpp
class EventDispatcher {
private:
    std::unordered_map<std::string,
        std::vector<std::function<void(const Event&)>>> handlers;
public:
    template<typename F>
    void subscribe(const std::string& eventType, F&& handler) {
        handlers[eventType].push_back(std::forward<F>(handler));
    }

    void dispatch(const std::string& eventType, const Event& event) {
        auto it = handlers.find(eventType);
        if (it != handlers.end()) {
            for (const auto& handler : it->second) {
                handler(event);
            }
        }
    }
};
```

---

## Performance Considerations

![performance_considerations](/svg/courses/languages/c++/modern-c++-for-c-programmers/17_functional_abstraction/performance_considerations.svg)

---

## Best Practices

1. Use lambdas for local, short-lived callbacks
1. Prefer functors for stateful, reusable operations
1. Use std::function for type erasure when needed
1. Avoid std::bind in modern C++ (use lambdas)
1. Consider performance implications
1. Be careful with lambda captures (especially references)

---

## Common Pitfalls

```cpp
// Dangling reference
std::function<int()> makeCounter() {
    int count = 0;
    return [&count]() { return ++count; };  // BAD: captures local by ref
}

// Correct version
std::function<int()> makeCounter() {
    return [count = 0]() mutable { return ++count; };  // C++14
}

// Or with shared state
std::function<int()> makeCounter() {
    auto count = std::make_shared<int>(0);
    return [count]() { return ++(*count); };
}
```

---

## Real-World Example: GUI Event System

```cpp
class Button {
private:
    std::function<void()> onClick;
public:
    void setClickHandler(std::function<void()> handler) {
        onClick = std::move(handler);
    }

    void click() {
        if (onClick) onClick();
    }
};

class Calculator {
    Display display;
    double accumulator = 0;
public:
    void setupUI() {
        Button addBtn;
        addBtn.setClickHandler([this]() {
            accumulator += display.getValue();
            display.setValue(accumulator);
        });
    }
};
```

---

## Summary

- Function pointers: Simple but limited
- Command pattern: OOP approach to callbacks
- Functors: Stateful function objects
- Lambdas: Modern, flexible, inline callbacks
- std::function: Type-erased callable wrapper
- std::bind/std::mem_fn: Adapter utilities
- Choose the right tool for each use case

---

## Next Chapter: Containers

- STL Container Classes
- Container Selection
- Iterators and Algorithms
- Advanced container usage
