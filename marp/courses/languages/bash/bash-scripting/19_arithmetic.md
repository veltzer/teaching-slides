# Doing Arithmetic

---
## Arithmetic Operators Reference

![arithmetic_operators](svg/courses/languages/bash/bash-scripting/19_arithmetic/arithmetic_operators.svg)

---
## Integer Arithmetic: `$(( ))`

```bash
# Basic operations
echo $((5 + 3))      # 8
echo $((10 - 4))     # 6
echo $((3 * 7))      # 21
echo $((20 / 6))     # 3 (integer division, truncated)
echo $((20 % 6))     # 2 (modulo)
echo $((2 ** 8))     # 256 (exponentiation)

# Variables ($ is optional inside $(( )))
x=10
y=3
echo $((x + y))      # 13
echo $(($x + $y))    # 13 (also works, but $ is redundant)
```

---
## Assignment Operators

```bash
x=10

x=$((x + 5))     # x = 15 (long form)
((x += 5))        # x = 20 (shorthand)
((x -= 3))        # x = 17
((x *= 2))        # x = 34
((x /= 5))        # x = 6
((x %= 4))        # x = 2

# Increment and decrement
((x++))            # x = 3 (post-increment)
((++x))            # x = 4 (pre-increment)
((x--))            # x = 3 (post-decrement)
((--x))            # x = 2 (pre-decrement)
```

---
## The `(( ))` Command

```bash
# (( )) evaluates arithmetic expressions
# Returns 0 (true) if non-zero, 1 (false) if zero

(( 5 > 3 ))
echo $?    # 0 (true)

(( 3 > 5 ))
echo $?    # 1 (false)

# Use in conditionals
if (( x > 0 )); then
    echo "x is positive"
fi

# Ternary operator
(( y = x > 0 ? x : -x ))    # absolute value
```

---
## Comparison Operators in `(( ))`

```bash
# All C-style operators work:
(( a == b ))    # equal
(( a != b ))    # not equal
(( a > b ))     # greater than
(( a < b ))     # less than
(( a >= b ))    # greater or equal
(( a <= b ))    # less or equal

# Logical operators:
(( a > 0 && a < 100 ))     # AND
(( a == 0 || b == 0 ))     # OR
(( !(a > 0) ))              # NOT

# Bitwise operators:
echo $(( 0xFF & 0x0F ))    # 15 (AND)
echo $(( 0x0F | 0xF0 ))    # 255 (OR)
echo $(( 1 << 8 ))         # 256 (left shift)
```

---
## Bases and Number Representation

```bash
# Decimal (default)
echo $((42))         # 42

# Octal (prefix 0)
echo $((010))        # 8

# Hexadecimal (prefix 0x)
echo $((0xFF))       # 255

# Arbitrary base (base#number)
echo $((2#1010))     # 10 (binary)
echo $((8#77))       # 63 (octal)
echo $((16#FF))      # 255 (hex)
echo $((36#ZZ))      # 1295 (base 36)

# Output in other bases (use printf)
printf "%x\n" 255    # ff
printf "%o\n" 255    # 377
printf "%08b\n" 42   # not standard, use bc
```

---
## Integer Overflow

```bash
# bash uses 64-bit signed integers
echo $((2**62))               # 4611686018427387904
echo $((2**63 - 1))           # 9223372036854775807 (max)
echo $((2**63))               # -9223372036854775808 (overflow!)

# No warning, no error — just wraps around
# If you need larger numbers, use bc or python
```

---
## Floating Point: The Problem

```bash
# bash cannot do floating point arithmetic!
echo $((10 / 3))        # 3 (not 3.333...)
echo $((1.5 + 2.5))     # syntax error!

# You MUST use external tools for floating point
```

---
## Floating Point with `bc`

```bash
# bc is a calculator language
echo "10 / 3" | bc
# 3 (integer by default!)

# Set scale for decimal places
echo "scale=4; 10 / 3" | bc
# 3.3333

# More operations
echo "scale=10; sqrt(2)" | bc -l
# 1.4142135623

# Using here-string
bc -l <<< "scale=4; 22/7"
# 3.1428

# Complex calculations
bc -l << 'CALC'
scale=6
pi = 4 * a(1)
r = 5
area = pi * r * r
area
CALC
# 78.539816
```

---
## Floating Point with `awk`

```bash
# awk has built-in floating point
awk "BEGIN {print 10/3}"
# 3.33333

# With formatting
awk "BEGIN {printf \"%.4f\n\", 22/7}"
# 3.1429

# Trigonometry
awk "BEGIN {print sin(3.14159/2)}"
# 1

# Using variables
x=2.5
y=3.7
awk "BEGIN {print $x + $y}"
# 6.2
```

---
## Floating Point with `python3`

```bash
# When you need serious math, use Python
result=$(python3 -c "print(10/3)")
echo "$result"    # 3.3333333333333335

# More complex
python3 -c "
import math
print(f'pi = {math.pi:.10f}')
print(f'e  = {math.e:.10f}')
print(f'sqrt(2) = {math.sqrt(2):.10f}')
"

# Useful wrapper function
calc() {
    python3 -c "print($*)"
}
calc "2**100"
# 1267650600228229401496703205376
```

---
## Floating Point Comparison

```bash
# You cannot use (( )) for float comparison
# Use bc or awk

# Method 1: bc
a="3.14"
b="2.71"
if (( $(echo "$a > $b" | bc -l) )); then
    echo "$a is greater than $b"
fi

# Method 2: awk
if awk "BEGIN {exit !($a > $b)}"; then
    echo "$a is greater than $b"
fi

# Method 3: sort -V (version sort)
if [[ $(echo -e "$a\n$b" | sort -V | tail -1) == "$a" ]]; then
    echo "$a >= $b"
fi
```

---
## `let` Command

```bash
# let evaluates arithmetic expressions (like (( )))
let x=5+3
echo "$x"    # 8

let x++
echo "$x"    # 9

let "x = x * 2"
echo "$x"    # 18

# Multiple expressions
let "a = 5" "b = 3" "c = a + b"
echo "$c"    # 8

# Prefer (( )) over let — it's more readable
```

---
## Practical: Unit Conversion Script

```bash
#!/bin/bash

bytes_to_human() {
    local bytes=$1
    if (( bytes >= 1073741824 )); then
        echo "$(awk "BEGIN {printf \"%.2f GB\", $bytes/1073741824}")"
    elif (( bytes >= 1048576 )); then
        echo "$(awk "BEGIN {printf \"%.2f MB\", $bytes/1048576}")"
    elif (( bytes >= 1024 )); then
        echo "$(awk "BEGIN {printf \"%.2f KB\", $bytes/1024}")"
    else
        echo "${bytes} B"
    fi
}

# Usage:
bytes_to_human 1536          # 1.50 KB
bytes_to_human 2097152       # 2.00 MB
bytes_to_human 5368709120    # 5.00 GB
```
