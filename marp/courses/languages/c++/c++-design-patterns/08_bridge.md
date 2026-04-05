# Bridge Pattern

---

## Intent

- Decouple an abstraction from its implementation so the two can vary independently
- Avoid a proliferation of classes when combining multiple dimensions of variation
- Use composition instead of inheritance to combine implementations

---

## Problem: Class Explosion

```cpp
// Without Bridge: 2 shapes x 3 renderers = 6 classes
class CircleOpenGL { ... };
class CircleVulkan { ... };
class CircleDirectX { ... };
class RectangleOpenGL { ... };
class RectangleVulkan { ... };
class RectangleDirectX { ... };
// Adding a new shape or renderer multiplies the number of classes
```

Every new shape or renderer doubles the number of classes

---

## Bridge Structure

<svg width="600" height="280" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="30" width="180" height="70" fill="#e3f2fd" stroke="#1976d2" stroke-width="2"/>
  <text x="140" y="55" text-anchor="middle" font-size="13" font-weight="bold">Abstraction</text>
  <text x="140" y="75" text-anchor="middle" font-size="11">impl: Implementor*</text>

  <rect x="370" y="30" width="180" height="70" fill="#e8f5e8" stroke="#388e3c" stroke-width="2"/>
  <text x="460" y="55" text-anchor="middle" font-size="13" font-weight="bold">Implementor</text>
  <text x="460" y="75" text-anchor="middle" font-size="11" font-style="italic">+ operationImpl()</text>

  <line x1="230" y1="65" x2="370" y2="65" stroke="#333" stroke-width="2"/>
  <polygon points="360,60 370,65 360,70" fill="#333"/>

  <rect x="20" y="170" width="140" height="50" fill="#e1f5fe" stroke="#0277bd" stroke-width="2"/>
  <text x="90" y="200" text-anchor="middle" font-size="11">RefinedAbstraction</text>

  <rect x="180" y="170" width="140" height="50" fill="#e1f5fe" stroke="#0277bd" stroke-width="2"/>
  <text x="250" y="200" text-anchor="middle" font-size="11">RefinedAbstraction2</text>

  <rect x="370" y="170" width="140" height="50" fill="#f1f8e9" stroke="#689f38" stroke-width="2"/>
  <text x="440" y="200" text-anchor="middle" font-size="11">ConcreteImplA</text>

  <rect x="530" y="170" width="140" height="50" fill="#f1f8e9" stroke="#689f38" stroke-width="2"/>
  <text x="600" y="200" text-anchor="middle" font-size="11">ConcreteImplB</text>

  <line x1="90" y1="170" x2="120" y2="100" stroke="#333" stroke-width="1.5" stroke-dasharray="5,5"/>
  <line x1="250" y1="170" x2="170" y2="100" stroke="#333" stroke-width="1.5" stroke-dasharray="5,5"/>
  <line x1="440" y1="170" x2="460" y2="100" stroke="#333" stroke-width="1.5" stroke-dasharray="5,5"/>
  <line x1="600" y1="170" x2="480" y2="100" stroke="#333" stroke-width="1.5" stroke-dasharray="5,5"/>
</svg>

The Abstraction delegates to the Implementor — both can vary independently

---

## Implementation Interface

```cpp
class Renderer {
public:
    virtual void renderCircle(float x, float y, float radius) = 0;
    virtual void renderRectangle(float x, float y, float w, float h) = 0;
    virtual ~Renderer() = default;
};

class OpenGLRenderer : public Renderer {
public:
    void renderCircle(float x, float y, float radius) override {
        std::cout << "OpenGL: circle at (" << x << "," << y
                  << ") r=" << radius << "\n";
    }
    void renderRectangle(float x, float y, float w, float h) override {
        std::cout << "OpenGL: rect at (" << x << "," << y
                  << ") " << w << "x" << h << "\n";
    }
};

class VulkanRenderer : public Renderer {
public:
    void renderCircle(float x, float y, float radius) override {
        std::cout << "Vulkan: circle at (" << x << "," << y
                  << ") r=" << radius << "\n";
    }
    void renderRectangle(float x, float y, float w, float h) override {
        std::cout << "Vulkan: rect at (" << x << "," << y
                  << ") " << w << "x" << h << "\n";
    }
};
```

---

## Abstraction

```cpp
class Shape {
protected:
    Renderer& renderer;

public:
    explicit Shape(Renderer& r) : renderer(r) {}
    virtual void draw() = 0;
    virtual void resize(float factor) = 0;
    virtual ~Shape() = default;
};

class Circle : public Shape {
    float x, y, radius;
public:
    Circle(Renderer& r, float x, float y, float radius)
        : Shape(r), x(x), y(y), radius(radius) {}

    void draw() override { renderer.renderCircle(x, y, radius); }
    void resize(float factor) override { radius *= factor; }
};

class Rectangle : public Shape {
    float x, y, width, height;
public:
    Rectangle(Renderer& r, float x, float y, float w, float h)
        : Shape(r), x(x), y(y), width(w), height(h) {}

    void draw() override { renderer.renderRectangle(x, y, width, height); }
    void resize(float factor) override { width *= factor; height *= factor; }
};
```

---

## Bridge Usage

```cpp
OpenGLRenderer opengl;
VulkanRenderer vulkan;

// Same shapes, different renderers
Circle c1(opengl, 10, 20, 5);
Circle c2(vulkan, 10, 20, 5);

c1.draw();  // OpenGL: circle at (10,20) r=5
c2.draw();  // Vulkan: circle at (10,20) r=5

// Adding a new shape or renderer is independent
// No class explosion
```

---

## When to Use Bridge

**Use when:**

- You want to avoid a permanent binding between abstraction and implementation
- Both abstraction and implementation should be extensible independently
- You have a class explosion from combining multiple dimensions
- You want to switch implementations at runtime

**Bridge vs Adapter:**

- **Adapter** makes two existing interfaces work together (after design)
- **Bridge** separates interface from implementation (during design)
