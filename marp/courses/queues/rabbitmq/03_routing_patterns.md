---
tags:
  - tools:rabbitmq
  - data-and-ai:routing
level: intermediate
category: message-queue
audience:
  - audiences:developers

---
# Routing Patterns

---
## What This Chapter Covers

- Direct routing for point-to-point
- Topic-based routing with wildcards
- Fanout for broadcast
- Headers exchange for attribute-based
- Combining patterns
- Choosing the right one for the job

---
## Direct Routing

- Routing key on message matches binding key on queue
- One key, one (or more) queues
- The simplest pattern
- Default exchange uses this implicitly
- Use for: routing logs by severity, jobs by type

---
## Routing Patterns

![routing_patterns](svg/courses/queues/rabbitmq/03_routing_patterns/routing_patterns.svg)

---
## Direct Routing Example

- Exchange `log` (type direct)
- Queues bound: `errors` (key `error`), `infos` (key `info`)
- `publish(exchange='log', routing_key='error', body=...)` &#8594; errors queue
- `publish(exchange='log', routing_key='info', body=...)` &#8594; infos queue
- Add a new queue with key `warning`: zero code changes elsewhere

---
## Topic Routing

- Routing keys are dotted strings: `category.subcategory.detail`
- Wildcards in binding keys:
    - `*` matches exactly one word
    - `#` matches zero or more words
- Routing decisions become declarative

---
## Topic Routing Example

- Routing keys for events: `user.signup.usa`, `order.placed.eu`, `user.login.uk`
- `user.*.*` matches `user.signup.usa`, `user.login.uk`
- `*.signup.*` matches `user.signup.usa`
- `#` matches everything
- `*.placed.eu` matches just `order.placed.eu`

---
## Topic Use Cases

- Logs by service and severity: `<service>.<severity>`
- Geographical events: `event.<region>.<type>`
- Hierarchical data: `org.<team>.<project>.<event>`
- Subscribers can be selective without producers knowing
- Most flexible without going to headers exchange

---
## Fanout Routing

- No routing logic; just broadcasts to all bindings
- Routing key is ignored
- Use when: every subscriber needs every message
- Notifications, audit logs, cache invalidation
- Simple and predictable

---
## Fanout Use Cases

- "User updated profile" &#8594; refresh cache, update search index, audit log
- All subscribers care; no filtering needed
- Adding a new subscriber: bind a new queue, no producer change
- Risk: large fanout exchanges fill many queues; watch memory

---
## Headers Routing

- Routing by message headers (key-value pairs)
- Binding specifies header rules
- `x-match: any` (any header matches) or `all` (all must match)
- Useful when routing dimensions don't fit dotted hierarchy
- Less common than topic; harder to reason about

---
## Headers Routing Example

- Headers binding: `{format: pdf, region: eu, x-match: all}`
- Message with headers `{format: pdf, region: eu, ...}` &#8594; matches
- Message with headers `{format: pdf, region: us, ...}` &#8594; doesn't
- Producer sets headers; broker routes
- Slower than topic for the same expressive power

---
## Combining Routing

- A topic exchange's matched message can be routed to *another* exchange
- Lets you compose routing logic
- Common: business-event topic exchange &#8594; per-team direct exchanges
- Diagrams help; code alone gets confusing
- Document the routing graph

---
## Round-Robin To Queue

- A queue with multiple consumers: messages distributed round-robin
- Each message goes to *one* consumer in the group
- The "competing consumers" pattern
- Scaling: add consumers to the same queue
- Watch: prefetch and ack must be tuned

---
## Pub-Sub Across Many Queues

- Fanout to N queues, each consumed by a different group
- Each group sees all messages
- Like Kafka consumer groups
- Common for: independent services reacting to the same event

---
## Pub-Sub With Filtering

- Topic exchange + each subscriber binds with their pattern
- Each subscriber sees only what they care about
- Producer publishes to one place; broker filters
- Cleaner than client-side filtering
- The most common production pattern

---
## Anti-Pattern: Routing in Code

- Producer code that picks the queue name based on logic
- Tightly couples producer to consumer topology
- Adding a new consumer requires producer changes
- Use exchanges + bindings instead
- Producer publishes to a topic; consumers self-route via bindings

---
## A Decision Tree

- Same destination always? &#8594; direct (or default exchange)
- Many subscribers, all see everything? &#8594; fanout
- Subscribers see different subsets based on pattern? &#8594; topic
- Subscribers select by message metadata? &#8594; headers
- Most teams: direct or topic; rarely the other two

---
## Common Routing Mistakes

- Hardcoded routing keys (typos lurk)
- Overlapping topic patterns (messages duplicated)
- Fanout when topic was needed
- Routing logic split between producer and broker
- No diagram of the topology — nobody can keep it in their head
