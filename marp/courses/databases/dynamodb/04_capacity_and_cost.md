---
tags:
  - databases:dynamodb
level: intermediate
category: databases
audience:
  - audiences:developers

---
# Capacity and Cost

---
## What This Chapter Covers

- read capacity unit and write capacity unit
- Read modes
- On-demand vs provisioned
- Auto-scaling
- Cost levers

---
## Capacity Units

- write capacity unit: writes per second of 1KB items
- read capacity unit: reads per second of 4KB items
- Strong reads cost twice
- Transactional ops cost twice

---
## Sizing

- Average and peak rates
- Bigger items cost more
- Account for retries and contention
- Reserve headroom

---
## On-Demand

- No provisioning
- Auto scales instantly within service limits
- More expensive per request
- Best for unpredictable traffic

---
## Modes Compared

![on_demand_vs_provisioned](svg/courses/databases/dynamodb/04_capacity_and_cost/on_demand_vs_provisioned.svg)

---
## Provisioned

- Buy units up front
- Cheaper at scale
- Auto-scaling adjusts toward target utilization
- Plan for steady patterns

---
## Auto-Scaling Targets

- Aim for 70% utilization
- Allow burst overhead
- Both upper and lower bounds
- Watch alarm chatter

---
## Reserved Capacity

- One-year or three-year commits
- Big discount
- Lock in baseline
- Use on top of auto-scaling

---
## Hot Partition

- Single key absorbs traffic
- Throttles before total table limit
- Adaptive capacity helps but not always
- Re-shard via key design

---
## Item Size

- 400KB hard limit
- Larger items cost more units
- Compress JSON if needed
- Or store blob in S3 with reference

---
## Storage Cost

- Per GB month
- Includes index storage
- Sparse indexes save money
- Watch global-index sprawl

---
## Stream Cost

- Per shard hour
- Per get records
- Lambda triggers add Lambda cost
- Tune retention to needed window

---
## Backup Cost

- On-demand backups stored
- Continuous backups via PITR
- Per GB month
- Cheaper than storage of similar size

---
## Multi-Region Cost

- Replicated write capacity units
- Egress between regions
- Worth it for availability or latency
- Track per-region usage

---
## Tagging

- Tag tables and indexes
- Cost allocation reports
- Track per team or project
- Required for chargeback

---
## Common Cost Mistakes

- On-demand for steady high traffic
- No auto-scaling on provisioned
- Strongly consistent reads everywhere
- Big items uncompressed
- Many global indexes without need
