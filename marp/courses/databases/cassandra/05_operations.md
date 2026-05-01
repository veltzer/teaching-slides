---
tags:
  - databases:cassandra
level: intermediate
category: databases
audience:
  - audiences:developers
  - audiences:dba

---
# Operations

---
## What This Chapter Covers

- Cluster topology
- Adding and removing nodes
- Backups
- Monitoring
- Upgrades

---
## Cluster Topology

- Ring of nodes
- Tokens distribute keys
- Virtual nodes by default
- Rack and DC awareness

---
## Seed Nodes

- Bootstrap contacts
- Not special after startup
- Two or three per DC
- Avoid making all nodes seeds

---
## Adding a Node

- Bootstraps from neighbors
- Streams its tokens of data
- Triggers cluster rebalance
- Plan during low traffic

---
## Removing a Node

- Decommission cleanly
- Streams data out first
- Or use the remove-node command for failed nodes
- Always run repair after

---
## Backups

- Snapshots are hard links
- Per node
- Copy off-host
- Practice restores

---
## Incremental Backups

- Hard-link new SSTables as written
- Cheaper than snapshots
- Combine with full snapshots
- Test restore time

---
## Repair

- Anti-entropy across replicas
- Schedule weekly minimum
- Incremental and full options
- Required to bound staleness

---
## Monitoring Metrics

- Read and write latency
- Pending compactions
- Hints stored
- Heap usage
- Tombstone counts

---
## Alerts

- High pending compactions
- High GC pause
- Disk near full
- Hints accumulating

---
## Upgrades

- Rolling node by node
- Mind protocol versions
- Test on staging
- Have a rollback plan

---
## Capacity Planning

- Per-node disk and CPU limits
- Replication factor multiplies storage
- Plan growth quarterly
- Add nodes early

---
## Disaster Recovery

- Multi-DC replication is the primary tool
- Backups for accidental delete
- Restore tested quarterly
- Document the runbook

---
## Common Operational Mistakes

- No repair schedule
- Untested backups
- Single seed node
- No JVM tuning
- Surprising big-bang upgrades
