# Functions and the Stack

---

## The Stack

- Last-In-First-Out (LIFO) data structure
- Grows downward in memory
- ESP (Stack Pointer) points to the top of the stack
- Used for:
  - Local variables
  - Function parameters
  - Return addresses
  - Saving registers

---

## Stack Operations

Basic stack instructions:
- `push`: Decrement ESP and store value
- `pop`: Load value and increment ESP

Example:
```gas
    push %eax    # Push EAX onto the stack
    pop %ebx     # Pop top of stack into EBX
```

---

## Function Prologue

Setup at the beginning of a function:

```gas
my_function:
    push %ebp           # Save old base pointer
    mov %esp, %ebp      # Set new base pointer
    sub $16, %esp       # Allocate 16 bytes for local variables
    push %ebx           # Save callee-saved registers
    push %esi
    push %edi
```

---

## Function Epilogue

Cleanup at the end of a function:

```gas
    pop %edi            # Restore callee-saved registers
    pop %esi
    pop %ebx
    mov %ebp, %esp      # Restore stack pointer
    pop %ebp            # Restore base pointer
    ret                 # Return to caller
```

---

## Passing Arguments

Common ways to pass arguments:
1. Via the stack (cdecl calling convention)
1. Via registers (fastcall convention)

Stack example (cdecl):
```gas
    push $20        # Second argument
    push $10        # First argument
    call add_nums
    add $8, %esp    # Clean up stack after call
```

---

## Accessing Parameters on the Stack

With EBP as base pointer:

```gas
add_nums:
    push %ebp
    mov %esp, %ebp
    mov 8(%ebp), %eax   # First parameter
    add 12(%ebp), %eax  # Add second parameter
    # EAX now contains the result
    pop %ebp
    ret
```

---

## Local Variables

Allocating and using local variables:

```gas
my_function:
    push %ebp
    mov %esp, %ebp
    sub $8, %esp        # Allocate 8 bytes for locals
    mov $42, -4(%ebp)   # Initialize first local variable
    mov $10, -8(%ebp)   # Initialize second local variable
    # Use local variables...
    mov %ebp, %esp
    pop %ebp
    ret
```

---

## Preserving Registers

Callee-saved registers: EBX, ESI, EDI, EBP
Caller-saved registers: EAX, ECX, EDX

```gas
my_function:
    push %ebx       # Save callee-saved registers
    push %esi
    # Function body...
    pop %esi        # Restore callee-saved registers
    pop %ebx
    ret
```

---

## Returning Values

Common methods:
1. Via EAX register (for 32-bit values)
2. Via EDX:EAX (for 64-bit values)
3. Via the stack (for larger structures)

Example:
```gas
    mov $42, %eax   # Set return value
    ret             # Return to caller
```

---

## Recursive Functions

Recursive functions call themselves:

```gas
factorial:
    push %ebp
    mov %esp, %ebp
    mov 8(%ebp), %eax   # Get parameter n
    cmp $1, %eax
    jle base_case
    dec %eax
    push %eax
    call factorial
    imul 8(%ebp), %eax
    jmp end
base_case:
    mov $1, %eax
end:
    mov %ebp, %esp
    pop %ebp
    ret
```

---

## Stack Alignment

Some functions (especially system calls) require the stack to be aligned:

```gas
    and $-16, %esp   # Align stack to 16 bytes
    call aligned_function
```

Important for SSE instructions and certain library functions
