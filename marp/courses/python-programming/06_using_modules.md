# Using Modules
---
## What is a Module?
- A module is a `.py` file containing Python code
- Provides reusable functions, classes, and variables
- Helps organize code into logical units

```python
# math_utils.py is a module
import math_utils
```
---
## Why Use Modules?
- Code reuse across multiple files
- Namespace separation (avoid name collisions)
- Logical organization of code
- Easier maintenance
- Python's standard library is a collection of modules
---
## The `import` Statement

```python
import math

print(math.pi)          # 3.141592653589793
print(math.sqrt(16))    # 4.0
print(math.factorial(5))  # 120
```

- The module name becomes a namespace
- Access contents with dot notation
---
## `from ... import`

```python
from math import pi, sqrt, factorial

print(pi)           # 3.141592653589793
print(sqrt(16))     # 4.0
print(factorial(5))  # 120
```

- Imports specific names directly into the current namespace
- No need for the module prefix
---
## `from ... import *`

```python
from math import *

print(pi)        # Works
print(sqrt(16))  # Works
```

- Imports all public names from a module
- Generally discouraged: pollutes namespace
- Hard to know where names come from
- Can shadow existing names
---
## Import with Alias

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Common aliases in the Python ecosystem
arr = np.array([1, 2, 3])
```

- Use `as` to create shorter or clearer names
- Some aliases are conventions (e.g., `np`, `pd`, `plt`)
---
## `from ... import ... as`

```python
from datetime import datetime as dt
from collections import OrderedDict as OD

now = dt.now()
print(now)
```
---
## Namespaces
- A namespace maps names to objects
- Python has several namespaces:
    - **Built-in**: `print`, `len`, `int`, etc.
    - **Global**: Module-level names
    - **Local**: Function-level names
    - **Enclosing**: Enclosing function names

```python
import math
# math.pi is in the math namespace
# pi would be in your local/global namespace if imported directly
```
---
## The `dir()` Function
- Lists names in a module or current namespace

```python
import math

print(dir(math))
# ['__doc__', '__name__', ..., 'pi', 'sin', 'sqrt', ...]

# Filter to useful names
public = [name for name in dir(math) if not name.startswith("_")]
print(public)
```
---
## The `help()` Function

```python
import json

help(json)           # Full module documentation
help(json.dumps)     # Function documentation
help(json.loads)     # Function documentation
```

- Displays docstrings and usage information
- Extremely useful in the interactive shell
---
## How Python Finds Modules
- Python searches for modules in this order:
    1. Current directory
    1. `PYTHONPATH` environment variable
    1. Installation-dependent default paths

```python
import sys
print(sys.path)
```

- `sys.path` is a list of directories to search
---
## Modifying the Module Search Path

```python
import sys

# Add a directory to the search path
sys.path.append("/home/user/my_modules")
sys.path.insert(0, "/home/user/priority_modules")

# Now Python will look in these directories too
import my_custom_module
```
---
## The `PYTHONPATH` Environment Variable

```bash
# Set in shell before running Python
export PYTHONPATH="/home/user/my_modules:/home/user/other_modules"
python3 my_script.py
```

- Directories in `PYTHONPATH` are added to `sys.path`
- Colon-separated on Unix, semicolon on Windows
---
## Module Attributes
- Every module has special attributes

```python
import math

print(math.__name__)   # 'math'
print(math.__doc__)    # Module docstring
print(math.__file__)   # Path to module file
print(math.__spec__)   # Module specification
```
---
## The `__name__` Variable
- Set to `"__main__"` when script runs directly
- Set to the module name when imported

```python
# my_module.py
def main():
    print("Running as main program")

if __name__ == "__main__":
    main()
```

- Common pattern to make a module both importable and runnable
---
## `__name__` in Action

```python
# greetings.py
def greet(name):
    return f"Hello, {name}!"

if __name__ == "__main__":
    # This only runs when executed directly
    print(greet("World"))
```

```bash
python3 greetings.py       # Prints "Hello, World!"
```

```python
import greetings           # Does NOT print anything
greetings.greet("Alice")   # "Hello, Alice!"
```
---
## Reloading Modules
- Modules are cached after first import
- Changes to module source are not automatically reflected

```python
import importlib
import my_module

# After modifying my_module.py
importlib.reload(my_module)
```

- Useful during interactive development
- Not recommended in production code
---
## Standard Library - `os` Module

```python
import os

print(os.getcwd())          # Current directory
print(os.listdir("."))      # List directory contents
print(os.path.exists("f"))  # Check if path exists
print(os.environ["HOME"])   # Environment variable

os.makedirs("a/b/c", exist_ok=True)  # Create dirs
```
---
## Standard Library - `os.path`

```python
import os.path

path = "/home/user/documents/file.txt"

print(os.path.dirname(path))    # /home/user/documents
print(os.path.basename(path))   # file.txt
print(os.path.splitext(path))   # ('/home/.../file', '.txt')
print(os.path.join("a", "b"))   # a/b
print(os.path.expanduser("~"))  # /home/user
```
---
## Standard Library - `pathlib` (Modern)

```python
from pathlib import Path

p = Path("/home/user/documents/file.txt")
print(p.parent)      # /home/user/documents
print(p.name)        # file.txt
print(p.suffix)      # .txt
print(p.stem)        # file
print(p.exists())    # True/False

# Create path
new = Path("output") / "data" / "results.csv"
print(new)  # output/data/results.csv
```
---
## Standard Library - `sys` Module

```python
import sys

print(sys.version)        # Python version string
print(sys.platform)       # 'linux', 'darwin', 'win32'
print(sys.argv)           # Command-line arguments
print(sys.path)           # Module search paths
print(sys.stdin)          # Standard input
print(sys.stdout)         # Standard output
print(sys.maxsize)        # Max integer for platform
sys.exit(0)               # Exit program
```
---
## Standard Library - `datetime`

```python
from datetime import datetime, date, timedelta

now = datetime.now()
print(now)                        # 2026-03-11 10:30:45.123
print(now.strftime("%Y-%m-%d"))   # 2026-03-11

today = date.today()
birthday = date(1990, 5, 15)
age = today - birthday
print(age.days)  # Days since birthday

tomorrow = today + timedelta(days=1)
```
---
## Standard Library - `json`

```python
import json

# Python dict to JSON string
data = {"name": "Alice", "age": 30}
json_str = json.dumps(data, indent=2)
print(json_str)

# JSON string to Python dict
parsed = json.loads(json_str)
print(parsed["name"])  # Alice

# Read/write JSON files
with open("data.json", "w") as f:
    json.dump(data, f, indent=2)
```
---
## Standard Library - `re` (Regular Expressions)

```python
import re

text = "My phone is 555-1234 and email is a@b.com"

# Find pattern
match = re.search(r"\d{3}-\d{4}", text)
if match:
    print(match.group())  # 555-1234

# Find all matches
numbers = re.findall(r"\d+", text)
print(numbers)  # ['555', '1234']

# Replace
clean = re.sub(r"\d", "X", text)
print(clean)  # My phone is XXX-XXXX and ...
```
---
## Standard Library - `collections`

```python
from collections import Counter, defaultdict, deque

# Counter
words = "the cat sat on the mat the".split()
print(Counter(words))
# Counter({'the': 3, 'cat': 1, 'sat': 1, 'on': 1, 'mat': 1})

# defaultdict
dd = defaultdict(int)
for w in words:
    dd[w] += 1

# deque
d = deque(maxlen=3)
d.extend([1, 2, 3, 4])
print(d)  # deque([2, 3, 4], maxlen=3)
```
---
## Standard Library - `itertools`

```python
from itertools import chain, cycle, product, permutations

# Chain multiple iterables
print(list(chain([1, 2], [3, 4])))  # [1, 2, 3, 4]

# Cartesian product
print(list(product("AB", "12")))
# [('A', '1'), ('A', '2'), ('B', '1'), ('B', '2')]

# Permutations
print(list(permutations("ABC", 2)))
# [('A', 'B'), ('A', 'C'), ('B', 'A'), ...]
```
---
## Standard Library - `functools`

```python
from functools import lru_cache, partial, reduce

# Memoization
@lru_cache(maxsize=128)
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

print(fibonacci(100))  # Instant!

# Partial application
from functools import partial
double = partial(pow, exp=2)
```
---
## Standard Library - `random`

```python
import random

print(random.random())           # Float [0.0, 1.0)
print(random.randint(1, 10))     # Int [1, 10]
print(random.choice([1, 2, 3]))  # Random element

items = [1, 2, 3, 4, 5]
random.shuffle(items)            # Shuffle in place
print(items)

print(random.sample(range(100), 5))  # 5 unique randoms
```
---
## Standard Library - `logging`

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.debug("Debug message")     # Not shown
logger.info("Info message")       # Shown
logger.warning("Warning message") # Shown
logger.error("Error message")     # Shown
logger.critical("Critical!")      # Shown
```
---
## Standard Library - `argparse`

```python
import argparse

parser = argparse.ArgumentParser(description="My tool")
parser.add_argument("filename", help="Input file")
parser.add_argument("-v", "--verbose", action="store_true")
parser.add_argument("-n", "--count", type=int, default=1)

args = parser.parse_args()
print(args.filename)
print(args.verbose)
print(args.count)
```

```bash
python3 tool.py data.txt -v -n 5
```
---
## Standard Library - `unittest`

```python
import unittest

def add(a, b):
    return a + b

class TestAdd(unittest.TestCase):
    def test_positive(self):
        self.assertEqual(add(2, 3), 5)

    def test_negative(self):
        self.assertEqual(add(-1, -1), -2)

    def test_zero(self):
        self.assertEqual(add(0, 0), 0)

if __name__ == "__main__":
    unittest.main()
```
---
## Standard Library Overview
| Module | Purpose |
|--------|---------|
| `os`, `pathlib` | File system operations |
| `sys` | System-specific parameters |
| `json` | JSON encoding/decoding |
| `re` | Regular expressions |
| `datetime` | Date and time |
| `collections` | Specialized containers |
| `itertools` | Iterator building blocks |
| `functools` | Higher-order functions |
| `logging` | Logging facility |
| `argparse` | Command-line parsing |
---
## Circular Imports
- Module A imports B, and B imports A
- Can cause `ImportError` or partial imports

```python
# a.py
from b import func_b

# b.py
from a import func_a  # Circular!
```

- Solutions:
    - Restructure to avoid the cycle
    - Move import inside a function
    - Use late imports
---
## Summary
- Modules are `.py` files that organize reusable code
- Import with `import`, `from ... import`, or aliases
- `dir()` and `help()` for exploring modules
- Python searches `sys.path` for modules
- `__name__ == "__main__"` pattern for runnable modules
- Standard library provides hundreds of useful modules
- Avoid circular imports
