---
tags:
  - databases:dynamodb
level: intermediate
category: databases
audience:
  - audiences:developers

---
# Operations and Querying

---
## What This Chapter Covers

- Item operations
- Query and scan
- Conditions
- Transactions
- Batch operations

---
## Get Operation

- Read by primary key
- Strongly or eventually consistent
- Single item only
- Cheapest read

---
## Put Operation

- Insert or replace
- Conditional support
- Unique-key enforcement via condition
- Returns old item optionally

---
## Update Operation

- Modify in place
- Atomic at item level
- Conditions allow optimistic locking
- Increment, append, set

---
## Delete Operation

- By primary key
- Conditional too
- Returns old item
- Triggers a stream event

---
## Query

- By partition key
- Optionally bounded by sort key
- Returns up to 1MB per call
- Pagination via tokens

---
## Scan

- Reads whole table
- Expensive
- Avoid in production
- Filter is server-side but post-read

---
## Conditional Writes

- Optimistic concurrency
- Attribute-not-exists for unique inserts
- Attribute-exists for updates
- Compare to versions

---
## Transactions

- Transactional read and write APIs
- Across items in same region
- ACID at item level
- Twice the cost of normal ops

---
## Batch Operations

- Bulk read and write APIs
- Up to 25 items per call
- Partial failures possible
- Retry unprocessed

---
## Pagination

- Last evaluated key returned
- Pass back as exclusive start key
- Loop until none
- Watch for hot pagination

---
## Filter Expressions

- Applied after read
- Do not save read units
- Useful for simple post-filters
- Prefer schema design over filters

---
## Projection

- Limit attributes returned
- Reduces network bytes
- Saves cost on large items
- Set per query or index

---
## TTL

- Background sweep deletes expired items
- Hours of imprecision
- Low cost
- Use for sessions, carts, caches

---
## Common Operation Mistakes

- Scan in hot paths
- Filter expressions instead of index design
- Batch without retry on unprocessed
- No conditional checks
- Transactions for non-critical writes
