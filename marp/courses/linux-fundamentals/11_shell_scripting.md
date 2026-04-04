# Shell Scripting Introduction
## Getting Started with Shell Programming
---
## Your First Shell Script

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="20" y="15" width="130" height="55" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="85" y="37" text-anchor="middle" font-size="11" font-weight="bold">#!/bin/bash</text>
  <text x="85" y="55" text-anchor="middle" font-size="9">Shebang line</text>
  <rect x="170" y="15" width="130" height="55" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="235" y="37" text-anchor="middle" font-size="11" font-weight="bold">chmod +x</text>
  <text x="235" y="55" text-anchor="middle" font-size="9">Make executable</text>
  <rect x="320" y="15" width="130" height="55" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="385" y="37" text-anchor="middle" font-size="11" font-weight="bold">./script.sh</text>
  <text x="385" y="55" text-anchor="middle" font-size="9">Execute script</text>
  <rect x="470" y="15" width="110" height="55" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="525" y="37" text-anchor="middle" font-size="11" font-weight="bold">exit $?</text>
  <text x="525" y="55" text-anchor="middle" font-size="9">Return status</text>
  <line x1="150" y1="42" x2="170" y2="42" stroke="#333" stroke-width="2" marker-end="url(#arrowd0_10_shell_scripting)"/>
  <line x1="300" y1="42" x2="320" y2="42" stroke="#333" stroke-width="2" marker-end="url(#arrowd0_10_shell_scripting)"/>
  <line x1="450" y1="42" x2="470" y2="42" stroke="#333" stroke-width="2" marker-end="url(#arrowd0_10_shell_scripting)"/>
  <rect x="50" y="100" width="500" height="75" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="5"/>
  <text x="300" y="120" text-anchor="middle" font-size="11" font-weight="bold">Script Execution Flow</text>
  <text x="300" y="140" text-anchor="middle" font-size="10">1. Shell reads shebang -> 2. Loads interpreter -> 3. Executes line by line</text>
  <text x="300" y="158" text-anchor="middle" font-size="10">4. Returns exit code (0 = success, non-zero = error)</text>
  <defs>
    <marker id="arrowd0_10_shell_scripting" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

Basic script:

```bash
#!/bin/bash
# My first script
echo "Hello, World!"
```

Running the script:

```bash
chmod +x script.sh
./script.sh
```

---

## Script Structure

```bash
#!/bin/bash

# Comments and documentation
# Author: Your Name
# Date: 2024-11-19
# Purpose: Example script

# Constants
readonly MAX_COUNT=10

# Variables
name="John"

# Main logic
echo "Starting script..."
echo "Hello, $name"

# Exit with status
exit 0
```

---

## Variables

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="20" y="15" width="170" height="70" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="105" y="35" text-anchor="middle" font-size="11" font-weight="bold">Local Variables</text>
  <text x="105" y="52" text-anchor="middle" font-size="10">name="John"</text>
  <text x="105" y="68" text-anchor="middle" font-size="10">age=25</text>
  <rect x="215" y="15" width="170" height="70" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="35" text-anchor="middle" font-size="11" font-weight="bold">Environment Vars</text>
  <text x="300" y="52" text-anchor="middle" font-size="10">$HOME, $PATH</text>
  <text x="300" y="68" text-anchor="middle" font-size="10">export MY_VAR</text>
  <rect x="410" y="15" width="170" height="70" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="495" y="35" text-anchor="middle" font-size="11" font-weight="bold">Cmd Substitution</text>
  <text x="495" y="52" text-anchor="middle" font-size="10">$(date)</text>
  <text x="495" y="68" text-anchor="middle" font-size="10">`whoami`</text>
  <rect x="80" y="110" width="200" height="55" fill="#fff3e0" stroke="#333" stroke-width="1" rx="5"/>
  <text x="180" y="132" text-anchor="middle" font-size="11" font-weight="bold">Access: $var / ${var}</text>
  <text x="180" y="150" text-anchor="middle" font-size="9">No spaces around = sign</text>
  <rect x="320" y="110" width="200" height="55" fill="#ffebee" stroke="#333" stroke-width="1" rx="5"/>
  <text x="420" y="132" text-anchor="middle" font-size="11" font-weight="bold">Read-only: readonly</text>
  <text x="420" y="150" text-anchor="middle" font-size="9">readonly MAX=100</text>
</svg>

Variable examples:

```bash
# Assignment
name="John"
age=25

# Using variables
echo "Name: $name"
echo "Age: ${age}"

# Command output
current_date=$(date)
files=`ls`

# Read user input
read -p "Enter name: " user_name
```

---

## Command Line Arguments

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="20" y="15" width="140" height="50" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="90" y="35" text-anchor="middle" font-size="10" font-weight="bold">./script.sh</text>
  <text x="90" y="52" text-anchor="middle" font-size="10">arg1 arg2 arg3</text>
  <line x1="160" y1="40" x2="190" y2="40" stroke="#333" stroke-width="2" marker-end="url(#arrowd2_10_shell_scripting)"/>
  <rect x="190" y="10" width="85" height="30" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="3"/>
  <text x="232" y="30" text-anchor="middle" font-size="10">$0</text>
  <rect x="285" y="10" width="85" height="30" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="3"/>
  <text x="327" y="30" text-anchor="middle" font-size="10">$1</text>
  <rect x="380" y="10" width="85" height="30" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="3"/>
  <text x="422" y="30" text-anchor="middle" font-size="10">$2</text>
  <rect x="475" y="10" width="85" height="30" fill="#fff3e0" stroke="#333" stroke-width="1" rx="3"/>
  <text x="517" y="30" text-anchor="middle" font-size="10">$3</text>
  <text x="232" y="58" text-anchor="middle" font-size="9" fill="#555">script name</text>
  <text x="327" y="58" text-anchor="middle" font-size="9" fill="#555">arg1</text>
  <text x="422" y="58" text-anchor="middle" font-size="9" fill="#555">arg2</text>
  <text x="517" y="58" text-anchor="middle" font-size="9" fill="#555">arg3</text>
  <rect x="50" y="80" width="230" height="50" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="5"/>
  <text x="165" y="100" text-anchor="middle" font-size="10" font-weight="bold">$# = argument count</text>
  <text x="165" y="118" text-anchor="middle" font-size="9">$@ = all args, $* = all as one</text>
  <rect x="310" y="80" width="240" height="50" fill="#ffebee" stroke="#333" stroke-width="1" rx="5"/>
  <text x="430" y="100" text-anchor="middle" font-size="10" font-weight="bold">shift = remove $1</text>
  <text x="430" y="118" text-anchor="middle" font-size="9">$2 becomes $1, $3 becomes $2...</text>
  <rect x="100" y="150" width="400" height="35" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="3"/>
  <text x="300" y="172" text-anchor="middle" font-size="10">$? = exit status of last command (0=success)</text>
  <defs>
    <marker id="arrowd2_10_shell_scripting" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

Argument handling:

```bash
#!/bin/bash

echo "Script name: $0"
echo "First argument: $1"
echo "Second argument: $2"
echo "Number of arguments: $#"
echo "All arguments: $@"

# Shift arguments
shift
echo "New first argument: $1"
```

---

## Mathematical Operations

```bash
# Basic arithmetic
result=$((5 + 3))
echo $result

# Using let
let "a = 5"
let "b = a + 3"

# Using expr (legacy)
result=`expr 5 + 3`

# Floating point with bc
result=$(echo "5.5 + 3.2" | bc)

# Increment/Decrement
let "count++"
let "count--"
```

---

## Exit Status and Error Handling

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="20" y="15" width="120" height="65" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="80" y="35" text-anchor="middle" font-size="11" font-weight="bold">Exit 0</text>
  <text x="80" y="52" text-anchor="middle" font-size="10">Success</text>
  <text x="80" y="68" text-anchor="middle" font-size="9" fill="#2e7d32">Command OK</text>
  <rect x="160" y="15" width="120" height="65" fill="#ffebee" stroke="#333" stroke-width="2" rx="5"/>
  <text x="220" y="35" text-anchor="middle" font-size="11" font-weight="bold">Exit 1</text>
  <text x="220" y="52" text-anchor="middle" font-size="10">General Error</text>
  <text x="220" y="68" text-anchor="middle" font-size="9" fill="#c62828">Catchall</text>
  <rect x="300" y="15" width="120" height="65" fill="#ffebee" stroke="#333" stroke-width="2" rx="5"/>
  <text x="360" y="35" text-anchor="middle" font-size="11" font-weight="bold">Exit 2</text>
  <text x="360" y="52" text-anchor="middle" font-size="10">Misuse</text>
  <text x="360" y="68" text-anchor="middle" font-size="9" fill="#c62828">Bad syntax</text>
  <rect x="440" y="15" width="140" height="65" fill="#ffebee" stroke="#333" stroke-width="2" rx="5"/>
  <text x="510" y="35" text-anchor="middle" font-size="11" font-weight="bold">Exit 126/127</text>
  <text x="510" y="52" text-anchor="middle" font-size="10">Not executable /</text>
  <text x="510" y="68" text-anchor="middle" font-size="9" fill="#c62828">Not found</text>
  <rect x="20" y="100" width="560" height="75" fill="#fff3e0" stroke="#333" stroke-width="1" rx="5"/>
  <text x="300" y="122" text-anchor="middle" font-size="11" font-weight="bold">Error Handling Patterns</text>
  <text x="300" y="140" text-anchor="middle" font-size="10">$? = check last exit code | set -e = exit on error</text>
  <text x="300" y="158" text-anchor="middle" font-size="10">trap 'cleanup' EXIT | command || { echo "failed"; exit 1; }</text>
</svg>

Error handling:

```bash
#!/bin/bash

# Check command success
if ! command -v git &> /dev/null; then
    echo "Error: git not found"
    exit 1
fi

# Check previous command
some_command
if [ $? -ne 0 ]; then
    echo "Error occurred"
    exit 1
fi
```

---

## Expressions and Operators

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="20" y="10" width="170" height="70" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="105" y="30" text-anchor="middle" font-size="11" font-weight="bold">Numeric Tests</text>
  <text x="105" y="48" text-anchor="middle" font-size="9">-eq -ne -lt -gt</text>
  <text x="105" y="62" text-anchor="middle" font-size="9">-le -ge</text>
  <rect x="215" y="10" width="170" height="70" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="30" text-anchor="middle" font-size="11" font-weight="bold">String Tests</text>
  <text x="300" y="48" text-anchor="middle" font-size="9">= != -z (empty)</text>
  <text x="300" y="62" text-anchor="middle" font-size="9">-n (non-empty)</text>
  <rect x="410" y="10" width="170" height="70" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="495" y="30" text-anchor="middle" font-size="11" font-weight="bold">File Tests</text>
  <text x="495" y="48" text-anchor="middle" font-size="9">-f (file) -d (dir)</text>
  <text x="495" y="62" text-anchor="middle" font-size="9">-r -w -x (perms)</text>
  <rect x="60" y="100" width="220" height="55" fill="#fff3e0" stroke="#333" stroke-width="1" rx="5"/>
  <text x="170" y="120" text-anchor="middle" font-size="10" font-weight="bold">[ ... ] single bracket</text>
  <text x="170" y="140" text-anchor="middle" font-size="9">POSIX compatible, classic test</text>
  <rect x="320" y="100" width="220" height="55" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="5"/>
  <text x="430" y="120" text-anchor="middle" font-size="10" font-weight="bold">[[ ... ]] double bracket</text>
  <text x="430" y="140" text-anchor="middle" font-size="9">Bash extended, regex support</text>
  <rect x="60" y="165" width="480" height="25" fill="#ffebee" stroke="#333" stroke-width="1" rx="3"/>
  <text x="300" y="183" text-anchor="middle" font-size="10">Logical: && (AND) | || (OR) | ! (NOT)</text>
</svg>

Examples:

```bash
# Arithmetic
[ $a -eq $b ]  # Equal
[ $a -lt $b ]  # Less than

# String
[ -z "$str" ]  # Empty
[ "$a" = "$b" ] # Equal

# File
[ -f "file" ]  # Exists and regular
[ -d "dir" ]   # Directory exists
```

---

## Flow Control: If Statements

```bash
# Basic if
if [ "$a" -eq "$b" ]; then
    echo "Equal"
fi

# If-else
if [ "$count" -gt 10 ]; then
    echo "Greater than 10"
else
    echo "Less than or equal to 10"
fi

# If-elif-else
if [ "$grade" -ge 90 ]; then
    echo "A"
elif [ "$grade" -ge 80 ]; then
    echo "B"
else
    echo "C"
fi
```

---

## Case Statements

```bash
case "$option" in
    start)
        echo "Starting service"
        start_service
        ;;
    stop)
        echo "Stopping service"
        stop_service
        ;;
    restart)
        echo "Restarting service"
        restart_service
        ;;
    *)
        echo "Usage: $0 {start|stop|restart}"
        exit 1
        ;;
esac
```

---

## Loops

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="20" y="10" width="170" height="80" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="105" y="30" text-anchor="middle" font-size="11" font-weight="bold">for loop</text>
  <text x="105" y="48" text-anchor="middle" font-size="9">for i in list; do</text>
  <text x="105" y="62" text-anchor="middle" font-size="9">  commands</text>
  <text x="105" y="76" text-anchor="middle" font-size="9">done</text>
  <rect x="215" y="10" width="170" height="80" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="30" text-anchor="middle" font-size="11" font-weight="bold">while loop</text>
  <text x="300" y="48" text-anchor="middle" font-size="9">while [ cond ]; do</text>
  <text x="300" y="62" text-anchor="middle" font-size="9">  commands</text>
  <text x="300" y="76" text-anchor="middle" font-size="9">done</text>
  <rect x="410" y="10" width="170" height="80" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="495" y="30" text-anchor="middle" font-size="11" font-weight="bold">until loop</text>
  <text x="495" y="48" text-anchor="middle" font-size="9">until [ cond ]; do</text>
  <text x="495" y="62" text-anchor="middle" font-size="9">  commands</text>
  <text x="495" y="76" text-anchor="middle" font-size="9">done</text>
  <rect x="50" y="110" width="230" height="40" fill="#fff3e0" stroke="#333" stroke-width="1" rx="5"/>
  <text x="165" y="128" text-anchor="middle" font-size="10" font-weight="bold">break</text>
  <text x="165" y="142" text-anchor="middle" font-size="9">Exit loop immediately</text>
  <rect x="310" y="110" width="230" height="40" fill="#ffebee" stroke="#333" stroke-width="1" rx="5"/>
  <text x="425" y="128" text-anchor="middle" font-size="10" font-weight="bold">continue</text>
  <text x="425" y="142" text-anchor="middle" font-size="9">Skip to next iteration</text>
  <rect x="100" y="165" width="400" height="25" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="3"/>
  <text x="300" y="183" text-anchor="middle" font-size="10">C-style: for ((i=0; i&lt;10; i++)); do ... done</text>
</svg>

Examples:

```bash
# For loop
for i in 1 2 3 4 5; do
    echo "Number: $i"
done

# While loop
count=0
while [ $count -lt 5 ]; do
    echo "Count: $count"
    let count++
done

# Until loop
until [ "$answer" = "yes" ]; do
    read -p "Continue? " answer
done
```

---

## Functions

```bash
# Function definition
greeting() {
    local name="$1"
    echo "Hello, $name!"
}

# Function with return
is_number() {
    [[ "$1" =~ ^[0-9]+$ ]]
    return $?
}

# Using functions
greeting "John"

if is_number "123"; then
    echo "Valid number"
fi
```

---

## Practical Script Example

```bash
#!/bin/bash

# Backup script
backup_files() {
    local source_dir="$1"
    local backup_dir="$2"
    local timestamp=$(date +%Y%m%d_%H%M%S)

    # Check directories
    if [ ! -d "$source_dir" ]; then
        echo "Error: Source directory not found"
        return 1
    fi

    # Create backup
    tar -czf "$backup_dir/backup_$timestamp.tar.gz" \
        -C "$source_dir" .

    if [ $? -eq 0 ]; then
        echo "Backup created successfully"
        return 0
    else
        echo "Backup failed"
        return 1
    fi
}

# Main script
backup_files "/path/to/source" "/path/to/backup"
```

---

## Debugging Scripts

```bash
# Enable debugging
set -x  # Print commands
set -e  # Exit on error
set -u  # Error on undefined variables

# Run with debug
bash -x script.sh

# Debug specific section
set -x
# debugging starts
commands here
set +x
# debugging ends
```
