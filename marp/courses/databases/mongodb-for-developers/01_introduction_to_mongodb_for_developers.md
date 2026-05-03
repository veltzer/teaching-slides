---
tags:
  - databases:mongodb
level: intermediate
category: databases
audience:
  - audiences:developers

---
# Introduction to MongoDB for Developers

---
## What This Chapter Covers

- What MongoDB is
- Document model
- When to choose it
- The ecosystem
- A short history

---
## What MongoDB Is

- A document-oriented NoSQL database
- Stores BSON (binary JSON)
- Schemaless by default; schema-validated optionally
- Strong horizontal scaling
- Most-deployed document DB

---
## When MongoDB Shines

![mongo_strengths](svg/courses/databases/mongodb-for-developers/01_introduction_to_mongodb_for_developers/mongo_strengths.svg)

---
## Document Model

- A document = JSON-ish object
- Nested fields, arrays, references
- Collections of documents (like tables of rows)
- No fixed schema per collection

---
## When MongoDB Wins

- Hierarchical / nested data
- Schema flexibility
- Read-heavy with embedded relationships
- Geospatial queries
- Quick prototyping with evolving schema

---
## When MongoDB Loses

- Heavy transactional workload (ACID across collections)
- Many-to-many with complex joins
- Reporting / analytics requiring SQL
- When you actually want a schema

---
## The Ecosystem

- MongoDB Atlas: hosted
- Community Server: free, self-hosted
- Compass: GUI client
- mongosh: shell
- Drivers for every major language

---
## Versions

- 6.x and 7.x are current LTS branches
- Major changes per release
- Backward compatibility usually maintained
- Run a recent version

---
## A Sample Document

```json
{
  "_id": ObjectId("..."),
  "name": "Alice",
  "email": "alice@example.com",
  "addresses": [
    {"type": "home", "city": "Boston"},
    {"type": "work", "city": "NYC"}
  ]
}
```

- Nested data inline
- No SQL joins to compose

---
## Key Concepts

- Database &#8594; Collection &#8594; Document
- Field: a single key-value pair
- _id: every document has one
- ObjectId: the default _id type

---
## Document Versus Relational

![document_vs_relational](svg/courses/databases/mongodb-for-developers/01_introduction_to_mongodb_for_developers/document_vs_relational.svg)

---
## SQL Comparison

- Database = Database
- Table = Collection
- Row = Document
- Column = Field
- JOIN = $lookup (or denormalise)

---
## Common Misconceptions

- "Schemaless = no schema" — your app has one; just unenforced
- "Web scale" — yes, but only with sharding
- "JSON storage" — BSON; not 100% identical
- "No transactions" — wrong since 4.0; ACID across collections

---
## What's Next

- Tools and dev environment
- Schema design
- Drivers and connections
- CRUD, queries, aggregations
- Indexing, transactions, change streams
- Validation, security, performance
