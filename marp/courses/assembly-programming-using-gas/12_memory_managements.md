# Memory Management

---

## Memory Layout

Typical memory layout of a program:
1. Text (Code) segment
1. Data segment
1. BSS segment
1. Heap
1. Stack

---

## Static Memory Allocation

- Allocated at compile time
- Stored in data or BSS segments
- Lifetime is the entire program execution

Example:
```gas
.data
    static_int: .long 42
.bss
    static_array: .space 1000
```

---

## Stack Allocation

- Automatic allocation and deallocation
- Fast, but limited in size
- Local variables, function parameters

Example:
```gas
    sub $16, %esp      # Allocate 16 bytes on stack
    mov $42, (%esp)    # Use allocated memory
    add $16, %esp      # Deallocate 16 bytes
```

---

## Heap Allocation

- Dynamic allocation during runtime
- Flexible size, but slower than stack
- Requires explicit management

System calls:
- `brk`: Change program break
- `mmap`: Map files or devices into memory

---

## Using brk for Heap Allocation

Steps:
1. Get current program break
1. Increment break to allocate memory
1. Use allocated memory
1. Decrement break to free memory

```gas
    # Get current break
    mov $45, %eax      # sys_brk
    xor %ebx, %ebx
    int $0x80
    mov %eax, %esi     # Save current break

    # Allocate memory
    mov $45, %eax
    lea 1000(%esi), %ebx
    int $0x80

    # Use memory...

    # Free memory
    mov $45, %eax
    mov %esi, %ebx
    int $0x80
```

---

## Using mmap for Allocation

Advantages:
- Can allocate memory at specific addresses
- Supports file-backed memory mapping

Example:
```gas
    # Allocate 4096 bytes
    mov $192, %eax     # sys_mmap2
    xor %ebx, %ebx     # Let kernel choose address
    mov $4096, %ecx    # Page size
    mov $3, %edx       # PROT_READ | PROT_WRITE
    mov $34, %esi      # MAP_PRIVATE | MAP_ANONYMOUS
    mov $-1, %edi      # fd (-1 for anonymous mapping)
    xor %ebp, %ebp     # offset
    int $0x80
    # Allocated memory address is in EAX
```

---

## Memory Alignment

- Proper alignment can improve performance
- Some instructions require aligned data
- Use `.align` directive or ensure proper allocation

Example:
```gas
.data
    .align 16
    aligned_data: .space 64
```

---

## Memory Access Patterns

- Sequential access is generally faster
- Minimize cache misses by using appropriate access patterns
- Consider cache line size (typically 64 bytes)

Example of stride-1 access:
```gas
    mov $0, %ecx
loop:
    mov array(,%ecx,4), %eax
    # Process data...
    inc %ecx
    cmp $1000, %ecx
    jl loop
```

---

## Memory Barriers

- Ensure visibility of memory operations across threads
- Types: Full, Read, Write barriers
- x86 is strongly ordered, but still important for portable code

Example (full barrier):
```gas
    mfence
```

---

## Virtual Memory Concepts

- Pages: Fixed-size blocks of memory (typically 4KB)
- Page tables: Map virtual addresses to physical addresses
- TLB (Translation Lookaside Buffer): Cache for page table entries
