---
tags:
  - data-and-ai:data-engineering
level: intermediate
category: data-engineering
audience:
  - audiences:data-engineers

---

# Security, Sharing, and Operations

---

## What This Chapter Covers

- Access control
- Data masking
- Data sharing
- Cost control
- Disaster recovery

---

## Roles and Privileges

- Privileges granted to roles
- Roles granted to users
- Roles can grant other roles
- Least privilege by default

---

## Role Inheritance

![role_hierarchy](svg/courses/data_engineering/snowflake/05_security_and_sharing/role_hierarchy.svg)

---

## Custom Roles

- Per-team or per-project
- Granted dataset access
- Granted warehouse usage
- Avoid raw user grants

---

## Network Policies

- Allow IP ranges
- Block public access
- Per-account or per-user
- Helpful for compliance

---

## Authentication

- Username and password
- Single sign-on
- Key-pair for service users
- MFA for humans

---

## Dynamic Data Masking

- Function on column at read time
- Per-role unmask
- Used for PII
- Audit access carefully

---

## Row Access Policies

- Filter rows per role
- Multi-tenant patterns
- Define per table
- Test thoroughly

---

## Tags and Classifications

- Annotate columns
- Drive masking and audits
- Discoverable in catalog
- Required for compliance

---

## Data Sharing

- Share live tables across accounts
- No copy
- Provider controls access
- Consumer queries directly

---

## Marketplace

- Discover external datasets
- Subscribe to feeds
- Payments handled by Snowflake
- New data without ingest

---

## Resource Monitors

- Quotas per warehouse
- Suspend at threshold
- Notify before suspend
- Prevent runaway spend

---

## Time Travel as Recovery

- Recover dropped tables and schemas
- Restore from past version
- Useful for accidental delete
- Bound by retention

---

## Replication

- Cross-region account replication
- Failover for disaster
- Watch egress costs
- Test failover periodically

---

## Common Security Mistakes

- Account admin role for daily use
- No MFA
- No network policy
- Permissions per user
- No resource monitor
