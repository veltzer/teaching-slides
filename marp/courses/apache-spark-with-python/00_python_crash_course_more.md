# Python Crash Course for Spark

---
## Course Introduction

### Overview
- Introduction to Python programming
- Focus on Spark-relevant concepts
- Hands-on approach with examples
- Prerequisites and expectations

---
### Why Python for Spark?
- Easy to learn and read
- Rich ecosystem of libraries
- Strong data processing capabilities
- Native support in Spark
- Large community and resources

---
### Learning Objectives
- Master Python syntax and concepts
- Understand data structures
- Learn functional programming concepts
- Develop Spark-ready coding skills
- Practice memory-efficient coding

---
## Python Fundamentals

### Variables and Assignment

```python
# Basic assignment
name = "John"
age = 30
height = 1.75
is_student = True

# Multiple assignment
x, y, z = 1, 2, 3

# Augmented assignment
counter = 0
counter += 1  # Increment
counter *= 2  # Multiply and assign
```

---
### Data Types

```python
# Numbers
integer_num = 42
float_num = 3.14
complex_num = 1 + 2j

# Strings
single_quoted = 'Hello'
double_quoted = "World"
multi_line = """
    This is a
    multi-line string
"""

# Boolean
is_valid = True
is_complete = False

# None type
empty_value = None
```

---
### Type Conversion

```python
# Explicit conversion
str_num = "123"
int_num = int(str_num)
float_num = float(str_num)
str_back = str(int_num)

# Type checking
print(isinstance(int_num, int))  # True
print(type(float_num))  # <class 'float'>
```

---
## String Operations

### String Manipulation

```python
# Basic operations
text = "Hello, World!"
length = len(text)
upper_case = text.upper()
lower_case = text.lower()
title_case = text.title()

# Slicing
first_five = text[:5]
last_five = text[-5:]
reversed_text = text[::-1]
```

---
### String Methods

```python
# Common string methods
text = "  Python Programming  "
stripped = text.strip()
replaced = text.replace("Python", "Spark")
split_words = text.split()

# String formatting
name = "Alice"
age = 25
formatted = f"{name} is {age} years old"
template = "{} is {} years old".format(name, age)
```

---
### String Operations for Spark

```python
# Common string operations in Spark
def clean_text(text):
    return (text.lower()
            .strip()
            .replace(",", "")
            .split())

# Pattern matching
import re
def extract_numbers(text):
    return re.findall(r'\d+', text)
```

---
## Advanced Data Types

### Lists in Depth

```python
# List creation
numbers = [1, 2, 3, 4, 5]
mixed = [1, "hello", 3.14, True]
nested = [[1, 2], [3, 4]]
generated = list(range(10))

# List operations
numbers.append(6)
numbers.extend([7, 8])
numbers.insert(0, 0)
last = numbers.pop()
first = numbers.pop(0)
numbers.remove(5)

# List slicing
first_three = numbers[:3]
last_three = numbers[-3:]
every_second = numbers[::2]
```

---
### Tuples

```python
# Tuple creation
point = (3, 4)
nested_tuple = ((1, 2), (3, 4))
single_tuple = (1,)  # Note the comma

# Tuple operations
x, y = point  # Unpacking
coordinates = zip([1, 2, 3], [4, 5, 6])
tuple_coords = tuple(coordinates)

# Named tuples
from collections import namedtuple
Person = namedtuple('Person', ['name', 'age'])
person = Person('John', 30)
```

---
### Dictionaries Extended

```python
# Dictionary creation
person = {
    'name': 'Alice',
    'age': 25,
    'skills': ['Python', 'Spark']
}

# Dictionary methods
keys = person.keys()
values = person.values()
items = person.items()

# Dictionary operations
person.update({'location': 'New York'})
skills = person.get('skills', [])
person.setdefault('email', 'default@example.com')

# Dictionary comprehension
squares = {x: x**2 for x in range(5)}
```

---
## Functional Programming

### Lambda Functions

```python
# Basic lambda
square = lambda x: x**2
add = lambda x, y: x + y
is_even = lambda x: x % 2 == 0

# Lambda with conditionals
get_status = lambda x: 'High' if x > 90 else 'Low'

# Lambda with multiple statements
complex_lambda = lambda x: [
    y for y in range(x) if y % 2 == 0
]
```

---
### Higher-Order Functions

```python
# Map examples
numbers = [1, 2, 3, 4, 5]
squares = list(map(lambda x: x**2, numbers))
names = ['alice', 'bob', 'charlie']
capitalized = list(map(str.capitalize, names))

# Filter examples
even_numbers = list(filter(lambda x: x % 2 == 0, numbers))
non_empty = list(filter(None, ['', 'a', '', 'b']))

# Reduce examples
from functools import reduce
sum_all = reduce(lambda x, y: x + y, numbers)
max_value = reduce(lambda x, y: x if x > y else y, numbers)
```

---
### List Comprehensions Advanced

```python
# Basic comprehension
squares = [x**2 for x in range(10)]

# Conditional comprehension
even_squares = [x**2 for x in range(10) if x % 2 == 0]

# Nested comprehension
matrix = [[i+j for j in range(3)] for i in range(3)]

# Multiple if conditions
filtered = [x for x in range(100)
           if x % 2 == 0
           if x % 3 == 0]

# Dictionary comprehension
word_length = {word: len(word) for word in ['cat', 'dog', 'elephant']}
```

---
## Memory Management

### Memory Efficiency

```python
# Generators vs Lists
# Bad - creates large list in memory
large_list = [x**2 for x in range(1000000)]

# Good - generates values on demand
large_gen = (x**2 for x in range(1000000))

# Custom generator
def number_generator(n):
    for i in range(n):
        yield i**2
```

---
### Memory Optimization

```python
# Using itertools for memory efficiency
from itertools import islice

# Instead of creating a large list
def process_large_dataset(data):
    return islice(data, 0, None, 2)

# Memory-efficient data processing
def chunk_processor(data, chunk_size=1000):
    buffer = []
    for item in data:
        buffer.append(item)
        if len(buffer) >= chunk_size:
            yield buffer
            buffer = []
    if buffer:
        yield buffer
```

---
## Exception Handling

### Basic Exception Handling
```python
# Try-except structure
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    print("Cleanup code")

# Multiple exceptions
try:
    value = int("abc")
except (ValueError, TypeError) as e:
    print(f"Conversion error: {e}")
```

---
### Custom Exceptions
```python
# Define custom exception
class DataValidationError(Exception):
    def __init__(self, message, errors):
        super().__init__(message)
        self.errors = errors

# Using custom exception
def validate_data(data):
    errors = []
    if not data:
        errors.append("Data is empty")
    if errors:
        raise DataValidationError("Invalid data", errors)
```

---
## File Handling

### File Operations
```python
# Basic file operations
with open('data.txt', 'r') as file:
    content = file.read()

with open('output.txt', 'w') as file:
    file.write('Hello, World!')

# Reading large files efficiently
def read_large_file(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            yield line.strip()
```

---
### CSV Processing
```python
import csv

# Reading CSV
with open('data.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        process_row(row)

# Writing CSV
with open('output.csv', 'w') as file:
    writer = csv.writer(file)
    writer.writerows(data)
```

---
## Best Practices for Spark

### Code Organization
```python
# Module structure
class DataProcessor:
    def __init__(self, spark_session):
        self.spark = spark_session
    
    def process_data(self, data):
        return data.map(self.transform)
    
    @staticmethod
    def transform(row):
        return row.upper()
```

---
### Performance Optimization

```python
# Efficient data handling
def process_rdd_data(rdd):
    # Use broadcast variables for lookup tables
    lookup_table = spark.sparkContext.broadcast({
        'A': 1, 'B': 2, 'C': 3
    })
    
    return (rdd
            .map(lambda x: (x, 1))
            .reduceByKey(lambda x, y: x + y)
            .filter(lambda x: x[1] > lookup_table.value.get(x[0], 0)))
```

---
### Testing Patterns

```python
import unittest

class TestDataProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = DataProcessor()
    
    def test_transform(self):
        result = self.processor.transform("test")
        self.assertEqual(result, "TEST")
        
    def test_process_data(self):
        test_data = ["a", "b", "c"]
        expected = ["A", "B", "C"]
        result = self.processor.process_data(test_data)
        self.assertEqual(result, expected)
```

---
## Practical Exercises

### Exercise 1: Data Processing

```python
# Process sales data
sales_data = [
    {"date": "2024-01-01", "amount": 100},
    {"date": "2024-01-02", "amount": 200}
]

def analyze_sales(data):
    # Calculate total sales
    total = sum(sale["amount"] for sale in data)
    
    # Find highest sale
    highest = max(data, key=lambda x: x["amount"])
    
    return {"total": total, "highest": highest}
```

---
### Exercise 2: Text Analysis

```python
def analyze_text(text):
    # Word frequency analysis
    words = text.lower().split()
    frequency = {}
    
    for word in words:
        frequency[word] = frequency.get(word, 0) + 1
        
    # Sort by frequency
    return sorted(
        frequency.items(),
        key=lambda x: x[1],
        reverse=True
    )
```

---
### Exercise 3: Data Transformation

```python
def transform_data(data):
    """
    Transform data for Spark processing
    """
    return (
        data
        .map(lambda x: x.strip())
        .filter(lambda x: x)
        .map(lambda x: x.split(','))
        .map(lambda x: {
            'id': x[0],
            'value': float(x[1])
        })
    )
```

---
## Summary

### Key Takeaways
- Python fundamentals mastered
- Data structures and their operations
- Functional programming concepts
- Memory efficiency techniques
- Best practices for Spark

---
### Preparation for Spark
- Practice with large datasets
- Focus on functional programming
- Understand memory management
- Master data transformations

---
## Final Notes
- Keep code readable and maintainable
- Focus on efficiency with large datasets
- Practice functional programming concepts
- Prepare for Spark Core concepts
