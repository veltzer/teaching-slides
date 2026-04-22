---
tags:
  - languages:python
level: advanced
category: language
audience:
  - audiences:developers

---
# Python Function Decorators

## Overview
- Understanding function decorators
- How decorators work internally
- Creating your own decorators
- Common decorator patterns and use cases
- Examples from the standard library

---

## What Are Decorators?: Introduction to Decorators

- Modify or enhance functions without changing their definition
- Apply a wrapper function using special syntax
- Follows the "decorator" design pattern
- First-class functions make decorators possible
- Powerful tool for separation of concerns

```python
# Using a decorator
@my_decorator
def my_function():
    pass

# Equivalent to:
def my_function():
    pass
my_function = my_decorator(my_function)
```

---

## What Are Decorators?: When to Use Decorators

- Add functionality that's not part of the core logic
- Cross-cutting concerns like:
    - Timing and profiling
    - Logging
    - Access control and authentication
    - Caching
    - Input validation
    - Rate limiting
- Avoid code duplication
- Separate business logic from technical concerns

---

## Decorator Wrapping and Call Flow

![decorator_wrapping](svg/courses/languages/python/advanced-python/14_decorators/decorator_wrapping.svg)

---

## How Decorators Work

## Decorator Fundamentals
- Decorators are callable objects that take a function as input
- They return a new function that wraps the original
- The wrapper adds functionality before/after the original function
- The original function is replaced with the wrapped version
- Python applies decorators at function definition time

```python
def simple_decorator(func):
    # Define a wrapper function
    def wrapper():
        print("Before the function call")
        func()  # Call the original function
        print("After the function call")
    # Return the wrapper function
    return wrapper

# Apply the decorator
@simple_decorator
def say_hello():
    print("Hello!")

# Calling the decorated function
say_hello()
# Output:
# Before the function call
# Hello!
# After the function call
```

---

## Creating Decorators: Basic Decorator Pattern

- Create a function that takes a function as an argument
- Define a wrapper function inside the decorator
- The wrapper adds functionality before/after the original
- Return the wrapper function
- Use proper argument handling for flexibility

```python
def my_decorator(func):
    def wrapper(*args, **kwargs):
        # Code to run before the function
        print(f"Calling {func.__name__}")

        # Call the original function
        result = func(*args, **kwargs)

        # Code to run after the function
        print(f"{func.__name__} returned {result}")

        # Return the result
        return result

    return wrapper

@my_decorator
def add(a, b):
    return a + b

print(add(2, 3))
# Output:
# Calling add
# add returned 5
# 5
```

---

## Creating Decorators: Preserving Metadata with functools.wraps

- Decorators hide the original function's metadata
- This affects debugging, introspection, and documentation
- `functools.wraps` preserves function metadata
- Copies attributes like __name__, __doc__, __module__
- Always use it when creating decorators

```python
from functools import wraps

def my_decorator(func):
    @wraps(func)  # This preserves metadata
    def wrapper(*args, **kwargs):
        """Wrapper docstring"""
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@my_decorator
def example():
    """Example function docstring"""
    pass

# Without wraps:
# print(example.__name__)  # Would print "wrapper"
# print(example.__doc__)   # Would print "Wrapper docstring"

# With wraps:
print(example.__name__)  # Prints "example"
print(example.__doc__)   # Prints "Example function docstring"
```

---

## Creating Decorators: Decorators with Arguments

- Create a decorator factory that returns a decorator
- Three levels of functions:
    1. Decorator factory (takes decorator arguments)
    1. Decorator (takes the function)
    1. Wrapper (takes function arguments)
- Allows customizable decorators

```python
def repeat(times):
    """Decorator factory that creates a decorator to repeat a function."""
    # This is the actual decorator
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            """Wrapper that runs the function multiple times."""
            result = None
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

# Using the decorator with arguments
@repeat(times=3)
def greet(name):
    print(f"Hello, {name}!")

greet("Alice")
# Output:
# Hello, Alice!
# Hello, Alice!
# Hello, Alice!
```

---

## Common Decorator Patterns: Timing Decorator

- Measure how long a function takes to execute
- Useful for performance analysis
- Simple but practical example
- Demonstrates the decorator structure

```python
import time
from functools import wraps

def timing_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"{func.__name__} took {execution_time:.4f} seconds to run")
        return result
    return wrapper

@timing_decorator
def slow_function(n):
    time.sleep(n)  # Simulate a slow operation
    return f"Completed after {n} seconds"

print(slow_function(1.5))
# Output:
# slow_function took 1.5001 seconds to run
# Completed after 1.5 seconds
```

---

## Common Decorator Patterns: Logging Decorator

- Log when functions are called
- Record arguments and return values
- Helpful for debugging and monitoring
- Non-intrusive way to add logging

```python
import logging
from functools import wraps

# Set up logging
logging.basicConfig(level=logging.INFO)

def log_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)

        logging.info(f"Calling {func.__name__}({signature})")
        result = func(*args, **kwargs)
        logging.info(f"{func.__name__} returned {result!r}")

        return result
    return wrapper

@log_decorator
def calculate_sum(a, b):
    return a + b

calculate_sum(5, b=3)
# Output logs:
# INFO:root:Calling calculate_sum(5, b=3)
# INFO:root:calculate_sum returned 8
```

---

## Common Decorator Patterns: Retry Decorator

- Automatically retry a function when it fails
- Customizable retry count and delay
- Handle transient errors gracefully
- Common pattern for network operations

```python
import time
from functools import wraps

def retry(max_attempts=3, delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts == max_attempts:
                        raise
                    print(f"Attempt {attempts} failed with {e}, retrying in {delay}s...")
                    time.sleep(delay)
            return None  # Should never reach here
        return wrapper
    return decorator

@retry(max_attempts=3, delay=0.5)
def unstable_network_call(url):
    import random
    if random.random() < 0.7:  # 70% chance of failure
        raise ConnectionError("Network error")
    return f"Data from {url}"

# Try the function
result = unstable_network_call("example.com")
```

---

## Common Decorator Patterns: Memoization / Caching Decorator

- Cache function results based on arguments
- Avoid redundant calculations for same inputs
- Significant performance improvement for expensive functions
- Similar to functools.lru_cache

```python
from functools import wraps

def memoize(func):
    cache = {}

    @wraps(func)
    def wrapper(*args, **kwargs):
        # Create a key from the arguments
        # (assumes args and kwargs are hashable)
        key = str(args) + str(kwargs)

        if key not in cache:
            # Call function only if result not in cache
            cache[key] = func(*args, **kwargs)

        return cache[key]

    return wrapper

@memoize
def fibonacci(n):
    """Calculate the nth Fibonacci number recursively."""
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# Without memoization, this would be very slow
print(fibonacci(35))  # 9227465
```

---

## Common Decorator Patterns: Validation Decorator

- Check function arguments before execution
- Enforce contracts and preconditions
- Centralize validation logic
- Cleaner than repetitive checks in functions

```python
from functools import wraps

def validate_types(**expected_types):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Get function parameter names
            import inspect
            sig = inspect.signature(func)
            params = list(sig.parameters.keys())

            # Check positional arguments
            for arg_name, arg_value in zip(params, args):
                if arg_name in expected_types:
                    if not isinstance(arg_value, expected_types[arg_name]):
                        raise TypeError(f"Argument {arg_name} must be {expected_types[arg_name]}")

            # Check keyword arguments
            for arg_name, arg_value in kwargs.items():
                if arg_name in expected_types:
                    if not isinstance(arg_value, expected_types[arg_name]):
                        raise TypeError(f"Argument {arg_name} must be {expected_types[arg_name]}")

            return func(*args, **kwargs)
        return wrapper
    return decorator

@validate_types(name=str, age=int)
def greet_person(name, age):
    return f"Hello {name}, you are {age} years old"

print(greet_person("Alice", 30))  # Works fine
# print(greet_person("Bob", "thirty"))  # Raises TypeError
```

---

## Decorators in the Standard Library: functools.lru_cache

- Least Recently Used cache decorator
- Memoize function calls for performance
- Configurable maximum cache size
- Cache statistics for monitoring
- Perfect for expensive deterministic functions

```python
from functools import lru_cache
import time

@lru_cache(maxsize=128)
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# Measure performance
start = time.time()
fibonacci(35)
end = time.time()
print(f"First call: {end - start:.6f} seconds")

# Second call uses cached result
start = time.time()
fibonacci(35)
end = time.time()
print(f"Second call: {end - start:.6f} seconds")

# Check cache info
print(fibonacci.cache_info())
# Output: CacheInfo(hits=34, misses=36, maxsize=128, currsize=36)
```

---

## Decorators in the Standard Library: functools.singledispatch

- Function overloading based on argument type
- Register handlers for different types
- Select implementation at runtime
- Enables cleaner code than long if-elif chains
- Extensible system for type-specific behavior

```python
from functools import singledispatch

@singledispatch
def process(obj):
    raise NotImplementedError(f"Cannot process object of type {type(obj)}")

@process.register
def _(obj: int):
    return f"Processing int: {obj * 2}"

@process.register
def _(obj: str):
    return f"Processing str: {obj.upper()}"

@process.register(list)  # Alternative registration syntax
def _(obj):
    return f"Processing list with {len(obj)} items"

# Use the multi-implementation function
print(process(10))        # Processing int: 20
print(process("hello"))   # Processing str: HELLO
print(process([1, 2, 3])) # Processing list with 3 items
```

---

## Decorators in the Standard Library: @property Decorator

- Convert methods into properties
- Control attribute access
- Add validation for setting attributes
- Computed properties that look like attributes
- Create read-only attributes

```python
class Person:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name
        self._age = 0

    @property
    def full_name(self):
        """Return the person's full name."""
        return f"{self.first_name} {self.last_name}"

    @property
    def age(self):
        """Get the person's age."""
        return self._age

    @age.setter
    def age(self, value):
        """Set the person's age with validation."""
        if not isinstance(value, int):
            raise TypeError("Age must be an integer")
        if value < 0 or value > 150:
            raise ValueError("Age must be between 0 and 150")
        self._age = value

person = Person("John", "Doe")
print(person.full_name)  # John Doe
person.age = 30
print(person.age)        # 30
# person.age = -5        # ValueError
```

---

## Decorators in the Standard Library: @classmethod and @staticmethod

- Modify method behavior
- @classmethod receives the class as first argument
- @staticmethod doesn't receive special first argument
- Different ways to organize class functionality
- Alternative constructors with @classmethod

```python
class Date:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    @classmethod
    def from_string(cls, date_string):
        """Create a Date from a string like 'YYYY-MM-DD'."""
        year, month, day = map(int, date_string.split('-'))
        return cls(year, month, day)

    @classmethod
    def today(cls):
        """Create a Date for the current date."""
        import datetime
        d = datetime.datetime.now()
        return cls(d.year, d.month, d.day)

    @staticmethod
    def is_valid_date(year, month, day):
        """Check if a date is valid."""
        if year < 0 or month < 1 or month > 12 or day < 1:
            return False
        return day <= [31, 29 if year % 4 == 0 else 28,
                      31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month-1]

# Using class methods as alternate constructors
date1 = Date.from_string("2023-05-15")
date2 = Date.today()

# Using static method
print(Date.is_valid_date(2023, 2, 29))  # False
```

---

## Advanced Decorator Techniques: Class Decorators

- Decorators that modify classes instead of functions
- Apply the decorator to the class definition
- Can modify class attributes and methods
- Can add new attributes and methods
- Useful for metaclass-like behavior

```python
def add_repr(cls):
    """Add a simple __repr__ method to a class."""
    def __repr__(self):
        # Create a string of attr=value pairs
        attrs = ", ".join(f"{key}={value!r}"
                         for key, value in self.__dict__.items())
        return f"{cls.__name__}({attrs})"

    # Add the __repr__ method to the class
    cls.__repr__ = __repr__
    return cls

@add_repr
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

person = Person("Alice", 30)
print(person)  # Person(name='Alice', age=30)
```

---

## Advanced Decorator Techniques: Method Decorators

- Decorating methods inside classes
- Special considerations for instance methods
- Preserving the `self` parameter
- Decorating all methods in a class

```python
def debug_method(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        # Access instance attributes via self
        class_name = self.__class__.__name__
        print(f"Calling {class_name}.{func.__name__}")
        return func(self, *args, **kwargs)
    return wrapper

class Calculator:
    def __init__(self, name):
        self.name = name

    @debug_method
    def add(self, a, b):
        return a + b

    @debug_method
    def multiply(self, a, b):
        return a * b

calc = Calculator("MyCalc")
print(calc.add(2, 3))        # Calling Calculator.add \n 5
print(calc.multiply(2, 3))   # Calling Calculator.multiply \n 6
```

---

## Advanced Decorator Techniques: Decorator Stacking

- Apply multiple decorators to a function
- Decorators are applied from bottom to top
- Each decorator wraps the result of the one below it
- Useful for combining different concerns
- Order can be important

```python
from functools import wraps

def bold(func):
    @wraps(func)
    def wrapper():
        return f"<b>{func()}</b>"
    return wrapper

def italic(func):
    @wraps(func)
    def wrapper():
        return f"<i>{func()}</i>"
    return wrapper

def underline(func):
    @wraps(func)
    def wrapper():
        return f"<u>{func()}</u>"
    return wrapper

@bold
@italic
@underline
def hello():
    return "Hello, world!"

print(hello())
# Output: <b><i><u>Hello, world!</u></i></b>
# Decorators applied from bottom to top: underline, then italic, then bold
```

---

## Advanced Decorator Techniques: Stateful Decorators

- Decorators that maintain state between calls
- Track function call history
- Accumulate results
- Control function behavior based on past calls
- Implement rate limiting, caching, etc.

```python
def counter(func):
    # State is stored in the wrapper's function attributes
    @wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.count += 1
        print(f"Call {wrapper.count} to {func.__name__}")
        return func(*args, **kwargs)

    # Initialize the state
    wrapper.count = 0
    return wrapper

@counter
def hello(name):
    return f"Hello, {name}!"

print(hello("Alice"))  # Call 1 to hello \n Hello, Alice!
print(hello("Bob"))    # Call 2 to hello \n Hello, Bob!
print(hello("Alice"))  # Call 3 to hello \n Hello, Alice!

# Access the state
print(f"Function called {hello.count} times")  # Function called 3 times
```

---

## Advanced Decorator Techniques: Creating Decorator Libraries

- Design reusable decorators
- Combine decorators for complex behavior
- Documentation and metadata
- Testing decorators effectively
- Decorator composition patterns

```python
# Example of a small decorator library

def debug(level='INFO'):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(f"[{level}] Calling {func.__name__}")
            return func(*args, **kwargs)
        return wrapper
    return decorator

def timing(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.5f} seconds")
        return result
    return wrapper
```

---

## Creating Decorator Libraries: Retry Decorator

```python
def retry(attempts=3):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == attempts:
                        raise
                    print(f"Attempt {attempt} failed: {e}")
            return None
        return wrapper
    return decorator
```

---

## Practical Examples

## Complete Decorator Example: Setup and Signature
```python
import time
import functools
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def logged(level=logging.INFO, name=None, message=None):
    """
    Add logging to a function.
    level: the logging level
    name: the logger name (default: function's module)
    message: the log message (default: function name with args)
    """
    def decorator(func):
        logname = name if name else func.__module__
        log = logging.getLogger(logname)
        logmsg = message if message else func.__name__
```

---

## Complete Decorator Example: Wrapper Implementation

```python
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Log before function execution
            log_args = ", ".join(str(a) for a in args)
            log_kwargs = ", ".join(f"{k}={v}" for k, v in kwargs.items())
            log_params = ", ".join(filter(None, [log_args, log_kwargs]))
            log.log(level, f"Calling {logmsg}({log_params})")

            # Run the function
            start = time.time()
            try:
                result = func(*args, **kwargs)
                # Log after successful execution
                end = time.time()
                log.log(level, f"{logmsg} returned {result} in {end-start:.2f}s")
                return result
            except Exception as e:
                # Log exceptions
                end = time.time()
                log.exception(f"{logmsg} failed in {end-start:.2f}s: {str(e)}")
                raise

        return wrapper
    return decorator
```

---

## Complete Decorator Example: Usage

```python
# Using the decorator
@logged()
def divide(a, b):
    return a / b

divide(10, 5)   # Normal case
try:
    divide(10, 0)  # Exception case
except ZeroDivisionError:
    pass
```

---

## Summary

## Key Takeaways
- Decorators are a powerful tool for modifying function behavior
- They implement the wrapper pattern with a clean syntax
- Always use @functools.wraps to preserve metadata
- Common uses include logging, timing, validation, and caching
- Decorator stacking and parameterized decorators add flexibility
- Many standard library decorators provide useful functionality
- Advanced techniques include class decorators and stateful decorators
