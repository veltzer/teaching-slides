---
tags:
  - languages:cpp
  - concepts:design-patterns
  - concepts:oop
  - practices:software-design
level: advanced
category: language
audience:
  - audiences:developers

---
# Flyweight Pattern

---

## Intent

- Use sharing to support large numbers of fine-grained objects efficiently
- Separate intrinsic (shared) state from extrinsic (context-specific) state
- Reduce memory usage when many objects share common data

---

## Problem: Memory Explosion

```cpp
// A game with millions of tree objects
class Tree {
    int x, y;                    // Position — unique per tree
    std::string type;            // "Oak", "Pine" — shared by many
    Texture texture;             // 10 MB per texture — shared by many
    Mesh mesh;                   // 5 MB per mesh — shared by many
    Color color;                 // Shared by type
};
// 1,000,000 trees x 15 MB each = 15 TB of memory!
```

---

## Flyweight Structure

![flyweight_structure](svg/courses/languages/c++/c++-design-patterns/12_flyweight/flyweight_structure.svg)

---

## Flyweight Solution

```cpp
// Intrinsic state — shared across many objects
class TreeType {
    std::string name;
    Texture texture;
    Mesh mesh;
    Color color;

public:
    TreeType(std::string name, Texture tex, Mesh m, Color c)
        : name(std::move(name)), texture(std::move(tex)),
          mesh(std::move(m)), color(std::move(c)) {}

    void draw(int x, int y) const {
        // Use shared data with position-specific coordinates
        std::cout << "Drawing " << name << " at (" << x << "," << y << ")\n";
    }
};
```

---

## Flyweight Factory

```cpp
class TreeTypeFactory {
    std::unordered_map<std::string, std::shared_ptr<TreeType>> types;

public:
    std::shared_ptr<TreeType> getTreeType(
            const std::string& name,
            const Texture& texture,
            const Mesh& mesh,
            const Color& color) {
        auto it = types.find(name);
        if (it == types.end()) {
            auto type = std::make_shared<TreeType>(
                name, texture, mesh, color);
            types[name] = type;
            return type;
        }
        return it->second;
    }

    size_t getTypeCount() const { return types.size(); }
};
```

---

## Using the Flyweight

```cpp
// Extrinsic state — unique per object
class Tree {
    int x, y;
    std::shared_ptr<TreeType> type;  // Shared flyweight

public:
    Tree(int x, int y, std::shared_ptr<TreeType> type)
        : x(x), y(y), type(std::move(type)) {}

    void draw() const {
        type->draw(x, y);
    }
};

class Forest {
    std::vector<Tree> trees;
    TreeTypeFactory factory;

public:
    void plantTree(int x, int y, const std::string& name,
                   const Texture& tex, const Mesh& mesh, const Color& col) {
        auto type = factory.getTreeType(name, tex, mesh, col);
        trees.emplace_back(x, y, std::move(type));
    }
};

// 1,000,000 trees but only ~10 TreeType objects in memory
```

---

## Memory Savings

| Approach | Per Tree | 1M Trees |
|----------|---------|----------|
| Without Flyweight | ~15 MB | ~15 TB |
| With Flyweight | ~16 bytes (x, y + pointer) | ~16 MB |
| Shared TreeTypes | ~15 MB each | ~150 MB (for 10 types) |
| **Total with Flyweight** | | **~166 MB** |

Over 99% memory reduction

---

## When to Use Flyweight

**Use when:**

- An application uses a large number of objects
- Storage costs are high due to the sheer quantity of objects
- Most object state can be made extrinsic (passed in from outside)
- Many groups of objects can be replaced by a few shared objects

**Key distinction:**

- **Intrinsic state**: Stored in the flyweight, shared, immutable
- **Extrinsic state**: Stored by the client, passed to flyweight methods

**Trade-off**: Saves memory but adds complexity and CPU cost for separating/recombining state
