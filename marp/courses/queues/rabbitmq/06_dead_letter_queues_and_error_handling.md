---
tags:
  - tools:rabbitmq
  - concepts:error-handling
level: intermediate
category: message-queue
audience:
  - audiences:developers

---
# Dead Letter Queues and Error Handling

---
## DLQ Flow

![dlq_flow](svg/courses/queues/rabbitmq/06_dead_letter_queues_and_error_handling/dlq_flow.svg)

---
## What This Chapter Covers

- Dead letter exchanges and queues
- Message rejection and nacking
- Retry strategies
- Delayed requeuing
- Poison message handling
- A complete error-handling pattern

---
## Why Errors Need Special Handling

- A consumer may fail to process a message
- Retrying forever blocks the queue
- Dropping silently loses data
- A graceful pattern catches errors, retries some, dead-letters others
- Get this right; production reliability depends on it

---
## ack, nack, reject

- `basic_ack`: success; remove from queue
- `basic_nack`: failed; with `requeue=True` puts it back
- `basic_reject`: similar to nack but for one message
- nack is the modern preferred form
- Not acking forever &#8594; broker thinks you're slow; eventually redelivered

---
## Auto-Ack vs Manual Ack

- `auto_ack=True`: ack on receive
- Lost message if consumer crashes after receiving
- For production: manual ack after successful processing
- Comes at the cost of more code, but worth it
- Trade-off: complexity for reliability

---
## Dead Letter Exchanges (DLX)

- A normal exchange that receives "dead" messages
- Configured per-queue: messages go to DLX when:
    - Rejected (nack with requeue=False)
    - Expired (TTL)
    - Queue length limit hit
- Dead-lettered messages can be inspected, retried, or dropped

---
## Setting Up a DLX

```python
ch.exchange_declare(exchange='my.dlx', exchange_type='direct')
ch.queue_declare(queue='my.dlq')
ch.queue_bind(queue='my.dlq', exchange='my.dlx', routing_key='dead')

ch.queue_declare(
    queue='my.queue',
    arguments={
        'x-dead-letter-exchange': 'my.dlx',
        'x-dead-letter-routing-key': 'dead',
    }
)
```

- Failed messages from `my.queue` end up in `my.dlq`

---
## Retry Strategies

- **Immediate retry**: nack with requeue=True
- **Delayed retry**: dead-letter to a TTL queue, which dead-letters back
- **Limited retries**: count on the message; dead-letter after N
- **No retry**: nack with requeue=False; straight to DLX

---
## Immediate Retry Risks

- Same error reproduces immediately
- Tight loop; broker overhead
- Sometimes useful (transient network glitch)
- Often bad (broken message hammers the queue)
- Combine with retry counter to avoid infinite loops

---
## Delayed Retry With TTL

- Set `x-message-ttl` on a "retry queue"
- Messages dead-letter back to the original queue after the TTL
- Implements exponential backoff with multiple retry queues
- A common pattern for "try again in N seconds"

---
## Retry Count Headers

- Worker increments a counter header on each retry
- Drops to DLX after threshold (e.g., 5)
- The DLX captures truly broken messages
- Manual investigation handles them
- Without a count, retries can loop forever

---
## Poison Messages

- Messages that cannot be processed by *any* consumer
- Often: malformed data, missing dependencies, version mismatches
- A poison message blocking a queue stops everyone
- DLX + retry count gets them out of the way
- Inspect periodically; fix the source

---
## DLX as Investigation Queue

- Dead-letter messages: keep them; don't drop
- A separate "DLQ" queue accumulates them
- Engineers inspect via the management UI
- Common patterns: replay after fixing the bug, or archive
- Without DLX, you lose the failure mode

---
## A Production Pattern

- Main queue with DLX configured
- Consumer: process; on success, ack; on failure, nack with requeue=False
- Retry queue: receives the dead-letter, has a TTL, dead-letters back to main
- Counter header tracked
- After 5 retries: lands in a poison-DLQ for manual handling

---
## Reject vs Nack vs Throw

- nack with requeue=True: try again immediately
- nack with requeue=False: dead-letter
- Throwing an unhandled exception: depends on client; often nacks
- Be explicit; don't rely on default behaviour
- Document the team's pattern

---
## Logging Failures

- Each failure should log: message ID, queue, error, retry count
- Helps trace patterns over time
- Aggregate: which messages fail repeatedly?
- Alert on DLQ depth growing
- Without logs, mysteries

---
## Monitoring DLQ Depth

- DLQ should be near-empty in healthy operation
- Growth = something is broken
- Alert at, say, 100 messages
- Review weekly; fix sources
- Don't let DLQs become permanent garbage dumps

---
## Common Error-Handling Mistakes

- No DLX &#8594; broken messages hammer the queue forever
- Auto-ack with retries &#8594; lost data
- Logging the error but not the message ID
- DLQ that nobody monitors
- Same retry policy for transient and permanent errors
