---
tags:
  - data-and-ai:big-data
level: intermediate
category: data-engineering
audience:
  - audiences:data-engineers

---
# Introduction to Spark

---
## What This Chapter Covers

- What Spark is
- Architecture
- APIs
- Where Spark fits
- Course outline

---
## What Spark Is

- Distributed compute engine
- In-memory where possible
- Works on petabyte data
- Multi-language SDK

---
## Why Spark

- Replaced MapReduce
- Faster on iterative work
- Unified batch and stream
- Strong ecosystem

---
## Architecture

- Driver coordinates
- Cluster manager schedules
- Executors do work
- Storage external

---
## Components

![spark_pieces](svg/courses/data_engineering/spark/01_introduction/spark_pieces.svg)

---
## Cluster Architecture

![spark_cluster](svg/courses/data_engineering/spark/01_introduction/spark_cluster.svg)

---
## Driver

- Plans the job
- Tracks state
- Sends tasks to executors
- Single point of failure for job

---
## Executors

- Run tasks
- Hold cached data
- Shuffle service
- One per worker per app

---
## Cluster Managers

- Standalone
- YARN
- Kubernetes
- Mesos (declining)

---
## APIs

- RDD: low-level, rarely used today
- DataFrame: typed columns, optimized
- Dataset: typed rows in JVM
- Streaming and SQL on same engine

---
## Lazy Evaluation

- Transformations build a plan
- Actions trigger execution
- Catalyst optimizes
- Saves work

---
## Storage Sources

- Local files
- HDFS
- S3 and equivalents
- Databases via JDBC

---
## When Spark Wins

- Multi-TB data
- Complex transformations
- ML on big data
- ETL into warehouses

---
## When It Loses

- Small data: overhead too big
- Pure SQL on warehouse: warehouse wins
- Single-machine analytics: pandas-class tools win
- Streaming with strict latency: dedicated engines

---
## Course Outline

- DataFrames
- SQL
- Performance
- Streaming
- Operations

---
## Common Beginner Mistakes

- collect() on big data
- No schema
- Wrong join type
- One partition for huge data
- Caching everything
