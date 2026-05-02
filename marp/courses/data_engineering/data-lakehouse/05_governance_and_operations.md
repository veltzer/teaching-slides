---
tags:
  - data-and-ai:data-engineering
level: intermediate
category: data-engineering
audience:
  - audiences:data-engineers
  - audiences:architects

---
# Governance and Operations

---
## What This Chapter Covers

- Data quality
- Lineage
- Access control
- Monitoring
- Cost

---
## Data Quality

- Validate at ingest
- Validate before promotion
- Track failure rates
- Block bad data, do not silently drop

---
## Quality Tests

- Not-null
- Uniqueness
- Range
- Referential integrity

---
## Quality Frameworks

- Built-in test runners
- Schedule with the pipeline
- Surface failures in alerts
- Block downstream on failure

---
## Lineage

- Source to table to dashboard
- Captured automatically by tooling
- Required for audits
- Required for debugging

---
## Lineage and Quality

![lineage_quality](svg/courses/data_engineering/data-lakehouse/05_governance_and_operations/lineage_quality.svg)

---
## Cataloging

- Inventory of tables
- Owners, descriptions
- Sample queries
- Discovery for users

---
## Access Control

- Per-table read and write
- Column-level masks
- Row-level filters
- Audit access logs

---
## PII Handling

- Tag PII columns
- Mask in non-prod
- Encrypt where required
- Honor deletion requests

---
## Monitoring

- Pipeline success rate
- Latency
- File counts
- Storage usage

---
## Alerts

- Late tables
- Schema drift
- Failed checks
- Cost spikes

---
## Cost Levers

- Compaction reduces small-file overhead
- Vacuum removes dead bytes
- Cluster on hot columns
- Cache hot tables

---
## Storage Tiers

- Hot for active data
- Cold for archive
- Lifecycle rules automate transitions
- Watch for accidental hot-data demotion

---
## Disaster Recovery

- Cross-region replication
- Catalog backed up
- Tested restore
- RPO and RTO documented

---
## Common Operational Mistakes

- Quality checks added after incidents
- No catalog
- No PII tagging
- Compaction skipped for months
- Cost reviewed yearly
