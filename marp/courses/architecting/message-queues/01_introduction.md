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

# Introduction to Message Queues

---

## What This Chapter Covers

- What a queue is
- Why use one
- Queue vs topic
- Common terminology
- Course outline

---

## What a Queue Is

- Buffer between producer and consumer
- Decouples in time
- Decouples in load
- Decouples in topology

---

## Why Use One

- Smooth load spikes
- Survive consumer outages
- Independent scaling
- Async workflows

---

## Reasons Visualised

![why_queues](svg/courses/architecting/message-queues/01_introduction/why_queues.svg)

---

## Queue vs Topic

- Queue: one consumer per message
- Topic: many consumers per message
- Both are common
- Many systems offer both

---

## Producer and Consumer

- Producer writes messages
- Consumer reads and processes
- Broker stores in between
- Broker is the trust boundary

---

## Three Roles

![producer_broker_consumer](svg/courses/architecting/message-queues/01_introduction/producer_broker_consumer.svg)

---

## Pull vs Push

- Pull: consumer asks for work
- Push: broker sends to consumer
- Pull is more common
- Push needs flow control

---

## Throughput Model

- Messages per second
- Bytes per second
- Latency end-to-end
- Bound by slowest consumer

---

## Persistence

- In-memory only: fast, lossy
- Disk-backed: durable
- Replicated: survives node failure
- Pick by data value

---

## Ordering

- Per-queue or per-key
- Strict order limits parallelism
- Often relaxed for throughput
- Document the guarantee

---

## At-Most-Once

- May be lost
- Never duplicated
- Cheapest
- Suitable for telemetry only

---

## At-Least-Once

- Never lost
- May be duplicated
- Most common
- Consumer must be idempotent

---

## Exactly-Once

- Lossless and unique
- Hard to provide end-to-end
- Often "effectively once"
- Idempotency still required

---

## Course Outline

- Patterns
- Reliability
- Routing and partitioning
- Operations
- Failure modes

---

## Common Beginner Mistakes

- Using queue as a database
- Ignoring duplicates
- Not bounding queue depth
- Treating broker as free
- Coupling consumer to broker library
