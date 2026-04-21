---
tags:
  - infrastructure:cloud
  - infrastructure:databases
  - concepts:architecture
level: intermediate
category: cloud
audience:
  - audiences:developers
  - audiences:architects
  - audiences:devops

---
# Data Storage in the Cloud

---

## Relational vs NoSQL
- Relational: structured data, ACID, SQL, joins
- NoSQL: flexible schema, eventual consistency, scale-out
- Not a binary choice: use both where appropriate
- Relational for transactions and complex queries
- NoSQL for high throughput and simple access patterns

---

## When to Choose Relational
- Complex queries with joins
- ACID transactions (banking, inventory)
- Well-defined, stable schema
- Reporting and analytics on structured data
- Mature tooling and wide expertise

---

## When to Choose NoSQL
- Massive scale (millions of operations/second)
- Flexible or evolving schema
- Simple access patterns (key-value, document)
- Low latency at any scale
- Geographic distribution

---

## Managed Relational Databases
- AWS RDS, Azure SQL, Cloud SQL
- Provider manages patching, backups, failover
- Multi-AZ for high availability
- Read replicas for scaling reads
- Choose engine: MySQL, PostgreSQL, SQL Server, etc.

---

## Amazon Aurora
- AWS-built relational database
- MySQL and PostgreSQL compatible
- 3-5x faster than standard engines
- Auto-scaling storage up to 128 TB
- Up to 15 read replicas with millisecond lag

---

## Aurora Architecture: Details
- Shared distributed storage layer
- 6 copies of data across 3 AZs
- Self-healing: automatically repairs corruption
- Continuous backup to S3
- Designed for cloud from the ground up

---

## Aurora Architecture

![aurora](svg/courses/cloud/architecting-in-the-cloud/10_data_storage/aurora_architecture.svg)

---

## Aurora Serverless
- Auto-scales compute up and down
- Scales to zero (v2 scales to minimum)
- Pay per ACU-second (Aurora Capacity Unit)
- Great for variable and unpredictable workloads
- No instance management

---

## Managed NoSQL Databases
- AWS DynamoDB, Azure Cosmos DB, Google Firestore
- Fully managed, serverless
- Single-digit millisecond latency
- Automatic scaling
- Global distribution options

---

## DynamoDB Architecture
- Partitioned across many storage nodes
- Partition key determines data placement
- Consistent performance at any scale
- On-Demand or Provisioned capacity
- Global Tables for multi-Region replication

---

## DynamoDB Put and Query

```bash
# Put an item
aws dynamodb put-item --table-name Orders \
  --item '{
    "orderId": {"S": "O-1001"},
    "customerId": {"S": "C-42"},
    "total": {"N": "149.99"},
    "status": {"S": "pending"}
  }'

# Query by partition key
aws dynamodb query --table-name Orders \
  --key-condition-expression "customerId = :cid" \
  --expression-attribute-values '{":cid":{"S":"C-42"}}'
```

---

## Cosmos DB Overview
- Microsoft's globally distributed NoSQL
- Multiple APIs: SQL, MongoDB, Cassandra, Gremlin, Table
- Tunable consistency levels (5 options)
- Global distribution with multi-region writes
- Comprehensive SLAs (latency, throughput, availability)

---

## Rolling Databases on Your Own
- Run MySQL, PostgreSQL, MongoDB on EC2/VMs
- Full control over configuration and version
- Full operational burden (patches, backups, failover)
- Only if managed service doesn't meet requirements
- Consider: is the control worth the operations cost?

---

## When to Self-Manage
- Need a specific database version or extension
- Very custom configuration requirements
- License restrictions on managed services
- Cost optimization at very large scale
- Most teams should use managed services

---

## Caching in the Cloud
- ElastiCache (Redis, Memcached), Azure Cache, Memorystore
- In-memory data store for microsecond latency
- Reduce database load
- Session storage
- Real-time leaderboards and counters

---

## Caching Patterns
- Cache-Aside: application checks cache, then database
- Write-Through: write to cache and database simultaneously
- Write-Behind: write to cache, async write to database
- TTL-based expiration
- Cache invalidation is the hardest problem

---

## When to Cache
- Read-heavy workloads (90%+ reads)
- Data that doesn't change frequently
- Expensive database queries
- Session data
- API response caching

---

## Graph Databases
- Model relationships between entities
- Amazon Neptune, Azure Cosmos DB (Gremlin), Neo4j
- Social networks, recommendation engines, fraud detection
- Traverse relationships efficiently
- Not for general-purpose storage

---

## Time Series Databases
- Optimized for time-stamped data
- Amazon Timestream, InfluxDB, TimescaleDB
- IoT sensor data, metrics, financial data
- Efficient compression and querying
- Retention policies for aging data

---

## Data Warehouses
- Optimized for analytical queries
- Amazon Redshift, Azure Synapse, Google BigQuery
- Columnar storage for fast aggregations
- Separate from OLTP databases
- ETL or ELT to load data

---

## Database Encryption
- Encryption at rest: enable for all databases
- KMS-managed keys or customer-managed keys
- Encryption in transit: SSL/TLS connections
- Transparent to applications
- Some engines require encryption at creation time

---

## Database Monitoring
- CloudWatch metrics: CPU, connections, IOPS, free storage
- Performance Insights: SQL-level performance analysis
- Slow query logs
- Set alarms on critical thresholds
- Monitor replication lag for read replicas

---

## Database Backup Strategy
- Automated daily snapshots (RDS)
- Point-in-time recovery (to any second in retention period)
- Manual snapshots for major changes
- Cross-Region copies for DR
- Test restoration regularly

---

## Database Migration
- AWS DMS (Database Migration Service)
- Azure Database Migration Service
- Homogeneous: same engine (MySQL -> MySQL)
- Heterogeneous: different engines (Oracle -> PostgreSQL)
- Continuous replication for minimal downtime

---

## Multi-Model Databases
- Azure Cosmos DB: document, key-value, graph, column-family
- Amazon DynamoDB: key-value and document
- Single database, multiple access patterns
- Reduces number of databases to manage
- Trade-off: jack of all trades, master of none

---

## Data Storage Decision Framework
1. What is the data model? (relational, key-value, document, graph)
1. What are the access patterns? (complex queries vs simple lookups)
1. What scale is needed? (thousands vs millions of operations)
1. What consistency is required? (strong vs eventual)
1. What is the budget? (managed vs self-hosted)

---

## Database Decision Framework

![decision](svg/courses/cloud/architecting-in-the-cloud/10_data_storage/database_decision_framework.svg)

---

## Connection Pooling
- Database connections are expensive to create
- Connection pools reuse connections
- RDS Proxy: managed connection pooling for AWS
- Especially important for serverless (many short-lived connections)
- Configure pool size based on database limits

---

## RDS Proxy in Terraform

```hcl
resource "aws_db_proxy" "app" {
  name          = "app-proxy"
  engine_family = "POSTGRESQL"
  role_arn      = aws_iam_role.proxy.arn
  vpc_subnet_ids = [
    aws_subnet.private_a.id,
    aws_subnet.private_b.id,
  ]
  auth {
    auth_scheme = "SECRETS"
    iam_auth    = "REQUIRED"
    secret_arn  = aws_secretsmanager_secret.db.arn
  }
}
```

---

## Read/Write Splitting: Details
- Write to primary database
- Read from read replicas
- Application or proxy routes queries
- Scale reads independently from writes
- Eventual consistency for reads (replication lag)

---

## Read/Write Splitting

![rw_split](svg/courses/cloud/architecting-in-the-cloud/10_data_storage/read_write_splitting.svg)

---

## Database Sharding
- Split data across multiple database instances
- Each shard holds a subset of data
- Enables horizontal write scaling
- Complex: shard key selection, cross-shard queries
- Consider DynamoDB/Cosmos DB before manual sharding

---

## Data Storage Best Practices
- Use managed services by default
- Choose the right database for the access pattern
- Implement caching for read-heavy workloads
- Plan for multi-AZ from the start
- Automate backups and test restoration
- Monitor database performance metrics
