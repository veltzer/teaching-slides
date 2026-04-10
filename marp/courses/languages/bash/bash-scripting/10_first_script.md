# Writing Your First Script

---

## Bash Script Structure

![Bash Script Structure](svg/courses/languages/bash/bash-scripting/10_first_script/script_structure.svg)

---
## Day 2: Scripts, Syntax & I/O
- Writing and running scripts
- Control flow: conditionals, loops
- Pipes and how they work
- I/O: reading and writing files and processes
- Redirection in scripts
- Multi processing

---
## What is a Script?
- A text file containing shell commands
- Executed top to bottom (like a program)
- Can include variables, logic, loops, functions
- Automates tasks you would type manually

```bash
# The simplest script:
echo "Hello, World!"
```

---
## Choosing an Editor
| Editor | Type | Learning Curve | Power |
|--------|------|---------------|-------|
| `nano` | Terminal | Easy | Low |
| `vim` | Terminal | Steep | High |
| `emacs` | Terminal/GUI | Steep | Very High |
| `VS Code` | GUI | Easy | High |
| `Sublime` | GUI | Easy | Medium |

- For quick edits: `nano` or `vim`
- For development: `VS Code` with `bash` extensions

---
## The Shebang Line

```bash
#!/bin/bash

# The shebang (#!) tells the OS which interpreter to use
# It MUST be the very first line (no blank lines before it)

# Common shebangs:
#!/bin/bash          # use bash explicitly
#!/usr/bin/env bash  # find bash in PATH (more portable)
#!/bin/sh            # POSIX shell (might not be bash!)

# Wrong shebangs:
#! /bin/bash          # space after #! (works on Linux, not all)
# !/bin/bash          # space before ! (NOT a shebang)
```

---
## Why `#!/usr/bin/env bash`?

```bash
# On most Linux systems:
# /bin/bash exists

# But on some systems (macOS with brew, NixOS, FreeBSD):
# bash might be in /usr/local/bin/bash or elsewhere

# env searches PATH for the program:
#!/usr/bin/env bash
# This finds bash wherever it is installed

# Trade-off: you can't pass flags to bash this way
#!/bin/bash -x        # works (debug mode)
#!/usr/bin/env bash -x  # DOES NOT WORK on Linux
```

---
## Making a Script Executable

```bash
# Method 1: chmod
chmod +x myscript.sh
./myscript.sh

# Method 2: chmod with specific permissions
chmod 755 myscript.sh   # rwxr-xr-x (everyone can execute)
chmod 700 myscript.sh   # rwx------ (only owner)

# Method 3: run with bash explicitly (no chmod needed)
bash myscript.sh

# What happens without chmod +x:
./myscript.sh
# bash: ./myscript.sh: Permission denied
```

---
## File Extensions

```bash
# .sh extension is optional but conventional
myscript.sh       # common convention
myscript.bash     # some people prefer this
myscript          # also fine (many system scripts)
deploy            # commands often have no extension

# The extension does NOT determine the interpreter
# The shebang does!

# In /usr/bin, almost nothing has an extension:
ls /usr/bin/ | head -20
# adduser, apt, awk, base64, basename, bash...
```

---
## Script Arguments

```bash
#!/bin/bash

# Special variables for arguments:
echo "Script name: $0"
echo "First arg:   $1"
echo "Second arg:  $2"
echo "All args:    $@"
echo "All args:    $*"
echo "Num of args: $#"

# Usage:
# ./script.sh hello world
# Script name: ./script.sh
# First arg:   hello
# Second arg:  world
# All args:    hello world
# All args:    hello world
# Num of args: 2
```

---
## `$@` vs `$*`

```bash
#!/bin/bash

# Without quotes, they behave the same
# With quotes, they differ:

# "$@" preserves each argument as a separate word
for arg in "$@"; do
    echo "arg: [$arg]"
done
# ./script.sh "hello world" foo
# arg: [hello world]
# arg: [foo]

# "$*" joins all arguments into one string
for arg in "$*"; do
    echo "arg: [$arg]"
done
# arg: [hello world foo]
```

---
## The `shift` Command

```bash
#!/bin/bash

# shift removes the first argument and shifts the rest down
echo "Before: $1 $2 $3"    # a b c
shift
echo "After:  $1 $2 $3"    # b c

# Common pattern: process flags
while [ $# -gt 0 ]; do
    case "$1" in
        -v|--verbose) verbose=1 ;;
        -o|--output)  output="$2"; shift ;;
        -h|--help)    show_help; exit 0 ;;
        *)            files+=("$1") ;;
    esac
    shift
done
```

---
## Failure Handling: The Strict Mode

```bash
#!/bin/bash
set -euo pipefail

# Always put this near the top of your scripts
# -e : exit on error
# -u : error on undefined variable
# -o pipefail : catch errors in pipelines

# Consider also:
IFS=$'\n\t'     # safer word splitting
```

---
## Debugging Scripts

```bash
# Method 1: bash -x (trace every command)
bash -x myscript.sh

# Method 2: set -x inside the script
#!/bin/bash
set -x
echo "this line is traced"
set +x
echo "this line is not traced"

# Method 3: PS4 for better trace output
export PS4='+ ${BASH_SOURCE}:${LINENO}: '
set -x
# + myscript.sh:5: echo hello
```

---
## More Debugging Techniques

```bash
# Syntax check without running
bash -n myscript.sh
# Only reports syntax errors, doesn't execute

# Verbose mode (print each line before execution)
bash -v myscript.sh

# Combine them
bash -xv myscript.sh

# Debug specific sections
#!/bin/bash
echo "normal"
set -x          # start debugging
problematic_function
set +x          # stop debugging
echo "normal"
```

---
## Using `shellcheck`

```bash
# shellcheck is a static analysis tool for bash scripts
# Install: apt install shellcheck / brew install shellcheck

# Run it:
shellcheck myscript.sh

# Example output:
# In myscript.sh line 3:
# echo $foo
#      ^--^ SC2086: Double quote to prevent globbing
#                    and word splitting

# Inline directives to suppress warnings:
# shellcheck disable=SC2086
echo $foo
```

---
## Template: Basic Script

```bash
#!/bin/bash
set -euo pipefail

readonly SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
readonly SCRIPT_NAME="$(basename "$0")"

usage() {
    cat << EOF
Usage: $SCRIPT_NAME [options] <argument>

Options:
    -h, --help     Show this help
    -v, --verbose  Enable verbose output
EOF
}

main() {
    local verbose=0

    while [[ $# -gt 0 ]]; do
        case "$1" in
            -h|--help)    usage; exit 0 ;;
            -v|--verbose) verbose=1 ;;
            *)            break ;;
        esac
        shift
    done

    [[ $# -lt 1 ]] && { usage; exit 1; }

    echo "Working with: $1"
}

main "$@"
```

---
## The `source` Command (`.`)

```bash
# source (or .) runs a script in the CURRENT shell
# Variables and functions persist

# config.sh:
export DB_HOST="localhost"
export DB_PORT=5432

# main.sh:
source config.sh
echo "$DB_HOST:$DB_PORT"    # localhost:5432

# Shorthand:
. config.sh

# IMPORTANT: source vs execute
bash config.sh    # runs in subshell, changes are lost
source config.sh  # runs in current shell, changes persist
```
