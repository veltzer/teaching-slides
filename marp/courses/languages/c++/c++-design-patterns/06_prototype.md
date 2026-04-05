# Prototype Pattern

---

## Intent

- Create new objects by cloning existing ones
- Avoid costly creation from scratch when similar objects are needed
- Allow runtime specification of object types to create

---

## Problem: Expensive Object Creation

```cpp
// Creating objects from scratch can be expensive
class GameLevel {
    std::vector<Mesh> meshes;           // Loaded from disk
    std::vector<Texture> textures;      // GPU resources
    PhysicsWorld physics;               // Complex simulation setup
    AINavMesh navigation;               // Pre-computed pathfinding

public:
    GameLevel() {
        // This takes seconds of loading
        loadMeshes();
        loadTextures();
        initPhysics();
        computeNavMesh();
    }
};
```

Cloning an existing configured object is much faster

---

## Prototype Structure

<svg width="550" height="230" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="20" width="200" height="60" fill="#e3f2fd" stroke="#1976d2" stroke-width="2"/>
  <text x="150" y="45" text-anchor="middle" font-size="13" font-weight="bold">Prototype</text>
  <text x="150" y="65" text-anchor="middle" font-size="11" font-style="italic">+ clone(): Prototype</text>

  <rect x="350" y="20" width="160" height="60" fill="#fff3e0" stroke="#f57c00" stroke-width="2"/>
  <text x="430" y="45" text-anchor="middle" font-size="13">Client</text>
  <text x="430" y="65" text-anchor="middle" font-size="11">+ operation()</text>

  <line x1="350" y1="50" x2="250" y2="50" stroke="#333" stroke-width="1.5" marker-end="url(#pArr)"/>
  <text x="300" y="42" text-anchor="middle" font-size="9">uses</text>

  <rect x="30" y="140" width="160" height="50" fill="#e8f5e8" stroke="#388e3c" stroke-width="2"/>
  <text x="110" y="160" text-anchor="middle" font-size="11">ConcretePrototype1</text>
  <text x="110" y="178" text-anchor="middle" font-size="10">+ clone()</text>

  <rect x="220" y="140" width="160" height="50" fill="#e8f5e8" stroke="#388e3c" stroke-width="2"/>
  <text x="300" y="160" text-anchor="middle" font-size="11">ConcretePrototype2</text>
  <text x="300" y="178" text-anchor="middle" font-size="10">+ clone()</text>

  <line x1="110" y1="140" x2="130" y2="80" stroke="#333" stroke-width="1.5" stroke-dasharray="5,5"/>
  <line x1="300" y1="140" x2="170" y2="80" stroke="#333" stroke-width="1.5" stroke-dasharray="5,5"/>

  <defs>
    <marker id="pArr" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Prototype Interface

```cpp
class Shape {
public:
    virtual ~Shape() = default;
    virtual std::unique_ptr<Shape> clone() const = 0;
    virtual void draw() const = 0;
    virtual std::string getInfo() const = 0;
};
```

---

## Concrete Prototypes

```cpp
class Circle : public Shape {
    double radius;
    std::string color;

public:
    Circle(double r, const std::string& c) : radius(r), color(c) {}

    std::unique_ptr<Shape> clone() const override {
        return std::make_unique<Circle>(*this);
    }

    void draw() const override {
        std::cout << "Drawing " << color << " circle, r=" << radius << "\n";
    }

    std::string getInfo() const override {
        return "Circle(r=" + std::to_string(radius) + ", " + color + ")";
    }
};

class Rectangle : public Shape {
    double width, height;
    std::string color;

public:
    Rectangle(double w, double h, const std::string& c)
        : width(w), height(h), color(c) {}

    std::unique_ptr<Shape> clone() const override {
        return std::make_unique<Rectangle>(*this);
    }

    void draw() const override {
        std::cout << "Drawing " << color << " rectangle "
                  << width << "x" << height << "\n";
    }

    std::string getInfo() const override {
        return "Rectangle(" + std::to_string(width) + "x"
               + std::to_string(height) + ", " + color + ")";
    }
};
```

---

## Prototype Registry

```cpp
class ShapeRegistry {
    std::unordered_map<std::string, std::unique_ptr<Shape>> prototypes;

public:
    void registerPrototype(const std::string& name,
                           std::unique_ptr<Shape> prototype) {
        prototypes[name] = std::move(prototype);
    }

    std::unique_ptr<Shape> create(const std::string& name) const {
        auto it = prototypes.find(name);
        if (it == prototypes.end()) {
            throw std::runtime_error("Unknown prototype: " + name);
        }
        return it->second->clone();
    }
};

// Usage
ShapeRegistry registry;
registry.registerPrototype("red-circle",
    std::make_unique<Circle>(5.0, "red"));
registry.registerPrototype("blue-rect",
    std::make_unique<Rectangle>(10.0, 20.0, "blue"));

auto shape1 = registry.create("red-circle");
auto shape2 = registry.create("red-circle");  // Independent clone
```

---

## Deep vs Shallow Copy

```cpp
class Document : public Cloneable {
    std::string title;
    std::shared_ptr<Style> style;          // Shared — shallow copy OK
    std::vector<std::unique_ptr<Page>> pages; // Owned — needs deep copy

public:
    std::unique_ptr<Document> clone() const {
        auto copy = std::make_unique<Document>();
        copy->title = title;
        copy->style = style;               // Shallow: shares style
        for (const auto& page : pages) {
            copy->pages.push_back(page->clone()); // Deep: clones pages
        }
        return copy;
    }
};
```

Choose shallow vs deep copy based on ownership semantics

---

## When to Use Prototype

**Use when:**

- Object creation is expensive (database, network, complex computation)
- System should be independent of how products are created
- Objects differ only in a few attributes (clone and modify)
- Runtime specification of object types is needed

**Avoid when:**

- Objects are simple and cheap to create
- Objects have circular references (complex to clone correctly)
- The clone semantics are unclear (shallow vs deep copy ambiguity)
