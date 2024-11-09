# Database Architecture and Design
## Modern Architecture Course

---

## Agenda

1. Core Database Concepts
2. ACID Properties
3. SQL vs NoSQL Databases
4. Database Types Deep Dive
5. Data Modeling
6. Scalability Patterns
7. High Availability
8. Performance Optimization

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

![0](../../../out/mermaid/marp/courses/architecting/XX_database.md/0.png)

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
2. Read Committed
3. Repeatable Read
4. Serializable

---

## Isolation Problems

![1](../../../out/mermaid/marp/courses/architecting/XX_database.md/1.png)

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
2. Document Databases
3. Column-Family Stores
4. Graph Databases

---

## Key-Value Stores (Redis)

```python
import redis

r = redis.Redis(host='localhost', port=6379)

## Set value
r.set('user:1', 'John Doe')
r.hset('user:1:details', mapping={
    'email': 'john@example.com',
    'age': '30'
})

## Get value
name = r.get('user:1')
details = r.hgetall('user:1:details')
```

---

## Document Store (MongoDB)

```python
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['mydb']

## Insert document
db.users.insert_one({
    'name': 'John Doe',
    'email': 'john@example.com',
    'preferences': {
        'theme': 'dark',
        'notifications': True
    }
})

## Query
user = db.users.find_one({'email': 'john@example.com'})
```

---

## Column-Family Store (Cassandra)

```python
from cassandra.cluster import Cluster

cluster = Cluster(['127.0.0.1'])
session = cluster.connect('mykeyspace')

## Create table
session.execute("""
    CREATE TABLE users (
        user_id uuid PRIMARY KEY,
        name text,
        email text
    )
"""")

## Insert data
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
2. Denormalization
3. Indexing Strategies
4. Partitioning
5. Sharding

---

## Normalization Example

![2](../../../out/mermaid/marp/courses/architecting/XX_database.md/2.png)

---

## Index Types

1. B-Tree
2. Hash
3. Bitmap
4. GiST
5. Full-Text

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
2. List Partitioning
3. Hash Partitioning
4. Composite Partitioning

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

![3](../../../out/mermaid/marp/courses/architecting/XX_database.md/3.png)

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

## High Availability

1. Replication
2. Failover
3. Load Balancing
4. Backup Strategies

---

## Replication Types

![4](../../../out/mermaid/marp/courses/architecting/XX_database.md/4.png)

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
2. Incremental Backup
3. Differential Backup
4. Point-in-Time Recovery

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
2. Index Optimization
3. Connection Pooling
4. Caching Strategies
5. Resource Management

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

![5](../../../out/mermaid/marp/courses/architecting/XX_database.md/5.png)

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
    user = db.query(f"SELECT * FROM users WHERE id = {user_id}")
    redis_client.setex(f'user:{user_id}', 3600, json.dumps(user))
    return user
```

---

## Monitoring and Metrics

1. Query Performance
2. Connection Stats
3. Cache Hit Ratio
4. Resource Usage
5. Error Rates

---

## Monitoring Dashboard

![6](../../../out/mermaid/marp/courses/architecting/XX_database.md/6.png)

---

## Security Best Practices

1. Access Control
2. Encryption
3. Audit Logging
4. Network Security
5. Backup Security

---

## Security Implementation

```python
# User management
CREATE ROLE readonly WITH 
    LOGIN 
    PASSWORD 'secure_password'
    CONNECTION LIMIT 10
    VALID UNTIL '2025-01-01';

GRANT SELECT ON ALL TABLES IN SCHEMA public TO readonly;

# Encryption
ALTER SYSTEM SET ssl = on;
ALTER SYSTEM SET ssl_cert_file = 'server.crt';
ALTER SYSTEM SET ssl_key_file = 'server.key';
```

---

## Data Migration Strategies

1. Big Bang Migration
2. Incremental Migration
3. Zero-Downtime Migration
4. Reversible Migration

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
2. Serverless Databases
3. Edge Databases
4. AI Integration
5. Time-Series Optimization

---

## Best Practices

1. Use Connection Pooling
2. Implement Caching
3. Regular Maintenance
4. Monitor Performance
5. Plan for Scale
6. Secure Access
7. Regular Backups
