# Database ACID Guarantees

---

## What Are ACID Guarantees?

ACID is an acronym that stands for:
- Atomicity
- Consistency
- Isolation
- Durability

These properties ensure reliable processing of database transactions.

---

## Why ACID Matters

- Ensures data integrity even when errors occur
- Prevents data corruption during concurrent operations
- Provides reliability for critical business applications
- Forms the foundation of enterprise database systems

---

## Atomicity

A transaction is an all-or-nothing operation.
- Either all operations in a transaction succeed
- Or none of them take effect

---

## Atomicity Example

```sql
BEGIN TRANSACTION;
    UPDATE accounts SET balance = balance - 100 WHERE account_id = 123;
    UPDATE accounts SET balance = balance + 100 WHERE account_id = 456;
COMMIT;
```

If any statement fails, the entire transaction is rolled back.

---

## Atomicity Visualized

![0](../../out/mermaid/marp/lectures/acid.md/0.png)

---

## Consistency

The database must transition from one valid state to another.
- Database constraints must be maintained
- Referential integrity is preserved
- Business rules are enforced

---

## Consistency Example

```sql
-- Account balance cannot be negative (constraint)
CREATE TABLE accounts (
    account_id INT PRIMARY KEY,
    balance DECIMAL CHECK (balance >= 0)
);

-- Transaction will fail if it violates the constraint
BEGIN TRANSACTION;
    UPDATE accounts SET balance = balance - 1000 WHERE account_id = 123;
COMMIT;
```

---

## Consistency Visualized

![1](../../out/mermaid/marp/lectures/acid.md/1.png)

---

## Isolation

Concurrent transactions should not interfere with each other.
- Each transaction should appear to execute in isolation
- Intermediate states should not be visible to other transactions

---

## Isolation Levels

1. **Read Uncommitted** - Lowest isolation, allows dirty reads
1. **Read Committed** - Prevents dirty reads
1. **Repeatable Read** - Prevents non-repeatable reads
1. **Serializable** - Highest isolation, prevents phantom reads

---

## Isolation Problems

1. **Dirty Reads** - Reading uncommitted changes
1. **Non-repeatable Reads** - Reading different values within same transaction
1. **Phantom Reads** - Row set changes during transaction

---

## Dirty Reads Example

```sql
-- Transaction 1
BEGIN TRANSACTION;
    UPDATE accounts SET balance = 1000 WHERE account_id = 123;
    -- No COMMIT yet

-- Transaction 2 (with READ UNCOMMITTED)
BEGIN TRANSACTION;
    SELECT balance FROM accounts WHERE account_id = 123; -- Returns 1000
COMMIT;

-- Transaction 1 rolls back
ROLLBACK; -- Balance is back to original value
```

---

## Isolation Visualization

![2](../../out/mermaid/marp/lectures/acid.md/2.png)

---

## Isolation Level Comparison

| Isolation Level | Dirty Reads | Non-repeatable Reads | Phantom Reads |
|-----------------|-------------|----------------------|---------------|
| Read Uncommitted| Possible    | Possible             | Possible      |
| Read Committed  | Prevented   | Possible             | Possible      |
| Repeatable Read | Prevented   | Prevented            | Possible      |
| Serializable    | Prevented   | Prevented            | Prevented     |

---

## Setting Isolation Level

```sql
-- PostgreSQL
BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE;

-- MySQL
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
BEGIN;

-- SQL Server
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
BEGIN TRANSACTION;
```

---

## Durability

Once a transaction is committed, it remains committed.
- Changes survive system failures
- Committed data is permanently stored
- Recovery mechanisms ensure data persistence

---

## Durability Implementation

1. **Write-Ahead Logging (WAL)**
1. **Transaction Logs**
1. **Checkpoints**
1. **Database Backups**

---

## Durability Example

```sql
BEGIN TRANSACTION;
    INSERT INTO critical_records (id, data) VALUES (1, 'important');
COMMIT;
```

Even if the system crashes immediately after commit:
- The record will be recovered during restart
- No committed data is lost

---

## Durability Visualization

![3](../../out/mermaid/marp/lectures/acid.md/3.png)

---

## ACID in Action: Bank Transfer

```sql
BEGIN TRANSACTION;
    -- Check if sufficient funds
    SELECT balance INTO @current_balance FROM accounts WHERE id = 123;

    IF @current_balance >= 500 THEN
        -- Debit one account
        UPDATE accounts SET balance = balance - 500 WHERE id = 123;

        -- Credit another account
        UPDATE accounts SET balance = balance + 500 WHERE id = 456;

        COMMIT;
    ELSE
        ROLLBACK;
    END IF;
```

---

## ACID Trade-offs

1. **Performance Impact** - Ensuring ACID properties requires overhead
1. **Concurrency Limitations** - Strict isolation can reduce throughput
1. **Complexity** - Implementation and management become more complex

---

## When to Relax ACID?

- High-volume read operations
- Distributed systems with CAP theorem constraints
- Analytics workloads
- When eventual consistency is acceptable

---

## NoSQL and BASE

Many NoSQL systems follow BASE instead of ACID:
- Basically Available
- Soft state
- Eventual consistency

---

## Eventual Consistency

![4](../../out/mermaid/marp/lectures/acid.md/4.png)

---

## Implementing ACID: Transactions

```sql
-- Good practice
BEGIN TRANSACTION;
    -- Operations here

    -- Validate operations were successful
    IF @error_occurred THEN
        ROLLBACK;
    ELSE
        COMMIT;
    END IF;
```

---

## Implementing ACID: Error Handling

```sql
BEGIN TRANSACTION;
    BEGIN TRY
        INSERT INTO orders (customer_id, total) VALUES (123, 499.99);
        INSERT INTO order_items (order_id, product_id, quantity) VALUES
            (SCOPE_IDENTITY(), 456, 2),
            (SCOPE_IDENTITY(), 789, 1);
        COMMIT;
    END TRY
    BEGIN CATCH
        ROLLBACK;
        -- Log error
    END CATCH;
```

---

## Implementing ACID: Deadlock Handling

```sql
-- PostgreSQL retry logic
DO $$
DECLARE
    _retry_counter INT := 0;
    _max_retries CONSTANT INT := 3;
    _retry_delay CONSTANT INT := 100; -- milliseconds
BEGIN
    WHILE _retry_counter < _max_retries LOOP
        BEGIN
            -- Transaction logic here

            EXIT; -- Success, exit loop
        EXCEPTION WHEN deadlock_detected THEN
            _retry_counter := _retry_counter + 1;
            IF _retry_counter >= _max_retries THEN
                RAISE; -- Re-raise if max retries reached
            END IF;
            -- Wait before retry
            PERFORM pg_sleep(_retry_delay / 1000.0);
        END;
    END LOOP;
END$$;
```

---

## Monitoring ACID Compliance

Key metrics to track:
1. Transaction rollback rate
1. Deadlock frequency
1. Lock wait times
1. Recovery time after failures

---

## ACID Best Practices

1. Keep transactions short
1. Use appropriate isolation levels
1. Implement proper error handling
1. Consider optimistic vs. pessimistic locking
1. Regular testing of failure scenarios

---

## Summary: ACID Guarantees

- **Atomicity**: All-or-nothing transaction execution
- **Consistency**: Database remains in valid state
- **Isolation**: Transactions appear to execute in isolation
- **Durability**: Committed changes are permanent

---

## Further Learning Resources

1. Database system documentation (PostgreSQL, MySQL, SQL Server)
1. "Transaction Processing: Concepts and Techniques" by Jim Gray
1. "Designing Data-Intensive Applications" by Martin Kleppmann
1. Database vendor certification courses
