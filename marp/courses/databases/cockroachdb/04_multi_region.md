---
tags:
  - databases:cockroachdb
level: intermediate
category: databases
audience:
  - audiences:developers
  - audiences:dba

---
# Multi-Region

---
## What This Chapter Covers

- Multi-region setup
- Survival goals
- Table localities
- Latency planning
- Trade-offs

---
## Why Multi-Region

- Survive a region outage
- Lower latency for global users
- Data residency requirements
- Compliance with sovereignty

---
## Setting It Up

- Add nodes in multiple regions
- Tag each node with region
- Set survival goal at database level
- Choose locality per table

---
## Survival Goals

- Zone: tolerate zone loss
- Region: tolerate region loss
- Region survival costs more replicas
- Document the choice

---
## Table Localities

- Regional by row
- Regional by table
- Global
- Each suits a pattern

---
## Locality Choices

![locality_choices](svg/courses/databases/cockroachdb/04_multi_region/locality_choices.svg)

---
## Localities Compared

![table_localities](svg/courses/databases/cockroachdb/04_multi_region/table_localities.svg)

---
## Regional By Row

- Each row pinned to a region
- Reads and writes local to home region
- Cross-region rare
- Common for user-owned data

---
## Regional By Table

- Whole table pinned to one region
- Reads outside slower
- Simple to reason about
- Suits region-specific data

---
## Global Tables

- Reads everywhere with bounded staleness
- Writes coordinate across regions
- Suit reference data
- Higher write latency

---
## Latency Planning

- Local writes within region
- Quorum across replicas adds RTT
- Cross-region reads vs follower reads
- Map every query

---
## Failure Behaviors

- Zone outage: continues
- Region outage: continues if region survival set
- Network partition: AP behavior is not the default
- Test each scenario

---
## Cost

- More replicas, more storage
- Cross-region traffic egress
- Longer p99 on writes
- Worth it for tier-1 data

---
## Hybrid Patterns

- Some tables global
- Most regional
- Per-tenant pinning
- Document the policy

---
## Disaster Recovery

- Backups still required
- Multi-region replication is not backup
- Test restores
- Practice failover

---
## Common Multi-Region Mistakes

- One region in production
- Wrong locality per table
- Cross-region for chatty workloads
- No follower reads where they would help
- Untested region failover
