# Writing Your First Assembly Program
## Assembly Programming using GAS

---
## "Hello, World!" in Assembly

A simple program to print "Hello, World!" to the console.

```nasm
.section .data
    msg: .ascii "Hello, World!\n"
    len: .long . - msg

.section .text
.globl _start

_start:
    # Write the message to stdout
    movl $4, %eax   # syscall number for write
    movl $1, %ebx   # file descriptor 1 is stdout
    movl $msg, %ecx # address of string to output
    movl len, %edx  # number of bytes to write
    int $0x80       # call kernel

    # Exit the program
    movl $1, %eax   # syscall number for exit
    movl $0, %ebx   # exit status is 0
    int $0x80       # call kernel
```

---
## Assembling and Linking

1. Save the program as `hello.s`
1. Assemble: `as hello.s -o hello.o`
1. Link: `ld hello.o -o hello`
1. Run: `./hello`

Output:

```misc
Hello, World!
```

---

## Program Structure Breakdown

1. `.section .data`: Declares the data section
1. `.section .text`: Declares the code section
1. `.globl _start`: Makes the _start label global
1. `_start:`: Entry point of the program
1. System calls: `write` for output, `exit` to terminate

---

## System Calls

- `int $0x80`: Interrupt to invoke a system call
- Register usage for system calls:
    - `%eax`: System call number
    - `%ebx`, `%ecx`, `%edx`: Arguments

Common system calls:
- 1: exit
- 4: write

---

## Debugging with GDB

1. Compile with debug symbols: `as -g hello.s -o hello.o`
1. Link: `ld hello.o -o hello`
1. Start GDB: `gdb ./hello`
1. Set breakpoint: `break _start`
1. Run: `run`
1. Step through: `stepi`
1. Examine registers: `info registers`

---

## Modifying the Program

Let's change the message:

```nasm
.section .data
    msg: .ascii "Assembly is awesome!\n"
    len: .long . - msg

## ... rest of the code remains the same
```

Reassemble, link, and run to see the new output.

---

## Adding User Input

```nasm
.section .data
    prompt: .ascii "Enter your name: "
    prompt_len: .long . - prompt
    greeting: .ascii "Hello, "
    greeting_len: .long . - greeting

.section .bss
    .lcomm name, 50

.section .text
.globl _start

_start:
    # Print prompt
    movl $4, %eax
    movl $1, %ebx
    movl $prompt, %ecx
    movl prompt_len, %edx
    int $0x80

    # Read input
    movl $3, %eax
    movl $0, %ebx
    movl $name, %ecx
    movl $50, %edx
    int $0x80

    # Print greeting
    movl $4, %eax
    movl $1, %ebx
    movl $greeting, %ecx
    movl greeting_len, %edx
    int $0x80

    # Print name
    movl $4, %eax
    movl $1, %ebx
    movl $name, %ecx
    movl $50, %edx
    int $0x80

    # Exit
    movl $1, %eax
    movl $0, %ebx
    int $0x80
```

---

## Common Errors and Debugging

1. Segmentation fault
    - Often due to accessing invalid memory
    - Use GDB to identify the problematic instruction
1. Incorrect output
    - Check your data declarations
    - Verify system call arguments
1. Assembler errors
    - Syntax errors in your code
    - Incorrect directives or register names

---
## Best Practices
1. Comment your code thoroughly
1. Use meaningful label names
1. Organize your code into logical sections
1. Test small parts of your program incrementally
1. Use debugging tools like GDB to understand program flow

---
## Exercises
1. Modify the "Hello, World!" program to print your name
1. Write a program that adds two numbers and prints the result
1. Create a program that prints numbers from 1 to 10

---
## Additional Resources
- [GAS manual](https://sourceware.org/binutils/docs/as)
- [x86 instruction set reference](https://www.felixcloutier.com/x86)
- [Linux system call table](https://chromium.googlesource.com/chromiumos/docs/+/master/constants/syscalls.md)
