# Safe Association

---

## What is Safe Association?

Safe association ensures objects maintain valid relationships throughout their lifetimes

Key challenges with raw pointers:
1. **Dangling pointers** - pointing to destroyed objects
1. **Memory leaks** - forgetting to delete allocated memory
1. **Double deletion** - deleting the same memory twice
1. **Ownership ambiguity** - unclear who should delete what

```cpp
// Unsafe association
class Car {
    Engine* engine;  // Who owns this? When to delete?
public:
    Car() : engine(new Engine()) {}
    ~Car() { delete engine; }  // What if engine is shared?
};
```

---

## Association Lifetime Models

<svg width="550" height="250" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="150" height="80" fill="#e3f2fd" stroke="#1976d2" stroke-width="2"/>
  <text x="125" y="75" text-anchor="middle" font-size="12">Independent</text>
  <text x="125" y="95" text-anchor="middle" font-size="10">Objects live</text>
  <text x="125" y="110" text-anchor="middle" font-size="10">independently</text>
  
  <rect x="220" y="50" width="150" height="80" fill="#e8f5e8" stroke="#4caf50" stroke-width="2"/>
  <text x="295" y="75" text-anchor="middle" font-size="12">Structured</text>
  <text x="295" y="95" text-anchor="middle" font-size="10">Owner controls</text>
  <text x="295" y="110" text-anchor="middle" font-size="10">lifetime</text>
  
  <rect x="390" y="50" width="150" height="80" fill="#fff3e0" stroke="#f57c00" stroke-width="2"/>
  <text x="465" y="75" text-anchor="middle" font-size="12">Shared</text>
  <text x="465" y="95" text-anchor="middle" font-size="10">Multiple owners</text>
  <text x="465" y="110" text-anchor="middle" font-size="10">ref counting</text>
  
  <rect x="135" y="150" width="150" height="80" fill="#f3e5f5" stroke="#7b1fa2" stroke-width="2"/>
  <text x="210" y="175" text-anchor="middle" font-size="12">Weak</text>
  <text x="210" y="195" text-anchor="middle" font-size="10">Non-owning</text>
  <text x="210" y="210" text-anchor="middle" font-size="10">observer</text>
  
  <rect x="305" y="150" width="150" height="80" fill="#ffebee" stroke="#d32f2f" stroke-width="2"/>
  <text x="380" y="175" text-anchor="middle" font-size="12">Temporary</text>
  <text x="380" y="195" text-anchor="middle" font-size="10">Short-lived</text>
  <text x="380" y="210" text-anchor="middle" font-size="10">references</text>
</svg>

Different lifetime models require different association strategies

---

## Association for Independent Lifetimes

Objects that exist independently should not manage each other's lifetimes

```cpp
class Person {
    std::string name;
public:
    Person(const std::string& n) : name(n) {}
    const std::string& getName() const { return name; }
};

class Company {
    std::vector<Person*> employees;  // Non-owning pointers
    
public:
    void addEmployee(Person* person) {
        if (person) {
            employees.push_back(person);
        }
    }
    
    void removeEmployee(Person* person) {
        employees.erase(
            std::remove(employees.begin(), employees.end(), person),
            employees.end()
        );
    }
    // No destructor needed - doesn't own employees
};
```

---

## Problems with Raw Pointers

Raw pointers provide no ownership semantics:

```cpp
class Database {
    Connection* conn;
public:
    Database() : conn(new Connection()) {}
    
    // Problem 1: Who deletes conn?
    ~Database() { delete conn; }  // Assumes exclusive ownership
    
    // Problem 2: Copy semantics unclear
    Database(const Database& other) : conn(other.conn) {}  // Shallow copy!
    
    // Problem 3: Assignment issues
    Database& operator=(const Database& other) {
        conn = other.conn;  // Memory leak + double delete
        return *this;
    }
    
    Connection* getConnection() { return conn; }  // Exposes raw pointer
};
```

---

## Structured Lifetimes

Parent objects control the lifetime of their components

```cpp
class Engine {
public:
    void start() { std::cout << "Engine starting\n"; }
    void stop() { std::cout << "Engine stopping\n"; }
};

class Car {
    std::unique_ptr<Engine> engine;  // Car owns the engine
    std::string model;
    
public:
    Car(const std::string& m) 
        : engine(std::make_unique<Engine>()), model(m) {}
    
    void startCar() {
        engine->start();
        std::cout << model << " is running\n";
    }
    
    // No explicit destructor needed - unique_ptr handles cleanup
};
```

---

## Introducing unique_ptr

`std::unique_ptr` provides exclusive ownership semantics:

```cpp
#include <memory>

class Resource {
public:
    Resource() { std::cout << "Resource created\n"; }
    ~Resource() { std::cout << "Resource destroyed\n"; }
    void use() { std::cout << "Using resource\n"; }
};

void demonstrateUniquePtr() {
    std::unique_ptr<Resource> ptr = std::make_unique<Resource>();
    
    ptr->use();           // Access through ->
    (*ptr).use();         // Access through *
    
    if (ptr) {            // Check if not null
        ptr->use();
    }
    
    std::unique_ptr<Resource> ptr2 = std::move(ptr);  // Transfer ownership
    // ptr is now null, ptr2 owns the resource
    
    ptr2.reset();         // Explicitly delete the resource
    ptr2 = std::make_unique<Resource>();  // Create new resource
    
    // Automatic cleanup when ptr2 goes out of scope
}
```

---

## unique_ptr Benefits

<svg width="500" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="30" width="180" height="140" fill="#e8f5e8" stroke="#4caf50" stroke-width="2"/>
  <text x="140" y="55" text-anchor="middle" font-size="14">unique_ptr</text>
  <text x="140" y="80" text-anchor="middle" font-size="11">Automatic cleanup</text>
  <text x="140" y="100" text-anchor="middle" font-size="11">Move semantics</text>
  <text x="140" y="120" text-anchor="middle" font-size="11">Zero overhead</text>
  <text x="140" y="140" text-anchor="middle" font-size="11">Exception safe</text>
  <text x="140" y="160" text-anchor="middle" font-size="11">Clear ownership</text>
  
  <rect x="270" y="30" width="180" height="140" fill="#ffebee" stroke="#d32f2f" stroke-width="2"/>
  <text x="360" y="55" text-anchor="middle" font-size="14">Raw Pointers</text>
  <text x="360" y="80" text-anchor="middle" font-size="11">Manual cleanup</text>
  <text x="360" y="100" text-anchor="middle" font-size="11">Copy confusion</text>
  <text x="360" y="120" text-anchor="middle" font-size="11">Memory leaks</text>
  <text x="360" y="140" text-anchor="middle" font-size="11">Exception unsafe</text>
  <text x="360" y="160" text-anchor="middle" font-size="11">Unclear ownership</text>
</svg>

`unique_ptr` eliminates common memory management errors

---

## Wrapping new

Never use raw `new` - always wrap in smart pointers:

```cpp
// Bad - exception unsafe
void riskyFunction() {
    Resource* resource = new Resource();
    
    // If this throws, resource leaks!
    potentiallyThrowingFunction();
    
    delete resource;  // May never be reached
}

// Good - exception safe
void safeFunction() {
    auto resource = std::make_unique<Resource>();
    
    // If this throws, resource is automatically cleaned up
    potentiallyThrowingFunction();
    
    // No explicit delete needed
}

// Even better - use factory functions
std::unique_ptr<Database> createDatabase(const std::string& url) {
    return std::make_unique<Database>(url);
}
```

---

## Custom Deleters

`unique_ptr` supports custom deletion strategies:

```cpp
// Custom deleter for C-style APIs
struct FileDeleter {
    void operator()(FILE* file) {
        if (file) {
            std::fclose(file);
            std::cout << "File closed\n";
        }
    }
};

using FilePtr = std::unique_ptr<FILE, FileDeleter>;

FilePtr openFile(const char* filename) {
    FILE* file = std::fopen(filename, "r");
    return FilePtr(file);  // Will auto-close when destroyed
}

// Lambda deleter
auto createBuffer() {
    return std::unique_ptr<int[], std::function<void(int*)>>(
        new int[100],
        [](int* ptr) { 
            std::cout << "Deleting array\n";
            delete[] ptr; 
        }
    );
}
```

---

## Pointer Function Parameters

Guidelines for function parameters with smart pointers:

```cpp
class Widget {
public:
    void process();
};

// Prefer raw pointers for parameters (non-owning)
void processWidget(Widget* widget) {
    if (widget) {
        widget->process();
    }
}

// Use references when null is not allowed
void processWidget(Widget& widget) {
    widget.process();
}

// Use unique_ptr only when transferring ownership
void takeOwnership(std::unique_ptr<Widget> widget) {
    // Function now owns the widget
    widget->process();
}

// Usage
auto widget = std::make_unique<Widget>();
processWidget(widget.get());      // Non-owning access
takeOwnership(std::move(widget)); // Transfer ownership
```

---

## Shared Ownership with shared_ptr

`std::shared_ptr` enables multiple owners through reference counting:

```cpp
#include <memory>

class Document {
    std::string content;
public:
    Document(const std::string& text) : content(text) {}
    const std::string& getContent() const { return content; }
    void edit(const std::string& newContent) { content = newContent; }
};

class Editor {
    std::shared_ptr<Document> doc;
public:
    Editor(std::shared_ptr<Document> d) : doc(d) {}
    void editDocument() { doc->edit("Modified content"); }
};

class Viewer {
    std::shared_ptr<Document> doc;
public:
    Viewer(std::shared_ptr<Document> d) : doc(d) {}
    void viewDocument() { std::cout << doc->getContent() << std::endl; }
};
```

---

## shared_ptr Reference Counting

<svg width="500" height="250" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="100" height="60" fill="#e3f2fd" stroke="#1976d2" stroke-width="2"/>
  <text x="100" y="75" text-anchor="middle" font-size="10">shared_ptr</text>
  <text x="100" y="90" text-anchor="middle" font-size="10">count: 3</text>
  
  <rect x="50" y="130" width="100" height="60" fill="#e3f2fd" stroke="#1976d2" stroke-width="2"/>
  <text x="100" y="155" text-anchor="middle" font-size="10">shared_ptr</text>
  <text x="100" y="170" text-anchor="middle" font-size="10">count: 3</text>
  
  <rect x="50" y="210" width="100" height="60" fill="#e3f2fd" stroke="#1976d2" stroke-width="2"/>
  <text x="100" y="235" text-anchor="middle" font-size="10">shared_ptr</text>
  <text x="100" y="250" text-anchor="middle" font-size="10">count: 3</text>
  
  <line x1="150" y1="80" x2="200" y2="80" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="150" y1="160" x2="200" y2="120" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="150" y1="240" x2="200" y2="160" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/>
  
  <rect x="200" y="80" width="120" height="80" fill="#e8f5e8" stroke="#4caf50" stroke-width="2"/>
  <text x="260" y="105" text-anchor="middle" font-size="12">Object</text>
  <text x="260" y="125" text-anchor="middle" font-size="10">Control Block</text>
  <text x="260" y="145" text-anchor="middle" font-size="10">ref_count: 3</text>
  
  <rect x="350" y="100" width="100" height="40" fill="#fff3e0" stroke="#f57c00" stroke-width="2"/>
  <text x="400" y="125" text-anchor="middle" font-size="10">Shared Data</text>
  
  <line x1="320" y1="120" x2="350" y2="120" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/>
  
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#333"/>
    </marker>
  </defs>
</svg>

Object is destroyed when reference count reaches zero

---

## shared_ptr Usage Patterns

```cpp
void demonstrateSharedPtr() {
    // Create shared resource
    auto doc = std::make_shared<Document>("Initial content");
    std::cout << "Reference count: " << doc.use_count() << std::endl; // 1
    
    {
        Editor editor(doc);  // Share ownership
        Viewer viewer(doc);  // Share ownership
        std::cout << "Reference count: " << doc.use_count() << std::endl; // 3
        
        // Both editor and viewer can safely use the document
        editor.editDocument();
        viewer.viewDocument();
        
    } // editor and viewer destroyed, count decreases
    
    std::cout << "Reference count: " << doc.use_count() << std::endl; // 1
    
    // Document still alive because doc still holds it
    std::cout << doc->getContent() << std::endl;
    
} // doc destroyed, document finally deleted
```

---

## Circular References Problem

`shared_ptr` can create memory leaks with circular references:

```cpp
class Node {
public:
    std::shared_ptr<Node> next;
    std::shared_ptr<Node> prev;  // Creates circular reference!
    
    Node() { std::cout << "Node created\n"; }
    ~Node() { std::cout << "Node destroyed\n"; }
};

void createCircularReference() {
    auto node1 = std::make_shared<Node>();
    auto node2 = std::make_shared<Node>();
    
    node1->next = node2;  // node1 holds node2
    node2->prev = node1;  // node2 holds node1
    
    // Memory leak! Neither can be destroyed because
    // each holds a reference to the other
}
```

---

## Introducing weak_ptr

`std::weak_ptr` breaks circular references by providing non-owning observation:

```cpp
class Node {
public:
    std::shared_ptr<Node> next;      // Owning reference
    std::weak_ptr<Node> prev;        // Non-owning reference
    
    Node() { std::cout << "Node created\n"; }
    ~Node() { std::cout << "Node destroyed\n"; }
};

void createSafeList() {
    auto node1 = std::make_shared<Node>();
    auto node2 = std::make_shared<Node>();
    
    node1->next = node2;       // Ownership: node1 -> node2
    node2->prev = node1;       // Weak reference: node2 observes node1
    
    // No circular ownership - proper cleanup occurs
}
```

---

## Using weak_ptr Safely

`weak_ptr` must be converted to `shared_ptr` before use:

```cpp
class Observer {
    std::weak_ptr<Document> doc;
    
public:
    Observer(std::shared_ptr<Document> d) : doc(d) {}
    
    void checkDocument() {
        // Convert weak_ptr to shared_ptr
        if (auto shared_doc = doc.lock()) {
            // Safe to use - object is guaranteed to live
            std::cout << "Document exists: " << shared_doc->getContent() << std::endl;
        } else {
            std::cout << "Document has been destroyed" << std::endl;
        }
    }
    
    bool isDocumentAlive() const {
        return !doc.expired();  // Check without locking
    }
};
```

---

## weak_ptr Lock Patterns

<svg width="500" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="120" height="100" fill="#fff3e0" stroke="#f57c00" stroke-width="2"/>
  <text x="110" y="75" text-anchor="middle" font-size="12">weak_ptr</text>
  <text x="110" y="100" text-anchor="middle" font-size="10">Non-owning</text>
  <text x="110" y="120" text-anchor="middle" font-size="10">May be null</text>
  
  <text x="200" y="105" text-anchor="middle" font-size="14">lock()</text>
  
  <rect x="250" y="50" width="120" height="100" fill="#e8f5e8" stroke="#4caf50" stroke-width="2"/>
  <text x="310" y="75" text-anchor="middle" font-size="12">shared_ptr</text>
  <text x="310" y="100" text-anchor="middle" font-size="10">Temporary owner</text>
  <text x="310" y="120" text-anchor="middle" font-size="10">Safe to use</text>
  
  <line x1="170" y1="100" x2="200" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="220" y1="100" x2="250" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/>
</svg>

Always check the result of `lock()` before using the object

---

## Smart Pointer Performance

Performance characteristics of different smart pointers:

```cpp
#include <chrono>
#include <memory>

class TestObject {
    int data[100];  // Some data to make object non-trivial
public:
    TestObject() { /* initialize */ }
    void doWork() { /* some work */ }
};

void performanceComparison() {
    const int iterations = 1000000;
    
    // Raw pointer (baseline)
    auto start = std::chrono::high_resolution_clock::now();
    for (int i = 0; i < iterations; ++i) {
        TestObject* obj = new TestObject();
        obj->doWork();
        delete obj;
    }
    auto end = std::chrono::high_resolution_clock::now();
    auto raw_time = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
    
    // unique_ptr (minimal overhead)
    start = std::chrono::high_resolution_clock::now();
    for (int i = 0; i < iterations; ++i) {
        auto obj = std::make_unique<TestObject>();
        obj->doWork();
    }
    end = std::chrono::high_resolution_clock::now();
    auto unique_time = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
}
```

---

## Safe Copying with Association

Implement safe copy semantics with smart pointers:

```cpp
class Document {
    std::string content;
public:
    Document(const std::string& text) : content(text) {}
    Document(const Document& other) : content(other.content) {
        std::cout << "Document copied\n";
    }
    const std::string& getContent() const { return content; }
};

class Editor {
    std::shared_ptr<Document> doc;
    
public:
    Editor(std::shared_ptr<Document> d) : doc(d) {}
    
    // Copy constructor - shares the document
    Editor(const Editor& other) : doc(other.doc) {}
    
    // Deep copy method when needed
    Editor deepCopy() const {
        auto newDoc = std::make_shared<Document>(*doc);  // Copy document
        return Editor(newDoc);
    }
    
    void editDocument(const std::string& newContent) {
        // Create new document if shared to avoid affecting others
        if (doc.use_count() > 1) {
            doc = std::make_shared<Document>(*doc);  // Copy-on-write
        }
        doc->edit(newContent);
    }
};
```

---

## Copy-on-Write Pattern

Implement copy-on-write for efficient sharing:

```cpp
class CowString {
private:
    std::shared_ptr<std::string> data;
    
    void ensureUnique() {
        if (data.use_count() > 1) {
            data = std::make_shared<std::string>(*data);  // Copy only when needed
        }
    }
    
public:
    CowString(const std::string& str) 
        : data(std::make_shared<std::string>(str)) {}
    
    // Copy is cheap - just share the data
    CowString(const CowString& other) : data(other.data) {}
    
    // Non-const access triggers copy-on-write
    std::string& get() {
        ensureUnique();
        return *data;
    }
    
    // Const access is always safe
    const std::string& get() const {
        return *data;
    }
    
    // Assignment
    CowString& operator=(const CowString& other) {
        data = other.data;  // Share the data
        return *this;
    }
};
```

---

## RAII and Smart Pointers

Resource Acquisition Is Initialization works perfectly with smart pointers:

```cpp
class FileManager {
    std::unique_ptr<FILE, std::function<void(FILE*)>> file;
    
public:
    FileManager(const std::string& filename) {
        FILE* f = std::fopen(filename.c_str(), "r");
        if (!f) {
            throw std::runtime_error("Cannot open file");
        }
        
        file = std::unique_ptr<FILE, std::function<void(FILE*)>>(
            f,
            [](FILE* ptr) { 
                if (ptr) {
                    std::fclose(ptr);
                    std::cout << "File closed\n";
                }
            }
        );
    }
    
    FILE* get() const { return file.get(); }
    
    // Automatic cleanup in destructor - no explicit code needed
};
```

---

## Exception Safety with Smart Pointers

Smart pointers provide strong exception safety guarantees:

```cpp
class Service {
    std::unique_ptr<Database> db;
    std::unique_ptr<Logger> logger;
    
public:
    Service(const std::string& dbUrl, const std::string& logFile) {
        // If any constructor throws, previous objects are cleaned up automatically
        db = std::make_unique<Database>(dbUrl);
        logger = std::make_unique<Logger>(logFile);
        
        // If this throws, both db and logger are cleaned up
        initializeService();
    }
    
    void processRequest(const Request& req) {
        auto transaction = std::make_unique<Transaction>();
        
        try {
            transaction->begin();
            db->execute(req.getQuery());
            logger->log("Request processed");
            transaction->commit();
        } catch (...) {
            // transaction automatically rolls back in destructor
            throw;
        }
    }
};
```

---

## Smart Pointer Factory Pattern

Use factories to encapsulate object creation:

```cpp
class ConnectionFactory {
public:
    static std::unique_ptr<Database> createDatabase(const std::string& type, 
                                                   const std::string& url) {
        if (type == "mysql") {
            return std::make_unique<MySQLDatabase>(url);
        } else if (type == "postgres") {
            return std::make_unique<PostgreSQLDatabase>(url);
        } else {
            throw std::invalid_argument("Unknown database type");
        }
    }
    
    static std::shared_ptr<ConnectionPool> createPool(const std::string& type,
                                                     const std::string& url,
                                                     size_t poolSize) {
        auto pool = std::make_shared<ConnectionPool>();
        for (size_t i = 0; i < poolSize; ++i) {
            pool->addConnection(createDatabase(type, url));
        }
        return pool;
    }
};
```

---

## Polymorphism with Smart Pointers

Smart pointers work seamlessly with polymorphism:

```cpp
class Shape {
public:
    virtual ~Shape() = default;
    virtual void draw() = 0;
    virtual double area() = 0;
};

class Circle : public Shape {
    double radius;
public:
    Circle(double r) : radius(r) {}
    void draw() override { std::cout << "Drawing circle\n"; }
    double area() override { return 3.14159 * radius * radius; }
};

class ShapeManager {
    std::vector<std::unique_ptr<Shape>> shapes;
    
public:
    void addShape(std::unique_ptr<Shape> shape) {
        shapes.push_back(std::move(shape));
    }
    
    double totalArea() const {
        double total = 0;
        for (const auto& shape : shapes) {
            total += shape->area();  // Polymorphic call
        }
        return total;
    }
};
```

---

## Observer Pattern with weak_ptr

Implement the observer pattern safely:

```cpp
class Subject {
    std::vector<std::weak_ptr<Observer>> observers;
    
public:
    void addObserver(std::shared_ptr<Observer> observer) {
        observers.push_back(observer);
    }
    
    void notifyObservers() {
        // Remove expired observers while notifying
        observers.erase(
            std::remove_if(observers.begin(), observers.end(),
                [this](const std::weak_ptr<Observer>& weak_obs) {
                    if (auto obs = weak_obs.lock()) {
                        obs->update(this);
                        return false;  // Keep this observer
                    }
                    return true;  // Remove expired observer
                }),
            observers.end()
        );
    }
};
```

---

## Memory Pool with Smart Pointers

Combine smart pointers with custom memory management:

```cpp
template<typename T>
class PoolAllocator {
    std::vector<std::unique_ptr<T>> pool;
    std::stack<T*> available;
    
public:
    PoolAllocator(size_t poolSize) {
        for (size_t i = 0; i < poolSize; ++i) {
            auto obj = std::make_unique<T>();
            available.push(obj.get());
            pool.push_back(std::move(obj));
        }
    }
    
    std::shared_ptr<T> acquire() {
        if (available.empty()) {
            throw std::runtime_error("Pool exhausted");
        }
        
        T* ptr = available.top();
        available.pop();
        
        return std::shared_ptr<T>(ptr, [this](T* p) {
            this->release(p);  // Return to pool instead of deleting
        });
    }
    
private:
    void release(T* ptr) {
        available.push(ptr);
    }
};
```

---

## Thread Safety Considerations

Smart pointers have specific thread safety guarantees:

```cpp
#include <atomic>
#include <mutex>

class ThreadSafeCounter {
    std::atomic<std::shared_ptr<int>> counter;
    
public:
    ThreadSafeCounter() : counter(std::make_shared<int>(0)) {}
    
    void increment() {
        std::shared_ptr<int> old_counter;
        std::shared_ptr<int> new_counter;
        
        do {
            old_counter = counter.load();
            new_counter = std::make_shared<int>(*old_counter + 1);
        } while (!counter.compare_exchange_weak(old_counter, new_counter));
    }
    
    int getValue() const {
        return *counter.load();
    }
};

// For shared_ptr itself: reference counting is thread-safe,
// but object access is not
std::shared_ptr<Document> global_doc;
std::mutex doc_mutex;

void safeAccess() {
    std::lock_guard<std::mutex> lock(doc_mutex);
    if (global_doc) {
        global_doc->edit("New content");  // Protected access
    }
}
```

---

## Common Smart Pointer Mistakes

Avoid these common pitfalls:

```cpp
// Mistake 1: Double management
void badExample1() {
    auto ptr = new int(42);
    std::unique_ptr<int> smart1(ptr);
    std::unique_ptr<int> smart2(ptr);  // Double delete!
}

// Mistake 2: Circular shared_ptr
class BadNode {
public:
    std::shared_ptr<BadNode> parent;  // Should be weak_ptr
    std::shared_ptr<BadNode> child;
};

// Mistake 3: Unnecessary shared_ptr
void badExample3(std::shared_ptr<int> value) {  // Should be int or const int&
    std::cout << *value << std::endl;  // No ownership transfer needed
}

// Mistake 4: get() with new ownership
void badExample4() {
    auto smart = std::make_unique<int>(42);
    std::unique_ptr<int> another(smart.get());  // Double delete!
}

// Correct approaches
void goodExample() {
    auto smart = std::make_unique<int>(42);
    processValue(*smart);              // Pass by reference
    processPointer(smart.get());       // Pass raw pointer (non-owning)
    auto moved = std::move(smart);     // Transfer ownership
}

---

## Smart Pointer Guidelines

Best practices for using smart pointers effectively:

**Ownership Rules:**
1. Use `std::unique_ptr` by default
1. Use `std::shared_ptr` only when sharing is necessary
1. Use `std::weak_ptr` to break cycles
1. Prefer `make_unique` and `make_shared`
1. Never mix smart pointers with raw `new`/`delete`

```cpp
// Good patterns
auto resource = std::make_unique<Resource>();
auto shared = std::make_shared<Document>("content");
std::weak_ptr<Node> parent_ref = node->parent;

// Bad patterns
std::unique_ptr<Resource> resource(new Resource());  // Not exception safe
auto ptr = shared.get(); delete ptr;                 // Manual delete
```

---

## Performance Comparison

<svg width="550" height="250" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="100" height="40" fill="#ffebee" stroke="#d32f2f" stroke-width="2"/>
  <text x="100" y="75" text-anchor="middle" font-size="12">Raw Pointer</text>
  
  <rect x="170" y="50" width="100" height="40" fill="#e8f5e8" stroke="#4caf50" stroke-width="2"/>
  <text x="220" y="75" text-anchor="middle" font-size="12">unique_ptr</text>
  
  <rect x="290" y="50" width="100" height="40" fill="#fff3e0" stroke="#f57c00" stroke-width="2"/>
  <text x="340" y="75" text-anchor="middle" font-size="12">shared_ptr</text>
  
  <rect x="410" y="50" width="100" height="40" fill="#f3e5f5" stroke="#7b1fa2" stroke-width="2"/>
  <text x="460" y="75" text-anchor="middle" font-size="12">weak_ptr</text>
  
  <rect x="50" y="110" width="100" height="30" fill="#ffcdd2"/>
  <text x="100" y="130" text-anchor="middle" font-size="10">Creation: Fast</text>
  
  <rect x="170" y="110" width="100" height="30" fill="#c8e6c8"/>
  <text x="220" y="130" text-anchor="middle" font-size="10">Creation: Fast</text>
  
  <rect x="290" y="110" width="100" height="30" fill="#ffe0b2"/>
  <text x="340" y="130" text-anchor="middle" font-size="10">Creation: Slow</text>
  
  <rect x="410" y="110" width="100" height="30" fill="#e1bee7"/>
  <text x="460" y="130" text-anchor="middle" font-size="10">Creation: Medium</text>
  
  <rect x="50" y="150" width="100" height="30" fill="#ffcdd2"/>
  <text x="100" y="170" text-anchor="middle" font-size="10">Copy: Fast</text>
  
  <rect x="170" y="150" width="100" height="30" fill="#ffcdd2"/>
  <text x="220" y="170" text-anchor="middle" font-size="10">Copy: Move only</text>
  
  <rect x="290" y="150" width="100" height="30" fill="#ffe0b2"/>
  <text x="340" y="170" text-anchor="middle" font-size="10">Copy: Atomic ops</text>
  
  <rect x="410" y="150" width="100" height="30" fill="#c8e6c8"/>
  <text x="460" y="170" text-anchor="middle" font-size="10">Copy: Fast</text>
  
  <rect x="50" y="190" width="100" height="30" fill="#ffcdd2"/>
  <text x="100" y="210" text-anchor="middle" font-size="10">Safety: Poor</text>
  
  <rect x="170" y="190" width="100" height="30" fill="#c8e6c8"/>
  <text x="220" y="210" text-anchor="middle" font-size="10">Safety: Excellent</text>
  
  <rect x="290" y="190" width="100" height="30" fill="#c8e6c8"/>
  <text x="340" y="210" text-anchor="middle" font-size="10">Safety: Excellent</text>
  
  <rect x="410" y="190" width="100" height="30" fill="#c8e6c8"/>
  <text x="460" y="210" text-anchor="middle" font-size="10">Safety: Excellent</text>
</svg>

Choose the right smart pointer based on your performance and safety needs

---

## Migration Strategy

Migrating from raw pointers to smart pointers:

```cpp
// Step 1: Identify ownership
class OldClass {
    Resource* owned;      // This should be unique_ptr
    Resource* borrowed;   // This should stay raw pointer
    Resource* shared;     // This might be shared_ptr
    
public:
    OldClass() : owned(new Resource()), borrowed(nullptr), shared(nullptr) {}
    ~OldClass() { delete owned; }  // Only delete owned resources
};

// Step 2: Replace owned pointers
class NewClass {
    std::unique_ptr<Resource> owned;
    Resource* borrowed;                    // Non-owning, keep as raw
    std::shared_ptr<Resource> shared;
    
public:
    NewClass() : owned(std::make_unique<Resource>()), borrowed(nullptr) {}
    // No destructor needed - automatic cleanup
    
    void setBorrowed(Resource* res) { borrowed = res; }
    void setShared(std::shared_ptr<Resource> res) { shared = res; }
};
```

---

## Summary

Safe Association in Modern C++:

1. **Smart pointers eliminate** manual memory management errors
1. **unique_ptr provides** zero-overhead exclusive ownership
1. **shared_ptr enables** safe shared ownership with reference counting
1. **weak_ptr breaks** circular references and provides safe observation
1. **RAII with smart pointers** ensures exception safety
1. **Factory functions** encapsulate creation and improve safety
1. **Clear ownership semantics** make code more maintainable

Smart pointers are essential for writing robust, safe C++ code that properly manages object relationships and lifetimes.
