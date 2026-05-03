---
tags:
  - infrastructure:real-time
  - infrastructure:memory
level: advanced
category: real-time
audience:
  - audiences:embedded-engineers
  - audiences:developers

---
# Real-Time and Memory Allocations

---
## What This Chapter Covers

- Why malloc is incompatible with hard RT
- The buddy algorithm
- Allocation pools and slab allocators
- Stack allocation
- Lock-free allocators
- Memory allocation patterns for RT

---
## Why malloc Is Bad for RT

- Variable execution time
- May trigger system calls (mmap, sbrk)
- May trigger page faults
- May fragment memory over time
- Worst case: tens to hundreds of microseconds
- A single malloc can blow a tight deadline

---
## Allocation Strategies

![alloc_strategies](svg/courses/real_time/real-time-programming/07_real_time_and_memory_allocations/alloc_strategies.svg)

---
## Pool Allocator

![pool_allocator](svg/courses/real_time/real-time-programming/07_real_time_and_memory_allocations/pool_allocator.svg)

---
## What malloc Does

- Maintains free lists of memory chunks
- Searches for a chunk that fits the requested size
- May split or coalesce chunks
- May ask the OS for more memory if none fits
- The "may"s are why timing varies

---
## The Buddy Algorithm

- Memory split into power-of-two-sized blocks
- Allocation: find smallest block that fits; split if needed
- Free: merge with "buddy" block if both free
- Used by Linux kernel for page allocation
- Bounded operations, but variable cost

---
## Slab Allocators

- Pre-allocated cache of fixed-size objects
- Allocation = pop from a free list (O(1))
- Free = push to free list (O(1))
- Used by kernel for frequently-allocated kernel objects
- The right tool when you have a specific size

---
## Pool Allocation

- Pre-allocate a pool of N objects at startup
- Allocate = take from pool
- Free = return to pool
- O(1) allocation and free
- Works only when N is known in advance
- The standard pattern for RT

---
## Pool Allocation in Code

```c
#define POOL_SIZE 1024
static MyObject pool[POOL_SIZE];
static int next_free[POOL_SIZE];
static atomic_int top = 0;

MyObject* pool_alloc() {
    int idx = atomic_fetch_sub(&top, 1) - 1;
    if (idx < 0) return NULL;
    return &pool[next_free[idx]];
}
```

- A free-stack of indices
- Atomic operations for thread safety
- Bounded; predictable

---
## Stack Allocation

- Variables on the stack: zero-cost allocation
- Lifetime tied to the function scope
- For small, short-lived objects: best choice
- Caveat: stack size is limited (often 8 MB)
- VLAs (variable-length arrays in C99) work but be careful with sizes

---
## Pre-Allocation at Startup

- Allocate all needed memory before entering the RT path
- During non-RT init, malloc is fine
- During RT execution, no allocations
- Pre-touch all pages so the kernel commits them
- `mlockall(MCL_CURRENT | MCL_FUTURE)` to prevent swapping

---
## mlockall

```c
#include <sys/mman.h>
if (mlockall(MCL_CURRENT | MCL_FUTURE) != 0) {
    perror("mlockall");
}
```

- Pin the process's pages in RAM
- No swap, no page faults
- Requires elevated privileges (CAP_IPC_LOCK)
- Costs RAM; use for hard RT processes
- Pre-faults future allocations too

---
## Lock-Free Allocators

- Pool allocators that handle concurrent allocation
- Examples: tcmalloc, jemalloc (general-purpose), custom lock-free pools
- Trade memory (per-thread caches) for time
- Often part of an RT framework
- For one-thread RT: a simple pool is enough

---
## Per-Thread Pools

- Each thread has its own pool
- No contention between threads
- Cross-thread free is harder (return to original thread's pool)
- Common pattern in high-performance servers
- Folly, libumem, jemalloc all use variants of this

---
## Common Allocation Patterns

- **Object pool**: N pre-allocated, recycled in/out
- **Ring buffer**: fixed-size circular allocation
- **Bump allocator**: linear region; reset whole region at once
- **Region (arena)**: many sub-allocations, freed together
- Each fits a specific use case

---
## Fragmentation

- malloc's worst long-term enemy
- Free space exists but no contiguous chunk fits a request
- Pool allocators with fixed-size objects: zero fragmentation
- Variable-size pools: fragmentation possible
- Long-running RT systems must avoid this

---
## Memory Pressure and OOM

- If physical memory runs out, kernel may kill processes (OOM killer)
- For RT: lock memory, set process out of OOM scope
- `/proc/<pid>/oom_score_adj` to tune
- Better: design memory budget so OOM never occurs
- Cgroups (Linux) for hard limits

---
## Stack Overflow

- Recursive code or large stack frames blow past the stack size
- For RT: pre-set stack size with `pthread_attr_setstacksize`
- Stack-checking tools: `ulimit -s`, `pstack`
- For deeply recursive algorithms, convert to iterative
- A stack overflow is a guaranteed bad day

---
## Common Mistakes

- Calling malloc in the RT path
- Using STL containers that allocate (vector::push_back may allocate)
- Forgetting `mlockall` and getting page faults
- Using shared global allocator across many RT threads (contention)
- Believing "we have lots of memory" — fragmentation is a time problem, not a space one
