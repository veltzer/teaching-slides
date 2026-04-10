# Functions

---
## Defining Functions

```python
def greet(name):
    """Return a greeting string."""
    return f"Hello, {name}!"

result = greet("Alice")
print(result)  # Hello, Alice!
```

- Use the `def` keyword
- Function name follows `snake_case` convention
- Parentheses contain parameters
- Body is indented

---
## Functions Without Return

```python
def say_hello(name):
    print(f"Hello, {name}!")

result = say_hello("Alice")
print(result)  # None
```

- Functions without `return` implicitly return `None`
- `return` without a value also returns `None`

---
## Multiple Return Values

```python
def divide(a, b):
    quotient = a // b
    remainder = a % b
    return quotient, remainder

q, r = divide(17, 5)
print(f"17 / 5 = {q} remainder {r}")
# 17 / 5 = 3 remainder 2
```

- Actually returns a tuple

---
## Early Return

```python
def absolute(n):
    if n < 0:
        return -n
    return n

print(absolute(-5))  # 5
print(absolute(3))   # 3
```

---
## Parameters vs Arguments
- **Parameters**: Variables in the function definition
- **Arguments**: Values passed when calling the function

```python
def greet(name):      # 'name' is a parameter
    return f"Hello, {name}!"

greet("Alice")        # "Alice" is an argument
```

---
## Positional Arguments

```python
def power(base, exponent):
    return base ** exponent

print(power(2, 10))   # 1024
print(power(10, 2))   # 100 (order matters!)
```

---
## Keyword Arguments

```python
def power(base, exponent):
    return base ** exponent

# Using keyword arguments
print(power(base=2, exponent=10))    # 1024
print(power(exponent=10, base=2))    # 1024 (order doesn't matter)
print(power(2, exponent=10))         # 1024 (mix positional and keyword)
# print(power(base=2, 10))           # SyntaxError!
```

---
## Default Parameter Values

```python
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

print(greet("Alice"))            # Hello, Alice!
print(greet("Alice", "Hi"))      # Hi, Alice!
print(greet("Alice", greeting="Hey"))  # Hey, Alice!
```

---
## Mutable Default Arguments - Beware!

```python
# BUG: mutable default is shared across calls
def append_to(item, lst=[]):
    lst.append(item)
    return lst

print(append_to(1))  # [1]
print(append_to(2))  # [1, 2] - unexpected!

# FIX: use None as default
def append_to(item, lst=None):
    if lst is None:
        lst = []
    lst.append(item)
    return lst
```

---
## `*args` - Variable Positional Arguments

```python
def add(*args):
    print(type(args))  # <class 'tuple'>
    return sum(args)

print(add(1, 2))        # 3
print(add(1, 2, 3, 4))  # 10
print(add())             # 0
```

- `*args` collects extra positional arguments into a tuple

---
## `**kwargs` - Variable Keyword Arguments

```python
def print_info(**kwargs):
    print(type(kwargs))  # <class 'dict'>
    for key, value in kwargs.items():
        print(f"{key}: {value}")

print_info(name="Alice", age=30, city="NYC")
```

```output
name: Alice
age: 30
city: NYC
```

---
## Combining `*args` and `**kwargs`

```python
def func(a, b, *args, **kwargs):
    print(f"a={a}, b={b}")
    print(f"args={args}")
    print(f"kwargs={kwargs}")

func(1, 2, 3, 4, x=5, y=6)
```

```output
a=1, b=2
args=(3, 4)
kwargs={'x': 5, 'y': 6}
```

---
## Parameter Order Rules
- The order must be:
    1. Regular positional parameters
    1. `*args`
    1. Keyword-only parameters
    1. `**kwargs`

```python
def func(a, b, *args, c=10, **kwargs):
    print(a, b, args, c, kwargs)

func(1, 2, 3, 4, c=20, x=30)
# 1 2 (3, 4) 20 {'x': 30}
```

---
## Keyword-Only Arguments
- Parameters after `*` must be passed as keywords

```python
def connect(host, port, *, timeout=30, retries=3):
    print(f"host={host}, port={port}")
    print(f"timeout={timeout}, retries={retries}")

connect("localhost", 8080, timeout=10)
# connect("localhost", 8080, 10)  # TypeError!
```

---
## Positional-Only Arguments (Python 3.8+)
- Parameters before `/` must be passed positionally

```python
def greet(name, /, greeting="Hello"):
    return f"{greeting}, {name}!"

print(greet("Alice"))             # Hello, Alice!
print(greet("Alice", "Hi"))       # Hi, Alice!
# print(greet(name="Alice"))      # TypeError!
```

---
## Complete Parameter Syntax

```python
def func(pos_only, /, normal, *, kw_only):
    print(pos_only, normal, kw_only)

func(1, 2, kw_only=3)          # OK
func(1, normal=2, kw_only=3)   # OK
# func(pos_only=1, ...)        # TypeError
# func(1, 2, 3)                # TypeError
```

---
## Unpacking Arguments

```python
def add(a, b, c):
    return a + b + c

# Unpack list/tuple with *
args = [1, 2, 3]
print(add(*args))  # 6

# Unpack dict with **
kwargs = {"a": 1, "b": 2, "c": 3}
print(add(**kwargs))  # 6
```

---
## Lambda Functions
- Anonymous, single-expression functions

```python
# Regular function
def double(x):
    return x * 2

# Equivalent lambda
double = lambda x: x * 2

print(double(5))  # 10
```

---
## Lambda Use Cases

```python
# Sorting with custom key
people = [("Alice", 30), ("Bob", 25), ("Charlie", 35)]
people.sort(key=lambda p: p[1])
print(people)
# [('Bob', 25), ('Alice', 30), ('Charlie', 35)]

# Filtering
numbers = [1, -2, 3, -4, 5]
positives = list(filter(lambda x: x > 0, numbers))
print(positives)  # [1, 3, 5]
```

---
## `map()` Function

```python
numbers = [1, 2, 3, 4, 5]

# Apply function to each element
doubled = list(map(lambda x: x * 2, numbers))
print(doubled)  # [2, 4, 6, 8, 10]

# With named function
def square(x):
    return x ** 2

squared = list(map(square, numbers))
print(squared)  # [1, 4, 9, 16, 25]
```

---
## `filter()` Function

```python
numbers = range(-5, 6)

# Filter elements
positives = list(filter(lambda x: x > 0, numbers))
print(positives)  # [1, 2, 3, 4, 5]

# Filter with named function
def is_even(n):
    return n % 2 == 0

evens = list(filter(is_even, numbers))
print(evens)  # [-4, -2, 0, 2, 4]
```

---
## `reduce()` Function

```python
from functools import reduce

numbers = [1, 2, 3, 4, 5]

# Sum using reduce
total = reduce(lambda a, b: a + b, numbers)
print(total)  # 15

# Product using reduce
product = reduce(lambda a, b: a * b, numbers)
print(product)  # 120
```

---
## LEGB Scope Rules

![legb_scope](svg/courses/languages/python/python-programming/06_functions/legb_scope.svg)

---

## Variable Scope - LEGB Rule
- Python looks up names in this order:
    1. **L**ocal: Inside the current function
    1. **E**nclosing: In enclosing function(s)
    1. **G**lobal: At module level
    1. **B**uilt-in: In the built-in namespace

```python
x = "global"

def outer():
    x = "enclosing"
    def inner():
        x = "local"
        print(x)  # local
    inner()
```

---
## Local vs Global Scope

```python
x = 10  # Global

def func():
    x = 20  # Local (shadows global)
    print(x)

func()     # 20
print(x)   # 10 (global unchanged)
```

---
## The `global` Keyword

```python
x = 10

def func():
    global x
    x = 20
    print(x)

func()     # 20
print(x)   # 20 (global changed)
```

- Use sparingly; prefer returning values instead

---
## The `nonlocal` Keyword

```python
def outer():
    count = 0

    def increment():
        nonlocal count
        count += 1
        return count

    print(increment())  # 1
    print(increment())  # 2
    print(increment())  # 3

outer()
```

---
## Closures
- A function that remembers values from its enclosing scope

```python
def make_multiplier(factor):
    def multiply(x):
        return x * factor
    return multiply

double = make_multiplier(2)
triple = make_multiplier(3)

print(double(5))   # 10
print(triple(5))   # 15
```

---
## Closure - Counter Example

```python
def make_counter(start=0):
    count = start

    def counter():
        nonlocal count
        count += 1
        return count

    return counter

c = make_counter()
print(c())  # 1
print(c())  # 2
print(c())  # 3
```

---
## Functions are First-Class Objects
- Functions can be:
    - Assigned to variables
    - Passed as arguments
    - Returned from other functions
    - Stored in data structures

```python
def greet(name):
    return f"Hello, {name}!"

# Assign to variable
say_hi = greet
print(say_hi("Alice"))  # Hello, Alice!

# Store in list
funcs = [len, str.upper, abs]
```

---
## Functions as Arguments

```python
def apply(func, value):
    return func(value)

print(apply(abs, -5))        # 5
print(apply(str.upper, "hi"))  # HI
print(apply(len, [1, 2, 3]))  # 3
```

---
## Decorators - Concept
- A decorator wraps a function to extend its behavior

```python
def my_decorator(func):
    def wrapper(*args, **kwargs):
        print("Before function call")
        result = func(*args, **kwargs)
        print("After function call")
        return result
    return wrapper
```

---
## Decorators - Usage

```python
def my_decorator(func):
    def wrapper(*args, **kwargs):
        print("Before")
        result = func(*args, **kwargs)
        print("After")
        return result
    return wrapper

@my_decorator
def say_hello(name):
    print(f"Hello, {name}!")

say_hello("Alice")
```

```output
Before
Hello, Alice!
After
```

---
## Decorator - Timing Example

```python
import time

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"{func.__name__} took {elapsed:.4f}s")
        return result
    return wrapper

@timer
def slow_function():
    time.sleep(1)

slow_function()  # slow_function took 1.0012s
```

---
## Preserving Function Metadata

```python
from functools import wraps

def my_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@my_decorator
def greet(name):
    """Greet someone."""
    return f"Hello, {name}!"

print(greet.__name__)  # 'greet' (not 'wrapper')
print(greet.__doc__)   # 'Greet someone.'
```

---
## Decorators with Arguments

```python
from functools import wraps

def repeat(n):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(n):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(3)
def say_hi():
    print("Hi!")

say_hi()  # Prints "Hi!" three times
```

---
## Type Hints

```python
def greet(name: str) -> str:
    return f"Hello, {name}!"

def add(a: int, b: int) -> int:
    return a + b

def process(items: list[str]) -> dict[str, int]:
    return {item: len(item) for item in items}
```

- Type hints are optional and not enforced at runtime
- Used by IDEs and type checkers like `mypy`

---
## Type Hints - Optional and Union

```python
from typing import Optional, Union

def find(items: list[str], target: str) -> Optional[int]:
    """Return index or None if not found."""
    try:
        return items.index(target)
    except ValueError:
        return None

# Python 3.10+ union syntax
def process(value: int | str) -> str:
    return str(value)
```

---
## Recursive Functions

```python
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

print(factorial(5))  # 120

def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

print(fibonacci(10))  # 55
```

---
## Recursion Limit

```python
import sys

print(sys.getrecursionlimit())  # 1000 (default)

# Can be changed (use with caution)
sys.setrecursionlimit(5000)
```

- Python has a default recursion limit of 1000
- Exceeding it raises `RecursionError`
- Prefer iterative solutions for deep recursion

---
## Docstring Conventions

```python
def calculate_area(length: float, width: float) -> float:
    """Calculate the area of a rectangle.

    Args:
        length: The length of the rectangle.
        width: The width of the rectangle.

    Returns:
        The area of the rectangle.

    Raises:
        ValueError: If length or width is negative.
    """
    if length < 0 or width < 0:
        raise ValueError("Dimensions must be non-negative")
    return length * width
```

---
## `callable()` and `__call__`

```python
print(callable(print))   # True
print(callable(42))       # False

# Make an object callable
class Adder:
    def __init__(self, n):
        self.n = n

    def __call__(self, x):
        return self.n + x

add5 = Adder(5)
print(add5(10))    # 15
print(callable(add5))  # True
```

---
## Summary
- Functions are defined with `def` and can return values
- Parameters support defaults, `*args`, `**kwargs`
- Keyword-only and positional-only parameters control calling syntax
- Lambda for simple anonymous functions
- LEGB rule governs variable scope
- Closures capture enclosing scope variables
- Decorators modify function behavior
- Type hints improve readability and enable static analysis
