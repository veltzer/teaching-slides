# Pub/Sub Messaging with Redis

---

## What is Pub/Sub?

- **Publish**/**Subscribe** messaging pattern
- Senders (publishers) send messages to channels
- Receivers (subscribers) subscribe to channels
- Publishers don't know who receives messages
- Subscribers don't know who sent messages
- Decouples components in distributed systems

---

## Pub/Sub Pattern

![pub_sub_pattern](/svg/courses/databases/redis/04_pubsub/pub_sub_pattern.svg)

---

## Pub/Sub vs. Other Communication Patterns

![pub_sub_vs_other_communication_patterns](/svg/courses/databases/redis/04_pubsub/pub_sub_vs_other_communication_patterns.svg)

---

## Why Redis for Pub/Sub?

- Simple and fast implementation
- No additional dependencies
- Easy to set up and integrate
- Scales to thousands of channels
- Pattern-based subscriptions
- Minimal overhead on Redis
- Works alongside other Redis features

---

## Redis Pub/Sub Limitations

- No message persistence
    - Messages are lost if no subscribers
    - No message history for new subscribers
- No acknowledgment mechanism
    - No guarantee messages are processed
- No load balancing among subscribers
    - All subscribers receive all messages
- No message replay capability
- Not for mission-critical messaging

---

## When to Use Redis Pub/Sub

**Good for**:
- Real-time notifications
- Broadcasting events
- Simple workflows
- System coordination
- Chat applications
- Non-critical events

**Not ideal for**:
- Mission-critical messaging
- Guaranteed delivery
- Complex workflows
- Heavy message processing
- Event sourcing

---

## Redis Pub/Sub Basic Commands

```bash
# Publishing
PUBLISH channel message

# Subscribing
SUBSCRIBE channel [channel ...]
PSUBSCRIBE pattern [pattern ...]

# Unsubscribing
UNSUBSCRIBE [channel [channel ...]]
PUNSUBSCRIBE [pattern [pattern ...]]

# Channel information
PUBSUB CHANNELS [pattern]
PUBSUB NUMSUB [channel [channel ...]]
PUBSUB NUMPAT
```

---

## Basic Pub/Sub Example

![basic_pub_sub_example](/svg/courses/databases/redis/04_pubsub/basic_pub_sub_example.svg)

---

## Pattern-Based Subscriptions

```bash
# Subscribe to all user-related channels
PSUBSCRIBE user:*

# Subscribe to all notification channels for a specific user
PSUBSCRIBE user:1000:notification:*

# Subscribe to all error channels
PSUBSCRIBE *:error
```

Pattern matching:
- `?` matches any single character
- `*` matches any sequence of characters
- `[abc]` matches any character in the brackets
- `[^abc]` matches any character not in the brackets

---

## Working with Channels

```bash
# List all active channels
PUBSUB CHANNELS

# List channels matching a pattern
PUBSUB CHANNELS user:*

# Count subscribers for specific channels
PUBSUB NUMSUB notifications user:updates

# Count pattern subscriptions
PUBSUB NUMPAT
```

---

## Pub/Sub in Python (redis-py)

```python
import redis
import threading

# Initialize Redis client
r = redis.Redis(host='localhost', port=6379, db=0)

# Subscriber function
def subscribe():
    pubsub = r.pubsub()
    pubsub.subscribe('my-channel')

    for message in pubsub.listen():
        if message['type'] == 'message':
            print(f"Received: {message['data']}")

            # Unsubscribe after receiving "EXIT"
            if message['data'] == b'EXIT':
                pubsub.unsubscribe()
                break

# Start subscriber in a thread
subscriber_thread = threading.Thread(target=subscribe)
subscriber_thread.start()

# Publish messages
r.publish('my-channel', 'Hello from Python!')
r.publish('my-channel', 'Another message')
r.publish('my-channel', 'EXIT')

# Wait for subscriber to exit
subscriber_thread.join()
```

---

## Pub/Sub in Node.js (ioredis)

```javascript
const Redis = require('ioredis');

// Create publisher and subscriber clients (separate connections)
const publisher = new Redis();
const subscriber = new Redis();

// Subscribe to a channel
subscriber.subscribe('my-channel', (err, count) => {
  if (err) {
    console.error('Failed to subscribe:', err);
  } else {
    console.log(`Subscribed to ${count} channel(s)`);

    // Publish a message
    publisher.publish('my-channel', 'Hello from Node.js!');
  }
});

// Listen for messages
subscriber.on('message', (channel, message) => {
  console.log(`Received ${message} from ${channel}`);

  if (message === 'EXIT') {
    subscriber.unsubscribe();
    subscriber.quit();
    publisher.quit();
  }
});

// Publish more messages
setTimeout(() => {
  publisher.publish('my-channel', 'Another message');
  publisher.publish('my-channel', 'EXIT');
}, 1000);
```

---

## Pub/Sub Use Case: Chat System

![pub_sub_use_case_chat_system](/svg/courses/databases/redis/04_pubsub/pub_sub_use_case_chat_system.svg)

---

## Pub/Sub Use Case: Real-time Dashboard

![pub_sub_use_case_real_time_dashboard](/svg/courses/databases/redis/04_pubsub/pub_sub_use_case_real_time_dashboard.svg)

---

## Pub/Sub Use Case: Cache Invalidation

![pub_sub_use_case_cache_invalidation](/svg/courses/databases/redis/04_pubsub/pub_sub_use_case_cache_invalidation.svg)

---

## Pub/Sub Use Case: Microservices Communication

![pub_sub_use_case_microservices_communication](/svg/courses/databases/redis/04_pubsub/pub_sub_use_case_microservices_communication.svg)

---

## Building Reliability on Redis Pub/Sub

Since Redis Pub/Sub offers no persistence:

1. **Message acknowledgment**:
    - Implement custom ACK protocol

1. **Message replay**:
    - Store critical messages in Redis Lists/Streams

1. **Delivery guarantees**:
    - Combine with Redis Streams for persistence

1. **Error handling**:
    - Implement dead-letter channels

---

## Message Acknowledgment Pattern

![message_acknowledgment_pattern](/svg/courses/databases/redis/04_pubsub/message_acknowledgment_pattern.svg)

---

## Sentinel Events with Pub/Sub

Use Redis Pub/Sub for Redis Sentinel events:

![sentinel_events_with_pub_sub](/svg/courses/databases/redis/04_pubsub/sentinel_events_with_pub_sub.svg)

---

## Introduction to Redis Streams

Streams (introduced in Redis 5.0):
- Append-only data structures
- Persistent append-only logs
- Support consumer groups
- Perfect complement to Pub/Sub

![introduction_to_redis_streams](/svg/courses/databases/redis/04_pubsub/introduction_to_redis_streams.svg)

---

## Redis Streams Basic Commands

```bash
# Adding entries
XADD key [MAXLEN [~] count] ID field value [field value ...]

# Reading entries
XREAD [COUNT count] [BLOCK milliseconds] STREAMS key [key ...] ID [ID ...]
XRANGE key start end [COUNT count]
XREVRANGE key end start [COUNT count]

# Managing streams
XLEN key
XDEL key ID [ID ...]
XTRIM key MAXLEN [~] count
```

---

## Consumer Groups in Streams

```bash
# Creating consumer groups
XGROUP CREATE key group ID

# Reading as consumer
XREADGROUP GROUP group consumer [COUNT count] [BLOCK milliseconds] STREAMS key [key ...] ID [ID ...]

# Managing message acknowledgment
XACK key group ID [ID ...]
XPENDING key group [start end count [consumer]]
XCLAIM key group consumer min-idle-time ID [ID ...]
```

---

## Streams vs Pub/Sub: When to Use What

![streams_vs_pub_sub_when_to_use_what](/svg/courses/databases/redis/04_pubsub/streams_vs_pub_sub_when_to_use_what.svg)

---

## Combining Pub/Sub with Streams

![combining_pub_sub_with_streams](/svg/courses/databases/redis/04_pubsub/combining_pub_sub_with_streams.svg)

---

## Scaling Pub/Sub with Redis Cluster

![scaling_pub_sub_with_redis_cluster](/svg/courses/databases/redis/04_pubsub/scaling_pub_sub_with_redis_cluster.svg)

---

## Monitoring Pub/Sub

Important metrics to monitor:

1. **Channel count**:
    - `PUBSUB CHANNELS` or `PUBSUB CHANNELS pattern`

1. **Subscriber count**:
    - `PUBSUB NUMSUB channel [channel ...]`

1. **Pattern subscriber count**:
    - `PUBSUB NUMPAT`

1. **Published messages**:
    - Monitor with `INFO stats`
    - `published_messages` count

---

## Handling Pub/Sub Connection Issues

Best practices:

1. **Auto-reconnect**:
    - Most clients support this
    - Implement backoff strategy

1. **Subscription restoration**:
    - Re-subscribe after reconnection
    - Keep subscription list

1. **Missed messages**:
    - Consider supplementary storage
    - Use timestamp-based reconciliation

1. **Health checks**:
    - PING/PONG mechanism
    - Heartbeat channels

---

## Pub/Sub Security Considerations

Security practices:

1. **Authentication**:
    - Use Redis AUTH
    - ACL for Redis 6.0+

1. **Transport security**:
    - TLS encryption
    - VPN or secure network

1. **Channel access control**:
    - Use Redis ACLs to restrict channel access
    - Implement application-level permissions

1. **Message validation**:
    - Validate message structure
    - Sign/verify important messages

---

## Implementing a Notification System

![implementing_a_notification_system](/svg/courses/databases/redis/04_pubsub/implementing_a_notification_system.svg)

---

## Real-time Metrics with Pub/Sub

![real_time_metrics_with_pub_sub](/svg/courses/databases/redis/04_pubsub/real_time_metrics_with_pub_sub.svg)

---

## Lab: Pub/Sub Messaging with Redis

1. **Exercise 1**: Set up basic publisher and subscriber
1. **Exercise 2**: Implement pattern-based subscriptions
1. **Exercise 3**: Create a simple chat system
1. **Exercise 4**: Implement cache invalidation with Pub/Sub
1. **Exercise 5**: Build a real-time dashboard with live updates
1. **Exercise 6**: Combine Pub/Sub with Streams for reliability
1. **Exercise 7**: Implement a notification system

---

## Summary

- Redis Pub/Sub provides simple, efficient messaging
- Great for real-time communication and broadcasting
- No message persistence by default
- Pattern subscriptions for flexible topic grouping
- Ideal for notifications, cache invalidation, and events
- Can be extended with Streams for persistence
- Easy to integrate with different programming languages

Next chapter: Redis Transactions and Scripting
