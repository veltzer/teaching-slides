---
tags:
  - databases:clickhouse
level: intermediate
category: databases
audience:
  - audiences:developers
  - audiences:data-engineers

---

# Operations

---

## What This Chapter Covers

- Cluster setup
- Coordination
- Backups
- Monitoring
- Upgrades

---

## Cluster Topology

- Shards spread data
- Replicas duplicate per shard
- Coordination service for replicas
- Distributed table fans out reads

---

## Topology Visualized

![clickhouse_topology](svg/courses/databases/clickhouse/05_operations/clickhouse_topology.svg)

---

## Coordination

- ZooKeeper or Keeper
- Used for replicated tables
- Watch for performance issues
- Run dedicated nodes

---

## Replicated Tables

- Use the replicated merge-tree variant
- Inserts replicated automatically
- Reads served by any replica
- Recover from local crash

---

## Sharding Key

- Decide before inserts
- Hash of business key common
- Even distribution required
- Resharding is painful

---

## Backups

- BACKUP command in modern versions
- Or filesystem snapshot of parts
- Off-host storage
- Test restores

---

## TTL Management

- Drop old data automatically
- Move parts to cold storage tier
- Set per table or column
- Saves disk over time

---

## Monitoring Metrics

- system.parts for part counts
- system.query_log for query trends
- Memory and disk usage
- Replication lag

---

## Alerts

- Pending merges high
- Many small parts
- Replica out of sync
- Disk pressure

---

## Upgrades

- Rolling per replica
- Read protocol compatibility
- Test on staging
- Have rollback plan

---

## Capacity Planning

- Project rows per second
- Project query QPS
- Memory for joins
- Network for distributed reads

---

## Multi-Tenant

- Quota per user
- Resource control
- Per-database access
- Audit query log

---

## Security

- TLS in transit
- Disk encryption
- LDAP or OIDC for auth
- Per-table grants

---

## Common Operational Mistakes

- ZooKeeper undersized
- One huge merge thread pool
- No part-count alert
- Skipping TTL configuration
- Manual node-by-node tweaks
