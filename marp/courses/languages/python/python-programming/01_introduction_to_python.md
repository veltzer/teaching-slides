# Introduction to Python

![h:500](/jpg/courses/languages/python/python-programming/guido_van_rossum.jpg)

---
## What is Python?
- Python is a high-level, general-purpose programming language
- Created by Guido van Rossum
- First released in 1991
- Named after Monty Python's Flying Circus
- Emphasizes code readability and simplicity
---
## A Brief History of Python
- 1989: Guido van Rossum starts working on Python
- 1991: Python 0.9.0 released
- 2000: Python 2.0 released
    - List comprehensions
    - Garbage collection
- 2008: Python 3.0 released
    - Major backwards-incompatible release
- 2020: Python 2 end of life
---
## Python 2 vs Python 3
| Feature | Python 2 | Python 3 |
|---------|----------|----------|
| Print | `print "hello"` | `print("hello")` |
| Division | `5/2 = 2` | `5/2 = 2.5` |
| Strings | ASCII by default | Unicode by default |
| `range()` | Returns list | Returns iterator |
| Support | Ended 2020 | Active |
---
## Why Python?
- Easy to learn and read
- Huge standard library ("batteries included")
- Massive ecosystem of third-party packages
- Cross-platform (Windows, macOS, Linux)
- Free and open source
- Large and active community
---
## Python Use Cases
- Web development (Django, Flask, FastAPI)
- Data science and machine learning (NumPy, Pandas, scikit-learn)
- Automation and scripting
- DevOps and system administration
- Scientific computing
- Desktop applications
- Game development
---
## Who Uses Python?
- Google (YouTube, search infrastructure)
- Netflix (recommendation engine)
- Instagram (backend)
- Spotify (data analysis)
- NASA (scientific computing)
- Dropbox (desktop client)
- Reddit (web platform)
---
## Python vs C/C++
| Aspect | Python | C/C++ |
|--------|--------|-------|
| Typing | Dynamic | Static |
| Speed | Slower (interpreted) | Faster (compiled) |
| Memory | Automatic GC | Manual management |
| Syntax | Simple | Complex |
| Use case | Rapid development | Systems programming |
---
## Python vs Java
| Aspect | Python | Java |
|--------|--------|------|
| Typing | Dynamic | Static |
| Syntax | Concise | Verbose |
| Indentation | Meaningful | Cosmetic |
| Compilation | Interpreted | Compiled to bytecode |
| OOP | Optional | Required |
---
## Python vs JavaScript
| Aspect | Python | JavaScript |
|--------|--------|------------|
| Primary use | General purpose | Web (now general) |
| Typing | Dynamic | Dynamic |
| Concurrency | GIL limits threads | Event loop |
| Indentation | Meaningful | Cosmetic |
| Package manager | pip | npm |
---
## Python vs Bash
| Aspect | Python | Bash |
|--------|--------|------|
| Readability | High | Low for complex scripts |
| Portability | Cross-platform | Unix-focused |
| Data structures | Rich | Limited |
| Error handling | Exceptions | Exit codes |
| Best for | Complex scripts | Simple automation |
---
## The Zen of Python

```python
import this
```

- Beautiful is better than ugly
- Explicit is better than implicit
- Simple is better than complex
- Readability counts
- There should be one obvious way to do it
---
## Python is Interpreted
- Python code is compiled to bytecode (`.pyc` files)
- Bytecode is executed by the Python Virtual Machine (PVM)
- No separate compilation step needed
- Trade-off: slower execution, faster development

![python_is_interpreted](/svg/courses/languages/python/python-programming/01_introduction_to_python/python_is_interpreted.svg)

---
## Dynamic Typing
- Variables do not have a fixed type
- Types are checked at runtime, not compile time

```python
x = 42        # x is an int
x = "hello"   # now x is a str
x = [1, 2, 3] # now x is a list
```
---
## Dynamic Typing - Implications
- More flexible code
- Faster prototyping
- Potential runtime errors that static typing would catch
- Type hints available since Python 3.5

```python
def greet(name: str) -> str:
    return f"Hello, {name}"
```
---
## Python is Strongly Typed
- Python is dynamically typed but strongly typed
- You cannot mix types implicitly

```python
"hello" + 42  # TypeError!
"hello" + str(42)  # "hello42" - explicit conversion
```
---
## Indentation Matters
- Python uses indentation to define code blocks
- No curly braces `{}` like C/Java
- Standard is 4 spaces per level

```python
if True:
    print("This is indented")
    if True:
        print("This is more indented")
```
---
## Everything is an Object
- In Python, everything is an object
- Integers, strings, functions, classes, modules
- Every object has a type, an identity, and a value

```python
x = 42
print(type(x))    # <class 'int'>
print(id(x))      # memory address
print(x.__add__)   # even int has methods
```
---
## Python Implementations
- **CPython**: The reference implementation (written in C)
- **PyPy**: JIT-compiled, faster for long-running programs
- **Jython**: Runs on the JVM
- **IronPython**: Runs on .NET
- **MicroPython**: For microcontrollers
- **GraalPy**: On GraalVM
---
## The Python Community
- Python Enhancement Proposals (PEPs)
- PEP 8: Style guide for Python code
- PEP 20: The Zen of Python
- PyPI: Python Package Index (over 500,000 packages)
- Annual PyCon conferences worldwide
---
## Python Versioning
- Current stable: Python 3.12+
- New minor version every year (October)
- Each version supported for ~5 years
- Always use the latest stable release for new projects
- Check version:

```python
import sys
print(sys.version)
```
---
## The GIL (Global Interpreter Lock)
- CPython has a Global Interpreter Lock
- Only one thread executes Python bytecode at a time
- Affects CPU-bound multithreading
- I/O-bound threads are not affected
- Workarounds: `multiprocessing`, C extensions
- Python 3.13+ has experimental free-threaded mode
---
## Python's Philosophy
- "There should be one-- and preferably only one --obvious way to do it"
- Favor readability over cleverness
- Explicit is better than implicit
- Practicality beats purity
- Errors should never pass silently
---
## REPL - Read Eval Print Loop
- Python has an interactive interpreter
- Great for experimentation and learning

```console
$ python3
>>> 2 + 2
4
>>> print("Hello")
Hello
>>> exit()
```
---
## Python in the Real World
- Most popular language on GitHub (2024)
- #1 on TIOBE index
- Fastest growing language for data science
- Default language for AI/ML development
- Used in education as first programming language
---
## Summary
- Python is a high-level, interpreted, dynamically typed language
- Created in 1991 by Guido van Rossum
- Python 3 is the current and only supported version
- Used across web, data science, DevOps, and more
- Large ecosystem and active community
- Emphasizes readability and simplicity
