---
tags:
  - tools:make
  - languages:c
  - practices:build-systems
  - infrastructure:linux
level: intermediate
category: build-system
audience:
  - audiences:developers

---
# Advanced Features

---

## GNU Make Advanced Features

![make_advanced_features](svg/courses/build_systems/make/04_advanced_features/make_advanced_features.svg)

---

## Overview

- Pattern rules and implicit rules
- Functions for string manipulation
- Conditionals
- Include directive
- Parallel builds

---

## Pattern Rules

```makefile
# Pattern rule for C files
%.o: %.c
    $(CC) $(CFLAGS) -c $< -o $@

# Pattern rule for C++ files
%.o: %.cpp
    $(CXX) $(CXXFLAGS) -c $< -o $@
```

The `%` matches any non-empty string.

---

## Pattern Rules - Multiple Patterns

```makefile
# Generate .d dependency files
%.d: %.c
    $(CC) -MM $< > $@

# Build objects from assembly
%.o: %.s
    $(AS) $(ASFLAGS) -o $@ $<

# Generate header from template
%.h: %.h.in
    ./configure.sh $< > $@
```

---

## Implicit Rules

- Make has built-in rules for common tasks:

```makefile
# These are implicit (you don't need to write them)
# %.o: %.c
#     $(CC) $(CFLAGS) $(CPPFLAGS) -c $<

# %.o: %.cpp
#     $(CXX) $(CXXFLAGS) $(CPPFLAGS) -c $<
```

```bash
# View implicit rules
make -p | grep -A2 "%.o"
```

---

## Disabling Implicit Rules

```makefile
# Cancel implicit rule with empty recipe
%.o: %.c

# Or disable all implicit rules
MAKEFLAGS += --no-builtin-rules
.SUFFIXES:
```

---

## Static Pattern Rules

```makefile
OBJECTS = foo.o bar.o baz.o

# Only applies to listed targets
$(OBJECTS): %.o: %.c
    $(CC) -c $(CFLAGS) $< -o $@

# Different rule for test objects
TEST_OBJS = test_foo.o test_bar.o
$(TEST_OBJS): %.o: %.c
    $(CC) -c $(CFLAGS) -DTEST $< -o $@
```

---

## String Functions

```makefile
FILES := foo.c bar.c baz.c

# Substitution
$(subst .c,.o,$(FILES))     # foo.o bar.o baz.o
$(patsubst %.c,%.o,$(FILES)) # same result

# Filtering
$(filter %.c,$(FILES))       # foo.c bar.c baz.c
$(filter-out %.c,$(FILES))   # (empty)
```

---

## More String Functions

```makefile
FILES := src/foo.c src/bar.c

# Path manipulation
$(dir $(FILES))        # src/ src/
$(notdir $(FILES))     # foo.c bar.c
$(basename $(FILES))   # src/foo src/bar
$(suffix $(FILES))     # .c .c
$(addprefix build/,$(notdir $(FILES)))
# build/foo.c build/bar.c
```

---

## Wildcard Function

```makefile
# Find all C files in current directory
SRCS := $(wildcard *.c)

# Find recursively (GNU Make 4.0+)
SRCS := $(wildcard src/*.c) $(wildcard src/**/*.c)

# Using shell for recursive
SRCS := $(shell find src -name '*.c')
```

---

## Shell Function

```makefile
# Get current date
DATE := $(shell date +%Y%m%d)

# Get git commit
GIT_HASH := $(shell git rev-parse --short HEAD)

# List files
FILES := $(shell find . -name '*.c')

VERSION := $(shell cat VERSION)
```

---

## Conditionals

```makefile
DEBUG ?= 0

ifeq ($(DEBUG),1)
    CFLAGS += -g -DDEBUG
else
    CFLAGS += -O2 -DNDEBUG
endif

program: main.c
    $(CC) $(CFLAGS) -o $@ $<
```

---

## Conditional Syntax

```makefile
# Check equality
ifeq ($(VAR),value)
endif

# Check inequality
ifneq ($(VAR),value)
endif

# Check if defined
ifdef VAR
endif

# Check if not defined
ifndef VAR
endif
```

---

## Conditional Example - Platform-Specific Builds

```makefile
UNAME := $(shell uname)

ifeq ($(UNAME),Linux)
    LDLIBS += -lrt
endif

ifeq ($(UNAME),Darwin)
    LDLIBS += -framework CoreFoundation
endif

ifdef CROSS_COMPILE
    CC := $(CROSS_COMPILE)gcc
endif
```

---

## Include Directive

```makefile
# Include other makefiles
include config.mk
include rules.mk

# Optional include (no error if missing)
-include local.mk
-include .deps/*.d
```

---

## Auto-Generated Dependencies

```makefile
SRCS := main.c utils.c
DEPS := $(SRCS:.c=.d)

# Include dependency files
-include $(DEPS)

# Generate dependency files
%.d: %.c
    $(CC) -MM -MT $(@:.d=.o) $< > $@
```

---

## Parallel Builds

```bash
# Use 4 parallel jobs
make -j4

# Use all available cores
make -j$(nproc)

# Unlimited parallel jobs (not recommended)
make -j
```

---

## Parallel Build Issues

```makefile
# Problem: both might run simultaneously
clean:
    rm -rf build/

build:
    mkdir -p build/

# Solution: use order-only prerequisites
build: | setup

setup:
    mkdir -p build/
```

---

## Order-Only Prerequisites

```makefile
# Normal: rebuild if dir timestamp changes
output.o: output.c build

# Order-only: just ensure dir exists
output.o: output.c | build

build:
    mkdir -p $@
```

After `|`, prerequisites only need to exist, not be newer.

---

## Recursive Make

```makefile
SUBDIRS := lib app tests

.PHONY: all clean $(SUBDIRS)

all: $(SUBDIRS)

$(SUBDIRS):
    $(MAKE) -C $@

clean:
    for dir in $(SUBDIRS); do \
        $(MAKE) -C $$dir clean; \
    done
```

---

## Recursive Make Issues

```makefile
# Problem: each submake is independent
# Can't share dependency information

# Better: single Makefile with paths
lib/utils.o: lib/utils.c
    $(CC) -c $< -o $@

app/main.o: app/main.c lib/utils.h
    $(CC) -c $< -o $@
```

---

## Secondary Expansion

```makefile
.SECONDEXPANSION:

# $@ not normally available in prerequisites
# With secondary expansion, it is!

$(OBJECTS): $$(patsubst %.o,%.c,$$@)
    $(CC) -c $< -o $@
```

---

## Eval Function

```makefile
define PROGRAM_template
$(1): $$($(1)_OBJS)
    $$(CC) -o $$@ $$^
endef

client_OBJS := client.o net.o
server_OBJS := server.o net.o

$(eval $(call PROGRAM_template,client))
$(eval $(call PROGRAM_template,server))
```

---

## Summary

- Pattern rules with `%` for generic building
- String and path manipulation functions
- Conditionals for platform-specific builds
- Include directive for modular Makefiles
- Parallel builds with `-j`
- Order-only prerequisites with `|`
