---
tags:
  - data-and-ai:data-engineering
level: intermediate
category: data-engineering
audience:
  - audiences:data-engineers

---
# Introduction to ETL

---
## What This Chapter Covers

- What ETL is
- ETL vs ELT
- Why ELT won
- Common architectures
- Course outline

---
## What ETL Is

- Extract from source
- Transform data
- Load into target
- Move data where it is useful

---
## What Each Step Does

- Extract: read from systems
- Transform: clean and reshape
- Load: write to destination
- Schedule: repeat

---
## Why ETL

- Source systems are operational
- Targets are analytical
- Data formats differ
- Volumes need batching

---
## ETL vs ELT

- ETL transforms before load
- ELT loads raw, then transforms
- ELT relies on target compute
- Most modern warehouses use ELT

---
## Why ELT Won

- Cheap warehouse compute
- Faster iteration
- Raw data preserved
- Simpler operationally

---
## Where ETL Still Fits

- Sensitive data masking
- Format incompatibilities
- Slow transforms
- Air-gapped environments

---
## Common Sources

- Operational databases
- Files
- APIs
- Event streams

---
## Common Targets

- Data warehouse
- Data lakehouse
- Search engine
- Cache

---
## Batch vs Streaming

- Batch: periodic
- Streaming: continuous
- Lambda: both at once
- Kappa: streaming only

---
## Tools Landscape

- Workflow orchestrators
- Connector platforms
- Transformation frameworks
- Hand-coded scripts

---
## Build vs Buy

- Connectors are commodity products
- Transforms are domain-specific
- Buy connectors, write transforms
- Mind cost at scale

---
## Course Outline

- Extraction
- Loading
- Transformation
- Orchestration
- Operations

---
## Common ETL Beginner Mistakes

- One giant pipeline
- No idempotency
- Hand-coded connectors
- Transforms in extract step
- No data quality checks
