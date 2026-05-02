---
tags:
  - architecture:serverless
  - architecture:events
level: intermediate
category: architecture
audience:
  - audiences:developers

---
# Event Sources and Integration

---
## What This Chapter Covers

- Sync vs async invocation
- HTTP via API Gateway
- Queue-based triggers
- Stream-based triggers
- Storage events
- Scheduled events
- EventBridge

---
## Sync vs Async

- **Sync**: caller waits for response (HTTP)
- **Async**: caller fires and forgets (events)
- Different invocation patterns at AWS Lambda
- Async: built-in retries, DLQ
- Sync: caller responsible for handling errors

---
## Event Source Categories

![event_sources](svg/courses/architecting/serverless-architecture/05_event_sources_and_integration/event_sources.svg)

---
## API Gateway + Lambda

- HTTP requests trigger Lambda
- Sync invocation
- Up to 30s timeout (gateway limit)
- Standard for REST APIs
- HTTP API for cheaper / faster than REST API

---
## SQS (Queue-Based)

- Messages in queue trigger Lambda
- Async; built-in retries
- Batch invocations: up to 10 messages
- DLQ for poison messages
- The classic decoupled pattern

---
## SQS Patterns

- Producer service writes to queue
- Lambda processes; deletes message on success
- Failure: visibility timeout expires; message reprocessed
- After N retries: message goes to DLQ
- Idempotency required (retries happen)

---
## Kinesis (Stream-Based)

- Ordered, partitioned event stream
- Lambda invoked with records
- Per-partition processing (one Lambda per shard)
- Replay possible (offset-based)
- Used for: high-volume event ingestion

---
## DynamoDB Streams

- Capture changes to DynamoDB tables
- Each item change &#8594; stream record
- Lambda processes records
- Common for: replication, denormalisation, audit
- Free with the table

---
## S3 Events

- File uploaded / deleted &#8594; Lambda
- Image processing, OCR, transcoding
- Metadata extraction
- Synchronous, exactly-once-ish (at-least-once with idempotency)
- The original "serverless trigger"

---
## SNS Events

- Pub-sub
- Many subscribers per topic
- Each subscriber: Lambda, SQS, HTTP, ...
- Fan-out pattern
- Cheaper than EventBridge but less feature-rich

---
## EventBridge

- AWS's event bus
- Many AWS services emit events automatically
- Custom events from your apps
- Rules route events to targets (Lambda, SQS, others)
- The modern AWS event hub

---
## EventBridge Patterns

- Rule: filter by source + detail
- Multiple targets per rule
- Schemas: type-safe events
- Cross-account / cross-region
- Replaces a lot of custom event-routing code

---
## Scheduled Events

- EventBridge / CloudWatch Schedules: cron-like
- "Every hour" / "Every weekday at 9am UTC"
- Triggers Lambda
- The serverless replacement for cron jobs
- Reliable, easy to set up

---
## API Gateway Authoriser

- Lambda authorises API Gateway requests
- JWT authoriser is built-in
- Custom logic in Lambda for complex auth
- Cached by default to reduce calls

---
## Event Filtering

- SNS, SQS, EventBridge support filtering
- Lambda only invoked when filter matches
- Saves cost (fewer invocations)
- "Process only orders > $1000"
- Filter at the source, not in code

---
## Failure Modes

- Sync: caller gets error; retry is caller's job
- Async: built-in retry (up to 3x), then DLQ
- Stream: blocks on poison record; bisect to handle
- Queue: returns to queue; eventually DLQ
- Each pattern has its own failure semantics

---
## Common Integration Mistakes

- Using sync where async would do (cost, latency)
- No DLQ on async (lost messages)
- Stream consumer that crashes on bad data (blocks the stream)
- Event filtering done in code instead of at source
- Using SNS when EventBridge would simplify
