---
tags:
  - data-and-ai:data-engineering
level: intermediate
category: data-engineering
audience:
  - audiences:data-engineers

---
# Operations and Quality

---
## What This Chapter Covers

- Data quality
- Monitoring
- Alerts
- Cost
- Debugging

---
## Why Data Quality

- Bad data is worse than no data
- Decisions made on wrong inputs
- Trust takes years to rebuild
- Catch at the boundary

---
## Quality Dimensions

- Accuracy
- Completeness
- Consistency
- Timeliness
- Uniqueness

---
## Where to Check

- At ingest
- After transform
- Before publish
- In dashboards

---
## Tests as Code

- Stored next to models
- Run on every change
- Block pipeline on critical fails
- Warn on soft fails

---
## Quality Gates

![quality_gates](svg/courses/data_engineering/etl/05_operations_and_quality/quality_gates.svg)

---
## Anomaly Detection

- Volume changes
- Schema drift
- Distribution shifts
- Auto-thresholds beat fixed ones

---
## Monitoring

- Pipeline success rate
- Latency to land
- Row counts
- Resource use

---
## Dashboards

- One per pipeline
- Trend over time
- Compare to SLA
- Tag by owner

---
## Alerts

- On failures
- On SLA misses
- On quality degradation
- Route to on-call

---
## Cost

- Compute per run
- Storage per dataset
- Egress for cross-region
- Tag for chargeback

---
## Debugging

- Replay a partition
- Inspect intermediate data
- Compare runs
- Use logs and lineage

---
## Schema Changes

- Coordinate with consumers
- Backward compatibility default
- Migration plan for breaks
- Deprecate, do not delete

---
## Privacy

- Tag PII columns
- Mask in non-prod
- Honor deletion requests
- Encrypt at rest and in transit

---
## Common Operational Mistakes

- Quality checks added after incidents
- No dashboards
- No SLA
- One owner for everything
- Cost reviewed yearly
