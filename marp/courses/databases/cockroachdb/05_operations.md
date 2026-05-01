---
tags:
  - databases:cockroachdb
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
- Backups
- Upgrades
- Monitoring
- Performance tuning

---
## Topology

- Three or more nodes
- Multiple availability zones
- Multiple regions for tier-1
- Plan replicas to survive

---
## Cluster Init

- Start nodes
- Run init once
- Designate license if applicable
- Configure cluster settings

---
## Adding Nodes

- Start with same join address
- Bootstraps automatically
- Cluster rebalances ranges
- No manual sharding

---
## Removing Nodes

- Decommission cleanly
- Watch ranges drain
- Verify replicas before stopping
- Avoid abrupt stops

---
## Backups

- Full and incremental
- Native command to object storage
- Encrypted at rest
- Test restores quarterly

---
## Restore

- Full plus incremental backups applied
- Can restore individual tables
- Mind cluster compatibility
- Validate before swap

---
## Upgrades

- Rolling node by node
- Major version requires plan
- Read release notes for breaking changes
- Have rollback plan

---
## Monitoring Metrics

- Replicas leader, follower counts
- Range counts
- Latency p99 on key operations
- Live nodes vs expected

---
## Built-in DB Console

- Real-time view of cluster
- Statements and transactions stats
- Replica heatmap
- Slow query insight

---
## Alerts

- Under-replicated ranges
- Cluster unavailable
- Disk near full
- Time skew exceeded

---
## Performance Tuning

- Hot range fixes
- Index review
- Statistics refresh
- Query plan inspection

---
## Cost Awareness

- Three replicas means three times storage
- Multi-region multiplies again
- Egress in multi-region
- Tag and chargeback

---
## Security

- TLS required
- Per-user roles
- LDAP or OIDC for auth
- Encryption at rest

---
## Common Operational Mistakes

- One AZ deployment
- No clock sync alarm
- Disk filling silently
- Skipping major-version notes
- Manual range moves
