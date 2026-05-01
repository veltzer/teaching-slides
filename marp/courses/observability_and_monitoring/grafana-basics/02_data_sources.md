---
tags:
  - observability:grafana
level: beginner
category: observability
audience:
  - audiences:devops

---
# Data Sources

---
## What This Chapter Covers

- Common data sources
- Adding a source
- Authentication
- Versioning
- Mixing sources

---
## Common Sources

- Time-series metrics stores
- Log storage backends
- Trace storage backends
- Relational and document databases

---
## Adding A Source

- Configuration UI or API
- URL plus credentials
- Test connection before saving
- Save to workspace

---
## Naming Sources

- Use descriptive names
- Include environment in name
- Helps when many backends present
- Version control names too

---
## Authentication

- Direct credentials
- Workspace-level service accounts
- OIDC for users
- Avoid embedding secrets

---
## TLS To Backends

- Always TLS in production
- Verify certificates
- Internal CAs supported
- Disable plain HTTP

---
## Per-User vs Per-Service

- Service accounts for dashboards
- User identity for ad-hoc exploration
- Audit trails differ
- Pick based on backend support

---
## Provisioning

- Sources defined as code
- Loaded at startup
- Source of truth in git
- Easy disaster recovery

---
## Versioning

- Track changes to sources
- Especially URL and auth
- Surprises when backends move
- Test after each change

---
## Mixed Sources In One Dashboard

- Different panels, different sources
- Unified time picker
- Helpful for cross-system views
- Mix metrics with logs

---
## Caching

- Optional in some setups
- Reduces backend load
- Watch for staleness
- Tune carefully

---
## Permissions

- Per-source view and edit
- Per-folder dashboards
- Avoid wide admin grants
- Audit periodically

---
## Backups

- Source definitions backed up
- Dashboards too
- Grafana DB snapshot
- Test restore

---
## Common Data Source Mistakes

- Hardcoded credentials in source
- No naming convention
- Plain HTTP in production
- Manual provisioning
- One service account everywhere
