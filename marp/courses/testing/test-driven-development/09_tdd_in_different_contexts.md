---
tags:
  - practices:tdd
level: intermediate
category: testing
audience:
  - audiences:developers

---
# TDD in Different Contexts

---
## What This Chapter Covers

- TDD for web applications
- TDD for APIs and microservices
- TDD for data processing and algorithms
- TDD with databases and persistence
- TDD in legacy codebases
- Where TDD struggles

---
## Across Contexts

![tdd_contexts](svg/courses/testing/test-driven-development/09_tdd_in_different_contexts/tdd_contexts.svg)

---
## Web Applications

- Unit tests: components, controllers, business logic
- Integration tests: API contracts, DB interactions
- E2E tests: critical user journeys (signup, checkout)
- Frontend: testing-library, Cypress, Playwright
- Backend: framework-specific (Rails, Django, Spring)

---
## Frontend TDD

- Component-level tests with React Testing Library, Vue Test Utils
- Mock fetch / network at the boundary
- Snapshot tests for UI structure (use sparingly)
- Visual regression testing for the rendered UI (Chromatic, Percy)
- E2E with Cypress / Playwright for flows

---
## APIs and Microservices

- TDD per endpoint
- Tests describe the API contract
- Integration tests against a real server
- Contract testing (Pact, Spring Cloud Contract) for cross-service
- Mock external services; test against the contract

---
## Contract Testing

- Provider says "I support these calls"
- Consumer says "I need these calls"
- Tests verify both sides agree
- Catches breaking API changes early
- Pact is the leading tool

---
## Algorithms and Data Processing

- TDD shines here
- Pure functions; easy to test
- Many small examples drive the design
- Property-based testing complements (Hypothesis, QuickCheck)
- Performance tests separate from correctness tests

---
## Property-Based Testing

```python
from hypothesis import given, strategies as st

@given(st.lists(st.integers()))
def test_sort_idempotent(xs):
    assert sorted(sorted(xs)) == sorted(xs)

@given(st.integers(), st.integers())
def test_add_commutative(a, b):
    assert add(a, b) == add(b, a)
```

- Generate inputs; check invariants
- Catches edge cases you didn't think of
- Combines well with TDD

---
## Databases

- Unit tests: mock the repository
- Integration tests: real DB (or in-memory variant)
- Per-test: transaction rollback for speed
- Avoid: shared DB state across tests
- Tools: testcontainers for ephemeral DBs

---
## TestContainers

```python
from testcontainers.postgres import PostgresContainer

@pytest.fixture(scope='session')
def db():
    with PostgresContainer('postgres:16') as p:
        yield connect(p.get_connection_url())

def test_user_save(db):
    save(db, User(name='Alice'))
    assert get(db, name='Alice') is not None
```

- Real Postgres; ephemeral
- Per-test or per-session
- Drops the "but unit tests can't touch the DB" problem

---
## Legacy Codebases

- Untested code; making changes is risky
- Add characterisation tests first
- Then refactor inside the safety net
- Then add features (TDD-style for the new code)
- Don't try to test everything at once

---
## Brownfield TDD

- Existing code; partial test coverage
- New features: TDD
- Bug fixes: write the failing test first
- Refactors: tests must exist (write characterisation if not)
- Coverage grows over time

---
## When TDD Struggles

- UI animations and visual design
- Highly stochastic systems (ML training)
- Throwaway scripts
- Embedded code with hardware-only behaviour
- Discovery / research where you don't know the requirements

---
## TDD With ML

- Tests for: data pipeline, feature engineering, post-processing
- Hard to test: model training, model accuracy
- Train/test split *is* a kind of test
- Track metrics over time; alert on regressions
- TDD applies to the *engineering*, not the *learning*

---
## TDD With Embedded

- Pure logic: tests on the host
- Hardware-touching code: simulators or test fixtures
- Hardware-in-the-loop tests are slower
- Architecture: separate the algorithm from the hardware bindings
- Test the algorithm; integration-test the bindings

---
## TDD With Distributed Systems

- Per-service: TDD as usual
- Cross-service: contract tests
- Failure scenarios: chaos engineering tools
- E2E tests: few, focused on critical paths
- Don't try to E2E-test every interaction

---
## TDD Mindset Across Contexts

- Always: separate logic from I/O
- Logic is testable; I/O is integration
- The architectural pressure pays off
- Once you've TDD'd a system, it's natural
- The first project is hard; subsequent ones easier

---
## Common Context Mistakes

- Forcing TDD where it doesn't help (UI animation)
- Skipping TDD where it does (legacy bug fixes)
- "We can't TDD this" without trying
- Heavy-handed TDD that slows shipping
- Treating TDD as religion rather than tool
