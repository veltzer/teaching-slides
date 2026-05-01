---
tags:
  - tools:rabbitmq
  - data-and-ai:amqp
level: intermediate
category: message-queue
audience:
  - audiences:developers

---
# Introduction to RabbitMQ and AMQP

---
## What This Chapter Covers

- Message broker concepts
- The AMQP protocol
- RabbitMQ's architecture
- Installation and the management UI
- A first end-to-end message flow
- Where RabbitMQ fits

---
## What a Message Broker Is

- A server that mediates messages between producers and consumers
- Producers don't know who consumes
- Consumers don't know who produces
- Broker handles routing, persistence, delivery
- Decouples sender and receiver in time and space

---
## Why Use a Broker

- Asynchronous processing (web request returns fast; work happens later)
- Buffering during traffic spikes
- Multiple subscribers without code changes
- Cross-language integration
- Reliability via persistence and acks

---
## What AMQP Is

- Advanced Message Queuing Protocol
- A wire-level protocol; multiple implementations
- Defines: exchanges, queues, bindings, messages, acks
- AMQP 0.9.1 is what RabbitMQ implements
- AMQP 1.0 exists but is a different protocol entirely (RabbitMQ supports it via plugin)

---
## RabbitMQ vs Kafka

- RabbitMQ: rich routing, per-message ack, RPC, smaller messages
- Kafka: high throughput, replay, log model, larger messages
- RabbitMQ for: workflow orchestration, RPC, pub/sub with complex routing
- Kafka for: streaming, event sourcing, log aggregation
- Both can do many things; pick by primary need

---
## RabbitMQ Architecture

- **Broker**: the server (or cluster of servers)
- **Connection**: TCP between client and broker
- **Channel**: lightweight session within a connection
- **Exchange**: receives published messages
- **Queue**: holds messages for consumers
- **Binding**: rule connecting exchange to queue

---
## Connections vs Channels

- One Connection per process (TCP is expensive)
- Many Channels per Connection (lightweight)
- Each thread gets its own Channel
- Channels are not thread-safe; share Connections, not Channels
- A common beginner mistake: too many Connections

---
## Installation

```bash
# Docker (easiest for dev)
docker run -d --name rabbit \
  -p 5672:5672 -p 15672:15672 \
  rabbitmq:3-management
```

- Port 5672: AMQP
- Port 15672: management web UI
- Production: install via package or use a managed service

---
## The Management UI

- Web UI at http://host:15672 (default user: guest/guest, localhost only)
- Inspect connections, channels, exchanges, queues, bindings
- Publish and consume messages manually
- Monitor: messages/second, memory, disk
- Indispensable for development and ops

---
## A First Message Flow

```python
import pika
conn = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
ch = conn.channel()
ch.queue_declare(queue='hello')
ch.basic_publish(exchange='', routing_key='hello', body='Hello!')
conn.close()
```

- Connect, get channel, declare queue, publish, close
- `exchange=''` uses the default exchange
- `routing_key='hello'` routes to queue named 'hello'

---
## Consuming The Message

```python
import pika
conn = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
ch = conn.channel()
ch.queue_declare(queue='hello')

def callback(ch, method, properties, body):
    print(f"Received: {body}")

ch.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)
ch.start_consuming()
```

- `auto_ack=True`: ack on receive (lossy if processing fails)
- For real apps: manual ack after processing

---
## Default Exchange

- Every queue is automatically bound to the default exchange
- Routing key = queue name &#8594; goes to that queue
- Useful for simple "send to a specific queue" patterns
- Custom exchanges give you routing flexibility

---
## What's Stored

- Messages in queues, until consumed (or expired, or queue purged)
- Configurations (exchanges, queues, bindings) survive broker restarts when *durable*
- Non-durable: lost on restart (useful for transient streams)
- Memory + disk; broker pages out to disk under pressure
- Persistence is per-message and per-queue

---
## Where RabbitMQ Wins

- Complex routing rules
- RPC patterns (request-reply with correlation IDs)
- Per-message TTL, priorities, dead-lettering
- Tight integration with sub-millisecond ack latencies
- A wide language ecosystem (every major language has a client)

---
## Where Other Tools Win

- Kafka: high-throughput streaming, replay
- NATS: ultra-low latency, simpler model
- AWS SQS / SNS: managed, simple, no ops
- Pulsar: Kafka-like with multi-tenancy
- Pick by: throughput, ops complexity, vendor preference

---
## Common Mistakes

- One Connection per message (TCP overhead)
- One Channel per Connection (no parallelism)
- Sharing a Channel across threads
- Auto-ack in production (lose messages on consumer crash)
- Not declaring exchanges/queues at startup &#8594; race conditions
