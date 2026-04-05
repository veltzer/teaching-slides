# Iterator Pattern

---

## Intent

- Provide a way to access elements of a collection sequentially without exposing its internal structure
- Support multiple traversals of the same collection
- Provide a uniform interface for traversing different data structures

---

## Iterator Structure

<svg width="550" height="220" xmlns="http://www.w3.org/2000/svg">
  <rect x="30" y="20" width="180" height="70" fill="#e3f2fd" stroke="#1976d2" stroke-width="2"/>
  <text x="120" y="45" text-anchor="middle" font-size="13" font-weight="bold">Collection</text>
  <text x="120" y="65" text-anchor="middle" font-size="11">+ begin(): Iterator</text>
  <text x="120" y="80" text-anchor="middle" font-size="11">+ end(): Iterator</text>

  <rect x="310" y="20" width="200" height="70" fill="#e8f5e8" stroke="#388e3c" stroke-width="2"/>
  <text x="410" y="45" text-anchor="middle" font-size="13" font-weight="bold">Iterator</text>
  <text x="410" y="65" text-anchor="middle" font-size="11">+ operator*(): T&amp;</text>
  <text x="410" y="80" text-anchor="middle" font-size="11">+ operator++(): Iterator&amp;</text>

  <line x1="210" y1="55" x2="310" y2="55" stroke="#333" stroke-width="1.5" marker-end="url(#itArr)"/>
  <text x="260" y="47" text-anchor="middle" font-size="9">creates</text>

  <rect x="100" y="150" width="160" height="40" fill="#e1f5fe" stroke="#0277bd" stroke-width="2"/>
  <text x="180" y="175" text-anchor="middle" font-size="11">ConcreteCollection</text>

  <rect x="360" y="150" width="160" height="40" fill="#f1f8e9" stroke="#689f38" stroke-width="2"/>
  <text x="440" y="175" text-anchor="middle" font-size="11">ConcreteIterator</text>

  <line x1="180" y1="150" x2="120" y2="90" stroke="#333" stroke-width="1.5" stroke-dasharray="5,5"/>
  <line x1="440" y1="150" x2="410" y2="90" stroke="#333" stroke-width="1.5" stroke-dasharray="5,5"/>

  <defs>
    <marker id="itArr" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## C++ Iterators Overview

C++ has built-in iterator support in the STL. The iterator pattern is deeply integrated into the language:

```cpp
std::vector<int> v = {1, 2, 3, 4, 5};

// Iterator-based traversal
for (auto it = v.begin(); it != v.end(); ++it) {
    std::cout << *it << " ";
}

// Range-based for (uses iterators internally)
for (int val : v) {
    std::cout << val << " ";
}
```

---

## Custom Iterator for a Collection

```cpp
template<typename T>
class DynamicArray {
    T* data;
    size_t sz;
    size_t capacity;

public:
    class Iterator {
        T* ptr;
    public:
        using iterator_category = std::random_access_iterator_tag;
        using value_type = T;
        using difference_type = std::ptrdiff_t;
        using pointer = T*;
        using reference = T&;

        explicit Iterator(T* p) : ptr(p) {}
        reference operator*() const { return *ptr; }
        pointer operator->() const { return ptr; }
        Iterator& operator++() { ++ptr; return *this; }
        Iterator operator++(int) { Iterator tmp = *this; ++ptr; return tmp; }
        bool operator==(const Iterator& other) const { return ptr == other.ptr; }
        bool operator!=(const Iterator& other) const { return ptr != other.ptr; }
    };

    Iterator begin() { return Iterator(data); }
    Iterator end() { return Iterator(data + sz); }
};
```

---

## Making a Class Range-Based For Compatible

```cpp
class NumberRange {
    int start, stop;

public:
    NumberRange(int start, int stop) : start(start), stop(stop) {}

    class Iterator {
        int current;
    public:
        explicit Iterator(int val) : current(val) {}
        int operator*() const { return current; }
        Iterator& operator++() { ++current; return *this; }
        bool operator!=(const Iterator& other) const {
            return current != other.current;
        }
    };

    Iterator begin() const { return Iterator(start); }
    Iterator end() const { return Iterator(stop); }
};

// Usage
for (int i : NumberRange(1, 10)) {
    std::cout << i << " ";  // 1 2 3 4 5 6 7 8 9
}
```

---

## Tree Iterator (Non-Trivial Traversal)

```cpp
template<typename T>
class BinaryTree {
    struct Node {
        T value;
        std::unique_ptr<Node> left, right;
    };
    std::unique_ptr<Node> root;

public:
    class InOrderIterator {
        std::stack<Node*> stack;

        void pushLeft(Node* node) {
            while (node) {
                stack.push(node);
                node = node->left.get();
            }
        }

    public:
        explicit InOrderIterator(Node* root) { pushLeft(root); }
        InOrderIterator() = default;  // End iterator

        T& operator*() { return stack.top()->value; }
        InOrderIterator& operator++() {
            Node* node = stack.top();
            stack.pop();
            pushLeft(node->right.get());
            return *this;
        }
        bool operator!=(const InOrderIterator& other) const {
            return stack.size() != other.stack.size();
        }
    };

    InOrderIterator begin() { return InOrderIterator(root.get()); }
    InOrderIterator end() { return InOrderIterator(); }
};
```

---

## STL Iterator Categories

| Category | Operations | Examples |
|----------|-----------|----------|
| Input | `++`, `*`, `==` | `istream_iterator` |
| Output | `++`, `*` | `ostream_iterator` |
| Forward | Input + multi-pass | `forward_list::iterator` |
| Bidirectional | Forward + `--` | `list::iterator`, `set::iterator` |
| Random Access | Bidirectional + `[]`, `+`, `-` | `vector::iterator`, `deque::iterator` |

Stronger categories support more algorithms

---

## Iterator Adaptors

```cpp
#include <iterator>

std::vector<int> src = {1, 2, 3, 4, 5};
std::vector<int> dst;

// Back insert iterator
std::copy(src.begin(), src.end(), std::back_inserter(dst));

// Reverse iterator
for (auto it = src.rbegin(); it != src.rend(); ++it) {
    std::cout << *it << " ";  // 5 4 3 2 1
}

// Stream iterators
std::copy(src.begin(), src.end(),
          std::ostream_iterator<int>(std::cout, ", "));
// Output: 1, 2, 3, 4, 5,
```

---

## When to Use Iterator

**Use when:**

- You need to traverse a collection without exposing its internal structure
- You want to support multiple simultaneous traversals
- You need a uniform interface for traversing different data structures

**In C++:**

- Prefer using STL iterators and range-based for loops
- Implement custom iterators to make your classes work with STL algorithms
- C++20 ranges provide even more powerful iteration abstractions
