# Basic Types and Operators
---
## Python's Built-in Types
- **Numeric**: `int`, `float`, `complex`
- **Text**: `str`
- **Boolean**: `bool`
- **None**: `NoneType`
- The `type()` function reveals an object's type

```python
print(type(42))       # <class 'int'>
print(type(3.14))     # <class 'float'>
print(type("hello"))  # <class 'str'>
print(type(True))     # <class 'bool'>
```
---
## Integers (`int`)
- Whole numbers, positive or negative
- Unlimited precision (no overflow!)

```python
x = 42
y = -17
big = 10 ** 100  # 100-digit number, no problem
print(type(x))   # <class 'int'>
```
---
## Integer Literals
- Decimal: `42`
- Binary: `0b101010`
- Octal: `0o52`
- Hexadecimal: `0x2A`
- Underscores for readability: `1_000_000`

```python
print(0b101010)    # 42
print(0o52)        # 42
print(0x2A)        # 42
print(1_000_000)   # 1000000
```
---
## Arithmetic Operators
| Operator | Description | Example |
|----------|-------------|---------|
| `+` | Addition | `5 + 3` = `8` |
| `-` | Subtraction | `5 - 3` = `2` |
| `*` | Multiplication | `5 * 3` = `15` |
| `/` | Division (float) | `5 / 3` = `1.666...` |
| `//` | Floor division | `5 // 3` = `1` |
| `%` | Modulo | `5 % 3` = `2` |
| `**` | Power | `5 ** 3` = `125` |
---
## Division Types

```python
# True division always returns float
print(7 / 2)    # 3.5
print(6 / 2)    # 3.0

# Floor division truncates toward negative infinity
print(7 // 2)   # 3
print(-7 // 2)  # -4

# Modulo returns remainder
print(7 % 2)    # 1
print(-7 % 2)   # 1
```
---
## Integer Methods and Functions

```python
x = -42

print(abs(x))         # 42
print(pow(2, 10))     # 1024
print(divmod(17, 5))  # (3, 2)
print(bin(42))        # '0b101010'
print(hex(255))       # '0xff'
print(oct(8))         # '0o10'
```
---
## Floats (`float`)
- Floating-point numbers (IEEE 754 double precision)
- 64-bit, ~15-17 significant digits

```python
x = 3.14
y = -0.001
z = 2.0e8    # Scientific notation: 200000000.0
w = 1.5e-3   # 0.0015

print(type(x))  # <class 'float'>
```
---
## Float Precision Issues
- Floats cannot represent all decimal numbers exactly

```python
print(0.1 + 0.2)           # 0.30000000000000004
print(0.1 + 0.2 == 0.3)    # False

# Use math.isclose for comparison
import math
print(math.isclose(0.1 + 0.2, 0.3))  # True
```
---
## The `decimal` Module
- For exact decimal arithmetic

```python
from decimal import Decimal

a = Decimal("0.1")
b = Decimal("0.2")
print(a + b)          # 0.3
print(a + b == Decimal("0.3"))  # True
```

- Use when precision matters (e.g., financial calculations)
---
## Float Functions

```python
import math

print(math.floor(3.7))   # 3
print(math.ceil(3.2))    # 4
print(round(3.5))        # 4
print(round(2.675, 2))   # 2.67 (banker's rounding)
print(math.sqrt(16))     # 4.0
print(math.pi)           # 3.141592653589793
```
---
## Special Float Values

```python
import math

pos_inf = float("inf")
neg_inf = float("-inf")
nan = float("nan")

print(pos_inf > 1e308)       # True
print(math.isinf(pos_inf))   # True
print(math.isnan(nan))       # True
print(nan == nan)             # False (NaN quirk)
```
---
## Complex Numbers

```python
z = 3 + 4j
print(z.real)     # 3.0
print(z.imag)     # 4.0
print(abs(z))     # 5.0 (magnitude)
print(z.conjugate())  # (3-4j)

w = complex(1, 2)  # 1+2j
print(z + w)        # (4+6j)
print(z * w)        # (-5+10j)
```
---
## Type Conversion (Casting)

```python
# int to float
print(float(42))     # 42.0

# float to int (truncates)
print(int(3.9))      # 3
print(int(-3.9))     # -3

# string to number
print(int("42"))     # 42
print(float("3.14")) # 3.14
```
---
## Booleans (`bool`)
- Two values: `True` and `False`
- Subclass of `int` (`True` is `1`, `False` is `0`)

```python
print(type(True))    # <class 'bool'>
print(True + True)   # 2
print(True * 10)     # 10
print(isinstance(True, int))  # True
```
---
## Comparison Operators
| Operator | Description |
|----------|-------------|
| `==` | Equal to |
| `!=` | Not equal to |
| `<` | Less than |
| `>` | Greater than |
| `<=` | Less than or equal to |
| `>=` | Greater than or equal to |
| `is` | Identity (same object) |
| `is not` | Not the same object |
---
## Comparison Examples

```python
print(5 == 5)     # True
print(5 != 3)     # True
print(5 > 3)      # True
print(5 <= 5)     # True

# Chained comparisons
print(1 < 2 < 3)  # True
print(1 < 2 > 0)  # True
```
---
## Boolean Operators

```python
print(True and False)   # False
print(True or False)    # True
print(not True)         # False

# Short-circuit evaluation
print(True or 1/0)      # True (1/0 not evaluated)
print(False and 1/0)    # False (1/0 not evaluated)
```
---
## Truthiness and Falsiness
- These are falsy (evaluate to `False`):
    - `False`, `None`
    - `0`, `0.0`, `0j`
    - `""` (empty string)
    - `[]`, `()`, `{}`, `set()` (empty containers)
- Everything else is truthy

```python
print(bool(0))     # False
print(bool(""))    # False
print(bool([]))    # False
print(bool(42))    # True
print(bool("hi"))  # True
```
---
## The `None` Type
- Represents the absence of a value
- Only one `None` object exists (singleton)
- Always use `is` to compare with `None`

```python
x = None
print(type(x))      # <class 'NoneType'>
print(x is None)     # True
print(x == None)     # True (but use 'is')
```
---
## `==` vs `is`
- `==` checks value equality
- `is` checks identity (same object in memory)

```python
a = [1, 2, 3]
b = [1, 2, 3]
c = a

print(a == b)   # True (same value)
print(a is b)   # False (different objects)
print(a is c)   # True (same object)
```
---
## Strings (`str`)
- Sequence of Unicode characters
- Immutable (cannot be changed after creation)
- Created with single, double, or triple quotes

```python
s1 = 'hello'
s2 = "hello"
s3 = '''multi
line'''
s4 = """also
multi-line"""
```
---
## String Escape Characters
| Escape | Meaning |
|--------|---------|
| `\n` | Newline |
| `\t` | Tab |
| `\\` | Backslash |
| `\'` | Single quote |
| `\"` | Double quote |
| `\0` | Null character |

```python
print("Hello\nWorld")
print("Tab\there")
print("She said \"hi\"")
```
---
## Raw Strings
- Prefix with `r` to disable escape processing
- Useful for regex patterns and file paths

```python
print(r"No \n newline here")
# Output: No \n newline here

path = r"C:\Users\name\documents"
print(path)
# Output: C:\Users\name\documents
```
---
## String Indexing
- Zero-based indexing
- Negative indexing from the end

```python
s = "Python"
print(s[0])    # 'P'
print(s[1])    # 'y'
print(s[-1])   # 'n'
print(s[-2])   # 'o'
```

```diagram
 P  y  t  h  o  n
 0  1  2  3  4  5
-6 -5 -4 -3 -2 -1
```
---
## String Slicing
- `s[start:stop:step]`
- `start` is inclusive, `stop` is exclusive

```python
s = "Python"
print(s[0:3])    # 'Pyt'
print(s[2:])     # 'thon'
print(s[:4])     # 'Pyth'
print(s[::2])    # 'Pto'
print(s[::-1])   # 'nohtyP' (reversed)
```
---
## String Operations

```python
s = "hello"
print(len(s))          # 5
print(s + " world")    # 'hello world'
print(s * 3)           # 'hellohellohello'
print("ell" in s)      # True
print("xyz" not in s)  # True
```
---
## String Methods - Case

```python
s = "Hello World"
print(s.upper())       # 'HELLO WORLD'
print(s.lower())       # 'hello world'
print(s.title())       # 'Hello World'
print(s.capitalize())  # 'Hello world'
print(s.swapcase())    # 'hELLO wORLD'
```
---
## String Methods - Search

```python
s = "Hello World Hello"
print(s.find("World"))      # 6
print(s.find("xyz"))        # -1
print(s.index("World"))     # 6
print(s.count("Hello"))     # 2
print(s.startswith("Hello"))  # True
print(s.endswith("Hello"))    # True
```
---
## String Methods - Modify

```python
s = "  Hello World  "
print(s.strip())           # 'Hello World'
print(s.lstrip())          # 'Hello World  '
print(s.rstrip())          # '  Hello World'

s2 = "Hello World"
print(s2.replace("World", "Python"))  # 'Hello Python'
```
---
## String Methods - Split and Join

```python
s = "one,two,three"
parts = s.split(",")
print(parts)  # ['one', 'two', 'three']

words = ["Hello", "World"]
print(" ".join(words))   # 'Hello World'
print("-".join(words))   # 'Hello-World'
print(",".join(words))   # 'Hello,World'
```
---
## String Methods - Testing

```python
print("abc".isalpha())     # True
print("123".isdigit())     # True
print("abc123".isalnum())  # True
print("   ".isspace())     # True
print("Hello".isupper())   # False
print("HELLO".isupper())   # True
print("hello".islower())   # True
```
---
## String Formatting - f-strings (Python 3.6+)
- Recommended way to format strings

```python
name = "Alice"
age = 30
print(f"Name: {name}, Age: {age}")

# Expressions inside braces
print(f"2 + 3 = {2 + 3}")
print(f"Name in upper: {name.upper()}")

# Formatting numbers
pi = 3.14159
print(f"Pi is {pi:.2f}")  # Pi is 3.14
```
---
## f-string Format Specifiers

```python
x = 42
print(f"{x:d}")      # '42' (decimal)
print(f"{x:05d}")    # '00042' (zero-padded)
print(f"{x:b}")      # '101010' (binary)
print(f"{x:x}")      # '2a' (hex)
print(f"{x:o}")      # '52' (octal)

y = 1234567.89
print(f"{y:,.2f}")   # '1,234,567.89'
print(f"{y:.2e}")    # '1.23e+06'
```
---
## f-string Alignment

```python
s = "hi"
print(f"{s:<10}")   # 'hi        ' (left)
print(f"{s:>10}")   # '        hi' (right)
print(f"{s:^10}")   # '    hi    ' (center)
print(f"{s:*^10}")  # '****hi****' (fill)
```
---
## String Formatting - `.format()` Method

```python
print("Name: {}, Age: {}".format("Alice", 30))
print("Name: {0}, Age: {1}".format("Alice", 30))
print("Name: {name}".format(name="Alice"))
print("{:.2f}".format(3.14159))
```

- Older style but still valid
- f-strings are preferred for new code
---
## String Formatting - `%` Operator (Legacy)

```python
print("Name: %s, Age: %d" % ("Alice", 30))
print("Pi: %.2f" % 3.14159)
print("Hex: %x" % 255)
```

- Oldest formatting style
- Still found in older codebases
- Not recommended for new code
---
## Strings are Immutable

```python
s = "hello"
# s[0] = "H"  # TypeError!

# Create a new string instead
s = "H" + s[1:]
print(s)  # 'Hello'
```

- Every string operation creates a new string
- Original string is never modified
---
## Bitwise Operators
| Operator | Description | Example |
|----------|-------------|---------|
| `&` | AND | `5 & 3` = `1` |
| `\|` | OR | `5 \| 3` = `7` |
| `^` | XOR | `5 ^ 3` = `6` |
| `~` | NOT | `~5` = `-6` |
| `<<` | Left shift | `5 << 1` = `10` |
| `>>` | Right shift | `5 >> 1` = `2` |
---
## Augmented Assignment Operators

```python
x = 10
x += 5    # x = x + 5 -> 15
x -= 3    # x = x - 3 -> 12
x *= 2    # x = x * 2 -> 24
x /= 4    # x = x / 4 -> 6.0
x //= 2   # x = x // 2 -> 3.0
x **= 3   # x = x ** 3 -> 27.0
x %= 5    # x = x % 5 -> 2.0
```
---
## Operator Precedence (High to Low)
1. `**` (exponentiation)
1. `~`, `+x`, `-x` (unary)
1. `*`, `/`, `//`, `%`
1. `+`, `-`
1. `<<`, `>>`
1. `&`
1. `^`
1. `|`
1. Comparisons (`==`, `!=`, `<`, `>`, etc.)
1. `not`
1. `and`
1. `or`
---
## The `math` Module

```python
import math

print(math.pi)         # 3.141592653589793
print(math.e)          # 2.718281828459045
print(math.sqrt(16))   # 4.0
print(math.log(100))   # 4.605 (natural log)
print(math.log10(100)) # 2.0
print(math.sin(math.pi / 2))  # 1.0
print(math.factorial(5))      # 120
```
---
## Built-in Numeric Functions

```python
print(abs(-5))         # 5
print(max(1, 5, 3))    # 5
print(min(1, 5, 3))    # 1
print(sum([1, 2, 3]))  # 6
print(round(3.7))      # 4
print(round(3.145, 2)) # 3.15
print(pow(2, 10))      # 1024
```
---
## Summary
- Python has rich built-in types: `int`, `float`, `str`, `bool`, `None`
- Integers have unlimited precision
- Floats follow IEEE 754 (be aware of precision issues)
- Strings are immutable sequences of Unicode characters
- f-strings are the preferred formatting method
- Python provides comprehensive arithmetic and comparison operators
- Boolean logic uses `and`, `or`, `not`
