---
tags:
  - infrastructure:real-time
  - infrastructure:latency
level: advanced
category: real-time
audience:
  - audiences:embedded-engineers
  - audiences:developers

---

# The Sources of Latency

---

## What This Chapter Covers

- A budget approach to latency
- Interrupt latency
- OS scheduling latency
- Context switch latency
- Software latency
- Cache and TLB effects
- How to measure each

---

## Latency Is Cumulative

- An end-to-end deadline includes hardware + OS + your code + output
- Each layer adds its share
- Worst-case latency = sum of worst-cases at each layer
- One bad layer destroys the budget for everyone else
- A "1ms deadline" must be split: 100us interrupt + 200us OS + 600us code + 100us output

---

## Latency Source Map

![latency_sources](svg/courses/real_time/real-time-programming/04_the_sources_of_latency/latency_sources.svg)

---

## Latency by Layer

![latency_layers](svg/courses/real_time/real-time-programming/04_the_sources_of_latency/latency_layers.svg)

---

## Latency Budget

![latency_budget](svg/courses/real_time/real-time-programming/04_the_sources_of_latency/latency_budget.svg)

---

## Interrupt Latency

- Time between hardware event and the start of the ISR
- Sources: interrupt controller config, current critical section, interrupt priority
- Modern CPUs: hundreds of nanoseconds at best
- Bad cases: hundreds of microseconds
- Bound it by: minimising critical sections; high interrupt priority

---

## OS Scheduling Latency

- Time between an event being ready and the OS scheduling its handler
- Stock Linux: variable, often ms-class
- PREEMPT_RT Linux: ~10-50us typical worst case
- RTOS: nanoseconds to microseconds
- Use `cyclictest` to measure your kernel's behaviour

---

## Context Switch Latency

- Time to swap one running thread for another
- Costs: register save/restore, page table swap, TLB flush, cache eviction
- Modern hardware: microseconds typical
- Pinning a thread to a CPU avoids most of this between context switches with itself
- Reduce switches by reducing the number of runnable threads

---

## Software Latency

- Your code's own contribution
- Variable depending on input, branch prediction, cache behaviour
- WCET analysis estimates worst case
- Often dwarfed by other sources for short code paths
- For long paths, the dominant factor

---

## Cache Effects

- L1 cache: ~1 ns access
- L2: ~5 ns
- L3: ~30 ns
- DRAM: ~100 ns
- A cache miss is 100x slower than a cache hit
- A cold cache after a context switch is a real cost

---

## TLB (Translation Lookaside Buffer)

- Caches virtual-to-physical address translations
- TLB miss: page table walk, dozens of ns extra
- Large memory footprints thrash the TLB
- Huge pages reduce TLB pressure
- Worth understanding for memory-heavy RT code

---

## Branch Prediction

- Modern CPUs predict branches; mispredict costs ~10-20 cycles
- Hot loops with predictable branches: nearly free
- Data-dependent branches: variable cost
- For RT: minimise unpredictable branches in hot paths
- Profile-guided optimisation can help

---

## Memory Allocation

- `malloc()` / `new` are non-deterministic
- Allocation may trigger system calls, page faults, fragmentation
- For RT: pre-allocate at startup, reuse buffers
- Pool allocators trade memory for time
- Lock-free allocators exist for hard cases

---

## Page Faults

- Accessing a virtual page not backed by physical memory
- Cost: several milliseconds (huge!)
- For RT: lock memory in RAM with `mlockall(MCL_CURRENT | MCL_FUTURE)`
- Pre-touch all memory at startup so the kernel maps it
- A single page fault can blow a 1ms budget

---

## Disk and Filesystem

- Spinning disks: 5-10ms seek time (catastrophic for RT)
- SSDs: better but variable
- For RT: avoid disk in the hot path entirely
- Logging: buffer in memory, flush periodically
- Configuration: load once at startup

---

## Network Latency

- Even on a local LAN: variable, jitter-prone
- For RT over network: use UDP, not TCP (TCP retransmits add unbounded delay)
- Real-time Ethernet protocols: TSN (Time-Sensitive Networking), EtherCAT
- Wireless RT is hard; possible but careful design needed
- Avoid the network in the hot path if you can

---

## Lock Contention

- Waiting for a lock = waiting for an arbitrary amount of time
- For RT: minimise locking, use lock-free data structures, or use priority inheritance
- The "priority inversion" problem (next chapter)
- Even short locks can cascade into long waits under contention
- A locked thread is an unscheduled thread

---

## Garbage Collection

- Languages with GC (Java, Go, C#): unpredictable pauses
- Modern GCs (ZGC, Shenandoah, Java 21+): sub-millisecond pauses possible
- Still a risk for hard RT
- For Java RT: real-time GCs (Azul Zing, Sun RTSJ) exist
- For C# RT: rare; Rust or C is the typical pick

---

## Measuring Latency

- `cyclictest`: kernel wake-up latency (Linux)
- Hardware timers: precise event timing
- `perf` / `ftrace`: kernel-level event tracing
- DTrace / eBPF: probe-based tracing
- Always measure under realistic load, not idle

---

## Common Mistakes

- Optimising the average case; ignoring the worst
- Believing benchmarks taken on an idle system
- Forgetting `mlockall`; one page fault later, deadline missed
- Using `printf` in the hot path (formats strings, blocks on stdout)
- Putting any unbounded operation (malloc, lock, syscall) in a deadline-bound thread
