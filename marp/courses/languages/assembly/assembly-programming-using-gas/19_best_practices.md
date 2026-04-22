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
# Best Practices and Coding Standards

---

## Assembly Best Practices

![Assembly best practices overview](svg/courses/languages/assembly/assembly-programming-using-gas/19_best_practices/asm_best_practices.svg)

---

## Code Organization

- Use a consistent file structure
- Separate code into logical sections

Example:

```nasm
.section .data
    # Data declarations

.section .bss
    # Uninitialized data

.section .text
    # Code
```

---

## Naming Conventions

- Use descriptive names for labels and variables
- Follow a consistent naming style

Examples:

```nasm
calculate_sum:
    # Function to calculate sum

MAX_ARRAY_SIZE: .equ 100

current_index: .long 0
```

---

## Commenting

- Comment your code thoroughly
- Explain the "why", not just the "what"

Example:

```nasm
# Calculate factorial of n (in eax)
# Result stored in eax
factorial:
    push ebx
    mov ebx, eax    # Store n in ebx
    cmp eax, 1
    jle .done       # Special case: n <= 1

.loop:
    dec ebx
    mul ebx         # eax *= ebx
    cmp ebx, 1
    jg .loop

.done:
    pop ebx
    ret
```

---

## Modular Programming

- Break code into reusable functions
- Use stack for parameter passing

Example:

```gas
.globl add_numbers
add_numbers:
    pushl %ebp
    movl %esp, %ebp
    movl 8(%ebp), %eax    # First parameter
    addl 12(%ebp), %eax   # Second parameter
    popl %ebp
    ret
```

---

## Consistent Register Usage

- Use registers consistently across your program
- Document register usage in comments

Example:

```nasm
# eax: loop counter
# ebx: array base address
# ecx: current array element
# edx: sum
```

---

## Proper Alignment
- Align data for optimal performance
- Use appropriate directives

Example:

```nasm
.align 16
sse_data:
    .float 1.0, 2.0, 3.0, 4.0
```

---

## Error Handling in Assembly
- Use conditional jumps for error checking
- Set error codes in a consistent manner

Example:

```nasm
    cmp eax, 0
    jl .error_handler

    # Normal execution continues

.error_handler:
    mov [error_code], eax
    call print_error
    jmp .cleanup
```

---
## Use of Macros

- Create macros for repeated code patterns
- Improves readability and maintainability

Example:
```nasm
.macro push_all
    push eax
    push ebx
    push ecx
    push edx
.endm

.macro pop_all
    pop edx
    pop ecx
    pop ebx
    pop eax
.endm
```

---

## Consistent Indentation

- Use consistent indentation for readability
- Align similar instructions

Example:
```nasm
.loop:
    mov eax, [ebx]
    add eax, ecx
    mov [ebx], eax
    add ebx, 4
    dec edx
    jnz .loop
```

---

## Documentation

- Provide a header comment for each file
- Include purpose, author, date, and usage

Example:

```nasm
# File: math_utils.s
# Author: John Doe
# Date: 2023-09-07
# Description: Utility functions for mathematical operations
# Usage: Include this file and call the functions as needed
```

---

## Avoid Self-Modifying Code

- Self-modifying code is hard to maintain
- Use it only when absolutely necessary

Instead of:
```nasm
    mov byte [instruction+1], 42
instruction:
    mov al, 0
```

Use variables or conditional execution

---

## Testing and Validation

- Write test cases for your assembly code
- Use assertions to catch errors early

Example:
```nasm
    call calculate_sum
    cmp eax, expected_sum
    je .test_passed
    call report_test_failure
```
