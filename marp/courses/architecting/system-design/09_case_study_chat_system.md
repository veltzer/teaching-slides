---
tags:
  - architecture:system-design
level: intermediate
category: architecture
audience:
  - audiences:developers

---
# Case Study: Chat System

---
## Chat Design

![chat_design](svg/courses/architecting/system-design/09_case_study_chat_system/chat_design.svg)

---
## Component Breakdown

![chat_components](svg/courses/architecting/system-design/09_case_study_chat_system/chat_components.svg)

---
## What This Chapter Covers

- Requirements
- Real-time delivery
- Message storage
- Presence
- Group chat
- Push notifications
- Scaling

---
## Requirements

- 1:1 and group chat
- Real-time delivery
- Message history
- Online presence
- Push notifications
- 100M users

---
## Architecture Overview

- Client &#8596; WebSocket gateway &#8594; backend &#8594; DB
- WebSocket for real-time
- HTTP for history queries
- Push for offline users

---
## Real-Time Delivery

- WebSockets: bidirectional, persistent
- Each user: 1 connection
- Messages: routed by user ID
- Server-side: message broker (Kafka, NATS)

---
## Server Affinity

- User connects to one gateway
- Gateways share state via broker
- "Send to user X" published; X's gateway delivers
- Sticky session via load balancer

---
## Message Storage

- Cassandra: time-series; partition by chat ID
- Or DynamoDB: similar
- 100M users * 100 msgs/day = 10B msgs/day
- Append-only; archive old

---
## Group Chat

- Group ID; members list
- Send to group: fan out to each member's queue
- Large groups: lazy fan-out (read-time)
- Limit: typical 1000-10000 members per group

---
## Presence

- Last-seen heartbeat
- Online: heartbeat in last 30s
- Stored in Redis (volatile, fast)
- Pub/sub: presence changes broadcast
- Costly at scale; aggregate

---
## Push Notifications

- User offline: push via APNs / FCM
- Queue: user device tokens, message
- Worker: dispatch to provider
- Retry; rate-limit per user
- Cost: per-message push fees

---
## Read Receipts

- Per-message-per-user state
- "Seen" event &#8594; update store
- For groups: count seen, not full list
- Privacy / cost trade-offs

---
## Search

- Optional; expensive
- Index messages in Elasticsearch
- Per-user index (privacy + size)
- Add when users demand it

---
## Scaling

- WebSocket gateways: stateless behind LB
- Brokers: Kafka topics per shard
- DB: Cassandra horizontally scales
- Redis cluster for presence
- Scale each independently

---
## Failure Modes

- Gateway crash: clients reconnect; brief gap
- Broker partition: dual-deliver to both halves
- DB partition: degraded write availability
- Most: graceful degradation, not catastrophic

---
## End-To-End Encryption

- Message bodies encrypted client-to-client
- Server can't read
- Search becomes harder
- Key management: hard
- Optional in many systems; default in some (Signal)

---
## Common Discussion Points

- "How do you order messages?" — server timestamp + client ordering
- "How do groups of millions work?" — lazy delivery, snapshot reads
- "How do you handle a user with 10 devices?" — multi-device fan-out
- "What about message receipts?" — bandwidth-cost trade-off
- Practice articulating trade-offs
