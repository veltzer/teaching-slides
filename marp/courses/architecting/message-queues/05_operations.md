---
tags:
  - architecting:patterns
  - queues:overview
level: intermediate
category: architecting
audience:
  - audiences:architects
  - audiences:developers

---

# Operations

---

## What This Chapter Covers

- Monitoring
- Alerting
- Capacity
- Upgrades
- Multi-tenant

---

## Key Metrics

- Queue depth
- Producer rate
- Consumer rate
- Lag

---

## Lag

- Difference between produced and consumed
- Most useful single metric
- Per partition matters
- Alert thresholds by topic

---

## Lag Visualized

![lag_metrics](svg/courses/architecting/message-queues/05_operations/lag_metrics.svg)

---

## Latency

- End-to-end time
- Includes broker time
- Includes consumer time
- Track p95 and p99

---

## Error Rate

- Failed deliveries
- Failed acknowledgments
- Dead-lettered count
- Per-topic dashboards

---

## Alerts

- Lag exceeds threshold
- Queue grows unbounded
- Broker node down
- Dead-letter queue grew

---

## Capacity Planning

- Peak vs steady rates
- Disk for retention
- Network for replication
- Headroom for spikes

---

## Retention

- Time-based or size-based
- Disks fill silently
- Compaction for log topics
- Tiered storage in modern brokers

---

## Upgrades

- Rolling restart
- Mind schema compatibility
- Test on staging
- Have a rollback plan

---

## Broker Failover

- Replicas elect new leader
- Producers retry
- Consumers re-fetch
- Test it

---

## Multi-Tenant

- Per-tenant quotas
- Separate topics
- Authorization per topic
- Audit access

---

## Authentication

- Mutual TLS or username/password
- Service identities
- Rotate credentials
- Limit scope

---

## Authorization

- Per-topic ACLs
- Per-action permissions
- Default deny
- Audit periodically

---

## Common Operational Mistakes

- No lag alert
- One ACL for everything
- No capacity plan
- Ignoring dead-letter queue
- Manual rollouts
