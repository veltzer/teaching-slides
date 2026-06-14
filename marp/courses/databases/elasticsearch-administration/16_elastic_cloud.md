---
tags:
  - databases:elasticsearch
level: intermediate
category: databases
audience:
  - audiences:dbas

---
# Elastic Cloud

---
## What This Chapter Covers

- Cloud deployment options: hosted, ECE, and ECK
- Configuring deployments with templates and hardware profiles
- Scaling and autoscaling
- Cloud monitoring
- Cloud security: TLS, traffic filters, and SSO
- Snapshot management with managed repositories
- Migrating to the cloud
- Managed vs self-managed responsibilities

---
## Why Managed Elasticsearch

- Offloads provisioning, patching, and upgrades to Elastic
- Built-in security, snapshots, and monitoring out of the box
- Elastic-aware data tiers and autoscaling
- Faster time to value than building self-managed
- Trades fine-grained control for operational simplicity
- Still your job: data modeling, queries, and capacity planning

---
## Deployment Option: Elastic Cloud Hosted

- Fully managed service run by Elastic on AWS, GCP, or Azure
- Provision a deployment through the Elastic Cloud console
- Elastic handles the infrastructure, OS, and orchestration
- Pick region, version, and data-tier topology
- Lowest operational burden of the three options

---
## Deployment Option: ECE

- Elastic Cloud Enterprise runs the platform on your own hardware
- Same orchestration as hosted, but in your data center
- You operate the underlying hosts and the ECE control plane
- Good for on-prem, sovereignty, or hybrid requirements
- More control than hosted, more effort than hosted

---
## Deployment Option: ECK

- Elastic Cloud on Kubernetes is an operator for K8s clusters
- Declarative CRDs describe Elasticsearch and Kibana resources
- The operator reconciles desired state and handles certs
- Native fit for teams standardized on Kubernetes
- You own the K8s cluster, storage classes, and node pools

```yaml
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
metadata:
  name: prod
spec:
  version: 9.0.1
  nodeSets:
    - name: data
      count: 3
```

---
## Deployment Templates

- Templates predefine a topology for a workload type
- Examples: general purpose, observability, search, security
- They set sensible defaults for tiers and node sizes
- Start from a template, then customize as needed
- Reduce guesswork when standing up a new deployment

---
## Hardware Profiles

- Hardware profiles map nodes to optimized instance types
- Profiles target CPU, memory, or storage-heavy workloads
- A storage-optimized profile suits warm and cold tiers
- A compute-optimized profile suits heavy search or ingest
- Choose per data tier to match the access pattern

---
## Data Tiers in the Cloud

- Hot tier: fast storage for recent, frequently queried data
- Warm tier: less-queried data on cheaper storage
- Cold tier: infrequently accessed, searchable snapshots
- Frozen tier: rarely accessed data backed by object storage
- ILM moves indices between tiers automatically

```bash
GET _cat/nodes?v&h=name,node.role,disk.total
```

---
## Scaling Deployments

- Resize tiers by changing the RAM and storage per zone
- Add availability zones to increase resilience and capacity
- Scale up (bigger nodes) or out (more zones)
- Changes apply via a rolling, no-downtime plan
- Plan capacity from indexing rate and retention requirements

---
## Autoscaling

- Deployments can grow automatically as data grows
- Autoscaling adjusts data-tier capacity within set limits
- The frozen tier scales based on searchable-snapshot needs
- Set maximum sizes to cap cost
- Reduces manual resizing for steadily growing datasets

```bash
PUT _autoscaling/policy/my_policy
{
  "roles": ["data_hot"],
  "deciders": { "reactive_storage": {} }
}
```

---
## Cloud Monitoring

- Send monitoring data to a separate monitoring deployment
- Avoids monitoring load impacting the production cluster
- View health, performance, and logs in the console
- Built-in dashboards for JVM, indexing, and search metrics
- Configure alerting on health and resource thresholds

---
## Cloud Security: Built-In TLS

- TLS is enabled by default for transport and HTTP layers
- Certificates are provisioned and rotated by the platform
- Clients connect over HTTPS with no manual cert setup
- The native realm and RBAC are enabled out of the box
- Security is on by default, not an afterthought

---
## Cloud Security: Traffic Filters

- Restrict which networks can reach your deployment
- IP allowlists limit access to known CIDR ranges
- Private link connects without traversing the public internet
- Attach filters to deployments to enforce network policy
- Combine with authentication for defense in depth

---
## Cloud Security: SSO

- Integrate with corporate identity via SAML or OIDC
- Map identity-provider groups to Elasticsearch roles
- Centralize authentication and offboarding in the IdP
- Enforce MFA at the identity provider
- Reduces local credential sprawl across teams

```yaml
xpack.security.authc.realms.saml.corp:
  order: 2
  idp.metadata.path: "https://idp.example.com/metadata.xml"
```

---
## Snapshot Management: Managed Repos

- Hosted deployments include a managed snapshot repository
- Automated snapshots run on a schedule with retention
- Snapshots back to object storage handled for you
- Restore from the console or the snapshot API
- Use SLM for custom schedules and retention policies

```bash
GET _slm/policy
GET _snapshot/found-snapshots/_all
```

---
## Migration: Snapshot and Restore

- Snapshot the source cluster to a shared repository
- Register the same repository on the cloud deployment
- Restore selected indices into the cloud cluster
- Simplest path when downtime windows are acceptable
- Source and target versions must be compatible

```bash
POST _snapshot/my_repo/migrate_snap?wait_for_completion=false
POST _snapshot/my_repo/migrate_snap/_restore
{ "indices": "logs-*" }
```

---
## Migration: Remote Reindex

- Reindex directly from the source cluster over HTTP
- Whitelist the source host on the target cluster
- Moves data live without an intermediate repository
- Good for selective or transformed migration
- Throttle to avoid overloading the source

```bash
POST _reindex
{
  "source": {
    "remote": { "host": "https://old-cluster:9200" },
    "index": "logs-2026"
  },
  "dest": { "index": "logs-2026" }
}
```

---
## Migration: Cross-Cluster Replication

- CCR replicates indices from source to the cloud cluster
- Keeps a follower in sync for a near-zero-downtime cutover
- Pause indexing on source, let the follower catch up, promote
- Best for large datasets requiring minimal downtime
- Requires network connectivity and a remote cluster setup

```bash
PUT logs-2026/_ccr/follow
{ "remote_cluster": "on_prem", "leader_index": "logs-2026" }
```

---
## Managed vs Self-Managed Responsibilities

- Managed: Elastic owns infra, patching, TLS, and snapshots
- Self-managed: you own all of the above plus the OS and JVM
- Both: you own data modeling, mappings, queries, and ILM
- Both: you own capacity planning and cost control
- Managed shifts toil to Elastic, not accountability for design
- Choose based on team size, control needs, and compliance

---
## Elastic Cloud Checklist

- Pick the deployment model that matches your control needs
- Start from a template, tune hardware profiles per tier
- Enable autoscaling with cost caps
- Lock down access with traffic filters and SSO
- Confirm SLM snapshots and test a restore
- Plan migration via snapshot, remote reindex, or CCR
