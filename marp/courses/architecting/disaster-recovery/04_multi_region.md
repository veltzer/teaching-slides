---
tags:
  - architecting:patterns
  - practices:reliability
level: intermediate
category: architecting
audience:
  - audiences:architects
  - audiences:devops

---

# Multi-Region

---

## What This Chapter Covers

- Why multi-region
- Topologies
- Data consistency
- Failover
- Cost

---

## Why Multi-Region

- Region-level outage survival
- Geographic latency
- Regulatory residency
- Compliance with sovereignty

---

## Topologies

- Active-passive
- Active-active
- Read-local, write-global
- Sharded by region

---

## Failover Modes

![failover_modes](svg/courses/architecting/disaster-recovery/04_multi_region/failover_modes.svg)

---

## Read-Local, Write-Global

- Reads local, fast
- Writes funnel to a primary
- Failover requires election
- Common with managed databases

---

## Active-Active

- Writes accepted in any region
- Conflict resolution required
- Best for partition tolerance
- Hardest to operate

---

## Conflict Resolution

- Last writer wins
- CRDTs
- Application-defined merges
- Avoid where consistency matters

---

## Latency Trade-offs

- Sync replication adds RTT
- Async replication risks loss
- Eventual consistency leaks to users
- Test from real client locations

---

## Failover Mechanics

- Detect failure
- Promote secondary
- Reroute traffic
- Reconcile conflicts after

---

## DNS-Based Failover

- Health-checked routes
- TTL matters
- Some clients ignore TTL
- Pair with client retry logic

---

## Network Path

- Inter-region links
- Use private backbone if available
- Encrypt regardless
- Plan for jitter

---

## Stateful Services

- Caches per region
- Queues per region
- Cross-region replication is hard
- Idempotent producers required

---

## Data Residency

- Pin user data to a region
- Tag data by jurisdiction
- Block cross-region replication where required
- Audit access logs

---

## Cost

- Egress dominates
- Duplicated capacity
- Tooling complexity
- Engineering time

---

## Common Multi-Region Mistakes

- Cache coherence ignored
- DNS TTL too long
- Async replica treated as zero loss
- Untested failback
- Manual steps in failover
