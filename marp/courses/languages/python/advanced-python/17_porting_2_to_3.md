---
tags:
  - languages:python
level: advanced
category: language
audience:
  - audiences:developers

---
# **Porting from Python 2 to Python 3**

## A Comprehensive Guide

---

## **Why Port to Python 3?**

* **Python 2 End of Life (EOL):** January 1, 2020. No more official support, bug fixes, or security updates.
* **Vibrant Python 3 Ecosystem:** Most new libraries and frameworks are Python 3 only.
* **Modern Language Features:** Python 3 offers significant improvements and new capabilities.
* **Performance Enhancements:** Python 3 often brings better performance.

---

## What is Python 3?

* The current and future generation of Python
* Not strictly backward-compatible with Python 2
* Introduced to fix fundamental design flaws of Python 2
* Focus on cleaner syntax, better Unicode handling, and more consistent APIs

---

## **Key Benefits of Python 3**

* **Improved Unicode Support:** Strings are Unicode by default.
* **Clearer Syntax:** e.g., `print()` function, new exception handling.
* **Iterator-based Standard Library:** More memory efficient.
* **New Features:** `asyncio`, f-strings, type hints, walrus operator (`:=`), etc.
* **Active Development:** Continuous improvements and new features.

---

## **Agenda: Our Porting Journey**

1. Understanding Key Differences
1. Planning Your Port
1. Essential Porting Tools
1. The Step-by-Step Porting Process
1. Common Pitfalls & Challenges
1. Best Practices for a Smooth Transition
1. Embracing Python 3 Features
1. Q&A

---

## **Part 1: Understanding Key Differences**

---

## **Difference 1: `print` Statement vs. Function**

* **Python 2:** `print "Hello"` (statement)
```python
# Python 2
print "Value:", x
print >> sys.stderr, "Error!"
```
* **Python 3:** `print("Hello")` (function)
        ```python
        # Python 3
        print("Value:", x)
        print("Error!", file=sys.stderr)
        ```
        Offers more flexibility (e.g., `sep`, `end`, `file` arguments).

---

## **Difference 2: Integer Division**

* **Python 2:** `/` operator performs floor division for integers.
    ```python
    # Python 2
    print 3 / 2  # Output: 1
    print 3 // 2 # Output: 1
    print 3 / 2.0 # Output: 1.5
    ```
* **Python 3:** `/` operator performs true division. `//` is for floor division.
    ```python
    # Python 3
    print(3 / 2)  # Output: 1.5
    print(3 // 2) # Output: 1
    ```
* To get Python 3 division behavior in Python 2: `from __future__ import division`

---

## **Difference 3: Unicode and Strings/Bytes**

* **Python 2:**
    * `str`: Byte strings (ASCII by default).
    * `unicode`: Unicode strings.
    * Implicit coercion between `str` and `unicode` can lead to errors.
    ```python
    # Python 2
    s = "hello"  # bytes
    u = u"你好" # unicode
    ```
* **Python 3:**
    * `str`: Unicode strings (UTF-8 by default).
    * `bytes`: Byte strings.
    * No implicit coercion. Explicit `encode()` and `decode()`.
    ```python
    # Python 3
    s = "hello"  # unicode (str)
    b = b"hello" # bytes
    u = "你好"   # unicode (str)
    byte_data = u.encode('utf-8')
    str_data = byte_data.decode('utf-8')
    ```

---

## **Difference 4: Exception Handling**

* **Python 2:**
    ```python
    # Python 2
    try:
        # ...
    except IOError, e: # Comma syntax
        print "Error:", e
    ```
* **Python 3:**
    ```python
    # Python 3
    try:
        # ...
    except IOError as e: # 'as' keyword
        print("Error:", e)
    ```
    * The `as` keyword is mandatory in Python 3.
    * Exception objects are not directly accessible via `sys.exc_info()` in the `except` block as easily.

---

## **Difference 5: `xrange` vs. `range`**

* **Python 2:**
    * `range()`: Returns a list.
    * `xrange()`: Returns an iterator (more memory efficient for large ranges).
    ```python
    # Python 2
    my_list = range(10)    # Creates a list [0, ..., 9]
    my_iterator = xrange(10) # Creates an xrange object
    ```
* **Python 3:**
    * `range()`: Behaves like Python 2's `xrange()`, returning an immutable sequence type.
    * `xrange()` is gone.
    ```python
    # Python 3
    my_range_obj = range(10) # Creates a range object
    # To get a list: list(range(10))
    ```

---

## **Difference 6: Dictionary Methods `.keys()`, `.values()`, `.items()`**

* **Python 2:** These methods return lists.
    * `.iterkeys()`, `.itervalues()`, `.iteritems()` return iterators.
    ```python
    # Python 2
    d = {'a': 1, 'b': 2}
    keys_list = d.keys()
    items_iterator = d.iteritems()
    ```
* **Python 3:** These methods return dictionary "views" (iterator-like).
    * They are dynamic and reflect changes in the dictionary.
    * To get a list: `list(d.keys())`.
    ```python
    # Python 3
    d = {'a': 1, 'b': 2}
    keys_view = d.keys() # Returns a view object
    # for k in d.keys(): ...
    ```

---

## **Difference 7: `map()`, `filter()`, `zip()`**

* **Python 2:** These functions return lists.
    ```python
    # Python 2
    squared_numbers = map(lambda x: x*x, [1, 2, 3]) # list
    ```
* **Python 3:** These functions return iterators.
    ```python
    # Python 3
    squared_numbers_iter = map(lambda x: x*x, [1, 2, 3]) # iterator
    # list(map(...)) to get a list
    ```
    * This change is for memory efficiency.
    * `itertools` module has `imap`, `ifilter`, `izip` in Python 2 for iterator behavior.

---

## **Difference 8: Standard Library Reorganization**

* Many modules have been renamed or reorganized for clarity.
* Examples:
    * `urllib`, `urllib2`, `urlparse` -> `urllib` package (`urllib.request`, `urllib.parse`, `urllib.error`).
    * `httplib` -> `http.client`.
    * `ConfigParser` -> `configparser`.
    * `StringIO` -> `io.StringIO` and `io.BytesIO`.
    * `cPickle` -> `pickle`.
* `2to3` tool helps automate these changes.

---

## **Difference 9: `long` Integer Type**

* **Python 2:** Has two integer types: `int` (fixed-precision, usually 32 or 64-bit) and `long` (arbitrary precision).
    * `123` is an `int`, `123L` is a `long`.
    * Automatic promotion from `int` to `long` on overflow.
* **Python 3:** Has a single `int` type which behaves like Python 2's `long` (arbitrary precision).
    * The `L` suffix is a syntax error.
    * `sys.maxint` is gone (use `sys.maxsize` for practical limits of system containers).

---

## **Difference 10: `input()` vs. `raw_input()`**

* **Python 2:**
    * `raw_input()`: Reads a line from stdin and returns it as a string.
    * `input()`: Reads a line from stdin, then `eval()`s it (SECURITY RISK!).
    ```python
    # Python 2
    name = raw_input("Enter name: ") # Safe
    # data = input("Enter data: ") # Unsafe!
    ```
* **Python 3:**
    * `input()`: Behaves like Python 2's `raw_input()`.
    * `raw_input()` is gone.
    * If you need `eval()` behavior, use `eval(input())`.
    ```python
    # Python 3
    name = input("Enter name: ") # Safe, returns string
    ```

---

## **Difference 11: Relative Imports**

* **Python 2:** Allows implicit relative imports (e.g., `import mymodule` could find `mymodule.py` in the same directory). This can be ambiguous.
* **Python 3:** Requires explicit relative imports for modules within the same package.
    ```python
    # Python 3 - inside a package
    from . import sibling_module
    from .. import parent_module_sibling
    ```
* Python 2 can enable this behavior with `from __future__ import absolute_import`.

---

## **Difference 12: Metaclass Syntax**

* **Python 2:**
    ```python
    # Python 2
    class MyClass(object):
        __metaclass__ = MyMeta
        # ...
    ```
* **Python 3:**
    ```python
    # Python 3
    class MyClass(metaclass=MyMeta):
        # ...
    ```
* The `six` library provides a compatible way: `six.with_metaclass(MyMeta, MyBaseClass)`.

---

## **Other Notable Python 2 vs 3 Differences**

* **`next()` method:** Use `next(iterator)` function instead of `iterator.next()`.
* **`raise` statement:** `raise Exception, "message"` becomes `raise Exception("message")`.
* **Octal literals:** `0777` (Py2) becomes `0o777` (Py3).
* **Comparison:** Unorderable types (e.g., `None < 1`, `1 < "a"`) raise `TypeError` in Py3; Py2 had arbitrary but consistent ordering.
* **`StandardError`:** Removed. Use `Exception`.
* **Many C API changes.**

---

## **Part 2: Planning Your Port**

---

## **Step 1: Assess Your Codebase**

* **Size and Complexity:** How much code needs porting?
* **Dependencies:**
    * Are your third-party libraries Python 3 compatible?
    * Check PyPI (Python Package Index) using tools like `caniusepython3`.
* **Test Coverage:** Good tests are CRUCIAL.
    * Aim for high coverage before starting.
    * Tests will verify the port's correctness.
* **Python 2 Specific Idioms:** Identify code heavily reliant on Py2 features.
* **Team Familiarity:** Is your team comfortable with Python 3?

---

## **Step 2: Choose a Porting Strategy**

1. **Big Bang (All at Once):**
    * Port the entire codebase to Python 3.
    * Switch over when everything is ready.
    * Pros: Cleaner, single codebase eventually.
    * Cons: Risky, long development freeze, hard for large projects.
1. **Incremental (Coexistence):**
    * Modify code to run on *both* Python 2 and Python 3 simultaneously.
    * Use compatibility libraries like `six`.
    * Pros: Lower risk, continuous deployment, gradual rollout.
    * Cons: Code can be less idiomatic, longer transition period.
    * **Often the recommended approach for larger projects.**

---

## **Step 3: Set Up a Python 3 Environment**

* Install the latest stable Python 3 version.
* Use virtual environments (`venv`, `conda`).
    ```bash
    python3 -m venv py3env
    source py3env/bin/activate
    # or with conda
    conda create -n py3env python=3.x
    conda activate py3env
    ```
* Install necessary tools and dependencies in this environment.

---

## **Step 4: Version Control is Your Friend!**

* **Commit Often:** Before, during, and after making changes.
* **Use Branches:** Create a dedicated branch for the porting effort (e.g., `py3-porting`).
    ```bash
    git checkout -b py3-porting
    ```
* Makes it easy to:
    * Track changes.
    * Revert if something goes wrong.
    * Collaborate with others.

---

## **Step 5: Communication & Team**

* **Involve Stakeholders:** Explain the "why" and the plan.
* **Team Training:** If needed, get the team up to speed on Python 3 differences.
* **Allocate Time:** Porting takes time and effort; don't underestimate it.
* **Designate a Lead/Champion:** Someone to drive the porting effort.

---

## **Part 3: Tools for Porting**

---

## **Tool 1: `2to3`**

* A Python script that reads Python 2 source code and applies a series of "fixers" to transform it into valid Python 3 code.
* Comes bundled with Python.
* **Basic Usage:**
    ```bash
    2to3 my_python2_script.py  # Shows diffs
    2to3 -w my_python2_script.py # Writes changes back to file
    2to3 -w -n --no-diffs my_project_dir/ # Process a directory, no backup
    ```
* Can run specific fixers or exclude some.

---

## **`2to3` - Common Fixers**

* `print`: Converts `print` statement to `print()` function.
* `division`: Changes `/` to `//` for integer division if `from __future__ import division` is not present.
* `imports`: Handles renamed standard library modules (e.g., `urllib2` to `urllib.request`).
* `xrange`: Converts `xrange()` to `range()`.
* `raw_input`: Converts `raw_input()` to `input()`.
* `dict`: Converts `.iteritems()` to `.items()`, etc.
* `except`: Changes `except E, N:` to `except E as N:`.
* And many more!

---

## **Limitations of `2to3`**

* **Not a Silver Bullet:** It automates many mechanical changes but can't handle everything.
* **Unicode/Bytes:** Struggles with complex string/byte issues. These often require manual intervention.
* **Logic Changes:** Cannot understand the *intent* of your code; it only applies syntactic transformations.
* **Idiomatic Python 3:** It produces working Python 3 code, but not necessarily *idiomatic* or *optimal* Python 3 code.
* **May Miss Edge Cases:** Always review changes carefully.

---

## **Tool 2: `six` Library**

* Provides utility functions for writing code that is compatible with both Python 2 and Python 3.
* Excellent for the incremental porting strategy.
* Install: `pip install six`
* **Key Features:**
    * `six.PY2`, `six.PY3` booleans.
    * `six.string_types`, `six.text_type`, `six.binary_type`.
    * `six.moves` for renamed standard library modules (e.g., `from six.moves import configparser`).
    * `six.print_()`.
    * `six.reraise()`.
    * `@six.add_metaclass(MyMeta)`.

---

## **Using `six` - Example**

```python
import six

# String types
if isinstance(value, six.string_types): # True for str/unicode in Py2, str in Py3
    print("It's a string-like type")

# Iteritems
my_dict = {'a': 1}
for k, v in six.iteritems(my_dict):
    print(k, v)

# Renamed module
from six.moves.urllib.parse import urlparse
urlparse("[http://example.com](http://example.com)")

# Print function
six.print_("Hello", "world", sep="-", end="!\n")
```

---

## **Tool 3: `python-future` & `python-modernize`**

* **`python-future`:**
    * Aims to provide a clean Python 3.x-compatible layer on Python 2.7 and 3.3+.
    * Includes `future` (backports Py3 features to Py2) and `past` (Py2 features on Py3) modules.
    * Tool: `futurize`.
* **`python-modernize`:**
    * A tool that uses `2to3` and `six` to update Python 2 code to a common subset of Python 2 and 3 that uses `six` for compatibility.
    * Often preferred over raw `2to3` if aiming for a Py2/Py3 compatible codebase.
    ```bash
    pip install future modernize
    python-modernize -w my_project_dir/
    ```

---

## **Tool 4: Linters (Pylint, Flake8)**

* Configure your linters to check for Python 3 compatibility and common porting issues.
* **Pylint:**
    * Can be run with `--py3k` flag in Python 2 to identify some Python 3 incompatibilities.
    * Run it with your Python 3 interpreter after porting.
* **Flake8:** (Combines PyFlakes, pycodestyle, McCabe)
    * Excellent for catching syntax errors and style issues.
* Integrate linters into your CI/CD pipeline.

---

## **Part 4: The Porting Process - Step-by-Step**

---

### **Phase 1: Preparation**

1. **Ensure Excellent Test Coverage:**
    * **This is the most critical step.**
    * Write unit tests, integration tests, and end-to-end tests.
    * Your tests are your safety net. They will tell you if the porting broke something.
    * Aim for >80-90% coverage if possible.

---

### **Phase 1: Preparation (Cont.)**

1. **Identify Python 2 Specific Idioms:**
    * Manually review code or use tools to find patterns that will break in Python 3.
    * Examples: `print` statements, old-style exception handling, `xrange`, dictionary methods returning lists, `apply()`.
1. **Update Dependencies:**
    * Check if your dependencies have Python 3 compatible versions.
    * Use `caniusepython3` or check individual project documentation.
    * Update them in your Python 2 environment *before* porting if possible, or plan for updates.

---

### **Phase 2: Automated Conversion**

1. **Choose your tool:**
    * `2to3`: For a direct Py2 -> Py3 port.
    * `python-modernize`: For a Py2/Py3 compatible codebase using `six`.
1. **Run the tool on your codebase:**
    * Start with a single file or small module to see how it works.
    * `2to3 -w my_module.py`
    * `python-modernize -w my_module.py`
1. **Review Automated Changes Carefully:**
    * Use `git diff` to see exactly what the tool changed.
    * Understand *why* each change was made.
    * Don't blindly trust the automation.

---

### **Phase 3: Manual Fixes & Refactoring**

1. **Address `2to3` / `python-modernize` Warnings/Failures:**
    * The tools might flag areas they couldn't fix automatically.
1. **Tackle Unicode/Bytes Issues:**
    * This is often the most complex part.
    * Distinguish text (Unicode, `str` in Py3) from binary data (`bytes` in Py3).
    * Ensure proper `encode()` (str -> bytes) and `decode()` (bytes -> str) at I/O boundaries.
    * Open files in text mode (`'r'`, `'w'`) or binary mode (`'rb'`, `'wb'`) explicitly.
    ```python
    # Python 3
    with open('data.txt', 'r', encoding='utf-8') as f: # Text mode
        content = f.read()
    with open('image.png', 'rb') as f: # Binary mode
        binary_content = f.read()
    ```

---

### **Phase 3: Manual Fixes (Cont.)**

1. **Update Dependencies (if not done earlier):**
    * Install Python 3 versions of your libraries in your Python 3 environment.
    * Some libraries might have different APIs in their Python 3 versions.
1. **Handle C Extensions (if any):**
    * C extensions need to be recompiled for Python 3.
    * The C API has changed significantly between Python 2 and 3. This can be a major task.
    * Consider alternatives like CFFI or Cython if rebuilding is too complex.
1. **Refactor for Python 3 Idioms:**
    * Once the code works, look for opportunities to use new Python 3 features (f-strings, `yield from`, etc.) for cleaner, more readable code. This can be a later step.

---

### **Phase 4: Testing! Testing! Testing!**
1. **Run ALL Tests in Python 3:**
    * Execute your entire test suite using your Python 3 interpreter.
    * `python3 -m unittest discover` or `pytest`
1. **Fix Test Failures:**
    * Systematically go through each failing test.
    * Debug the code to understand why it's failing in Python 3.
    * This is where your good test coverage pays off.
1. **Perform Manual/Exploratory Testing:**
    * Use the application as a user would.
    * Check critical paths and edge cases that automated tests might miss.

---

### **Iterative Process**

* For larger projects, the porting process (Automated -> Manual -> Test) is often iterative.
* You might port one module or component at a time.
* Run tests frequently.

---

### **Iterative Process**

![iterative_process](svg/courses/languages/python/advanced-python/17_porting_2_to_3/iterative_process.svg)

---

## **Example: `dict.iteritems()` to `dict.items()`**

**Python 2:**
```python
d = {'a': 1, 'b': 2}
for k, v in d.iteritems(): # Returns an iterator
    print k, v
# If you needed a list of items: list(d.iteritems()) - less common
# d.items() returns a list of tuples
```

**`2to3` / `python-modernize` might change it to:**

```python
# Using six (from python-modernize)
import six
d = {'a': 1, 'b': 2}
for k, v in six.iteritems(d):
    print(k, v)

# Direct 2to3 might change d.items() to list(d.items())
# and d.iteritems() to d.items()
```
**Python 3 (idiomatic):**

```python
d = {'a': 1, 'b': 2}
for k, v in d.items(): # Returns a view (iterator-like)
    print(k, v)
```

---

## **Example: Unicode Handling**

**Python 2 (potential issue):**

```python
# data might be bytes or unicode
def process_data(data):
    if "user:" in data: # Potential TypeError if data is unicode and "user:" is bytes
        # or UnicodeDecodeError if data is bytes with non-ASCII
        print data.upper()

# filename = "file_with_utf8.txt"
# with open(filename, 'r') as f: # 'r' in Py2 might give bytes
#    content = f.read()
# process_data(content)
```

**Python 3 (and good practice):**

```python
def process_data(text_data: str): # Expect unicode string
    if "user:" in text_data:
        print(text_data.upper())

# filename = "file_with_utf8.txt"
# with open(filename, 'r', encoding='utf-8') as f: # Explicit encoding
#    content = f.read() # content is str (unicode)
# process_data(content)
```
* Be clear about text vs. binary data.
* Decode bytes to text at input boundaries, encode text to bytes at output boundaries.

---

## **Part 5: Common Pitfalls & Challenges**

---

## **Pitfall 1: Underestimating the Effort**

* Porting can be more time-consuming than expected, especially for large, old, or complex codebases.
* "It's just a syntax change" is a dangerous assumption.
* **Solution:** Plan thoroughly, allocate sufficient resources, and start with a small pilot project if unsure.

---

## **Pitfall 2: Unicode Errors (`UnicodeDecodeError`, `UnicodeEncodeError`)**

* The most common and often trickiest issues.
* Caused by mixing bytes and text (Unicode) improperly.
* **Solution:**
    * Understand the Python 3 string model (`str` is Unicode, `bytes` is for binary).
    * Explicitly `encode()` text to bytes and `decode()` bytes to text.
    * Specify encodings when opening files or handling I/O.
    * Use `io.open` in Python 2 with explicit encoding for easier transition.

---

## **Pitfall 3: Dependency Hell**

* Some Python 2 libraries may not have Python 3 equivalents, or their Python 3 versions have breaking API changes.
* **Solution:**
    * Research dependencies *before* starting the port (`caniusepython3`).
    * Look for alternative libraries if necessary.
    * Be prepared to update or refactor code that uses these dependencies.
    * Sometimes, you might need to fork and port a dependency yourself (last resort).

---

## **Pitfall 4: Performance Regressions**

* While Python 3 is often faster, some specific operations or code patterns might be slower.
    * e.g., String operations if not handled carefully, or if old code relied on Py2's byte-string speed for certain tasks.
* **Solution:**
    * Profile your application in Python 3 if performance is critical.
    * Optimize bottlenecks. Python 3 often offers better tools for optimization.

---

## **Pitfall 5: Subtle Bugs Post-Porting**

* Changes in behavior (e.g., division, dictionary ordering pre-3.7, comparison of unorderable types) can lead to subtle bugs not caught by basic tests.
* **Solution:**
    * Thorough testing (unit, integration, E2E).
    * Code reviews by developers familiar with Python 3.
    * Gradual rollout with monitoring if possible.

---

## **Part 6: Best Practices for a Smooth Transition**

---

## **Best Practice 1: Write New Code with Python 3 in Mind**

* Even if you're still on Python 2, start writing new code that is easily portable or already Python 2/3 compatible.
* Use `from __future__ import ...` statements:
    ```python
    # In Python 2 code
    from __future__ import absolute_import
    from __future__ import division
    from __future__ import print_function
    from __future__ import unicode_literals # Be careful, can have wide impact
    ```
* Avoid Python 2-only idioms.

---

## **Best Practice 2: Use Compatibility Libraries Wisely**

* Libraries like `six`, `future`, or `past` are invaluable for making code run on both Python 2 and 3.
* This is key for incremental porting.
* However, aim to eventually remove them once fully on Python 3 to simplify code and leverage pure Python 3 features.

---

## **Best Practice 3: Test, Test, and Test Again!**

* Cannot be emphasized enough.
* Automated tests are your best friend in verifying the port.
* Cover:
    * Core logic (unit tests).
    * Interactions between components (integration tests).
    * User workflows (acceptance/E2E tests).
    * Especially test areas with string/byte manipulation and I/O.

---

## **Best Practice 4: Incremental Porting if Possible**

* For large applications, port module by module or feature by feature.
* Allows for continuous integration and deployment.
* Reduces risk compared to a "big bang" approach.
* Requires a codebase that can run in a hybrid Py2/Py3 environment (using `six` or similar).

---

## **Part 7: Beyond the Port: Embracing Python 3**

---

## **Leverage New Python 3 Features**

Once your code is running stably on Python 3, start refactoring to use modern Python 3 features:

* **f-strings (Formatted String Literals):** Cleaner, faster string formatting.
    ```python
    name = "World"
    print(f"Hello, {name}!") # Python 3.6+
    ```
* **Type Hinting (PEP 484):** Improved code clarity and tooling (e.g., MyPy).
    ```python
    def greet(name: str) -> str:
        return "Hello, " + name
    ```
* **`asyncio` and `async/await`:** For high-performance asynchronous programming.
* **Pathlib module:** Object-oriented filesystem paths.
    ```python
    from pathlib import Path
    p = Path("/usr/local/bin")
    for child in p.iterdir(): print(child)
    ```
* **Walrus Operator (`:=`) (PEP 572):** Assignment expressions (Python 3.8+).
* Dictionary comprehensions, set comprehensions, extended iterable unpacking, etc.

---

## **Stay Updated**

* Python 3 continues to evolve with new features and performance improvements in each minor release (3.7, 3.8, 3.9, 3.10, 3.11, 3.12...).
* Keep an eye on Python release notes.
* Consider a regular schedule for upgrading your Python 3 version.

---

## **Recap: Key Takeaways**

1. **Why Port?** EOL, features, ecosystem.
1. **Key Differences:** `print()`, division, Unicode/bytes, `range()`, dict views, etc.
1. **Plan:** Assess, strategize (incremental often best), set up env, use VCS.
1. **Tools:** `2to3`, `six`, `python-modernize`, linters.
1. **Process:** Prepare (TESTS!), auto-convert, manual fixes (Unicode!), TEST.
1. **Pitfalls:** Underestimation, Unicode, dependencies.
1. **Best Practices:** Future imports, `six`, TEST, incremental.
1. **Embrace Python 3:** Use new features post-port.

**Porting is an investment that pays off in maintainability, performance, and access to modern Python.**
