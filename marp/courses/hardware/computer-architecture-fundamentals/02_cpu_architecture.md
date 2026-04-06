# CPU Architecture

---

## Table of Contents

1. CPU Overview and Components
1. The ALU and Registers
1. Control Unit and Instruction Cycle
1. Pipelining
1. Branch Prediction
1. Superscalar Execution
1. CISC vs RISC
1. x86 vs ARM
1. Cache Hierarchy
1. Cache Coherence

---

## What is a CPU?

The Central Processing Unit is the "brain" of the computer. It executes
instructions from programs by performing arithmetic, logic, control, and
I/O operations.

```diagram
┌─────────────────────────────────────────────────────┐
│                        CPU                          │
│  ┌──────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ Control  │  │     ALU      │  │  Registers   │  │
│  │  Unit    │──│ (Arithmetic  │──│  (Fast local │  │
│  │ (CU)    │  │  Logic Unit) │  │   storage)   │  │
│  └──────────┘  └──────────────┘  └──────────────┘  │
│       │               │                │            │
│       └───────────────┼────────────────┘            │
│                       │                             │
│              ┌────────┴────────┐                    │
│              │   Internal Bus  │                    │
│              └────────┬────────┘                    │
│  ┌────────────┐  ┌────┴─────┐  ┌────────────────┐  │
│  │ L1 I-Cache │  │ L1 D-Cache│  │ Branch Pred.  │  │
│  └────────────┘  └──────────┘  └────────────────┘  │
└──────────────────────┬──────────────────────────────┘
                       │
              ┌────────┴────────┐
              │  External Bus   │
              └─────────────────┘
```

---

## The Arithmetic Logic Unit (ALU)

The ALU performs all arithmetic and logical operations inside the CPU.

**Arithmetic operations:**
- Addition, subtraction
- Multiplication, division
- Increment, decrement

**Logical operations:**
- AND, OR, NOT, XOR
- Shift left, shift right
- Comparison (sets flags)

```diagram
          ┌───────────┐
 Input A──┤           ├──Result
          │    ALU    │
 Input B──┤           ├──Flags (Zero, Carry, Overflow, Sign)
          │           │
 Opcode───┤           │
          └───────────┘
```

The ALU reads two operands (A and B), performs the operation specified by the
opcode, and produces a result plus status flags.

---

## Status Flags Register

The flags register records the outcome of the last ALU operation.
Conditional branches use these flags to make decisions.

| Flag | Name | Set When |
|------|------|----------|
| ZF | Zero Flag | Result is zero |
| CF | Carry Flag | Unsigned overflow occurred |
| OF | Overflow Flag | Signed overflow occurred |
| SF | Sign Flag | Result is negative (MSB = 1) |
| PF | Parity Flag | Result has even number of 1-bits |

Example: after computing `5 - 5`, ZF=1, SF=0, CF=0, OF=0.
A `JZ` (jump if zero) instruction would take the branch.

---

## CPU Registers

Registers are the fastest storage in a computer -- accessed in a single
clock cycle with zero latency.

**General-purpose registers (x86-64):**

```diagram
┌────────────────────────────────────────────────────┐
│ 64-bit    RAX  RBX  RCX  RDX  RSI  RDI  RSP  RBP │
│ 64-bit    R8   R9   R10  R11  R12  R13  R14  R15  │
├────────────────────────────────────────────────────┤
│ Special   RIP (instruction pointer)                │
│           RFLAGS (status flags)                    │
│           RSP (stack pointer)                      │
├────────────────────────────────────────────────────┤
│ Segment   CS  DS  SS  ES  FS  GS                   │
├────────────────────────────────────────────────────┤
│ Vector    XMM0-XMM15  (128-bit SSE)               │
│           YMM0-YMM15  (256-bit AVX)               │
│           ZMM0-ZMM31  (512-bit AVX-512)           │
└────────────────────────────────────────────────────┘
```

---

## Register Naming in x86-64

The x86-64 registers have sub-register access for backward compatibility:

```diagram
 63                              31              15      7      0
┌────────────────────────────────┬───────────────┬───────┬──────┐
│                                │               │       │  AL  │  8-bit
│                                │               │  AX   │──────│ 16-bit
│                                │     EAX       │───────│──────│ 32-bit
│              RAX               │───────────────│───────│──────│ 64-bit
└────────────────────────────────┴───────────────┴───────┴──────┘
```

- `AL` = low 8 bits of RAX
- `AX` = low 16 bits of RAX
- `EAX` = low 32 bits of RAX
- `RAX` = full 64 bits

Writing to `EAX` zero-extends into `RAX`. Writing to `AX` or `AL` does not.

---

## Register Conventions (System V AMD64 ABI)

On Linux/macOS x86-64, function arguments are passed in registers:

| Argument # | Register | Purpose |
|------------|----------|---------|
| 1st | RDI | First integer/pointer arg |
| 2nd | RSI | Second integer/pointer arg |
| 3rd | RDX | Third integer/pointer arg |
| 4th | RCX | Fourth integer/pointer arg |
| 5th | R8 | Fifth integer/pointer arg |
| 6th | R9 | Sixth integer/pointer arg |
| Return | RAX | Return value |
| Stack ptr | RSP | Stack pointer |
| Base ptr | RBP | Frame pointer (optional) |

Arguments beyond the 6th are passed on the stack. Floating-point arguments
use XMM0-XMM7.

---

## The Control Unit

The control unit orchestrates the CPU. It reads instructions from memory,
decodes them, and generates control signals that tell other components
what to do.

```diagram
┌──────────────────────────────────────────┐
│              Control Unit                │
│                                          │
│  ┌──────────────┐   ┌────────────────┐   │
│  │ Instruction  │   │   Instruction  │   │
│  │  Register    │──>│    Decoder     │   │
│  │   (IR)       │   │                │   │
│  └──────────────┘   └───────┬────────┘   │
│                             │            │
│                    ┌────────┴────────┐   │
│                    │ Control Signal  │   │
│                    │   Generator     │   │
│                    └────────┬────────┘   │
│                             │            │
└─────────────────────────────┼────────────┘
                              │
          ┌───────────────────┼──────────────────┐
          │                   │                  │
     ┌────┴────┐       ┌─────┴─────┐     ┌──────┴──────┐
     │   ALU   │       │ Registers │     │   Memory    │
     └─────────┘       └───────────┘     └─────────────┘
```

---

## The Instruction Cycle: Fetch-Decode-Execute

Every instruction goes through a fundamental cycle:

```diagram
    ┌─────────┐     ┌──────────┐     ┌───────────┐     ┌────────────┐
    │  FETCH  │────>│  DECODE  │────>│  EXECUTE  │────>│ WRITE-BACK │
    │         │     │          │     │           │     │            │
    │ Read    │     │ Identify │     │ Perform   │     │ Store      │
    │ instr   │     │ opcode & │     │ operation │     │ result in  │
    │ from    │     │ operands │     │ in ALU    │     │ register   │
    │ memory  │     │          │     │           │     │ or memory  │
    └─────────┘     └──────────┘     └───────────┘     └────────────┘
         ^                                                    │
         │                                                    │
         └────────────────────────────────────────────────────┘
                        (next instruction)
```

**Step by step:**

1. **Fetch**: Read instruction at address in PC (Program Counter / RIP)
2. **Decode**: Determine what operation and which operands
3. **Execute**: ALU performs the computation or address calculation
4. **Memory Access**: Load from or store to memory (if needed)
5. **Write-Back**: Write result to destination register

---

## Example: Instruction Execution Trace

Consider the x86 instruction: `ADD RAX, RBX`

```misc
Cycle 1 - FETCH:
    Memory[RIP] → Instruction Register
    RIP = RIP + instruction_length

Cycle 2 - DECODE:
    IR = "ADD RAX, RBX"
    Opcode = ADD
    Source1 = RAX, Source2 = RBX, Dest = RAX

Cycle 3 - EXECUTE:
    ALU_input_A = value of RAX
    ALU_input_B = value of RBX
    ALU_operation = ADD
    ALU_output = A + B

Cycle 4 - WRITE-BACK:
    RAX = ALU_output
    Update RFLAGS (ZF, CF, OF, SF)
```

Without pipelining, only one instruction completes every 4+ clock cycles.

---

## Pipelining

Pipelining overlaps instruction execution stages, like an assembly line.
While one instruction is being executed, the next is being decoded, and
the one after that is being fetched.

```diagram
Clock:    1    2    3    4    5    6    7    8
         ┌────┬────┬────┬────┐
Instr 1: │ IF │ ID │ EX │ WB │
         └────┴────┴────┴────┘
              ┌────┬────┬────┬────┐
Instr 2:     │ IF │ ID │ EX │ WB │
              └────┴────┴────┴────┘
                   ┌────┬────┬────┬────┐
Instr 3:          │ IF │ ID │ EX │ WB │
                   └────┴────┴────┴────┘
                        ┌────┬────┬────┬────┐
Instr 4:               │ IF │ ID │ EX │ WB │
                        └────┴────┴────┴────┘

IF = Instruction Fetch    ID = Instruction Decode
EX = Execute              WB = Write Back
```

**Throughput**: After the pipeline is full, one instruction completes per cycle.
**Latency**: Each instruction still takes 4 cycles from start to finish.

---

## Pipeline Hazards

Three types of hazards can stall or break the pipeline:

**1. Data Hazards** -- An instruction needs data not yet produced:
```asm
ADD RAX, RBX    ; produces RAX
SUB RCX, RAX    ; needs RAX -- but ADD hasn't written it yet!
```
Solution: **forwarding/bypassing** -- route ALU output directly to next stage.

**2. Control Hazards** -- Branch instructions change flow:
```asm
CMP RAX, 0
JZ  label       ; do we take the branch? Pipeline already fetched next instr
ADD RBX, 1      ; this might need to be flushed
```
Solution: **branch prediction** (next slide).

**3. Structural Hazards** -- Two instructions need the same hardware:
```misc
Both instruction fetch and data load need memory in same cycle
```
Solution: **separate I-cache and D-cache** (Harvard architecture internally).

---

## Branch Prediction

Modern CPUs predict branch outcomes to keep the pipeline full.
A misprediction costs 10-20+ cycles (pipeline flush).

**Static prediction:**
- Always predict "not taken"
- Backward branches predicted taken (loops)

**Dynamic prediction -- 2-bit saturating counter:**

```diagram
                    taken
    ┌──────────┐ ─────────> ┌──────────┐
    │ Strongly │             │ Strongly │
    │ Not Taken│ <───────── │  Taken   │
    └────┬─────┘  not taken └─────┬────┘
         │ taken                  │ not taken
         v                        v
    ┌──────────┐             ┌──────────┐
    │  Weakly  │ ──taken──> │  Weakly  │
    │ Not Taken│             │  Taken   │
    │          │ <─not taken─│          │
    └──────────┘             └──────────┘
```

Modern CPUs (like Intel Alder Lake) use neural branch predictors with
97%+ accuracy on typical workloads.

---

## Branch Prediction Impact

Why does branch prediction matter? Consider a tight loop:

```c
// Summing an array -- branch at loop condition
int sum = 0;
for (int i = 0; i < N; i++) {   // branch: i < N
    if (data[i] > 128) {         // branch: data dependent
        sum += data[i];
    }
}
```

If `data` is sorted, the `data[i] > 128` branch is highly predictable:
first all "not taken", then all "taken". Prediction accuracy ~99%.

If `data` is unsorted, the branch is essentially random.
Prediction accuracy ~50%. Massive performance penalty.

**Benchmark result (typical):**
| Data | Time |
|------|------|
| Sorted array | ~5 ms |
| Unsorted array | ~15 ms |

Same algorithm, same data, 3x slowdown from branch misprediction.

---

## Superscalar Execution

A superscalar CPU can issue multiple instructions per clock cycle.
It has multiple execution units working in parallel.

```diagram
┌──────────────────────────────────────────────────────┐
│                  Superscalar CPU                     │
│                                                      │
│  ┌──────────────────────────────────────────────┐    │
│  │          Instruction Fetch & Decode          │    │
│  │          (fetches 4-6 instr/cycle)           │    │
│  └──────────────────────┬───────────────────────┘    │
│                         │                            │
│  ┌──────────────────────┴───────────────────────┐    │
│  │           Instruction Scheduler              │    │
│  │         (out-of-order dispatch)              │    │
│  └──┬──────┬──────┬──────┬──────┬──────┬────────┘    │
│     │      │      │      │      │      │             │
│  ┌──┴──┐┌──┴──┐┌──┴──┐┌──┴──┐┌──┴──┐┌──┴──┐         │
│  │ALU 1││ALU 2││ALU 3││FPU 1││FPU 2││ AGU │         │
│  └─────┘└─────┘└─────┘└─────┘└─────┘└─────┘         │
│                                                      │
│  ALU = Arithmetic Logic Unit                         │
│  FPU = Floating Point Unit                           │
│  AGU = Address Generation Unit                       │
└──────────────────────────────────────────────────────┘
```

A modern Intel/AMD core can retire 4-6 instructions per cycle.

---

## Out-of-Order Execution

Modern CPUs do not execute instructions in program order. They find
independent instructions and execute them whenever their operands are ready.

```misc
Original order:           Reordered execution:
1: LOAD  R1, [addr1]      1: LOAD R1, [addr1]    (cycle 1, cache miss!)
2: ADD   R2, R1, 1        4: MUL  R5, R3, R4     (cycle 1, independent)
3: STORE [addr2], R2      5: ADD  R6, R5, 1      (cycle 2, depends on 4)
4: MUL   R5, R3, R4       2: ADD  R2, R1, 1      (cycle ~50, R1 ready)
5: ADD   R6, R5, 1        3: STORE [addr2], R2   (cycle 51)
```

Key hardware for OoO execution:
- **Reorder Buffer (ROB)**: tracks instruction order for correct retirement
- **Reservation Stations**: hold instructions waiting for operands
- **Register Renaming**: eliminates false dependencies (WAR, WAW hazards)

---

## CISC vs RISC

Two fundamental CPU design philosophies:

| Aspect | CISC | RISC |
|--------|------|------|
| Full name | Complex Instruction Set | Reduced Instruction Set |
| Instructions | Many, variable-length | Few, fixed-length |
| Complexity | In hardware | In compiler |
| Examples | x86, x86-64 | ARM, RISC-V, MIPS, PowerPC |
| Registers | Fewer (historically) | Many (32+) |
| Memory access | Many instructions can access memory | Load/Store only |
| Encoding | Variable (1-15 bytes on x86) | Fixed (4 bytes on ARM) |
| Decode | Complex, multi-cycle | Simple, single-cycle |
| Power efficiency | Higher power | Lower power |
| Philosophy | Do more per instruction | Do less but faster |

---

## CISC Example: x86

x86 has complex instructions that do multiple things at once:

```asm
; x86: single instruction does load + compare + conditional jump
REP MOVSB          ; copy RCX bytes from [RSI] to [RDI]
                   ; equivalent to a memcpy loop!

LOOP label         ; decrement RCX, jump if not zero

ENTER 16, 0        ; create stack frame: push RBP, mov RBP RSP, sub RSP 16
```

Variable-length instruction encoding:
```misc
90                      ; NOP                    (1 byte)
48 89 C3                ; MOV RBX, RAX           (3 bytes)
48 C7 C0 01 00 00 00    ; MOV RAX, 1             (7 bytes)
C4 E2 7D 36 04 0E       ; VPERMD YMM0, YMM0...  (6 bytes)
```

Modern x86 CPUs internally decompose CISC instructions into micro-ops (uops)
that are RISC-like internally.

---

## RISC Example: ARM

ARM has simple, fixed-size instructions:

```asm
; ARM AArch64: all instructions are 4 bytes
ADD  X0, X1, X2        ; X0 = X1 + X2
LDR  X3, [X4, #8]      ; X3 = memory[X4 + 8]
STR  X5, [X6]           ; memory[X6] = X5
CBZ  X0, label          ; compare and branch if zero
```

ARM design principles:
- All instructions same size (easy to decode, easy to pipeline)
- Load/Store architecture (only LDR/STR access memory)
- Conditional execution (reduces branches)
- Large register file (31 general-purpose 64-bit registers)

---

## x86 vs ARM: Modern Comparison

| Feature | x86-64 (Intel/AMD) | ARM (AArch64) |
|---------|-------------------|----------------|
| Market | Desktop, Server, Laptop | Mobile, Embedded, Server |
| Power | 15-250W typical | 1-30W typical |
| Performance/Watt | Good | Excellent |
| ISA license | Intel/AMD only | Licensed to many vendors |
| Software | Vast legacy ecosystem | Growing rapidly |
| Server examples | Intel Xeon, AMD EPYC | AWS Graviton, Ampere Altra |
| Desktop examples | Intel Core, AMD Ryzen | Apple M-series |
| Decode complexity | High (variable length) | Low (fixed length) |
| Transistor budget | More on decode | More on execution units |

Apple's M-series chips demonstrated that ARM can match or exceed x86
performance while using far less power.

---

## The Memory Wall Problem

CPU speed has grown much faster than memory speed. This gap is the
"memory wall" and is the reason caches exist.

```diagram
    Access Time (approximate):
    ┌──────────────────────────────────────────┐
    │ Register     :  ~0.3 ns    (1 cycle)     │
    │ L1 Cache     :  ~1 ns      (3-4 cycles)  │
    │ L2 Cache     :  ~3-5 ns    (10-15 cycles) │
    │ L3 Cache     :  ~10-20 ns  (30-60 cycles) │
    │ Main Memory  :  ~50-100 ns (150-300 cyc)  │
    │ SSD          :  ~100 us    (300k cycles)   │
    │ HDD          :  ~10 ms     (30M cycles)    │
    └──────────────────────────────────────────┘

    Analogy (if register = 1 second):
    Register     :  1 second
    L1 Cache     :  3 seconds
    L2 Cache     :  15 seconds
    L3 Cache     :  1 minute
    Main Memory  :  5 minutes
    SSD          :  3.8 days
    HDD          :  1 year
```

---

## Cache Hierarchy

Modern CPUs use a multi-level cache hierarchy to bridge the memory wall:

```diagram
┌─────────────────────────────────────────────────────┐
│                   CPU Core 0                        │
│  ┌───────────────────────────────────────────┐      │
│  │  L1 I-Cache    │    L1 D-Cache            │      │
│  │  32 KB, ~1 ns  │    32-48 KB, ~1 ns       │      │
│  └───────────────────────────────────────────┘      │
│  ┌───────────────────────────────────────────┐      │
│  │        L2 Cache (Unified)                 │      │
│  │        256 KB - 1.25 MB, ~3-5 ns          │      │
│  └───────────────────────────────────────────┘      │
└─────────────────────────┬───────────────────────────┘
                          │
┌─────────────────────────┴───────────────────────────┐
│              L3 Cache (Shared across cores)          │
│              8-96 MB, ~10-20 ns                      │
└─────────────────────────┬───────────────────────────┘
                          │
┌─────────────────────────┴───────────────────────────┐
│                 Main Memory (DRAM)                   │
│                 8-512+ GB, ~50-100 ns                │
└─────────────────────────────────────────────────────┘
```

L1 is split into instruction cache (I-Cache) and data cache (D-Cache).
L2 and L3 are unified (hold both instructions and data).

---

## Cache Lines and Spatial Locality

Caches do not store individual bytes. They store **cache lines**, typically
64 bytes on x86.

```diagram
Memory address: 0x1000
                ┌────────────────────────────────────────────┐
Cache line:     │ byte 0 │ byte 1 │ byte 2 │ ... │ byte 63  │
                └────────────────────────────────────────────┘
                0x1000   0x1001   0x1002         0x103F

When you access address 0x1010, the entire 64-byte line
(0x1000 - 0x103F) is loaded into cache.
```

This exploits **spatial locality**: if you access one byte, you are likely
to access nearby bytes soon.

**Implication for programming:**
```c
// GOOD: sequential access, uses spatial locality
for (int i = 0; i < N; i++)
    sum += array[i];          // next element is in same cache line

// BAD: strided access, wastes cache lines
for (int i = 0; i < N; i += 16)
    sum += array[i];          // skips most of each cache line
```

---

## Cache Associativity

Where can a cache line be placed? This defines associativity:

```diagram
Direct-mapped (1-way):     Each address maps to exactly one cache slot
┌───┬───┬───┬───┬───┬───┬───┬───┐
│ 0 │ 1 │ 2 │ 3 │ 4 │ 5 │ 6 │ 7 │  ← cache slots
└───┴───┴───┴───┴───┴───┴───┴───┘
  Address 0x100 → always slot 0 (conflict if 0x200 also maps here)

Fully associative:         Any address can go in any slot
  Most flexible, but expensive to search

N-way set associative:     Each address maps to a SET of N slots
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│ Set 0            │ │ Set 1            │ │ Set 2            │
│ Way0 Way1 ... WN │ │ Way0 Way1 ... WN │ │ Way0 Way1 ... WN │
└─────────────────┘ └─────────────────┘ └─────────────────┘
```

**Typical modern CPUs:**
- L1: 8-12 way set associative
- L2: 8-16 way set associative
- L3: 12-20 way set associative

---

## Cache Replacement Policies

When a cache set is full and a new line must be loaded, which line is evicted?

| Policy | Description | Used In |
|--------|-------------|---------|
| LRU | Least Recently Used | Approximated in L1/L2 |
| Pseudo-LRU | Tree-based LRU approximation | Common in hardware |
| Random | Randomly select victim | Some ARM designs |
| RRIP | Re-Reference Interval Prediction | Intel L3 |

**LRU example (4-way set):**
```misc
Access sequence: A B C D E

After A: [A _ _ _]         A is most recent
After B: [A B _ _]         B is most recent
After C: [A B C _]         C is most recent
After D: [A B C D]         Full, A is LRU
After E: [E B C D]         A evicted (was LRU), E takes its place
```

---

## Write Policies

When the CPU writes data, when does it update main memory?

**Write-Through:**
```diagram
CPU Write ──> Update Cache ──> Update Memory (immediately)
                                  │
                              Slow but simple
                              Memory always consistent
```

**Write-Back:**
```diagram
CPU Write ──> Update Cache ──> Mark line "dirty"
                                  │
                              Memory updated only on eviction
                              Fast but complex
                              Used in modern CPUs
```

**Write-Allocate vs No-Write-Allocate:**
- Write-Allocate: on a write miss, load the line into cache first, then write
- No-Write-Allocate: on a write miss, write directly to memory, skip cache

Modern CPUs typically use **write-back + write-allocate**.

---

## Cache Coherence Problem

In multi-core systems, each core has its own L1/L2 cache. If two cores
cache the same memory address, writes by one core must be visible to others.

```diagram
    Core 0                 Core 1
┌──────────┐          ┌──────────┐
│ L1 Cache │          │ L1 Cache │
│ X = 42   │          │ X = 42   │  (both cached same address)
└────┬─────┘          └─────┬────┘
     │                      │
     │   Core 0 writes      │
     │   X = 99             │
     │                      │
│ X = 99   │          │ X = 42   │  ← INCOHERENT!
                              Core 1 still sees stale value
```

Solution: **cache coherence protocols**.

---

## MESI Protocol

The most common cache coherence protocol. Each cache line has one of
four states:

| State | Meaning |
|-------|---------|
| **M**odified | Line is dirty, only in this cache, must write back |
| **E**xclusive | Line is clean, only in this cache |
| **S**hared | Line is clean, may be in other caches too |
| **I**nvalid | Line is not valid, treat as cache miss |

```diagram
State transitions (simplified):

     Read hit     ┌───┐
    ┌────────────>│ E │──── Other core reads ────> S
    │             └───┘
    │               │
    │          Write hit
    │               │
    │               v
    │             ┌───┐
    │             │ M │──── Other core reads ────> S (flush dirty data)
    │             └───┘
    │
  ┌───┐          ┌───┐
  │ I │─ Read ──>│ S │──── Write ────> M (invalidate others)
  └───┘          └───┘
```

When Core 0 writes to a Shared line, it sends an "invalidate" message
to all other cores, forcing them to mark their copies Invalid.

---

## Cache Performance: Key Metrics

Understanding cache behavior is essential for performance tuning:

**Hit rate**: percentage of accesses found in cache (target: >95% for L1)

**Miss types:**
- **Compulsory (cold)**: first access to a line, unavoidable
- **Capacity**: cache is too small to hold all needed data
- **Conflict**: multiple addresses map to same set

**Measuring cache performance on Linux:**

```bash
# Using perf to measure cache misses
perf stat -e cache-references,cache-misses,L1-dcache-loads,\
L1-dcache-load-misses,LLC-loads,LLC-load-misses ./my_program

# Example output:
#  1,234,567,890  cache-references
#      5,678,901  cache-misses     # 0.46% of all refs
#  2,345,678,901  L1-dcache-loads
#     12,345,678  L1-dcache-load-misses  # 0.53% of L1 loads
```

---

## Summary: CPU Architecture

```diagram
┌─────────────────────────────────────────────────────────┐
│                    Modern CPU Overview                   │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Core Components:                                       │
│  - ALU performs arithmetic/logic operations              │
│  - Registers provide fastest storage (sub-nanosecond)   │
│  - Control Unit orchestrates fetch-decode-execute        │
│                                                         │
│  Performance Features:                                  │
│  - Pipelining: overlap instruction stages               │
│  - Superscalar: multiple instructions per cycle         │
│  - Out-of-Order: execute ready instructions first       │
│  - Branch Prediction: speculate on branch outcomes      │
│                                                         │
│  Memory Hierarchy:                                      │
│  - L1/L2/L3 caches bridge the memory wall              │
│  - Cache coherence (MESI) keeps multi-core consistent  │
│                                                         │
│  ISA Families:                                          │
│  - CISC (x86): complex instructions, huge ecosystem    │
│  - RISC (ARM): simple instructions, power efficient    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```
