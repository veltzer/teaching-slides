---
tags:
  - databases:dynamodb
level: intermediate
category: databases
audience:
  - audiences:developers

---
# Global Tables, Streams, and Operations

---
## What This Chapter Covers

- Global Tables
- Streams
- Triggers
- Backups
- Monitoring

---
## Global Tables

- Multi-region replication
- Active-active writes
- Last-writer-wins
- Local read latency

---
## Conflict Resolution

- Last writer wins by item
- Per-attribute reconciliation possible with version columns
- App-level merge if business needs
- Document the policy

---
## Topology

- All regions writeable
- Add regions over time
- Remove with care
- Watch egress

---
## Streams Overview

- Change feed of writes
- 24-hour window
- Ordered per key
- Fan-out via Kinesis or Lambda

---
## Stream Records

- New image
- Old image
- Both
- Choose by need

---
## Lambda Triggers

- Subscribe to stream
- Process batches
- Idempotent handlers required
- Watch for retries on errors

---
## Trigger Patterns

![lambda_triggers](svg/courses/databases/dynamodb/05_global_and_streams/lambda_triggers.svg)

---
## Use Cases

- Replicate to search index
- Audit trail
- Cross-system sync
- Materialized views

---
## Backups

- On-demand snapshots
- Continuous PITR backups
- Restore to a new table
- Same region only

---
## Cross-Region Restore

- Restore in source region
- Copy via AWS DMS or app code
- Or rely on Global Tables for DR
- Plan ahead

---
## Monitoring

- Consumed capacity
- Throttled requests
- Latency p99
- Item count and table size

---
## Alarms

- Throttling
- Errors
- Latency spikes
- Storage growth

---
## Logging

- DynamoDB metrics in CloudWatch
- API calls in CloudTrail
- Query analyzer for hot patterns
- Pay attention to streams metrics

---
## Security

- IAM policies per table
- Fine-grained per item via leading keys
- Encryption at rest
- VPC endpoints for private access

---
## Common Operational Mistakes

- Global Tables without conflict plan
- Streams retention skipped
- No PITR enabled
- Wide IAM policies
- No throttling alarm
