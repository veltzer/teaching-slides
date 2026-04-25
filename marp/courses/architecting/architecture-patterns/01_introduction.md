---
tags:
  - concepts:architecture
  - concepts:design-patterns
level: intermediate
category: architecture
audience:
  - audiences:developers
  - audiences:architects

---
# Introduction & Pattern Taxonomy

---
## What an Architectural Pattern Is

- A named, reusable solution to a recurring structural problem in software
- Defined by:
    - The forces or trade-offs it balances
    - The components and their relationships
    - The constraints it imposes
- Patterns describe shapes, not implementations — they survive technology churn

---
## What This Course Covers

- A working catalog of architectural patterns at three scopes:
    - Communication patterns (how components talk)
    - System architectures (how applications are structured)
    - Internal code architectures (how a single application is layered)
- Operational deep-dives on the data path:
    - Databases, caching, isolation, queues, streaming, big data, monitoring
- Each pattern is presented with overview, key concepts, diagram, pros/cons, and when to use

---
## Audience and Level

- Intermediate developers and architects
- Assumes basic familiarity with web services, databases, and concurrency
- Goal: be able to recognize, name, and choose between competing patterns
- Not a prescription — every pattern has trade-offs and a context where it fails

---
## Pattern Scope: Three Levels

1. Communication Patterns
    - How two or more components exchange information
    - Examples: Client-Server, Broker, Pub-Sub, Event Bus
1. System Architectures
    - How an application is decomposed into deployable units
    - Examples: Monolith, Microservices, SOA, Serverless, EDA
1. Internal Code Architectures
    - How a single deployable is organized internally
    - Examples: Hexagonal, Clean, Onion, DDD, CQRS

---
## Cross-Cutting Concerns

- Some patterns address concerns that span scopes:
    - Resiliency: Circuit Breaker, Bulkhead, Saga, Retry
    - Integration: API Gateway, BFF, Anti-Corruption Layer
    - Operations: Throttling, Sidecar, Ambassador
- These are usually overlaid on top of a primary architecture

---
## Data and Operations

- A correct architecture means little without the right data path
- This course also covers:
    - Storage: SQL, NoSQL, sharding, replication
    - Concurrency: isolation levels, transactions
    - Performance: caching strategies
    - Asynchrony: queues, Kafka, streaming
    - Scale: data lakes, big data, batch + streaming
    - Visibility: monitoring, observability

---
## How to Read This Course

- Each chapter groups related patterns
- Compare patterns within a chapter — the differences are the lesson
- Compare across chapters — many patterns combine (e.g., Microservices + API Gateway + Saga)
- The goal is judgment, not memorization

---
## A Note on Trade-Offs

- Every pattern adds complexity in exchange for some property:
    - Coupling vs. autonomy
    - Consistency vs. availability
    - Latency vs. throughput
    - Simplicity vs. flexibility
- "It depends" is the honest answer to most architecture questions
- The patterns name the dependencies so you can reason about them

---
## Course Outline

- 02 Communication Patterns
- 03 System Architectures
- 04 Internal Code Architectures
- 05 Classic Structural Patterns
- 06 Resiliency & Cross-Cutting Patterns
- 07 Small-Scale Design Patterns
- 08-17 Data, concurrency, caching, streaming, big data, workflows, monitoring
