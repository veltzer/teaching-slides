---
tags:
  - tools:kafka
  - data-and-ai:streaming
level: beginner
category: message-queue
audience:
  - audiences:developers

---
# Consumer API

---
## Consumer Groups

![consumer_groups](svg/courses/queues/kafka/03_consumer_api/consumer_groups.svg)

---
## What This Chapter Covers

- The high-level Consumer
- Consumer groups and partition assignment
- Offsets and commits
- The simple/low-level consumer (briefly)
- Rebalances
- Common consumer patterns

---
## High-Level Consumer

```java
Properties p = new Properties();
p.put("bootstrap.servers", "broker1:9092");
p.put("group.id", "order-processors");
p.put("key.deserializer", StringDeserializer.class.getName());
p.put("value.deserializer", StringDeserializer.class.getName());

KafkaConsumer<String, String> consumer = new KafkaConsumer<>(p);
consumer.subscribe(List.of("orders"));

while (true) {
    ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(100));
    for (ConsumerRecord<String, String> r : records) {
        process(r);
    }
}
```

- `subscribe` joins a consumer group
- `poll` gets a batch of records

---
## Consumer Groups

- A `group.id` defines a logical consumer
- Multiple processes with the same group.id share work
- Each partition assigned to *one* consumer in the group
- More consumers = more parallelism (up to partition count)
- Different group.id = independent reading of the same data

---
## Partition Assignment

- Kafka coordinator assigns partitions to consumers
- Default strategy: range or round-robin
- `partition.assignment.strategy`: configurable
- Re-assigned on consumer add/remove (rebalance)
- Sticky assignment minimises movement on rebalance

---
## Offsets

- Each consumer tracks where it is in each partition
- Committed offsets stored in a special Kafka topic (`__consumer_offsets`)
- On restart: resume from last committed offset
- Manual or auto commit
- Misunderstanding offsets is the #1 source of consumer bugs

---
## Auto-Commit

- `enable.auto.commit=true` (default)
- `auto.commit.interval.ms` (default 5s)
- Convenient but: can re-process or skip records on crash
- For at-least-once: usually fine
- For exactly-once: must commit manually after processing

---
## Manual Commit

```java
while (true) {
    ConsumerRecords<...> records = consumer.poll(Duration.ofMillis(100));
    for (var r : records) process(r);
    consumer.commitSync();
}
```

- Commit *after* processing
- Crash before commit = re-process on restart (at-least-once)
- Commit before processing = potential skip on crash (don't do this)

---
## Async vs Sync Commit

- `commitAsync`: faster, doesn't block; failures less obvious
- `commitSync`: slower, blocks until ack; failures explicit
- Common: async between batches, sync at shutdown
- Failure handling for async: callback parameter

---
## Rebalances

- When consumers join or leave the group
- All consumers stop processing briefly
- Partitions reassigned
- Then everyone resumes
- Frequent rebalances kill throughput

---
## Causes of Frequent Rebalances

- Consumers timing out (`session.timeout.ms`)
- Consumers crashing
- Consumers taking too long between polls (`max.poll.interval.ms`)
- Cluster-side: brokers restarting
- Tune timeouts to avoid spurious rebalances

---
## Cooperative Rebalance

- Newer protocol; only the affected partitions move
- `partition.assignment.strategy=CooperativeStickyAssignor`
- Less downtime during rebalance
- Available since Kafka 2.4
- The default for new deployments

---
## Pause and Resume

- `consumer.pause(partitions)` stops fetching from those partitions
- Use when downstream is overloaded
- `consumer.resume(partitions)` to restart
- Cleaner than dropping records or filling memory
- A common back-pressure pattern

---
## Seek

- `consumer.seek(partition, offset)` jumps to a specific offset
- `seekToBeginning()`, `seekToEnd()`
- Use for: replay from a specific point, debugging, testing
- Combine with timestamp lookup (`offsetsForTimes`) to seek by time

---
## Simple/Low-Level Consumer

- Manual partition assignment (`assign` instead of `subscribe`)
- No group coordination
- Use for: read all partitions in one process, special use cases
- Less common than the high-level consumer
- Worth knowing exists

---
## Reading From the Beginning

- New consumer group with no committed offsets
- Default: starts at *latest* (skips existing data)
- `auto.offset.reset=earliest` to read history
- For consumers reading change data, usually want `earliest` initially
- After first run, consumer continues from last commit

---
## Long-Running Consumer Pattern

```java
try {
    while (running.get()) {
        var records = consumer.poll(Duration.ofMillis(100));
        process(records);
        consumer.commitAsync();
    }
} finally {
    consumer.commitSync();
    consumer.close();
}
```

- Loop, poll, process, commit
- Final sync commit and close on shutdown

---
## Common Consumer Pitfalls

- Long-running processing inside the poll loop &#8594; rebalance
- Auto-commit + slow processing &#8594; commit happens for unprocessed records
- Multiple consumers with same group.id but different subscriptions &#8594; chaos
- Forgetting to close &#8594; offsets not committed
- Not handling rebalances &#8594; double-processing

---
## Common Mistakes

- Treating Kafka like a queue with one consumer (use 1 partition)
- Adding consumers past the partition count (idle consumers)
- Polling rarely &#8594; rebalance kicks in
- Ignoring commit failures
- Auto-commit in exactly-once flows
