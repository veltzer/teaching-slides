# Technology Around Python
---
## Overview
- Debugging Python code
- Profiling performance
- Code formatting and linting
- Virtual environments in depth
- PyPI ecosystem
- Useful developer tools
---
## The Python Debugger (`pdb`)
- Built-in interactive debugger
- Set breakpoints, inspect variables, step through code

```python
import pdb

def buggy_function(items):
    total = 0
    for item in items:
        pdb.set_trace()  # Breakpoint
        total += item
    return total
```
---
## `pdb` Commands
| Command | Description |
|---------|-------------|
| `n` (next) | Execute next line |
| `s` (step) | Step into function |
| `c` (continue) | Continue to next breakpoint |
| `p expr` | Print expression |
| `pp expr` | Pretty-print expression |
| `l` (list) | Show source code |
| `w` (where) | Show stack trace |
| `q` (quit) | Quit debugger |
| `b N` | Set breakpoint at line N |
| `h` (help) | Show help |
---
## `breakpoint()` (Python 3.7+)

```python
def calculate(x, y):
    result = x + y
    breakpoint()  # Modern way to set breakpoint
    return result * 2
```

- Equivalent to `import pdb; pdb.set_trace()`
- Can be configured via `PYTHONBREAKPOINT` env variable

```bash
# Disable all breakpoints
PYTHONBREAKPOINT=0 python3 script.py

# Use a different debugger
PYTHONBREAKPOINT=ipdb.set_trace python3 script.py
```
---
## Running `pdb` from Command Line

```bash
# Start script in debugger
python3 -m pdb script.py

# Run until exception
python3 -m pdb -c continue script.py
```

- Starts at the first line
- Use `c` to run until an exception or breakpoint
---
## `pdb` - Post-mortem Debugging

```python
import pdb

try:
    result = 1 / 0
except ZeroDivisionError:
    pdb.post_mortem()
```

- Inspects the state at the point of the exception
- Very useful for debugging crashes
---
## `pdb` - Practical Session

```python
def find_max(numbers):
    breakpoint()
    if not numbers:
        return None
    current_max = numbers[0]
    for num in numbers[1:]:
        if num > current_max:
            current_max = num
    return current_max
```

```console
(Pdb) p numbers
[3, 1, 4, 1, 5]
(Pdb) n
(Pdb) p current_max
3
(Pdb) c
```
---
## `ipdb` - Enhanced Debugger

```bash
pip install ipdb
```

```python
import ipdb
ipdb.set_trace()
```

- Syntax highlighting
- Tab completion
- Better stack traces
- All `pdb` commands work
---
## VS Code Debugging
- Set breakpoints by clicking line numbers
- Run with F5 or Debug panel
- Features:
    - Variable inspection
    - Watch expressions
    - Call stack view
    - Conditional breakpoints
    - Logpoints

```json
{
    "type": "python",
    "request": "launch",
    "program": "${file}"
}
```
---
## Profiling - Why?
- Find performance bottlenecks
- Understand where time is spent
- Optimize the right parts of code
- "Premature optimization is the root of all evil" - Donald Knuth
---
## `time` Module for Basic Timing

```python
import time

start = time.time()
result = sum(range(10_000_000))
elapsed = time.time() - start
print(f"Elapsed: {elapsed:.4f}s")

# More precise
start = time.perf_counter()
result = sum(range(10_000_000))
elapsed = time.perf_counter() - start
print(f"Elapsed: {elapsed:.6f}s")
```
---
## `timeit` Module

```python
import timeit

# Time a simple expression
t = timeit.timeit("sum(range(1000))", number=10000)
print(f"Total: {t:.4f}s")

# Compare approaches
t1 = timeit.timeit("'-'.join(str(n) for n in range(100))", number=10000)
t2 = timeit.timeit("'-'.join(map(str, range(100)))", number=10000)
print(f"Generator: {t1:.4f}s")
print(f"Map:       {t2:.4f}s")
```
---
## `timeit` from Command Line

```bash
python3 -m timeit "sum(range(1000))"
# 10000 loops, best of 5: 15.2 usec per loop

python3 -m timeit -s "data = list(range(1000))" "sorted(data)"
# 10000 loops, best of 5: 12.5 usec per loop
```
---
## `cProfile` - The Built-in Profiler

```python
import cProfile

def slow_function():
    total = 0
    for i in range(1000000):
        total += i ** 2
    return total

cProfile.run("slow_function()")
```

```output
         4 function calls in 0.215 seconds
   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.215    0.215    0.215    0.215 script.py:3(slow_function)
        1    0.000    0.000    0.215    0.215 <string>:1(<module>)
```
---
## `cProfile` from Command Line

```bash
# Profile a script
python3 -m cProfile script.py

# Sort by cumulative time
python3 -m cProfile -s cumtime script.py

# Save to file for analysis
python3 -m cProfile -o output.prof script.py
```
---
## Analyzing Profile Data

```python
import pstats

stats = pstats.Stats("output.prof")
stats.sort_stats("cumulative")
stats.print_stats(20)  # Top 20 functions

# Filter by module
stats.print_stats("my_module")

# Print callers
stats.print_callers("slow_function")
```
---
## `line_profiler` - Line-by-Line Profiling

```bash
pip install line_profiler
```

```python
@profile
def slow_function():
    result = []
    for i in range(10000):
        result.append(i ** 2)
    return sum(result)
```

```bash
kernprof -l -v script.py
```

- Shows time spent on each line
- Very useful for optimizing hot loops
---
## `memory_profiler`

```bash
pip install memory_profiler
```

```python
from memory_profiler import profile

@profile
def memory_hungry():
    a = [i for i in range(1000000)]
    b = [i ** 2 for i in range(1000000)]
    del a
    return b
```

```bash
python3 -m memory_profiler script.py
```
---
## Code Formatting - `black`

```bash
pip install black

# Format a file
black my_script.py

# Format a directory
black src/

# Check without modifying
black --check src/

# Show diff
black --diff my_script.py
```

- Opinionated formatter: one way to format code
- Default line length: 88 characters
---
## `black` Configuration in `pyproject.toml`

```toml
[tool.black]
line-length = 88
target-version = ["py312"]
include = '\.pyi?$'
```
---
## Code Formatting - `isort`
- Sorts and organizes imports

```bash
pip install isort

# Sort imports
isort my_script.py

# Sort entire project
isort .

# Check without modifying
isort --check-only .
```

```python
# Before isort
import os
from collections import defaultdict
import sys
import json

# After isort
import json
import os
import sys
from collections import defaultdict
```
---
## Linting - `flake8`

```bash
pip install flake8

# Lint a file
flake8 my_script.py

# Lint with configuration
flake8 --max-line-length 88 src/
```

- Checks PEP 8 compliance
- Detects common errors
- Configurable rules
---
## Linting - `ruff`
- Modern, fast Python linter (written in Rust)
- Replaces `flake8`, `isort`, `pyupgrade`, and more

```bash
pip install ruff

# Lint
ruff check .

# Fix auto-fixable issues
ruff check --fix .

# Format (replaces black)
ruff format .
```
---
## `ruff` Configuration

```toml
[tool.ruff]
line-length = 88
target-version = "py312"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "UP"]

[tool.ruff.lint.isort]
known-first-party = ["my_package"]
```
---
## Type Checking - `mypy`

```bash
pip install mypy

# Check types
mypy my_script.py
mypy src/

# Strict mode
mypy --strict src/
```

```python
def greet(name: str) -> str:
    return f"Hello, {name}"

greet(42)  # mypy error: Argument 1 has incompatible type "int"
```
---
## `mypy` Configuration

```toml
[tool.mypy]
python_version = "3.12"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
```
---
## Pre-commit Hooks

```bash
pip install pre-commit
```

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 24.1.0
    hooks:
      - id: black
  - repo: https://github.com/charliermarsh/ruff-pre-commit
    rev: v0.2.0
    hooks:
      - id: ruff
```

```bash
pre-commit install
pre-commit run --all-files
```
---
## `virtualenv` vs `venv`
| Feature | `venv` | `virtualenv` |
|---------|--------|-------------|
| Built-in | Yes (3.3+) | No (pip install) |
| Speed | Slower | Faster |
| Python versions | Current only | Any version |
| Features | Basic | More options |

```bash
# virtualenv
pip install virtualenv
virtualenv myenv
virtualenv -p python3.11 myenv
```
---
## `pyenv` - Python Version Manager

```bash
# Install pyenv
curl https://pyenv.run | bash

# List available versions
pyenv install --list

# Install a version
pyenv install 3.12.0

# Set global version
pyenv global 3.12.0

# Set local version (per directory)
pyenv local 3.11.0
```
---
## `pipx` - Install CLI Tools

```bash
# Install pipx
pip install pipx

# Install tools in isolated environments
pipx install black
pipx install ruff
pipx install mypy
pipx install cookiecutter

# Run without installing
pipx run cowsay "Hello!"
```

- Each tool gets its own virtual environment
- Available globally without polluting your project
---
## `poetry` - Dependency Management

```bash
# Install poetry
pip install poetry

# Create new project
poetry new my-project

# Add dependency
poetry add requests

# Add dev dependency
poetry add --group dev pytest

# Install all dependencies
poetry install

# Run in virtual environment
poetry run python3 script.py

```
```console
---
## `uv` - Modern Python Package Manager

# Install uv
pip install uv

# Create virtual environment (very fast)
uv venv

# Install packages (very fast)
uv pip install requests

# Sync from requirements
uv pip sync requirements.txt
```

- Written in Rust, extremely fast
- Drop-in replacement for pip and venv
---
## `Makefile` for Python Projects

```makefile
.PHONY: test lint format install

install:
    pip install -e ".[dev]"

test:
    pytest

lint:
    ruff check .
    mypy src/

format:
    ruff format .
    ruff check --fix .

clean:
    rm -rf __pycache__ .pytest_cache dist build
```
---
## Continuous Integration Example

```yaml
# .github/workflows/ci.yml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -e ".[dev]"
      - run: ruff check .
      - run: mypy src/
      - run: pytest --cov
```
---
## Docker for Python Projects

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ src/
COPY pyproject.toml .

RUN pip install --no-cache-dir .

CMD ["python3", "-m", "my_package"]
```
---
## Python Performance Tips
1. Use built-in functions (`sum`, `max`, `min`, `sorted`)
1. Use list comprehensions over loops
1. Use `set` for membership testing
1. Avoid global variables in hot paths
1. Use `__slots__` for many instances
1. Consider `numpy` for numerical work
1. Profile before optimizing
---
## Useful Standard Library Tools

```bash
# Start a simple HTTP server
python3 -m http.server 8000

# Pretty-print JSON
python3 -m json.tool data.json

# Create a zip file
python3 -m zipfile -c archive.zip dir/

# Show Python configuration
python3 -m sysconfig

# Run doctests
python3 -m doctest module.py
```
---
## `logging` Best Practices

```python
import logging

# Configure once at application entry point
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Get module-level logger
logger = logging.getLogger(__name__)

def process():
    logger.info("Processing started")
    logger.debug("Debug details: %s", data)
    logger.error("Something failed", exc_info=True)
```
---
## Environment Management Summary
| Tool | Purpose |
|------|---------|
| `venv` | Built-in virtual environments |
| `virtualenv` | Enhanced virtual environments |
| `pyenv` | Python version management |
| `pip` | Package installation |
| `pipx` | Install CLI tools globally |
| `poetry` | Dependency management + packaging |
| `uv` | Fast pip/venv replacement |
---
## Developer Workflow Summary
1. Use `pyenv` to manage Python versions
1. Create virtual environment with `venv` or `uv`
1. Install dependencies with `pip` or `poetry`
1. Write code with type hints
1. Format with `black` or `ruff format`
1. Lint with `ruff check`
1. Type-check with `mypy`
1. Test with `pytest`
1. Use pre-commit hooks
1. CI/CD for automated checks
---
## Summary
- `pdb` and `breakpoint()` for debugging
- `cProfile` and `timeit` for profiling
- `black`/`ruff` for formatting, `flake8`/`ruff` for linting
- `mypy` for static type checking
- `venv`, `virtualenv`, `pyenv`, `poetry`, `uv` for environment management
- `pipx` for installing CLI tools
- Use CI/CD to automate quality checks
- Profile before optimizing
