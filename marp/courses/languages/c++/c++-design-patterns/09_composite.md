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

![composite_structure](/svg/courses/languages/c++/c++-design-patterns/09_composite/composite_structure.svg)

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
