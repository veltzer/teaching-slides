---
tags:
  - concepts:architecture
  - concepts:messaging
  - concepts:distributed-systems
level: intermediate
category: architecture
audience:
  - audiences:developers
  - audiences:architects

---
# Queues in Distributed Systems

---

## Agenda

1. Understanding Queues
1. Queue Types and Patterns
1. Message Ordering and Delivery
1. Operational Patterns (DLQ, retries, scaling)
1. Advanced Concepts

Note: side-by-side comparison of Kafka, SQS, and RabbitMQ lives in ch 12.

---

## What are Queues

- Asynchronous communication mechanism
- Decouples producers and consumers
- Handles backpressure
- Ensures reliable delivery
- Enables scalability

---

## Queue Components

![queue_components](svg/courses/architecting/architecture-patterns/11_queues/queue_components.svg)

---

## Types of Queues

1. Point-to-Point
1. Publish/Subscribe
1. Priority Queues
1. Dead Letter Queues
1. Delay Queues

---

## Point-to-Point vs Pub/Sub

![point_to_point_vs_pub_sub](svg/courses/architecting/architecture-patterns/11_queues/point_to_point_vs_pub_sub.svg)

---

## Basic Queue Operations

```python
from queue import Queue

# Create queue
queue = Queue()

# Producer
def produce():
    for i in range(10):
        queue.put(f"Message {i}")

# Consumer
def consume():
    while True:
        message = queue.get()
        process_message(message)
        queue.task_done()
```

---

## A Representative Queue (RabbitMQ)

```python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='task_queue', durable=True)

channel.basic_publish(
    exchange='', routing_key='task_queue', body='Hello World!',
    properties=pika.BasicProperties(delivery_mode=2),
)

def callback(ch, method, properties, body):
    print(f" [x] Received {body}")
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(queue='task_queue', on_message_callback=callback)
channel.start_consuming()
```

The shapes (producer, queue, consumer, ack) are common across systems; the trade-offs differ. See ch 12 for system-by-system comparison.

---

## Message Ordering

1. FIFO (First-In-First-Out)
1. Priority-based
1. Time-based
1. Custom ordering

---

## FIFO Implementation

```python
from collections import deque
import threading

class FIFOQueue:
    def __init__(self):
        self.queue = deque()
        self.lock = threading.Lock()

    def enqueue(self, item):
        with self.lock:
            self.queue.append(item)

    def dequeue(self):
        with self.lock:
            return self.queue.popleft() if self.queue else None
```

---

## Priority Queue Example

```python
import heapq

class PriorityQueue:
    def __init__(self):
        self._queue = []
        self._index = 0

    def push(self, item, priority):
        heapq.heappush(self._queue, (-priority, self._index, item))
        self._index += 1

    def pop(self):
        return heapq.heappop(self._queue)[-1]
```

---

## Message Batching

```python
class BatchProducer:
    def __init__(self, batch_size=100):
        self.batch = []
        self.batch_size = batch_size

    def add_message(self, message):
        self.batch.append(message)
        if len(self.batch) >= self.batch_size:
            self.flush()

    def flush(self):
        if self.batch:
            send_batch_to_queue(self.batch)
            self.batch = []
```

---

## Dead Letter Queues

![dead_letter_queues](svg/courses/architecting/architecture-patterns/11_queues/dead_letter_queues.svg)

---

## DLQ Implementation

```python
def process_message(message):
    try:
        # Process message
        process(message)
        # Acknowledge success
        message.ack()
    except Exception as e:
        # Move to DLQ
        move_to_dlq(message, str(e))

def move_to_dlq(message, error):
    dlq_message = {
        'original_message': message.body,
        'error': error,
        'timestamp': datetime.now().isoformat(),
        'retry_count': message.retry_count + 1
    }
    dlq.send_message(dlq_message)
```

---

## Queue Monitoring

Key Metrics:
- Queue Length
- Processing Time
- Error Rate
- Throughput
- Consumer Lag

---

## Monitoring Dashboard

![monitoring_dashboard](svg/courses/architecting/architecture-patterns/11_queues/monitoring_dashboard.svg)

---

## Error Handling Patterns

1. Retry with Backoff
1. Circuit Breaker
1. Fallback Handler
1. Poison Message Handler

---

## Retry Pattern

```python
def retry_with_backoff(func, max_retries=3):
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            wait_time = (2 ** attempt) * 1000  # exponential backoff
            time.sleep(wait_time / 1000.0)
```

---

## Scaling Patterns

1. Horizontal Consumer Scaling
1. Partition Distribution
1. Consumer Groups
1. Load Balancing

---

## Consumer Group Pattern

![consumer_group_pattern](svg/courses/architecting/architecture-patterns/11_queues/consumer_group_pattern.svg)

---

## Performance Optimization

1. Message Compression
1. Batch Processing
1. Prefetch Count
1. Connection Pooling
1. Resource Management

---

## Best Practices

1. Use Dead Letter Queues
1. Implement Retry Logic
1. Monitor Queue Health
1. Handle Poison Messages
1. Plan for Scaling
1. Ensure Message Persistence
