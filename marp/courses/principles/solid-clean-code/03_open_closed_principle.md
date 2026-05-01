---
tags:
  - concepts:solid
  - concepts:ocp
level: intermediate
category: design-patterns
audience:
  - audiences:developers

---
# Open/Closed Principle (OCP)

---
## What This Chapter Covers

- A precise statement of OCP
- A worked refactoring from a switch chain to polymorphism
- Strategy pattern as OCP's main vehicle
- Plugin architectures
- Limits: when to *not* apply OCP

---
## The Principle, Stated Carefully

- "Open for extension, closed for modification" — Bertrand Meyer
- You should be able to *add* behaviour without *changing* existing code
- Achieved through abstractions: interfaces, base classes, callbacks
- The *abstraction* is closed; the *implementations* extend it
- Reduces the risk of breaking working code when adding features

---
## A Smelly Function

```python
def calculate_pay(employee):
    if employee.type == "salaried":
        return employee.salary / 12
    elif employee.type == "hourly":
        return employee.hours * employee.rate
    elif employee.type == "contractor":
        return sum(invoice.amount for invoice in employee.invoices)
    else:
        raise ValueError(f"unknown type: {employee.type}")
```

- Adding a new employee type means *editing* this function
- Same change in tax calculation, benefits, leave accrual — touches every function
- High risk: regressions in the other branches

---
## A First Refactor: Polymorphism

```python
class Employee(ABC):
    @abstractmethod
    def monthly_pay(self): ...

class Salaried(Employee):
    def monthly_pay(self): return self.salary / 12

class Hourly(Employee):
    def monthly_pay(self): return self.hours * self.rate

class Contractor(Employee):
    def monthly_pay(self):
        return sum(i.amount for i in self.invoices)
```

- Adding `Intern(Employee)` doesn't touch any existing class
- The "calculate_pay" function shrinks to `employee.monthly_pay()`

---
## Strategy Pattern

- A specific OCP-realising design
- Pass the varying behaviour as an *object*
- Add new strategies without touching the consumer
- Common in libraries: comparators, validators, parsers
- Functional languages do it with first-class functions

---
## Strategy in Java

```java
public interface Discount {
    double apply(double price);
}

public class CartCalculator {
    private final Discount discount;
    public CartCalculator(Discount d) { this.discount = d; }
    public double total(List<Item> items) {
        return discount.apply(items.stream().mapToDouble(Item::price).sum());
    }
}
```

- New discount = new class implementing `Discount`
- `CartCalculator` doesn't change

---
## Strategy in Python

```python
def total(items, discount):
    return discount(sum(i.price for i in items))

# Just functions:
def no_discount(amount): return amount
def black_friday(amount): return amount * 0.8
```

- Functions are first-class — no need for an interface class
- Add new pricing rules by writing a new function
- Pass it in at the call site

---
## Plugin Architectures

- A program defines an interface and discovers implementations at runtime
- Examples: `pytest` plugins, Visual Studio Code extensions, IDE syntax highlighters
- Adding a new plugin doesn't recompile the host
- The host is the OCP "closed" part; plugins are the "open" part
- Heavy investment, big payoff for systems with many extension points

---
## OCP and Inheritance

- Subclasses extend without modifying the base
- Easy to misuse: subclasses that depend on the base's *implementation*
- Better: program to interfaces, not to concrete base classes
- Composition + delegation often beats deep inheritance for OCP
- See the Liskov chapter for what happens when subclass contracts diverge

---
## Limits of OCP

- Every extension point is a *cost*: an interface, more files, more indirection
- Don't add an extension point until the second variation actually arrives
- "We might need to support X" is the most common design fallacy
- Adding extension *for the second variation* is cheap and informed
- Adding extension *speculatively* is expensive and usually wrong

---
## When OCP Hurts

- One implementation forever: the abstraction is overhead
- The variation is one branch in one place: a switch is fine
- The team is two people and the design churns: defer abstractions
- Premature OCP gives you many tiny one-implementation interfaces

---
## Recognising the Smell

- Long if/elif/switch chains that grow with each release
- A central function that you have to touch for *any* feature
- "Add a new type" tickets that always touch the same 4 files
- Clear pattern across the branches — same shape, different details
- Bug fix in one branch leaves the others broken because they need the same fix

---
## A Refactoring Recipe

- Identify the switch / if-chain
- Extract each branch into a method
- Find a common interface (a base class or a function signature)
- Replace the switch with a dispatch through that interface
- Add new variants as new implementations

---
## OCP and the Other Principles

- OCP needs polymorphism &#8594; needs LSP to be safe
- OCP without ISP gives bloated interfaces
- OCP without DIP couples the consumer to a concrete extension mechanism
- The principles reinforce each other when applied together

---
## Common Mistakes

- Adding interfaces "in case we need them" — premature OCP
- Switch chains kept on the consumer side after extraction
- Subclasses that only override one method — could be a function instead
- Plugin frameworks for things that change once a year — overengineering
- Forgetting that *adding the abstraction* is itself a modification
