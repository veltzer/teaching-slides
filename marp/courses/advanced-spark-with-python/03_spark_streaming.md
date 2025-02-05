# Spark Streaming and Structured Streaming
---
## Streaming Fundamentals
* Real-time data processing
* Stream processing models
* Micro-batch processing
* Continuous processing
---
## Stream Processing Models
![0](../../../out/mermaid/marp/courses/advanced-spark-with-python/03_spark_streaming.md/0.png)

---
## Basic Concepts
1. Data sources
1. Processing time
1. Event time
1. Watermarks
---
## Streaming Sources
```python
# Kafka source example
stream = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "host:port") \
    .option("subscribe", "topic") \
    .load()
```
---
## Input Data Sources
![1](../../../out/mermaid/marp/courses/advanced-spark-with-python/03_spark_streaming.md/1.png)

---
## Stream Processing Modes
1. Micro-batch processing
1. Continuous processing
1. Trigger options
1. Processing guarantees
---
## Event Time Processing
```python
from pyspark.sql.functions import window

windowed = stream.groupBy(
    window("eventTime", "1 hour"),
    "id"
).count()
```
---
## Watermark Configuration
![2](../../../out/mermaid/marp/courses/advanced-spark-with-python/03_spark_streaming.md/2.png)

---
## Late Data Handling
```python
# Configure watermark
stream_df = stream_df \
    .withWatermark("eventTime", "10 minutes") \
    .groupBy("id") \
    .count()
```
---
## Stateful Processing
1. Window operations
1. Aggregations
1. State management
1. Checkpointing
---
## Window Operations
![3](../../../out/mermaid/marp/courses/advanced-spark-with-python/03_spark_streaming.md/3.png)

---
## Window Types
```python
# Sliding window
windowed = stream.groupBy(
    window("timestamp", "30 minutes", "5 minutes")
).count()
```
---
## State Management
```python
# Maintain running count
def update_state(key, value, state):
    if state.exists():
        state.update(state.get() + value)
    else:
        state.update(value)
```
---
## Checkpointing
![4](../../../out/mermaid/marp/courses/advanced-spark-with-python/03_spark_streaming.md/4.png)

---
## Fault Tolerance
1. Exactly-once processing
1. Checkpoint configuration
1. Recovery mechanisms
1. State recovery
---
## Output Modes
```python
# Complete output mode
query = stream.writeStream \
    .outputMode("complete") \
    .format("console") \
    .start()
```
---
## Output Sinks
![5](../../../out/mermaid/marp/courses/advanced-spark-with-python/03_spark_streaming.md/5.png)

---
## Streaming Joins
1. Stream-stream joins
1. Stream-static joins
1. Watermark considerations
1. State cleanup
---
## Stream-Stream Join
```python
# Join two streams
joined = stream1.join(
    stream2,
    "joinKey",
    "leftOuter"
)
```
---
## Performance Optimization
![6](../../../out/mermaid/marp/courses/advanced-spark-with-python/03_spark_streaming.md/6.png)

---
## Memory Management
1. State cleanup
1. Watermark tuning
1. Checkpoint cleanup
1. Resource allocation
---
## Trigger Options
```python
# Process every 5 minutes
query = stream.writeStream \
    .trigger(processingTime='5 minutes') \
    .start()
```
---
## Monitoring Streams
![7](../../../out/mermaid/marp/courses/advanced-spark-with-python/03_spark_streaming.md/7.png)

---
## Performance Metrics
1. Input rate
1. Processing rate
1. Batch duration
1. Operation metrics
---
## Error Handling
```python
def handle_errors(df, epoch_id):
    try:
        process_batch(df)
    except Exception as e:
        log_error(e)
```
---
## Data Quality
![8](../../../out/mermaid/marp/courses/advanced-spark-with-python/03_spark_streaming.md/8.png)

---
## Schema Evolution
```python
# Schema enforcement
stream = spark.readStream \
    .schema(schema) \
    .json("path")
```
---
## Custom Sources
```python
from pyspark.sql.streaming import Source

class CustomSource(Source):
    def getBatch(self, start, end):
        return get_data(start, end)
```
---
## Custom Sinks
![9](../../../out/mermaid/marp/courses/advanced-spark-with-python/03_spark_streaming.md/9.png)

---
## Rate Limiting
1. Input rate control
1. Processing rate control
1. Backpressure handling
1. Resource management
---
## Kafka Integration
```python
# Write to Kafka
query = stream.writeStream \
    .format("kafka") \
    .option("topic", "output") \
    .start()
```
---
## Security Setup
![10](../../../out/mermaid/marp/courses/advanced-spark-with-python/03_spark_streaming.md/10.png)

---
## Production Deployment
1. Monitoring setup
1. Alert configuration
1. Resource planning
1. Scaling strategy
---
## Recovery Mechanisms
```python
# Checkpoint configuration
stream.writeStream \
    .option("checkpointLocation", "path") \
    .start()
```
---
## Testing Strategies
![11](../../../out/mermaid/marp/courses/advanced-spark-with-python/03_spark_streaming.md/11.png)

---
## Debugging Tools
1. Progress monitoring
1. Query explanation
1. Metrics tracking
1. Log analysis
---
## Advanced Patterns
```python
# Streaming aggregation pattern
def process_stream(batch_df, batch_id):
    batch_df.cache()
    process_aggregations(batch_df)
```
---
## Stream Processing Patterns
![12](../../../out/mermaid/marp/courses/advanced-spark-with-python/03_spark_streaming.md/12.png)

---
## State Store
1. RocksDB backend
1. State versioning
1. Cleanup policies
1. Size management
---
## Metrics Collection
```python
# Custom metrics
def process_metrics(batch_df, epoch_id):
    metrics = compute_metrics(batch_df)
    log_metrics(metrics)
```
---
## Monitoring Dashboard
![13](../../../out/mermaid/marp/courses/advanced-spark-with-python/03_spark_streaming.md/13.png)

---
## Scaling Considerations
1. Partition management
1. Resource allocation
1. Cluster sizing
1. Load balancing
---
## Best Practices
```python
# Configure proper watermark
df = df.withWatermark("timestamp", "1 hour")
    .groupBy("key")
    .agg(...)
```
---
## Common Pitfalls
![14](../../../out/mermaid/marp/courses/advanced-spark-with-python/03_spark_streaming.md/14.png)

---
## Optimization Tips
1. Proper partitioning
1. Efficient watermarks
1. Memory management
1. Batch size tuning
---
## Advanced Features
```python
# Arbitrary stateful processing
def update_state(key, values, state):
    updated = process_values(values, state)
    return updated
```
---
## Future Development
![15](../../../out/mermaid/marp/courses/advanced-spark-with-python/03_spark_streaming.md/15.png)

---
## Integration Patterns
1. Lambda architecture
1. Kappa architecture
1. Hybrid solutions
1. Custom patterns
---
## Production Checklist
```python
# Essential configurations
spark.conf.set("spark.streaming.stopGracefullyOnShutdown", "true")
spark.conf.set("spark.sql.streaming.checkpointLocation", "path")
```
---
## Documentation
![16](../../../out/mermaid/marp/courses/advanced-spark-with-python/03_spark_streaming.md/16.png)

---
## Additional Resources
* Official documentation
* Community guides
* Best practices
* Performance tips
