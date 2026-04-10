# Idiomatic Python

## Overview
- Writing pythonic code
- Using Python as it was designed
- Leveraging language-specific features and idioms
- Moving beyond "translated" code from other languages

---

## Idiomatic Python Patterns

![Idiomatic Python patterns overview](svg/courses/languages/python/advanced-python/02_idiomatic_python/idiomatic_patterns.svg)

---

## What is Idiomatic Python?

## Pythonic Code
- Clear, readable, and maintainable
- Follows community conventions
- Leverages Python's built-in features
- Expresses intent directly and concisely
- "There should be one-- and preferably only one --obvious way to do it"

---

## What is Idiomatic Python?

## Recognizing Non-Idiomatic Code
- Resembles code from other languages (C, Java, etc.)
- Unnecessarily verbose
- Reinvents built-in functionality
- Ignores Python's strengths
- Feels awkward to experienced Python developers

---

## Why Write Idiomatic Python?

## Benefits
- More readable by Python developers
- Typically more concise
- Often more efficient
- Easier to maintain
- Leverages Python ecosystem better
- More predictable behavior

---

## Idiomatic Data Structures

## Choosing the Right Container
- Lists: Ordered, mutable sequence of items
- Tuples: Immutable sequence of related items
- Sets: Unordered collection of unique items
- Dictionaries: Key-value mappings
- Strings: Sequence of characters (immutable)
- `collections` module for specialized containers

---

## Idiomatic Data Structures

## Lists: When to Use
- When order matters
- When items need to be modified
- For homogeneous collections
- When you need to grow/shrink dynamically

```python
# Idiomatic list operations
names = ["Alice", "Bob", "Charlie"]
names.append("Dave")
names.extend(["Eve", "Frank"])
first_two = names[:2]
```

---

## Idiomatic Data Structures

## Tuples: When to Use
- For immutable sequences
- To group related values
- As dictionary keys (when needed)
- For heterogeneous data with positional meaning

```python
# Tuple as a record
person = ("Alice", 30, "Engineer")
name, age, role = person  # Unpacking

# Tuple as a dictionary key
locations = {(40.7128, -74.0060): "New York City"}
```

---

## Idiomatic Data Structures

## Sets: When to Use
- When uniqueness matters
- For membership testing
- For mathematical set operations
- When order is irrelevant

```python
# Idiomatic set operations
users_a = {"Alice", "Bob", "Charlie"}
users_b = {"Bob", "Charlie", "Dave"}

all_users = users_a | users_b
common_users = users_a & users_b
unique_to_a = users_a - users_b
```

---

## Idiomatic Data Structures

## Dictionaries: When to Use
- For key-value associations
- For lookups by key
- For storing object properties
- For frequency counting

```python
# Idiomatic dictionary usage
user = {
    "name": "Alice",
    "age": 30,
    "roles": ["admin", "user"]
}

# Get with default
role = user.get("department", "Engineering")

# Dictionary comprehension
squares = {x: x**2 for x in range(10)}
```

---

## Idiomatic Data Structures

## Frozen Structures
- Immutable versions of mutable collections
- Better for caching, hashing, and thread safety
- Less prone to accidental mutation
- Available for most collection types

```python
# Frozen set
unique_ids = frozenset([1, 2, 3, 4])

# Named tuple (immutable with field names)
from collections import namedtuple
Point = namedtuple("Point", ["x", "y"])
p = Point(10, 20)
print(p.x, p.y)  # 10 20
```

---

## Idiomatic Data Structures

## Named Tuples
- Immutable, field-accessible records
- More memory-efficient than classes
- Self-documenting with field names
- Supports all tuple operations

```python
from collections import namedtuple

# Define a named tuple type
Student = namedtuple("Student", ["name", "id", "gpa"])

# Create instances
alice = Student("Alice", 12345, 3.9)
print(f"{alice.name} has GPA {alice.gpa}")

# Unpack like regular tuples
name, id_num, gpa = alice
```

---

## Idiomatic Data Structures

## Data Classes (Python 3.7+)
- Class-based data containers
- Automatically generated methods
- Mutable by default, can be frozen
- Type hints support

```python
from dataclasses import dataclass

@dataclass(frozen=True)  # Immutable version
class Point:
    x: float
    y: float

    def distance_from_origin(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5

p = Point(3.0, 4.0)
print(p.distance_from_origin())  # 5.0
```

---

## Idiomatic Data Structures

## Specialized Collections
- `collections.defaultdict`: Dict with default factory
- `collections.Counter`: Dict for counting hashable objects
- `collections.deque`: Double-ended queue
- `collections.ChainMap`: Multiple dicts as a single mapping
- `collections.OrderedDict`: Dict that remembers insertion order (pre-3.7)

---

## Idiomatic Data Structures

## DefaultDict
- Dictionary with default values for missing keys
- No more KeyError or repetitive .get() with defaults
- Default value is determined by a factory function

```python
from collections import defaultdict

# Group words by first letter
words = ["apple", "banana", "cherry", "date", "apricot", "blueberry"]
by_letter = defaultdict(list)

for word in words:
    by_letter[word[0]].append(word)

# No need to check if key exists first
print(by_letter["a"])  # ["apple", "apricot"]
print(by_letter["z"])  # [] (empty list, no KeyError)
```

---

## Idiomatic Data Structures

## Counter
- Dictionary subclass for counting hashable objects
- Has specialized methods for counter operations
- Good for histograms, frequency analysis

```python
from collections import Counter

# Count occurrences of elements
colors = ["red", "blue", "red", "green", "blue", "blue"]
color_count = Counter(colors)

print(color_count)  # Counter({'blue': 3, 'red': 2, 'green': 1})
print(color_count["yellow"])  # 0 (not KeyError)
print(color_count.most_common(2))  # [('blue', 3), ('red', 2)]
```

---

## Idiomatic Data Structures

## Deque
- Double-ended queue
- Efficient appends and pops from both ends
- Thread-safe, memory-efficient
- Good for FIFO queues and sliding windows

```python
from collections import deque

# Create a queue with max length
history = deque(maxlen=3)
history.append("command1")
history.append("command2")
history.append("command3")
history.append("command4")  # Pushes out "command1"

print(list(history))  # ["command2", "command3", "command4"]
```

---

## Correct Use of Basic Features

## List Comprehensions
- Concise way to create lists
- Replace map/filter with clearer syntax
- Can include conditionals
- Often more readable than loops

```python
# Non-idiomatic
squares = []
for x in range(10):
    if x % 2 == 0:
        squares.append(x**2)

# Idiomatic
squares = [x**2 for x in range(10) if x % 2 == 0]
```

---

## Correct Use of Basic Features

## Dictionary Comprehensions
- Create dictionaries concisely
- Transform keys and values in one expression
- Filter with conditionals

```python
# Non-idiomatic
word_lengths = {}
for word in words:
    if len(word) > 2:
        word_lengths[word] = len(word)

# Idiomatic
word_lengths = {word: len(word) for word in words if len(word) > 2}
```

---

## Correct Use of Basic Features

## Set Comprehensions
- Create sets directly from iterables
- Apply transformations and filters

```python
# Non-idiomatic
unique_lengths = set()
for word in words:
    unique_lengths.add(len(word))

# Idiomatic
unique_lengths = {len(word) for word in words}
```

---

## Correct Use of Basic Features

## Generator Expressions
- Like list comprehensions but lazy (on-demand)
- More memory-efficient for large sequences
- Use parentheses instead of brackets

```python
# List comprehension (materializes entire list)
sum([x**2 for x in range(1000000)])  # Creates large list in memory

# Generator expression (evaluates on demand)
sum((x**2 for x in range(1000000)))  # No large list created
# or even simpler:
sum(x**2 for x in range(1000000))  # Parentheses can be omitted here
```

---

## Correct Use of Basic Features

## String Formatting
- f-strings (Python 3.6+)
- str.format() method
- Avoid + concatenation for complex strings

```python
name = "Alice"
age = 30

# Non-idiomatic (inefficient for multiple values)
greeting = "Hello, " + name + "! You are " + str(age) + " years old."

# Better (str.format)
greeting = "Hello, {}! You are {} years old.".format(name, age)

# Best (f-strings, Python 3.6+)
greeting = f"Hello, {name}! You are {age} years old."
```

---

## Correct Use of Basic Features

## Advanced f-strings (Python 3.8+)
- Self-documenting expressions with = specifier
- Format specifiers for precision, alignment
- Multiline f-strings

```python
import math
radius = 5

# Debug-friendly output with variable names
print(f"{radius=}")  # radius=5
print(f"{math.pi=:.3f}")  # math.pi=3.142

# Formatting options
print(f"{name:>10}")  # Right-aligned, width 10
print(f"{age:03d}")   # Zero-padded, 3 digits
```

---

## Correct Use of Basic Features

## Correct Iteration

## Range vs. Direct Iteration
- Iterate directly over containers when possible
- Use range only when you need the index numbers
- Use enumerate when you need both items and indices

```python
# Non-idiomatic (C-style)
for i in range(len(names)):
    print(names[i])

# Idiomatic (direct iteration)
for name in names:
    print(name)

# When you need indices too
for i, name in enumerate(names):
    print(f"{i}: {name}")
```

---

## Correct Use of Basic Features

## Enumerate
- Get index and value in one operation
- Can specify start index (default is 0)
- More readable than manual indexing

```python
# Create indexed output
for i, name in enumerate(names, start=1):
    print(f"Student #{i}: {name}")

# Create a dictionary mapping values to indices
position = {name: i for i, name in enumerate(names)}
```

---

## Correct Use of Basic Features

## Zip
- Combine multiple iterables in parallel
- Stops at the shortest iterable
- Use `zip_longest` from itertools for different behavior

```python
names = ["Alice", "Bob", "Charlie"]
scores = [85, 92, 78]

# Iterate through pairs
for name, score in zip(names, scores):
    print(f"{name} scored {score}")

# Create dictionary from two lists
name_to_score = dict(zip(names, scores))
```

---

## Correct Use of Basic Features

## Unpacking
- Destructure sequences into individual variables
- Works with any sequence type
- Use * for capturing multiple values

```python
# Basic unpacking
a, b, c = [1, 2, 3]
first, second = {"a": 1, "b": 2}  # Unpacks keys

# Extended unpacking (Python 3+)
first, *middle, last = [1, 2, 3, 4, 5]
print(first)   # 1
print(middle)  # [2, 3, 4]
print(last)    # 5
```

---

## Correct Use of Basic Features

## Multiple Assignment
- Assign to multiple variables at once
- Swap values without temporary variable
- Create and assign tuples implicitly

```python
# Multiple assignment
x, y = 10, 20

# Value swapping
x, y = y, x

# Return multiple values from function
def get_user_info():
    return "Alice", 30, "Engineer"

name, age, role = get_user_info()
```

---

## Correct Use of Basic Features

## Membership Testing
- Use `in` operator for membership tests
- Works with lists, tuples, strings, dicts, sets
- Most efficient with sets and dicts (O(1))

```python
# Non-idiomatic
found = False
for item in container:
    if item == target:
        found = True
        break

# Idiomatic
found = target in container

# With dictionaries
if key in my_dict:
    print(my_dict[key])
```

---

## Correct Use of Basic Features

## Truthiness Testing
- Use implicit boolean conversion
- Empty containers, 0, None, and False are falsy
- Everything else is truthy

```python
# Non-idiomatic
if len(items) > 0:
    process(items)

if count != 0:
    handle_count(count)

# Idiomatic
if items:
    process(items)

if count:
    handle_count(count)
```

---

## Correct Use of Basic Features

## The Walrus Operator (Python 3.8+)
- Assignment expressions with :=
- Assign and test in a single expression
- Avoid duplicate computation

```python
# Without walrus operator
data = get_data()
if data:
    process(data)

# With walrus operator
if data := get_data():
    process(data)

# In list comprehensions
results = [transform(x) for x in data if (y := condition(x))]
```

---

## Correct Use of Basic Libraries

## Collections Module
- Specialized container datatypes
- Extend functionality of built-in containers
- More efficient for specific use cases

```python
from collections import Counter, defaultdict, deque, namedtuple

# Word frequency counter
words = text.split()
word_counts = Counter(words)
most_common = word_counts.most_common(5)

# Multi-level default dictionary
tree = lambda: defaultdict(tree)
taxonomy = tree()
taxonomy["Animals"]["Mammals"]["Cats"] = ["Lion", "Tiger"]
```

---

## Correct Use of Basic Libraries

## Itertools Module
- Functions for efficient iteration
- Create iterators for efficient looping
- Combinatoric generators

```python
import itertools

# Infinite counter
for i in itertools.count(10, 2):
    if i > 20: break
    print(i)  # 10, 12, 14, 16, 18, 20

# Combinations
for combo in itertools.combinations([1, 2, 3, 4], 2):
    print(combo)  # (1,2), (1,3), (1,4), (2,3), (2,4), (3,4)

# Chain multiple iterables
for x in itertools.chain([1, 2], [3, 4]):
    print(x)  # 1, 2, 3, 4
```

---

## Correct Use of Basic Libraries

## Functools Module
- Higher-order functions and operations on callable objects
- Partial function application
- Function caching

```python
import functools

# Caching function results
@functools.lru_cache(maxsize=None)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# Partial functions
base_converter = lambda x, base: int(x, base)
hex_to_int = functools.partial(base_converter, base=16)
```

---

## Correct Use of Basic Libraries

## Operator Module
- Function equivalents of Python's operators
- Useful with functional programming tools
- Cleaner alternative to lambdas in many cases

```python
import operator

# Instead of lambda functions
sorted(people, key=lambda p: p.age)  # With lambda
sorted(people, key=operator.attrgetter("age"))  # With operator

# Summing a specific field
sum(map(lambda p: p.salary, employees))  # With lambda
sum(map(operator.attrgetter("salary"), employees))  # With operator
```

---

## Correct Use of Basic Libraries

## Pathlib Module (Python 3.4+)
- Object-oriented filesystem paths
- Replaces os.path with a cleaner API
- Methods for common operations

```python
from pathlib import Path

# Create path objects
data_dir = Path("data")
file_path = data_dir / "input.txt"  # Path joining

# Common operations
if file_path.exists():
    with file_path.open() as f:
        content = f.read()

# Pattern matching
python_files = list(data_dir.glob("**/*.py"))
```

---

## Correct Use of Basic Libraries

## Context Managers (with statement)
- Automatic resource management
- Ensures cleanup code runs
- Built-in for files, locks, etc.

```python
# File handling with automatic close
with open("data.txt", "r") as f:
    content = f.read()
    # File is automatically closed after block

# Multiple context managers
with open("input.txt") as infile, open("output.txt", "w") as outfile:
    outfile.write(infile.read().upper())
```

---

## Idiomatic Error Handling

## Try-Except
- Easier to ask forgiveness than permission (EAFP)
- Handle exceptions, not prevent them
- Be specific about which exceptions to catch

```python
# Non-idiomatic (look before you leap)
if os.path.exists(filename):
    with open(filename) as f:
        data = f.read()
else:
    data = ""

# Idiomatic (EAFP)
try:
    with open(filename) as f:
        data = f.read()
except FileNotFoundError:
    data = ""
```

---

## Idiomatic Error Handling

## Else and Finally
- `else`: Runs when no exception occurs
- `finally`: Always runs, regardless of exceptions
- Separate normal flow from error handling

```python
try:
    result = perform_calculation(x, y)
except ZeroDivisionError:
    print("Cannot divide by zero")
    result = None
else:
    # Only runs if no exception occurred
    print(f"Calculation successful: {result}")
finally:
    # Always runs
    cleanup_resources()
```

---

## Replacing Common Patterns

## Dictionary Get with Default
- Use get() with default instead of checking existence
- More concise, avoids repetition

```python
# Non-idiomatic
if key in my_dict:
    value = my_dict[key]
else:
    value = default_value

# Idiomatic
value = my_dict.get(key, default_value)
```

---

## Replacing Common Patterns

## Dictionary Update Patterns
- Use dictionary methods for updates
- More concise than conditionals

```python
# Non-idiomatic
if key in counter:
    counter[key] += 1
else:
    counter[key] = 1

# Idiomatic options:
counter[key] = counter.get(key, 0) + 1
# Or better:
counter.setdefault(key, 0)
counter[key] += 1
# Or best:
from collections import Counter
counter = Counter()
counter[key] += 1  # Already handles missing keys
```

---

## Replacing Common Patterns

## Sorting
- Use `sorted()` with key function
- Use `list.sort()` for in-place sorting
- Customize with key parameter

```python
# Sort by name
sorted(people, key=lambda p: p.name)

# Sort by multiple criteria
sorted(people, key=lambda p: (p.age, p.name))

# Reverse sort
sorted(scores, reverse=True)

# Case-insensitive sort
sorted(words, key=str.lower)
```

---

## Replacing Common Patterns

## Grouping Data
- Use defaultdict or itertools.groupby
- Create hierarchical structures easily

```python
# Group people by department
from collections import defaultdict
by_dept = defaultdict(list)
for person in people:
    by_dept[person.department].append(person)

# With itertools (data must be sorted first)
import itertools
people.sort(key=lambda p: p.department)
for dept, group in itertools.groupby(people, key=lambda p: p.department):
    print(f"{dept}: {list(group)}")
```

---

## Replacing Common Patterns

## Flattening Lists
- Use chain or comprehensions
- Avoid nested loops

```python
nested = [[1, 2], [3, 4], [5, 6]]

# Non-idiomatic
flat = []
for sublist in nested:
    for item in sublist:
        flat.append(item)

# Idiomatic
from itertools import chain
flat = list(chain.from_iterable(nested))
# or
flat = [item for sublist in nested for item in sublist]
```

---

## Practical Examples

## Example: Data Processing Pipeline
```python
def process_data(filename):
    from collections import Counter
    from pathlib import Path

    # Read file contents
    data_path = Path(filename)
    try:
        content = data_path.read_text()
    except FileNotFoundError:
        print(f"File not found: {filename}")
        return {}

    # Process and count words
    words = [word.strip(",.!?").lower()
             for word in content.split()
             if len(word) > 3]

    # Return most common words
    return Counter(words).most_common(10)
```

---

## Practical Examples

## Example: Custom Data Container
```python
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Student:
    name: str
    id: int
    grades: List[int] = field(default_factory=list)

    @property
    def average(self) -> Optional[float]:
        return sum(self.grades) / len(self.grades) if self.grades else None

    def add_grade(self, grade: int) -> None:
        if not 0 <= grade <= 100:
            raise ValueError("Grade must be between 0 and 100")
        self.grades.append(grade)
```

---

## Summary

## Key Points
- Choose the right data structure for your needs
- Leverage Python's built-in features and libraries
- Prefer clear, concise, and readability
- Follow Python's idioms for more maintainable code
- Know when to break the rules for clarity or performance

---

## Further Reading

## Resources
- "Fluent Python" by Luciano Ramalho
- "Effective Python" by Brett Slatkin
- "Python Cookbook" by David Beazley and Brian K. Jones
- PEP 8 - Style Guide for Python Code
- The Zen of Python (`import this`)
