---
tags:
  - databases:elasticsearch
level: intermediate
category: databases
audience:
  - audiences:dbas

---
# Query Extensions

---
## What This Chapter Covers

- SQL access to Elasticsearch via the `_sql` API
- JDBC and ODBC connectivity and translating SQL to DSL
- Runtime fields and schema-on-read
- Painless scripts and runtime mappings
- Enrich processors and enrich policies
- Geospatial queries with geo_point and geo_shape
- Practical SQL and JSON examples for each

---
## Why Query Extensions Matter

- Not every consumer wants to write Query DSL
- SQL opens Elasticsearch to analysts and BI tools
- Runtime fields add columns without reindexing
- Enrich joins reference data at ingest time
- Geospatial queries answer location questions natively
- These extensions widen access while keeping one data store

---
## SQL Access: The _sql API

- Query indices with familiar SQL through the `_sql` endpoint
- Results come back as rows and columns, not nested JSON

```json
POST /_sql?format=txt
{
  "query": "SELECT customer, SUM(amount) AS total FROM orders GROUP BY customer ORDER BY total DESC",
  "fetch_size": 100
}
```

- `format` supports `txt`, `json`, `csv`, and `tsv`
- `fetch_size` paginates large result sets with a cursor
- SQL covers SELECT, WHERE, GROUP BY, and many functions

---
## SQL Cursors and Pagination

- Large results return a `cursor` to fetch the next page
- Pass the cursor back to continue; close it when done

```json
POST /_sql
{ "cursor": "sDXF1ZXJ5QW5kRmV0Y2gB..." }

POST /_sql/close
{ "cursor": "sDXF1ZXJ5QW5kRmV0Y2gB..." }
```

- Always close cursors to free server-side state
- Long-lived open cursors waste resources on the cluster

---
## JDBC and ODBC

- Elasticsearch ships JDBC and ODBC drivers for SQL clients
- BI tools connect as if Elasticsearch were a relational database
- The driver sends SQL and receives standard result sets

```output
jdbc:elasticsearch://localhost:9200
```

- Configure TLS and credentials in the connection string or DSN
- These drivers are a licensed feature; confirm your subscription tier
- Pushdown sends filtering and aggregation to the cluster, not the client

---
## Translating SQL to DSL

- `_sql/translate` converts SQL into the equivalent Query DSL
- Use it to learn DSL or to embed an optimized query

```json
POST /_sql/translate
{ "query": "SELECT customer FROM orders WHERE amount > 100 LIMIT 10" }
```

- The output is a ready-to-run `_search` body
- Great for debugging why a SQL query is slow
- Lets you start in SQL and graduate to hand-tuned DSL

---
## Runtime Fields: Schema-on-Read

- Runtime fields are evaluated at query time, not stored on disk
- They add or override fields without reindexing
- The trade-off is query cost versus storage and reindex cost
- Ideal for fields needed occasionally or still being shaped
- Promote a hot runtime field to an indexed field later if needed
- Define them in the mapping or inline per search

---
## Runtime Mappings in the Mapping

- Declare a runtime field with a Painless script

```json
PUT /logs
{
  "mappings": {
    "runtime": {
      "status_category": {
        "type": "keyword",
        "script": {
          "source": "emit(doc['status'].value >= 500 ? 'error' : 'ok')"
        }
      }
    }
  }
}
```

- `emit` produces the field value for each document
- The field behaves like a normal field in queries and aggregations

---
## Inline Runtime Fields per Search

- Define a runtime field just for one search request
- Nothing is persisted; it exists only for that query

```json
POST /logs/_search
{
  "runtime_mappings": {
    "duration_s": {
      "type": "double",
      "script": { "source": "emit(doc['duration_ms'].value / 1000.0)" }
    }
  },
  "fields": ["duration_s"],
  "query": { "range": { "duration_s": { "gte": 1.5 } } }
}
```

- Use this to prototype before committing to a mapping change

---
## Enrich Processors: The Policy

- Enrich adds reference data to documents during ingest
- First define an enrich policy over a source lookup index

```json
PUT /_enrich/policy/geo_ip_policy
{
  "match": {
    "indices": "ip_geo_lookup",
    "match_field": "ip",
    "enrich_fields": ["city", "country"]
  }
}
```

- Then execute the policy to build its internal enrich index

```bash
POST /_enrich/policy/geo_ip_policy/_execute
```

- Re-execute the policy whenever the source lookup data changes

---
## Enrich in an Ingest Pipeline

- An `enrich` processor matches incoming docs against the policy
- Matched reference fields are merged into the document

```json
PUT /_ingest/pipeline/add_geo
{
  "processors": [
    {
      "enrich": {
        "policy_name": "geo_ip_policy",
        "field": "client_ip",
        "target_field": "geo"
      }
    }
  ]
}
```

- The enrich index is cached on nodes for fast lookups
- Keep lookup indices modest in size to keep enrich fast

---
## Geospatial Field Types

- `geo_point` stores latitude and longitude points
- `geo_shape` stores polygons, lines, and complex shapes

```json
PUT /stores
{
  "mappings": {
    "properties": {
      "location": { "type": "geo_point" },
      "delivery_area": { "type": "geo_shape" }
    }
  }
}
```

- Use `geo_point` for things at a place, `geo_shape` for regions
- Points support fast distance and bounding-box queries

---
## Geo Bounding Box and Distance

- `geo_bounding_box` filters points inside a rectangle
- `geo_distance` filters points within a radius of a center

```json
POST /stores/_search
{
  "query": {
    "geo_distance": {
      "distance": "10km",
      "location": { "lat": 32.08, "lon": 34.78 }
    }
  }
}
```

- Bounding box is cheapest; distance is exact and slightly costlier
- Combine with `sort` by distance to rank nearest results first

---
## Geo Shape Queries

- Query `geo_shape` fields by spatial relation to a shape
- Relations include `intersects`, `within`, `contains`, `disjoint`

```json
POST /stores/_search
{
  "query": {
    "geo_shape": {
      "delivery_area": {
        "shape": { "type": "point", "coordinates": [34.78, 32.08] },
        "relation": "intersects"
      }
    }
  }
}
```

- This answers which delivery areas cover a given point
- Index complex shapes carefully; they cost more than points

---
## Query Extensions Checklist

- Use `_sql` and the drivers to serve analysts and BI tools
- Close SQL cursors to free server-side resources
- Use `_sql/translate` to learn and tune DSL
- Reach for runtime fields to avoid reindexing for new fields
- Re-execute enrich policies whenever lookup data changes
- Pick `geo_point` for places and `geo_shape` for regions
- Prefer bounding box for cheap geo filters, distance for radius search
