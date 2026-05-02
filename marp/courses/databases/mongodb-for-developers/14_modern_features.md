---
tags:
  - databases:mongodb
  - databases:modern
level: intermediate
category: databases
audience:
  - audiences:developers

---
# Modern Features

---
## What This Chapter Covers

- Time-series collections
- Atlas Search
- Vector search
- Queryable encryption
- Atlas Triggers
- The roadmap

---
## Time-Series Collections

- MongoDB 5+
- Optimised storage for time-series data
- Compressed; smaller; faster
- Native support for: granularity, expireAfter

---
## Recent Features

![recent_features](svg/courses/databases/mongodb-for-developers/14_modern_features/recent_features.svg)

---
## Time-Series Example

```javascript
db.createCollection("metrics", {
    timeseries: {
        timeField: "ts",
        metaField: "device_id",
        granularity: "minutes"
    },
    expireAfterSeconds: 86400 * 30
});
```

- 30-day retention; minute-granularity buckets

---
## Atlas Search

- Full-text search built into Atlas
- Backed by Lucene
- Faceting, fuzzy, relevance
- Aggregation pipeline integration
- "Mongo + Elasticsearch" in one

---
## Atlas Search Indexes

- Define field mappings
- Per-collection
- Standard text + autocomplete + numeric
- Updated near-real-time

---
## Vector Search

- Embed documents into vectors
- Search by similarity
- Useful: semantic search, recommendations, RAG
- Atlas + MongoDB 6.0.4+

---
## Vector Search Example

```javascript
db.docs.aggregate([{
    $vectorSearch: {
        queryVector: [0.1, 0.2, ...],
        path: "embedding",
        numCandidates: 100,
        limit: 10,
        index: "vector_index"
    }
}]);
```

---
## Queryable Encryption

- Equality queries on encrypted fields
- Server holds encrypted index
- Stronger than client-side encryption
- Slight performance cost

---
## Atlas Triggers

- Serverless functions on data changes
- Like change streams + Lambda
- Hosted; no infra
- Use: webhook on insert, sync to other systems

---
## Atlas Functions

- Serverless backend in Atlas
- HTTP endpoints, scheduled triggers
- JavaScript / Node
- For: small APIs, prototypes

---
## Atlas Charts

- Visualisation built into Atlas
- Dashboards from collections
- No external BI tool needed
- For: simple internal dashboards

---
## Atlas Data API

- HTTP API on top of MongoDB
- No driver needed
- Useful for: serverless, web clients (with care)
- Auth via API keys

---
## Atlas SQL Interface

- Query MongoDB with SQL
- Read-only; analytical
- For: BI tools, data science
- Backed by Atlas Data Federation

---
## Federation

- Query across collections, S3, other clusters
- Single query spanning sources
- Useful for: archived data, cross-cluster

---
## What's Coming

- Continued search / vector enhancements
- Better OLAP integration
- Stronger encryption guarantees
- More serverless capabilities

---
## Common Feature Mistakes

- Using time-series collection for non-time-series data
- Atlas Search without proper field mappings
- Vector search without good embeddings
- Enabling everything; only what you use
- Treating Atlas-only features as portable
