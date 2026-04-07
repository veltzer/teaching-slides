# Functional Python
---
## What is Functional Programming?
- Programming paradigm that treats computation as evaluation of functions
- Key principles:
    - First-class functions
    - Pure functions (no side effects)
    - Immutability
    - Higher-order functions
- Python supports functional style alongside OOP
---
## Iterables
- An iterable is any object you can loop over
- Examples: `list`, `tuple`, `str`, `dict`, `set`, `range`, `file`

```python
# All of these are iterables
for x in [1, 2, 3]: pass
for x in (1, 2, 3): pass
for x in "hello": pass
for x in {"a": 1}: pass
for x in range(5): pass
```
---
## The Iterator Protocol
- An **iterable** has an `__iter__` method that returns an **iterator**
- An **iterator** has a `__next__` method that returns values one at a time
- Raises `StopIteration` when exhausted

```python
my_list = [1, 2, 3]
iterator = iter(my_list)

print(next(iterator))  # 1
print(next(iterator))  # 2
print(next(iterator))  # 3
# print(next(iterator))  # StopIteration!
```
---
## How `for` Loops Work Internally

```python
# This for loop:
for item in [1, 2, 3]:
    print(item)

# Is equivalent to:
iterator = iter([1, 2, 3])
while True:
    try:
        item = next(iterator)
        print(item)
    except StopIteration:
        break
```
---
## Creating Custom Iterators

```python
class Countdown:
    def __init__(self, start):
        self.start = start

    def __iter__(self):
        return self

    def __next__(self):
        if self.start <= 0:
            raise StopIteration
        self.start -= 1
        return self.start + 1

for n in Countdown(5):
    print(n, end=" ")
# 5 4 3 2 1
```
---
## Iterators are Lazy
- Iterators produce values on demand
- They do not store all values in memory
- Once consumed, they are exhausted

```python
numbers = iter([1, 2, 3])

# First pass works
for n in numbers:
    print(n, end=" ")  # 1 2 3

print()

# Second pass produces nothing (exhausted)
for n in numbers:
    print(n, end=" ")  # (nothing)
```
---
## Generators - Introduction
- A simpler way to create iterators
- Use `yield` instead of `return`
- Function state is preserved between calls

```python
def countdown(n):
    while n > 0:
        yield n
        n -= 1

for x in countdown(5):
    print(x, end=" ")
# 5 4 3 2 1
```
---
## Generator vs Regular Function

```python
# Regular function: returns a value and exits
def get_squares_list(n):
    result = []
    for i in range(n):
        result.append(i ** 2)
    return result

# Generator: yields values one at a time
def get_squares_gen(n):
    for i in range(n):
        yield i ** 2

# Both work with for loops
for x in get_squares_gen(5):
    print(x, end=" ")  # 0 1 4 9 16
```
---
## Generator Memory Efficiency

```python
import sys

# List: stores all values in memory
squares_list = [x ** 2 for x in range(1_000_000)]
print(sys.getsizeof(squares_list))  # ~8 MB

# Generator: stores only the current value
squares_gen = (x ** 2 for x in range(1_000_000))
print(sys.getsizeof(squares_gen))   # ~200 bytes
```
---
## Generator Functions - Multiple Yields

```python
def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

# Get first 10 Fibonacci numbers
fib = fibonacci()
for _ in range(10):
    print(next(fib), end=" ")
# 0 1 1 2 3 5 8 13 21 34
```
---
## `yield` from

```python
def flatten(nested):
    for item in nested:
        if isinstance(item, list):
            yield from flatten(item)
        else:
            yield item

data = [1, [2, 3], [4, [5, 6]], 7]
print(list(flatten(data)))
# [1, 2, 3, 4, 5, 6, 7]
```

- `yield from` delegates to a sub-generator
---
## Generator Expressions
- Like list comprehensions but lazy
- Use parentheses instead of square brackets

```python
# List comprehension (creates full list)
squares_list = [x ** 2 for x in range(10)]

# Generator expression (lazy)
squares_gen = (x ** 2 for x in range(10))

print(type(squares_list))  # <class 'list'>
print(type(squares_gen))   # <class 'generator'>

# Use in functions that accept iterables
total = sum(x ** 2 for x in range(10))
print(total)  # 285
```
---
## List Comprehensions

```python
# Basic syntax: [expression for item in iterable]
squares = [x ** 2 for x in range(6)]
print(squares)  # [0, 1, 4, 9, 16, 25]

# With condition
evens = [x for x in range(10) if x % 2 == 0]
print(evens)  # [0, 2, 4, 6, 8]

# With transformation
words = ["hello", "world"]
upper = [w.upper() for w in words]
print(upper)  # ['HELLO', 'WORLD']
```
---
## List Comprehension vs Loop

```python
# Traditional loop
result = []
for x in range(10):
    if x % 2 == 0:
        result.append(x ** 2)

# List comprehension (more Pythonic)
result = [x ** 2 for x in range(10) if x % 2 == 0]
print(result)  # [0, 4, 16, 36, 64]
```

- List comprehensions are often faster than equivalent loops
- More readable for simple transformations
---
## Nested List Comprehensions

```python
# Flatten a matrix
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flat = [x for row in matrix for x in row]
print(flat)  # [1, 2, 3, 4, 5, 6, 7, 8, 9]

# Create a matrix
matrix = [[i * 3 + j for j in range(3)] for i in range(3)]
print(matrix)
# [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
```
---
## Dictionary Comprehensions

```python
# Basic syntax: {key: value for item in iterable}
squares = {x: x ** 2 for x in range(6)}
print(squares)  # {0: 0, 1: 1, 2: 4, 3: 9, 4: 16, 5: 25}

# Swap keys and values
original = {"a": 1, "b": 2, "c": 3}
swapped = {v: k for k, v in original.items()}
print(swapped)  # {1: 'a', 2: 'b', 3: 'c'}

# Filter
data = {"a": 1, "b": 2, "c": 3, "d": 4}
filtered = {k: v for k, v in data.items() if v > 2}
print(filtered)  # {'c': 3, 'd': 4}
```
---
## Set Comprehensions

```python
# Basic syntax: {expression for item in iterable}
squares = {x ** 2 for x in range(-3, 4)}
print(squares)  # {0, 1, 4, 9}

# Remove duplicates with transformation
words = ["Hello", "hello", "HELLO", "World"]
unique = {w.lower() for w in words}
print(unique)  # {'hello', 'world'}
```
---
## Comprehension with Walrus Operator

```python
# Filter and transform in one pass
import math

numbers = [2, -1, 16, -4, 25, 0]
roots = [
    root
    for x in numbers
    if x > 0
    if (root := math.sqrt(x)) > 2
]
print(roots)  # [4.0, 5.0]
```
---
## When NOT to Use Comprehensions
- When the logic is complex (use a loop instead)
- When you do not need the result (use a loop for side effects)
- When readability suffers

```python
# BAD: too complex
result = [
    func(x, y)
    for x in range(10)
    for y in range(10)
    if x != y
    if func(x, y) > threshold
]

# BETTER: use a loop
result = []
for x in range(10):
    for y in range(10):
        if x != y:
            val = func(x, y)
            if val > threshold:
                result.append(val)
```
---
## The `map()` Function

```python
numbers = [1, 2, 3, 4, 5]

# map applies a function to each element
squared = list(map(lambda x: x ** 2, numbers))
print(squared)  # [1, 4, 9, 16, 25]

# Equivalent list comprehension
squared = [x ** 2 for x in numbers]

# map with multiple iterables
sums = list(map(lambda a, b: a + b, [1, 2, 3], [10, 20, 30]))
print(sums)  # [11, 22, 33]
```
---
## The `filter()` Function

```python
numbers = range(-5, 6)

# filter keeps elements where function returns True
positives = list(filter(lambda x: x > 0, numbers))
print(positives)  # [1, 2, 3, 4, 5]

# Equivalent list comprehension
positives = [x for x in numbers if x > 0]

# Filter with None removes falsy values
data = [0, 1, "", "hello", None, 42, [], [1]]
truthy = list(filter(None, data))
print(truthy)  # [1, 'hello', 42, [1]]
```
---
## The `reduce()` Function

```python
from functools import reduce

numbers = [1, 2, 3, 4, 5]

# Sum
total = reduce(lambda a, b: a + b, numbers)
print(total)  # 15

# Product
product = reduce(lambda a, b: a * b, numbers)
print(product)  # 120

# Max (manual implementation)
maximum = reduce(lambda a, b: a if a > b else b, numbers)
print(maximum)  # 5
```
---
## `reduce()` Visualization

![reduce_visualization](/svg/courses/languages/python/python-programming/10_functional_python/reduce_visualization.svg)

---
## `any()` and `all()`

```python
numbers = [1, -2, 3, -4, 5]

# any: True if at least one is True
print(any(x > 0 for x in numbers))  # True
print(any(x > 10 for x in numbers))  # False

# all: True if all are True
print(all(x > 0 for x in numbers))  # False
print(all(x > -10 for x in numbers))  # True

# Short-circuit evaluation
print(any(x > 0 for x in numbers))  # Stops at first True
```
---
## `sorted()` with Key Functions

```python
# Sort by custom criteria
students = [
    {"name": "Charlie", "grade": 85},
    {"name": "Alice", "grade": 92},
    {"name": "Bob", "grade": 78},
]

by_grade = sorted(students, key=lambda s: s["grade"])
by_name = sorted(students, key=lambda s: s["name"])

# Using operator.itemgetter
from operator import itemgetter
by_grade = sorted(students, key=itemgetter("grade"))
```
---
## `itertools` - Infinite Iterators

```python
from itertools import count, cycle, repeat

# count: infinite counter
for i in count(10, 2):
    if i > 20:
        break
    print(i, end=" ")  # 10 12 14 16 18 20

# cycle: repeat forever
colors = cycle(["red", "green", "blue"])
for _, c in zip(range(5), colors):
    print(c, end=" ")  # red green blue red green

# repeat: repeat a value
threes = list(repeat(3, 5))
print(threes)  # [3, 3, 3, 3, 3]
```
---
## `itertools` - Combinatoric

```python
from itertools import combinations, permutations, product

# Combinations (order doesn't matter)
print(list(combinations("ABC", 2)))
# [('A', 'B'), ('A', 'C'), ('B', 'C')]

# Permutations (order matters)
print(list(permutations("ABC", 2)))
# [('A', 'B'), ('A', 'C'), ('B', 'A'), ('B', 'C'), ('C', 'A'), ('C', 'B')]

# Cartesian product
print(list(product([0, 1], repeat=3)))
# [(0,0,0), (0,0,1), (0,1,0), (0,1,1), (1,0,0), ...]
```
---
## `itertools` - Chain and Groupby

```python
from itertools import chain, groupby

# Chain multiple iterables
combined = list(chain([1, 2], [3, 4], [5]))
print(combined)  # [1, 2, 3, 4, 5]

# Groupby (data must be sorted by key)
data = [("A", 1), ("A", 2), ("B", 3), ("B", 4)]
for key, group in groupby(data, key=lambda x: x[0]):
    print(f"{key}: {list(group)}")
# A: [('A', 1), ('A', 2)]
# B: [('B', 3), ('B', 4)]
```
---
## `itertools` - Slicing Iterators

```python
from itertools import islice, takewhile, dropwhile

# islice: slice an iterator
fib = fibonacci()  # Infinite generator
first_10 = list(islice(fib, 10))
print(first_10)  # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

# takewhile: take while condition is True
nums = [1, 3, 5, 7, 2, 4, 6]
result = list(takewhile(lambda x: x < 6, nums))
print(result)  # [1, 3, 5]

# dropwhile: skip while condition is True
result = list(dropwhile(lambda x: x < 6, nums))
print(result)  # [7, 2, 4, 6]
```
---
## `itertools` - Accumulate

```python
from itertools import accumulate
import operator

numbers = [1, 2, 3, 4, 5]

# Running sum
print(list(accumulate(numbers)))
# [1, 3, 6, 10, 15]

# Running product
print(list(accumulate(numbers, operator.mul)))
# [1, 2, 6, 24, 120]

# Running max
print(list(accumulate([3, 1, 4, 1, 5], max)))
# [3, 3, 4, 4, 5]
```
---
## `functools.partial`

```python
from functools import partial

def multiply(x, y):
    return x * y

double = partial(multiply, 2)
triple = partial(multiply, 3)

print(double(5))   # 10
print(triple(5))   # 15

# Useful with map
numbers = [1, 2, 3, 4, 5]
doubled = list(map(partial(multiply, 2), numbers))
print(doubled)  # [2, 4, 6, 8, 10]
```
---
## `functools.lru_cache`

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

print(fibonacci(100))  # 354224848179261915075

# Cache info
print(fibonacci.cache_info())
# CacheInfo(hits=98, misses=101, maxsize=128, currsize=101)

# Clear cache
fibonacci.cache_clear()
```
---
## `operator` Module

```python
from operator import add, mul, itemgetter, attrgetter

# Use instead of lambda for common operations
from functools import reduce
print(reduce(add, [1, 2, 3, 4]))  # 10
print(reduce(mul, [1, 2, 3, 4]))  # 24

# itemgetter for sorting
students = [("Alice", 90), ("Bob", 85), ("Charlie", 92)]
by_grade = sorted(students, key=itemgetter(1))
print(by_grade)
# [('Bob', 85), ('Alice', 90), ('Charlie', 92)]
```
---
## Generator Pipelines

```python
def read_lines(filename):
    with open(filename) as f:
        for line in f:
            yield line.strip()

def filter_comments(lines):
    for line in lines:
        if not line.startswith("#"):
            yield line

def to_upper(lines):
    for line in lines:
        yield line.upper()

# Pipeline: read -> filter -> transform
lines = read_lines("config.txt")
filtered = filter_comments(lines)
result = to_upper(filtered)
```
---
## Chaining Generators

```python
def integers():
    n = 1
    while True:
        yield n
        n += 1

def squares(nums):
    for n in nums:
        yield n ** 2

def take(n, iterable):
    for _, item in zip(range(n), iterable):
        yield item

# Compose: first 5 perfect squares
result = list(take(5, squares(integers())))
print(result)  # [1, 4, 9, 16, 25]
```
---
## Pure Functions
- Same input always produces same output
- No side effects (no modifying external state)

```python
# Pure function
def add(a, b):
    return a + b

# Impure function (modifies external state)
total = 0
def add_to_total(n):
    global total
    total += n  # Side effect!
    return total
```
---
## Immutability Patterns

```python
# Use tuples instead of lists for fixed data
point = (3, 4)

# Use frozenset instead of set
colors = frozenset({"red", "green", "blue"})

# Use namedtuple for structured data
from collections import namedtuple
Point = namedtuple("Point", ["x", "y"])
p = Point(3, 4)
# p.x = 5  # AttributeError

# Or frozen dataclass
from dataclasses import dataclass

@dataclass(frozen=True)
class Config:
    host: str
    port: int
```
---
## Summary
- Iterators produce values lazily using `__next__`
- Generators simplify iterator creation with `yield`
- Comprehensions create lists, dicts, and sets concisely
- Generator expressions are lazy comprehensions
- `map()`, `filter()`, `reduce()` for functional transformations
- `itertools` provides powerful iterator building blocks
- `functools` offers caching, partial application, and more
- Generator pipelines chain transformations efficiently
