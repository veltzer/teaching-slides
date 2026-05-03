---
tags:
  - databases:mongodb
  - infrastructure:devops
level: intermediate
category: databases
audience:
  - audiences:developers
  - audiences:devops

---
# Deployment and DevOps

---
## What This Chapter Covers

- Deploying MongoDB
- Replica sets
- Sharding
- Backups and PITR
- Monitoring
- Atlas vs self-hosted

---
## Cluster Topology Choices

![cluster_topologies](svg/courses/databases/mongodb-for-developers/15_deployment_and_devops/cluster_topologies.svg)

---
## Replica Sets

- Primary + secondaries (typically 3 nodes)
- Automatic failover
- Read scaling possible
- Foundation for production

---
## Replica Set Setup

```bash
mongod --replSet rs0 ...
mongosh
> rs.initiate({...})
```

- Configure each node
- Initiate from one
- Cluster discovers itself

---
## Sharding

- Horizontal scaling
- Each shard = a replica set
- Config servers store metadata
- mongos routes queries

---
## When To Shard

- Data &gt; one node's storage / RAM
- Write throughput &gt; one node
- Geographic distribution
- Last resort; complex to operate

---
## Backups

- mongodump: logical export
- Filesystem snapshots: faster, larger
- Atlas: automated continuous backup
- Regularly test restoration

---
## Point-In-Time Recovery

- Atlas: any second within retention
- Self-hosted: replay oplog from last full backup
- Plan for: "we deleted at 14:32; restore to 14:30"

---
## Disaster Recovery

- Cross-region replica
- Backups in another region
- Tested failover
- RTO and RPO targets

---
## Monitoring

- Atlas: built-in dashboards, alerts
- Self-hosted: Prometheus exporter, Grafana
- Track: ops/sec, latency, replication lag, cache usage
- Alerts on: high lag, low free space, slow queries

---
## Logging

- mongod logs: connections, slow queries, errors
- Forward to centralised logging
- Watch for: assertion failures, OOM kills

---
## Capacity Planning

- Working set should fit in RAM
- Disk I/O is your bottleneck on cold reads
- Plan for growth: 2x current usage as headroom
- Atlas: scale up / scale down easily

---
## Upgrades

- Self-hosted: rolling upgrades on replica set
- Atlas: managed, click a button
- Major version: read release notes carefully
- Test on staging first

---
## Atlas vs Self-Hosted

- Atlas: managed, integrated, more expensive
- Self-hosted: cheaper at scale, requires ops
- Most teams: Atlas is the right choice
- Self-host when: cost, on-prem requirement, specific compliance

---
## Cost Considerations

- Storage, compute, network
- Atlas tier sizing
- Backup retention costs
- Auto-scaling: enable carefully

---
## Compliance

- HIPAA, SOC2, GDPR
- Atlas: compliance-certified
- Self-hosted: your responsibility
- BAA with MongoDB for HIPAA

---
## Common DevOps Mistakes

- Standalone MongoDB in production
- No backups (or untested)
- Alerts that fire constantly (ignored)
- Working set exceeding RAM (slow forever)
- Storing full document in oplog forever (oplog grows)

---
## Course Wrap-Up

- MongoDB: document-oriented, schema-flexible
- Schema design matters: embed vs reference
- CRUD, aggregation, indexes: the daily work
- Transactions, change streams: when needed
- Production: replica sets, monitoring, backups
- Pick when document model fits the domain
