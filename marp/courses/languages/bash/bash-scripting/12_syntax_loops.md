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
# Syntax: Loops

---
## Loop Types Overview

![loop_types_overview](svg/courses/languages/bash/bash-scripting/12_syntax_loops/loop_types_overview.svg)

---
## `while` Loops

```bash
# Basic while loop
count=1
while [ $count -le 5 ]; do
    echo "Count: $count"
    count=$((count + 1))
done

# Using [[ (bash):
while [[ $count -le 5 ]]; do
    echo "Count: $count"
    ((count++))
done
```

---
## `while` with a Command

```bash
# while tests the return code of any command
while ping -c 1 -W 1 server.example.com > /dev/null 2>&1; do
    echo "Server is up"
    sleep 5
done
echo "Server is DOWN!"

# Wait for a file to appear
while [ ! -f /tmp/ready.flag ]; do
    echo "Waiting..."
    sleep 1
done
echo "Ready!"
```

---
## Reading Lines with `while`

```bash
# Read a file line by line
while IFS= read -r line; do
    echo "Line: $line"
done < file.txt

# Why IFS= and -r?
# IFS=     : prevents stripping leading/trailing whitespace
# -r       : prevents backslash interpretation

# WRONG (common mistake):
cat file.txt | while read line; do
    count=$((count + 1))
done
echo "$count"    # 0! (while ran in subshell due to pipe)

# RIGHT:
count=0
while IFS= read -r line; do
    count=$((count + 1))
done < file.txt
echo "$count"    # correct count
```

---
## `until` Loops

```bash
# until is the opposite of while
# Runs UNTIL the condition is true (while it's false)

count=1
until [ $count -gt 5 ]; do
    echo "Count: $count"
    count=$((count + 1))
done

# Wait until a service is ready
until curl -s http://localhost:8080/health > /dev/null; do
    echo "Waiting for service..."
    sleep 2
done
echo "Service is ready!"
```

---
## Infinite Loops

```bash
# Method 1: while true
while true; do
    echo "Running forever..."
    sleep 1
done

# Method 2: while :
while :; do
    echo "Running forever..."
    sleep 1
done

# Method 3: C-style
for ((;;)); do
    echo "Running forever..."
    sleep 1
done

# Break out with break
while true; do
    read -p "Continue? (y/n) " answer
    [[ $answer == "n" ]] && break
done
```

---
## `for` Loops: Word List

```bash
# Iterate over a list of words
for fruit in apple banana cherry; do
    echo "I like $fruit"
done

# Iterate over files (glob)
for file in *.txt; do
    echo "Processing: $file"
done

# Iterate over command output
for user in $(cut -d: -f1 /etc/passwd); do
    echo "User: $user"
done

# Iterate over array
colors=(red green blue)
for color in "${colors[@]}"; do
    echo "Color: $color"
done
```

---
## `for` Loops: C-Style

```bash
# C-style for loop (bash extension)
for ((i = 0; i < 10; i++)); do
    echo "i = $i"
done

# Count down
for ((i = 10; i > 0; i--)); do
    echo "$i..."
done
echo "Liftoff!"

# Multiple variables
for ((i = 0, j = 10; i < j; i++, j--)); do
    echo "i=$i, j=$j"
done
```

---
## `for` with Sequences

```bash
# Using brace expansion
for i in {1..10}; do
    echo "$i"
done

# With step
for i in {0..100..10}; do
    echo "$i"
done

# Using seq (external command)
for i in $(seq 1 10); do
    echo "$i"
done

# seq with step
for i in $(seq 0 5 100); do
    echo "$i"
done
```

---
## `break` and `continue`

```bash
# break exits the loop
for i in {1..100}; do
    [[ $i -gt 5 ]] && break
    echo "$i"
done
# prints 1 2 3 4 5

# continue skips to the next iteration
for i in {1..10}; do
    [[ $((i % 2)) -eq 0 ]] && continue
    echo "$i"
done
# prints 1 3 5 7 9

# break N and continue N for nested loops
for i in {1..3}; do
    for j in {1..3}; do
        [[ $j -eq 2 ]] && continue 2  # continue outer loop
        echo "$i $j"
    done
done
```

---
## Loop Over Arguments

```bash
#!/bin/bash

# Process all script arguments
for arg in "$@"; do
    echo "Processing: $arg"
done

# Shorthand: for without "in list" uses "$@"
for arg; do
    echo "Processing: $arg"
done

# Process files passed as arguments
for file in "$@"; do
    if [[ -f "$file" ]]; then
        wc -l "$file"
    else
        echo "Not a file: $file" >&2
    fi
done
```

---
## Looping Over Lines (Safely)

```bash
# WRONG: for loop splits on whitespace, not lines
for line in $(cat file.txt); do   # BAD!
    echo "$line"
done
# "hello world" becomes two iterations: "hello" "world"

# RIGHT: use while read
while IFS= read -r line; do
    echo "$line"
done < file.txt

# Also RIGHT: use mapfile (bash 4.0+)
mapfile -t lines < file.txt
for line in "${lines[@]}"; do
    echo "$line"
done
```

---
## `select` Loop (Menus)

```bash
#!/bin/bash

# select creates an interactive menu
PS3="Choose a color: "    # prompt
select color in red green blue quit; do
    case "$color" in
        red)   echo "You chose red" ;;
        green) echo "You chose green" ;;
        blue)  echo "You chose blue" ;;
        quit)  break ;;
        *)     echo "Invalid choice" ;;
    esac
done

# Output:
# 1) red
# 2) green
# 3) blue
# 4) quit
# Choose a color:
```

---
## Loop Patterns: Find and Process Files

```bash
# Safe way to iterate over files with find
while IFS= read -r -d '' file; do
    echo "Processing: $file"
done < <(find /path -name "*.txt" -print0)

# -print0 uses null byte as separator
# -d '' reads until null byte
# This handles filenames with spaces, newlines, etc.

# Alternative with find -exec
find /path -name "*.txt" -exec process.sh {} \;

# Or with xargs
find /path -name "*.txt" -print0 | xargs -0 wc -l
```
