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
# Writing Bash Functions

---
## Day 3: Functions, Types & Advanced
- Functions: definition, return codes, parameters
- Variable types: strings, arrays, associative arrays
- Arithmetic: integer and floating point
- Arrays and associative arrays in depth
- Timing, OOP patterns, test harnesses, aliases

---
## Defining Functions

```bash
# Syntax 1: modern (preferred)
greet() {
    echo "Hello, $1!"
}

# Syntax 2: with function keyword
function greet {
    echo "Hello, $1!"
}

# Syntax 3: both (redundant but valid)
function greet() {
    echo "Hello, $1!"
}

# Call the function (no parentheses!)
greet "World"     # Hello, World!
greet Alice       # Hello, Alice!
```

---
## Functions are Commands

```bash
# Functions behave exactly like commands
# They have: arguments, return codes, stdin/stdout

greet() {
    echo "Hello, $1!"
}

# Pipe to a function
echo "World" | { read -r name; greet "$name"; }

# Redirect function output
greet "Alice" > greeting.txt

# Use in conditionals
is_even() {
    (( $1 % 2 == 0 ))
}

if is_even 42; then
    echo "42 is even"
fi
```

---
## Function Parameters

```bash
# Functions use the same $1, $2, $@ as scripts
# They HIDE the script's positional parameters

process_file() {
    echo "Function arg 1: $1"   # function's first arg
    echo "Function arg 2: $2"   # function's second arg
    echo "All function args: $@"
    echo "Number of args: $#"
}

# Call:
process_file "file1.txt" "file2.txt"
# Function arg 1: file1.txt
# Function arg 2: file2.txt
# All function args: file1.txt file2.txt
# Number of args: 2
```

---
## Return Codes from Functions

```bash
# return sets the function's exit status (0-255)
is_directory() {
    [[ -d "$1" ]] && return 0 || return 1
}

if is_directory "/tmp"; then
    echo "/tmp is a directory"
fi

# return without a value uses $? of the last command
check_file() {
    test -f "$1"    # return code becomes function's return code
}

# COMMON MISTAKE: using return for values
get_sum() {
    return $(( $1 + $2 ))    # WRONG! Limited to 0-255
}
get_sum 200 200    # returns 400 % 256 = 144!
```

---
## Returning Values from Functions

```bash
# Method 1: stdout (most common)
get_date() {
    date +%Y-%m-%d
}
today=$(get_date)

# Method 2: set a global variable
get_hostname() {
    RESULT=$(hostname)
}
get_hostname
echo "$RESULT"

# Method 3: nameref (bash 4.3+) - pass by reference
get_count() {
    local -n ref=$1    # ref is an alias for the named variable
    ref=$(wc -l < "$2")
}
get_count num_lines /etc/passwd
echo "Lines: $num_lines"
```

---
## Local Variables

```bash
# WITHOUT local: variables leak into the caller
bad_function() {
    x=42
}
x=1
bad_function
echo "$x"    # 42 (function changed our variable!)

# WITH local: variables are scoped to the function
good_function() {
    local x=42
    echo "inside: $x"    # 42
}
x=1
good_function
echo "outside: $x"       # 1 (unchanged)
```

---
## Always Use `local`

```bash
# Rule: EVERY variable in a function should be local
# unless you explicitly want it to be global

process() {
    local input="$1"
    local output=""
    local line
    local count=0

    while IFS= read -r line; do
        output+="$line"$'\n'
        count=$((count + 1))
    done < "$input"

    echo "$count lines processed"
}
```

---
## Pass By Reference (`nameref`)

```bash
# bash 4.3+ supports namerefs
swap() {
    local -n ref1=$1
    local -n ref2=$2
    local tmp="$ref1"
    ref1="$ref2"
    ref2="$tmp"
}

a=10
b=20
swap a b
echo "a=$a, b=$b"    # a=20, b=10

# namerefs work with arrays too!
fill_array() {
    local -n arr=$1
    arr=(one two three)
}
fill_array my_array
echo "${my_array[@]}"    # one two three
```

---
## Recursive Functions

```bash
# bash supports recursion
factorial() {
    local n=$1
    if (( n <= 1 )); then
        echo 1
    else
        local sub
        sub=$(factorial $((n - 1)))
        echo $((n * sub))
    fi
}

echo "5! = $(factorial 5)"    # 120

# WARNING: bash has a recursion limit
# FUNCNEST limits recursion depth (default: no limit,
# but stack will overflow)
FUNCNEST=100    # limit to 100 levels
```

---
## Function Libraries

```bash
# Create a library file (no shebang needed)
# lib/utils.sh

log_info()  { echo "[INFO]  $(date '+%T') $*"; }
log_error() { echo "[ERROR] $(date '+%T') $*" >&2; }

die() {
    log_error "$@"
    exit 1
}

require_command() {
    command -v "$1" > /dev/null || die "Required command not found: $1"
}

# Main script:
#!/bin/bash
source "$(dirname "$0")/lib/utils.sh"

require_command jq
require_command curl
log_info "All dependencies found"
```

---
## Function Scope: Dynamic Scoping

```bash
# bash uses DYNAMIC scoping (not lexical)
# A function can see locals of its caller!

outer() {
    local x=10
    inner
}

inner() {
    echo "x=$x"    # 10! inner sees outer's local
}

outer    # prints x=10

# This is unusual and can cause subtle bugs
# Python, JavaScript, C all use lexical scoping
# bash is different!
```

---
## Variadic Functions

```bash
# Accept any number of arguments
log_all() {
    local level=$1
    shift    # remove first arg, $@ now has the rest
    echo "[$level] $*"
}
log_all INFO "Server started on port" 8080
# [INFO] Server started on port 8080

# Process each argument
process_files() {
    local file
    for file in "$@"; do
        echo "Processing: $file"
        wc -l "$file"
    done
}
process_files *.txt
```

---
## Decorator Pattern

```bash
# Wrap a function with timing
with_timing() {
    local start end elapsed
    start=$(date +%s%N)
    "$@"
    local rc=$?
    end=$(date +%s%N)
    elapsed=$(( (end - start) / 1000000 ))
    echo "[$*] took ${elapsed}ms" >&2
    return $rc
}

# Usage:
with_timing sleep 2
# [sleep 2] took 2003ms

with_timing find /usr -name "*.so" -type f > /dev/null
```

---
## Functions vs Scripts vs Aliases
![functions_vs_scripts_vs_aliases](svg/courses/languages/bash/bash-scripting/17_functions/functions_vs_scripts_vs_aliases.svg)
