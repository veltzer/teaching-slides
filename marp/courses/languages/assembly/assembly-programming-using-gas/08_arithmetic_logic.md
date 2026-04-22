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
# Arithmetic and Logical Operations

---

## Arithmetic Operations Overview

![Arithmetic Operations Overview](svg/courses/languages/assembly/assembly-programming-using-gas/08_arithmetic_logic/arithmetic_operations_overview.svg)

---

## Basic Arithmetic Operations

- `add`: Addition
- `sub`: Subtraction
- `mul`: Unsigned multiplication
- `div`: Unsigned division
- `inc`: Increment
- `dec`: Decrement

Example:
```gas
    mov $10, %eax
    add $5, %eax      # EAX = 15
    sub $3, %eax      # EAX = 12
    inc %eax          # EAX = 13
    dec %eax          # EAX = 12
```

---

## Signed Arithmetic Operations

- `imul`: Signed multiplication
- `idiv`: Signed division
- `neg`: Negate (two's complement)

Example:
```gas
    mov $-5, %eax
    imul $-3, %eax    # EAX = 15
    neg %eax          # EAX = -15
```

---

## Multiplication Details

- `mul` (unsigned) and `imul` (signed) multiply by EAX
- Result stored in EDX:EAX (high:low)

Example:
```gas
    mov $1000000, %eax
    mov $1000, %ebx
    mul %ebx          # Result in EDX:EAX
```

---

## Division Details

- `div` (unsigned) and `idiv` (signed) divide EDX:EAX
- Quotient stored in EAX, remainder in EDX

Example:
```gas
    mov $0, %edx
    mov $100, %eax
    mov $3, %ebx
    div %ebx          # EAX = 33, EDX = 1
```

---

## Bitwise Operations

- `and`: Bitwise AND
- `or`: Bitwise OR
- `xor`: Bitwise XOR
- `not`: Bitwise NOT

Example:
```gas
    mov $0b1100, %eax
    and $0b1010, %eax  # EAX = 0b1000
    or $0b0001, %eax   # EAX = 0b1001
    xor $0b1111, %eax  # EAX = 0b0110
    not %eax           # EAX = 0b...11111001
```

---

## Shift Operations

- `shl`: Shift left
- `shr`: Shift right (unsigned)
- `sar`: Shift arithmetic right (signed)
- `rol`: Rotate left
- `ror`: Rotate right

Example:
```gas
    mov $8, %eax
    shl $2, %eax     # EAX = 32 (8 * 2^2)
    shr $1, %eax     # EAX = 16
```

---

## Arithmetic with Carry

- `adc`: Add with carry
- `sbb`: Subtract with borrow

Useful for multi-precision arithmetic:

```gas
    mov $0xFFFFFFFF, %eax
    mov $0xFFFFFFFF, %ebx
    add %ebx, %eax     # EAX = 0xFFFFFFFE, CF = 1
    mov $0, %eax
    adc $0, %eax       # EAX = 1 (from carry)
```

---

## Compare and Test

- `cmp`: Compare (performs subtraction without storing)
- `test`: Test (performs AND without storing)

Used to set flags for conditional jumps:

```gas
    cmp $10, %eax     # Compare EAX with 10
    je equal_ten      # Jump if equal

    test $1, %eax     # Test if EAX is odd
    jnz is_odd        # Jump if not zero (odd)
```

---

## Bit Testing and Manipulation

- `bt`: Bit test
- `bts`: Bit test and set
- `btr`: Bit test and reset
- `btc`: Bit test and complement

Example:
```gas
    mov $0b1010, %eax
    bt $1, %eax      # Test bit 1, CF = 1
    bts $2, %eax     # Set bit 2, EAX = 0b1110
```

---

## SIMD Arithmetic Operations

SIMD instructions for parallel arithmetic:

- `addps`: Add Packed Single-Precision
- `subps`: Subtract Packed Single-Precision
- `mulps`: Multiply Packed Single-Precision
- `divps`: Divide Packed Single-Precision

Example:
```gas
    movaps (%esi), %xmm0
    movaps (%edi), %xmm1
    addps %xmm1, %xmm0   # Add 4 floats in parallel
```

---

## Floating-Point Operations

x87 FPU instructions for floating-point arithmetic:

- `fadd`: Floating-point add
- `fsub`: Floating-point subtract
- `fmul`: Floating-point multiply
- `fdiv`: Floating-point divide

Example:
```gas
    flds var1
    fadds var2
    fstps result
```
