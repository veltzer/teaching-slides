---
tags:
  - concepts:architecture
  - concepts:resiliency
level: intermediate
category: architecture
audience:
  - audiences:developers

---

# Factor IX: Disposability

---

## The Rule

- Maximize robustness with fast startup and graceful shutdown
- Processes should be disposable — start fast, die safely
- Sudden termination is normal, not exceptional

---

## Process Lifecycle

![process_lifecycle](svg/courses/architecting/twelve-factor-app/10_disposability/process_lifecycle.svg)

---

## Fast Startup

- The process should be ready to serve in seconds, not minutes
- Slow startup makes scaling sluggish and deploys risky
- Pre-warm what you can; defer what you can defer
- Aim for under 30 seconds; 5 seconds is excellent

---

## Why Fast Startup Matters

- Autoscaling fires when load spikes; new processes need to absorb load **now**
- Rolling deploys: each new process must be ready before the next replaces
- Crash recovery: a slow restart is a long outage
- Local development: developers restart constantly

---

## Graceful Shutdown

- Receive a signal (typically SIGTERM)
- Stop accepting new work
- Finish in-flight work
- Release resources (connections, locks, file handles)
- Exit cleanly

---

## Signal Handling

```python
import signal, sys

def shutdown(signum, frame):
    print("draining requests...", flush=True)
    server.shutdown()
    print("flushing connections...", flush=True)
    db.close()
    sys.exit(0)

signal.signal(signal.SIGTERM, shutdown)
```

- Handle SIGTERM explicitly
- Don't ignore it; default exit on SIGTERM might leave work undone

---

## Drain Period

- The platform sends SIGTERM and waits a grace period (e.g., 30 seconds)
- The process must finish in-flight work in that window
- After the grace period, the platform sends SIGKILL — no more chances
- Design work to fit in the drain window

---

## Crash-Only Design

- The process should behave correctly even if it dies abruptly
- Persistent state must be transactional (no half-written records)
- Background work must be checkpointed so it can resume
- "Did the process exit cleanly?" should not affect correctness

---

## Implications for Long-Running Work

- Long jobs must checkpoint progress
- A killed worker should be replaceable; the job continues from the last checkpoint
- Without this, every deploy or scale-down loses partial work

---

## Implications for Connections

- Connection pools should detect closed connections and reconnect
- Don't assume the database connection survives across all events
- Don't hold locks longer than necessary; a sudden death will release them only after a timeout

---

## Anti-Patterns

- 5-minute startup because a cache must warm before serving
- Ignoring SIGTERM
- Long-running tasks with no checkpoint
- "It only works after a clean shutdown"
- Holding locks across sleep cycles

---

## Container Implications

- Containers are killed regularly: rolling deploys, autoscaling, node failures
- Disposability is a survival trait
- A container that takes 60 seconds to start fights against every container orchestration platform

---

## Summary

- Start fast, stop cleanly, survive sudden death
- Handle SIGTERM, drain in-flight work, exit
- Checkpoint long work; don't trust the process to live to the end
- Disposability is what makes "cattle, not pets" feasible
