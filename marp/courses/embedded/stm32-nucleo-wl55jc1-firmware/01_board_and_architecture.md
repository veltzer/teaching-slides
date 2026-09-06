---
tags:
  - hardware-and-embedded:embedded
  - hardware-and-embedded:hardware-programming
level: advanced
category: embedded
audience:
  - audiences:embedded-engineers
  - audiences:developers

---

# The Board And Its Dual-Core Architecture

---

## Chapter Overview

1. What the NUCLEO-WL55JC1 actually is
1. The STM32WL55 dual-core SoC
1. Memory map and shared SRAM
1. Clock tree and boot flow
1. How the two cores divide the work

---

## What Is The NUCLEO-WL55JC1?

1. ST evaluation board for the **STM32WL55JC** SoC
1. A single chip integrating an MCU **and** a sub-GHz radio
1. Targets LoRa, (G)FSK, (G)MSK and BPSK long-range links
1. On-board ST-LINK/V2-1 debugger and USB
1. Two on-board RF paths (high-power and low-power)

---

## The STM32WL55 Is Dual-Core

1. **Cortex-M4** at up to 48 MHz — the *application* core (CPU1)
1. **Cortex-M0+** at up to 48 MHz — the *network* core (CPU2)
1. Both cores share the same flash and SRAM
1. The M0+ has **no debug port exposed** on most setups
1. The M0+ usually runs the radio / protocol stack

---

## Why Two Cores?

1. Radio protocols (LoRaWAN) have **hard timing** requirements
1. Isolating the stack on CPU2 keeps it deterministic
1. CPU1 runs your application logic freely
1. ST ships the stack as a binary for CPU2
1. You can also ignore CPU2 and run **single-core**

---

## Memory Map Essentials

1. **Flash**: 256 KB, shared, securable into CPU1/CPU2 regions
1. **SRAM1**: 32 KB — general purpose
1. **SRAM2**: 32 KB — often used for shared / retained data
1. Peripherals are split by **bus** (APB1/APB2/AHB)
1. Some peripherals are *securable* to one core only

---

## Memory Map Overview

![memory_map_overview](svg/courses/embedded/stm32-nucleo-wl55jc1-firmware/01_board_and_architecture/memory_map_overview.svg)

---

## The Clock Tree

1. **MSI** — multi-speed internal RC, the default after reset
1. **HSE** — driven by a 32 MHz **TCXO** (needed for the radio)
1. **HSI16** — 16 MHz internal RC
1. **LSE** — 32.768 kHz crystal for RTC / low power
1. The radio derives its reference from the **HSE/TCXO**

---

## Boot Flow

1. Reset releases **CPU1 (M4)** first
1. CPU1 runs the option-byte-selected boot address
1. CPU1 is responsible for **booting CPU2** when needed
1. `PWR_CR4` `C2BOOT` bit starts the M0+
1. If you never set it, CPU2 simply stays asleep

---

## Dual-Core Boot Sequence

![dual_core_boot_sequence](svg/courses/embedded/stm32-nucleo-wl55jc1-firmware/01_board_and_architecture/dual_core_boot_sequence.svg)

---

## How Work Is Divided

1. **CPU1 (M4)**: application, sensors, UI, business logic
1. **CPU2 (M0+)**: LoRaWAN / radio MAC and PHY timing
1. They communicate over the **IPCC** mailbox
1. They share state in **SRAM2**
1. We will spend whole chapters on each of these

---

## Three Ways To Program This Board

1. **Single-core bare metal** — M4 only, registers directly
1. **Single-core with HAL** — M4 only, ST driver library
1. **Dual-core** — M4 + M0+ with IPCC and shared memory
1. We build up in exactly this order
1. Start simple; add the radio core last

---

## Key Takeaways

1. One chip = **MCU + sub-GHz radio**
1. Two cores: **M4 application**, **M0+ network**
1. Flash and SRAM are **shared** between the cores
1. The radio needs the **TCXO-driven HSE**
1. CPU1 boots CPU2 — never the other way around
