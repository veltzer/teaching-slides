---
tags:
  - languages:python
level: beginner
category: language
audience:
  - audiences:developers

---
# Creating Modules

---
## What Makes a Python Package?
- A directory with Python files
- An `__init__.py` file (can be empty)
- Organized source code
- Optional: tests, documentation, configuration

```tree
my_package/
    __init__.py
    core.py
    utils.py
    helpers.py
```

---
## Simple Module Example

```python
# calculator.py
"""A simple calculator module."""

def add(a, b):
    """Return the sum of a and b."""
    return a + b

def subtract(a, b):
    """Return the difference of a and b."""
    return a - b

def multiply(a, b):
    """Return the product of a and b."""
    return a * b
```

---
## Using Your Module

```python
# main.py (in the same directory)
import calculator

print(calculator.add(2, 3))       # 5
print(calculator.subtract(10, 4))  # 6

# Or import specific functions
from calculator import add, multiply
print(add(2, 3))        # 5
print(multiply(4, 5))   # 20
```

---
## Package Directory Structure

```tree
my_project/
    src/
        my_package/
            __init__.py
            core.py
            utils.py
            models/
                __init__.py
                user.py
                product.py
    tests/
        test_core.py
        test_utils.py
    pyproject.toml
    README.md
```

---
## The `__init__.py` File
- Makes a directory a Python package
- Can be empty or contain initialization code
- Controls what gets imported with `from package import *`

```python
# my_package/__init__.py
"""My awesome package."""

from .core import main_function
from .utils import helper_function

__version__ = "1.0.0"
__all__ = ["main_function", "helper_function"]
```

---
## Relative Imports

```python
# my_package/core.py
from .utils import helper_function
from .models.user import User
from ..other_package import something  # Parent package

# Dot notation:
# .  = current package
# .. = parent package
```

- Relative imports use dots to specify location
- Only work inside packages

---
## Absolute vs Relative Imports

```python
# Absolute import (always works)
from my_package.utils import helper

# Relative import (within a package)
from .utils import helper
from . import utils
```

- PEP 8 recommends absolute imports for clarity
- Relative imports are fine within a package

---
## The `__all__` Variable
- Controls what `from module import *` exports

```python
# utils.py
__all__ = ["public_function", "PublicClass"]

def public_function():
    pass

def _private_function():
    pass

class PublicClass:
    pass

class _InternalClass:
    pass
```

---
## Module-Level Variables

```python
# config.py
"""Configuration module."""

__version__ = "2.1.0"
__author__ = "Alice Smith"

# Module-level constants
DEFAULT_TIMEOUT = 30
MAX_RETRIES = 3
BASE_URL = "https://api.example.com"
```

---
## Documenting with Docstrings
- Every module, class, and function should have a docstring
- Follow Google, NumPy, or Sphinx style

```python
def fetch_data(url, timeout=30):
    """Fetch data from a URL.

    Args:
        url: The URL to fetch data from.
        timeout: Request timeout in seconds.

    Returns:
        The response data as a dictionary.

    Raises:
        ConnectionError: If the connection fails.
        TimeoutError: If the request times out.
    """
    pass
```

---
## Google Style Docstrings

```python
def calculate(numbers, operation="sum"):
    """Perform a calculation on a list of numbers.

    Args:
        numbers: A list of numbers to process.
        operation: The operation to perform.
            Can be "sum", "mean", or "product".

    Returns:
        The result of the calculation.

    Example:
        >>> calculate([1, 2, 3], "sum")
        6
    """
    pass
```

---
## NumPy Style Docstrings

```python
def calculate(numbers, operation="sum"):
    """Perform a calculation on a list of numbers.

    Parameters
    ----------
    numbers : list of float
        A list of numbers to process.
    operation : str, optional
        The operation to perform (default "sum").

    Returns
    -------
    float
        The result of the calculation.
    """
    pass
```

---
## Testing with `pytest`

```python
# test_calculator.py
from calculator import add, subtract, multiply

def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0

def test_subtract():
    assert subtract(5, 3) == 2
    assert subtract(0, 5) == -5

def test_multiply():
    assert multiply(3, 4) == 12
    assert multiply(0, 100) == 0
```

---
## Running `pytest`

```bash
# Install pytest
pip install pytest

# Run all tests
pytest

# Run specific file
pytest test_calculator.py

# Verbose output
pytest -v

# Run specific test
pytest test_calculator.py::test_add

# Show print output
pytest -s
```

---
## `pytest` - Fixtures

```python
import pytest

@pytest.fixture
def sample_data():
    return [1, 2, 3, 4, 5]

@pytest.fixture
def empty_list():
    return []

def test_sum(sample_data):
    assert sum(sample_data) == 15

def test_empty(empty_list):
    assert len(empty_list) == 0
```

---
## `pytest` - Parametrize

```python
import pytest
from calculator import add

@pytest.mark.parametrize("a, b, expected", [
    (1, 2, 3),
    (0, 0, 0),
    (-1, 1, 0),
    (100, 200, 300),
    (-5, -3, -8),
])
def test_add(a, b, expected):
    assert add(a, b) == expected
```

---
## `pytest` - Testing Exceptions

```python
import pytest

def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a / b

def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

def test_divide_by_zero_message():
    with pytest.raises(ZeroDivisionError, match="Cannot divide"):
        divide(10, 0)
```

---
## `pytest` - Markers

```python
import pytest

@pytest.mark.slow
def test_large_computation():
    # Takes a long time
    result = compute_large_dataset()
    assert result is not None

@pytest.mark.skip(reason="Not implemented yet")
def test_future_feature():
    pass

@pytest.mark.skipif(
    sys.platform == "win32",
    reason="Unix only"
)
def test_unix_feature():
    pass
```

---
## `pytest` - Configuration (`pytest.ini`)

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_functions = test_*
markers =
    slow: marks tests as slow
    integration: marks integration tests
addopts = -v --tb=short
```

---
## `pytest` - Coverage

```bash
# Install coverage plugin
pip install pytest-cov

# Run with coverage
pytest --cov=my_package

# Generate HTML report
pytest --cov=my_package --cov-report=html
```

```output
---------- coverage: ----------
Name                   Stmts   Miss  Cover
------------------------------------------
my_package/__init__.py     3      0   100%
my_package/core.py        25      3    88%
my_package/utils.py       15      2    87%
------------------------------------------
TOTAL                     43      5    88%
```

---
## `pyproject.toml` - Modern Configuration

```toml
[build-system]
requires = ["setuptools>=68.0"]
build-backend = "setuptools.backends._legacy:_Backend"

[project]
name = "my-package"
version = "1.0.0"
description = "My awesome package"
readme = "README.md"
requires-python = ">=3.10"
license = {text = "MIT"}
authors = [{name = "Alice", email = "alice@example.com"}]
dependencies = [
    "requests>=2.28",
    "click>=8.0",
]

[project.optional-dependencies]
dev = ["pytest>=7.0", "black", "mypy"]
```

---
## Entry Points (CLI Tools)

```toml
[project.scripts]
my-tool = "my_package.cli:main"
```

```python
# my_package/cli.py
import click

@click.command()
@click.argument("name")
def main(name):
    """Greet someone."""
    click.echo(f"Hello, {name}!")
```

```bash
pip install -e .
my-tool Alice  # Hello, Alice!
```

---
## Development Installation

```bash
# Install in development mode (editable)
pip install -e .

# Install with dev dependencies
pip install -e ".[dev]"
```

- `-e` (editable) mode links the package to your source
- Changes to code are reflected immediately
- No need to reinstall after every change

---
## Building and Distributing

```bash
# Install build tools
pip install build twine

# Build the package
python3 -m build

# This creates:
# dist/my_package-1.0.0.tar.gz
# dist/my_package-1.0.0-py3-none-any.whl

# Upload to PyPI
twine upload dist/*

# Upload to TestPyPI first
twine upload --repository testpypi dist/*
```

---
## Project Layout - `src` Layout

```tree
my-project/
    src/
        my_package/
            __init__.py
            core.py
    tests/
        test_core.py
    pyproject.toml
    README.md
    LICENSE
    .gitignore
```

- The `src` layout prevents accidental imports from the project root
- Recommended for distributable packages

---
## `.gitignore` for Python Projects

```config
__pycache__/
*.py[cod]
*.egg-info/
dist/
build/
.venv/
.env
*.egg
.pytest_cache/
.mypy_cache/
htmlcov/
.coverage
```

---
## Type Checking Your Package

```python
# my_package/utils.py
def process_items(items: list[str]) -> dict[str, int]:
    """Count the length of each item."""
    return {item: len(item) for item in items}
```

```bash
# Run mypy
mypy src/my_package/

# Add to pyproject.toml
# [tool.mypy]
# strict = true
```

---
## Summary
- Packages are directories with `__init__.py`
- Use relative imports within packages
- Document code with docstrings (Google or NumPy style)
- Test with `pytest` (fixtures, parametrize, markers)
- Configure builds with `pyproject.toml`
- Use `pip install -e .` for development
- Build with `python -m build`, publish with `twine`
- Use `src` layout for distributable packages
