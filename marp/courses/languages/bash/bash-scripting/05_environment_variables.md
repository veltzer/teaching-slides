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

# Environment and Shell Variables

---

## Two Kinds of Variables
![two_kinds_of_variables](svg/courses/languages/bash/bash-scripting/05_environment_variables/two_kinds_of_variables.svg)

---

## Shell Variables

```bash
# Define a shell variable
greeting="hello"

# It is visible in this shell
echo "$greeting"    # hello

# But NOT in child processes
bash -c 'echo "child sees: $greeting"'
# child sees:   (empty!)
```

---

## Environment Variables

```bash
# Promote a shell variable to the environment
greeting="hello"
export greeting

# Or define and export in one step
export greeting="hello"

# Now child processes can see it
bash -c 'echo "child sees: $greeting"'
# child sees: hello
```

---

## Viewing All Variables

```bash
# See all environment variables
env
# or
printenv

# See all shell variables (including environment)
set

# See just exported variables
export -p

# Check if a specific variable is exported
declare -p PATH
# declare -x PATH="/usr/local/bin:/usr/bin:/bin"
# The -x flag means "exported"
```

---

## Common Environment Variables

| Variable | Purpose |
|----------|---------|
| `PATH` | Command search path |
| `HOME` | User's home directory |
| `USER` | Current username |
| `SHELL` | User's default shell |
| `PWD` | Current working directory |
| `OLDPWD` | Previous working directory |
| `LANG` | Locale setting |
| `TERM` | Terminal type |
| `EDITOR` | Default text editor |

---

## Defining Variables: The Rules

```bash
# Variable names: letters, digits, underscores
# Must start with letter or underscore
my_var=1        # OK
_private=2      # OK
MY_CONST=3      # OK (convention: uppercase = constant/env)

# These are INVALID:
2things=bad     # starts with digit
my-var=bad      # contains hyphen
my.var=bad      # contains dot
my var=bad      # contains space
```

---

## Temporary Environment for One Command

```bash
# Set a variable ONLY for one command
LANG=C sort file.txt

# The variable is NOT set afterwards
echo "$LANG"    # unchanged

# Multiple variables:
CC=gcc CFLAGS="-O2" make

# This is extremely useful:
DEBUG=1 ./my_script.sh
TZ=UTC date
```

---

## Deleting Variables

```bash
# Remove a variable entirely
x=5
unset x
echo "$x"    # (empty)

# unset removes from both shell and environment
export y=10
unset y
# y is gone from everywhere

# Setting to empty is NOT the same as unsetting
z=""
echo "${z-default}"    # (empty string, z IS set)
unset z
echo "${z-default}"    # default (z is NOT set)
```

---

## Demoting Environment Variables

```bash
# There is no direct "unexport" command
# Method 1: unset and re-create as shell variable
export x=5
unset x
x=5         # now it's just a shell variable

# Method 2: use declare to remove export flag
export x=5
declare +x x   # removes the export attribute
bash -c 'echo "$x"'   # (empty - not inherited)
echo "$x"              # 5 (still exists locally)
```

---

## Checking If a Variable Exists

```bash
# Method 1: use -v test (bash 4.2+)
x=5
if [[ -v x ]]; then
    echo "x is set"
fi

unset x
if [[ ! -v x ]]; then
    echo "x is not set"
fi

# Method 2: use parameter expansion
if [ -z "${x+set}" ]; then
    echo "x is not set"
else
    echo "x is set (possibly empty)"
fi
```

---

## Distinguishing Empty from Unset

```bash
# ${var+word} returns "word" if var is set (even if empty)
# ${var:+word} returns "word" only if var is set AND non-empty

x=""
echo "${x+SET}"     # SET (x exists, even though empty)
echo "${x:+SET}"    # (empty, because x is empty)

unset x
echo "${x+SET}"     # (empty, x does not exist)
echo "${x:+SET}"    # (empty, x does not exist)
```

---

## Read-Only Variables

```bash
# Make a variable read-only (constant)
readonly PI=3.14159
PI=3.0
# bash: PI: readonly variable

# Alternative syntax:
declare -r DB_HOST="localhost"

# You cannot unset a readonly variable
unset PI
# bash: unset: PI: cannot unset: readonly variable

# Readonly variables persist until the shell exits
```

---

## Variable Scope: Summary
![variable_scope_summary](svg/courses/languages/bash/bash-scripting/05_environment_variables/variable_scope_summary.svg)

---

## `declare` Command

```bash
# declare is used to set variable attributes
declare -i num=42    # integer
declare -r const=99  # readonly
declare -x env_var   # exported
declare -l lower     # lowercase
declare -u upper     # uppercase
declare -a arr       # indexed array
declare -A hash      # associative array

# View attributes of a variable
declare -p num
# declare -i num="42"

# Integer variables do arithmetic automatically
declare -i x
x=5+3
echo "$x"    # 8 (not "5+3")
```
