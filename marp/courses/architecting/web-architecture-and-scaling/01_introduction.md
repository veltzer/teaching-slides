---
tags:
  - architecting:patterns
  - practices:scalability
level: intermediate
category: architecting
audience:
  - audiences:architects

---
# Introduction to Web Architecture and Scaling

---
## What This Chapter Covers

- What web architecture means
- Vertical vs horizontal scaling
- Request lifecycle
- Capacity vs reliability
- Course outline

---
## What Web Architecture Is

- Layers serving HTTP
- Stateless and stateful tiers
- Edge to origin path
- Concerns at each layer

---
## The Tier Model

- Edge cache
- Load balancer
- Application
- Cache
- Database

---
## Layers Visualized

![web_layers](svg/courses/architecting/web-architecture-and-scaling/01_introduction/web_layers.svg)

---
## Request Lifecycle

- Client to DNS
- DNS to nearest edge
- Edge to load balancer
- Load balancer to app
- App to data

---
## Vertical Scaling

- Bigger machine
- Simple, expensive
- Hits hardware ceiling
- Fast remediation

---
## Horizontal Scaling

- More machines
- Stateless first
- Load balancer required
- Cheaper per unit at scale

---
## Scale Axes

![scale_axes](svg/courses/architecting/web-architecture-and-scaling/01_introduction/scale_axes.svg)

---
## Stateless vs Stateful

- Stateless is easy to scale
- State pushes to a few systems
- Cache, queue, database
- These are the bottlenecks

---
## Capacity vs Reliability

- Capacity: handle load
- Reliability: keep handling under failure
- Both need redundancy
- Plan together

---
## Latency Budgets

- End-to-end target
- Slice across hops
- Each hop has variance
- p99 dominates user experience

---
## Cost Curve

- Capacity is linear
- Reliability is super-linear
- Engineering time is the hidden cost
- Set targets explicitly

---
## Why It Is Hard

- State must live somewhere
- Failure is constant
- Coordination is expensive
- Caching is correctness-sensitive

---
## Course Outline

- Load balancing
- Caching
- Database scaling
- Async patterns
- Observability

---
## Common Beginner Mistakes

- Scaling app before measuring DB
- Caching without invalidation plan
- Sticky sessions everywhere
- Ignoring p99
- One zone deployment
