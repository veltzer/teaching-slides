# Database Isolation Levels
## Understanding and Implementing Transaction Isolation

<!-- Add Mermaid.js support -->
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
<script>
  mermaid.initialize({ startOnLoad: true });
</script>

---

## Agenda

1. ACID Review
1. Isolation Problems
1. Isolation Levels
1. Implementation Patterns
1. Best Practices

---

## What is Isolation

- Part of ACID properties
- Handles concurrent transactions
- Prevents interference
- Ensures data consistency
- Balances consistency vs performance

---

## Common Isolation Problems

<div class="mermaid">
graph TB
subgraph "Isolation Problems"
DR[Dirty Read<br/>Reading uncommitted data]
NR[Non-repeatable Read<br/>Different reads same transaction]
PR[Phantom Read<br/>New rows appear]
end

subgraph "Effects"
E1[Data Inconsistency]
E2[Invalid Results]
E3[Lost Updates]
end

DR --> E1
NR --> E2
PR --> E3

style DR fill:#ffcdd2
style NR fill:#f8bbd0
style PR fill:#e1bee7
</div>

---

## Dirty Read Example

```sql
-- Transaction 1
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
-- Not yet committed

-- Transaction 2 (Dirty Read)
SELECT balance FROM accounts WHERE id = 1;
-- Reads uncommitted data

-- Transaction 1
ROLLBACK;
-- Now Transaction 2 has invalid data
```

---

## Non-repeatable Read Example

```sql
-- Transaction 1
BEGIN;
SELECT balance FROM accounts WHERE id = 1;  -- Returns 1000

-- Transaction 2
UPDATE accounts SET balance = 800 WHERE id = 1;
COMMIT;

-- Transaction 1
SELECT balance FROM accounts WHERE id = 1;  -- Returns 800
-- Different result in same transaction!
```

---

## Phantom Read Example

```sql
-- Transaction 1
BEGIN;
SELECT COUNT(*) FROM accounts WHERE balance > 1000;  -- Returns 5

-- Transaction 2
INSERT INTO accounts (id, balance) VALUES (6, 1500);
COMMIT;

-- Transaction 1
SELECT COUNT(*) FROM accounts WHERE balance > 1000;  -- Returns 6
-- New row appeared!
```

---

## Standard Isolation Levels

<div class="mermaid">
graph LR
subgraph "Isolation Levels"
RU[Read Uncommitted<br/>Lowest Isolation]
RC[Read Committed<br/>Default in many DBs]
RR[Repeatable Read<br/>MySQL Default]
SR[Serializable<br/>Highest Isolation]
end

RU -->|More Isolation| RC
RC -->|More Isolation| RR
RR -->|More Isolation| SR

RU -.->|High Performance| P1[Better<br/>Concurrency]
SR -.->|Low Performance| P2[Lower<br/>Concurrency]

style RU fill:#ffebee
style RC fill:#e3f2fd
style RR fill:#f3e5f5
style SR fill:#e8f5e9
</div>

---

## Isolation Level Characteristics

| Level | Dirty Read | Non-repeatable Read | Phantom Read |
|-------|------------|---------------------|--------------|
| Read Uncommitted | Yes | Yes | Yes |
| Read Committed | No | Yes | Yes |
| Repeatable Read | No | No | Yes* |
| Serializable | No | No | No |

---

## Setting Isolation Levels

```sql
-- Session level
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;

-- Transaction level
BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE;

-- PostgreSQL example
BEGIN;
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
-- your transaction
COMMIT;
```

---

## Optimistic vs Pessimistic Locking

<div class="mermaid">
graph TB
subgraph "Pessimistic Locking"
PL1[Lock First]
PL2[Perform Operation]
PL3[Release Lock]
end

subgraph "Optimistic Locking"
OL1[Read Version]
OL2[Perform Operation]
OL3[Check Version & Update]
end

PL1 --> PL2
PL2 --> PL3

OL1 --> OL2
OL2 --> OL3
OL3 -->|Version Mismatch| OL1

PL3 --> R1[Blocks Others]
OL3 --> R2[No Blocking]

style PL1 fill:#ffcdd2
style OL1 fill:#c8e6c9
</div>

---

## Optimistic Locking Example

```sql
-- Table structure
CREATE TABLE accounts (
    id INT PRIMARY KEY,
    balance DECIMAL,
    version INT
);

-- Update with version check
UPDATE accounts
SET balance = balance - 100,
    version = version + 1
WHERE id = 1
AND version = 5;

-- If no rows updated, transaction conflicts detected
```

---

## Row-Level Locking

```sql
-- Explicit row lock
SELECT * FROM accounts
WHERE id = 1
FOR UPDATE;

-- Skip locked rows
SELECT * FROM accounts
WHERE status = 'pending'
FOR UPDATE SKIP LOCKED
LIMIT 1;
```

---

## Handling Lost Updates

```python
def transfer_money(from_id, to_id, amount):
    while True:
        try:
            with transaction.atomic():
                # Lock both accounts
                from_acc = Account.objects.select_for_update().get(id=from_id)
                to_acc = Account.objects.select_for_update().get(id=to_id)

                # Perform transfer
                from_acc.balance -= amount
                to_acc.balance += amount

                from_acc.save()
                to_acc.save()
                break
        except DatabaseError:
            time.sleep(0.1)  # Brief delay before retry
```

---

## Dealing with Deadlocks

<div class="mermaid">
graph LR
subgraph "Transaction 1"
T1A[Lock Resource A]
T1B[Want Resource B]
end

subgraph "Transaction 2"
T2B[Lock Resource B]
T2A[Want Resource A]
end

T1A -.->|Waiting| T2B
T2B -.->|Waiting| T1A

T1A --> DL[DEADLOCK!]
T2B --> DL

DL --> R[Rollback One Transaction]

style DL fill:#ff5252,color:#fff
style T1A fill:#ffcdd2
style T2B fill:#f8bbd0
</div>

---

## Deadlock Prevention

```python
def safe_update(account_ids, callback):
    # Sort IDs to ensure consistent lock order
    sorted_ids = sorted(account_ids)

    with transaction.atomic():
        # Lock in consistent order
        accounts = [
            Account.objects.select_for_update().get(id=id)
            for id in sorted_ids
        ]

        # Perform updates
        callback(accounts)
```

---

## Multi-Version Concurrency Control (MVCC)

<div class="mermaid">
graph TB
subgraph "MVCC System"
V1[Version 1<br/>T1 Created]
V2[Version 2<br/>T2 Created]
V3[Version 3<br/>T3 Created]
end

subgraph "Readers"
R1[Transaction A<br/>Sees V1]
R2[Transaction B<br/>Sees V2]
R3[Transaction C<br/>Sees V3]
end

V1 -.->|Snapshot| R1
V2 -.->|Snapshot| R2
V3 -.->|Snapshot| R3

V1 --> V2
V2 --> V3

style V1 fill:#e3f2fd
style V2 fill:#f3e5f5
style V3 fill:#e8f5e9
</div>

---

## Handling Write Skew

```sql
-- Using Serializable Isolation
BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE;

-- Check constraint
SELECT COUNT(*) FROM doctors
WHERE on_call = true AND id != 123;

-- Update if safe
UPDATE doctors
SET on_call = false
WHERE id = 123;

COMMIT;
```

---

## Performance vs Consistency

1. Higher isolation = Lower concurrency
1. Lower isolation = Better performance
1. Choose based on requirements
1. Consider hybrid approaches
1. Monitor and adjust

---

## Best Practices

1. Use appropriate isolation level
1. Implement retry logic
1. Keep transactions short
1. Handle deadlocks gracefully
1. Monitor lock contention
1. Document isolation requirements
