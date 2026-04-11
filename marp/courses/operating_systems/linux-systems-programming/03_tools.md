---
tags:
  - infrastructure:linux
  - languages:c
  - concepts:systems-programming
level: advanced
category: operating-systems
audience:
  - audiences:developers
  - audiences:devops

---
# Tools for Linux Systems Programming

---

## Chapter Overview

1. **GCC Compiler Deep Dive**
1. **Make Build System**
1. **Building Applications**
1. **Creating Libraries**
1. **Dynamic Linking**
1. **Build Tools Comparison**
1. **Best Practices**

---

## The GCC Compiler Suite

## What is GCC?

- **GNU Compiler Collection**
- Supports C, C++, Fortran, Go, Ada
- De facto standard for Linux
- Cross-platform support
- Free and open source

Current version: GCC 13.x

---

## GCC Architecture

![gcc_architecture](svg/courses/operating_systems/linux-systems-programming/03_tools/gcc_architecture.svg)

---

## Compilation Stages

## 1. Preprocessing

```bash
# Run preprocessor only
gcc -E source.c -o source.i

# What it does:
# - Include headers (#include)
# - Expand macros (#define)
# - Process conditionals (#ifdef)
# - Remove comments
```

---

## Compilation Stages (cont.)

## 2. Compilation

```bash
# Compile to assembly
gcc -S source.c -o source.s

# Produces human-readable assembly:
    .globl main
    .type  main, @function
main:
    pushq  %rbp
    movq   %rsp, %rbp
    movl   $0, %eax
    popq   %rbp
    ret
```

---

## Compilation Stages (cont.)

## 3. Assembly

```bash
# Assemble to object file
gcc -c source.c -o source.o

# Creates binary object file
# Contains:
# - Machine code
# - Symbol table
# - Relocation info
# - Debug info (with -g)
```

---

## Compilation Stages (cont.)

## 4. Linking

```bash
# Link object files
gcc source.o helper.o -o program

# Linker (ld) performs:
# - Symbol resolution
# - Relocation
# - Section merging
# - Library inclusion
```

---

## Essential GCC Options

## Compilation Flags:

```bash
# Optimization levels
-O0    # No optimization (default)
-O1    # Basic optimization
-O2    # Recommended optimization
-O3    # Aggressive optimization
-Os    # Optimize for size
-Og    # Optimize for debugging

# Example
gcc -O2 program.c -o program
```

---

## Warning Flags

## Catch More Bugs:

```bash
# Essential warnings
-Wall      # All common warnings
-Wextra    # Extra warnings
-Werror    # Treat warnings as errors
-pedantic  # Strict ISO C compliance

# Specific warnings
-Wuninitialized
-Wformat-security
-Warray-bounds
-Wnull-dereference

# Recommended combination
gcc -Wall -Wextra -Werror -O2 source.c
```

---

## Debug Options

## Debugging Support:

```bash
# Debug symbols
-g     # Default debug info
-g3    # Maximum debug info
-ggdb  # GDB-specific format

# Debug and optimize
-Og -g  # Optimized for debugging

# Address Sanitizer
-fsanitize=address  # Memory errors
-fsanitize=undefined # UB detection
-fsanitize=thread   # Race conditions
```

---

## Architecture Options

## Target Specific Code:

```bash
# Architecture
-march=native     # Optimize for current CPU
-march=x86-64-v3  # x86-64 with AVX2
-m32              # 32-bit binary
-m64              # 64-bit binary

# Features
-msse4.2          # Enable SSE 4.2
-mavx2            # Enable AVX2
-fpic             # Position independent code
-fno-omit-frame-pointer  # Keep frame pointer
```

---

## Preprocessor Control

```bash
# Define macros
gcc -DDEBUG -DVERSION=2 source.c

# Include paths
gcc -I/usr/local/include -I./headers source.c

# In code:
#ifdef DEBUG
    printf("Debug mode\n");
#endif
```

---

## Make Build System

## What is Make?

- **Build automation tool**
- Tracks dependencies
- Incremental builds
- Language agnostic
- Rule-based system

File: `Makefile` or `makefile`

---

## Makefile Anatomy

```makefile
# Basic structure
target: dependencies
    command

# Variables
CC = gcc
CFLAGS = -Wall -O2

# Pattern rules
%.o: %.c
    $(CC) $(CFLAGS) -c $< -o $@

# Phony targets
.PHONY: clean
clean:
    rm -f *.o program
```

---

## Make Variables

## Automatic Variables:

```makefile
# $@ - Target name
# $< - First dependency
# $^ - All dependencies
# $* - Stem (pattern match)

# Example
program: main.o utils.o
    gcc $^ -o $@    # gcc main.o utils.o -o program

%.o: %.c
    gcc -c $< -o $@  # gcc -c main.c -o main.o
```

---

## Make Functions

```makefile
# String functions
sources = $(wildcard *.c)
objects = $(patsubst %.c,%.o,$(sources))
objects2 = $(sources:.c=.o)

# File functions
SRCS = $(shell find . -name "*.c")
DEPS = $(wildcard *.h)

# Conditional functions
DEBUG ?= 0
ifeq ($(DEBUG),1)
    CFLAGS += -g -DDEBUG
else
    CFLAGS += -O2
endif
```

---

## Complete Makefile Example

```makefile
# Compiler and flags
CC = gcc
CFLAGS = -Wall -Wextra -O2
LDFLAGS = -lm -lpthread

# Files
SRCS = $(wildcard src/*.c)
OBJS = $(SRCS:src/%.c=build/%.o)
TARGET = myprogram

# Build rules
all: $(TARGET)

$(TARGET): $(OBJS)
    $(CC) $(OBJS) -o $@ $(LDFLAGS)

build/%.o: src/%.c | build
    $(CC) $(CFLAGS) -c $< -o $@

build:
    mkdir -p build

clean:
    rm -rf build $(TARGET)

.PHONY: all clean
```

---

## Make Dependencies

## Automatic Dependency Generation:

```makefile
# Generate .d files with dependencies
DEPS = $(OBJS:.o=.d)

-include $(DEPS)

%.d: %.c
    $(CC) -MM -MT $(@:.d=.o) $< > $@

# Or using compiler flag
CFLAGS += -MMD -MP
```

---

## Building Applications

## Simple Application:

```bash
# Single file
gcc -o hello hello.c

# Multiple files
gcc -o program main.c utils.c helper.c

# With libraries
gcc -o program main.c -lm -lpthread

# Static linking
gcc -static -o program main.c
```

---

## Program Structure

![program_structure](svg/courses/operating_systems/linux-systems-programming/03_tools/program_structure.svg)

---

## Creating Static Libraries

## Archive (.a) Files:

```bash
# Compile object files
gcc -c file1.c -o file1.o
gcc -c file2.c -o file2.o

# Create static library
ar rcs libmylib.a file1.o file2.o

# View contents
ar t libmylib.a

# Extract files
ar x libmylib.a

# Use library
gcc main.c -L. -lmylib -o program
```

---

## Creating Shared Libraries

## Dynamic (.so) Files:

```bash
# Compile with PIC
gcc -fPIC -c file1.c -o file1.o
gcc -fPIC -c file2.c -o file2.o

# Create shared library
gcc -shared -o libmylib.so file1.o file2.o

# With version
gcc -shared -Wl,-soname,libmylib.so.1 \
    -o libmylib.so.1.0.0 file1.o file2.o

# Create symlinks
ln -s libmylib.so.1.0.0 libmylib.so.1
ln -s libmylib.so.1 libmylib.so
```

---

## Library Versioning

## SONAME Convention:

```bash
libname.so.MAJOR.MINOR.PATCH

# Example: libcurl.so.4.8.0
# SONAME: libcurl.so.4
# Linker name: libcurl.so

# Check SONAME
readelf -d libmylib.so | grep SONAME

# Version script for symbol versioning
cat > version.map << EOF
VER_1.0 {
    global: function1; function2;
    local: *;
};
EOF

gcc -shared -Wl,--version-script=version.map ...
```

---

## Finding Libraries at Runtime

## Library Search Path:

```bash
# 1. RPATH (compiled in)
gcc -Wl,-rpath,/opt/myapp/lib ...

# 2. LD_LIBRARY_PATH (environment)
export LD_LIBRARY_PATH=/opt/lib:$LD_LIBRARY_PATH

# 3. System paths (/etc/ld.so.conf)
cat /etc/ld.so.conf.d/myapp.conf
/opt/myapp/lib

# Update cache
sudo ldconfig

# 4. Default paths
/lib, /usr/lib, /lib64, /usr/lib64
```

---

## Dynamic Linker

## Runtime Linking:

```bash
# View dependencies
ldd program
    linux-vdso.so.1 =>  (0x00007fff...)
    libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6
    /lib64/ld-linux-x86-64.so.2

# Debug dynamic linking
LD_DEBUG=libs ./program
LD_DEBUG=symbols ./program

# Preload library
LD_PRELOAD=/path/to/lib.so ./program
```

---

## Symbol Resolution

![symbol_resolution](svg/courses/operating_systems/linux-systems-programming/03_tools/symbol_resolution.svg)

---

## Symbol Visibility

## Controlling Exports:

```c
// Default visibility
void public_function() { }

// Hidden visibility
__attribute__((visibility("hidden")))
void internal_function() { }

// Compiler flag for default hidden
// gcc -fvisibility=hidden

// Export specific symbols
__attribute__((visibility("default")))
void exported_function() { }
```

---

## Build Tools Comparison

| Tool | Pros | Cons | Use Case |
|------|------|------|----------|
| **Make** | Simple, ubiquitous | Complex syntax | Small projects |
| **CMake** | Cross-platform | Extra step | Large projects |
| **Ninja** | Very fast | Not human-friendly | Build backend |
| **Bazel** | Scalable, cached | Complex | Google-scale |
| **Meson** | Modern, fast | Less mature | New projects |

---

## CMake Basics

```cmake
# CMakeLists.txt
cmake_minimum_required(VERSION 3.10)
project(MyProject)

# Set C standard
set(CMAKE_C_STANDARD 11)
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -Wall -O2")

# Add executable
add_executable(program main.c utils.c)

# Add library
add_library(mylib SHARED lib.c)

# Link libraries
target_link_libraries(program mylib m pthread)

# Install
install(TARGETS program DESTINATION bin)
install(TARGETS mylib DESTINATION lib)
```

---

## CMake Build Process

```bash
# Out-of-source build
mkdir build
cd build

# Configure
cmake ..
# or with options
cmake -DCMAKE_BUILD_TYPE=Release ..

# Build
make -j$(nproc)

# Install
sudo make install

# Or use ninja
cmake -G Ninja ..
ninja
```

---

## Ninja Build System

```python
# build.ninja (usually generated)
rule cc
  command = gcc -c $in -o $out
  description = CC $out

rule link
  command = gcc $in -o $out
  description = LINK $out

build main.o: cc main.c
build utils.o: cc utils.c
build program: link main.o utils.o

default program
```

---

## Package Config (pkg-config)

## Finding Libraries:

```bash
# Check if library exists
pkg-config --exists libcurl

# Get compile flags
pkg-config --cflags libcurl
# Output: -I/usr/include/x86_64-linux-gnu

# Get link flags
pkg-config --libs libcurl
# Output: -lcurl

# Use in compilation
gcc $(pkg-config --cflags libcurl) main.c \
    $(pkg-config --libs libcurl) -o program
```

---

## Creating pkg-config Files

```bash
# mylib.pc
prefix=/usr/local
exec_prefix=${prefix}
libdir=${exec_prefix}/lib
includedir=${prefix}/include

Name: MyLib
Description: My awesome library
Version: 1.0.0
Libs: -L${libdir} -lmylib
Cflags: -I${includedir}
```

---

## Debugging Tools

## Essential Debugging:

```bash
# GDB - GNU Debugger
gdb ./program
(gdb) break main
(gdb) run
(gdb) next
(gdb) print variable
(gdb) backtrace

# Valgrind - Memory debugging
valgrind --leak-check=full ./program

# strace - System call tracing
strace -e open,read,write ./program

# ltrace - Library call tracing
ltrace ./program
```

---

## Performance Tools

```bash
# perf - Performance analysis
perf record ./program
perf report

# gprof - Profiling
gcc -pg program.c -o program
./program
gprof program gmon.out

# time - Basic timing
time ./program

# cachegrind - Cache analysis
valgrind --tool=cachegrind ./program
```

---

## Static Analysis

```bash
# Compiler warnings
gcc -Wall -Wextra -Wanalyzer

# cppcheck
cppcheck --enable=all source.c

# clang static analyzer
scan-build gcc -c source.c

# Address Sanitizer
gcc -fsanitize=address -g program.c
./program  # Runtime checking
```

---

## Best Practices

## Code Organization:

```tree
project/
├── src/          # Source files
├── include/      # Header files
├── lib/          # Libraries
├── build/        # Build output
├── tests/        # Unit tests
├── docs/         # Documentation
├── CMakeLists.txt
└── README.md
```

---

## Compilation Best Practices

1. **Always use warning flags**
   ```bash
   -Wall -Wextra -Werror
   ```

1. **Enable optimization for release**
   ```bash
   -O2 or -O3
   ```

1. **Include debug info for development**
   ```bash
   -g -Og
   ```

1. **Use static analysis**

1. **Test with sanitizers**

---

## Library Best Practices

1. **Use semantic versioning**
    - MAJOR.MINOR.PATCH

1. **Provide pkg-config files**

1. **Document dependencies**

1. **Use symbol versioning**

1. **Hide internal symbols**

1. **Provide both static and shared**

---

## Makefile Best Practices

1. **Use automatic variables**
    - $@, $<, $^

1. **Generate dependencies**
    - -MMD -MP

1. **Out-of-source builds**

1. **Parallel builds**
    - make -j

1. **PHONY targets**

1. **Provide clean target**

---

## Cross-Compilation

```bash
# Set cross compiler
CC = arm-linux-gnueabihf-gcc

# Cross compile
arm-linux-gnueabihf-gcc program.c -o program.arm

# CMake cross compilation
cmake -DCMAKE_TOOLCHAIN_FILE=arm-toolchain.cmake

# Check binary
file program.arm
# program.arm: ELF 32-bit LSB executable, ARM
```

---

## Continuous Integration

```yaml
# .github/workflows/build.yml
name: Build
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Build
      run: |
        mkdir build && cd build
        cmake ..
        make -j$(nproc)
    - name: Test
      run: make test
```

---

## Summary

## Key Takeaways:

- **GCC** is more than a compiler
- **Make** automates builds efficiently
- **Libraries** enable code reuse
- **Dynamic linking** saves memory
- **Tools** help debug and optimize
- **Best practices** ensure quality
- **Modern alternatives** offer benefits

Master these tools = Professional development!
