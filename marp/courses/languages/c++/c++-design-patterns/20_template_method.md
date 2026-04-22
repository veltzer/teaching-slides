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
# Template Method Pattern

---

## Intent

- Define the skeleton of an algorithm in a base class
- Let subclasses override specific steps without changing the algorithm's structure
- Promote code reuse by factoring common behavior into the base class

---

## Problem: Duplicated Algorithm Structure

```cpp
// Both classes have the same overall structure but different details
class CSVDataMiner {
public:
    void mine(const std::string& path) {
        auto file = openCSV(path);      // Different
        auto raw = extractCSV(file);    // Different
        auto data = parseData(raw);     // Same
        auto report = analyze(data);    // Same
        sendReport(report);             // Same
    }
};

class PDFDataMiner {
public:
    void mine(const std::string& path) {
        auto file = openPDF(path);      // Different
        auto raw = extractPDF(file);    // Different
        auto data = parseData(raw);     // Same
        auto report = analyze(data);    // Same
        sendReport(report);             // Same
    }
};
```

---

## Template Method Structure

![template_method_structure](svg/courses/languages/c++/c++-design-patterns/20_template_method/template_method_structure.svg)

---

## Template Method Solution

```cpp
class DataMiner {
public:
    // Template method — defines the algorithm skeleton
    void mine(const std::string& path) {
        auto file = openFile(path);
        auto raw = extractData(file);
        auto data = parseData(raw);
        auto report = analyze(data);
        sendReport(report);
    }

    virtual ~DataMiner() = default;

protected:
    // Steps that subclasses must implement
    virtual std::string openFile(const std::string& path) = 0;
    virtual std::string extractData(const std::string& file) = 0;

    // Steps with default implementations (hooks)
    virtual std::vector<Record> parseData(const std::string& raw) {
        // Default parsing logic
        return defaultParser(raw);
    }

    virtual Report analyze(const std::vector<Record>& data) {
        return Report(data);
    }

    virtual void sendReport(const Report& report) {
        std::cout << "Report: " << report.summary() << "\n";
    }
};
```

---

## Concrete Implementations

```cpp
class CSVDataMiner : public DataMiner {
protected:
    std::string openFile(const std::string& path) override {
        std::cout << "Opening CSV file: " << path << "\n";
        // Read CSV file
        return readFileContents(path);
    }

    std::string extractData(const std::string& file) override {
        std::cout << "Extracting CSV data\n";
        // Parse CSV format
        return parseCSV(file);
    }
};

class PDFDataMiner : public DataMiner {
protected:
    std::string openFile(const std::string& path) override {
        std::cout << "Opening PDF file: " << path << "\n";
        return readPDFContents(path);
    }

    std::string extractData(const std::string& file) override {
        std::cout << "Extracting text from PDF\n";
        return extractTextFromPDF(file);
    }
};
```

---

## Hooks

```cpp
class GameAI {
public:
    // Template method
    void takeTurn() {
        collectResources();
        buildStructures();
        buildUnits();
        attack();
    }

    virtual ~GameAI() = default;

protected:
    virtual void collectResources() {
        // Default: collect from built structures
    }

    // Pure virtual — must be overridden
    virtual void buildStructures() = 0;
    virtual void buildUnits() = 0;

    virtual void attack() {
        // Default: send all units to nearest enemy
    }
};
```

---

## Hooks: Concrete AI Subclasses

```cpp
class AggressiveAI : public GameAI {
protected:
    void buildStructures() override { /* build barracks */ }
    void buildUnits() override { /* build attack units */ }
    void attack() override { /* send all units to weakest enemy */ }
};

class DefensiveAI : public GameAI {
protected:
    void buildStructures() override { /* build walls and towers */ }
    void buildUnits() override { /* build defensive units */ }
    // Uses default attack behavior
};
```

---

## Template Method with NVI (Non-Virtual Interface)

```cpp
class Validator {
public:
    // Public non-virtual interface
    bool validate(const std::string& input) {
        if (input.empty()) return false;
        return doValidate(sanitize(input));
    }

private:
    // Private virtual functions — implementation details
    virtual std::string sanitize(const std::string& input) {
        return input;  // Default: no sanitization
    }
    virtual bool doValidate(const std::string& input) = 0;
};

class EmailValidator : public Validator {
private:
    bool doValidate(const std::string& input) override {
        return input.find('@') != std::string::npos;
    }
};
```

NVI idiom ensures the invariant code (empty check) always runs

---

## When to Use Template Method

**Use when:**

- Subclasses should extend only particular steps of an algorithm
- You have several classes with nearly identical algorithms
- You want to control which parts of an algorithm subclasses can override

**Template Method vs Strategy:**

- **Template Method** uses inheritance: override steps
- **Strategy** uses composition: swap entire algorithms
