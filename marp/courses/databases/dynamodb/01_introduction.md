---
tags:
  - databases:dynamodb
level: intermediate
category: databases
audience:
  - audiences:developers

---
# Introduction to DynamoDB

---
## What This Chapter Covers

- What DynamoDB is
- Why hosted NoSQL
- Architecture
- Use cases
- Course outline

---
## What DynamoDB Is

- Hosted key-value and document store
- Single-digit millisecond latency
- Auto-scales storage and throughput
- Multi-region option

---
## Why Hosted

- No servers to manage
- No patching
- No capacity planning at the OS level
- Pay per request or provisioned

---
## When To Use

- High-throughput key-value
- Predictable access patterns
- Serverless apps
- Multi-region active-active

---
## Fit Visualised

![dynamo_fit](svg/courses/databases/dynamodb/01_introduction/dynamo_fit.svg)

---
## When Not To Use

- Ad-hoc analytics
- Complex relational queries
- Many cross-item joins
- Cost-sensitive read-heavy traffic

---
## Architecture

- Tables of items
- Each item identified by primary key
- Items can have flexible attributes
- Storage and compute managed

---
## Primary Keys

- Partition key alone
- Or partition key plus sort key
- Determines distribution
- Most important design choice

---
## Partition Routing

![partition_routing](svg/courses/databases/dynamodb/01_introduction/partition_routing.svg)

---
## Capacity Modes

- On-demand: pay per request
- Provisioned: pay for reserved throughput
- Auto-scaling adjusts provisioned
- Switch as workloads stabilize

---
## Consistency

- Eventual by default
- Strongly consistent reads optional
- Strong reads cost more
- Local to region

---
## Global Tables

- Multi-region replication
- Active-active writes
- Last-writer-wins resolution
- Latency local to user

---
## Streams

- Change feed of table writes
- Trigger Lambdas
- Replicate to other systems
- 24-hour retention

---
## Time To Live

- Per-item expiration
- Removes within hours of TTL
- Cheap to set
- Useful for sessions and caches

---
## Course Outline

- Data modeling
- Querying
- Capacity
- Multi-region
- Operations

---
## Common Beginner Mistakes

- Using it like a relational store
- Hot partitions from monotonic keys
- Strongly consistent reads everywhere
- Scan instead of Query
- No GSI plan
