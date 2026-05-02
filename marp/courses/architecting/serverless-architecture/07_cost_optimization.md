---
tags:
  - architecture:serverless
  - architecture:cost
level: intermediate
category: architecture
audience:
  - audiences:developers
  - audiences:architects

---
# Cost Optimisation

---
## What This Chapter Covers

- Pay-per-use vs always-on
- Cost components
- Right-sizing memory
- Reducing invocations
- Avoiding the "millions of micro-invocations" trap
- Monitoring spend

---
## The Pricing Model

- Lambda: $0.20 per million requests + per-GB-second of execution
- API Gateway: $1-$3.50 per million requests
- DynamoDB: per-read / per-write or provisioned capacity
- S3: per-GB-month + per-request
- Add up across services

---
## Cost Levers

![cost_levers](svg/courses/architecting/serverless-architecture/07_cost_optimization/cost_levers.svg)

---
## When Serverless Is Cheap

- Sporadic workloads (idle most of the time)
- Bursty traffic
- Predictable but low-volume
- Pay nothing during quiet periods
- Most prototypes / startups

---
## When Serverless Is Expensive

- Sustained high volume (a VM runs 24/7 for fixed cost)
- Long-running computations
- Heavy data egress
- Many small invocations stack up
- The cross-over point depends; do the math

---
## Lambda Memory and Cost

- Memory tier sets CPU as well
- More memory = more CPU = faster execution
- Cost per ms drops with more memory (sometimes)
- Sweet spot: lowest cost-per-execution
- Tools: AWS Lambda Power Tuning

---
## AWS Lambda Power Tuning

- Open-source tool
- Runs your function at different memory sizes
- Picks the cheapest / fastest
- Result: data-driven memory choice
- Run after major code changes

---
## Reducing Invocations

- Batch where possible (SQS batches, EventBridge batching)
- Cache results (avoid hot-path invocations)
- Filter at source (don't invoke for irrelevant events)
- Compose: one Lambda doing 10 things vs 10 Lambdas
- Each invocation has fixed overhead

---
## API Gateway Costs

- HTTP API: ~$1 / million
- REST API: ~$3.50 / million
- Switch to HTTP API where features allow
- 3x cost reduction for many APIs
- Often the biggest savings

---
## Data Transfer Costs

- Between regions: $0.01-$0.02 / GB
- Out to internet: $0.05-$0.09 / GB
- Free within a region (mostly)
- Big payloads in serverless: watch the bill
- Compress; cache at the edge

---
## DynamoDB Cost

- On-demand: pay per request
- Provisioned: pay for reserved capacity
- For predictable load: provisioned + auto-scaling
- For spiky: on-demand
- Reserved capacity: 40-50% discount for 1-3 years

---
## ElastiCache / Redis

- 24/7 cost; not pay-per-use
- Big saver if it cuts DB / Lambda calls
- Sized for peak; idle = waste
- Worth it when cache hit ratio is high
- Easy place to overspend

---
## CloudWatch Logs

- Default: every Lambda log goes to CloudWatch
- Storage and ingestion both billed
- A noisy app generates GB of logs per day
- Set retention (default: forever)
- Filter at source; only log what you need

---
## Free Tier

- AWS Lambda: 1M requests + 400K GB-seconds free monthly
- API Gateway: 1M requests / first year
- DynamoDB: 25 GB storage + reads/writes
- For prototypes: virtually free
- Great for learning; doesn't scale

---
## Monitoring Spend

- AWS Cost Explorer: per-service breakdown
- AWS Budgets: alerts at thresholds
- Tag resources by team / project
- Daily review for new deployments
- Surprises happen; alert before they bite

---
## When To Switch Off Serverless

- Sustained 1M+ requests / hour at high CPU
- Traffic is predictable; reservations are cheaper
- Margin is tight; per-request cost matters
- Migration to ECS / Fargate / EKS
- Often: hybrid; serverless for spike, VMs for baseline

---
## Common Cost Mistakes

- REST API when HTTP API would do (3x cost)
- Lambda memory not right-sized
- No log retention &#8594; CloudWatch bill grows forever
- Forgotten dev resources (running for months)
- No tagging &#8594; can't attribute costs

---
## Practical Tips

- Tag everything
- Set budgets and alerts
- Review monthly
- Right-size memory after load tests
- Switch HTTP API where possible
- Prune unused Lambdas / API Gateway routes
