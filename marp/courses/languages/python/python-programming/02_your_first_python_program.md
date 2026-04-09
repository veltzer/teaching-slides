# Your First Python Program

---
## Installing Python on Linux
- Most Linux distributions come with Python pre-installed
- Check your version:

```bash
python3 --version
```

- Install on Ubuntu/Debian:

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

---
## Installing Python on macOS
- macOS may come with an older Python
- Recommended: use Homebrew

```bash
brew install python3
```

- Or download from python.org
- Verify installation:

```bash
python3 --version
```

---
## Installing Python on Windows
- Download from https://python.org
- Check "Add Python to PATH" during installation
- Verify in Command Prompt:

```bash
python --version
```

- On Windows, use `python` instead of `python3`

---
## The Python Interactive Shell
- Start by typing `python3` in terminal
- The `>>>` prompt means Python is ready

```console
$ python3
Python 3.12.0 (main, Oct  2 2023)
>>> 2 + 3
5
>>> "hello".upper()
'HELLO'
>>> exit()
```

---
## Using the Interactive Shell
- Immediate feedback for expressions
- Great for testing small code snippets
- Use `help()` for built-in documentation
- Use `dir()` to list available attributes

```python
>>> help(str)
>>> dir(list)
>>> help(print)
```

---
## IPython - Enhanced Interactive Shell
- More powerful than the default shell
- Install with `pip install ipython`
- Features:
    - Tab completion
    - Syntax highlighting
    - Magic commands (`%timeit`, `%run`)
    - Better tracebacks

```bash
pip install ipython
ipython
```

---
## Your First Script
- Create a file called `hello.py`

```python
print("Hello, World!")
```

- Run it from the terminal:

```bash
python3 hello.py
```

- Output:

```output
Hello, World!
```

---
## The Shebang Line
- On Unix systems, you can make scripts executable

```python
#!/usr/bin/env python3
print("Hello, World!")
```

```bash
chmod +x hello.py
./hello.py
```

- `#!/usr/bin/env python3` tells the OS which interpreter to use

---
## Comments in Python
- Single-line comments start with `#`
- No multi-line comment syntax (use multiple `#`)

```python
# This is a comment
x = 42  # This is an inline comment

# This is a
# multi-line comment
# using multiple hash marks
```

---
## Docstrings
- Triple-quoted strings used for documentation
- First statement in a module, function, class, or method

```python
def greet(name):
    """Return a greeting for the given name.

    Args:
        name: The name to greet.

    Returns:
        A greeting string.
    """
    return f"Hello, {name}"
```

---
## The `print()` Function
- Outputs text to the console
- Can print multiple values separated by space

```python
print("Hello")
print("Name:", "Alice")
print("Age:", 30)
print(1, 2, 3, sep=", ")
print("No newline", end="")
print(" here")
```

---
## Print Output

```output
Hello
Name: Alice
Age: 30
1, 2, 3
No newline here
```

---
## The `input()` Function
- Reads text input from the user
- Always returns a string

```python
name = input("What is your name? ")
print(f"Hello, {name}!")

age = input("How old are you? ")
age = int(age)  # Convert to integer
print(f"Next year you will be {age + 1}")
```

---
## A Complete Interactive Program

```python
#!/usr/bin/env python3
name = input("Enter your name: ")
birth_year = int(input("Enter your birth year: "))
current_year = 2026
age = current_year - birth_year
print(f"Hello {name}, you are {age} years old!")
```

---
## Running Python with `-c` Flag
- Execute a one-liner from the command line

```bash
python3 -c "print('Hello from command line')"
python3 -c "import sys; print(sys.version)"
python3 -c "print(2 ** 10)"
```

- Useful for quick calculations and checks

---
## Running Python with `-m` Flag
- Run a module as a script

```bash
python3 -m http.server 8000
python3 -m json.tool data.json
python3 -m venv myenv
python3 -m pip install requests
```

---
## IDEs for Python - VS Code
- Free, open source, by Microsoft
- Excellent Python extension
- Features:
    - IntelliSense (autocompletion)
    - Debugging
    - Integrated terminal
    - Git integration
    - Extensions marketplace

---
## IDEs for Python - PyCharm
- By JetBrains
- Community Edition is free
- Professional Edition is paid
- Features:
    - Advanced code analysis
    - Built-in debugger
    - Database tools (Pro)
    - Django support (Pro)
    - Scientific tools (Pro)

---
## IDEs for Python - Other Options
- **Vim/Neovim**: With Python plugins
- **Emacs**: With `elpy` or `lsp-mode`
- **Sublime Text**: Lightweight, fast
- **Spyder**: Scientific Python IDE
- **Jupyter Notebook**: Interactive computing
- **IDLE**: Built-in with Python (basic)

---
## Jupyter Notebooks
- Interactive documents mixing code and text
- Popular in data science and education
- Install and run:

```bash
pip install jupyter
jupyter notebook
```

- Cells can contain Python code or Markdown
- Code cells show output inline

---
## Python File Encoding
- Python 3 source files are UTF-8 by default
- You can specify encoding explicitly:

```python
# -*- coding: utf-8 -*-
```

- This was more important in Python 2
- In Python 3, UTF-8 is the default

---
## Python Style Guide (PEP 8)
- Use 4 spaces for indentation (never tabs)
- Maximum line length: 79 characters
- Two blank lines before top-level definitions
- One blank line before method definitions
- Use `snake_case` for functions and variables
- Use `PascalCase` for classes
- Use `UPPER_CASE` for constants

---
## PEP 8 - Naming Conventions

```python
# Variables and functions: snake_case
my_variable = 42
def my_function():
    pass

# Classes: PascalCase
class MyClass:
    pass

# Constants: UPPER_CASE
MAX_SIZE = 100
PI = 3.14159
```

---
## Linting with `flake8`
- Checks code against PEP 8

```bash
pip install flake8
flake8 my_script.py
```

- Common checks:
    - Line length
    - Whitespace issues
    - Import order
    - Unused variables

---
## Formatting with `black`
- Automatic code formatter
- Opinionated: one way to format

```bash
pip install black
black my_script.py
```

- Enforces consistent style across a project
- Widely adopted in the Python community

---
## Type Checking with `mypy`
- Static type checker for Python
- Uses type hints to find bugs

```bash
pip install mypy
mypy my_script.py
```

```python
def add(a: int, b: int) -> int:
    return a + b

add("hello", "world")  # mypy catches this
```

---
## Summary
- Python can be installed on all major platforms
- Use `python3` to start the interactive shell
- Write scripts in `.py` files
- Multiple IDE options available (VS Code, PyCharm)
- Follow PEP 8 style guidelines
- Use tools like `flake8`, `black`, and `mypy`
