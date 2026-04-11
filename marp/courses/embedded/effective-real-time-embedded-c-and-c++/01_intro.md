---
tags:
  - hardware-and-embedded:embedded
  - infrastructure:real-time
  - languages:c
  - languages:c++
level: advanced
category: embedded
audience:
  - audiences:embedded-engineers
  - audiences:developers
---
# Effective Real Time Embedded C and C++

---

## Welcome to the Course

This comprehensive 4-day course will enhance your C and C++ programming skills for real-time embedded systems development.

---

## Course Overview

1. Advanced language features for embedded systems
1. Real-time programming considerations
1. Hardware-software interaction
1. Best practices and safety standards

---

## What Makes Embedded Different?

1. Limited resources (memory, processing power)
1. Real-time constraints
1. Direct hardware interaction
1. Safety and reliability requirements

---

## Real-Time Systems

**Definition**: Systems where correctness depends not only on logical results but also on the time at which results are produced.

---

## Types of Real-Time Systems

1. **Hard Real-Time**: Missing deadlines causes system failure
1. **Soft Real-Time**: Missing deadlines degrades performance
1. **Firm Real-Time**: Occasional deadline misses tolerable

---

## Embedded System Constraints

![embedded_system_constraints](svg/courses/embedded/effective-real-time-embedded-c-and-c++/01_intro/embedded_system_constraints.svg)

---

## Course Goals

1. Master advanced C/C++ features for embedded systems
1. Understand compile, link, and runtime issues
1. Learn real-time programming techniques
1. Apply best practices for safety and reliability

---

## What You'll Learn

1. Memory management in constrained environments
1. Interrupt handling and timing
1. Inter-task communication
1. Hardware peripheral programming
1. Safety standards (MISRA-C)

---

## Prerequisites Check

1. **Required**: Good grasp of C and/or C++ fundamentals
1. **Helpful**: Understanding of real-time concepts
1. **Beneficial**: Experience with embedded systems

---

## Course Structure

1. **Day 1**: Embedded C fundamentals and memory
1. **Day 2**: Communication, synchronization, and toolchain
1. **Day 3**: Hardware, timing, and safety
1. **Day 4**: C++ for embedded systems

---

## Development Environment

Typical embedded development setup:
1. Cross-compiler toolchain
1. Hardware debugger (JTAG/SWD)
1. Target board or simulator
1. IDE or command-line tools

---

## Embedded vs Desktop Programming

| Desktop | Embedded |
|---------|----------|
| Abundant resources | Limited resources |
| OS abstractions | Direct hardware access |
| Virtual memory | Fixed memory |
| Standard libraries | Custom/minimal libraries |

---

## The Embedded Software Stack

![the_embedded_software_stack](svg/courses/embedded/effective-real-time-embedded-c-and-c++/01_intro/the_embedded_software_stack.svg)

---

## Common Embedded Architectures

1. **8-bit**: AVR, 8051, PIC
1. **16-bit**: MSP430, PIC24
1. **32-bit**: ARM Cortex-M, RISC-V
1. **DSP**: TI C2000, Analog Devices SHARC

---

## Memory Types in Embedded Systems

1. **ROM/Flash**: Program code and constants
1. **RAM**: Variables and stack
1. **EEPROM**: Non-volatile configuration
1. **External Memory**: SDRAM, SPI Flash

---

## Real-Time Operating Systems (RTOS)

Popular choices:
1. FreeRTOS
1. Zephyr
1. RT-Thread
1. Bare metal (no OS)

---

## Development Tools

1. **Compilers**: GCC, IAR, Keil
1. **Debuggers**: GDB, J-Link, ST-Link
1. **Analyzers**: Logic analyzers, oscilloscopes
1. **Profilers**: Runtime analysis tools

---

## Industry Standards

1. **MISRA-C**: Motor Industry Software Reliability
1. **AUTOSAR**: Automotive Open System Architecture
1. **DO-178C**: Avionics Software
1. **IEC 61508**: Functional Safety

---

## Course Methodology

1. Theory and concepts
1. Practical examples
1. Code demonstrations
1. Best practices
1. Common pitfalls
