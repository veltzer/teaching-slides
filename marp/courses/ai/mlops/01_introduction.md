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
# Introduction to MLOps

---
## What This Chapter Covers

- What MLOps is
- Why it differs from DevOps
- The ML lifecycle
- Common roles
- Tooling landscape

---
## What MLOps Is

- DevOps for machine learning
- Reproducible training and serving
- Automated pipelines
- Continuous delivery of models

---
## Why Not Just DevOps

- Models are data plus code
- Outputs drift over time
- Training is expensive
- Evaluation is statistical, not boolean

---
## ML Lifecycle

- Data ingestion
- Feature engineering
- Training
- Evaluation
- Deployment
- Monitoring

---
## Reproducibility

- Pin data version
- Pin code version
- Pin environment
- Pin random seed

---
## Roles

- Data engineer
- Data scientist
- ML engineer
- Platform engineer
- SRE

---
## Why Roles Blur

- Data scientists ship code
- Engineers tune models
- SREs read confusion matrices
- Hand-offs cause failures

---
## Tooling Landscape

- Pipelines: Kubeflow, Airflow
- Tracking: MLflow, W&B
- Serving: Seldon, BentoML, KServe
- Feature stores: Feast, Tecton

---
## Build vs Buy

- Cloud platforms bundle most of it
- OSS gives flexibility, costs effort
- Mix is common
- Choose by team size

---
## Maturity Levels

- Manual everything
- CI for code
- CI for data and models
- Auto-retraining and rollback

---
## Cost Reality

- GPUs are expensive
- Storage adds up
- Idle clusters bleed money
- Track cost per experiment

---
## Course Outline

- Pipelines
- Experiment tracking
- Model registry and serving
- Monitoring and drift
- Governance

---
## Common Misconceptions

- "Just deploy the notebook"
- "Accuracy is enough"
- "We will retrain when needed"
- "It is just DevOps"
- "We do not need a feature store"
