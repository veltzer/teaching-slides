# Debugging, Linting, and Testing your Python Code

## Overview
- Python debugging techniques and tools
- Using assertions correctly
- Type hints for code quality
- Linting and static analysis tools
- Unit testing with unittest and pytest
- Test organization and best practices
- Code coverage analysis

---

## Code Quality Fundamentals

## The Python Code Quality Ecosystem
- Debugging: Find and fix logical errors
- Linting: Identify stylistic and potential issues
- Type checking: Verify type consistency
- Testing: Verify functional correctness
- Coverage analysis: Ensure thorough testing

```python
# A function with multiple quality issues
def caLc_average(vals):
    # No type hints, inconsistent naming
    total = 0
    for val in vals:
        total = total + val  # Inefficient, could use sum()
    return total / len(vals)  # Will fail on empty list
```

---

## Debugging Techniques

## Print Debugging
- Simplest form of debugging
- Add print statements to track execution
- View variable values at different points
- Quick but limited approach
- Difficult in complex programs

```python
def calculate_total(items):
    print(f"Starting with items: {items}")

    total = 0
    for i, item in enumerate(items):
        print(f"Processing item {i}: {item}")
        value = item['value']
        print(f"  Value: {value}")
        total += value
        print(f"  Running total: {total}")

    print(f"Final total: {total}")
    return total
```

---

## Debugging Techniques

## Logging
- More sophisticated than print statements
- Configurable output levels
- Can be enabled/disabled as needed
- Output to multiple destinations
- Remains in code for production use

```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def calculate_total(items):
    logger.debug(f"Starting with {len(items)} items")

    total = 0
    for item in items:
        logger.debug(f"Processing item: {item}")
        try:
            total += item['value']
        except KeyError:
            logger.error(f"Missing 'value' key in item: {item}")

    logger.info(f"Final total: {total}")
    return total
```

---

## Python Debuggers

## Python Debugger (pdb)
- Built-in Python debugger
- Interactive command-line interface
- Set breakpoints and step through code
- Inspect variables at runtime
- Available in any Python installation

```python
import pdb

def complex_function(data):
    result = []
    for item in data:
        # Set a breakpoint
        pdb.set_trace()
        # Debug commands:
        # n (next) - execute current line
        # s (step) - step into function call
        # c (continue) - continue execution
        # q (quit) - exit debugger
        # p <expr> - evaluate and print expression
        processed = process_item(item)
        result.append(processed)
    return result
```

---

## Python Debuggers

## pdb Commands
- `l` (list): Show current line in context
- `n` (next): Execute current line, proceed to next
- `s` (step): Step into function called on current line
- `c` (continue): Continue execution until next breakpoint
- `p <expr>`: Print value of expression
- `pp <expr>`: Pretty-print value of expression
- `q` (quit): Quit debugger and execution
- `b <line>`: Set breakpoint at line number
- `h` (help): Show command help

---

## Python Debuggers

## breakpoint() Function
- Added in Python 3.7
- Built-in function to enter the debugger
- Uses environment variable to select debugger
- Cleaner than import pdb; pdb.set_trace()
- Can be globally disabled with PYTHONBREAKPOINT=0

```python
def complex_calculation(data):
    result = initial_processing(data)

    # Insert breakpoint
    breakpoint()

    # Code will pause here when running
    final_result = final_processing(result)
    return final_result

# Disable all breakpoints
# PYTHONBREAKPOINT=0 python script.py

# Use a different debugger
# PYTHONBREAKPOINT=pudb.set_trace python script.py
```

---

## Python Debuggers

## IPython and ipdb
- Enhanced interactive debugger
- Better display of variables
- Tab completion
- Syntax highlighting
- Integration with IPython/Jupyter
- Improved development experience

```python
# Install ipdb
# pip install ipdb

import ipdb

def problematic_function():
    data = [1, 2, 3, 4]
    result = []

    ipdb.set_trace()

    for x in data:
        # Complex processing that might have bugs
        y = complex_operation(x)
        result.append(y)

    return result
```

---

## Python Debuggers

## pudb
- Visual, console-based debugger
- TUI (Text User Interface)
- Shows code, variables, stack simultaneously
- Easier to navigate than pdb
- Works in terminal environments

```python
# Install pudb
# pip install pudb

import pudb

def analyze_data(data):
    # Start the visual debugger
    pudb.set_trace()

    results = {}
    for key, values in data.items():
        if not values:
            continue

        results[key] = sum(values) / len(values)

    return results
```

---

## Python Debuggers

## IDE Debuggers
- Visual Studio Code, PyCharm, etc.
- Graphical debugging interface
- Set breakpoints with a click
- Watch variables in separate windows
- Step controls with buttons
- Visualize data structures
- Conditional breakpoints
- Debug configurations

---

## Python Debuggers

## Remote Debugging
- Debug code running in a different process
- Connect to running application
- Useful for web applications, microservices
- Several options available (pdb++, remote-pdb)
- Most IDEs support remote debugging

```python
# Using remote-pdb
# pip install remote-pdb

from remote_pdb import RemotePdb

def function_to_debug():
    # Start a remote debugger on port 4444
    RemotePdb('127.0.0.1', 4444).set_trace()

    # Continue with code to debug
    result = complex_calculation()
    return result

# Connect with telnet:
# telnet 127.0.0.1 4444
```

---

## Python Debuggers

## Post-Mortem Debugging
- Analyze program after it crashes
- Examine stack trace and variables
- Understand what led to the exception
- Available in pdb and other debuggers

```python
import pdb

def main():
    try:
        result = problematic_function()
        print(f"Result: {result}")
    except Exception:
        # Enter post-mortem debugging on exception
        pdb.post_mortem()

def problematic_function():
    data = [1, 2, 3]
    # This will raise an IndexError
    return data[10]

if __name__ == "__main__":
    main()
```

---

## Using Assertions Correctly

## What Are Assertions?
- Runtime checks for program correctness
- Validate assumptions and invariants
- Crash early when assumptions are violated
- Disabled when running with -O flag
- Not for input validation or error handling

```python
def calculate_average(numbers):
    # Validate internal assumption
    assert len(numbers) > 0, "Cannot calculate average of empty list"
    assert all(isinstance(n, (int, float)) for n in numbers), "All values must be numeric"

    return sum(numbers) / len(numbers)

# Appropriate use - checking internal logic
def binary_search(sorted_list, item):
    # Verify the list is actually sorted
    assert all(sorted_list[i] <= sorted_list[i+1] for i in range(len(sorted_list)-1))

    # Binary search implementation...
```

---

## Using Assertions Correctly

## When to Use Assertions
- Checking internal invariants
- Validating function preconditions
- Verifying postconditions and invariants
- Checking assumptions about internal state
- Detecting impossible conditions
- Documentation of logical assumptions

```python
class Rectangle:
    def __init__(self, width, height):
        assert width > 0, "Width must be positive"
        assert height > 0, "Height must be positive"
        self.width = width
        self.height = height

    def set_width(self, width):
        assert width > 0, "Width must be positive"
        self.width = width

    def area(self):
        # Invariant check
        assert self.width > 0 and self.height > 0, "Invalid rectangle state"
        return self.width * self.height
```

---

## Using Assertions Correctly

## When Not to Use Assertions
- Validating user input
- Handling expected error conditions
- Checking for events that should trigger exceptions
- Situations that must be handled in production
- Performance-critical code

```python
# Bad - assertion might be disabled with -O
def process_user_data(data):
    assert "username" in data, "Username is required"  # Wrong!
    return data["username"]

# Good - explicit validation with exceptions
def process_user_data(data):
    if "username" not in data:
        raise ValueError("Username is required")
    return data["username"]
```

---

## Using Assertions Correctly

## Advanced Assertion Techniques
- Use with classes to enforce contracts
- Validate complex data structures
- Create self-documenting code
- Detect edge cases
- Support debugging

```python
class DataProcessor:
    def process(self, dataset):
        # Pre-condition
        assert isinstance(dataset, list), "Dataset must be a list"
        assert all(isinstance(item, dict) for item in dataset), "All items must be dictionaries"

        result = self._process_items(dataset)

        # Post-condition
        assert len(result) == len(dataset), "Result length changed unexpectedly"
        assert all(isinstance(r, dict) for r in result), "Not all results are dictionaries"

        return result
```

---

## Type Hints

## Introduction to Type Hints
- Added in Python 3.5 (PEP 484)
- Static type annotations
- Not enforced at runtime
- Checked by external tools
- Improved code readability
- Better IDE autocompletion and error detection

```python
def greeting(name: str) -> str:
    return f"Hello, {name}!"

def calc_stats(values: list[float]) -> dict[str, float]:
    return {
        "mean": sum(values) / len(values),
        "min": min(values),
        "max": max(values)
    }

# Function with multiple parameter types
def process_item(item_id: int, details: dict[str, str]) -> bool:
    # Implementation...
    return True
```

---

## Type Hints

## Basic Type Annotations
- Primitive types: `int`, `float`, `str`, `bool`
- Container types: `list`, `dict`, `tuple`, `set`
- Generic types: `List[T]`, `Dict[K, V]`, `Set[T]`
- `None` and `Optional[T]`
- `Any` type for flexibility
- Union types with `Union[T1, T2]` or `T1 | T2` (Python 3.10+)

```python
from typing import List, Dict, Optional, Union, Any

# Variable annotations
name: str = "Alice"
age: int = 30
scores: List[int] = [95, 89, 92]
user_info: Dict[str, Union[str, int]] = {"name": "Bob", "age": 25}
maybe_score: Optional[int] = None  # None or int

# Function with optional parameter
def find_user(user_id: int, details: bool = False) -> Optional[Dict[str, Any]]:
    # Implementation...
    return None
```

---

## Type Hints

## Advanced Type Annotations
- Type aliases
- Callable types
- TypeVar for generics
- NewType for distinct types
- Protocol for duck typing
- Literal types
- TypedDict for dictionary structure

```python
from typing import Callable, TypeVar, NewType, Protocol, List, Dict, Literal

# Type alias
UserId = int
UserDict = Dict[str, str]

# Custom type
AdminId = NewType('AdminId', int)

# Generic type variable
T = TypeVar('T')

def first(items: List[T]) -> T:
    return items[0]

# Function types
Processor = Callable[[str], str]

def apply_processor(text: str, processor: Processor) -> str:
    return processor(text)

# Literal types
Mode = Literal["r", "w", "a", "r+", "w+", "a+"]
def open_file(path: str, mode: Mode) -> None:
    # Implementation...
    pass
```

---

## Type Hints

## Class and Method Type Hints
- Annotations for class methods
- Self parameter doesn't need annotation
- Return type annotations
- Property type hints
- Forward references for recursive types

```python
class User:
    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age

    def greet(self) -> str:
        return f"Hello, I'm {self.name}"

    def is_adult(self) -> bool:
        return self.age >= 18

    @property
    def username(self) -> str:
        return self.name.lower().replace(" ", "_")

    # Forward reference (for recursive types)
    def get_friends(self) -> List["User"]:
        # Implementation...
        pass
```

---

## Type Hints

## Type Checking with mypy
- Static type checker for Python
- Analyzes code without running it
- Identifies type inconsistencies
- Integrates with CI/CD pipelines
- Configurable strictness

```bash
# Install mypy
pip install mypy

# Check a file
mypy script.py

# Check with specific Python version
mypy --python-version 3.8 script.py

# More strict checking
mypy --strict script.py

# Configuration file (mypy.ini)
# [mypy]
# python_version = 3.8
# warn_return_any = True
# disallow_untyped_defs = True
```

---

## Type Hints

## Type Checking in IDEs
- Real-time type checking
- Error highlighting
- Autocompletion based on types
- Refactoring support
- PyCharm, VS Code with Pylance, etc.

```python
# IDE can detect these errors:

def process_name(name: str) -> str:
    return name.upper()

# Error: Argument has incompatible type
process_name(123)

# Error: Return type mismatch
def get_age() -> str:
    return 25

# Error: Incompatible attribute type
class Person:
    name: str

person = Person()
person.name = 42
```

---

## Linting Tools

## What is Linting?
- Static code analysis
- Identify stylistic issues
- Find potential bugs
- Enforce coding standards
- Improve code maintainability
- Run before code execution

---

## Linting Tools

## pylint
- Comprehensive Python linter
- Checks for errors, enforces coding standards
- Evaluates code complexity
- Highly configurable
- Generates detailed reports
- Integrates with editors and CI

```bash
# Install pylint
pip install pylint

# Run pylint on a file
pylint script.py

# Run on a package
pylint mypackage/

# Generate configuration file
pylint --generate-rcfile > .pylintrc

# Sample output:
# ************* Module script
# script.py:10:0: C0111: Missing module docstring (missing-docstring)
# script.py:12:4: W0612: Unused variable 'unused' (unused-variable)
# script.py:15:0: C0111: Missing function docstring (missing-docstring)
```

---

## Linting Tools

## flake8
- Lightweight, fast linter
- Combines PyFlakes, pycodestyle, McCabe
- Checks for errors and style issues
- Less opinionated than pylint
- Easier to adopt in existing projects
- Extensible with plugins

```bash
# Install flake8
pip install flake8

# Run flake8 on a file
flake8 script.py

# Run on a directory
flake8 mypackage/

# Configuration in setup.cfg or .flake8
# [flake8]
# max-line-length = 88
# extend-ignore = E203
# exclude = .git,__pycache__,build,dist
```

---

## Linting Tools

## black
- Code formatter, not a traditional linter
- "Uncompromising" Python code formatter
- Enforces consistent style
- Minimal configuration options
- Resolves style debates in teams
- Widely adopted in modern Python projects

```bash
# Install black
pip install black

# Format a file
black script.py

# Format all Python files in a directory
black mypackage/

# Check if files would be reformatted
black --check script.py

# Configuration in pyproject.toml
# [tool.black]
# line-length = 88
# target-version = ['py38']
# include = '\.pyi?$'
# exclude = '/(\.git|\.hg|\.mypy_cache|\.tox|\.venv|_build|buck-out|build|dist)/'
```

---

## Linting Tools

## isort
- Sorts and formats imports
- Groups imports by type
- Removes unused imports
- Combines well with black
- Ensures consistent import organization

```bash
# Install isort
pip install isort

# Sort imports in a file
isort script.py

# Check if files need sorting
isort --check script.py

# Configuration that works with black
# [tool.isort]
# profile = "black"
# multi_line_output = 3
```

---

## Linting Tools

## Combining Linting Tools
- Use multiple tools for comprehensive checks
- Automate with pre-commit hooks
- Standardize across team
- Configure compatible settings
- Integrate with CI/CD

```yaml
# .pre-commit-config.yaml
repos:
-   repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
    -   id: trailing-whitespace
    -   id: end-of-file-fixer
-   repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
    -   id: isort
-   repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
    -   id: black
-   repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
    -   id: flake8
```

---

## Testing Fundamentals

## Testing Pyramid
- Unit tests: Test individual components
- Integration tests: Test component interactions
- End-to-end tests: Test entire system
- Ratio should favor unit tests (fast, focused)
- Balance coverage and test time

```txt
        /\
       /  \
      /    \
     / E2E  \
    /--------\
   /          \
  / Integration \
 /----------------\
/      Unit        \
---------------------
```

---

## Testing Fundamentals

## Test-Driven Development (TDD)
- Write test before implementation
- Red-Green-Refactor cycle
- Design from the user perspective
- Small, incremental changes
- Immediate feedback on code changes
- Built-in regression testing

```python
# TDD Example

# 1. Write test first (Red)
def test_calculate_total():
    items = [{'value': 10}, {'value': 20}, {'value': 30}]
    assert calculate_total(items) == 60

    empty_items = []
    assert calculate_total(empty_items) == 0

# 2. Write minimal implementation (Green)
def calculate_total(items):
    if not items:
        return 0
    return sum(item['value'] for item in items)

# 3. Refactor if needed while keeping tests passing
```

---

## Testing Fundamentals

## Testing Vocabulary
- Test case: Specific test scenario
- Test suite: Collection of test cases
- Test fixture: Setup/teardown environment
- Test runner: Executes tests and reports results
- Assertions: Verify expected outcomes
- Mocks/Stubs: Test isolation components
- Test coverage: Measure of code exercised by tests

---

## Testing with unittest

## The unittest Framework
- Standard library testing framework
- Inspired by JUnit (Java)
- Class-based test organization
- Rich set of assertions
- Test discovery and execution
- Support for fixtures and mocks

```python
import unittest

class TestStringMethods(unittest.TestCase):
    def test_upper(self):
        self.assertEqual('hello'.upper(), 'HELLO')

    def test_isupper(self):
        self.assertTrue('HELLO'.isupper())
        self.assertFalse('Hello'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])

if __name__ == '__main__':
    unittest.main()
```

---

## Testing with unittest

## unittest Assertions
- `assertEqual(a, b)` - Check if a == b
- `assertNotEqual(a, b)` - Check if a != b
- `assertTrue(x)` - Check if bool(x) is True
- `assertFalse(x)` - Check if bool(x) is False
- `assertIs(a, b)` - Check if a is b
- `assertIsNot(a, b)` - Check if a is not b
- `assertIsNone(x)` - Check if x is None
- `assertIsNotNone(x)` - Check if x is not None
- `assertIn(a, b)` - Check if a in b
- `assertNotIn(a, b)` - Check if a not in b
- `assertRaises(exc, fun, *args, **kwds)` - Check if fun(*args, **kwds) raises exc

---

## Testing with unittest

## Test Fixtures with unittest
- `setUp()`: Prepare for each test
- `tearDown()`: Clean up after each test
- `setUpClass()`: One-time setup for class
- `tearDownClass()`: One-time teardown for class
- Common patterns for resource management

```python
import unittest
import tempfile
import os

class TestFileOperations(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create a temporary directory
        cls.temp_dir = tempfile.mkdtemp()

    def setUp(self):
        # Create a new test file for each test
        self.test_file = os.path.join(self.temp_dir, "test.txt")
        with open(self.test_file, "w") as f:
            f.write("Initial content")

    def test_read_file(self):
        with open(self.test_file, "r") as f:
            content = f.read()
        self.assertEqual(content, "Initial content")

    def tearDown(self):
        # Remove test file after each test
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    @classmethod
    def tearDownClass(cls):
        # Remove temporary directory
        os.rmdir(cls.temp_dir)
```

---

## Testing with unittest

## Running unittest Tests
- Run a single test file
- Discover and run all tests
- Filter tests to run
- Control verbosity
- Generate test reports

```bash
# Run a single test file
python test_module.py

# Run with more details
python -m unittest -v test_module.py

# Run a specific test
python -m unittest test_module.TestClass.test_method

# Discover and run all tests
python -m unittest discover

# Discover with specific pattern and directory
python -m unittest discover -s tests -p "test_*.py"
```

---

## Testing with pytest

## Introduction to pytest
- Popular third-party testing framework
- Simple, elegant syntax
- Powerful fixture system
- Rich plugin ecosystem
- Detailed failure reports
- Compatible with unittest tests

```python
# Install pytest
# pip install pytest

# Simple pytest test function
def test_addition():
    assert 1 + 1 == 2

def test_string_methods():
    assert 'hello'.upper() == 'HELLO'
    assert 'HELLO'.isupper() is True
    assert 'Hello'.isupper() is False

# Run with: pytest test_file.py
# or simply: pytest (for automatic discovery)
```

---

## Testing with pytest

## pytest Fixtures
- Function for setting up test resources
- Declarative dependency injection
- Support for setup/teardown via yield
- Scoped at function, class, module, or session
- Composable and reusable

```python
import pytest
import tempfile
import os

@pytest.fixture
def temp_file():
    # Setup: create a temporary file
    fd, path = tempfile.mkstemp()
    with os.fdopen(fd, 'w') as f:
        f.write("Test content")

    # Provide the resource
    yield path

    # Teardown: remove the file
    os.unlink(path)

def test_read_file(temp_file):
    # The fixture value is passed as an argument
    with open(temp_file, 'r') as f:
        content = f.read()
    assert content == "Test content"
```

---

## Testing with pytest

## pytest Advanced Features
- Parameterized tests
- Marking tests (skip, xfail, etc.)
- Filtering tests to run
- Fixture factories
- Plugins for coverage, async, etc.

```python
import pytest

# Parameterized tests
@pytest.mark.parametrize("input,expected", [
    ("hello", "HELLO"),
    ("world", "WORLD"),
    ("Python", "PYTHON"),
])
def test_upper(input, expected):
    assert input.upper() == expected

# Marking tests
@pytest.mark.slow
def test_slow_operation():
    # Long running test
    pass

# Conditional skip
@pytest.mark.skipif(sys.platform == "win32", reason="Does not run on Windows")
def test_linux_only():
    # Linux-specific test
    pass
```

---

## Testing with pytest

## Running pytest Tests
- Automatic test discovery
- Verbose and quiet modes
- Filter by test name or marker
- Stop on first failure
- Generate reports

```bash
# Run all tests
pytest

# Run with more details
pytest -v

# Run a specific test file
pytest test_module.py

# Run a specific test
pytest test_module.py::test_function

# Run tests matching a pattern
pytest -k "addition or subtraction"

# Run tests with a specific marker
pytest -m slow

# Stop on first failure
pytest -x

# Show N slowest tests
pytest --durations=5
```

---

## Mocking

## Introduction to Mocking
- Replace parts of the system with mock objects
- Verify interactions with dependencies
- Simulate various conditions (errors, etc.)
- Isolate unit under test
- Control test environment

```python
# Using unittest.mock (built-in since Python 3.3)
from unittest.mock import Mock, patch

# Create a mock object
mock_database = Mock()
mock_database.get_user.return_value = {"id": 1, "name": "Test User"}

# Use the mock
def test_get_user_name():
    user = mock_database.get_user(1)
    assert user["name"] == "Test User"
    mock_database.get_user.assert_called_once_with(1)
```

---

## Mocking

## Patching with Mock
- Replace objects during tests
- Patch functions, classes, or modules
- Use as decorator or context manager
- Restore original object after test
- Control return values and side effects

```python
import requests
from unittest.mock import patch

def get_user_data(user_id):
    response = requests.get(f"https://api.example.com/users/{user_id}")
    return response.json()

# Patch with decorator
@patch('requests.get')
def test_get_user_data(mock_get):
    # Configure the mock
    mock_response = Mock()
    mock_response.json.return_value = {"id": 123, "name": "Test User"}
    mock_get.return_value = mock_response

    # Call the function
    result = get_user_data(123)

    # Assertions
    mock_get.assert_called_once_with("https://api.example.com/users/123")
    assert result["name"] == "Test User"

# Patch with context manager
def test_get_user_data_context():
    with patch('requests.get') as mock_get:
        # Configure and test as above
        pass
```

---

## Mocking

## Mock Assertions and Verification
- Verify call counts
- Check call arguments
- Inspect call history
- Verify call order
- Assert not called

```python
from unittest.mock import Mock, call

# Create mock
mock_service = Mock()

# Call the mock multiple times
mock_service.process(1)
mock_service.process(2)
mock_service.other_method()

# Assertions
mock_service.process.assert_called_with(2)  # Last call was with 2
mock_service.process.assert_any_call(1)     # Was called with 1 at some point
assert mock_service.process.call_count == 2  # Called twice

# Check call history
expected_calls = [call(1), call(2)]
mock_service.process.assert_has_calls(expected_calls, any_order=False)

# Check if method was called
assert mock_service.other_method.called
```

---

## Mocking

## MagicMock and spec
- `MagicMock` supports magic methods
- `spec` validates attribute access
- `autospec` copies the API of the mocked object
- More type safety in mocks
- Prevents typos and attribute errors

```python
from unittest.mock import Mock, MagicMock, create_autospec

# MagicMock allows magic methods
mock_list = MagicMock()
result = mock_list[0]  # Works with __getitem__
str_result = str(mock_list)  # Works with __str__

# Mock with spec
mock_dict = Mock(spec=dict)
mock_dict["key"] = "value"  # Works
# mock_dict.invalid_method()  # Raises AttributeError

# Autospec
def complex_function(a, b, c=None):
    return a + b + (c or 0)

mock_func = create_autospec(complex_function)
mock_func(1, 2)  # Works
# mock_func(1)  # Raises TypeError - missing argument
```

---

## Mocking

## Side Effects with Mocks
- Return different values on successive calls
- Raise exceptions
- Call custom functions
- Simulate complex behavior

```python
from unittest.mock import Mock

# Return different values on successive calls
mock_function = Mock()
mock_function.side_effect = [1, 2, 3]
print(mock_function())  # 1
print(mock_function())  # 2
print(mock_function())  # 3

# Raise an exception
error_mock = Mock()
error_mock.side_effect = ValueError("Test error")
# error_mock()  # Raises ValueError

# Custom function as side effect
def custom_effect(arg):
    if arg < 0:
        raise ValueError("Negative value")
    return arg * 2

custom_mock = Mock()
custom_mock.side_effect = custom_effect
print(custom_mock(5))  # 10
# custom_mock(-1)  # Raises ValueError
```

---

## Test Organization

## Project Test Structure
- Common test organization patterns
- Test discovery considerations
- Package vs. module testing
- Integration with build tools

```txt
project/
├── src/
│   └── mypackage/
│       ├── __init__.py
│       ├── module1.py
│       └── module2.py
├── tests/
│   ├── __init__.py
│   ├── test_module1.py
│   ├── test_module2.py
│   ├── integration/
│   │   └── test_integration.py
│   └── conftest.py  # Shared pytest fixtures
└── setup.py
```

---

## Test Organization

## Test Naming Conventions
- Files: `test_*.py` or `*_test.py`
- Functions: `test_*`
- Classes: `Test*`
- Methods: `test_*`
- Follow consistent patterns for clarity
- Group related tests together

```python
# test_user_service.py

def test_create_user():
    # Test user creation
    pass

def test_get_user_by_id():
    # Test retrieving a user
    pass

def test_update_user_profile():
    # Test updating user profile
    pass

class TestUserAuthentication:
    def test_login(self):
        # Test user login
        pass

    def test_logout(self):
        # Test user logout
        pass
```

---

## Test Organization

## Shared Test Fixtures
- Reuse setup/teardown code
- Share fixtures across test modules
- Reduce duplication
- Maintain consistency
- pytest: conftest.py
- unittest: base test classes

```python
# conftest.py for pytest
import pytest
import tempfile
import os

@pytest.fixture(scope="session")
def database_connection():
    # Set up test database
    db = connect_to_test_db()
    yield db
    # Tear down test database
    db.close()

@pytest.fixture
def test_user(database_connection):
    # Create a test user
    user = database_connection.create_user("testuser", "password")
    yield user
    # Remove test user
    database_connection.delete_user(user.id)
```

---

## Test Organization

## Test Categories and Markers
- Group tests by category
- Enable selective test running
- Mark tests with metadata
- Skip tests conditionally
- unittest: subTest, skipIf
- pytest: mark

```python
# pytest markers
import pytest
import sys

# Custom markers
pytest.mark.slow        # Slow tests
pytest.mark.integration # Integration tests
pytest.mark.api         # API tests

# Built-in markers
@pytest.mark.skip(reason="Not implemented yet")
def test_future_feature():
    pass

@pytest.mark.skipif(sys.platform == "win32", reason="Unix only test")
def test_unix_specific():
    pass

@pytest.mark.xfail
def test_expected_to_fail():
    assert False
```

---

## Test Organization

## tox: Testing in Multiple Environments
- Test with multiple Python versions
- Automated test environments
- Standardized testing workflow
- Consistent environment for CI
- Configuration in tox.ini

```ini
# tox.ini
[tox]
envlist = py36, py37, py38, py39

[testenv]
deps =
    pytest
    pytest-cov
commands =
    pytest --cov=mypackage tests/

[testenv:lint]
deps =
    flake8
    black
commands =
    flake8 src/mypackage
    black --check src/mypackage
```

---

## Code Coverage

## Introduction to Code Coverage
- Measure which code is executed by tests
- Identify untested code
- Set quality targets
- Four main types:
    - Line coverage: lines executed
    - Branch coverage: conditional branches taken
    - Function coverage: functions called
    - Statement coverage: statements executed

---

## Code Coverage

## coverage.py
- Standard Python coverage tool
- Measures line coverage
- Generate HTML, XML, and console reports
- Configurable
- Integrates with testing frameworks

```bash
# Install coverage.py
pip install coverage

# Run with coverage
coverage run -m unittest discover

# Generate report
coverage report -m

# Generate HTML report
coverage html

# Sample output:
# Name                      Stmts   Miss  Cover   Missing
# -------------------------------------------------------
# mypackage/__init__.py         4      0   100%
# mypackage/module1.py         20      4    80%   24-27
# mypackage/module2.py         15      7    53%   11-23
# -------------------------------------------------------
# TOTAL                        39     11    72%
```

---

## Code Coverage

## pytest-cov
- pytest plugin for coverage.py
- Simplifies coverage with pytest
- Same reporting options
- More integrated workflow

```bash
# Install pytest-cov
pip install pytest-cov

# Run tests with coverage
pytest --cov=mypackage

# Generate reports
pytest --cov=mypackage --cov-report=term-missing
pytest --cov=mypackage --cov-report=html

# Enforce minimum coverage
pytest --cov=mypackage --cov-fail-under=80
```

---

## Code Coverage

## Coverage Configuration
- .coveragerc file
- Control what to measure
- Exclude files or lines
- Set branch coverage
- Configure reporting

```ini
# .coveragerc
[run]
source = mypackage
branch = True
omit =
    */tests/*
    */__init__.py

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise NotImplementedError
    if __name__ == .__main__.:
    pass
    raise ImportError

[html]
directory = coverage_html_report
```

---

## Code Coverage

## Understanding Coverage Reports
- Interpreting coverage numbers
- High coverage ≠ good tests
- Uncovered lines vs. important code
- Balancing coverage and maintainability
- Setting reasonable targets

```txt
Coverage Report Guidelines:
- Aim for 80%+ coverage for critical code
- Look for uncovered code in error handling paths
- Focus on meaningful tests, not just coverage numbers
- Use coverage to find missing tests, not as a primary goal
- Exclude generated code or boilerplate from metrics
```

---

## Continuous Integration

## CI for Python Testing
- Automated testing on every commit
- Multiple environments and Python versions
- Linting and type checking
- Coverage reports
- GitHub Actions, Travis CI, Jenkins, etc.

```yaml
# GitHub Actions example (.github/workflows/test.yml)
name: Python Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.7, 3.8, 3.9]

    steps:
    - uses: actions/checkout@v2
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v2
      with:
        python-version: ${{ matrix.python-version }}
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install tox tox-gh-actions
    - name: Test with tox
      run: tox
```

---

## Practical Example

## Complete Testing Example
```python
# src/mypackage/calculator.py
class Calculator:
    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b

# tests/test_calculator.py
import pytest
from mypackage.calculator import Calculator

class TestCalculator:
    @pytest.fixture
    def calculator(self):
        return Calculator()

    def test_add(self, calculator):
        assert calculator.add(2, 3) == 5
        assert calculator.add(-1, 1) == 0
        assert calculator.add(0, 0) == 0

    def test_subtract(self, calculator):
        assert calculator.subtract(5, 3) == 2
        assert calculator.subtract(1, 5) == -4

    def test_multiply(self, calculator):
        assert calculator.multiply(2, 3) == 6
        assert calculator.multiply(0, 5) == 0

    def test_divide(self, calculator):
        assert calculator.divide(6, 3) == 2
        assert calculator.divide(5, 2) == 2.5

    def test_divide_by_zero(self, calculator):
        with pytest.raises(ValueError) as exc_info:
            calculator.divide(5, 0)
        assert str(exc_info.value) == "Cannot divide by zero"
```

---

## Practical Example

## Complete Debugging and Linting
```bash
# Example dev workflow commands

# Run static type checking
mypy src/

# Run linting tools
black src/
isort src/
flake8 src/

# Run tests
pytest

# Debug a specific test
pytest tests/test_failing.py -v --pdb

# Run with coverage
pytest --cov=src/ --cov-report=html

# Complete CI check
tox
```

---

## Summary

## Key Takeaways
- Debugging: Use appropriate tools for different situations
- Assertions: Validate internal assumptions and invariants
- Type hints: Catch errors before runtime
- Linting: Maintain code quality and style consistency
- Testing: Verify functionality at multiple levels
- Coverage: Measure test thoroughness
- Integration: Automate quality checks in your workflow

---

## Resources

## Further Learning
- Python Debugging: https://docs.python.org/3/library/pdb.html
- mypy Type Checking: https://mypy.readthedocs.io/
- pytest Documentation: https://docs.pytest.org/
- unittest Documentation: https://docs.python.org/3/library/unittest.html
- coverage.py: https://coverage.readthedocs.io/
- Black: https://black.readthedocs.io/
- Python Testing with pytest (Book by Brian Okken)
