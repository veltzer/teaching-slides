---
tags:
  - architecture:serverless
  - architecture:state
level: intermediate
category: architecture
audience:
  - audiences:developers

---
# State Management

---
## What This Chapter Covers

- Serverless functions are stateless
- Where state lives
- Database options
- Caching with ElastiCache / Redis
- Sessions and JWTs
- File state (S3)
- Common patterns

---
## Stateless By Design

- Each invocation is independent
- Container may not be the same as last time
- Local memory: not durable
- Local disk: ephemeral, small
- Don't rely on either for state

---
## Where State Lives

- Database (DynamoDB, RDS, MongoDB Atlas)
- Object storage (S3) for blobs
- Cache (Redis, Memcached)
- Message queues (SQS) for in-flight state
- Config (Parameter Store, Secrets Manager)

---
## DynamoDB With Lambda

- Serverless DB; scales to zero (per-request pricing)
- Single-digit ms latency
- Eventually consistent reads (or strongly consistent)
- Common pairing for Lambda
- Limitations: query model, no joins

---
## RDS With Lambda

- Traditional relational DB
- Connection pooling: tricky (Lambda instances burst)
- RDS Proxy: connection pooling for Lambda
- Cold starts + RDS connect: latency adds up
- Often: RDS Aurora Serverless instead

---
## RDS Proxy

- AWS managed connection pooler
- Lambda &#8594; Proxy &#8594; RDS
- Proxy holds connections to RDS
- Solves the "thousands of Lambdas, RDS connection limit" problem
- Adds cost; required at scale

---
## Aurora Serverless

- MySQL / Postgres compatible
- Scales capacity automatically
- v2 supports near-zero idle costs
- Better fit for serverless than provisioned RDS
- Paying for capacity, not connections

---
## ElastiCache / Redis

- Managed Redis
- For: session state, caching, leaderboards
- Lambda connects, queries, returns
- Cost: 24/7 instance (not serverless)
- Acceptable when used heavily

---
## Sessions

- Don't store session in Lambda memory (won't persist)
- DynamoDB with TTL: standard pattern
- ElastiCache for fast access
- JWT in cookies: stateless; no DB lookup
- Pick by: how much state, how often accessed

---
## JWTs As State

- Encode user state in the token
- No DB lookup per request
- Best for: auth, simple state
- Limit: token size; not for big data
- Sign with a server key; verify on each request

---
## File State (S3)

- For documents, images, blobs
- Lambda reads from / writes to S3
- Pre-signed URLs for upload
- S3 events trigger downstream Lambdas
- The standard pattern for file workflows

---
## Step Functions As State

- Step Functions tracks workflow state
- Multi-step processes; long-running
- State accessible to each step
- No need to store in DB
- Limit: state size (256 KB typical)

---
## In-Memory Caching

- Cache outside the handler (in init code)
- Persists across warm invocations on same container
- Doesn't survive cold start or container churn
- Useful for: config, rarely-changing data
- Periodically invalidate

---
## Distributed State

- Shared state between Lambdas: needs external store
- DynamoDB locks for distributed mutexes
- ElastiCache for fast shared counters
- Consensus (etcd) usually overkill for serverless
- Match the store to the access pattern

---
## Common State Mistakes

- Local files / globals expected to persist
- RDS with no connection pooling under burst load
- Caching that doesn't survive deploys
- Forgetting TTLs on session stores
- Storing PII in JWTs without encryption

---
## A Decision Tree

- Per-user, short-lived &#8594; JWT or DynamoDB
- Shared, fast &#8594; ElastiCache
- Big files &#8594; S3
- Complex queries &#8594; RDS / Aurora
- Workflow state &#8594; Step Functions
- Each pattern has its place
