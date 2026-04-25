---
tags:
  - concepts:architecture
  - concepts:messaging
  - infrastructure:kafka
level: intermediate
category: architecture
audience:
  - audiences:developers
  - audiences:architects

---
# Message Queue Systems
## Kafka vs Traditional Queue Systems

---
## What This Chapter Compares

- Three messaging systems: Kafka, SQS, RabbitMQ
- Storage models, ordering, delivery guarantees, scaling, error handling, cost
- Ch 11 covers queue concepts generally; this chapter is the side-by-side comparison
- Kafka gets the deepest treatment because its model (durable log) differs most from classic queues

---
## Traditional Messaging vs Streaming

- Traditional queues: messages are consumed, acknowledged, then deleted
- Streaming logs (Kafka): messages persist; consumers track their own offset
- The same broker can be either depending on retention and consumption pattern
- Choosing one is choosing how messages relate to time

---
## Traditional vs Streaming Diagram

![traditional_kafka_vs_streaming](svg/courses/architecting/architecture-patterns/12_kafka/traditional_kafka_vs_streaming.svg)

---
## Traditional Message Processing

- Messages are **consumed and committed**
- Processing is done **after** retrieval
- Suited for **event messaging**
- Focus on **durability** and **reliability**

---
## Kafka Streams

![kafka_streams](svg/courses/architecting/architecture-patterns/12_kafka/kafka_streams.svg)

---
## Kafka Streams Features

- **Real-time** processing
- **Stateful** operations
- Built-in **windowing**
- **Exactly-once** semantics
- **Fault-tolerant** processing

---
## Message Queue Comparison

| Feature | Kafka | SQS | RabbitMQ | ActiveMQ |
|---------|-------|-----|----------|----------|
| Throughput | Very High | Medium | High | Medium |
| Latency | ~10ms | ~100ms | ~1ms | ~1ms |
| Max Message Size | 1MB default | 256KB | No limit | No limit |
| Ordering | Per partition | FIFO queues | Per queue | Per queue |
| Retention | Configurable | 14 days max | Until consumed | Until consumed |

---
## SQS Deep Dive

![sqs_deep_dive](svg/courses/architecting/architecture-patterns/12_kafka/sqs_deep_dive.svg)

---
## SQS Key Features

- **Standard** vs **FIFO** queues
- Message retention up to 14 days
- Built-in **Dead Letter Queues**
- **Visibility timeout** mechanism
- **Long polling** support

---

## Kafka vs SQS: Use Cases

### Kafka Ideal For
- High-throughput event streaming
- Real-time analytics
- Event sourcing
- Log aggregation
- Long-term event storage

### SQS Ideal For
- Decoupling microservices
- Task queues
- Serverless architectures
- Auto-scaling triggers
- Temporary message storage

---
## RabbitMQ Architecture

![rabbitmq_architecture](svg/courses/architecting/architecture-patterns/12_kafka/rabbitmq_architecture.svg)

---
## RabbitMQ Key Features

- **Exchange types**: Direct, Fanout, Topic, Headers
- **Advanced routing** capabilities
- **Publisher confirms**
- **Consumer acknowledgments**
- **Queue mirroring**

---

## Storage Models Compared

![storage_models_compared](svg/courses/architecting/architecture-patterns/12_kafka/storage_models_compared.svg)

---

## Performance Characteristics

### Kafka Performance
- Sequential disk I/O
- Zero-copy data transfer
- Batch processing
- Partition-based parallelism

### SQS Performance
- Distributed queues
- Auto-scaling
- Limited batching
- At-least-once delivery

### RabbitMQ Performance
- In-memory with disk backup
- Smart routing
- Publisher confirms
- Complex topologies

---
## Kafka Deep Dive: Topics & Partitions

![kafka_deep_dive_topics_partitions](svg/courses/architecting/architecture-patterns/12_kafka/kafka_deep_dive_topics_partitions.svg)

---
## Kafka Partition Details

- Each partition is an **ordered log**
- Segments are **physical files**
- **Retention** by time or size
- **Compaction** for key-based retention

---
## Advanced Kafka: Consumer Groups

![advanced_kafka_consumer_groups](svg/courses/architecting/architecture-patterns/12_kafka/advanced_kafka_consumer_groups.svg)

---
## Consumer Group Features

- **Automatic partition assignment**
- **Rebalancing** on consumer changes
- **Offset management**
- **Group coordination**

---

## Message Delivery Guarantees

| System | At Most Once | At Least Once | Exactly Once |
|--------|--------------|---------------|--------------|
| Kafka | Yes | Yes | Yes (with transactions) |
| SQS | No | Yes | No |
| RabbitMQ | Yes | Yes | Yes (with plugins) |
| ActiveMQ | Yes | Yes | Yes (with XA) |

---
## Kafka Scaling Patterns

![kafka](svg/courses/architecting/architecture-patterns/12_kafka/kafka.svg)

---
## Kafka Scaling Details

- **Horizontal scaling** via partitions
- **Replication** for fault tolerance
- **Leader/follower** model
- **Consumer group** scaling

---
## SQS Scaling Patterns

![sqs_scaling_patterns](svg/courses/architecting/architecture-patterns/12_kafka/sqs_scaling_patterns.svg)

---
## SQS Scaling Approaches

- **Queue-per-microservice**
- **Auto-scaling** based on queue depth
- **Regional** failover
- **Visibility timeout** management

---

## Performance Optimization: Producers

- Use appropriate **batch.size** (16KB-1MB)
- Enable **compression** (lz4 recommended)
- Increase **linger.ms** (5-100ms)
- Use multiple **producer threads**
- Set **acks** based on durability needs

---
## Performance Optimization: Topics

- Choose proper **partition count**
    - ~(Desired Throughput) / (Single Partition Throughput)
    - Typically 1 partition per broker for start

---
## Topic Optimization Diagram

![performance_optimization_topics](svg/courses/architecting/architecture-patterns/12_kafka/performance_optimization_topics.svg)

---
## Advanced Kafka: Replication

![advanced_kafka_replication](svg/courses/architecting/architecture-patterns/12_kafka/advanced_kafka_replication.svg)

---
## Kafka Replication Details

- **Leader** handles all reads/writes
- **Followers** maintain replicas
- **ISR** (In-Sync Replicas) concept
- **min.insync.replicas** setting
- **Unclean leader election** options

---

## Error Handling Comparison

### Error Handling in Kafka
- Retry policies
- Dead letter topics
- Error topic patterns
- Transaction support

### Error Handling in SQS
- Visibility timeout
- Dead letter queues
- Redrive policies
- Maximum receives

### Error Handling in RabbitMQ
- Negative acknowledgments
- Dead letter exchanges
- Poison message handling
- TTL policies

---

## Cost Considerations

| Aspect | Kafka | SQS | RabbitMQ |
|--------|-------|-----|----------|
| Infrastructure | High | Low | Medium |
| Maintenance | High | Low | Medium |
| Message Cost | Very Low | Per Message | N/A |
| Storage | Configurable | 14 Days Max | Memory/Disk |
| Scale Cost | Linear | Pay per use | Step-wise |

---

## Monitoring Essentials

Key Metrics to Watch
- Producer batch size
- Request latency
- Broker CPU & memory
- Consumer lag
- Records per second
- Garbage collection

---

## When to Choose What

### Choose Kafka When
- Need high throughput
- Long-term storage required
- Stream processing needed
- Complex event patterns
- Large scale deployments

### Choose SQS When
- Serverless architecture
- Simple queue patterns
- AWS integration needed
- Variable load patterns
- Minimal maintenance desired

### Choose RabbitMQ When
- Complex routing needed
- Low latency required
- Traditional messaging patterns
- Small to medium scale
- Need protocol variety

---
## Integration Patterns

![integration_patterns](svg/courses/architecting/architecture-patterns/12_kafka/integration_patterns.svg)

---
## Integration Approaches

- **Hybrid** approaches
- **Bridge** patterns
- **Multi-protocol** support
- **Cross-region** replication

---

## Future Considerations

### Future of Kafka
- KRaft (replacement for ZooKeeper)
- Tiered storage
- Improved exactly-once semantics

### Future of Queue Systems
- Serverless integration
- Enhanced security features
- Cross-region improvements
- Cost optimizations

---

## Resources

Resources
- kafka.apache.org
- aws.amazon.com/sqs
- rabbitmq.com
