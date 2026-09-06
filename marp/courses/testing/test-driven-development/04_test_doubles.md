---
tags:
  - practices:tdd
  - practices:test-doubles
level: intermediate
category: testing
audience:
  - audiences:developers

---

# Test Doubles

---

## Four Flavors

![test_doubles](svg/courses/testing/test-driven-development/04_test_doubles/test_doubles.svg)

---

## What This Chapter Covers

- Types of test doubles: dummy, stub, spy, mock, fake
- When to use each
- Hand-rolled vs framework-generated
- Testing interactions vs state
- Over-mocking
- Choosing the right double

---

## What A Test Double Is

- A stand-in for a real collaborator
- Lets you test a unit in isolation
- Decouples test from external systems
- Coined by Gerard Meszaros (xUnit Test Patterns)
- Five types, each with a specific role

---

## Dummy

- Passed but never used
- Just satisfies a method signature
- Often `null` or a placeholder
- Cheap; no behaviour
- Example: a logger argument the test doesn't care about

---

## Stub

- Returns canned answers
- Doesn't verify *how* it's called
- Used to control what the unit under test sees
- "When asked, return X"
- Most-common test double

---

## Stub Example

```python
class StubRepo:
    def __init__(self, returns):
        self._returns = returns
    def get(self, id):
        return self._returns

def test_processes_user():
    repo = StubRepo(returns=User(id=1, name='Alice'))
    service = UserService(repo)
    result = service.greet(1)
    assert result == 'Hello, Alice'
```

---

## Spy

- Records what was called
- Test asserts on the recorded calls
- Like a stub but also remembers
- Useful when you care about side effects
- "Was this method called with the right args?"

---

## Spy Example

```python
class SpyEmailer:
    def __init__(self):
        self.sent = []
    def send(self, to, subject, body):
        self.sent.append((to, subject, body))

def test_signup_sends_welcome():
    emailer = SpyEmailer()
    service = SignupService(emailer)
    service.signup('a@b.com')
    assert ('a@b.com', 'Welcome', ANY) in emailer.sent
```

---

## Mock

- Pre-programmed expectations
- Verifies that specific calls happened
- Often via a mocking framework (Mockito, unittest.mock)
- Combines stub + spy + verification
- Most common in OO codebases

---

## Mock Example

```python
from unittest.mock import Mock

def test_signup_sends_welcome():
    emailer = Mock()
    service = SignupService(emailer)
    service.signup('a@b.com')
    emailer.send.assert_called_once_with('a@b.com', 'Welcome', ANY)
```

- Less code than a hand-rolled spy
- Verification syntax is framework-specific

---

## Fake

- A working implementation, simplified
- Examples: in-memory database, in-memory file system
- Behaves like the real thing for the tested operations
- Faster than the real thing
- Reused across many tests

---

## Fake Example

```python
class FakeRepo:
    def __init__(self):
        self._users = {}
    def save(self, u): self._users[u.id] = u
    def get(self, id): return self._users.get(id)
```

- A real, working repository — just in-memory
- Many tests can share it
- More confidence than mocks (real behaviour)

---

## When To Use Each

- **Dummy**: argument required but unused
- **Stub**: you need a value the unit will read
- **Spy**: you need to verify a call but care about state too
- **Mock**: you need to verify interactions
- **Fake**: you need realistic behaviour without external dependencies

---

## Testing State vs Interactions

- **State testing**: assert the resulting state of the unit
- **Interaction testing**: assert what calls were made
- State is more durable; refactors don't break it
- Interaction is more precise; refactors often break it
- Prefer state when you can

---

## When Interaction Testing Wins

- Testing side effects (sent an email, wrote a log)
- The call *is* the observable behaviour
- No state change to assert on
- Calls to external systems
- Use sparingly; over-mocking ties tests to implementation

---

## Hand-Rolled vs Framework Mocks

- Hand-rolled: explicit class, more code, more control
- Framework: less code, more magic
- For complex behaviour: hand-rolled
- For simple stubs/mocks: framework
- A mix in most codebases

---

## Over-Mocking

- Every collaborator mocked
- Tests pass even when the real implementation breaks
- Refactors break dozens of tests
- Tests become a maintenance burden
- Use real objects where they're cheap; mock the slow / external

---

## Mockist vs Classicist

- **Mockist** (London school): mock all collaborators; test in pure isolation
- **Classicist** (Detroit/Chicago school): use real objects where practical
- Both have merit; mostly a personal preference
- Classicist tests often have lower maintenance
- Choose a school; apply consistently

---

## Common Test Double Mistakes

- Mocking everything; not testing the unit
- Mocks that diverge from the real interface
- Verifying a long sequence of calls (brittle)
- Not using fakes for in-memory equivalents
- Confusing one type with another (call a stub a mock)
