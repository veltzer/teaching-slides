---
tags:
  - infrastructure:real-time
  - infrastructure:timing
level: advanced
category: real-time
audience:
  - audiences:embedded-engineers
  - audiences:developers

---
# Measuring Time

---
## What This Chapter Covers

- Hardware time sources: TSC, HPET, ARM Generic Timer
- Wall-clock time vs monotonic time vs ticks
- Resolution, accuracy, precision
- POSIX timing APIs
- Measuring code path durations
- Avoiding measurement bias

---
## Why Measuring Time Is Hard

- Multiple time sources, each with their own quirks
- Wall-clock time can jump (NTP adjustments, leap seconds)
- Monotonic time doesn't, but doesn't track real-world time
- High-resolution times have caveats
- Knowing which to use is the first skill

---
## Hardware Time Sources (x86)

- **TSC (Time Stamp Counter)**: a 64-bit counter that ticks at CPU clock rate
- Cheap to read (one instruction), high resolution
- Modern CPUs: invariant TSC across power states, frequency changes
- Older systems: TSC could drift across cores; not anymore on modern hardware
- The default high-res clock on Linux x86

---
## Hardware Time Sources (ARM)

- ARM Generic Timer: a system-level counter, accessible from any privilege level
- Reliable, monotonic, well-specified
- The ARM equivalent of TSC done right from the start
- Used by all modern ARMv8 systems
- What CLOCK_MONOTONIC reads on aarch64 Linux

---
## Other Sources

- **HPET (High Precision Event Timer)**: x86 platform timer, ~10 MHz
- **APIC timer**: per-CPU local timer, used for kernel scheduling
- **PIT**: legacy programmable interval timer (8254 chip), ~1.2 MHz
- Modern systems prefer TSC; HPET is fallback
- The kernel picks the best available

---
## Wall-Clock Time

- "What time is it in the world?"
- Source: NTP, GPS, sometimes manual
- Can jump backward (clock corrections, daylight savings, leap seconds)
- POSIX: `clock_gettime(CLOCK_REALTIME, ...)`
- Use for: timestamps, scheduled events tied to wall time

---
## Monotonic Time

- Counts time since some arbitrary point (boot, often)
- Never goes backward
- Doesn't track wall-clock corrections
- POSIX: `clock_gettime(CLOCK_MONOTONIC, ...)`
- Use for: measuring durations between events

---
## CLOCK_MONOTONIC_RAW

- Like CLOCK_MONOTONIC but unaffected by NTP slewing
- Slewing: NTP gradually adjusts the clock rate to converge on accurate time
- For purest "elapsed time" measurement
- Linux-specific
- Use when you want raw CPU-rate ticks

---
## CLOCK_PROCESS_CPUTIME_ID

- Time the *current process* spent on CPU
- Excludes time spent waiting (sleeping, blocked on I/O)
- Useful for measuring code path time without scheduling noise
- Per-thread variant: `CLOCK_THREAD_CPUTIME_ID`
- Powerful for performance work

---
## Resolution vs Accuracy vs Precision

- **Resolution**: smallest distinguishable time unit (1 ns? 1 us?)
- **Accuracy**: how close to true time
- **Precision**: how repeatable the measurement
- High resolution doesn't imply high accuracy
- A 1 ns resolution on a clock that drifts 1 ms/hour is misleading

---
## POSIX Timing API

```c
#include <time.h>
struct timespec ts;
clock_gettime(CLOCK_MONOTONIC, &ts);
// ts.tv_sec  : seconds
// ts.tv_nsec : nanoseconds within the current second
```

- The standard cross-Unix API
- Nanosecond resolution; nanosecond accuracy on modern systems
- Returns 0 on success, -1 on error
- Available on Linux, macOS, BSDs

---
## Measuring a Code Path

```c
struct timespec t0, t1;
clock_gettime(CLOCK_MONOTONIC, &t0);
do_work();
clock_gettime(CLOCK_MONOTONIC, &t1);

long ns = (t1.tv_sec - t0.tv_sec) * 1000000000L
        + (t1.tv_nsec - t0.tv_nsec);
```

- Bracket the work with two reads
- Subtract; convert to a unit you care about
- Run many times for distribution, not single sample

---
## Histograms, Not Means

- A single mean hides the worst case
- Plot a histogram: log y-axis, fine x bins
- Look for: shape, tail, modes
- Tools: HdrHistogram, custom bucketed counters
- This view tells the truth that means hide

---
## Beware of Optimisations

- The compiler may reorder around your timing reads
- Use compiler barriers (`asm volatile("" ::: "memory")`)
- Or use atomic operations with sequential consistency
- Otherwise the measured code may not be what you wrote
- Compiler intrinsics may also matter on the CPU side

---
## Measurement Overhead

- `clock_gettime` itself takes nanoseconds
- For very short code paths, overhead matters
- Subtract the measurement overhead, or use a coarser measurement
- vDSO (virtual dynamic shared object) makes Linux's clock_gettime fast — no syscall
- On older systems or unusual configs, expect microseconds

---
## Measuring Distributions

- Run the operation 10000+ times
- Sort the times
- Report p50, p95, p99, p99.9, max
- Max often dominates the truth
- Aim for: tight distribution, low p99.9, low max

---
## Common Mistakes

- Using `time()` (1-second resolution) for sub-second work
- Measuring once and trusting the number
- Forgetting that `gettimeofday` returns wall time (can jump)
- Measuring on an idle system; getting deceptively good numbers
- Ignoring measurement overhead in tight loops
