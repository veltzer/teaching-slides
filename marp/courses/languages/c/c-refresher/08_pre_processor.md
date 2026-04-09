# Using the C Preprocessor

---

## Introduction to the C Preprocessor

- What is the preprocessor?
    - First stage of compilation
    - Text substitution tool
- Key functions:
    - File inclusion
    - Macro expansion
    - Conditional compilation
    - Line control

---

## File Inclusion

- `#include` directive
- Two forms:
    - `#include <file>` (system headers)
    - `#include "file"` (user-defined headers)
- Example:

```c
#include <stdio.h>
#include "myheader.h"
```

---

## Macro Definitions

- `#define` directive
- Object-like macros:

```c
#define PI 3.14159
#define MAX_SIZE 100
```

- Function-like macros:

```c
#define MAX(a, b) ((a) > (b) ? (a) : (b))
```

---

## Conditional Compilation

- `#ifdef`, `#ifndef`, `#if`, `#elif`, `#else`, `#endif`
- Used for:
    - Platform-specific code
    - Debugging
    - Feature toggles
- Example:

```c
#ifdef DEBUG
printf("Debug: x = %d\n", x);
#endif
```

---

## Predefined Macros

- Automatically defined by the compiler
- Examples:
    - `__FILE__`: Current source file name
    - `__LINE__`: Current line number
    - `__DATE__`: Compilation date
    - `__TIME__`: Compilation time
    - `__STDC__`: Conformance to ISO Standard C

---
## Macro Pitfalls and Best Practices
- Be cautious with side effects
- Use parentheses in macro definitions
- Consider using inline functions instead
- Avoid overly complex macros
- Example of a problematic macro:

```c
#define SQUARE(x) x * x
// SQUARE(a + 1) expands to a + 1 * a + 1
```

---
## #pragma Directive
- Compiler-specific instructions
- Common uses:
    - Control struct packing
    - Manage warnings
    - Specify optimization levels
- Example:

```c
#pragma pack(1)
struct tightly_packed {
  char c;
  int i;
};
#pragma pack()
```

---

## Advanced Preprocessing Techniques

- Token pasting operator (`##`)
- Stringification operator (`#`)
- Variadic macros
- Example:

```c
#define CONCAT(a, b) a ## b
#define STRINGIFY(x) #x
#define DEBUG_PRINT(...) printf("Debug: " __VA_ARGS__)
```

---

## Preprocessor in the Build Process

- Preprocessing stage:
    1. Tokenization
    1. Macro expansion
    1. Include file expansion
    1. Conditional compilation
    1. Line control
- View preprocessor output:

```bash
gcc -E source.c -o preprocessed.i
```

---

## Best Practices

- Use include guards
- Minimize macro usage where possible
- Keep macros simple and clear
- Use inline functions for complex operations
- Be consistent with naming conventions
- Document macros and their intended use

---

## Include Guards vs #pragma once

```c
/* Traditional include guard */
#ifndef MY_HEADER_H
#define MY_HEADER_H

struct MyStruct {
    int value;
};

void my_function(void);

#endif /* MY_HEADER_H */
```

```c
/* Modern alternative (non-standard but widely supported) */
#pragma once

struct MyStruct {
    int value;
};

void my_function(void);
```

| Feature | Include Guards | `#pragma once` |
|---------|---------------|----------------|
| Standard C | Yes | No (extension) |
| Portability | All compilers | Most compilers |
| Handles symlinks | Yes | May fail |
| Verbosity | More | Less |

---

## X-Macros: An Advanced Pattern

```c
#include <stdio.h>

/* Define all error codes in ONE place */
#define ERROR_LIST \
    X(ERR_NONE,     "No error")        \
    X(ERR_NOMEM,    "Out of memory")   \
    X(ERR_IO,       "I/O error")       \
    X(ERR_TIMEOUT,  "Timeout")         \
    X(ERR_INVALID,  "Invalid input")

/* Generate enum */
enum ErrorCode {
    #define X(code, msg) code,
    ERROR_LIST
    #undef X
    ERR_COUNT
};

/* Generate string table */
static const char *error_messages[] = {
    #define X(code, msg) msg,
    ERROR_LIST
    #undef X
};

const char *error_to_string(enum ErrorCode code) {
    if (code >= 0 && code < ERR_COUNT) {
        return error_messages[code];
    }
    return "Unknown error";
}

int main(void) {
    for (int i = 0; i < ERR_COUNT; i++) {
        printf("Error %d: %s\n", i, error_to_string(i));
    }
    return 0;
}
```

---

## Debug Macros: A Practical Toolkit

```c
#include <stdio.h>
#include <stdlib.h>

/* Enable by compiling with -DDEBUG */
#ifdef DEBUG
  #define DBG(fmt, ...) \
      fprintf(stderr, "[DBG %s:%d] " fmt "\n", \
              __FILE__, __LINE__, ##__VA_ARGS__)
#else
  #define DBG(fmt, ...) ((void)0)
#endif

/* Assert with message */
#define ASSERT(cond, msg) do { \
    if (!(cond)) { \
        fprintf(stderr, "ASSERT FAILED: %s\n  %s:%d: %s\n", \
                #cond, __FILE__, __LINE__, msg); \
        abort(); \
    } \
} while (0)

/* Safe malloc */
#define SAFE_MALLOC(ptr, size) do { \
    (ptr) = malloc(size); \
    if ((ptr) == NULL) { \
        fprintf(stderr, "malloc failed at %s:%d\n", \
                __FILE__, __LINE__); \
        exit(EXIT_FAILURE); \
    } \
} while (0)

int main(void) {
    DBG("Starting program with pid=%d", getpid());

    int *data;
    SAFE_MALLOC(data, 100 * sizeof(int));
    DBG("Allocated %zu bytes", 100 * sizeof(int));

    ASSERT(data != NULL, "data must not be NULL");

    free(data);
    DBG("Cleanup complete");
    return 0;
}
```

Compile: `gcc -DDEBUG -Wall -o prog prog.c`

---

## Multi-Line Macros: The do-while(0) Idiom

```c
/* WRONG: breaks in if-else without braces */
#define BAD_SWAP(a, b) { int tmp = a; a = b; b = tmp; }

/* CORRECT: works in all contexts */
#define SWAP(a, b) do { \
    int tmp = (a); \
    (a) = (b); \
    (b) = tmp; \
} while (0)

/* Why? Consider: */
/* if (condition)      */
/*     BAD_SWAP(x, y); */
/* else                */
/*     do_something(); */
/* The else becomes dangling because BAD_SWAP expands to { }; */
```

---

## Predefined Macros: Complete Example

```c
#include <stdio.h>

int main(void) {
    printf("File:      %s\n", __FILE__);
    printf("Line:      %d\n", __LINE__);
    printf("Date:      %s\n", __DATE__);
    printf("Time:      %s\n", __TIME__);
    printf("Function:  %s\n", __func__);  /* C99 */

    #ifdef __STDC__
    printf("Standard C: yes\n");
    #endif

    #ifdef __STDC_VERSION__
    printf("C version: %ldL\n", __STDC_VERSION__);
    /* 199901L = C99, 201112L = C11, 201710L = C17 */
    #endif

    #ifdef __GNUC__
    printf("GCC version: %d.%d.%d\n",
           __GNUC__, __GNUC_MINOR__, __GNUC_PATCHLEVEL__);
    #endif

    return 0;
}
```

---

## Platform-Specific Code with Preprocessor

```c
#include <stdio.h>

/* Detect operating system */
#if defined(_WIN32) || defined(_WIN64)
    #define PLATFORM "Windows"
    #include <windows.h>
    void sleep_ms(int ms) { Sleep(ms); }
#elif defined(__linux__)
    #define PLATFORM "Linux"
    #include <unistd.h>
    void sleep_ms(int ms) { usleep(ms * 1000); }
#elif defined(__APPLE__)
    #define PLATFORM "macOS"
    #include <unistd.h>
    void sleep_ms(int ms) { usleep(ms * 1000); }
#else
    #define PLATFORM "Unknown"
    void sleep_ms(int ms) { (void)ms; }
#endif

/* Detect architecture */
#if defined(__x86_64__) || defined(_M_X64)
    #define ARCH "x86_64"
#elif defined(__i386__) || defined(_M_IX86)
    #define ARCH "x86"
#elif defined(__aarch64__)
    #define ARCH "ARM64"
#else
    #define ARCH "Unknown"
#endif

int main(void) {
    printf("Platform: %s\n", PLATFORM);
    printf("Architecture: %s\n", ARCH);
    return 0;
}
```

---

## Conclusion

- The preprocessor is a powerful tool
- Key features:
    - File inclusion
    - Macro expansion
    - Conditional compilation
- Use `do { } while(0)` for multi-statement macros
- X-macros keep enum and string tables synchronized
- Use `#pragma once` or include guards to prevent double inclusion
- Use with caution and follow best practices
- Balance between preprocessor and language features
