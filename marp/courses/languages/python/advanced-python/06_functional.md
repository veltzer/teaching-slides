# Functional Python

## Overview
- What is functional programming?
- Python's functional features
- Higher-order functions
- Functional tools in Python
- Closures and function composition
- Iterators and generators
- Advanced functional techniques

---

## map / filter / reduce

![map / filter / reduce](svg/courses/languages/python/advanced-python/06_functional/functional_concepts.svg)

---

## What is Functional Programming?

## Core Principles
- Functions as first-class citizens
- Pure functions without side effects
- Immutability of data
- Declarative rather than imperative style
- Composing functions to form larger operations
- Focus on what to compute, not how to compute

---

## What is Functional Programming?

## Benefits of Functional Programming
- Easier to reason about code
- Better parallelization
- More testable code
- Reduced mutable state
- Less prone to certain classes of bugs
- Elegant solutions to complex problems

---

## What is Functional Programming?

## Python as a Multi-Paradigm Language
- Python supports multiple programming styles
- Incorporates functional concepts alongside OOP
- Not a "pure" functional language like Haskell
- Pragmatic mix of paradigms
- Allows functional programming when appropriate

```python
# Imperative style
result = []
for x in range(1, 11):
    if x % 2 == 0:
        result.append(x * x)

# Functional style
result = list(map(lambda x: x * x, filter(lambda x: x % 2 == 0, range(1, 11))))

# Modern Python functional style
result = [x * x for x in range(1, 11) if x % 2 == 0]
```

---

## Functions as First-Class Objects

## What Are First-Class Functions?
- Functions can be assigned to variables
- Functions can be passed as arguments
- Functions can be returned from other functions
- Functions can be stored in data structures
- Functions have attributes and methods
- Functions can be created at runtime

```python
# Assign a function to a variable
def greet(name):
    return f"Hello, {name}!"

say_hello = greet
print(say_hello("Alice"))  # Hello, Alice!

# Store functions in a data structure
function_list = [str.upper, str.lower, str.capitalize]
for func in function_list:
    print(func("python"))  # PYTHON, python, Python
```

---

## Functions as First-Class Objects

## Function Attributes
- Functions are objects with attributes
- Can add custom attributes to functions
- Access built-in attributes like __name__, __doc__
- Function identity is preserved when passed around

```python
def multiply(a, b):
    """Return the product of a and b."""
    return a * b

# Built-in attributes
print(multiply.__name__)  # multiply
print(multiply.__doc__)   # Return the product of a and b.

# Custom attributes
multiply.author = "Alice"
multiply.version = "1.0"

print(multiply.author)    # Alice
print(multiply.version)   # 1.0
```

---

## Higher-Order Functions

## What Are Higher-Order Functions?
- Functions that take other functions as arguments
- Functions that return other functions
- Enable abstraction over actions, not just values
- Foundation of functional programming
- Allow more generic, reusable code

```python
# Function that takes another function as an argument
def apply_twice(func, arg):
    return func(func(arg))

def add_five(x):
    return x + 5

print(apply_twice(add_five, 10))  # 20 (10+5+5)

# Function that returns another function
def create_multiplier(factor):
    def multiplier(number):
        return number * factor
    return multiplier

double = create_multiplier(2)
triple = create_multiplier(3)
print(double(5))  # 10
print(triple(5))  # 15
```

---

## Higher-Order Functions

## Built-in Higher-Order Functions: map()
- Apply a function to each item in an iterable
- Returns a map object (iterator)
- Lazy evaluation - processes items on demand
- More memory efficient than explicit loops
- Works with any iterable

```python
# Square all numbers in a list
numbers = [1, 2, 3, 4, 5]
squared = map(lambda x: x * x, numbers)
print(list(squared))  # [1, 4, 9, 16, 25]

# Convert strings to integers
strings = ["1", "2", "3", "4", "5"]
integers = map(int, strings)
print(list(integers))  # [1, 2, 3, 4, 5]

# Apply function to multiple iterables
list1 = [1, 2, 3]
list2 = [10, 20, 30]
summed = map(lambda x, y: x + y, list1, list2)
print(list(summed))  # [11, 22, 33]
```

---

## Higher-Order Functions

## Built-in Higher-Order Functions: filter()
- Select items from an iterable based on a function
- Returns iterator of items where function returns True
- Function should return a boolean value
- Lazy evaluation for efficiency
- Often replaced by list comprehensions

```python
# Get even numbers from a list
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
evens = filter(lambda x: x % 2 == 0, numbers)
print(list(evens))  # [2, 4, 6, 8, 10]

# Filter out None values
values = [0, None, "", False, 1, "hello", None, True]
non_none = filter(lambda x: x is not None, values)
print(list(non_none))  # [0, "", False, 1, "hello", True]

# Filter with a named function
def is_palindrome(s):
    s = s.lower()
    return s == s[::-1]

words = ["radar", "python", "level", "hello", "madam"]
palindromes = filter(is_palindrome, words)
print(list(palindromes))  # ["radar", "level", "madam"]
```

---

## Higher-Order Functions

## Built-in Higher-Order Functions: reduce()
- Apply a function cumulatively to all items
- Reduces an iterable to a single value
- Function takes two arguments (accumulator and item)
- Imported from functools module
- Powerful but sometimes less readable

```python
from functools import reduce

# Sum all numbers in a list
numbers = [1, 2, 3, 4, 5]
sum_result = reduce(lambda acc, x: acc + x, numbers)
print(sum_result)  # 15

# Find maximum value
max_value = reduce(lambda a, b: a if a > b else b, numbers)
print(max_value)  # 5

# Concatenate strings
words = ["Hello", ",", " ", "World", "!"]
sentence = reduce(lambda a, b: a + b, words)
print(sentence)  # "Hello, World!"

# With an initial value
product = reduce(lambda acc, x: acc * x, numbers, 10)
print(product)  # 1200 (10*1*2*3*4*5)
```

---

## Lambda Functions

## What Are Lambda Functions?
- Anonymous functions defined with `lambda` keyword
- Can be created without a name
- Limited to a single expression
- No statements allowed (if, for, etc.)
- Return the value of their expression
- Often used with higher-order functions

```python
# Named function
def add(a, b):
    return a + b

# Equivalent lambda function
add_lambda = lambda a, b: a + b

print(add(5, 3))       # 8
print(add_lambda(5, 3))  # 8

# Common use with sorting
pairs = [(1, 'one'), (3, 'three'), (2, 'two')]
pairs.sort(key=lambda pair: pair[1])  # Sort by second element
print(pairs)  # [(1, 'one'), (3, 'three'), (2, 'two')]
```

---

## Lambda Functions

## Lambda Limitations
- Single expression only
- Cannot contain statements
- Limited for complex logic
- May reduce readability for complex expressions
- Named functions often better for reusability
- Best for simple, throwaway functions

```python
# Good use of lambda
sorted_names = sorted(names, key=lambda name: name.lower())

# Poor use of lambda (complex logic)
complex_lambda = lambda x: x**2 if x > 0 else 0 if x == 0 else x**3

# Better as a named function
def complex_function(x):
    if x > 0:
        return x**2
    elif x == 0:
        return 0
    else:
        return x**3
```

---

## Lambda Functions

## When to Use Lambda Functions
- With higher-order functions (map, filter, reduce)
- As key functions (sorting, min, max)
- In GUI callbacks
- For simple data transformations
- One-off functions that aren't reused
- When function definition is simple and inline

```python
# With map
celsius = [0, 10, 20, 30, 40]
fahrenheit = list(map(lambda c: c * 9/5 + 32, celsius))

# As a key function
names = ["Alice", "Bob", "charlie", "Dave"]
sorted_names = sorted(names, key=lambda s: s.lower())

# With filter
numbers = list(range(-5, 6))
positives = list(filter(lambda x: x > 0, numbers))

# With reduce
from functools import reduce
numbers = [1, 2, 3, 4, 5]
factorial = reduce(lambda x, y: x * y, numbers)
```

---

## List Comprehensions

## Basic List Comprehensions
- Concise way to create lists based on existing lists
- More readable alternative to map and filter
- Creates a new list by applying an expression
- Can include conditions to filter elements
- Preferred over map+lambda in most Python code

```python
# Simple list comprehension
squares = [x**2 for x in range(10)]
print(squares)  # [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

# With filtering condition
even_squares = [x**2 for x in range(10) if x % 2 == 0]
print(even_squares)  # [0, 4, 16, 36, 64]

# Equivalent to map and filter
numbers = [1, 2, 3, 4, 5]
squared_evens = list(map(lambda x: x**2, filter(lambda x: x % 2 == 0, numbers)))
squared_evens_comp = [x**2 for x in numbers if x % 2 == 0]
print(squared_evens)      # [4, 16]
print(squared_evens_comp)  # [4, 16]
```

---

## List Comprehensions

## Nested List Comprehensions
- Create more complex transformations
- Equivalent to nested loops
- Can combine multiple iterables
- May become less readable with complexity
- Useful for matrix operations

```python
# Flatten a matrix
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flattened = [num for row in matrix for num in row]
print(flattened)  # [1, 2, 3, 4, 5, 6, 7, 8, 9]

# Create a matrix
matrix = [[i * j for j in range(1, 4)] for i in range(1, 4)]
print(matrix)  # [[1, 2, 3], [2, 4, 6], [3, 6, 9]]

# Cartesian product
colors = ['red', 'green', 'blue']
sizes = ['S', 'M', 'L']
combinations = [(color, size) for color in colors for size in sizes]
print(combinations)
# [('red', 'S'), ('red', 'M'), ('red', 'L'),
#  ('green', 'S'), ('green', 'M'), ('green', 'L'),
#  ('blue', 'S'), ('blue', 'M'), ('blue', 'L')]
```

---

## Other Comprehensions

## Dictionary Comprehensions
- Create dictionaries from iterables
- Similar syntax to list comprehensions
- Use curly braces with key:value pairs
- Efficient way to transform dictionaries

```python
# Basic dictionary comprehension
squares_dict = {x: x**2 for x in range(6)}
print(squares_dict)  # {0: 0, 1: 1, 2: 4, 3: 9, 4: 16, 5: 25}

# Filter items during creation
even_squares = {x: x**2 for x in range(10) if x % 2 == 0}
print(even_squares)  # {0: 0, 2: 4, 4: 16, 6: 36, 8: 64}

# Transform an existing dictionary
prices = {'apple': 0.5, 'banana': 0.3, 'orange': 0.6}
double_prices = {fruit: price * 2 for fruit, price in prices.items()}
print(double_prices)  # {'apple': 1.0, 'banana': 0.6, 'orange': 1.2}

# Create from two lists
fruits = ['apple', 'banana', 'orange']
counts = [3, 6, 4]
fruit_inventory = {fruit: count for fruit, count in zip(fruits, counts)}
print(fruit_inventory)  # {'apple': 3, 'banana': 6, 'orange': 4}
```

---

## Other Comprehensions

## Set Comprehensions
- Create sets from iterables
- Automatically removes duplicates
- Similar syntax to list comprehensions
- Uses curly braces without key:value pairs

```python
# Basic set comprehension
square_set = {x**2 for x in range(10)}
print(square_set)  # {0, 1, 4, 9, 16, 25, 36, 49, 64, 81}

# With filtering
even_squares = {x**2 for x in range(10) if x % 2 == 0}
print(even_squares)  # {0, 4, 16, 36, 64}

# Removing duplicates from a list
numbers = [1, 2, 2, 3, 3, 3, 4, 4, 5]
unique = {x for x in numbers}
print(unique)  # {1, 2, 3, 4, 5}

# Character set from a string
text = "hello world"
chars = {c for c in text if c.isalpha()}
print(chars)  # {'d', 'e', 'h', 'l', 'o', 'r', 'w'}
```

---

## Other Comprehensions

## Generator Expressions
- Like list comprehensions but lazy (on-demand)
- Use parentheses instead of brackets
- Don't create the entire result at once
- More memory efficient for large datasets
- Can be used as function arguments directly

```python
# List comprehension (eager)
squares_list = [x**2 for x in range(1000000)]  # Creates full list in memory

# Generator expression (lazy)
squares_gen = (x**2 for x in range(1000000))  # Creates generator object

# Memory usage comparison
import sys
print(sys.getsizeof(squares_list))  # Large (8+ MB)
print(sys.getsizeof(squares_gen))   # Small (112 bytes)

# Using generator expression with sum
total = sum(x**2 for x in range(1000))  # No need for extra parentheses
print(total)  # 332833500

# Processing large files with generator expressions
with open('large_file.txt') as file:
    line_lengths = (len(line.strip()) for line in file)
    avg_length = sum(line_lengths) / 1000  # Efficient processing
```

---

## Iterators and Generators

## Understanding Iterators
- Objects that implement the iterator protocol
- Must have `__iter__()` and `__next__()` methods
- Used in for loops and comprehensions
- Consumed as they are iterated over
- Enable lazy evaluation

```python
# Creating an iterator from an iterable
numbers = [1, 2, 3, 4, 5]
iter_numbers = iter(numbers)

# Manual iteration with next()
print(next(iter_numbers))  # 1
print(next(iter_numbers))  # 2
print(next(iter_numbers))  # 3

# Iteration continues where it left off
for num in iter_numbers:
    print(num)  # 4, 5

# After full iteration, StopIteration is raised
try:
    next(iter_numbers)
except StopIteration:
    print("Iterator exhausted")
```

---

## Iterators and Generators

## Custom Iterator Classes
- Implement iterator protocol directly
- Define `__iter__` and `__next__` methods
- Control the iteration behavior
- Hold internal state between calls to next()
- Raise StopIteration when done

```python
class Countdown:
    def __init__(self, start):
        self.start = start

    def __iter__(self):
        # Iterator objects should return themselves
        return self

    def __next__(self):
        if self.start <= 0:
            raise StopIteration
        self.start -= 1
        return self.start + 1

# Using the custom iterator
for num in Countdown(5):
    print(num)  # 5, 4, 3, 2, 1

# Manual iteration
counter = Countdown(3)
print(next(counter))  # 3
print(next(counter))  # 2
print(next(counter))  # 1
# next(counter) would raise StopIteration
```

---

## Iterators and Generators

## Generator Functions
- Functions that use `yield` instead of `return`
- Automatically implement iterator protocol
- Maintain state between yields
- Resume execution from where they left off
- Simpler than custom iterator classes

```python
def countdown(n):
    while n > 0:
        yield n
        n -= 1

# Using the generator function
for num in countdown(5):
    print(num)  # 5, 4, 3, 2, 1

# Creating a generator object
counter = countdown(3)
print(next(counter))  # 3
print(next(counter))  # 2
print(next(counter))  # 1
# next(counter) would raise StopIteration

# Materializing all values
print(list(countdown(5)))  # [5, 4, 3, 2, 1]
```

---

## Iterators and Generators

## The Difference Between Iterators and Generators
- Iterators: objects implementing iterator protocol
- Generators: special iterators created with yield
- Generators automatically implement iterator protocol
- Generators maintain local state between yields
- Both enable laziness and on-demand computation

```python
# Custom iterator class
class CountUpTo:
    def __init__(self, max_value):
        self.max_value = max_value
        self.current = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.current > self.max_value:
            raise StopIteration
        self.current += 1
        return self.current - 1

# Equivalent generator function
def count_up_to(max_value):
    current = 0
    while current <= max_value:
        yield current
        current += 1

# Both work the same way
iter1 = CountUpTo(3)
iter2 = count_up_to(3)

for i in iter1:
    print(i, end=" ")  # 0 1 2 3

print()

for i in iter2:
    print(i, end=" ")  # 0 1 2 3
```

---

## Iterators and Generators

## Generator Features
- State is preserved between yield statements
- Local variables retain their values
- Execution pauses and resumes with each next() call
- Can receive values with generator.send()
- Can be closed with generator.close()

```python
def echo_generator():
    value = yield "Ready for input"
    while True:
        value = yield f"You said: {value}"

gen = echo_generator()
print(next(gen))           # Ready for input
print(gen.send("Hello"))   # You said: Hello
print(gen.send("Python"))  # You said: Python

# Early termination
gen.close()
try:
    next(gen)
except StopIteration:
    print("Generator closed")
```

---

## Iterators and Generators

## Advanced Generator Features: send(), throw(), close()
- `send()`: Pass values back into generator
- `throw()`: Raise exception inside generator
- `close()`: Stop generator execution
- Enable two-way communication
- Create coroutine-like behavior

```python
def echo():
    print("Generator started")
    while True:
        value = yield
        print(f"Received: {value}")

# Using send
gen = echo()
next(gen)  # Prime the generator
gen.send("Hello")  # Received: Hello
gen.send("World")  # Received: World

# Using throw
def handle_exceptions():
    try:
        while True:
            try:
                value = yield
                print(f"Got: {value}")
            except ValueError:
                print("Caught ValueError inside generator")
    finally:
        print("Generator exiting")

gen = handle_exceptions()
next(gen)  # Prime the generator
gen.send("Hello")  # Got: Hello
gen.throw(ValueError)  # Caught ValueError inside generator
gen.close()  # Generator exiting
```

---

## Iterators and Generators

## Generator Expressions vs Generator Functions
- Generator expressions: for simple cases
- Generator functions: for complex logic
- Generator functions can have multiple yields
- Generator functions allow more control
- Both are memory-efficient

```python
# Generator expression - simple
squares_gen = (x**2 for x in range(10))

# Generator function - complex
def squares_func(n):
    print("Starting generation")
    for i in range(n):
        print(f"About to yield {i}^2")
        yield i**2
        print(f"Continuing after yield {i}^2")
    print("Generation complete")

# The function allows more control and side effects
for sq in squares_func(5):
    print(f"Got value: {sq}")
```

---

## Iterators and Generators

## Infinite Generators
- Generators that never stop yielding values
- No predefined end point
- Must be limited externally
- Useful for mathematical sequences
- Memory-efficient representation of infinite series

```python
def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

# Using an infinite generator safely
fib = fibonacci()
for _ in range(10):
    print(next(fib), end=" ")  # 0 1 1 2 3 5 8 13 21 34

# Using itertools to limit
import itertools
first_10_fibs = list(itertools.islice(fibonacci(), 10))
print(first_10_fibs)  # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
```

---

## Iterators and Generators

## Generator Pipelines
- Connect generators to process data in stages
- Each stage transforms data from previous stage
- Memory-efficient for processing large datasets
- Similar to Unix pipes
- Process one item at a time through entire pipeline

```python
def read_large_file(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            yield line.strip()

def grep(pattern, lines):
    for line in lines:
        if pattern in line:
            yield line

def count_words(lines):
    for line in lines:
        yield len(line.split())

# Pipeline to process a large log file
file_lines = read_large_file('large_log.txt')
error_lines = grep('ERROR', file_lines)
word_counts = count_words(error_lines)

total_words = sum(word_counts)
print(f"Total words in error lines: {total_words}")
```

---

## The itertools Module

## Overview of itertools
- Library of fast, memory-efficient iterator tools
- Functions for creating and working with iterators
- Inspired by functional programming constructs
- Building blocks for iterator algebra
- Enables advanced iterator manipulation

```python
import itertools

# Count indefinitely
counter = itertools.count(10, 2)  # Start at 10, step by 2
for i in itertools.islice(counter, 5):
    print(i)  # 10, 12, 14, 16, 18

# Cycle through elements
cycler = itertools.cycle(['red', 'green', 'blue'])
for i in range(7):
    print(next(cycler))  # red, green, blue, red, green, blue, red

# Repeat an element
repeater = itertools.repeat('hello', 3)
for item in repeater:
    print(item)  # hello, hello, hello
```

---

## The itertools Module

## Combining Iterables
- `chain()`: Concatenate iterables
- `zip_longest()`: Zip with fill value for uneven lengths
- `product()`: Cartesian product
- Efficient alternatives to nested loops

```python
import itertools

# Chain multiple iterables
numbers = list(itertools.chain([1, 2, 3], [4, 5], [6, 7, 8]))
print(numbers)  # [1, 2, 3, 4, 5, 6, 7, 8]

# Zip with longer iterable
for pair in itertools.zip_longest([1, 2], ['a', 'b', 'c'], fillvalue=0):
    print(pair)  # (1, 'a'), (2, 'b'), (0, 'c')

# Cartesian product
products = list(itertools.product([1, 2], ['a', 'b']))
print(products)  # [(1, 'a'), (1, 'b'), (2, 'a'), (2, 'b')]

# Nested cartesian product
deck = list(itertools.product(
    ['Hearts', 'Diamonds', 'Clubs', 'Spades'],
    ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
))
print(len(deck))  # 52 (complete deck of cards)
```

---

## The itertools Module

## Filtering and Slicing
- `islice()`: Slice iterators
- `takewhile()`: Take items while condition is true
- `dropwhile()`: Drop items while condition is true
- `filterfalse()`: Opposite of filter()

```python
import itertools

# Slice an iterator
numbers = range(10)
evens = list(itertools.islice(numbers, 0, 10, 2))
print(evens)  # [0, 2, 4, 6, 8]

# Take items while condition is true
data = [1, 2, 3, 4, 0, 5, 6, 0, 7]
result = list(itertools.takewhile(lambda x: x > 0, data))
print(result)  # [1, 2, 3, 4]

# Drop items while condition is true
data = [0, 0, 0, 1, 2, 3, 0, 4]
result = list(itertools.dropwhile(lambda x: x == 0, data))
print(result)  # [1, 2, 3, 0, 4]

# Filter false values
data = [0, 1, 2, 0, 3, 0, 4]
result = list(itertools.filterfalse(bool, data))
print(result)  # [0, 0, 0]
```

---

## The itertools Module

## Combinatoric Generators
- `combinations()`: r-length tuples, no repeated elements
- `permutations()`: r-length tuples, all possible orderings
- `combinations_with_replacement()`: r-length tuples with repeated elements
- Memory-efficient alternatives to nested loops

```python
import itertools

# Generate all combinations
result = list(itertools.combinations([1, 2, 3, 4], 2))
print(result)  # [(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)]

# Generate all permutations
result = list(itertools.permutations([1, 2, 3], 2))
print(result)  # [(1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2)]

# Combinations with replacement
result = list(itertools.combinations_with_replacement([1, 2, 3], 2))
print(result)  # [(1, 1), (1, 2), (1, 3), (2, 2), (2, 3), (3, 3)]

# Example: Generate a poker hand
import random
deck = list(itertools.product(
    ['Hearts', 'Diamonds', 'Clubs', 'Spades'],
    ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
))
hand = random.sample(deck, 5)
print(hand)  # 5 random cards
```

---

## The functools Module

## Overview of functools
- Higher-order functions and operations on callables
- Tools for functional programming
- Function decoration utilities
- Function combination and transformation
- Caching and memoization

```python
import functools

# Partial function application
base_10 = functools.partial(int, base=10)
base_2 = functools.partial(int, base=2)
base_16 = functools.partial(int, base=16)

print(base_10('42'))    # 42
print(base_2('101010'))  # 42
print(base_16('2A'))     # 42

# Caching function results
@functools.lru_cache(maxsize=None)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

print(fibonacci(30))  # Fast because of caching
```

---

## The functools Module

## Partial Function Application
- `partial()`: Fix a subset of arguments
- Creates a new function with pre-set arguments
- Useful for callback interfaces
- Simplifies complex parameter sets
- Enables function specialization

```python
import functools

# Original function
def power(base, exponent):
    return base ** exponent

# Create specialized functions
square = functools.partial(power, exponent=2)
cube = functools.partial(power, exponent=3)
power_of_2 = functools.partial(power, base=2)

print(square(4))     # 16
print(cube(3))       # 27
print(power_of_2(8))  # 256

# Partial with positional arguments
def log(message, level='INFO'):
    print(f"[{level}] {message}")

debug = functools.partial(log, level='DEBUG')
error = functools.partial(log, level='ERROR')

debug("Starting process")  # [DEBUG] Starting process
error("Process failed")    # [ERROR] Process failed
```

---

## The functools Module

## Function Decoration with functools.wraps
- Preserves metadata when decorating functions
- Copies __name__, __doc__, and other attributes
- Makes debugging and introspection easier
- Essential for writing proper decorators

```python
import functools

def my_decorator(func):
    @functools.wraps(func)  # Preserves metadata
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned {result}")
        return result
    return wrapper

@my_decorator
def add(a, b):
    """Add two numbers and return the result."""
    return a + b

# Metadata is preserved
print(add.__name__)  # add (not wrapper)
print(add.__doc__)   # Add two numbers and return the result.

# Without functools.wraps, we would see:
# __name__ = wrapper
# __doc__ = None
```

---

## The functools Module

## Caching with lru_cache
- Memoizes function calls
- Avoids recomputation of expensive calls
- Configurable cache size
- Tracks hits and misses
- Perfect for recursive or repeated calculations

```python
import functools
import time

# Without caching
def fibonacci_slow(n):
    if n < 2:
        return n
    return fibonacci_slow(n-1) + fibonacci_slow(n-2)

# With caching
@functools.lru_cache(maxsize=None)
def fibonacci_fast(n):
    if n < 2:
        return n
    return fibonacci_fast(n-1) + fibonacci_fast(n-2)

# Performance comparison
start = time.time()
fibonacci_slow(30)
slow_time = time.time() - start

start = time.time()
fibonacci_fast(30)
fast_time = time.time() - start

print(f"Slow: {slow_time:.6f}s, Fast: {fast_time:.6f}s")
print(f"Speedup: {slow_time / fast_time:.1f}x")

# Cache statistics
print(fibonacci_fast.cache_info())
```

---

## The functools Module

## Function Composition with reduce
- Powerful tool for combining functions
- Apply operations sequentially
- Build complex transformations
- Enables functional composition patterns

```python
import functools

# Compose multiple functions
def compose(*functions):
    def composed_function(x):
        result = x
        for func in reversed(functions):
            result = func(result)
        return result
    return composed_function

# Example functions
def double(x): return x * 2
def increment(x): return x + 1
def square(x): return x * x

# Create composed functions
f = compose(square, increment, double)  # square(increment(double(x)))
g = compose(double, square, increment)  # double(square(increment(x)))

print(f(5))  # 121: square(increment(double(5))) = square(increment(10)) = square(11) = 121
print(g(5))  # 72: double(square(increment(5))) = double(square(6)) = double(36) = 72
```

---

## Understanding Closures

## What Are Closures?
- Functions that remember their surrounding scope
- Inner functions that capture outer variables
- Retain access to variables even after outer function returns
- Fundamental concept in functional programming
- Building block for many advanced patterns

```python
def create_counter(start=0):
    # 'count' is a free variable captured by the closure
    count = start

    def increment():
        nonlocal count  # Need nonlocal to modify captured variable
        count += 1
        return count

    return increment

counter1 = create_counter(10)
counter2 = create_counter()

print(counter1())  # 11
print(counter1())  # 12
print(counter2())  # 1
print(counter2())  # 2
print(counter1())  # 13 (counter1 maintains its own state)
```

---

## Understanding Closures

## How Closures Work
- Inner function captures references to variables in outer scope
- Python creates a "cell" object for each captured variable
- These cells are stored in the function's `__closure__` attribute
- The closure remembers the cells, not the values
- Allows the inner function to access and modify captured variables

```python
def make_multiplier(factor):
    # 'factor' is captured in the closure
    def multiply(x):
        return x * factor

    # Examine the closure
    print(f"Closure cells: {multiply.__closure__}")
    print(f"Cell contents: {multiply.__closure__[0].cell_contents}")

    return multiply

double = make_multiplier(2)
triple = make_multiplier(3)

print(double(5))  # 10
print(triple(5))  # 15

# Each function has its own closure with different captured values
print(f"double closure: {double.__closure__[0].cell_contents}")  # 2
print(f"triple closure: {triple.__closure__[0].cell_contents}")  # 3
```

---

## Understanding Closures

## Variables Are Captured by Reference
- Closures capture references, not values
- Changes to variables after closure creation can affect behavior
- Closures capture the variables, not their values at definition time
- Common source of confusion and bugs

```python
def create_multipliers():
    multipliers = []

    # This doesn't work as expected
    for i in range(1, 4):
        multipliers.append(lambda x: x * i)

    return multipliers

m1, m2, m3 = create_multipliers()
# All use the final value of i (3)
print(m1(10))  # 30, not 10 as might be expected
print(m2(10))  # 30, not 20 as might be expected
print(m3(10))  # 30

# Fixing the issue by binding i to a default parameter
def create_multipliers_fixed():
    multipliers = []

    for i in range(1, 4):
        multipliers.append(lambda x, i=i: x * i)  # i=i binds current i value

    return multipliers

m1, m2, m3 = create_multipliers_fixed()
print(m1(10))  # 10
print(m2(10))  # 20
print(m3(10))  # 30
```

---

## The Problem of Mutable Default Arguments

## Understanding the Issue
- Default argument values are evaluated once at function definition
- Mutable defaults (lists, dicts, etc.) are created only once
- All function calls share the same default object
- Changes to the default persist between calls
- Common source of bugs for Python newcomers

```python
# Problematic function with mutable default
def append_to(item, lst=[]):
    lst.append(item)
    return lst

print(append_to(1))  # [1]
print(append_to(2))  # [1, 2] - Not a fresh empty list!
print(append_to(3))  # [1, 2, 3] - Shared state between calls

# What's happening:
# The list is created once when the function is defined
# All calls to append_to without a list argument share the same list

# View the default argument
print(append_to.__defaults__)  # ([1, 2, 3],)
```

---

## The Problem of Mutable Default Arguments

## The Solution: None Default
- Use `None` as default and create a new object in the function
- This is a common Python idiom
- Ensures a fresh mutable object for each call
- Explicit, clear, and safe

```python
# Correct approach
def append_to_fixed(item, lst=None):
    if lst is None:
        lst = []  # Create a new list each time when default is used
    lst.append(item)
    return lst

print(append_to_fixed(1))  # [1]
print(append_to_fixed(2))  # [2] - Fresh list each time
print(append_to_fixed(3))  # [3] - No shared state

# Can still pass in a list to append to
my_list = [10, 20]
print(append_to_fixed(30, my_list))  # [10, 20, 30]
print(my_list)  # [10, 20, 30] - Same list is modified
```

---

## Applying Functional Concepts

## Pure Functions
- Always return the same result for same arguments
- No side effects (no I/O, no global state changes)
- Easier to test, debug, and reason about
- Can be called in any order or context
- Enable better optimization and parallelization

```python
# Impure function - uses global state
counter = 0
def impure_increment(x):
    global counter
    counter += 1
    return x + counter

# Impure function - side effect
def impure_print(x):
    print(x)  # Side effect - I/O
    return x

# Pure function
def pure_add(x, y):
    return x + y  # Always same result for same inputs, no side effects

# Pure function with internal calculation
def pure_factorial(n):
    if n <= 1:
        return 1
    return n * pure_factorial(n - 1)  # Recursive but pure

# Testing determinism of pure function
print(pure_add(2, 3))  # 5
print(pure_add(2, 3))  # 5 - Same inputs, same output always
```

---

## Applying Functional Concepts

## Immutable Data Structures
- Avoid modifying data in place
- Create new objects rather than changing existing ones
- Use tuples, frozensets, and namedtuples
- More predictable, thread-safe code
- Easier to reason about program state

```python
# Mutable approach
def add_item_mutable(item, lst):
    lst.append(item)  # Modifies the input list
    return lst

# Immutable approach
def add_item_immutable(item, lst):
    return lst + [item]  # Creates a new list

# Example usage
original = [1, 2, 3]

# Mutable version modifies original
result1 = add_item_mutable(4, original)
print(original)  # [1, 2, 3, 4] - Original is changed
print(result1)   # [1, 2, 3, 4] - Same object

# Reset for immutable example
original = [1, 2, 3]

# Immutable version preserves original
result2 = add_item_immutable(4, original)
print(original)  # [1, 2, 3] - Original unchanged
print(result2)   # [1, 2, 3, 4] - New object
```

---

## Advanced Functional Techniques

## Decorators
- Higher-order functions that modify other functions
- Add functionality without changing the original function
- Common for cross-cutting concerns
- Enable aspect-oriented programming in Python
- Powerful way to apply functional composition

```python
# Basic decorator
def log_calls(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__} with {args}, {kwargs}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned {result}")
        return result
    return wrapper

# Apply decorator with @ syntax
@log_calls
def add(a, b):
    return a + b

# Equivalent to: add = log_calls(add)
add(2, 3)
# Output:
# Calling add with (2, 3), {}
# add returned 5

# Decorator with arguments
def repeat(n):
    def decorator(func):
        def wrapper(*args, **kwargs):
            result = None
            for _ in range(n):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(3)
def say_hello(name):
    print(f"Hello, {name}!")
    return name

say_hello("Alice")  # Prints "Hello, Alice!" three times
```

---

## Advanced Functional Techniques

## Currying and Partial Application
- Transform a function that takes multiple arguments into a sequence of functions
- Fix some arguments of a function, creating a new function
- Specialize general functions for specific use cases
- Similar to currying in other functional languages

```python
# Manual currying
def curry_add(a):
    def add_b(b):
        def add_c(c):
            return a + b + c
        return add_c
    return add_b

# Usage
add_1 = curry_add(1)      # Function that adds 1 to (b+c)
add_1_2 = add_1(2)        # Function that adds 1+2 to c
result = add_1_2(3)       # 1 + 2 + 3 = 6
print(result)             # 6

# Using functools.partial for partial application
from functools import partial

def power(base, exponent):
    return base ** exponent

# Create specialized functions
square = partial(power, exponent=2)
cube = partial(power, exponent=3)

print(square(4))  # 16
print(cube(3))    # 27
```

---

## Practical Examples

## Example: Data Processing Pipeline
```python
# Process a list of data records functionally

# Sample data: user records with potential issues
users = [
    {"id": 1, "name": "Alice", "email": "alice@example.com"},
    {"id": 2, "name": "", "email": "bob@example.com"},
    {"id": 3, "name": "Charlie", "email": "invalid-email"},
    {"id": 4, "name": "Dave", "email": "dave@example.com"},
    {"id": None, "name": "Eve", "email": "eve@example.com"}
]

# Pure validation functions
def has_valid_id(user):
    return user["id"] is not None

def has_name(user):
    return user["name"] and len(user["name"]) > 0

def has_valid_email(user):
    return "@" in user["email"] and "." in user["email"]

# Transformation function
def normalize_user(user):
    return {
        "id": user["id"],
        "name": user["name"].strip(),
        "email": user["email"].lower(),
        "display_name": user["name"] or "Anonymous"
    }

# Functional pipeline
valid_users = (
    filter(has_valid_id, users) |
    filter(has_name) |
    filter(has_valid_email) |
    map(normalize_user)
)

# Process the results
for user in valid_users:
    print(f"Valid user: {user['id']} - {user['name']} ({user['email']})")
```

---

## Practical Examples

## Example: Event Stream Processing
```python
# Simulate processing an event stream functionally

# Sample event data
events = [
    {"type": "LOGIN", "user_id": 123, "timestamp": 1623423421},
    {"type": "VIEW", "user_id": 123, "page": "home", "timestamp": 1623423422},
    {"type": "CLICK", "user_id": 123, "element": "button", "timestamp": 1623423426},
    {"type": "LOGIN", "user_id": 456, "timestamp": 1623423430},
    {"type": "VIEW", "user_id": 456, "page": "products", "timestamp": 1623423435},
    {"type": "LOGOUT", "user_id": 123, "timestamp": 1623423437},
    {"type": "VIEW", "user_id": 456, "page": "cart", "timestamp": 1623423440},
    {"type": "PURCHASE", "user_id": 456, "amount": 125.99, "timestamp": 1623423447}
]

# Event processors (pure functions)
def filter_by_type(events, event_type):
    return filter(lambda e: e["type"] == event_type, events)

def get_user_sessions(events):
    # Group events by user_id
    sessions = {}
    for event in events:
        user_id = event["user_id"]
        if user_id not in sessions:
            sessions[user_id] = []
        sessions[user_id].append(event)
    return sessions

def calculate_session_duration(events):
    if not events:
        return 0
    # Find first and last event timestamps
    timestamps = [event["timestamp"] for event in events]
    return max(timestamps) - min(timestamps)

# Process the event stream
user_sessions = get_user_sessions(events)

# Calculate statistics
session_stats = {
    user_id: {
        "events": len(events),
        "duration": calculate_session_duration(events),
        "purchases": len(list(filter_by_type(events, "PURCHASE")))
    }
    for user_id, events in user_sessions.items()
}

# Output results
for user_id, stats in session_stats.items():
    print(f"User {user_id}: {stats['events']} events, "
          f"{stats['duration']} seconds, {stats['purchases']} purchases")
```

---

## Summary

## Key Takeaways
- Python has strong support for functional programming
- Functions are first-class objects
- Higher-order functions enable powerful abstractions
- List comprehensions and generator expressions are concise and efficient
- Closures provide state encapsulation
- Immutability and pure functions improve code quality
- Mix functional concepts with Python's pragmatic approach

---

## Further Reading

## Resources for Functional Python
- "Functional Programming in Python" by David Mertz
- "Python Cookbook" by David Beazley and Brian K. Jones
- "Fluent Python" by Luciano Ramalho
- "Functional Python Programming" by Steven Lott
- Standard library modules: functools, itertools, operator
- Third-party libraries: toolz, funcy, more-itertools
