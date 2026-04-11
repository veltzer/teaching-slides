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
# System Calls and File I/O

---

## Introduction to System Calls

- Interface between user programs and the kernel
- Provide access to operating system services
- Invoked using the `int 0x80` instruction on x86
- System call number in EAX
- Arguments in EBX, ECX, EDX, ESI, EDI, EBP

---

## System Call Mechanism

![System call mechanism: user space to kernel space flow with register assignments and common syscall table](svg/courses/languages/assembly/assembly-programming-using-gas/12_system_calls/system_call_mechanism.svg)

---

## Common System Calls

| Number | Name | Description |
|--------|------|-------------|
| 1 | sys_exit | Terminate the program |
| 2 | sys_fork | Create a new process |
| 3 | sys_read | Read from a file descriptor |
| 4 | sys_write | Write to a file descriptor |
| 5 | sys_open | Open a file |
| 6 | sys_close | Close a file descriptor |

---

## File Descriptors

- Integer that uniquely identifies an open file
- Standard file descriptors:
    - 0: stdin (Standard input)
    - 1: stdout (Standard output)
    - 2: stderr (Standard error)

---

## Opening a File

Using `sys_open` system call:

```gas
    mov $5, %eax       # sys_open
    mov $filename, %ebx
    mov $0, %ecx       # O_RDONLY flag
    mov $0644, %edx    # File permissions
    int $0x80
    # File descriptor is returned in EAX
```

---

## Reading from a File

Using `sys_read` system call:

```gas
    mov $3, %eax       # sys_read
    mov file_descriptor, %ebx
    mov $buffer, %ecx
    mov $buffer_size, %edx
    int $0x80
    # Number of bytes read is returned in EAX
```

---

## Writing to a File

Using `sys_write` system call:

```gas
    mov $4, %eax       # sys_write
    mov file_descriptor, %ebx
    mov $buffer, %ecx
    mov $buffer_size, %edx
    int $0x80
    # Number of bytes written is returned in EAX
```

---

## Closing a File

Using `sys_close` system call:

```gas
    mov $6, %eax       # sys_close
    mov file_descriptor, %ebx
    int $0x80
```

---

## Error Handling

- System calls return negative values on error
- Error code is the negative of the errno value
- Check return value after each system call

```gas
    int $0x80
    cmp $0, %eax
    jl error_handler
```

---

## File I/O Example: Copy File

```gas
.data
    src_file: .asciz "source.txt"
    dst_file: .asciz "destination.txt"
    buffer:   .space 1024

.text
.globl _start
_start:
    # Open source file
    mov $5, %eax
    mov $src_file, %ebx
    mov $0, %ecx       # O_RDONLY
    int $0x80
    mov %eax, %esi     # Save source fd

    # Open destination file
    mov $5, %eax
    mov $dst_file, %ebx
    mov $0x241, %ecx   # O_WRONLY | O_CREAT | O_TRUNC
    mov $0644, %edx
    int $0x80
    mov %eax, %edi     # Save destination fd

copy_loop:
    # Read from source
    mov $3, %eax
    mov %esi, %ebx
    mov $buffer, %ecx
    mov $1024, %edx
    int $0x80

    test %eax, %eax
    jz close_files     # EOF reached

    # Write to destination
    mov %eax, %edx     # Number of bytes to write
    mov $4, %eax
    mov %edi, %ebx
    mov $buffer, %ecx
    int $0x80

    jmp copy_loop

close_files:
    # Close source file
    mov $6, %eax
    mov %esi, %ebx
    int $0x80

    # Close destination file
    mov $6, %eax
    mov %edi, %ebx
    int $0x80

    # Exit
    mov $1, %eax
    xor %ebx, %ebx
    int $0x80
```
