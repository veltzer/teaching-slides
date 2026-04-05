# Decorator Pattern

---

## Intent

- Attach additional responsibilities to an object dynamically
- Provide a flexible alternative to subclassing for extending functionality
- Wrap objects to add behavior without modifying the original class

---

## Problem: Subclassing Explosion

```cpp
// Adding features via inheritance creates class explosion
class Coffee { ... };
class CoffeeWithMilk : public Coffee { ... };
class CoffeeWithSugar : public Coffee { ... };
class CoffeeWithMilkAndSugar : public Coffee { ... };
class CoffeeWithMilkAndSugarAndWhip : public Coffee { ... };
// Every combination needs its own class!
```

---

## Decorator Structure

<svg width="550" height="300" xmlns="http://www.w3.org/2000/svg">
  <rect x="175" y="10" width="180" height="60" fill="#e3f2fd" stroke="#1976d2" stroke-width="2"/>
  <text x="265" y="35" text-anchor="middle" font-size="13" font-weight="bold">Component</text>
  <text x="265" y="55" text-anchor="middle" font-size="11" font-style="italic">+ operation()</text>

  <rect x="50" y="120" width="150" height="50" fill="#e8f5e8" stroke="#388e3c" stroke-width="2"/>
  <text x="125" y="150" text-anchor="middle" font-size="12">ConcreteComponent</text>

  <rect x="280" y="120" width="200" height="50" fill="#fff3e0" stroke="#f57c00" stroke-width="2"/>
  <text x="380" y="140" text-anchor="middle" font-size="12">Decorator</text>
  <text x="380" y="158" text-anchor="middle" font-size="10">wrappee: Component</text>

  <rect x="250" y="230" width="130" height="40" fill="#fce4ec" stroke="#c2185b" stroke-width="2"/>
  <text x="315" y="255" text-anchor="middle" font-size="11">ConcreteDecA</text>

  <rect x="400" y="230" width="130" height="40" fill="#fce4ec" stroke="#c2185b" stroke-width="2"/>
  <text x="465" y="255" text-anchor="middle" font-size="11">ConcreteDecB</text>

  <line x1="125" y1="120" x2="225" y2="70" stroke="#333" stroke-width="1.5" stroke-dasharray="5,5"/>
  <line x1="380" y1="120" x2="305" y2="70" stroke="#333" stroke-width="1.5" stroke-dasharray="5,5"/>
  <line x1="315" y1="230" x2="360" y2="170" stroke="#333" stroke-width="1.5" stroke-dasharray="5,5"/>
  <line x1="465" y1="230" x2="400" y2="170" stroke="#333" stroke-width="1.5" stroke-dasharray="5,5"/>
</svg>

---

## Component Interface

```cpp
class Beverage {
public:
    virtual ~Beverage() = default;
    virtual std::string getDescription() const = 0;
    virtual double getCost() const = 0;
};

class Espresso : public Beverage {
public:
    std::string getDescription() const override {
        return "Espresso";
    }
    double getCost() const override {
        return 1.99;
    }
};

class HouseBlend : public Beverage {
public:
    std::string getDescription() const override {
        return "House Blend Coffee";
    }
    double getCost() const override {
        return 0.89;
    }
};
```

---

## Decorator Base

```cpp
class CondimentDecorator : public Beverage {
protected:
    std::unique_ptr<Beverage> beverage;

public:
    explicit CondimentDecorator(std::unique_ptr<Beverage> b)
        : beverage(std::move(b)) {}
};
```

---

## Concrete Decorators

```cpp
class Milk : public CondimentDecorator {
public:
    using CondimentDecorator::CondimentDecorator;

    std::string getDescription() const override {
        return beverage->getDescription() + ", Milk";
    }
    double getCost() const override {
        return beverage->getCost() + 0.30;
    }
};

class Sugar : public CondimentDecorator {
public:
    using CondimentDecorator::CondimentDecorator;

    std::string getDescription() const override {
        return beverage->getDescription() + ", Sugar";
    }
    double getCost() const override {
        return beverage->getCost() + 0.20;
    }
};

class WhippedCream : public CondimentDecorator {
public:
    using CondimentDecorator::CondimentDecorator;

    std::string getDescription() const override {
        return beverage->getDescription() + ", Whipped Cream";
    }
    double getCost() const override {
        return beverage->getCost() + 0.50;
    }
};
```

---

## Decorator Usage

```cpp
// Start with a base beverage
std::unique_ptr<Beverage> drink = std::make_unique<Espresso>();

// Dynamically add condiments by wrapping
drink = std::make_unique<Milk>(std::move(drink));
drink = std::make_unique<Sugar>(std::move(drink));
drink = std::make_unique<WhippedCream>(std::move(drink));

std::cout << drink->getDescription() << "\n";
// Espresso, Milk, Sugar, Whipped Cream

std::cout << "$" << drink->getCost() << "\n";
// $2.99
```

Each decorator wraps the previous one, adding its behavior

---

## Real-World Example: Stream Decorators

```cpp
class DataStream {
public:
    virtual void write(const std::string& data) = 0;
    virtual std::string read() = 0;
    virtual ~DataStream() = default;
};

class FileStream : public DataStream {
public:
    void write(const std::string& data) override { /* write to file */ }
    std::string read() override { return /* read from file */; }
};

class EncryptionDecorator : public DataStream {
    std::unique_ptr<DataStream> wrapped;
public:
    explicit EncryptionDecorator(std::unique_ptr<DataStream> s)
        : wrapped(std::move(s)) {}

    void write(const std::string& data) override {
        wrapped->write(encrypt(data));
    }
    std::string read() override {
        return decrypt(wrapped->read());
    }
};

class CompressionDecorator : public DataStream {
    std::unique_ptr<DataStream> wrapped;
public:
    explicit CompressionDecorator(std::unique_ptr<DataStream> s)
        : wrapped(std::move(s)) {}

    void write(const std::string& data) override {
        wrapped->write(compress(data));
    }
    std::string read() override {
        return decompress(wrapped->read());
    }
};
```

---

## Composing Stream Decorators

```cpp
// Compose: file -> compress -> encrypt
std::unique_ptr<DataStream> stream = std::make_unique<FileStream>("data.bin");
stream = std::make_unique<CompressionDecorator>(std::move(stream));
stream = std::make_unique<EncryptionDecorator>(std::move(stream));

stream->write("sensitive data");
// Data is encrypted, then compressed, then written to file
```

---

## When to Use Decorator

**Use when:**

- You want to add responsibilities to objects dynamically
- Extension by subclassing is impractical (too many combinations)
- You want to combine behaviors in arbitrary ways

**Avoid when:**

- The component interface is large (many methods to delegate)
- Order of decoration matters and is hard to control
- A simpler composition approach would suffice
