---
tags:
  - databases:design
  - databases:security
level: intermediate
category: databases
audience:
  - audiences:developers

---
# Security and Integrity in Database Design

---
## What This Chapter Covers

- Role-based access
- Row-level security
- Encryption
- Audit logs
- Backup and recovery
- Compliance considerations

---
## Database Users

- Don't use root / superuser for apps
- Per-app users with limited privileges
- GRANT only what's needed
- Audit periodically

---
## Roles

- Group privileges
- Assign roles to users
- Easier to manage at scale
- Standard in Postgres, MySQL, others

---
## Row-Level Security

- Postgres: RLS policies
- "Users can only see their own rows"
- DB enforces; app can't bypass (mostly)
- Powerful; setup carefully

---
## Access Control Layers

![access_control](svg/courses/databases/database-design/08_security_and_integrity_in_database_design/access_control.svg)

---
## Layers of Data Integrity

![integrity_layers](svg/courses/databases/database-design/08_security_and_integrity_in_database_design/integrity_layers.svg)

---
## Encryption At Rest

- Disk-level: TDE (Transparent Data Encryption)
- Per-column: pgcrypto, encrypt function
- Backups: encrypt those too
- Standard for compliance

---
## Encryption In Transit

- TLS to the database
- Required for compliance
- Performance: tiny CPU cost
- Cloud DBs: usually default-on

---
## Audit Logs

- Log: who did what, when
- Sensitive operations especially
- Per-table audit columns
- Or: pgaudit / built-in audit

---
## Backups

- Regular, automated, tested
- Restore drill: actually recover from backup
- Off-site / cross-region copies
- Retention policy aligned with compliance

---
## Point-In-Time Recovery

- Restore to any specific moment
- Requires WAL / binlog archive
- Recover from "we deleted at 14:32"
- Most cloud DBs offer this

---
## Disaster Recovery

- Multi-region replication
- Failover plan tested
- RTO (recovery time): minutes vs hours
- RPO (recovery point): how much data can you lose
- Match to business need

---
## Compliance

- HIPAA, PCI, GDPR, SOX
- Each has data-handling requirements
- Encryption, audit, retention
- DBAs and engineers both involved

---
## Data Retention

- How long do you keep data?
- GDPR: right to be forgotten
- Tombstone or hard delete
- Document the policy

---
## SQL Injection

- App-layer concern; mention here
- Use parameterised queries
- ORMs help
- Never concatenate user input into SQL

---
## Common Security Mistakes

- App connecting as superuser
- No backup verification
- Plaintext sensitive columns
- Audit log writes that fail silently
- Forgetting to encrypt backup snapshots

---
## Course Wrap-Up

- ER &#8594; logical &#8594; physical
- Normalise; denormalise where needed
- Indexes for queries; not blanket
- Security: layered (auth, encryption, audit)
- Test backups; not just have them
