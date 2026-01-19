# Variables and Macros

## Overview
- Defining and using variables
- Automatic variables
- Variable assignment types
- Built-in variables
- Environment variables

---

## Why Variables?

## Benefits
- Avoid repetition (DRY principle)
- Easy to change settings in one place
- Cleaner, more maintainable Makefiles
- Enable configuration from command line

---

## Basic Variable Syntax

## Definition and Usage
```makefile
# Define a variable
CC = gcc
CFLAGS = -Wall -g

# Use a variable with $(...)
program: main.c
	$(CC) $(CFLAGS) -o program main.c
```

---

## Variable Reference Styles

## Two Equivalent Syntaxes
```makefile
CC = gcc

# Both are valid
program: main.c
	$(CC) -o program main.c
	${CC} -o program main.c
```

**Convention**: `$(VAR)` is more common in GNU Make

---

## Assignment Operators

## Four Types of Assignment
```makefile
# Simple assignment (evaluated immediately)
CC := gcc

# Recursive assignment (evaluated when used)
CC = gcc

# Conditional assignment (only if not set)
CC ?= gcc

# Append to variable
CFLAGS += -Wall
```

---

## Simple vs Recursive

## The Difference
```makefile
# Recursive (=) - evaluated each time used
A = $(B)
B = hello
# $(A) is "hello"

# Simple (:=) - evaluated once at definition
A := $(B)
B = hello
# $(A) is empty (B wasn't defined yet)
```

---

## Simple vs Recursive

## Practical Example
```makefile
# Recursive - can cause infinite loops
CFLAGS = $(CFLAGS) -Wall  # WRONG! Infinite recursion

# Simple - safe to self-reference
CFLAGS := $(CFLAGS) -Wall  # OK

# Best: use append
CFLAGS += -Wall  # OK
```

---

## Conditional Assignment

## Set If Not Defined
```makefile
# Only set if CC is not already defined
CC ?= gcc

# Useful for user overrides
# User can: make CC=clang
```

```bash
make CC=clang  # Uses clang
make           # Uses gcc (default)
```

---

## Common Variables

## Standard Conventions
```makefile
CC = gcc           # C compiler
CXX = g++          # C++ compiler
CFLAGS = -Wall -g  # C compiler flags
CXXFLAGS = -Wall   # C++ compiler flags
LDFLAGS = -L/lib   # Linker flags
LDLIBS = -lm       # Libraries to link
PREFIX = /usr/local
```

---

## Automatic Variables

## Built-in Special Variables
```makefile
$@    # Target name
$<    # First prerequisite
$^    # All prerequisites (no duplicates)
$+    # All prerequisites (with duplicates)
$?    # Prerequisites newer than target
$*    # Stem (matched by %)
$(@D) # Directory part of target
$(@F) # File part of target
```

---

## Automatic Variables Examples

## Using $@ and $<
```makefile
program: main.o utils.o
	$(CC) -o $@ $^
# Expands to: gcc -o program main.o utils.o

main.o: main.c
	$(CC) -c $< -o $@
# Expands to: gcc -c main.c -o main.o
```

---

## Automatic Variables Examples

## Using $^ and $?
```makefile
# $^ - all prerequisites
archive.tar: file1 file2 file3
	tar -cvf $@ $^

# $? - only newer prerequisites
backup: file1 file2 file3
	cp $? backup_dir/
	touch $@
```

---

## Pattern Rules with %

## The $* Variable
```makefile
%.o: %.c
	$(CC) -c $< -o $@
	@echo "Compiled $* from $<"

# When building main.o from main.c:
# $* = main
# $< = main.c
# $@ = main.o
```

---

## Built-in Variables

## Predefined by Make
```makefile
# Compiler defaults
$(CC)      # cc
$(CXX)     # g++
$(AR)      # ar
$(RM)      # rm -f

# Flag defaults (usually empty)
$(CFLAGS)
$(CXXFLAGS)
$(LDFLAGS)
```

---

## Environment Variables

## Automatic Import
```makefile
# Environment variables are available
# But Makefile definitions take precedence

program: main.c
	$(CC) -o program main.c  # Uses env CC if not defined
```

```bash
export CC=clang
make  # Will use clang (if CC not in Makefile)
```

---

## Override Directive

## Force Use of Environment
```makefile
# Override prevents command-line override
override CFLAGS += -Wall

# Without override:
# make CFLAGS="-O2" would replace
# With override:
# make CFLAGS="-O2" keeps -Wall too
```

---

## Multi-line Variables

## Using define
```makefile
define HELP_TEXT
Usage: make [target]
Targets:
  all     - Build everything
  clean   - Remove build files
  install - Install program
endef

help:
	@echo "$(HELP_TEXT)"
```

---

## Variable Substitution

## Pattern Replacement
```makefile
SRCS = main.c utils.c lib.c
OBJS = $(SRCS:.c=.o)
# OBJS = main.o utils.o lib.o

# Alternative syntax
OBJS = $(SRCS:%.c=%.o)
```

---

## Variable Functions

## Common Text Functions
```makefile
FILES = main.c utils.c lib.c

# Get directory/filename
$(dir src/main.c)      # src/
$(notdir src/main.c)   # main.c

# Pattern substitution
$(patsubst %.c,%.o,$(FILES))

# Word functions
$(words $(FILES))       # 3
$(firstword $(FILES))   # main.c
$(lastword $(FILES))    # lib.c
```

---

## Practical Example

## Complete Variable Usage
```makefile
CC := gcc
CFLAGS := -Wall -Wextra -g
LDFLAGS :=
LDLIBS := -lm

SRCS := main.c utils.c math.c
OBJS := $(SRCS:.c=.o)
TARGET := myprogram

$(TARGET): $(OBJS)
	$(CC) $(LDFLAGS) -o $@ $^ $(LDLIBS)

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@
```

---

## Summary

## Key Takeaways
- Use `:=` for simple assignment (evaluated once)
- Use `=` for recursive (evaluated when used)
- Use `?=` for defaults that users can override
- Use `+=` to append
- Master automatic variables: `$@`, `$<`, `$^`, `$*`
- Follow naming conventions for standard variables
