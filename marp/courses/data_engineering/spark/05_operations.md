---
tags:
  - data-and-ai:big-data
level: intermediate
category: data-engineering
audience:
  - audiences:data-engineers

---

# Operations

---

## What This Chapter Covers

- Cluster managers
- Submitting jobs
- Resource policies
- Logging
- Cost

---

## Cluster Managers

- Kubernetes is now common
- YARN still used in legacy
- Standalone for small setups
- Cloud platforms abstract many

---

## Submitting Jobs

- spark-submit
- Pre-built jars or python files
- Configurations as flags
- Or via APIs in platforms

---

## Configuration Sources

- Defaults
- spark-defaults.conf
- spark-submit flags
- Code-set values

---

## Resource Policies

- Cores and memory per executor
- Dynamic allocation
- Min and max executor counts
- Match to cluster

---

## Allocation Layout

![resource_allocation](svg/courses/data_engineering/spark/05_operations/resource_allocation.svg)

---

## Dynamic Allocation

- Add executors under load
- Release when idle
- Saves money on multi-tenant
- Watch shuffle service interactions

---

## Logging

- Driver logs
- Executor logs
- Aggregate to central store
- Searchable

---

## Spark UI

- Real-time job view
- Stage and task detail views
- Shuffle and storage details
- Persist as event logs

---

## History Server

- Replays event logs
- Inspect post-mortem jobs
- Required in production
- Storage for event logs

---

## Failures and Retries

- Tasks retry by default
- Stage retries on data loss
- Driver fails the whole job
- Use job-level orchestrator for retries

---

## Multi-Tenant

- Separate queues
- Per-team quotas
- Tag jobs for chargeback
- Watch for noisy neighbors

---

## Security

- Encrypt at rest
- Encrypt in transit
- Authentication via Kerberos or OAuth
- Least-privilege roles

---

## Cost Levers

- Right-size executors
- Spot instances for fault-tolerant batch
- Shorter retention for shuffle data
- Tag and report

---

## Capacity Planning

- Profile real workloads
- Track peak concurrency
- Headroom for spikes
- Rebalance quarterly

---

## Common Operational Mistakes

- One configuration for all jobs
- No history server
- No tagging for cost
- Spot instances for time-critical jobs
- Driver memory too small
