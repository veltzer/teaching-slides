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

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <!-- Background -->
  <rect width="800" height="400" fill="#f9f9f9" stroke="#ddd" stroke-width="1"/>

  <!-- Start Transaction -->
  <rect x="350" y="20" width="140" height="40" rx="5" fill="#4CAF50" stroke="#388E3C" stroke-width="2"/>
  <text x="420" y="45" text-anchor="middle" fill="white" font-family="Arial, sans-serif" font-size="14" font-weight="bold">Start Transaction</text>

  <!-- Arrow to Operation 1 -->
  <path d="M 420 60 L 420 90" stroke="#333" stroke-width="2" fill="none" marker-end="url(#arrowhead)"/>

  <!-- Operation 1: Withdraw $100 -->
  <rect x="310" y="90" width="220" height="40" rx="5" fill="#2196F3" stroke="#1976D2" stroke-width="2"/>
  <text x="420" y="115" text-anchor="middle" fill="white" font-family="Arial, sans-serif" font-size="14">Operation 1: Withdraw $100</text>

  <!-- Arrow to Operation 2 -->
  <path d="M 420 130 L 420 160" stroke="#333" stroke-width="2" fill="none" marker-end="url(#arrowhead)"/>

  <!-- Operation 2: Deposit $100 -->
  <rect x="310" y="160" width="220" height="40" rx="5" fill="#2196F3" stroke="#1976D2" stroke-width="2"/>
  <text x="420" y="185" text-anchor="middle" fill="white" font-family="Arial, sans-serif" font-size="14">Operation 2: Deposit $100</text>

  <!-- Arrow to Decision -->
  <path d="M 420 200 L 420 230" stroke="#333" stroke-width="2" fill="none" marker-end="url(#arrowhead)"/>

  <!-- Decision Diamond -->
  <path d="M 420 230 L 520 270 L 420 310 L 320 270 Z" fill="#FFC107" stroke="#F57C00" stroke-width="2"/>
  <text x="420" y="265" text-anchor="middle" fill="#333" font-family="Arial, sans-serif" font-size="12">All Operations</text>
  <text x="420" y="280" text-anchor="middle" fill="#333" font-family="Arial, sans-serif" font-size="12">Successful?</text>

  <!-- Yes branch -->
  <path d="M 520 270 L 580 270" stroke="#333" stroke-width="2" fill="none" marker-end="url(#arrowhead)"/>
  <text x="550" y="260" text-anchor="middle" fill="#4CAF50" font-family="Arial, sans-serif" font-size="12" font-weight="bold">Yes</text>

  <!-- COMMIT -->
  <rect x="580" y="250" width="180" height="40" rx="5" fill="#4CAF50" stroke="#388E3C" stroke-width="2"/>
  <text x="670" y="275" text-anchor="middle" fill="white" font-family="Arial, sans-serif" font-size="14" font-weight="bold">COMMIT: All changes saved</text>

  <!-- No branch -->
  <path d="M 320 270 L 260 270" stroke="#333" stroke-width="2" fill="none" marker-end="url(#arrowhead)"/>
  <text x="290" y="260" text-anchor="middle" fill="#F44336" font-family="Arial, sans-serif" font-size="12" font-weight="bold">No</text>

  <!-- ROLLBACK -->
  <rect x="80" y="250" width="180" height="40" rx="5" fill="#F44336" stroke="#D32F2F" stroke-width="2"/>
  <text x="170" y="275" text-anchor="middle" fill="white" font-family="Arial, sans-serif" font-size="14" font-weight="bold">ROLLBACK: No changes made</text>

  <!-- Arrow marker definition -->
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="10" refX="9" refY="5" orient="auto">
      <polygon points="0 0, 10 5, 0 10" fill="#333"/>
    </marker>
  </defs>
</svg>

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

<svg viewBox="0 0 800 300" xmlns="http://www.w3.org/2000/svg">
  <!-- Background -->
  <rect width="800" height="300" fill="#f9f9f9" stroke="#ddd" stroke-width="1"/>

  <!-- Valid State 1 -->
  <rect x="50" y="120" width="120" height="60" rx="10" fill="#4CAF50" stroke="#388E3C" stroke-width="2"/>
  <text x="110" y="155" text-anchor="middle" fill="white" font-family="Arial, sans-serif" font-size="14" font-weight="bold">Valid State 1</text>

  <!-- Arrow to Transaction -->
  <path d="M 170 150 L 250 150" stroke="#333" stroke-width="2" fill="none" marker-end="url(#arrow1)"/>

  <!-- Transaction -->
  <rect x="250" y="120" width="120" height="60" rx="10" fill="#2196F3" stroke="#1976D2" stroke-width="2"/>
  <text x="310" y="155" text-anchor="middle" fill="white" font-family="Arial, sans-serif" font-size="14" font-weight="bold">Transaction</text>

  <!-- Arrow to Valid State 2 -->
  <path d="M 370 150 L 450 150" stroke="#333" stroke-width="2" fill="none" marker-end="url(#arrow1)"/>

  <!-- Valid State 2 -->
  <rect x="450" y="120" width="120" height="60" rx="10" fill="#4CAF50" stroke="#388E3C" stroke-width="2"/>
  <text x="510" y="155" text-anchor="middle" fill="white" font-family="Arial, sans-serif" font-size="14" font-weight="bold">Valid State 2</text>

  <!-- Dotted arrow to Invalid State -->
  <path d="M 310 180 L 310 230" stroke="#F44336" stroke-width="2" stroke-dasharray="5,5" fill="none" marker-end="url(#arrow2)"/>
  <text x="340" y="210" fill="#F44336" font-family="Arial, sans-serif" font-size="12" font-style="italic">Violates Rules</text>

  <!-- Invalid State -->
  <rect x="250" y="230" width="120" height="60" rx="10" fill="#ffebee" stroke="#F44336" stroke-width="2" stroke-dasharray="5,5"/>
  <text x="310" y="265" text-anchor="middle" fill="#F44336" font-family="Arial, sans-serif" font-size="14" font-weight="bold">Invalid State</text>

  <!-- Rejected arrow back to Valid State 1 -->
  <path d="M 250 260 Q 150 260 110 180" stroke="#F44336" stroke-width="2" fill="none" marker-end="url(#arrow2)"/>
  <text x="150" y="245" fill="#F44336" font-family="Arial, sans-serif" font-size="12" font-weight="bold">Rejected</text>

  <!-- Legend/Explanation -->
  <text x="400" y="40" font-family="Arial, sans-serif" font-size="16" font-weight="bold" fill="#333" text-anchor="middle">Database Consistency: Only Valid State Transitions Allowed</text>

  <text x="650" y="120" font-family="Arial, sans-serif" font-size="12" fill="#666">Rules enforced:</text>
  <text x="650" y="140" font-family="Arial, sans-serif" font-size="11" fill="#666">• Constraints</text>
  <text x="650" y="155" font-family="Arial, sans-serif" font-size="11" fill="#666">• Referential integrity</text>
  <text x="650" y="170" font-family="Arial, sans-serif" font-size="11" fill="#666">• Business rules</text>

  <!-- Arrow marker definitions -->
  <defs>
    <marker id="arrow1" markerWidth="10" markerHeight="10" refX="9" refY="5" orient="auto">
      <polygon points="0 0, 10 5, 0 10" fill="#333"/>
    </marker>
    <marker id="arrow2" markerWidth="10" markerHeight="10" refX="9" refY="5" orient="auto">
      <polygon points="0 0, 10 5, 0 10" fill="#F44336"/>
    </marker>
  </defs>
</svg>

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

<svg viewBox="0 0 800 500" xmlns="http://www.w3.org/2000/svg">
  <!-- Background -->
  <rect width="800" height="500" fill="#f9f9f9" stroke="#ddd" stroke-width="1"/>

  <!-- Title -->
  <text x="400" y="30" font-family="Arial, sans-serif" font-size="16" font-weight="bold" fill="#333" text-anchor="middle">Dirty Read Problem - Isolation Violation</text>

  <!-- Participants -->
  <rect x="100" y="60" width="120" height="40" rx="5" fill="#2196F3" stroke="#1976D2" stroke-width="2"/>
  <text x="160" y="85" text-anchor="middle" fill="white" font-family="Arial, sans-serif" font-size="14" font-weight="bold">Transaction 1</text>
  <line x1="160" y1="100" x2="160" y2="470" stroke="#2196F3" stroke-width="2" stroke-dasharray="2,2"/>

  <rect x="340" y="60" width="120" height="40" rx="5" fill="#4CAF50" stroke="#388E3C" stroke-width="2"/>
  <text x="400" y="85" text-anchor="middle" fill="white" font-family="Arial, sans-serif" font-size="14" font-weight="bold">Database</text>
  <line x1="400" y1="100" x2="400" y2="470" stroke="#4CAF50" stroke-width="2" stroke-dasharray="2,2"/>

  <rect x="580" y="60" width="120" height="40" rx="5" fill="#9C27B0" stroke="#7B1FA2" stroke-width="2"/>
  <text x="640" y="85" text-anchor="middle" fill="white" font-family="Arial, sans-serif" font-size="14" font-weight="bold">Transaction 2</text>
  <line x1="640" y1="100" x2="640" y2="470" stroke="#9C27B0" stroke-width="2" stroke-dasharray="2,2"/>

  <!-- T1: BEGIN TRANSACTION -->
  <path d="M 160 120 L 400 120" stroke="#333" stroke-width="2" fill="none" marker-end="url(#arrow3)"/>
  <rect x="200" y="105" width="150" height="25" rx="3" fill="white" stroke="#333" stroke-width="1"/>
  <text x="275" y="122" text-anchor="middle" font-family="Arial, sans-serif" font-size="12">BEGIN TRANSACTION</text>

  <!-- T2: BEGIN TRANSACTION -->
  <path d="M 640 150 L 400 150" stroke="#333" stroke-width="2" fill="none" marker-end="url(#arrow3)"/>
  <rect x="450" y="135" width="150" height="25" rx="3" fill="white" stroke="#333" stroke-width="1"/>
  <text x="525" y="152" text-anchor="middle" font-family="Arial, sans-serif" font-size="12">BEGIN TRANSACTION</text>

  <!-- T1: Read A = 100 -->
  <path d="M 160 180 L 400 180" stroke="#333" stroke-width="2" fill="none" marker-end="url(#arrow3)"/>
  <rect x="210" y="165" width="130" height="25" rx="3" fill="white" stroke="#333" stroke-width="1"/>
  <text x="275" y="182" text-anchor="middle" font-family="Arial, sans-serif" font-size="12">Read A = 100</text>

  <!-- T1: Write A = 50 -->
  <path d="M 160 210 L 400 210" stroke="#333" stroke-width="2" fill="none" marker-end="url(#arrow3)"/>
  <rect x="210" y="195" width="130" height="25" rx="3" fill="white" stroke="#333" stroke-width="1"/>
  <text x="275" y="212" text-anchor="middle" font-family="Arial, sans-serif" font-size="12">Write A = 50</text>

  <!-- T2: Read A = 50 (Dirty Read!) -->
  <path d="M 640 250 L 400 250" stroke="#F44336" stroke-width="2" fill="none" marker-end="url(#arrow4)"/>
  <rect x="440" y="235" width="170" height="25" rx="3" fill="#ffebee" stroke="#F44336" stroke-width="2"/>
  <text x="525" y="252" text-anchor="middle" font-family="Arial, sans-serif" font-size="12" fill="#F44336" font-weight="bold">Read A = 50 (Dirty Read!)</text>

  <!-- Warning symbol for dirty read -->
  <circle cx="620" cy="250" r="12" fill="#F44336" stroke="none"/>
  <text x="620" y="255" text-anchor="middle" fill="white" font-family="Arial, sans-serif" font-size="16" font-weight="bold">!</text>

  <!-- T1: ROLLBACK -->
  <path d="M 160 290 L 400 290" stroke="#F44336" stroke-width="2" fill="none" marker-end="url(#arrow4)"/>
  <rect x="230" y="275" width="90" height="25" rx="3" fill="#ffebee" stroke="#F44336" stroke-width="2"/>
  <text x="275" y="292" text-anchor="middle" font-family="Arial, sans-serif" font-size="12" fill="#F44336" font-weight="bold">ROLLBACK</text>

  <!-- T2: Make decision based on A=50 (Incorrect!) -->
  <path d="M 640 330 L 400 330" stroke="#F44336" stroke-width="2" fill="none" marker-end="url(#arrow4)"/>
  <rect x="410" y="315" width="210" height="25" rx="3" fill="#ffebee" stroke="#F44336" stroke-width="2"/>
  <text x="515" y="332" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" fill="#F44336">Decision based on A=50 (Incorrect!)</text>

  <!-- T2: COMMIT -->
  <path d="M 640 370 L 400 370" stroke="#333" stroke-width="2" fill="none" marker-end="url(#arrow3)"/>
  <rect x="490" y="355" width="90" height="25" rx="3" fill="white" stroke="#333" stroke-width="1"/>
  <text x="535" y="372" text-anchor="middle" font-family="Arial, sans-serif" font-size="12">COMMIT</text>

  <!-- Explanation box -->
  <rect x="50" y="410" width="700" height="70" rx="5" fill="#fff3e0" stroke="#FF9800" stroke-width="2"/>
  <text x="400" y="435" text-anchor="middle" font-family="Arial, sans-serif" font-size="13" font-weight="bold" fill="#E65100">Problem: Transaction 2 reads uncommitted data from Transaction 1</text>
  <text x="400" y="455" text-anchor="middle" font-family="Arial, sans-serif" font-size="12" fill="#666">When T1 rolls back, T2 has already made decisions based on invalid data (A=50 instead of A=100).</text>
  <text x="400" y="470" text-anchor="middle" font-family="Arial, sans-serif" font-size="12" fill="#666">This violates isolation and can lead to data inconsistency.</text>

  <!-- Arrow marker definitions -->
  <defs>
    <marker id="arrow3" markerWidth="10" markerHeight="10" refX="9" refY="5" orient="auto">
      <polygon points="0 0, 10 5, 0 10" fill="#333"/>
    </marker>
    <marker id="arrow4" markerWidth="10" markerHeight="10" refX="9" refY="5" orient="auto">
      <polygon points="0 0, 10 5, 0 10" fill="#F44336"/>
    </marker>
  </defs>
</svg>

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

<svg viewBox="0 0 800 450" xmlns="http://www.w3.org/2000/svg">
  <!-- Background -->
  <rect width="800" height="450" fill="#f9f9f9" stroke="#ddd" stroke-width="1"/>

  <!-- Title -->
  <text x="400" y="30" font-family="Arial, sans-serif" font-size="16" font-weight="bold" fill="#333" text-anchor="middle">Durability: Surviving System Failures</text>

  <!-- Normal Operation Flow -->
  <text x="150" y="60" font-family="Arial, sans-serif" font-size="14" font-weight="bold" fill="#2196F3">Normal Operation</text>

  <!-- Client: COMMIT -->
  <rect x="50" y="80" width="120" height="40" rx="5" fill="#2196F3" stroke="#1976D2" stroke-width="2"/>
  <text x="110" y="105" text-anchor="middle" fill="white" font-family="Arial, sans-serif" font-size="13" font-weight="bold">Client: COMMIT</text>

  <!-- Arrow to Write to Transaction Log -->
  <path d="M 170 100 L 230 100" stroke="#333" stroke-width="2" fill="none" marker-end="url(#arrow5)"/>

  <!-- Write to Transaction Log -->
  <rect x="230" y="80" width="180" height="40" rx="5" fill="#4CAF50" stroke="#388E3C" stroke-width="2"/>
  <text x="320" y="105" text-anchor="middle" fill="white" font-family="Arial, sans-serif" font-size="13" font-weight="bold">Write to Transaction Log</text>

  <!-- Arrow to Acknowledgment -->
  <path d="M 410 100 L 470 100" stroke="#333" stroke-width="2" fill="none" marker-end="url(#arrow5)"/>

  <!-- Acknowledgment to Client -->
  <rect x="470" y="80" width="160" height="40" rx="5" fill="#4CAF50" stroke="#388E3C" stroke-width="2"/>
  <text x="550" y="105" text-anchor="middle" fill="white" font-family="Arial, sans-serif" font-size="13" font-weight="bold">ACK to Client</text>

  <!-- Asynchronous Write branch -->
  <path d="M 320 120 L 320 150" stroke="#333" stroke-width="2" fill="none" marker-end="url(#arrow5)"/>

  <!-- Asynchronous Write to Data Files -->
  <rect x="210" y="150" width="220" height="40" rx="5" fill="#FF9800" stroke="#F57C00" stroke-width="2"/>
  <text x="320" y="175" text-anchor="middle" fill="white" font-family="Arial, sans-serif" font-size="13">Async Write to Data Files</text>

  <!-- Separator line -->
  <line x1="50" y1="220" x2="750" y2="220" stroke="#666" stroke-width="1" stroke-dasharray="5,5"/>

  <!-- Crash Recovery Flow -->
  <text x="150" y="250" font-family="Arial, sans-serif" font-size="14" font-weight="bold" fill="#F44336">Crash Recovery</text>

  <!-- System Crash -->
  <g transform="translate(50, 270)">
    <rect width="120" height="40" rx="5" fill="#F44336" stroke="#D32F2F" stroke-width="2"/>
    <text x="60" y="25" text-anchor="middle" fill="white" font-family="Arial, sans-serif" font-size="13" font-weight="bold">System Crash</text>
    <!-- Crash icon -->
    <path d="M 40 5 L 50 15 L 45 15 L 55 25 L 45 15 L 50 15" fill="yellow" stroke="none"/>
    <path d="M 70 5 L 80 15 L 75 15 L 85 25 L 75 15 L 80 15" fill="yellow" stroke="none"/>
  </g>

  <!-- Arrow to Recovery Process -->
  <path d="M 170 290 L 230 290" stroke="#333" stroke-width="2" fill="none" marker-end="url(#arrow5)"/>

  <!-- Recovery Process -->
  <rect x="230" y="270" width="140" height="40" rx="5" fill="#9C27B0" stroke="#7B1FA2" stroke-width="2"/>
  <text x="300" y="295" text-anchor="middle" fill="white" font-family="Arial, sans-serif" font-size="13" font-weight="bold">Recovery Process</text>

  <!-- Arrow to Read Transaction Log -->
  <path d="M 370 290 L 430 290" stroke="#333" stroke-width="2" fill="none" marker-end="url(#arrow5)"/>

  <!-- Read Transaction Log -->
  <rect x="430" y="270" width="160" height="40" rx="5" fill="#9C27B0" stroke="#7B1FA2" stroke-width="2"/>
  <text x="510" y="295" text-anchor="middle" fill="white" font-family="Arial, sans-serif" font-size="13" font-weight="bold">Read Transaction Log</text>

  <!-- Arrow down -->
  <path d="M 510 310 L 510 340" stroke="#333" stroke-width="2" fill="none" marker-end="url(#arrow5)"/>

  <!-- Replay Committed Transactions -->
  <rect x="410" y="340" width="200" height="40" rx="5" fill="#9C27B0" stroke="#7B1FA2" stroke-width="2"/>
  <text x="510" y="365" text-anchor="middle" fill="white" font-family="Arial, sans-serif" font-size="13" font-weight="bold">Replay Committed Transactions</text>

  <!-- Arrow to final state -->
  <path d="M 410 360 L 350 360" stroke="#333" stroke-width="2" fill="none" marker-end="url(#arrow5)"/>

  <!-- Database Restored -->
  <rect x="150" y="340" width="200" height="40" rx="5" fill="#4CAF50" stroke="#388E3C" stroke-width="2"/>
  <text x="250" y="360" text-anchor="middle" fill="white" font-family="Arial, sans-serif" font-size="12" font-weight="bold">Database Restored to</text>
  <text x="250" y="375" text-anchor="middle" fill="white" font-family="Arial, sans-serif" font-size="12" font-weight="bold">Consistent State</text>

  <!-- Explanation boxes -->
  <rect x="650" y="80" width="130" height="110" rx="5" fill="#E3F2FD" stroke="#1976D2" stroke-width="1"/>
  <text x="715" y="100" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" font-weight="bold" fill="#1976D2">Key Points:</text>
  <text x="655" y="120" font-family="Arial, sans-serif" font-size="10" fill="#666">• Log written first</text>
  <text x="655" y="135" font-family="Arial, sans-serif" font-size="10" fill="#666">• Then ACK sent</text>
  <text x="655" y="150" font-family="Arial, sans-serif" font-size="10" fill="#666">• Data files later</text>
  <text x="655" y="165" font-family="Arial, sans-serif" font-size="10" fill="#666">• Log enables</text>
  <text x="665" y="180" font-family="Arial, sans-serif" font-size="10" fill="#666">recovery</text>

  <!-- Bottom explanation -->
  <rect x="50" y="400" width="700" height="40" rx="5" fill="#E8F5E9" stroke="#4CAF50" stroke-width="2"/>
  <text x="400" y="425" text-anchor="middle" font-family="Arial, sans-serif" font-size="12" font-weight="bold" fill="#2E7D32">Durability Guarantee: All committed transactions survive system failures through Write-Ahead Logging (WAL)</text>

  <!-- Arrow marker definition -->
  <defs>
    <marker id="arrow5" markerWidth="10" markerHeight="10" refX="9" refY="5" orient="auto">
      <polygon points="0 0, 10 5, 0 10" fill="#333"/>
    </marker>
  </defs>
</svg>

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

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <!-- Background -->
  <rect width="800" height="400" fill="#f9f9f9" stroke="#ddd" stroke-width="1"/>
  <!-- Title -->
  <text x="400" y="30" font-family="Arial, sans-serif" font-size="16" font-weight="bold" fill="#333" text-anchor="middle">Eventual Consistency in Distributed Systems</text>
  <!-- Write Operation -->
  <rect x="50" y="150" width="120" height="40" rx="5" fill="#2196F3" stroke="#1976D2" stroke-width="2"/>
  <text x="110" y="175" text-anchor="middle" fill="white" font-family="Arial, sans-serif" font-size="14" font-weight="bold">Write Operation</text>
  <!-- Arrows to database nodes -->
  <path d="M 170 170 L 250 120" stroke="#333" stroke-width="2" fill="none" marker-end="url(#arrow6)"/>
  <path d="M 170 170 L 250 170" stroke="#333" stroke-width="2" fill="none" marker-end="url(#arrow6)"/>
  <path d="M 170 170 L 250 220" stroke="#333" stroke-width="2" fill="none" marker-end="url(#arrow6)"/>
  <!-- Database Node 1 -->
  <g>
    <circle cx="280" cy="120" r="30" fill="#4CAF50" stroke="#388E3C" stroke-width="2"/>
    <text x="280" y="125" text-anchor="middle" fill="white" font-family="Arial, sans-serif" font-size="12" font-weight="bold">Node 1</text>
    <rect x="250" y="90" width="60" height="60" fill="none" stroke="none"/>
  </g>
  <!-- Database Node 2 -->
  <g>
    <circle cx="280" cy="200" r="30" fill="#4CAF50" stroke="#388E3C" stroke-width="2"/>
    <text x="280" y="205" text-anchor="middle" fill="white" font-family="Arial, sans-serif" font-size="12" font-weight="bold">Node 2</text>
    <rect x="250" y="170" width="60" height="60" fill="none" stroke="none"/>
  </g>
  <!-- Database Node 3 -->
  <g>
    <circle cx="280" cy="280" r="30" fill="#4CAF50" stroke="#388E3C" stroke-width="2"/>
    <text x="280" y="285" text-anchor="middle" fill="white" font-family="Arial, sans-serif" font-size="12" font-weight="bold">Node 3</text>
    <rect x="250" y="250" width="60" height="60" fill="none" stroke="none"/>
  </g>
  <!-- Sync arrows between nodes -->
  <!-- Node1 to Node2 -->
  <path d="M 295 145 Q 320 170 295 175" stroke="#FF9800" stroke-width="2" stroke-dasharray="3,3" fill="none" marker-end="url(#arrow7)"/>
  <text x="330" y="165" font-family="Arial, sans-serif" font-size="10" fill="#FF9800">Sync</text>
  <!-- Node2 to Node3 -->
  <path d="M 295 225 Q 320 250 295 255" stroke="#FF9800" stroke-width="2" stroke-dasharray="3,3" fill="none" marker-end="url(#arrow7)"/>
  <text x="330" y="245" font-family="Arial, sans-serif" font-size="10" fill="#FF9800">Sync</text>
  <!-- Node3 to Node1 -->
  <path d="M 265 255 Q 240 190 265 145" stroke="#FF9800" stroke-width="2" stroke-dasharray="3,3" fill="none" marker-end="url(#arrow7)"/>
  <text x="225" y="200" font-family="Arial, sans-serif" font-size="10" fill="#FF9800">Sync</text>
  <!-- Arrows to Eventually Consistent state -->
  <path d="M 310 120 L 450 170" stroke="#333" stroke-width="2" fill="none" marker-end="url(#arrow6)"/>
  <path d="M 310 200 L 450 200" stroke="#333" stroke-width="2" fill="none" marker-end="url(#arrow6)"/>
  <path d="M 310 280 L 450 230" stroke="#333" stroke-width="2" fill="none" marker-end="url(#arrow6)"/>
  <!-- Eventually Consistent -->
  <rect x="450" y="170" width="160" height="60" rx="10" fill="#9C27B0" stroke="#7B1FA2" stroke-width="2"/>
  <text x="530" y="195" text-anchor="middle" fill="white" font-family="Arial, sans-serif" font-size="14" font-weight="bold">Eventually</text>
  <text x="530" y="215" text-anchor="middle" fill="white" font-family="Arial, sans-serif" font-size="14" font-weight="bold">Consistent</text>
  <!-- Timeline visualization -->
  <g transform="translate(650, 100)">
    <text x="0" y="0" font-family="Arial, sans-serif" font-size="12" font-weight="bold" fill="#666">Timeline</text>
    <!-- Timeline arrow -->
    <path d="M 0 20 L 0 200" stroke="#666" stroke-width="2" fill="none" marker-end="url(#arrow8)"/>
    <text x="10" y="215" font-family="Arial, sans-serif" font-size="10" fill="#666">Time</text>
    <!-- States over time -->
    <circle cx="0" cy="40" r="4" fill="#F44336"/>
    <text x="15" y="45" font-family="Arial, sans-serif" font-size="10" fill="#666">Write occurs</text>
    <circle cx="0" cy="80" r="4" fill="#FF9800"/>
    <text x="15" y="85" font-family="Arial, sans-serif" font-size="10" fill="#666">Inconsistent</text>
    <circle cx="0" cy="120" r="4" fill="#FFC107"/>
    <text x="15" y="125" font-family="Arial, sans-serif" font-size="10" fill="#666">Syncing...</text>
    <circle cx="0" cy="160" r="4" fill="#4CAF50"/>
    <text x="15" y="165" font-family="Arial, sans-serif" font-size="10" fill="#666">Consistent</text>
  </g>
  <!-- Explanation box -->
  <rect x="50" y="340" width="700" height="50" rx="5" fill="#FFF3E0" stroke="#FF9800" stroke-width="2"/>
  <text x="400" y="360" text-anchor="middle" font-family="Arial, sans-serif" font-size="12" font-weight="bold" fill="#E65100">BASE Model: Eventually all nodes converge to the same state</text>
  <text x="400" y="378" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" fill="#666">Trade-off: Higher availability and partition tolerance at the cost of immediate consistency</text>
  <!-- Arrow marker definitions -->
  <defs>
    <marker id="arrow6" markerWidth="10" markerHeight="10" refX="9" refY="5" orient="auto">
      <polygon points="0 0, 10 5, 0 10" fill="#333"/>
    </marker>
    <marker id="arrow7" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
      <polygon points="0 0, 8 4, 0 8" fill="#FF9800"/>
    </marker>
    <marker id="arrow8" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
      <polygon points="0 0, 8 4, 0 8" fill="#666"/>
    </marker>
  </defs>
</svg>

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
