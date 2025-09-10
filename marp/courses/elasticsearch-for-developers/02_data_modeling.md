# Data Modeling and Mappings

## Designing Your Data Structure

---

## Why Mappings Matter

1. Define how fields are indexed
1. Control search behavior
1. Optimize storage and performance
1. Prevent mapping explosions

---

## Mapping Definition

```json
PUT /products
{
  "mappings": {
    "properties": {
      "title": { "type": "text" },
      "price": { "type": "float" },
      "in_stock": { "type": "boolean" }
    }
  }
}
```

---

## Field Types Overview

<svg viewBox="0 0 400 300" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="30" width="100" height="40" fill="#4CAF50" rx="5"/>
  <text x="100" y="55" text-anchor="middle" fill="white">Text Types</text>
  <rect x="50" y="80" width="100" height="40" fill="#2196F3" rx="5"/>
  <text x="100" y="105" text-anchor="middle" fill="white">Numeric</text>
  <rect x="50" y="130" width="100" height="40" fill="#FF9800" rx="5"/>
  <text x="100" y="155" text-anchor="middle" fill="white">Date/Time</text>
  <rect x="250" y="30" width="100" height="40" fill="#9C27B0" rx="5"/>
  <text x="300" y="55" text-anchor="middle" fill="white">Boolean</text>
  <rect x="250" y="80" width="100" height="40" fill="#F44336" rx="5"/>
  <text x="300" y="105" text-anchor="middle" fill="white">Object/Nested</text>
  <rect x="250" y="130" width="100" height="40" fill="#00BCD4" rx="5"/>
  <text x="300" y="155" text-anchor="middle" fill="white">Geo Types</text>
</svg>

---

## Text vs Keyword

```json
{
  "properties": {
    "description": {
      "type": "text"     // Analyzed for search
    },
    "product_id": {
      "type": "keyword"  // Exact match only
    }
  }
}
```

---

## Text Field Analysis

`text` field process:
1. Tokenization: "Quick Brown Fox" → ["quick", "brown", "fox"]
1. Lowercasing: ["quick", "brown", "fox"]
1. Stemming: "running" → "run"
1. Synonyms: "fast" → "quick"

---

## Keyword Field Uses

Best for:
1. Filtering: `status: "active"`
1. Aggregations: Group by category
1. Sorting: Order by product_id
1. Exact matches: Email addresses

---

## Multi-Fields Pattern

```json
{
  "properties": {
    "email": {
      "type": "text",
      "fields": {
        "keyword": {
          "type": "keyword",
          "ignore_above": 256
        }
      }
    }
  }
}
```

---

## Numeric Types

```json
{
  "properties": {
    "quantity": { "type": "integer" },
    "price": { "type": "float" },
    "revenue": { "type": "double" },
    "views": { "type": "long" },
    "rating": { "type": "half_float" }
  }
}
```

---

## Numeric Type Selection

| Type | Range | Use Case |
|------|-------|----------|
| `byte` | -128 to 127 | Status codes |
| `short` | -32,768 to 32,767 | Counts |
| `integer` | -2³¹ to 2³¹-1 | IDs |
| `long` | -2⁶³ to 2⁶³-1 | Timestamps |
| `float` | 32-bit IEEE 754 | Prices |
| `double` | 64-bit IEEE 754 | Scientific |

---

## Date Fields

```json
{
  "properties": {
    "created_at": {
      "type": "date",
      "format": "yyyy-MM-dd HH:mm:ss||epoch_millis"
    }
  }
}
```

---

## Date Formats

Common formats:
1. `"2024-01-15"` - Date only
1. `"2024-01-15T10:30:00Z"` - ISO 8601
1. `1705315800000` - Epoch milliseconds
1. `"15/01/2024"` - Custom format

---

## Boolean Fields

```json
{
  "properties": {
    "is_active": { "type": "boolean" },
    "published": { "type": "boolean" }
  }
}
```

Accepts: `true`, `false`, `"true"`, `"false"`

---

## Object Type

```json
{
  "properties": {
    "user": {
      "properties": {
        "name": { "type": "text" },
        "age": { "type": "integer" }
      }
    }
  }
}
```

Flattened internally: `user.name`, `user.age`

---

## Nested Type

```json
{
  "properties": {
    "comments": {
      "type": "nested",
      "properties": {
        "author": { "type": "keyword" },
        "text": { "type": "text" }
      }
    }
  }
}
```

Maintains array relationships

---

## Object vs Nested

<svg viewBox="0 0 400 250" xmlns="http://www.w3.org/2000/svg">
  <text x="100" y="20" text-anchor="middle" font-weight="bold">Object (Flattened)</text>
  <rect x="50" y="30" width="100" height="80" fill="#FF9800" rx="5"/>
  <text x="100" y="60" text-anchor="middle" fill="white" font-size="12">user.name:</text>
  <text x="100" y="80" text-anchor="middle" fill="white" font-size="12">["Alice", "Bob"]</text>
  <text x="250" y="20" text-anchor="middle" font-weight="bold">Nested (Preserved)</text>
  <rect x="200" y="30" width="100" height="40" fill="#4CAF50" rx="5"/>
  <text x="250" y="55" text-anchor="middle" fill="white" font-size="12">{name: "Alice"}</text>
  <rect x="200" y="80" width="100" height="40" fill="#4CAF50" rx="5"/>
  <text x="250" y="105" text-anchor="middle" fill="white" font-size="12">{name: "Bob"}</text>
</svg>

---

## Arrays

No special type needed:
```json
{
  "tags": ["electronics", "mobile", "smartphone"],
  "prices": [99.99, 89.99, 79.99],
  "available": [true, false, true]
}
```

All values must be same type

---

## Geo Point

```json
{
  "properties": {
    "location": {
      "type": "geo_point"
    }
  }
}

// Document:
{
  "location": {
    "lat": 40.7128,
    "lon": -74.0060
  }
}
```

---

## Geo Shape

```json
{
  "properties": {
    "area": {
      "type": "geo_shape"
    }
  }
}

// Document:
{
  "area": {
    "type": "polygon",
    "coordinates": [[[100.0, 0.0], [101.0, 0.0], [101.0, 1.0]]]
  }
}
```

---

## Mapping Parameters

```json
{
  "properties": {
    "title": {
      "type": "text",
      "index": true,
      "store": false,
      "doc_values": false,
      "norms": true
    }
  }
}
```

---

## Index Parameter

Controls if field is searchable:
```json
{
  "properties": {
    "internal_id": {
      "type": "keyword",
      "index": false  // Not searchable
    }
  }
}
```

---

## Store Parameter

Store field separately:
```json
{
  "properties": {
    "content": {
      "type": "text",
      "store": true  // Retrieve without _source
    }
  }
}
```

---

## Doc Values

Column-oriented storage for sorting/aggregations:
```json
{
  "properties": {
    "price": {
      "type": "float",
      "doc_values": true  // Default for most fields
    }
  }
}
```

---

## Norms

Scoring information storage:
```json
{
  "properties": {
    "title": {
      "type": "text",
      "norms": true  // Needed for scoring
    },
    "description": {
      "type": "text",
      "norms": false  // Save space if no scoring
    }
  }
}
```

---

## Null Value

Handle null/missing values:
```json
{
  "properties": {
    "status": {
      "type": "keyword",
      "null_value": "unknown"
    }
  }
}
```

---

## Copy To

Copy multiple fields to one:
```json
{
  "properties": {
    "title": {
      "type": "text",
      "copy_to": "full_text"
    },
    "description": {
      "type": "text",
      "copy_to": "full_text"
    },
    "full_text": {
      "type": "text"
    }
  }
}
```

---

## Denormalization Strategy

Instead of joins, duplicate data:
```json
{
  "product_name": "Laptop",
  "category": {
    "id": "electronics",
    "name": "Electronics",
    "parent": "Technology"
  }
}
```

---

## Parent-Child Relationships

```json
{
  "mappings": {
    "properties": {
      "join_field": {
        "type": "join",
        "relations": {
          "product": "review"
        }
      }
    }
  }
}
```

---

## Join Field Usage

Parent document:
```json
{
  "name": "Laptop",
  "join_field": "product"
}
```

Child document:
```json
{
  "text": "Great product!",
  "join_field": {
    "name": "review",
    "parent": "product_id_123"
  }
}
```

---

## Index Templates

```json
PUT /_index_template/logs_template
{
  "index_patterns": ["logs-*"],
  "template": {
    "settings": {
      "number_of_shards": 2
    },
    "mappings": {
      "properties": {
        "timestamp": { "type": "date" }
      }
    }
  }
}
```

---

## Dynamic Templates

```json
{
  "mappings": {
    "dynamic_templates": [{
      "strings_as_keywords": {
        "match_mapping_type": "string",
        "match": "*_id",
        "mapping": {
          "type": "keyword"
        }
      }
    }]
  }
}
```

---

## Component Templates

```json
PUT /_component_template/common_settings
{
  "template": {
    "settings": {
      "number_of_replicas": 1
    }
  }
}

PUT /_index_template/my_template
{
  "index_patterns": ["data-*"],
  "composed_of": ["common_settings"]
}
```

---

## Mapping Explosion Prevention

Limit dynamic mappings:
```json
{
  "settings": {
    "index.mapping.total_fields.limit": 1000,
    "index.mapping.depth.limit": 20,
    "index.mapping.nested_fields.limit": 50
  }
}
```

---

## Strict Dynamic Mapping

```json
{
  "mappings": {
    "dynamic": "strict",  // Reject unknown fields
    "properties": {
      "known_field": { "type": "text" }
    }
  }
}
```

Options: `true`, `false`, `strict`, `runtime`

---

## Runtime Fields

```json
{
  "mappings": {
    "runtime": {
      "day_of_week": {
        "type": "keyword",
        "script": {
          "source": "emit(doc['@timestamp'].value.dayOfWeek)"
        }
      }
    }
  }
}
```

---

## Data Modeling Best Practices

1. Denormalize when possible
1. Use correct field types
1. Limit nested fields
1. Consider query patterns
1. Plan for growth

---

## Common Modeling Patterns

1. **Time-series**: Daily indices
1. **Multi-tenant**: Index per tenant or routing
1. **Hierarchical**: Nested or parent-child
1. **Search**: Text with multi-fields

---

## Performance Considerations

1. Fewer fields = better performance
1. Disable unused features (`norms`, `doc_values`)
1. Use `keyword` for exact matches
1. Limit `nested` field usage
1. Consider field cardinality

---

## Next Steps

1. Data Ingestion strategies
1. Bulk operations optimization
1. Ingest pipelines
1. Data transformation
