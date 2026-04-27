---
tags:
  - data-and-ai:nlp
  - concepts:deployment
level: advanced
category: ai
audience:
  - audiences:developers
  - audiences:data-scientists
  - audiences:architects

---
# Practical NLP Systems

---
## What This Chapter Covers

- The lifecycle of an `NLP` system from problem definition to retirement
- Architecture patterns for serving language models in production
- Data engineering: collection, labeling, versioning, and feedback loops
- Monitoring, observability, and incident response specific to language models
- Cost engineering: where the dollars go and how to compress them
- The skills that turn a notebook into a system that runs without you

---
## From Notebook to System

- A working notebook is the start, not the finish
- Production-grade `NLP` is mostly engineering, not modeling
- The hard problems are reliability, cost, observability, evolution
- This chapter is about what comes after the model trains
- Few of these lessons make it into research papers

---
## NLP System Lifecycle

![nlp_lifecycle](svg/courses/ai/natural-language-processing/26_practical_nlp_systems/nlp_lifecycle.svg)

---
## Defining the Problem

- Start with the user-visible behavior, not the model
- A measurable success criterion, not a vibe
- A failure mode budget — what is acceptable when the system is wrong
- Stakeholders aligned on scope before any modeling
- The most expensive bug to fix is a misframed problem

---
## Choosing the Approach

- Rule-based when the rules are stable and small
- Classical `ML` when interpretability matters and data is small
- Fine-tuned transformer when accuracy beats cost
- Prompted `LLM` when iteration speed beats cost
- The right answer changes as the system matures

---
## Data Collection

- The single biggest determinant of system quality
- Coverage of the actual user distribution, not the easy distribution
- Edge cases collected deliberately, not hoped for
- Synthetic data has its place but cannot substitute for the real thing
- Allocate engineering effort here, not just labeling budget

---
## Annotation Pipelines

- Define the schema before annotating a single example
- Pilot with a few annotators before scaling to many
- Track inter-annotator agreement; below 0.7 indicates an unclear schema
- Reconcile disagreements with adjudication, not majority vote
- Label dataset versioning is as important as code versioning

---
## Annotation Quality Control

- Gold questions seeded among real questions
- Per-annotator quality scores; remove low performers
- Active learning to focus annotation on hard examples
- Calibration training rounds for new annotators
- A messy label set produces a messy model — debt compounds

---
## Data Versioning

- Datasets evolve; freeze versions for reproducibility
- `DVC`, `LakeFS`, `lakeFS`, `Weights & Biases Artifacts`
- Tag training, validation, and test versions independently
- A model trained on dataset v3 should be reproducible later
- Treat data as a first-class artifact, not a side effect

---
## Training Pipelines

- Reproducible from a single command, ideally with `Make` or a workflow tool
- Hyperparameter sweeps logged to a tracking system
- Checkpoints versioned and immutable
- Evaluation runs gated by a quality threshold before promotion
- A pipeline that lives in someone's notebook is a future incident

---
## Model Registry

- Central catalog of trained models with metadata
- Each entry: training data version, code commit, metrics, evaluation reports
- Promotion through stages: dev → staging → prod
- Rollback to any prior version on demand
- The model registry is what makes "ship a model" a routine operation

---
## Serving Architecture

![serving_architecture](svg/courses/ai/natural-language-processing/26_practical_nlp_systems/serving_architecture.svg)

---
## Inference Optimization

- Quantization (`INT8`, `INT4`) shrinks models without retraining
- Distillation produces smaller students for production
- Pruning removes redundant parameters
- Compilation with `TensorRT`, `ONNX Runtime`, `vLLM` gets the most from hardware
- Inference cost dominates training cost for any product that ships

---
## Quantization

- Reduce parameter precision to `INT8`, `INT4`, or lower
- 4x memory and bandwidth savings with minimal accuracy loss
- Per-channel and group-wise quantization preserve quality
- `GPTQ`, `AWQ`, `bitsandbytes` are common toolkits
- The cheapest first step in inference cost reduction

---
## Distillation

- Train a small student to mimic a large teacher
- Teacher provides soft labels that carry richer signal than hard labels
- Often recovers 90%+ of teacher quality at 10x speed
- `DistilBERT`, `MiniLM`, and many production checkpoints exist
- Especially valuable for latency-sensitive serving

---
## Caching Strategies

- Embedding cache for documents that never change
- Prompt cache for shared system prompts across requests
- KV cache reuse across decode steps
- Result cache for common queries with idempotent outputs
- Caching is the single biggest cost lever after model size

---
## Latency Engineering

- Latency-to-first-token matters more than total time on chat
- Streaming hides total latency behind perceived responsiveness
- Speculative decoding cuts inference time substantially
- Continuous batching keeps GPUs busy across requests
- Tail latency at p99 matters more than average

---
## Observability

- Log every prediction with input, output, and metadata
- Distribution metrics: token count, sentiment, language, error rate
- Per-cohort metrics across user segments
- Alerts for distribution shifts before users complain
- An `NLP` system without observability is a black box

---
## Drift Detection

- Input drift: user queries change over time
- Output drift: model outputs change after a release
- Performance drift: accuracy degrades against a held-out gold set
- Continuous monitoring catches drift before it becomes an outage
- Drift dashboards belong on the same screen as health checks

---
## Drift in Production

![drift_detection](svg/courses/ai/natural-language-processing/26_practical_nlp_systems/drift_detection.svg)

---
## A/B Testing

- Compare candidate model against the current production model
- Statistical power planning before launch
- Per-segment analysis to catch reverse effects
- Multiple metrics gate promotion: quality, latency, cost, complaints
- Trust the test, not your intuition

---
## Shadow Deployment

- Run a candidate model on real traffic without exposing outputs to users
- Compare against production model offline
- Catches issues that synthetic tests miss
- A required step before any high-risk model swap
- Cost: doubles inference compute for the shadow window

---
## Feedback Loops

- Capture user signals: thumbs, edits, dwell time, conversion
- Use signals to retrain and improve over time
- Beware the feedback trap: the model shapes the data that shapes the model
- Calibrate signals against held-out gold to stay grounded
- A working feedback loop is the durable advantage of mature systems

---
## Incident Response

- A clear on-call rotation for the team that owns the model
- Runbooks for common failures: latency, accuracy regression, content issues
- Rollback plan tested before deployment, not during
- Postmortems with root cause and prevention, not blame
- `NLP` incidents differ from outages — model misbehavior may not look like a "down" event

---
## Cost Engineering

- Track cost per query as a first-class metric
- Token-level pricing rewards prompt compression
- Mixed-model routing: cheap model for easy queries, expensive for hard ones
- Cache the expensive paths; precompute when possible
- The most accurate model that bankrupts the team is not the right one

---
## Mixed-Model Routing

- A small classifier decides which model serves a given query
- Easy queries go to a cheap fast model
- Hard queries escalate to a stronger model
- Often cuts cost 5-10x with negligible quality loss
- A standard production pattern at scale

---
## Compliance and Auditing

- Log retention policies for personally identifiable content
- Right-to-be-forgotten support if your jurisdiction requires it
- Bias audits run on a schedule, not just at launch
- Accessibility for screen readers and other assistive tech
- Document the system enough that an auditor can verify it

---
## Team Skills

- `NLP` engineers + ML engineers + product + data + infra + linguists + annotators
- The notebook-only researcher is not enough
- Production `NLP` is a multidisciplinary team effort
- Hire for systems thinking and feedback loops, not just modeling
- Career growth comes from owning a feature end to end

---
## Documentation

- Model cards for every deployed model
- Data sheets for every annotated dataset
- Runbooks for every recurring failure mode
- Architecture decision records for irreversible choices
- An `NLP` system you cannot explain is one you cannot maintain

---
## Retirement

- Models eventually outlive their usefulness
- Retirement is an explicit decision, not neglect
- Migrate users, archive the registry entry, redirect monitoring
- Document why the model existed and why it was sunset
- A clean retirement is part of system hygiene

---
## Common Production Pitfalls

- Treating evaluation as a one-time gate instead of a continuous practice
- Ignoring p99 latency until users complain
- No rollback plan for the model swap
- Skipping data versioning because "we have git"
- Coupling model and serving code so tightly that updating either breaks both

---
## Anti-Patterns

- The "we'll instrument it next sprint" production system
- Single point of failure in a hand-tuned prompt with no version control
- Cost dashboards built only after the budget is already over
- Annotators with no path to escalate ambiguous examples
- Models retired by deletion rather than archive

---
## What Good Looks Like

- A system that passes regression tests on every change
- Drift dashboards reviewed weekly
- Cost per query trending down across releases
- Model swaps that are routine, not heroic
- A team that can ship the next version without the original author

---
## Summary

- `NLP` systems live or die in production, not in notebooks
- Data, evaluation, and monitoring are first-class engineering concerns
- Cost and latency are quality dimensions, not nice-to-haves
- Feedback loops are the durable advantage of mature systems
- Build for change: models, data, and requirements all evolve continuously
