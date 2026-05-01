---
tags:
  - tools:kafka
  - infrastructure:configuration
level: beginner
category: message-queue
audience:
  - audiences:developers

---
# Configuration

---
## What This Chapter Covers

- Broker configuration: the basics
- Producer configuration: the knobs that matter
- Consumer configuration: timing and behaviour
- New Producer specifics
- Configuration files in production
- The 80/20 of Kafka tuning

---
## Three Layers of Configuration

- **Broker**: cluster-wide and per-broker settings
- **Topic**: per-topic overrides (retention, replication)
- **Client**: producer and consumer per-instance
- Each layer overrides the layer above
- Most production tuning happens at client level

---
## Broker Config: The Basics

- `broker.id`: unique per broker
- `log.dirs`: where to store logs
- `num.network.threads`, `num.io.threads`: parallelism
- `default.replication.factor`: usually 3
- `min.insync.replicas`: usually 2
- `auto.create.topics.enable`: usually false in prod

---
## Replication Settings

- `replication.factor`: how many copies of each partition
- `min.insync.replicas`: how many must ack a write (with `acks=all`)
- Common: replication=3, min.isr=2 — survives one broker failure
- Higher replication = more durability + more cost
- These trade off carefully

---
## Topic Configuration

- `partitions`: parallelism (hard to change later)
- `replication.factor`: durability
- `retention.ms`: how long to keep messages (default 7 days)
- `retention.bytes`: per-partition size cap
- `cleanup.policy`: `delete` (time-based) or `compact` (key-based)

---
## Log Compaction

- Special retention: keep only the *latest* value per key
- Useful for: change-data capture, configuration topics
- Requires: keys on all messages
- Old values eventually deleted by the compactor
- `cleanup.policy=compact` enables it

---
## Retention Trade-offs

- Longer retention = more disk; more replay possible
- Shorter retention = less disk; less replay
- Most consumers want "long enough to recover from a multi-day outage"
- 7-30 days is typical
- Compacted topics keep state forever (per key)

---
## Producer Config: The Important Ones

- `bootstrap.servers`: comma-separated broker list
- `acks`: 0 / 1 / all
- `enable.idempotence`: true (always)
- `compression.type`: lz4 or zstd
- `linger.ms`, `batch.size`: throughput tuning
- `max.in.flight.requests.per.connection`: 5 default

---
## Producer Config: Reliability

- `retries`: how many retry attempts (default int max)
- `retry.backoff.ms`: between retries
- `delivery.timeout.ms`: total time to deliver (default 2 min)
- `request.timeout.ms`: per-request timeout
- With idempotence on, retries are safe

---
## "New Producer" Note

- Older Kafka had two producers: legacy and "new"
- Modern Kafka: only one producer (the "new" one)
- "Producer" and "New Producer" mean the same thing today
- The legacy SimpleProducer is gone
- Mentioned because old docs and tutorials may distinguish

---
## Consumer Config: The Important Ones

- `bootstrap.servers`
- `group.id`: which consumer group to join
- `auto.offset.reset`: earliest / latest / none
- `enable.auto.commit`: usually false in production code
- `max.poll.records`: batch size per poll
- `max.poll.interval.ms`: max time between polls before kicked from group

---
## Consumer Config: Timing

- `session.timeout.ms`: how long before broker considers consumer dead
- `heartbeat.interval.ms`: how often consumer pings broker
- Typical: heartbeat = 1/3 of session timeout
- `max.poll.interval.ms`: how long between polls before kicked
- Don't make these too tight; spurious rebalances follow

---
## Consumer Config: Performance

- `fetch.min.bytes`: server waits for this much data before responding
- `fetch.max.wait.ms`: max wait if not enough data
- `max.partition.fetch.bytes`: per-partition fetch size
- Tune these for batch size vs latency trade-off
- Defaults are usually fine

---
## Production Config Files

- Brokers: `server.properties`
- Producers / consumers: code or properties files
- Use environment variables for secrets
- Schema registry config separate
- Version-control everything

---
## A Sane Producer Profile

```properties
acks=all
enable.idempotence=true
compression.type=lz4
linger.ms=10
batch.size=32768
max.in.flight.requests.per.connection=5
```

- Durable, fast-enough, idempotent
- Good starting point for most production use

---
## A Sane Consumer Profile

```properties
group.id=my-service
enable.auto.commit=false
auto.offset.reset=earliest
max.poll.records=500
max.poll.interval.ms=300000
session.timeout.ms=45000
heartbeat.interval.ms=15000
```

- Manual commit, processes from start, generous timeouts
- Adjust per-service

---
## Topic Defaults vs Overrides

- Set sane cluster defaults
- Override per topic where needed
- `kafka-configs.sh --alter` to change
- Topic-level overrides survive broker restarts
- Document why each override exists

---
## Common Configuration Mistakes

- `acks=0` in production
- `enable.auto.commit=true` with manual processing logic
- Tight timeouts &#8594; rebalance storms
- Same `group.id` for unrelated services
- Not setting `min.insync.replicas` &#8594; durability surprises
