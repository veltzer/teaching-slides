# Building a Larger-Than-One-File System in C

---

## Introduction

- Why use multiple files?
    - Better organization
    - Improved readability
    - Easier maintenance
    - Code reusability

---

## Project Structure

- Typical structure:
    - Header files (.h)
    - Source files (.c)
    - Main file (main.c)

---

## Header Files

- Purpose:
    - Declare functions, structures, and variables
    - Provide interfaces for modules
- Best practices:
    - Use header guards
    - Keep declarations only

---

## Header File Example

```c
// math_operations.h
#ifndef MATH_OPERATIONS_H
#define MATH_OPERATIONS_H

int add(int a, int b);
int subtract(int a, int b);

#endif // MATH_OPERATIONS_H
```

---

## Source Files

- Purpose:
    - Implement functions declared in header files
    - Contain the actual code logic
- Best practices:
    - One source file per module
    - Include corresponding header file

---

## Source File Example

```c
// math_operations.c
#include "math_operations.h"

int add(int a, int b) {
    return a + b;
}

int subtract(int a, int b) {
    return a - b;
}
```

---

## Main File

- Purpose:
    - Entry point of the program
    - Coordinates the use of other modules
- Best practices:
    - Keep it simple
    - Include necessary header files

---

## Main File Example

```c
// main.c
#include <stdio.h>
#include "math_operations.h"

int main() {
    int result = add(5, 3);
    printf("5 + 3 = %d\n", result);
    return 0;
}
```

---

## Compilation Process

1. Compile each .c file into object files
1. Link object files to create executable

Example:

```bash
gcc -c math_operations.c
gcc -c main.c
gcc math_operations.o main.o -o program
```

---

## Using Makefiles

- Automate the build process
- Define dependencies
- Rebuild only what's necessary

Example Makefile:
```makefile
CC = gcc
CFLAGS = -Wall -Wextra

program: main.o math_operations.o
    $(CC) $(CFLAGS) main.o math_operations.o -o program

main.o: main.c math_operations.h
    $(CC) $(CFLAGS) -c main.c

math_operations.o: math_operations.c math_operations.h
    $(CC) $(CFLAGS) -c math_operations.c

clean:
    rm -f *.o program
```

---

## Best Practices

- Use meaningful file names
- Keep files focused on a single responsibility
- Use header guards to prevent multiple inclusions
- Minimize dependencies between modules
- Document your code and file structure

---

---

## Static vs Extern Linkage

```c
/* === utils.c === */
#include "utils.h"

/* External linkage: visible to other translation units */
int global_counter = 0;

/* Internal linkage: visible only in this file */
static int internal_state = 0;

/* External function */
void increment_counter(void) {
    global_counter++;
    internal_state++;
}

/* Static (file-private) helper */
static void reset_internal(void) {
    internal_state = 0;
}
```

```c
/* === utils.h === */
#ifndef UTILS_H
#define UTILS_H

extern int global_counter;  /* declaration only */
void increment_counter(void);
/* reset_internal is NOT declared here: it's private to utils.c */

#endif
```

---

## A More Complete Makefile

```makefile
CC       = gcc
CFLAGS   = -Wall -Wextra -Werror -std=c11 -pedantic -g
LDFLAGS  =
LDLIBS   = -lm

SRCS     = $(wildcard *.c)
OBJS     = $(SRCS:.c=.o)
DEPS     = $(SRCS:.c=.d)
TARGET   = program

.PHONY: all clean run

all: $(TARGET)

$(TARGET): $(OBJS)
	$(CC) $(LDFLAGS) -o $@ $^ $(LDLIBS)

# Auto-generate dependency files
%.o: %.c
	$(CC) $(CFLAGS) -MMD -MP -c $< -o $@

-include $(DEPS)

clean:
	rm -f $(OBJS) $(DEPS) $(TARGET)

run: $(TARGET)
	./$(TARGET)
```

Key features:
- Automatic dependency tracking with `-MMD -MP`
- Wildcard source file discovery
- Separate compile and link flags

---

## Opaque Types: True Encapsulation in C

```c
/* === stack.h === */
#ifndef STACK_H
#define STACK_H

#include <stdbool.h>

/* Forward declaration -- internals hidden from users */
typedef struct Stack Stack;

Stack *stack_create(int capacity);
void   stack_destroy(Stack *s);
bool   stack_push(Stack *s, int value);
bool   stack_pop(Stack *s, int *out);
bool   stack_is_empty(const Stack *s);
int    stack_size(const Stack *s);

#endif
```

```c
/* === stack.c === */
#include "stack.h"
#include <stdlib.h>

struct Stack {
    int *data;
    int top;
    int capacity;
};

Stack *stack_create(int capacity) {
    Stack *s = malloc(sizeof(Stack));
    if (s == NULL) return NULL;
    s->data = malloc(capacity * sizeof(int));
    if (s->data == NULL) { free(s); return NULL; }
    s->top = -1;
    s->capacity = capacity;
    return s;
}

void stack_destroy(Stack *s) {
    if (s) {
        free(s->data);
        free(s);
    }
}

bool stack_push(Stack *s, int value) {
    if (s->top >= s->capacity - 1) return false;
    s->data[++s->top] = value;
    return true;
}

bool stack_pop(Stack *s, int *out) {
    if (s->top < 0) return false;
    *out = s->data[s->top--];
    return true;
}

bool stack_is_empty(const Stack *s) { return s->top < 0; }
int  stack_size(const Stack *s) { return s->top + 1; }
```

Users of `stack.h` cannot access struct internals -- true information hiding.

---

## Project Directory Structure

```
project/
├── Makefile
├── include/             # Public headers
│   ├── stack.h
│   └── utils.h
├── src/                 # Source files
│   ├── main.c
│   ├── stack.c
│   └── utils.c
├── tests/               # Test files
│   ├── test_stack.c
│   └── test_utils.c
├── lib/                 # Third-party libraries
├── build/               # Build artifacts (gitignored)
└── README.md
```

Corresponding Makefile:

```makefile
CC       = gcc
CFLAGS   = -Wall -Wextra -std=c11 -Iinclude -g
SRCS     = $(wildcard src/*.c)
OBJS     = $(patsubst src/%.c, build/%.o, $(SRCS))
TARGET   = build/program

all: $(TARGET)

$(TARGET): $(OBJS) | build
	$(CC) -o $@ $^

build/%.o: src/%.c | build
	$(CC) $(CFLAGS) -MMD -MP -c $< -o $@

build:
	mkdir -p build

clean:
	rm -rf build

-include $(wildcard build/*.d)
```

---

## Conditional Compilation for Testing

```c
/* === math_ops.c === */
#include "math_ops.h"

int factorial(int n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}

/* Self-contained test when compiled with -DTEST */
#ifdef TEST
#include <stdio.h>
#include <assert.h>

int main(void) {
    assert(factorial(0) == 1);
    assert(factorial(1) == 1);
    assert(factorial(5) == 120);
    assert(factorial(10) == 3628800);
    printf("All tests passed!\n");
    return 0;
}
#endif
```

```bash
# Build and run tests
gcc -DTEST -Wall -o test_math math_ops.c && ./test_math

# Build production (no main in this file)
gcc -Wall -c math_ops.c -o math_ops.o
```

---

## Conclusion

- Multi-file systems improve:
    - Code organization
    - Maintainability
    - Reusability
- Use opaque types for true encapsulation
- Use static linkage to keep functions file-private
- Auto-generate Makefile dependencies with `-MMD -MP`
- Key components:
    - Header files (interfaces)
    - Source files (implementations)
    - Main file (entry point)
    - Build system (e.g., Makefile)
