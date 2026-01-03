# Queues in Distributed Systems
## Modern Architecture Course

<!-- Add Mermaid.js support -->
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
<script>
  mermaid.initialize({ startOnLoad: true });
</script>

---

## Agenda

1. Understanding Queues
1. Queue Types and Patterns
1. Message Ordering and Delivery
1. Queue Systems Deep Dive
   - RabbitMQ
   - Apache Kafka
   - Amazon SQS
1. Advanced Concepts

---

## What are Queues

- Asynchronous communication mechanism
- Decouples producers and consumers
- Handles backpressure
- Ensures reliable delivery
- Enables scalability

---

## Queue Components

<div class="mermaid">
graph LR
    P[Producer] --> Q[Message Queue]
    Q --> C[Consumer]

    subgraph "Queue Details"
        Q --> H[Head/Front]
        Q --> T[Tail/Back]
        Q --> M[Messages]
    end

    subgraph "Features"
        Q --> PE[Persistence]
        Q --> RT[Retry Logic]
        Q --> DL[Dead Letter]
    end

    style P fill:#e3f2fd
    style Q fill:#f3e5f5
    style C fill:#e8f5e9
</div>

---

## Types of Queues

1. Point-to-Point
1. Publish/Subscribe
1. Priority Queues
1. Dead Letter Queues
1. Delay Queues

---

## Point-to-Point vs Pub/Sub

<div class="mermaid">
graph TB
    subgraph "Point-to-Point"
        P1[Producer] --> Q1[Queue]
        Q1 --> C1[Consumer 1]
    end

    subgraph "Publish/Subscribe"
        P2[Publisher] --> T[Topic]
        T --> S1[Subscriber 1]
        T --> S2[Subscriber 2]
        T --> S3[Subscriber 3]
    end

    style P1 fill:#e3f2fd
    style T fill:#f3e5f5
    style S1 fill:#e8f5e9
</div>

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

## RabbitMQ Architecture

<div class="mermaid">
graph LR
    P[Producer] --> E[Exchange]

    E --> |Routing Key| Q1[Queue 1]
    E --> |Routing Key| Q2[Queue 2]
    E --> |Routing Key| Q3[Queue 3]

    Q1 --> C1[Consumer 1]
    Q2 --> C2[Consumer 2]
    Q3 --> C3[Consumer 3]

    subgraph "Exchange Types"
        D[Direct]
        F[Fanout]
        T[Topic]
        H[Headers]
    end

    style P fill:#e3f2fd
    style E fill:#f3e5f5
    style Q1 fill:#e8f5e9
</div>

---

## RabbitMQ Example

```python
import pika

# Connection
connection = pika.BlockingConnection(
    pika.ConnectionParameters('localhost')
)
channel = connection.channel()

# Declare queue
channel.queue_declare(queue='task_queue', durable=True)

# Producer
channel.basic_publish(
    exchange='',
    routing_key='task_queue',
    body='Hello World!',
    properties=pika.BasicProperties(
        delivery_mode=2,  # make message persistent
    )
)

# Consumer
def callback(ch, method, properties, body):
    print(f" [x] Received {body}")
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(
    queue='task_queue',
    on_message_callback=callback
)
channel.start_consuming()
```

---

## Apache Kafka Architecture

<div class="mermaid">
graph TB
    subgraph "Kafka Cluster"
        B1[Broker 1]
        B2[Broker 2]
        B3[Broker 3]
    end

    subgraph "Topic"
        P0[Partition 0]
        P1[Partition 1]
        P2[Partition 2]
    end

    PR[Producers] --> B1
    PR --> B2
    PR --> B3

    B1 --> P0
    B2 --> P1
    B3 --> P2

    P0 --> CG[Consumer Group]
    P1 --> CG
    P2 --> CG

    style PR fill:#e3f2fd
    style B1 fill:#f3e5f5
    style CG fill:#e8f5e9
</div>

---

## Kafka Topics and Partitions

<div class="mermaid">
graph LR
    subgraph "Topic: Orders"
        subgraph "Partition 0"
            M1[Msg 0]
            M2[Msg 3]
            M3[Msg 6]
        end

        subgraph "Partition 1"
            M4[Msg 1]
            M5[Msg 4]
            M6[Msg 7]
        end

        subgraph "Partition 2"
            M7[Msg 2]
            M8[Msg 5]
            M9[Msg 8]
        end
    end

    P[Producer] -->|Key Hash| M1
    P -->|Key Hash| M4
    P -->|Key Hash| M7

    style M1 fill:#e3f2fd
    style M4 fill:#f3e5f5
    style M7 fill:#e8f5e9
</div>

---

## Kafka Producer Example

```python
from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Produce message
producer.send('my_topic', {
    'user_id': 123,
    'action': 'login',
    'timestamp': '2024-01-01T10:00:00Z'
})

# Flush and close
producer.flush()
producer.close()
```

---

## Kafka Consumer Example

```python
from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'my_topic',
    bootstrap_servers=['localhost:9092'],
    group_id='my_group',
    auto_offset_reset='earliest',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# Consume messages
for message in consumer:
    print(f"Partition: {message.partition}")
    print(f"Offset: {message.offset}")
    print(f"Value: {message.value}")
```

---

## Amazon SQS Architecture

<div class="mermaid">
graph TB
    subgraph "AWS Region"
        subgraph "SQS Service"
            Q1[Standard Queue]
            Q2[FIFO Queue]
        end

        P[Producer<br/>Lambda/EC2] --> Q1
        P --> Q2

        Q1 --> C1[Consumer 1]
        Q1 --> C2[Consumer 2]
        Q2 --> C3[Consumer 3]

        Q1 -.->|Failed Messages| DLQ1[Dead Letter Queue]
        Q2 -.->|Failed Messages| DLQ2[Dead Letter Queue]
    end

    CW[CloudWatch<br/>Monitoring] -.-> Q1
    CW -.-> Q2

    style P fill:#e3f2fd
    style Q1 fill:#f3e5f5
    style DLQ1 fill:#ffcdd2
</div>

---

## SQS Example

```python
import boto3

# Create SQS client
sqs = boto3.client('sqs')

# Send message
response = sqs.send_message(
    QueueUrl='https://sqs.region.amazonaws.com/123456789012/MyQueue',
    MessageBody='Hello from SQS!',
    MessageAttributes={
        'Author': {
            'StringValue': 'John Doe',
            'DataType': 'String'
        }
    }
)

# Receive messages
response = sqs.receive_message(
    QueueUrl='https://sqs.region.amazonaws.com/123456789012/MyQueue',
    MaxNumberOfMessages=10,
    WaitTimeSeconds=20
)
```

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

<div class="mermaid">
graph LR
    P[Producer] --> MQ[Main Queue]
    MQ --> C[Consumer]

    C -->|Success| P1[Process Complete]
    C -->|Failure 1| R1[Retry 1]
    R1 -->|Failure 2| R2[Retry 2]
    R2 -->|Failure 3| R3[Retry 3]
    R3 -->|Max Retries| DLQ[Dead Letter Queue]

    DLQ --> M[Manual Review]
    M --> RE[Reprocess]
    RE --> MQ

    style MQ fill:#e3f2fd
    style DLQ fill:#ffcdd2
    style M fill:#fff3e0
</div>

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

<div class="mermaid">
graph TB
    subgraph "Queue Metrics"
        M1[Queue Length]
        M2[Message Age]
        M3[Processing Time]
        M4[Error Rate]
        M5[Throughput]
    end

    subgraph "Alerts"
        A1[High Queue Length > 1000]
        A2[Old Messages > 5min]
        A3[High Error Rate > 5%]
    end

    M1 --> A1
    M2 --> A2
    M4 --> A3

    A1 --> N[Notification]
    A2 --> N
    A3 --> N

    N --> T[Team Alert]

    style M1 fill:#e3f2fd
    style A1 fill:#ffcdd2
    style N fill:#fff3e0
</div>

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

<div class="mermaid">
graph LR
    subgraph "Topic with 4 Partitions"
        P0[Partition 0]
        P1[Partition 1]
        P2[Partition 2]
        P3[Partition 3]
    end

    subgraph "Consumer Group 1"
        C1[Consumer 1]
        C2[Consumer 2]
    end

    subgraph "Consumer Group 2"
        C3[Consumer 3]
        C4[Consumer 4]
        C5[Consumer 5]
    end

    P0 --> C1
    P1 --> C1
    P2 --> C2
    P3 --> C2

    P0 --> C3
    P1 --> C4
    P2 --> C5
    P3 --> C3

    style P0 fill:#e3f2fd
    style C1 fill:#f3e5f5
    style C3 fill:#e8f5e9
</div>

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
