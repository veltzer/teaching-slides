---
tags:
  - infrastructure:cloud
  - infrastructure:aws
  - infrastructure:azure
  - infrastructure:gcp
  - concepts:architecture
level: advanced
category: cloud
audience:
  - audiences:architects
  - audiences:managers

---
# Migration Strategies for Multi-Cloud

---

## The Seven Rs

![seven_rs](svg/courses/cloud/multi-cloud-strategy/12_migration_strategies/seven_rs.svg)

---

## Why Migrate to Multi-Cloud?
- Avoid vendor lock-in after single-cloud adoption
- Leverage best-of-breed services across providers
- Meet regulatory requirements for provider diversity
- Merger or acquisition brings a second cloud
- Strategic risk management

---

## Migration is Not Lift-and-Shift
- Moving between clouds is not the same as moving to the cloud
- Cloud-native services differ fundamentally between providers
- Database engines, APIs, and networking models are different
- Migration requires re-architecture for many workloads
- Plan for 2-3x the effort of initial cloud migration

---

## The 7 Rs of Migration
1. Rehost: move as-is (VMs, containers)
1. Replatform: minor adjustments (e.g., swap managed database)
1. Refactor: rearchitect for target cloud
1. Repurchase: switch to SaaS equivalent
1. Retire: decommission the workload
1. Retain: keep on current cloud
1. Relocate: move infrastructure without changes (VMware-based)

---

## Assessing Workloads for Migration
- Inventory all workloads on current cloud
- Categorize by migration complexity
- Factors: cloud-specific dependencies, data volume, latency requirements
- Low complexity: stateless containers, standard databases
- High complexity: deep cloud-native integrations (Lambda + DynamoDB + SQS chains)

---

## Migration Decision Tree

![migration](svg/courses/cloud/multi-cloud-strategy/12_migration_strategies/migration_decision_tree.svg)

---

## Workload Assessment Matrix
- Business value: high vs low
- Migration difficulty: easy vs hard
- Four quadrants determine priority
- High value + easy migration: migrate first
- Low value + hard migration: retire or retain
- Document dependencies between workloads

---

## Phased Migration Approach
1. Phase 1: Assessment and planning (weeks 1-4)
1. Phase 2: Foundation (networking, identity, governance) (weeks 5-8)
1. Phase 3: Pilot migration (1-2 workloads) (weeks 9-12)
1. Phase 4: Bulk migration (iterative waves)
1. Phase 5: Optimization and decommission

---

## Phase 1: Assessment Deep Dive
- Discovery tools: AWS Migration Hub, Azure Migrate, GCP Migration Center
- Map all dependencies between services
- Identify data gravity (where is the most data?)
- Calculate egress costs for data migration
- Establish success criteria and rollback plan

---

## Phase 2: Foundation Setup
- Networking: set up cross-cloud connectivity (VPN, interconnect)
- Identity: federate identity across both clouds
- IaC: establish Terraform modules for target cloud
- CI/CD: extend pipelines to deploy to target cloud
- Monitoring: unified observability across both clouds

---

## Phase 3: Pilot Migration
- Select 1-2 low-risk, representative workloads
- Execute full migration including data
- Validate functionality, performance, and cost
- Document lessons learned
- Refine processes before bulk migration

---

## Data Migration Challenges
- Data is the hardest part of any migration
- Volume: terabytes or petabytes take time to transfer
- Consistency: data changes during migration
- Format: schema differences between managed databases
- Downtime: minimize or eliminate with CDC (Change Data Capture)

---

## Database Migration Approaches
- Dump and restore: simplest, requires downtime
- Continuous replication: near-zero downtime
- Schema conversion: tools for translating DDL
- AWS DMS, Azure Database Migration Service, GCP Database Migration Service
- Test data integrity thoroughly after migration

---

## Database Migration Example

```bash
# Export from AWS RDS PostgreSQL
pg_dump \
  --host=mydb.abc123.us-east-1.rds.amazonaws.com \
  --port=5432 \
  --username=admin \
  --format=custom \
  --file=mydb_export.dump \
  mydb

# Import to GCP Cloud SQL PostgreSQL
gcloud sql import sql my-gcp-instance \
  gs://my-migration-bucket/mydb_export.sql \
  --database=mydb

# Alternative: use continuous replication with pglogical
# On source (AWS RDS):
# CREATE EXTENSION pglogical;
# SELECT pglogical.create_node(
#   node_name := 'provider',
#   dsn := 'host=mydb.abc123.rds.amazonaws.com dbname=mydb'
# );
```

---

## Container Migration
- Containers are the most portable workload type
- Docker images work across all cloud container services
- Migration path: EKS -> AKS or GKE (or vice versa)
- Challenges: Kubernetes config differences, storage classes, load balancers
- Use Helm charts or Kustomize for cloud-specific overlays

---

## Container Migration: EKS to GKE

```bash
# Export Kubernetes resources from EKS
kubectl get deployments,services,configmaps,secrets \
  -n my-app -o yaml > workload-export.yaml

# Adjust cloud-specific annotations
# - Remove AWS-specific annotations (alb.ingress, eks.amazonaws.com)
# - Add GCP-specific annotations (cloud.google.com/neg)
# - Update storage classes (gp2 -> standard-rwo)

# Apply to GKE cluster
gcloud container clusters get-credentials my-gke-cluster \
  --zone=europe-west1-b
kubectl apply -f workload-export.yaml -n my-app

# Verify deployment
kubectl get pods -n my-app
kubectl get svc -n my-app
```

---

## Serverless Migration Challenges
- Lambda, Azure Functions, Cloud Functions have different runtimes
- Event sources differ completely between providers
- No standard packaging format (each has its own)
- Often the hardest workloads to migrate
- Consider: is migration worth it, or retain on original cloud?

---

## Networking During Migration
- Both clouds must be connected during transition
- VPN or dedicated interconnect between clouds
- DNS-based traffic splitting for gradual cutover
- Firewall rules must allow cross-cloud communication
- Monitor latency between clouds during migration

---

## Testing and Validation
- Functional testing: does the migrated workload work correctly?
- Performance testing: latency, throughput, resource utilization
- Data integrity: compare checksums, row counts, sample queries
- Security testing: ensure policies are enforced on target cloud
- User acceptance testing before cutover

---

## Rollback Planning
- Every migration phase needs a rollback plan
- Rollback criteria: define what triggers a rollback
- Data rollback is the hardest: how to sync changes back
- Keep source environment running until migration is validated
- Time-box validation period (e.g., 2 weeks of dual-running)

---

## Migration Tools
- Terraform Import: import existing resources into IaC
- Velero: Kubernetes backup and migration
- AWS DMS / Azure DMS / GCP DMS: database migration
- rclone: object storage migration across clouds
- CloudEndure / Azure Migrate: VM-level migration

---

## Cost of Migration
- Direct costs: tooling, consulting, cloud spend during dual-running
- Indirect costs: team time, reduced velocity, opportunity cost
- Egress charges for data transfer out of source cloud
- Dual-running period: paying for both clouds simultaneously
- Budget 20-30% contingency for unexpected complexity

---

## Post-Migration Optimization
- Do not just replicate the old architecture on the new cloud
- Leverage target cloud's native services where appropriate
- Rightsize resources (instance types differ between providers)
- Implement target cloud's cost optimization features
- Update monitoring, alerting, and runbooks

---

## Common Migration Pitfalls
- Underestimating data migration complexity
- Not accounting for egress costs
- Skipping the pilot phase
- Insufficient testing of migrated workloads
- Attempting to migrate everything at once
- Not training the team on the target cloud first

---

## Case Study: E-Commerce Platform Migration
- AWS-only platform migrating critical services to GCP
- Phase 1: Containerized microservices (EKS to GKE) - 4 weeks
- Phase 2: Database migration (RDS PostgreSQL to Cloud SQL) - 3 weeks
- Phase 3: Object storage migration (S3 to GCS) - 2 weeks
- Total: 12 weeks including validation
- Result: critical path services on both clouds for DR

---

## Key Takeaways
- Assess workloads before deciding what to migrate
- Phase the migration: foundation, pilot, waves, optimize
- Data migration is the hardest part; plan for it specifically
- Containers are the most portable; serverless is the least
- Budget for dual-running costs and egress fees
- Always have a rollback plan
