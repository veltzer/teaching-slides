---
tags:
  - networking:graphql
level: intermediate
category: networking
audience:
  - audiences:developers

---
# Subscriptions

---
## What This Chapter Covers

- What subscriptions are
- Transport
- Use cases
- Server side
- Client side
- Tradeoffs

---
## What Subscriptions Are

- Streaming GraphQL operations
- Server pushes updates
- Live data
- Long-lived connection

---
## Sample Subscription

```graphql
subscription OnNewMessage($room: ID!) {
    messageAdded(room: $room) {
        id
        text
        author { name }
    }
}
```

- Same selection model as queries
- Stream of events

---
## Transport

- WebSocket: classic, bidirectional
- SSE: server-sent events
- graphql-ws protocol: standard
- HTTP: not native

---
## Use Cases

- Chat / messaging
- Notifications
- Live dashboards
- Collaborative editing

---
## Server Side

- Resolver returns async iterator
- Triggered by pub/sub
- Filter events by subscription args

---
## Pub / Sub Backend

- Redis, Kafka, etc.
- Resolver listens to channel
- Pushes matching events to client
- Decouples publisher and subscriber

---
## Sample Resolver

- Subscribe: listen on channel
- On event: filter and yield
- On disconnect: unsubscribe

---
## Authentication

- Auth at connection time
- Token in connection params
- Refresh handling tricky on long connections

---
## Scaling

- WebSockets: stateful
- Sticky sessions or shared backend
- Backpressure: client slow consumers
- Limit connections per user

---
## Versus Polling

- Polling: pull, simple, more load
- Subscriptions: push, complex, lower latency
- Pick by frequency and latency needs

---
## Versus Webhooks

- Webhooks: server-to-server
- Subscriptions: server-to-client
- Different trust models

---
## Tradeoffs

- Live UX is great
- Operational complexity rises
- Reconnection, replay, ordering
- Use only when needed

---
## Common Subscription Mistakes

- Subscribing to everything; UI floods
- No reconnection logic
- Filtering on client; sending too much
- Missing auth on connection upgrade
- Subscriptions for data better fetched once
