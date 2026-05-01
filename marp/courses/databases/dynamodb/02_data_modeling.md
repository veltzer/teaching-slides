---
tags:
  - databases:dynamodb
level: intermediate
category: databases
audience:
  - audiences:developers

---
# Data Modeling

---
## What This Chapter Covers

- Single-table design
- Partition and sort keys
- Indexes
- Item collections
- Patterns

---
## Single-Table Design

- One table per service
- Many entity types in it
- Common access patterns served by one query
- Cost-efficient

---
## Why Single Table

- Fewer requests per page
- Cheaper at scale
- Less ops overhead
- More design upfront

---
## Partition Key

- Routes item to physical partition
- High cardinality required
- Hot keys hurt
- Often combines entity type and id

---
## Sort Key

- Within a partition
- Defines order
- Enables range queries
- Common for time-ordered data

---
## Composite Keys

- Partition and sort key together
- Unique constraint per pair
- Allows hierarchical access
- Foundation of most designs

---
## Item Collections

- All items sharing partition key
- Queryable as a group
- Mix entity types in one collection
- Power of single-table

---
## GSI

- Global secondary index
- Different partition and sort key
- Eventually consistent
- Adds capacity and storage cost

---
## LSI

- Local secondary index
- Same partition key, different sort
- Strongly consistent
- Defined at table create only

---
## Sparse Indexes

- Only items with the index attribute
- Saves cost
- Useful for "active" subsets
- Common pattern

---
## Access Patterns First

- List queries up front
- Each pattern maps to one query
- Iterate model until all served
- Only then write code

---
## Overloading Attributes

- Generic SK like "DETAIL" or "USER#123"
- Filter by attribute prefix
- Saves indexes
- Increases cognitive load

---
## Document Attributes

- JSON-like Map and List types
- Up to 400KB per item
- Editable in place
- Watch payload size

---
## Common Modeling Mistakes

- Many tables instead of single-table
- Querying by Scan
- Hot partition keys
- Strongly consistent reads everywhere
- No design for new access patterns
