---
tags:
  - databases:mysql
level: beginner
category: databases
audience:
  - audiences:developers

---

# MySQL

---

## What This Chapter Covers

- MySQL overview
- Storage engines
- Connecting
- Basic operations
- Performance basics
- vs Postgres

---

## What MySQL Is

- Open-source relational database
- Most-deployed database
- Runs everywhere
- Web app default

---

## Quick Tour

![mysql_features](svg/courses/databases/introduction-to-databases/06_mysql/mysql_features.svg)

---

## MySQL vs Postgres

- MySQL: simpler, faster for some workloads
- Postgres: more features, stricter
- Both: capable; pick by ecosystem
- Most: Postgres preferred for new projects

---

## Storage Engines

- InnoDB: default; ACID; row-level locks
- MyISAM: legacy; no transactions
- Memory: in-RAM (volatile)
- Use InnoDB unless special reason

---

## Engine Comparison

![storage_engines_compare](svg/courses/databases/introduction-to-databases/06_mysql/storage_engines.svg)

---

## Connecting

```bash
mysql -h host -u user -p database
```

- Or: connection URL: `mysql://user:pass@host:3306/db`
- TLS for production

---

## Auto-Increment

```sql
CREATE TABLE users (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE
);
```

---

## CHARSET

- utf8 (3 bytes; doesn't cover all UTF-8)
- utf8mb4 (4 bytes; full Unicode)
- Always use utf8mb4

---

## Indexes

- Primary key clustered
- Secondary indexes contain primary key
- B-tree default
- Hash for memory tables

---

## Replication

- Source / replica (formerly master / slave)
- Async by default
- Read scaling
- Standard in production

---

## Group Replication

- Multi-leader; consensus-based
- Higher availability
- Newer, complex
- Galera Cluster: third-party alternative

---

## Backups

- mysqldump: logical
- Percona XtraBackup: physical, online
- Cloud (RDS): automated
- Test restores

---

## Common Configuration

- innodb_buffer_pool_size: 70% of RAM typical
- max_connections
- sync_binlog: durability
- innodb_flush_log_at_trx_commit: durability vs perf

---

## Hosted MySQL

- AWS RDS, Aurora MySQL
- GCP Cloud SQL
- Azure Database for MySQL
- PlanetScale: serverless MySQL
- Each: different cost / feature trade-off

---

## MariaDB

- Fork of MySQL
- API-compatible
- Some features differ
- Common: distro default in some Linux

---

## Common MySQL Mistakes

- utf8 instead of utf8mb4
- Default buffer pool (128MB)
- No replication
- mysqldump as the only backup
- Binary log retention too short
