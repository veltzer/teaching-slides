# Bash Scripting Course
---
## Course Overview
- Duration: 3 days (~24 hours)
- Focus: deep understanding of `bash` scripting
- Emphasis on real-world patterns and common pitfalls
- Hands-on: lots of code examples and exercises
---
## Who Should Take This Course?
- System administrators automating tasks
- DevOps engineers writing deployment scripts
- Developers who work in `Linux` environments
- Anyone who wants to master the command line
---
## Prerequisites
- Basic familiarity with `Linux` or `macOS`
- Ability to open a terminal and type commands
- No prior scripting experience required
---
## What You Will Learn
- Day 1: Shell theory, variables, redirection, globbing
- Day 2: Writing scripts, syntax, pipes, I/O, multiprocessing
- Day 3: Functions, arrays, arithmetic, advanced topics
---
## Course Materials
- All examples tested on `bash` 5.x
- Compatible with most `Linux` distributions
- `macOS` users: install modern `bash` via `brew`
- All code available for download after the course
---
## What is a Shell?
- A program that interprets commands
- The interface between the user and the operating system kernel
- Takes text input, executes programs, returns output
- Both an interactive tool and a programming language

```
User --> Shell --> Kernel --> Hardware
```
---
## Why Do We Need a Shell?
- The kernel does not have a user interface
- Somebody must translate human intent into system calls
- The shell is that translator
- Without a shell, you would need to write C programs for every task
---
## Shell vs GUI
| Feature | Shell (CLI) | GUI |
|---------|------------|-----|
| Speed | Fast for experts | Slower, more clicks |
| Automation | Easily scriptable | Hard to automate |
| Remote access | Works over `SSH` | Needs X forwarding / VNC |
| Resource usage | Minimal | Heavy |
| Learning curve | Steep | Gentle |
| Reproducibility | Exact | Approximate |
---
## When to Use a Shell
- Automating repetitive tasks
- Managing remote servers via `SSH`
- Processing text files and log data
- Build systems and CI/CD pipelines
- System administration and monitoring
- Any task that needs to be reproducible
---
## When a GUI Wins
- Image and video editing
- Web browsing
- Complex IDE features (debugging, refactoring)
- Presentation and document creation
- Tasks where visual feedback is essential
---
## Shell Families

```
+-- Bourne family
|   +-- sh (1977, Bourne Shell)
|   +-- ksh (1983, Korn Shell)
|   +-- bash (1989, Bourne Again Shell)
|   +-- zsh (1990)
|
+-- C family
|   +-- csh (1978)
|   +-- tcsh (1981)
|
+-- Others
    +-- fish (2005)
    +-- PowerShell (2006)
```
---
## The Bourne Shell (`sh`)
- Written by Stephen Bourne at Bell Labs in 1977
- Shipped with Unix Version 7
- Introduced key concepts: variables, control flow, here documents
- Still the standard "minimal" shell on many systems
- `/bin/sh` is often a symlink to another shell today
---
## The Korn Shell (`ksh`)
- Written by David Korn at Bell Labs in 1983
- Backward compatible with `sh`
- Added: arrays, arithmetic, built-in string manipulation
- Was the dominant Unix shell in the 1980s-1990s
- Two major versions: `ksh88` and `ksh93`
---
## The Birth of `bash`
- "Bourne Again Shell" - a pun on "born again"
- Written by Brian Fox for the GNU project in 1989
- Goal: free replacement for `sh` with `ksh` features
- Now maintained by Chet Ramey
- Default shell on most `Linux` distributions
---
## `bash` Version History
| Version | Year | Key Features |
|---------|------|-------------|
| 1.0 | 1989 | Initial release |
| 2.0 | 1996 | Programmable completion |
| 3.0 | 2004 | Regex matching `=~` |
| 4.0 | 2009 | Associative arrays, `&>>` |
| 5.0 | 2019 | Various improvements |
| 5.2 | 2022 | Latest stable release |
---
## Check Your `bash` Version
```bash
# Method 1: the --version flag
bash --version

# Method 2: the BASH_VERSION variable
echo "$BASH_VERSION"

# Method 3: the BASH_VERSINFO array
echo "${BASH_VERSINFO[0]}.${BASH_VERSINFO[1]}"
```
---
## Why `bash`?
- Installed everywhere (every `Linux`, `macOS`, `WSL`)
- POSIX compatible (mostly)
- Enormous ecosystem of scripts and documentation
- Good balance between power and portability
- The "lingua franca" of shell scripting
---
## `bash` vs `zsh` vs `fish`
| Feature | `bash` | `zsh` | `fish` |
|---------|--------|-------|--------|
| Default on `Linux` | Yes | No | No |
| Default on `macOS` | No (was) | Yes | No |
| POSIX compatible | Yes | Mostly | No |
| Scripting ecosystem | Huge | Large | Small |
| Interactive features | Basic | Excellent | Excellent |
---
## The Takeaway
- Write scripts in `bash` for portability
- Use `zsh` or `fish` interactively if you prefer
- Always specify `#!/bin/bash` in scripts
- Never assume `sh` is `bash` — it often is not
