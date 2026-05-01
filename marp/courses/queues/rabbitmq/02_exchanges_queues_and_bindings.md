---
tags:
  - tools:rabbitmq
  - data-and-ai:amqp
level: intermediate
category: message-queue
audience:
  - audiences:developers

---
# Exchanges, Queues, and Bindings

---
## What This Chapter Covers

- Queue declaration and properties
- Exchange types: direct, fanout, topic, headers
- Bindings and routing keys
- The default exchange
- Custom exchange configuration
- A practical guide to choosing

---
## Queues

- Hold messages until consumed
- Properties: durable, exclusive, auto-delete, arguments
- Order: FIFO by default (mostly)
- One queue, many consumers possible (round-robin)
- One queue, one *message destination* per delivery

---
## Queue Declaration

```python
ch.queue_declare(
    queue='orders',
    durable=True,           # survives broker restart
    exclusive=False,        # accessible by other connections
    auto_delete=False       # don't delete when last consumer disconnects
)
```

- Idempotent: redeclaring with same args is fine
- Redeclaring with different args is an error
- Use durable=True for queues with messages you can't lose

---
## Queue Arguments

- `x-message-ttl`: messages expire after N ms
- `x-max-length`: cap queue length
- `x-dead-letter-exchange`: where to send rejected/expired messages
- `x-max-priority`: priority queue
- `x-queue-mode`: lazy (page to disk aggressively) or default

---
## Exchanges

- Producers publish to exchanges, not queues
- Exchanges route messages to queues based on bindings
- Four standard types: direct, fanout, topic, headers
- Exchange type defines the routing logic
- A single exchange may bind to many queues

---
## Direct Exchange

- Routes by exact match between routing key and binding key
- "send to queue.X" pattern
- Default exchange is a special direct exchange
- Use for: point-to-point messaging

---
## Direct Example

```python
ch.exchange_declare(exchange='direct.orders', exchange_type='direct')
ch.queue_bind(queue='shipping.q', exchange='direct.orders', routing_key='ship')
ch.queue_bind(queue='billing.q',  exchange='direct.orders', routing_key='bill')

ch.basic_publish(exchange='direct.orders', routing_key='ship', body='...')
# goes to shipping.q only
```

---
## Fanout Exchange

- Ignores routing key
- Sends every message to *every* bound queue
- Pure pub/sub
- Use for: broadcast to all subscribers

---
## Fanout Example

```python
ch.exchange_declare(exchange='events', exchange_type='fanout')
ch.queue_bind(queue='audit.q',     exchange='events')
ch.queue_bind(queue='analytics.q', exchange='events')

ch.basic_publish(exchange='events', routing_key='', body='user_signed_up')
# goes to BOTH queues
```

---
## Topic Exchange

- Routes by pattern matching on a dotted routing key
- Wildcards: `*` (one word), `#` (zero or more words)
- "user.signup.usa" matches "user.*.usa", "user.#", "*.signup.*"
- Use for: hierarchical/categorised events

---
## Topic Example

```python
ch.exchange_declare(exchange='log', exchange_type='topic')
ch.queue_bind(queue='errors.q',  exchange='log', routing_key='*.error')
ch.queue_bind(queue='auth.q',    exchange='log', routing_key='auth.#')

ch.basic_publish(exchange='log', routing_key='auth.error', body='login failed')
# goes to BOTH queues
```

---
## Headers Exchange

- Routes by message *headers*, not routing key
- "match all headers" or "match any header"
- More flexible than topic; less commonly needed
- Heavier per-message overhead
- Use only when topic isn't expressive enough

---
## Bindings

- The relationship between an exchange and a queue
- Binding key + routing key (for direct/topic) determines delivery
- Multiple bindings: a queue can receive from many exchanges
- Bindings are explicit; exchanges + queues + bindings are the routing rules

---
## The Default Exchange

- Pre-declared, type direct, name `""` (empty)
- Every queue is bound to it with the queue's name as binding key
- "Publish to default with routing_key='X'" &#8594; goes to queue X
- Useful for simple cases; doesn't scale to complex routing
- Don't rely on it for production routing logic

---
## Naming Conventions

- Exchanges: `exchange.<service>.<type>` or just `<service>.events`
- Queues: `<service>.<purpose>` (e.g., `orders.shipping`)
- Routing keys: `<entity>.<action>.<context>` (e.g., `user.signup.web`)
- Consistency makes ops easier
- Document the conventions for your project

---
## Choosing An Exchange Type

- One queue gets the message? &#8594; **direct**
- All queues get every message? &#8594; **fanout**
- Pattern-based (some get some, others get others)? &#8594; **topic**
- Match by message headers? &#8594; **headers**
- Most use cases: direct or topic

---
## Multi-Exchange Setups

- A producer publishes to one exchange
- That exchange may bind to another exchange (`exchange.bind`)
- Forms graphs of routing
- Used for: layered routing, gradual rollout, A/B testing
- Powerful; can be confusing — diagram before building

---
## Common Mistakes

- Publishing to queues directly (use exchanges instead)
- Using fanout when you need topic
- Topic with overly broad bindings (everyone gets everything)
- Different teams declaring overlapping exchanges
- Not naming exchanges and queues consistently
