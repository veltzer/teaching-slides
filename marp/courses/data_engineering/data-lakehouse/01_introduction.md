---
tags:
  - data-and-ai:data-engineering
level: intermediate
category: data-engineering
audience:
  - audiences:data-engineers
  - audiences:architects

---
# Introduction to Data Lakehouse

---
## What This Chapter Covers

- What a lakehouse is
- Lake vs warehouse vs lakehouse
- Why now
- Components
- Course outline

---
## What a Lakehouse Is

- Single store for raw and curated data
- Open file formats
- Transactional metadata layer
- Both BI and ML workloads

---
## Data Lake

- Cheap object storage
- Any format
- Schema on read
- Flexible but messy

---
## Data Warehouse

- Structured tables
- Strong SQL
- Curated schemas
- Expensive at scale

---
## The Gap

- Two systems, two copies
- ETL between them
- Stale data in warehouse
- Wasted storage

---
## Lake vs Warehouse vs Lakehouse

![lakehouse_compare](svg/courses/data_engineering/data-lakehouse/01_introduction/lakehouse_compare.svg)

---
## Lakehouse Promise

- One copy of the data
- Both batch and stream
- Both BI and ML
- Open formats

---
## Why Now

- Cheap object storage matured
- Open formats hardened
- Query engines improved
- Cloud platforms support it

---
## Open Table Formats

- Provide ACID over object stores
- Versioned writes
- Schema evolution
- Compaction and clustering

---
## Storage Layer

- Object stores (S3 and equivalents)
- Cheap, durable, scalable
- Eventually consistent listings
- Designed for big-block reads

---
## Compute Engines

- Read open tables
- Scale independent of storage
- Multiple engines on one table
- Pay for what you use

---
## Workloads

- Batch ETL
- Streaming ingestion
- BI queries
- ML feature pipelines

---
## When Lakehouse Fits

- Mixed BI and ML
- Multi-engine teams
- Cost pressure on warehouse
- Data sovereignty needs

---
## Course Outline

- Storage and formats
- Table formats
- Ingestion
- Querying
- Operations

---
## Common Beginner Mistakes

- Treating object store as a database
- No schema discipline
- Too many small files
- One engine forever
- No retention policy
