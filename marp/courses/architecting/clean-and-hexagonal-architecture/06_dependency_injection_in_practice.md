---
tags:
  - architecture:clean-architecture
  - architecture:di
level: intermediate
category: architecture
audience:
  - audiences:developers

---
# Dependency Injection in Practice

---
## Container Pattern

![di_container](svg/courses/architecting/clean-and-hexagonal-architecture/06_dependency_injection_in_practice/di_container.svg)

---
## DI Styles

![di_styles](svg/courses/architecting/clean-and-hexagonal-architecture/06_dependency_injection_in_practice/di_styles.svg)

---
## What This Chapter Covers

- Why DI
- Manual wiring
- DI containers
- Constructor injection
- Common DI mistakes
- Tool choice

---
## Why DI

- Inner layers don't construct outer
- Implementations passed in
- Replaceable for testing
- Wiring at the composition root

---
## Constructor Injection

- Dependencies in constructor
- Fail fast: missing deps fail at construction
- Object always valid post-construction
- The default

---
## Setter Injection

- Dependencies via setters after construction
- Object can exist without dependencies
- Useful for circular dependencies (rare)
- Use sparingly

---
## Manual Wiring

```python
def main():
    db = create_db()
    order_repo = PostgresOrderRepository(db)
    mailer = SmtpMailer()
    use_case = PlaceOrderUseCase(order_repo, mailer)
    controller = OrderController(use_case)
    serve(controller)
```

- Explicit; readable
- For small / medium apps: ideal

---
## DI Containers

- Spring (Java), Microsoft.Extensions (.NET), wired (Go), inversify (TS)
- Auto-wire dependencies
- Useful at scale (hundreds of components)
- Magic: harder to debug

---
## Composition Root

- The single place wiring happens
- main() / Application class
- Everything else: pure dependency consumption
- Avoid: wiring scattered throughout the code

---
## Lifetime / Scope

- Singleton: one instance per app
- Scoped: one per request
- Transient: new each call
- Pick by: stateful or stateless component
- Misuse: state leaks across requests (singleton with state)

---
## DI Anti-Patterns

- Service Locator: components ask container for deps
- Hides dependencies (constructor lies)
- Hard to test; magic
- Avoid

---
## Optional Dependencies

- Some deps are optional
- Default to a no-op
- Or: nullable / Optional in language
- Don't make tests construct everything

---
## Circular Dependencies

- A &#8594; B &#8594; A
- Smell: redesign
- Workaround: setter injection, lazy init
- Better: extract a third component to break the cycle

---
## Test-Time DI

- Test constructs use case with fakes
- No container needed for unit tests
- Integration tests: small container or manual
- Don't pull in the production wiring for unit tests

---
## DI vs Service Locator

- DI: constructor declares deps; passed in
- Service Locator: code fetches from container
- DI better: dependencies visible
- Service Locator: hides; harder to test

---
## Common DI Mistakes

- Service Locator pattern
- DI container in unit tests (slow)
- Singletons with mutable state
- Scope misuse (request-scoped used as singleton)
- "Configure all the things" container as a god-object
