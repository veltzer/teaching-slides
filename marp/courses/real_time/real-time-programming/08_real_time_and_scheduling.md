---
tags:
  - infrastructure:real-time
  - infrastructure:scheduling
level: advanced
category: real-time
audience:
  - audiences:embedded-engineers
  - audiences:developers

---
# Real-Time and Scheduling

---
## RMS vs EDF

![scheduling](svg/courses/real_time/real-time-programming/08_real_time_and_scheduling/scheduling.svg)

---
## What This Chapter Covers

- Designing threads and priorities
- CPU affinity and migration
- Interrupts as latency sources
- Pinning interrupts to CPUs
- The priority inversion problem and its solutions
- Schedulability analysis basics

---
## Linux Scheduling Classes

- **SCHED_OTHER (CFS)**: default; fair-share; non-RT
- **SCHED_BATCH**: like OTHER but optimised for batch
- **SCHED_IDLE**: lowest priority
- **SCHED_FIFO**: first-in-first-out at fixed priority
- **SCHED_RR**: like FIFO but with time slicing
- **SCHED_DEADLINE**: EDF-based, true real-time

---
## SCHED_FIFO

- Real-time priority class
- Priorities 1-99 (higher = more important)
- A SCHED_FIFO thread runs until it blocks or yields
- Preempts SCHED_OTHER
- The simplest real-time scheduling

---
## SCHED_RR

- Like SCHED_FIFO but with time slices
- Same priority threads share CPU in round-robin
- Default time slice 100ms (configurable)
- Less commonly used than FIFO
- Useful when several equal-priority RT threads need to run

---
## SCHED_DEADLINE

- EDF (Earliest Deadline First) scheduler
- Each thread has period, deadline, runtime
- Kernel guarantees runtime per period
- Theoretically optimal for many task sets
- Linux 3.14+; less commonly used than FIFO

---
## Setting Priority

```c
#include <sched.h>
struct sched_param p = { .sched_priority = 80 };
pthread_setschedparam(pthread_self(), SCHED_FIFO, &p);
```

- Or via `chrt -f 80 ./myapp` from the shell
- Requires `CAP_SYS_NICE` capability (or root)
- SCHED_FIFO at priority 99: highest non-kernel priority

---
## Designing Priorities

- One thread per criticality level
- More critical = higher priority
- *Don't* give all RT threads priority 99; you lose information
- Document the priority assignment
- Standard practice: rate-monotonic — shorter period = higher priority

---
## Rate-Monotonic Analysis

- Theoretical analysis of fixed-priority scheduling
- A task set is schedulable if `sum(C_i / T_i) <= n * (2^(1/n) - 1)`
- For n &#8594; infinity, the bound is ~69%
- For practical n (say 5): ~74%
- A budget; not a guarantee, but a useful starting point

---
## CPU Affinity

```c
cpu_set_t set;
CPU_ZERO(&set);
CPU_SET(2, &set);                       // CPU 2 only
sched_setaffinity(0, sizeof(set), &set);
```

- Pin a thread to a specific CPU
- Avoids migration cost
- Improves cache locality
- Critical for predictable RT
- `taskset` for command-line use

---
## CPU Isolation

- Take CPUs out of the kernel's general scheduler pool
- Boot Linux with `isolcpus=2,3`
- CPUs 2-3 won't run anything unless explicitly assigned
- Reserved for RT workloads
- Pair with `nohz_full=2,3` to disable scheduler tick on those CPUs

---
## Interrupts as Latency Sources

- An interrupt preempts whatever is running, including RT threads
- A high-rate interrupt source can starve RT threads
- Solutions: route interrupts away from RT CPUs
- `/proc/irq/<n>/smp_affinity` controls per-IRQ CPU
- Some IRQs (timer, IPI) can't be moved

---
## Pinning Interrupts

```bash
echo 1 > /proc/irq/24/smp_affinity     # IRQ 24 -> CPU 0
```

- Bitmask: bit 0 = CPU 0, bit 1 = CPU 1, etc.
- Default: kernel balances across all CPUs (`irqbalance`)
- For RT: disable irqbalance, pin manually
- Verify with `cat /proc/interrupts`

---
## Priority Inversion

- Low-priority thread holds a lock that a high-priority thread needs
- High-priority thread blocks
- Medium-priority thread runs, indirectly delaying the high-priority one
- A famous example: Mars Pathfinder rover (1997)
- Without protection, can cause arbitrary delays

---
## Priority Inversion Diagram

![priority_inversion](svg/courses/real_time/real-time-programming/08_real_time_and_scheduling/priority_inversion.svg)

---
## Solution: Priority Inheritance

- The lock-holding thread *temporarily inherits* the priority of any waiter
- A medium-priority thread can no longer preempt
- Lock release returns the holder to its original priority
- Linux: `pthread_mutexattr_setprotocol(..., PTHREAD_PRIO_INHERIT)`
- The standard solution

---
## Solution: Priority Ceiling

- Each lock has a priority ceiling — the highest priority of any thread that uses it
- A thread holding the lock runs at the ceiling priority
- Avoids many forms of priority inversion analytically
- Requires knowing all threads that may use the lock
- Less common in user-space than priority inheritance

---
## Schedulability in Practice

- Compute total CPU usage (sum of C/T)
- Add safety margin (RM bound is conservative)
- Measure the worst case under realistic load
- If a deadline is missed, either reduce work or increase priority of the blocker
- Be skeptical of "average" measurements — RT is about the worst case

---
## Common Mistakes

- All RT threads at priority 99 (no ordering, surprises)
- Forgetting to pin interrupts away from RT CPUs
- Using non-PI mutexes &#8594; priority inversion bites
- Not using isolcpus &#8594; non-RT load steals time
- Not measuring worst-case latency under realistic load
