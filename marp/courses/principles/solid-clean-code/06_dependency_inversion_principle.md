---
tags:
  - concepts:solid
  - concepts:dip
level: intermediate
category: design-patterns
audience:
  - audiences:developers

---
# Dependency Inversion Principle (DIP)

---
## What This Chapter Covers

- A precise statement of DIP
- High-level vs low-level modules
- Dependency injection
- IoC containers — when to use, when not
- Testing benefits
- Common pitfalls

---
## The Principle, Stated Carefully

- "High-level modules shouldn't depend on low-level modules — both should depend on abstractions"
- "Abstractions shouldn't depend on details — details should depend on abstractions"
- The "inversion" is the direction of dependency at the boundary
- Without DIP: business logic imports the database module
- With DIP: business logic depends on a Repository interface; the database module implements it

---
## A Smelly Class

```python
class OrderService:
    def __init__(self):
        self.db = PostgresDB("host", "user", "pass")  # concrete
        self.email = SMTPClient("smtp.gmail.com")     # concrete

    def place_order(self, order):
        self.db.save(order)
        self.email.send_confirmation(order)
```

- Construction is hidden; can't supply alternatives
- Can't unit test without a real Postgres and SMTP server
- Switching DB or SMTP provider edits this class

---
## After DIP

```python
class OrderService:
    def __init__(self, db: OrderRepository, email: Notifier):
        self._db = db
        self._email = email

    def place_order(self, order):
        self._db.save(order)
        self._email.send_confirmation(order)
```

- Dependencies are *passed in*
- `OrderRepository` and `Notifier` are abstractions in the same layer as `OrderService`
- Postgres and SMTP implementations live in another layer that imports the abstractions

---
## Dependency Injection

- The pattern of passing collaborators in, instead of constructing them inside
- Three flavours:
    - **Constructor injection** (most common)
    - **Setter injection** (mutable state, used for optional dependencies)
    - **Method injection** (pass per call — for things that vary per request)
- Constructor injection wins by default — invariants set at construction

---
## Wiring at the Edge

```python
def main():
    db = PostgresOrderRepository(...)
    email = SMTPNotifier(...)
    service = OrderService(db, email)
    service.place_order(...)
```

- All concrete construction happens at one place
- Often called the "composition root"
- The rest of the app talks to abstractions
- Replacing implementations means changing one file

---
## IoC Containers

- A library that registers types and resolves their dependencies automatically
- Examples: Spring (Java), Microsoft.Extensions.DependencyInjection (.NET), wired (Go)
- Useful in large apps with deep dependency graphs
- Overkill for small projects — manual wiring is clearer
- Magic resolution can mask cyclic dependencies and other smells

---
## Testing Benefits

```python
class StubRepo:
    def save(self, order): self.saved = order
    def get(self, id): return self.saved

class StubNotifier:
    def send_confirmation(self, order): self.sent = order

def test_place_order():
    repo, mailer = StubRepo(), StubNotifier()
    OrderService(repo, mailer).place_order(my_order)
    assert repo.saved == my_order
    assert mailer.sent == my_order
```

- Fast, isolated, no real I/O
- Test exactly the OrderService logic

---
## DIP and Plugin Architectures

- The plugin host depends on a plugin interface
- Plugins implement the interface
- Both depend on the abstraction; the host depends on no specific plugin
- Loading is dynamic, often via the language's reflection or service-loader mechanism
- Same idea, scaled up

---
## DIP at Layer Boundaries

- Business layer defines `Repository` interface
- Persistence layer implements it
- Persistence layer *imports* the business layer's interface
- This inverts the natural "business uses persistence" dependency
- Hexagonal/Clean architecture is built on this inversion

---
## When DIP Hurts

- One implementation forever &#8594; the abstraction is overhead
- Two-class apps where everything is in one file
- Performance-critical inner loops where the indirection hurts
- Premature DIP gives you many one-implementation interfaces

---
## DIP Done Wrong: Service Locator

- Class asks a global container for its dependencies
- "Hidden" dependencies — the constructor signature lies
- Hard to test because dependencies are pulled, not pushed
- Generally an anti-pattern; constructor injection is clearer

---
## DIP Done Wrong: Anaemic Interfaces

- One interface per implementation, even when there's one of each
- Every class has its `IFoo` next to it
- Adds files and noise without flexibility
- Refactor: until the second implementation appears, just use the concrete class

---
## DIP and the Test Pyramid

- The unit-test layer especially benefits from DIP — fast, isolated tests
- Integration tests still exercise the real implementations
- End-to-end tests prove the whole composition works
- DIP gives you the *option* to mock; doesn't oblige you

---
## A Refactoring Recipe

- Find the concrete dependency hiding in a constructor or method
- Define an interface that captures only what the consumer uses
- Have the consumer depend on the interface
- Move the concrete construction to the composition root
- Pass the concrete instance into the consumer at startup

---
## Common Mistakes

- Defining interfaces that mirror the implementation (`IDatabaseConnection` with `connect()`/`disconnect()`)
- Putting wiring logic deep inside the application
- Creating multi-level inheritance instead of injection
- Mocking everything — including pure functions and value objects
- Confusing "DI framework" with "DIP" — they're related, not the same thing
