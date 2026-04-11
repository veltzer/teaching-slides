---
tags:
  - infrastructure:cloud
  - concepts:architecture
  - concepts:messaging
level: intermediate
category: cloud
audience:
  - audiences:developers
  - audiences:architects
  - audiences:devops

---
# Distributed Queues

---

## Why Queues?
- Decouple producers from consumers
- Buffer for traffic spikes
- Enable asynchronous processing
- Improve reliability (retry on failure)
- Fundamental building block for distributed systems

---

## Synchronous vs Asynchronous
- Synchronous: caller waits for response
- Asynchronous: caller sends message and continues
- Queues enable asynchronous communication
- Better resilience: consumer can be down temporarily
- Better scalability: scale producer and consumer independently

---

## What Do Cloud Queues Give You?
- Fully managed message queuing service
- No servers to provision or manage
- Automatic scaling to handle any throughput
- Built-in redundancy (multi-AZ)
- Pay per message or per request

---

## Cloud Queue Services
- AWS SQS (Simple Queue Service)
- Azure Queue Storage / Service Bus
- GCP Pub/Sub / Cloud Tasks
- Each has different features and trade-offs
- SQS: simplest, most widely used

---

## SQS: Create Queue and Send Message

```bash
# Create a queue
aws sqs create-queue --queue-name orders

# Send a message
aws sqs send-message \
  --queue-url https://sqs.us-east-1.amazonaws.com/\
123456789012/orders \
  --message-body '{"orderId":"O-1234","total":99.50}'

# Receive and delete
MSG=$(aws sqs receive-message --queue-url $URL)
aws sqs delete-message --queue-url $URL \
  --receipt-handle $(echo $MSG | jq -r '.Messages[0].ReceiptHandle')
```

---

## SNS: Pub/Sub Notifications
- Amazon Simple Notification Service
- Publish a message to a topic
- Multiple subscribers receive it (fan-out)
- Subscribers: SQS queues, Lambda, email, HTTP
- Combine SNS + SQS for robust fan-out

---

## SNS Fan-Out Pattern

```bash
# Create topic and subscribe queues
aws sns create-topic --name order-events

aws sns subscribe \
  --topic-arn arn:aws:sns:us-east-1:123:order-events \
  --protocol sqs \
  --notification-endpoint arn:aws:sqs:us-east-1:123:email-queue

aws sns subscribe \
  --topic-arn arn:aws:sns:us-east-1:123:order-events \
  --protocol sqs \
  --notification-endpoint arn:aws:sqs:us-east-1:123:inventory-queue

# Publish event (goes to BOTH queues)
aws sns publish \
  --topic-arn arn:aws:sns:us-east-1:123:order-events \
  --message '{"orderId":"O-1234"}'
```

---

## EventBridge
- Serverless event bus
- Rule-based event routing
- Filter events by content
- Connect AWS services, SaaS, and custom apps
- Schema registry for event discovery

---

## Message Size and Limits
- SQS: max 256 KB per message
- Large messages: use S3 + pointer in SQS
- SNS: max 256 KB per message
- Kinesis: max 1 MB per record
- Design for these limits from the start

---

## How Costly Is It?
- SQS: ~$0.40 per million requests
- Very cheap for most workloads
- No charge for empty queues
- Data transfer charges may apply
- Almost always cheaper than running your own

---

## Is It Better to Run Your Own?
- Almost always no
- Running RabbitMQ or Kafka: operational burden
- Patching, scaling, monitoring, failover
- Cloud-managed: all handled for you
- Run your own only if you need specific features (e.g., Kafka for streaming)

---

## Queue Semantics: At-Least-Once
- Message delivered at least once
- Consumer may receive duplicates
- Application must handle idempotency
- Most cloud queues use this model
- Simpler, more scalable than exactly-once

---

## Queue Semantics: Exactly-Once
- Each message processed exactly once
- Much harder to implement at scale
- SQS FIFO queues offer exactly-once within scope
- Often achieved at application level (idempotency keys)
- Don't assume it unless explicitly guaranteed

---

## Queue Semantics: Ordering
- Standard queues: best-effort ordering
- FIFO queues: strict first-in-first-out
- Standard: higher throughput
- FIFO: lower throughput, guaranteed order
- Use FIFO only when order matters

---

## Queue Patterns: Work Queue
- One producer, multiple consumers
- Each message processed by one consumer
- Load distribution across workers
- Auto-scale workers based on queue depth
- Most common queue pattern

---

## Queue Patterns: Fan-Out
- One message sent to multiple subscribers
- Use SNS + SQS (or Pub/Sub + subscriptions)
- Each subscriber gets a copy
- Different consumers process differently
- Example: order placed -> email + inventory + analytics

---

## Queue Patterns: Dead Letter Queue
- Messages that fail processing repeatedly
- Moved to a separate DLQ after N retries
- Investigate and reprocess failures
- Prevents poison messages from blocking the queue
- Always configure a DLQ

---

## Queue Patterns

![patterns](svg/courses/cloud/architecting-in-the-cloud/06_distributed_queues/queue_patterns.svg)

---

## Guarantees from Various Cloud Queues
- SQS Standard: at-least-once, best-effort order, unlimited throughput
- SQS FIFO: exactly-once, strict order, 300-3000 msg/sec
- Azure Service Bus: at-least-once, FIFO with sessions
- GCP Pub/Sub: at-least-once, ordering keys for order
- Choose based on your requirements

---

## Visibility Timeout
- After a consumer receives a message, it becomes invisible
- Consumer has a window to process and delete
- If not deleted, message reappears for another consumer
- Prevents multiple consumers processing the same message
- Set timeout based on expected processing time

---

## Visibility Timeout

![visibility](svg/courses/cloud/architecting-in-the-cloud/06_distributed_queues/visibility_timeout.svg)

---

## Long Polling
- Standard polling: frequent empty responses (wasteful)
- Long polling: wait up to 20 seconds for a message
- Reduces cost and latency
- Enable by default for SQS
- Fewer empty responses, lower request count

---

## Scaling with Queues
- Monitor queue depth (ApproximateNumberOfMessages)
- Auto-scale consumers based on queue depth
- If queue grows: add consumers
- If queue empties: reduce consumers
- Queue acts as a natural backpressure mechanism

---

## Queue Security
- IAM policies control who can send/receive
- Encryption at rest and in transit
- VPC endpoints for private access
- Resource policies for cross-account access
- Audit with CloudTrail

---

## Queues vs Event Streaming
- Queues: message consumed once, then deleted
- Streaming (Kafka, Kinesis): messages retained, replay possible
- Queues: simple work distribution
- Streaming: event sourcing, analytics, multiple consumers
- Choose based on your use case

---

## Queues vs Streaming

![queues_streaming](svg/courses/cloud/architecting-in-the-cloud/06_distributed_queues/queues_vs_streaming.svg)

---

## Event Streaming: Kafka and Kinesis
- Messages retained for days or weeks (not deleted on consume)
- Multiple consumer groups read independently
- Replay capability for reprocessing
- High throughput, ordered within partitions
- Managed: MSK (Kafka), Kinesis Data Streams, Confluent Cloud

---

## When to Use Streaming vs Queues
- Queue: task distribution, one consumer per message
- Streaming: event log, multiple consumers, replay
- Queue: simpler, cheaper for simple work distribution
- Streaming: event sourcing, analytics, audit logs
- Some architectures use both

---

## Event-Driven Architecture with Queues
- SNS + SQS: fan-out pattern
- EventBridge: rule-based routing
- Pub/Sub: flexible filtering
- Events as first-class citizens
- Loose coupling, easy to extend

---

## Idempotency in Queue Consumers
- Consumer may receive the same message twice
- Processing must be safe to repeat
- Use unique message IDs for deduplication
- Database upserts instead of inserts
- Design for at-least-once delivery

---

## Batch Processing with Queues
- Accumulate messages, process in batches
- SQS: receive up to 10 messages at once
- Lambda: batch event source mapping
- Reduces per-message overhead
- Increases throughput

---

## FIFO Queues in Detail
- Strict ordering guarantees
- Exactly-once processing (within deduplication window)
- Message Group ID: ordering within a group
- Deduplication ID: prevent duplicates
- Lower throughput: 300 msg/sec (3,000 with batching)

---

## Delay Queues
- Delay delivery of new messages
- SQS: up to 15 minutes delay
- Use case: schedule processing for later
- Use case: rate limiting
- Per-queue or per-message delay

---

## Queue Monitoring
- Queue depth: how many messages waiting
- Age of oldest message: processing lag
- Number of messages in flight: being processed
- Error rate: messages going to DLQ
- Set alarms on all these metrics

---

## Queue Architecture Best Practices
- Always use a dead letter queue
- Design consumers to be idempotent
- Use long polling to reduce costs
- Monitor queue depth and age of oldest message
- Auto-scale consumers based on queue metrics
- Encrypt messages in transit and at rest
