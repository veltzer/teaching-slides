---
tags:
  - languages:c
  - concepts:programming
  - concepts:memory-management
  - concepts:pointers
level: intermediate
category: language
audience:
  - audiences:developers

---
# C Syntax Refresher

---

## C Program Structure

![C Program Structure](svg/courses/languages/c/c-refresher/03_syntax/c_program_structure.svg)

---

## Basic Program Structure

A simple C program consists of:

```c
#include <stdio.h>

int main() {
    // Your code here
    return 0;
}
```

- `#include`: Preprocessor directive
- `main()`: Entry point of the program
- `{}`: Block of code
- `return 0;`: Indicates successful program execution

---

## Comments

- Single-line comments: `// This is a comment`
- Multi-line comments: `/* This is a multi-line comment */`

```c
// This is a single-line comment

/* This is a
   multi-line comment */
```

---

## Variables and Constants

- Variables: `type name = value;`
- Constants: `const type NAME = value;`

```c
int age = 25;
const float PI = 3.14159;
```

---

## Data Types

Basic data types:
- `int`: Integer
- `float`: Single-precision floating-point
- `double`: Double-precision floating-point
- `char`: Single character

```c
int count = 10;
float price = 9.99;
char grade = 'A';
```

---

## Operators

- Arithmetic: `+`, `-`, `*`, `/`, `%`
- Comparison: `==`, `!=`, `<`, `>`, `<=`, `>=`
- Logical: `&&` (AND), `||` (OR), `!` (NOT)
- Assignment: `=`, `+=`, `-=`, `*=`, `/=`, `%=`

```c
int a = 5, b = 3;
int sum = a + b;
int is_equal = (a == b);
```

---

## Control Structures: if-else

```c
if (condition) {
    // Code to execute if condition is true
} else if (another_condition) {
    // Code to execute if another_condition is true
} else {
    // Code to execute if all conditions are false
}
```

Example:

```c
if (score >= 90) {
    printf("Grade: A");
} else if (score >= 80) {
    printf("Grade: B");
} else {
    printf("Grade: C");
}
```

---

## Control Structures: switch

```c
switch (expression) {
    case constant1:
        // Code to execute for constant1
        break;
    case constant2:
        // Code to execute for constant2
        break;
    default:
        // Code to execute if no match is found
}
```

Example:

```c
switch (day) {
    case 1:
        printf("Monday");
        break;
    case 2:
        printf("Tuesday");
        break;
    default:
        printf("Other day");
}
```

---

## Loops: for

```c
for (initialization; condition; update) {
    // Code to repeat
}
```

Example:

```c
for (int i = 0; i < 5; i++) {
    printf("%d ", i);
}
```

---

## Loops: while and do-while

While loop:

```c
while (condition) {
    // Code to repeat
}
```

Do-while loop:

```c
do {
    // Code to repeat
} while (condition);
```

Example:

```c
int i = 0;
while (i < 5) {
    printf("%d ", i);
    i++;
}
```

---

## Functions

Function declaration and definition:

```c
return_type function_name(parameter_list) {
    // Function body
    return value;
}
```

Example:

```c
int add(int a, int b) {
    return a + b;
}

int result = add(5, 3);
```

---

## Arrays

Declaration and initialization:

```c
type array_name[size];
type array_name[] = {value1, value2, ...};
```

Example:

```c
int numbers[5] = {1, 2, 3, 4, 5};
char name[] = "John";
```

---

## Pointers

Declaration and usage:

```c
type *pointer_name;
pointer_name = &variable;
```

Example:

```c
int x = 10;
int *ptr = &x;
printf("Value of x: %d", *ptr);
```

---

## Structures

Definition and usage:

```c
struct structure_name {
    type member1;
    type member2;
    // ...
};

struct structure_name variable_name;
```

Example:

```c
struct Person {
    char name[50];
    int age;
};

struct Person p1 = {"Alice", 30};
```

---

## Preprocessor Directives

- `#include`: Include header files
- `#define`: Define macros or constants
- `#ifdef`, `#ifndef`, `#endif`: Conditional compilation

Example:

```c
#include <stdio.h>
#define MAX_SIZE 100

#ifdef DEBUG
    printf("Debug mode on");
#endif
```

---

## Scope and Lifetime

```c
#include <stdio.h>

int global_var = 100;  /* file scope, static lifetime */

void demonstrate_scope(void) {
    static int persist = 0;   /* local scope, static lifetime */
    int local = 42;           /* local scope, automatic lifetime */
    persist++;
    printf("persist=%d, local=%d\n", persist, local);
}

int main(void) {
    demonstrate_scope();  /* persist=1, local=42 */
    demonstrate_scope();  /* persist=2, local=42 */
    demonstrate_scope();  /* persist=3, local=42 */

    /* Block scope (C99+) */
    for (int i = 0; i < 3; i++) {
        int block_var = i * 10;
        printf("block_var=%d\n", block_var);
    }
    /* i and block_var not accessible here */

    return 0;
}
```

---

## Storage Class Specifiers

| Specifier | Scope | Lifetime | Default Value | Typical Use |
|-----------|-------|----------|---------------|-------------|
| `auto` | Block | Automatic | Garbage | Local variables (default) |
| `static` (local) | Block | Static | 0 | Persistent local state |
| `static` (global) | File | Static | 0 | Internal linkage |
| `extern` | Global | Static | 0 | External linkage |
| `register` | Block | Automatic | Garbage | Hint for optimization |

```c
static int file_private = 0;     /* only visible in this file */
extern int shared_across_files;  /* defined elsewhere */
```

---

## Operator Precedence Table (Key Levels)

| Precedence | Operators | Associativity |
|------------|-----------|---------------|
| 1 (highest) | `()` `[]` `->` `.` | Left to right |
| 2 | `!` `~` `++` `--` `+` `-` `*` `&` `(type)` `sizeof` | Right to left |
| 3 | `*` `/` `%` | Left to right |
| 4 | `+` `-` | Left to right |
| 5 | `<<` `>>` | Left to right |
| 6 | `<` `<=` `>` `>=` | Left to right |
| 7 | `==` `!=` | Left to right |
| 8 | `&` | Left to right |
| 9 | `^` | Left to right |
| 10 | `\|` | Left to right |
| 11 | `&&` | Left to right |
| 12 | `\|\|` | Left to right |
| 13 | `?:` | Right to left |
| 14 | `=` `+=` `-=` etc. | Right to left |
| 15 (lowest) | `,` | Left to right |

---

## Operator Precedence Pitfalls

```c
#include <stdio.h>

int main(void) {
    /* Pitfall 1: & vs == */
    int flags = 0x0F;
    if (flags & 0x04 == 0x04) {
        /* WRONG! == has higher precedence than & */
        /* Parsed as: flags & (0x04 == 0x04) => flags & 1 */
    }
    if ((flags & 0x04) == 0x04) {
        /* CORRECT: parentheses force desired order */
        printf("Bit 2 is set\n");
    }

    /* Pitfall 2: ternary and assignment */
    int a = 1, b = 2, c;
    c = a > b ? a : b;  /* OK: c = 2 */

    /* Pitfall 3: comma operator */
    int x = (1, 2, 3);  /* x = 3 (last value) */
    printf("x = %d\n", x);

    return 0;
}
```

---

## The Ternary Operator

```c
#include <stdio.h>

int main(void) {
    int score = 75;

    /* Simple ternary */
    const char *result = (score >= 60) ? "PASS" : "FAIL";
    printf("Result: %s\n", result);

    /* Nested ternary (use sparingly) */
    const char *grade = (score >= 90) ? "A" :
                        (score >= 80) ? "B" :
                        (score >= 70) ? "C" :
                        (score >= 60) ? "D" : "F";
    printf("Grade: %s\n", grade);

    /* Ternary as lvalue (GCC extension, non-standard) */
    int a = 1, b = 2;
    /* Better: use if-else for complex cases */
    if (a > b) {
        printf("a is larger\n");
    } else {
        printf("b is larger\n");
    }

    return 0;
}
```

---

## Goto and Labels (Use with Caution)

```c
#include <stdio.h>
#include <stdlib.h>

/* goto is acceptable for error-handling cleanup in C */
int process_file(const char *filename) {
    FILE *f = NULL;
    char *buf = NULL;
    int result = -1;

    f = fopen(filename, "r");
    if (f == NULL) goto cleanup;

    buf = malloc(1024);
    if (buf == NULL) goto cleanup;

    /* ... process data ... */
    result = 0;  /* success */

cleanup:
    free(buf);
    if (f) fclose(f);
    return result;
}

int main(void) {
    int rc = process_file("test.txt");
    printf("Result: %d\n", rc);
    return 0;
}
```

This pattern is widely used in the Linux kernel.

---

## The Comma Operator

```c
#include <stdio.h>

int main(void) {
    /* In for loops: multiple initializations/updates */
    for (int i = 0, j = 10; i < j; i++, j--) {
        printf("i=%d, j=%d\n", i, j);
    }

    /* Comma operator evaluates left, discards, returns right */
    int x = (printf("side effect\n"), 42);
    printf("x = %d\n", x);  /* x = 42 */

    return 0;
}
```

---

## Compound Literals (C99)

```c
#include <stdio.h>

struct Point {
    int x;
    int y;
};

void print_point(struct Point p) {
    printf("(%d, %d)\n", p.x, p.y);
}

int main(void) {
    /* Pass a struct without declaring a variable */
    print_point((struct Point){10, 20});

    /* Create an array on the fly */
    int *arr = (int[]){1, 2, 3, 4, 5};
    for (int i = 0; i < 5; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");

    return 0;
}
```

---

## Designated Initializers (C99)

```c
#include <stdio.h>

struct Config {
    int width;
    int height;
    int depth;
    int flags;
};

int main(void) {
    /* Initialize specific fields by name */
    struct Config cfg = {
        .width = 1920,
        .height = 1080,
        .flags = 0x01,
        /* .depth defaults to 0 */
    };

    /* Array designated initializers */
    int lookup[256] = {
        ['A'] = 1,
        ['B'] = 2,
        ['C'] = 3,
    };

    printf("Config: %dx%d, flags=0x%x\n",
           cfg.width, cfg.height, cfg.flags);
    printf("lookup['B'] = %d\n", lookup['B']);

    return 0;
}
```

---

## Summary
- C programs have a specific structure with the `main()` function as the entry point
- Variables and constants store data, with various data types available
- Control structures (`if-else`, `switch`) and loops (`for`, `while`) control program flow
- Functions encapsulate reusable code
- Understand operator precedence to avoid subtle bugs -- use parentheses when in doubt
- Scope and storage class determine variable visibility and lifetime
- Use `goto` only for structured cleanup patterns
- C99 introduced compound literals and designated initializers for cleaner code
