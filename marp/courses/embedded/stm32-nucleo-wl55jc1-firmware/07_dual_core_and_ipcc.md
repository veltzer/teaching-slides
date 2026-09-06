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

# Dual-Core: Booting CPU2 And IPCC

---

## Chapter Overview

1. Bringing the second core to life
1. Why cores need a mailbox, not just shared RAM
1. The IPCC peripheral
1. Channels, signalling and acknowledgement
1. The full request/response round trip

---

## Two Cores, One Chip

1. **CPU1 (M4)** boots first and owns the system
1. **CPU2 (M0+)** stays asleep until CPU1 starts it
1. Both see the **same** flash and SRAM
1. They run **truly in parallel** — not time-sliced
1. Coordination is now a **hardware** problem

---

## Booting CPU2

```c
// CPU1 starts CPU2. CPU2's image lives in flash;
// its boot address is set by option bytes / SBRV.
HAL_PWREx_EnableBootC2();   // sets PWR_CR4 C2BOOT

// From here CPU2 runs its own vector table and main().
```

1. CPU2 will not run until this bit is set
1. CPU2's reset vector is configured separately
1. Get this wrong and CPU2 silently does nothing

---

## Why Not Just Share RAM?

1. Shared RAM lets cores **read/write** the same bytes
1. But how does CPU2 know CPU1 **wrote** something?
1. Polling RAM wastes power and adds latency
1. We need a **notification** mechanism
1. That is exactly what **IPCC** provides

---

## The IPCC Peripheral

1. **Inter-Processor Communication Controller**
1. A set of **channels** (six each direction on WL)
1. Each channel can be flagged **occupied** or **free**
1. Flagging a channel raises an **interrupt** on the other core
1. It carries **signals**, not data — data goes in shared RAM

---

## IPCC Channel Model

![ipcc_channel_model](svg/courses/embedded/stm32-nucleo-wl55jc1-firmware/07_dual_core_and_ipcc/ipcc_channel_model.svg)

---

## The Division Of Labour

1. **IPCC** = "something happened on channel N" (the doorbell)
1. **Shared SRAM** = the actual message payload (the parcel)
1. Sender writes payload to RAM, then rings the doorbell
1. Receiver reads payload from RAM, then clears the channel
1. Clearing the channel signals **"done"** back to the sender

---

## Sending: CPU1 To CPU2

```c
// 1. Write the request into the shared buffer
shared->cmd = CMD_TRANSMIT;
shared->len = len;
memcpy(shared->payload, data, len);

// 2. Ensure writes land before the doorbell
__DMB();

// 3. Ring the doorbell: occupy the TX channel
HAL_IPCC_NotifyCPU(&hipcc, IPCC_CHANNEL_1,
                   IPCC_CHANNEL_DIR_TX);
```

---

## Receiving: CPU2 Side

```c
// IPCC RX interrupt fires on CPU2 for channel 1
void rx_channel1_callback(IPCC_HandleTypeDef *h,
                          uint32_t ch, IPCC_CHANNELDirTypeDef dir) {
    __DMB();
    handle_command(shared->cmd, shared->payload, shared->len);

    // Mark channel free -> signals completion to CPU1
    HAL_IPCC_NotifyCPU(h, ch, IPCC_CHANNEL_DIR_RX);
}
```

---

## The Full Round Trip

![ipcc_round_trip](svg/courses/embedded/stm32-nucleo-wl55jc1-firmware/07_dual_core_and_ipcc/ipcc_round_trip.svg)

---

## ST's Stack Uses This For You

1. The LoRaWAN middleware speaks IPCC under the hood
1. ST defines a **MBMUX** (mailbox multiplexer) protocol
1. Your app calls a normal API on CPU1
1. MBMUX marshals it across to the stack on CPU2
1. You rarely touch IPCC directly — but you must understand it

---

## Memory Barriers Are Mandatory

1. The cores have **store buffers** and reorder memory ops
1. A payload write may not be visible when the doorbell rings
1. `__DMB()` forces writes to **complete first**
1. Skip the barrier and you get **intermittent** corruption
1. This is the gateway to the **race conditions** chapter

---

## Key Takeaways

1. CPU1 boots CPU2 via the **C2BOOT** bit
1. **IPCC** is a doorbell; **shared RAM** is the parcel
1. Notify to send, clear to acknowledge
1. **`__DMB()`** before ringing — ordering is not free
1. ST's **MBMUX** stack is built on exactly this
