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
# Modern C: C11, C17, and C23

---

## C Standards Timeline

```misc
1972    1989    1999    2011    2018    2024
  |       |       |       |       |       |
  K&R    C89     C99     C11     C17     C23
         ANSI    ISO     ISO     ISO     ISO
```

| Standard | Key Additions |
|----------|--------------|
| C89/C90 | First standard, function prototypes |
| C99 | `//` comments, VLAs, `_Bool`, `<stdint.h>`, designated initializers |
| C11 | `_Generic`, `_Static_assert`, `_Atomic`, `_Thread_local`, anonymous structs |
| C17 | Bug fixes, no new features |
| C23 | `typeof`, `nullptr`, `constexpr`, `#embed`, `auto`, digit separators |

---

## C Standards Timeline

![C standards evolution from K&R to C23 with key features per standard](svg/courses/languages/c/c-refresher/15_modern_c/c_standards_timeline.svg)

---

## Designated Initializers (C99)

```c
#include <stdio.h>

struct Config {
    int port;
    int max_connections;
    int timeout_ms;
    int backlog;
    int verbose;
};

int main(void) {
    /* Initialize specific fields by name, rest default to 0 */
    struct Config server = {
        .port = 8080,
        .max_connections = 100,
        .timeout_ms = 5000,
        /* .backlog and .verbose default to 0 */
    };

    /* Array designated initializers */
    int status_codes[600] = {
        [200] = 1,  /* OK */
        [301] = 1,  /* Moved */
        [404] = 1,  /* Not Found */
        [500] = 1,  /* Server Error */
    };

    printf("Port: %d, Max: %d, Timeout: %d ms\n",
           server.port, server.max_connections, server.timeout_ms);
    printf("status[200] = %d, status[404] = %d, status[0] = %d\n",
           status_codes[200], status_codes[404], status_codes[0]);

    return 0;
}
```

---

## Compound Literals (C99)

```c
#include <stdio.h>

struct Point {
    double x;
    double y;
};

double distance(struct Point a, struct Point b) {
    double dx = a.x - b.x;
    double dy = a.y - b.y;
    return dx * dx + dy * dy;  /* squared distance */
}

void process_array(const int *arr, int n) {
    for (int i = 0; i < n; i++) printf("%d ", arr[i]);
    printf("\n");
}

int main(void) {
    /* Pass a struct literal directly -- no need for a variable */
    double d = distance(
        (struct Point){0.0, 0.0},
        (struct Point){3.0, 4.0}
    );
    printf("Distance squared: %.1f\n", d);

    /* Pass an array literal */
    process_array((int[]){10, 20, 30, 40, 50}, 5);

    /* Compound literal as a pointer */
    int *ptr = (int[]){100, 200, 300};
    printf("ptr[1] = %d\n", ptr[1]);

    return 0;
}
```

---

## _Generic: Type-Generic Macros (C11)

```c
#include <stdio.h>
#include <math.h>

/* _Generic selects an expression based on the type of the first argument */
#define type_name(x) _Generic((x), \
    int:         "int",            \
    float:       "float",          \
    double:      "double",         \
    char *:      "char *",         \
    const char *:"const char *",   \
    default:     "unknown"         \
)

/* Type-generic abs function */
#define generic_abs(x) _Generic((x), \
    int:    abs,                      \
    long:   labs,                     \
    float:  fabsf,                    \
    double: fabs                      \
)(x)

/* Type-generic print */
#define print_val(x) _Generic((x),    \
    int:    printf("%d\n", (x)),      \
    float:  printf("%f\n", (x)),      \
    double: printf("%f\n", (x)),      \
    char *: printf("%s\n", (x))       \
)

int main(void) {
    int i = -42;
    double d = -3.14;
    float f = -2.5f;

    printf("Type of i: %s\n", type_name(i));   /* int */
    printf("Type of d: %s\n", type_name(d));   /* double */
    printf("Type of \"hi\": %s\n", type_name("hi")); /* char * */

    printf("abs(%d) = %d\n", i, generic_abs(i));
    printf("abs(%.2f) = %.2f\n", d, generic_abs(d));

    print_val(42);
    print_val(3.14);
    print_val("Hello, _Generic!");

    return 0;
}
```

---

## _Static_assert: Compile-Time Checks (C11)

```c
#include <stdio.h>
#include <stdint.h>
#include <limits.h>

/* Verify assumptions at compile time -- no runtime cost */
_Static_assert(sizeof(int) >= 4,
    "This code requires int to be at least 32 bits");

_Static_assert(sizeof(void *) == 8,
    "This code requires a 64-bit platform");

_Static_assert(CHAR_BIT == 8,
    "This code requires 8-bit bytes");

struct Packet {
    uint8_t  type;
    uint8_t  flags;
    uint16_t length;
    uint32_t payload;
};

/* Ensure struct has expected size (no unexpected padding) */
_Static_assert(sizeof(struct Packet) == 8,
    "Packet struct must be exactly 8 bytes");

int main(void) {
    /* In C23, you can use static_assert (without underscore) */
    /* static_assert(1 + 1 == 2, "math is broken"); */

    /* C23 also allows static_assert without message */
    /* static_assert(sizeof(int) == 4); */

    printf("All compile-time assertions passed.\n");
    printf("sizeof(Packet) = %zu\n", sizeof(struct Packet));
    return 0;
}
```

If an assertion fails:

```misc
error: static assertion failed: "This code requires a 64-bit platform"
```

---

## _Atomic: Lock-Free Atomics (C11)

```c
#include <stdio.h>
#include <stdatomic.h>
#include <pthread.h>

_Atomic int counter = 0;

void *increment(void *arg) {
    (void)arg;
    for (int i = 0; i < 1000000; i++) {
        atomic_fetch_add(&counter, 1);
        /* Equivalent to counter++ but thread-safe */
    }
    return NULL;
}

int main(void) {
    pthread_t threads[4];

    for (int i = 0; i < 4; i++) {
        pthread_create(&threads[i], NULL, increment, NULL);
    }
    for (int i = 0; i < 4; i++) {
        pthread_join(threads[i], NULL);
    }

    printf("Counter = %d (expected 4000000)\n",
           atomic_load(&counter));

    return 0;
}
```

Compile: `gcc -std=c11 -pthread -o atomic atomic.c`

---

## Atomic Operations Reference

| Operation | Description |
|-----------|-------------|
| `atomic_store(&a, val)` | Store value |
| `atomic_load(&a)` | Load value |
| `atomic_fetch_add(&a, n)` | Add and return old value |
| `atomic_fetch_sub(&a, n)` | Subtract and return old value |
| `atomic_fetch_or(&a, n)` | OR and return old value |
| `atomic_fetch_and(&a, n)` | AND and return old value |
| `atomic_exchange(&a, val)` | Swap and return old value |
| `atomic_compare_exchange_strong(&a, &exp, val)` | CAS operation |

Memory orderings:

| Order | Description |
|-------|-------------|
| `memory_order_relaxed` | No ordering (fastest) |
| `memory_order_acquire` | Load barrier |
| `memory_order_release` | Store barrier |
| `memory_order_seq_cst` | Full barrier (default) |

---

## _Thread_local: Thread-Local Storage (C11)

```c
#include <stdio.h>
#include <pthread.h>

/* Each thread gets its own copy of this variable */
_Thread_local int thread_id = 0;
_Thread_local int call_count = 0;

void process(void) {
    call_count++;
    printf("Thread %d: call #%d\n", thread_id, call_count);
}

void *worker(void *arg) {
    thread_id = *(int *)arg;
    for (int i = 0; i < 3; i++) {
        process();
    }
    return NULL;
}

int main(void) {
    pthread_t threads[3];
    int ids[] = {1, 2, 3};

    for (int i = 0; i < 3; i++) {
        pthread_create(&threads[i], NULL, worker, &ids[i]);
    }
    for (int i = 0; i < 3; i++) {
        pthread_join(threads[i], NULL);
    }

    return 0;
}
```

Each thread independently counts from 1 to 3.

---

## Anonymous Structs and Unions (C11)

```c
#include <stdio.h>

struct Vector3D {
    union {
        struct { float x, y, z; };          /* anonymous struct */
        struct { float r, g, b; };          /* another view */
        float components[3];                 /* array view */
    };                                       /* anonymous union */
};

int main(void) {
    struct Vector3D v = { .x = 1.0f, .y = 2.0f, .z = 3.0f };

    /* Access as position */
    printf("Position: (%.1f, %.1f, %.1f)\n", v.x, v.y, v.z);

    /* Access as color */
    printf("Color: (%.1f, %.1f, %.1f)\n", v.r, v.g, v.b);

    /* Access as array */
    for (int i = 0; i < 3; i++) {
        printf("components[%d] = %.1f\n", i, v.components[i]);
    }

    /* All refer to the same memory */
    v.components[0] = 10.0f;
    printf("After array write: x = %.1f\n", v.x);  /* 10.0 */

    return 0;
}
```

---

## VLAs: Pros and Cons (C99, Optional in C11+)

```c
#include <stdio.h>
#include <string.h>

/* VLAs are useful for variable-size stack arrays */
void zero_matrix(int rows, int cols) {
    int matrix[rows][cols];  /* VLA on stack */
    memset(matrix, 0, sizeof(matrix));

    /* sizeof works correctly with VLAs */
    printf("Matrix size: %zu bytes\n", sizeof(matrix));

    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            matrix[i][j] = i * cols + j;
            printf("%3d ", matrix[i][j]);
        }
        printf("\n");
    }
}

int main(void) {
    zero_matrix(3, 5);
    return 0;
}
```

| Pro | Con |
|-----|-----|
| Natural syntax for dynamic-size arrays | Stack overflow risk with large sizes |
| `sizeof` works correctly | Cannot detect allocation failure |
| No need for malloc/free | Optional in C11+ |
| Good for small, bounded sizes | Not supported by MSVC |
| Parameters can use earlier params | Harder to analyze statically |

---

## typeof: Type Inference (C23)

```c
#include <stdio.h>

/* In C23, typeof is standardized */
/* Before C23, GCC provided __typeof__ as an extension */

#define MAX(a, b) ({ \
    typeof(a) _a = (a); \
    typeof(b) _b = (b); \
    _a > _b ? _a : _b; \
})

#define SWAP(a, b) do { \
    typeof(a) _tmp = (a); \
    (a) = (b); \
    (b) = _tmp; \
} while (0)

int main(void) {
    int x = 10, y = 20;
    printf("MAX(%d, %d) = %d\n", x, y, MAX(x, y));

    double a = 3.14, b = 2.72;
    printf("MAX(%.2f, %.2f) = %.2f\n", a, b, MAX(a, b));

    SWAP(x, y);
    printf("After SWAP: x=%d, y=%d\n", x, y);

    /* typeof for variable declarations */
    int arr[] = {1, 2, 3};
    typeof(arr[0]) first = arr[0];
    printf("first = %d\n", first);

    return 0;
}
```

Note: `typeof` was a GCC extension (`__typeof__`) for decades before C23.

---

## nullptr: The Null Pointer Constant (C23)

```c
#include <stdio.h>
#include <stddef.h>

/* Before C23: NULL could be (void *)0 or just 0 */
/* This caused ambiguity in _Generic and overloaded macros */

/* C23 introduces nullptr as a dedicated null pointer constant */

#if __STDC_VERSION__ >= 202311L

#define describe(x) _Generic((x), \
    int:        "integer",         \
    nullptr_t:  "null pointer",    \
    int *:      "int pointer",     \
    char *:     "char pointer"     \
)

int main(void) {
    /* nullptr has type nullptr_t, not int */
    printf("Type of nullptr: %s\n", describe(nullptr));
    printf("Type of 42: %s\n", describe(42));

    int *p = nullptr;
    if (p == nullptr) {
        printf("p is null\n");
    }

    return 0;
}

#else

int main(void) {
    /* Pre-C23 fallback */
    int *p = NULL;
    printf("Using NULL (pre-C23)\n");
    if (p == NULL) {
        printf("p is null\n");
    }
    return 0;
}

#endif
```

---

## constexpr: Compile-Time Constants (C23)

```c
#include <stdio.h>

/* C23 constexpr: truly compile-time constants */
/* Unlike const, constexpr values MUST be computable at compile time */

#if __STDC_VERSION__ >= 202311L

constexpr int MAX_SIZE = 1024;
constexpr double PI = 3.14159265358979323846;
constexpr int TABLE_SIZE = MAX_SIZE / 4;

/* constexpr can be used in array dimensions */
int buffer[MAX_SIZE];
int lookup[TABLE_SIZE];

int main(void) {
    printf("MAX_SIZE = %d\n", MAX_SIZE);
    printf("PI = %.15f\n", PI);
    printf("TABLE_SIZE = %d\n", TABLE_SIZE);

    /* constexpr in local scope */
    constexpr int ITEMS = 10;
    int data[ITEMS];

    for (int i = 0; i < ITEMS; i++) {
        data[i] = i * i;
    }

    return 0;
}

#else

/* Pre-C23: use #define or enum for compile-time constants */
#define MAX_SIZE 1024
enum { TABLE_SIZE = MAX_SIZE / 4 };

int main(void) {
    printf("MAX_SIZE = %d\n", MAX_SIZE);
    printf("TABLE_SIZE = %d\n", TABLE_SIZE);
    return 0;
}

#endif
```

---

## auto Type Inference (C23)

```c
#include <stdio.h>

/* C23 introduces auto for type inference (like C++ auto) */

#if __STDC_VERSION__ >= 202311L

int main(void) {
    auto x = 42;          /* deduced as int */
    auto pi = 3.14;       /* deduced as double */
    auto ch = 'A';        /* deduced as int (character literal) */

    /* auto with pointers */
    int arr[] = {1, 2, 3};
    auto ptr = arr;        /* deduced as int * */

    printf("x=%d, pi=%f, ch=%c\n", x, pi, (char)ch);
    printf("ptr[0]=%d\n", ptr[0]);

    return 0;
}

#else

int main(void) {
    /* Pre-C23: must write types explicitly */
    int x = 42;
    double pi = 3.14;
    printf("x=%d, pi=%f\n", x, pi);
    return 0;
}

#endif
```

---

## Digit Separators (C23)

```c
#include <stdio.h>
#include <stdint.h>

#if __STDC_VERSION__ >= 202311L

int main(void) {
    /* Digit separators improve readability of large numbers */
    int million = 1'000'000;
    long long gdp = 25'000'000'000'000LL;
    double avogadro = 6.022'140'76e23;

    /* Hex with separators */
    uint32_t color = 0xFF'80'00'FF;
    uint32_t mask = 0b1111'0000'1111'0000;

    printf("Million: %d\n", million);
    printf("GDP: %lld\n", gdp);
    printf("Avogadro: %e\n", avogadro);
    printf("Color: 0x%08X\n", color);
    printf("Mask: 0x%04X\n", mask);

    return 0;
}

#else

int main(void) {
    int million = 1000000;
    printf("Million: %d (no separators pre-C23)\n", million);
    return 0;
}

#endif
```

---

## #embed: Binary Data Inclusion (C23)

```c
#include <stdio.h>

#if __STDC_VERSION__ >= 202311L

/* Embed a file's contents directly as an array initializer */
const unsigned char icon[] = {
    #embed "icon.png"
};

/* With limit */
const unsigned char header[] = {
    #embed "large_file.dat" limit(64)
};

int main(void) {
    printf("Icon size: %zu bytes\n", sizeof(icon));
    printf("Header (first 64 bytes) of large file\n");

    for (size_t i = 0; i < sizeof(header); i++) {
        printf("%02X ", header[i]);
        if ((i + 1) % 16 == 0) printf("\n");
    }
    return 0;
}

#else

/* Pre-C23: use xxd or bin2c to convert binary to C array */
/* Or use linker tricks with objcopy */

int main(void) {
    printf("#embed not available before C23\n");
    printf("Use: xxd -i file.bin > file_data.h\n");
    return 0;
}

#endif
```

---

## Compile-Time Feature Detection

```c
#include <stdio.h>

int main(void) {
    printf("C Standard Version: ");

    #if __STDC_VERSION__ >= 202311L
        printf("C23\n");
    #elif __STDC_VERSION__ >= 201710L
        printf("C17\n");
    #elif __STDC_VERSION__ >= 201112L
        printf("C11\n");
    #elif __STDC_VERSION__ >= 199901L
        printf("C99\n");
    #elif defined(__STDC__)
        printf("C89/C90\n");
    #else
        printf("Pre-standard\n");
    #endif

    /* Check for optional features (C11+) */
    #ifdef __STDC_NO_VLA__
        printf("VLAs: NOT supported\n");
    #else
        printf("VLAs: supported\n");
    #endif

    #ifdef __STDC_NO_ATOMICS__
        printf("Atomics: NOT supported\n");
    #else
        printf("Atomics: supported\n");
    #endif

    #ifdef __STDC_NO_THREADS__
        printf("Threads: NOT supported\n");
    #else
        printf("Threads: supported\n");
    #endif

    return 0;
}
```

---

## Modern C Idioms Summary

| Old Way | Modern Way | Since |
|---------|-----------|-------|
| `#define MAX 100` | `enum { MAX = 100 };` or `constexpr int MAX = 100;` | C23 |
| `(void *)0` or `0` | `nullptr` | C23 |
| Explicit types | `auto x = expr;` | C23 |
| `xxd -i file.bin` | `#embed "file.bin"` | C23 |
| `#define ABS(x) ...` | `_Generic` dispatch | C11 |
| Runtime assertion | `_Static_assert` | C11 |
| `volatile` flag | `_Atomic` variable | C11 |
| Global thread state | `_Thread_local` | C11 |
| `struct s = {0, 0, 0}` | `struct s = {.field = val}` | C99 |
| Declare at top of block | Declare where needed | C99 |

---

## Summary

- C11 brought `_Generic` for type-generic macros, `_Static_assert` for compile-time checks, `_Atomic` for lock-free atomics, and anonymous structs/unions
- C17 was primarily a bug-fix release with no new features
- C23 adds `typeof`, `nullptr`, `constexpr`, `auto`, digit separators, and `#embed`
- Use designated initializers and compound literals for clearer initialization
- VLAs are convenient but optional since C11 -- use with care
- Always check `__STDC_VERSION__` for feature availability
- Modern C is expressive and safe when you use its features properly
- Compile with `-std=c11` (minimum) or `-std=c23` to access modern features
