---
tags:
  - observability:tracing
level: intermediate
category: observability
audience:
  - audiences:devops
  - audiences:developers

---

# Sampling and Storage

---

## What This Chapter Covers

- Sampling strategies
- Tail-based sampling
- Storage backends
- Indexing
- Cost control

---

## Why Sample

- Full collection too expensive
- Storage and network cost
- Most traces look alike
- Keep the interesting ones

---

## Probabilistic Sampling

- Fixed percentage of traces
- Decision at root
- Simple and effective
- Misses rare bugs

---

## Sampling Strategies

![sampling_strategies](svg/courses/observability_and_monitoring/jaeger/04_sampling_and_storage/sampling_strategies.svg)

---

## Rate Limiting

- N traces per second per service
- Caps cost
- Distorts comparisons
- Combine with probabilistic

---

## Adaptive Sampling

- Higher rate for rare endpoints
- Lower for high-traffic
- Better signal per byte
- Configurable in modern collectors

---

## Tail-Based Sampling

- Buffer traces in collector
- Decide after seeing whole trace
- Keep errors and slow ones
- More expensive collector

---

## Head vs Tail

![tail_sampling](svg/courses/observability_and_monitoring/jaeger/04_sampling_and_storage/tail_sampling.svg)

---

## Force Sampling

- App-level decision to keep
- Useful for known important paths
- Override sampler defaults
- Use sparingly

---

## Storage Backends

- Cassandra: high write throughput
- Elasticsearch / OpenSearch: search
- Cloud-managed services
- Memory for testing only

---

## Indexing

- By service, operation, tag
- Required for fast search
- Indexes cost storage
- Tune to query patterns

---

## Retention

- Days for high-volume systems
- Weeks for compliance
- Cold tier for older data
- Drop after retention

---

## Compaction

- Merge small files
- Reduces metadata cost
- Background process
- Required for long-running clusters

---

## Cost Control

- Sample harder
- Drop boring tags
- Shorten retention
- Tier storage

---

## Privacy

- PII in tags must be redacted
- Configure redaction at collector
- Audit tag values
- Compliance dictates

---

## Capacity Planning

- Spans per second
- Tags per span
- Average span size
- Multiplied by retention

---

## Common Storage Mistakes

- 100% sampling forever
- No retention policy
- One backend node
- Skipping index tuning
- Storing PII without redaction
