# Memory Systems

---

## Table of Contents

1. Memory Hierarchy Overview
1. SRAM vs DRAM
1. DRAM Organization and Timing
1. Virtual Memory
1. Page Tables and TLB
1. Memory Mapping
1. DMA and Memory-Mapped I/O
1. Memory Performance Optimization

---

## The Memory Hierarchy

Computer systems use a hierarchy of memory technologies, trading off
speed, size, and cost:

```text
                    ┌───────┐
                    │  Reg  │  ~0.3 ns, ~1 KB
                    │       │  $$$$$$$
                   ┌┴───────┴┐
                   │ L1 Cache │  ~1 ns, 32-48 KB
                   │          │  $$$$$$
                  ┌┴──────────┴┐
                  │  L2 Cache   │  ~5 ns, 256 KB - 1.25 MB
                  │             │  $$$$$
                 ┌┴─────────────┴┐
                 │   L3 Cache     │  ~15 ns, 8-96 MB
                 │                │  $$$$
                ┌┴────────────────┴┐
                │   Main Memory    │  ~80 ns, 8-512 GB
                │   (DRAM)         │  $$$
               ┌┴──────────────────┴┐
               │      SSD            │  ~100 us, 256 GB - 8 TB
               │                     │  $$
              ┌┴─────────────────────┴┐
              │       HDD              │  ~10 ms, 1-20 TB
              │                        │  $
              └────────────────────────┘
```

Each level is larger, slower, and cheaper per byte than the one above it.

---

## Why a Hierarchy?

### The key insight: locality of reference

Programs do not access memory uniformly. They exhibit:

**Temporal locality**: If you accessed address X, you will likely access X
again soon.
- Example: loop counter variables, frequently called functions

**Spatial locality**: If you accessed address X, you will likely access
addresses near X soon.
- Example: iterating through arrays, sequential instruction execution

**Quantified**: A typical program spends 90% of its time in 10% of its code.
A well-designed cache can satisfy >95% of memory requests.

| Memory Level | Typical Hit Rate |
|-------------|-----------------|
| L1 Cache | 95-97% |
| L2 Cache | 80-95% of L1 misses |
| L3 Cache | 70-90% of L2 misses |

---

## SRAM: Static Random Access Memory

SRAM stores each bit using a flip-flop circuit (6 transistors per bit).

```text
     VDD
      │
    ┌─┴─┐    ┌─┴─┐
    │ P1 │    │ P2 │     6-Transistor SRAM Cell
    └─┬─┘    └─┬─┘
      ├────────┤
    ┌─┴─┐    ┌─┴─┐
    │ N1 │    │ N2 │
    └─┬─┘    └─┬─┘
      │        │
    ┌─┴─┐    ┌─┴─┐
    │ N3 │    │ N4 │
    └─┬─┘    └─┬─┘
      │        │
     BL       BL_bar     (Bit Lines)
  ────────────────────
       Word Line
```

**Properties:**
- Fast: ~1 ns access time
- No refresh needed (static)
- Expensive: 6 transistors per bit
- Low density
- Used for: CPU caches (L1, L2, L3)

---

## DRAM: Dynamic Random Access Memory

DRAM stores each bit as charge on a tiny capacitor (1 transistor + 1 capacitor).

```text
     Bit Line
       │
     ┌─┴─┐
     │ T1 │── Word Line
     └─┬─┘
       │
     ──┴──
     ──┬──  Capacitor (stores charge = 1 bit)
       │
      GND
```

**Properties:**
- Slower: ~50-100 ns access time
- Must refresh every ~64 ms (charge leaks)
- Cheap: 1T + 1C per bit
- High density
- Used for: main memory (DDR4, DDR5)

---

## SRAM vs DRAM Comparison

| Property | SRAM | DRAM |
|----------|------|------|
| Speed | ~1 ns | ~50-100 ns |
| Density | Low (6T/bit) | High (1T+1C/bit) |
| Cost/bit | ~10x more expensive | Cheap |
| Refresh | Not needed | Every ~64 ms |
| Power (idle) | Low (no refresh) | Higher (refresh) |
| Power (active) | Higher | Lower |
| Typical size | KB to tens of MB | GB to hundreds of GB |
| Use case | CPU caches | Main memory |
| Volatility | Volatile | Volatile |
| Typical product | On-die cache | DDR5 DIMM |

---

## DRAM Organization

DRAM is organized as a 2D array of rows and columns:

```text
┌─────────────────────────────────────────┐
│              DRAM Bank                  │
│                                         │
│    Column 0  Column 1  Column 2  ...    │
│   ┌────────┬────────┬────────┬────┐     │
│ R │  bit   │  bit   │  bit   │    │     │
│ o │        │        │        │    │     │
│ w ├────────┼────────┼────────┼────┤     │
│   │  bit   │  bit   │  bit   │    │     │
│ 0 │        │        │        │    │     │
│   ├────────┼────────┼────────┼────┤     │
│ R │  bit   │  bit   │  bit   │    │     │
│ o │        │        │        │    │     │
│ w ├────────┼────────┼────────┼────┤     │
│   │  bit   │  bit   │  bit   │    │     │
│ 1 │        │        │        │    │     │
│   └────────┴────────┴────────┴────┘     │
│                                         │
│   ┌──────────────────────────────┐      │
│   │         Row Buffer           │      │
│   │  (holds one activated row)   │      │
│   └──────────────────────────────┘      │
└─────────────────────────────────────────┘
```

**Access steps:**
1. **RAS** (Row Address Strobe): activate a row, copy to row buffer (~13 ns)
2. **CAS** (Column Address Strobe): select column from row buffer (~13 ns)
3. **Data** appears on the data bus

Accessing another column in the same row (row buffer hit) is much faster
than activating a different row.

---

## DDR Memory Generations

| Feature | DDR3 | DDR4 | DDR5 |
|---------|------|------|------|
| Year | 2007 | 2014 | 2020 |
| Data Rate | 800-2133 MT/s | 1600-3200 MT/s | 3200-8800 MT/s |
| Voltage | 1.5V | 1.2V | 1.1V |
| Prefetch | 8n | 8n | 16n |
| Bank Groups | None | 4 | 4-8 |
| Channels/DIMM | 1 | 1 | 2 |
| Max DIMM size | 8 GB typical | 32 GB typical | 64 GB typical |
| ECC | Optional | Optional | On-die ECC |

**DDR = Double Data Rate**: transfers data on both rising and falling clock edges.

DDR5-4800: base clock 2400 MHz, data rate 4800 MT/s (megatransfers/sec),
effective bandwidth ~38.4 GB/s per channel.

---

## Memory Bandwidth Calculation

```text
Bandwidth = Data_Rate x Bus_Width x Channels

Example: DDR5-4800, 64-bit bus, dual channel
= 4800 MT/s x 8 bytes x 2 channels
= 76,800 MB/s ≈ 76.8 GB/s

Example: DDR4-3200, 64-bit bus, dual channel
= 3200 MT/s x 8 bytes x 2 channels
= 51,200 MB/s ≈ 51.2 GB/s
```

**But actual throughput is lower** due to:
- Row activation latency (tRAS)
- CAS latency (CL)
- Refresh cycles stealing bandwidth
- Protocol overhead

Real-world bandwidth is typically 60-80% of theoretical maximum.

---

## Virtual Memory: Concept

Virtual memory gives each process its own private address space, even though
physical RAM is shared.

```bash
  Process A                              Physical Memory
┌────────────────┐                    ┌────────────────┐
│ 0x0000_0000    │                    │ Frame 0        │
│   (code)       │───────────────────>│ (Proc A code)  │
│ 0x0040_0000    │                    ├────────────────┤
│   (heap)       │──────┐             │ Frame 1        │
│                │      │        ┌───>│ (Proc B data)  │
│ 0x7FFF_0000    │      │        │    ├────────────────┤
│   (stack)      │──┐   └───────────> │ Frame 2        │
└────────────────┘  │            │    │ (Proc A heap)  │
                    │            │    ├────────────────┤
  Process B         │            │    │ Frame 3        │
┌────────────────┐  │            │    │ (Proc A stack) │
│ 0x0000_0000    │  │            │    ├────────────────┤
│   (code)       │  └────────────────>│ Frame 4        │
│ 0x0040_0000    │               │    │                │
│   (data)       │───────────────┘    ├────────────────┤
└────────────────┘                    │ Frame 5        │
                                      │ (free)         │
Both processes use the same           └────────────────┘
virtual addresses, but they
map to different physical frames.
```

---

## Benefits of Virtual Memory

**1. Process isolation**: each process has its own address space;
one process cannot access another's memory (unless shared explicitly).

**2. Simplified programming**: every process sees a contiguous address space
starting from 0; no need to worry about where physical memory is.

**3. Memory overcommit**: processes can allocate more virtual memory than
physical RAM exists. Unused pages are not allocated until accessed.

**4. Demand paging**: pages are loaded from disk only when first accessed
(page fault), not when the program starts.

**5. Shared memory**: the same physical frame can be mapped into multiple
process address spaces (shared libraries, IPC).

**6. Memory-mapped files**: files can be accessed as if they were arrays
in memory, and the OS handles loading pages as needed.

---

## Pages and Frames

Virtual memory divides the address space into fixed-size **pages**
(typically 4 KB on x86-64):

```bash
Virtual Address (48 bits on x86-64):

 47          39 38          30 29          21 20          12 11           0
┌─────────────┬──────────────┬──────────────┬──────────────┬─────────────┐
│   PML4      │    PDPT      │     PD       │     PT       │   Offset    │
│  (9 bits)   │   (9 bits)   │   (9 bits)   │   (9 bits)   │  (12 bits)  │
└─────────────┴──────────────┴──────────────┴──────────────┴─────────────┘
   Level 4       Level 3        Level 2        Level 1       Page offset
   index         index          index          index         (4 KB page)
```

- **Page**: a 4 KB block in virtual address space
- **Frame**: a 4 KB block in physical memory
- **Page table**: maps virtual pages to physical frames
- **Offset**: position within a page (12 bits = 4096 bytes)

x86-64 also supports **huge pages**: 2 MB (21-bit offset) and 1 GB
(30-bit offset) for reducing TLB misses.

---

## The Page Table

The page table translates virtual addresses to physical addresses.
On x86-64, it is a 4-level radix tree:

```python
           CR3 register
               │
               v
        ┌──────────────┐
        │    PML4       │  Page Map Level 4 (512 entries)
        │   Table       │
        └──────┬───────┘
               │ PML4 index
               v
        ┌──────────────┐
        │    PDPT       │  Page Directory Pointer Table
        │   Table       │
        └──────┬───────┘
               │ PDPT index
               v
        ┌──────────────┐
        │     PD        │  Page Directory
        │   Table       │
        └──────┬───────┘
               │ PD index
               v
        ┌──────────────┐
        │     PT        │  Page Table
        │   Table       │
        └──────┬───────┘
               │ PT index
               v
        ┌──────────────┐
        │   Physical    │  + page offset from virtual address
        │   Frame       │
        └──────────────┘
```

Each table is one 4 KB page containing 512 entries of 8 bytes each.

---

## Page Table Entry (PTE) Format

Each page table entry on x86-64 contains:

```text
 63    62       52 51                                  12 11  9 8 7 6 5 4 3 2 1 0
┌──┬──┬──────────┬──────────────────────────────────────┬─────┬─┬─┬─┬─┬─┬─┬─┬─┬─┐
│NX│  │ Available │     Physical Frame Number            │ AVL │G│ │D│A│ │ │U│W│P│
└──┴──┴──────────┴──────────────────────────────────────┴─────┴─┴─┴─┴─┴─┴─┴─┴─┴─┘
```

| Bit | Name | Meaning |
|-----|------|---------|
| P (0) | Present | Page is in physical memory |
| W (1) | Writable | Page is writable (else read-only) |
| U (2) | User | Accessible from user mode (ring 3) |
| A (5) | Accessed | Page has been read |
| D (6) | Dirty | Page has been written |
| G (8) | Global | Not flushed from TLB on context switch |
| NX (63) | No Execute | Cannot execute code from this page |

If P=0, accessing the page triggers a **page fault**, and the OS must
handle it (load from disk, allocate a frame, or kill the process).

---

## The TLB (Translation Lookaside Buffer)

Walking the 4-level page table for every memory access would be extremely
slow (~4 extra memory accesses). The TLB caches recent translations.

```bash
Virtual Address ──> ┌───────┐ ──HIT──> Physical Address
                    │  TLB  │          (1-2 cycles)
                    └───┬───┘
                        │
                      MISS
                        │
                        v
                ┌───────────────┐
                │  Page Table   │     (4 memory accesses
                │   Walk        │      ~200+ cycles)
                └───────┬───────┘
                        │
                        v
                Physical Address
                (+ update TLB)
```

**Typical TLB sizes:**

| TLB Level | Entries | Page Size | Coverage |
|-----------|---------|-----------|----------|
| L1 ITLB | 64-128 | 4 KB | 256-512 KB |
| L1 DTLB | 64-96 | 4 KB | 256-384 KB |
| L2 STLB | 1536-2048 | 4 KB | 6-8 MB |
| L1 DTLB | 32 | 2 MB huge | 64 MB |

TLB miss rate is critical. Huge pages (2 MB, 1 GB) dramatically reduce
TLB misses for large working sets.

---

## TLB Shootdown

When the OS modifies page tables (e.g., unmapping a page), it must
invalidate the TLB entries on ALL CPU cores -- this is called a
**TLB shootdown**.

```text
Core 0: unmaps page X
  │
  ├──> Invalidate own TLB entry for X
  │
  ├──> Send IPI (Inter-Processor Interrupt) to Cores 1, 2, 3
  │         │              │              │
  │         v              v              v
  │    Invalidate     Invalidate     Invalidate
  │    TLB for X      TLB for X      TLB for X
  │         │              │              │
  │         └──── ACK ─────┴──── ACK ─────┘
  │                        │
  └── Wait for all ACKs ──┘
  │
  Continue execution
```

TLB shootdowns are expensive because they interrupt other cores.
Frequent mmap/munmap in multi-threaded programs can cause performance
problems due to excessive TLB shootdowns.

---

## Page Faults

When a process accesses a virtual page that is not currently in physical
memory (Present bit = 0), a **page fault** occurs:

**Minor page fault**: page is in memory but not yet mapped
- Example: first access to a newly allocated page (demand paging)
- The OS allocates a frame and updates the page table
- Cost: ~1-10 microseconds

**Major page fault**: page must be loaded from disk (swap)
- Example: page was swapped out to make room for other pages
- The OS reads the page from swap space on disk
- Cost: ~1-10 milliseconds (1000x slower!)

```bash
# Monitor page faults per process
ps -o min_flt,maj_flt,cmd -p <PID>

# Watch page faults in real time
perf stat -e page-faults,minor-faults,major-faults ./my_program
```

---

## Memory Mapping: mmap()

`mmap()` maps files or anonymous memory into a process's virtual address space:

```c
#include <sys/mman.h>

// Map a file into memory
int fd = open("data.bin", O_RDONLY);
struct stat st;
fstat(fd, &st);

void *ptr = mmap(NULL, st.st_size, PROT_READ, MAP_PRIVATE, fd, 0);
// Now ptr[0..st.st_size-1] accesses the file contents
// Pages are loaded on demand (page faults)

// Process the file as a plain array
char *data = (char *)ptr;
for (size_t i = 0; i < st.st_size; i++) {
    // Each page faults in on first access
    process_byte(data[i]);
}

munmap(ptr, st.st_size);
close(fd);
```

**Advantages over read():**
- No extra copy from kernel buffer to user buffer
- OS manages pages automatically
- Multiple processes can share the same physical pages

---

## mmap() Flags and Uses

| Flag | Meaning |
|------|---------|
| MAP_PRIVATE | Copy-on-write, changes are private |
| MAP_SHARED | Changes are visible to other processes and written to file |
| MAP_ANONYMOUS | No file backing, just allocate memory |
| MAP_FIXED | Map at exact address (dangerous) |
| MAP_HUGETLB | Use huge pages (2 MB or 1 GB) |
| MAP_POPULATE | Pre-fault all pages (avoid later page faults) |

```c
// Allocate 1 GB of anonymous memory with huge pages
void *buf = mmap(NULL, 1UL << 30,
                 PROT_READ | PROT_WRITE,
                 MAP_PRIVATE | MAP_ANONYMOUS | MAP_HUGETLB,
                 -1, 0);

// Shared memory between processes
void *shm = mmap(NULL, 4096,
                  PROT_READ | PROT_WRITE,
                  MAP_SHARED | MAP_ANONYMOUS,
                  -1, 0);
// After fork(), parent and child share this memory
```

---

## DMA: Direct Memory Access

DMA allows hardware devices to transfer data directly to/from memory
without involving the CPU for each byte.

```text
Without DMA (Programmed I/O):
┌─────┐     byte     ┌────────┐     byte     ┌────────┐
│ CPU │◄────────────►│ Device │              │ Memory │
│     │──────────────────────────────────────►│        │
└─────┘  CPU copies each byte!               └────────┘
  CPU is 100% busy during transfer

With DMA:
┌─────┐  1. Setup    ┌─────────┐              ┌────────┐
│ CPU │──────────────►│   DMA   │              │ Memory │
│     │              │ Control │◄────────────►│        │
└─────┘              └────┬────┘   bulk data   └────────┘
  │                       │
  │ CPU is free!     2. Transfer
  │ Does other work       │
  │                  3. Interrupt ──►  CPU notified: "done!"
```

**DMA flow:**
1. CPU programs the DMA controller (source, destination, size)
2. DMA controller transfers data directly between device and memory
3. DMA controller interrupts CPU when transfer is complete
4. CPU was free to do other work during the transfer

---

## Memory-Mapped I/O (MMIO)

Instead of using special I/O instructions (IN/OUT on x86), devices
can be accessed through regular memory addresses:

```bash
Physical Address Space:
┌──────────────────────┐ 0x0000_0000
│                      │
│    Main Memory       │
│    (DRAM)            │
│                      │
├──────────────────────┤ 0x????_????
│                      │
│    Memory Hole       │
│    (MMIO Region)     │
│                      │
│  ┌────────────────┐  │
│  │ GPU VRAM       │  │ GPU framebuffer mapped here
│  ├────────────────┤  │
│  │ NIC Registers  │  │ Network card registers
│  ├────────────────┤  │
│  │ USB Controller │  │ USB host controller
│  └────────────────┘  │
│                      │
├──────────────────────┤
│    Main Memory       │
│    (continued)       │
└──────────────────────┘
```

**Advantage**: no special instructions needed; regular loads and stores
access device registers. The CPU and compiler must be told not to cache
or reorder these accesses (volatile, memory barriers).

---

## Memory-Mapped I/O in Practice

```c
#include <sys/mman.h>
#include <fcntl.h>

// Access hardware registers via MMIO (Linux userspace example)
int fd = open("/dev/mem", O_RDWR | O_SYNC);

// Map the device's register space
volatile uint32_t *regs = mmap(NULL, 4096,
    PROT_READ | PROT_WRITE, MAP_SHARED,
    fd, 0xFE200000);   // GPIO base on Raspberry Pi

// Read a register
uint32_t value = regs[0];   // GPFSEL0

// Write a register
regs[7] = (1 << 16);        // GPSET0 - set GPIO 16 high

munmap((void *)regs, 4096);
close(fd);
```

**Important**: MMIO accesses must use `volatile` to prevent the compiler
from optimizing away reads/writes or reordering them.

---

## Port-Mapped I/O vs Memory-Mapped I/O

| Feature | Port-Mapped I/O (PMIO) | Memory-Mapped I/O (MMIO) |
|---------|----------------------|------------------------|
| Instructions | Special (IN/OUT on x86) | Regular (MOV/LOAD/STORE) |
| Address space | Separate I/O space | Shared with memory |
| Address bits | 16-bit (65536 ports) | Full address space |
| Protection | Ring 0 only (IOPL) | Page table based |
| Used by | Legacy x86 devices | Modern devices (PCIe) |
| Examples | COM ports, PIC, PIT | GPU, NIC, USB, NVMe |

Modern systems overwhelmingly use MMIO. PCIe devices expose their
registers and memory through MMIO regions called BARs (Base Address
Registers).

---

## NUMA: Non-Uniform Memory Access

In multi-socket systems, each CPU has its own local memory. Accessing
remote memory (attached to another CPU) is slower:

```text
┌──────────────────┐         ┌──────────────────┐
│     Socket 0     │         │     Socket 1     │
│  ┌────────────┐  │         │  ┌────────────┐  │
│  │ Core 0..15 │  │         │  │ Core 16..31│  │
│  └─────┬──────┘  │         │  └─────┬──────┘  │
│        │         │         │        │         │
│  ┌─────┴──────┐  │  QPI/   │  ┌─────┴──────┐  │
│  │ Memory     │  │  UPI    │  │ Memory     │  │
│  │ Controller │◄─┼─────────┼─►│ Controller │  │
│  └─────┬──────┘  │  link   │  └─────┬──────┘  │
│        │         │         │        │         │
│  ┌─────┴──────┐  │         │  ┌─────┴──────┐  │
│  │ Local DRAM │  │         │  │ Local DRAM │  │
│  │ 64 GB      │  │         │  │ 64 GB      │  │
│  └────────────┘  │         │  └────────────┘  │
└──────────────────┘         └──────────────────┘

Local access:  ~80 ns
Remote access: ~130 ns  (1.5-2x slower)
```

---

## NUMA in Practice

```bash
# View NUMA topology
numactl --hardware

# Example output:
# available: 2 nodes (0-1)
# node 0 cpus: 0 1 2 3 4 5 6 7
# node 0 size: 65536 MB
# node 0 free: 32000 MB
# node 1 cpus: 8 9 10 11 12 13 14 15
# node 1 size: 65536 MB
# node 1 free: 31500 MB
# node distances:
# node   0   1
#   0:  10  21
#   1:  21  10

# Run a process on NUMA node 0 only
numactl --cpunodebind=0 --membind=0 ./my_program

# View NUMA statistics
numastat
numastat -p <PID>
```

**NUMA-aware programming rule**: keep data close to the CPUs that access it.
A thread should allocate memory on the same NUMA node where it runs.

---

## Memory Performance: Row-Major vs Column-Major

Memory layout has a dramatic effect on performance due to cache lines:

```c
#define N 4096
int matrix[N][N];

// Row-major traversal (C default layout): FAST
// Accesses are sequential in memory
for (int i = 0; i < N; i++)
    for (int j = 0; j < N; j++)
        sum += matrix[i][j];    // stride = 4 bytes

// Column-major traversal: SLOW
// Each access jumps N*4 bytes = 16 KB
for (int j = 0; j < N; j++)
    for (int i = 0; i < N; i++)
        sum += matrix[i][j];    // stride = 16384 bytes
```

**Memory layout of `matrix[N][N]`:**
```text
Address:  [0][0] [0][1] [0][2] ... [0][N-1] [1][0] [1][1] ...
          ──────────────────────── ──────────────────────────
          Row 0 (contiguous)       Row 1 (contiguous)

Row-major:    accesses [0][0] [0][1] [0][2] ... ← sequential, cache-friendly
Column-major: accesses [0][0] [1][0] [2][0] ... ← strided, cache-hostile
```

Typical speedup of row-major over column-major: **5-20x** for large matrices.

---

## Measuring Memory Latency

You can measure memory access latency by creating a pointer-chase:

```c
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

// Pointer chase: each element points to the next
// This defeats prefetching and measures true latency
#define SIZE (64 * 1024 * 1024)  // 64 MB

int main() {
    void **chain = malloc(SIZE);
    int count = SIZE / sizeof(void *);

    // Create a random pointer chain
    // (simplified: sequential for L1/L2, random for DRAM measurement)
    for (int i = 0; i < count - 1; i++)
        chain[i] = &chain[i + 1];
    chain[count - 1] = &chain[0];

    // Chase pointers and measure time
    struct timespec start, end;
    void **p = chain;
    int iterations = 10000000;

    clock_gettime(CLOCK_MONOTONIC, &start);
    for (int i = 0; i < iterations; i++) {
        p = (void **)*p;  // follow pointer
    }
    clock_gettime(CLOCK_MONOTONIC, &end);

    double ns = (end.tv_sec - start.tv_sec) * 1e9
              + (end.tv_nsec - start.tv_nsec);
    printf("Average latency: %.1f ns\n", ns / iterations);
    printf("Dummy: %p\n", p);  // prevent optimization
    free(chain);
    return 0;
}
```

---

## Memory Prefetching

Modern CPUs detect sequential and strided access patterns and prefetch
data before you need it:

```bash
Without prefetching:
  Access [0] → cache miss (100 ns wait)
  Access [1] → cache miss (100 ns wait)
  Access [2] → cache miss (100 ns wait)

With hardware prefetcher:
  Access [0] → cache miss (100 ns wait)
  Prefetcher detects pattern, starts loading [1], [2], [3]...
  Access [1] → cache HIT (data already loaded)
  Access [2] → cache HIT
  Access [3] → cache HIT
```

**Software prefetch hints** (when hardware prefetcher is not enough):

```c
#include <xmmintrin.h>  // for _mm_prefetch

for (int i = 0; i < N; i++) {
    _mm_prefetch(&array[i + 64], _MM_HINT_T0);  // prefetch ahead
    sum += array[i];
}
```

`_MM_HINT_T0` = prefetch to L1, `_MM_HINT_T1` = to L2, `_MM_HINT_T2` = to L3.

---

## Summary: Memory Systems

| Concept | Key Takeaway |
|---------|-------------|
| Memory hierarchy | Speed vs size vs cost tradeoff |
| SRAM vs DRAM | 6T fast for cache, 1T+1C dense for main memory |
| DDR generations | Each generation: higher bandwidth, lower voltage |
| Virtual memory | Isolation, overcommit, demand paging |
| Page tables | 4-level radix tree on x86-64, 4 KB pages |
| TLB | Caches address translations, huge pages reduce misses |
| mmap | Map files and devices into address space |
| DMA | Devices transfer data without CPU involvement |
| MMIO | Access device registers through memory addresses |
| NUMA | Local memory is faster; keep data near its CPU |
| Locality | Sequential access patterns are critical for performance |
