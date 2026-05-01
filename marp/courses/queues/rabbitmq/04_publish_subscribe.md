---
tags:
  - tools:rabbitmq
  - concepts:pub-sub
level: intermediate
category: message-queue
audience:
  - audiences:developers

---
# Publish/Subscribe

---
## What This Chapter Covers

- The pub/sub pattern with fanout
- Filtering messages with topic exchanges
- Consumer groups vs competing consumers
- Pub/sub vs Kafka pub/sub
- Pub/sub patterns in practice
- Common pitfalls

---
## What Pub/Sub Is

- One producer publishes a message
- Many subscribers receive copies
- Producer doesn't know subscribers
- Subscribers don't know producer
- Loose coupling at the messaging layer

---
## Fanout Pub/Sub

- Producer publishes to a fanout exchange
- N queues bound to that exchange
- Each queue gets a copy
- Each queue may have its own consumers
- Standard fan-out pattern

---
## Fanout Setup

```python
ch.exchange_declare(exchange='events', exchange_type='fanout')
ch.queue_declare(queue='audit')
ch.queue_declare(queue='analytics')
ch.queue_bind(queue='audit',     exchange='events')
ch.queue_bind(queue='analytics', exchange='events')

ch.basic_publish(exchange='events', routing_key='', body='user_signed_up')
```

- Both `audit` and `analytics` get the message
- Add a third queue: bind it; no producer change

---
## Topic Pub/Sub With Filtering

- Producer publishes with a routing key
- Subscribers bind queues with patterns
- Each subscriber sees only matching messages
- More efficient than fanout + client-side filter

---
## Topic Pub/Sub Example

```python
ch.exchange_declare(exchange='events', exchange_type='topic')
ch.queue_bind(queue='audit',  exchange='events', routing_key='#')
ch.queue_bind(queue='alerts', exchange='events', routing_key='*.error')

ch.basic_publish(exchange='events', routing_key='auth.error', body='...')
# goes to BOTH (matches # and *.error)

ch.basic_publish(exchange='events', routing_key='auth.success', body='...')
# goes to ONLY audit
```

---
## Competing Consumers

- One queue, multiple consumers
- Messages distributed round-robin (default) or based on QoS prefetch
- Each message handled by *one* consumer
- For scaling work, not for fan-out
- Different from pub/sub

---
## Pub/Sub + Competing Consumers

- A queue per "consumer group"
- Each group has multiple competing consumers
- Each group gets all messages; within a group, work is shared
- Mirrors Kafka's consumer groups
- The common scalable pub/sub pattern

---
## Diagram In Words

- Producer &#8594; events exchange
- events &#8594; audit queue (consumed by audit-1, audit-2)
- events &#8594; analytics queue (consumed by analytics-1, analytics-2, analytics-3)
- audit and analytics each get every message
- Within a group, work is shared

---
## Pub/Sub vs Kafka Pub/Sub

- RabbitMQ: each subscriber needs its own queue (or queue group)
- Kafka: each consumer group reads from the same topic, tracks its own offset
- Kafka is more storage-efficient (one log, many readers)
- RabbitMQ is more flexible per-subscriber (TTL, priority, etc.)
- Different mental models; pick by need

---
## Late Subscribers

- RabbitMQ: subscribers see only messages published *after* they bind
- Kafka: subscribers can read from the beginning of retention
- For "history matters": Kafka is better
- For "current and forward": RabbitMQ is fine
- Workaround: durable queues that buffer until consumers connect

---
## Durable Subscribers

- Queue is durable; subscriber can disconnect and reconnect
- Messages published while disconnected wait in the queue
- Crash-resilient
- Mark queue durable; mark messages persistent
- Both required for full durability

---
## Ephemeral Subscribers

- Auto-delete queue; gone when consumer disconnects
- Useful for: live dashboards, temporary subscribers
- No backlog accumulation if consumer goes away
- Common pattern with `queue_declare(exclusive=True)`

---
## Slow Consumers

- A subscriber that can't keep up
- Messages back up in *its* queue
- Memory pressure on the broker
- Other subscribers unaffected (they have their own queues)
- This is *the* RabbitMQ pub/sub advantage over shared-queue brokers

---
## Backpressure

- When a queue fills:
    - `x-max-length`: drops oldest or rejects newest
    - `x-overflow=reject-publish`: producer gets a NACK
- Producer must handle the NACK (retry, log, drop)
- Without policy: queue grows until broker out-of-memory
- Always set max-length on pub/sub queues

---
## A Real-World Example

- Customer signs up
- `signups` exchange (fanout)
- Bound queues: `welcome-email`, `analytics`, `crm-sync`, `audit`
- Each consumed by a service
- Adding a `slack-notification` queue: zero changes elsewhere
- Adding a producer that emits signups too: zero changes to subscribers

---
## Common Pub/Sub Mistakes

- One queue, many subscribers expecting all to see all messages (it's competing-consumers)
- No queue length limits &#8594; broker dies
- Publishing without `mandatory=True` and getting silent drops
- Adding pub/sub later by changing producer code (use exchanges from day 1)
- Ignoring slow-consumer queues until they crash the broker
