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
# Debugging and Tools

---

## GDB for Assembly Programs
- GNU Debugger (GDB)
- Powerful tool for debugging assembly code
- Supports both source-level and machine-level debugging

---

## GDB Debugging Workflow

![GDB debugging workflow flowchart with key assembly-level commands for registers, memory, and stepping](svg/courses/languages/assembly/assembly-programming-using-gas/18_debugging/gdb_debugging_workflow.svg)

---

## Compiling for Debugging

```bash
as -g program.s -o program.o
ld -g program.o -o program
```

The `-g` flag includes debugging information.

---

## Basic GDB Commands

- `run` (r): Start the program
- `break` (b): Set a breakpoint
- `continue` (c): Continue execution
- `step` (s): Step into
- `next` (n): Step over
- `print` (p): Print value
- `info registers`: Show register values

---

## GDB Example Session

```gdb
$ gdb ./program
(gdb) break _start
(gdb) run
(gdb) info registers
(gdb) stepi
(gdb) print $eax
(gdb) x/10i $eip
```

---

## Examining Memory in GDB

- `x/nfu addr`: Examine memory
    - n: number of units to display
    - f: format (x: hex, d: decimal, u: unsigned, i: instruction)
    - u: unit size (b: byte, h: halfword, w: word, g: giant word)

Example:

```gdb
(gdb) x/10xw $esp
```

---

## Objdump

- Displays information about object files
- Useful for disassembling binary files

Basic usage:
```bash
objdump -d program
```

---

## Objdump Output Example

```misc
0000000000001129 <main>:
    1129:   55                      push   %rbp
    112a:   48 89 e5                mov    %rsp,%rbp
    112d:   48 83 ec 10             sub    $0x10,%rsp
    1131:   c7 45 fc 00 00 00 00    movl   $0x0,-0x4(%rbp)
    1138:   83 7d fc 09             cmpl   $0x9,-0x4(%rbp)
    113c:   7f 23                   jg     1161 <main+0x38>
    113e:   8b 45 fc                mov    -0x4(%rbp),%eax
    1141:   89 c6                   mov    %eax,%esi
    1143:   48 8d 3d ba 0e 00 00    lea    0xeba(%rip),%rdi
    114a:   b8 00 00 00 00          mov    $0x0,%eax
    114f:   e8 dc fe ff ff          callq  1030 <printf@plt>
    1154:   8b 45 fc                mov    -0x4(%rbp),%eax
    1157:   83 c0 01                add    $0x1,%eax
    115a:   89 45 fc                mov    %eax,-0x4(%rbp)
    115d:   eb d9                   jmp    1138 <main+0xf>
    115f:   eb 05                   jmp    1166 <main+0x3d>
    1161:   b8 00 00 00 00          mov    $0x0,%eax
    1166:   c9                      leaveq
    1167:   c3                      retq
```

---

## Other Binary Analysis Tools

- `nm`: List symbols from object files
- `readelf`: Display information about ELF files
- `strings`: Print printable strings in files
- `ltrace`: Library call tracer
- `strace`: System call tracer

---

## Performance Profiling

- Identify performance bottlenecks
- Tools:
    - `gprof`: GNU Profiler
    - `perf`: Linux profiling tool
    - Valgrind

---

## Using gprof

1. Compile with profiling support:

```bash
gcc -pg program.c -o program
```

1. Run the program:

```bash
./program
```

1. Analyze the profile:

```bash
gprof program gmon.out > analysis.txt
```

---

## perf Example

Record performance data:
```bash
perf record ./program
```

Analyze the data:
```bash
perf report
```

---

## Valgrind

- Suite of debugging and profiling tools
- Memcheck: Memory error detector
- Cachegrind: Cache and branch-prediction profiler
- Callgrind: Call-graph generating cache profiler

Example:
```bash
valgrind --tool=callgrind ./program
```

---

## Debugging Tips

1. Use meaningful labels in your code
1. Comment your code thoroughly
1. Test small code sections independently
1. Use print statements for quick debugging
1. Leverage debugging symbols (-g flag)
