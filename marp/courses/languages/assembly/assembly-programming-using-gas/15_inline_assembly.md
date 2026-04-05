# Inline Assembly in C

---

## What is Inline Assembly?

- Assembly code embedded directly in C code
- Allows low-level optimizations and hardware access
- Useful for performance-critical sections
- Syntax varies by compiler (we'll focus on GCC)

---

## Basic Syntax

```c
__asm__ (
    "assembly code here"
);
```

Example:
```c
__asm__ (
    "movl $1, %eax\n\t"
    "movl $0, %ebx\n\t"
    "int $0x80"
);
```

---

## Extended ASM Syntax

```c
__asm__ (
    "assembly template"
    : output operands
    : input operands
    : clobbers
);
```

Example:
```c
int a = 10, b = 20, result;
__asm__ (
    "addl %%ebx, %%eax"
    : "=a" (result)
    : "a" (a), "b" (b)
);
```

---

## Output Operands

- Specify where results are stored
- Use "=" for write-only, "+" for read-write

Example:
```c
int result;
__asm__ (
    "movl $42, %0"
    : "=r" (result)
);
```

---

## Input Operands

- Provide values to the assembly code
- Can use variables or constants

Example:
```c
int a = 10, b = 20;
__asm__ (
    "addl %1, %0"
    : "+r" (a)
    : "r" (b)
);
```

---

## Clobbers

- Tell the compiler which registers or memory are modified
- Use "memory" for any memory writes

Example:
```c
__asm__ (
    "cpuid"
    :
    :
    : "eax", "ebx", "ecx", "edx"
);
```

---

## Constraints

- Tell the compiler how to allocate variables
- Common constraints:
    - "r": Any general-purpose register
    - "m": Memory operand
    - "i": Immediate integer operand
    - "0", "1", "2", etc.: Use the same place as the nth operand

Example:

```c
int src = 1, dst;
__asm__ (
    "movl %1, %0"
    : "=r" (dst)
    : "r" (src)
);
```

---
## Using Inline Assembly for Optimization

Example: Fast integer square root
```c
static inline int isqrt(int num) {
    int result;
    __asm__ (
        "bsrl %1, %%ecx\n\t"
        "shrl $1, %%ecx\n\t"
        "movl $1, %0\n\t"
        "shll %%cl, %0"
        : "=r" (result)
        : "r" (num)
        : "ecx"
    );
    return result;
}
```

---

## Accessing Special CPU Instructions

Example: Using RDTSC to read CPU timestamp
```c
unsigned long long rdtsc() {
    unsigned long long result;
    __asm__ (
        "rdtsc\n\t"
        "shlq $32, %%rdx\n\t"
        "orq %%rdx, %%rax"
        : "=A" (result)
        :
        : "rdx"
    );
    return result;
}
```

---

## Inline Assembly in Functions

Example: Optimized strlen
```c
size_t my_strlen(const char *str) {
    size_t len;
    __asm__ (
        "movq %1, %%rdi\n\t"
        "xorq %%rax, %%rax\n\t"
        "movq $-1, %%rcx\n\t"
        "repne scasb\n\t"
        "notq %%rcx\n\t"
        "decq %%rcx"
        : "=c" (len)
        : "r" (str)
        : "rdi", "rax"
    );
    return len;
}
```

---

## Portability Concerns

- Inline assembly is architecture-specific
- May break with compiler optimizations
- Consider using intrinsics or compiler-specific extensions instead

Example of using intrinsics:
```c
#include <immintrin.h>

void add_vectors(float *a, float *b, float *result, int size) {
    for (int i = 0; i < size; i += 4) {
        __m128 va = _mm_load_ps(a + i);
        __m128 vb = _mm_load_ps(b + i);
        __m128 vr = _mm_add_ps(va, vb);
        _mm_store_ps(result + i, vr);
    }
}
```

---

## Best Practices

1. Use inline assembly sparingly
1. Document thoroughly
1. Consider portability and maintainability
1. Profile to ensure actual performance gains
1. Use constraints and clobbers correctly
1. Be aware of compiler optimizations
