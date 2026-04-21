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

## Database Models Comparison

![database_models_comparison](svg/courses/cloud/introduction-to-aws/06_database_services/database_models_comparison.svg)

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

## Aurora Architecture: Details
- Shared distributed storage layer
- 6 copies of data across 3 AZs
- Self-healing storage
- Continuous backup to S3
- Up to 15 read replicas with low lag

---

## Aurora Architecture

![aurora_architecture](svg/courses/cloud/introduction-to-aws/06_database_services/aurora_architecture.svg)

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

## RDS Multi-AZ Failover

![rds_multi_az_failover](svg/courses/cloud/introduction-to-aws/06_database_services/rds_multi_az_failover.svg)

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

## Create an RDS Instance

```bash
aws rds create-db-instance \
  --db-instance-identifier my-postgres \
  --db-instance-class db.t3.medium \
  --engine postgres \
  --master-username admin \
  --master-user-password 'SecurePass123!' \
  --allocated-storage 20 \
  --multi-az \
  --storage-encrypted
```

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

## DynamoDB CLI Example

```bash
# Create a table
aws dynamodb create-table \
  --table-name Users \
  --attribute-definitions \
    AttributeName=UserId,AttributeType=S \
  --key-schema \
    AttributeName=UserId,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST

# Put an item
aws dynamodb put-item \
  --table-name Users \
  --item '{"UserId":{"S":"u001"},"Name":{"S":"Alice"}}'
```

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
