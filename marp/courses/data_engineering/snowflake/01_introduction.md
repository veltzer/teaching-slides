---
tags:
  - data-and-ai:data-engineering
level: intermediate
category: data-engineering
audience:
  - audiences:data-engineers

---

# Introduction to Snowflake

---

## What This Chapter Covers

- What Snowflake is
- Architecture
- Account model
- Pricing
- Course outline

---

## What Snowflake Is

- Cloud data warehouse
- SaaS, runs on AWS, Azure, GCP
- Stores compressed columnar data
- Decoupled storage and compute

---

## Why It Took Off

- Easy to operate
- Scales without moving data
- Strong performance defaults
- Familiar SQL

---

## Architecture

- Storage layer on object storage
- Compute on virtual warehouses
- Cloud services layer for metadata
- Each scales independently

---

## Architecture Visualized

![snowflake_arch](svg/courses/data_engineering/snowflake/01_introduction/snowflake_arch.svg)

---

## Virtual Warehouses

- Compute clusters
- T-shirt sizes
- Suspend when idle
- Scale up or out per workload

---

## Multi-Cluster

- Add clusters under load
- Each handles a slice of queries
- Automatic queue management
- Pay for active clusters

---

## Storage

- Compressed columnar
- Micro-partitions
- Automatic clustering
- Time travel built in

---

## Account Model

- Account at top
- Databases, schemas, tables
- Roles and users
- Resource monitors for cost

---

## Core Concepts

![snowflake_concepts](svg/courses/data_engineering/snowflake/01_introduction/snowflake_concepts.svg)

---

## Roles

- Hierarchical
- Privileges granted to roles
- Users assume roles
- Role-based access control everywhere

---

## Pricing Model

- Storage by GB month
- Compute by warehouse second
- Cloud services usage
- Egress in some cases

---

## Auto-Suspend

- Warehouses stop when idle
- Default 10 minutes
- Tune lower to save cost
- Restart latency is small

---

## Editions

- Standard
- Enterprise
- Business Critical
- Higher tiers add features and SLAs

---

## Course Outline

- Tables and storage
- Loading data
- Query performance
- Data sharing
- Operations

---

## Common Beginner Mistakes

- One huge warehouse for everything
- No auto-suspend
- No resource monitor
- Wide users with account admin
- Ignoring micro-partition skew
