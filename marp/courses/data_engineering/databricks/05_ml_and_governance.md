---
tags:
  - data-and-ai:data-engineering
level: intermediate
category: data-engineering
audience:
  - audiences:data-engineers

---
# ML Workflows and Governance

---
## What This Chapter Covers

- ML on Databricks
- Feature store
- Model registry
- Unity Catalog
- Cost and security

---
## ML Runtime

- Pre-installed frameworks
- GPU support
- Optimized for distributed training
- Pinned to runtime version

---
## Notebooks for ML

- Iterate on data
- Try models
- Visualize metrics
- Promote to jobs

---
## Tracking

- Built-in experiment tracking
- Auto-log hyperparameters
- Auto-log metrics
- Compare runs side by side

---
## Feature Store

- Centralize feature definitions
- Same code train and serve
- Online and offline access
- Lineage to source data

---
## Model Registry

- Versioned models
- Stages: dev, staging, prod
- Approvals via UI or API
- Source of truth for production models

---
## Serving

- Hosted endpoints
- Autoscaling
- A/B testing
- Latency monitoring

---
## Unity Catalog

- Centralized governance
- Three-level namespace
- Object-level permissions
- Cross-workspace sharing

---
## Lineage

- Automatic capture
- Across jobs and queries
- Required for audit
- Powers impact analysis

---
## Access Control

- Group-based
- Object-level grants
- Column masks
- Row filters

---
## Audit Logs

- Every action recorded
- Exported to your store
- Required for compliance
- Watch for failed access

---
## Cost Controls

- Tags per workspace, job, cluster
- Budgets and alerts
- Auto-termination
- Spot instances for fault-tolerant work

---
## Disaster Recovery

- Catalog backups
- Tables on cross-region storage
- Job definitions in git
- Test restores

---
## Common Governance Mistakes

- No catalog at all
- Permissions per user
- No tagging for cost
- Models promoted manually without approvals
- Audit logs not exported
