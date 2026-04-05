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

<svg width="600" height="300" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="30" width="180" height="80" fill="#e3f2fd" stroke="#1976d2" stroke-width="2"/>
  <text x="140" y="55" text-anchor="middle" font-size="13" font-weight="bold">Creator</text>
  <text x="140" y="75" text-anchor="middle" font-size="11" font-style="italic">+ factoryMethod()</text>
  <text x="140" y="92" text-anchor="middle" font-size="11">+ operation()</text>

  <rect x="350" y="30" width="180" height="80" fill="#e8f5e8" stroke="#388e3c" stroke-width="2"/>
  <text x="440" y="55" text-anchor="middle" font-size="13" font-weight="bold">Product</text>
  <text x="440" y="75" text-anchor="middle" font-size="11" font-style="italic">+ doStuff()</text>

  <rect x="50" y="190" width="180" height="60" fill="#e1f5fe" stroke="#0277bd" stroke-width="2"/>
  <text x="140" y="215" text-anchor="middle" font-size="13">ConcreteCreator</text>
  <text x="140" y="235" text-anchor="middle" font-size="11">+ factoryMethod()</text>

  <rect x="350" y="190" width="180" height="60" fill="#f1f8e9" stroke="#689f38" stroke-width="2"/>
  <text x="440" y="215" text-anchor="middle" font-size="13">ConcreteProduct</text>
  <text x="440" y="235" text-anchor="middle" font-size="11">+ doStuff()</text>

  <line x1="140" y1="110" x2="140" y2="190" stroke="#333" stroke-width="1.5" stroke-dasharray="5,5"/>
  <polygon points="130,190 140,180 150,190" fill="white" stroke="#333" stroke-width="1.5"/>

  <line x1="440" y1="110" x2="440" y2="190" stroke="#333" stroke-width="1.5" stroke-dasharray="5,5"/>
  <polygon points="430,190 440,180 450,190" fill="white" stroke="#333" stroke-width="1.5"/>

  <line x1="230" y1="70" x2="350" y2="70" stroke="#333" stroke-width="1.5" stroke-dasharray="3,3"/>
  <text x="290" y="62" text-anchor="middle" font-size="10">creates</text>
</svg>

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
