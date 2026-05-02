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
# Experiment Tracking and Model Registry

---
## What This Chapter Covers

- Why track experiments
- What to log
- Comparison and search
- Model registry
- Promotion flow

---
## Why Tracking

- Reproducibility
- Compare runs
- Defend a model decision
- Debug regressions

---
## What to Log

- Code version
- Data version
- Hyperparameters
- Metrics
- Artifacts

---
## Tools

- MLflow: open, simple
- Weights and Biases: rich UI
- Neptune, Comet: similar
- Pick one and standardize

---
## Run Identity

- Unique ID per run
- Tag by experiment, branch, user
- Group related runs
- Always link to git SHA

---
## Metrics Beyond Accuracy

- Precision, recall, F1
- Calibration
- Fairness slices
- Latency at inference
- Cost per inference

---
## Artifacts

- Model weights
- Confusion matrices
- Feature importance
- Sample predictions
- Evaluation reports

---
## Model Registry

- Source of truth for models
- Versioned by hash
- Metadata: metrics, owner, lineage
- Stage: dev, staging, prod

---
## Promotion Flow

- Train and evaluate
- Register candidate
- Run shadow tests
- Promote to staging
- Promote to prod

---
## Promotion Visualized

![registry_promotion](svg/courses/ai/mlops/03_experiment_tracking_and_registry/registry_promotion.svg)

---
## Approval Gates

- Metric thresholds
- Bias and fairness checks
- Security scan of dependencies
- Manual sign-off when required

---
## Lineage

- Which data trained which model
- Which model served which prediction
- Required for audits
- Required for incident triage

---
## Rollbacks

- Keep previous version warm
- One-line revert
- Feature-flag rollouts
- Canary new versions

---
## Common Tracking Mistakes

- Logging only the final run
- No data version
- No git SHA
- Manual exports of metrics
- Treating notebooks as the registry
