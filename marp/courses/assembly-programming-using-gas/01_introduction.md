---
marp: true
theme: default
paginate: true
---

# Chapter 1: Introduction to Assembly Language

---

## What is Assembly Language?

- Low-level programming language
- Direct correspondence with machine code
- Architecture-specific
- Provides direct hardware control

---

## Assembly vs. High-Level Languages

| Assembly | High-Level Languages |
|----------|----------------------|
| Direct hardware control | Abstracted from hardware |
| Architecture-specific | Portable across platforms |
| Manual memory management | Automatic memory management |
| Faster execution (potentially) | Easier to write and maintain |

---

## Advantages of Assembly Language

1. **Performance**: Potential for highly optimized code
2. **Hardware Control**: Direct access to system resources
3. **Size Efficiency**: Smaller program size possible
4. **Understanding Computer Architecture**: Learn how computers work at a low level

---

## Disadvantages of Assembly Language

1. **Complexity**: Steeper learning curve
2. **Time-consuming**: Writing and debugging can be slower
3. **Lack of Portability**: Code is specific to an architecture
4. **Maintenance Challenges**: Can be harder to update and maintain

---

## When to Use Assembly Language

- Operating system kernels
- Device drivers
- Embedded systems programming
- Performance-critical sections of code
- Reverse engineering and malware analysis

---

## x86 Architecture Overview

- Developed by Intel
- CISC (Complex Instruction Set Computing) architecture
- Widely used in personal computers and servers
- Versions:
  - 16-bit (8086/8088)
  - 32-bit (IA-32 or i386)
  - 64-bit (x86-64 or AMD64)

---

## x86 Register Set (32-bit)

- General Purpose Registers:
  - EAX, EBX, ECX, EDX
  - ESI, EDI
  - EBP, ESP
- Segment Registers: CS, DS, SS, ES, FS, GS
- Status Flags Register: EFLAGS
- Instruction Pointer: EIP

---

## x86-64 Architecture

- 64-bit extension of x86 architecture
- Introduced by AMD, later adopted by Intel
- Backward compatible with 32-bit and 16-bit x86 code
- Expanded register set and wider registers

---

## x86-64 Register Set

- General Purpose Registers:
  - RAX, RBX, RCX, RDX, RSI, RDI, RBP, RSP
  - R8 to R15 (new 64-bit registers)
- Wider registers (64-bit instead of 32-bit)
- More registers available for general use

---

## Assembly Language Syntax

```x86asm
section .data
    message db 'Hello, World!', 0

section .text
    global _start

_start:
    ; Your code here
    mov eax, 1    ; System call number for exit
    xor ebx, ebx  ; Exit status 0
    int 0x80      ; Call kernel
```

---

## Next Steps

- Setting up your development environment
- Understanding GAS syntax
- Writing your first assembly program
