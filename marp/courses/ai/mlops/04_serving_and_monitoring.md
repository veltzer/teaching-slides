---
tags:
  - data-and-ai:machine-learning
  - practices:devops
level: advanced
category: machine-learning
audience:
  - audiences:data-scientists
  - audiences:devops

---
# Serving and Monitoring

---
## What This Chapter Covers

- Serving patterns
- Performance
- Monitoring quality
- Drift
- Alerts

---
## Online Serving

- Synchronous request, response
- Tight latency budget
- Autoscaling
- High availability

---
## Batch Serving

- Bulk inference offline
- Throughput over latency
- Cheaper compute
- Scheduled jobs

---
## Streaming Serving

- Process events as they arrive
- Microsecond to second latency
- Often Kafka backed
- State for session-based features

---
## Serving Frameworks

- TensorFlow Serving
- PyTorch Serve
- BentoML
- KServe

---
## Performance Knobs

- Batch size
- Quantization
- GPU vs CPU
- Async pipelining

---
## Operational Metrics

- Latency p50, p95, p99
- QPS
- Error rate
- Resource use

---
## Quality Metrics

- Live accuracy where labels arrive
- Calibration
- Slice metrics
- Business KPI link

---
## Data Drift

- Input distribution changes
- Compare live data to training
- Statistical tests
- Alert when drift exceeds threshold

---
## Concept Drift

- Relationship between input and label changes
- Detected via dropping accuracy
- Often slower than data drift
- Triggers retraining

---
## Shadow and Canary

- Shadow: new model gets traffic, no answer
- Canary: small slice of users
- Compare metrics
- Promote on success

---
## A/B Testing

- Split users
- Equal traffic, different model
- Measure business KPI
- Decide with statistical rigor

---
## Alerting

- On latency
- On error rate
- On drift
- On accuracy regression

---
## Common Serving Mistakes

- No online metrics
- No drift monitor
- Hard rollouts
- No load test
- Training and serving skew
