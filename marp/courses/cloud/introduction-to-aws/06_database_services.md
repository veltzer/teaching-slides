---
tags:
  - infrastructure:cloud
  - infrastructure:aws
  - infrastructure:databases
level: beginner
category: cloud
audience:
  - audiences:developers
  - audiences:sysadmins
  - audiences:managers

---
# Database Services

---

## Why Managed Databases?
- No server provisioning or patching
- Automated backups and recovery
- High availability built in
- Scalability without downtime
- Focus on your application, not the database

---

## Database Models
- Relational (SQL): structured data, ACID transactions
- Key-Value: simple lookups, high throughput
- Document: flexible schemas, JSON-like data
- Graph: relationships between entities
- Choose based on data model and access patterns

---

## SQL vs NoSQL
- SQL: fixed schema, joins, transactions
- NoSQL: flexible schema, horizontal scaling
- SQL: best for complex queries and relationships
- NoSQL: best for high throughput and simple access
- AWS offers managed services for both

---

## AWS Database Services Overview
- Amazon RDS: managed relational databases
- Amazon Aurora: high-performance relational
- Amazon DynamoDB: managed NoSQL
- Amazon ElastiCache: in-memory caching
- Amazon Redshift: data warehousing

---

## Amazon RDS Overview
- Relational Database Service
- Managed relational databases
- Handles provisioning, patching, backups
- Six database engines supported
- Multi-AZ for high availability

---

## RDS Supported Engines
1. Amazon Aurora (MySQL and PostgreSQL compatible)
1. MySQL
1. PostgreSQL
1. MariaDB
1. Oracle
1. SQL Server

---

## RDS Instance Classes
- Standard (db.m6i): general purpose
- Memory Optimized (db.r6i): memory-intensive
- Burstable (db.t3): variable workloads
- Choose based on workload requirements
- Can resize with some downtime

---

## Amazon Aurora
- AWS-built relational database
- MySQL and PostgreSQL compatible
- Up to 5x faster than standard MySQL
- Up to 3x faster than standard PostgreSQL
- Auto-scales storage up to 128 TB

---

## Aurora Architecture
- Shared distributed storage layer
- 6 copies of data across 3 AZs
- Self-healing storage
- Continuous backup to S3
- Up to 15 read replicas with low lag

---

## Aurora Serverless
- On-demand auto-scaling Aurora
- Scales compute capacity up and down
- Pay per second of usage
- Ideal for intermittent or unpredictable workloads
- No capacity planning needed

---

## RDS Multi-AZ Deployments
- Synchronous replication to standby
- Automatic failover on failure (60-120 seconds)
- No manual intervention required
- Same DNS endpoint after failover
- Use for production databases

---

## RDS Read Replicas
- Asynchronous replication
- Offload read traffic from primary
- Up to 5 read replicas (RDS), 15 (Aurora)
- Can be in different Regions
- Can be promoted to standalone database

---

## RDS Backups
- Automated daily backups (snapshot + transaction logs)
- Retention period: 1-35 days
- Manual snapshots (no expiration)
- Point-in-time recovery (to any second in retention period)
- Snapshots can be shared or copied across Regions

---

## RDS Security
- Encryption at rest with KMS
- Encryption in transit with SSL/TLS
- Network isolation with VPC
- Security Groups control access
- IAM database authentication (MySQL, PostgreSQL)

---

## Amazon DynamoDB Overview
- Fully managed NoSQL database
- Key-value and document data model
- Single-digit millisecond performance at any scale
- Serverless (no servers to manage)
- Automatic scaling

---

## DynamoDB Key Concepts
- Tables: collection of items
- Items: collection of attributes (like rows)
- Primary Key: partition key or partition + sort key
- Attributes: data elements (like columns)
- No fixed schema beyond the primary key

---

## DynamoDB Partition Key
- Hash key: determines data distribution
- Must be unique if used alone
- Composite key: partition key + sort key
- Sort key allows range queries
- Choose partition key for even distribution

---

## DynamoDB Capacity Modes
- Provisioned: specify read/write capacity units
- On-Demand: pay per request, auto-scales
- Provisioned with Auto Scaling: automatic adjustment
- On-Demand for unpredictable workloads
- Provisioned for steady, predictable traffic

---

## DynamoDB Secondary Indexes
- Global Secondary Index (GSI): different partition key
- Local Secondary Index (LSI): same partition key, different sort key
- Query data using alternative keys
- GSI: up to 20 per table
- LSI: up to 5, must be created at table creation

---

## DynamoDB Advanced Features
- Global Tables: multi-Region, multi-active replication
- DynamoDB Streams: capture item-level changes
- DAX: in-memory caching (microsecond reads)
- TTL: automatic item expiration
- Point-in-time recovery (up to 35 days)

---

## DynamoDB Use Cases
- Web session management
- Gaming leaderboards
- IoT data ingestion
- Shopping carts
- Real-time bidding

---

## Amazon ElastiCache
- Managed in-memory caching
- Redis or Memcached engines
- Microsecond response times
- Reduce database load
- Session storage, leaderboards, real-time analytics

---

## Choosing Between RDS and DynamoDB
- RDS: complex queries, joins, transactions
- DynamoDB: simple access patterns, massive scale
- RDS: predictable schema, SQL skills
- DynamoDB: flexible attributes, key-value access
- Consider access patterns first, not just data model

---

## Database Migration
- AWS Database Migration Service (DMS)
- Migrate to and from AWS
- Supports homogeneous and heterogeneous migrations
- Continuous replication for minimal downtime
- Schema Conversion Tool for engine changes
