# Flow Control

---

## Unconditional Jumps

The `jmp` instruction:
- Transfers control to a different part of the program
- Can be used for loops, function calls, and more

Example:
```gas
    jmp label     # Jump to label
    # ...
label:
    # Code here
```

---

## Conditional Jumps

Based on the state of the flags register (EFLAGS):

- `je/jz`: Jump if equal / zero
- `jne/jnz`: Jump if not equal / not zero
- `jg/jnle`: Jump if greater (signed)
- `jge/jnl`: Jump if greater or equal (signed)
- `jl/jnge`: Jump if less (signed)
- `jle/jng`: Jump if less or equal (signed)

---

## More Conditional Jumps

- `ja/jnbe`: Jump if above (unsigned)
- `jae/jnb`: Jump if above or equal (unsigned)
- `jb/jnae`: Jump if below (unsigned)
- `jbe/jna`: Jump if below or equal (unsigned)
- `jo`: Jump if overflow
- `jno`: Jump if no overflow
- `js`: Jump if sign (negative)
- `jns`: Jump if no sign (positive or zero)

---

## Using Conditional Jumps

Example: Comparing two numbers

```gas
    mov $10, %eax
    cmp $5, %eax
    jg greater
    # Code for eax <= 5
    jmp end
greater:
    # Code for eax > 5
end:
    # Continue program
```

---

## Loops

Implementing loops using conditional jumps:

```gas
    mov $0, %ecx    # Initialize counter
loop_start:
    # Loop body
    inc %ecx
    cmp $10, %ecx
    jl loop_start   # Jump if less than 10
```

---

## The LOOP Instruction

`loop` instruction: Decrement ECX and jump if not zero

```gas
    mov $10, %ecx
loop_start:
    # Loop body
    loop loop_start
```

Note: Less flexible than manual loops, but can be useful in simple cases

---

## Switch Statements

Implementing switch statements using jump tables:

```gas
    mov some_value, %eax
    cmp $3, %eax        # Ensure value is in range
    ja default_case
    jmp *jump_table(,%eax,4)

jump_table:
    .long case_0
    .long case_1
    .long case_2
    .long case_3

case_0:
    # Handle case 0
    jmp end_switch
# ... other cases ...
default_case:
    # Handle default case
end_switch:
```

---

## Function Calls

Using `call` and `ret` instructions:

```gas
    call my_function
    # Continue here after function returns

my_function:
    # Function body
    ret
```

`call` pushes the return address onto the stack
`ret` pops the return address and jumps to it

---

## Conditional Move Instructions

Conditional moves can sometimes replace branches:

- `cmove/cmovz`: Move if equal / zero
- `cmovne/cmovnz`: Move if not equal / not zero
- `cmovg/cmovnle`: Move if greater (signed)
- `cmovge/cmovnl`: Move if greater or equal (signed)
- `cmovl/cmovnge`: Move if less (signed)
- `cmovle/cmovng`: Move if less or equal (signed)

---

## Using Conditional Moves

Example: Choosing the larger of two numbers

```gas
    mov $10, %eax
    mov $20, %ebx
    cmp %eax, %ebx
    cmovg %ebx, %eax  # EAX = max(EAX, EBX)
```

Can improve performance by avoiding branch mispredictions

---

## Short and Near Jumps

- Short jumps: 8-bit offset (-128 to 127 bytes)
- Near jumps: 32-bit offset (within the same segment)

Most assemblers automatically choose the appropriate jump type

```gas
    jmp short_label  # Force short jump
    jmp near label   # Force near jump
```
