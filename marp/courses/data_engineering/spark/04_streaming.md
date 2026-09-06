---
tags:
  - data-and-ai:big-data
level: intermediate
category: data-engineering
audience:
  - audiences:data-engineers

---

# Streaming

---

## What This Chapter Covers

- Structured Streaming basics
- Sources and sinks
- Watermarks
- State
- Reliability

---

## Structured Streaming

- DataFrame API for streams
- Same operators as batch
- Continuous incremental execution
- Strong fault tolerance

---

## Trigger Modes

- Default micro-batch
- Continuous (limited)
- Available-now for one-shot
- Pick by latency target

---

## Sources

- Kafka and friends
- Files arriving in directory
- Socket for testing
- Delta tables as a source

---

## Sinks

- Console for testing
- Files
- Tables (Delta)
- foreachBatch for custom

---

## Output Modes

- Append: only new rows
- Update: changed rows
- Complete: full result each time
- Pick by query type

---

## Streaming Modes

![streaming_modes](svg/courses/data_engineering/spark/04_streaming/streaming_modes.svg)

---

## Stateful Operations

- Aggregations need state
- Joins of two streams need state
- State stored on disk
- Tune state retention

---

## Watermarks

- Allow late data window
- Drop older than watermark
- Required for stateful queries
- Tune to source lateness

---

## Watermark Visualized

![watermark](svg/courses/data_engineering/spark/04_streaming/watermark.svg)

---

## Joins

- Stream to static
- Stream to stream
- Constraints on watermarks
- Test with bursty data

---

## Checkpointing

- Required for fault tolerance
- Stores offsets and state
- Path on durable storage
- Not interchangeable across queries

---

## Exactly-Once Sinks

- Some sinks support
- Combine with checkpoint
- Idempotent producers required
- Verify per sink

---

## Backpressure

- Slow downstream
- Source pulls slower
- Configure rate limits
- Monitor lag

---

## Monitoring

- Input rows per second
- Processed rows per second
- Lag
- State size

---

## Common Streaming Mistakes

- No watermark on stateful query
- Checkpoint on local disk
- Mixing checkpoints across queries
- Stateful query without state cleanup
- No lag alert
