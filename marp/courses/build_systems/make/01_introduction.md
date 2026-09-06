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

# Introduction to Make

---

## Overview

- What is `make` and why use it?
- History and evolution of build systems
- Core concepts: targets, dependencies, and recipes
- When to use `make` vs alternatives

---

## What is Make?

- `make` is a build automation tool
- Automatically builds executable programs from source code
- Determines which pieces need to be recompiled
- Executes commands to rebuild those pieces

```bash
# Simple invocation
make
make target_name
make -f custom_makefile
```

---

## Why Use Make?

- Automates repetitive build tasks
- Only rebuilds what has changed (incremental builds)
- Documents the build process in code
- Portable across Unix-like systems
- Handles complex dependency graphs

---

## History of Make

- 1976: Created by Stuart Feldman at Bell Labs
- Originally for Unix systems
- GNU Make released in 1988
- Still widely used today (nearly 50 years later!)
- GNU Make (most common on Linux)
- BSD Make
- Microsoft NMAKE
- Many others with slight differences

---

## Alternatives to Make

- Modern Build Tools:
    - `CMake` - generates Makefiles and other build files
    - `Ninja` - focused on speed
    - `Bazel` - Google's build tool
    - `Meson` - modern, fast, user-friendly
- Language-Specific:
    - `Cargo` (Rust)
    - `Maven`/`Gradle` (Java)
    - `npm`/`yarn` (JavaScript)

---

## When to Use Make

- C/C++ projects
- Simple automation tasks
- Projects requiring portability
- When dependencies are file-based
- Shell script orchestration
- Consider alternatives when:
    - Very large codebases (Bazel, Buck)
    - Cross-platform GUI builds (CMake)
    - Language with built-in tooling

---

## Core Concepts

1. **Targets** - what you want to build
1. **Dependencies** - what the target needs
1. **Recipes** - how to build the target

```makefile
target: dependencies
    recipe_command
```

---

## Anatomy of a Makefile

```makefile
# This is a comment
program: main.o utils.o
    gcc -o program main.o utils.o

main.o: main.c
    gcc -c main.c

utils.o: utils.c utils.h
    gcc -c utils.c
```

---

## Dependency Resolution

![dependency_resolution](svg/courses/build_systems/make/01_introduction/dependency_resolution.svg)

---

## Make Algorithm

![make_algorithm](svg/courses/build_systems/make/01_introduction/make_algorithm.svg)

---

## The Algorithm Steps

1. Read the Makefile
1. Build the dependency graph
1. Check timestamps of files
1. Rebuild targets older than their dependencies
1. Execute recipes in the correct order

---

## Installing Make

```bash
# Debian/Ubuntu
sudo apt install build-essential

# Fedora/RHEL
sudo dnf install make

# Arch
sudo pacman -S make
```

On macOS:

```bash
xcode-select --install
# or via Homebrew
brew install make
```

---

## Your First Makefile

```makefile
hello: hello.c
    gcc -o hello hello.c

clean:
    rm -f hello
```

```bash
# Build
make hello

# Clean
make clean
```

---

## Summary

- `make` automates build processes
- Uses targets, dependencies, and recipes
- Only rebuilds what has changed
- Still relevant after nearly 50 years
- Foundation for understanding build systems
