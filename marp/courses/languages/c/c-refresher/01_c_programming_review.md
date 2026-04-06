# C Programming Review

---

## Introduction to C

![h:300](../../../../raw/dennis_ritchie.jpg)

- Developed by Dennis Ritchie at Bell Labs in 1972
- Widely used in embedded systems, operating systems, and application development
- Known for efficiency and low-level control

---

## C Standards

- C89/C90: First standardized version
- C99: Added new features like inline functions, variable-length arrays
- C11: Added multi-threading support, anonymous structures
- C17: Bug fixes and clarifications

---

## Basic C Program Structure

```c
#include <stdio.h>
#include <stdlib.h>

int main() {
    printf("Hello, World!\n");
    return EXIT_SUCCESS;
}
```

Compile and run:

```bash
gcc hello.c -o hello
./hello
```

---

## C23: The Latest Standard

- C23 (ISO/IEC 9899:2024) is the newest C standard
- Key additions:
    - `nullptr` keyword (replaces `NULL` in many contexts)
    - `constexpr` for compile-time constants
    - `typeof` operator standardized
    - `#embed` directive for binary data
    - Digit separators: `1'000'000`
- Compiler support: GCC 14+, Clang 18+

```bash
gcc -std=c23 program.c -o program
```

---

## The C Compilation Pipeline

<svg xmlns="http://www.w3.org/2000/svg" width="700" height="120" font-family="sans-serif">
  <defs>
    <marker id="arr" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#555"/>
    </marker>
  </defs>
  <!-- Source box -->
  <rect x="5" y="10" width="100" height="40" fill="#e3f2fd" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="55" y="27" font-size="12" font-weight="bold" fill="#222" text-anchor="middle">Source</text>
  <text x="55" y="43" font-size="11" fill="#555" text-anchor="middle">(.c / .h)</text>
  <text x="55" y="65" font-size="11" fill="#777" text-anchor="middle">#include</text>
  <text x="55" y="78" font-size="11" fill="#777" text-anchor="middle">#define</text>
  <text x="55" y="91" font-size="11" fill="#777" text-anchor="middle">#ifdef</text>
  <!-- arrow -->
  <line x1="105" y1="30" x2="120" y2="30" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <!-- Preprocessor box -->
  <rect x="122" y="10" width="110" height="40" fill="#e8f5e9" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="177" y="27" font-size="12" font-weight="bold" fill="#222" text-anchor="middle">Preprocessor</text>
  <text x="177" y="43" font-size="11" fill="#555" text-anchor="middle">(cpp)</text>
  <!-- arrow -->
  <line x1="232" y1="30" x2="247" y2="30" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <!-- Compiler box -->
  <rect x="249" y="10" width="100" height="40" fill="#fff3e0" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="299" y="27" font-size="12" font-weight="bold" fill="#222" text-anchor="middle">Compiler</text>
  <text x="299" y="43" font-size="11" fill="#555" text-anchor="middle">(cc1)</text>
  <text x="299" y="65" font-size="11" fill="#777" text-anchor="middle">.s</text>
  <text x="299" y="78" font-size="11" fill="#777" text-anchor="middle">assembly</text>
  <!-- arrow -->
  <line x1="349" y1="30" x2="364" y2="30" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <!-- Assembler box -->
  <rect x="366" y="10" width="100" height="40" fill="#fce4ec" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="416" y="27" font-size="12" font-weight="bold" fill="#222" text-anchor="middle">Assembler</text>
  <text x="416" y="43" font-size="11" fill="#555" text-anchor="middle">(as)</text>
  <text x="416" y="65" font-size="11" fill="#777" text-anchor="middle">.o</text>
  <text x="416" y="78" font-size="11" fill="#777" text-anchor="middle">object</text>
  <text x="416" y="91" font-size="11" fill="#777" text-anchor="middle">files</text>
  <!-- arrow -->
  <line x1="466" y1="30" x2="481" y2="30" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <!-- Linker box -->
  <rect x="483" y="10" width="100" height="40" fill="#ede7f6" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="533" y="27" font-size="12" font-weight="bold" fill="#222" text-anchor="middle">Linker</text>
  <text x="533" y="43" font-size="11" fill="#555" text-anchor="middle">(ld)</text>
  <text x="533" y="65" font-size="11" fill="#777" text-anchor="middle">executable</text>
</svg>

View each stage:

```bash
gcc -E hello.c -o hello.i      # Preprocessor output
gcc -S hello.c -o hello.s      # Assembly output
gcc -c hello.c -o hello.o      # Object file
gcc hello.o -o hello           # Linked executable
```

---

## Anatomy of a C Program

```c
/* 1. Preprocessor directives */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* 2. Type definitions and macros */
#define MAX_NAME 64
typedef unsigned int uint;

/* 3. Function prototypes (declarations) */
static void greet(const char *name);

/* 4. Global variables (use sparingly!) */
static int call_count = 0;

/* 5. Function definitions */
static void greet(const char *name) {
    call_count++;
    printf("Hello, %s! (call #%d)\n", name, call_count);
}

/* 6. Entry point */
int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stderr, "Usage: %s <name>\n", argv[0]);
        return EXIT_FAILURE;
    }
    greet(argv[1]);
    return EXIT_SUCCESS;
}
```

---

## Compiler Flags You Should Always Use

| Flag | Purpose |
|------|---------|
| `-Wall` | Enable most common warnings |
| `-Wextra` | Enable additional warnings |
| `-Werror` | Treat warnings as errors |
| `-std=c11` | Use C11 standard |
| `-pedantic` | Strict ISO C compliance |
| `-O2` | Optimization level 2 |
| `-g` | Include debug information |
| `-fsanitize=address` | AddressSanitizer (ASan) |
| `-fsanitize=undefined` | UndefinedBehaviorSanitizer (UBSan) |

Recommended development command:

```bash
gcc -Wall -Wextra -Werror -std=c11 -pedantic -g \
    -fsanitize=address,undefined program.c -o program
```

---

## Undefined Behavior: The Silent Killer

Undefined behavior (UB) means the C standard imposes no requirements.
The compiler may do **anything** -- including "working correctly" sometimes.

Common sources of UB:

```c
/* 1. Signed integer overflow */
int x = INT_MAX;
x = x + 1;  /* UB! */

/* 2. Dereferencing NULL */
int *p = NULL;
*p = 42;     /* UB! */

/* 3. Out-of-bounds array access */
int arr[5];
arr[10] = 0; /* UB! */

/* 4. Using uninitialized variables */
int y;
printf("%d\n", y);  /* UB! */

/* 5. Double free */
int *q = malloc(sizeof(int));
free(q);
free(q);     /* UB! */
```

---

## Implementation-Defined vs Unspecified vs Undefined

| Category | Meaning | Example |
|----------|---------|---------|
| **Defined** | Standard specifies exactly | `sizeof(char)` is always 1 |
| **Implementation-defined** | Compiler chooses, must document | Size of `int` |
| **Unspecified** | Compiler chooses, need not document | Order of function argument evaluation |
| **Undefined** | Anything can happen | Signed integer overflow |

---

## The `main` Function Signatures

Valid signatures for `main`:

```c
/* Standard: no arguments */
int main(void) {
    return 0;
}

/* Standard: with command-line arguments */
int main(int argc, char *argv[]) {
    for (int i = 0; i < argc; i++) {
        printf("argv[%d] = %s\n", i, argv[i]);
    }
    return 0;
}

/* Also valid (equivalent) */
int main(int argc, char **argv) {
    return 0;
}
```

Note: `void main()` is **not** standard C. Always return `int`.

---

## Return Values and Exit Codes

```c
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    FILE *f = fopen("config.txt", "r");
    if (f == NULL) {
        perror("fopen");
        return EXIT_FAILURE;  /* value 1 on most systems */
    }
    /* process file... */
    fclose(f);
    return EXIT_SUCCESS;      /* value 0 */
}
```

Check exit code in shell:

```bash
./program
echo $?   # prints 0 on success, non-zero on failure
```

---

## Summary

- C has evolved through multiple standards: C89, C99, C11, C17, C23
- The compilation pipeline has four stages: preprocess, compile, assemble, link
- Always use warning flags (`-Wall -Wextra -Werror`) during development
- Understand the difference between undefined, unspecified, and implementation-defined behavior
- The `main` function should always return `int`
- Use `EXIT_SUCCESS` and `EXIT_FAILURE` for portable exit codes
