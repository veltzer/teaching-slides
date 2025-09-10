# Elasticsearch Fundamentals

## Document-Oriented Database

---

## Document-Oriented Model

Unlike relational databases:
1. No tables, rows, columns
1. Documents instead of records
1. JSON format
1. Schema-flexible

---

## Document Structure

<svg viewBox="0 0 400 300" xmlns="http://www.w3.org/2000/svg">
  <rect x="100" y="50" width="200" height="200" fill="#f0f0f0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="200" y="80" text-anchor="middle" font-weight="bold">Document</text>
  <rect x="120" y="100" width="160" height="30" fill="#4CAF50" rx="3"/>
  <text x="200" y="120" text-anchor="middle" fill="white">_id: "123"</text>
  <rect x="120" y="140" width="160" height="30" fill="#2196F3" rx="3"/>
  <text x="200" y="160" text-anchor="middle" fill="white">_index: "products"</text>
  <rect x="120" y="180" width="160" height="50" fill="#FF9800" rx="3"/>
  <text x="200" y="200" text-anchor="middle" fill="white">_source: {data}</text>
</svg>

---

## JSON Documents

```json
{
  "product_id": "SKU-12345",
  "name": "Wireless Mouse",
  "description": "Ergonomic wireless mouse with USB receiver",
  "price": 29.99,
  "in_stock": true,
  "categories": ["Electronics", "Computer Accessories"]
}
```

---

## Document Metadata

Every document has:
1. **_index**: Where it's stored
1. **_id**: Unique identifier
1. **_source**: Original JSON
1. **_version**: Version number

---

## Metadata Example

```json
{
  "_index": "products",
  "_id": "SKU-12345",
  "_version": 1,
  "_seq_no": 0,
  "_primary_term": 1,
  "_source": {
    "name": "Wireless Mouse",
    "price": 29.99
  }
}
```

---

## Document Lifecycle

<svg viewBox="0 0 400 250" xmlns="http://www.w3.org/2000/svg">
  <circle cx="80" cy="125" r="40" fill="#4CAF50"/>
  <text x="80" y="130" text-anchor="middle" fill="white">Create</text>
  <path d="M120 125 L160 125" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/>
  <circle cx="200" cy="125" r="40" fill="#2196F3"/>
  <text x="200" y="130" text-anchor="middle" fill="white">Update</text>
  <path d="M240 125 L280 125" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/>
  <circle cx="320" cy="125" r="40" fill="#FF9800"/>
  <text x="320" y="130" text-anchor="middle" fill="white">Delete</text>
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## CRUD Operations

1. `Create` - Index new documents
1. `Read` - Retrieve documents
1. `Update` - Modify documents
1. `Delete` - Remove documents

---

## Creating Documents - POST

```bash
POST /products/_doc
{
  "name": "Keyboard",
  "price": 79.99,
  "brand": "TechBrand"
}
```

Auto-generates ID: `"_id": "x3K9m4sBz1..."`

---

## Creating Documents - PUT

```bash
PUT /products/_doc/KB-001
{
  "name": "Mechanical Keyboard",
  "price": 149.99,
  "brand": "ProType"
}
```

Specify your own ID: `"_id": "KB-001"`

---

## Create vs Index

1. **_create**: Fails if document exists
1. **PUT with ID**: Overwrites if exists
1. **POST**: Always creates new

```bash
PUT /products/_create/KB-001
{
  "name": "Gaming Keyboard"
}
```

---

## Retrieving Documents

```bash
GET /products/_doc/KB-001
```

Response:
```json
{
  "_index": "products",
  "_id": "KB-001",
  "_version": 1,
  "_source": {
    "name": "Mechanical Keyboard",
    "price": 149.99
  }
}
```

---

## Get Multiple Documents

```bash
GET /products/_mget
{
  "ids": ["KB-001", "MS-002", "HD-003"]
}
```

Returns array of documents

---

## Source Filtering

Get only specific fields:
```bash
GET /products/_doc/KB-001?_source=name,price
```

Exclude source entirely:
```bash
GET /products/_doc/KB-001?_source=false
```

---

## Updating Documents - Full

```bash
PUT /products/_doc/KB-001
{
  "name": "Mechanical Keyboard v2",
  "price": 139.99,
  "brand": "ProType",
  "wireless": true
}
```

Replaces entire document

---

## Updating Documents - Partial

```bash
POST /products/_update/KB-001
{
  "doc": {
    "price": 129.99,
    "on_sale": true
  }
}
```

Merges with existing fields

---

## Scripted Updates

```bash
POST /products/_update/KB-001
{
  "script": {
    "source": "ctx._source.price *= 0.9",
    "lang": "painless"
  }
}
```

Apply 10% discount

---

## Update with Retry

```bash
POST /products/_update/KB-001?retry_on_conflict=3
{
  "doc": {
    "stock": 45
  }
}
```

Handles concurrent updates

---

## Deleting Documents

```bash
DELETE /products/_doc/KB-001
```

Response:
```json
{
  "_index": "products",
  "_id": "KB-001",
  "_version": 2,
  "result": "deleted"
}
```

---

## Delete by Query

```bash
POST /products/_delete_by_query
{
  "query": {
    "term": {
      "in_stock": false
    }
  }
}
```

Removes multiple documents

---

## Bulk Operations

```bash
POST /_bulk
{"index": {"_index": "products", "_id": "1"}}
{"name": "Product 1", "price": 10.99}
{"create": {"_index": "products", "_id": "2"}}
{"name": "Product 2", "price": 20.99}
{"update": {"_index": "products", "_id": "1"}}
{"doc": {"price": 9.99}}
{"delete": {"_index": "products", "_id": "3"}}
```

---

## Bulk Format Rules

1. NDJSON format (newline-delimited)
1. Action and metadata line
1. Document source line (except delete)
1. No pretty printing
1. Newline at end

---

## Bulk Performance

1. Optimal batch size: 5-15 MB
1. 1000-5000 documents per batch
1. Monitor rejection rates
1. Use parallel requests

---

## Index Management

```bash
PUT /my_index
{
  "settings": {
    "number_of_shards": 3,
    "number_of_replicas": 1
  }
}
```

---

## Index Settings

Key settings:
1. **number_of_shards**: Cannot change after creation
1. **number_of_replicas**: Can change anytime
1. **refresh_interval**: How often to make data searchable
1. **max_result_window**: Max results for pagination

---

## Check Index Existence

```bash
HEAD /my_index
```

Returns:
- `200 OK` if exists
- `404 Not Found` if doesn't exist

---

## Get Index Information

```bash
GET /my_index
```

Returns settings, mappings, and aliases

---

## Index Aliases

```bash
POST /_aliases
{
  "actions": [
    {
      "add": {
        "index": "products_v1",
        "alias": "products"
      }
    }
  ]
}
```

---

## Alias Benefits

1. Zero-downtime reindexing
1. Logical views of data
1. Simplify index management
1. Time-based data handling

---

## Reindexing Data

```bash
POST /_reindex
{
  "source": {
    "index": "old_products"
  },
  "dest": {
    "index": "new_products"
  }
}
```

---

## Reindex with Transformation

```bash
POST /_reindex
{
  "source": {
    "index": "products_v1",
    "query": {
      "term": { "active": true }
    }
  },
  "dest": {
    "index": "products_v2"
  }
}
```

---

## Dynamic Mapping

Elasticsearch auto-detects types:
```json
{
  "text_field": "Hello",      // text & keyword
  "number_field": 42,          // long
  "float_field": 3.14,         // float
  "bool_field": true,          // boolean
  "date_field": "2024-01-01"   // date
}
```

---

## View Mappings

```bash
GET /products/_mapping
```

Shows field types and settings

---

## Field Data Types

1. **text**: Full-text search
1. **keyword**: Exact matches, aggregations
1. **numeric**: Numbers (long, integer, float)
1. **date**: Date/time values
1. **boolean**: true/false

---

## Text vs Keyword

```json
{
  "mappings": {
    "properties": {
      "description": { "type": "text" },
      "product_code": { "type": "keyword" }
    }
  }
}
```

---

## Multi-Fields

```json
{
  "properties": {
    "title": {
      "type": "text",
      "fields": {
        "keyword": {
          "type": "keyword"
        }
      }
    }
  }
}
```

Use as `title` (text) or `title.keyword`

---

## Optimistic Concurrency Control

```bash
PUT /products/_doc/1?if_seq_no=0&if_primary_term=1
{
  "name": "Updated Product",
  "version": 2
}
```

Prevents lost updates

---

## Version Conflicts

When concurrent updates occur:
1. Read document with version
1. Modify locally
1. Update with version check
1. Retry if conflict

---

## Best Practices

1. Use bulk API for multiple operations
1. Specify IDs when possible
1. Handle version conflicts
1. Monitor failed operations

---

## Common Pitfalls

1. Not using bulk for batch operations
1. Ignoring version conflicts
1. Over-updating documents
1. Not handling errors properly

---

## Next Steps

1. Data Modeling and Mappings
1. Field types deep dive
1. Index templates
1. Complex data structures
