---
tags:
  - concepts:rdbms
  - concepts:transactions
  - concepts:isolation
  - concepts:acid
level: advanced
category: architecture
audience:
  - audiences:developers
  - audiences:architects

---

# Relational Databases

---

## What Is an RDBMS?

A relational database management system stores data in tables with rows and columns, enforces schemas, and exposes SQL for queries.

- **Schema-on-write**: types, constraints, foreign keys enforced before data lands
- **Transactions**: group operations that succeed or fail together
- **Declarative queries**: you say what you want, the optimizer picks how
- **Joins**: combine related tables at read time

Examples: PostgreSQL, MySQL/MariaDB, SQL Server, Oracle, SQLite.

---

## ACID

The four properties that make an RDBMS transaction trustworthy:

- **Atomicity** — all statements in a transaction succeed, or none do
- **Consistency** — transactions move the database between valid states (foreign keys, unique constraints, triggers all enforced)
- **Isolation** — concurrent transactions don't corrupt each other's view
- **Durability** — once committed, data survives a crash

Isolation is the most subtle of the four — and the focus of this chapter.

---

## The Isolation Problem

A database serves many clients at once. Two transactions running in parallel can interfere in ways that produce wrong answers even though each transaction, viewed alone, is correct.

The SQL standard catalogs four classes of interference — called **anomalies** — and defines **isolation levels** as promises about which anomalies the database will prevent.

Higher isolation → more correctness, less concurrency, more retries.

---

## Anomaly 1: Dirty Read

![dirty_read](svg/courses/architecting/architecting/05_rdbms/dirty_read.svg)

---

## Anomaly 2: Non-Repeatable Read

![non_repeatable_read](svg/courses/architecting/architecting/05_rdbms/non_repeatable_read.svg)

---

## Anomaly 3: Phantom Read

![phantom_read](svg/courses/architecting/architecting/05_rdbms/phantom_read.svg)

---

## Anomaly 4: Write Skew

![write_skew](svg/courses/architecting/architecting/05_rdbms/write_skew.svg)

---

## Related Anomaly: Lost Update

![lost_update](svg/courses/architecting/architecting/05_rdbms/lost_update.svg)

---

## ANSI Isolation Levels

![isolation_levels_table](svg/courses/architecting/architecting/05_rdbms/isolation_levels_table.svg)

---

## PostgreSQL's REPEATABLE READ Is Different

The SQL standard says REPEATABLE READ allows phantom reads. PostgreSQL's implementation uses **snapshot isolation** and prevents them.

But snapshot isolation is **not** true serializable:

- Dirty read — prevented
- Non-repeatable read — prevented
- Phantom read — prevented (snapshot sees consistent row set)
- **Write skew** — still possible

For write skew, use `SERIALIZABLE`, which PostgreSQL implements with Serializable Snapshot Isolation (SSI). SSI detects dependency cycles between snapshots and aborts offenders at commit time.

---

## Configuring Isolation: PostgreSQL

Per transaction:

```sql
BEGIN;
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
SELECT ...;
COMMIT;
```

Or inline:

```sql
BEGIN ISOLATION LEVEL REPEATABLE READ;
```

Per session (sticks for all future transactions on the connection):

```sql
SET SESSION CHARACTERISTICS AS TRANSACTION ISOLATION LEVEL SERIALIZABLE;
```

Default is `READ COMMITTED`. Note: `READ UNCOMMITTED` exists as a keyword but PostgreSQL silently upgrades it to `READ COMMITTED`.

---

## Configuring Isolation: MySQL / InnoDB

Per next transaction only (one-shot, must precede `BEGIN`):

```sql
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
START TRANSACTION;
SELECT ...;
COMMIT;
```

Per session:

```sql
SET SESSION TRANSACTION ISOLATION LEVEL REPEATABLE READ;
```

Globally (needs `SUPER` or `SYSTEM_VARIABLES_ADMIN`):

```sql
SET GLOBAL TRANSACTION ISOLATION LEVEL READ COMMITTED;
```

Default is `REPEATABLE READ`. InnoDB uses next-key locks, so phantom reads are also blocked in practice — stronger than the ANSI definition.

---

## Configuring Isolation: SQL Server

Per session (sticky until changed or disconnected):

```sql
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
BEGIN TRAN;
SELECT ...;
COMMIT;
```

Per query (table hint, overrides session):

```sql
SELECT * FROM Orders WITH (SERIALIZABLE) WHERE id = 42;
```

Hints also available: `READUNCOMMITTED`, `READCOMMITTED`, `REPEATABLEREAD`, `SNAPSHOT`.

Snapshot isolation is MVCC-based and off by default:

```sql
ALTER DATABASE MyDb SET ALLOW_SNAPSHOT_ISOLATION ON;
SET TRANSACTION ISOLATION LEVEL SNAPSHOT;
```

---

## Choosing an Isolation Level

- **READ UNCOMMITTED** — almost never. A curiosity.
- **READ COMMITTED** — the default on PostgreSQL and SQL Server. Right for most OLTP: cheap, prevents the worst anomaly (dirty reads), tolerates the rest.
- **REPEATABLE READ** — when a single transaction reads the same row multiple times and needs stable values. Reporting queries, financial calculations within one request.
- **SERIALIZABLE** — when correctness depends on invariants across multiple rows that aren't enforced by constraints (write skew territory). Expect retries.

Rule of thumb: start at the default, raise only when you hit an anomaly you can't work around.

---

## Optimistic vs. Pessimistic Concurrency

Two strategies for handling contention — both work at any isolation level.

**Pessimistic** — take locks upfront:

```sql
SELECT balance FROM accounts WHERE id = 1 FOR UPDATE;
-- other txns that touch this row now block
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
COMMIT;
```

**Optimistic** — no lock; detect conflict on write:

```sql
UPDATE accounts SET balance = ?, version = version + 1
WHERE id = 1 AND version = ?;
-- if 0 rows affected, someone else won — retry
```

Pick pessimistic for high-contention short transactions; optimistic when conflicts are rare and retries are cheap.

---

## Serialization Failures & Retry

At `SERIALIZABLE`, the database may abort a transaction at COMMIT with a serialization failure — not because anything is broken, but because the concurrent schedule was not serializable.

Your application must retry:

```python
import psycopg2.errors

for attempt in range(5):
    try:
        with conn.transaction():
            conn.execute("SET TRANSACTION ISOLATION LEVEL SERIALIZABLE")
            do_work(conn)
        break
    except psycopg2.errors.SerializationFailure:
        if attempt == 4:
            raise
        time.sleep(0.01 * (2 ** attempt))  # exponential backoff
```

The retry loop is not optional at SERIALIZABLE — it's part of the contract.

---

## Schema, Keys, and Indexes

Things an RDBMS gives you that NoSQL systems often don't:

- **Primary keys** — one unique row identifier per table
- **Foreign keys** — referential integrity enforced by the database, not the app
- **Unique constraints** — prevent duplicates atomically, even under concurrency
- **Check constraints** — declarative data validation (`CHECK (age >= 0)`)
- **Indexes** — B-tree for most queries, hash / GIN / GiST / BRIN for specialized access
- **Triggers** — side effects on INSERT/UPDATE/DELETE

These are enforced inside transactions and respect isolation levels — a unique violation is a hard stop, not a race.

---

## Normalization vs. Denormalization

**Normalization** (3NF) stores every fact once. Joins at read time.

- Pros: no update anomalies, smaller storage, easy schema evolution
- Cons: many-way joins get slow, reports are expensive

**Denormalization** copies frequently-joined fields into wider tables.

- Pros: fewer joins, faster reads, simpler queries
- Cons: duplicated data, must update every copy, harder to keep consistent

Start normalized. Denormalize when a specific read path proves too slow and the write-side cost is acceptable.

---

## Chapter Takeaways

- ACID's "I" is the one that bites — isolation levels are a contract, not magic
- Four anomalies: dirty / non-repeatable / phantom reads, write skew
- Defaults vary: PG & SQL Server use READ COMMITTED; MySQL/InnoDB uses REPEATABLE READ
- PostgreSQL's REPEATABLE READ is snapshot isolation — prevents phantoms but not write skew
- SERIALIZABLE costs retries, not just throughput
- Use `SELECT ... FOR UPDATE` or version columns for lost-update protection
- Normalize first, denormalize on measured need
