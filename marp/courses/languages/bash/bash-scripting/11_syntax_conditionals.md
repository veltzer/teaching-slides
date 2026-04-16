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
# Syntax: Conditionals

---

## Conditional Flow in Bash

![Conditional Flow in Bash](svg/courses/languages/bash/bash-scripting/11_syntax_conditionals/if_elif_else_flow.svg)

---
## The `if` Statement

```bash
# Basic structure:
if command; then
    echo "command succeeded"
fi

# if checks the RETURN CODE of the command
# 0 = true (success), non-zero = false (failure)

if grep -q "root" /etc/passwd; then
    echo "root user exists"
fi

# With else:
if [ -f "$file" ]; then
    echo "File exists"
else
    echo "File not found"
fi
```

---
## `if` / `elif` / `else`

```bash
#!/bin/bash

if [ "$1" = "start" ]; then
    echo "Starting service..."
elif [ "$1" = "stop" ]; then
    echo "Stopping service..."
elif [ "$1" = "restart" ]; then
    echo "Restarting service..."
else
    echo "Usage: $0 {start|stop|restart}"
    exit 1
fi
```

---
## No Brace Style (Using Commands Directly)

```bash
# You don't need [ or [[ at all!
# if just tests the return code of any command

if grep -q "error" logfile.txt; then
    echo "Errors found"
fi

if ping -c 1 -W 1 google.com > /dev/null 2>&1; then
    echo "Network is up"
fi

if cd /target/directory; then
    echo "Changed to target directory"
else
    echo "Cannot access directory"
fi
```

---
## The `test` Command and `[`

```bash
# [ is literally a command (alias for test)
# It requires a closing ]

# File tests:
[ -f "$file" ]     # file exists and is regular file
[ -d "$dir" ]      # directory exists
[ -e "$path" ]     # path exists (any type)
[ -r "$file" ]     # file is readable
[ -w "$file" ]     # file is writable
[ -x "$file" ]     # file is executable
[ -s "$file" ]     # file exists and is non-empty
[ -L "$link" ]     # is a symbolic link
```

---
## String Tests with `[`

```bash
# String comparison
[ "$a" = "$b" ]       # strings are equal
[ "$a" != "$b" ]      # strings are not equal
[ -z "$str" ]         # string is empty (zero length)
[ -n "$str" ]         # string is non-empty

# ALWAYS QUOTE YOUR VARIABLES!
# Without quotes:
x=""
[ $x = "hello" ]      # becomes: [ = "hello" ] -> ERROR
[ "$x" = "hello" ]    # becomes: [ "" = "hello" ] -> OK
```

---
## Numeric Tests with `[`

```bash
# Integer comparison (not string comparison!)
[ "$a" -eq "$b" ]    # equal
[ "$a" -ne "$b" ]    # not equal
[ "$a" -lt "$b" ]    # less than
[ "$a" -le "$b" ]    # less than or equal
[ "$a" -gt "$b" ]    # greater than
[ "$a" -ge "$b" ]    # greater than or equal

# COMMON MISTAKE: using string comparison for numbers
[ 10 > 9 ]           # WRONG! > is redirection
[ "10" \> "9" ]       # string comparison: "10" < "9" (1 < 9)
[ 10 -gt 9 ]         # CORRECT: numeric comparison
```

---
## Logical Operators with `[`

```bash
# AND: -a (inside test) or && (between tests)
[ -f "$file" -a -r "$file" ]       # old style
[ -f "$file" ] && [ -r "$file" ]   # preferred

# OR: -o (inside test) or || (between tests)
[ "$x" -eq 1 -o "$x" -eq 2 ]      # old style
[ "$x" -eq 1 ] || [ "$x" -eq 2 ]  # preferred

# NOT: !
[ ! -f "$file" ]
if ! [ -f "$file" ]; then
    echo "file missing"
fi
```

---
## The `[[` Keyword (bash Extension)

```bash
# [[ is a bash keyword, not a command
# Advantages over [:

# 1. No word splitting on variables (quotes optional)
[[ $name = "hello" ]]     # safe even without quotes

# 2. Pattern matching with = or ==
[[ $file == *.txt ]]       # glob pattern matching

# 3. Regex matching with =~
[[ $email =~ ^[a-z]+@[a-z]+\.[a-z]+$ ]]

# 4. Logical operators && and || inside
[[ -f $file && -r $file ]]

# 5. No need to escape < and >
[[ "abc" < "def" ]]       # string comparison
```

---
## `[[` Pattern Matching

```bash
# Glob patterns (not regex!)
[[ $filename == *.tar.gz ]]    # ends with .tar.gz
[[ $hostname == web* ]]        # starts with web
[[ $char == [a-z] ]]           # single lowercase letter

# IMPORTANT: do NOT quote the pattern
[[ $filename == "*.tar.gz" ]]  # matches literal *.tar.gz
[[ $filename == *.tar.gz ]]    # matches the pattern

# Extended globbing works too
shopt -s extglob
[[ $file == *.@(jpg|png|gif) ]]
```

---
## `[[` Regex Matching

```bash
# =~ operator for regular expressions
if [[ $email =~ ^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$ ]]; then
    echo "Valid email"
fi

# Capture groups via BASH_REMATCH
if [[ "2024-03-15" =~ ^([0-9]{4})-([0-9]{2})-([0-9]{2})$ ]]; then
    echo "Year:  ${BASH_REMATCH[1]}"    # 2024
    echo "Month: ${BASH_REMATCH[2]}"    # 03
    echo "Day:   ${BASH_REMATCH[3]}"    # 15
fi

# Store complex regex in a variable
pattern='^[0-9]+$'
[[ "$input" =~ $pattern ]] && echo "is a number"
```

---
## `[` vs `[[` Summary
| Feature | `[` (test) | `[[` |
|---------|-----------|------|
| POSIX compatible | Yes | No (bash only) |
| Word splitting | Yes (quote!) | No |
| Glob patterns | No | `==` |
| Regex | No | `=~` |
| `&&` / `\|\|` inside | No | Yes |
| `<` / `>` for strings | Must escape | Direct |

---
## The `case` Statement

```bash
#!/bin/bash

case "$1" in
    start)
        echo "Starting..."
        ;;
    stop)
        echo "Stopping..."
        ;;
    restart|reload)
        echo "Restarting..."
        ;;
    status)
        echo "Status: running"
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status}"
        exit 1
        ;;
esac
```

---
## `case` with Patterns

```bash
# case supports glob patterns
case "$filename" in
    *.tar.gz|*.tgz)
        tar xzf "$filename"
        ;;
    *.tar.bz2)
        tar xjf "$filename"
        ;;
    *.zip)
        unzip "$filename"
        ;;
    *.txt|*.md|*.rst)
        cat "$filename"
        ;;
    *)
        echo "Unknown file type: $filename"
        ;;
esac
```

---
## `case` Fall-Through (`bash` 4.0+)

```bash
# ;; stops execution (like break)
# ;;& tests the next pattern too
# ;& falls through to next action (like C switch)

case "$level" in
    error)
        echo "ERROR" >&2
        ;;&
    warning)
        echo "WARNING" >&2
        ;;&
    info|error|warning)
        log_to_file "$level" "$message"
        ;;
esac
# error triggers: ERROR, WARNING, and log_to_file
```

---
## Ternary-Style Expressions

```bash
# bash doesn't have a ternary operator, but you can fake it:

# Method 1: && / ||
[[ $x -gt 0 ]] && result="positive" || result="non-positive"

# Method 2: arithmetic ternary
result=$(( x > 0 ? x : -x ))    # absolute value

# Method 3: one-line if
if [[ $x -gt 0 ]]; then echo "pos"; else echo "neg"; fi
```
