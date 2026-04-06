# How the Shell Runs Things
---
## What Happens When You Type a Command?
- You type `ls -la /tmp` and press Enter
- The shell must figure out:
  1. What program to run
  2. Where that program lives
  3. How to pass arguments to it
  4. What to do with the result
---
## Command Line Parsing: Step by Step

<svg xmlns="http://www.w3.org/2000/svg" width="640" height="320">
  <!-- Input bar -->
  <rect x="10" y="10" width="620" height="38" rx="4" fill="#333" stroke="#333" stroke-width="1.5"/>
  <text x="20" y="34" font-family="monospace" font-size="13" fill="#a5d6a7">Input: echo "hello world" &gt; output.txt</text>

  <!-- Step boxes -->
  <rect x="10" y="60" width="620" height="45" rx="4" fill="#f0f4f8" stroke="#555" stroke-width="1.5"/>
  <text x="20" y="78" font-family="monospace" font-size="12" font-weight="bold" fill="#1565c0">Step 1: Tokenize</text>
  <text x="160" y="78" font-family="monospace" font-size="12" fill="#222">→  [echo]  ["hello world"]  [&gt;]  [output.txt]</text>

  <rect x="10" y="115" width="620" height="65" rx="4" fill="#f0f4f8" stroke="#555" stroke-width="1.5"/>
  <text x="20" y="133" font-family="monospace" font-size="12" font-weight="bold" fill="#1565c0">Step 2: Identify</text>
  <text x="160" y="133" font-family="monospace" font-size="12" fill="#222">→  command:  echo</text>
  <text x="160" y="151" font-family="monospace" font-size="12" fill="#222">   args:     "hello world"</text>
  <text x="160" y="169" font-family="monospace" font-size="12" fill="#222">   redirect: &gt; output.txt</text>

  <rect x="10" y="190" width="620" height="45" rx="4" fill="#f0f4f8" stroke="#555" stroke-width="1.5"/>
  <text x="20" y="208" font-family="monospace" font-size="12" font-weight="bold" fill="#1565c0">Step 3: Expand</text>
  <text x="160" y="208" font-family="monospace" font-size="12" fill="#555">→  no expansions needed</text>

  <rect x="10" y="245" width="620" height="45" rx="4" fill="#e8f5e9" stroke="#2e7d32" stroke-width="1.5"/>
  <text x="20" y="263" font-family="monospace" font-size="12" font-weight="bold" fill="#1565c0">Step 4: Execute</text>
  <text x="160" y="263" font-family="monospace" font-size="12" fill="#222">→  run /usr/bin/echo with arg</text>

  <rect x="10" y="300" width="620" height="45" rx="4" fill="#e8f5e9" stroke="#2e7d32" stroke-width="1.5"/>
  <text x="20" y="318" font-family="monospace" font-size="12" font-weight="bold" fill="#1565c0">Step 5: Redirect</text>
  <text x="160" y="318" font-family="monospace" font-size="12" fill="#222">→  send stdout to output.txt</text>
</svg>
---
## The Full Parsing Order
1. Brace expansion: `{a,b,c}`
2. Tilde expansion: `~`
3. Parameter/variable expansion: `$VAR`
4. Command substitution: `$(cmd)`
5. Arithmetic expansion: `$((1+2))`
6. Word splitting
7. Pathname expansion (globbing): `*.txt`
8. Quote removal
---
## Why the Order Matters

```bash
# This works because variable expansion happens
# BEFORE word splitting
files="file1 file2 file3"
echo $files
# echo sees three separate arguments

# This does NOT glob because quotes prevent
# pathname expansion
echo "*.txt"
# Prints literally: *.txt
```
---
## Finding Commands: Three Types

| Built-in Commands | Function Definitions | External Programs |
|-------------------|----------------------|-------------------|
| cd, echo, pwd, export, read, test, [, [[ | User-defined functions in the current shell session | /usr/bin/ls, /usr/bin/grep, /usr/bin/awk |
| No fork needed | No fork needed | Fork + exec |
---
## The `type` Command

```bash
# Find out what kind of command something is
type cd
# cd is a shell builtin

type ls
# ls is /usr/bin/ls

type type
# type is a shell builtin

# Show ALL definitions (aliases, functions, builtins)
type -a echo
# echo is a shell builtin
# echo is /usr/bin/echo
```
---
## Built-in Commands
- Executed inside the shell process itself
- No new process is created
- Can modify shell state (variables, directory, etc.)
- Examples: `cd`, `export`, `source`, `read`, `echo`, `printf`

```bash
# cd MUST be a built-in
# If it were external, it would change the directory
# of the child process, not the shell itself
cd /tmp  # changes THIS shell's directory
```
---
## Why `cd` Cannot Be External

```bash
# Imagine cd as an external program:
# 1. Shell forks a child process
# 2. Child calls chdir("/tmp")
# 3. Child's working directory changes
# 4. Child exits
# 5. Shell's working directory is UNCHANGED

# This is why cd is a built-in:
# It must run inside the shell process itself
```
---
## External Commands and `PATH`
- External commands are programs on disk
- The shell must find them before executing
- `PATH` is the search path: a colon-separated list of directories

```bash
echo "$PATH"
# /usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin

# The shell searches directories LEFT to RIGHT
# First match wins
```
---
## How `PATH` Search Works

```bash
# When you type "python3":
# 1. Is it a built-in? No.
# 2. Is it a function? No.
# 3. Search PATH:
#    /usr/local/bin/python3 ? YES -> run it
#    (stop searching)

# If not found anywhere:
python3000
# bash: python3000: command not found
```
---
## Viewing and Modifying `PATH`

```bash
# View current PATH (one directory per line)
echo "$PATH" | tr ':' '\n'

# Add a directory to the BEGINNING (highest priority)
export PATH="/my/custom/bin:$PATH"

# Add a directory to the END (lowest priority)
export PATH="$PATH:/my/custom/bin"

# WARNING: never set PATH without including the old value
export PATH="/only/this"  # DANGEROUS! Most commands vanish
```
---
## The `which` and `command -v` Commands

```bash
# Find where a command lives
which python3
# /usr/bin/python3

# Preferred in scripts (POSIX):
command -v python3
# /usr/bin/python3

# which can be fooled by aliases; command -v cannot
alias ls='ls --color=auto'
which ls     # may show the alias
command -v ls  # /usr/bin/ls
```
---
## `fork` and `exec`: How External Commands Run

<svg xmlns="http://www.w3.org/2000/svg" width="520" height="310">
  <defs>
    <marker id="arr" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
      <path d="M0,0 L0,6 L8,3 z" fill="#555"/>
    </marker>
  </defs>
  <!-- Shell Process -->
  <rect x="10" y="10" width="220" height="50" rx="4" fill="#333" stroke="#333" stroke-width="1.5"/>
  <text x="120" y="30" font-family="monospace" font-size="13" fill="#fff" text-anchor="middle">Shell Process</text>
  <text x="120" y="50" font-family="monospace" font-size="12" fill="#aaa" text-anchor="middle">(PID 100)</text>

  <!-- vertical down to fork -->
  <line x1="120" y1="60" x2="120" y2="90" stroke="#555" stroke-width="1.5"/>
  <!-- fork label on left branch -->
  <line x1="120" y1="90" x2="320" y2="90" stroke="#555" stroke-width="1.5"/>
  <line x1="320" y1="90" x2="320" y2="120" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <text x="185" y="84" font-family="monospace" font-size="12" fill="#333">fork()</text>
  <!-- continue shell left branch -->
  <line x1="120" y1="90" x2="120" y2="240" stroke="#555" stroke-width="1.5"/>

  <!-- Child Process -->
  <rect x="250" y="120" width="260" height="50" rx="4" fill="#e3f2fd" stroke="#333" stroke-width="1.5"/>
  <text x="380" y="140" font-family="monospace" font-size="13" fill="#222" text-anchor="middle">Child Process</text>
  <text x="380" y="160" font-family="monospace" font-size="12" fill="#555" text-anchor="middle">(PID 101)</text>

  <line x1="320" y1="170" x2="320" y2="195" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <rect x="250" y="195" width="260" height="44" rx="4" fill="#fff3e0" stroke="#555" stroke-width="1.5"/>
  <text x="380" y="215" font-family="monospace" font-size="12" fill="#222" text-anchor="middle">exec("/usr/bin/ls", ...)</text>
  <text x="380" y="231" font-family="sans-serif" font-size="11" fill="#555" text-anchor="middle">(child becomes ls)</text>

  <line x1="320" y1="239" x2="320" y2="260" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <rect x="250" y="260" width="260" height="36" rx="4" fill="#e8f5e9" stroke="#2e7d32" stroke-width="1.5"/>
  <text x="380" y="283" font-family="monospace" font-size="12" fill="#222" text-anchor="middle">ls runs and exits</text>

  <!-- Shell wait() and ready -->
  <rect x="10" y="240" width="220" height="36" rx="4" fill="#f0f4f8" stroke="#555" stroke-width="1.5"/>
  <text x="120" y="263" font-family="monospace" font-size="12" fill="#222" text-anchor="middle">wait() → collect exit status</text>

  <line x1="120" y1="276" x2="120" y2="296" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <rect x="10" y="296" width="220" height="36" rx="4" fill="#e8f5e9" stroke="#2e7d32" stroke-width="1.5"/>
  <text x="120" y="319" font-family="monospace" font-size="12" fill="#222" text-anchor="middle">ready for next command</text>
</svg>
---
## Watching `fork`/`exec` in Action

```bash
# Use strace to see the system calls
strace -f -e trace=clone,execve bash -c 'ls /tmp' 2>&1 | head -20

# You will see:
# execve("/bin/bash", ["bash", "-c", "ls /tmp"], ...)
# clone(...) = 12345           <-- fork
# [pid 12345] execve("/usr/bin/ls", ["ls", "/tmp"], ...)
```
---
## The Search Order
When you type a command name, `bash` searches in this order:

1. **Aliases** (interactive shells only)
1. **Functions** defined in the current shell
1. **Built-in** commands
1. **Hash table** (cached paths of previously found commands)
1. **`PATH`** search (left to right)

```bash
# See the hash table
hash
# /usr/bin/ls -> ls
# /usr/bin/cat -> cat
```

---
## Bypassing the Search Order

```bash
# Run the built-in version explicitly
builtin echo "hello"

# Run the external version explicitly
command echo "hello"

# Run by absolute path (skip all searching)
/usr/bin/echo "hello"

# Clear the hash table
hash -r
```
