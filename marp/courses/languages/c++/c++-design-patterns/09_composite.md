# Composite Pattern

---

## Intent

- Compose objects into tree structures to represent part-whole hierarchies
- Let clients treat individual objects and compositions uniformly
- Simplify code that deals with complex tree structures

---

## Problem: Treating Groups and Individuals Differently

```cpp
// Without Composite — client must know the difference
void calculatePrice(const Box& box) {
    double total = 0;
    for (auto& product : box.products) {
        total += product.price;
    }
    for (auto& innerBox : box.boxes) {
        total += calculatePrice(innerBox);  // Recursive, different logic
    }
    total += box.wrappingCost;
    return total;
}
```

Client code must handle leaves and composites differently

---

## Composite Structure

<svg width="500" height="280" xmlns="http://www.w3.org/2000/svg">
  <rect x="175" y="10" width="150" height="60" fill="#e3f2fd" stroke="#1976d2" stroke-width="2"/>
  <text x="250" y="35" text-anchor="middle" font-size="13" font-weight="bold">Component</text>
  <text x="250" y="55" text-anchor="middle" font-size="11" font-style="italic">+ operation()</text>

  <rect x="50" y="150" width="130" height="50" fill="#e8f5e8" stroke="#388e3c" stroke-width="2"/>
  <text x="115" y="180" text-anchor="middle" font-size="12">Leaf</text>

  <rect x="310" y="150" width="150" height="50" fill="#fff3e0" stroke="#f57c00" stroke-width="2"/>
  <text x="385" y="170" text-anchor="middle" font-size="12">Composite</text>
  <text x="385" y="188" text-anchor="middle" font-size="10">children: Component[]</text>

  <line x1="115" y1="150" x2="220" y2="70" stroke="#333" stroke-width="1.5" stroke-dasharray="5,5"/>
  <line x1="385" y1="150" x2="280" y2="70" stroke="#333" stroke-width="1.5" stroke-dasharray="5,5"/>

  <path d="M 385 200 C 385 250, 450 250, 450 70" stroke="#333" stroke-width="1.5" fill="none" marker-end="url(#arrow)"/>
  <text x="440" y="230" font-size="10">has children</text>

  <defs>
    <marker id="arrow" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Component Interface

```cpp
class FileSystemItem {
public:
    virtual ~FileSystemItem() = default;
    virtual std::string getName() const = 0;
    virtual size_t getSize() const = 0;
    virtual void print(int indent = 0) const = 0;
};
```

---

## Leaf

```cpp
class File : public FileSystemItem {
    std::string name;
    size_t size;

public:
    File(std::string name, size_t size)
        : name(std::move(name)), size(size) {}

    std::string getName() const override { return name; }
    size_t getSize() const override { return size; }

    void print(int indent = 0) const override {
        std::cout << std::string(indent, ' ') << name
                  << " (" << size << " bytes)\n";
    }
};
```

---

## Composite

```cpp
class Directory : public FileSystemItem {
    std::string name;
    std::vector<std::unique_ptr<FileSystemItem>> children;

public:
    explicit Directory(std::string name) : name(std::move(name)) {}

    std::string getName() const override { return name; }

    size_t getSize() const override {
        size_t total = 0;
        for (const auto& child : children) {
            total += child->getSize();
        }
        return total;
    }

    void add(std::unique_ptr<FileSystemItem> item) {
        children.push_back(std::move(item));
    }

    void print(int indent = 0) const override {
        std::cout << std::string(indent, ' ') << "[" << name << "]\n";
        for (const auto& child : children) {
            child->print(indent + 2);
        }
    }
};
```

---

## Composite Usage

```cpp
auto root = std::make_unique<Directory>("root");

auto src = std::make_unique<Directory>("src");
src->add(std::make_unique<File>("main.cpp", 1500));
src->add(std::make_unique<File>("utils.cpp", 800));

auto include = std::make_unique<Directory>("include");
include->add(std::make_unique<File>("utils.h", 200));

root->add(std::move(src));
root->add(std::move(include));
root->add(std::make_unique<File>("Makefile", 300));

root->print();
// [root]
//   [src]
//     main.cpp (1500 bytes)
//     utils.cpp (800 bytes)
//   [include]
//     utils.h (200 bytes)
//   Makefile (300 bytes)

std::cout << "Total: " << root->getSize() << " bytes\n";
// Total: 2800 bytes
```

Client code treats files and directories uniformly

---

## When to Use Composite

**Use when:**

- You need to represent part-whole hierarchies (trees)
- Clients should treat individual objects and compositions uniformly
- You want to apply operations recursively over a structure

**Common examples:**

- File systems (files and directories)
- GUI widgets (buttons and panels containing buttons)
- Organization charts (employees and departments)
- Arithmetic expressions (operands and operators)
