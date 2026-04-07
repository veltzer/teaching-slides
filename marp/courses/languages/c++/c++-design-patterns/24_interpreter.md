# Interpreter Pattern

---

## Intent

- Define a grammar for a simple language
- Build an interpreter that uses the grammar to interpret sentences in the language
- Represent language rules as a class hierarchy

---

## Problem: Evaluating Expressions

```cpp
// Hardcoded evaluation — not extensible
double evaluate(const std::string& expr) {
    // How do you parse "3 + 5 * 2"?
    // How do you add new operators?
    // How do you handle nested expressions?
}
```

---

## Interpreter Structure

![interpreter_structure](svg/courses/languages/c++/c++-design-patterns/24_interpreter/interpreter_structure.svg)

---

## Expression Interface

```cpp
class Expression {
public:
    virtual double interpret() const = 0;
    virtual std::string toString() const = 0;
    virtual ~Expression() = default;
};
```

---

## Terminal and Non-Terminal Expressions

```cpp
class NumberExpression : public Expression {
    double value;
public:
    explicit NumberExpression(double v) : value(v) {}
    double interpret() const override { return value; }
    std::string toString() const override {
        return std::to_string(value);
    }
};

class AddExpression : public Expression {
    std::unique_ptr<Expression> left, right;
public:
    AddExpression(std::unique_ptr<Expression> l,
                  std::unique_ptr<Expression> r)
        : left(std::move(l)), right(std::move(r)) {}

    double interpret() const override {
        return left->interpret() + right->interpret();
    }
    std::string toString() const override {
        return "(" + left->toString() + " + " + right->toString() + ")";
    }
};

class MultiplyExpression : public Expression {
    std::unique_ptr<Expression> left, right;
public:
    MultiplyExpression(std::unique_ptr<Expression> l,
                       std::unique_ptr<Expression> r)
        : left(std::move(l)), right(std::move(r)) {}

    double interpret() const override {
        return left->interpret() * right->interpret();
    }
    std::string toString() const override {
        return "(" + left->toString() + " * " + right->toString() + ")";
    }
};
```

---

## Building and Evaluating Expressions

```cpp
// Represent: (3 + 5) * 2
auto expr = std::make_unique<MultiplyExpression>(
    std::make_unique<AddExpression>(
        std::make_unique<NumberExpression>(3),
        std::make_unique<NumberExpression>(5)
    ),
    std::make_unique<NumberExpression>(2)
);

std::cout << expr->toString() << " = " << expr->interpret() << "\n";
// ((3 + 5) * 2) = 16
```

---

## Boolean Expression Interpreter

```cpp
class BoolExpression {
public:
    virtual bool interpret(
        const std::unordered_map<std::string, bool>& context) const = 0;
    virtual ~BoolExpression() = default;
};

class Variable : public BoolExpression {
    std::string name;
public:
    explicit Variable(std::string n) : name(std::move(n)) {}
    bool interpret(const std::unordered_map<std::string, bool>& ctx) const override {
        return ctx.at(name);
    }
};

class AndExpression : public BoolExpression {
    std::unique_ptr<BoolExpression> left, right;
public:
    AndExpression(std::unique_ptr<BoolExpression> l,
                  std::unique_ptr<BoolExpression> r)
        : left(std::move(l)), right(std::move(r)) {}

    bool interpret(const std::unordered_map<std::string, bool>& ctx) const override {
        return left->interpret(ctx) && right->interpret(ctx);
    }
};

class OrExpression : public BoolExpression {
    std::unique_ptr<BoolExpression> left, right;
public:
    OrExpression(std::unique_ptr<BoolExpression> l,
                 std::unique_ptr<BoolExpression> r)
        : left(std::move(l)), right(std::move(r)) {}

    bool interpret(const std::unordered_map<std::string, bool>& ctx) const override {
        return left->interpret(ctx) || right->interpret(ctx);
    }
};

class NotExpression : public BoolExpression {
    std::unique_ptr<BoolExpression> operand;
public:
    explicit NotExpression(std::unique_ptr<BoolExpression> op)
        : operand(std::move(op)) {}

    bool interpret(const std::unordered_map<std::string, bool>& ctx) const override {
        return !operand->interpret(ctx);
    }
};
```

---

## Boolean Expression Usage

```cpp
// (A AND B) OR (NOT C)
auto expr = std::make_unique<OrExpression>(
    std::make_unique<AndExpression>(
        std::make_unique<Variable>("A"),
        std::make_unique<Variable>("B")
    ),
    std::make_unique<NotExpression>(
        std::make_unique<Variable>("C")
    )
);

std::unordered_map<std::string, bool> ctx = {
    {"A", true}, {"B", false}, {"C", false}
};
std::cout << std::boolalpha << expr->interpret(ctx) << "\n";
// true (A AND B = false, NOT C = true, false OR true = true)
```

---

## When to Use Interpreter

**Use when:**

- The grammar is simple and efficiency is not critical
- You want to evaluate expressions or rules defined at runtime
- The language can be represented as an abstract syntax tree

**Avoid when:**

- The grammar is complex (use a proper parser generator instead)
- Performance is critical (tree walking is slow for large expressions)

**Common examples:**

- SQL WHERE clause parsing
- Configuration file parsing
- Regular expression engines
- Rule engines for business logic
