# UNIX Shells
## Understanding Shell Types and Usage

---

## Why Use a Shell

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="10" width="130" height="40" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="115" y="35" text-anchor="middle" font-size="11" font-weight="bold">User Input</text>
  <rect x="235" y="10" width="130" height="40" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="35" text-anchor="middle" font-size="11" font-weight="bold">Shell (bash)</text>
  <rect x="420" y="10" width="130" height="40" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="485" y="35" text-anchor="middle" font-size="11" font-weight="bold">Kernel</text>
  <line x1="180" y1="30" x2="235" y2="30" stroke="#333" stroke-width="2" marker-end="url(#arr_sh0)"/>
  <line x1="365" y1="30" x2="420" y2="30" stroke="#333" stroke-width="2" marker-end="url(#arr_sh0)"/>
  <rect x="50" y="65" width="500" height="50" fill="#fff3e0" stroke="#333" stroke-width="1" rx="3"/>
  <text x="300" y="82" text-anchor="middle" font-size="10" font-weight="bold">Shell Role: Command Interpreter + Scripting Language</text>
  <text x="300" y="102" text-anchor="middle" font-size="10">Reads input -> Parses -> Expands (glob,var) -> Executes (fork/exec)</text>
  <rect x="50" y="130" width="120" height="55" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="3"/>
  <text x="110" y="150" text-anchor="middle" font-size="10">Command</text>
  <text x="110" y="168" text-anchor="middle" font-size="10">interpretation</text>
  <rect x="190" y="130" width="120" height="55" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="3"/>
  <text x="250" y="150" text-anchor="middle" font-size="10">Script</text>
  <text x="250" y="168" text-anchor="middle" font-size="10">execution</text>
  <rect x="330" y="130" width="120" height="55" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="3"/>
  <text x="390" y="150" text-anchor="middle" font-size="10">Process</text>
  <text x="390" y="168" text-anchor="middle" font-size="10">control</text>
  <rect x="465" y="130" width="100" height="55" fill="#ffebee" stroke="#333" stroke-width="1" rx="3"/>
  <text x="515" y="150" text-anchor="middle" font-size="10">Environment</text>
  <text x="515" y="168" text-anchor="middle" font-size="10">management</text>
  <defs>
    <marker id="arr_sh0" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
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
  <text x="300" y="18" text-anchor="middle" font-size="12" font-weight="bold">Shell Family Tree</text>
  <rect x="225" y="25" width="150" height="30" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="45" text-anchor="middle" font-size="10">Thompson Shell (1971)</text>
  <line x1="240" y1="55" x2="130" y2="75" stroke="#333" stroke-width="1"/>
  <line x1="360" y1="55" x2="470" y2="75" stroke="#333" stroke-width="1"/>
  <rect x="50" y="75" width="160" height="30" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="130" y="95" text-anchor="middle" font-size="10" font-weight="bold">Bourne sh (1977)</text>
  <rect x="390" y="75" width="160" height="30" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="470" y="95" text-anchor="middle" font-size="10" font-weight="bold">C Shell csh (1978)</text>
  <line x1="80" y1="105" x2="80" y2="125" stroke="#333" stroke-width="1"/>
  <line x1="130" y1="105" x2="200" y2="125" stroke="#333" stroke-width="1"/>
  <line x1="180" y1="105" x2="330" y2="125" stroke="#333" stroke-width="1"/>
  <line x1="470" y1="105" x2="470" y2="125" stroke="#333" stroke-width="1"/>
  <rect x="30" y="125" width="100" height="28" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="3"/>
  <text x="80" y="144" text-anchor="middle" font-size="10">ksh (1983)</text>
  <rect x="150" y="125" width="100" height="28" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="3"/>
  <text x="200" y="144" text-anchor="middle" font-size="10" font-weight="bold">bash (1989)</text>
  <rect x="280" y="125" width="100" height="28" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="3"/>
  <text x="330" y="144" text-anchor="middle" font-size="10">zsh (1990)</text>
  <rect x="420" y="125" width="100" height="28" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="3"/>
  <text x="470" y="144" text-anchor="middle" font-size="10">tcsh</text>
  <rect x="50" y="165" width="500" height="25" fill="#ffebee" stroke="#333" stroke-width="1" rx="3"/>
  <text x="300" y="182" text-anchor="middle" font-size="10">Default shell set in /etc/passwd  |  Change with: chsh -s /bin/zsh</text>
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
  <text x="300" y="18" text-anchor="middle" font-size="11" font-weight="bold">Variable Scope: Local vs Environment</text>
  <rect x="50" y="30" width="240" height="70" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="170" y="50" text-anchor="middle" font-size="10" font-weight="bold">Shell (local) Variable</text>
  <text x="170" y="68" text-anchor="middle" font-family="monospace" font-size="10">name="John"</text>
  <text x="170" y="86" text-anchor="middle" font-size="10" fill="#666">Only in current shell</text>
  <rect x="310" y="30" width="240" height="70" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="430" y="50" text-anchor="middle" font-size="10" font-weight="bold">Environment Variable</text>
  <text x="430" y="68" text-anchor="middle" font-family="monospace" font-size="10">export PATH=...</text>
  <text x="430" y="86" text-anchor="middle" font-size="10" fill="#666">Inherited by child processes</text>
  <rect x="50" y="115" width="500" height="30" fill="#fff3e0" stroke="#333" stroke-width="1" rx="3"/>
  <text x="300" y="135" text-anchor="middle" font-size="10">Parent Shell --fork/exec--> Child Shell (inherits exported vars only)</text>
  <rect x="50" y="155" width="500" height="35" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="3"/>
  <text x="300" y="170" text-anchor="middle" font-size="10" font-weight="bold">Key env vars: PATH, HOME, USER, SHELL, LANG, PS1, TERM</text>
  <text x="300" y="185" text-anchor="middle" font-size="10" fill="#666">View all: env | sort   or   printenv</text>
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
  <text x="300" y="18" text-anchor="middle" font-size="11" font-weight="bold">Glob Pattern Expansion (by the shell, not the command)</text>
  <rect x="50" y="30" width="120" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="110" y="48" text-anchor="middle" font-size="11" font-weight="bold">*</text>
  <text x="110" y="68" text-anchor="middle" font-size="10">any string</text>
  <rect x="190" y="30" width="120" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="250" y="48" text-anchor="middle" font-size="11" font-weight="bold">?</text>
  <text x="250" y="68" text-anchor="middle" font-size="10">single char</text>
  <rect x="330" y="30" width="120" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="390" y="48" text-anchor="middle" font-size="11" font-weight="bold">[abc]</text>
  <text x="390" y="68" text-anchor="middle" font-size="10">char class</text>
  <rect x="470" y="30" width="90" height="50" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="515" y="48" text-anchor="middle" font-size="11" font-weight="bold">{a,b}</text>
  <text x="515" y="68" text-anchor="middle" font-size="10">brace exp</text>
  <rect x="50" y="95" width="500" height="40" fill="#ffebee" stroke="#333" stroke-width="1" rx="3"/>
  <text x="300" y="108" text-anchor="middle" font-family="monospace" font-size="10">ls *.txt  ->  ls file1.txt file2.txt notes.txt</text>
  <text x="300" y="125" text-anchor="middle" font-size="10" fill="#666">Shell expands globs BEFORE passing to command</text>
  <rect x="50" y="150" width="500" height="40" fill="#fff3e0" stroke="#333" stroke-width="1" rx="3"/>
  <text x="300" y="165" text-anchor="middle" font-size="10">Extended: **/ (recursive), !(pat) (negate), +(pat) (one or more)</text>
  <text x="300" y="182" text-anchor="middle" font-size="10" fill="#666">Enable: shopt -s extglob globstar</text>
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
  <text x="300" y="18" text-anchor="middle" font-size="11" font-weight="bold">I/O Redirection: File Descriptors 0, 1, 2</text>
  <rect x="50" y="30" width="100" height="60" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="50" text-anchor="middle" font-size="10" font-weight="bold">stdin (0)</text>
  <text x="100" y="70" text-anchor="middle" font-size="10">keyboard</text>
  <text x="100" y="82" text-anchor="middle" font-size="10" fill="#666">&lt; file</text>
  <rect x="250" y="30" width="100" height="60" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="50" text-anchor="middle" font-size="10" font-weight="bold">stdout (1)</text>
  <text x="300" y="70" text-anchor="middle" font-size="10">terminal</text>
  <text x="300" y="82" text-anchor="middle" font-size="10" fill="#666">&gt; file</text>
  <rect x="450" y="30" width="100" height="60" fill="#ffebee" stroke="#333" stroke-width="2" rx="5"/>
  <text x="500" y="50" text-anchor="middle" font-size="10" font-weight="bold">stderr (2)</text>
  <text x="500" y="70" text-anchor="middle" font-size="10">terminal</text>
  <text x="500" y="82" text-anchor="middle" font-size="10" fill="#666">2&gt; file</text>
  <line x1="150" y1="60" x2="250" y2="60" stroke="#333" stroke-width="2" marker-end="url(#arr_io)"/>
  <rect x="170" y="48" width="60" height="18" fill="#fff3e0" stroke="none"/>
  <text x="200" y="61" text-anchor="middle" font-size="10">Process</text>
  <rect x="50" y="105" width="500" height="35" fill="#fff3e0" stroke="#333" stroke-width="1" rx="3"/>
  <text x="300" y="118" text-anchor="middle" font-family="monospace" font-size="10">cmd &gt; out.txt 2&gt; err.txt     cmd &gt;&gt; append.txt</text>
  <text x="300" y="133" text-anchor="middle" font-family="monospace" font-size="10">cmd &gt; file 2&gt;&amp;1              cmd &amp;&gt; both.txt</text>
  <rect x="50" y="150" width="500" height="40" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="3"/>
  <text x="300" y="165" text-anchor="middle" font-size="10" font-weight="bold">Here document:  cmd &lt;&lt; EOF ... EOF</text>
  <text x="300" y="182" text-anchor="middle" font-size="10">Here string:  cmd &lt;&lt;&lt; "text"   |   /dev/null: discard output</text>
  <defs>
    <marker id="arr_io" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
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
  <text x="300" y="18" text-anchor="middle" font-size="11" font-weight="bold">Pipeline: stdout of one -> stdin of next</text>
  <rect x="30" y="30" width="110" height="45" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="85" y="48" text-anchor="middle" font-size="10" font-weight="bold">ps aux</text>
  <text x="85" y="65" text-anchor="middle" font-size="9" fill="#666">stdout</text>
  <rect x="175" y="38" width="30" height="28" fill="#fff3e0" stroke="#333" stroke-width="2" rx="3"/>
  <text x="190" y="57" text-anchor="middle" font-size="13" font-weight="bold">|</text>
  <rect x="240" y="30" width="110" height="45" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="295" y="48" text-anchor="middle" font-size="10" font-weight="bold">grep nginx</text>
  <text x="295" y="65" text-anchor="middle" font-size="9" fill="#666">filter</text>
  <rect x="385" y="38" width="30" height="28" fill="#fff3e0" stroke="#333" stroke-width="2" rx="3"/>
  <text x="400" y="57" text-anchor="middle" font-size="13" font-weight="bold">|</text>
  <rect x="450" y="30" width="110" height="45" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="505" y="48" text-anchor="middle" font-size="10" font-weight="bold">wc -l</text>
  <text x="505" y="65" text-anchor="middle" font-size="9" fill="#666">count</text>
  <line x1="140" y1="52" x2="175" y2="52" stroke="#333" stroke-width="2" marker-end="url(#arr_pipe)"/>
  <line x1="350" y1="52" x2="385" y2="52" stroke="#333" stroke-width="2" marker-end="url(#arr_pipe)"/>
  <rect x="50" y="90" width="500" height="45" fill="#ffebee" stroke="#333" stroke-width="1" rx="3"/>
  <text x="300" y="107" text-anchor="middle" font-size="10" font-weight="bold">All processes in pipeline run concurrently</text>
  <text x="300" y="125" text-anchor="middle" font-size="10">Kernel buffers data between them (4KB pipe buffer)</text>
  <rect x="50" y="145" width="500" height="45" fill="#fff3e0" stroke="#333" stroke-width="1" rx="3"/>
  <text x="300" y="162" text-anchor="middle" font-size="10">tee: split output    |   xargs: build command from stdin</text>
  <text x="300" y="180" text-anchor="middle" font-family="monospace" font-size="10">cmd | tee log.txt | next_cmd    find . | xargs grep pat</text>
  <defs>
    <marker id="arr_pipe" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
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
  <text x="300" y="18" text-anchor="middle" font-size="11" font-weight="bold">Bash Startup File Load Order</text>
  <rect x="50" y="28" width="160" height="35" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="130" y="50" text-anchor="middle" font-size="10">/etc/profile</text>
  <line x1="210" y1="45" x2="235" y2="45" stroke="#333" stroke-width="1" marker-end="url(#arr_init)"/>
  <rect x="235" y="28" width="160" height="35" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="5"/>
  <text x="315" y="50" text-anchor="middle" font-size="10">~/.bash_profile</text>
  <line x1="395" y1="45" x2="420" y2="45" stroke="#333" stroke-width="1" marker-end="url(#arr_init)"/>
  <rect x="420" y="28" width="130" height="35" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="5"/>
  <text x="485" y="50" text-anchor="middle" font-size="10">~/.bashrc</text>
  <rect x="50" y="78" width="250" height="35" fill="#fff3e0" stroke="#333" stroke-width="1" rx="3"/>
  <text x="175" y="95" text-anchor="middle" font-size="10" font-weight="bold">Login Shell (ssh, console)</text>
  <text x="175" y="108" text-anchor="middle" font-size="9">/etc/profile -> ~/.bash_profile</text>
  <rect x="320" y="78" width="230" height="35" fill="#ffebee" stroke="#333" stroke-width="1" rx="3"/>
  <text x="435" y="95" text-anchor="middle" font-size="10" font-weight="bold">Interactive (terminal)</text>
  <text x="435" y="108" text-anchor="middle" font-size="9">~/.bashrc only</text>
  <rect x="50" y="125" width="500" height="60" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="3"/>
  <text x="300" y="142" text-anchor="middle" font-size="10" font-weight="bold">Common Pattern: ~/.bash_profile sources ~/.bashrc</text>
  <text x="300" y="160" text-anchor="middle" font-family="monospace" font-size="10">[ -f ~/.bashrc ] && source ~/.bashrc</text>
  <text x="300" y="178" text-anchor="middle" font-size="10" fill="#666">Logout: ~/.bash_logout  |  Non-interactive: $BASH_ENV</text>
  <defs>
    <marker id="arr_init" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
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
