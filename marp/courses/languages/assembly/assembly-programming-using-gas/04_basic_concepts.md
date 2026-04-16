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
# Basic Assembly Concepts

---

## Registers

- Small, fast storage locations in the CPU
- Used for temporary data storage and manipulation
- Different types and purposes

---

## General Purpose Registers (32-bit)

- EAX: Accumulator for arithmetic operations
- EBX: Base register for memory addressing
- ECX: Counter for string and loop operations
- EDX: Data register, also used for I/O
- ESI: Source index for string operations
- EDI: Destination index for string operations
- EBP: Base pointer for stack frames
- ESP: Stack pointer

---

## Memory

- RAM (Random Access Memory)
- Organized in bytes
- Each byte has a unique address
- Big Endian vs Little Endian

Example:
```gas
section .data
    my_variable dd 0x12345678
```

---

## Instruction Set Architecture (ISA)
- Set of instructions that a CPU can execute
- Defines:
    - Available operations
    - Instruction formats
    - Registers
    - Addressing modes
    - Memory organization

---

## Basic x86 Instruction Format

```nasm
[label:] mnemonic [operands] [; comment]
```

Example:
```gas
_start:
    mov eax, 5      ; Move 5 into EAX register
    add eax, 10     ; Add 10 to EAX
```

---

## Addressing Modes

![addressing_modes](svg/courses/languages/assembly/assembly-programming-using-gas/04_basic_concepts/addressing_modes.svg)

---

## Addressing Modes Detail

1. Immediate: Constant value

```gas
mov eax, 42
```

1. Register: Value in a register

```gas
mov ebx, eax
```

1. Direct: Memory address

```gas
mov eax, [0x1000]
```

---

## Addressing Modes (continued)

1. Indirect: Address stored in a register

```gas
mov eax, [ebx]
```

1. Base + Offset: Address calculated from base and offset

```gas
mov eax, [ebx + 8]
```

1. Scaled Index: Used for array access

```gas
mov eax, [ebx + ecx*4]
```

---

## Data Types
- Byte: 8 bits
- Word: 16 bits
- Double Word: 32 bits
- Quad Word: 64 bits

Example:

```gas
section .data
    my_byte  db 0xFF
    my_word  dw 0xFFFF
    my_dword dd 0xFFFFFFFF
    my_qword dq 0xFFFFFFFFFFFFFFFF
```

---

## Basic Arithmetic Instructions

- ADD: Addition
- SUB: Subtraction
- MUL: Unsigned multiplication
- DIV: Unsigned division
- INC: Increment
- DEC: Decrement

Example:

```gas
mov eax, 5
add eax, 3      ; EAX now contains 8
sub eax, 2      ; EAX now contains 6
inc eax         ; EAX now contains 7
```

---

## Logical Operations

- AND: Bitwise AND
- OR: Bitwise OR
- XOR: Bitwise XOR
- NOT: Bitwise NOT
- SHL/SHR: Shift left/right

Example:
```gas
mov eax, 0b1100
and eax, 0b1010  ; EAX now contains 0b1000
```

---

## Control Flow

- JMP: Unconditional jump
- Conditional jumps: JE, JNE, JG, JL, etc.
- CALL: Call a function
- RET: Return from a function

Example:
```gas
    cmp eax, 10
    je equal_ten
    jmp not_equal

equal_ten:
    ; Code for when EAX equals 10
    ret

not_equal:
    ; Code for when EAX does not equal 10
    ret
```

---

## The Stack

- Last-In-First-Out (LIFO) data structure
- Grows downwards in memory
- Managed by ESP (Stack Pointer)
- Used for:
    - Local variables
    - Function parameters
    - Return addresses
