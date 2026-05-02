---
tags:
  - tools:rabbitmq
  - infrastructure:integration
level: intermediate
category: message-queue
audience:
  - audiences:developers

---
# Client Libraries and Integration

---
## What This Chapter Covers

- RabbitMQ client libraries by language
- Connection and channel management
- Serialisation and message formats
- Web framework integration
- Microservices patterns
- Common integration pitfalls

---
## Major Client Libraries

- **Python**: pika (synchronous), aio-pika (async)
- **Java**: official `amqp-client`, RabbitMQ Java Client
- **Node.js**: amqplib, rascal (higher-level)
- **Go**: amqp091-go (community fork of amqp)
- **C#**: official `RabbitMQ.Client`
- **Ruby**: bunny

---
## Side by Side

![client_libraries](svg/courses/queues/rabbitmq/08_client_libraries_and_integration/client_libraries.svg)

---
## Higher-Level Frameworks

- **Spring AMQP** (Java): templated patterns, annotations
- **Celery** (Python): task queue built on top of RabbitMQ
- **MassTransit** (.NET): conventions over wire protocol
- **Sidekiq** (Ruby): similar idea, different broker often
- Higher-level frameworks save boilerplate

---
## Connection Management

- TCP connection: expensive (~1 second to open)
- Long-lived: open at startup, close at shutdown
- One connection per process is the rule
- Don't connect-per-message; *ever*
- Most libraries support connection pooling internally

---
## Channels

- Lightweight session within a connection
- Each thread / coroutine gets its own channel
- Channels are *not* thread-safe
- Cheap to create; can have hundreds per connection
- Close channels explicitly; leaks are common

---
## Reconnection

- Connections drop (network blip, broker restart)
- Library should reconnect automatically
- Recover topology: re-declare exchanges, queues, bindings
- Reattach consumers
- Most modern libraries handle this; older ones don't

---
## Serialisation

- AMQP carries opaque bytes
- You pick: JSON, Protobuf, Avro, MessagePack, plain bytes
- JSON: easy, human-readable, large
- Protobuf / Avro: compact, schema-managed, less debuggable
- Pick based on size, speed, schema-evolution needs

---
## JSON Example

```python
import json

ch.basic_publish(
    exchange='',
    routing_key='orders',
    body=json.dumps({'id': 42, 'total': 99.99}),
    properties=pika.BasicProperties(content_type='application/json')
)
```

- Set `content_type` so consumers know how to deserialise
- Easy to debug; verbose on the wire

---
## Protobuf Example

```python
import order_pb2

order = order_pb2.Order(id=42, total=99.99)
ch.basic_publish(
    exchange='',
    routing_key='orders',
    body=order.SerializeToString(),
    properties=pika.BasicProperties(content_type='application/x-protobuf')
)
```

- Compact; fast
- Requires a schema (.proto file)
- Schema evolution rules; easier than ad-hoc JSON

---
## Web Framework Integration

- **Flask + Celery**: defer slow work to background workers
- **Django + Celery**: same; ubiquitous in Django
- **Spring Boot + Spring AMQP**: declarative consumers
- **Express.js + amqplib**: manual; many wrappers exist
- Pattern: web request &#8594; publish job &#8594; respond fast; worker &#8594; consumes &#8594; processes

---
## A Web + Worker Pattern

- Web app: handle request, validate input, publish to queue, return 202 Accepted
- Worker: consume, do the actual work
- Web app stays fast; long jobs don't block requests
- Status of jobs: separate API or DB
- Standard pattern for emails, reports, processing

---
## Microservices Integration

- Each service has its own queues
- Pub/sub for events between services
- RPC for sync responses (when not using HTTP)
- The broker is shared infrastructure
- Choreography (events) often beats orchestration (RPC)

---
## Service Discovery

- Producer doesn't need to know consumer addresses
- Both connect to the broker
- The broker *is* the discovery mechanism
- Adding a new consumer: nothing changes for the producer
- Removing a consumer: nothing changes for the producer

---
## Schema Management

- Producers and consumers must agree on message format
- Schema registry (Confluent, Apicurio): central source of truth
- For RabbitMQ: less common; teams often coordinate manually
- Evolution: add fields (forward compatible), don't remove (backward incompatible)
- Versioning fields helps

---
## Connection Limits

- Each connection costs broker resources
- Default RabbitMQ limit: ~700 connections per Erlang process
- Plan capacity: how many connections per service?
- Monitor: connection count via management UI
- Surprise: a leak can take the broker down

---
## Channel Limits

- Per-connection channel limit (default 2047)
- Easy to leak channels
- Always close channels in `finally` blocks
- Monitor: channel count per connection
- Restart-and-redeploy patterns help bound growth

---
## TLS

- Encrypt the broker-client traffic
- AMQP over TLS: port 5671 (vs 5672 plain)
- Configure broker with cert; clients with cert + verification
- Required for compliance in many environments
- Rotate certs; many incidents are stale-cert related

---
## Authentication

- Default user: `guest/guest`, only from localhost
- Production: per-service users with limited permissions
- LDAP, OAuth, JWT plugins available
- vhosts isolate logical broker instances
- Apply principle of least privilege

---
## Common Integration Mistakes

- One connection per request (TCP overhead)
- Channels shared across threads (corruption)
- No reconnection logic
- Hardcoded broker URLs (use env config)
- Same `guest` credentials in production
