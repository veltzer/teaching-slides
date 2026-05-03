---
tags:
  - infrastructure:real-time
  - infrastructure:operating-systems
level: advanced
category: real-time
audience:
  - audiences:embedded-engineers
  - audiences:developers

---
# Real-Time Systems and Operating Systems

---
## What This Chapter Covers

- Traditional real-time operating systems
- Linux as a real-time platform
- The PREEMPT_RT patch
- Deficiencies in traditional RTOSes
- A pragmatic comparison
- Picking the right OS for your problem

---
## What an RTOS Is

- An operating system designed for *predictable* response, not throughput
- Bounded interrupt latency
- Bounded scheduler decision time
- Deterministic context switches
- Often small kernels, no virtual memory, no swap
- Sells the desktop conveniences for predictability

---
## RTOS Features

![rtos_features](svg/courses/real_time/real-time-programming/03_the_connections_between_real_time_systems_and_operating_systems/rtos_features.svg)

---
## Common RTOSes

- **FreeRTOS**: dominant in microcontrollers; open source; small footprint
- **VxWorks**: long history in aerospace and industrial; commercial
- **INTEGRITY**: high-assurance; safety-certified; commercial
- **QNX**: microkernel; common in automotive; commercial
- **Zephyr**: newer; permissively licensed; growing
- **RTEMS**: open source; aerospace heritage

---
## Linux as RT?

- Stock Linux is *not* hard real-time
- The kernel can preempt user space, but not always itself
- High-priority threads can be blocked by kernel work
- Worst-case latency: tens to hundreds of milliseconds
- Acceptable for soft RT; unacceptable for hard RT

---
## PREEMPT_RT

- A patch set making the Linux kernel fully preemptible
- Almost everything becomes preemptible: spinlocks become mutexes, IRQ handlers become threads
- Worst-case latency drops from ms to tens of microseconds
- Cost: somewhat lower throughput
- Available as a patch; large parts merged into mainline (5.x onward)

---
## Linux + PREEMPT_RT in Practice

- Now a serious soft-RT and even some hard-RT platform
- Industrial automation, audio production, lab instruments
- Combined with isolcpus, no_hz, and CPU pinning, can hit ~10-50us latency
- Still not certified for safety-critical (avionics, automotive)
- For most "we need real-time" needs, this is the answer

---
## Real-Time Linux Toolkit

- `cyclictest`: measures wake-up latency (the canonical RT benchmark)
- `chrt`: set scheduling policy and priority of a process
- `taskset`: pin processes to CPUs
- `tuned` profiles: prebuilt RT-friendly system tunings
- `tracecmd` / `kernelshark`: trace what's happening in the kernel

---
## Where RTOSes Beat Linux

- Memory footprint: 10s of KB vs 100s of MB
- Boot time: milliseconds vs seconds
- Determinism: nanoseconds of jitter vs tens of microseconds
- Certification: pre-certified for industry standards
- Simplicity: smaller attack surface, smaller code base

---
## Where Linux Beats RTOSes

- Hardware support: drivers for everything
- Network stack: production-quality TCP/IP, modern protocols
- Tooling: gdb, perf, strace, etc.
- Languages: full Python, modern compilers, libraries
- Developer experience: way easier

---
## Mixed-Criticality with Hypervisors

- Run an RTOS for the safety-critical workload
- Run Linux for the rich features
- A hypervisor (Xen, Jailhouse) keeps them isolated
- Common pattern in modern automotive / industrial systems
- Bare-metal hypervisors avoid the overhead of full virtualisation

---
## Deficiencies in Traditional RTOSes

- Older RTOSes: no memory protection between tasks
- Single bug crashes the whole system
- Modern variants address this (memory protection units)
- Tooling lags general-purpose ecosystems
- Cost of certification is sometimes opaque
- Lock-in: switching RTOSes is a major project

---
## Choosing for a New Project

- Hard RT, certified, safety-critical &#8594; commercial RTOS
- Hard RT, not certified, embedded &#8594; FreeRTOS, Zephyr
- Soft RT, rich features, networking &#8594; Linux + PREEMPT_RT
- Best-effort, just needs to be fast &#8594; tuned Linux is fine
- Mixed criticality &#8594; hypervisor + RTOS + Linux

---
## Cost Considerations

- FreeRTOS: free
- Zephyr / RTEMS: free
- Linux: free; hardening costs engineering time
- VxWorks / INTEGRITY / QNX: substantial licence fees, support contracts
- Pre-certified versions cost more again (DO-178, ISO 26262)

---
## A Decision Tree

- Need DO-178 / ISO 26262 / IEC 62304? &#8594; commercial certified RTOS
- Microcontroller, &lt; 1 MB RAM? &#8594; FreeRTOS or Zephyr
- Soft RT with networking and full Linux ecosystem? &#8594; PREEMPT_RT Linux
- Mixed: hard RT logic + soft RT UI? &#8594; hypervisor architecture
- "Just fast"? &#8594; tuned Linux

---
## Tuning Linux for RT (Quick Tour)

- Apply `PREEMPT_RT` patch (or use mainline RT enabled)
- Boot with `isolcpus`, `nohz_full`, `rcu_nocbs` to isolate cores
- Use `chrt -f 50 ./app` to run with SCHED_FIFO priority 50
- Disable CPU frequency scaling (`cpupower frequency-set -g performance`)
- Lock memory with `mlockall` to avoid page faults

---
## Common Mistakes

- Picking VxWorks for a hobby project; paying enormous fees for nothing
- Picking stock Linux for hard RT; missing deadlines in production
- Believing a vendor's "real-time" marketing without measuring
- Switching OSes mid-project; underestimating the porting effort
- Not measuring latency before shipping
