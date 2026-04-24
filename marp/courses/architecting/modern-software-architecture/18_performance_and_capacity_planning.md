---
tags:
  - concepts:architecture
  - concepts:performance
  - concepts:capacity-planning
level: advanced
category: architecture
audience:
  - audiences:developers
  - audiences:architects

---
# Performance and Capacity Planning

---
## Why Architects Own Performance

- Performance and cost are two sides of the same coin
- A 10× performance problem is an architectural problem, not an optimization problem
- Capacity decisions made at design time constrain the system for years
- Teams that skip capacity planning discover limits only at peak traffic

---
## Performance Vocabulary

- **Latency** — time to serve one request
- **Throughput** — requests served per unit time
- **Concurrency** — requests in flight simultaneously
- **Utilization** — fraction of capacity in use
- **Saturation** — queue depth beyond the capacity

Do not conflate latency with throughput — they trade against each other.

---
## Little's Law

`L = lambda * W`

- **L** — average number of requests in the system (concurrency)
- **lambda** — arrival rate (throughput)
- **W** — average time in the system (latency)

Example: 1000 req/s × 0.1s average latency = 100 concurrent requests in flight.
Useful for sanity-checking capacity numbers in seconds.

---
## Latency vs Throughput Trade-Off

- More concurrency can raise throughput but queues up latency
- Adding servers raises throughput linearly only if the work is independent
- Shared resources (database, cache) cap throughput regardless of server count
- Batch processing sacrifices latency for throughput

---
## Percentiles, Not Averages

- Average latency hides the bad experiences
- Report p50, p95, p99, p999
- A 1% tail latency of 5 seconds means 1 in 100 users sees 5 seconds
- At microservice fan-out of 10, p99 at each service becomes p90 overall

---
## Tail Latency Amplification

- User request fans out to N backend calls
- Overall latency is driven by the slowest of N — tail of tail
- 10-way fan-out turns a 1% tail into a 10% overall experience
- Fight with hedging, parallelism, and aggressive timeouts on non-critical paths

---
## The USE Method

For resources (CPU, memory, disk, network):

- **Utilization** — percentage of capacity in use
- **Saturation** — how much work is queued beyond capacity
- **Errors** — failed operations on the resource

Walk through each resource in USE order when diagnosing performance.

---
## The RED Method

For services:

- **Rate** — requests per second
- **Errors** — percentage of requests failing
- **Duration** — latency distribution

Track RED per service; track USE per host/pod.

---
## Back-of-Envelope Capacity

- Expected peak requests per second (RPS)?
- Requests per second one instance handles?
- Required instances = peak RPS ÷ per-instance RPS × safety factor
- Add headroom for growth, deployment, and burst

A 10-minute calculation saves a 10-day overrun.

---
## Example: Sizing a Service

- 1M daily active users
- Average 50 requests per user per day → 50M req/day
- Peak-to-average ratio 4× → peak ~2300 req/s
- Each instance handles 200 req/s → 12 instances
- Plus 50% headroom = 18 instances
- Plus rolling update surge = 20 instances

---
## Cost Modeling

- Compute cost per 1M requests
- Storage cost per GB per month
- Egress cost per GB (often the surprise line item)
- Managed service markup (RDS, DynamoDB, etc.)
- Cost must be a first-class metric, not a quarterly surprise

---
## Load Testing Workflow

- Start with a realistic workload model (not random traffic)
- Use production logs to build request mix
- Ramp gradually; observe break point
- Test the dependencies too, not just the service you own
- Tools: `k6`, `Gatling`, `Locust`, `wrk2`, `JMeter`

---
## Soak Testing

- Run moderate load for hours or days
- Catches memory leaks, connection pool exhaustion, log rotation bugs
- A system that passes 10-minute load can still fall over after 6 hours
- Production is a soak test you're running on your users

---
## Stress and Spike Testing

- **Stress** — push beyond expected load to find the breaking point
- **Spike** — sudden bursts (2× to 10× normal) to test elasticity
- Verify graceful degradation — rate limiting, circuit breakers, queue shedding
- The goal is not to survive unlimited load; it is to fail predictably

---
## Identifying Bottlenecks

- Profile under load, not in isolation
- Suspect the usual: database, network, serialization, locks
- Look for utilization approaching 100% on any single resource
- Queue length is the earliest warning sign of saturation

---
## The Database Is Usually the Bottleneck

- Stateless services scale horizontally cheaply
- The database does not
- Watch for: connection pool saturation, lock waits, slow queries, write amplification
- Caching layers shift but do not eliminate database load

---
## Caching: When and Where

- Identify reads with high rate and low change frequency
- Cache close to the reader (client → CDN → edge → service → DB)
- Set TTLs explicitly; avoid "infinite" caches
- Invalidation is genuinely hard — design for staleness when possible

---
## Cache-Hit Math

- Cache hit ratio 95% means 5% of traffic still hits the origin
- If DB can only handle 20% of peak, 5% of 5× peak = 25% — still overloaded
- Headroom on origin matters even with a "good" cache
- Thundering herd on cache expiry can break origin anyway

---
## Connection Pool Sizing

- Too small — requests queue behind connections; latency spikes
- Too large — database runs out of worker slots; everyone degrades together
- Rule of thumb: pool size ≈ DB max connections / number of service instances × 0.8
- Always monitor pool utilization and wait time

---
## Tail Latency Mitigation

- **Hedged requests** — send to two instances, use the first response
- **Adaptive timeouts** — fail fast on slow instances
- **Connection warm-up** — avoid first-request penalties
- **Load balancer least-loaded** — avoid sending to the slow one
- **Priority queueing** — user-facing work ahead of background work

---
## Autoscaling Done Right

- Scale on leading indicators (queue depth, in-flight requests), not CPU alone
- Scale-out faster than scale-in to absorb spikes
- Pre-scale before known events (sales, launches, business hours)
- Beware the cold-start cost — new instances take time to be useful

---
## Capacity Planning Cadence

- Refresh capacity model quarterly or before known events
- Revisit after any architectural change
- Include downstream dependencies — your scale is their load
- Share the numbers with product; demand drives capacity

---
## Performance Testing as a Gate

- CI job: run a representative load test on every release candidate
- Fail the build on latency regressions beyond tolerance
- Store historical results; watch trends, not just this run
- Budget-based testing: reject changes that spend more than the performance budget

---
## SLOs as Capacity Anchors

- Latency SLO (p99 < 200ms) sets the capacity target
- Error budget ties reliability to release pace
- Capacity model must support SLO at peak with headroom
- If SLO is unachievable within cost constraints, architecture is the answer

---
## Common Performance Mistakes

- **Averaging percentiles** — p95 of averages is meaningless
- **Testing in isolation** — production has noisy neighbors
- **Ignoring cold start** — serverless and autoscaling both suffer
- **Premature optimization** — measure before tuning
- **No capacity math** — "we'll scale when we need to" is a post-mortem in waiting

---
## Summary

- Little's Law ties latency, throughput, and concurrency with one equation
- Measure percentiles, not averages; the tail is the user experience
- USE for resources, RED for services — two dashboards, always
- Back-of-envelope sizing beats gut-feel capacity decisions
- Load, stress, spike, and soak tests each expose a different class of bug
- Caching moves bottlenecks; it does not eliminate them
- Capacity and cost are the same conversation — own both as the architect
