---
tags:
  - infrastructure:real-time
level: advanced
category: real-time
audience:
  - audiences:embedded-engineers
  - audiences:developers

---
# Definitions

---
## What This Chapter Covers

- What "real-time" actually means
- Latency, jitter, and determinism
- Worst-case execution time
- The distinction from "fast"
- Why naive code rarely qualifies

---
## What "Real Time" Means

- A system whose correctness depends on *when* a result is delivered, not just *what* is delivered
- The right answer at the wrong time is a wrong answer
- "Fast" is *not* the same as "real time"
- A 1 GHz processor that occasionally takes 50ms to respond is unfit for many real-time tasks
- A 100 MHz processor that always responds within 10us may be fit

---
## Latency

- Time between an *event* and a *response*
- Measured at the system boundary (sensor input &#8594; actuator output)
- Includes hardware, OS, application
- Average latency hides the bad cases
- Always look at the *worst case*, not the average

---
## Jitter

- The *variation* in latency
- A system with 100us mean latency and 50us jitter is worse than one with 200us mean and 10us jitter
- Predictability often matters more than raw speed
- Jitter sources accumulate down the stack
- Reducing jitter is the central engineering challenge of RT

---
## Determinism

- Same input, same conditions &#8594; same response time, every time
- The opposite of "usually fast"
- Achievable only by being deliberate about every layer
- Off-the-shelf desktop OSes are *non-deterministic* by design (favour throughput)
- Real-time OSes (RTOS) are deterministic by design (favour predictability)

---
## Worst-Case Execution Time (WCET)

- The maximum time a piece of code can take, under all valid inputs
- For RT systems, this is what matters — not the average
- Hard to compute analytically; usually estimated empirically + safety margin
- Tools and techniques exist (static WCET analysis), but they require discipline
- "It usually finishes in 1ms" is *not* a WCET

---
## Real-Time Is Not Speed

- A system delivering 10ms responses is real-time *if* it always does
- A system delivering 1ms responses average but occasionally 100ms is *not*
- This is the most common misunderstanding
- Game engines aren't typically real-time (frame drops are tolerated)
- Pacemakers, anti-lock brakes, audio synthesis are real-time

---
## Real-Time Examples

- Aircraft flight control
- Anti-lock brakes
- Industrial robotics
- Audio synthesis (200us-1ms budget)
- Software-defined radio
- High-frequency trading (sub-microsecond)
- Each has a *deadline* the system must meet

---
## Hard, Soft, Near

- **Hard**: missing a deadline = system failure (medical, automotive)
- **Soft**: missing a deadline degrades quality (video, voice)
- **Near** (firm): missed result is useless but not catastrophic (frame drop)
- Different engineering disciplines for each
- Most real-world systems are mixed

---
## What Naive Code Lacks

- Bounded execution time
- No dynamic memory allocation in hot paths
- No blocking syscalls without bounded wait
- Predictable thread scheduling
- Awareness of cache, TLB, branch prediction effects
- All this needs to be *designed in*, not discovered

---
## Vocabulary

- **Deadline**: when a response must be delivered
- **Period**: how often a task must run
- **Slack**: time between completion and deadline
- **Schedulable**: a task set that meets all deadlines under analysis
- These terms appear constantly in RT literature

---
## What This Course Will Do

- Define types of RT systems precisely
- Walk through the OS-level mechanisms
- Identify all the latency sources
- Cover memory, scheduling, locking, logging
- Each chapter ends with measurement and observation techniques
- Aim: build the intuition to design a system that meets a deadline reliably

---
## Common Misuses of the Term

- "Real-time analytics" usually means "fresh", not RT
- "Real-time chat" usually means "low latency", not RT
- "Real-time dashboard" — almost never RT
- The marketing department has captured the term
- In this course, we mean it literally

---
## A Litmus Test

- Can you state the deadline?
- Can you measure WCET against it?
- Will the system fail in some defined way if missed?
- If yes to all three: it's real-time
- Otherwise: it's just fast

---
## Common Mistakes

- Confusing average latency with worst-case
- Designing for the *typical* case, ignoring the tail
- Believing a desktop OS will deliver hard real-time
- Underestimating the complexity of doing RT well
- Adding "real-time" to project requirements without thinking through what it means
