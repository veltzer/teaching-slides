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
# Factor VIII: Concurrency

---
## The Rule

- Scale out via the process model
- Different process types handle different workloads
- Adding capacity = adding more processes

---
## Process Types

![concurrency_via_processes](svg/courses/architecting/twelve-factor-app/09_concurrency/concurrency_via_processes.svg)

---
## The Process Model

- Each process is a unit of horizontal scaling
- Add load? Run more processes
- Need parallelism? Multiple processes do the same job
- The OS schedules them; no orchestration needed inside the app

---
## Process Types

- A web app might have: `web`, `worker`, `scheduler`, `migration`
- Each type is a separate process (or set of processes)
- Each type scales independently
- Different concurrency rules per type

---
## Examples

- `web`: handles HTTP requests; scales with traffic
- `worker`: processes background jobs; scales with queue depth
- `scheduler`: triggers periodic tasks; usually single-instance
- The Procfile (Heroku-style) declares process types

---
## Procfile Example

```yaml
web: gunicorn app:app
worker: python worker.py
scheduler: python scheduler.py
```

- Each line is a process type
- The platform runs one or more instances of each
- Scaling = changing the count

---
## Within a Process

- Processes themselves can be threaded, async, or use event loops
- Internal concurrency is fine and often necessary
- But it doesn't replace horizontal scaling — single-process bottlenecks remain
- Threads ≠ processes; the factor is about processes

---
## Scaling By Process Type

![scaling_axes](svg/courses/architecting/twelve-factor-app/09_concurrency/scaling_axes.svg)

---
## Horizontal Scaling Patterns

- Stateless processes (factor VI) make horizontal scaling work
- Load balancer in front, N processes behind
- Add a process: load redistributes
- Remove a process: requests drain naturally

---
## Workload Diversity

- HTTP requests need fast response, low latency
- Background jobs need throughput, can take seconds-minutes
- Scheduled tasks need only one runner at a time
- Different workloads → different process types → different scaling profiles

---
## Container Orchestration

- Kubernetes Deployments map onto process types
- Each Deployment scales independently (replica count)
- HPA (Horizontal Pod Autoscaler) adjusts count based on load
- The factor maps cleanly onto K8s primitives

---
## Anti-Patterns

- One process trying to do everything (web + worker + scheduler in one)
- Vertical scaling instead of horizontal — bigger machine, same one process
- Internal scheduling logic instead of process-level orchestration
- Using sticky sessions to avoid horizontal scaling complexity

---
## Summary

- Concurrency = adding more processes
- Different process types for different workloads
- Internal concurrency (threads, async) is complementary, not a substitute
- Stateless processes make horizontal scaling cheap and safe
