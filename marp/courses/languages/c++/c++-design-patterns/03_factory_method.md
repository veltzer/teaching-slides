# Factory Method Pattern

---

## Intent

- Define an interface for creating objects, but let subclasses decide which class to instantiate
- Decouple object creation from usage
- Enable extension without modifying existing code

---

## Problem: Direct Construction Couples Code

```cpp
// Tightly coupled - hard to extend
void processDocument(const std::string& type) {
    Document* doc;
    if (type == "pdf") {
        doc = new PDFDocument();
    } else if (type == "word") {
        doc = new WordDocument();
    } else if (type == "html") {
        doc = new HTMLDocument();
    }
    doc->open();
    doc->process();
    // Adding a new type requires modifying this function
}
```

Every new document type means changing existing code

---

## Factory Method Structure

![factory_method_structure](/svg/courses/languages/c++/c++-design-patterns/03_factory_method/factory_method_structure.svg)

---

## Basic Factory Method

```cpp
class Transport {
public:
    virtual void deliver() = 0;
    virtual ~Transport() = default;
};

class Truck : public Transport {
public:
    void deliver() override {
        std::cout << "Delivering by land in a truck\n";
    }
};

class Ship : public Transport {
public:
    void deliver() override {
        std::cout << "Delivering by sea in a ship\n";
    }
};
```

---

## Factory Method Creator

```cpp
class Logistics {
public:
    virtual ~Logistics() = default;

    // Factory method
    virtual std::unique_ptr<Transport> createTransport() = 0;

    // Business logic that uses the factory method
    void planDelivery() {
        auto transport = createTransport();
        transport->deliver();
    }
};

class RoadLogistics : public Logistics {
public:
    std::unique_ptr<Transport> createTransport() override {
        return std::make_unique<Truck>();
    }
};

class SeaLogistics : public Logistics {
public:
    std::unique_ptr<Transport> createTransport() override {
        return std::make_unique<Ship>();
    }
};
```

---

## Parameterized Factory Method

```cpp
class ShapeFactory {
public:
    enum class ShapeType { Circle, Rectangle, Triangle };

    static std::unique_ptr<Shape> create(ShapeType type) {
        switch (type) {
            case ShapeType::Circle:
                return std::make_unique<Circle>();
            case ShapeType::Rectangle:
                return std::make_unique<Rectangle>();
            case ShapeType::Triangle:
                return std::make_unique<Triangle>();
        }
        throw std::invalid_argument("Unknown shape type");
    }
};

// Usage
auto shape = ShapeFactory::create(ShapeFactory::ShapeType::Circle);
shape->draw();
```

---

## Registry-Based Factory

```cpp
class WidgetFactory {
    using Creator = std::function<std::unique_ptr<Widget>()>;
    std::unordered_map<std::string, Creator> registry;

public:
    void registerWidget(const std::string& name, Creator creator) {
        registry[name] = std::move(creator);
    }

    std::unique_ptr<Widget> create(const std::string& name) {
        auto it = registry.find(name);
        if (it == registry.end()) {
            throw std::runtime_error("Unknown widget: " + name);
        }
        return it->second();
    }
};

// Usage
WidgetFactory factory;
factory.registerWidget("button", []{ return std::make_unique<Button>(); });
factory.registerWidget("slider", []{ return std::make_unique<Slider>(); });

auto widget = factory.create("button");
```

---

## Factory Method vs Direct Construction

| Aspect | Direct `new` | Factory Method |
|--------|-------------|----------------|
| Coupling | Tight | Loose |
| Adding types | Modify existing code | Add new creator class |
| Testing | Hard to mock | Easy to substitute |
| Flexibility | Fixed | Runtime selection |
| Complexity | Simple | More classes |

**Rule of thumb**: Use Factory Method when the exact type to create is determined by subclasses or configuration
