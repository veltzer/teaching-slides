---
tags:
  - hardware-and-embedded:embedded
  - hardware-and-embedded:hardware-programming
  - infrastructure:real-time
level: advanced
category: embedded
audience:
  - audiences:embedded-engineers
  - audiences:developers

---
# Race Conditions To Expect

---

## Chapter Overview

1. Three sources of concurrency on this board
1. Memory ordering and store buffers
1. Torn reads and writes
1. Lost updates and the ABA problem
1. Deadlock, priority inversion and how to debug

---

## Three Concurrency Sources

1. **CPU1 vs its own interrupts** — classic single-core race
1. **CPU1 vs CPU2** — true parallel race across cores
1. **CPU vs DMA / radio** — hardware writing memory behind you
1. Each needs different protection
1. Most bugs come from assuming the wrong source

---

## The Single-Core Interrupt Race

```c
volatile uint32_t counter;

void main_loop(void) { counter++; }        // read-mod-write
void TIM2_IRQHandler(void){ counter++; }    // also r-m-w

// If the IRQ fires between the read and the write,
// one increment is LOST. 'volatile' does NOT fix this.
```

Fix: disable the IRQ around the access, or use an atomic.

---

## Critical Sections On One Core

```c
uint32_t primask = __get_PRIMASK();
__disable_irq();
counter++;                 // now atomic w.r.t. interrupts
__set_PRIMASK(primask);    // restore prior state
```

1. Keep critical sections **tiny**
1. Restore the **previous** mask — don't blindly enable
1. This protects against **interrupts**, not against CPU2

---

## Why Cross-Core Is Harder

1. Disabling **your** interrupts does nothing to the other core
1. CPU2 keeps running while CPU1 is in its "critical section"
1. There is no shared `__disable_irq()`
1. You need **HSEM** or a lock-free protocol
1. The mental model from single-core **does not transfer**

---

## Memory Ordering Across Cores

![memory_ordering](svg/courses/embedded/stm32-nucleo-wl55jc1-firmware/09_race_conditions/memory_ordering.svg)

---

## The Reordering Trap

```c
// CPU1 intends: write data, THEN announce it
g_shared.payload[0] = 0x42;
g_shared.ready = 1;          // CPU2 may see this FIRST

// CPU2 sees ready==1 but reads a STALE payload.
```

The store buffer can make `ready` visible before `payload`.
Insert `__DMB()` between them. Every time.

---

## Torn Reads And Writes

1. A 64-bit value is written as **two** 32-bit stores
1. The other core can read **between** the halves
1. Result: a value that **never existed**
1. Only naturally-aligned **word** access is atomic here
1. Keep cross-core fields ≤ 32 bits, or guard them

---

## A Torn 64-bit Timestamp

```c
volatile uint64_t timestamp;   // two 32-bit stores!

// CPU1: timestamp = 0x0000_0001_FFFF_FFFF;
//   store low  = 0xFFFFFFFF
//   --- CPU2 reads here ---
//   store high = 0x00000001
// CPU2 may observe 0x0000_0000_FFFF_FFFF: garbage.
```

Use a 32-bit value, a sequence lock, or an HSEM.

---

## The Lost-Update Race

```c
// Both cores run: shared.count = shared.count + 1;
// CPU1 reads 5            CPU2 reads 5
// CPU1 writes 6           CPU2 writes 6
// Two increments, result is 6, not 7. One was LOST.
```

1. Read-modify-write on shared data is **never** safe bare
1. `volatile` does not help — it is not atomic
1. Guard with **HSEM** or make it single-writer

---

## The Sequence-Lock Pattern

```c
// Writer bumps seq odd before, even after.
do {
    s1 = seq; __DMB();
    copy = shared_struct;        // read whole struct
    __DMB(); s2 = seq;
} while ((s1 & 1) || s1 != s2);  // retry if writer was active
```

Lets a reader get a **consistent snapshot** without a lock.

---

## The ABA Problem

1. You read a value **A**, plan an update based on it
1. Meanwhile it changes to **B** and back to **A**
1. Your check "still A?" passes — but state really moved
1. Bites lock-free **stacks/queues** using raw pointers
1. Defend with a **version counter** alongside the value

---

## Deadlock Across Cores

1. CPU1 takes HSEM 0, then wants HSEM 1
1. CPU2 takes HSEM 1, then wants HSEM 0
1. Both wait forever — **deadlock**
1. Fix: always take semaphores in a **fixed global order**
1. Or use a single lock; never nest if you can avoid it

---

## Priority Inversion

1. Low-priority task holds a lock the radio IRQ needs
1. A medium task preempts the low task
1. The radio is now blocked by an **unrelated** task
1. On an RF node this can **miss a receive window**
1. Keep locked sections short; avoid locks in hot paths

---

## Debugging Concurrency Bugs

1. Symptoms are **intermittent** and **timing-dependent**
1. Adding a `printf` often makes them **vanish** (Heisenbug)
1. Log to a **shared ring buffer**, read it after the fact
1. Suspect a missing **`__DMB()`** first
1. Reproduce by **stressing** timing, not by single-stepping

---

## A Defensive Checklist

1. Is every cross-core field **≤ 32 bits and aligned**?
1. Is there a **barrier** between data and its "ready" flag?
1. Is each field written by **exactly one** core?
1. Are shared mutations guarded by **HSEM**?
1. Are semaphores always taken in the **same order**?

---

## Key Takeaways

1. Three race sources: **IRQ, cross-core, DMA/radio**
1. `volatile` ≠ atomic and ≠ ordering
1. **`__DMB()`** prevents the reordering trap
1. Keep shared fields **word-sized and aligned** to avoid tearing
1. **HSEM**, single-writer, and fixed lock order keep you safe
