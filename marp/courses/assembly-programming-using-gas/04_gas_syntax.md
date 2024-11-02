# GNU Assembler (GAS) Syntax

---

## AT&T Syntax vs. Intel Syntax

GAS primarily uses AT&T syntax, which differs from Intel syntax:

| Feature | AT&T Syntax | Intel Syntax |
|---------|-------------|--------------|
| Order of operands | Source, Destination | Destination, Source |
| Register names | Prefixed with % | No prefix |
| Immediate values | Prefixed with $ | No prefix |
| Memory references | Offset(Base,Index,Scale) | [Base + Index*Scale + Offset] |

---

## AT&T Syntax Example

```gas
movl $42, %eax
addl $10, (%ebx)
```

Equivalent Intel Syntax:
```nasm
mov eax, 42
add [ebx], 10
```

---

## Directives

Directives are commands to the assembler, not CPU instructions.

Common directives:
- `.text`: Start of code section
- `.data`: Start of data section
- `.bss`: Start of uninitialized data section
- `.globl`: Make a symbol global
- `.equ`: Define a constant

---

## Data Definition Directives

- `.byte`: Define byte(s)
- `.word`: Define 16-bit word(s)
- `.long`: Define 32-bit word(s)
- `.quad`: Define 64-bit word(s)
- `.float`: Define single precision float(s)
- `.double`: Define double precision float(s)
- `.ascii`: Define ASCII string
- `.asciz`: Define null-terminated ASCII string

---

## Example: Data Definition

```gas
.data
    number:     .long 42
    pi:         .double 3.14159
    message:    .asciz "Hello, World!"
```

---

## Pseudo-ops

Pseudo-ops are similar to directives but more complex:

- `.macro` and `.endm`: Define a macro
- `.if`, `.else`, `.endif`: Conditional assembly
- `.rept` and `.endr`: Repeat block of code
- `.include`: Include another file

---

## Example: Macro Definition

```gas
.macro print_string str
    pushl %eax
    pushl $\str
    call printf
    addl $4, %esp
    popl %eax
.endm

.text
.globl main
main:
    print_string hello_msg
    ret

.data
hello_msg: .asciz "Hello, World!\n"
```

---

## Labels

Labels are used to mark locations in code or data:

```gas
.data
start_message:
    .asciz "Program started.\n"

.text
.globl _start
_start:
    # Code here
    jmp exit_program

print_error:
    # Error handling code

exit_program:
    movl $1, %eax  # sys_exit
    xorl %ebx, %ebx
    int $0x80
```

---

## Comments

GAS supports two types of comments:

1. Full-line comments start with `#` or `/* */`
1. End-of-line comments start with `#` or `//`

Example:
```gas
# This is a full-line comment
movl $1, %eax  // This is an end-of-line comment
/* This is a
   multi-line comment */
```

---

## Sections

GAS programs typically have three main sections:

1. `.text`: Contains executable code
1. `.data`: Contains initialized data
1. `.bss`: Contains uninitialized data

Example:

```gas
.section .data
    message: .asciz "Hello, World!\n"

.section .text
.globl _start
_start:
    # Code here

.section .bss
    .lcomm buffer, 1024
```

---

## Assembler Operators

GAS supports various operators for use in expressions:

- Arithmetic: `+`, `-`, `*`, `/`, `%`
- Bitwise: `&`, `|`, `^`, `~`
- Shift: `<<`, `>>`
- Comparison: `<`, `>`, `<=`, `>=`, `==`, `!=`
- Logical: `&&`, `||`, `!`

Example:

```gas
.equ BUFFER_SIZE, 1024
.equ HALF_BUFFER, BUFFER_SIZE / 2
```
