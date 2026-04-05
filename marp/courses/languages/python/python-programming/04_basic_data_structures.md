# Basic Data Structures
---
## Python's Built-in Data Structures
| Type | Ordered | Mutable | Duplicates | Syntax |
|------|---------|---------|------------|--------|
| `list` | Yes | Yes | Yes | `[1, 2, 3]` |
| `tuple` | Yes | No | Yes | `(1, 2, 3)` |
| `dict` | Yes* | Yes | Keys: No | `{"a": 1}` |
| `set` | No | Yes | No | `{1, 2, 3}` |

Insertion-ordered since `Python` 3.7

---
## Lists - Creating

```python
empty = []
numbers = [1, 2, 3, 4, 5]
mixed = [1, "hello", 3.14, True]
nested = [[1, 2], [3, 4]]
from_range = list(range(5))  # [0, 1, 2, 3, 4]
```
---
## Lists - Indexing and Slicing

```python
fruits = ["apple", "banana", "cherry", "date"]

print(fruits[0])     # 'apple'
print(fruits[-1])    # 'date'
print(fruits[1:3])   # ['banana', 'cherry']
print(fruits[:2])    # ['apple', 'banana']
print(fruits[::2])   # ['apple', 'cherry']
print(fruits[::-1])  # reversed list
```
---
## Lists - Modifying Elements

```python
fruits = ["apple", "banana", "cherry"]

# Change single element
fruits[1] = "blueberry"
print(fruits)  # ['apple', 'blueberry', 'cherry']

# Change slice
fruits[0:2] = ["avocado", "blackberry"]
print(fruits)  # ['avocado', 'blackberry', 'cherry']
```
---
## Lists - Adding Elements

```python
fruits = ["apple", "banana"]

# Append: add to end
fruits.append("cherry")
# ['apple', 'banana', 'cherry']

# Insert: add at index
fruits.insert(1, "avocado")
# ['apple', 'avocado', 'banana', 'cherry']

# Extend: add multiple items
fruits.extend(["date", "elderberry"])
# ['apple', 'avocado', 'banana', 'cherry', 'date', 'elderberry']
```
---
## Lists - Removing Elements

```python
fruits = ["apple", "banana", "cherry", "banana"]

# Remove by value (first occurrence)
fruits.remove("banana")
# ['apple', 'cherry', 'banana']

# Remove by index
del fruits[0]
# ['cherry', 'banana']

# Pop: remove and return
last = fruits.pop()      # 'banana'
first = fruits.pop(0)    # 'cherry'
```
---
## Lists - Searching

```python
numbers = [10, 20, 30, 20, 40]

print(20 in numbers)        # True
print(50 not in numbers)    # True
print(numbers.index(20))    # 1 (first occurrence)
print(numbers.count(20))    # 2
```
---
## Lists - Sorting

```python
numbers = [3, 1, 4, 1, 5, 9, 2, 6]

# Sort in place
numbers.sort()
print(numbers)  # [1, 1, 2, 3, 4, 5, 6, 9]

# Sort descending
numbers.sort(reverse=True)
print(numbers)  # [9, 6, 5, 4, 3, 2, 1, 1]

# sorted() returns new list (original unchanged)
original = [3, 1, 2]
new = sorted(original)
print(original)  # [3, 1, 2]
print(new)       # [1, 2, 3]
```
---
## Lists - Sorting with Key

```python
words = ["banana", "Apple", "cherry", "date"]

# Sort by length
words.sort(key=len)
print(words)  # ['date', 'Apple', 'banana', 'cherry']

# Case-insensitive sort
words.sort(key=str.lower)
print(words)  # ['Apple', 'banana', 'cherry', 'date']
```
---
## Lists - Other Methods

```python
numbers = [1, 2, 3]

# Reverse in place
numbers.reverse()
print(numbers)  # [3, 2, 1]

# Copy (shallow)
copy = numbers.copy()

# Clear
numbers.clear()
print(numbers)  # []
```
---
## Lists - Concatenation and Repetition

```python
a = [1, 2, 3]
b = [4, 5, 6]

# Concatenation
print(a + b)    # [1, 2, 3, 4, 5, 6]

# Repetition
print(a * 3)    # [1, 2, 3, 1, 2, 3, 1, 2, 3]

# Length
print(len(a))   # 3
```
---
## Lists - Unpacking

```python
coordinates = [10, 20, 30]
x, y, z = coordinates
print(x, y, z)  # 10 20 30

# Star unpacking
first, *rest = [1, 2, 3, 4, 5]
print(first)  # 1
print(rest)   # [2, 3, 4, 5]

*start, last = [1, 2, 3, 4, 5]
print(start)  # [1, 2, 3, 4]
print(last)   # 5
```
---
## Shallow vs Deep Copy

```python
import copy

original = [[1, 2], [3, 4]]

# Shallow copy - inner lists are shared
shallow = original.copy()
shallow[0][0] = 99
print(original[0][0])  # 99 (modified!)

# Deep copy - completely independent
original = [[1, 2], [3, 4]]
deep = copy.deepcopy(original)
deep[0][0] = 99
print(original[0][0])  # 1 (unchanged)
```
---
## Tuples - Creating

```python
empty = ()
single = (42,)    # Note the comma!
numbers = (1, 2, 3)
mixed = (1, "hello", 3.14)
no_parens = 1, 2, 3  # Parentheses are optional
from_list = tuple([1, 2, 3])
```
---
## Tuples are Immutable

```python
t = (1, 2, 3)

# Accessing works like lists
print(t[0])     # 1
print(t[-1])    # 3
print(t[1:])    # (2, 3)

# Modification is not allowed
# t[0] = 10  # TypeError!
# t.append(4)  # AttributeError!
```
---
## Why Use Tuples?
- Immutable: safe to use as dictionary keys
- Slightly faster than lists
- Signal intent: data should not change
- Function return values
- Named tuples for structured data

```python
# Multiple return values
def divide(a, b):
    return a // b, a % b

quotient, remainder = divide(17, 5)
print(quotient, remainder)  # 3 2
```
---
## Tuple Methods

```python
t = (1, 2, 3, 2, 1)

# Only two methods
print(t.count(2))   # 2
print(t.index(3))   # 2
```

- Tuples have very few methods because they are immutable
---
## Named Tuples

```python
from collections import namedtuple

Point = namedtuple("Point", ["x", "y"])
p = Point(3, 4)
print(p.x)      # 3
print(p.y)      # 4
print(p[0])     # 3 (still works)
print(p)        # Point(x=3, y=4)
```
---
## Dictionaries - Creating

```python
empty = {}
person = {"name": "Alice", "age": 30}
from_pairs = dict([("a", 1), ("b", 2)])
from_kwargs = dict(name="Alice", age=30)
from_keys = dict.fromkeys(["a", "b", "c"], 0)
# {'a': 0, 'b': 0, 'c': 0}
```
---
## Dictionaries - Accessing Values

```python
person = {"name": "Alice", "age": 30, "city": "NYC"}

# Square bracket access
print(person["name"])     # 'Alice'
# print(person["email"])  # KeyError!

# get() with default
print(person.get("name"))          # 'Alice'
print(person.get("email"))         # None
print(person.get("email", "N/A"))  # 'N/A'
```
---
## Dictionaries - Modifying

```python
person = {"name": "Alice", "age": 30}

# Add or update
person["email"] = "alice@example.com"
person["age"] = 31

# Update multiple keys
person.update({"age": 32, "city": "NYC"})

# Setdefault: set only if key missing
person.setdefault("name", "Bob")    # 'Alice' (exists)
person.setdefault("phone", "555")   # '555' (added)
```
---
## Dictionaries - Removing

```python
person = {"name": "Alice", "age": 30, "city": "NYC"}

# Remove by key
del person["city"]

# Pop: remove and return
age = person.pop("age")       # 30
missing = person.pop("x", 0)  # 0 (default)

# Pop last item
last = person.popitem()  # ('name', 'Alice')

# Clear all
person.clear()
```
---
## Dictionaries - Checking Keys

```python
person = {"name": "Alice", "age": 30}

print("name" in person)       # True
print("email" in person)      # False
print("email" not in person)  # True

# Note: 'in' checks keys, not values
print("Alice" in person)      # False
print("Alice" in person.values())  # True
```
---
## Dictionaries - Views

```python
person = {"name": "Alice", "age": 30}

print(person.keys())    # dict_keys(['name', 'age'])
print(person.values())  # dict_values(['Alice', 30])
print(person.items())   # dict_items([('name', 'Alice'), ('age', 30)])

# Iterate over items
for key, value in person.items():
    print(f"{key}: {value}")
```
---
## Dictionaries - Merge Operator (Python 3.9+)

```python
defaults = {"color": "red", "size": 10}
custom = {"size": 20, "weight": 5}

# Merge with | operator
merged = defaults | custom
print(merged)
# {'color': 'red', 'size': 20, 'weight': 5}

# Update in place with |=
defaults |= custom
```
---
## Dictionary Ordering
- Since Python 3.7, dictionaries maintain insertion order
- Before 3.7, use `collections.OrderedDict`

```python
d = {}
d["c"] = 3
d["a"] = 1
d["b"] = 2
print(list(d.keys()))  # ['c', 'a', 'b']
```
---
## Sets - Creating

```python
empty = set()  # NOT {} (that's a dict)
numbers = {1, 2, 3, 4, 5}
from_list = set([1, 2, 2, 3, 3])
print(from_list)  # {1, 2, 3}

# Remove duplicates from a list
items = [1, 2, 2, 3, 3, 3]
unique = list(set(items))
print(unique)  # [1, 2, 3]
```
---
## Sets - Adding and Removing

```python
s = {1, 2, 3}

# Add element
s.add(4)
print(s)  # {1, 2, 3, 4}

# Remove (raises KeyError if missing)
s.remove(2)

# Discard (no error if missing)
s.discard(99)

# Pop random element
item = s.pop()

# Clear all
s.clear()
```
---
## Sets - Operations

```python
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}

print(a | b)   # Union: {1, 2, 3, 4, 5, 6}
print(a & b)   # Intersection: {3, 4}
print(a - b)   # Difference: {1, 2}
print(a ^ b)   # Symmetric diff: {1, 2, 5, 6}
```
---
## Sets - Operations Diagram

```txt
A = {1, 2, 3, 4}    B = {3, 4, 5, 6}

A | B (union):       {1, 2, 3, 4, 5, 6}
A & B (intersection): {3, 4}
A - B (difference):   {1, 2}
B - A (difference):   {5, 6}
A ^ B (symmetric):    {1, 2, 5, 6}
```
---
## Sets - Subset and Superset

```python
a = {1, 2, 3}
b = {1, 2, 3, 4, 5}

print(a < b)       # True (proper subset)
print(a <= b)      # True (subset)
print(b > a)       # True (proper superset)
print(b >= a)      # True (superset)
print(a.isdisjoint({4, 5}))  # True (no common elements)
```
---
## Frozen Sets
- Immutable version of a set
- Can be used as dictionary keys or set elements

```python
fs = frozenset([1, 2, 3])
# fs.add(4)  # AttributeError!

# Can be used as dict key
cache = {frozenset([1, 2]): "result"}

# Can be used in a set
s = {frozenset([1, 2]), frozenset([3, 4])}
```
---
## The `enumerate()` Function
- Pairs each element with its index

```python
fruits = ["apple", "banana", "cherry"]

for i, fruit in enumerate(fruits):
    print(f"{i}: {fruit}")
```

```txt
0: apple
1: banana
2: cherry
```
---
## `enumerate()` with Start Index

```python
fruits = ["apple", "banana", "cherry"]

for i, fruit in enumerate(fruits, start=1):
    print(f"{i}. {fruit}")
```

```txt
1. apple
2. banana
3. cherry
```
---
## The `zip()` Function
- Combines iterables element by element

```python
names = ["Alice", "Bob", "Charlie"]
ages = [30, 25, 35]

for name, age in zip(names, ages):
    print(f"{name} is {age}")
```

```txt
Alice is 30
Bob is 25
Charlie is 35
```
---
## `zip()` - Creating Dictionaries

```python
keys = ["name", "age", "city"]
values = ["Alice", 30, "NYC"]

person = dict(zip(keys, values))
print(person)
# {'name': 'Alice', 'age': 30, 'city': 'NYC'}
```
---
## `zip()` - Unequal Lengths

```python
a = [1, 2, 3]
b = [10, 20]

# zip stops at shortest
print(list(zip(a, b)))
# [(1, 10), (2, 20)]

# Use zip_longest for padding
from itertools import zip_longest
print(list(zip_longest(a, b, fillvalue=0)))
# [(1, 10), (2, 20), (3, 0)]
```
---
## Performance - Time Complexity
| Operation | List | Dict | Set |
|-----------|------|------|-----|
| Access by index | O(1) | - | - |
| Search | O(n) | O(1) | O(1) |
| Insert at end | O(1) | O(1) | O(1) |
| Insert at start | O(n) | - | - |
| Delete | O(n) | O(1) | O(1) |
| Iteration | O(n) | O(n) | O(n) |
---
## When to Use What?
- **List**: Ordered collection, need index access, allow duplicates
- **Tuple**: Immutable sequence, function return values, dict keys
- **Dict**: Key-value mapping, fast lookup by key
- **Set**: Unique elements, membership testing, set operations
---
## Performance Example - Membership Testing

```python
import time

data_list = list(range(1_000_000))
data_set = set(data_list)

# List: O(n) - slow
start = time.time()
999_999 in data_list
print(f"List: {time.time() - start:.6f}s")

# Set: O(1) - fast
start = time.time()
999_999 in data_set
print(f"Set: {time.time() - start:.6f}s")
```
---
## Nested Data Structures

```python
# List of dictionaries
students = [
    {"name": "Alice", "grade": 90},
    {"name": "Bob", "grade": 85},
    {"name": "Charlie", "grade": 92},
]

# Access nested data
print(students[0]["name"])  # 'Alice'

# Sort by grade
students.sort(key=lambda s: s["grade"], reverse=True)
```
---
## Dictionary of Lists

```python
grades = {
    "math": [90, 85, 92],
    "science": [88, 91, 87],
    "english": [95, 89, 93],
}

# Average per subject
for subject, scores in grades.items():
    avg = sum(scores) / len(scores)
    print(f"{subject}: {avg:.1f}")
```
---
## The `collections` Module
- `Counter`: Count occurrences
- `defaultdict`: Dict with default factory
- `deque`: Double-ended queue
- `OrderedDict`: Ordered dictionary
- `ChainMap`: Group multiple dicts

```python
from collections import Counter

words = ["apple", "banana", "apple", "cherry", "banana", "apple"]
count = Counter(words)
print(count)
# Counter({'apple': 3, 'banana': 2, 'cherry': 1})
print(count.most_common(2))
# [('apple', 3), ('banana', 2)]
```
---
## `defaultdict`

```python
from collections import defaultdict

# Group words by first letter
words = ["apple", "banana", "avocado", "blueberry", "cherry"]
grouped = defaultdict(list)

for word in words:
    grouped[word[0]].append(word)

print(dict(grouped))
# {'a': ['apple', 'avocado'], 'b': ['banana', 'blueberry'], 'c': ['cherry']}
```
---
## `deque` - Double-ended Queue

```python
from collections import deque

d = deque([1, 2, 3])
d.append(4)       # Add to right
d.appendleft(0)   # Add to left
print(d)           # deque([0, 1, 2, 3, 4])

d.pop()            # Remove from right
d.popleft()        # Remove from left
print(d)           # deque([1, 2, 3])
```
---
## Summary
- **Lists**: Mutable, ordered, `[]`, most versatile
- **Tuples**: Immutable, ordered, `()`, safe and fast
- **Dicts**: Key-value pairs, `{}`, O(1) lookup
- **Sets**: Unique elements, `set()`, set operations
- Use `enumerate()` for index-value pairs
- Use `zip()` to combine iterables
- Choose data structure based on your access patterns
