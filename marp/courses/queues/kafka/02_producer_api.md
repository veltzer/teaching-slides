---
tags:
  - tools:kafka
  - data-and-ai:streaming
level: beginner
category: message-queue
audience:
  - audiences:developers

---
# Producer API

---
## What This Chapter Covers

- The Producer in Kafka
- Producing records in Java
- Keys, values, and partitioning
- Acknowledgements and reliability
- Batching and compression
- Common producer patterns and pitfalls

---
## What a Producer Does

- Constructs records (key + value + metadata)
- Sends them to brokers
- Handles serialisation
- Buffers and batches for throughput
- Tracks acknowledgements
- That's the whole job; everything else is configuration

---
## A Minimal Java Producer

```java
Properties p = new Properties();
p.put("bootstrap.servers", "broker1:9092,broker2:9092");
p.put("key.serializer", StringSerializer.class.getName());
p.put("value.serializer", StringSerializer.class.getName());

KafkaProducer<String, String> producer = new KafkaProducer<>(p);
producer.send(new ProducerRecord<>("orders", "key1", "value1"));
producer.close();
```

- Five lines of setup, one line to send
- The hard part is configuration

---
## Records Have a Key

- The key is optional but powerful
- Same key &#8594; same partition (consistent hashing)
- Use for: grouping related events together
- Example: `customer_id` as key keeps a customer's events in order
- No key &#8594; round-robin across partitions

---
## Why Keys Matter

- Within a partition, records are ordered
- Across partitions, no order guarantee
- "Customer X's events in order" requires keying by customer
- Otherwise: a slow consumer of one partition could see X's events out of order
- Pick the key carefully

---
## Serialisation

- Records are bytes on the wire
- Producer needs a Serializer for key and value
- Common choices: String, Avro, Protobuf, JSON
- Schema Registry centralises Avro/Protobuf schemas
- Don't ship JSON in production at scale (Avro/Protobuf much smaller)

---
## Acknowledgements (acks)

- `acks=0`: fire and forget; fastest, can lose data
- `acks=1`: leader confirms; medium safety
- `acks=all`: leader + all in-sync replicas confirm; safest
- For most production use: `acks=all`
- Trade-off: latency vs durability

---
## Idempotent Producer

- `enable.idempotence=true`
- Producer sends sequence numbers; broker dedupes
- Prevents duplicates from retries
- Costs nothing meaningful; turn it on
- Required for transactional producer

---
## Transactional Producer

- Atomic writes across multiple topics/partitions
- "Process this record AND write these outputs OR neither"
- Used in Kafka Streams for exactly-once processing
- More complex setup; not needed for most cases
- Performance overhead modest

---
## Batching

- Producer accumulates records in memory; sends in batches
- `linger.ms`: max wait before sending a partial batch
- `batch.size`: max bytes per batch
- Bigger batches = better throughput, worse latency
- Default: 0ms linger, 16KB batches; tune for your workload

---
## Compression

- `compression.type`: none, gzip, snappy, lz4, zstd
- Compresses entire batch (more efficient than per-record)
- Reduces network and storage
- CPU cost; usually worth it for text-like payloads
- `lz4` and `zstd` are good defaults

---
## Async Sending

```java
producer.send(record, (metadata, exception) -> {
    if (exception != null) handleError(exception);
    else log.info("sent to partition {} offset {}", metadata.partition(), metadata.offset());
});
```

- Send returns a Future; callback fires on completion
- Don't block on the Future in hot path — defeats batching
- Handle errors in the callback or via global error handler

---
## Sync Sending

```java
RecordMetadata md = producer.send(record).get();
```

- Blocks until ack
- Use for: critical writes where you must know the result
- Costs throughput
- Avoid in tight loops

---
## Partitioning Strategies

- **Default**: hash(key) mod numPartitions, or round-robin if no key
- **Custom**: implement Partitioner interface
- Custom for: weighted distribution, geographic affinity, anti-skew
- Default is correct for most cases
- Watch for partition skew (one partition takes most traffic)

---
## Common Producer Pitfalls

- `acks=0` in production — silent data loss
- Forgetting to close the producer — buffered data lost on crash
- Synchronous send in a tight loop — terrible throughput
- Custom Serializers that allocate per record — GC pressure
- Logging every successful send — drowns the logs

---
## Producer Tuning Knobs

- `acks`, `linger.ms`, `batch.size`, `compression.type`
- `buffer.memory`: total RAM for buffering
- `max.in.flight.requests.per.connection`: parallelism per broker
- `request.timeout.ms`: how long before a request is given up on
- Tune based on your throughput / latency / durability trade-off

---
## Common Mistakes

- No key on data that needs ordering
- `acks=0` "for performance"
- Each record sent synchronously
- Not closing the producer cleanly
- Over-tuning before measuring
