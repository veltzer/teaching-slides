---
tags:
  - languages:bash
  - practices:scripting
  - infrastructure:linux
  - practices:automation
level: intermediate
category: language
audience:
  - audiences:developers
  - audiences:sysadmins
  - audiences:devops
---
# Variable Types

---
## Variable Types Overview

![variable_types_overview](svg/courses/languages/bash/bash-scripting/18_variable_types/variable_types_overview.svg)

---
## Everything is a String (by Default)

```bash
# In bash, all variables are strings by default
x=42
echo "$x"       # "42" (a string that looks like a number)

# Arithmetic context treats strings as numbers
echo $((x + 1))    # 43

# String operations on numbers
echo "${#x}"        # 2 (length of "42")
echo "${x:0:1}"     # 4 (first character)

# Unset variables in arithmetic are 0
unset y
echo $((y + 5))    # 5
```

---
## Integer Variables

```bash
# declare -i forces integer behavior
declare -i num
num=5+3
echo "$num"    # 8 (not "5+3"!)

num="hello"
echo "$num"    # 0 (non-numeric strings become 0)

num=10/3
echo "$num"    # 3 (integer division)

# Integer variables in assignment
declare -i a=5 b=3 c
c=a+b
echo "$c"      # 8
```

---
## String Operations: Comprehensive

```bash
str="Hello, World!"

# Length
echo "${#str}"                    # 13

# Substring
echo "${str:0:5}"                 # Hello
echo "${str:7}"                   # World!
echo "${str: -6}"                 # orld! (note the space)

# Search and replace
echo "${str/World/Bash}"          # Hello, Bash!
echo "${str//l/L}"                # HeLLo, WorLd!

# Case conversion
echo "${str^^}"                   # HELLO, WORLD!
echo "${str,,}"                   # hello, world!

# Prefix/suffix removal
filename="archive.tar.gz"
echo "${filename%.gz}"            # archive.tar
echo "${filename%%.*}"            # archive
echo "${filename#*.}"             # tar.gz
echo "${filename##*.}"            # gz
```

---
## Indexed Arrays

```bash
# Create an array
fruits=("apple" "banana" "cherry")

# Access elements (0-indexed)
echo "${fruits[0]}"     # apple
echo "${fruits[1]}"     # banana
echo "${fruits[2]}"     # cherry

# All elements
echo "${fruits[@]}"     # apple banana cherry

# Number of elements
echo "${#fruits[@]}"    # 3

# Length of a specific element
echo "${#fruits[0]}"    # 5 (length of "apple")
```

---
## Associative Arrays (`bash` 4.0+)

```bash
# Must declare with -A
declare -A user

# Set key-value pairs
user[name]="Alice"
user[age]=30
user[email]="alice@example.com"

# Access values
echo "${user[name]}"     # Alice
echo "${user[age]}"      # 30

# All keys
echo "${!user[@]}"       # name age email

# All values
echo "${user[@]}"        # Alice 30 alice@example.com

# Number of pairs
echo "${#user[@]}"       # 3
```

---
## When to Use Which Type
| Type | Use Case |
|------|----------|
| Plain string | Single values, paths, messages |
| Integer (`-i`) | Counters, arithmetic variables |
| Indexed array | Ordered lists, command args |
| Associative array | Key-value mappings, configs |

---
## Nameref Variables (`bash` 4.3+)

```bash
# declare -n creates a reference to another variable
x=42
declare -n ref=x

echo "$ref"    # 42
ref=99
echo "$x"      # 99 (changed through ref)

# Useful in functions:
increment() {
    local -n var=$1
    var=$((var + 1))
}
count=0
increment count
increment count
echo "$count"    # 2
```

---
## Variable Attributes Summary

```bash
# declare sets variable attributes
declare -i x        # integer
declare -r x        # readonly
declare -x x        # exported (environment)
declare -l x        # lowercase
declare -u x        # uppercase
declare -a x        # indexed array
declare -A x        # associative array
declare -n x        # nameref

# View attributes
declare -p x

# Remove attributes
declare +i x        # remove integer attribute
declare +x x        # remove export (unexport)
```
