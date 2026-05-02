---
tags:
  - observability:grafana
level: beginner
category: observability
audience:
  - audiences:devops

---
# Operations

---
## What This Chapter Covers

- Deployment options
- Authentication
- Permissions
- Backups
- Performance

---
## Deployment Options

- Self-hosted single node
- Self-hosted high-availability
- Hosted offering
- Embedded vendor product

---
## High Availability

- Multiple frontends
- Shared backend database
- Object storage for state in some setups
- Health checks at the load balancer

---
## HA Topology

![ha_topology](svg/courses/observability_and_monitoring/grafana-basics/05_operations/ha_topology.svg)

---
## Backend Database

- SQLite for small setups
- PostgreSQL or MySQL for HA
- Backups and restores
- Tested restore matters

---
## Authentication

- Local accounts for small teams
- LDAP for enterprises
- OIDC for modern stacks
- Pick by org-wide identity

---
## Authorization

- Organizations and teams
- Folder permissions
- Dashboard permissions
- Avoid per-dashboard sprawl

---
## Provisioning

- Sources, dashboards, alerts as code
- Loaded at startup
- Easy disaster recovery
- Avoid drift between environments

---
## Backups

- Database snapshot
- Dashboard JSON export
- Regular schedule
- Practice restores

---
## Performance

- Dashboard render speed
- Query load on backends
- Browser cost on big dashboards
- Profile slow ones

---
## Reducing Backend Load

- Cache where supported
- Avoid huge time ranges
- Pre-aggregate where possible
- Limit concurrent queries

---
## Audit Logs

- User actions
- Login attempts
- Dashboard edits
- Forwarded to central store

---
## Plugins

- Data source and panel plugins
- Pin versions
- Audit before installing
- Test in lower env first

---
## Upgrades

- Read release notes
- Check plugin compatibility
- Roll in lower env first
- Backup before upgrade

---
## Cost Awareness

- Hosted: per active user
- Self-hosted: infrastructure plus ops
- Plugin licenses
- Track who uses dashboards

---
## Common Operational Mistakes

- SQLite in production HA
- No provisioning
- No backup of dashboards
- Plugins from unknown sources
- Skipping upgrade staging
