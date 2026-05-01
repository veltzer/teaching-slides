---
tags:
  - tools:rabbitmq
  - concepts:rpc
level: intermediate
category: message-queue
audience:
  - audiences:developers

---
# RPC With RabbitMQ

---
## What This Chapter Covers

- The request-reply pattern
- Correlation IDs and reply queues
- Synchronous vs asynchronous RPC
- Timeout handling and error propagation
- When to use RabbitMQ for RPC
- When *not* to

---
## What RPC Is

- Remote Procedure Call
- Caller sends a request; receives a reply
- Synchronous from caller's perspective (usually)
- Building block for service-to-service calls
- Many transports: HTTP, gRPC, AMQP, custom

---
## Why Use RabbitMQ For RPC

- The broker handles routing
- Workers can be added without client changes
- Built-in load balancing across workers
- Survives broker crashes (with persistence)
- Especially nice when you already use RabbitMQ for messaging

---
## Why NOT to Use RabbitMQ For RPC

- HTTP / gRPC are more common; better tooling
- Adds latency (extra hop)
- More moving parts to debug
- Most teams: use HTTP for sync calls, RabbitMQ for async
- RabbitMQ RPC fits when async is the natural model

---
## The Request-Reply Pattern

- Client publishes a request to a request queue
- Includes: a `reply_to` queue and a `correlation_id`
- Worker processes the request, publishes a reply to `reply_to` with the same `correlation_id`
- Client correlates the reply to the original request

---
## Correlation IDs

- A unique ID per request
- Worker echoes it back in the reply
- Client uses it to match reply to request
- Without it: client can't tell which reply is for which request
- Usually a UUID

---
## Reply Queues

- Where the reply lands
- Per-client, often per-connection
- Often `exclusive=True, auto_delete=True` (cleaned up automatically)
- "Direct reply-to" feature: a special pseudo-queue, no declaration needed

---
## A Simple RPC Client

```python
import uuid, pika

ch = ... # channel
result_q = ch.queue_declare(queue='', exclusive=True).method.queue

corr_id = str(uuid.uuid4())
response = {}

def on_reply(ch, method, props, body):
    if props.correlation_id == corr_id:
        response['body'] = body

ch.basic_consume(queue=result_q, on_message_callback=on_reply, auto_ack=True)

ch.basic_publish(
    exchange='',
    routing_key='rpc_queue',
    properties=pika.BasicProperties(reply_to=result_q, correlation_id=corr_id),
    body='compute me'
)

while 'body' not in response:
    ch.connection.process_data_events()
```

---
## A Simple RPC Worker

```python
def on_request(ch, method, props, body):
    result = compute(body)
    ch.basic_publish(
        exchange='',
        routing_key=props.reply_to,
        properties=pika.BasicProperties(correlation_id=props.correlation_id),
        body=str(result)
    )
    ch.basic_ack(delivery_tag=method.delivery_tag)

ch.basic_consume(queue='rpc_queue', on_message_callback=on_request)
```

- Echoes the correlation_id and routes to the reply_to queue

---
## Timeout Handling

- Worker may not respond (crashed, slow, never existed)
- Client must time out gracefully
- `select`-style wait with timeout
- On timeout: cancel, log, retry or escalate
- Without timeout: client hangs forever

---
## Error Propagation

- Worker failed mid-request
- Options:
    - Send an error reply (with the correlation_id)
    - Don't reply; client times out
- Sending error replies is cleaner
- Define an error contract (HTTP-style status, body)

---
## Async RPC

- Same pattern but caller doesn't block
- Submit request, return immediately
- Reply arrives later; trigger a callback
- Useful when caller has other work to do
- Forms the basis of orchestration patterns

---
## Direct Reply-To

- A RabbitMQ feature: `amq.rabbitmq.reply-to` pseudo-queue
- No queue declaration; no cleanup
- Faster (no queue setup overhead)
- Limitation: each consumer sees only their own replies
- Modern recommended approach for RPC

---
## Load Balancing

- Multiple workers consuming the same request queue
- Each request goes to *one* worker (round-robin / by prefetch)
- Add workers = more throughput
- The natural way to scale RPC backends
- One queue, N workers, each replying directly

---
## Idempotency

- Worker may process a request twice (retry, network glitch)
- Make handlers idempotent: same request &#8594; same result
- Or: dedupe on correlation_id
- Without idempotency, retries cause subtle bugs
- Pattern across all messaging, not just RPC

---
## When To Pick RabbitMQ RPC

- You're already using RabbitMQ for other messaging
- You want async submit + reply
- You want to load-balance across workers without an LB
- You want delivery guarantees stronger than HTTP
- You can tolerate the extra latency

---
## When To Pick HTTP / gRPC Instead

- Simple sync calls
- Strong typing required
- Better tooling (curl, Postman, OpenAPI)
- Lower latency requirements
- Most synchronous service-to-service: just use HTTP

---
## Common RPC Mistakes

- No timeout &#8594; clients hang
- No correlation_id &#8594; replies misrouted
- No idempotency &#8594; retries cause problems
- One reply queue across many requests &#8594; confusion
- Building RPC over RabbitMQ when HTTP would do
