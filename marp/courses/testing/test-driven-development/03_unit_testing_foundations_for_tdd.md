---
tags:
  - practices:tdd
  - practices:unit-testing
level: intermediate
category: testing
audience:
  - audiences:developers

---

# Unit Testing Foundations for TDD

---

## What This Chapter Covers

- Effective unit tests
- Arrange-Act-Assert
- Naming conventions
- Edge cases and boundary conditions
- Test independence and isolation
- Keeping tests fast and deterministic

---

## What Makes A Unit Test Good

- Tests *one* thing
- Fast (milliseconds)
- Independent of other tests
- Deterministic (same result every run)
- Clear when it fails (good name + clear assertion)
- Easy to read

---

## FIRST Principles

![test_fundamentals](svg/courses/testing/test-driven-development/03_unit_testing_foundations_for_tdd/test_fundamentals.svg)

---

## FIRST Expanded

![first_principles](svg/courses/testing/test-driven-development/03_unit_testing_foundations_for_tdd/first_principles.svg)

---

## Arrange-Act-Assert

```python
def test_user_promotion():
    # Arrange
    user = User(role='member')

    # Act
    user.promote()

    # Assert
    assert user.role == 'admin'
```

- Three sections, in order
- Each test follows the same structure
- A reader can scan for "what's being tested?"
- Spaces or comments separate the sections

---

## Arrange Act Assert Layout

![arrange_act_assert](svg/courses/testing/test-driven-development/03_unit_testing_foundations_for_tdd/arrange_act_assert.svg)

---

## Test Naming

- The test name should describe the behaviour
- Bad: `test_user`
- Better: `test_user_promote`
- Best: `test_promote_changes_role_to_admin`
- A descriptive name doubles as documentation

---

## Naming Conventions

- `test_<unit>_<scenario>_<expected>`
- Or: `test_<expected>_when_<scenario>`
- Or: `test_<unit>_should_<behaviour>`
- Pick one and stick with it
- Consistency aids navigation

---

## One Assertion Per Test

- A test should have one *concept* being verified
- Multiple assertions are fine if they verify the same concept
- Don't mix unrelated assertions in one test
- "If this test fails, what should I look at?" should have one answer
- Multiple tests > one mega-test

---

## Edge Cases

- Empty input
- Single element
- Maximum size
- Zero
- Negative
- Null / None
- Unicode / special characters
- Each is a potential test

---

## Boundary Conditions

- Just below the boundary
- At the boundary
- Just above the boundary
- "Off by one" lives here
- Test these explicitly

---

## Test Independence

- Tests should be runnable in any order
- Don't rely on other tests setting up state
- Don't share mutable state across tests
- Test runners often randomise order
- Failures should be reproducible in isolation

---

## Independence Pitfalls

![test_independence](svg/courses/testing/test-driven-development/03_unit_testing_foundations_for_tdd/test_independence.svg)

---

## Test Isolation

- Each test sets up what it needs
- Each test cleans up what it created
- Use setup/teardown methods if needed
- Or: per-test fixtures (preferred in modern frameworks)
- Tests that pollute the environment are flaky

---

## Setup and Teardown

```python
@pytest.fixture
def user():
    u = User.create()
    yield u
    u.delete()

def test_user_promotion(user):
    user.promote()
    assert user.role == 'admin'
```

- pytest fixtures: clean and composable
- JUnit `@BeforeEach`/`@AfterEach`: similar idea
- The cleanup runs even if the test fails

---

## Speed Matters

- A test suite that takes 30 seconds runs constantly
- A test suite that takes 30 minutes runs once a day
- Slow tests get skipped, then break
- Aim: < 1ms per unit test
- Keep slow tests in a separate (integration) suite

---

## What Slows Tests Down

- Database access
- File I/O
- Network calls
- Sleeping (`time.sleep`)
- Constructing large objects
- These belong in *integration* tests, not unit tests

---

## Determinism

- Same code, same input &#8594; same result, every run
- Avoid: random values, current time, network, file ordering
- Inject sources of variability so tests can control them
- Flaky tests are worse than no tests
- Track and fix; don't tolerate

---

## Test Patterns

- **AAA**: Arrange, Act, Assert
- **Given-When-Then**: same as AAA, BDD style
- **Spec**: tests grouped by behaviour, not by function
- **Property-based**: generate inputs, check invariants
- Pick what fits your team and codebase

---

## Reading Test Failures

- The error message should make the failure obvious
- "Expected 5, got 4" beats "AssertionError"
- Custom messages help: `assert x == y, f"expected {y}, got {x}"`
- Modern frameworks (pytest, JUnit 5) format these well by default
- Bad messages waste minutes per failure

---

## Common Foundation Mistakes

- Tests that depend on each other
- Tests that share global state
- Slow tests in the unit suite
- Vague test names ("test_1", "test_user")
- Multiple unrelated assertions per test
- Tests that always pass (assertions never run)
