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

<svg width="550" height="250" xmlns="http://www.w3.org/2000/svg">
  <rect x="30" y="20" width="150" height="60" fill="#fff3e0" stroke="#f57c00" stroke-width="2"/>
  <text x="105" y="45" text-anchor="middle" font-size="13" font-weight="bold">Client</text>
  <text x="105" y="65" text-anchor="middle" font-size="10">extrinsic state</text>

  <rect x="230" y="20" width="160" height="60" fill="#e3f2fd" stroke="#1976d2" stroke-width="2"/>
  <text x="310" y="45" text-anchor="middle" font-size="13" font-weight="bold">FlyweightFactory</text>
  <text x="310" y="65" text-anchor="middle" font-size="10">+ getFlyweight(key)</text>

  <rect x="230" y="130" width="160" height="60" fill="#e8f5e8" stroke="#388e3c" stroke-width="2"/>
  <text x="310" y="155" text-anchor="middle" font-size="13" font-weight="bold">Flyweight</text>
  <text x="310" y="175" text-anchor="middle" font-size="10">intrinsic state (shared)</text>

  <rect x="460" y="130" width="80" height="30" fill="#f1f8e9" stroke="#689f38" stroke-width="1.5"/>
  <text x="500" y="150" text-anchor="middle" font-size="9">Flyweight A</text>
  <rect x="460" y="165" width="80" height="30" fill="#f1f8e9" stroke="#689f38" stroke-width="1.5"/>
  <text x="500" y="185" text-anchor="middle" font-size="9">Flyweight B</text>

  <line x1="180" y1="50" x2="230" y2="50" stroke="#333" stroke-width="1.5" marker-end="url(#fwArr)"/>
  <line x1="310" y1="80" x2="310" y2="130" stroke="#333" stroke-width="1.5" marker-end="url(#fwArr)"/>
  <line x1="390" y1="150" x2="460" y2="145" stroke="#333" stroke-width="1" stroke-dasharray="3,3"/>
  <line x1="390" y1="170" x2="460" y2="175" stroke="#333" stroke-width="1" stroke-dasharray="3,3"/>

  <defs>
    <marker id="fwArr" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#333"/>
    </marker>
  </defs>
</svg>

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
