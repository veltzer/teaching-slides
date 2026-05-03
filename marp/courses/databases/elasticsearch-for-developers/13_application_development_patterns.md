---
tags:
  - databases:elasticsearch
  - architecture:patterns
level: intermediate
category: databases
audience:
  - audiences:developers

---
# Application Development Patterns

---

## Application Development Patterns Overview

![dev_patterns](svg/courses/databases/elasticsearch-for-developers/13_application_development_patterns/dev_patterns.svg)

---
## What This Chapter Covers

- ES as primary store?
- Sync from another DB
- Search over multiple data sources
- Read-heavy patterns
- Write-heavy patterns

---
## Patterns

![app_patterns](svg/courses/databases/elasticsearch-for-developers/13_application_development_patterns/app_patterns.svg)

---
## ES As Primary Store

- Risky: no transactions, no joins
- Backup harder than relational
- Schema evolution painful
- Most teams: don't

---
## ES As Search Index

- Authoritative data in primary DB (Postgres / MongoDB)
- ES indexes a copy
- Sync via change-data-capture or app-level events
- The standard pattern

---
## CDC Sync

- Debezium, MongoDB change streams
- Stream changes into Kafka
- Consumer indexes to ES
- Eventually consistent; near-real-time

---
## Application-Level Sync

- Write to DB; on success, write to ES
- Two-phase risk (DB succeeds; ES fails)
- Outbox pattern: log to DB, async-publish
- Idempotent indexing handles retries

---
## Outbox Pattern

- Write to outbox table in same DB transaction
- Worker reads outbox; indexes to ES
- Atomic with respect to the DB
- Eventually pushed to ES

---
## Read-Heavy

- Many readers, fewer writers
- Add replicas
- Cache hot queries
- ES scales naturally

---
## Write-Heavy

- Bulk index from queue
- More shards (within reason)
- Disable refresh during bulk
- ILM for old data

---
## Multi-Tenant

- Per-tenant index: small tenants share; big ones get own index
- Per-tenant field with filter: simpler; less isolation
- Index-per-tenant is common at scale

---
## Per-User Filtering

- Always filter by user_id in queries
- Document-level security in Elastic Stack X-Pack
- Or: app-level enforcement

---
## Reindexing

- Mappings change &#8594; reindex
- New index; copy data; alias swap
- Tools: Reindex API, Logstash
- Plan for it; routine operation

---
## Aliases

- An alias points to one or more indexes
- Apps query the alias
- Swap underlying index without app change
- Standard for blue/green deploys of indexes

---
## ILM Strategy

- Hot: actively written
- Warm: read but rarely written
- Cold: occasional access
- Frozen: archive
- Delete: gone
- Move automatically based on age

---
## Common Pattern Mistakes

- ES as primary; data lost
- Sync that's "eventually consistent" but readers expect strong
- One huge index for all tenants
- No alias indirection
- ILM not configured; cluster fills up
