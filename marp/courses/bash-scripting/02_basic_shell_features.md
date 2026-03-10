# Basic Shell Features
---
## Running Multiple Commands

```bash
# Semicolons: run commands sequentially
echo "first"; echo "second"; echo "third"

# Each command runs regardless of whether
# the previous one succeeded or failed
false; echo "this still runs"

# Newlines work the same as semicolons
echo "first"
echo "second"
```
---
## Semicolons vs Newlines vs `&&`

```bash
# Semicolon: always run next command
false; echo "runs"    # prints "runs"

# &&: run next command only if previous succeeded
false && echo "nope"  # prints nothing

# ||: run next command only if previous failed
false || echo "yes"   # prints "yes"
```
---
## Command Grouping

```bash
# Group with curly braces (runs in CURRENT shell)
{ echo "a"; echo "b"; } > output.txt
# Note: space after { and semicolon before } are required

# Group with parentheses (runs in a SUBSHELL)
(echo "a"; echo "b") > output.txt

# The difference matters for variable changes
x=1
{ x=2; }
echo "$x"   # prints 2 (same shell)

x=1
(x=2)
echo "$x"   # prints 1 (subshell change lost)
```
---
## Variables: The Basics

```bash
# Assign a variable (NO SPACES around =)
name="Bash Scripting"

# WRONG - this tries to run "name" as a command
name = "Bash Scripting"
# bash: name: command not found

# Access a variable with $
echo "$name"

# Curly braces for clarity
echo "${name}_course"
```
---
## Why No Spaces Around `=`?

```bash
# The shell parses this as:
#   command: "name"
#   arg1: "="
#   arg2: "value"
name = value

# But this is parsed as:
#   assignment: name=value
name=value

# This is a fundamental bash design decision
# and one of the most common beginner mistakes
```
---
## Variable Substitution

```bash
name="world"

# Simple substitution
echo "Hello $name"         # Hello world

# With curly braces (recommended)
echo "Hello ${name}"       # Hello world

# Why braces matter:
echo "$namefoo"            # empty! (no var named "namefoo")
echo "${name}foo"          # worldfoo
```
---
## Default Values

```bash
# Use default if variable is unset or empty
echo "${name:-default_value}"

# Use default if variable is unset (but not if empty)
echo "${name-default_value}"

# Assign default if unset or empty
echo "${name:=default_value}"

# Example:
unset color
echo "${color:-blue}"    # prints "blue", color still unset
echo "${color:=blue}"    # prints "blue", color is now "blue"
echo "$color"            # prints "blue"
```
---
## Error on Unset Variables

```bash
# Produce error if variable is unset or empty
echo "${name:?Variable name is required}"
# bash: name: Variable name is required

# Produce error only if unset
echo "${name?Variable name is required}"

# This is great for scripts that need certain variables
: "${DATABASE_URL:?DATABASE_URL must be set}"
```
---
## String Operations on Variables

```bash
path="/home/user/documents/file.txt"

# Length
echo "${#path}"               # 33

# Substring (offset, length)
echo "${path:6:4}"            # user

# Remove shortest prefix match
echo "${path#*/}"             # home/user/documents/file.txt

# Remove longest prefix match
echo "${path##*/}"            # file.txt

# Remove shortest suffix match
echo "${path%/*}"             # /home/user/documents

# Remove longest suffix match
echo "${path%%/*}"            # (empty, first char is /)
```
---
## String Replacement

```bash
text="hello world hello bash"

# Replace first occurrence
echo "${text/hello/goodbye}"
# goodbye world hello bash

# Replace ALL occurrences
echo "${text//hello/goodbye}"
# goodbye world goodbye bash

# Replace at beginning
echo "${text/#hello/goodbye}"
# goodbye world hello bash

# Replace at end
echo "${text/%bash/shell}"
# hello world hello shell
```
---
## Case Conversion (`bash` 4.0+)

```bash
name="Hello World"

# Lowercase first character
echo "${name,}"     # hello World

# Lowercase all
echo "${name,,}"    # hello world

# Uppercase first character
echo "${name^}"     # Hello World

# Uppercase all
echo "${name^^}"    # HELLO WORLD
```
---
## Quoting: The Three Types

```bash
# 1. No quotes: word splitting + globbing happen
files=*.txt
echo $files        # expands to matching files

# 2. Double quotes: variable expansion, no splitting/globbing
echo "$files"      # prints literally: *.txt

# 3. Single quotes: NO expansion at all
echo '$files'      # prints literally: $files
echo '$((1+1))'   # prints literally: $((1+1))
```
---
## When to Use Double Quotes

```bash
# ALWAYS double-quote variable references
# Unless you specifically want word splitting

name="John Doe"

# WRONG: word splitting turns this into two arguments
touch $name        # creates "John" and "Doe"

# RIGHT: preserves the space
touch "$name"      # creates "John Doe"

# WRONG: glob expansion can surprise you
pattern="*"
echo $pattern      # prints all files in directory!

# RIGHT:
echo "$pattern"    # prints: *
```
---
## The Golden Rule of Quoting
> **Always double-quote your variables unless you have
> a specific reason not to.**

```bash
# Good habits:
echo "$variable"
cp "$source" "$destination"
if [ "$answer" = "yes" ]; then

# Only skip quotes when you WANT splitting:
for word in $sentence; do
    echo "$word"
done
```
---
## Escaping Special Characters

```bash
# Backslash escapes the next character
echo "The price is \$5.00"    # The price is $5.00
echo "She said \"hello\""     # She said "hello"
echo "Line one\nLine two"     # Line one\nLine two (no newline!)

# Use $'...' for escape sequences
echo $'Line one\nLine two'    # Actually prints two lines
echo $'Tab\there'              # Tab   here

# Backslash at end of line = line continuation
echo "this is a very \
long line"
# prints: this is a very long line
```
---
## Special Characters Summary
| Character | Meaning | Escape with |
|-----------|---------|-------------|
| `$` | Variable expansion | `\$` or single quotes |
| `` ` `` | Command substitution | `` \` `` or `$(...)` |
| `"` | Double quote | `\"` |
| `\` | Escape character | `\\` |
| `!` | History expansion | `\!` or single quotes |
| `#` | Comment | `\#` or quotes |
| `*`, `?` | Globbing | quotes |
| `~` | Home directory | quotes |
---
## Command Substitution

```bash
# Modern syntax (preferred):
today=$(date +%Y-%m-%d)
echo "Today is $today"

# Legacy syntax (avoid - hard to nest):
today=`date +%Y-%m-%d`

# Nesting is easy with $():
echo "Kernel: $(uname -r) on $(hostname)"

# Nesting with backticks is painful:
echo "Files: `ls \`pwd\``"   # Don't do this
echo "Files: $(ls $(pwd))"   # Much clearer
```
---
## Arithmetic Expansion

```bash
# Use $(( )) for integer arithmetic
echo $((2 + 3))        # 5
echo $((10 / 3))       # 3 (integer division!)
echo $((10 % 3))       # 1 (modulo)
echo $((2 ** 10))      # 1024 (exponentiation)

# Variables inside don't need $
x=5
echo $((x + 3))        # 8
echo $((x * x))        # 25

# WARNING: no floating point
echo $((10 / 3))       # 3, not 3.333...
```
