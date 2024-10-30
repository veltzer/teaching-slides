# Data Types and Data Movement

---

## Integer Representations

- Byte (8 bits): -128 to 127 or 0 to 255
- Word (16 bits): -32,768 to 32,767 or 0 to 65,535
- Doubleword (32 bits): -2^31 to 2^31-1 or 0 to 2^32-1
- Quadword (64 bits): -2^63 to 2^63-1 or 0 to 2^64-1

Example:
```gas
.data
    byte_val:  .byte  42
    word_val:  .word  30000
    dword_val: .long  2000000000
    qword_val: .quad  9000000000000000000
```

---

## Signed vs Unsigned Integers

- Signed integers use two's complement representation
- Most significant bit (MSB) indicates sign (0 positive, 1 negative)
- Same bit patterns, different interpretations

Example:
```gas
    mov $-1, %eax   # EAX = 0xFFFFFFFF (signed)
    mov $0xFFFFFFFF, %ebx  # EBX = 4294967295 (unsigned)
```

---

## Floating-Point Representations

- Single precision (32 bits): ~7 decimal digits precision
- Double precision (64 bits): ~15 decimal digits precision

Example:
```gas
.data
    pi_single: .float  3.14159
    pi_double: .double 3.141592653589793
```

---

## ASCII and Unicode

- ASCII: 7-bit encoding, 128 characters
- Unicode: Variable-length encoding (UTF-8, UTF-16, UTF-32)

Example:
```gas
.data
    ascii_string: .ascii "Hello"
    utf8_string:  .ascii "unicode-string"
```

---

## MOV Instruction

Basic syntax: `mov source, destination`

Examples:
```gas
    mov $42, %eax          # Immediate to register
    mov %eax, %ebx         # Register to register
    mov %eax, variable     # Register to memory
    mov variable, %ecx     # Memory to register
```

---

## MOV Variants

- `movzx`: Move with zero-extend
- `movsx`: Move with sign-extend
- `movb`, `movw`, `movl`, `movq`: Move specific sizes

Examples:
```gas
    movzx %al, %eax    # Zero-extend 8-bit to 32-bit
    movsx %ax, %eax    # Sign-extend 16-bit to 32-bit
    movb $5, (%ebx)    # Move 8-bit value to memory
```

---

## LEA Instruction

`lea` (Load Effective Address) calculates an address without accessing memory.

Example:
```gas
    lea (%ebx, %ecx, 4), %eax   # EAX = EBX + ECX * 4
```

Useful for:
- Address calculations
- Simple arithmetic (addition and multiplication)

---

## XCHG Instruction

`xchg` exchanges the contents of two operands.

Example:
```gas
    xchg %eax, %ebx   # Swap contents of EAX and EBX
```

Note: `xchg` with memory is always atomic (useful for synchronization).

---

## Push and Pop

Stack operations for saving and retrieving data:

- `push`: Decrements ESP and stores value on stack
- `pop`: Retrieves value from stack and increments ESP

Example:
```gas
    push %eax    # Save EAX on stack
    # ... some operations ...
    pop %eax     # Restore EAX from stack
```

---

## Data Movement and Alignment

- Alignment: Memory addresses divisible by data size
- Improves performance and is required on some architectures
- Use `.align` directive to ensure proper alignment

Example:
```gas
.data
    .align 4
    aligned_data: .long 42
```

---

## SIMD Data Movement

SIMD (Single Instruction, Multiple Data) instructions for parallel data movement:

- `movaps`: Move Aligned Packed Single-Precision
- `movups`: Move Unaligned Packed Single-Precision
- `movdqa`: Move Aligned Packed Double-Quadword
- `movdqu`: Move Unaligned Packed Double-Quadword

Example:
```gas
    movaps %xmm0, %xmm1   # Move 4 floats at once
```
