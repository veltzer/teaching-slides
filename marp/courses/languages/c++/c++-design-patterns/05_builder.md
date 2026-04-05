# Builder Pattern

---

## Intent

- Separate the construction of a complex object from its representation
- Allow the same construction process to create different representations
- Avoid constructors with many parameters (telescoping constructor problem)

---

## Problem: Telescoping Constructors

```cpp
class Pizza {
public:
    // Too many parameters — hard to read and error-prone
    Pizza(Size size, bool cheese, bool pepperoni, bool mushrooms,
          bool onions, bool bacon, bool olives, bool peppers,
          CrustType crust, SauceType sauce) { ... }
};

// Which bool is which?
Pizza p(Size::Large, true, false, true, false, true, false, true,
        CrustType::Thin, SauceType::Tomato);
```

---

## Builder Structure

<svg width="600" height="250" xmlns="http://www.w3.org/2000/svg">
  <rect x="220" y="10" width="160" height="60" fill="#e3f2fd" stroke="#1976d2" stroke-width="2"/>
  <text x="300" y="35" text-anchor="middle" font-size="13" font-weight="bold">Director</text>
  <text x="300" y="55" text-anchor="middle" font-size="11">+ construct()</text>

  <rect x="220" y="110" width="160" height="70" fill="#e8f5e8" stroke="#388e3c" stroke-width="2"/>
  <text x="300" y="130" text-anchor="middle" font-size="13" font-weight="bold">Builder</text>
  <text x="300" y="150" text-anchor="middle" font-size="11" font-style="italic">+ buildStepA()</text>
  <text x="300" y="165" text-anchor="middle" font-size="11" font-style="italic">+ buildStepB()</text>

  <rect x="50" y="220" width="160" height="30" fill="#fff3e0" stroke="#f57c00" stroke-width="2"/>
  <text x="130" y="240" text-anchor="middle" font-size="11">ConcreteBuilder1</text>

  <rect x="390" y="220" width="160" height="30" fill="#fff3e0" stroke="#f57c00" stroke-width="2"/>
  <text x="470" y="240" text-anchor="middle" font-size="11">ConcreteBuilder2</text>

  <line x1="300" y1="70" x2="300" y2="110" stroke="#333" stroke-width="1.5" marker-end="url(#bArr)"/>
  <line x1="130" y1="220" x2="260" y2="180" stroke="#333" stroke-width="1.5" stroke-dasharray="5,5"/>
  <line x1="470" y1="220" x2="340" y2="180" stroke="#333" stroke-width="1.5" stroke-dasharray="5,5"/>

  <rect x="480" y="110" width="100" height="40" fill="#fce4ec" stroke="#c2185b" stroke-width="2"/>
  <text x="530" y="135" text-anchor="middle" font-size="12">Product</text>

  <line x1="380" y1="140" x2="480" y2="130" stroke="#333" stroke-width="1.5" stroke-dasharray="3,3"/>
  <text x="430" y="125" font-size="9">creates</text>

  <defs>
    <marker id="bArr" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Builder Solution

```cpp
class Pizza {
public:
    enum class Size { Small, Medium, Large };
    enum class Crust { Thin, Thick, Stuffed };
    enum class Sauce { Tomato, BBQ, Alfredo };

private:
    Size size;
    Crust crust;
    Sauce sauce;
    std::vector<std::string> toppings;

    friend class PizzaBuilder;
    Pizza() = default;

public:
    void describe() const {
        std::cout << "Pizza with " << toppings.size() << " toppings\n";
    }
};
```

---

## The Builder Class

```cpp
class PizzaBuilder {
    Pizza pizza;

public:
    PizzaBuilder& setSize(Pizza::Size s) {
        pizza.size = s;
        return *this;
    }

    PizzaBuilder& setCrust(Pizza::Crust c) {
        pizza.crust = c;
        return *this;
    }

    PizzaBuilder& setSauce(Pizza::Sauce s) {
        pizza.sauce = s;
        return *this;
    }

    PizzaBuilder& addTopping(const std::string& topping) {
        pizza.toppings.push_back(topping);
        return *this;
    }

    Pizza build() {
        return std::move(pizza);
    }
};
```

---

## Fluent Builder Usage

```cpp
auto pizza = PizzaBuilder()
    .setSize(Pizza::Size::Large)
    .setCrust(Pizza::Crust::Thin)
    .setSauce(Pizza::Sauce::Tomato)
    .addTopping("cheese")
    .addTopping("mushrooms")
    .addTopping("peppers")
    .build();

pizza.describe();
```

Clear, readable, and self-documenting

---

## Builder with Validation

```cpp
class QueryBuilder {
    std::string table;
    std::vector<std::string> columns;
    std::string whereClause;
    std::string orderBy;
    int limit = -1;

public:
    QueryBuilder& from(const std::string& t) {
        table = t;
        return *this;
    }

    QueryBuilder& select(const std::string& col) {
        columns.push_back(col);
        return *this;
    }

    QueryBuilder& where(const std::string& condition) {
        whereClause = condition;
        return *this;
    }

    std::string build() {
        if (table.empty()) {
            throw std::logic_error("Table name is required");
        }
        std::string query = "SELECT ";
        query += columns.empty() ? "*" : join(columns, ", ");
        query += " FROM " + table;
        if (!whereClause.empty()) query += " WHERE " + whereClause;
        if (!orderBy.empty()) query += " ORDER BY " + orderBy;
        if (limit > 0) query += " LIMIT " + std::to_string(limit);
        return query;
    }
};
```

---

## Director Pattern

```cpp
class MealDirector {
public:
    Pizza buildVeggiePizza(PizzaBuilder& builder) {
        return builder
            .setSize(Pizza::Size::Medium)
            .setCrust(Pizza::Crust::Thin)
            .setSauce(Pizza::Sauce::Tomato)
            .addTopping("mushrooms")
            .addTopping("peppers")
            .addTopping("onions")
            .addTopping("olives")
            .build();
    }

    Pizza buildMeatLoversPizza(PizzaBuilder& builder) {
        return builder
            .setSize(Pizza::Size::Large)
            .setCrust(Pizza::Crust::Thick)
            .setSauce(Pizza::Sauce::BBQ)
            .addTopping("pepperoni")
            .addTopping("bacon")
            .addTopping("sausage")
            .build();
    }
};
```

The Director encapsulates common construction recipes

---

## When to Use Builder

**Use when:**

- Objects require many construction steps
- Different representations of an object are needed
- Constructor would have too many parameters
- Object construction must be independent of parts that make up the object

**Avoid when:**

- Objects are simple with few fields
- Immutability is not a concern and setters suffice
- The overhead of a separate builder class is not justified
