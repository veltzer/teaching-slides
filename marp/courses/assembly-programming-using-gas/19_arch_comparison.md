# Comparison with Other Architectures

---

# ARM Assembly Basics

- Reduced Instruction Set Computing (RISC)
- Used in mobile devices, embedded systems
- Different syntax and conventions from x86

---

# ARM vs x86: Register Set

ARM:
- r0-r15 (general-purpose registers)
- sp (stack pointer, alias for r13)
- lr (link register, alias for r14)
- pc (program counter, alias for r15)

x86:
- eax, ebx, ecx, edx, esi, edi, ebp, esp
- eip (instruction pointer)

---

# ARM Assembly Example

```arm
.global _start
_start:
    mov r0, #1        @ File descriptor 1: STDOUT
    ldr r1, =message  @ Load address of message
    mov r2, #13       @ Message length
    mov r7, #4        @ System call 4: write
    swi 0             @ Software interrupt

    mov r7, #1        @ System call 1: exit
    swi 0

.data
message:
    .ascii "Hello, World\n"
```

---

# x86 Equivalent

```x86asm
.global _start
_start:
    mov eax, 4
    mov ebx, 1
    mov ecx, message
    mov edx, 13
    int 0x80

    mov eax, 1
    xor ebx, ebx
    int 0x80

.data
message:
    .ascii "Hello, World\n"
```

---

# RISC vs CISC

RISC (e.g., ARM):
- Simple instructions
- Fixed instruction length
- Load-store architecture

CISC (e.g., x86):
- Complex instructions
- Variable instruction length
- Memory-to-memory operations

---

# Instruction Comparison

ARM (RISC):
```arm
ldr r0, [r1]    @ Load from memory
add r0, r0, r2  @ Add
str r0, [r1]    @ Store to memory
```

x86 (CISC):
```x86asm
add [ecx], edx  @ Load, add, and store in one instruction
```

---

# MIPS Architecture

- Another RISC architecture
- Used in embedded systems and networking equipment
- 32 general-purpose registers ($0-$31)

MIPS Example:
```mips
.globl main
main:
    li $v0, 4           # System call for print_str
    la $a0, hello_msg   # Load address of string
    syscall

    li $v0, 10          # System call for exit
    syscall

.data
hello_msg: .asciiz "Hello, World!\n"
```

---

# PowerPC Architecture

- RISC architecture used in older Macs, game consoles
- 32 general-purpose registers (r0-r31)

PowerPC Example:
```
.global _start
_start:
    li r0, 4        # System call: write
    li r3, 1        # File descriptor: stdout
    lis r4, msg@ha  # Load high half of msg address
    addi r4, r4, msg@l  # Add low half of msg address
    li r5, 13       # Length of string
    sc              # System call

    li r0, 1        # System call: exit
    li r3, 0        # Exit status
    sc

.data
msg: .ascii "Hello, World\n"
```

---

# RISC-V Architecture

- Open-source RISC architecture
- Gaining popularity in embedded systems and academia
- Extensible instruction set

RISC-V Example:
```
.global _start
_start:
    li a7, 64       # System call: write
    li a0, 1        # File descriptor: stdout
    la a1, message  # Load address of message
    li a2, 13       # Length of message
    ecall

    li a7, 93       # System call: exit
    li a0, 0        # Exit status
    ecall

.data
message:
    .string "Hello, World\n"
```

---

# Instruction Set Comparison

| Architecture | Add           | Load                | Branch        |
|--------------|---------------|---------------------|---------------|
| x86          | add eax, ebx  | mov eax, [ebx]      | jne label     |
| ARM          | add r0, r1, r2| ldr r0, [r1]        | bne label     |
| MIPS         | add $t0,$t1,$t2| lw $t0, 0($t1)     | bne $t0,$t1,label |
| PowerPC      | add r3, r4, r5| lwz r3, 0(r4)       | bne cr0, label|
| RISC-V       | add a0, a1, a2| lw a0, 0(a1)        | bne a0, a1, label |

---

# Architectural Trade-offs

- Performance vs Power consumption
- Code density vs Simplicity
- Hardware complexity vs Software flexibility
- Backward compatibility vs Clean design

---

# Choosing an Architecture

- Consider target platform (mobile, desktop, server)
- Evaluate performance requirements
- Assess development tools and ecosystem
- Factor in power consumption and cost
