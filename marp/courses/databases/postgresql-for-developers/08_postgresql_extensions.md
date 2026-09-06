---
tags:
  - databases:postgresql
  - databases:extensions
level: intermediate
category: databases
audience:
  - audiences:developers

---

# PostgreSQL Extensions

---

## Popular Extensions

![popular_extensions](svg/courses/databases/postgresql-for-developers/08_postgresql_extensions/popular_extensions.svg)

---

## What This Chapter Covers

- Extension model
- Popular extensions
- Installing and enabling
- pg_stat_statements
- PostGIS
- pgcrypto
- Other notables

---

## Extension Model

- Loadable C / SQL packages
- Add types, functions, operators
- One of Postgres's strengths
- Often: distro packages

---

## Installing

```bash
sudo apt install postgresql-16-postgis-3
```

```sql
CREATE EXTENSION postgis;
```

- Install package; enable per-database

---

## pg_stat_statements

- Track query execution stats
- Total time, mean time, rows
- Find slow queries
- Standard in production

---

## Enabling pg_stat_statements

```bash
# postgresql.conf
shared_preload_libraries = 'pg_stat_statements'
```

```sql
CREATE EXTENSION pg_stat_statements;
SELECT * FROM pg_stat_statements ORDER BY total_time DESC LIMIT 10;
```

---

## PostGIS

- Geospatial extension
- Geometry types: point, line, polygon
- Spatial functions: distance, intersection, contains
- The de facto geospatial DB
- Used by ArcGIS, OpenStreetMap, Uber

---

## PostGIS Example

```sql
CREATE EXTENSION postgis;
CREATE TABLE places (id SERIAL, location GEOGRAPHY(POINT));
SELECT id FROM places
WHERE ST_DWithin(location, ST_MakePoint(-73.9, 40.7)::geography, 1000);
```

- Within 1km of a point

---

## pgcrypto

- Cryptographic functions
- Hashing, encryption
- bcrypt for passwords
- AES for column encryption

---

## uuid-ossp

- UUID generation
- gen_random_uuid() in core (Postgres 13+)
- uuid-ossp for UUID v1-v5
- Standard in many schemas

---

## TimescaleDB

- Time-series on Postgres
- Hypertables: auto-partitioned by time
- Continuous aggregations
- Compressed historical data

---

## Citus

- Distributed Postgres
- Sharding across nodes
- Acquired by Microsoft (Azure)
- For: very large workloads

---

## pg_partman

- Partition management automation
- Creates partitions on schedule
- Retains N partitions; drops older
- Standard with declarative partitioning

---

## Hypopg

- "Hypothetical" indexes
- Test if an index *would* help without creating it
- Useful for query plan exploration
- Read-only

---

## Common Extension Mistakes

- Not using pg_stat_statements (flying blind)
- PostGIS without spatial indexes (slow)
- Custom extensions without C-level expertise
- Enabling everything; only what you use
- Forgetting extensions on replicas
