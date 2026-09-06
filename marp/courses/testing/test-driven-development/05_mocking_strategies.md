---
tags:
  - practices:tdd
  - practices:mocking
level: intermediate
category: testing
audience:
  - audiences:developers

---

# Mocking Strategies

---

## When to Mock

![mocking_strategies](svg/courses/testing/test-driven-development/05_mocking_strategies/mocking_strategies.svg)

---

## What This Chapter Covers

- Mocking frameworks
- Setting up expectations and return values
- Verifying interactions and call counts
- Partial mocking and spies
- Mocking external dependencies
- Mocking time, randomness, and environment

---

## Mock Stub Fake Spy

![mock_vs_stub](svg/courses/testing/test-driven-development/05_mocking_strategies/mock_vs_stub.svg)

---

## Mocking Frameworks

- **Java**: Mockito, EasyMock, JMockit
- **Python**: unittest.mock, MagicMock
- **JavaScript**: Jest mocks, Sinon.JS
- **C#**: Moq, NSubstitute, FakeItEasy
- **Ruby**: RSpec mocks, mocha
- All similar; learn one, others are easy

---

## Mockito (Java)

```java
EmailService email = mock(EmailService.class);
when(email.send(anyString(), eq("Welcome"))).thenReturn(true);

new SignupService(email).signup("a@b.com");

verify(email).send("a@b.com", "Welcome");
```

- `when().thenReturn()`: stub
- `verify()`: assert the call happened

---

## unittest.mock (Python)

```python
from unittest.mock import Mock, patch

@patch('module.requests.get')
def test_fetches_user(mock_get):
    mock_get.return_value.json.return_value = {'id': 42}
    user = fetch_user(42)
    assert user.id == 42
    mock_get.assert_called_once_with('https://api/users/42')
```

- `@patch` swaps a name in another module
- `return_value` chains for fluent calls

---

## Jest (JavaScript)

```javascript
const send = jest.fn(() => true);
const service = new SignupService({ send });

service.signup('a@b.com');

expect(send).toHaveBeenCalledWith('a@b.com', 'Welcome');
```

- `jest.fn()` creates a mock function
- Tracks calls automatically
- Built into Jest

---

## Sinon (JavaScript)

```javascript
const stub = sinon.stub();
stub.withArgs('a@b.com').returns(true);

stub('a@b.com');           // returns true
sinon.assert.calledOnce(stub);
```

- For projects not on Jest
- Spies, stubs, mocks all separate
- Common in older JS codebases

---

## Setting Up Expectations

- "When this method is called with X, return Y"
- For complex stubs: matchers (`anyString`, `eq`, custom)
- Set up only what the test exercises
- Over-stubbing makes tests brittle
- Each `when` should have a reason

---

## Argument Matchers

- `anyString()`, `anyInt()`, etc.
- `eq(value)`: exact match
- Custom matchers for complex args
- Don't overuse `any` — you lose precision
- A specific matcher catches more bugs

---

## Verifying Calls

- `verify(mock).method(args)`: did it happen?
- `verify(mock, times(2)).method(args)`: how many times?
- `verify(mock, never()).method(args)`: didn't happen?
- `inOrder(mock).method(...)`: ordered verification
- More precision = more brittleness

---

## Partial Mocking

- Mock some methods of a real object
- Sometimes called a "spy" in mock-framework terms
- Useful when most of the object's behaviour is fine but one method needs control
- Smell: usually means the design needs work
- Use sparingly

---

## Mocking External Dependencies

- HTTP clients
- Database connections
- File systems
- Cloud SDKs (S3, SQS, etc.)
- Inject the dependency; mock it in tests

---

## Mocking HTTP

```python
@patch('requests.get')
def test_fetch_handles_500(mock_get):
    mock_get.return_value.status_code = 500
    with pytest.raises(ServerError):
        fetch_user(42)
```

- Saves real HTTP calls in unit tests
- Tests can simulate any response
- Pair with integration tests against a real server

---

## Mocking Time

- `freezegun` (Python), `Sinon.useFakeTimers()` (JS), `Clock` (Java)
- Pin "now" to a fixed timestamp
- Test time-dependent code without flakiness
- Avoid `sleep` in tests
- Inject a clock object for real flexibility

---

## Mocking Randomness

- Seed your random source (`random.seed(42)`)
- Or inject a random number generator
- Tests become deterministic
- Without it: occasional failures that disappear on retry
- Same approach as time

---

## Mocking Environment

- `os.environ` patches in Python
- Constructor injection of config objects
- Don't read env in production code; pass config
- Easier to test; cleaner code
- The Twelve-Factor App approach

---

## Mock Boundaries

- Mock at the *seam* of your code
- Don't mock standard library functions you trust
- Don't mock the language itself
- Real objects for value types, simple data, pure functions
- Mocks for: I/O, time, randomness, external services

---

## Auto-Spec / Strict Mocks

- `unittest.mock.create_autospec`: matches the real object's interface
- Catches typos: `mock.send_emial(...)` raises (not silent passing)
- Strict mocks fail on unexpected calls
- Use these to keep mocks honest as the real interface evolves

---

## Common Mocking Mistakes

- Mocking everything; not testing real logic
- Stubs that don't match the real interface (drift)
- Verifying too much (every call's args)
- Mocking standard library or framework calls
- Not testing the integration where mocks meet the real world
