# Exceptions

---
## What are Exceptions?
- Exceptions are errors that occur during program execution
- They interrupt the normal flow of the program
- Python uses exceptions extensively (EAFP style)

```python
print(1 / 0)
# ZeroDivisionError: division by zero

print(int("hello"))
# ValueError: invalid literal for int()
```

---
## EAFP vs LBYL
- **EAFP**: Easier to Ask Forgiveness than Permission
- **LBYL**: Look Before You Leap

```python
# LBYL style (less Pythonic)
if key in dictionary:
    value = dictionary[key]

# EAFP style (Pythonic)
try:
    value = dictionary[key]
except KeyError:
    value = default
```

---
## Common Built-in Exceptions
| Exception | Cause |
|-----------|-------|
| `TypeError` | Wrong type |
| `ValueError` | Wrong value |
| `KeyError` | Missing dict key |
| `IndexError` | Index out of range |
| `AttributeError` | Missing attribute |
| `FileNotFoundError` | File not found |
| `ZeroDivisionError` | Division by zero |
| `ImportError` | Failed import |
| `NameError` | Undefined variable |

---
## The `try`/`except` Statement

```python
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero!")
    result = 0

print(result)  # 0
```

---
## Catching the Exception Object

```python
try:
    value = int("hello")
except ValueError as e:
    print(f"Error: {e}")
    # Error: invalid literal for int() with base 10: 'hello'
    print(type(e))
    # <class 'ValueError'>
```

---
## Catching Multiple Exceptions

```python
try:
    data = {"key": "not_a_number"}
    value = int(data["key"])
except KeyError as e:
    print(f"Key not found: {e}")
except ValueError as e:
    print(f"Invalid value: {e}")
except (TypeError, AttributeError) as e:
    print(f"Type or attribute error: {e}")
```

---
## Catching All Exceptions

```python
try:
    result = risky_operation()
except Exception as e:
    print(f"Something went wrong: {e}")
```

- `except Exception` catches most exceptions
- `except BaseException` catches ALL (including `KeyboardInterrupt`)
- Avoid bare `except:` without a type
- Catching too broadly hides bugs

---
## The `else` Clause

```python
try:
    value = int(input("Enter a number: "))
except ValueError:
    print("That's not a valid number!")
else:
    # Only runs if NO exception occurred
    print(f"You entered: {value}")
    print(f"Doubled: {value * 2}")
```

- `else` executes only if `try` block succeeds
- Keeps the `try` block minimal

---
## The `finally` Clause

```python
try:
    f = open("data.txt")
    data = f.read()
except FileNotFoundError:
    print("File not found!")
finally:
    # ALWAYS runs, even if exception occurs
    print("Cleanup complete")
```

- `finally` runs regardless of exception
- Used for cleanup (closing files, connections, etc.)

---
## `try`/`except`/`else`/`finally`

```python
try:
    result = 10 / 2
except ZeroDivisionError:
    print("Division by zero!")
else:
    print(f"Result: {result}")  # Runs on success
finally:
    print("Done!")              # Always runs
```

```output
Result: 5.0
Done!
```

---
## Raising Exceptions

```python
def set_age(age):
    if not isinstance(age, int):
        raise TypeError("Age must be an integer")
    if age < 0:
        raise ValueError("Age must be non-negative")
    return age

try:
    set_age(-5)
except ValueError as e:
    print(e)  # Age must be non-negative
```

---
## Re-raising Exceptions

```python
import logging

def process_data(data):
    try:
        result = complex_operation(data)
    except Exception as e:
        logging.error(f"Failed to process: {e}")
        raise  # Re-raise the same exception
```

- Use bare `raise` to re-raise the current exception
- Preserves the original traceback

---
## Exception Chaining

```python
def load_config(path):
    try:
        with open(path) as f:
            return f.read()
    except FileNotFoundError as e:
        raise RuntimeError(f"Config not found: {path}") from e

try:
    load_config("missing.conf")
except RuntimeError as e:
    print(e)
    print(f"Caused by: {e.__cause__}")
```

- `raise ... from ...` chains exceptions
- Original exception is preserved as `__cause__`

---
## Custom Exceptions

```python
class AppError(Exception):
    """Base exception for our application."""
    pass

class ValidationError(AppError):
    """Raised when validation fails."""
    pass

class NotFoundError(AppError):
    """Raised when a resource is not found."""
    pass

try:
    raise ValidationError("Email is invalid")
except AppError as e:
    print(f"App error: {e}")
```

---
## Custom Exceptions with Data

```python
class HttpError(Exception):
    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message
        super().__init__(f"{status_code}: {message}")

try:
    raise HttpError(404, "Page not found")
except HttpError as e:
    print(e.status_code)  # 404
    print(e.message)      # Page not found
    print(e)              # 404: Page not found
```

---
## Exception Hierarchy

![exception_hierarchy](svg/courses/languages/python/python-programming/09_exceptions/exception_hierarchy.svg)

---

## Exception Hierarchy Detail

```tree
BaseException
  +-- SystemExit
  +-- KeyboardInterrupt
  +-- GeneratorExit
  +-- Exception
       +-- ArithmeticError
       |    +-- ZeroDivisionError
       +-- LookupError
       |    +-- IndexError
       |    +-- KeyError
       +-- OSError
       |    +-- FileNotFoundError
       +-- TypeError
       +-- ValueError
       +-- RuntimeError
       +-- StopIteration
```

---
## `BaseException` vs `Exception`
- `BaseException`: Root of all exceptions
- `Exception`: Base for most user-catchable exceptions
- `KeyboardInterrupt`, `SystemExit`: Not subclasses of `Exception`

```python
try:
    while True:
        pass
except Exception:
    # Does NOT catch Ctrl+C
    pass
except KeyboardInterrupt:
    # This catches Ctrl+C
    print("Interrupted!")
```

---
## Exception Groups (Python 3.11+)

```python
def process_items(items):
    errors = []
    for item in items:
        try:
            validate(item)
        except ValueError as e:
            errors.append(e)
    if errors:
        raise ExceptionGroup("Validation failed", errors)

try:
    process_items(["a", "b", "c"])
except* ValueError as eg:
    for e in eg.exceptions:
        print(f"Error: {e}")
```

---
## Context Managers and Exceptions

```python
# with statement handles cleanup automatically
with open("data.txt") as f:
    data = f.read()
# File is closed even if an exception occurs

# Equivalent to:
f = open("data.txt")
try:
    data = f.read()
finally:
    f.close()
```

---
## Suppressing Exceptions

```python
from contextlib import suppress

# Instead of try/except/pass
try:
    os.remove("temp.txt")
except FileNotFoundError:
    pass

# Use suppress
with suppress(FileNotFoundError):
    os.remove("temp.txt")
```

---
## Traceback Information

```python
import traceback

try:
    1 / 0
except ZeroDivisionError:
    traceback.print_exc()
    # Prints the full traceback

    tb_str = traceback.format_exc()
    # Get traceback as string
```

---
## Accessing Traceback Programmatically

```python
import sys

try:
    1 / 0
except ZeroDivisionError:
    exc_type, exc_value, exc_tb = sys.exc_info()
    print(f"Type: {exc_type}")
    print(f"Value: {exc_value}")
    print(f"Traceback: {exc_tb}")
```

---
## Warnings vs Exceptions

```python
import warnings

def deprecated_function():
    warnings.warn(
        "This function is deprecated",
        DeprecationWarning,
        stacklevel=2,
    )
    return "result"

result = deprecated_function()
# Warning is shown but execution continues
```

---
## Best Practices - Be Specific

```python
# BAD: catches everything
try:
    value = data[key]
except:
    value = default

# GOOD: catch specific exception
try:
    value = data[key]
except KeyError:
    value = default
```

---
## Best Practices - Keep `try` Blocks Small

```python
# BAD: too much in try block
try:
    data = load_file(path)
    parsed = parse_data(data)
    result = process(parsed)
    save(result)
except Exception as e:
    print(f"Error: {e}")

# GOOD: minimal try block
data = load_file(path)
try:
    parsed = parse_data(data)
except ValueError as e:
    print(f"Parse error: {e}")
else:
    result = process(parsed)
    save(result)
```

---
## Best Practices - Don't Silence Exceptions

```python
# BAD: swallowing exceptions
try:
    do_something()
except Exception:
    pass

# GOOD: at minimum, log the error
try:
    do_something()
except Exception as e:
    logging.error(f"Operation failed: {e}")
```

---
## Best Practices - Use Custom Exceptions

```python
# BAD: using generic exceptions
def validate(data):
    if not data:
        raise Exception("Data is empty")

# GOOD: use custom exceptions
class EmptyDataError(ValueError):
    pass

def validate(data):
    if not data:
        raise EmptyDataError("Data is empty")
```

---
## Common Patterns - Retry Logic

```python
import time

def retry(func, max_attempts=3, delay=1):
    for attempt in range(max_attempts):
        try:
            return func()
        except Exception as e:
            if attempt == max_attempts - 1:
                raise
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(delay)
```

---
## Common Patterns - Default Values

```python
def safe_get(dictionary, key, default=None):
    try:
        return dictionary[key]
    except KeyError:
        return default

def safe_int(value, default=0):
    try:
        return int(value)
    except (ValueError, TypeError):
        return default

print(safe_int("42"))       # 42
print(safe_int("hello"))    # 0
print(safe_int(None, -1))   # -1
```

---
## `assert` Statement

```python
def calculate_average(numbers):
    assert len(numbers) > 0, "List must not be empty"
    return sum(numbers) / len(numbers)

# Works
print(calculate_average([1, 2, 3]))  # 2.0

# Fails
# calculate_average([])  # AssertionError: List must not be empty
```

- Use for debugging and internal checks
- Disabled with `python -O` (optimized mode)
- Never use for input validation

---
## Summary
- Exceptions interrupt normal flow; `try`/`except` handles them
- Catch specific exceptions, not broad ones
- `else` runs on success; `finally` always runs
- `raise` to throw exceptions; `raise ... from ...` to chain
- Create custom exception hierarchies for your application
- Use context managers (`with`) for automatic cleanup
- Follow EAFP style (Easier to Ask Forgiveness than Permission)
