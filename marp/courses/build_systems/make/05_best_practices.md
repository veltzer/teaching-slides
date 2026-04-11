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
# Best Practices and Real Examples

---

## Makefile Best Practices

![makefile_best_practices](svg/courses/build_systems/make/05_best_practices/makefile_best_practices.svg)

---

## Overview

- Makefile organization and structure
- Common patterns and idioms
- Real-world examples
- Debugging tips
- Common pitfalls to avoid

---

## Makefile Structure

```makefile
# 1. Variables and configuration
CC := gcc
CFLAGS := -Wall

# 2. Phony targets declaration
.PHONY: all clean install

# 3. Default target
all: program

# 4. Main build rules
# 5. Pattern rules
# 6. Utility targets (clean, install)
```

---

## Standard Targets

```makefile
.PHONY: all clean install uninstall test dist

all: $(TARGET)           # Build everything
clean:                   # Remove build artifacts
    rm -f $(OBJS) $(TARGET)
install: $(TARGET)       # Install to system
    install -m 755 $(TARGET) $(PREFIX)/bin/
uninstall:               # Remove from system
    rm -f $(PREFIX)/bin/$(TARGET)
test: $(TARGET)          # Run tests
    ./run_tests.sh
```

---

## Directory Structure

```makefile
SRCDIR := src
OBJDIR := build
BINDIR := bin

SRCS := $(wildcard $(SRCDIR)/*.c)
OBJS := $(SRCS:$(SRCDIR)/%.c=$(OBJDIR)/%.o)
TARGET := $(BINDIR)/program

$(TARGET): $(OBJS) | $(BINDIR)
    $(CC) -o $@ $^

$(OBJDIR)/%.o: $(SRCDIR)/%.c | $(OBJDIR)
    $(CC) $(CFLAGS) -c $< -o $@
```

---

## Creating Directories

```makefile
DIRS := build bin

$(DIRS):
    mkdir -p $@

# Objects depend on build/ existing
$(OBJDIR)/%.o: $(SRCDIR)/%.c | $(OBJDIR)
    $(CC) -c $< -o $@

# Target depends on bin/ existing
$(TARGET): $(OBJS) | $(BINDIR)
    $(CC) -o $@ $^
```

---

## Complete C Project

```makefile
CC := gcc
CFLAGS := -Wall -Wextra -std=c11
LDFLAGS :=
LDLIBS := -lm

SRCDIR := src
OBJDIR := obj
BINDIR := bin

SRCS := $(wildcard $(SRCDIR)/*.c)
OBJS := $(SRCS:$(SRCDIR)/%.c=$(OBJDIR)/%.o)
TARGET := $(BINDIR)/myapp

.PHONY: all clean
```

---

## Complete C Project (continued)

```makefile
all: $(TARGET)

$(TARGET): $(OBJS) | $(BINDIR)
    $(CC) $(LDFLAGS) -o $@ $^ $(LDLIBS)

$(OBJDIR)/%.o: $(SRCDIR)/%.c | $(OBJDIR)
    $(CC) $(CFLAGS) -c $< -o $@

$(BINDIR) $(OBJDIR):
    mkdir -p $@

clean:
    rm -rf $(OBJDIR) $(BINDIR)
```

---

## Debug vs Release

```makefile
DEBUG ?= 0

ifeq ($(DEBUG),1)
    CFLAGS += -g -O0 -DDEBUG
    OBJDIR := obj/debug
    BINDIR := bin/debug
else
    CFLAGS += -O2 -DNDEBUG
    OBJDIR := obj/release
    BINDIR := bin/release
endif
```

```bash
make DEBUG=1    # Debug build
make            # Release build
```

---

## Header Dependencies

```makefile
DEPDIR := .deps
DEPS := $(SRCS:$(SRCDIR)/%.c=$(DEPDIR)/%.d)

# Include existing dependencies
-include $(DEPS)

# Generate deps while compiling
$(OBJDIR)/%.o: $(SRCDIR)/%.c | $(OBJDIR) $(DEPDIR)
    $(CC) $(CFLAGS) -MMD -MF $(DEPDIR)/$*.d -c $< -o $@

$(DEPDIR):
    mkdir -p $@
```

---

## Multi-Binary Project

```makefile
BINS := client server utils

all: $(BINS)

client: client.o network.o
    $(CC) -o $@ $^

server: server.o network.o handler.o
    $(CC) -o $@ $^

utils: utils.o
    $(CC) -o $@ $^

clean:
    rm -f *.o $(BINS)
```

---

## Library Building - Static Library

```makefile
LIBNAME := mylib
LIB := lib$(LIBNAME).a
OBJS := foo.o bar.o baz.o

$(LIB): $(OBJS)
    $(AR) rcs $@ $^

# Usage
program: main.o $(LIB)
    $(CC) -o $@ main.o -L. -l$(LIBNAME)
```

---

## Library Building - Shared Library

```makefile
LIBNAME := mylib
LIB := lib$(LIBNAME).so
OBJS := foo.o bar.o baz.o

CFLAGS += -fPIC

$(LIB): $(OBJS)
    $(CC) -shared -o $@ $^

install: $(LIB)
    install -m 644 $(LIB) /usr/local/lib/
    ldconfig
```

---

## Help Target

```makefile
.PHONY: help
help:
    @echo "Available targets:"
    @echo "  all      - Build the program"
    @echo "  clean    - Remove build files"
    @echo "  install  - Install to system"
    @echo "  test     - Run tests"
    @echo ""
    @echo "Variables:"
    @echo "  DEBUG=1  - Enable debug build"
    @echo "  CC=...   - Override compiler"
```

---

## Version Embedding

```makefile
VERSION := 1.0.0
GIT_HASH := $(shell git rev-parse --short HEAD 2>/dev/null)
BUILD_DATE := $(shell date -u +%Y-%m-%dT%H:%M:%SZ)

CFLAGS += -DVERSION=\"$(VERSION)\"
CFLAGS += -DGIT_HASH=\"$(GIT_HASH)\"
CFLAGS += -DBUILD_DATE=\"$(BUILD_DATE)\"
```

---

## Common Pitfalls

1. **Spaces instead of tabs** in recipes
1. **Missing dependencies** on headers
1. **Recursive make** without care
1. **Forgetting `.PHONY`** for non-file targets
1. **Shell vs Make variables** (`$$var` vs `$(var)`)

---

## Pitfall: Shell Variables

```makefile
# WRONG - $i is Make variable (empty)
list:
    for i in 1 2 3; do echo $i; done

# CORRECT - $$i is shell variable
list:
    for i in 1 2 3; do echo $$i; done

# Also note: recipe is one shell command per line
# Use \ for continuation
```

---

## Pitfall: Recipe Execution

```makefile
# WRONG - cd doesn't persist
wrong:
    cd subdir
    make

# CORRECT - one shell command
correct:
    cd subdir && make

# OR use -C flag
better:
    $(MAKE) -C subdir
```

---

## Debugging Techniques

```bash
# Show what would be done
make -n

# Show why target is being rebuilt
make --debug=why

# Print all variables and rules
make -p

# Trace execution
make --trace

# Check specific variable
make -p | grep 'VARIABLE'
```

---

## Makefile Linting

```bash
# Check syntax
make -n -p > /dev/null

# Use checkmake (install separately)
checkmake Makefile

# Common warnings to watch for:
# - Undefined variables
# - Unused variables
# - Missing .PHONY declarations
```

---

## Performance Tips

1. Use parallel builds: `make -j$(nproc)`
1. Use `:=` instead of `=` when possible
1. Avoid recursive make
1. Use precompiled headers for C++
1. Use `ccache` for compilation caching

```bash
CC := ccache gcc
make -j8
```

---

## Summary

- Follow consistent structure and naming
- Use `.PHONY` for all non-file targets
- Separate source, object, and binary directories
- Track header dependencies automatically
- Provide `help`, `clean`, and `install` targets
- Use debug/release configurations
- Document your Makefile
