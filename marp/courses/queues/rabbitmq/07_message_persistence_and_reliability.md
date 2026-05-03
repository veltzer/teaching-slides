---
tags:
  - tools:rabbitmq
  - concepts:reliability
level: intermediate
category: message-queue
audience:
  - audiences:developers

---
# Message Persistence and Reliability

---
## Three Layers of Durability

![durability](svg/courses/queues/rabbitmq/07_message_persistence_and_reliability/durability.svg)

---
## Publisher Confirms

![publisher_confirms](svg/courses/queues/rabbitmq/07_message_persistence_and_reliability/publisher_confirms.svg)

---
## What This Chapter Covers

- Durable queues and persistent messages
- Publisher confirms
- Consumer acknowledgements
- Transactions vs publisher confirms
- High-availability queues and mirroring
- A reliability checklist

---
## Three Levels of Reliability

- **Best-effort**: fast, no guarantees
- **At-most-once**: may lose; never duplicates
- **At-least-once**: may duplicate; never lose
- **Exactly-once**: every message processed once
- RabbitMQ offers at-least-once with care; exactly-once needs idempotency

---
## Durable Queues

- `queue_declare(durable=True)`
- Survives broker restart
- Without it: queue gone after restart
- For any queue you depend on: durable
- Doesn't make messages persistent; you need both

---
## Persistent Messages

- `properties=BasicProperties(delivery_mode=2)`
- Tells broker to write to disk
- Survives restart (combined with durable queue)
- Without it: messages lost on restart
- Write performance lower; reliability higher

---
## Both Are Required

- Durable queue + non-persistent message: queue survives, messages don't
- Non-durable queue + persistent message: queue gone &#8594; messages too
- For full durability: both
- Most production setups: both
- Default to both unless you have a reason

---
## Publisher Confirms

- Producer asks the broker: "did you persist this?"
- `confirm_select` then publish
- Broker sends ack/nack per message (or batch)
- Without confirms: producer can't tell if persist failed
- The producer-side reliability mechanism

---
## Setting Up Confirms

```python
ch.confirm_delivery()   # enables confirms

if ch.basic_publish(exchange='', routing_key='q', body='msg', mandatory=True):
    # ack received
    pass
else:
    # nack received; message not stored
    handle_failure()
```

- `mandatory=True`: also returns if no queue accepted the message
- Synchronous; high overhead per message

---
## Async Confirms

- Don't wait per message
- Track outstanding `delivery_tag`s
- Get an async ack/nack callback
- Higher throughput than sync
- Used in production high-throughput pipelines

---
## Consumer Acknowledgements

- Consumer must ack to remove from queue
- `auto_ack=True`: automatic; lose-on-crash
- `auto_ack=False`: manual; safer
- Ack *after* processing
- The consumer-side reliability mechanism

---
## Manual Ack Pattern

```python
def callback(ch, method, properties, body):
    try:
        process(body)
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

ch.basic_consume(queue='q', on_message_callback=callback, auto_ack=False)
```

---
## Transactions

- AMQP supports transactions: `tx_select`, publish, `tx_commit`
- Atomic: all messages persist or none do
- Slow: 100x slower than non-transactional
- Mostly historical; publisher confirms preferred today
- Use only if you absolutely need cross-message atomicity

---
## Publisher Confirms vs Transactions

- Both ensure broker received and persisted the message
- Confirms are async-friendly and fast
- Transactions are sync and slow
- Almost everyone uses confirms now
- Transactions are an old API; aware-of, not used-by-default

---
## High Availability: Mirrored Queues

- Old approach (RabbitMQ < 3.8): queue mirrored across brokers
- One leader, N followers
- Leader crash &#8594; follower promoted
- Configurable via policies
- Some performance hit; brittleness in network partitions

---
## Quorum Queues (Modern)

- Replacement for mirrored queues since RabbitMQ 3.8
- Raft-based; better partition tolerance
- Persistent by design
- Recommended for new HA needs
- Some features differ; check compatibility

---
## When To Use Quorum

- Multi-broker cluster
- Messages must survive broker failure
- Throughput requirements within quorum capabilities
- Newer code; older clients work via standard AMQP
- Default for new HA queue declarations

---
## Lazy Queues

- Page messages to disk aggressively
- Lower memory use; some performance cost
- Useful for queues that may grow large
- `x-queue-mode=lazy`
- Combine with TTLs to prevent unbounded growth

---
## Network Partition Handling

- Cluster partitioned: brokers can't see each other
- Default: `pause_minority` — minority side stops accepting
- Alternative: `autoheal`, `ignore`
- Pick based on your CAP preference
- Test partition behaviour before production

---
## A Reliability Checklist

- [ ] Durable queues
- [ ] Persistent messages
- [ ] Manual ack
- [ ] Publisher confirms
- [ ] DLX for failed messages
- [ ] HA queues (quorum) for critical workloads
- [ ] Monitoring for queue depths and broker health

---
## Trade-Offs

- Reliability has a throughput cost
- Persistent messages: 5-10x slower than non-persistent
- Confirms add latency (mitigated by async)
- HA replication adds network and CPU cost
- Pick the level your business needs

---
## Common Reliability Mistakes

- "We have RabbitMQ; messages won't be lost" — without durable + persistent + ack, they will
- Confirming once per message synchronously &#8594; throughput tank
- HA without quorum &#8594; old mirrored-queue gotchas
- No DLX &#8594; broken messages stuck in queue
- No monitoring &#8594; reliability problems unseen
