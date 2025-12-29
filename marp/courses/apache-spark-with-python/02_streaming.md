# Spark Streaming
## Introduction to Spark Streaming

---
## What is Spark Streaming
- Extension of core Spark API for stream processing
- Enables scalable, high-throughput, fault-tolerant processing
- Supports both real-time and batch processing
- Integrated with the rest of Spark ecosystem

---
## Architecture Overview
<svg viewBox="0 0 900 400" xmlns="http://www.w3.org/2000/svg">
  <!-- Data Sources -->
  <rect x="30" y="170" width="120" height="60" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="90" y="205" text-anchor="middle" font-family="Arial, sans-serif" font-size="14" font-weight="bold">Data Sources</text>

  <!-- Receivers -->
  <rect x="200" y="170" width="100" height="60" rx="5" fill="#d4edda" stroke="#28a745" stroke-width="2"/>
  <text x="250" y="205" text-anchor="middle" font-family="Arial, sans-serif" font-size="14" font-weight="bold">Receivers</text>

  <!-- DStreams -->
  <rect x="350" y="170" width="100" height="60" rx="5" fill="#fff3cd" stroke="#ffc107" stroke-width="2"/>
  <text x="400" y="205" text-anchor="middle" font-family="Arial, sans-serif" font-size="14" font-weight="bold">DStreams</text>

  <!-- RDDs -->
  <rect x="500" y="80" width="80" height="50" rx="5" fill="#cce5ff" stroke="#007bff" stroke-width="2"/>
  <text x="540" y="110" text-anchor="middle" font-family="Arial, sans-serif" font-size="13">RDD 1</text>

  <rect x="500" y="170" width="80" height="50" rx="5" fill="#cce5ff" stroke="#007bff" stroke-width="2"/>
  <text x="540" y="200" text-anchor="middle" font-family="Arial, sans-serif" font-size="13">RDD 2</text>

  <rect x="500" y="260" width="80" height="50" rx="5" fill="#cce5ff" stroke="#007bff" stroke-width="2"/>
  <text x="540" y="290" text-anchor="middle" font-family="Arial, sans-serif" font-size="13">RDD 3</text>

  <!-- Processing -->
  <rect x="640" y="170" width="100" height="60" rx="5" fill="#f8d7da" stroke="#dc3545" stroke-width="2"/>
  <text x="690" y="205" text-anchor="middle" font-family="Arial, sans-serif" font-size="14" font-weight="bold">Processing</text>

  <!-- Output -->
  <rect x="790" y="170" width="80" height="60" rx="5" fill="#e2d5f1" stroke="#6f42c1" stroke-width="2"/>
  <text x="830" y="205" text-anchor="middle" font-family="Arial, sans-serif" font-size="14" font-weight="bold">Output</text>

  <!-- Arrows -->
  <defs>
    <marker id="arrow5" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>

  <!-- Data Sources to Receivers -->
  <line x1="150" y1="200" x2="200" y2="200" stroke="#666" stroke-width="2" marker-end="url(#arrow5)"/>

  <!-- Receivers to DStreams -->
  <line x1="300" y1="200" x2="350" y2="200" stroke="#666" stroke-width="2" marker-end="url(#arrow5)"/>

  <!-- DStreams to RDDs -->
  <line x1="450" y1="180" x2="500" y2="105" stroke="#666" stroke-width="2" marker-end="url(#arrow5)"/>
  <line x1="450" y1="200" x2="500" y2="195" stroke="#666" stroke-width="2" marker-end="url(#arrow5)"/>
  <line x1="450" y1="220" x2="500" y2="285" stroke="#666" stroke-width="2" marker-end="url(#arrow5)"/>

  <!-- RDDs to Processing -->
  <line x1="580" y1="105" x2="640" y2="180" stroke="#666" stroke-width="2" marker-end="url(#arrow5)"/>
  <line x1="580" y1="195" x2="640" y2="200" stroke="#666" stroke-width="2" marker-end="url(#arrow5)"/>
  <line x1="580" y1="285" x2="640" y2="220" stroke="#666" stroke-width="2" marker-end="url(#arrow5)"/>

  <!-- Processing to Output -->
  <line x1="740" y1="200" x2="790" y2="200" stroke="#666" stroke-width="2" marker-end="url(#arrow5)"/>
</svg>

---
## Supported Input Sources
- Kafka
- Flume
- Kinesis
- TCP sockets
- HDFS/S3
- Custom sources

---
## Key Features
1. Fault Tolerance
    - Exactly-once semantics
    - Automatic recovery
    - Checkpointing
1. Integration
    - Seamless integration with Spark SQL
    - MLlib for streaming ML
    - GraphX for graph processing
---
## DStream (Discretized Stream)

## DStream Basics
- Continuous sequence of RDDs
- Each RDD contains data from a specific interval
- Supports all RDD operations
- Automatic batching of data

---
## Creating DStreams

```python
# Create StreamingContext
from pyspark.streaming import StreamingContext
ssc = StreamingContext(sc, batchDuration=1)

# Socket stream
lines = ssc.socketTextStream("localhost", 9999)

# File stream
file_stream = ssc.textFileStream("/path/to/directory")

# Kafka stream
from pyspark.streaming.kafka import KafkaUtils
kafka_stream = KafkaUtils.createDirectStream(ssc,
    topics=["topic1"],
    kafkaParams={"metadata.broker.list": "localhost:9092"})
```

---
## DStream Operations

## Transformations

```python
# Basic transformations
words = lines.flatMap(lambda line: line.split())
pairs = words.map(lambda word: (word, 1))
word_counts = pairs.reduceByKey(lambda x, y: x + y)

# Window operations
windowed = word_counts.window(
    windowDuration=30,
    slideDuration=10
)

# Join operations
stream1 = ...
stream2 = ...
joined = stream1.join(stream2)
```

---
## Output Operations

```python
# Print first 10 elements
word_counts.pprint()

# Save as text files
word_counts.saveAsTextFiles("prefix", "suffix")

# Save to database
word_counts.foreachRDD(lambda rdd: rdd.foreachPartition(save_to_db))
```

---
## Window Operations

<svg viewBox="0 0 900 500" xmlns="http://www.w3.org/2000/svg">
  <!-- Window 1 -->
  <g>
    <rect x="50" y="50" width="250" height="120" rx="5" fill="#f0f8ff" stroke="#4a90e2" stroke-width="2" stroke-dasharray="5,5"/>
    <text x="175" y="35" text-anchor="middle" font-family="Arial, sans-serif" font-size="14" font-weight="bold">Window 1</text>
    <rect x="70" y="90" width="60" height="40" rx="3" fill="#cce5ff" stroke="#007bff" stroke-width="2"/>
    <text x="100" y="113" text-anchor="middle" font-family="Arial, sans-serif" font-size="12">RDD 1</text>
    <rect x="145" y="90" width="60" height="40" rx="3" fill="#cce5ff" stroke="#007bff" stroke-width="2"/>
    <text x="175" y="113" text-anchor="middle" font-family="Arial, sans-serif" font-size="12">RDD 2</text>
    <rect x="220" y="90" width="60" height="40" rx="3" fill="#cce5ff" stroke="#007bff" stroke-width="2"/>
    <text x="250" y="113" text-anchor="middle" font-family="Arial, sans-serif" font-size="12">RDD 3</text>
    <!-- Arrows within Window 1 -->
    <line x1="130" y1="110" x2="145" y2="110" stroke="#666" stroke-width="2" marker-end="url(#arrow6)"/>
    <line x1="205" y1="110" x2="220" y2="110" stroke="#666" stroke-width="2" marker-end="url(#arrow6)"/>
  </g>

  <!-- Window 2 -->
  <g>
    <rect x="325" y="200" width="250" height="120" rx="5" fill="#f0fff0" stroke="#28a745" stroke-width="2" stroke-dasharray="5,5"/>
    <text x="450" y="185" text-anchor="middle" font-family="Arial, sans-serif" font-size="14" font-weight="bold">Window 2</text>
    <rect x="345" y="240" width="60" height="40" rx="3" fill="#d4edda" stroke="#28a745" stroke-width="2"/>
    <text x="375" y="263" text-anchor="middle" font-family="Arial, sans-serif" font-size="12">RDD 2</text>
    <rect x="420" y="240" width="60" height="40" rx="3" fill="#d4edda" stroke="#28a745" stroke-width="2"/>
    <text x="450" y="263" text-anchor="middle" font-family="Arial, sans-serif" font-size="12">RDD 4</text>
    <rect x="495" y="240" width="60" height="40" rx="3" fill="#d4edda" stroke="#28a745" stroke-width="2"/>
    <text x="525" y="263" text-anchor="middle" font-family="Arial, sans-serif" font-size="12">RDD 5</text>
    <!-- Arrows within Window 2 -->
    <line x1="405" y1="260" x2="420" y2="260" stroke="#666" stroke-width="2" marker-end="url(#arrow6)"/>
    <line x1="480" y1="260" x2="495" y2="260" stroke="#666" stroke-width="2" marker-end="url(#arrow6)"/>
  </g>

  <!-- Window 3 -->
  <g>
    <rect x="600" y="350" width="250" height="120" rx="5" fill="#fff9e6" stroke="#ffc107" stroke-width="2" stroke-dasharray="5,5"/>
    <text x="725" y="335" text-anchor="middle" font-family="Arial, sans-serif" font-size="14" font-weight="bold">Window 3</text>
    <rect x="620" y="390" width="60" height="40" rx="3" fill="#fff3cd" stroke="#ffc107" stroke-width="2"></rect>
    <text x="650" y="413" text-anchor="middle" font-family="Arial, sans-serif" font-size="12">RDD 4</text>
    <rect x="695" y="390" width="60" height="40" rx="3" fill="#fff3cd" stroke="#ffc107" stroke-width="2"/>
    <text x="725" y="413" text-anchor="middle" font-family="Arial, sans-serif" font-size="12">RDD 6</text>
    <rect x="770" y="390" width="60" height="40" rx="3" fill="#fff3cd" stroke="#ffc107" stroke-width="2"/>
    <text x="800" y="413" text-anchor="middle" font-family="Arial, sans-serif" font-size="12">RDD 7</text>
    <!-- Arrows within Window 3 -->
    <line x1="680" y1="410" x2="695" y2="410" stroke="#666" stroke-width="2" marker-end="url(#arrow6)"/>
    <line x1="755" y1="410" x2="770" y2="410" stroke="#666" stroke-width="2" marker-end="url(#arrow6)"/>
  </g>
  <!-- Connection arrows between windows -->
  <line x1="175" y1="170" x2="375" y2="240" stroke="#999" stroke-width="2" stroke-dasharray="3,3" marker-end="url(#arrow6)"/>
  <line x1="450" y1="320" x2="650" y2="390" stroke="#999" stroke-width="2" stroke-dasharray="3,3" marker-end="url(#arrow6)"/>
  <!-- Arrow marker definition -->
  <defs>
    <marker id="arrow6" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>
</svg>

---
## Stateful Operations

## UpdateStateByKey

```python
def update_function(new_values, running_count):
    if running_count is None:
        running_count = 0
    return sum(new_values, running_count)

# Track running counts
running_counts = pairs.updateStateByKey(update_function)
```

## MapWithState

```python
# More efficient state tracking
state_spec = StateSpec.function(state_update_fn)
state_stream = stream.mapWithState(state_spec)
```

---
## Use Cases

## Real-time Analytics Dashboard

```python
def process_metrics(time, rdd):
    if not rdd.isEmpty():
        # Calculate metrics
        metrics = rdd.map(parse_metric).reduceByKey(sum)

        # Update dashboard
        metrics.foreachPartition(update_dashboard)

# Process metrics every 5 seconds
metrics_stream = input_stream.window(5)
metrics_stream.foreachRDD(process_metrics)
```

---
## Fraud Detection System

```python
def detect_fraud(transaction):
    # Apply fraud detection rules
    return fraud_score > threshold

# Process transactions in real-time
transactions = kafka_stream.map(parse_transaction)
fraudulent = transactions.filter(detect_fraud)
fraudulent.foreachRDD(alert_security_team)
```

---
## Log Analysis

```python
# Parse and analyze logs in real-time
logs = file_stream.map(parse_log)

# Track errors
errors = logs.filter(lambda log: log.level == "ERROR")
error_counts = errors.countByWindow(60, 10)  # 1 min window, 10 sec slide

# Monitor response times
response_times = logs.map(lambda log: log.response_time)
avg_response = response_times.meanByWindow(60, 10)
```

---
## Performance Tuning

## Batch Size Optimization
- Smaller batches: lower latency but higher overhead
- Larger batches: higher throughput but increased latency
- Finding the right balance:

```python
# Adjust batch size based on processing time
ssc = StreamingContext(sc, batchDuration=optimize_batch_size())
```

---
## Memory Tuning

```python
# Configure memory fraction for streaming
conf = SparkConf().set("spark.streaming.memory.fraction", 0.8)

# Set cleanup policy
ssc.remember(duration)  # How long to remember old data
```

---
## Backpressure

```python
# Enable backpressure
conf = SparkConf().set("spark.streaming.backpressure.enabled", "true")
```

---
## Error Handling and Recovery

## Checkpointing

```python
# Set checkpoint directory
ssc.checkpoint("hdfs://checkpoint-dir")

# Reliable receiver
reliable_stream = ssc.receiverStream(reliable_receiver)
```

---
### Error Recovery

```python
def create_context():
    ssc = StreamingContext(...)
    stream = setup_stream()
    return ssc

# Recover from checkpoint
context = StreamingContext.getOrCreate(checkpoint_dir, create_context)
```

---
## Monitoring and Debugging

## Metrics Collection

```python
# Register metrics
from pyspark.streaming.listener import StreamingListener

class CustomListener(StreamingListener):
    def onBatchCompleted(self, batchCompleted):
        # Log batch metrics
        print(f"Batch processing time: {batchCompleted.processingDelay}")

ssc.addStreamingListener(CustomListener())
```

---
## Common Issues and Solutions
1. Data Loss
    - Enable Write Ahead Logs
    - Use reliable receivers
    - Implement retry logic
1. Slow Processing
    - Optimize batch size
    - Increase parallelism
    - Monitor backpressure
1. Memory Issues
    - Tune executor memory
    - Adjust cleaning interval
    - Monitor garbage collection

---
## Integration Patterns

## Kafka Integration

```python
# Direct Kafka approach
directKafkaStream = KafkaUtils.createDirectStream(ssc,
    ["topic"],
    {"metadata.broker.list": "broker1:9092,broker2:9092"})

# With exactly-once semantics
stream = directKafkaStream.transform(lambda rdd: process_with_exactly_once(rdd))
```

---
### Database Integration

```python
def save_partition(partition):
    # Set up database connection
    db = connect_to_db()
    for record in partition:
        db.save(record)
    db.close()

# Save stream to database
stream.foreachRDD(lambda rdd: rdd.foreachPartition(save_partition))
```

---
## Best Practices

### Production Deployment
1. Monitoring Setup
    - Implement custom metrics
    - Set up alerting
    - Monitor throughput and latency
1. Error Handling
    - Implement retry logic
    - Set up dead letter queues
    - Log error details

---

1. Testing

```python
# Unit testing streams
def test_streaming_word_count():
    test_input = [["hello world"], ["hello spark"]]
    expected_output = [("hello", 2), ("world", 1), ("spark", 1)]

    ssc = StreamingContext(sc, 1)
    stream = ssc.queueStream(test_input)
    result = stream.flatMap(lambda x: x.split()).countByValue()
```

---
## Summary
- Spark Streaming enables real-time processing
- DStreams provide high-level abstraction
- Rich ecosystem integration
- Robust fault tolerance and recovery
- Performance optimization options
