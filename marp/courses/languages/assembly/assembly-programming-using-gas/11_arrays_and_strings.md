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

# Working with Arrays and Strings

---

## Arrays and Strings in Memory

![Arrays and strings memory layout in assembly](svg/courses/languages/assembly/assembly-programming-using-gas/11_arrays_and_strings/array_string_memory.svg)

---

## Declaring Arrays

In the data section:

```gas
.data
    int_array:   .long 1, 2, 3, 4, 5
    char_array:  .ascii "Hello"
    float_array: .float 1.0, 2.0, 3.0, 4.0
```

---

## Accessing Array Elements

Using base + index addressing:

```gas
    mov int_array(,%ecx,4), %eax  # Load int_array[ecx] into eax
    mov $2, %ecx
    mov int_array(,%ecx,4), %ebx  # Load int_array[2] into ebx
```

---

## Iterating Through Arrays

Using a loop:

```gas
    mov $0, %ecx           # Initialize counter
    mov $5, %edx           # Array length
loop_start:
    mov int_array(,%ecx,4), %eax
    # Process %eax...
    inc %ecx
    cmp %edx, %ecx
    jl loop_start
```

---

## String Operations

Basic string instructions:
- `movsb`, `movsw`, `movsd`: Move string
- `cmpsb`, `cmpsw`, `cmpsd`: Compare string
- `scasb`, `scasw`, `scasd`: Scan string
- `stosb`, `stosw`, `stosd`: Store string
- `lodsb`, `lodsw`, `lodsd`: Load string

---

## String Operation Prefixes

- `rep`: Repeat
- `repe`/`repz`: Repeat while equal/zero
- `repne`/`repnz`: Repeat while not equal/not zero

Example:
```gas
    cld              # Clear direction flag (forward)
    mov $5, %ecx     # Set counter
    lea src, %esi    # Load source address
    lea dest, %edi   # Load destination address
    rep movsd        # Move 5 dwords
```

---

## Null-terminated Strings

Calculating string length:

```gas
    mov $0, %ecx     # Initialize counter
    mov $str, %edi   # Load string address
count_loop:
    cmp $0, (%edi)   # Check for null terminator
    je done
    inc %ecx         # Increment counter
    inc %edi         # Move to next character
    jmp count_loop
done:
    # Length is in %ecx
```

---

## String Comparison

Using `cmpsb` instruction:

```gas
    mov $str1, %esi
    mov $str2, %edi
    cld
compare_loop:
    cmpsb
    jne not_equal
    cmp $0, (%esi)   # Check for end of string
    jne compare_loop
    # Strings are equal
    jmp done
not_equal:
    # Strings are not equal
done:
```

---

## SIMD String Operations

Using SSE instructions for faster string operations:

```gas
    movdqu (%esi), %xmm0   # Load 16 bytes from source
    movdqu %xmm0, (%edi)   # Store 16 bytes to destination
    add $16, %esi
    add $16, %edi
```

---

## Array of Structures

Defining and accessing:

```gas
.data
    struct Point {
        .long x
        .long y
    }
    points:
        .rept 5
        Point {.long 0, .long 0}
        .endr

.text
    # Accessing x of the second point
    mov points+8, %eax   # 8 = size of Point * index + offset of x
```

---

## Multidimensional Arrays

Declaring and accessing:

```gas
.data
    matrix:
        .long 1, 2, 3
        .long 4, 5, 6
        .long 7, 8, 9

.text
    # Accessing matrix[1][2]
    mov matrix+20, %eax  # 20 = (row * cols + col) * 4
```
