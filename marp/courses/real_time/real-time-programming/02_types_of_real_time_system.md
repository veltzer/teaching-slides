---
tags:
  - infrastructure:real-time
level: advanced
category: real-time
audience:
  - audiences:embedded-engineers
  - audiences:developers

---
# Types of Real-Time System

---
## What This Chapter Covers

- Near real-time
- Soft real-time
- Hard real-time
- Mixed-criticality systems
- The economic implications of each
- How to choose the right level for your system

---
## The Three Categories

- **Near real-time**: deadlines aspirational; misses tolerated
- **Soft real-time**: misses degrade quality but don't break
- **Hard real-time**: misses are unacceptable failures
- Each has distinct engineering practices and costs
- Don't pay for hard RT when soft will do

---
## Examples by Category

![system_examples](svg/courses/real_time/real-time-programming/02_types_of_real_time_system/system_examples.svg)

---
## Near Real-Time

- "As fast as we can manage"
- No formal deadline
- Examples: chat applications, dashboard updates, log shipping
- Most consumer software is near real-time at most
- Engineering effort: minimal beyond normal performance work

---
## Soft Real-Time

- A defined deadline; missing it degrades but doesn't break
- Examples: video playback, voice calls, multiplayer games
- A dropped frame is annoying but the system works
- Engineering effort: profile the worst case; optimise; tolerate small misses
- Most multimedia and interactive software lives here

---
## Soft Real-Time Examples

- A 60 fps video means a 16.7ms budget per frame
- Miss it once: a stutter
- Miss it often: unwatchable
- Voice calls: 20ms packet rate, ~150ms total budget for round-trip
- Acceptable miss rate: low single-digit percent

---
## Hard Real-Time

- A defined deadline; missing it is a failure
- Examples: anti-lock brakes, avionics, pacemakers, motor control
- A single missed deadline can cause injury or death
- Engineering effort: enormous; formal analysis, certification
- A different mindset entirely

---
## Hard Real-Time Examples

- Pacemaker: pulse delivery on a strict cycle
- Anti-lock brakes: brake-pulse decisions every few ms
- Aircraft flight surfaces: position updates at known cadence
- Industrial robot arm: closed-loop control at kHz rates
- All have *certifications* (DO-178C, IEC 62304, ISO 26262)

---
## Firm Real-Time

- Sometimes called "near hard"
- A late result is useless, but missing one is not catastrophic
- Examples: streaming media frame deadlines, real-time databases
- Drop the missed work and continue
- Less stringent than hard, more stringent than soft

---
## Mixed-Criticality

- Many real systems mix hard, soft, and best-effort tasks
- A car has hard RT (brakes), soft RT (infotainment audio), best-effort (navigation)
- Modern approach: separate execution domains
- Hypervisors that guarantee isolation between criticality levels
- ARINC 653, Hypervisor partitioning, eBPF sandboxes

---
## Cost Comparison

- Near RT: ~normal SW project cost
- Soft RT: 1.5-3x normal cost (profiling, hardening)
- Hard RT: 10-100x normal cost (certification, formal methods, custom OS)
- The cost curve is steep
- Get the requirements right before picking the category

---
## Choosing a Category

- What are the *consequences* of a missed deadline?
- Is there a regulatory body involved?
- Is there a time budget you can quote?
- Can you measure misses?
- Be honest — many "we need real-time" requests are actually "we want low average latency"

---
## Hardware Implications

- Hard RT often needs predictable hardware: deterministic memory access, no out-of-order execution surprises, no SMM
- Soft RT runs on general-purpose hardware
- Cache effects matter more for hard RT
- Real-time CPUs (ARM Cortex-R, automotive-grade microcontrollers) exist for this
- Picking hardware affects everything downstream

---
## Software Implications

- Hard RT: typically an RTOS (FreeRTOS, VxWorks, INTEGRITY, RTEMS)
- Soft RT: tuned Linux (PREEMPT_RT patch) is often enough
- Near RT: any modern OS
- Language: C and C++ dominate; Rust is gaining; Python is rare
- The further down the stack you go, the less choice you have

---
## A Spectrum, Not Buckets

- Real systems often span the spectrum
- A car: brake control is hard, audio is soft, sat-nav is near
- The challenge is *isolation* — keeping non-critical from blocking critical
- This is the central design problem in mixed-criticality systems
- It's why airline avionics is structured the way it is

---
## Common Mistakes

- Calling soft RT "hard" because it sounds important
- Building for hard RT when soft would do (massive over-engineering)
- Ignoring the cost curve when scoping
- Thinking "we'll add real-time later" — usually impossible
- Confusing "low latency" with "real-time"
