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
```
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

## Conclusion

- Multi-file systems improve:
  - Code organization
  - Maintainability
  - Reusability
- Key components:
  - Header files
  - Source files
  - Main file
  - Build system (e.g., Makefile)
