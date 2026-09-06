---
tags:
  - languages:python
level: advanced
category: language
audience:
  - audiences:developers

---

# Python Refresher

## Overview
- 2-hour refresher on Python fundamentals
- Review of basic concepts for advanced Python developers
- Foundation for more complex topics in later chapters

---

## Python Data Model

![Python data model overview](svg/courses/languages/python/advanced-python/01_python_refresher/python_data_model.svg)

---

## Python Basic Types: Numbers

- Integers: `42`, `-7`, `0`
- Floating point: `3.14`, `-0.001`, `2e10`
- Complex numbers: `3+4j`
- Operations: `+`, `-`, `*`, `/`, `//`, `%`, `**`

```python
x = 5
y = 3.14
z = x + y  # 8.14
```

---

## Python Basic Types: Booleans

- Values: `True`, `False`
- Operations: `and`, `or`, `not`
- Conversion: `bool()`

```python
is_valid = True
is_complete = False
can_proceed = is_valid and not is_complete
```

---

## Python Basic Types: Strings

- Immutable sequences of characters
- Created with: `'single'`, `"double"`, `'''triple'''`, `"""triple"""`
- Methods: `.strip()`, `.split()`, `.join()`, `.format()`, f-strings

```python
name = "Python"
version = 3.10
message = f"Hello {name} {version}!"
```

---

## Python Basic Types: Lists

- Mutable sequences
- Created with: `[]`, `list()`
- Operations: `append()`, `extend()`, `insert()`, `pop()`, `remove()`
- Slicing: `my_list[1:4]`

```python
numbers = [1, 2, 3, 4, 5]
numbers.append(6)  # [1, 2, 3, 4, 5, 6]
numbers[1:3] = [10, 20]  # [1, 10, 20, 4, 5, 6]
```

---

## Python Basic Types: Tuples

- Immutable sequences
- Created with: `()`, `tuple()`
- Often used for multiple return values
- Support unpacking

```python
point = (3, 4)
x, y = point  # Unpacking
coordinates = (*point, 5)  # (3, 4, 5)
```

---

## Python Basic Types: Dictionaries

- Key-value mappings
- Created with: `{}`, `dict()`
- Fast lookups by key
- Methods: `.get()`, `.items()`, `.keys()`, `.values()`

```python
user = {"name": "Alice", "age": 30}
user["email"] = "alice@example.com"
age = user.get("age", 0)  # Default if key not found
```

---

## Python Basic Types: Sets

- Unordered collections of unique elements
- Created with: `{1, 2, 3}`, `set()`
- Operations: `.add()`, `.remove()`, union `|`, intersection `&`

```python
unique_numbers = {1, 2, 3, 2, 1}  # {1, 2, 3}
more_numbers = {3, 4, 5}
combined = unique_numbers | more_numbers  # {1, 2, 3, 4, 5}
```

---

## Python Basic Types: None

- Represents absence of a value
- Default return value for functions
- Testing with `is None`, not `== None`

```python
def no_return():
    pass

result = no_return()  # result is None
if result is None:
    print("Function returned None")
```

---

## Python Iterators: What Are Iterators?

- Objects implementing the iterator protocol
- Support the iteration concept in Python
- Protocol requires `__iter__()` and `__next__()` methods
- Raises `StopIteration` when exhausted

```python
iterator = iter([1, 2, 3])
next(iterator)  # 1
next(iterator)  # 2
next(iterator)  # 3
next(iterator)  # Raises StopIteration
```

---

## Python Iterators: Common Iterables

- Lists, tuples, strings, dictionaries, sets
- File objects
- Custom objects implementing the iterator protocol
- Generator functions and expressions

```python
for char in "Python":  # String is iterable
    print(char)

for line in open("file.txt"):  # File is iterable
    print(line.strip())
```

---

## Python Iterators: Iterator Consumption

- Iterators are consumed as you use them
- Cannot be "reset" without creating a new iterator
- Use `list()` to materialize an iterator's contents

```python
numbers = [1, 2, 3, 4, 5]
iter_nums = iter(numbers)
print(list(iter_nums))  # [1, 2, 3, 4, 5]
print(list(iter_nums))  # [] - already consumed
```

---

## Python Iterators: Creating Custom Iterators

- Implement both `__iter__()` and `__next__()`
- `__iter__()` returns self for iterators
- `__next__()` returns next value or raises StopIteration

```python
class CountDown:
    def __init__(self, start):
        self.count = start

    def __iter__(self):
        return self

    def __next__(self):
        if self.count <= 0:
            raise StopIteration
        self.count -= 1
        return self.count + 1
```

---

## Python Iterators: Generators

- Functions that use `yield` instead of `return`
- Create iterators automatically
- Maintain state between calls
- More memory-efficient than storing all values

```python
def count_up_to(limit):
    count = 1
    while count <= limit:
        yield count
        count += 1

for num in count_up_to(5):
    print(num)  # Prints 1, 2, 3, 4, 5
```

---

## Python Iterators: Iterator Tools

## The itertools Module
- Efficient iterator algebra
- Functions like `chain()`, `cycle()`, `islice()`
- Combinatoric functions like `permutations()`, `combinations()`

```python
import itertools

merged = itertools.chain([1, 2], [3, 4])  # 1, 2, 3, 4
pairs = itertools.combinations([1, 2, 3], 2)  # (1,2), (1,3), (2,3)
repeated = list(itertools.repeat("x", 3))  # ["x", "x", "x"]
```

---

## type() vs isinstance(): Understanding Type Checking

- `type()` returns the exact type of an object
- `isinstance()` checks if object belongs to a type or its subclasses
- `isinstance()` supports checking against multiple types

```python
class Parent:
    pass

class Child(Parent):
    pass

obj = Child()
type(obj) == Child  # True
type(obj) == Parent  # False
isinstance(obj, Child)  # True
isinstance(obj, Parent)  # True - checks inheritance
```

---

## type() vs isinstance(): When to Use Each

- Use `isinstance()` for most type checking
    - Respects inheritance
    - More flexible
    - Duck-typing friendly with abstract base classes
- Use `type()` when exact type matters
    - When subclasses should be treated differently
    - For debugging or introspection

---

## type() vs isinstance(): Type Checking with Abstract Base Classes

- Import from `collections.abc`
- Check against protocols, not implementations
- More aligned with Python's duck typing philosophy

```python
from collections.abc import Sequence, Mapping

isinstance([1, 2, 3], Sequence)  # True
isinstance((1, 2, 3), Sequence)  # True
isinstance({"a": 1}, Mapping)  # True
isinstance(42, Sequence)  # False
```

---

## type() vs isinstance(): Common Pitfalls

- Using `==` for type checking (use `is` with types)
- Not accounting for inheritance
- Too rigid type checking (against Python's dynamic nature)

```python
# Don't do this:
if type(x) == list:
    # ...

# Do this instead:
if isinstance(x, list):
    # ...

# Even better (supports duck typing):
if isinstance(x, collections.abc.Sequence) and not isinstance(x, str):
    # ...
```

---

## Python Memory Model: Everything is an Object

- Even types are objects
- Objects have identity, type, and value
- Variables are references to objects

```python
a = [1, 2, 3]
b = a  # b references the same list object as a
b.append(4)  # modifies the object both a and b reference
print(a)  # [1, 2, 3, 4]
```

---

## Python Memory Model: Object Identity

- `id()` function returns unique object identifier
- `is` operator compares object identity
- Different from value equality (`==`)

```python
a = [1, 2, 3]
b = [1, 2, 3]
a == b  # True (same values)
a is b  # False (different objects)

x = 42
y = 42
x is y  # May be True due to integer interning
```

---

## Common Beginner Mistakes: Mutable Default Arguments

- Default arguments are evaluated once at function definition
- Mutable defaults persist between calls

```python
# Problematic:
def add_item(item, items=[]):
    items.append(item)
    return items

# Better:
def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items
```

---

## Common Beginner Mistakes: Late Binding Closures

- Closure variables are bound at execution time, not definition
- Can cause unexpected behavior in loops

```python
# Problematic:
funcs = []
for i in range(3):
    funcs.append(lambda: i)
[f() for f in funcs]  # [2, 2, 2]

# Better:
funcs = []
for i in range(3):
    funcs.append(lambda i=i: i)  # Binding i as default arg
[f() for f in funcs]  # [0, 1, 2]
```

---

## Questions to Consider

## For Your Projects
- Are you using the most appropriate data structures?
- Are you following Python's idiomatic patterns?
- Do you understand how your code behaves with Python's memory model?
- Are you leveraging iterators effectively?

---

## Next Chapter Preview

## Idiomatic Python
- Writing more Pythonic code
- Leveraging Python's built-in features effectively
- Using standard libraries the way they were designed
- Moving from "code that works" to "code that works well"
