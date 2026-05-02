---
tags:
  - infrastructure:real-time
  - infrastructure:hardware
level: advanced
category: real-time
audience:
  - audiences:embedded-engineers
  - audiences:developers

---
# Real-Time and the Hardware

---
## What This Chapter Covers

- Hardware-induced latency sources
- I/O bus timing and behaviour
- Interrupt sources and priorities
- SMM and other hidden traps
- CPU power management
- Picking RT-friendly hardware

---
## Hardware Matters

- Software can't fix bad hardware behaviour
- Modern PCs are optimised for throughput, not predictability
- Microcontrollers are optimised for predictability
- The hardware sets a floor on what's achievable
- Pick hardware before tuning software

---
## Hardware Concerns

![hw_concerns](svg/courses/real_time/real-time-programming/10_real_time_and_the_hardware/hw_concerns.svg)

---
## I/O Buses and Latency

- **PCIe**: high throughput, variable latency
- **SPI / I2C**: bounded by clock, predictable
- **UART**: simple, predictable
- **CAN**: bounded by protocol, used for automotive
- For RT: simpler buses are easier to reason about

---
## DMA Adds Predictability

- DMA controller transfers without CPU
- CPU doesn't compete with the device for memory cycles (much)
- Common in: networking, audio, sensor data
- Reduces interrupt rate (one per DMA completion vs per byte)
- Modern peripherals usually offer DMA

---
## Interrupt Storms

- A misbehaving device can fire interrupts faster than the CPU handles them
- Can lock out RT threads entirely
- Mitigation: rate-limit, mask, debounce
- Test under fault conditions, not just nominal load
- A failed sensor can take down the system

---
## Interrupt Priorities

- Hardware-level priority encoder picks the next IRQ
- Higher priority interrupts preempt lower ones
- Most RT systems have well-defined priority orderings
- Check your CPU's interrupt controller docs (NVIC on ARM, APIC on x86)
- A misconfigured priority gives surprises

---
## SMM (System Management Mode) on x86

- A hardware-level mode invisible to the OS
- BIOS / firmware can run code in SMM
- Latency: tens to hundreds of microseconds, *unmasked*
- Problem: can preempt anything, even the kernel
- Mitigations: vendor firmware that minimises SMM use, custom firmware, alternative platforms

---
## CPU Power Management

- C-states: power-saving idle states
- Deeper state = longer wake-up latency
- C0 (active) &#8594; C1 (~1 us) &#8594; C6 (~30 us) &#8594; C10 (~100+ us)
- For RT: pin the CPU to C0 or C1 (`cpuidle.off=1` or set governor)
- Saves power, costs predictability

---
## CPU Frequency Scaling

- Modern CPUs change frequency based on load
- Wakeup may need to ramp up frequency before running
- Slows the first instruction
- For RT: set governor to `performance` (`cpupower frequency-set -g performance`)
- Disables scaling, locks at max

---
## Hyperthreading

- Two logical CPUs share one physical core
- Threads can interfere with each other unpredictably
- For RT: disable hyperthreading or pin RT threads to dedicated physical cores
- The cost of fewer logical cores is worth the predictability
- Modern CPUs: SMT can be disabled in BIOS or at boot

---
## Cache Effects from Other Cores

- Cache snoop traffic can stall an RT core
- A non-RT core writing heavily can invalidate RT-core caches
- Mitigations: cache partitioning (Intel CAT), L3 isolation
- High-end CPUs offer hardware cache QoS
- For demanding RT: dedicate a CPU and minimise sharing

---
## NUMA Effects

- Multi-socket systems: memory is local or remote
- Remote memory access: 2-3x slower
- RT thread + memory should be on the same NUMA node
- `numactl --cpunodebind=0 --membind=0 ./app`
- Verify with `numastat`

---
## Picking RT Hardware

- For hard RT: dedicated microcontroller (ARM Cortex-M, RISC-V)
- For soft RT on Linux: server-grade CPU with good SMM behaviour
- Avoid laptops and consumer hardware (aggressive power management)
- Industrial PCs (Advantech, Kontron) tested for RT
- ARM Cortex-R and -A processors aimed at RT

---
## Real-Time Ethernet

- Standard Ethernet: best-effort, no timing guarantees
- TSN (Time-Sensitive Networking): IEEE 802.1 standards for bounded latency
- EtherCAT, PROFINET: industrial RT Ethernet protocols
- Hardware support required (switches and NICs)
- Plain Ethernet is fine for soft RT; TSN for hard RT over network

---
## Watchdog Timers

- A hardware timer that *resets the system* if not "kicked" regularly
- Catches deadlocks, infinite loops, runaway threads
- The application kicks every N ms; if it doesn't, reboot
- Last line of defence in safety-critical systems
- Standard practice in embedded RT

---
## Common Hardware Pitfalls

- SMM interrupts on x86 (especially older firmware)
- Power management waking up slow
- Hyperthreading interference
- Shared L3 cache thrashing
- BIOS settings aimed at "energy efficiency"
- Always test on production hardware, not your laptop

---
## A Pre-Production Checklist

- BIOS: disable hyperthreading, set CPU to performance
- Bootloader: isolcpus, nohz_full, rcu_nocbs for RT cores
- Kernel: PREEMPT_RT, current LTS
- App: SCHED_FIFO, mlockall, pinned to CPU
- IRQs: pinned away from RT CPUs
- Run cyclictest under load; verify worst-case latency

---
## Course Wrap-Up

- Real-time is about *predictability*, not speed
- Every layer of the stack contributes latency
- Worst-case is what matters, not average
- The OS, the libraries, the hardware all need attention
- Measure relentlessly; trust nothing without data
- Most RT failures come from skipping one of these steps
