---
tags:
  - architecture:system-design
  - architecture:queues
level: intermediate
category: architecture
audience:
  - audiences:developers

---

# Message Queues

---

## What This Chapter Covers

- Why queues
- Brokers: Kafka, RabbitMQ, SQS
- Producer / consumer patterns
- At-least-once vs exactly-once
- Dead letter queues
- Backpressure
- Common patterns

---

## Why Queues

- Decouple producer and consumer
- Buffer traffic spikes
- Asynchronous processing
- Reliable delivery
- Scale consumers independently

---

## Use Cases at a Glance

![queue_use_cases](svg/courses/architecting/system-design/06_message_queues/queue_use_cases.svg)

---

## When to Reach for One

![queue_uses](svg/courses/architecting/system-design/06_message_queues/queue_uses.svg)

---

## Queue Versus Log

![queue_vs_log](svg/courses/architecting/system-design/06_message_queues/queue_vs_log.svg)

---

## Kafka

- Distributed log
- High throughput
- Replay possible
- Stream processing native
- Best for: events, analytics

---

## RabbitMQ

- Traditional message broker
- AMQP protocol
- Per-message ack, routing
- Best for: workflow, RPC

---

## SQS

- AWS managed queue
- Simple, reliable
- No replay; no streaming
- Best for: AWS-native event-driven

---

## Producer-Consumer

- Producer puts messages on queue
- Consumer takes off, processes
- Multiple consumers: load balance
- Failed: retry or dead-letter

---

## At-Least-Once

- Default in most queues
- Message processed at least once
- May process more than once
- Consumer must be idempotent

---

## Exactly-Once

- Hard; usually approximated
- Kafka transactions provide this
- Most systems: at-least-once + idempotency
- Don't over-engineer for it

---

## Dead Letter Queues

- For messages that repeatedly fail
- Investigation; retry after fix
- Without it: poison messages block the queue
- Standard pattern

---

## Backpressure

- Producer faster than consumer
- Queue grows; eventually fills
- Solutions: throttle producer, drop, scale consumer
- Detect: queue depth metrics

---

## Patterns: Fan-Out

- One message; many consumers
- Pub/sub
- Each consumer has own queue
- Clean decoupling

---

## Patterns: Work Queues

- Many messages; multiple workers
- Each message processed once (by one worker)
- Scaling: add workers
- The classic batch processing pattern

---

## Patterns: Request-Reply

- Producer sends; expects reply
- Correlation ID matches reply to request
- More complex than fire-and-forget
- Used: RPC over queues

---

## Choosing A Queue

- Streaming, replay, high throughput: Kafka
- Routing, RPC, low-latency: RabbitMQ
- AWS: SQS for queue, SNS for fan-out, EventBridge for events
- Match to your use case

---

## Common Queue Mistakes

- Treating Kafka as RabbitMQ (or vice versa)
- No DLQ &#8594; poison messages stuck
- Not idempotent &#8594; retry causes bugs
- No backpressure handling
- Queue depth not monitored
