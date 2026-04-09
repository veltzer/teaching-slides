# Debugging and Tools for C

---

## The Debugging Mindset

- Bugs are not random: they have deterministic causes
- Read error messages carefully before reaching for tools
- Reproduce the bug reliably first, then fix it
- Add assertions and checks early -- they catch bugs close to the source
- Use the right tool for the job:

| Problem | Tool |
|---------|------|
| Logic errors, crashes | GDB |
| Memory errors | Valgrind, ASan |
| Undefined behavior | UBSan |
| Thread bugs | Helgrind, TSan |
| Performance | perf, Cachegrind |
| Code quality | clang-tidy, cppcheck |

---

## Compiler Warnings: Your First Defense

```bash
# Minimum recommended flags
gcc -Wall -Wextra -Werror -std=c11 -pedantic program.c

# Even more warnings
gcc -Wall -Wextra -Werror -Wpedantic -Wshadow -Wconversion \
    -Wdouble-promotion -Wformat=2 -Wundef -Wstrict-prototypes \
    -Wmissing-prototypes -Wold-style-definition \
    -std=c11 program.c
```

| Flag | What It Catches |
|------|----------------|
| `-Wall` | Most common issues |
| `-Wextra` | Additional warnings |
| `-Werror` | Treat warnings as errors |
| `-Wshadow` | Variable shadowing |
| `-Wconversion` | Implicit type conversions |
| `-Wformat=2` | Format string problems |
| `-Wundef` | Undefined macros in `#if` |
| `-Wpedantic` | Strict ISO compliance |
| `-Wstrict-prototypes` | Missing parameter types |

---

## Example: Bugs Caught by Warnings

```c
#include <stdio.h>

int main(void) {
    /* -Wshadow: variable shadows outer scope */
    int x = 10;
    {
        int x = 20;  /* warning: shadows previous declaration */
        printf("%d\n", x);
    }

    /* -Wformat: wrong format specifier */
    long val = 42L;
    printf("%d\n", val);  /* warning: format '%d' for 'long' */

    /* -Wconversion: implicit narrowing conversion */
    double pi = 3.14159;
    int truncated = pi;  /* warning: conversion from double to int */

    /* -Wunused: unused variable */
    int unused_var = 0;  /* warning: unused variable */

    return 0;
}
```

---

## GDB: Getting Started

```bash
# Compile with debug info
gcc -g -O0 -o program program.c

# Start GDB
gdb ./program

# Or attach to a running process
gdb -p <pid>
```

Essential GDB commands:

| Command | Short | Description |
|---------|-------|-------------|
| `run [args]` | `r` | Start program |
| `break main` | `b main` | Set breakpoint at main |
| `break file.c:42` | `b file.c:42` | Break at line 42 |
| `next` | `n` | Step over (next line) |
| `step` | `s` | Step into function |
| `continue` | `c` | Continue to next breakpoint |
| `print expr` | `p expr` | Print expression |
| `backtrace` | `bt` | Show call stack |
| `info locals` | | Show local variables |
| `quit` | `q` | Exit GDB |

---

## GDB: Debugging a Crash

```c
/* crash.c */
#include <stdio.h>
#include <string.h>

void process(char *data) {
    printf("Length: %zu\n", strlen(data));  /* crash if data is NULL */
}

int main(void) {
    char *ptr = NULL;
    process(ptr);
    return 0;
}
```

```bash
$ gcc -g -O0 -o crash crash.c
$ gdb ./crash
(gdb) run
Program received signal SIGSEGV, Segmentation fault.
0x0000... in strlen () from /lib/x86_64-linux-gnu/libc.so.6
(gdb) bt
#0  0x0000... in strlen () from /lib/x86_64-linux-gnu/libc.so.6
#1  0x0000... in process (data=0x0) at crash.c:5
#2  0x0000... in main () at crash.c:10
(gdb) frame 1
#1  0x0000... in process (data=0x0) at crash.c:5
(gdb) print data
$1 = 0x0
(gdb) quit
```

The bug is clear: `data` is `NULL` at frame #1.

---

## GDB: Breakpoints and Watchpoints

```bash
(gdb) break process          # break when process() is called
(gdb) break crash.c:5        # break at specific line
(gdb) break process if data == 0  # conditional breakpoint

# Watchpoints: break when variable changes
(gdb) watch counter          # break when counter is modified
(gdb) rwatch buffer[10]      # break when buffer[10] is read

# Managing breakpoints
(gdb) info breakpoints       # list all breakpoints
(gdb) delete 2               # delete breakpoint #2
(gdb) disable 1              # temporarily disable breakpoint #1
(gdb) enable 1               # re-enable breakpoint #1
```

---

## GDB: Examining Memory

```bash
# Print variable
(gdb) print x                # print value of x
(gdb) print *array@10        # print 10 elements of array
(gdb) print /x val           # print in hexadecimal
(gdb) print sizeof(struct Foo)

# Examine raw memory
(gdb) x/16xb ptr             # 16 bytes in hex
(gdb) x/4xw ptr              # 4 words (32-bit) in hex
(gdb) x/s str                # as string
(gdb) x/10i main             # 10 instructions at main

# Memory layout info
(gdb) info registers          # CPU registers
(gdb) info frame              # current stack frame
(gdb) info proc mappings      # memory map
```

---

## GDB: Post-Mortem with Core Dumps

```bash
# Enable core dumps
ulimit -c unlimited

# Run program (crashes and creates core file)
./program

# Analyze core dump
gdb ./program core
(gdb) bt            # see where it crashed
(gdb) info locals   # see local variables at crash point
```

Or trigger a core dump from GDB:

```bash
(gdb) run
# ... program hangs ...
# Press Ctrl+C
(gdb) bt              # see what the program is doing
(gdb) generate-core-file  # save core dump
```

---

## Valgrind Memcheck: Memory Error Detection

```bash
# Basic usage
valgrind ./program

# Full leak check
valgrind --leak-check=full --show-leak-kinds=all \
         --track-origins=yes --verbose ./program
```

What Valgrind detects:

| Error Type | Example |
|-----------|---------|
| Invalid read/write | Buffer overflow, use-after-free |
| Conditional jump on uninitialized value | `if (uninitialized_var)` |
| Memory leak | malloc without free |
| Invalid free | Double free, free of stack memory |
| Mismatched free | malloc with delete (C++ issue) |
| Overlapping memcpy | Source and dest overlap |

---

## Valgrind: Reading the Output

```c
/* leak.c */
#include <stdlib.h>

int main(void) {
    int *p = malloc(40);
    p[10] = 42;           /* invalid write (out of bounds) */
    return 0;             /* memory leak: p not freed */
}
```

```bash
$ gcc -g -O0 -o leak leak.c
$ valgrind --leak-check=full ./leak

==1234== Invalid write of size 4
==1234==    at 0x401136: main (leak.c:5)
==1234==  Address 0x4a47068 is 0 bytes after a block of size 40 alloc'd
==1234==    at 0x4841888: malloc (vg_replace_malloc.c:381)
==1234==    by 0x401127: main (leak.c:4)
==1234==
==1234== HEAP SUMMARY:
==1234==   in use at exit: 40 bytes in 1 blocks
==1234==   total heap usage: 1 allocs, 0 frees, 40 bytes allocated
==1234==
==1234== 40 bytes in 1 blocks are definitely lost
==1234==    at 0x4841888: malloc (vg_replace_malloc.c:381)
==1234==    by 0x401127: main (leak.c:4)
```

---

## Valgrind Helgrind: Thread Error Detection

```bash
# Detect data races and lock ordering problems
valgrind --tool=helgrind ./threaded_program
```

Helgrind detects:
- Data races (unsynchronized access to shared data)
- Lock order violations (potential deadlocks)
- Misuse of POSIX threads API

---

## Valgrind Cachegrind: Cache Profiling

```bash
# Profile cache usage
valgrind --tool=cachegrind ./program

# View results
cg_annotate cachegrind.out.<pid>
```

Output shows:
- L1 instruction/data cache miss rates
- Last-level cache miss rates
- Branch prediction miss rates
- Per-line cache miss annotations

---

## AddressSanitizer (ASan)

```bash
gcc -g -fsanitize=address -fno-omit-frame-pointer -o program program.c
./program
```

```c
/* asan_demo.c */
#include <stdlib.h>

int main(void) {
    int *arr = malloc(10 * sizeof(int));
    arr[10] = 42;  /* heap buffer overflow */
    free(arr);
    return 0;
}
```

ASan output:

```misc
==1234==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x604...
WRITE of size 4 at 0x604... thread T0
    #0 0x401234 in main asan_demo.c:5
    #1 0x7f... in __libc_start_main ...

0x604... is located 0 bytes after 40-byte region [0x604...,0x604...)
allocated by thread T0 here:
    #0 0x7f... in malloc ...
    #1 0x401200 in main asan_demo.c:4
```

---

## ASan vs Valgrind Comparison

| Feature | AddressSanitizer | Valgrind Memcheck |
|---------|-----------------|-------------------|
| Slowdown | ~2x | ~10-20x |
| Memory overhead | ~3x | ~2x |
| Requires recompilation | Yes | No |
| Stack buffer overflow | Yes | No |
| Use-after-return | Yes (with flag) | No |
| Uninitialized reads | No (use MSan) | Yes |
| Works on optimized code | Yes | Yes |
| Thread support | Limited | Yes (Helgrind) |

---

## UndefinedBehaviorSanitizer (UBSan)

```bash
gcc -g -fsanitize=undefined -o program program.c
./program
```

```c
/* ubsan_demo.c */
#include <stdio.h>
#include <limits.h>

int main(void) {
    /* Signed integer overflow */
    int x = INT_MAX;
    int y = x + 1;  /* UB! UBSan catches this */
    printf("y = %d\n", y);

    /* Division by zero */
    int z = 42 / 0;  /* UB! */

    /* Shift overflow */
    int shifted = 1 << 33;  /* UB for 32-bit int */

    /* NULL dereference */
    int *p = NULL;
    /* int val = *p; */  /* UB! */

    return 0;
}
```

UBSan output:

```misc
ubsan_demo.c:7:17: runtime error: signed integer overflow:
2147483647 + 1 cannot be represented in type 'int'
```

---

## Combining Sanitizers

```bash
# ASan + UBSan together (recommended for development)
gcc -g -fsanitize=address,undefined \
    -fno-omit-frame-pointer \
    -O1 -o program program.c

# ThreadSanitizer (cannot be combined with ASan)
gcc -g -fsanitize=thread -o program program.c

# MemorySanitizer (Clang only, cannot combine with ASan)
clang -g -fsanitize=memory -o program program.c
```

Recommended Makefile:

```makefile
# Development build with all sanitizers
debug: CFLAGS += -g -O0 -fsanitize=address,undefined \
                 -fno-omit-frame-pointer
debug: LDFLAGS += -fsanitize=address,undefined
debug: program

# Release build
release: CFLAGS += -O2 -DNDEBUG
release: program
```

---

## Static Analysis: clang-tidy

```bash
# Run clang-tidy on a file
clang-tidy program.c -- -std=c11

# With specific checks
clang-tidy -checks='bugprone-*,cert-*,clang-analyzer-*' program.c

# Fix issues automatically
clang-tidy -fix program.c -- -std=c11
```

Common clang-tidy checks:
- `bugprone-sizeof-expression`: suspicious sizeof usage
- `bugprone-string-literal-with-embedded-nul`: nulls in strings
- `clang-analyzer-core.NullDereference`: potential NULL deref
- `cert-err34-c`: unchecked return values from string-to-number
- `cert-msc30-c`: use of rand()

---

## Static Analysis: cppcheck

```bash
# Basic check
cppcheck program.c

# Enable all checks
cppcheck --enable=all --suppress=missingIncludeSystem program.c

# Check entire project
cppcheck --enable=all src/

# Generate XML report
cppcheck --enable=all --xml-version=2 src/ 2> report.xml
```

What cppcheck finds:
- Null pointer dereferences
- Buffer overflows
- Resource leaks (file handles)
- Unused functions and variables
- Style issues

---

## Makefile Best Practices

```makefile
CC       = gcc
CFLAGS   = -Wall -Wextra -Werror -std=c11 -pedantic
LDFLAGS  =
LDLIBS   = -lm

# Source and object files
SRCS     = $(wildcard src/*.c)
OBJS     = $(patsubst src/%.c,build/%.o,$(SRCS))
DEPS     = $(OBJS:.o=.d)
TARGET   = build/program

.PHONY: all clean debug release test check

# Default target
all: release

# Debug build with sanitizers
debug: CFLAGS  += -g -O0 -fsanitize=address,undefined -fno-omit-frame-pointer
debug: LDFLAGS += -fsanitize=address,undefined
debug: $(TARGET)

# Release build
release: CFLAGS += -O2 -DNDEBUG
release: $(TARGET)

# Link
$(TARGET): $(OBJS) | build
    $(CC) $(LDFLAGS) -o $@ $^ $(LDLIBS)

# Compile with auto-dependencies
build/%.o: src/%.c | build
    $(CC) $(CFLAGS) -MMD -MP -c $< -o $@

build:
    mkdir -p build

# Run tests
test: debug
    ./$(TARGET) --test

# Static analysis
check:
    cppcheck --enable=all --suppress=missingIncludeSystem src/
    clang-tidy src/*.c -- $(CFLAGS)

# Memory check
memcheck: debug
    valgrind --leak-check=full --show-leak-kinds=all \
             --track-origins=yes ./$(TARGET)

clean:
    rm -rf build

-include $(DEPS)
```

---

## Assert: Catching Bugs Early

```c
#include <stdio.h>
#include <assert.h>
#include <stdlib.h>

/* assert() checks a condition at runtime */
/* If false: prints message and calls abort() */
/* Disabled when compiled with -DNDEBUG */

double divide(double a, double b) {
    assert(b != 0.0 && "Division by zero!");
    return a / b;
}

void *safe_malloc(size_t size) {
    assert(size > 0 && "Cannot allocate 0 bytes");
    void *ptr = malloc(size);
    assert(ptr != NULL && "malloc failed");
    return ptr;
}

int main(void) {
    printf("%.2f\n", divide(10.0, 3.0));   /* OK */
    /* printf("%.2f\n", divide(10.0, 0.0)); */  /* assert fires! */

    int *data = safe_malloc(100 * sizeof(int));
    free(data);

    return 0;
}
```

```misc
program: program.c:9: divide: Assertion `b != 0.0 && "Division by zero!"' failed.
Aborted (core dumped)
```

---

## Debugging Techniques Without Tools

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>

/* 1. Diagnostic macros */
#define LOG(level, fmt, ...) \
    fprintf(stderr, "[%s] %s:%d: " fmt "\n", \
            level, __FILE__, __LINE__, ##__VA_ARGS__)

#define LOG_ERROR(fmt, ...) LOG("ERROR", fmt, ##__VA_ARGS__)
#define LOG_DEBUG(fmt, ...) LOG("DEBUG", fmt, ##__VA_ARGS__)

/* 2. Check system call return values */
#define CHECK(expr) do { \
    if (!(expr)) { \
        LOG_ERROR("Check failed: %s (errno=%d: %s)", \
                  #expr, errno, strerror(errno)); \
        exit(EXIT_FAILURE); \
    } \
} while (0)

int main(void) {
    LOG_DEBUG("Program started");

    FILE *f = fopen("/etc/hostname", "r");
    CHECK(f != NULL);

    char buf[256];
    CHECK(fgets(buf, sizeof(buf), f) != NULL);
    /* Remove trailing newline */
    buf[strcspn(buf, "\n")] = '\0';

    LOG_DEBUG("Hostname: %s", buf);
    fclose(f);

    return 0;
}
```

---

## Profiling with perf

```bash
# Record performance data
perf record ./program

# Show hotspots
perf report

# Quick stat summary
perf stat ./program

# Flamegraph (requires flamegraph.pl)
perf record -g ./program
perf script | stackcollapse-perf.pl | flamegraph.pl > flame.svg
```

Key perf stat metrics:

| Metric | Meaning |
|--------|---------|
| task-clock | CPU time used |
| instructions | Total instructions executed |
| cycles | CPU cycles consumed |
| IPC | Instructions per cycle (higher = better) |
| cache-misses | L1/LLC cache misses |
| branch-misses | Branch prediction failures |

---

## strace: System Call Tracing

```bash
# Trace all system calls
strace ./program

# Show only file operations
strace -e trace=file ./program

# Show only network operations
strace -e trace=network ./program

# Show timing information
strace -T ./program

# Attach to running process
strace -p <pid>

# Count system calls
strace -c ./program
```

Example output:

```misc
open("config.txt", O_RDONLY) = -1 ENOENT (No such file or directory)
write(2, "Error: config file not found\n", 29) = 29
```

---

## Debugging Checklist

1. **Reproduce**: Can you trigger the bug reliably?
1. **Minimize**: What is the smallest input that triggers it?
1. **Warnings**: Does `gcc -Wall -Wextra` show anything?
1. **Sanitizers**: Run with ASan + UBSan. Any findings?
1. **Valgrind**: Any memory errors or leaks?
1. **GDB**: Set breakpoint near the bug. Step through.
1. **Print debugging**: Add strategic `fprintf(stderr, ...)` calls
1. **Assertions**: Add `assert()` for invariants you expect
1. **Static analysis**: Run `cppcheck` or `clang-tidy`
1. **Rubber duck**: Explain the code line by line

---

## Summary

- Turn on all compiler warnings and treat them as errors
- Use GDB for interactive debugging: breakpoints, stepping, examining memory
- Use Valgrind for memory leak detection and memory error checking
- Use AddressSanitizer for fast memory error detection (requires recompilation)
- Use UndefinedBehaviorSanitizer to catch undefined behavior at runtime
- Use clang-tidy and cppcheck for static analysis
- Write a Makefile with debug/release/test/memcheck targets
- Add assertions early and liberally -- they document assumptions and catch bugs
- Use `strace` and `perf` for system-level and performance debugging
