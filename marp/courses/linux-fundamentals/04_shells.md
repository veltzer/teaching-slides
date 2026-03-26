# UNIX Shells
## Understanding Shell Types and Usage

---

## Why Use a Shell

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="75" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="250" y="75" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="450" y="75" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="105" text-anchor="middle" font-size="12">Node 1</text>
  <text x="300" y="105" text-anchor="middle" font-size="12">Node 2</text>
  <text x="500" y="105" text-anchor="middle" font-size="12">Node 3</text>
  <line x1="150" y1="100" x2="250" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd0_03_shells)"/>
  <line x1="350" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd0_03_shells)"/>
  <defs>
    <marker id="arrowd0_03_shells" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

The shell is your interface to the system:
- Command interpretation
- Script execution
- Process control
- Environment management

---

## Shell Families

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="75" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="250" y="75" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="450" y="75" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="105" text-anchor="middle" font-size="12">Node 1</text>
  <text x="300" y="105" text-anchor="middle" font-size="12">Node 2</text>
  <text x="500" y="105" text-anchor="middle" font-size="12">Node 3</text>
  <line x1="150" y1="100" x2="250" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd1_03_shells)"/>
  <line x1="350" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd1_03_shells)"/>
  <defs>
    <marker id="arrowd1_03_shells" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

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

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="75" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="250" y="75" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="450" y="75" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="105" text-anchor="middle" font-size="12">Node 1</text>
  <text x="300" y="105" text-anchor="middle" font-size="12">Node 2</text>
  <text x="500" y="105" text-anchor="middle" font-size="12">Node 3</text>
  <line x1="150" y1="100" x2="250" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd2_03_shells)"/>
  <line x1="350" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd2_03_shells)"/>
  <defs>
    <marker id="arrowd2_03_shells" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

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

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="75" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="250" y="75" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="450" y="75" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="105" text-anchor="middle" font-size="12">Node 1</text>
  <text x="300" y="105" text-anchor="middle" font-size="12">Node 2</text>
  <text x="500" y="105" text-anchor="middle" font-size="12">Node 3</text>
  <line x1="150" y1="100" x2="250" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd3_03_shells)"/>
  <line x1="350" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd3_03_shells)"/>
  <defs>
    <marker id="arrowd3_03_shells" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

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

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="75" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="250" y="75" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="450" y="75" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="105" text-anchor="middle" font-size="12">Node 1</text>
  <text x="300" y="105" text-anchor="middle" font-size="12">Node 2</text>
  <text x="500" y="105" text-anchor="middle" font-size="12">Node 3</text>
  <line x1="150" y1="100" x2="250" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd4_03_shells)"/>
  <line x1="350" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd4_03_shells)"/>
  <defs>
    <marker id="arrowd4_03_shells" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

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

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="75" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="250" y="75" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="450" y="75" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="105" text-anchor="middle" font-size="12">Node 1</text>
  <text x="300" y="105" text-anchor="middle" font-size="12">Node 2</text>
  <text x="500" y="105" text-anchor="middle" font-size="12">Node 3</text>
  <line x1="150" y1="100" x2="250" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd5_03_shells)"/>
  <line x1="350" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd5_03_shells)"/>
  <defs>
    <marker id="arrowd5_03_shells" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

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

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="75" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="250" y="75" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="450" y="75" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="105" text-anchor="middle" font-size="12">Node 1</text>
  <text x="300" y="105" text-anchor="middle" font-size="12">Node 2</text>
  <text x="500" y="105" text-anchor="middle" font-size="12">Node 3</text>
  <line x1="150" y1="100" x2="250" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd6_03_shells)"/>
  <line x1="350" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd6_03_shells)"/>
  <defs>
    <marker id="arrowd6_03_shells" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

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
