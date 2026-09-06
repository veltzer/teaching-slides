---
tags:
- concepts:idempotency
- concepts:api-design
- concepts:reliability
level: intermediate
category: architecture
audience:
- audiences:developers

---

# Idempotency in Web Services
## Building Reliable APIs
## Mark Veltzer
## [mark.veltzer@gmail.com](mailto:mark.veltzer@gmail.com)

---

## What is Idempotency?

![title](svg/lectures/architecting/idempotency/title.svg)

---

## What is Idempotency?: Overview

**Idempotent**: An operation that can be performed multiple times with the same result.

> "No matter how many times you call it, the outcome is the same"

Mathematical example: `f(f(x)) = f(x)`

---

## Why Does Idempotency Matter?

- **Network failures** are inevitable
- **Timeouts** cause uncertainty
- **Retry mechanisms** are essential
- **Double-clicks** happen
- **Distributed systems** amplify these issues

Without idempotency: chaos and data corruption

---

## Real-World Example: Payment Processing

![real_world_example_payment_processing](svg/lectures/architecting/idempotency/real_world_example_payment_processing.svg)

---

## Real-World Example: Payment Processing: Overview

**With idempotency**: Second click is safe, only one $100 charge

---

## HTTP Methods and Idempotency

| Method | Idempotent?  | Safe? |
|--------|--------------|-------|
| GET    | Yes          | Yes   |
| HEAD   | Yes          | Yes   |
| PUT    | Yes          | No    |
| DELETE | Yes          | No    |
| POST   | No           | No    |
| PATCH  | Not required | No    |

Idempotency of PATCH depends on the patch semantics (e.g., JSON Patch can be; "add 1 to counter" is not).

---

## The POST Problem

```http
POST /api/orders
{
  "product_id": 123,
  "quantity": 2,
  "total": 50.00
}
```

Each call creates a **new order**
- First call: Order #1001
- Second call: Order #1002
- Third call: Order #1003

---

## Idempotency Keys: The Solution

```http
POST /api/orders
Idempotency-Key: 550e8400-e29b-41d4-a716-446655440000

{
  "product_id": 123,
  "quantity": 2,
  "total": 50.00
}
```

Same key = same result, regardless of how many times called

---

## How Idempotency Keys Work

![how_idempotency_keys_work](svg/lectures/architecting/idempotency/how_idempotency_keys_work.svg)

---

## Key Generation Strategies

- **Client-generated (Recommended)**
```javascript
const key = crypto.randomUUID();
// 550e8400-e29b-41d4-a716-446655440000
```

- **Content-based**
```python
import hashlib
key = hashlib.sha256(json.dumps(request_data, sort_keys=True).encode()).hexdigest()
```

- **Timestamp + User ID**
```python
key = f"{user_id}:{timestamp}:{hash(request_content)}"
```

---

## Request Flow with Idempotency

![request_flow_with_idempotency](svg/lectures/architecting/idempotency/request_flow_with_idempotency.svg)

---

## Implementation Strategy

1. 1. 1. **Generate unique keys** (UUID, hash, etc.)
1. 1. 1. **Store key-response pairs** (database, cache)
1. 1. 1. **Check for existing keys** before processing
1. 1. 1. **Return cached response** if key exists
1. 1. 1. **Clean up old keys** periodically

---

## Implementing the Key Store

How you store the key-to-response mapping determines correctness, latency, and operational shape.

---

## What the Store Must Do

Regardless of the backend, the store provides three operations:

- **claim(key)** — atomic: reserves the key, returns false if someone else owns it
- **commit(key, response)** — durably records the response for future replays
- **get(key)** — returns the stored response, or "still in progress", or "unknown"

Plus two properties:

- **TTL** — keys eventually expire
- **Atomicity with the effect** — ideally `commit` and the business write happen in one transaction

The backend choice is about which properties you get natively and which you have to build.

---

## Basic Pattern (Storage-Agnostic)

```python
def handle_request(request, key):
    cached = store.get(key)
    if cached is not None:
        return cached

    if not store.claim(key):
        return store.wait_for_result(key)

    try:
        result = process_request(request)
        store.commit(key, result)
        return result
    except Exception:
        store.release(key)
        raise
```

Every backend in this chapter implements `claim` / `commit` / `get` differently. The caller doesn't change.

---

## Option 1: SQL Database

**Key idea**: use the database you already have. `INSERT ... ON CONFLICT` is your atomic claim, and the idempotency write lives in the same transaction as the business write.

This is the strongest guarantee available: the key and the effect commit or roll back together.

---

## SQL: Schema

```sql
CREATE TABLE idempotency_keys (
    key           VARCHAR(255) PRIMARY KEY,
    status        VARCHAR(16) NOT NULL,  -- 'pending' or 'done'
    response_code INTEGER,
    response_body TEXT,
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at    TIMESTAMP NOT NULL
);

CREATE INDEX idx_expires_at ON idempotency_keys(expires_at);
```

`status` lets us distinguish "someone is working on this" from "done, here's the response".

---

## SQL: Atomic Claim + Commit

```python
def handle_sql(conn, key, process):
    with conn.transaction():
        row = conn.execute(
            "INSERT INTO idempotency_keys (key, status, expires_at) "
            "VALUES (%s, 'pending', now() + interval '24 hours') "
            "ON CONFLICT (key) DO NOTHING RETURNING key",
            (key,)
        ).fetchone()

        if row is None:
            # Someone else claimed it — read their result
            return _read_existing(conn, key)

        # We own the key. Do the business write AND record the response
        # in the same transaction. Either both commit or both roll back.
        response = process(conn)
        conn.execute(
            "UPDATE idempotency_keys SET status='done', "
            "response_code=%s, response_body=%s WHERE key=%s",
            (response.code, response.body, key)
        )
        return response
```

---

## SQL: Why This Is the Gold Standard

No two-phase problem. The idempotency record and the business row share a transaction:

- Crash before commit → both disappear, retry gets a fresh shot
- Crash after commit → both present, retry reads the stored response
- There is no window where one exists without the other

**Cost**: every idempotent call costs a DB write. If your DB is already the bottleneck, look at Redis.

---

## Option 2: Redis

**Key idea**: fast, TTL-native, atomic `SET NX` for claim. Not transactional with your business DB — that's the tradeoff.

Right when the effect is cheap to repeat or when you're wrapping a service whose ledger you don't own.

---

## Redis: Claim + Commit

```python
import redis, json
r = redis.Redis()

def handle_redis(key, process):
    cached = r.get(f"idem:done:{key}")
    if cached:
        return json.loads(cached)

    # Atomic claim: SET ... NX EX succeeds only if the key doesn't exist
    claimed = r.set(f"idem:lock:{key}", "1", nx=True, ex=60)
    if not claimed:
        return _wait_for_result(key)

    try:
        response = process()
        # Commit: store the response with a long TTL, then release the lock
        r.set(f"idem:done:{key}", json.dumps(response), ex=86400)
        r.delete(f"idem:lock:{key}")
        return response
    except Exception:
        r.delete(f"idem:lock:{key}")
        raise
```

---

## Redis: The Two-Phase Problem

```python
response = process()                              # writes to business DB
r.set(f"idem:done:{key}", json.dumps(response))   # writes to Redis
```

What if the process crashes between these two lines?

- Business write committed
- Redis record missing
- Retry runs `process()` again → **double effect**

Redis cannot share a transaction with PostgreSQL. Mitigations: make `process()` itself idempotent (e.g., use the key as a unique constraint inside the business write), or accept that Redis-based idempotency has this window.

---

## Flask with Redis

```python
from flask import Flask, request, jsonify
import redis, json

app = Flask(__name__)
r = redis.Redis(host='localhost', port=6379, db=0)

@app.route('/api/orders', methods=['POST'])
def create_order():
    key = request.headers.get('Idempotency-Key')
    if not key:
        return jsonify({'error': 'Idempotency-Key required'}), 400

    cached = r.get(f"idem:{key}")
    if cached:
        return json.loads(cached)

    order = process_order(request.json)
    r.setex(f"idem:{key}", 86400, json.dumps(order))
    return jsonify(order)
```

Simple, but vulnerable to the two-phase problem above. Fine for low-stakes effects; risky for money.

---

## Option 3: Disk / Local File

**Key idea**: use filesystem atomicity primitives. Single-node only, but requires zero infrastructure — right for CLI tools, batch workers, single-host daemons.

The core trick: `open(O_CREAT | O_EXCL)` is atomic at the kernel level. Exactly one caller wins the race.

---

## Disk: The Durability Problem

A naive implementation is not crash-safe:

```python
def bad_commit(key, response):
    with open(f"/var/idem/{key}", "w") as f:
        f.write(json.dumps(response))
    # Process crashes here. File may be empty or partially written.
    # Page cache may not have flushed to disk yet.
```

Three things can go wrong:

- Crash mid-`write()` → truncated file
- Power loss after `write()` but before kernel flush → empty or zero-length file after reboot
- Reader sees a partially-written file between `open` and `close`

**Fix**: write to a temp file, `fsync`, then atomic `rename`.

---

## Disk: Crash-Safe Commit

```python
import os, json, tempfile

IDEM_DIR = "/var/idem"

def commit_disk(key, response):
    final = os.path.join(IDEM_DIR, key)
    # Write to temp file in the SAME directory (rename requires same filesystem)
    fd, tmp = tempfile.mkstemp(dir=IDEM_DIR, prefix=f".{key}.")
    try:
        with os.fdopen(fd, "w") as f:
            f.write(json.dumps(response))
            f.flush()               # flush stdio buffer to kernel
            os.fsync(f.fileno())    # flush kernel buffer to disk platters
        os.rename(tmp, final)       # atomic: either old file or new file, never partial
    except Exception:
        os.unlink(tmp)
        raise
```

After `os.rename` returns, readers see either no file or the complete new file. Never a half-written one.

---

## Disk: fsync the Directory Too

A subtle gotcha: `rename` updates the directory entry, but the *directory* itself is also a file on disk with its own buffer.

```python
def commit_disk_safe(key, response):
    final = os.path.join(IDEM_DIR, key)
    fd, tmp = tempfile.mkstemp(dir=IDEM_DIR, prefix=f".{key}.")
    with os.fdopen(fd, "w") as f:
        f.write(json.dumps(response))
        f.flush()
        os.fsync(f.fileno())
    os.rename(tmp, final)

    # fsync the directory to persist the rename itself
    dir_fd = os.open(IDEM_DIR, os.O_RDONLY)
    try:
        os.fsync(dir_fd)
    finally:
        os.close(dir_fd)
```

Without the directory fsync, a crash can leave you with the new file's contents on disk but no directory entry pointing to it.

---

## Disk: Atomic Claim with O_EXCL

```python
def claim_disk(key):
    lock_path = os.path.join(IDEM_DIR, f".lock.{key}")
    try:
        # O_CREAT | O_EXCL: kernel-level atomic "create if not exists"
        fd = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
        os.write(fd, str(os.getpid()).encode())
        os.fsync(fd)
        os.close(fd)
        return True
    except FileExistsError:
        return False
```

Exactly one caller per key wins `O_EXCL`. On release, `os.unlink(lock_path)`.

**Limitation**: single filesystem only. Two machines writing to the same NFS mount can both win `O_EXCL` depending on client caching. Use disk only when there's one writer host.

---

## Option 4: DynamoDB

**Key idea**: conditional writes give you atomic claim without running your own database. Native TTL handles expiration. Replicated across availability zones.

Right for serverless (Lambda) and high-scale multi-region deployments.

---

## DynamoDB: Atomic Claim

```python
import boto3, json, time
from botocore.exceptions import ClientError

table = boto3.resource('dynamodb').Table('idempotency')

def claim_dynamo(key):
    try:
        table.put_item(
            Item={
                'key': key,
                'status': 'pending',
                'ttl': int(time.time()) + 86400,  # DynamoDB native TTL
            },
            ConditionExpression='attribute_not_exists(#k)',
            ExpressionAttributeNames={'#k': 'key'},
        )
        return True
    except ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            return False
        raise
```

`ConditionExpression='attribute_not_exists(key)'` makes the write atomic: it either creates the item or fails. No locks, no transactions — the condition is evaluated on the storage node.

---

## DynamoDB: Commit and Transactions

```python
def commit_dynamo(key, response):
    table.update_item(
        Key={'key': key},
        UpdateExpression='SET #s = :done, response = :r',
        ExpressionAttributeNames={'#s': 'status'},
        ExpressionAttributeValues={':done': 'done', ':r': json.dumps(response)},
    )
```

For stronger guarantees, DynamoDB supports transactions across up to 100 items:

```python
client = boto3.client('dynamodb')
client.transact_write_items(TransactItems=[
    {'Put': {
        'TableName': 'orders',
        'Item': {'id': {'S': order_id}, ...},
    }},
    {'Update': {
        'TableName': 'idempotency',
        'Key': {'key': {'S': key}},
        'UpdateExpression': 'SET #s = :done',
        ExpressionAttributeNames={'#s': 'status'},
        ExpressionAttributeValues={':done': {'S': 'done'}},
    }},
])
```

Both writes commit together, or neither does. This is the SQL-gold-standard pattern on DynamoDB.

---

## Option 5: Kafka (Log-Compacted Topic)

**Key idea**: the idempotency key is the message key; Kafka's log compaction keeps only the latest record per key. The log *is* the store.

Right when you already have a Kafka-based architecture and want idempotency without adding new infrastructure.

---

## Kafka: The Setup

```bash
kafka-topics.sh --create \
  --topic idempotency \
  --config cleanup.policy=compact \
  --config min.cleanable.dirty.ratio=0.1 \
  --partitions 12
```

- **cleanup.policy=compact**: Kafka keeps only the latest value per key, forever
- Partitioned by key → same key always hits the same partition → ordering preserved
- Consumers rebuild state by replaying the compacted log

---

## Kafka: Producer-Side Deduplication

```python
from confluent_kafka import Producer

p = Producer({
    'bootstrap.servers': 'kafka:9092',
    'enable.idempotence': True,       # exactly-once for producer retries
    'transactional.id': 'orders-svc', # enables transactions
})
p.init_transactions()

def produce_order(key, order):
    p.begin_transaction()
    try:
        p.produce('orders', key=key, value=json.dumps(order))
        p.produce('idempotency', key=key, value=json.dumps({'status': 'done'}))
        p.commit_transaction()
    except Exception:
        p.abort_transaction()
        raise
```

Both records land atomically across both topics. Downstream consumers see all-or-nothing.

---

## Kafka: Consumer-Side Replay Check

```python
# Maintain an in-memory or RocksDB-backed view of the compacted topic
seen = {}  # key -> response

def on_idempotency_record(msg):
    seen[msg.key()] = json.loads(msg.value())

def handle_request(key, process):
    if key in seen:
        return seen[key]

    response = process()
    # Publishing to the compacted topic IS the commit
    p.produce('idempotency', key=key, value=json.dumps(response))
    p.flush()
    seen[key] = response
    return response
```

The Kafka log is the canonical key store; `seen` is just a materialized view. If the consumer crashes, it rebuilds by replaying the compacted topic from the beginning.

---

## Comparing the Five Backends

| Backend   | Atomic with business write | Crash-safe commit | Multi-node | Native TTL | Latency |
|-----------|---------------------------|-------------------|------------|------------|---------|
| SQL       | Yes (same txn)            | Yes               | Yes        | Manual     | ~1-5 ms |
| Redis     | No                        | Yes (AOF)         | Yes        | Yes        | <1 ms   |
| Disk      | No                        | Yes (with fsync)  | No         | Manual     | 1-10 ms |
| DynamoDB  | Yes (TransactWriteItems)  | Yes               | Yes        | Yes        | ~5-10 ms|
| Kafka     | Yes (cross-topic txn)     | Yes               | Yes        | No (compaction) | ~10 ms |

---

## Choosing a Backend

- **SQL** — you already have it, and the business write is in the same DB. Default choice.
- **Redis** — you need sub-millisecond lookups and can tolerate the two-phase problem, or the effect is naturally idempotent.
- **Disk** — single-host tools and workers. Zero external dependencies.
- **DynamoDB** — serverless, multi-region, or you're already on AWS and want managed infra.
- **Kafka** — event-driven architecture, idempotency is a natural fit with your existing log.

The best backend is usually the one you already operate. Don't add infrastructure for idempotency alone.

---

## Race Conditions Recap

Regardless of backend, two concurrent requests with the same key must produce one effect.

```python
def atomic_idempotent_check(key, process, max_wait=5.0):
    if not store.claim(key, ttl=30):
        # Lost the race — poll for the winner's result
        deadline = time.monotonic() + max_wait
        while time.monotonic() < deadline:
            cached = store.get(key)
            if cached:
                return cached
            time.sleep(0.1)
        raise TimeoutError(f"Idempotent request {key} still processing")

    try:
        result = process()
        store.commit(key, result)
        return result
    finally:
        store.release(key)
```

Every backend above implements `claim` atomically: SQL via `ON CONFLICT`, Redis via `SET NX`, disk via `O_EXCL`, DynamoDB via conditional writes, Kafka via transactional produce.

---

## Idempotency in Microservices

A request typically crosses several services:

`API Gateway → Order Service → Payment Service → Email Service`

Each hop can fail and retry independently.

- A retry at the gateway becomes N retries downstream
- Each service sees the same logical request as a fresh call
- Without coordination, one user click = multiple charges, multiple emails

**Rule**: idempotency must be enforced by the service that performs the real-world effect — not only at the edge.

---

## Push Idempotency Down to the Actor

The **actor** is the service that causes the side effect: charges a card, sends an email, ships a package, writes the canonical row.

- Edge-only keys protect against client double-clicks, not internal retries
- Middle services (routers, orchestrators) should **forward** the key, not consume it
- The actor checks the key against its own store, inside the same transaction as the effect

```diagram
Client ──key──▶ Gateway ──key──▶ Orchestrator ──key──▶ Payment (checks key here)
```

The key travels end-to-end. Only the actor has the authority to say "already done".

---

## Why the Actor Must Own the Check

```python
# WRONG: orchestrator checks, then calls payment
if already_processed(key):
    return cached
charge = payment_service.charge(amount)   # retry here = double charge
cache(key, charge)
```

The window between the check and the downstream call is a **double-charge window**. A crash, timeout, or retry in that window causes the exact problem idempotency was supposed to prevent.

```python
# RIGHT: forward the key, let payment decide
charge = payment_service.charge(amount, idempotency_key=key)
```

The payment service's check and its write to the ledger happen atomically. There is no window.

---

## Wrapping a Non-Idempotent Service

You don't always control the actor. Third-party APIs, legacy services, and vendor SDKs often lack idempotency support.

**Pattern**: put an idempotent wrapper in front of it.

---

## The Wrapper Pattern

![wrapper_pattern](svg/lectures/architecting/idempotency/wrapper_pattern.svg)

---

## Wrapper Responsibilities

The wrapper is a small service (or sidecar) that owns:

1. 1. 1. **Key storage** — durable record of `key → response`
1. 1. 1. **Single-flight** — only one in-flight call per key
1. 1. 1. **Result capture** — store what the legacy service returned
1. 1. 1. **Replay** — return the stored response on repeat

The legacy service stays untouched. The wrapper is the new source of truth for "did this already happen?".

---

## Wrapper Implementation

```python
def idempotent_call(key, legacy_call):
    cached = store.get(key)
    if cached is not None:
        return cached

    # Atomic: only one worker proceeds; others wait for the result
    if not store.claim(key, ttl=60):
        return store.wait_for_result(key, timeout=30)

    try:
        result = legacy_call()            # the non-idempotent call
        store.commit(key, result, ttl=86400)
        return result
    except Exception:
        store.release(key)                # let a retry try again
        raise
```

`claim` is an atomic `SET NX` — exactly one worker owns the key while the legacy call runs.

---

## The Dangerous Case: Crash Mid-Call

The legacy service charged the card, then the wrapper crashed before storing the result.

- The key is claimed but has no committed response
- A retry sees the claim and waits, then times out
- We **don't know** if the effect happened

Options:
- **Reconcile**: query the legacy service (`GET /charges?client_ref=key`) — requires the legacy API to accept your key as a lookup field
- **Manual review**: flag the key, alert an operator
- **Accept the risk**: only safe for low-stakes effects (emails, not payments)

There is no purely technical fix if the legacy service has no lookup by your key. This is the fundamental cost of wrapping instead of fixing.

---

## Wrapper vs. Fix the Actor

| | Wrapper | Fix the actor |
|---|---|---|
| Effort | Low | High (often impossible for 3rd party) |
| Correctness under crash | Requires reconciliation | Atomic with the effect |
| Latency | +1 hop | None |
| Scope | Per-caller | Global |

**Use a wrapper when** the actor is out of your control or the cost of changing it is prohibitive.
**Fix the actor when** you own it — the wrapper is always a second-best solution.

---

## Error Handling

```python
def handle_idempotent_request(key, request_data):
    try:
        cached = store.get(key)
        if cached:
            return cached

        result = process_request(request_data)

        # Only cache successful responses
        if result.status_code < 400:
            store.commit(key, result)

        return result

    except Exception as e:
        # Don't cache errors — let the retry try again
        log_error(e)
        raise
```

---

## Testing Idempotency

```python
def test_idempotent_order_creation():
    key = str(uuid.uuid4())
    order_data = {"product_id": 123, "quantity": 2}

    response1 = client.post('/api/orders',
                           json=order_data,
                           headers={'Idempotency-Key': key})

    response2 = client.post('/api/orders',
                           json=order_data,
                           headers={'Idempotency-Key': key})

    assert response1.status_code == 201
    assert response2.status_code == 201
    assert response1.json['id'] == response2.json['id']
    assert get_order_count() == 1  # Only one order created
```

---

## Common Pitfalls

- **Caching errors**
```python
# Wrong - caches 500 errors
store.commit(key, error_response)
```

- **No key validation**
```python
# Wrong - accepts any key format
idempotency_key = request.headers.get('key')
```

- **Infinite TTL**
```python
# Wrong - keys never expire
redis_client.set(key, response)  # No expiration
```

---

## Monitoring and Observability

- **Key Metrics**
    - Cache hit rate for idempotency keys
    - Key storage size and growth
    - Response time difference (cached vs fresh)
- **Alerting**
    - High cache miss rates
    - Storage capacity issues
    - Failed key lookups
- **Logging**
  ```python
    logger.info(f"Idempotency key {key}: {'HIT' if cached else 'MISS'}")
  ```

---

## Advanced Patterns

- **Conditional Idempotency**
```python
# Only idempotent for certain operations
if request.json.get('amount', 0) > 1000:
    require_idempotency_key()
```

- **Fingerprinting**
```python
# Generate key from request content
def generate_fingerprint(user_id, request_data):
    content = f"{user_id}:{json.dumps(request_data, sort_keys=True)}"
    return hashlib.sha256(content.encode()).hexdigest()
```

---

## Key Management Best Practices

- **Expiration**
    - Set reasonable TTL (24-48 hours typical)
    - Clean up expired keys regularly
- **Scope**
    - Keys should be scoped to user/tenant
    - Avoid global key conflicts
- **Durability**
    - Match store durability to the effect's reversibility
    - Money: SQL or DynamoDB transactions. Emails: Redis is fine.

---

## Key Takeaways

- **Always implement idempotency for state-changing operations**
- **Use client-generated UUIDs for keys**
- **Push the check down to the actor that performs the effect**
- **Pick a store that matches the effect's reversibility — SQL for money, Redis for cheap retries**
- **Store successful responses only**
- **Set appropriate TTL**
- **Test the retry path, not just the happy path**

Idempotency = reliability in distributed systems
