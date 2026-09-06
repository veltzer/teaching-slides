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

![builder_structure](svg/courses/languages/c++/c++-design-patterns/05_builder/builder_structure.svg)

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
