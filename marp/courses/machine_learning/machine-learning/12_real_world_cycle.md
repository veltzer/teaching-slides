---
tags:
  - data-and-ai:machine-learning
level: intermediate
category: machine-learning
audience:
  - audiences:data-scientists

---
# Real World ML Cycle

---
## What This Chapter Covers

- Project framing
- Baselines
- Iteration
- Deployment options
- Monitoring
- Drift and retraining
- A/B testing
- MLOps basics

---
## The Cycle

- Frame
- Data
- Train
- Evaluate
- Deploy
- Monitor
- Retrain

---
## Frame The Problem

- What decision does this support
- Who consumes the prediction
- What's the metric
- What's the cost of being wrong

---
## Define Success Early

- Business KPI, not just model metric
- Revenue, retention, latency
- Tie metric to KPI
- Agree before training

---
## Stakeholders

- Product
- Engineering
- Data
- Legal and compliance
- Talk to all of them

---
## Baselines First

- Random guess
- Majority class
- Simple rule
- Linear / logistic regression
- Beat these before going fancy

---
## Why Baselines

- Tells you the floor
- Cheap to run
- Sanity check
- Sometimes good enough

---
## Iteration

- One change at a time
- Track experiments
- Reproduce results
- Compare honestly

---
## Experiment Tracking

- MLflow, Weights and Biases, Neptune
- Hyperparameters, metrics, artefacts
- Searchable history
- Shareable

---
## Reproducibility

- Pin versions
- Seed RNGs
- Track data versions
- Containerise

---
## Data Versioning

- DVC, lakeFS, Delta Lake
- Snapshots of training data
- Re-run any experiment
- Audit trail

---
## Train In CI

- Run training in CI
- Reproducible builds
- Tests pass before merging
- Catches accidental regressions

---
## Deployment Options

- Batch: predict offline, store
- Real-time: REST or gRPC API
- Streaming: Kafka, Flink
- Edge: phone, IoT, browser

---
## Batch Serving

- Run nightly, store predictions
- Cheapest, simplest
- Latency is hours
- Good for scoring catalogues

---
## Real-Time Serving

- HTTP endpoint
- Sub-second latency
- Autoscale
- Most complexity

---
## Edge Serving

- Run on device
- Privacy
- Offline
- Constraints: memory, power

---
## Inference Optimisation

- Quantisation
- Pruning
- Distillation
- ONNX, TensorRT, OpenVINO

---
## Feature Stores

- Centralised feature storage
- Same features train and serve
- Avoids skew
- Feast, Tecton, Hopsworks

---
## Train-Serve Skew

- Different features in training vs production
- Silent killer
- Same code path
- Feature stores help

---
## Model Registry

- Versioned models
- Stages: dev, staging, prod
- Rollback support
- MLflow, SageMaker, Vertex

---
## Model Packaging

- Container image
- Model file + dependencies
- Reproducible
- Scan for vulnerabilities

---
## Canary Deployment

- Roll out to small percentage
- Monitor
- Promote or rollback
- Standard for risky changes

---
## Shadow Mode

- Run new model in parallel
- Don't act on its predictions
- Compare to current
- Validate before switch

---
## Rollback Plan

- Always have one
- One-command revert
- Practise it
- Old model stays warm

---
## A/B Testing

- Random assignment to model versions
- Measure business KPI
- Statistical test for significance
- Run long enough

---
## Sample Size

- Power analysis upfront
- Detect the smallest effect that matters
- Don't peek
- Document the plan

---
## Multi-Armed Bandit

- Adaptive A/B
- Exploit better arms over time
- Useful when traffic is precious
- Less rigorous than full A/B

---
## Monitoring

- Inputs
- Outputs
- Performance
- System health

---
## Input Drift

- Distribution of features changes
- Statistical tests, KL divergence
- Alerts when drift exceeds threshold

---
## Output Drift

- Distribution of predictions changes
- Cheap to monitor
- Catches many problems
- Still need ground truth eventually

---
## Performance Decay

- Compare predictions to actuals
- Latency between prediction and label
- Lagging indicator
- Plan retraining frequency

---
## Logging

- Every prediction
- Inputs, output, version, timestamp
- Helps debugging
- Needed for retraining

---
## Alerting

- Drift exceeded
- Error rate up
- Latency up
- Page someone

---
## Retraining

- Scheduled
- Triggered by drift
- Continuous learning
- Match cadence to problem

---
## Continual Learning

- Update model with new data
- Risk of forgetting
- Replay old data
- Validate every update

---
## Champion Challenger

- New model challenges current
- Promote if better on holdout
- Automated pipeline
- Standard pattern

---
## MLOps Pipeline

- Data ingest
- Validation
- Train
- Evaluate
- Register
- Deploy

---
## CI / CD For ML

- Code, data, model all versioned
- Automated tests
- Promotion through stages
- Rollback ready

---
## Common Production Mistakes

- No monitoring
- No rollback plan
- One-off training, never retrained
- Train-serve skew
- Deploying without baselines

---
## Summary

- ML success is mostly process
- Baselines, monitoring, retraining
- Train-serve consistency
- Treat models like software, but more

---
## Champion / Challenger

![champion_challenger](svg/courses/machine_learning/machine-learning/12_real_world_cycle/champion_challenger.svg)

---
## A/B vs Bandit

![ab_vs_bandit](svg/courses/machine_learning/machine-learning/12_real_world_cycle/ab_vs_bandit.svg)

---
## Drift Monitoring

![drift_monitoring](svg/courses/machine_learning/machine-learning/12_real_world_cycle/drift_monitoring.svg)

---
## MLOps Pipeline

![mlops_pipeline](svg/courses/machine_learning/machine-learning/12_real_world_cycle/mlops_pipeline.svg)

---
## Train-Serve Skew

![train_serve_skew](svg/courses/machine_learning/machine-learning/12_real_world_cycle/train_serve_skew.svg)

---
## Canary / Shadow

![canary_shadow](svg/courses/machine_learning/machine-learning/12_real_world_cycle/canary_shadow.svg)

---
## Retraining Loop

![retraining_loop](svg/courses/machine_learning/machine-learning/12_real_world_cycle/retraining_loop.svg)

---
## End Of Module

- ML is engineering plus statistics
- Iterate fast, monitor everything
- Be honest about results
