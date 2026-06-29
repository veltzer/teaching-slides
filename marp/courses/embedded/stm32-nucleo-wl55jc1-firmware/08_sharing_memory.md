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
# Sharing Memory Between The Cores

---

## Chapter Overview

1. Carving out a shared region in the linker scripts
1. Placing data there from both cores
1. Layout, alignment and ownership rules
1. Lock-free patterns that actually work
1. Hardware semaphores for true mutual exclusion

---

## Where Shared Memory Lives

1. Both cores already see all of SRAM1 and SRAM2
1. "Sharing" means **both build artifacts agree** on an address
1. Convention: dedicate part of **SRAM2** to shared data
1. Both linker scripts must **reserve the same region**
1. ST examples call this section `MAPPING_TABLE` / shared RAM

---

## Reserve The Region (CPU1 Linker)

```ld
MEMORY
{
  FLASH  (rx)  : ORIGIN = 0x08000000, LENGTH = 256K
  RAM1   (xrw) : ORIGIN = 0x20000000, LENGTH = 32K
  /* Carve the top of SRAM2 out for sharing */
  RAM2   (xrw) : ORIGIN = 0x20008000, LENGTH = 30K
  RAM_SHARED (xrw) : ORIGIN = 0x2000F800, LENGTH = 2K
}
```

The **CPU2 linker script must declare the identical region.**

---

## Place A Struct In Shared RAM

```c
// Both cores compile this same header
typedef struct {
    volatile uint32_t cmd;
    volatile uint32_t len;
    uint8_t  payload[256];
} shared_block_t;

// Force it into the shared section by both linkers
__attribute__((section(".ram_shared")))
shared_block_t g_shared;
```

Identical layout on both sides is **non-negotiable**.

---

## The Shared Memory Picture

![shared_memory_map](svg/courses/embedded/stm32-nucleo-wl55jc1-firmware/08_sharing_memory/shared_memory_map.svg)

---

## Layout Must Match Exactly

1. Same struct definition compiled by **both** cores
1. Same **packing** and **alignment** — pin it with `aligned`
1. Same **endianness** (both are little-endian here — easy)
1. Beware the compilers differ (M4 vs M0+ flags)
1. A single field mismatch = silent **garbage**

---

## Alignment And `volatile`

```c
// Align to a word so single-word reads/writes are atomic
typedef struct __attribute__((aligned(4))) {
    volatile uint32_t producer_index;
    volatile uint32_t consumer_index;
    uint32_t buffer[64];
} ring_t;
```

1. `volatile` stops the compiler caching shared fields
1. `volatile` does **not** provide ordering — that is `__DMB()`
1. `volatile` is **not** a lock

---

## Ownership: The Single-Writer Rule

1. Easiest correct pattern: **one writer per field**
1. CPU1 owns "command", CPU2 owns "response"
1. No field is written by both cores
1. The reader only ever **reads** the other's field
1. Eliminates most races by **construction**

---

## A Lock-Free Mailbox

```c
// CPU1 produces, CPU2 consumes. One slot, one flag.
// 'ready' is written only by CPU1, cleared only by CPU2.
void cpu1_send(const msg_t *m) {
    while (g_shared.ready) { }      // wait for slot free
    g_shared.msg = *m;
    __DMB();                        // publish data first
    g_shared.ready = 1;             // then the flag
    HAL_IPCC_NotifyCPU(&hipcc, CH, IPCC_CHANNEL_DIR_TX);
}
```

Publish data, **barrier**, then the flag — order is everything.

---

## A Lock-Free Ring Buffer

1. Producer advances `head`; consumer advances `tail`
1. Each index has **exactly one** writer
1. Reader checks `head != tail` for data available
1. **Barrier** between writing data and advancing the index
1. Power-of-two size lets you mask instead of modulo

---

## When You Truly Need A Lock

1. Two cores must update the **same** structure
1. The single-writer rule cannot be applied
1. You need genuine **mutual exclusion**
1. Plain `volatile` flags **cannot** do this safely
1. Use the hardware **semaphore (HSEM)** peripheral

---

## The Hardware Semaphore (HSEM)

```c
// Atomic test-and-set across both cores, in hardware
if (HAL_HSEM_FastTake(HSEM_ID_0) == HAL_OK) {
    // critical section: both cores honor this lock
    update_shared_table();
    HAL_HSEM_Release(HSEM_ID_0, 0);
}
```

1. HSEM is **atomic across cores** — `volatile` is not
1. It can also raise an IRQ when released
1. The right tool for shared mutable structures

---

## Don't Reinvent Atomics In RAM

1. A software "lock = 1" flag in shared RAM is **broken**
1. Both cores can read 0, both write 1, both proceed
1. This is the classic **lost-update** race
1. The M0+ has **no exclusive-access** monitor pairing here
1. Use **HSEM** — it exists precisely for this

---

## Key Takeaways

1. Sharing = both linker scripts **reserve the same region**
1. **Identical struct layout** on both cores, no exceptions
1. Prefer the **single-writer** rule — it kills races by design
1. Lock-free mailboxes/rings need a **barrier**, not a lock
1. For shared mutation, use the hardware **HSEM**
