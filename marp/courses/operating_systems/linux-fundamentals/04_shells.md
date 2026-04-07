# UNIX Shells
## Understanding Shell Types and Usage

---

## Why Use a Shell

![why_use_a_shell](svg/courses/operating_systems/linux-fundamentals/04_shells/why_use_a_shell.svg)

The shell is your interface to the system:
- Command interpretation
- Script execution
- Process control
- Environment management

---

## Shell Families

![shell_families](svg/courses/operating_systems/linux-fundamentals/04_shells/shell_families.svg)

---

## Shell Variables: Bourne Family (sh/ksh/bash)

```bash
# Setting variables
name="John"
age=25

# Using variables
echo $name
echo ${name}

# Environment variables
export PATH=$PATH:/new/path
echo $PATH
```

![environment_variables](svg/courses/operating_systems/linux-fundamentals/04_shells/environment_variables.svg)

---

## Shell Variables: C Shell Family (csh/tcsh)

```bash
# Setting variables
set name = "John"
set age = 25

# Using variables
echo $name

# Environment variables
setenv PATH "$PATH:/new/path"
echo $PATH
```

Key differences:
- `set` for local variables
- `setenv` for environment variables
- Different syntax for assignment

---

## Command Line Substitution

## Bourne substitutions

```bash
# Backticks
files=`ls`

# Modern syntax
current_date=$(date)
files=$(ls)

# Arithmetic
result=$((5 + 3))
```

## C Shell Family

```bash
# Command substitution
set files = `ls`

# Arithmetic
@ result = (5 + 3)
```

---

## Glob Patterns

![glob_patterns](svg/courses/operating_systems/linux-fundamentals/04_shells/glob_patterns.svg)

Examples:

```bash
# List all text files
ls *.txt

# Match single character
ls file?.txt

# Match character range
ls [a-z]*.txt
```

---

## Input/Output Redirection

![input_output_redirection](svg/courses/operating_systems/linux-fundamentals/04_shells/input_output_redirection.svg)

Examples:

```bash
# Redirect input
sort < input.txt

# Redirect output
ls > output.txt

# Append output
echo "new line" >> file.txt

# Redirect error
command 2> error.log

# Redirect both
command > output.txt 2> error.log
```

---
## Aliases

## Bourne aliases

```bash
# Create alias
alias ll='ls -l'
alias gs='git status'

# List aliases
alias

# Remove alias
unalias ll
```

## C Shell aliases

```bash
# Create alias
alias ll 'ls -l'
alias gs 'git status'

# List aliases
alias

# Remove alias
unalias ll
```

---

## Pipes

![pipes](svg/courses/operating_systems/linux-fundamentals/04_shells/pipes.svg)

Examples:

```bash
# Count files
ls | wc -l

# Find specific processes
ps aux | grep nginx

# Sort and unique
cat file.txt | sort | uniq

# Complex pipeline
find . -type f | grep ".txt" | xargs wc -l
```

---

## Command History

## Bourne Family

```bash
# View history
history

# Search history
Ctrl+R

# Execute previous command
!!

# Execute specific command
!number
```

## C Shell history

```bash
# View history
history

# Previous command
!!

# Command number
!number
```

---

## Session Initialization

![session_initialization](svg/courses/operating_systems/linux-fundamentals/04_shells/session_initialization.svg)

Files for Bourne Family:

```bash
/etc/profile            # System-wide
~/.profile             # User login
~/.bashrc              # Interactive bash
~/.bash_profile        # Login specific
```

Files for C Shell Family:

```bash
/etc/csh.cshrc         # System-wide
~/.cshrc               # User specific
~/.login               # Login specific
```

---

## Practical Examples

```bash
# Pipeline processing
find . -type f -name "*.log" | \
  xargs grep "ERROR" | \
  sort | \
  uniq -c

# Command substitution
for file in $(ls *.txt); do
  echo "Processing $file"
  wc -l "$file"
done

# Error redirection
make 2> error.log > output.log
```

---

## Shell Features Comparison

| Feature | Bourne Family | C Shell Family |
|---------|--------------|----------------|
| Variables | name=value | set name = value |
| Environment | export name=value | setenv name value |
| Arithmetic | $((expr)) | @ result = (expr) |
| History | !command | !command |
| Aliases | alias name='cmd' | alias name 'cmd' |

---

## Practice Exercises

1. Variable Management

```bash
# Bourne family
name="test"
echo "Hello, $name"
export PATH="$PATH:/new/path"

# C shell family
set name = "test"
echo "Hello, $name"
setenv PATH "$PATH:/new/path"
```

1. Redirection and Pipes

```bash
# Create test data
ls -l > files.txt
sort < files.txt | uniq | wc -l
```
