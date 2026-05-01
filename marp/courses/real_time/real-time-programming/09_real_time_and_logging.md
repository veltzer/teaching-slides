---
tags:
  - infrastructure:real-time
  - infrastructure:logging
level: advanced
category: real-time
audience:
  - audiences:embedded-engineers
  - audiences:developers

---
# Real-Time and Logging

---
## What This Chapter Covers

- Why naive logging breaks RT
- The cost of writing to files
- Async logging
- Shared-memory logging
- Trade-offs of each approach
- Practical patterns

---
## Why Logging Is Dangerous

- A `printf` looks innocent
- Reality: format string parsing, malloc, stdio buffer, syscall, possible block on stdout
- Worst case: tens of milliseconds
- Logging is *the* most common cause of missed deadlines
- A debug log added "just to investigate" can break the system

---
## What printf Does

- Parses the format string
- May allocate temporary buffers
- Writes to stdout (a global, locked stream)
- Stdout flushes (usually line-buffered) &#8594; write syscall
- Write may block on file I/O
- Each step has unbounded worst case

---
## Cost of File Writes

- Filesystem journals (ext4, xfs): write may trigger journal commit
- Buffer flushes: synchronous when full
- fsync: always blocks
- Logs to NFS: network round trip
- Logs to slow storage (SD card): tens of milliseconds typical

---
## The Naive Solution: Just Don't Log

- Tempting; usually wrong
- Without logs, you can't diagnose what went wrong
- Real RT systems need logging *for the post-mortem*
- The challenge is: log without breaking the deadline
- Answer: defer the I/O

---
## Async Logging

- Log call: write to a buffer; *don't* do I/O
- Background thread: drains the buffer to disk
- Foreground thread: bounded, fast operation
- Background thread can be lower-priority
- Pattern used by every serious RT logging library

---
## Async Logging in Code

```c
// Producer (RT thread)
log_event(LOG_INFO, "event %d at %lld", id, ts);

// log_event:
//   formats into a fixed-size record
//   atomic-pushes to a ring buffer
//   returns immediately
//
// Consumer (background thread):
//   pops records from the ring buffer
//   formats and writes to disk
```

---
## The Ring Buffer

- Pre-allocated, fixed size
- Single writer, single reader (lock-free) for one RT thread
- Multi-producer, single-consumer for multiple RT threads
- Bounded — old records overwrite new (or drop) when full
- The producer never blocks

---
## What If The Buffer Fills

- Two strategies:
    - **Overwrite**: lose oldest records
    - **Drop**: lose newest records
- Overwrite is simpler; drop preserves history at the cost of recent context
- Pick based on what's more useful in a post-mortem
- Either way: instrument the drop count

---
## Shared-Memory Logging

- Producer writes to a memory region shared with another process
- Consumer process reads, writes to disk
- Producer never touches disk
- Consumer can crash without affecting producer
- Common in flight-control and industrial systems

---
## What's Logged Inside the Hot Path

- Numeric event codes (not strings)
- Pre-allocated buffers
- Timestamp (cheap clock_gettime)
- Minimal context: enough for offline reconstruction
- Defer formatting (sprintf, etc.) to the consumer

---
## Symbol Tables for Compactness

- "OrderPlaced(id=42, amount=199)" &#8594; "EVT_OP id=42 amount=199" &#8594; binary record
- Producer: log a binary record with an event ID and binary fields
- Consumer: lookup table maps event ID to format string
- 5x-50x smaller; faster to write
- LTTng, eBPF, kernel tracepoints all work this way

---
## Don't Log These in the Hot Path

- Strings constructed at runtime (sprintf)
- Calls to standard logging libraries (most do I/O)
- Anything that takes a lock you don't own
- Timestamps from wall-clock (NTP-jumpable)
- File operations of any kind

---
## Sample Buffer Sizes

- Hot-path ring buffer: 64 KB to 1 MB typical
- Consumer reads in batches, writes large blocks
- Background flush every few ms or on threshold
- Trade-off: bigger buffer = more lossy on crash, more expensive
- Tune based on expected event rate

---
## Logging in Linux Kernel

- printk: lock-free ring buffer
- klogd / journald reads from /dev/kmsg
- Designed for high-rate, no-loss-or-bounded-loss
- A model worth studying for user-space RT systems

---
## A Practical Pattern

- One ring buffer per CPU (no contention)
- One consumer thread aggregating across buffers
- Consumer writes to disk in large sequential blocks
- Drops are counted and surfaced as a metric
- Tested under production-like load before deployment

---
## Common Mistakes

- Calling printf in an RT thread "just for debugging"
- Using a synchronous logger and blaming the storage
- One huge mutex protecting all logging
- Not measuring the worst case under production load
- Treating dropped logs as silent failures (they should be metrics)

---
## What to Take Away

- Logging in RT is a *systems* problem, not a library config
- Ring buffer + async drain is the standard pattern
- Measure; tune; verify under realistic load
- Production debug logs are a feature, not a luxury
- Get the logging right early; it's painful to retrofit
