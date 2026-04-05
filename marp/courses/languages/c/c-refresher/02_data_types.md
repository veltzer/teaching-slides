# C Data Types Refresher

---

## Basic Data Types in C

C provides several basic data types:

- Integer types
- Floating-point types
- Character type
- Void type

---

## Integer Types

- Used to store whole numbers
- Various sizes available:
    - `char`: 1 byte
    - `short`: 2 bytes
    - `int`: 2 or 4 bytes (usually 4)
    - `long`: 4 or 8 bytes
    - `long long`: 8 bytes (C99 and later)

```c
int a = 10;
long long big_num = 1234567890123456789LL;
```

---

## Integer Modifiers

- `signed`: Can represent positive and negative numbers (default)
- `unsigned`: Can only represent non-negative numbers

```c
unsigned int positive = 4294967295U;
signed char small = -128;
```

---

## Floating-Point Types

- Used to store decimal numbers
- Three types available:
    - `float`: Single precision (4 bytes)
    - `double`: Double precision (8 bytes)
    - `long double`: Extended precision (at least 10 bytes, often 16)

```c
float pi = 3.14159F;
double e = 2.71828;
long double big_pi = 3.141592653589793238L;
```

---

## Character Type

- Used to store a single character
- Typically 1 byte in size
- Represented by `char`

```c
char grade = 'A';
char newline = '\n';
```

---

## Void Type

- Represents the absence of a value
- Used in three ways:
    1. Function returns nothing
    1. Function takes no parameters
    1. Generic pointer type

```c
void print_hello(void) {
    printf("Hello, World!\n");
}

void *generic_ptr;
```

---

## Derived Data Types

C also provides several derived data types:

- Arrays
- Pointers
- Structures
- Unions
- Enumerations

---

## Arrays

- Collection of elements of the same type
- Index-based access (starting from 0)

```c
int numbers[5] = {1, 2, 3, 4, 5};
char name[] = "John";  // Null-terminated string
```

---

## Pointers

- Store memory addresses of variables
- Declared using the `*` operator

```c
int x = 10;
int *ptr = &x;
printf("Value of x: %d\n", *ptr);  // Dereference
```

---

## Structures

- Group related data of different types
- Defined using the `struct` keyword

```c
struct Point {
    int x;
    int y;
};

struct Point p1 = {10, 20};
```

---

## Unions

- Store different data types in the same memory location
- Only one member can hold a value at a time

```c
union Data {
    int i;
    float f;
    char str[20];
};

union Data data;
data.i = 10;
```

---

## Enumerations

- User-defined type consisting of named integer constants
- Defined using the `enum` keyword

```c
enum Days {MON, TUE, WED, THU, FRI, SAT, SUN};
enum Days today = WED;
```

---

## Type Qualifiers

- `const`: Value cannot be changed after initialization
- `volatile`: Value may change unexpectedly
- `restrict`: Pointer is the only way to access an object (C99)

```c
const int MAX_SIZE = 100;
volatile int sensor_value;
int *restrict ptr = malloc(sizeof(int));
```

---

## Type Conversion

- Implicit conversion: Automatically done by the compiler
- Explicit conversion: Done by the programmer using typecasting

```c
int i = 10;
float f = 3.14;
double d = (double)i + f;  // Explicit conversion of i to double
```

---

## sizeof Operator

- Returns the size of a data type in bytes
- Useful for portable code and dynamic memory allocation

```c
printf("Size of int: %zu bytes\n", sizeof(int));
printf("Size of float: %zu bytes\n", sizeof(float));
```

---

## Complete sizeof Example

```c
#include <stdio.h>

int main(void) {
    printf("%-20s %zu bytes\n", "char",        sizeof(char));
    printf("%-20s %zu bytes\n", "short",       sizeof(short));
    printf("%-20s %zu bytes\n", "int",         sizeof(int));
    printf("%-20s %zu bytes\n", "long",        sizeof(long));
    printf("%-20s %zu bytes\n", "long long",   sizeof(long long));
    printf("%-20s %zu bytes\n", "float",       sizeof(float));
    printf("%-20s %zu bytes\n", "double",      sizeof(double));
    printf("%-20s %zu bytes\n", "long double", sizeof(long double));
    printf("%-20s %zu bytes\n", "void *",      sizeof(void *));
    return 0;
}
```

Typical output on x86-64 Linux:

```txt
char                 1 bytes
short                2 bytes
int                  4 bytes
long                 8 bytes
long long            8 bytes
float                4 bytes
double               8 bytes
long double          16 bytes
void *               8 bytes
```

---

## Fixed-Width Integer Types (C99)

The `<stdint.h>` header provides types with guaranteed sizes:

| Type | Width | Signed Range |
|------|-------|-------------|
| `int8_t` | 8 bits | -128 to 127 |
| `int16_t` | 16 bits | -32768 to 32767 |
| `int32_t` | 32 bits | -2^31 to 2^31-1 |
| `int64_t` | 64 bits | -2^63 to 2^63-1 |
| `uint8_t` | 8 bits | 0 to 255 |
| `uint16_t` | 16 bits | 0 to 65535 |
| `uint32_t` | 32 bits | 0 to 2^32-1 |
| `uint64_t` | 64 bits | 0 to 2^64-1 |

```c
#include <stdint.h>
#include <stdio.h>
#include <inttypes.h>

int main(void) {
    uint32_t ip_addr = 0xC0A80001;  /* 192.168.0.1 */
    int64_t big = INT64_MAX;
    printf("IP: 0x%08" PRIX32 "\n", ip_addr);
    printf("Big: %" PRId64 "\n", big);
    return 0;
}
```

---

## Integer Promotion Rules

When integers of different types are mixed in expressions, C promotes them:

```txt
┌─────────────────────────────────────────────┐
│         Implicit Conversion Hierarchy       │
│                                             │
│  long double                                │
│       ^                                     │
│     double                                  │
│       ^                                     │
│     float                                   │
│       ^                                     │
│  unsigned long long                         │
│       ^                                     │
│    long long                                │
│       ^                                     │
│  unsigned long                              │
│       ^                                     │
│     long                                    │
│       ^                                     │
│  unsigned int                               │
│       ^                                     │
│     int  <-- char, short promoted to here   │
└─────────────────────────────────────────────┘
```

---

## Dangerous Implicit Conversions

```c
#include <stdio.h>

int main(void) {
    /* Pitfall 1: signed/unsigned comparison */
    int a = -1;
    unsigned int b = 1;
    if (a < b) {
        printf("Expected: -1 < 1\n");
    } else {
        printf("Surprise: -1 >= 1 (unsigned comparison!)\n");
    }
    /* -1 is converted to UINT_MAX (4294967295), which is > 1 */

    /* Pitfall 2: truncation */
    int big = 100000;
    short small = big;  /* may truncate silently */
    printf("big=%d, small=%d\n", big, small);

    /* Pitfall 3: float to int truncation */
    double pi = 3.99;
    int rounded = pi;  /* truncates to 3, not 4 */
    printf("pi=%f, rounded=%d\n", pi, rounded);

    return 0;
}
```

---

## Boolean Type (C99)

```c
#include <stdbool.h>
#include <stdio.h>

int main(void) {
    bool is_ready = true;
    bool is_empty = false;

    if (is_ready && !is_empty) {
        printf("Processing...\n");
    }

    /* Before C99, programmers used: */
    /* typedef int bool; */
    /* #define true 1    */
    /* #define false 0   */

    return 0;
}
```

---

## Memory Layout of Data Types

```
┌──────────────────────────────────────────────┐
│  char c = 'A';         (1 byte)              │
│  ┌────┐                                      │
│  │ 41 │  (0x41 = 65 = 'A')                   │
│  └────┘                                      │
│                                              │
│  int x = 0x12345678;   (4 bytes, little-endian) │
│  ┌────┬────┬────┬────┐                       │
│  │ 78 │ 56 │ 34 │ 12 │                       │
│  └────┴────┴────┴────┘                       │
│  addr  +1   +2   +3                          │
│                                              │
│  double d = 3.14;      (8 bytes, IEEE 754)   │
│  ┌────┬────┬────┬────┬────┬────┬────┬────┐   │
│  │ 1F │ 85 │ EB │ 51 │ B8 │ 1E │ 09 │ 40 │   │
│  └────┴────┴────┴────┴────┴────┴────┴────┘   │
└──────────────────────────────────────────────┘
```

---

## Floating-Point Pitfalls

```c
#include <stdio.h>
#include <math.h>
#include <float.h>

int main(void) {
    /* Pitfall 1: equality comparison */
    double a = 0.1 + 0.2;
    double b = 0.3;
    printf("0.1 + 0.2 == 0.3? %s\n",
           (a == b) ? "yes" : "NO!");  /* prints NO! */

    /* Correct approach: use epsilon comparison */
    if (fabs(a - b) < DBL_EPSILON * 10) {
        printf("Approximately equal\n");
    }

    /* Pitfall 2: precision loss with large + small */
    float big = 1e10f;
    float small = 1.0f;
    printf("big + small - big = %f\n",
           (big + small) - big);  /* may print 0.000000 */

    /* Pitfall 3: NaN and infinity */
    double inf = 1.0 / 0.0;
    double nan = 0.0 / 0.0;
    printf("inf=%f, nan=%f\n", inf, nan);
    printf("nan == nan? %s\n",
           (nan == nan) ? "yes" : "NO!");  /* NO! */

    return 0;
}
```

---

## Format Specifiers Reference Table

| Type | printf | scanf | Notes |
|------|--------|-------|-------|
| `char` | `%c` | `%c` | Single character |
| `int` | `%d` or `%i` | `%d` or `%i` | Signed decimal |
| `unsigned` | `%u` | `%u` | Unsigned decimal |
| `long` | `%ld` | `%ld` | Long signed |
| `unsigned long` | `%lu` | `%lu` | Long unsigned |
| `long long` | `%lld` | `%lld` | Long long signed |
| `float` | `%f` | `%f` | 6 decimal places |
| `double` | `%f` or `%lf` | `%lf` | scanf needs `%lf` |
| `size_t` | `%zu` | `%zu` | Unsigned size |
| `ptrdiff_t` | `%td` | `%td` | Pointer difference |
| `void *` | `%p` | - | Pointer value |
| hex | `%x` / `%X` | `%x` | Hexadecimal |
| octal | `%o` | `%o` | Octal |

---

## typedef: Creating Type Aliases

```c
#include <stdio.h>
#include <stdint.h>

/* Simple alias */
typedef unsigned long ulong;

/* Alias for a struct */
typedef struct {
    double x;
    double y;
} Point;

/* Alias for a function pointer */
typedef int (*Comparator)(const void *, const void *);

/* Alias for a fixed-size buffer */
typedef char Name[64];

int main(void) {
    Point p = {3.0, 4.0};
    Name greeting = "Hello";
    printf("Point: (%.1f, %.1f)\n", p.x, p.y);
    printf("Name: %s\n", greeting);
    return 0;
}
```

---

## Summary

- C provides basic types: integers, floating-point, characters, and void
- Derived types include arrays, pointers, structures, unions, and enums
- Use `<stdint.h>` for fixed-width integer types in portable code
- Be aware of implicit conversions and integer promotion rules
- Never compare floating-point numbers with `==`
- Use `typedef` to create meaningful type aliases
- Use appropriate format specifiers for each type
- Be aware of type sizes and conversions for efficient and correct code
