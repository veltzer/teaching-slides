---
tags:
  - languages:python
level: advanced
category: language
audience:
  - audiences:developers

---
# Memory and Garbage Collector

## Overview
- Understanding Python's memory management
- Memory usage of Python data structures
- Garbage collection mechanisms
- Techniques to reduce memory footprint
- Performance implications of memory usage

---

## Python Memory Management Levels

![Python Memory Management Levels](svg/courses/languages/python/advanced-python/03_memory_and_garbage_collector/python_memory_management_levels.svg)

---

## Reference Counting

![Reference Counting](svg/courses/languages/python/advanced-python/03_memory_and_garbage_collector/reference_counting.svg)

---

## Python Memory Management: Principles

- Everything in Python is an object
- Objects are allocated on the heap
- Reference counting for memory management
- Supplementary cyclic garbage collector
- Memory is managed automatically
- No explicit memory allocation/deallocation

---

## Python Memory Management: Levels of Memory Management

1. Operating system level allocation
1. Python memory manager (allocating/freeing blocks)
1. Object-specific memory manager
1. Python garbage collector

---

## Python Memory Management: How Objects are Stored

- Each object has a header (type, reference count)
- Followed by object's data
- Even simple values like integers are full objects
- Small optimizations like integer caching

```python
# These may be the same object (implementation dependent)
a = 42
b = 42
print(a is b)  # Often True due to small integer caching

# These are different objects
c = [1, 2, 3]
d = [1, 2, 3]
print(c is d)  # Always False (different list objects)
```

---

## Reference Counting: How it Works

- Each object maintains a count of references to it
- When count reaches zero, object is deallocated
- Core memory management mechanism in Python
- Fast for most cases
- Implemented in the Python object header

```python
import sys

# Create an object and check its reference count
x = [1, 2, 3]
print(sys.getrefcount(x) - 1)  # Subtract 1 for getrefcount's reference

# Create another reference
y = x
print(sys.getrefcount(x) - 1)  # Count increases

# Remove reference
y = None
print(sys.getrefcount(x) - 1)  # Count decreases
```

---

## Reference Counting: Advantages

- Immediate reclamation of memory
- Predictable cleanup timing
- Works well for most memory usage patterns
- Simplifies extension code (clear ownership rules)

---

## Reference Counting: Limitations

- Cannot detect reference cycles
- Overhead of maintaining counts
- Thread-safety requirements add complexity
- Performance impact of frequent updates

---

## Cyclic Garbage Collection: The Problem with Cycles

- Reference counting fails with circular references
- Objects can reference each other but be unreachable
- Memory leaks would occur without additional collection

```python
def create_cycle():
    x = {}
    y = {}
    x['y'] = y  # x references y
    y['x'] = x  # y references x
    return "Cycle created"

# Create and lose reference to the cycle
create_cycle()
# Without cyclic GC, x and y would never be collected
```

---

## Cyclic Garbage Collection: How Python's Cyclic GC Works

- Tracks potentially container objects
- Periodically checks for reference cycles
- Uses generational approach (3 generations)
- Can be controlled via `gc` module
- Runs automatically or can be triggered manually

```python
import gc

# Get GC statistics
print(gc.get_stats())

# Manual collection
gc.collect()

# Disable automatic collection
gc.disable()

# Enable automatic collection
gc.enable()
```

---

## Cyclic Garbage Collection: Generations

- Generation 0: New objects
- Generation 1: Objects that survived one collection
- Generation 2: Long-lived objects
- Each generation collected at different frequency
- Optimization based on generational hypothesis

---

## Cyclic Garbage Collection: Thresholds

- Each generation has a threshold
- When threshold is reached, collection is triggered
- Default thresholds: (700, 10, 10)
- Adjustable via `gc.set_threshold()`

```python
import gc

# Get current thresholds
print(gc.get_threshold())  # Default: (700, 10, 10)

# Set custom thresholds
gc.set_threshold(900, 15, 15)
```

---

## Object Size in Memory: Basic Structure

- Python object header: typically 16 bytes
- Plus the object's data
- Plus references to other objects
- Plus alignment and padding

---

## Object Size in Memory: Measuring Object Size

- `sys.getsizeof()` gives shallow size
- Does not include size of referenced objects
- External libraries for deep size calculation

```python
import sys

# Basic types
print(sys.getsizeof(1))         # Integer
print(sys.getsizeof(1.0))       # Float
print(sys.getsizeof("a"))       # Single-char string
print(sys.getsizeof("abc"))     # Multi-char string

# Container types (shallow size only)
print(sys.getsizeof([]))        # Empty list
print(sys.getsizeof([1, 2, 3])) # List with 3 elements
```

---

## Object Size in Memory: Size of Common Types

## Integers
- Fixed overhead plus variable storage
- Small integers (-5 to 256) are pre-allocated
- Arbitrary precision (can grow as needed)

```python
import sys

# Size depends on value magnitude
print(sys.getsizeof(0))      # Typically 24 bytes
print(sys.getsizeof(1000))   # Typically 28 bytes
print(sys.getsizeof(2**100)) # Larger due to value size
```

---

## Object Size in Memory: Size of Common Types

## Strings
- Fixed overhead plus character storage
- Latin-1 strings: 1 byte per character
- Unicode strings: up to 4 bytes per character
- Small string optimization in some implementations

```python
import sys

# String sizes
print(sys.getsizeof(""))      # Empty string overhead
print(sys.getsizeof("a"))     # Single ASCII char
print(sys.getsizeof("abc"))   # Multiple ASCII chars
print(sys.getsizeof("🐍"))    # Unicode character
```

---

## Object Size in Memory: Size of Common Types

## Lists
- Fixed overhead (typically 64-80 bytes)
- Plus references to contained objects
- Over-allocation for append efficiency
- Doesn't include size of contained objects

```python
import sys

# List sizes
empty_list = []
print(sys.getsizeof(empty_list))

# Lists over-allocate for future appends
one_item = [1]
print(sys.getsizeof(one_item))

# Over-allocation becomes evident
many_items = list(range(10))
print(sys.getsizeof(many_items))
```

---

## Object Size in Memory: Size of Common Types

## Dictionaries
- Significant overhead (typically 232+ bytes)
- Hash table with pre-allocated slots
- Sparse structure for collision avoidance
- Optimized in Python 3.6+ (more compact)

```python
import sys

# Dictionary sizes
empty_dict = {}
print(sys.getsizeof(empty_dict))

# Adding items
small_dict = {"a": 1}
print(sys.getsizeof(small_dict))

# Dictionaries resize at certain thresholds
large_dict = {str(i): i for i in range(100)}
print(sys.getsizeof(large_dict))
```

---

## Object Size in Memory: Deep Size Calculation

- Recursively measure all referenced objects
- Account for shared references
- Several third-party libraries available

```python
def get_deep_size(obj, seen=None):
    import sys
    if seen is None:
        seen = set()

    obj_id = id(obj)
    if obj_id in seen:
        return 0

    seen.add(obj_id)
    size = sys.getsizeof(obj)

    if isinstance(obj, dict):
        size += sum(get_deep_size(k, seen) + get_deep_size(v, seen)
                   for k, v in obj.items())
    elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes)):
        size += sum(get_deep_size(i, seen) for i in obj)

    return size
```

---

## Object Size in Memory: Using Third-Party Tools

- `pympler` package for memory profiling
- `objgraph` for object reference visualization
- `memory_profiler` for line-by-line memory usage

```python
from pympler import asizeof

# Deep size calculation
data = [1, 2, [3, 4, [5, 6]], {7: 8, 9: 10}]
print(asizeof.asizeof(data))  # Full recursive size

# Size of multiple objects
print(asizeof.asizeof(1, "hello", [1, 2, 3]))
```

---

## How Many Python Objects?: Memory Limitations

- Limited by system memory
- Reference table overhead
- OS memory fragmentation
- Python's internal limits

---

## How Many Python Objects?: Practical Limits

- CPython can address up to system memory
- Lists limited to ~536 million elements (32-bit indices)
- Dictionaries can handle millions of entries
- Real limits often hit well before theoretical limits

```python
# Large list creation example
try:
    # Create a list with 10 million integers
    large_list = list(range(10_000_000))
    print(f"Created list with {len(large_list)} elements")

    # Check memory usage (shallow)
    import sys
    print(f"Shallow size: {sys.getsizeof(large_list) / (1024 * 1024):.2f} MB")

    # Approximate deep size
    element_size = sys.getsizeof(0)
    total_size = sys.getsizeof(large_list) + element_size * len(large_list)
    print(f"Estimated total size: {total_size / (1024 * 1024):.2f} MB")
except MemoryError:
    print("Memory error - couldn't allocate list")
```

---

## How Many Python Objects?: Memory Traps

- List comprehensions versus generator expressions
- Large dictionaries with many small keys
- Temporary objects in loops
- String concatenation in loops
- High-frequency object creation/deletion

---

## Reducing Memory Footprint: General Strategies

- Use generators instead of lists when possible
- Process data in chunks
- Reuse objects instead of creating new ones
- Free references when no longer needed
- Use appropriate data structures

---

## Reducing Memory Footprint: Using Generators

- Process one item at a time
- Avoid loading everything into memory
- Perfect for processing large datasets

```python
# Memory-intensive approach
def process_file_list(filename):
    with open(filename) as f:
        lines = f.readlines()  # Loads entire file into memory

    return [line.strip().upper() for line in lines if line.strip()]

# Memory-efficient approach
def process_file_generator(filename):
    with open(filename) as f:
        for line in f:  # Reads one line at a time
            line = line.strip()
            if line:
                yield line.upper()
```

---

## Reducing Memory Footprint: Specialized Libraries

## NumPy
- Efficient array storage
- Uses contiguous memory blocks
- Much smaller footprint than Python lists
- Vectorized operations

```python
import numpy as np
import sys

# Compare memory usage: list vs numpy array
py_list = list(range(1000000))
np_array = np.arange(1000000)

print(f"Python list: {sys.getsizeof(py_list) / (1024 * 1024):.2f} MB")
print(f"NumPy array: {sys.getsizeof(np_array) / (1024 * 1024):.2f} MB")
```

---

## Reducing Memory Footprint: Specialized Libraries

## Arrays Module
- Homogeneous numeric arrays
- More memory-efficient than lists
- Good for large collections of uniform data
- Limited to C numeric types

```python
import array
import sys

# Regular Python list of integers
int_list = list(range(10000))
print(f"List size: {sys.getsizeof(int_list)} bytes")

# Array of integers
int_array = array.array('i', range(10000))
print(f"Array size: {sys.getsizeof(int_array)} bytes")
```

---

## Reducing Memory Footprint: Specialized Libraries

## Collections
- `collections.namedtuple` for small, immutable records
- More memory-efficient than classes
- `collections.deque` for efficient queue operations

```python
from collections import namedtuple
import sys

# Compare memory usage: class vs namedtuple
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

PointTuple = namedtuple('PointTuple', ['x', 'y'])

p1 = Point(10, 20)
p2 = PointTuple(10, 20)

print(f"Class instance: {sys.getsizeof(p1)} bytes")
print(f"Named tuple: {sys.getsizeof(p2)} bytes")
```

---

## Reducing Memory Footprint: Copy on Write

- Share memory between objects until modification
- Common in NumPy and Pandas operations
- Requires explicit handling in pure Python

```python
import numpy as np

# NumPy arrays use copy-on-write semantics
a = np.arange(1000000)  # Original array
b = a  # Reference to same data, no copy made
c = a.view()  # View of same data, no copy made

# Only creates a copy when data is modified
b[0] = 999  # Modifies a as well
d = a.copy()  # Explicit copy
d[0] = 555  # Doesn't affect a
```

---

## Reducing Memory Footprint: Flyweight Design Pattern

- Share common data between many instances
- Reduces redundancy for repeated data
- Useful for large collections of similar objects

```python
class Flyweight:
    _shared_data = {}

    def __new__(cls, key, *args, **kwargs):
        if key not in cls._shared_data:
            instance = super().__new__(cls)
            cls._shared_data[key] = instance
            return instance
        return cls._shared_data[key]

    def __init__(self, key, *args, **kwargs):
        # Only runs on first creation
        if not hasattr(self, 'initialized'):
            self.key = key
            self.initialized = True
```

---

## Reducing Memory Footprint: String Interning

- Python automatically interns some strings
- Same object used for identical strings
- Can explicitly intern with `sys.intern()`
- Useful for dictionaries with many string keys

```python
import sys

# Automatic interning for simple strings
a = 'hello'
b = 'hello'
print(a is b)  # Often True, implementation-dependent

# Strings from operations aren't auto-interned
c = 'he' + 'llo'
print(a is c)  # Might be False

# Explicit interning
d = sys.intern('hello')
e = sys.intern('he' + 'llo')
print(d is e)  # Always True
```

---

## Reducing Memory Footprint: Slots in Classes

- Restricts instance attributes
- Eliminates per-instance __dict__
- Significantly reduces memory usage

```python
import sys

# Regular class
class RegularPerson:
    def __init__(self, name, age, email):
        self.name = name
        self.age = age
        self.email = email

# Class using __slots__
class SlottedPerson:
    __slots__ = ['name', 'age', 'email']

    def __init__(self, name, age, email):
        self.name = name
        self.age = age
        self.email = email

# Compare memory usage
regular = RegularPerson('John', 30, 'john@example.com')
slotted = SlottedPerson('John', 30, 'john@example.com')

print(f"Regular: {sys.getsizeof(regular)} + {sys.getsizeof(regular.__dict__)} bytes")
print(f"Slotted: {sys.getsizeof(slotted)} bytes")
```

---

## Reducing Memory Footprint: Using C Extensions

- Python C API for extension modules
- Native code for memory-intensive operations
- Pre-existing extensions like NumPy, Pandas
- Cython for easier C extension creation

```python
# Using NumPy for memory-efficient operations
import numpy as np

# Example: matrix operations in NumPy use much less memory
# than nested Python lists
matrix = np.zeros((1000, 1000), dtype=np.float32)  # 4MB, not ~8MB
```

---

## Finding Memory Issues: Memory Profiling

- Track memory usage over time
- Identify leaks and excessive usage
- Several tools available

```python
# Using memory_profiler
from memory_profiler import profile

@profile
def memory_intensive_function():
    data = []
    for i in range(1000000):
        data.append(i)
    return data

# Execute and see line-by-line memory usage
result = memory_intensive_function()
```

---

## Finding Memory Issues: Tracemalloc Module

- Built-in memory allocation tracking
- Added in Python 3.4
- Traces Python memory allocations
- Helps find memory leaks

```python
import tracemalloc

# Start tracing
tracemalloc.start()

# Run your code
data = [list(range(100)) for _ in range(1000)]

# Get current and peak memory usage
current, peak = tracemalloc.get_traced_memory()
print(f"Current: {current / 1024:.2f} KB")
print(f"Peak: {peak / 1024:.2f} KB")

# Get top allocations by source
snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')
for stat in top_stats[:5]:
    print(stat)
```

---

## Finding Memory Issues: Resource Module

- Monitor process resources
- Track memory usage over time
- Works across platforms

```python
import resource

# Get baseline memory usage
baseline = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

# Run your code
data = [list(range(100)) for _ in range(1000)]

# Check memory usage after
current = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
print(f"Memory increase: {(current - baseline) / 1024:.2f} MB")
```

---

## Finding Memory Issues: gc and objgraph

- Analyze object references
- Find reference cycles
- Visualize object graphs

```python
import gc
import objgraph

# Find objects of specific type
print(objgraph.count('list'))
print(objgraph.count('dict'))

# Find what's referencing an object
obj = ['example']
objgraph.show_backrefs(obj, filename='backrefs.png')

# Find what an object is referencing
objgraph.show_refs(obj, filename='refs.png')
```

---

## Common Memory Problems: Memory Leaks

- Objects never released
- Reference cycles not collected
- Global variables accumulating data
- Caches without size limits

---

## Common Memory Problems: Memory Fragmentation

- Free blocks too small for new allocations
- Especially with mixed-size allocations
- Can lead to higher memory usage than expected

---

## Common Memory Problems: Excessive Temporary Objects

- String concatenation in loops
- Intermediate lists in comprehensions
- Repeated format operations

```python
# Bad: creates many temporary strings
result = ""
for i in range(1000):
    result += str(i)  # Creates a new string each time

# Better: use join with a list comprehension
result = "".join(str(i) for i in range(1000))
```

---

## Common Memory Problems: Copying Large Data

- Unnecessary copies of large structures
- Function arguments without shared references
- Deep copies when shallow would suffice

```python
import copy

data = [list(range(1000)) for _ in range(100)]

# Creates a full copy
data_copy = copy.deepcopy(data)  # Expensive!

# Often a shallow copy is sufficient
data_shallow = copy.copy(data)  # Only copies the outer list
```

---

## Practical Examples: Example: Processing Large Files

```python
def process_large_file(filename):
    """Process a file without loading it all into memory."""
    with open(filename) as f:
        # Use generators for line-by-line processing
        for i, line in enumerate(f):
            # Process one line at a time
            line = line.strip()
            if line:
                # Do something with the line
                yield process_line(line)

            # Optional: report progress periodically
            if i % 100000 == 0:
                print(f"Processed {i} lines")

def process_line(line):
    """Process a single line from the file."""
    # This function is called for each line
    return line.upper()
```

---

## Practical Examples: Example: Memory-Efficient Data Class

```python
class EfficientRecord:
    __slots__ = ['id', 'name', 'value']

    def __init__(self, id, name, value=0):
        self.id = id
        self.name = sys.intern(name)  # Intern strings
        self.value = value

# Creating many records with common strings
records = [
    EfficientRecord(i, "type_" + str(i % 10), i * 1.5)
    for i in range(100000)
]
```

---

## Practical Examples: Example: Chunked Processing

```python
def process_data_in_chunks(data_source, chunk_size=1000):
    """Process a large dataset in manageable chunks."""
    # Either a file or another iterable
    iter_source = iter(data_source)

    # Process one chunk at a time
    while True:
        # Get the next chunk
        chunk = list(itertools.islice(iter_source, chunk_size))
        if not chunk:
            break

        # Process this chunk (can use full memory for this small piece)
        results = process_chunk(chunk)

        # Yield or save the results
        for result in results:
            yield result

        # Explicitly delete to help garbage collection
        del chunk
        del results
```

---

## Summary

## Key Takeaways
- Understand how Python manages memory
- Measure and monitor memory usage
- Choose appropriate data structures
- Use generators for large data processing
- Leverage specialized libraries when appropriate
- Profile memory usage to identify issues
- Think about memory patterns in your algorithms

---

## Further Reading

## Resources
- "High Performance Python" by Micha Gorelick and Ian Ozsvald
- Python documentation on garbage collection
- Memory profiler documentation
- NumPy and Pandas documentation
- Python internals documentation
