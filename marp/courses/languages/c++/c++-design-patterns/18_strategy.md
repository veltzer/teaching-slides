# Strategy Pattern

---

## Intent

- Define a family of algorithms, encapsulate each one, and make them interchangeable
- Let the algorithm vary independently from clients that use it
- Eliminate conditional statements for selecting desired behavior

---

## Problem: Conditional Algorithm Selection

```cpp
class Sorter {
public:
    void sort(std::vector<int>& data, const std::string& algorithm) {
        if (algorithm == "bubble") {
            // 50 lines of bubble sort
        } else if (algorithm == "merge") {
            // 80 lines of merge sort
        } else if (algorithm == "quick") {
            // 60 lines of quick sort
        }
        // Adding a new algorithm means modifying this class
    }
};
```

---

## Strategy Structure

<svg width="550" height="230" xmlns="http://www.w3.org/2000/svg">
  <rect x="30" y="20" width="180" height="70" fill="#fff3e0" stroke="#f57c00" stroke-width="2"/>
  <text x="120" y="45" text-anchor="middle" font-size="13" font-weight="bold">Context</text>
  <text x="120" y="63" text-anchor="middle" font-size="10">strategy: Strategy*</text>
  <text x="120" y="78" text-anchor="middle" font-size="10">+ execute()</text>

  <rect x="300" y="20" width="200" height="60" fill="#e3f2fd" stroke="#1976d2" stroke-width="2"/>
  <text x="400" y="45" text-anchor="middle" font-size="13" font-weight="bold">Strategy</text>
  <text x="400" y="65" text-anchor="middle" font-size="11" font-style="italic">+ algorithm()</text>

  <line x1="210" y1="55" x2="300" y2="50" stroke="#333" stroke-width="1.5" marker-end="url(#stArr)"/>

  <rect x="250" y="150" width="140" height="40" fill="#e8f5e8" stroke="#388e3c" stroke-width="2"/>
  <text x="320" y="175" text-anchor="middle" font-size="11">ConcreteStrategyA</text>

  <rect x="410" y="150" width="140" height="40" fill="#e8f5e8" stroke="#388e3c" stroke-width="2"/>
  <text x="480" y="175" text-anchor="middle" font-size="11">ConcreteStrategyB</text>

  <line x1="320" y1="150" x2="370" y2="80" stroke="#333" stroke-width="1.5" stroke-dasharray="5,5"/>
  <line x1="480" y1="150" x2="430" y2="80" stroke="#333" stroke-width="1.5" stroke-dasharray="5,5"/>

  <defs>
    <marker id="stArr" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Strategy Interface

```cpp
class SortStrategy {
public:
    virtual void sort(std::vector<int>& data) = 0;
    virtual ~SortStrategy() = default;
};

class BubbleSort : public SortStrategy {
public:
    void sort(std::vector<int>& data) override {
        for (size_t i = 0; i < data.size(); ++i)
            for (size_t j = 0; j < data.size() - i - 1; ++j)
                if (data[j] > data[j + 1])
                    std::swap(data[j], data[j + 1]);
    }
};

class QuickSort : public SortStrategy {
public:
    void sort(std::vector<int>& data) override {
        std::sort(data.begin(), data.end());
    }
};

class MergeSort : public SortStrategy {
public:
    void sort(std::vector<int>& data) override {
        std::stable_sort(data.begin(), data.end());
    }
};
```

---

## Context Class

```cpp
class DataProcessor {
    std::unique_ptr<SortStrategy> strategy;

public:
    explicit DataProcessor(std::unique_ptr<SortStrategy> s)
        : strategy(std::move(s)) {}

    void setStrategy(std::unique_ptr<SortStrategy> s) {
        strategy = std::move(s);
    }

    void processData(std::vector<int>& data) {
        std::cout << "Processing " << data.size() << " elements\n";
        strategy->sort(data);
    }
};

// Usage
DataProcessor processor(std::make_unique<QuickSort>());
processor.processData(data);

// Switch strategy at runtime
processor.setStrategy(std::make_unique<MergeSort>());
processor.processData(data);
```

---

## Strategy with std::function

```cpp
class TextFormatter {
    std::function<std::string(const std::string&)> formatStrategy;

public:
    explicit TextFormatter(
        std::function<std::string(const std::string&)> strategy)
        : formatStrategy(std::move(strategy)) {}

    std::string format(const std::string& text) {
        return formatStrategy(text);
    }
};

// Using lambdas as strategies
TextFormatter upper([](const std::string& s) {
    std::string result = s;
    std::transform(result.begin(), result.end(), result.begin(), ::toupper);
    return result;
});

TextFormatter prefix([](const std::string& s) {
    return ">>> " + s;
});

std::cout << upper.format("hello");   // "HELLO"
std::cout << prefix.format("hello");  // ">>> hello"
```

---

## Real-World Example: Compression

```cpp
class CompressionStrategy {
public:
    virtual std::vector<uint8_t> compress(
        const std::vector<uint8_t>& data) = 0;
    virtual std::vector<uint8_t> decompress(
        const std::vector<uint8_t>& data) = 0;
    virtual ~CompressionStrategy() = default;
};

class ZipCompression : public CompressionStrategy {
public:
    std::vector<uint8_t> compress(
        const std::vector<uint8_t>& data) override { /* zip */ }
    std::vector<uint8_t> decompress(
        const std::vector<uint8_t>& data) override { /* unzip */ }
};

class GzipCompression : public CompressionStrategy {
public:
    std::vector<uint8_t> compress(
        const std::vector<uint8_t>& data) override { /* gzip */ }
    std::vector<uint8_t> decompress(
        const std::vector<uint8_t>& data) override { /* gunzip */ }
};

class FileArchiver {
    std::unique_ptr<CompressionStrategy> strategy;
public:
    explicit FileArchiver(std::unique_ptr<CompressionStrategy> s)
        : strategy(std::move(s)) {}

    void archive(const std::string& filename) {
        auto data = readFile(filename);
        auto compressed = strategy->compress(data);
        writeFile(filename + ".compressed", compressed);
    }
};
```

---

## Strategy vs Template Method

| Aspect | Strategy | Template Method |
|--------|----------|----------------|
| Mechanism | Composition | Inheritance |
| Varies | Entire algorithm | Steps in an algorithm |
| Selection | Runtime | Compile time |
| Coupling | Loose | Tighter |
| Granularity | Whole behavior | Individual steps |

---

## When to Use Strategy

**Use when:**

- Many related classes differ only in their behavior
- You need different variants of an algorithm
- An algorithm uses data that clients should not know about
- A class defines many behaviors via conditionals

**In modern C++**: `std::function` and lambdas often provide a lighter-weight alternative to the full class-based Strategy pattern
