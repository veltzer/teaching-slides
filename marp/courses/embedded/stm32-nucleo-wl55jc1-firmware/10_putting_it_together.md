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
# Putting It Together

---

## Chapter Overview

1. A reference architecture for a WL55 node
1. How the layers we learned stack up
1. A worked end-to-end data flow
1. Common mistakes and how to avoid them
1. Where to go next

---

## A Sensor-To-Cloud Node

1. **CPU1 (M4)**: reads a sensor, runs app logic, sleeps
1. **CPU2 (M0+)**: runs the LoRaWAN stack and radio timing
1. **IPCC**: carries send/receive requests between them
1. **Shared SRAM**: holds the payloads
1. **Low power**: both cores sleep between transmissions

---

## The Full Stack We Built

![full_node_architecture](svg/courses/embedded/stm32-nucleo-wl55jc1-firmware/10_putting_it_together/full_node_architecture.svg)

---

## End-To-End: Sending A Reading

1. RTC wakes **CPU1** from Stop2
1. CPU1 reads the sensor over I2C
1. CPU1 writes the payload to **shared SRAM**, `__DMB()`
1. CPU1 rings **IPCC**; **CPU2** wakes and takes the job
1. CPU2 transmits over the radio, then both cores sleep

---

## Choosing Your Approach

| Goal                         | Use                       |
| ---------------------------- | ------------------------- |
| Learn the silicon            | bare metal                |
| Ship an app fast             | HAL                       |
| Tight ISR / radio timing     | LL or registers           |
| Use the radio at all         | dual-core + ST middleware |
| Shared mutable state         | HSEM                      |

---

## Common Mistakes

1. Forgetting to **enable a peripheral clock**
1. Omitting **`__DMB()`** before a cross-core flag
1. Editing outside CubeMX **`USER CODE`** markers
1. Not re-running `SystemClock_Config()` after Stop
1. Treating a `volatile` flag as a **lock**

---

## Performance And Power Hygiene

1. Measure sleep current with a **real meter**, not a guess
1. Keep ISRs short; defer to the main loop
1. Prefer **DMA** for bulk transfers
1. Let the node spend most of its life in **Stop2**
1. Profile before stripping the HAL for "speed"

---

## Where To Go Next

1. Read the **STM32WL reference manual** (RM0453)
1. Study ST's **STM32CubeWL** dual-core examples
1. Learn the **LoRaWAN** regional parameters for your area
1. Explore an **RTOS** on CPU1 (FreeRTOS / ThreadX)
1. Add **secure boot** and the TrustZone-lite features

---

## Course Recap

1. Three programming styles: **bare metal, HAL, dual-core**
1. Peripherals are **memory-mapped** and **interrupt-driven**
1. Two cores cooperate via **IPCC + shared SRAM**
1. Concurrency brings **races** — barriers and HSEM defend
1. Low power is a **first-class design constraint**

---

## Thank You

1. Questions welcome
1. [mark.veltzer@gmail.com](mailto:mark.veltzer@gmail.com)
1. Go build something that talks to the sky
