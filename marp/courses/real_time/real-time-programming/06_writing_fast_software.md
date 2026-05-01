---
tags:
  - infrastructure:real-time
  - languages:c
  - languages:assembly
level: advanced
category: real-time
audience:
  - audiences:embedded-engineers
  - audiences:developers

---
# Writing Fast Software

---
## What This Chapter Covers

- Knowing the system APIs (memcpy, etc.)
- CPU-vendor libraries
- When to drop into assembly
- DMA for offload
- Memory mappings
- Atomics, mutexes, RW locks
- RCU and copy-on-write

---
## Know Your Standard Library

- `memcpy` is heavily optimised; do not write your own
- Same for `memset`, `memcmp`, `strcpy` (though prefer `strncpy` for safety)
- glibc on x86: AVX-512 versions, hand-tuned
- Replacing them with naive loops is a common own-goal
- Profile first; the standard library is rarely the bottleneck

---
## CPU-Vendor Libraries

- Intel MKL: linear algebra, FFTs, statistics — vectorised
- ARM Performance Libraries: similar for ARM
- AMD AOCL: AMD-tuned BLAS / FFT
- Vendor BLAS: 5-100x faster than naive code for matrix work
- Use them when applicable; reinventing is rarely worth it

---
## When to Write Assembly

- Almost never
- The compiler beats handwritten asm in 99% of cases
- Exceptions: SIMD intrinsics, special instructions, very tight loops in known contexts
- Even then: prefer compiler intrinsics over raw asm
- Profile first; you may not need to

---
## SIMD Intrinsics

```c
#include <immintrin.h>
__m256i sum = _mm256_add_epi32(a, b);
```

- Vectorised operations: 4-16 values processed in one instruction
- AVX, AVX2, AVX-512 on x86; NEON, SVE on ARM
- 4-16x speedup for parallelisable work
- Compiler may auto-vectorise; help it by writing simple loops
- Manual intrinsics for cases where the compiler doesn't get it

---
## DMA (Direct Memory Access)

- The CPU offloads data movement to a dedicated controller
- CPU does other work in parallel
- Common in: networking, disk I/O, embedded peripherals
- Modern systems use DMA implicitly via drivers
- For embedded RT: explicit DMA programming is a major optimisation

---
## Memory Mappings

- `mmap` maps a file or device directly into the process's address space
- Reads/writes are page-fault-driven (or eager)
- Useful for: large files, shared memory between processes
- `mmap` with `MAP_POPULATE` to pre-fault all pages
- Avoid `mmap` of disk files in RT hot paths — page faults hurt

---
## Huge Pages

- Default page size: 4 KB
- Huge pages: 2 MB or 1 GB
- One TLB entry covers more memory &#8594; fewer TLB misses
- Beneficial for memory-heavy workloads
- Allocate with `mmap(MAP_HUGETLB)` or via `transparent_hugepage` (THP)

---
## Atomic Variables

```c
#include <stdatomic.h>
atomic_int counter = 0;
atomic_fetch_add(&counter, 1);
```

- Lock-free updates to a single variable
- Cheap (single CPU instruction usually)
- Memory ordering matters: `memory_order_relaxed`, `memory_order_acquire`, etc.
- Building blocks for lock-free data structures
- C11, C++11 standardised

---
## Memory Ordering

- CPUs and compilers reorder operations for performance
- Atomics declare *what's allowed*: relaxed, acquire, release, seq_cst
- `seq_cst`: strongest; no reorder; expensive
- `relaxed`: cheapest; only the operation is atomic, not its ordering
- Picking the right ordering is half the skill of lock-free programming

---
## Mutexes

- The basic mutual-exclusion primitive
- Linux: futex underneath; cheap when uncontended, syscall when contended
- Worst case: arbitrary wait
- For RT: use priority inheritance mutexes (next chapter)
- Keep critical sections short

---
## Reader-Writer Locks

- Many readers OR one writer
- Useful when reads dominate
- More overhead per op than a plain mutex
- Writer can be starved by continuous readers (or vice versa)
- Carefully consider before using; benchmarks may surprise

---
## RCU (Read-Copy Update)

- Readers never block; writers create new versions
- Reads are extremely cheap (often just a pointer load)
- Writers update by copying, mutating, swapping the pointer
- Old copies freed once no readers reference them
- Used heavily in the Linux kernel
- Library: liburcu in user space

---
## Copy-on-Write (COW)

- Don't copy data until something needs to change it
- All readers share one copy
- A writer makes a private copy
- `fork()` uses COW for the address space
- Pattern: snapshot data structures, deferred mutation

---
## Lock-Free Data Structures

- Queues (Michael-Scott), stacks (Treiber), hash maps
- Use atomics + careful memory ordering
- Pros: no waiting, predictable
- Cons: hard to write correctly, hard to debug, ABA problems
- Use existing libraries (folly, concurrent-toolkit) before rolling your own

---
## Cache-Friendly Code

- Access memory sequentially
- Pack hot fields together
- Keep "structure of arrays" in mind for vectorisation
- Avoid pointer-chasing in hot loops
- Profile cache misses with `perf stat -e cache-misses`

---
## False Sharing

- Two threads writing to *different* variables that happen to share a cache line
- Each write invalidates the other's cache line
- Slowdown: 10x or more on what looks like independent work
- Fix: pad to cache line size (64 bytes typical)
- `alignas(64)` in C11/C++11

---
## Branch-Free Code

- Replace conditional branches with arithmetic when possible
- `int max = a + ((b - a) & ((b - a) >> 31));` — no branch
- Compiler does many of these for you
- Worth knowing the technique for hot inner loops
- Don't hand-optimise without profiling first

---
## Common Mistakes

- Optimising before profiling
- Re-implementing libc; getting it wrong
- Sprinkling `volatile` thinking it gives atomicity (it doesn't)
- Using full memory barriers everywhere (slow); using none anywhere (wrong)
- Believing "it's faster on my laptop" applies to the target hardware
