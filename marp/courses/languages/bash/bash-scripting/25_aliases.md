# Aliases

---
## Alias Expansion Flow

![alias_expansion](svg/courses/languages/bash/bash-scripting/25_aliases/alias_expansion.svg)

---
## What is an Alias?
- A shortcut for a command or command sequence
- Text substitution before the shell parses the line
- Only work in interactive shells (by default)
- Defined in `~/.bashrc` or `~/.bash_aliases`

```bash
# Define an alias
alias ll='ls -la'
alias gs='git status'
alias ..='cd ..'

# Now typing ll expands to ls -la
ll
# equivalent to: ls -la
```

---
## Creating Aliases

```bash
# Simple command shortcuts
alias cls='clear'
alias h='history'
alias q='exit'
alias mkdir='mkdir -p'     # always create parents
alias rm='rm -i'           # always confirm
alias cp='cp -i'           # always confirm
alias mv='mv -i'           # always confirm

# Multi-command aliases (use semicolons)
alias update='sudo apt update && sudo apt upgrade -y'
alias myip='curl -s ifconfig.me && echo'

# Aliases with pipes
alias topcpu='ps aux --sort=-%cpu | head -10'
alias topmem='ps aux --sort=-%mem | head -10'
```

---
## Viewing and Removing Aliases

```bash
# List all defined aliases
alias

# Show a specific alias
alias ll
# alias ll='ls -la'

# Remove an alias
unalias ll

# Remove ALL aliases
unalias -a

# Temporarily bypass an alias
\ls        # runs /usr/bin/ls, not the alias
command ls  # also bypasses the alias
/usr/bin/ls # explicit path bypasses everything
```

---
## Aliases vs Functions

```bash
# Aliases cannot take arguments in the middle
alias greet='echo Hello'
greet World
# Hello World (args are appended at the end)

# But you can't put args in the middle:
alias backup='cp $1 $1.bak'    # DOES NOT WORK!
# $1 is not an alias parameter

# Use a function instead:
backup() {
    cp "$1" "$1.bak"
}
backup myfile.txt    # copies myfile.txt to myfile.txt.bak

# Rule of thumb:
# - Simple shortcuts: use aliases
# - Anything with logic or arguments: use functions
```

---
## Aliases in Scripts

```bash
# By default, aliases are NOT expanded in scripts
#!/bin/bash
alias ll='ls -la'
ll    # bash: ll: command not found

# To enable alias expansion in scripts:
#!/bin/bash
shopt -s expand_aliases
alias ll='ls -la'
ll    # now works

# But DON'T do this!
# Functions are the right tool for scripts
```

---
## Common Useful Aliases

```bash
# Navigation
alias ..='cd ..'
alias ...='cd ../..'
alias ....='cd ../../..'

# Git
alias ga='git add'
alias gc='git commit'
alias gp='git push'
alias gl='git log --oneline --graph --decorate'
alias gd='git diff'
alias gco='git checkout'

# Safety
alias rm='rm -I'
alias chmod='chmod --preserve-root'
alias chown='chown --preserve-root'
```

---
## Making Aliases Permanent

```bash
# Add to ~/.bashrc or ~/.bash_aliases

# In ~/.bashrc:
if [ -f ~/.bash_aliases ]; then
    . ~/.bash_aliases
fi

# In ~/.bash_aliases:
alias ll='ls -la'
alias gs='git status'
# ... etc ...

# After editing, reload:
source ~/.bashrc
# or start a new terminal
```

---
## Day 3 & Course Summary
- Functions: use `local`, return codes vs stdout, namerefs
- Variable types: strings (default), integers, arrays, assoc. arrays
- Arithmetic: `$(( ))` for integers, `bc`/`awk` for floats
- Indexed arrays: ordered, zero-based, sparse-capable
- Associative arrays: key-value pairs, must declare with `-A`
- Timing: `time`, `SECONDS`, `date +%s%N`
- OOP: possible but not recommended for production
- Testing: write tests, use BATS for serious projects
- Aliases: interactive shortcuts, use functions in scripts

---
## Best Practices: Final Checklist
```misc
Scripts:
  [x] Always use #!/bin/bash or #!/usr/bin/env bash
  [x] Always use set -euo pipefail
  [x] Always double-quote your variables
  [x] Always use [[ ]] instead of [ ]
  [x] Always declare function variables as local
  [x] Always use $(cmd) instead of backticks
  [x] Always handle errors explicitly
  [x] Always clean up temp files (trap EXIT)

Code Quality:
  [x] Run shellcheck on all scripts
  [x] Write tests for complex functions
  [x] Use meaningful variable and function names
  [x] Comment the "why", not the "what"
  [x] Keep functions small and focused
```

---
## Recommended Reading
- `man bash` — the definitive reference
- "Advanced Bash-Scripting Guide" (tldp.org)
- `shellcheck` wiki — explains every warning
- Wooledge BashFAQ — common questions answered correctly
- Wooledge BashPitfalls — mistakes to avoid
- Google Shell Style Guide — industry conventions

---
## Thank You!
- Practice daily: automate one task per week
- Read other people's scripts (in `/etc/init.d/`, GitHub)
- Start simple, add complexity only when needed
- When `bash` gets too complex, switch to `Python`
- Remember: the goal is automation, not cleverness
