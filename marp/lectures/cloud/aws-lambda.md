---
tags:
  - infrastructure:cloud
  - infrastructure:aws
  - practices:serverless
level: intermediate
category: cloud
audience:
  - audiences:developers
  - audiences:devops
  - audiences:architects

---

# AWS Lambda
## Mark Veltzer
## [mark.veltzer@gmail.com](mailto:mark.veltzer@gmail.com)

---

## Overview

![title](svg/lectures/cloud/aws-lambda/title.svg)

---

## What is AWS Lambda?
- A serverless compute service from AWS
- You upload code; AWS runs it on demand
- No servers to provision, patch, or scale
- Runs in response to *events*
- You pay only for the compute you actually use
- Scales from zero to thousands of concurrent executions

---

## What "Serverless" Really Means
- There *are* servers — you just do not manage them
- No OS to patch, no capacity planning, no idle hosts
- The unit of deployment is a **function**, not a host
- The cloud provider owns availability and scaling
- Billing is per-request and per-millisecond, not per-hour

---

## Serverless vs Traditional Compute

![compute-spectrum](svg/lectures/cloud/aws-lambda/compute-spectrum.svg)

---

## The Core Idea: Event → Function → Result
- Something happens (an *event*)
- Lambda runs your *function* with that event as input
- The function does work and returns a result
- AWS handles everything in between
- No long-running process sitting idle waiting

---

## Anatomy of a Lambda Function
- **Handler**: the entry-point function AWS calls
- **Event**: the input payload (JSON)
- **Context**: runtime metadata (request id, time left, memory)
- **Runtime**: the language environment (Python, Node, Java, …)
- **Return value**: the function's output, sent back to the caller

---

## A Minimal Python Handler
```python
def handler(event, context):
    name = event.get("name", "world")
    return {
        "statusCode": 200,
        "body": f"Hello, {name}!"
    }
```
- `event` carries the input data
- `context` exposes request id, deadline, memory limit
- Return a plain dict — AWS serializes it for you

---

## The Lambda Execution Model

![execution-model](svg/lectures/cloud/aws-lambda/execution-model.svg)

---

## Where Does the Code Run?
- AWS provisions a **micro-VM** (Firecracker) per execution environment
- Your code, runtime, and dependencies live inside it
- Each environment handles one request at a time
- Many environments run in parallel for concurrency
- You never see or SSH into these machines

---

## The Execution Lifecycle

![lifecycle](svg/lectures/cloud/aws-lambda/lifecycle.svg)

---

## Cold Starts vs Warm Starts
- **Cold start**: a fresh environment must be created and initialized
- The runtime boots and your init code runs once
- **Warm start**: an existing environment is reused — much faster
- AWS keeps environments warm for a while after a request
- Cold starts hurt latency-sensitive, infrequently-called functions

---

## Reducing Cold Start Pain
- Keep deployment packages small
- Do heavy setup *outside* the handler (module scope)
- Reuse clients and connections across invocations
- Choose lighter runtimes for latency-sensitive paths
- Use **provisioned concurrency** to keep environments ready

---

## What Can Trigger a Lambda?

![event-sources](svg/lectures/cloud/aws-lambda/event-sources.svg)

---

## Common Event Sources
- **API Gateway**: HTTP/REST requests → function
- **S3**: object created / deleted → function
- **DynamoDB Streams**: row changes → function
- **SQS / SNS**: messages and notifications → function
- **EventBridge**: scheduled and event-driven rules
- **Kinesis**: streaming data records

---

## Invocation Types

![invocation-types](svg/lectures/cloud/aws-lambda/invocation-types.svg)

---

## Synchronous vs Asynchronous
- **Synchronous**: caller waits for the result (API Gateway)
- The response goes straight back to the caller
- **Asynchronous**: caller just hands off the event (S3, SNS)
- Lambda queues it internally and retries on failure
- **Stream / poll**: Lambda polls the source in batches (SQS, Kinesis)

---

## Concurrency and Scaling

![scaling](svg/lectures/cloud/aws-lambda/scaling.svg)

---

## How Lambda Scales
- One environment serves one request at a time
- More concurrent requests → more environments, automatically
- Scales out in seconds, with no configuration
- **Reserved concurrency** caps a function's max environments
- **Provisioned concurrency** pre-warms a fixed pool

---

## Configuration Knobs
- **Memory**: 128 MB up to 10 GB — also scales CPU and network
- **Timeout**: up to 15 minutes per invocation
- **Ephemeral storage**: `/tmp`, 512 MB up to 10 GB
- **Environment variables**: config without code changes
- **Layers**: shared dependencies across functions

---

## Memory Tunes Everything

![memory-cpu](svg/lectures/cloud/aws-lambda/memory-cpu.svg)

---

## Permissions: The Execution Role
- Every function runs with an **IAM execution role**
- The role grants what the function may access (S3, DynamoDB, …)
- Follow least privilege — grant only what is needed
- Resource policies control *who* may invoke the function
- No long-lived keys baked into your code

---

## The IAM Trust Model

![iam-model](svg/lectures/cloud/aws-lambda/iam-model.svg)

---

## Packaging Your Code
- **Zip archive**: code plus dependencies, up to 250 MB unzipped
- **Container image**: up to 10 GB, your own base image
- **Layers**: reusable dependency bundles, shared across functions
- Bigger packages mean slower cold starts
- Pin dependency versions for reproducible builds

---

## Observability and Logging
- Logs stream automatically to **CloudWatch Logs**
- **CloudWatch Metrics**: invocations, errors, duration, throttles
- **X-Ray**: distributed tracing across services
- Structured (JSON) logs are far easier to query
- Alarm on error rate and on throttling

---

## Errors and Retries

![error-handling](svg/lectures/cloud/aws-lambda/error-handling.svg)

---

## Handling Failure Well
- Synchronous errors return to the caller — handle them there
- Async invocations are retried automatically (twice by default)
- Send unprocessable events to a **dead-letter queue (DLQ)**
- Make handlers **idempotent** — retries can run code twice
- Set timeouts deliberately; do not rely on the 15-minute max

---

## A Serverless Web API

![web-api](svg/lectures/cloud/aws-lambda/web-api.svg)

---

## Event-Driven Data Pipeline

![data-pipeline](svg/lectures/cloud/aws-lambda/data-pipeline.svg)

---

## Pricing Model
- Pay per **request** (per million invocations)
- Pay per **GB-second** of compute (memory × duration)
- A generous always-free tier each month
- No charge while idle — zero traffic costs nothing
- Right-size memory: faster runs can cost *less*

---

## When Lambda Shines — and When Not
- **Great for**: event handlers, glue code, spiky/bursty traffic
- **Great for**: APIs, cron jobs, stream and file processing
- **Poor fit**: long-running jobs over 15 minutes
- **Poor fit**: heavy, steady, predictable load (containers win)
- **Poor fit**: ultra-low-latency needs sensitive to cold starts

---

## Best Practices
- One function, one responsibility
- Keep handlers thin; push logic into testable modules
- Initialize clients once, outside the handler
- Least-privilege IAM roles, always
- Make operations idempotent and observable
- Use infrastructure-as-code (SAM, CDK, Terraform)

---

## Summary
- Lambda runs your code in response to events, serverless
- Event → Function → Result, with AWS managing the rest
- Scales automatically; you pay only for what you use
- Mind cold starts, concurrency, IAM, and idempotency
- Ideal for event-driven, bursty, glue-style workloads

---

## Thank You
## Mark Veltzer
## [mark.veltzer@gmail.com](mailto:mark.veltzer@gmail.com)
