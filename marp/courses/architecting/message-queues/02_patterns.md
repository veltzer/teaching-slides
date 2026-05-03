---
tags:
  - architecting:patterns
  - queues:overview
level: intermediate
category: architecting
audience:
  - audiences:architects
  - audiences:developers

---
# Messaging Patterns

---
## What This Chapter Covers

- Point-to-point
- Publish-subscribe
- Request-reply
- Competing consumers
- Dead-letter queues

---
## Point-to-Point

- One queue
- One consumer per message
- Load balanced across workers
- Classic work queue

---
## Pattern Catalog

![messaging_patterns](svg/courses/architecting/message-queues/02_patterns/messaging_patterns.svg)

---
## Publish-Subscribe

- Topic, not queue
- Each subscriber gets every message
- Independent failures
- Filtered subscriptions optional

---
## Queue vs Topic

![queue_vs_topic](svg/courses/architecting/message-queues/02_patterns/queue_vs_topic.svg)

---
## Fan-Out

- One producer, many consumers
- Often used with topics
- Can also use multiple queues
- Add subscribers without producer change

---
## Fan-In

- Many producers, one queue
- Aggregator pattern
- Watch for ordering
- Watch for hot keys

---
## Request-Reply

- Producer sends request
- Includes reply queue
- Consumer responds there
- Adds latency, useful for sync

---
## Correlation IDs

- Tag each message
- Match request to reply
- Trace across hops
- Standard for debugging

---
## Competing Consumers

- Multiple consumers on one queue
- Broker assigns work
- Linear scaling under load
- Hot keys break it

---
## Worker Pool

- Stateless workers
- Pull from queue
- Scale by worker count
- Idempotent processing

---
## Dead-Letter Queue

- Messages that fail too many times
- Inspect manually
- Replay after fix
- Required in production

---
## Retry With Backoff

- Transient failures retry
- Exponential backoff
- Cap on retries
- Then dead-letter

---
## Delayed Delivery

- Schedule for later
- Useful for retries
- Useful for reminders
- Native in some brokers

---
## Priority Queues

- Urgent messages first
- Often abused
- Use sparingly
- Prefer separate queues

---
## Message Routing

- By topic
- By key
- By header
- Routing logic in broker

---
## Common Pattern Mistakes

- Reply queue per request
- Ignoring correlation IDs
- No dead-letter queue
- No backoff
- Unbounded retries
