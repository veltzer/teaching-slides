# Advanced Topics in Assembly Programming

---

## Floating-Point Operations

- x87 FPU (Floating-Point Unit)
- SSE (Streaming SIMD Extensions)
- AVX (Advanced Vector Extensions)

---

## x87 FPU Instructions

- Stack-based architecture
- 8 80-bit registers (ST0-ST7)

Example:
```nasm
fld dword ptr [x]    ; Load x into ST0
fld dword ptr [y]    ; Load y into ST0, push previous value to ST1
faddp                ; Add ST0 and ST1, pop
fstp dword ptr [z]   ; Store result in z and pop
```

---
## SSE Floating-Point Operations

- SIMD (Single Instruction, Multiple Data)
- 128-bit XMM registers (XMM0-XMM15)

Example:
```nasm
movss xmm0, [x]      ; Move single-precision float x to xmm0
addss xmm0, [y]      ; Add single-precision float y to xmm0
movss [z], xmm0      ; Store result in z
```

---

## AVX Floating-Point Operations

- Extended SSE capabilities
- 256-bit YMM registers

Example:
```nasm
vmovaps ymm0, [array1]   ; Load 8 floats from array1
vmovaps ymm1, [array2]   ; Load 8 floats from array2
vaddps ymm2, ymm0, ymm1  ; Add 8 pairs of floats
vmovaps [result], ymm2   ; Store 8 float results
```

---

## SIMD Programming: SSE

- Perform multiple operations in parallel
- 128-bit XMM registers

Example (4 simultaneous integer additions):
```nasm
movdqa xmm0, [array1]    ; Load 4 ints from array1
paddd xmm0, [array2]     ; Add 4 ints from array2
movdqa [result], xmm0    ; Store 4 int results
```

---

## SIMD Programming: AVX

- Extended SIMD capabilities
- 256-bit YMM registers

Example (8 simultaneous float multiplications):
```nasm
vmovaps ymm0, [array1]   ; Load 8 floats from array1
vmulps ymm0, ymm0, [array2] ; Multiply by 8 floats from array2
vmovaps [result], ymm0   ; Store 8 float results
```

---

## Multi-threading Basics

- Parallel execution of code
- Shared memory between threads
- Synchronization mechanisms

---

## Creating Threads (Using Pthreads)

```c
#include <pthread.h>

void *thread_function(void *arg) {
    // Thread code here
    return NULL;
}

int main() {
    pthread_t thread_id;
    pthread_create(&thread_id, NULL, thread_function, NULL);
    pthread_join(thread_id, NULL);
    return 0;
}
```

---

## Thread Synchronization: Mutex

```c
pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;

pthread_mutex_lock(&mutex);
// Critical section
pthread_mutex_unlock(&mutex);
```

In assembly:
```nasm
lock xadd dword ptr [mutex], eax
```

---

## Atomic Operations

Example: Atomic increment
```nasm
lock inc dword ptr [counter]
```

Example: Compare and Swap
```nasm
mov eax, old_value
lock cmpxchg dword ptr [address], new_value
```

---

## Memory Ordering

- Compiler and CPU can reorder instructions
- Memory barriers ensure proper ordering

Example:
```nasm
mfence  ; Full memory barrier
lfence  ; Load fence
sfence  ; Store fence
```

---

## Cache Considerations

- Understand cache line size (typically 64 bytes)
- Align data to cache lines for better performance
- Avoid false sharing in multi-threaded code
