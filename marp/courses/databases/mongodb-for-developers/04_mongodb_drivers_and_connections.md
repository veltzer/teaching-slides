---
tags:
  - databases:mongodb
level: intermediate
category: databases
audience:
  - audiences:developers

---
# MongoDB Drivers and Connections

---
## What This Chapter Covers

- Official drivers
- Connection strings
- Connection pooling
- Replica set awareness
- Retries
- Read preferences

---
## Official Drivers

- Python (pymongo / motor for async)
- Node.js (mongodb)
- Java (mongodb-driver-sync / async)
- C# (.NET driver)
- Go (mongo-go-driver)
- Each maintained by MongoDB Inc.

---
## Connection String

```misc
mongodb://user:pass@host1,host2,host3/db?replicaSet=rs0
```

- Multiple hosts for replica awareness
- replicaSet: name of the cluster
- TLS, auth, timeouts as params

---
## srv-Style URL

```misc
mongodb+srv://user:pass@cluster.mongodb.net/db
```

- DNS-based; one entry expands to many hosts
- Standard for Atlas
- Easier to maintain across cluster changes

---
## Connection Pool

- Driver maintains a pool of TCP connections
- Default: 100
- Reused across requests
- Tune for high concurrency

---
## Replica Set Awareness

- Driver knows: primary, secondaries, arbiter
- Auto-routes writes to primary
- Reads: primary by default; configurable
- Detects failover; reconnects

---
## Read Preferences

- `primary`: default; strongest consistency
- `primaryPreferred`: primary unless unavailable
- `secondary`: from secondary (eventual consistency)
- `secondaryPreferred`: secondary unless unavailable
- `nearest`: lowest network latency

---
## Write Concern

- `w: 1`: primary acks (default)
- `w: majority`: majority of replicas ack (durable)
- `w: 0`: fire-and-forget
- `journaled: true`: written to journal
- Match to data importance

---
## Retries

- Modern drivers: retryable writes by default
- Network blip: retry once
- Idempotent operations
- Set `retryWrites=true` (default in modern drivers)

---
## Timeouts

- `socketTimeout`: TCP-level
- `connectTimeout`: initial connect
- `serverSelectionTimeout`: how long to wait for a usable server
- Tune to your environment

---
## Bulk Operations

- Batch many ops in one call
- `insertMany`, `updateMany`, `deleteMany`
- Or: bulkWrite for mixed operations
- Massively faster for large batches

---
## Async Drivers

- motor (Python), mongodb (Node), reactive streams (Java)
- Non-blocking I/O
- Higher concurrency
- Match your app's concurrency model

---
## Connection Per Process

- One MongoClient per process
- Reused across all operations
- Don't create / destroy per request
- Pool handles concurrency

---
## Common Driver Mistakes

- New connection per request
- No retries (network blips kill operations)
- Reading from primary always (waste of replicas)
- Wrong write concern (data loss risk)
- No timeouts (apps hang on issues)
