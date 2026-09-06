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

# Reliability

---

## What This Chapter Covers

- Delivery semantics in depth
- Acknowledgments
- Idempotency
- Outbox pattern
- Backpressure

---

## Acknowledgments

- Consumer signals success
- Broker removes message
- No ack means redelivery
- Tunes the at-least-once guarantee

---

## Delivery Guarantees

![delivery_guarantees](svg/courses/architecting/message-queues/03_reliability/delivery_guarantees.svg)

---

## Auto-Ack

- Ack on receive
- Lost on consumer crash
- Use only for telemetry
- Default in some clients

---

## Manual Ack

- Ack after processing
- Survives crashes
- Default in production
- Slightly more work

---

## Visibility Timeout

- Ack window
- Locked while consumer works
- Expires on slow processing
- Tune to typical work time

---

## Idempotent Consumers

- Same message twice yields same effect
- Required under at-least-once
- Use a dedup table
- Or use natural keys

---

## Deduplication Window

- Time-bounded uniqueness
- Trade memory for window size
- Beyond window: rely on idempotency
- Document the window

---

## Outbox Pattern

- Write event to local table in same transaction as data
- Separate process publishes to broker
- Solves dual-write problem
- Required when correctness matters

---

## Outbox Visualized

![outbox_pattern](svg/courses/architecting/message-queues/03_reliability/outbox_pattern.svg)

---

## Inbox Pattern

- Receiver records processed IDs
- Drops duplicates
- Pairs with outbox at sender
- Closes the loop

---

## Backpressure

- Slow consumer
- Queue grows
- Producer must feel pressure
- Drop, block, or scale

---

## Bounded Queues

- Cap on depth
- Producer blocks or drops on full
- Visibility into health
- Prevents runaway memory

---

## Flow Control

- Credits or windows
- Broker tells producer to slow
- Standard in modern brokers
- Avoid silent overload

---

## Disaster Scenarios

- Broker total loss
- Network partition
- Producer ahead of consumer
- Replay from backup

---

## Common Reliability Mistakes

- Auto-ack in production
- Long visibility timeout
- No idempotency
- Dual-writes without outbox
- Unbounded queues
