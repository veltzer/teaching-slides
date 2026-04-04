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

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd0_03_pubsub" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <!-- Publisher -->
  <rect x="20" y="70" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="70" y="92" text-anchor="middle" font-size="11" font-weight="bold">Publisher</text>
  <text x="70" y="106" text-anchor="middle" font-size="10">PUBLISH msg</text>
  <!-- Channel -->
  <rect x="220" y="60" width="140" height="70" fill="#fff3e0" stroke="#333" stroke-width="2" rx="8"/>
  <text x="290" y="85" text-anchor="middle" font-size="12" font-weight="bold">Channel</text>
  <text x="290" y="100" text-anchor="middle" font-size="10">"news:sports"</text>
  <text x="290" y="115" text-anchor="middle" font-size="10" fill="#666">fan-out delivery</text>
  <!-- Subscribers -->
  <rect x="460" y="30" width="110" height="40" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="515" y="55" text-anchor="middle" font-size="11">Subscriber A</text>
  <rect x="460" y="80" width="110" height="40" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="515" y="105" text-anchor="middle" font-size="11">Subscriber B</text>
  <rect x="460" y="130" width="110" height="40" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="515" y="155" text-anchor="middle" font-size="11">Subscriber C</text>
  <!-- Arrows -->
  <line x1="120" y1="95" x2="218" y2="95" stroke="#333" stroke-width="2" marker-end="url(#arrowd0_03_pubsub)"/>
  <line x1="360" y1="80" x2="458" y2="50" stroke="#333" stroke-width="2" marker-end="url(#arrowd0_03_pubsub)"/>
  <line x1="360" y1="95" x2="458" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd0_03_pubsub)"/>
  <line x1="360" y1="110" x2="458" y2="150" stroke="#333" stroke-width="2" marker-end="url(#arrowd0_03_pubsub)"/>
</svg>

---

## Pub/Sub vs. Other Communication Patterns

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd1_03_pubsub" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
    <marker id="arrowd1b_03_pubsub" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <!-- Request/Response -->
  <text x="100" y="20" text-anchor="middle" font-size="11" font-weight="bold">Request/Response</text>
  <rect x="20" y="30" width="70" height="35" fill="#e3f2fd" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="55" y="52" text-anchor="middle" font-size="10">Client</text>
  <rect x="120" y="30" width="70" height="35" fill="#f3e5f5" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="155" y="52" text-anchor="middle" font-size="10">Server</text>
  <line x1="90" y1="42" x2="118" y2="42" stroke="#333" stroke-width="1.5" marker-end="url(#arrowd1_03_pubsub)"/>
  <line x1="120" y1="55" x2="92" y2="55" stroke="#333" stroke-width="1.5" stroke-dasharray="4,3" marker-end="url(#arrowd1b_03_pubsub)"/>
  <!-- Message Queue -->
  <text x="310" y="20" text-anchor="middle" font-size="11" font-weight="bold">Message Queue</text>
  <rect x="225" y="30" width="70" height="35" fill="#e3f2fd" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="260" y="52" text-anchor="middle" font-size="10">Producer</text>
  <rect x="310" y="30" width="50" height="35" fill="#fff3e0" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="335" y="52" text-anchor="middle" font-size="10">Queue</text>
  <rect x="375" y="30" width="70" height="35" fill="#e8f5e9" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="410" y="52" text-anchor="middle" font-size="10">Consumer</text>
  <line x1="295" y1="48" x2="308" y2="48" stroke="#333" stroke-width="1.5" marker-end="url(#arrowd1_03_pubsub)"/>
  <line x1="360" y1="48" x2="373" y2="48" stroke="#333" stroke-width="1.5" marker-end="url(#arrowd1_03_pubsub)"/>
  <!-- Pub/Sub -->
  <text x="300" y="95" text-anchor="middle" font-size="11" font-weight="bold">Pub/Sub (broadcast to all)</text>
  <rect x="30" y="110" width="90" height="35" fill="#e3f2fd" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="75" y="132" text-anchor="middle" font-size="10">Publisher</text>
  <rect x="230" y="105" width="120" height="45" fill="#fff3e0" stroke="#333" stroke-width="1.5" rx="6"/>
  <text x="290" y="125" text-anchor="middle" font-size="10">Channel</text>
  <text x="290" y="140" text-anchor="middle" font-size="10" fill="#666">"events"</text>
  <rect x="440" y="100" width="90" height="30" fill="#e8f5e9" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="485" y="120" text-anchor="middle" font-size="10">Sub 1</text>
  <rect x="440" y="135" width="90" height="30" fill="#e8f5e9" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="485" y="155" text-anchor="middle" font-size="10">Sub 2</text>
  <rect x="440" y="170" width="90" height="30" fill="#e8f5e9" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="485" y="190" text-anchor="middle" font-size="10">Sub 3</text>
  <line x1="120" y1="128" x2="228" y2="128" stroke="#333" stroke-width="1.5" marker-end="url(#arrowd1_03_pubsub)"/>
  <line x1="350" y1="118" x2="438" y2="115" stroke="#333" stroke-width="1.5" marker-end="url(#arrowd1_03_pubsub)"/>
  <line x1="350" y1="128" x2="438" y2="150" stroke="#333" stroke-width="1.5" marker-end="url(#arrowd1_03_pubsub)"/>
  <line x1="350" y1="138" x2="438" y2="185" stroke="#333" stroke-width="1.5" marker-end="url(#arrowd1_03_pubsub)"/>
</svg>

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

<svg width="600" height="250" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd2_03_pubsub" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <!-- Lifelines -->
  <line x1="100" y1="50" x2="100" y2="240" stroke="#333" stroke-width="1.5" stroke-dasharray="4,3"/>
  <line x1="300" y1="50" x2="300" y2="240" stroke="#333" stroke-width="1.5" stroke-dasharray="4,3"/>
  <line x1="500" y1="50" x2="500" y2="240" stroke="#333" stroke-width="1.5" stroke-dasharray="4,3"/>
  <!-- Headers -->
  <rect x="45" y="15" width="110" height="35" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="4"/>
  <text x="100" y="37" text-anchor="middle" font-size="11" font-weight="bold">Subscriber</text>
  <rect x="245" y="15" width="110" height="35" fill="#fff3e0" stroke="#333" stroke-width="2" rx="4"/>
  <text x="300" y="37" text-anchor="middle" font-size="11" font-weight="bold">Redis Server</text>
  <rect x="445" y="15" width="110" height="35" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="4"/>
  <text x="500" y="37" text-anchor="middle" font-size="11" font-weight="bold">Publisher</text>
  <!-- Step 1: SUBSCRIBE -->
  <line x1="100" y1="75" x2="298" y2="75" stroke="#1565c0" stroke-width="2" marker-end="url(#arrowd2_03_pubsub)"/>
  <text x="200" y="70" text-anchor="middle" font-size="10" fill="#1565c0">SUBSCRIBE my-channel</text>
  <!-- Step 2: Subscribed confirmation -->
  <line x1="300" y1="105" x2="102" y2="105" stroke="#1565c0" stroke-width="1.5" stroke-dasharray="5,3" marker-end="url(#arrowd2_03_pubsub)"/>
  <text x="200" y="100" text-anchor="middle" font-size="10" fill="#666">subscribe confirmation</text>
  <!-- Step 3: PUBLISH -->
  <line x1="500" y1="140" x2="302" y2="140" stroke="#2e7d32" stroke-width="2" marker-end="url(#arrowd2_03_pubsub)"/>
  <text x="400" y="135" text-anchor="middle" font-size="10" fill="#2e7d32">PUBLISH my-channel "Hello"</text>
  <!-- Step 4: Deliver message -->
  <line x1="300" y1="170" x2="102" y2="170" stroke="#e65100" stroke-width="2" marker-end="url(#arrowd2_03_pubsub)"/>
  <text x="200" y="165" text-anchor="middle" font-size="10" fill="#e65100">message: "Hello"</text>
  <!-- Step 5: Return count -->
  <line x1="300" y1="200" x2="498" y2="200" stroke="#666" stroke-width="1.5" stroke-dasharray="5,3" marker-end="url(#arrowd2_03_pubsub)"/>
  <text x="400" y="195" text-anchor="middle" font-size="10" fill="#666">(integer) 1</text>
</svg>

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

<svg width="600" height="250" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd3_03_pubsub" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <!-- Chat Users -->
  <rect x="10" y="20" width="90" height="40" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="55" y="45" text-anchor="middle" font-size="11">User Alice</text>
  <rect x="10" y="90" width="90" height="40" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="55" y="115" text-anchor="middle" font-size="11">User Bob</text>
  <rect x="10" y="160" width="90" height="40" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="55" y="185" text-anchor="middle" font-size="11">User Carol</text>
  <!-- Redis -->
  <rect x="200" y="60" width="120" height="110" fill="#fff3e0" stroke="#333" stroke-width="2" rx="8"/>
  <text x="260" y="85" text-anchor="middle" font-size="12" font-weight="bold">Redis</text>
  <rect x="210" y="95" width="100" height="25" fill="#ffffff" stroke="#999" stroke-width="1" rx="3"/>
  <text x="260" y="112" text-anchor="middle" font-size="10">chat:room:general</text>
  <rect x="210" y="125" width="100" height="25" fill="#ffffff" stroke="#999" stroke-width="1" rx="3"/>
  <text x="260" y="142" text-anchor="middle" font-size="10">chat:room:dev</text>
  <!-- Chat Rooms / Subscribers -->
  <rect x="430" y="20" width="100" height="40" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="480" y="36" text-anchor="middle" font-size="10">Alice + Bob</text>
  <text x="480" y="50" text-anchor="middle" font-size="10" fill="#666">#general</text>
  <rect x="430" y="90" width="100" height="40" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="480" y="106" text-anchor="middle" font-size="10">Bob + Carol</text>
  <text x="480" y="120" text-anchor="middle" font-size="10" fill="#666">#dev</text>
  <!-- Arrows: publish -->
  <line x1="100" y1="40" x2="198" y2="105" stroke="#1565c0" stroke-width="1.5" marker-end="url(#arrowd3_03_pubsub)"/>
  <line x1="100" y1="110" x2="198" y2="115" stroke="#1565c0" stroke-width="1.5" marker-end="url(#arrowd3_03_pubsub)"/>
  <line x1="100" y1="180" x2="198" y2="140" stroke="#1565c0" stroke-width="1.5" marker-end="url(#arrowd3_03_pubsub)"/>
  <!-- Arrows: deliver -->
  <line x1="320" y1="107" x2="428" y2="40" stroke="#2e7d32" stroke-width="1.5" marker-end="url(#arrowd3_03_pubsub)"/>
  <line x1="320" y1="137" x2="428" y2="110" stroke="#2e7d32" stroke-width="1.5" marker-end="url(#arrowd3_03_pubsub)"/>
  <!-- Labels -->
  <text x="145" y="60" text-anchor="middle" font-size="10" fill="#1565c0">PUBLISH</text>
  <text x="380" y="65" text-anchor="middle" font-size="10" fill="#2e7d32">deliver</text>
  <!-- Legend -->
  <text x="300" y="210" text-anchor="middle" font-size="10" fill="#666">Each chat room = a Redis Pub/Sub channel</text>
  <text x="300" y="225" text-anchor="middle" font-size="10" fill="#666">Users subscribe to rooms they join</text>
</svg>

---

## Pub/Sub Use Case: Real-time Dashboard

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd4_03_pubsub" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <!-- Data Sources -->
  <rect x="10" y="15" width="95" height="35" fill="#e3f2fd" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="57" y="37" text-anchor="middle" font-size="10">Web Server</text>
  <rect x="10" y="60" width="95" height="35" fill="#e3f2fd" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="57" y="82" text-anchor="middle" font-size="10">API Service</text>
  <rect x="10" y="105" width="95" height="35" fill="#e3f2fd" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="57" y="127" text-anchor="middle" font-size="10">DB Monitor</text>
  <!-- Redis Channels -->
  <rect x="180" y="20" width="140" height="120" fill="#fff3e0" stroke="#333" stroke-width="2" rx="8"/>
  <text x="250" y="42" text-anchor="middle" font-size="11" font-weight="bold">Redis Channels</text>
  <rect x="190" y="50" width="120" height="22" fill="#fff" stroke="#999" stroke-width="1" rx="3"/>
  <text x="250" y="65" text-anchor="middle" font-size="10">metrics:cpu</text>
  <rect x="190" y="77" width="120" height="22" fill="#fff" stroke="#999" stroke-width="1" rx="3"/>
  <text x="250" y="92" text-anchor="middle" font-size="10">metrics:requests</text>
  <rect x="190" y="104" width="120" height="22" fill="#fff" stroke="#999" stroke-width="1" rx="3"/>
  <text x="250" y="119" text-anchor="middle" font-size="10">metrics:errors</text>
  <!-- Dashboard -->
  <rect x="400" y="25" width="160" height="110" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="8"/>
  <text x="480" y="48" text-anchor="middle" font-size="11" font-weight="bold">Live Dashboard</text>
  <rect x="415" y="58" width="60" height="30" fill="#fff" stroke="#999" stroke-width="1" rx="3"/>
  <text x="445" y="77" text-anchor="middle" font-size="10">CPU %</text>
  <rect x="485" y="58" width="60" height="30" fill="#fff" stroke="#999" stroke-width="1" rx="3"/>
  <text x="515" y="77" text-anchor="middle" font-size="10">RPS</text>
  <rect x="415" y="95" width="130" height="30" fill="#ffebee" stroke="#999" stroke-width="1" rx="3"/>
  <text x="480" y="114" text-anchor="middle" font-size="10">Error Alerts</text>
  <!-- Arrows -->
  <line x1="105" y1="32" x2="178" y2="60" stroke="#333" stroke-width="1.5" marker-end="url(#arrowd4_03_pubsub)"/>
  <line x1="105" y1="78" x2="178" y2="88" stroke="#333" stroke-width="1.5" marker-end="url(#arrowd4_03_pubsub)"/>
  <line x1="105" y1="122" x2="178" y2="115" stroke="#333" stroke-width="1.5" marker-end="url(#arrowd4_03_pubsub)"/>
  <line x1="320" y1="80" x2="398" y2="80" stroke="#2e7d32" stroke-width="2" marker-end="url(#arrowd4_03_pubsub)"/>
  <!-- Labels -->
  <text x="140" y="160" text-anchor="middle" font-size="10" fill="#1565c0">PUBLISH</text>
  <text x="360" y="68" text-anchor="middle" font-size="10" fill="#2e7d32">SUBSCRIBE</text>
  <text x="300" y="180" text-anchor="middle" font-size="10" fill="#666">Real-time metrics streamed via Pub/Sub to dashboard</text>
</svg>

---

## Pub/Sub Use Case: Cache Invalidation

<svg width="600" height="250" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd5_03_pubsub" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <!-- Step labels -->
  <text x="300" y="15" text-anchor="middle" font-size="12" font-weight="bold" fill="#333">Cache Invalidation via Pub/Sub</text>
  <!-- Write Service -->
  <rect x="10" y="40" width="110" height="45" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="65" y="58" text-anchor="middle" font-size="11" font-weight="bold">Write Service</text>
  <text x="65" y="73" text-anchor="middle" font-size="10" fill="#666">updates DB</text>
  <!-- Redis -->
  <rect x="220" y="35" width="130" height="55" fill="#fff3e0" stroke="#333" stroke-width="2" rx="8"/>
  <text x="285" y="57" text-anchor="middle" font-size="11" font-weight="bold">Redis Pub/Sub</text>
  <text x="285" y="73" text-anchor="middle" font-size="10">cache:invalidate</text>
  <!-- Cache Nodes -->
  <rect x="455" y="25" width="110" height="35" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="510" y="47" text-anchor="middle" font-size="10">App Server 1</text>
  <rect x="455" y="68" width="110" height="35" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="510" y="90" text-anchor="middle" font-size="10">App Server 2</text>
  <!-- Step 1 arrow -->
  <line x1="120" y1="62" x2="218" y2="62" stroke="#1565c0" stroke-width="2" marker-end="url(#arrowd5_03_pubsub)"/>
  <text x="170" y="55" text-anchor="middle" font-size="10" fill="#1565c0">1. PUBLISH</text>
  <!-- Step 2 arrows -->
  <line x1="350" y1="52" x2="453" y2="42" stroke="#2e7d32" stroke-width="2" marker-end="url(#arrowd5_03_pubsub)"/>
  <line x1="350" y1="68" x2="453" y2="85" stroke="#2e7d32" stroke-width="2" marker-end="url(#arrowd5_03_pubsub)"/>
  <text x="400" y="45" text-anchor="middle" font-size="10" fill="#2e7d32">2. notify</text>
  <!-- Local cache boxes with X -->
  <rect x="460" y="115" width="100" height="35" fill="#ffebee" stroke="#c62828" stroke-width="1.5" rx="4"/>
  <text x="510" y="130" text-anchor="middle" font-size="10" fill="#c62828">Local Cache</text>
  <text x="510" y="143" text-anchor="middle" font-size="11" fill="#c62828" font-weight="bold">DEL key</text>
  <!-- Step 3 arrows from servers to cache -->
  <line x1="510" y1="103" x2="510" y2="113" stroke="#c62828" stroke-width="1.5" marker-end="url(#arrowd5_03_pubsub)"/>
  <text x="545" y="112" font-size="10" fill="#c62828">3.</text>
  <!-- Flow description -->
  <rect x="30" y="140" width="340" height="95" fill="#f5f5f5" stroke="#999" stroke-width="1" rx="5"/>
  <text x="50" y="162" font-size="10" fill="#333">1. Write service updates DB and publishes invalidation</text>
  <text x="50" y="180" font-size="10" fill="#333">2. Redis delivers to all subscribed app servers</text>
  <text x="50" y="198" font-size="10" fill="#333">3. Each server evicts stale key from local cache</text>
  <text x="50" y="220" font-size="10" fill="#666">Result: all caches stay consistent without polling</text>
</svg>

---

## Pub/Sub Use Case: Microservices Communication

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd6_03_pubsub" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <!-- Microservices -->
  <rect x="10" y="15" width="100" height="35" fill="#e3f2fd" stroke="#333" stroke-width="1.5" rx="5"/>
  <text x="60" y="37" text-anchor="middle" font-size="10">Order Service</text>
  <rect x="10" y="65" width="100" height="35" fill="#e3f2fd" stroke="#333" stroke-width="1.5" rx="5"/>
  <text x="60" y="87" text-anchor="middle" font-size="10">User Service</text>
  <!-- Redis hub -->
  <rect x="195" y="20" width="130" height="110" fill="#fff3e0" stroke="#333" stroke-width="2" rx="10"/>
  <text x="260" y="42" text-anchor="middle" font-size="11" font-weight="bold">Redis Pub/Sub</text>
  <rect x="205" y="50" width="110" height="20" fill="#fff" stroke="#999" stroke-width="1" rx="3"/>
  <text x="260" y="64" text-anchor="middle" font-size="10">order:created</text>
  <rect x="205" y="75" width="110" height="20" fill="#fff" stroke="#999" stroke-width="1" rx="3"/>
  <text x="260" y="89" text-anchor="middle" font-size="10">user:updated</text>
  <rect x="205" y="100" width="110" height="20" fill="#fff" stroke="#999" stroke-width="1" rx="3"/>
  <text x="260" y="114" text-anchor="middle" font-size="10">payment:complete</text>
  <!-- Subscribing services -->
  <rect x="410" y="10" width="110" height="30" fill="#e8f5e9" stroke="#333" stroke-width="1.5" rx="5"/>
  <text x="465" y="30" text-anchor="middle" font-size="10">Email Service</text>
  <rect x="410" y="50" width="110" height="30" fill="#e8f5e9" stroke="#333" stroke-width="1.5" rx="5"/>
  <text x="465" y="70" text-anchor="middle" font-size="10">Inventory Svc</text>
  <rect x="410" y="90" width="110" height="30" fill="#f3e5f5" stroke="#333" stroke-width="1.5" rx="5"/>
  <text x="465" y="110" text-anchor="middle" font-size="10">Analytics Svc</text>
  <rect x="410" y="130" width="110" height="30" fill="#f3e5f5" stroke="#333" stroke-width="1.5" rx="5"/>
  <text x="465" y="150" text-anchor="middle" font-size="10">Billing Service</text>
  <!-- Publish arrows -->
  <line x1="110" y1="32" x2="193" y2="60" stroke="#1565c0" stroke-width="1.5" marker-end="url(#arrowd6_03_pubsub)"/>
  <line x1="110" y1="82" x2="193" y2="85" stroke="#1565c0" stroke-width="1.5" marker-end="url(#arrowd6_03_pubsub)"/>
  <!-- Subscribe arrows -->
  <line x1="325" y1="55" x2="408" y2="25" stroke="#2e7d32" stroke-width="1.5" marker-end="url(#arrowd6_03_pubsub)"/>
  <line x1="325" y1="65" x2="408" y2="65" stroke="#2e7d32" stroke-width="1.5" marker-end="url(#arrowd6_03_pubsub)"/>
  <line x1="325" y1="85" x2="408" y2="105" stroke="#2e7d32" stroke-width="1.5" marker-end="url(#arrowd6_03_pubsub)"/>
  <line x1="325" y1="110" x2="408" y2="145" stroke="#2e7d32" stroke-width="1.5" marker-end="url(#arrowd6_03_pubsub)"/>
  <!-- Legend -->
  <text x="300" y="185" text-anchor="middle" font-size="10" fill="#666">Services communicate via events -- no direct coupling</text>
</svg>

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

<svg width="600" height="250" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd7_03_pubsub" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <!-- Lifelines -->
  <line x1="100" y1="55" x2="100" y2="240" stroke="#333" stroke-width="1.5" stroke-dasharray="4,3"/>
  <line x1="300" y1="55" x2="300" y2="240" stroke="#333" stroke-width="1.5" stroke-dasharray="4,3"/>
  <line x1="500" y1="55" x2="500" y2="240" stroke="#333" stroke-width="1.5" stroke-dasharray="4,3"/>
  <!-- Headers -->
  <rect x="40" y="15" width="120" height="35" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="4"/>
  <text x="100" y="37" text-anchor="middle" font-size="11" font-weight="bold">Publisher</text>
  <rect x="240" y="15" width="120" height="35" fill="#fff3e0" stroke="#333" stroke-width="2" rx="4"/>
  <text x="300" y="37" text-anchor="middle" font-size="11" font-weight="bold">Redis</text>
  <rect x="440" y="15" width="120" height="35" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="4"/>
  <text x="500" y="37" text-anchor="middle" font-size="11" font-weight="bold">Subscriber</text>
  <!-- Step 1: Publish with msg ID -->
  <line x1="100" y1="75" x2="298" y2="75" stroke="#1565c0" stroke-width="2" marker-end="url(#arrowd7_03_pubsub)"/>
  <text x="200" y="70" text-anchor="middle" font-size="10" fill="#1565c0">1. PUBLISH task:{id:"t1", data:...}</text>
  <!-- Step 2: Deliver -->
  <line x1="300" y1="100" x2="498" y2="100" stroke="#2e7d32" stroke-width="2" marker-end="url(#arrowd7_03_pubsub)"/>
  <text x="400" y="95" text-anchor="middle" font-size="10" fill="#2e7d32">2. deliver message</text>
  <!-- Step 3: Process -->
  <rect x="475" y="110" width="50" height="25" fill="#e8f5e9" stroke="#2e7d32" stroke-width="1" rx="3"/>
  <text x="500" y="127" text-anchor="middle" font-size="10" fill="#2e7d32">process</text>
  <!-- Step 4: ACK back -->
  <line x1="500" y1="150" x2="302" y2="150" stroke="#e65100" stroke-width="2" marker-end="url(#arrowd7_03_pubsub)"/>
  <text x="400" y="145" text-anchor="middle" font-size="10" fill="#e65100">3. PUBLISH ack:{id:"t1"}</text>
  <!-- Step 5: Deliver ACK -->
  <line x1="300" y1="175" x2="102" y2="175" stroke="#e65100" stroke-width="2" marker-end="url(#arrowd7_03_pubsub)"/>
  <text x="200" y="170" text-anchor="middle" font-size="10" fill="#e65100">4. deliver ACK</text>
  <!-- Timeout note -->
  <rect x="20" y="195" width="180" height="40" fill="#ffebee" stroke="#c62828" stroke-width="1" rx="4"/>
  <text x="110" y="212" text-anchor="middle" font-size="10" fill="#c62828">If no ACK within timeout:</text>
  <text x="110" y="226" text-anchor="middle" font-size="10" fill="#c62828">re-publish message</text>
</svg>

---

## Sentinel Events with Pub/Sub

Use Redis Pub/Sub for Redis Sentinel events:

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd8_03_pubsub" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <!-- Sentinel nodes -->
  <rect x="15" y="10" width="90" height="35" fill="#f3e5f5" stroke="#333" stroke-width="1.5" rx="5"/>
  <text x="60" y="32" text-anchor="middle" font-size="10">Sentinel 1</text>
  <rect x="15" y="55" width="90" height="35" fill="#f3e5f5" stroke="#333" stroke-width="1.5" rx="5"/>
  <text x="60" y="77" text-anchor="middle" font-size="10">Sentinel 2</text>
  <rect x="15" y="100" width="90" height="35" fill="#f3e5f5" stroke="#333" stroke-width="1.5" rx="5"/>
  <text x="60" y="122" text-anchor="middle" font-size="10">Sentinel 3</text>
  <!-- Sentinel Pub/Sub channels -->
  <rect x="185" y="15" width="170" height="120" fill="#fff3e0" stroke="#333" stroke-width="2" rx="8"/>
  <text x="270" y="35" text-anchor="middle" font-size="11" font-weight="bold">Sentinel Channels</text>
  <rect x="195" y="42" width="150" height="20" fill="#ffebee" stroke="#c62828" stroke-width="1" rx="3"/>
  <text x="270" y="56" text-anchor="middle" font-size="10" fill="#c62828">+sdown (subj. down)</text>
  <rect x="195" y="67" width="150" height="20" fill="#ffebee" stroke="#c62828" stroke-width="1" rx="3"/>
  <text x="270" y="81" text-anchor="middle" font-size="10" fill="#c62828">+odown (obj. down)</text>
  <rect x="195" y="92" width="150" height="20" fill="#e8f5e9" stroke="#2e7d32" stroke-width="1" rx="3"/>
  <text x="270" y="106" text-anchor="middle" font-size="10" fill="#2e7d32">+switch-master</text>
  <rect x="195" y="117" width="150" height="12" fill="#fff" stroke="#999" stroke-width="1" rx="3"/>
  <text x="270" y="127" text-anchor="middle" font-size="9" fill="#666">...more events</text>
  <!-- Application -->
  <rect x="440" y="35" width="120" height="80" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="8"/>
  <text x="500" y="58" text-anchor="middle" font-size="11" font-weight="bold">Application</text>
  <text x="500" y="75" text-anchor="middle" font-size="10">SUBSCRIBE</text>
  <text x="500" y="90" text-anchor="middle" font-size="10">+switch-master</text>
  <text x="500" y="105" text-anchor="middle" font-size="10" fill="#666">reconnect logic</text>
  <!-- Arrows -->
  <line x1="105" y1="28" x2="183" y2="50" stroke="#333" stroke-width="1.5" marker-end="url(#arrowd8_03_pubsub)"/>
  <line x1="105" y1="72" x2="183" y2="75" stroke="#333" stroke-width="1.5" marker-end="url(#arrowd8_03_pubsub)"/>
  <line x1="105" y1="118" x2="183" y2="102" stroke="#333" stroke-width="1.5" marker-end="url(#arrowd8_03_pubsub)"/>
  <line x1="355" y1="75" x2="438" y2="75" stroke="#2e7d32" stroke-width="2" marker-end="url(#arrowd8_03_pubsub)"/>
  <!-- Bottom label -->
  <text x="300" y="170" text-anchor="middle" font-size="10" fill="#666">Apps subscribe to Sentinel events for automatic failover handling</text>
</svg>

---

## Introduction to Redis Streams

Streams (introduced in Redis 5.0):
- Append-only data structures
- Persistent append-only logs
- Support consumer groups
- Perfect complement to Pub/Sub

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd9_03_pubsub" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <!-- Producer -->
  <rect x="10" y="60" width="90" height="40" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="55" y="76" text-anchor="middle" font-size="10" font-weight="bold">Producer</text>
  <text x="55" y="90" text-anchor="middle" font-size="10">XADD</text>
  <!-- Stream (append-only log) -->
  <rect x="155" y="30" width="270" height="100" fill="#fff3e0" stroke="#333" stroke-width="2" rx="8"/>
  <text x="290" y="50" text-anchor="middle" font-size="11" font-weight="bold">Redis Stream (append-only log)</text>
  <!-- Stream entries -->
  <rect x="165" y="60" width="75" height="30" fill="#fff" stroke="#999" stroke-width="1" rx="3"/>
  <text x="202" y="73" text-anchor="middle" font-size="9">1609459200-0</text>
  <text x="202" y="85" text-anchor="middle" font-size="9" fill="#666">{temp:22}</text>
  <rect x="248" y="60" width="75" height="30" fill="#fff" stroke="#999" stroke-width="1" rx="3"/>
  <text x="285" y="73" text-anchor="middle" font-size="9">1609459201-0</text>
  <text x="285" y="85" text-anchor="middle" font-size="9" fill="#666">{temp:23}</text>
  <rect x="331" y="60" width="75" height="30" fill="#fff" stroke="#999" stroke-width="1" rx="3"/>
  <text x="368" y="73" text-anchor="middle" font-size="9">1609459202-0</text>
  <text x="368" y="85" text-anchor="middle" font-size="9" fill="#666">{temp:21}</text>
  <!-- Persistent indicator -->
  <text x="290" y="118" text-anchor="middle" font-size="10" fill="#e65100">persisted on disk -- survives restart</text>
  <!-- Consumer Group -->
  <rect x="475" y="20" width="110" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="530" y="38" text-anchor="middle" font-size="10" font-weight="bold">Consumer Grp</text>
  <text x="530" y="52" text-anchor="middle" font-size="10">XREADGROUP</text>
  <!-- Single consumer -->
  <rect x="475" y="90" width="110" height="40" fill="#f3e5f5" stroke="#333" stroke-width="1.5" rx="5"/>
  <text x="530" y="108" text-anchor="middle" font-size="10">Consumer</text>
  <text x="530" y="122" text-anchor="middle" font-size="10">XREAD</text>
  <!-- Arrows -->
  <line x1="100" y1="80" x2="153" y2="80" stroke="#1565c0" stroke-width="2" marker-end="url(#arrowd9_03_pubsub)"/>
  <line x1="425" y1="55" x2="473" y2="45" stroke="#2e7d32" stroke-width="1.5" marker-end="url(#arrowd9_03_pubsub)"/>
  <line x1="425" y1="80" x2="473" y2="105" stroke="#2e7d32" stroke-width="1.5" marker-end="url(#arrowd9_03_pubsub)"/>
  <!-- Bottom label -->
  <text x="290" y="165" text-anchor="middle" font-size="10" fill="#666">Unlike Pub/Sub: messages are stored, replayable, and support consumer groups</text>
</svg>

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

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd10_03_pubsub" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <!-- Pub/Sub side -->
  <rect x="10" y="15" width="250" height="160" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="8"/>
  <text x="135" y="35" text-anchor="middle" font-size="12" font-weight="bold">Pub/Sub</text>
  <text x="135" y="55" text-anchor="middle" font-size="10">Fire-and-forget broadcast</text>
  <text x="30" y="75" font-size="10" fill="#333">+ Real-time, low latency</text>
  <text x="30" y="92" font-size="10" fill="#333">+ All subscribers get all msgs</text>
  <text x="30" y="109" font-size="10" fill="#333">+ Simple API</text>
  <text x="30" y="130" font-size="10" fill="#c62828">- No persistence</text>
  <text x="30" y="147" font-size="10" fill="#c62828">- No replay / history</text>
  <text x="30" y="164" font-size="10" fill="#c62828">- No consumer groups</text>
  <!-- Streams side -->
  <rect x="290" y="15" width="280" height="160" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="8"/>
  <text x="430" y="35" text-anchor="middle" font-size="12" font-weight="bold">Streams</text>
  <text x="430" y="55" text-anchor="middle" font-size="10">Persistent log with consumers</text>
  <text x="310" y="75" font-size="10" fill="#333">+ Messages persisted on disk</text>
  <text x="310" y="92" font-size="10" fill="#333">+ Consumer groups / load balance</text>
  <text x="310" y="109" font-size="10" fill="#333">+ Message ACK and replay</text>
  <text x="310" y="130" font-size="10" fill="#c62828">- Higher latency than Pub/Sub</text>
  <text x="310" y="147" font-size="10" fill="#c62828">- More complex API</text>
  <text x="310" y="164" font-size="10" fill="#c62828">- Needs storage management</text>
  <!-- VS divider -->
  <text x="275" y="100" text-anchor="middle" font-size="13" font-weight="bold" fill="#333">vs</text>
</svg>

---

## Combining Pub/Sub with Streams

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd11_03_pubsub" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <!-- Producer -->
  <rect x="10" y="55" width="90" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="55" y="76" text-anchor="middle" font-size="11" font-weight="bold">Producer</text>
  <text x="55" y="92" text-anchor="middle" font-size="10" fill="#666">app code</text>
  <!-- Redis box -->
  <rect x="155" y="15" width="230" height="155" fill="#fff3e0" stroke="#333" stroke-width="2" rx="8"/>
  <text x="270" y="35" text-anchor="middle" font-size="11" font-weight="bold">Redis Server</text>
  <!-- Stream storage -->
  <rect x="170" y="45" width="120" height="40" fill="#e8f5e9" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="230" y="62" text-anchor="middle" font-size="10" font-weight="bold">Stream</text>
  <text x="230" y="78" text-anchor="middle" font-size="10">XADD (persist)</text>
  <!-- Pub/Sub channel -->
  <rect x="170" y="100" width="120" height="40" fill="#f3e5f5" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="230" y="117" text-anchor="middle" font-size="10" font-weight="bold">Pub/Sub</text>
  <text x="230" y="133" text-anchor="middle" font-size="10">PUBLISH (notify)</text>
  <!-- Arrow from stream to pubsub -->
  <line x1="230" y1="85" x2="230" y2="98" stroke="#e65100" stroke-width="1.5" marker-end="url(#arrowd11_03_pubsub)"/>
  <text x="310" y="95" font-size="9" fill="#e65100">trigger</text>
  <!-- Real-time subscriber -->
  <rect x="450" y="25" width="120" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="510" y="45" text-anchor="middle" font-size="10" font-weight="bold">Live Consumer</text>
  <text x="510" y="60" text-anchor="middle" font-size="10">SUBSCRIBE</text>
  <!-- Late/catch-up consumer -->
  <rect x="450" y="100" width="120" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="510" y="118" text-anchor="middle" font-size="10" font-weight="bold">Catch-up</text>
  <text x="510" y="135" text-anchor="middle" font-size="10">XREAD / XRANGE</text>
  <!-- Arrows -->
  <line x1="100" y1="72" x2="168" y2="60" stroke="#1565c0" stroke-width="2" marker-end="url(#arrowd11_03_pubsub)"/>
  <line x1="100" y1="88" x2="168" y2="118" stroke="#1565c0" stroke-width="2" marker-end="url(#arrowd11_03_pubsub)"/>
  <text x="125" y="60" font-size="9" fill="#1565c0">1. XADD</text>
  <text x="110" y="118" font-size="9" fill="#1565c0">2. PUBLISH</text>
  <line x1="290" y1="120" x2="448" y2="50" stroke="#2e7d32" stroke-width="1.5" marker-end="url(#arrowd11_03_pubsub)"/>
  <line x1="290" y1="65" x2="448" y2="125" stroke="#9c27b0" stroke-width="1.5" stroke-dasharray="5,3" marker-end="url(#arrowd11_03_pubsub)"/>
  <!-- Legend -->
  <text x="300" y="190" text-anchor="middle" font-size="10" fill="#666">Stream for persistence + Pub/Sub for real-time notification</text>
</svg>

---

## Scaling Pub/Sub with Redis Cluster

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd12_03_pubsub" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <!-- Publisher client -->
  <rect x="10" y="70" width="90" height="40" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="55" y="86" text-anchor="middle" font-size="10" font-weight="bold">Publisher</text>
  <text x="55" y="100" text-anchor="middle" font-size="10">PUBLISH</text>
  <!-- Cluster nodes -->
  <rect x="155" y="10" width="290" height="160" fill="#f5f5f5" stroke="#333" stroke-width="2" rx="10" stroke-dasharray="5,3"/>
  <text x="300" y="28" text-anchor="middle" font-size="11" font-weight="bold">Redis Cluster</text>
  <rect x="170" y="40" width="80" height="45" fill="#fff3e0" stroke="#333" stroke-width="1.5" rx="5"/>
  <text x="210" y="58" text-anchor="middle" font-size="10" font-weight="bold">Node A</text>
  <text x="210" y="73" text-anchor="middle" font-size="9" fill="#666">slots 0-5460</text>
  <rect x="260" y="40" width="80" height="45" fill="#fff3e0" stroke="#333" stroke-width="1.5" rx="5"/>
  <text x="300" y="58" text-anchor="middle" font-size="10" font-weight="bold">Node B</text>
  <text x="300" y="73" text-anchor="middle" font-size="9" fill="#666">slots 5461-10922</text>
  <rect x="350" y="40" width="80" height="45" fill="#fff3e0" stroke="#333" stroke-width="1.5" rx="5"/>
  <text x="390" y="58" text-anchor="middle" font-size="10" font-weight="bold">Node C</text>
  <text x="390" y="73" text-anchor="middle" font-size="9" fill="#666">slots 10923-16383</text>
  <!-- Broadcast arrows between nodes -->
  <line x1="210" y1="85" x2="210" y2="105" stroke="#e65100" stroke-width="1" marker-end="url(#arrowd12_03_pubsub)"/>
  <line x1="300" y1="85" x2="300" y2="105" stroke="#e65100" stroke-width="1" marker-end="url(#arrowd12_03_pubsub)"/>
  <line x1="390" y1="85" x2="390" y2="105" stroke="#e65100" stroke-width="1" marker-end="url(#arrowd12_03_pubsub)"/>
  <!-- Broadcast note -->
  <rect x="175" y="105" width="250" height="22" fill="#ffebee" stroke="#c62828" stroke-width="1" rx="3"/>
  <text x="300" y="120" text-anchor="middle" font-size="10" fill="#c62828">PUBLISH broadcasts to ALL nodes</text>
  <!-- Subscribers on different nodes -->
  <rect x="170" y="135" width="80" height="25" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="4"/>
  <text x="210" y="152" text-anchor="middle" font-size="10">Sub on A</text>
  <rect x="350" y="135" width="80" height="25" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="4"/>
  <text x="390" y="152" text-anchor="middle" font-size="10">Sub on C</text>
  <!-- Publisher arrow -->
  <line x1="100" y1="90" x2="168" y2="62" stroke="#1565c0" stroke-width="2" marker-end="url(#arrowd12_03_pubsub)"/>
  <!-- Subscriber clients -->
  <rect x="500" y="40" width="80" height="35" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="540" y="55" text-anchor="middle" font-size="10">Sub Client</text>
  <text x="540" y="68" text-anchor="middle" font-size="10" fill="#666">any node</text>
  <line x1="430" y1="62" x2="498" y2="57" stroke="#2e7d32" stroke-width="1.5" marker-end="url(#arrowd12_03_pubsub)"/>
  <!-- Note -->
  <text x="300" y="190" text-anchor="middle" font-size="10" fill="#666">Messages propagated cluster-wide via internal bus</text>
</svg>

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

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd13_03_pubsub" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <!-- Event sources -->
  <rect x="10" y="15" width="100" height="30" fill="#e3f2fd" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="60" y="35" text-anchor="middle" font-size="10">New Order</text>
  <rect x="10" y="55" width="100" height="30" fill="#e3f2fd" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="60" y="75" text-anchor="middle" font-size="10">User Signup</text>
  <rect x="10" y="95" width="100" height="30" fill="#ffebee" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="60" y="115" text-anchor="middle" font-size="10">System Alert</text>
  <!-- Redis channels -->
  <rect x="175" y="10" width="160" height="125" fill="#fff3e0" stroke="#333" stroke-width="2" rx="8"/>
  <text x="255" y="30" text-anchor="middle" font-size="11" font-weight="bold">Redis Channels</text>
  <rect x="185" y="38" width="140" height="20" fill="#fff" stroke="#999" stroke-width="1" rx="3"/>
  <text x="255" y="52" text-anchor="middle" font-size="10">notify:user:{uid}:order</text>
  <rect x="185" y="63" width="140" height="20" fill="#fff" stroke="#999" stroke-width="1" rx="3"/>
  <text x="255" y="77" text-anchor="middle" font-size="10">notify:admin:signup</text>
  <rect x="185" y="88" width="140" height="20" fill="#fff" stroke="#999" stroke-width="1" rx="3"/>
  <text x="255" y="102" text-anchor="middle" font-size="10">notify:ops:alert</text>
  <text x="255" y="128" text-anchor="middle" font-size="9" fill="#666">PSUBSCRIBE notify:*</text>
  <!-- Notification handlers -->
  <rect x="415" y="10" width="130" height="35" fill="#e8f5e9" stroke="#333" stroke-width="1.5" rx="5"/>
  <text x="480" y="24" text-anchor="middle" font-size="10" font-weight="bold">Push Handler</text>
  <text x="480" y="38" text-anchor="middle" font-size="10" fill="#666">WebSocket/SSE</text>
  <rect x="415" y="55" width="130" height="35" fill="#f3e5f5" stroke="#333" stroke-width="1.5" rx="5"/>
  <text x="480" y="69" text-anchor="middle" font-size="10" font-weight="bold">Email Handler</text>
  <text x="480" y="83" text-anchor="middle" font-size="10" fill="#666">SMTP queue</text>
  <rect x="415" y="100" width="130" height="35" fill="#ffebee" stroke="#333" stroke-width="1.5" rx="5"/>
  <text x="480" y="114" text-anchor="middle" font-size="10" font-weight="bold">SMS Handler</text>
  <text x="480" y="128" text-anchor="middle" font-size="10" fill="#666">Twilio API</text>
  <!-- Arrows -->
  <line x1="110" y1="30" x2="173" y2="48" stroke="#1565c0" stroke-width="1.5" marker-end="url(#arrowd13_03_pubsub)"/>
  <line x1="110" y1="70" x2="173" y2="73" stroke="#1565c0" stroke-width="1.5" marker-end="url(#arrowd13_03_pubsub)"/>
  <line x1="110" y1="110" x2="173" y2="98" stroke="#1565c0" stroke-width="1.5" marker-end="url(#arrowd13_03_pubsub)"/>
  <line x1="335" y1="48" x2="413" y2="27" stroke="#2e7d32" stroke-width="1.5" marker-end="url(#arrowd13_03_pubsub)"/>
  <line x1="335" y1="73" x2="413" y2="72" stroke="#2e7d32" stroke-width="1.5" marker-end="url(#arrowd13_03_pubsub)"/>
  <line x1="335" y1="98" x2="413" y2="117" stroke="#2e7d32" stroke-width="1.5" marker-end="url(#arrowd13_03_pubsub)"/>
  <!-- Legend -->
  <text x="300" y="165" text-anchor="middle" font-size="10" fill="#666">Pattern subscriptions route notifications to appropriate handlers</text>
  <text x="300" y="180" text-anchor="middle" font-size="10" fill="#666">Each handler processes only relevant notification types</text>
</svg>

---

## Real-time Metrics with Pub/Sub

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd14_03_pubsub" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <!-- Metric collectors -->
  <rect x="10" y="10" width="95" height="40" fill="#e3f2fd" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="57" y="27" text-anchor="middle" font-size="10" font-weight="bold">App Server</text>
  <text x="57" y="42" text-anchor="middle" font-size="10" fill="#666">CPU, mem, rps</text>
  <rect x="10" y="60" width="95" height="40" fill="#e3f2fd" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="57" y="77" text-anchor="middle" font-size="10" font-weight="bold">DB Server</text>
  <text x="57" y="92" text-anchor="middle" font-size="10" fill="#666">queries/s, lag</text>
  <rect x="10" y="110" width="95" height="40" fill="#e3f2fd" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="57" y="127" text-anchor="middle" font-size="10" font-weight="bold">Load Balancer</text>
  <text x="57" y="142" text-anchor="middle" font-size="10" fill="#666">connections</text>
  <!-- Redis -->
  <rect x="175" y="25" width="130" height="110" fill="#fff3e0" stroke="#333" stroke-width="2" rx="8"/>
  <text x="240" y="45" text-anchor="middle" font-size="11" font-weight="bold">Redis</text>
  <rect x="185" y="52" width="110" height="18" fill="#fff" stroke="#999" stroke-width="1" rx="3"/>
  <text x="240" y="65" text-anchor="middle" font-size="9">metrics:app:*</text>
  <rect x="185" y="74" width="110" height="18" fill="#fff" stroke="#999" stroke-width="1" rx="3"/>
  <text x="240" y="87" text-anchor="middle" font-size="9">metrics:db:*</text>
  <rect x="185" y="96" width="110" height="18" fill="#fff" stroke="#999" stroke-width="1" rx="3"/>
  <text x="240" y="109" text-anchor="middle" font-size="9">metrics:lb:*</text>
  <!-- Aggregator -->
  <rect x="375" y="35" width="100" height="45" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="425" y="53" text-anchor="middle" font-size="10" font-weight="bold">Aggregator</text>
  <text x="425" y="68" text-anchor="middle" font-size="10">PSUBSCRIBE</text>
  <text x="425" y="78" text-anchor="middle" font-size="9" fill="#666">metrics:*</text>
  <!-- Grafana / Dashboard -->
  <rect x="375" y="95" width="100" height="40" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="425" y="113" text-anchor="middle" font-size="10" font-weight="bold">Grafana</text>
  <text x="425" y="127" text-anchor="middle" font-size="10" fill="#666">live graphs</text>
  <!-- Alert engine -->
  <rect x="500" y="35" width="85" height="45" fill="#ffebee" stroke="#333" stroke-width="1.5" rx="5"/>
  <text x="542" y="53" text-anchor="middle" font-size="10" font-weight="bold">Alert Eng.</text>
  <text x="542" y="68" text-anchor="middle" font-size="10" fill="#c62828">thresholds</text>
  <!-- Arrows -->
  <line x1="105" y1="30" x2="173" y2="60" stroke="#1565c0" stroke-width="1.5" marker-end="url(#arrowd14_03_pubsub)"/>
  <line x1="105" y1="80" x2="173" y2="83" stroke="#1565c0" stroke-width="1.5" marker-end="url(#arrowd14_03_pubsub)"/>
  <line x1="105" y1="130" x2="173" y2="105" stroke="#1565c0" stroke-width="1.5" marker-end="url(#arrowd14_03_pubsub)"/>
  <line x1="305" y1="60" x2="373" y2="57" stroke="#2e7d32" stroke-width="1.5" marker-end="url(#arrowd14_03_pubsub)"/>
  <line x1="425" y1="80" x2="425" y2="93" stroke="#333" stroke-width="1.5" marker-end="url(#arrowd14_03_pubsub)"/>
  <line x1="305" y1="75" x2="498" y2="57" stroke="#c62828" stroke-width="1.5" marker-end="url(#arrowd14_03_pubsub)"/>
  <!-- Legend -->
  <text x="300" y="175" text-anchor="middle" font-size="10" fill="#666">Servers publish metrics every N seconds; consumers process in real-time</text>
  <text x="300" y="190" text-anchor="middle" font-size="10" fill="#666">Pattern subscriptions (metrics:*) capture all metric channels at once</text>
</svg>

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
