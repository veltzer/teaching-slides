---
tags:
  - concepts:architecture
  - concepts:databases
  - concepts:data-modeling
level: intermediate
category: architecture
audience:
  - audiences:developers
  - audiences:architects

---

# Database Architecture and Design

---

## Agenda

1. Core Database Concepts
1. ACID Properties
1. SQL vs NoSQL Databases
1. Database Types Deep Dive
1. Data Modeling
1. Scalability Patterns
1. High Availability
1. Performance Optimization

---

## Core Database Concepts

- Data persistence
- Data consistency
- Concurrent access
- Data integrity
- Query capabilities
- Transaction management

---

## ACID Properties

![acid_properties](svg/courses/architecting/architecture-patterns/08_database/acid_properties.svg)

---

## Atomicity Example

```sql
BEGIN TRANSACTION;

UPDATE accounts
SET balance = balance - 100
WHERE account_id = 'A';

UPDATE accounts
SET balance = balance + 100
WHERE account_id = 'B';

COMMIT;
```

---

## Isolation Levels

1. Read Uncommitted
1. Read Committed
1. Repeatable Read
1. Serializable

---

## Isolation Problems

![isolation_problems](svg/courses/architecting/architecture-patterns/08_database/isolation_problems.svg)

---

## SQL vs NoSQL

| SQL | NoSQL |
|-----|--------|
| Fixed Schema | Flexible Schema |
| ACID | BASE |
| Vertical Scaling | Horizontal Scaling |
| Complex Joins | Denormalized Data |
| Mature Tools | Modern Tools |

---

## NoSQL Database Types

1. Key-Value Stores
1. Document Databases
1. Column-Family Stores
1. Graph Databases

---

## Key-Value Stores (Redis)

```python
import redis

r = redis.Redis(host='localhost', port=6379)

# Set value
r.set('user:1', 'John Doe')
r.hset('user:1:details', mapping={
    'email': 'john@example.com',
    'age': '30'
})

# Get value
name = r.get('user:1')
details = r.hgetall('user:1:details')
```

---

## Document Store (MongoDB)

```python
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['mydb']

# Insert document
db.users.insert_one({
    'name': 'John Doe',
    'email': 'john@example.com',
    'preferences': {
        'theme': 'dark',
        'notifications': True
    }
})

# Query
user = db.users.find_one({'email': 'john@example.com'})
```

---

## Column-Family Store (Cassandra)

```python
from cassandra.cluster import Cluster

cluster = Cluster(['127.0.0.1'])
session = cluster.connect('mykeyspace')

# Create table
session.execute("""
    CREATE TABLE users (
        user_id uuid PRIMARY KEY,
        name text,
        email text
    )
""")

# Insert data
session.execute("""
    INSERT INTO users (user_id, name, email)
    VALUES (%s, %s, %s)
""", [uuid.uuid4(), 'John Doe', 'john@example.com'])
```

---

## Graph Database (Neo4j)

```python
from neo4j import GraphDatabase

driver = GraphDatabase.driver("neo4j://localhost:7687",
    auth=("neo4j", "password"))

def add_friend(tx, person1, person2):
    tx.run("MERGE (a:Person {name: $name1}) "
           "MERGE (b:Person {name: $name2}) "
           "MERGE (a)-[:FRIENDS_WITH]->(b)",
           name1=person1, name2=person2)

with driver.session() as session:
    session.write_transaction(add_friend, "John", "Jane")
```

---

## Database Schema Design

1. Normalization
1. Denormalization
1. Indexing Strategies
1. Partitioning
1. Sharding

---

## Normalization Example

![normalization_example](svg/courses/architecting/architecture-patterns/08_database/normalization_example.svg)

---

## Index Types

1. B-Tree
1. Hash
1. Bitmap
1. GiST
1. Full-Text

---

## Index Creation Example

```sql
-- B-Tree index
CREATE INDEX idx_users_email
ON users(email);

-- Composite index
CREATE INDEX idx_users_name_email
ON users(name, email);

-- Partial index
CREATE INDEX idx_active_users
ON users(email)
WHERE status = 'active';

-- Full-text search index
CREATE INDEX idx_users_full_text
ON users USING GIN (to_tsvector('english', description));
```

---

## Partitioning Strategies

1. Range Partitioning
1. List Partitioning
1. Hash Partitioning
1. Composite Partitioning

---

## Range Partitioning Example

```sql
CREATE TABLE orders (
    order_id int,
    order_date date,
    amount decimal
) PARTITION BY RANGE (order_date);

CREATE TABLE orders_2023
PARTITION OF orders
FOR VALUES FROM ('2023-01-01') TO ('2024-01-01');

CREATE TABLE orders_2024
PARTITION OF orders
FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');
```

---

## Sharding Architecture

![sharding_architecture](svg/courses/architecting/architecture-patterns/08_database/sharding_architecture.svg)

---

## Sharding Implementation

```python
def get_shard(key):
    shard_count = 3
    shard_id = hash(key) % shard_count
    return f"shard_{shard_id}"

def store_data(key, value):
    shard = get_shard(key)
    connection = get_connection(shard)
    connection.execute(
        "INSERT INTO data (key, value) VALUES (?, ?)",
        [key, value]
    )
```

---

## Sharded Architecture Pattern

- Horizontally partitions data across multiple databases or "shards"
- Each shard contains a subset of the data, determined by a shard key
- Improves scalability and performance for large-scale distributed databases
- Allows for parallel processing of queries across multiple shards
- Enables handling of larger datasets than can fit on a single server

---

## Sharded Architecture Diagram

![sharded_architecture_diagram](svg/courses/architecting/architecture-patterns/08_database/sharded_architecture_diagram.svg)

---

## Sharded Pros and Cons

Pros:
- Improves scalability for large datasets
- Enhances query performance through parallelization
- Allows for better resource utilization
- Provides fault isolation (issues in one shard don't affect others)
- Enables geographic distribution of data

Cons:
- Increases complexity in data management and application logic
- Can lead to data distribution skew if shard key is poorly chosen
- Makes it challenging to perform queries across multiple shards
- Complicates data consistency and transaction management
- Can make resharding (rebalancing data across shards) difficult

---

## Sharded When to Use

- When dealing with very large datasets that exceed single server capacity
- In systems requiring high throughput for read and write operations
- When you need to scale out database resources horizontally
- For applications with clear data partitioning strategies
- In scenarios where data can be naturally segmented (e.g., by customer, region, or time)
- When you need to improve performance by reducing contention and increasing cache efficiency

---

## Data Mesh Architecture

- Decentralized approach to data ownership and architecture
- Treats data as a product owned by domain teams
- Each domain manages its own data pipelines and storage
- Enables fine-grained control over data access and quality
- Removes central data team as a bottleneck

---

## Data Mesh Architecture Diagram

![mesh_architecture_diagram](svg/courses/architecting/architecture-patterns/08_database/mesh_architecture_diagram.svg)

---

## Data Mesh Pros and Cons

Pros:
- Improves scalability of data ownership across many domains
- Enhances data quality by aligning ownership with domain expertise
- Provides consistent governance policies across domains
- Enables independent evolution of domain data models
- Reduces bottlenecks of centralized data teams

Cons:
- Increases overall organizational complexity
- Requires mature platform tooling for self-service
- May have a steep learning curve for teams
- Can lead to inconsistent practices without strong platform guardrails
- Can be overkill for smaller organizations

---

## Data Mesh When to Use

- In large organizations with many independent product domains
- When central data teams have become a delivery bottleneck
- For systems requiring domain-aligned data ownership
- When implementing consistent data governance is crucial
- In environments where self-service data platforms are mature
- For gradual decentralization of data architecture

---

## High Availability

1. Replication
1. Failover
1. Load Balancing
1. Backup Strategies

---

## Replication Types

![replication_types](svg/courses/architecting/architecture-patterns/08_database/replication_types.svg)

---

## Replication Configuration

```yaml
replication:
  oplogSizeMB: 10240
  replSetName: "rs0"
  enableMajorityReadConcern: true

members:
  - host: "primary:27017"
    priority: 2
  - host: "secondary1:27017"
    priority: 1
  - host: "secondary2:27017"
    priority: 1
```

---

## Backup Strategies

1. Full Backup
1. Incremental Backup
1. Differential Backup
1. Point-in-Time Recovery

---

## Backup Implementation

```python
def backup_database():
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    # Full backup
    subprocess.run([
        'pg_dump',
        '-h', 'localhost',
        '-U', 'postgres',
        '-d', 'mydb',
        '-f', f'backup_{timestamp}.sql'
    ])

    # Compress
    subprocess.run([
        'gzip',
        f'backup_{timestamp}.sql'
    ])
```

---

## Performance Optimization

1. Query Optimization
1. Index Optimization
1. Connection Pooling
1. Caching Strategies
1. Resource Management

---

## Query Optimization Example

```sql
-- Before optimization
SELECT * FROM orders
WHERE status = 'pending'
AND created_at > '2024-01-01';

-- After optimization
CREATE INDEX idx_orders_status_date
ON orders(status, created_at);

SELECT order_id, status, amount
FROM orders
WHERE status = 'pending'
AND created_at > '2024-01-01';
```

---

## Connection Pooling

```python
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    'postgresql://user:pass@localhost/db',
    poolclass=QueuePool,
    pool_size=20,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800
)
```

---

## Caching Patterns

![caching_patterns](svg/courses/architecting/architecture-patterns/08_database/caching_patterns.svg)

---

## Cache Implementation

```python
from functools import lru_cache
import redis

redis_client = redis.Redis()

@lru_cache(maxsize=1000)
def get_user(user_id):
    # Try redis first
    user = redis_client.get(f'user:{user_id}')
    if user:
        return json.loads(user)

    # Fallback to database
    user = db.query("SELECT * FROM users WHERE id = %s", (user_id,))
    redis_client.setex(f'user:{user_id}', 3600, json.dumps(user))
    return user
```

---

## Monitoring and Metrics

1. Query Performance
1. Connection Stats
1. Cache Hit Ratio
1. Resource Usage
1. Error Rates

---

## Monitoring Dashboard

![monitoring_dashboard](svg/courses/architecting/architecture-patterns/08_database/monitoring_dashboard.svg)

---

## Security Best Practices

1. Access Control
1. Encryption
1. Audit Logging
1. Network Security
1. Backup Security

---

## Security Implementation

```sql
-- User management
CREATE ROLE readonly WITH
    LOGIN
    PASSWORD 'secure_password'
    CONNECTION LIMIT 10
    VALID UNTIL '2025-01-01';

GRANT SELECT ON ALL TABLES IN SCHEMA public TO readonly;

-- Encryption
ALTER SYSTEM SET ssl = on;
ALTER SYSTEM SET ssl_cert_file = 'server.crt';
ALTER SYSTEM SET ssl_key_file = 'server.key';
```

---

## Data Migration Strategies

1. Big Bang Migration
1. Incremental Migration
1. Zero-Downtime Migration
1. Reversible Migration

---

## Migration Example

```python
def migrate_data():
    # Create new schema
    execute_ddl("new_schema.sql")

    # Migrate in batches
    last_id = 0
    batch_size = 1000

    while True:
        # Get batch
        records = get_batch(last_id, batch_size)
        if not records:
            break

        # Transform and load
        transform_and_load(records)
        last_id = records[-1].id

        # Verify
        verify_migration(records)
```

---

## Modern Database Trends

1. NewSQL Databases
1. Serverless Databases
1. Edge Databases
1. AI Integration
1. Time-Series Optimization

---

## Best Practices

1. Use Connection Pooling
1. Implement Caching
1. Regular Maintenance
1. Monitor Performance
1. Plan for Scale
1. Secure Access
1. Regular Backups
