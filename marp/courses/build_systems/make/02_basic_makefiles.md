# Basic Makefiles

## Overview
- Writing your first rules
- Understanding targets and dependencies
- Phony targets
- Default targets
- Comments and formatting

---

## Rule Syntax

## The Basic Format
```makefile
target: prerequisites
    recipe
```

- **Target**: Usually a file name
- **Prerequisites**: Files the target depends on
- **Recipe**: Shell commands to create the target

**Important**: Recipe lines MUST start with a TAB character!

---

## Tab vs Spaces

## Common Mistake
```makefile
# WRONG - spaces before gcc
program: main.c
    gcc -o program main.c

# CORRECT - tab before gcc
program: main.c
    gcc -o program main.c
```

Configure your editor to show tabs!

---

## Simple C Project

## File Structure

```tree
project/
├── Makefile
├── main.c
├── utils.c
└── utils.h
```

---

## Simple C Project

## The Makefile
```makefile
program: main.o utils.o
    gcc -o program main.o utils.o

main.o: main.c
    gcc -c main.c

utils.o: utils.c utils.h
    gcc -c utils.c

clean:
    rm -f program main.o utils.o
```

---

## Multiple Targets

## Building Different Things
```makefile
all: program tests docs

program: main.o
    gcc -o program main.o

tests: test_main.o
    gcc -o tests test_main.o

docs:
    doxygen Doxyfile
```

---

## Default Target

## First Target is Default
- Make executes the first target by default
- Convention: name it `all`

```makefile
all: program

program: main.o
    gcc -o program main.o

main.o: main.c
    gcc -c main.c
```

```bash
make      # builds 'all' (which builds 'program')
make all  # same as above
```

---

## Phony Targets

## Targets That Are Not Files
```makefile
.PHONY: clean all install test

clean:
    rm -f *.o program

all: program

install:
    cp program /usr/local/bin/

test:
    ./run_tests.sh
```

---

## Why Use .PHONY?

## The Problem Without It
- If a file named `clean` exists, `make clean` won't run
- Make thinks the target is up to date

```makefile
# Without .PHONY
clean:
    rm -f *.o

# If file 'clean' exists:
# $ make clean
# make: 'clean' is up to date.
```

---

## Dependencies Deep Dive

## Transitive Dependencies
```makefile
program: main.o utils.o lib.o
    gcc -o program main.o utils.o lib.o

main.o: main.c config.h utils.h
    gcc -c main.c

utils.o: utils.c utils.h config.h
    gcc -c utils.c

lib.o: lib.c lib.h
    gcc -c lib.c
```

---

## Dependency Graph

## Visual Representation

![visual_representation](/out/mermaid/courses/build_systems/make/02_basic_makefiles/visual_representation.svg)

---

## Comments

## Documenting Your Makefile
```makefile
# Main build target
# Compiles all source files and links them
all: program

# Build the main executable
program: main.o utils.o
    gcc -o program main.o utils.o

# Compile main.c
main.o: main.c
    gcc -c main.c
```

---

## Multiple Rules for Same Target

## Adding Dependencies
```makefile
# First rule defines the recipe
main.o: main.c
    gcc -c main.c

# Additional rules add dependencies only
main.o: utils.h
main.o: config.h
```

This is equivalent to:
```makefile
main.o: main.c utils.h config.h
    gcc -c main.c
```

---

## Handling Errors

## Recipe Error Behavior
- By default, make stops on first error
- Prefix with `-` to ignore errors

```makefile
clean:
    -rm -f *.o      # Continue even if files don't exist
    -rm -f program

force_clean:
    rm -f *.o || true  # Alternative approach
```

---

## Silent Recipes

## Suppressing Echo
- By default, make prints each command
- Prefix with `@` to suppress

```makefile
hello:
    @echo "Building hello..."
    gcc -o hello hello.c
    @echo "Done!"
```

Output:

```output
Building hello...
gcc -o hello hello.c
Done!
```

---

## Running Make

## Common Invocations
```bash
make              # Build default target
make target       # Build specific target
make -n           # Dry run (show commands)
make -B           # Force rebuild all
make -j4          # Parallel build (4 jobs)
make -f MyMake    # Use different makefile
make -C dir       # Change to dir first
```

---

## Debugging Makefiles

## Useful Options
```bash
make -n           # Print commands without executing
make -d           # Debug output
make --debug=v    # Verbose debug
make -p           # Print database (all rules)
make --trace      # Trace rule execution
```

---

## Summary

## Key Points
- Rules consist of target, prerequisites, recipe
- Recipe lines MUST begin with TAB
- First target is the default
- Use `.PHONY` for non-file targets
- Use `@` for silent commands, `-` to ignore errors
- Use `-n` for dry runs when debugging
