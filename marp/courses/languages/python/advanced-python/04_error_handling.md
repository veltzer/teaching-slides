---
tags:
  - languages:python
level: advanced
category: language
audience:
  - audiences:developers

---
# Advanced Error Handling in Python

## Overview
- Building robust Python applications
- Correct exception handling patterns
- Creating custom exception hierarchies
- Using the `raise from` syntax
- Assertions and their proper use
- Best practices for error handling

---

## Python Exception Hierarchy

![Python Exception Hierarchy](svg/courses/languages/python/advanced-python/04_error_handling/exception_hierarchy.svg)

---

## Python's Exception Philosophy: The EAFP Principle

- "Easier to Ask Forgiveness than Permission"
- A core Python programming principle
- Prefer try/except over if-checking
- Cleaner, more readable code in most cases
- More efficient in many scenarios

```python
# Non-Pythonic (LBYL - Look Before You Leap)
if "key" in my_dict:
    value = my_dict["key"]
else:
    value = default

# Pythonic (EAFP)
try:
    value = my_dict["key"]
except KeyError:
    value = default
```

---

## Python's Exception Philosophy: Why EAFP is Preferred

- Avoids race conditions
- One-step instead of two-step process
- More readable in complex conditions
- Better performance in the common case
- Handles exceptional cases where they occur

---

## Exception Basics Review: Exception Types

- Python has a rich hierarchy of built-in exceptions
- All exceptions inherit from `BaseException`
- Most custom exceptions inherit from `Exception`
- System exit signals use specialized exceptions

```tree
BaseException
 ├── SystemExit
 ├── KeyboardInterrupt
 ├── GeneratorExit
 └── Exception  # Parent for most custom exceptions
      ├── StopIteration
      ├── ArithmeticError
      │    ├── FloatingPointError
      │    ├── OverflowError
      │    └── ZeroDivisionError
      ├── AttributeError
      ├── ImportError
      ├── LookupError
      │    ├── IndexError
      │    └── KeyError
      └── ... (many more)
```

---

## Exception Basics Review: Try-Except Block Structure

- Standard exception handling structure
- Can include `except`, `else`, and `finally` clauses
- Handle specific exceptions with type matching
- Access exception info with the `as` keyword

```python
try:
    # Code that might raise an exception
    result = risky_operation()
except ValueError as e:
    # Handle a specific exception
    print(f"Invalid value: {e}")
except (TypeError, KeyError) as e:
    # Handle multiple exception types
    print(f"Type or key error: {e}")
except Exception as e:
    # Catch-all for other exceptions
    print(f"Unexpected error: {e}")
    raise  # Re-raise the caught exception
else:
    # Executes if no exception was raised
    process_result(result)
finally:
    # Always executes, regardless of exception
    cleanup_resources()
```

---

## Correct Exception Handling: Be Specific About Exceptions

- Catch only exceptions you can handle
- Avoid bare `except:` clauses
- Target specific exception types
- Handle each exception appropriately

```python
# Bad - Catches everything, even KeyboardInterrupt
try:
    do_something()
except:
    handle_error()

# Good - Specific exception handling
try:
    do_something()
except ValueError as e:
    handle_value_error(e)
except IOError as e:
    handle_io_error(e)
```

---

## Correct Exception Handling: The Exception Hierarchy Advantage

- Catch specific exceptions when you need detailed handling
- Catch parent classes for common handling
- Use hierarchy to simplify error handling

```python
# Handling specific arithmetic errors
try:
    result = complex_calculation()
except ZeroDivisionError:
    print("Cannot divide by zero")
except OverflowError:
    print("Number too large")
except ArithmeticError:  # Catches all arithmetic errors
    print("Calculation error")
```

---

## Correct Exception Handling: Keep Try Blocks Focused

- Include only code that might raise the target exception
- Move non-error-prone code to the `else` block
- Helps identify exactly what failed
- Reduces indentation and improves readability

```python
# Less focused - mixing error-prone and regular code
try:
    data = fetch_data(url)
    process_data(data)  # This might fail separately
    save_results(data)  # This might also fail
except RequestException:
    handle_fetch_error()

# More focused - clear separation
try:
    data = fetch_data(url)
except RequestException:
    handle_fetch_error()
else:
    # Only runs if fetch_data succeeds
    process_data(data)
    save_results(data)
```

---

## Correct Exception Handling: Using the Finally Block

- Guarantees execution of cleanup code
- Runs whether exception occurs or not
- Even runs when `return`, `break`, or `continue` occurs
- Perfect for resource cleanup

```python
def read_file_content(filename):
    f = None
    try:
        f = open(filename, 'r')
        return f.read()
    except FileNotFoundError:
        print(f"File not found: {filename}")
        return None
    finally:
        # Always close the file, even if returning early
        if f:
            f.close()
```

---

## Correct Exception Handling: Context Managers (with statement)

- Elegant pattern for resource management
- Automatic cleanup even during exceptions
- Handles both normal and error cases
- Simplifies code and reduces bugs

```python
# Without context manager
f = open('file.txt', 'w')
try:
    f.write('Hello world')
finally:
    f.close()

# With context manager
with open('file.txt', 'w') as f:
    f.write('Hello world')
# File is automatically closed
```

---

## Correct Exception Handling: Re-raising Exceptions

- Process exception but still propagate it
- Preserves original traceback
- Can be used for logging or partial recovery

```python
try:
    authenticate_user(username, password)
except AuthenticationError as e:
    # Log the error but still raise it
    logger.error(f"Authentication failed: {e}")
    raise  # Re-raises the original exception
```

---

## The raise from Syntax: Exception Chaining

- Added in Python 3
- Explicitly chain exceptions
- Shows causal relationship between exceptions
- Preserves complete error context

```python
try:
    int("not a number")
except ValueError as e:
    # Chain a new exception with the original cause
    raise RuntimeError("Processing failed") from e

# Traceback will show both exceptions:
# RuntimeError: Processing failed
# The above exception was caused by:
# ValueError: invalid literal for int() with base 10: 'not a number'
```

---

## The raise from Syntax: Why Use Exception Chaining

- Provides better context for debugging
- Maintains both high-level and low-level error info
- Adds meaning to technical exceptions
- Creates clearer error narratives

```python
def get_user_by_id(user_id):
    try:
        return database.query(f"SELECT * FROM users WHERE id = {user_id}")
    except DatabaseError as e:
        raise UserNotFoundError(f"User {user_id} not found") from e
```

---

## The raise from Syntax: Suppressing Chained Exceptions

- Use `raise ... from None` to suppress the original
- Useful when original exception is not relevant
- Simplifies error reporting
- Avoids confusion with technical details

```python
try:
    config = load_config_file('config.json')
except (FileNotFoundError, JSONDecodeError) as e:
    # Hide the original exception, just use a clean message
    raise ConfigurationError("Invalid configuration") from None
```

---

## Writing Custom Exceptions: Creating Basic Exceptions

- Inherit from Exception class
- Add custom attributes and methods
- Provide meaningful error messages
- Support better error handling

```python
class ValidationError(Exception):
    """Exception raised for validation errors."""

    def __init__(self, message, field=None):
        self.message = message
        self.field = field
        super().__init__(self.message)

    def __str__(self):
        if self.field:
            return f"{self.field}: {self.message}"
        return self.message

# Usage
raise ValidationError("Value must be positive", "amount")
```

---

## Writing Custom Exceptions: Building Exception Hierarchies

- Create base exception for your module/application
- Define specific exceptions for different error types
- Establish meaningful relationships between exceptions
- Enable more flexible handling

```python
class DatabaseError(Exception):
    """Base class for database-related exceptions."""
    pass

class ConnectionError(DatabaseError):
    """Failed to connect to the database."""
    pass

class QueryError(DatabaseError):
    """Error executing a database query."""
    def __init__(self, message, query=None):
        self.query = query
        super().__init__(message)
```

---

## Writing Custom Exceptions: Adding Contextual Information

- Include relevant data in exception objects
- Helps with debugging and error handling
- Makes exceptions more informative
- Avoids losing important context

```python
class APIError(Exception):
    """Exception raised for API errors."""

    def __init__(self, message, status_code=None, response=None):
        self.status_code = status_code
        self.response = response
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        base_msg = self.message
        if self.status_code:
            base_msg += f" (Status code: {self.status_code})"
        return base_msg
```

---

## Writing Custom Exceptions: Exception Best Practices

- Make exception names descriptive and specific
- End class names with "Error" or "Exception"
- Document exceptions in function docstrings
- Keep exception hierarchies shallow
- Balance specificity with usability

```python
def transfer_funds(source_account, dest_account, amount):
    """Transfer funds between accounts.

    Args:
        source_account: Source account number
        dest_account: Destination account number
        amount: Amount to transfer

    Raises:
        InsufficientFundsError: If source account lacks funds
        AccountNotFoundError: If either account doesn't exist
        TransferLimitExceededError: If transfer exceeds daily limit
    """
    # Implementation...
```

---

## Advanced Exception Techniques: Exception Handling with Decorators

- Centralize error handling logic
- Apply consistent handling to multiple functions
- Separate business logic from error handling
- Reduce code duplication

```python
import functools

def handle_exceptions(func):
    """Decorator to handle and log exceptions."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            logger.warning(f"Invalid value in {func.__name__}: {e}")
            return None
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {e}")
            raise ApplicationError(f"Error in {func.__name__}") from e
    return wrapper

@handle_exceptions
def process_data(data):
    # Function without try/except boilerplate
    return transform(validate(data))
```

---

## Advanced Exception Techniques: Retry Pattern

- Automatically retry failed operations
- Perfect for transient errors (network, etc.)
- Implement backoff strategies for reliability
- Can be implemented as a decorator

```python
def retry(max_attempts=3, delay=1, backoff=2, exceptions=(Exception,)):
    """Retry decorator with exponential backoff."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            current_delay = delay

            while attempt < max_attempts:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    attempt += 1
                    if attempt == max_attempts:
                        raise

                    logger.warning(
                        f"Attempt {attempt} failed: {e}. "
                        f"Retrying in {current_delay}s..."
                    )

                    time.sleep(current_delay)
                    current_delay *= backoff
        return wrapper
    return decorator

@retry(max_attempts=3, exceptions=(ConnectionError, TimeoutError))
def fetch_data(url):
    return requests.get(url).json()
```

---

## Advanced Exception Techniques: Contextlib for Custom Context Managers

- `contextlib.contextmanager` simplifies context manager creation
- Turn generator functions into context managers
- Cleaner than implementing `__enter__` and `__exit__`
- Great for resource management

```python
from contextlib import contextmanager

@contextmanager
def transaction(session):
    """Handle database transaction with automatic rollback on error."""
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

# Usage
with transaction(Session()) as session:
    user = User(username="alice")
    session.add(user)
# Transaction is committed if no error occurred
# Or rolled back if an exception was raised
```

---

## Advanced Exception Techniques: Nested Exception Handling

- Structure complex error handling with nested blocks
- Handle different levels of abstraction
- Maintain error context at each level
- Add specific handling at appropriate levels

```python
def process_user_data(user_id):
    try:
        try:
            raw_data = fetch_user_data(user_id)
        except ConnectionError as e:
            logger.error(f"Connection failed: {e}")
            raise DataFetchError("Could not connect to data source") from e

        try:
            processed_data = transform_data(raw_data)
        except ValueError as e:
            logger.error(f"Invalid data format: {e}")
            raise DataProcessingError("Could not process user data") from e

        return processed_data

    except (DataFetchError, DataProcessingError) as e:
        # High-level handling for both error types
        notify_admin(f"User data processing failed: {e}")
        return None
```

---

## Assertions in Python: Purpose of Assertions

- Verify program correctness during development
- Document assumptions in code
- Catch programming errors early
- Not for handling runtime errors
- Can be disabled in production (with -O flag)

```python
def calculate_average(numbers):
    # Verify input is non-empty
    assert len(numbers) > 0, "Cannot calculate average of empty list"

    total = sum(numbers)
    return total / len(numbers)
```

---

## Assertions in Python: When to Use Assertions

- Checking internal invariants
- Verifying preconditions in non-public methods
- Documenting assumptions in your code
- Detecting impossible situations
- During testing and debugging

```python
def binary_search(sorted_list, item):
    # Internal invariant: list must be sorted
    assert all(sorted_list[i] <= sorted_list[i+1]
              for i in range(len(sorted_list)-1)), "List must be sorted"

    # Binary search implementation...
```

---

## Assertions in Python: When Not to Use Assertions

- Validating user input
- Checking for runtime errors
- Handling expected error conditions
- Public API validation
- Any case that should work in production

```python
# Bad - assertion might be disabled in production
def process_user_data(data):
    assert data is not None, "Data cannot be None"
    # Process data...

# Good - explicit exception always runs
def process_user_data(data):
    if data is None:
        raise ValueError("Data cannot be None")
    # Process data...
```

---

## Assertions in Python: Assertions vs. Exceptions

- Assertions are for developer errors
- Exceptions are for runtime errors
- Assertions can be disabled
- Exceptions are always active
- Use each for the appropriate purpose

```python
# Assertion for code correctness (developer error)
def calculate_discount(price, rate):
    assert 0 <= rate <= 1, "Discount rate must be between 0 and 1"
    return price * (1 - rate)

# Exception for runtime error
def divide_values(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
```

---

## Debugging with Exceptions: Understanding Tracebacks

- Python's traceback shows exception path
- Read from bottom to top for chronology
- Contains function calls, file names, line numbers
- Helps locate the source of the error

```output
Traceback (most recent call last):
  File "main.py", line 10, in <module>
    result = process_data(raw_data)
  File "main.py", line 5, in process_data
    return transform(data)
  File "utils.py", line 15, in transform
    return data['key'] * 2
KeyError: 'key'
```

---

## Debugging with Exceptions: Enhancing Tracebacks

- Add context to exceptions with `raise from`
- Use custom exceptions with descriptive messages
- Include relevant data in exception objects
- Consider using traceback enhancement libraries

```python
import traceback

try:
    process_data()
except Exception as e:
    print("An error occurred:")
    print(traceback.format_exc())  # Print full traceback

    # Enhanced information
    print(f"Error type: {type(e).__name__}")
    print(f"Error details: {e}")

    # Additional context if available
    if hasattr(e, 'status_code'):
        print(f"Status code: {e.status_code}")
```

---

## Debugging with Exceptions: The traceback Module

- Programmatically work with tracebacks
- Extract, format, and print exception information
- Capture tracebacks for logging
- Control level of detail

```python
import traceback
import logging

try:
    complex_operation()
except Exception as e:
    # Get formatted traceback as a string
    tb_str = traceback.format_exc()

    # Log the full traceback
    logging.error(f"Operation failed: {e}\n{tb_str}")

    # For user display, show simplified message
    print(f"Sorry, an error occurred: {e}")
```

---

## Exception Handling Patterns: The Guard Pattern

- Protect non-critical functionality
- Prevent exceptions from non-essential features
- Keep main program running despite errors
- Useful for plugins, extensions, or optional features

```python
def apply_plugins(data):
    """Apply all plugins to data, ignoring any that fail."""
    result = data.copy()

    for plugin in get_plugins():
        try:
            result = plugin.process(result)
        except Exception as e:
            logger.warning(f"Plugin {plugin.name} failed: {e}")
            # Continue with other plugins

    return result
```

---

## Exception Handling Patterns: The Circuit Breaker Pattern

- Prevent repeated calls to failing systems
- Automatically "trip" after consecutive failures
- Allow occasional retry attempts
- Reset after successful operation

```python
class CircuitBreaker:
    def __init__(self, failure_threshold=5, reset_timeout=60):
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.reset_timeout = reset_timeout
        self.last_failure_time = 0
        self.is_open = False
```

---

## Circuit Breaker: The `__call__` Wrapper

```python
    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if self.is_open:
                # Check if circuit should attempt reset
                if time.time() - self.last_failure_time > self.reset_timeout:
                    self.is_open = False
                    self.failure_count = 0
                else:
                    raise CircuitBreakerOpenError(
                        f"Circuit breaker is open for {func.__name__}"
                    )

            try:
                result = func(*args, **kwargs)
                # Success, reset failure count
                self.failure_count = 0
                return result
            except Exception as e:
                # Failure, increment count
                self.failure_count += 1
                self.last_failure_time = time.time()

                if self.failure_count >= self.failure_threshold:
                    self.is_open = True

                raise

        return wrapper
```

---

## Exception Handling Patterns: The Bubble-Up Pattern

- Handle exceptions at the appropriate level
- Let exceptions bubble up to where they can be handled
- Avoid premature exception catching
- Handle exceptions where you have the context to do so

```python
# Low level function - passes exceptions up
def fetch_data(url):
    # No try/except here - let caller handle network issues
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

# Mid level function - handles specific exceptions
def get_user_data(user_id):
    try:
        return fetch_data(f"/api/users/{user_id}")
    except requests.HTTPError as e:
        if e.response.status_code == 404:
            raise UserNotFoundError(f"User {user_id} not found") from e
        raise APIError("Failed to get user data") from e

# High level function - handles application flow
def display_user_profile(user_id):
    try:
        user_data = get_user_data(user_id)
        render_profile_page(user_data)
    except UserNotFoundError:
        render_not_found_page()
    except APIError as e:
        log_error(e)
        render_error_page("Sorry, we couldn't load the profile")
```

---

## Exception Handling Patterns: The Unified Handler Pattern

- Central exception handling for an application
- Consistent error reporting and logging
- Simplifies individual functions
- Good for web applications and services

```python
def exception_handler(func):
    """Global exception handler for application."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            logger.warning(f"Value error: {e}")
            return {"status": "error", "message": str(e), "code": 400}
        except ValidationError as e:
            logger.info(f"Validation error: {e}")
            return {"status": "error", "message": str(e), "code": 400}
        except AuthenticationError as e:
            logger.warning(f"Auth error: {e}")
            return {"status": "error", "message": "Authentication failed", "code": 401}
        except Exception as e:
            # Unexpected error
            incident_id = log_incident(e)
            logger.error(f"Unexpected error ({incident_id}): {e}")
            return {
                "status": "error",
                "message": "An unexpected error occurred",
                "code": 500,
                "incident_id": incident_id
            }
    return wrapper

@exception_handler
def api_endpoint(request):
    # Function can focus on business logic without error handling
    validate_request(request)
    data = process_request(request)
    return {"status": "success", "data": data}
```

---

## Real-World Example: API Client

## Complete Error Handling Example: Exception Hierarchy
```python
class APIError(Exception):
    """Base exception for API errors."""
    pass

class ConnectionError(APIError):
    """Failed to connect to the API."""
    pass

class AuthenticationError(APIError):
    """Authentication with the API failed."""
    pass

class NotFoundError(APIError):
    """Requested resource not found."""
    pass
```

---

## API Client: Class Setup

```python
class APIClient:
    def __init__(self, base_url, api_key=None):
        self.base_url = base_url
        self.api_key = api_key
        self.session = requests.Session()

    def _request(self, method, endpoint, **kwargs):
        """Make a request to the API with error handling."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        headers = kwargs.pop('headers', {})

        if self.api_key:
            headers['Authorization'] = f"Bearer {self.api_key}"
```

---

## API Client: Request and HTTP Error Handling

```python
        try:
            response = self.session.request(
                method, url, headers=headers, **kwargs
            )

            # Handle HTTP errors
            try:
                response.raise_for_status()
            except requests.HTTPError as e:
                if response.status_code == 401:
                    raise AuthenticationError("API key invalid or expired") from e
                elif response.status_code == 404:
                    raise NotFoundError(f"Resource not found: {endpoint}") from e
                else:
                    # Try to get error details from JSON response
                    try:
                        error_detail = response.json().get('message', str(e))
                    except ValueError:
                        error_detail = str(e)

                    raise APIError(f"API error ({response.status_code}): {error_detail}") from e
```

---

## API Client: JSON Parse and Connection Handling

```python
            # Parse JSON response
            try:
                return response.json()
            except ValueError as e:
                raise APIError("Invalid JSON response from API") from e

        except requests.ConnectionError as e:
            raise ConnectionError(f"Failed to connect to API: {e}") from e
        except requests.Timeout as e:
            raise ConnectionError(f"API request timed out: {e}") from e

    def get_resource(self, resource_id):
        """Get a resource from the API."""
        try:
            return self._request('GET', f"/resources/{resource_id}")
        except NotFoundError as e:
            # Convert to more specific error
            raise ResourceNotFoundError(f"Resource {resource_id} not found") from e
```

---

## Summary

## Key Takeaways
- Handle exceptions at the appropriate level
- Create meaningful exception hierarchies
- Use `raise from` to maintain context
- Use assertions to verify program correctness
- Apply exception patterns for robust applications
- Write clean, focused exception handling code

---

## Next Steps

## Further Resources
- Python documentation on exceptions
- "Effective Python" by Brett Slatkin
- Python's `traceback` module
- The `contextlib` module
- Raymond Hettinger's talks on Python
