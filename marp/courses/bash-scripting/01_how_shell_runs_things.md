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
```
Input: echo "hello world" > output.txt

Step 1: Tokenize    -> [echo] ["hello world"] [>] [output.txt]
Step 2: Identify    -> command: echo
                       args: "hello world"
                       redirect: > output.txt
Step 3: Expand      -> no expansions needed
Step 4: Execute     -> run /usr/bin/echo with arg
Step 5: Redirect    -> send stdout to output.txt
```
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
```
+------------------+-------------------+------------------+
|   Built-in       |   Function        |   External       |
|   Commands       |   Definitions     |   Programs       |
+------------------+-------------------+------------------+
| cd, echo, pwd,   | User-defined      | /usr/bin/ls      |
| export, read,    | functions in      | /usr/bin/grep     |
| test, [, [[      | the current       | /usr/bin/awk      |
|                  | shell session     |                  |
+------------------+-------------------+------------------+
| No fork needed   | No fork needed    | Fork + exec      |
+------------------+-------------------+------------------+
```
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

```
Shell Process (PID 100)
    |
    |-- fork() --> Child Process (PID 101)
    |                  |
    |                  |-- exec("/usr/bin/ls", ...)
    |                  |   (child becomes ls)
    |                  |
    |                  |-- ls runs and exits
    |
    |-- wait() --> collects exit status
    |
    |-- ready for next command
```
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
2. **Functions** defined in the current shell
3. **Built-in** commands
4. **Hash table** (cached paths of previously found commands)
5. **`PATH`** search (left to right)

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
