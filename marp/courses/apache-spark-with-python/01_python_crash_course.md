# Python Crash Course for Spark

---
## Course Introduction
- Welcome to the Python fundamentals section
- This crash course is designed for those familiar with programming but new to Python
- We'll cover essential concepts needed for Spark development

---
## Basic Syntax

## Variables and Data Types

```python
# Variable assignment
name = "John"
age = 30
height = 1.75
is_developer = True

# Multiple assignment
x, y, z = 1, 2, 3

# Type checking
print(type(name))  # <class 'str'>
print(type(age))   # <class 'int'>
```

---
## Basic Operations

```python
# Arithmetic
sum = 10 + 5
difference = 10 - 5
product = 10 * 5
division = 10 / 5
floor_division = 10 // 3
modulus = 10 % 3
power = 2 ** 3

# String operations
first = "Hello"
second = "World"
greeting = first + " " + second
repeated = "Hi " * 3
```

---
## Data Structures

## Tuples

```python
# Creating tuples
coordinates = (3, 4)
rgb = (255, 128, 0)

# Tuple operations
x, y = coordinates  # Unpacking
nested = ((1, 2), (3, 4))
```

---
## Lists

```python
# Creating lists
numbers = [1, 2, 3, 4, 5]
mixed = [1, "hello", 3.14, True]

# List operations
numbers.append(6)
numbers.extend([7, 8])
numbers.insert(0, 0)
last = numbers.pop()
```

---
## List Comprehensions

```python
# Traditional way
squares = []
for i in range(10):
    squares.append(i**2)

# List comprehension way
squares = [i**2 for i in range(10)]

# With condition
even_squares = [i**2 for i in range(10) if i % 2 == 0]
```

---
## Dictionaries

```python
# Creating dictionaries
person = {
    "name": "Alice",
    "age": 25,
    "skills": ["Python", "Spark"]
}

# Dictionary operations
person["location"] = "New York"
skills = person.get("skills", [])
keys = person.keys()
values = person.values()
```

---
## Lambda Functions

## Understanding Lambda Functions

```python
# Traditional function
def square(x):
    return x**2

# Lambda equivalent
square = lambda x: x**2

# Multiple parameters
add = lambda x, y: x + y
```

---
## Common Use Cases

```python
# With map
numbers = [1, 2, 3, 4, 5]
squares = list(map(lambda x: x**2, numbers))

# With filter
even_numbers = list(filter(lambda x: x % 2 == 0, numbers))

# With sort
pairs = [(1, 'one'), (2, 'two'), (3, 'three')]
sorted_pairs = sorted(pairs, key=lambda x: x[1])
```

---
## Python Best Practices for Spark

## Code Style
- Use meaningful variable names
- Follow PEP 8 guidelines
- Keep functions small and focused
- Use type hints when possible

---
## Memory Considerations

```python
# Bad - creates large intermediate lists
data = [i**2 for i in range(1000000)]

# Good - uses generator
data = (i**2 for i in range(1000000))
```

---
## Exercise Examples

## Basic Operations

```python
# Exercise 1: Create a function that converts temperature
def convert_temp(celsius):
    return (celsius * 9/5) + 32
```

---
## Data Structure Manipulation

```python
# Exercise 2: Process a list of transactions
transactions = [
    {"id": 1, "amount": 100},
    {"id": 2, "amount": 200},
    {"id": 3, "amount": 300}
]

total = sum(t["amount"] for t in transactions)
```

---
## Summary
- Python's syntax is clean and readable
- Key data structures: tuples, lists, dictionaries
- Lambda functions for functional programming
- These concepts form the foundation for Spark programming
