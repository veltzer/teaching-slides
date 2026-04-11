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
# Real-world Applications and Projects

---

## Real-World Assembly Use Cases

![Real-world assembly use cases overview](svg/courses/languages/assembly/assembly-programming-using-gas/17_real_world/real_world_use_cases.svg)

---

## Implementing Simple Algorithms

- Great way to practice assembly programming
- Examples:
    - Sorting algorithms
    - Search algorithms
    - Cryptographic functions

---

## Bubble Sort in Assembly

```nasm
.globl bubble_sort
bubble_sort:
    movl 4(%esp), %esi   # array pointer
    movl 8(%esp), %ecx   # array size
    decl %ecx            # size - 1 for outer loop
outer_loop:
    xorl %ebx, %ebx      # flag for swaps
    movl %esi, %edi      # reset to start of array
    movl %ecx, %edx      # copy loop counter
inner_loop:
    movl (%edi), %eax
    cmpl %eax, 4(%edi)
    jge next_pair
    xchgl %eax, 4(%edi)
    movl %eax, (%edi)
    incl %ebx            # set swap flag
next_pair:
    addl $4, %edi        # move to next pair
    decl %edx
    jnz inner_loop
    test %ebx, %ebx      # check if any swaps occurred
    jz done
    loop outer_loop
done:
    ret
```

---

## Writing Device Drivers

- Interface between hardware and OS
- Requires understanding of:
    - Hardware specifications
    - OS kernel API
    - Low-level I/O operations

---

## Simple Character Device Driver

```c
#include <linux/module.h>
#include <linux/fs.h>

static int device_open(struct inode *, struct file *);
static int device_release(struct inode *, struct file *);
static ssize_t device_read(struct file *, char *, size_t, loff_t *);
static ssize_t device_write(struct file *, const char *, size_t, loff_t *);

static struct file_operations fops = {
    .read = device_read,
    .write = device_write,
    .open = device_open,
    .release = device_release
};

int init_module(void) {
    major_num = register_chrdev(0, DEVICE_NAME, &fops);
    if (major_num < 0) {
        printk(KERN_ALERT "Failed to register a major number\n");
        return major_num;
    }
    printk(KERN_INFO "Registered character device with major number %d\n", major_num);
    return 0;
}

void cleanup_module(void) {
    unregister_chrdev(major_num, DEVICE_NAME);
    printk(KERN_INFO "Unregistered character device\n");
}

module_init(init_module);
module_exit(cleanup_module);
```

---

## Reverse Engineering

- Analyzing compiled binaries
- Understanding program behavior without source code
- Tools: IDA Pro, Ghidra, radare2

---

## Basic Reverse Engineering Workflow

1. Obtain the binary
1. Analyze file format and architecture
1. Disassemble the code
1. Identify key functions and data structures
1. Reconstruct program logic
1. Document findings

---

## Disassembly Example

Original C code:
```c
int add(int a, int b) {
    return a + b;
}
```

Disassembled x86 code:
```nasm
add:
    push ebp
    mov ebp, esp
    mov eax, [ebp+8]  ; Load a
    add eax, [ebp+12] ; Add b
    pop ebp
    ret
```

---

## Security Applications

- Vulnerability assessment
- Exploit development
- Malware analysis

---

## Buffer Overflow Example

Vulnerable C code:
```c
void vulnerable_function(char *input) {
    char buffer[64];
    strcpy(buffer, input);
}
```

Exploit in assembly:

```nasm
section .text
global _start

_start:
    ; Create a large input string
    push 0x41414141  ; "AAAA"
    mov ecx, esp
    mov edx, 100     ; length > 64

    ; Call vulnerable_function
    push ecx
    call vulnerable_function

    ; Exit
    mov eax, 1
    xor ebx, ebx
    int 0x80
```

---

## Malware Analysis Techniques

1. Static Analysis
    - Examine without running
    - Disassemble and analyze code structure
1. Dynamic Analysis
    - Run in controlled environment
    - Monitor behavior, network activity, etc.
1. Memory Analysis
    - Examine process memory dumps
    - Identify hidden functionality

---

## Project Ideas

1. Implement a simple encryption algorithm
1. Write a basic bootloader
1. Create a minimal operating system kernel
1. Develop a game in assembly (e.g., Pong, Snake)
1. Build a simple compiler or interpreter
