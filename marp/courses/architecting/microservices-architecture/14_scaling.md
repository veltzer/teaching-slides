---
tags:
  - concepts:microservices
  - concepts:scalability
level: intermediate
category: architecture
audience:
  - audiences:developers
  - audiences:architects

---
# Scaling Microservices

---
## Why Microservices Help With Scale

- Each service scales independently
- Hot paths get more replicas; cold paths stay small
- Teams scale: more people working in parallel without stepping on each other
- Tech: pick the right tool per service

---
## Scaling Axes

![scaling_axes](svg/courses/architecting/microservices-architecture/14_scaling/scaling_axes.svg)

---
## Horizontal vs Vertical

- **Horizontal**: more instances of the same service
- **Vertical**: bigger machine for one instance
- Horizontal is the default; vertical hits ceilings
- Stateless services scale horizontally trivially (twelve-factor)

---
## Autoscaling

- The platform scales replicas based on load
- Triggers: CPU, memory, request rate, queue depth, custom metrics
- Up: add replicas when load grows
- Down: remove replicas when load shrinks
- Kubernetes HPA is the typical tool

---
## Scaling Reads vs Writes

- Reads: scale horizontally easily (more replicas, more cache)
- Writes: harder; usually one writer per partition
- For reads at scale: read replicas, projections, caches
- For writes at scale: partition by key, accept eventual consistency

---
## Database Scaling

- Per-service databases scale per service
- Read replicas for read-heavy services
- Sharding for write-heavy services
- Or: switch to a database designed for scale (DynamoDB, Cassandra)

---
## Caching Strategies

- Per-service caches: Redis, Memcached
- Per-instance in-memory caches for hot reads
- CDN for static and semi-static responses
- See Architecture Patterns ch 10 (caching) for depth

---
## Backpressure

- A service overloaded: rejects work or slows down upstream
- Without backpressure: queues grow, latency explodes, cascade failures
- Tools: rate limiting, queue depth alarms, circuit breakers
- The signal travels upstream so the source slows down

---
## Async for Scale

- Replace synchronous calls with messages where possible
- Producers don't wait; consumers process at their own rate
- Spikes absorbed by the queue
- Trades immediacy for throughput

---
## Partitioning Data

- Split data by a key (user id, region, customer id)
- Each partition is independent; lives on its own node
- Cross-partition queries are harder; design to avoid them
- The pattern is the same for databases and message brokers

---
## Sharding Trade-Offs

- Shard key choice is critical and hard to change
- "Hot shards" if traffic is uneven
- Resharding is expensive
- Pick a key with good cardinality and even distribution

---
## Geographic Scaling

- Multi-region deployment
- Each region serves nearby users
- Data either replicated globally or partitioned by region
- Failover between regions: complex but feasible

---
## Capacity Planning

- Measure current load and growth rate
- Project: when will the current capacity be insufficient
- Add capacity ahead of need
- Don't autoscale alone — set bounds

---
## Cost vs Performance

- More replicas = higher cost
- Optimize per service: which ones need the most
- Right-sizing: not too small (latency), not too large (waste)
- Run cost reports per service; teams own the line item

---
## Anti-Patterns

- Premature scaling: 50 services for an MVP
- "Scale by adding caches" without invalidation strategy
- Autoscaling with no upper bound (cost runaway)
- Hot single instances that become bottlenecks
- Sharding before measuring whether it's needed

---
## Course Recap

- 14 chapters covering: principles, decomposition, communication, data, deployment, observability, composition, and scaling
- Microservices are not the only architecture; they're one of several valid choices
- Done right: independent teams, independent scaling, clear ownership
- Done wrong: distributed monolith with all the costs and none of the benefits

---
## Where to Go Next

- Pick one capability in your system
- Extract it via the strangler fig pattern
- Apply the principles from this course
- Measure operational impact; iterate
- Don't try to "go microservices" all at once

---
## Summary

- Horizontal scaling is the default; per-service granularity is the win
- Autoscaling on the right metric; bounds matter
- Reads scale easily; writes need partitioning
- Async absorbs spikes
- Capacity planning beats reactive scaling
