---
tags:
  - data-and-ai:big-data
level: beginner
category: data-driven
audience:
  - audiences:managers

---
# Big Data

---
## What This Chapter Covers

- What "big" means, in practice
- The Five V's (and why most companies don't have a "big data" problem)
- NoSQL and when to use it
- Hadoop, Spark, and the modern stack
- Data lakes, data buckets, data lakehouses
- Cloud-native big-data analytics

---
## What "Big" Means

- Big enough that traditional databases struggle
- Real number: TB-to-PB scale, billions of rows, high write rates
- Most companies *think* they have big data
- Most actually have Excel-sized data dressed up in cloud infrastructure
- 1 TB fits on a thumb drive; you may not need a Hadoop cluster

---
## The Five V's

- **Volume**: how much
- **Velocity**: how fast it arrives
- **Variety**: how many different shapes
- **Veracity**: how clean it is
- **Value**: what business outcome it enables
- "Big data" is a problem only when one or more V is genuinely extreme

---
## Honest Self-Assessment

- Is your data > 1 TB? Probably not
- Is it arriving > 10K events/second? Probably not
- Is it many varied shapes you can't normalise? Maybe
- If two V's are extreme, you may need big-data tools
- If none are extreme, a regular DB or warehouse will do

---
## NoSQL

- Databases that *don't* enforce SQL's relational model
- Four families:
    - **Key-value**: Redis, DynamoDB
    - **Document**: MongoDB, Couchbase
    - **Wide-column**: Cassandra, ScyllaDB
    - **Graph**: Neo4j, Amazon Neptune
- Each shines on a different access pattern

---
## When NoSQL

- Massive scale-out write workloads (Cassandra)
- Variable schema; user-generated documents (MongoDB)
- Sub-millisecond reads at any scale (Redis)
- Highly connected data; relationship traversal (Neo4j)
- Most apps still want a SQL DB; NoSQL serves specific needs

---
## Hadoop

- Original "big data" platform, born at Yahoo (2006)
- HDFS: distributed filesystem
- MapReduce: batch processing model
- YARN: resource scheduler
- Mostly being replaced by cloud-native alternatives
- Still common in on-prem enterprise; rarely the *first* choice now

---
## Spark

- The dominant batch + streaming engine today
- 10-100x faster than MapReduce for many workloads
- Runs on YARN, Kubernetes, or standalone
- APIs in Scala, Python, R, SQL
- Used at Netflix, Uber, Spotify, almost every big-data org

---
## What Spark Does

- Read data from anywhere (HDFS, S3, Kafka, JDBC, ...)
- Transform with SQL or DataFrame APIs
- Run distributed across many nodes
- Write back, or feed into ML models, or push to dashboards
- The Swiss Army knife of large-scale data processing

---
## Data Lakes

- Cheap storage of *raw*, often unstructured data
- Object storage: S3, GCS, Azure Blob
- Schema applied at *read time*, not *write time*
- Cheap to land, expensive to query (without good indexing)
- Foundation for modern analytics

---
## Lakehouses

- Lake (cheap storage) + Warehouse (fast queries) in one platform
- Tools: Databricks, Iceberg + Trino, Snowflake's iceberg integration
- Open table formats: Delta Lake, Apache Iceberg, Hudi
- Best of both worlds, in many cases
- The current "modern data stack" centre of gravity

---
## Cloud Big-Data Services

- **AWS**: S3 + Athena (SQL on S3), Redshift, EMR
- **GCP**: Cloud Storage + BigQuery (serverless warehouse), Dataproc
- **Azure**: ADLS + Synapse + Databricks
- Pay per query / per TB scanned — costs can balloon
- Set quotas and alerts before turning data scientists loose

---
## BigQuery, Specifically

- Google's serverless warehouse
- Pay per byte scanned
- Petabyte queries in seconds
- No server management
- Easy to overspend if your team isn't trained on partitioning and clustering

---
## Streaming vs Batch

- **Batch**: process today's data tomorrow morning
- **Streaming**: process as data arrives
- Streaming is harder, more expensive, often unnecessary
- Tools: Kafka + Spark Streaming, Flink, Kinesis
- "Real-time" requirements are often "fresh enough" requirements

---
## When Big Data Is Worth It

- Genuine scale that makes regular DBs unworkable
- Diverse sources you can't normalise upfront
- Streaming use cases with real time-sensitive decisions
- ML training over historical data
- Otherwise: a postgres + a warehouse + good ETL is plenty

---
## When It's Not

- Your data fits on one big server
- Daily batch is fine for your use case
- You have one team and you'd be burning their time on infra
- Cost is high; capability beyond your team's skill
- Premature scale is one of the most expensive mistakes

---
## Common Mistakes

- "We need a data lake" — before knowing what would land in it
- Spinning up Spark for jobs that fit in pandas
- Underestimating cloud query costs
- Treating big data as an end goal, not a tool for an end goal
- Hiring big-data talent before having big-data problems
