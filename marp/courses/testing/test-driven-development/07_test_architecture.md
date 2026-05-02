---
tags:
  - practices:tdd
  - practices:test-architecture
level: intermediate
category: testing
audience:
  - audiences:developers

---
# Test Architecture

---
## AAA Pattern

![test_architecture](svg/courses/testing/test-driven-development/07_test_architecture/test_architecture.svg)

---
## What This Chapter Covers

- The testing pyramid
- Organising test suites
- Test fixtures and shared setup
- Test data management
- Test configuration and environments
- Parallel test execution
- Coverage metrics

---
## The Testing Pyramid

- **Unit**: many; fast; isolated; the base
- **Integration**: some; slower; multiple components
- **End-to-end**: few; slow; whole system
- More at the bottom; less at the top
- Inverted pyramid (mostly E2E) is a smell

---
## Why Pyramid Shape

- Unit tests are fast and pinpoint failures
- E2E tests are slow and vague when they fail
- A 10000-test unit suite + 50 E2E tests is healthy
- A 50-test unit suite + 1000 E2E tests is dysfunctional
- Cost / value ratio favours the bottom

---
## Unit Test Layer

- One test, one unit (function or class)
- All collaborators stubbed or faked
- Milliseconds per test
- Run on every commit, every save
- The bedrock of fast feedback

---
## Integration Test Layer

- Multiple components together
- Real database (per-test or shared with cleanup)
- Real HTTP between services if needed
- Seconds per test
- Run on every PR, not every save

---
## End-to-End Test Layer

- The whole system, browser to database
- Tools: Playwright, Cypress, Selenium
- Test the critical user journeys
- Minutes per test suite
- Run nightly or pre-deploy

---
## Organising Test Suites

- Mirror the production code structure
- `src/auth/login.py` &#8594; `tests/auth/test_login.py`
- Or separate folders: `tests/unit/`, `tests/integration/`
- Run by tier or by module
- Whatever fits, use consistently

---
## Test Fixtures

- Reusable setup code
- Database with seed data
- Browser session
- Mock HTTP server
- Build once, share across tests

---
## pytest Fixtures

```python
@pytest.fixture(scope='session')
def db():
    db = create_test_db()
    yield db
    db.drop()

@pytest.fixture
def user(db):
    u = db.add(User('alice'))
    yield u
    db.delete(u)

def test_login(user):
    assert login(user.email, 'pwd')
```

- `scope`: function (default), class, module, session
- Composable: fixtures can use other fixtures
- Cleanup runs even on failure

---
## Test Data Management

- **Inline**: each test creates its own data
- **Fixtures**: reusable factories
- **Fixtures + factories**: factory-boy / faker for realistic data
- **Snapshots**: a known database state, restored between tests
- Pick one; consistency aids debugging

---
## Factories

```python
import factory

class UserFactory(factory.Factory):
    class Meta:
        model = User
    name = factory.Faker('name')
    email = factory.Faker('email')

# In a test:
user = UserFactory.create(role='admin')
```

- Realistic-looking data
- Override what you care about
- Default for the rest
- Reduces "magic" data in tests

---
## Test Configuration

- Different config per environment (test, integration, staging)
- Inject; don't hardcode
- `.env.test` files; `pytest.ini`; `jest.config.js`
- Tests should run with `pytest` (no flags) by default
- Special suites with markers (`@pytest.mark.slow`)

---
## Environment Setup

- Test against a clean state
- Reset DB between tests (transaction rollback is faster than truncate)
- Reset external systems too (mocks, fakes, in-memory)
- Test should not depend on previous test's leftovers
- Order-independent

---
## Parallel Execution

- Run tests in parallel across cores
- pytest-xdist, JUnit parallel runners
- 4-8x speedup typical
- Watch: shared state, ports, file locks
- Worth the upfront cleanup work

---
## What Breaks With Parallelism

- Shared mutable state
- Hardcoded ports
- Singleton clients to external systems
- Database without per-worker schema
- Identify and fix; you'll be glad later

---
## Test Coverage

- Percentage of code lines (or branches) executed by tests
- Tools: coverage.py, JaCoCo, Istanbul
- Useful as a *floor*, not a goal
- 80% is a reasonable starting target
- 100% coverage doesn't mean bug-free

---
## Coverage Metrics

- **Line**: did each line run?
- **Branch**: did each branch (if/else) run both ways?
- **Statement**: similar to line
- Branch coverage catches more than line
- Don't game the metric

---
## Coverage Gates

- Fail PRs that drop coverage below a threshold
- Coverage must increase or stay flat
- Codecov, Coveralls integrate with PRs
- Some teams require a target (80%+); some don't
- Either: gradual or hard threshold

---
## Common Architecture Mistakes

- Inverted pyramid (mostly E2E)
- Slow unit tests (hidden integration tests)
- Tests that depend on each other
- Shared mutable test data
- 100% coverage as the goal (writes meaningless tests)
- No CI; tests run only on developer machines
