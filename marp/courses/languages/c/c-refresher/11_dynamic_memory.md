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

# Dynamic Memory Management in C

---

## Memory Regions in a C Program

![memory_regions_in_a_c_program](svg/courses/languages/c/c-refresher/11_dynamic_memory/memory_regions_in_a_c_program.svg)

---

## Stack vs Heap

| Feature | Stack | Heap |
|---------|-------|------|
| Allocation | Automatic | Manual (malloc/free) |
| Deallocation | Automatic (scope exit) | Manual (free) |
| Speed | Very fast | Slower |
| Size | Limited (1-8 MB typical) | Limited by system RAM |
| Fragmentation | None | Possible |
| Thread safety | Each thread has own stack | Shared, needs sync |
| Lifetime | Function scope | Until free() |

---

## malloc: Allocate Uninitialized Memory

```c
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    /* Allocate space for 10 integers */
    int *arr = malloc(10 * sizeof(int));
    if (arr == NULL) {
        fprintf(stderr, "malloc failed\n");
        return EXIT_FAILURE;
    }

    /* WARNING: memory is NOT initialized! May contain garbage */
    for (int i = 0; i < 10; i++) {
        arr[i] = i * 10;  /* must initialize before reading */
    }

    for (int i = 0; i < 10; i++) {
        printf("arr[%d] = %d\n", i, arr[i]);
    }

    free(arr);
    arr = NULL;  /* prevent use-after-free */
    return EXIT_SUCCESS;
}
```

---

## calloc: Allocate Zero-Initialized Memory

```c
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    /* calloc(count, size) - allocates and zeros memory */
    int *arr = calloc(10, sizeof(int));
    if (arr == NULL) {
        fprintf(stderr, "calloc failed\n");
        return EXIT_FAILURE;
    }

    /* All elements are guaranteed to be 0 */
    for (int i = 0; i < 10; i++) {
        printf("arr[%d] = %d\n", i, arr[i]);  /* all print 0 */
    }

    free(arr);
    return EXIT_SUCCESS;
}
```

malloc vs calloc:

| Feature | `malloc(n)` | `calloc(count, size)` |
|---------|------------|---------------------|
| Initialization | None (garbage) | Zero-filled |
| Overflow check | No | Yes (count * size) |
| Speed | Slightly faster | Slightly slower |
| Use when | You will initialize immediately | You need zeroed memory |

---

## realloc: Resize Allocated Memory

```c
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    int capacity = 4;
    int size = 0;
    int *arr = malloc(capacity * sizeof(int));
    if (arr == NULL) return EXIT_FAILURE;

    /* Simulate dynamic growth */
    for (int i = 0; i < 20; i++) {
        if (size >= capacity) {
            capacity *= 2;
            int *tmp = realloc(arr, capacity * sizeof(int));
            if (tmp == NULL) {
                fprintf(stderr, "realloc failed\n");
                free(arr);  /* free original on failure */
                return EXIT_FAILURE;
            }
            arr = tmp;
            printf("  Grew to capacity %d\n", capacity);
        }
        arr[size++] = i * 10;
    }

    printf("Final array (%d elements, capacity %d):\n", size, capacity);
    for (int i = 0; i < size; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");

    free(arr);
    return EXIT_SUCCESS;
}
```

---

## realloc Pitfalls

```c
/* WRONG: lose original pointer if realloc fails */
int *arr = malloc(100 * sizeof(int));
arr = realloc(arr, 200 * sizeof(int));  /* if NULL, original is leaked! */

/* CORRECT: use a temporary pointer */
int *tmp = realloc(arr, 200 * sizeof(int));
if (tmp == NULL) {
    /* arr is still valid, handle error */
    free(arr);
    return -1;
}
arr = tmp;
```

Special cases:

```c
/* realloc(NULL, size) is equivalent to malloc(size) */
int *p = realloc(NULL, 100);

/* realloc(ptr, 0) is implementation-defined in C11 */
/* Do NOT rely on it to free memory -- use free() explicitly */
```

---

## free: Deallocate Memory

Rules for `free()`:

1. Only free memory allocated by `malloc`/`calloc`/`realloc`
1. Only free each allocation once
1. After free, the pointer is dangling -- do not use it
1. `free(NULL)` is safe and does nothing

```c
#include <stdlib.h>

int main(void) {
    int *p = malloc(sizeof(int));
    if (p == NULL) return 1;
    *p = 42;

    free(p);
    p = NULL;  /* always NULL after free */

    /* Safe: free(NULL) is a no-op */
    free(p);

    return 0;
}
```

---

## Memory Leak: Forgot to Free

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* LEAKY: caller must free, but it is easy to forget */
char *create_greeting(const char *name) {
    size_t len = strlen("Hello, ") + strlen(name) + 2;
    char *buf = malloc(len);
    if (buf == NULL) return NULL;
    snprintf(buf, len, "Hello, %s!", name);
    return buf;
}

void leaky_function(void) {
    char *msg = create_greeting("World");
    printf("%s\n", msg);
    /* OOPS: forgot free(msg) -- memory leak! */
}

void correct_function(void) {
    char *msg = create_greeting("World");
    if (msg != NULL) {
        printf("%s\n", msg);
        free(msg);  /* correct: always free */
    }
}

int main(void) {
    for (int i = 0; i < 1000000; i++) {
        leaky_function();  /* leaks ~14 bytes per call! */
    }
    /* After 1M calls: ~14 MB leaked */
    return 0;
}
```

---

## Dangling Pointer: Example

```c
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    int *p = malloc(sizeof(int));
    *p = 42;

    int *alias = p;  /* alias points to same memory */

    free(p);
    p = NULL;

    /* alias is now DANGLING -- still points to freed memory */
    /* printf("%d\n", *alias);  UB: use-after-free! */

    /* The memory may be reused by another allocation */
    int *q = malloc(sizeof(int));
    *q = 99;
    /* alias might now point to q's memory -- chaos! */

    free(q);
    return 0;
}
```

---

## Dangling Pointer

![dangling_pointer](svg/courses/languages/c/c-refresher/11_dynamic_memory/dangling_pointer.svg)

---

## Double Free

```c
#include <stdlib.h>

int main(void) {
    int *p = malloc(sizeof(int));
    *p = 42;

    free(p);
    /* free(p);  <-- DOUBLE FREE: undefined behavior! */
    /* May corrupt heap metadata, crash, or be exploitable */

    /* Prevention: always NULL after free */
    p = NULL;
    free(p);  /* safe: free(NULL) is a no-op */

    return 0;
}
```

Double free is a serious security vulnerability -- it can lead to
arbitrary code execution in some heap implementations.

---

## Use-After-Free

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct User {
    char name[32];
    int level;
};

int main(void) {
    struct User *admin = malloc(sizeof(struct User));
    strcpy(admin->name, "admin");
    admin->level = 9;

    free(admin);

    /* Attacker can cause another allocation to reuse the same memory */
    char *evil = malloc(sizeof(struct User));
    memset(evil, 0x41, sizeof(struct User));  /* fill with 'A' */

    /* If we still use admin, we read attacker-controlled data */
    /* printf("User: %s, Level: %d\n", admin->name, admin->level); */
    /* This is a USE-AFTER-FREE vulnerability */

    free(evil);
    return 0;
}
```

---

## Detecting Memory Errors with Valgrind

```bash
# Compile with debug info (no optimization)
gcc -g -O0 -o program program.c

# Run under Valgrind memcheck
valgrind --leak-check=full \
         --show-leak-kinds=all \
         --track-origins=yes \
         ./program
```

Example Valgrind output for a leak:

```c
==12345== HEAP SUMMARY:
==12345==   in use at exit: 40 bytes in 1 blocks
==12345==   total heap usage: 3 allocs, 2 frees, 1,064 bytes allocated
==12345==
==12345== 40 bytes in 1 blocks are definitely lost in loss record 1 of 1
==12345==    at 0x4C2BBAF: malloc (vg_replace_malloc.c:299)
==12345==    by 0x4005E7: create_array (program.c:12)
==12345==    by 0x400617: main (program.c:20)
```

---

## Detecting Memory Errors with AddressSanitizer

```bash
# Compile with ASan
gcc -g -fsanitize=address -fno-omit-frame-pointer -o program program.c

# Run normally -- ASan instruments the binary
./program
```

ASan detects at runtime:
- Heap buffer overflow
- Stack buffer overflow
- Use-after-free
- Double free
- Memory leaks (`-fsanitize=address -fsanitize=leak`)

ASan is faster than Valgrind (~2x slowdown vs ~20x) but requires recompilation.

---

## A Dynamic Array (Vector) Implementation

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct Vector {
    int *data;
    int size;
    int capacity;
};

struct Vector *vec_create(int initial_cap) {
    struct Vector *v = malloc(sizeof(struct Vector));
    if (v == NULL) return NULL;
    v->data = malloc(initial_cap * sizeof(int));
    if (v->data == NULL) { free(v); return NULL; }
    v->size = 0;
    v->capacity = initial_cap;
    return v;
}

int vec_push(struct Vector *v, int value) {
    if (v->size >= v->capacity) {
        int new_cap = v->capacity * 2;
        int *tmp = realloc(v->data, new_cap * sizeof(int));
        if (tmp == NULL) return -1;
        v->data = tmp;
        v->capacity = new_cap;
    }
    v->data[v->size++] = value;
    return 0;
}
```

---

## A Dynamic Array (Vector): Access and Destroy

```c
#include <stdio.h>
#include <stdlib.h>

struct Vector { int *data; int size; int capacity; };

int vec_get(const struct Vector *v, int index) {
    if (index < 0 || index >= v->size) {
        fprintf(stderr, "vec_get: index %d out of bounds\n", index);
        abort();
    }
    return v->data[index];
}

void vec_destroy(struct Vector *v) {
    if (v) {
        free(v->data);
        free(v);
    }
}
```

---

## A Dynamic Array (Vector): Usage

```c
#include <stdio.h>

int main(void) {
    struct Vector *v = vec_create(4);
    for (int i = 0; i < 20; i++) {
        vec_push(v, i * 10);
    }

    for (int i = 0; i < 20; i++) {
        printf("%d ", vec_get(v, i));
    }
    printf("\n");

    vec_destroy(v);
    return 0;
}
```

---

## Memory Pool: Pre-Allocated Fixed-Size Blocks

```c
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>

#define POOL_SIZE 1024
#define BLOCK_SIZE 64

struct MemPool {
    char memory[POOL_SIZE * BLOCK_SIZE];
    bool used[POOL_SIZE];
    int allocated;
};

void pool_init(struct MemPool *pool) {
    memset(pool->used, false, sizeof(pool->used));
    pool->allocated = 0;
}

void *pool_alloc(struct MemPool *pool) {
    for (int i = 0; i < POOL_SIZE; i++) {
        if (!pool->used[i]) {
            pool->used[i] = true;
            pool->allocated++;
            return &pool->memory[i * BLOCK_SIZE];
        }
    }
    return NULL;  /* pool exhausted */
}
```

---

## Memory Pool: pool_free

```c
void pool_free(struct MemPool *pool, void *ptr) {
    if (ptr == NULL) return;
    ptrdiff_t offset = (char *)ptr - pool->memory;
    int index = offset / BLOCK_SIZE;
    if (index >= 0 && index < POOL_SIZE && pool->used[index]) {
        pool->used[index] = false;
        pool->allocated--;
    }
}
```

---

## Memory Pool: Usage

```c
#include <stdio.h>

int main(void) {
    struct MemPool pool;
    pool_init(&pool);

    /* Allocate several blocks */
    int *a = pool_alloc(&pool);
    int *b = pool_alloc(&pool);
    int *c = pool_alloc(&pool);

    *a = 10; *b = 20; *c = 30;
    printf("a=%d, b=%d, c=%d\n", *a, *b, *c);

    pool_free(&pool, b);

    /* b's slot is reused */
    int *d = pool_alloc(&pool);
    *d = 40;
    printf("d=%d\n", *d);

    return 0;
}
```

---

## Arena Allocator

An arena allocates linearly and frees everything at once.
Useful for request-scoped allocations (parsers, compilers, web servers).

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define ARENA_SIZE (1024 * 1024)  /* 1 MB */

struct Arena {
    char *base;
    size_t offset;
    size_t capacity;
};

struct Arena *arena_create(size_t capacity) {
    struct Arena *a = malloc(sizeof(struct Arena));
    if (a == NULL) return NULL;
    a->base = malloc(capacity);
    if (a->base == NULL) { free(a); return NULL; }
    a->offset = 0;
    a->capacity = capacity;
    return a;
}

void *arena_alloc(struct Arena *a, size_t size) {
    /* Align to 8 bytes */
    size_t aligned = (size + 7) & ~(size_t)7;
    if (a->offset + aligned > a->capacity) return NULL;
    void *ptr = a->base + a->offset;
    a->offset += aligned;
    return ptr;
}
```

---

## Arena Allocator: Reset and Destroy

```c
#include <stdlib.h>

struct Arena { char *base; size_t offset; size_t capacity; };

void arena_reset(struct Arena *a) {
    a->offset = 0;  /* "free" everything instantly */
}

void arena_destroy(struct Arena *a) {
    if (a) {
        free(a->base);
        free(a);
    }
}
```

---

## Arena Allocator: Usage

```c
#include <stdio.h>
#include <stdlib.h>

#define ARENA_SIZE (1024 * 1024)

int main(void) {
    struct Arena *arena = arena_create(ARENA_SIZE);

    /* Allocate several objects -- no individual free needed */
    int *x = arena_alloc(arena, sizeof(int));
    int *y = arena_alloc(arena, sizeof(int));
    char *str = arena_alloc(arena, 100);

    *x = 42;
    *y = 99;
    snprintf(str, 100, "Arena allocated string");

    printf("x=%d, y=%d, str='%s'\n", *x, *y, str);

    /* Free everything at once */
    arena_reset(arena);

    arena_destroy(arena);
    return 0;
}
```

---

## Custom Allocator Overview

![custom_allocator_overview](svg/courses/languages/c/c-refresher/11_dynamic_memory/custom_allocator_overview.svg)

---

## Custom Allocator Overview: Details

When to use each:
- **Arena**: short-lived, batch-freed allocations (parsers, per-request)
- **Pool**: many same-sized objects (network connections, game entities)
- **Free list**: general-purpose, variable sizes
- **Slab**: kernel object caching (Linux kernel uses this)

---

## Common Memory Errors

![common_memory_errors](svg/courses/languages/c/c-refresher/11_dynamic_memory/common_memory_errors.svg)

---

## Common Memory Errors Summary

| Error | Symptom | Detection |
|-------|---------|-----------|
| Memory leak | Growing RSS, OOM | Valgrind, ASan |
| Use-after-free | Corrupted data, crash | ASan, Valgrind |
| Double free | Crash, heap corruption | ASan, Valgrind |
| Buffer overflow | Corrupted adjacent data | ASan, Valgrind |
| Uninitialized read | Unpredictable values | Valgrind, MSan |
| Stack overflow | Segfault in deep recursion | ulimit, ASan |
| Wild pointer | Random crash | ASan |

---

## Best Practices for Memory Management

1. Always check the return value of `malloc`/`calloc`/`realloc`
1. Always `free` allocated memory when done
1. Set pointers to `NULL` after `free`
1. Use a temporary pointer for `realloc` to avoid leaks on failure
1. Use `calloc` when you need zero-initialized memory
1. Match every `malloc` with exactly one `free`
1. Use Valgrind or ASan regularly during development
1. Consider arena allocators for batch/scoped allocations
1. Document ownership: who allocates, who frees
1. For complex projects, wrap allocation in helper functions

---

## Summary

- `malloc` allocates uninitialized memory, `calloc` zeros it, `realloc` resizes
- Always check for `NULL` return values
- Memory errors (leaks, use-after-free, double free) are among the most dangerous bugs in C
- Use Valgrind (`--leak-check=full`) or AddressSanitizer (`-fsanitize=address`) to detect errors
- Arena allocators and memory pools can reduce allocation overhead and prevent leaks
- Document memory ownership clearly in your APIs
- Set pointers to `NULL` after freeing to prevent dangling pointer use
