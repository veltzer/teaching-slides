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
![architecture_overview](/svg/courses/big_data/apache-spark-with-python/03_streaming/architecture_overview.svg)

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

![window_operations](/svg/courses/big_data/apache-spark-with-python/03_streaming/window_operations.svg)

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
