---
tags:
  - databases:mongodb
  - databases:transactions
level: intermediate
category: databases
audience:
  - audiences:developers

---

# Transactions and Data Consistency

---

## What This Chapter Covers

- Single-document atomicity
- Multi-document transactions
- Sessions
- Read / write concerns
- Causal consistency
- When to use; when not

---

## Single-Document Atomicity

- All MongoDB writes are atomic at the document level
- An update of nested fields: atomic
- Most apps don't need multi-document transactions
- Design schema to fit (embed related data)

---

## Transaction Scope

![transactions_scope](svg/courses/databases/mongodb-for-developers/09_transactions_and_data_consistency/transactions_scope.svg)

---

## Multi-Document Transactions

- Available since MongoDB 4.0 (replica sets) and 4.2 (sharded)
- ACID across multiple documents / collections
- Sessions wrap operations
- Performance cost: higher than single-doc

---

## Transaction Example

```python
with client.start_session() as session:
    with session.start_transaction():
        db.accounts.update_one({"_id": from_}, {"$inc": {"balance": -100}}, session=session)
        db.accounts.update_one({"_id": to}, {"$inc": {"balance": 100}}, session=session)
```

- Both succeed or both fail

---

## When To Use Transactions

- True multi-document atomicity required
- Money transfers
- Inventory + order in one go
- Multi-collection invariants

---

## When NOT To

- Single-document operations
- Operations that can use $set with embedded data
- High-throughput workloads (transactions slower)
- "Convenient" but unnecessary

---

## Consistency Choices

![consistency_choices](svg/courses/databases/mongodb-for-developers/09_transactions_and_data_consistency/consistency_choices.svg)

---

## Read Concerns

- `local`: latest data on this server (default)
- `majority`: data acknowledged by majority
- `linearizable`: strongest; slow
- Match to consistency need

---

## Write Concerns

- `w: 1`: primary acks
- `w: majority`: durable across replicas
- `w: 0`: fire-and-forget
- `journaled: true`: written to disk

---

## Causal Consistency

- "Read your writes" guarantee
- Achieved via session
- Use sessions for related operations
- Without: a write may not be visible on the next read from a secondary

---

## Sessions

```python
with client.start_session() as session:
    db.users.insert_one({"_id": 1}, session=session)
    user = db.users.find_one({"_id": 1}, session=session)
```

- Tied to operations
- Required for transactions
- Provides causal consistency

---

## Idempotency

- Network blip: client may retry
- Driver retries idempotent ops automatically
- Make custom retries idempotent (use unique IDs)
- Same as any distributed system

---

## Optimistic Concurrency

- "Read; modify; write with version check"
- `update_one({_id, version: 5}, {$set: ..., $inc: {version: 1}})`
- Atomic; no transaction needed
- A common alternative to transactions

---

## Watching For Conflicts

- Transactions can fail with TransientTransactionError
- Retry the whole transaction
- Driver helpers automate

---

## Performance Considerations

- Transactions: 100ms+ overhead easily
- Long transactions: hold resources
- Limit: 60 seconds default; 5 minutes max
- Keep them short

---

## Common Transaction Mistakes

- Using transactions for single-doc ops
- Long-running transactions
- Not handling TransientTransactionError
- Mixing transactional and non-transactional ops
- Expecting MongoDB to behave exactly like Postgres
