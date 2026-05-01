---
tags:
  - architecture:clean-architecture
  - practices:testing
level: intermediate
category: architecture
audience:
  - audiences:developers

---
# Testing Clean Architecture

---
## What This Chapter Covers

- Why clean architecture is testable
- Unit testing the domain
- Integration tests for adapters
- End-to-end tests
- Test pyramid for clean architecture
- Common patterns

---
## Why Testable

- Domain has no external dependencies
- Use cases work with port interfaces
- Adapters are replaceable with fakes
- Unit tests run in milliseconds
- Refactor with confidence

---
## Domain Tests

- Pure entity tests
- No mocks
- Just `assert` against domain rules
- Fast and reliable

---
## Use Case Tests

- Inject fake adapters
- Call execute()
- Assert on returned value and fake adapter state
- Fast (no DB, no HTTP)

---
## Use Case Test Example

```python
def test_place_order_persists_and_emails():
    repo = InMemoryOrderRepository()
    mailer = FakeMailer()
    use_case = PlaceOrderUseCase(repo, mailer)

    order = use_case.execute(customer_id=1, items=[Item(...)])

    assert repo.find(order.id) is not None
    assert mailer.sent_count() == 1
```

---
## Adapter Integration Tests

- Test the real adapter against a real (test) backend
- PostgresOrderRepository against real Postgres
- Catches: SQL errors, connection issues
- Slower than unit tests; runs less often

---
## End-To-End Tests

- Real HTTP / browser / etc.
- Whole stack
- Few; covering the critical paths
- The slow but most-realistic tier

---
## Test Pyramid

- Many: domain + use case (unit)
- Some: adapter integration
- Few: end-to-end
- Match cost to value

---
## Fakes vs Mocks

- Fakes: working implementations (in-memory repo)
- Mocks: pre-programmed expectations
- Clean architecture favours fakes
- Real behaviour, no expectations to maintain

---
## A Practical Fake

```python
class InMemoryOrderRepository(OrderRepository):
    def __init__(self):
        self._orders = {}
    def save(self, order):
        self._orders[order.id] = order
    def find(self, id):
        return self._orders.get(id)
```

- Simple; works for many tests; reusable

---
## Test Data Builders

- Construct test entities easily
- Fluent API: `OrderBuilder().with_items(...).build()`
- Reduces test boilerplate
- Faker for realistic-looking data

---
## Property-Based Testing

- Generate random valid inputs
- Check invariants
- Hypothesis (Python), QuickCheck (Haskell)
- Excellent for domain logic

---
## TDD With Clean Architecture

- Red: write failing test for use case
- Green: implement use case
- Refactor: clean up
- Adapters added later (or in parallel)
- Architecture supports the rhythm

---
## Common Testing Mistakes

- Testing through HTTP when use case test would do
- Mocking everything (over-mocking)
- Skipping adapter tests &#8594; missed SQL bugs
- One mega-test that covers everything
- Tests that depend on test order
