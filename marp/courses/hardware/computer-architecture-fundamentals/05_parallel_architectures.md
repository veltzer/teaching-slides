# Parallel Architectures

---

## Table of Contents

1. Why Parallelism?
1. Flynn's Taxonomy
1. SISD, SIMD, MISD, MIMD
1. Multi-Core Processors
1. Hyper-Threading and SMT
1. NUMA vs UMA Memory
1. GPU Architecture
1. Vector Processing and SIMD Instructions
1. Interconnects Between Cores
1. Cache Coherence in Multiprocessors
1. Amdahl's Law
1. Gustafson's Law

---

## Why Parallelism?

Single-core CPU performance hit a wall around 2005. Clock speeds stopped
increasing due to power and thermal limits. The only path forward is
parallelism: doing more work simultaneously.

```diagram
    Clock Frequency Over Time:

    GHz
    4 │                    ┌──────────────────── Wall
    3 │               ╱────┘
    2 │          ╱────┘
    1 │     ╱────┘
      │╱────┘
    0 └──────────────────────────────────────
      1990  1995  2000  2005  2010  2015  2020

    Core Count Over Time:

    Cores
    64│                              ╱────
    32│                         ╱────┘
    16│                    ╱────┘
     8│               ╱────┘
     4│          ╱────┘
     2│     ╱────┘
     1│─────┘
      └──────────────────────────────────────
      1990  1995  2000  2005  2010  2015  2020
```

The shift from "faster cores" to "more cores" fundamentally changed how
software must be written.

---

## Flynn's Taxonomy

Michael Flynn (1966) classified computer architectures by how many
instruction streams and data streams they process simultaneously.

```diagram
┌──────────────────────────────────────────────────────┐
│                Flynn's Taxonomy                      │
│                                                      │
│              Single Data    Multiple Data             │
│           ┌──────────────┬──────────────┐            │
│  Single   │              │              │            │
│  Instr    │    SISD       │    SIMD       │            │
│           │              │              │            │
│           ├──────────────┼──────────────┤            │
│  Multiple │              │              │            │
│  Instr    │    MISD       │    MIMD       │            │
│           │              │              │            │
│           └──────────────┴──────────────┘            │
└──────────────────────────────────────────────────────┘
```

| Category | Instructions | Data | Examples |
|----------|-------------|------|----------|
| SISD | Single | Single | Classic uniprocessor |
| SIMD | Single | Multiple | GPU, vector units, SSE/AVX |
| MISD | Multiple | Single | Rare (fault tolerance) |
| MIMD | Multiple | Multiple | Multi-core, clusters |

---

## SISD: Single Instruction, Single Data

The traditional von Neumann architecture. One instruction stream operates
on one data element at a time.

```diagram
┌────────────────┐     ┌────────────────┐
│  Instruction   │────>│  Processing    │────> Result
│    Stream      │     │    Unit        │
└────────────────┘     └────────┬───────┘
                                │
                       ┌────────┴───────┐
                       │   Data Stream  │
                       │   (one item)   │
                       └────────────────┘

Example: scalar addition
    A[0] = B[0] + C[0]    (cycle 1)
    A[1] = B[1] + C[1]    (cycle 2)
    A[2] = B[2] + C[2]    (cycle 3)
    A[3] = B[3] + C[3]    (cycle 4)
    ... 4 additions take 4 cycles
```

Historical examples: early Intel 8086, Motorola 68000.
Modern CPUs are technically SISD at the core level but incorporate
SIMD extensions internally.

---

## SIMD: Single Instruction, Multiple Data

One instruction operates on multiple data elements simultaneously.
This is the foundation of vector processing and GPU computing.

```diagram
┌────────────────┐     ┌────────────────────────────┐
│  Instruction   │────>│     Processing Units       │
│   Stream       │     │  ┌────┐┌────┐┌────┐┌────┐ │
│  (one ADD)     │     │  │ PU0││ PU1││ PU2││ PU3│ │
└────────────────┘     │  └──┬─┘└──┬─┘└──┬─┘└──┬─┘ │
                       └─────┼─────┼─────┼─────┼───┘
                             │     │     │     │
                       ┌─────┴─────┴─────┴─────┴───┐
                       │      Data Stream           │
                       │  D0    D1    D2    D3      │
                       └────────────────────────────┘

Example: SIMD addition
    A[0..3] = B[0..3] + C[0..3]    (single cycle!)
    ... 4 additions take 1 cycle
```

Implementations: SSE (4 floats), AVX (8 floats), AVX-512 (16 floats),
ARM NEON (4 floats), GPU warps (32 threads).

---

## MISD: Multiple Instructions, Single Data

Multiple instruction streams operate on the same data stream.
This is the rarest category and mainly theoretical.

```diagram
┌──────────────────┐
│ Instruction      │──┐
│ Stream 1         │  │
└──────────────────┘  │     ┌────────────────┐
                      ├────>│  Single Data   │──> Results
┌──────────────────┐  │     │    Stream      │    (compared)
│ Instruction      │──┘     └────────────────┘
│ Stream 2         │
└──────────────────┘
```

**Practical uses:**
- Fault-tolerant systems: run the same computation with different
  algorithms, compare results (Space Shuttle flight computer)
- Systolic arrays: data flows through a pipeline of different
  processing stages

Most textbooks consider MISD largely theoretical with very few
real-world implementations.

---

## MIMD: Multiple Instructions, Multiple Data

Multiple independent processors execute different instructions on
different data. This is the most common parallel architecture today.

```diagram
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ Instruction  │  │ Instruction  │  │ Instruction  │
│  Stream 0    │  │  Stream 1    │  │  Stream 2    │
└──────┬───────┘  └──────┬───────┘  └──────┬───────┘
       │                 │                 │
┌──────┴───────┐  ┌──────┴───────┐  ┌──────┴───────┐
│ Processing   │  │ Processing   │  │ Processing   │
│   Unit 0     │  │   Unit 1     │  │   Unit 2     │
└──────┬───────┘  └──────┬───────┘  └──────┬───────┘
       │                 │                 │
┌──────┴───────┐  ┌──────┴───────┐  ┌──────┴───────┐
│   Data 0     │  │   Data 1     │  │   Data 2     │
└──────────────┘  └──────────────┘  └──────────────┘
```

**Examples:**
- Multi-core CPUs (each core runs its own thread)
- Multi-socket servers (multiple CPUs on one motherboard)
- Distributed clusters (many machines connected by network)

MIMD is the dominant paradigm for general-purpose computing.

---

## Multi-Core Processors

A multi-core processor integrates multiple independent CPU cores
on a single die (chip). Each core has its own L1/L2 caches.

```diagram
┌───────────────────────────────────────────────────────────┐
│                    Multi-Core CPU Die                     │
│                                                           │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌────────┐│
│  │  Core 0   │  │  Core 1   │  │  Core 2   │  │ Core 3 ││
│  │ ┌───┐┌───┐│  │ ┌───┐┌───┐│  │ ┌───┐┌───┐│  │┌───┐┌──┐│
│  │ │L1I││L1D││  │ │L1I││L1D││  │ │L1I││L1D││  ││L1I││L1││
│  │ └───┘└───┘│  │ └───┘└───┘│  │ └───┘└───┘│  │└───┘└──┘│
│  │ ┌────────┐│  │ ┌────────┐│  │ ┌────────┐│  │┌───────┐│
│  │ │   L2   ││  │ │   L2   ││  │ │   L2   ││  ││  L2   ││
│  │ └────────┘│  │ └────────┘│  │ └────────┘│  │└───────┘│
│  └─────┬─────┘  └─────┬─────┘  └─────┬─────┘  └───┬────┘│
│        │              │              │             │      │
│  ┌─────┴──────────────┴──────────────┴─────────────┴───┐ │
│  │               Shared L3 Cache (8-96 MB)             │ │
│  └──────────────────────────┬──────────────────────────┘ │
│                             │                            │
│  ┌──────────────────────────┴──────────────────────────┐ │
│  │              Memory Controller                      │ │
│  └──────────────────────────┬──────────────────────────┘ │
└─────────────────────────────┼────────────────────────────┘
                              │
                     ┌────────┴────────┐
                     │   DRAM (DDR5)   │
                     └─────────────────┘
```

---

## Multi-Core: Key Characteristics

| Feature | Description |
|---------|-------------|
| Core count | 4-128+ cores per chip (consumer to server) |
| Private caches | Each core has own L1 and L2 |
| Shared cache | L3 shared by all cores |
| Memory controller | Integrated on-die, shared by all cores |
| Interconnect | Ring bus, mesh, or crossbar between cores |
| Coherence | Hardware maintains cache consistency (MESI/MOESI) |

**Examples of modern core counts:**

| Processor | Cores | Threads | Market |
|-----------|-------|---------|--------|
| Intel Core i9-14900K | 24 (8P+16E) | 32 | Desktop |
| AMD Ryzen 9 7950X | 16 | 32 | Desktop |
| AMD EPYC 9654 | 96 | 192 | Server |
| Ampere Altra Max | 128 | 128 | Cloud Server |
| Apple M3 Ultra | 32 (P+E) | 32 | Workstation |

---

## Hyper-Threading and SMT

**Simultaneous Multi-Threading (SMT)** allows a single physical core to
execute multiple threads concurrently by sharing execution resources.

Intel's implementation is called **Hyper-Threading Technology (HTT)**.

```bash
Without SMT (single-threaded core):

    Execution Units:  ALU1  ALU2  FPU1  FPU2  AGU
    Thread A cycle 1:  X     .     X     .     .    (gaps = idle units)
    Thread A cycle 2:  .     X     .     .     X
    Thread A cycle 3:  X     .     .     X     .
    Utilization: ~40%

With SMT (two hardware threads per core):

    Execution Units:  ALU1  ALU2  FPU1  FPU2  AGU
    Thread A cycle 1:  X     .     X     .     .
    Thread B cycle 1:  .     X     .     X     X
    Combined:          X     X     X     X     X    (much less idle)
    Utilization: ~65-80%
```

SMT does NOT double performance. Typical improvement: 15-30% because
both threads compete for the same execution units, caches, and bandwidth.

---

## SMT: Architecture Details

```diagram
┌────────────────────────────────────────────────────┐
│              Physical Core with SMT                │
│                                                    │
│  ┌─────────────────┐  ┌─────────────────┐          │
│  │ Thread 0 State  │  │ Thread 1 State  │          │
│  │ ┌─────────────┐ │  │ ┌─────────────┐ │          │
│  │ │ Registers   │ │  │ │ Registers   │ │ Separate │
│  │ │ (RAX..R15)  │ │  │ │ (RAX..R15)  │ │          │
│  │ └─────────────┘ │  │ └─────────────┘ │          │
│  │ ┌─────────────┐ │  │ ┌─────────────┐ │          │
│  │ │ Instr Ptr   │ │  │ │ Instr Ptr   │ │ Separate │
│  │ └─────────────┘ │  │ └─────────────┘ │          │
│  └─────────────────┘  └─────────────────┘          │
│                                                    │
│  ┌──────────────────────────────────────────┐      │
│  │         Shared Execution Engine           │      │
│  │  ┌─────┐┌─────┐┌─────┐┌─────┐┌─────┐    │      │
│  │  │ALU 1││ALU 2││ALU 3││FPU 1││FPU 2│    │ Shared│
│  │  └─────┘└─────┘└─────┘└─────┘└─────┘    │      │
│  └──────────────────────────────────────────┘      │
│                                                    │
│  ┌──────────────────────────────────────────┐      │
│  │      Shared L1 I-Cache and L1 D-Cache     │ Shared│
│  └──────────────────────────────────────────┘      │
│  ┌──────────────────────────────────────────┐      │
│  │            Shared L2 Cache                │ Shared│
│  └──────────────────────────────────────────┘      │
└────────────────────────────────────────────────────┘
```

**Duplicated per thread**: register file, instruction pointer, TLB entries
**Shared between threads**: ALU, FPU, caches, branch predictor, scheduler

---

## SMT: When It Helps and When It Hurts

| Workload | SMT Benefit | Why |
|----------|------------|-----|
| Web server | High (+25-30%) | Many threads stall on I/O, other thread runs |
| Database queries | High (+20-25%) | Memory latency hiding |
| Video encoding | Medium (+10-15%) | Compute-heavy, some parallelism |
| Scientific HPC | Low or negative | Threads fight over cache and FPU |
| Real-time / latency | Negative | Unpredictable interference |
| Crypto / security | Disabled | Side-channel attack surface |

**Checking SMT status on Linux:**

```bash
# See logical vs physical CPUs
lscpu | grep -E "^CPU\(s\)|Thread|Core|Socket"

# Output example:
# CPU(s):              16
# Thread(s) per core:  2    <-- SMT is enabled (2 threads per core)
# Core(s) per socket:  8
# Socket(s):           1

# Disable SMT at runtime (as root):
echo off > /sys/devices/system/cpu/smt/control
```

---

## UMA: Uniform Memory Access

In UMA systems, all processors share a single memory with equal
access latency. Traditional symmetric multiprocessing (SMP).

```python
┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│  Core 0  │  │  Core 1  │  │  Core 2  │  │  Core 3  │
└────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘
     │             │             │             │
┌────┴─────────────┴─────────────┴─────────────┴────┐
│                 Shared Bus / Crossbar              │
└────────────────────────┬──────────────────────────┘
                         │
              ┌──────────┴──────────┐
              │    Shared Memory    │
              │    (Equal latency   │
              │     from all cores) │
              └─────────────────────┘

Access latency: ~100 ns from any core (uniform)
```

**Advantages**: simple programming model, no data placement concerns
**Disadvantages**: bus becomes bottleneck, does not scale beyond ~8 cores

---

## NUMA: Non-Uniform Memory Access

In NUMA systems, each processor has local memory that is faster to
access. Accessing another processor's memory is slower.

```diagram
┌─────────────────────────┐     ┌─────────────────────────┐
│       NUMA Node 0       │     │       NUMA Node 1       │
│                         │     │                         │
│  ┌──────┐  ┌──────┐    │     │    ┌──────┐  ┌──────┐  │
│  │Core 0│  │Core 1│    │     │    │Core 4│  │Core 5│  │
│  └──┬───┘  └──┬───┘    │     │    └──┬───┘  └──┬───┘  │
│  ┌──┴───┐  ┌──┴───┐    │     │    ┌──┴───┐  ┌──┴───┐  │
│  │Core 2│  │Core 3│    │     │    │Core 6│  │Core 7│  │
│  └──┬───┘  └──┬───┘    │     │    └──┬───┘  └──┬───┘  │
│     └────┬─────┘        │     │        └──┬─────┘      │
│    ┌─────┴─────┐        │     │    ┌──────┴────┐       │
│    │ Local Mem │        │     │    │ Local Mem  │       │
│    │  (fast)   │        │     │    │  (fast)    │       │
│    │  ~80 ns   │        │     │    │  ~80 ns    │       │
│    └───────────┘        │     │    └────────────┘       │
│              │          │     │          │              │
└──────────────┼──────────┘     └──────────┼──────────────┘
               │                           │
               └──────────┬────────────────┘
                    ┌─────┴──────┐
                    │ Inter-node │
                    │ Interconnect│
                    │ (~150 ns)  │
                    └────────────┘
```

---

## NUMA vs UMA: Comparison

| Aspect | UMA | NUMA |
|--------|-----|------|
| Memory latency | Same from all cores | Depends on which node |
| Local access | ~100 ns | ~80 ns |
| Remote access | ~100 ns | ~130-200 ns |
| Scalability | Poor (8-16 cores) | Good (100+ cores) |
| Programming | Simpler | Must consider data placement |
| Used in | Laptops, desktops | Servers, workstations |
| Examples | Single-socket systems | Dual/quad-socket AMD EPYC |

**Checking NUMA topology on Linux:**

```bash
# Show NUMA nodes and their CPUs
numactl --hardware

# Output example:
# available: 2 nodes (0-1)
# node 0 cpus: 0 1 2 3 4 5 6 7
# node 0 size: 32768 MB
# node 1 cpus: 8 9 10 11 12 13 14 15
# node 1 size: 32768 MB
# node distances:
# node   0   1
#   0:  10  21
#   1:  21  10

# Run a program on a specific NUMA node
numactl --cpunodebind=0 --membind=0 ./my_program
```

---

## NUMA Performance Impact

Remote memory access can severely impact performance. A program that
accesses memory on the wrong NUMA node can be 30-50% slower.

```bash
    Benchmark: Memory bandwidth (GB/s)

    Local access    ████████████████████████████████████  45 GB/s
    Remote access   ████████████████████████              30 GB/s

    Benchmark: Latency (ns)

    Local access    ████████  80 ns
    Remote access   ████████████████  150 ns
```

**NUMA-aware programming tips:**
- Allocate memory on the same node where threads will access it
- Use `numactl --localalloc` to force local allocation
- Use `libnuma` for fine-grained control in C/C++
- Linux default: "first touch" policy (memory allocated on the node
  where it is first accessed)

```c
// Force memory allocation on a specific NUMA node
#include <numa.h>
void *buf = numa_alloc_onnode(size, node_id);
```

---

## GPU Architecture Overview

GPUs are massively parallel processors designed for throughput, not
single-thread latency. They contain thousands of simple cores.

```diagram
┌─────────────────────────────────────────────────────────────┐
│                         GPU Die                             │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐      ┌──────────────┐  │
│  │     SM 0     │  │     SM 1     │ ...  │    SM N      │  │
│  │ ┌──┐┌──┐┌──┐│  │ ┌──┐┌──┐┌──┐│      │ ┌──┐┌──┐┌──┐│  │
│  │ │CU││CU││CU││  │ │CU││CU││CU││      │ │CU││CU││CU││  │
│  │ └──┘└──┘└──┘│  │ └──┘└──┘└──┘│      │ └──┘└──┘└──┘│  │
│  │ ┌──┐┌──┐┌──┐│  │ ┌──┐┌──┐┌──┐│      │ ┌──┐┌──┐┌──┐│  │
│  │ │CU││CU││CU││  │ │CU││CU││CU││      │ │CU││CU││CU││  │
│  │ └──┘└──┘└──┘│  │ └──┘└──┘└──┘│      │ └──┘└──┘└──┘│  │
│  │ Shared Mem  │  │ Shared Mem  │      │ Shared Mem  │  │
│  │ L1 Cache    │  │ L1 Cache    │      │ L1 Cache    │  │
│  └──────┬───────┘  └──────┬───────┘      └──────┬───────┘  │
│         │                │                     │          │
│  ┌──────┴────────────────┴─────────────────────┴────────┐ │
│  │                    L2 Cache                           │ │
│  └──────────────────────────┬───────────────────────────┘ │
│                             │                             │
│  ┌──────────────────────────┴───────────────────────────┐ │
│  │            Memory Controllers (HBM/GDDR6)            │ │
│  └──────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘

SM = Streaming Multiprocessor     CU = CUDA Core (compute unit)
```

---

## Streaming Multiprocessors (SMs)

Each SM is a self-contained processing block. A modern GPU has
dozens to over a hundred SMs.

```diagram
┌────────────────────────────────────────────────────┐
│              Streaming Multiprocessor               │
│                                                    │
│  ┌──────────────────────────────────────────────┐  │
│  │         Warp Schedulers (x4)                 │  │
│  │  ┌─────────┐┌─────────┐┌─────────┐┌────────┐│  │
│  │  │ Sched 0 ││ Sched 1 ││ Sched 2 ││Sched 3 ││  │
│  │  └─────────┘└─────────┘└─────────┘└────────┘│  │
│  └──────────────────────────────────────────────┘  │
│                                                    │
│  ┌──────────────────────────────────────────────┐  │
│  │       INT32 Units     FP32 Units    FP64     │  │
│  │       (64 units)      (64 units)   (32 u.)  │  │
│  └──────────────────────────────────────────────┘  │
│                                                    │
│  ┌──────────────────────────────────────────────┐  │
│  │  Tensor Cores (for AI matrix operations)     │  │
│  │  (4 tensor cores per SM in modern GPUs)      │  │
│  └──────────────────────────────────────────────┘  │
│                                                    │
│  ┌───────────┐  ┌──────────────────────────┐       │
│  │ Register  │  │ Shared Memory / L1 Cache │       │
│  │   File    │  │    (configurable split)  │       │
│  │  (64 KB)  │  │       (128 KB)           │       │
│  └───────────┘  └──────────────────────────┘       │
└────────────────────────────────────────────────────┘
```

Each SM can manage hundreds of threads simultaneously.

---

## Warp Scheduling

A **warp** is a group of 32 threads that execute in lockstep on an SM.
All threads in a warp execute the same instruction at the same time
(SIMT: Single Instruction, Multiple Threads).

```diagram
    Warp 0:  [T0  T1  T2  T3  ... T31]  ── executing ADD
    Warp 1:  [T32 T33 T34 T35 ... T63]  ── waiting for memory
    Warp 2:  [T64 T65 T66 T67 ... T95]  ── executing MUL
    Warp 3:  [T96 T97 T98 T99 ... T127] ── ready to execute

    Warp Scheduler each cycle:
    ┌─────────────────────────────────┐
    │ Pick a warp that is READY       │
    │ Issue its next instruction      │
    │ If warp stalls (memory wait),   │
    │ switch to another warp (free!)  │
    └─────────────────────────────────┘
```

**Key insight**: GPUs hide memory latency by switching between warps,
not by using caches. When one warp waits for memory, another runs
instantly (zero-cost context switch since all register state is on-chip).

**Warp divergence**: if threads in a warp take different branches,
both paths must execute serially. This wastes throughput.

---

## CPU vs GPU: Architecture Comparison

```diagram
CPU: Few powerful cores               GPU: Many simple cores
┌────────────────────────┐             ┌──────────────────────────┐
│  ┌──────┐  ┌──────┐   │             │ ┌─┐┌─┐┌─┐┌─┐┌─┐┌─┐┌─┐  │
│  │      │  │      │   │             │ └─┘└─┘└─┘└─┘└─┘└─┘└─┘  │
│  │ Core │  │ Core │   │             │ ┌─┐┌─┐┌─┐┌─┐┌─┐┌─┐┌─┐  │
│  │  0   │  │  1   │   │             │ └─┘└─┘└─┘└─┘└─┘└─┘└─┘  │
│  │      │  │      │   │             │ ┌─┐┌─┐┌─┐┌─┐┌─┐┌─┐┌─┐  │
│  └──────┘  └──────┘   │             │ └─┘└─┘└─┘└─┘└─┘└─┘└─┘  │
│  ┌──────┐  ┌──────┐   │             │ ┌─┐┌─┐┌─┐┌─┐┌─┐┌─┐┌─┐  │
│  │      │  │      │   │             │ └─┘└─┘└─┘└─┘└─┘└─┘└─┘  │
│  │ Core │  │ Core │   │             │ ┌─┐┌─┐┌─┐┌─┐┌─┐┌─┐┌─┐  │
│  │  2   │  │  3   │   │             │ └─┘└─┘└─┘└─┘└─┘└─┘└─┘  │
│  │      │  │      │   │             │ ┌─┐┌─┐┌─┐┌─┐┌─┐┌─┐┌─┐  │
│  └──────┘  └──────┘   │             │ └─┘└─┘└─┘└─┘└─┘└─┘└─┘  │
│                        │             │                          │
│  ████████████████████  │             │ ███                      │
│       Big Caches       │             │ Small Caches             │
│  ████████████████████  │             │                          │
└────────────────────────┘             └──────────────────────────┘
  4 cores, OoO, branch pred,            Thousands of cores,
  big caches, low latency               in-order, high throughput
```

| Feature | CPU | GPU |
|---------|-----|-----|
| Cores | 4-128 complex cores | 1000-16000+ simple cores |
| Clock speed | 3-5.5 GHz | 1.5-2.5 GHz |
| Design goal | Low latency | High throughput |
| Thread switching | Expensive (OS) | Free (hardware) |
| Branch handling | Sophisticated prediction | Warp divergence penalty |
| Memory | Large caches | High bandwidth (HBM) |
| Best for | Serial, branchy code | Massively parallel data |

---

## Vector Processing

Vector processors operate on arrays of data with a single instruction.
This is the SIMD paradigm at the instruction level.

```diagram
    Scalar operation (one element at a time):

    A[0] = B[0] + C[0]         cycle 1
    A[1] = B[1] + C[1]         cycle 2
    A[2] = B[2] + C[2]         cycle 3
    A[3] = B[3] + C[3]         cycle 4
    Total: 4 cycles


    Vector operation (multiple elements at once):

    ┌──────────┬──────────┬──────────┬──────────┐
    │  B[0]    │  B[1]    │  B[2]    │  B[3]    │   Vector Register 1
    └──────────┴──────────┴──────────┴──────────┘
         +          +          +          +
    ┌──────────┬──────────┬──────────┬──────────┐
    │  C[0]    │  C[1]    │  C[2]    │  C[3]    │   Vector Register 2
    └──────────┴──────────┴──────────┴──────────┘
         =          =          =          =
    ┌──────────┬──────────┬──────────┬──────────┐
    │  A[0]    │  A[1]    │  A[2]    │  A[3]    │   Vector Register 3
    └──────────┴──────────┴──────────┴──────────┘
    Total: 1 cycle (4x speedup!)
```

---

## SIMD Instructions: SSE, AVX, AVX-512

x86 CPUs include progressively wider SIMD instruction sets:

| ISA Extension | Register Width | Floats per Op | Year |
|---------------|---------------|---------------|------|
| MMX | 64-bit | 2 (int only) | 1997 |
| SSE | 128-bit (XMM) | 4 float | 1999 |
| SSE2 | 128-bit (XMM) | 2 double | 2001 |
| AVX | 256-bit (YMM) | 8 float | 2011 |
| AVX2 | 256-bit (YMM) | 8 float + int | 2013 |
| AVX-512 | 512-bit (ZMM) | 16 float | 2017 |

```diagram
Register sizes:

XMM0 (SSE):   128 bits  ┌───────────────────┐
                          │ 4 x 32-bit float  │
                          └───────────────────┘

YMM0 (AVX):   256 bits  ┌───────────────────────────────────────┐
                          │ 8 x 32-bit float                      │
                          └───────────────────────────────────────┘

ZMM0 (AVX-512):512 bits ┌───────────────────────────────────────────────────────────┐
                          │ 16 x 32-bit float                                        │
                          └───────────────────────────────────────────────────────────┘
```

---

## SIMD: Code Examples

**Using SSE/AVX intrinsics in C:**

```c
#include <immintrin.h>

// SSE: add 4 floats at once (128-bit)
void add_sse(float *a, float *b, float *c, int n) {
    for (int i = 0; i < n; i += 4) {
        __m128 va = _mm_load_ps(&a[i]);
        __m128 vb = _mm_load_ps(&b[i]);
        __m128 vc = _mm_add_ps(va, vb);
        _mm_store_ps(&c[i], vc);
    }
}

// AVX: add 8 floats at once (256-bit)
void add_avx(float *a, float *b, float *c, int n) {
    for (int i = 0; i < n; i += 8) {
        __m256 va = _mm256_load_ps(&a[i]);
        __m256 vb = _mm256_load_ps(&b[i]);
        __m256 vc = _mm256_add_ps(va, vb);
        _mm256_store_ps(&c[i], vc);
    }
}
```

**Compiler auto-vectorization (no intrinsics):**

```c
// Compile with: gcc -O2 -march=native -ftree-vectorize
void add_auto(float *restrict a, float *restrict b, float *restrict c, int n) {
    for (int i = 0; i < n; i++)
        c[i] = a[i] + b[i];  // compiler generates SIMD automatically
}
```

---

## SIMD: Checking CPU Support

```bash
# Check which SIMD extensions your CPU supports
grep -o 'sse\S*\|avx\S*\|neon' /proc/cpuinfo | sort -u

# Typical output on a modern Intel CPU:
# avx
# avx2
# avx_vnni
# sse
# sse2
# sse3
# sse4_1
# sse4_2
# ssse3

# Check if AVX-512 is available
grep avx512 /proc/cpuinfo | head -1

# See compiler auto-vectorization report
gcc -O2 -march=native -ftree-vectorize -fopt-info-vec-optimized -c code.c
```

**ARM SIMD (NEON):**

```c
#include <arm_neon.h>

void add_neon(float *a, float *b, float *c, int n) {
    for (int i = 0; i < n; i += 4) {
        float32x4_t va = vld1q_f32(&a[i]);
        float32x4_t vb = vld1q_f32(&b[i]);
        float32x4_t vc = vaddq_f32(va, vb);
        vst1q_f32(&c[i], vc);
    }
}
```

---

## Interconnects Between Cores

Cores must communicate to maintain cache coherence and share data.
The interconnect topology determines communication speed.

**Bus (legacy):**

```diagram
┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐
│Core 0│  │Core 1│  │Core 2│  │Core 3│
└──┬───┘  └──┬───┘  └──┬───┘  └──┬───┘
   │         │         │         │
═══╧═════════╧═════════╧═════════╧═══  Shared Bus
```

Simple but becomes a bottleneck with more cores.

**Ring bus (used in Intel up to ~10 cores):**

```diagram
┌──────┐───┌──────┐───┌──────┐───┌──────┐
│Core 0│   │Core 1│   │Core 2│   │Core 3│
└──────┘───└──────┘───└──────┘───└──────┘
    │                                │
    └────────────────────────────────┘
```

Each core connects to two neighbors. Messages travel around the ring.
Latency increases with core count (must traverse more hops).

---

## Interconnects: Mesh and Crossbar

**Mesh (used in Intel Xeon, AMD EPYC):**

```diagram
┌──────┐────┌──────┐────┌──────┐────┌──────┐
│Core 0│    │Core 1│    │Core 2│    │Core 3│
└──┬───┘────└──┬───┘────└──┬───┘────└──┬───┘
   │           │           │           │
┌──┴───┐────┌──┴───┐────┌──┴───┐────┌──┴───┐
│Core 4│    │Core 5│    │Core 6│    │Core 7│
└──┬───┘────└──┬───┘────└──┬───┘────└──┬───┘
   │           │           │           │
┌──┴───┐────┌──┴───┐────┌──┴───┐────┌──┴───┐
│Core 8│    │Core 9│    │Core10│    │Core11│
└──────┘────└──────┘────└──────┘────└──────┘
```

Each core connects to 4 neighbors (N/S/E/W). Scales much better than
a ring. Maximum hops = rows + columns - 2.

**Crossbar:**

```diagram
         Core0  Core1  Core2  Core3
          │      │      │      │
Mem0 ─────┼──────┼──────┼──────┤
Mem1 ─────┼──────┼──────┼──────┤
Mem2 ─────┼──────┼──────┼──────┤
Mem3 ─────┼──────┼──────┼──────┤
```

Any-to-any connection. Low latency but expensive (O(N^2) switches).

---

## Interconnect Comparison

| Topology | Latency | Bandwidth | Scalability | Cost | Used In |
|----------|---------|-----------|-------------|------|---------|
| Bus | Low (few cores) | Low (shared) | Poor | Low | Legacy SMP |
| Ring | Medium | Medium | Fair (10-14 cores) | Medium | Intel client |
| Mesh | Low-Medium | High | Excellent | High | Intel Xeon, AMD EPYC |
| Crossbar | Lowest | Highest | Poor (N^2 cost) | Very High | Small systems |

**AMD Infinity Fabric:**

```diagram
┌──────────────────┐        ┌──────────────────┐
│   CCD 0          │        │   CCD 1          │
│  (8 cores + L3)  │        │  (8 cores + L3)  │
└────────┬─────────┘        └────────┬─────────┘
         │                           │
    ┌────┴───────────────────────────┴────┐
    │        Infinity Fabric (IF)         │
    │   (scalable on-die interconnect)    │
    └────┬───────────┬───────────────┬────┘
         │           │               │
    ┌────┴────┐ ┌────┴─────┐ ┌──────┴──────┐
    │ Memory  │ │   I/O    │ │ Inter-socket│
    │ Ctrl    │ │   Hub    │ │   Link      │
    └─────────┘ └──────────┘ └─────────────┘
```

---

## Cache Coherence in Multiprocessors

When multiple cores cache the same memory location, coherence protocols
ensure all cores see a consistent view of memory.

**The problem illustrated:**

```python
Time   Core 0 Cache    Core 1 Cache    Memory    Correct?
─────────────────────────────────────────────────────────
  T0   X = 42          X = 42          X = 42    Yes
  T1   X = 99 (write)  X = 42          X = 42    NO!
       Core 1 sees stale data!

With coherence protocol:
  T0   X = 42 (S)      X = 42 (S)      X = 42    Yes
  T1   Core 0 sends INVALIDATE to Core 1
       X = 99 (M)      X = INVALID     X = 42    Yes
  T2   Core 1 reads X -> miss -> gets 99 from Core 0
       X = 99 (S)      X = 99 (S)      X = 99    Yes
```

Hardware handles this automatically and transparently.
Software does not need to manage cache coherence (but should
avoid patterns that stress it, like false sharing).

---

## MESI Protocol: Detailed State Transitions

```bash
                    ┌───────────────────────────────────┐
                    │           MESI States              │
                    └───────────────────────────────────┘

        Read miss                       Read miss
       (no other cache has it)         (other cache has it)
   ┌────────────────────┐         ┌────────────────────┐
   │                    v         │                    v
┌──┴──┐   Write     ┌─────┐  Snoop   ┌─────┐      ┌─────┐
│     │   hit       │     │  read    │     │      │     │
│  I  │────────────>│  E  │─────────>│  S  │      │  M  │
│     │             │     │          │     │      │     │
└──┬──┘             └──┬──┘          └──┬──┘      └──┬──┘
   │                   │                │             │
   │                   │ Write hit      │ Write       │ Snoop read
   │                   └──────────┐     │ (invalidate │ (flush + share)
   │                              v     │  others)    │
   │                           ┌─────┐  │             │
   │                           │     │<─┘             │
   │    Write miss             │  M  │<───────────────┘
   │   (invalidate others)     │     │     Snoop write
   └──────────────────────────>└──┬──┘     (flush + invalidate)
                                  │                │
                                  └───────>  I  <──┘
```

| Transition | Trigger | Action |
|-----------|---------|--------|
| I -> E | Read miss, no sharers | Load from memory |
| I -> S | Read miss, other has it | Get copy from other cache |
| I -> M | Write miss | Load, invalidate others |
| E -> M | Local write | Silent transition (no bus traffic) |
| E -> S | Snoop read from other core | Allow sharing |
| S -> M | Local write | Invalidate all other copies |
| S -> I | Snoop invalidate | Drop line |
| M -> S | Snoop read | Flush dirty data, share |
| M -> I | Snoop write (RWITM) | Flush dirty data, invalidate |

---

## False Sharing

False sharing occurs when two cores modify different variables that
happen to reside on the same cache line. The coherence protocol
bounces the line back and forth even though there is no true sharing.

```diagram
Cache line (64 bytes):
┌──────────────────────────────────────────────────────────────┐
│  counter_core0  │  padding...  │  counter_core1  │  padding │
│  (8 bytes)      │              │  (8 bytes)       │          │
└──────────────────────────────────────────────────────────────┘
     Core 0 writes here              Core 1 writes here

Both in the SAME cache line! Every write by one core
invalidates the line in the other core's cache.
```

**Bad code (false sharing):**

```c
struct counters {
    long count0;  // used by thread 0
    long count1;  // used by thread 1 -- same cache line!
};
```

**Fixed code (padding to separate cache lines):**

```c
struct counters {
    long count0;
    char padding[64 - sizeof(long)];  // force onto different cache line
    long count1;
};
// Or use C11: _Alignas(64) long count0;
```

False sharing can cause 10-100x slowdown on tight loops.

---

## MOESI and MESIF Extensions

Some architectures extend MESI with additional states for better
performance:

**MOESI (AMD):**

| State | Meaning |
|-------|---------|
| M | Modified -- dirty, exclusive |
| O | **Owned** -- dirty, but shared with others |
| E | Exclusive -- clean, only copy |
| S | Shared -- clean, may have copies elsewhere |
| I | Invalid |

The **Owned** state allows a dirty line to be shared without writing
back to memory first. The owner supplies the data directly to other
cores on a snoop, reducing memory traffic.

**MESIF (Intel):**

| State | Meaning |
|-------|---------|
| F | **Forward** -- clean, shared, designated responder |

The **Forward** state selects one cache to respond to snoop requests,
avoiding multiple caches all trying to respond simultaneously.

---

## Amdahl's Law

Amdahl's Law gives the theoretical maximum speedup of a program when
parallelizing only a fraction of it.

```misc
                    1
Speedup = ─────────────────────
           (1 - P) + P / N

Where:
  P = fraction of the program that can be parallelized
  N = number of processors
```

**Example**: If 90% of a program is parallelizable (P = 0.9):

| Processors (N) | Speedup |
|-----------------|---------|
| 1 | 1.0x |
| 2 | 1.82x |
| 4 | 3.08x |
| 8 | 4.71x |
| 16 | 6.40x |
| 64 | 8.77x |
| 256 | 9.69x |
| Infinity | 10.0x |

Even with infinite processors, the maximum speedup is 1/(1-P) = 10x.
The 10% serial portion is the bottleneck.

---

## Amdahl's Law: Visualization

```diagram
    Speedup
    20 │
       │
    18 │                                            P = 0.99
    16 │                                        ╱───────────
       │                                   ╱────┘
    14 │                              ╱────┘
       │                         ╱────┘
    12 │                    ╱────┘
       │               ╱────┘           P = 0.95
    10 │          ╱────┘            ╱────────────────────
       │     ╱────┘           ╱────┘
     8 │╱────┘           ╱────┘
       │            ╱────┘          P = 0.90
     6 │       ╱────┘          ╱────────────────────────
       │  ╱────┘          ╱────┘
     4 │──┘          ╱────┘
       │        ╱────┘          P = 0.75
     2 │   ╱────┘      ╱───────────────────────────────
       │───┘      ╱────┘
     0 └──────────────────────────────────────────────
       1    4    8   16   32   64  128  256  512  1024
                    Number of Processors

    Key insight: even 5% serial code limits speedup to 20x
    no matter how many processors you add.
```

---

## Gustafson's Law

Gustafson's Law offers a more optimistic view. Instead of fixing the
problem size, it says: with more processors, we solve BIGGER problems.

```misc
Speedup = N - (1 - P) * (N - 1)

Simplified:
Speedup = N * P + (1 - P)

Where:
  N = number of processors
  P = parallel fraction (measured on the parallel system)
```

**Key difference from Amdahl:**

```misc
Amdahl:     Fixed problem size, add processors
            "How fast can we solve THIS problem?"
            Speedup is bounded by serial fraction

Gustafson:  Fixed time, scale problem with processors
            "How much MORE can we solve in the SAME time?"
            Speedup scales linearly with processors
```

**Example** (P = 0.9, serial fraction = 10%):

| Processors | Amdahl Speedup | Gustafson Speedup |
|-----------|----------------|-------------------|
| 4 | 3.08x | 3.70x |
| 16 | 6.40x | 14.50x |
| 64 | 8.77x | 57.70x |
| 256 | 9.69x | 230.50x |
| 1024 | 9.91x | 921.70x |

---

## Gustafson vs Amdahl: When Each Applies

```sql
┌─────────────────────────────────────────────────────────┐
│                                                         │
│  Amdahl's Law (pessimistic, but realistic for fixed     │
│  problem sizes):                                        │
│                                                         │
│  "I need to sort 1 million records. Adding more cores   │
│   won't help much beyond a point because merging the    │
│   final results is serial."                             │
│                                                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Gustafson's Law (optimistic, realistic for scalable    │
│  problems):                                             │
│                                                         │
│  "I have a weather simulation. With 1000 cores, I can   │
│   simulate a much finer grid in the same wall-clock     │
│   time. The serial fraction stays small."               │
│                                                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Real world: the truth is somewhere in between.         │
│  Communication overhead, synchronization costs, and     │
│  memory bandwidth limits also constrain scaling.        │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## Practical Parallelism: Putting It All Together

| Parallelism Level | Mechanism | Programmer Visible? |
|-------------------|-----------|-------------------|
| Bit-level | Wider data paths (8->16->32->64 bit) | No |
| Instruction-level | Pipelining, superscalar, OoO | No (hardware) |
| Data-level (SIMD) | SSE, AVX, NEON | Yes (intrinsics or auto) |
| Thread-level (SMT) | Hyper-threading | Yes (OS sees more CPUs) |
| Core-level | Multi-core | Yes (threads/processes) |
| Socket-level | Multi-socket NUMA | Yes (NUMA awareness) |
| Node-level | Clusters, MPI | Yes (distributed computing) |

**The parallelism stack on a modern server:**

```diagram
┌────────────────────────────────────────────────────┐
│  Cluster: 1000 nodes, MPI communication            │
│  ┌──────────────────────────────────────────────┐  │
│  │  Node: 2 sockets, NUMA-aware allocation      │  │
│  │  ┌────────────────────────────────────────┐  │  │
│  │  │  Socket: 64 cores, shared L3            │  │  │
│  │  │  ┌──────────────────────────────────┐  │  │  │
│  │  │  │  Core: 2 SMT threads, OoO + SIMD │  │  │  │
│  │  │  │  ┌────────────────────────────┐  │  │  │  │
│  │  │  │  │  AVX-512: 16 floats/cycle  │  │  │  │  │
│  │  │  │  └────────────────────────────┘  │  │  │  │
│  │  │  └──────────────────────────────────┘  │  │  │
│  │  └────────────────────────────────────────┘  │  │
│  └──────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────┘
```

---

## Summary: Parallel Architectures

```diagram
┌─────────────────────────────────────────────────────────┐
│           Parallel Architectures: Key Takeaways         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Classification:                                        │
│  - Flynn's Taxonomy: SISD, SIMD, MISD, MIMD            │
│  - Modern CPUs combine SIMD + MIMD                      │
│                                                         │
│  Hardware Parallelism:                                  │
│  - Multi-core: independent cores on one die             │
│  - SMT/Hyper-threading: multiple threads per core       │
│  - SIMD (SSE/AVX): operate on vectors of data           │
│  - GPU: thousands of simple cores for throughput         │
│                                                         │
│  Memory Architecture:                                   │
│  - UMA: equal access, simple, limited scalability       │
│  - NUMA: non-uniform access, scales to 100+ cores       │
│  - Cache coherence (MESI/MOESI) keeps cores consistent  │
│  - False sharing: avoidable performance killer           │
│                                                         │
│  Scaling Laws:                                          │
│  - Amdahl: serial fraction limits speedup               │
│  - Gustafson: scale problem size with processors        │
│  - Real systems: communication overhead matters too     │
│                                                         │
└─────────────────────────────────────────────────────────┘
```
