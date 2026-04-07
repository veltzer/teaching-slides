# Basic Statements
---
## Variable Assignment
- Variables are created by assignment
- No declaration needed
- Variable names: letters, digits, underscores (cannot start with digit)

```python
x = 42
name = "Alice"
is_valid = True
_private = "hidden"
```
---
## Multiple Assignment

```python
# Assign same value to multiple variables
a = b = c = 0
print(a, b, c)  # 0 0 0

# Assign multiple values at once
x, y, z = 1, 2, 3
print(x, y, z)  # 1 2 3

# Swap variables (no temp needed)
a, b = 1, 2
a, b = b, a
print(a, b)  # 2 1
```
---
## Augmented Assignment

```python
x = 10
x += 5    # x = x + 5
x -= 3    # x = x - 3
x *= 2    # x = x * 2
x /= 4   # x = x / 4
x //= 2  # x = x // 2
x %= 3   # x = x % 3
x **= 2  # x = x ** 2
```
---
## The Walrus Operator `:=` (Python 3.8+)
- Assignment expression: assigns and returns a value

```python
# Without walrus
line = input("Enter: ")
while line != "quit":
    print(f"You said: {line}")
    line = input("Enter: ")

# With walrus
while (line := input("Enter: ")) != "quit":
    print(f"You said: {line}")
```
---
## The `print()` Function - Detailed

```python
# Default behavior
print("Hello", "World")     # Hello World

# Custom separator
print("a", "b", "c", sep="-")  # a-b-c

# Custom end character
print("Hello", end=" ")
print("World")  # Hello World

# Print to file
with open("output.txt", "w") as f:
    print("Hello", file=f)
```
---
## Formatted Printing

```python
name = "Alice"
age = 30
score = 95.678

# f-string (recommended)
print(f"{name} is {age} and scored {score:.1f}")

# Format table columns
for item, price in [("Apple", 1.5), ("Banana", 0.75)]:
    print(f"{item:<10} ${price:>6.2f}")
```

```output
Alice is 30 and scored 95.7
Apple      $  1.50
Banana     $  0.75
```
---
## The `if` Statement

```python
age = 18

if age >= 18:
    print("You are an adult")
```

- The condition must evaluate to a boolean
- The indented block executes if condition is `True`
- No parentheses needed around the condition
---
## `if`/`else`

```python
age = 15

if age >= 18:
    print("You are an adult")
else:
    print("You are a minor")
```
---
## `if`/`elif`/`else`

```python
score = 85

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
elif score >= 60:
    grade = "D"
else:
    grade = "F"

print(f"Grade: {grade}")  # Grade: B
```
---
## Conditional Expression (Ternary)

```python
age = 20
status = "adult" if age >= 18 else "minor"
print(status)  # 'adult'

# Can be nested (but avoid deep nesting)
x = 15
label = "high" if x > 10 else "low" if x > 5 else "very low"
print(label)  # 'high'
```
---
## Truthy and Falsy in Conditions

```python
# These are all falsy
if not 0:
    print("0 is falsy")
if not "":
    print("empty string is falsy")
if not []:
    print("empty list is falsy")
if not None:
    print("None is falsy")

# Common pattern: check if list is non-empty
items = [1, 2, 3]
if items:
    print("List has items")
```
---
## The `while` Loop

```python
count = 0
while count < 5:
    print(count)
    count += 1
```

```output
0
1
2
3
4
```
---
## `while` with User Input

```python
while True:
    answer = input("Enter 'quit' to exit: ")
    if answer == "quit":
        break
    print(f"You entered: {answer}")
```
---
## The `for` Loop

```python
# Iterate over a list
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(fruit)

# Iterate over a string
for char in "Python":
    print(char, end=" ")
# P y t h o n
```
---
## The `range()` Function

```python
# range(stop)
for i in range(5):
    print(i, end=" ")  # 0 1 2 3 4

print()

# range(start, stop)
for i in range(2, 6):
    print(i, end=" ")  # 2 3 4 5

print()

# range(start, stop, step)
for i in range(0, 10, 2):
    print(i, end=" ")  # 0 2 4 6 8
```
---
## `range()` - Counting Down

```python
for i in range(5, 0, -1):
    print(i, end=" ")
# 5 4 3 2 1

# Reverse a range
for i in reversed(range(5)):
    print(i, end=" ")
# 4 3 2 1 0
```
---
## `range()` is Lazy
- `range()` does not create a list in memory
- It generates numbers on demand

```python
# This does NOT create a billion-element list
r = range(1_000_000_000)
print(999_999 in r)     # True (fast!)
print(len(r))            # 1000000000
print(r[500])            # 500
```
---
## Iterating Over Dictionaries

```python
person = {"name": "Alice", "age": 30, "city": "NYC"}

# Iterate over keys (default)
for key in person:
    print(key)

# Iterate over values
for value in person.values():
    print(value)

# Iterate over key-value pairs
for key, value in person.items():
    print(f"{key}: {value}")
```
---
## Nested Loops

```python
# Multiplication table
for i in range(1, 4):
    for j in range(1, 4):
        print(f"{i}x{j}={i*j}", end="\t")
    print()
```

```output
1x1=1   1x2=2   1x3=3
2x1=2   2x2=4   2x3=6
3x1=3   3x2=6   3x3=9
```
---
## The `break` Statement
- Exits the innermost loop immediately

```python
for i in range(10):
    if i == 5:
        break
    print(i, end=" ")
# 0 1 2 3 4

# Search example
numbers = [4, 7, 2, 9, 1, 5]
for n in numbers:
    if n == 9:
        print("Found 9!")
        break
```
---
## The `continue` Statement
- Skips the rest of the current iteration

```python
for i in range(10):
    if i % 2 == 0:
        continue
    print(i, end=" ")
# 1 3 5 7 9
```
---
## `break` vs `continue` Diagram

![break_vs_continue_diagram](/svg/courses/languages/python/python-programming/05_basic_statements/break_vs_continue_diagram.svg)

---
## The `else` Clause on Loops
- Executes when the loop completes without `break`

```python
# Search with else
numbers = [1, 3, 5, 7, 9]
for n in numbers:
    if n == 4:
        print("Found 4")
        break
else:
    print("4 not found")
# Output: 4 not found
```
---
## The `pass` Statement
- Does nothing (placeholder)

```python
# Empty function
def not_implemented_yet():
    pass

# Empty class
class MyClass:
    pass

# Empty loop body
for i in range(10):
    pass  # TODO: implement

# Empty if branch
if True:
    pass
```
---
## The `match` Statement (Python 3.10+)

```python
command = "quit"

match command:
    case "start":
        print("Starting...")
    case "stop":
        print("Stopping...")
    case "quit":
        print("Quitting...")
    case _:
        print(f"Unknown command: {command}")
```
---
## `match` with Patterns

```python
point = (0, 5)

match point:
    case (0, 0):
        print("Origin")
    case (0, y):
        print(f"On Y-axis at y={y}")
    case (x, 0):
        print(f"On X-axis at x={x}")
    case (x, y):
        print(f"Point at ({x}, {y})")
```
---
## `match` with Guards

```python
age = 25

match age:
    case n if n < 0:
        print("Invalid age")
    case n if n < 13:
        print("Child")
    case n if n < 18:
        print("Teenager")
    case n if n < 65:
        print("Adult")
    case _:
        print("Senior")
```
---
## Common Loop Patterns - Accumulator

```python
# Sum of numbers
numbers = [1, 2, 3, 4, 5]
total = 0
for n in numbers:
    total += n
print(total)  # 15

# Or use built-in
print(sum(numbers))  # 15
```
---
## Common Loop Patterns - Filtering

```python
numbers = [1, -2, 3, -4, 5, -6]

# Collect positive numbers
positives = []
for n in numbers:
    if n > 0:
        positives.append(n)
print(positives)  # [1, 3, 5]
```
---
## Common Loop Patterns - Transformation

```python
words = ["hello", "world", "python"]

# Transform each element
upper_words = []
for word in words:
    upper_words.append(word.upper())
print(upper_words)
# ['HELLO', 'WORLD', 'PYTHON']
```
---
## Common Loop Patterns - Finding Max/Min

```python
numbers = [3, 7, 1, 9, 4, 6]

# Manual approach
maximum = numbers[0]
for n in numbers[1:]:
    if n > maximum:
        maximum = n
print(maximum)  # 9

# Built-in approach
print(max(numbers))  # 9
print(min(numbers))  # 1
```
---
## Looping Techniques - `enumerate()`

```python
colors = ["red", "green", "blue"]

# Instead of this
for i in range(len(colors)):
    print(f"{i}: {colors[i]}")

# Do this
for i, color in enumerate(colors):
    print(f"{i}: {color}")
```
---
## Looping Techniques - `zip()`

```python
names = ["Alice", "Bob", "Charlie"]
scores = [90, 85, 92]

# Instead of indexing
for i in range(len(names)):
    print(f"{names[i]}: {scores[i]}")

# Do this
for name, score in zip(names, scores):
    print(f"{name}: {score}")
```
---
## Looping Techniques - `reversed()`

```python
colors = ["red", "green", "blue"]

for color in reversed(colors):
    print(color)
```

```output
blue
green
red
```
---
## Looping Techniques - `sorted()`

```python
numbers = [3, 1, 4, 1, 5, 9]

for n in sorted(numbers):
    print(n, end=" ")
# 1 1 3 4 5 9

print()

for n in sorted(numbers, reverse=True):
    print(n, end=" ")
# 9 5 4 3 1 1
```
---
## The `del` Statement
- Deletes variables, list items, dict keys

```python
# Delete variable
x = 42
del x
# print(x)  # NameError

# Delete list element
lst = [1, 2, 3, 4]
del lst[1]
print(lst)  # [1, 3, 4]

# Delete dict key
d = {"a": 1, "b": 2}
del d["a"]
print(d)  # {'b': 2}
```
---
## Assertions

```python
age = 25
assert age > 0, "Age must be positive"

# If condition is False, AssertionError is raised
# age = -1
# assert age > 0, "Age must be positive"
# AssertionError: Age must be positive
```

- Assertions are for debugging, not input validation
- Can be disabled with `python -O` flag
---
## Summary
- Assignment creates variables; no declaration needed
- `if`/`elif`/`else` for conditional branching
- `while` for condition-based loops
- `for` iterates over sequences and iterables
- `range()` generates number sequences lazily
- `break` exits loops; `continue` skips iterations
- `pass` is a no-op placeholder
- `match`/`case` for structural pattern matching (3.10+)
