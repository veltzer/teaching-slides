---
tags:
  - concepts:architecture
  - concepts:scalability
level: intermediate
category: architecture
audience:
  - audiences:developers
  - audiences:architects

---

# Factor VI: Processes

---

## The Rule

- Execute the app as one or more stateless processes
- Share-nothing between processes
- Persistent data lives in backing services, not in the process

---

## What "Stateless" Means

- The process holds no data across requests that another process couldn't reproduce
- Local memory is fine for the duration of a single request
- Anything longer-lived is in a backing service (database, cache, blob store)
- A process can be killed and replaced without data loss

---

## Why Stateless Processes

- Horizontal scaling by adding more processes works without coordination
- Failover is trivial: kill, replace, continue
- Updates are rolling restarts, not migrations
- Operations like "drain a node" are safe by default

---

## Sticky Sessions Are an Anti-Pattern

- Sticky sessions = a load balancer routes a user always to the same process
- The user's data is in that one process's memory
- If the process dies, the user's data is gone
- Sticky sessions exist because the app violated factor VI

---

## Where State Goes

- **User session**: in a session store (Redis, database, encrypted cookie)
- **Cached computation**: in a shared cache (Redis, Memcached)
- **Files uploaded**: in object storage (S3, Blob)
- **Long-running computation**: in a job queue with persistent state
- The process is a transient computer

---

## A Stateless Process Diagram

![stateless_process](svg/courses/architecting/twelve-factor-app/07_processes/stateless_process.svg)

---

## In-Memory Caches

- Local in-memory caches are fine if invalidation is correct
- Each process has its own; no coordination needed
- The cache is a performance optimization, not a source of truth
- A cold cache after restart is a slowdown, not a bug

---

## Disk Should Be Treated as Ephemeral

- The local filesystem outlives the process slightly, but not reliably
- A new release replaces the disk
- Containers explicitly delete the disk on restart
- Persistent state goes to a backing service, not local disk

---

## Anti-Patterns

- Storing user uploads in `/var/www/uploads/`
- In-process session storage that breaks on restart
- "Background processing" that loses queue state if the process dies
- Singleton state that requires only one process to exist

---

## When the App Has State

- Some apps are inherently stateful (databases, message brokers)
- These should be treated as backing services for everything else
- They follow different design rules — twelve-factor doesn't apply directly
- The line: most application code can be stateless; storage is a separate problem

---

## Summary

- Process = one or more stateless workers
- State lives in backing services
- Restart, scale-out, failover all become trivial
- Sticky sessions and local persistent files are violations
