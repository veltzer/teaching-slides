---
tags:
  - languages:assembly
  - hardware-and-embedded:x86
  - infrastructure:linux
  - infrastructure:low-level
level: advanced
category: language
audience:
  - audiences:developers

---

# Optimization Techniques

---

## Why Optimize?
- Improve execution speed
- Reduce memory usage
- Enhance energy efficiency
- Better utilization of hardware resources

---

## Common Optimization Strategies
1. Loop optimization
1. Function inlining
1. Branch prediction optimization
1. Data alignment
1. Register allocation
1. Instruction selection
1. Parallelization

---

## Loop Optimization: Loop Unrolling

Before:

```nasm
    mov ecx, 100
.loop:
    mov eax, [esi]
    add [edi], eax
    add esi, 4
    add edi, 4
    dec ecx
    jnz .loop
```

After:

```nasm
    mov ecx, 25
.loop:
    mov eax, [esi]
    add [edi], eax
    mov eax, [esi+4]
    add [edi+4], eax
    mov eax, [esi+8]
    add [edi+8], eax
    mov eax, [esi+12]
    add [edi+12], eax
    add esi, 16
    add edi, 16
    dec ecx
    jnz .loop
```

---

## Loop Unrolling: Before vs After

![Side-by-side comparison of original loop vs 4x unrolled loop showing iteration count reduction from 100 to 25 and instruction analysis](svg/courses/languages/assembly/assembly-programming-using-gas/14_optimization/loop_unrolling_before_after.svg)

---

## Function Inlining
- Replace function call with actual code
- Eliminates call/return overhead
- May increase code size

Example:

```nasm
; Instead of calling a function
call calculate_sum

; Inline the function code directly
mov eax, [num1]
add eax, [num2]
mov [result], eax
```

---

## Branch Prediction Optimization
- Arrange code so that the most likely path is fall-through
- Use conditional moves instead of branches for simple conditions

Example:

```nasm
    cmp eax, ebx
    jg .greater
    mov ecx, eax
    jmp .done
.greater:
    mov ecx, ebx
.done:
```

Can be optimized to:

```nasm
    cmp eax, ebx
    cmovle ecx, eax
    cmovg ecx, ebx
```

---

## Data Alignment
- Align data to natural boundaries
- Improves memory access efficiency

Example:

```nasm
.data
    .align 16
my_array:
    .long 1, 2, 3, 4
```

---

## Register Allocation
- Keep frequently used values in registers
- Minimize memory access

Example:

```nasm
; Less efficient
mov eax, [counter]
inc eax
mov [counter], eax

; More efficient
mov eax, [counter]
.loop:
    ; Use eax directly
    inc eax
    ; ... other operations
    jnz .loop
mov [counter], eax
```

---

## Instruction Selection
- Choose instructions with lower latency or higher throughput
- Use SIMD instructions for data parallelism

Example:

```nasm
; Instead of
mov eax, 0

; Use
xor eax, eax
```

SIMD example:
```nasm
movdqa xmm0, [array1]
paddd xmm0, [array2]
movdqa [result], xmm0
```

---

## Parallelization

- Utilize multiple cores or threads
- Use SIMD instructions for data-level parallelism

Example (pseudo-code):
```nasm
; Divide work among threads
mov ecx, thread_id
mov edx, num_threads
mov eax, total_elements
div edx
mov esi, eax  ; elements per thread
imul esi, ecx
add esi, array_start  ; starting point for this thread

; Process elements
.loop:
    ; ... process element
    dec eax
    jnz .loop
```

---

## Profiling and Benchmarking
- Use tools like `gprof`, `perf`, or `valgrind`
- Identify performance bottlenecks
- Measure impact of optimizations

Example:

```bash
gcc -pg program.c -o program
./program
gprof program gmon.out > analysis.txt
```

---

## Optimization Pitfalls
- Premature optimization
- Over-optimization leading to unreadable code
- Architecture-specific optimizations reducing portability
- Optimizations that break correctness

---

## Best Practices

1. Profile before optimizing
1. Focus on hot spots (frequently executed code)
1. Benchmark to verify improvements
1. Consider trade-offs (speed vs. readability, memory usage)
1. Comment optimized code thoroughly
