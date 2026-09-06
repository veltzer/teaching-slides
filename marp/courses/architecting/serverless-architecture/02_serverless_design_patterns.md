---
tags:
  - architecture:serverless
level: intermediate
category: architecture
audience:
  - audiences:developers

---

# Serverless Design Patterns

---

## Pattern Overview

![event_patterns](svg/courses/architecting/serverless-architecture/02_serverless_design_patterns/event_patterns.svg)

---

## What This Chapter Covers

- Common serverless patterns
- API + Lambda + DynamoDB
- Event-driven processing
- Fan-out / fan-in
- Step Functions and orchestration
- Saga pattern
- Anti-patterns

---

## API + Lambda + DB

- API Gateway routes HTTP requests
- Lambda handles each request
- DynamoDB (or RDS) stores state
- The "Hello World" of serverless
- Scales to zero; pay per request

---

## Event-Driven Processing

- Event source (S3, SQS, Kinesis) &#8594; Lambda
- File uploaded to S3 &#8594; resize, transcode, OCR
- Message in SQS &#8594; process, write to DB
- Pure serverless: no scheduling, no servers
- The most natural fit

---

## Queue-Decoupled Worker

![queue_decoupled_worker](svg/courses/architecting/serverless-architecture/02_serverless_design_patterns/queue_decoupled_worker.svg)

---

## Fan-Out

- One event triggers many parallel Lambdas
- SNS topic with multiple subscribers
- EventBridge rules
- Each downstream is independent
- Scale: linear with subscribers

---

## Fan-In

- Many sources collect into one place
- Kinesis / SQS / EventBridge
- One downstream Lambda processes
- Beware: throughput limits
- Backpressure built in (queue depth)

---

## Topology Compared

![fan_out_fan_in](svg/courses/architecting/serverless-architecture/02_serverless_design_patterns/fanout_fanin.svg)

---

## Step Functions

- AWS's orchestration service
- Express workflows as state machines
- Each step: Lambda, AWS service call, choice, parallel
- Built-in retry, error handling, history
- Replaces hand-coded orchestration

---

## Step Functions Example

- "When order arrives:
    1. Validate it (Lambda)
    1. If valid: charge card (Lambda)
    1. If charged: send confirmation (Lambda)
    1. If failed at any step: handle error"
- Each transition tracked
- Long-running (up to 1 year)

---

## Saga Pattern (Serverless)

- Distributed transaction across many services
- Each step has a compensating action
- Step Functions or hand-rolled
- "Reserve inventory; charge card; ship; if any fail, compensate"
- Critical for cross-service workflows

---

## API Composition

- One Lambda fronts multiple downstream calls
- Aggregates the responses
- Reduces client round trips
- Common in BFF (Backend for Frontend)
- Watch: increases function execution time

---

## CQRS With Lambda

- Command: writes to DynamoDB &#8594; stream &#8594; Lambda
- Lambda projects to query store (DynamoDB GSI, ElasticSearch)
- Reads hit the query store; fast
- Fits naturally with serverless events

---

## Scheduled Lambda

- CloudWatch / EventBridge schedules trigger Lambda
- Like cron, but managed
- "Every hour: clean expired sessions"
- Cheap; reliable
- Replacement for many cron jobs

---

## Anti-Pattern: Lambda As A Server

- Long-running listener-style code
- Defeats the model
- Use ECS / Fargate / Cloud Run instead
- Serverless is for *event-driven* work

---

## Anti-Pattern: Synchronous Chains

- Lambda A calls Lambda B calls Lambda C
- Each invocation costs; latency adds up
- Better: events between them; or one Lambda
- Async better than sync for serverless

---

## Anti-Pattern: Hot Lambda

- One function does many things
- Becomes a serverless monolith
- Better: small functions; specific purpose each
- Step Functions to orchestrate

---

## Common Pattern Mistakes

- Lambdas calling Lambdas synchronously
- Writing your own retry / orchestration when Step Functions would do
- Big Lambdas when small + composition would
- No DLQ on async invocations
- Saga without compensations
