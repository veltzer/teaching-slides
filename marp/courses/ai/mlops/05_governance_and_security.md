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
# Governance and Security

---
## What This Chapter Covers

- Data governance
- Model cards
- Privacy
- Security threats
- Compliance

---
## Data Governance

- Catalog of datasets
- Owners and stewards
- Quality SLAs
- Access controls

---
## PII Handling

- Identify and tag PII
- Mask, hash, or tokenize
- Encrypt at rest and in transit
- Limit who and what can read

---
## Model Cards

- Intended use
- Training data summary
- Metrics across slices
- Known limitations

---
## Datasheets for Datasets

- Source and collection
- Preprocessing
- Demographic coverage
- License and consent

---
## Bias and Fairness

- Slice metrics by sensitive group
- Fix data or model
- Document residual bias
- Monitor in production

---
## Slice Metrics

![bias_slices](svg/courses/ai/mlops/05_governance_and_security/bias_slices.svg)

---
## Threats Overview

![threats](svg/courses/ai/mlops/05_governance_and_security/threats.svg)

---
## Threats: Data Poisoning

- Attacker plants bad samples
- Model learns wrong signal
- Validate data sources
- Detect anomalies in distributions

---
## Threats: Adversarial Inputs

- Crafted inputs flip predictions
- Common in vision and NLP
- Use robust training
- Test with adversarial sets

---
## Threats: Model Theft

- Predictions leak weights
- Throttle queries
- Watermark outputs
- Limit confidence scores

---
## Threats: Inversion

- Reconstructing training data
- Differential privacy mitigates
- Limit memorization
- Audit memorized strings

---
## Compliance

- GDPR right to be forgotten
- HIPAA for health data
- SOC2 for vendors
- Sector-specific rules

---
## Audit Trail

- Who deployed which model when
- Which data trained it
- Which prediction came from where
- Retain by policy

---
## Access Control

- Per-environment IAM
- Least privilege
- Separate prod credentials
- Rotate secrets

---
## Common Governance Mistakes

- No data catalog
- No model card
- Treating compliance as a one-off
- No incident playbook
- Storing PII in features
