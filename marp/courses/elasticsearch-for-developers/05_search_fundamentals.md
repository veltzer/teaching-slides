# Search Fundamentals

## Building Powerful Search Queries

---

## Search API Basics

```json
GET /products/_search
{
  "query": {
    "match": {
      "name": "laptop"
    }
  }
}
```

Returns matching documents with scores

---

## Query vs Filter Context

<svg viewBox="0 0 400 250" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="140" height="150" fill="#4CAF50" rx="5"/>
  <text x="120" y="80" text-anchor="middle" fill="white" font-weight="bold">Query Context</text>
  <text x="120" y="110" text-anchor="middle" fill="white">• Calculates score</text>
  <text x="120" y="135" text-anchor="middle" fill="white">• "How well?"</text>
  <text x="120" y="160" text-anchor="middle" fill="white">• Not cached</text>
  <rect x="210" y="50" width="140" height="150" fill="#2196F3" rx="5"/>
  <text x="280" y="80" text-anchor="middle" fill="white" font-weight="bold">Filter Context</text>
  <text x="280" y="110" text-anchor="middle" fill="white">• No scoring</text>
  <text x="280" y="135" text-anchor="middle" fill="white">• "Yes or No?"</text>
  <text x="280" y="160" text-anchor="middle" fill="white">• Cached</text>
</svg>

---

## Score Calculation

Relevance score factors:
1. **Term Frequency (TF)**: How often term appears
1. **Inverse Document Frequency (IDF)**: How rare the term
1. **Field Length**: Shorter fields score higher
1. **Boost**: Manual score adjustment

---

## Match Query

```json
{
  "query": {
    "match": {
      "description": "wireless mouse"
    }
  }
}
```

Analyzes text and matches ANY term

---

## Match Options

```json
{
  "query": {
    "match": {
      "description": {
        "query": "wireless mouse",
        "operator": "and",
        "fuzziness": "AUTO"
      }
    }
  }
}
```

---

## Match Phrase Query

```json
{
  "query": {
    "match_phrase": {
      "description": "wireless mouse"
    }
  }
}
```

Matches exact phrase in order

---

## Match Phrase with Slop

```json
{
  "query": {
    "match_phrase": {
      "description": {
        "query": "wireless mouse",
        "slop": 2
      }
    }
  }
}
```

Allows 2 word positions between terms

---

## Multi Match Query

```json
{
  "query": {
    "multi_match": {
      "query": "laptop",
      "fields": ["name^2", "description", "category"]
    }
  }
}
```

Search multiple fields with boosting

---

## Multi Match Types

1. **best_fields**: Default, uses best matching field
1. **most_fields**: Combines scores from all fields
1. **cross_fields**: Treats fields as one
1. **phrase**: Runs match_phrase on each
1. **phrase_prefix**: For autocomplete

---

## Query String Query

```json
{
  "query": {
    "query_string": {
      "query": "laptop AND (dell OR hp)",
      "default_field": "description"
    }
  }
}
```

Supports Lucene syntax

---

## Simple Query String

```json
{
  "query": {
    "simple_query_string": {
      "query": "laptop +dell -refurbished",
      "fields": ["name", "description"]
    }
  }
}
```

Safer version, limited syntax

---

## Term Query

```json
{
  "query": {
    "term": {
      "status": "active"
    }
  }
}
```

Exact match, no analysis

---

## Terms Query

```json
{
  "query": {
    "terms": {
      "category": ["electronics", "computers", "mobile"]
    }
  }
}
```

Match any of the exact values

---

## Range Query

```json
{
  "query": {
    "range": {
      "price": {
        "gte": 100,
        "lte": 500
      }
    }
  }
}
```

Operators: `gt`, `gte`, `lt`, `lte`

---

## Date Range Query

```json
{
  "query": {
    "range": {
      "created_at": {
        "gte": "2024-01-01",
        "lte": "now",
        "format": "yyyy-MM-dd"
      }
    }
  }
}
```

---

## Date Math

```json
{
  "query": {
    "range": {
      "timestamp": {
        "gte": "now-7d/d",
        "lte": "now/d"
      }
    }
  }
}
```

Last 7 days, rounded to day

---

## Exists Query

```json
{
  "query": {
    "exists": {
      "field": "description"
    }
  }
}
```

Documents where field has value

---

## Prefix Query

```json
{
  "query": {
    "prefix": {
      "product_code": "LAP"
    }
  }
}
```

Matches documents starting with prefix

---

## Wildcard Query

```json
{
  "query": {
    "wildcard": {
      "email": "*@example.com"
    }
  }
}
```

`*` = zero or more, `?` = single character

---

## Regexp Query

```json
{
  "query": {
    "regexp": {
      "product_code": "[A-Z]{3}-[0-9]{4}"
    }
  }
}
```

Regular expression matching

---

## Fuzzy Query

```json
{
  "query": {
    "fuzzy": {
      "name": {
        "value": "laptp",
        "fuzziness": 2
      }
    }
  }
}
```

Handles typos and misspellings

---

## Bool Query Structure

```json
{
  "query": {
    "bool": {
      "must": [],
      "should": [],
      "must_not": [],
      "filter": []
    }
  }
}
```

---

## Bool Query Logic

<svg viewBox="0 0 400 200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="30" width="80" height="40" fill="#4CAF50" rx="5"/>
  <text x="90" y="55" text-anchor="middle" fill="white">must</text>
  <text x="90" y="90" text-anchor="middle">AND + Score</text>
  <rect x="150" y="30" width="80" height="40" fill="#2196F3" rx="5"/>
  <text x="190" y="55" text-anchor="middle" fill="white">should</text>
  <text x="190" y="90" text-anchor="middle">OR + Score</text>
  <rect x="250" y="30" width="80" height="40" fill="#FF9800" rx="5"/>
  <text x="290" y="55" text-anchor="middle" fill="white">filter</text>
  <text x="290" y="90" text-anchor="middle">AND No Score</text>
  <rect x="150" y="120" width="80" height="40" fill="#F44336" rx="5"/>
  <text x="190" y="145" text-anchor="middle" fill="white">must_not</text>
  <text x="190" y="175" text-anchor="middle">NOT</text>
</svg>

---

## Bool Query Example

```json
{
  "query": {
    "bool": {
      "must": [
        { "match": { "name": "laptop" } }
      ],
      "filter": [
        { "term": { "brand": "dell" } },
        { "range": { "price": { "lte": 1000 } } }
      ]
    }
  }
}
```

---

## Minimum Should Match

```json
{
  "query": {
    "bool": {
      "should": [
        { "term": { "color": "red" } },
        { "term": { "color": "blue" } },
        { "term": { "color": "green" } }
      ],
      "minimum_should_match": 2
    }
  }
}
```

---

## Boosting Query

```json
{
  "query": {
    "boosting": {
      "positive": {
        "match": { "name": "laptop" }
      },
      "negative": {
        "term": { "refurbished": true }
      },
      "negative_boost": 0.5
    }
  }
}
```

---

## Constant Score Query

```json
{
  "query": {
    "constant_score": {
      "filter": {
        "term": { "category": "electronics" }
      },
      "boost": 1.5
    }
  }
}
```

Wraps filter with fixed score

---

## Dis Max Query

```json
{
  "query": {
    "dis_max": {
      "queries": [
        { "match": { "title": "laptop" } },
        { "match": { "description": "laptop" } }
      ],
      "tie_breaker": 0.3
    }
  }
}
```

Best matching field wins

---

## Function Score Query

```json
{
  "query": {
    "function_score": {
      "query": { "match": { "name": "laptop" } },
      "functions": [{
        "filter": { "term": { "featured": true } },
        "weight": 2
      }],
      "boost_mode": "multiply"
    }
  }
}
```

---

## Score Functions

1. **weight**: Simple multiplier
1. **field_value_factor**: Use field value
1. **decay**: Distance-based scoring
1. **script_score**: Custom calculation
1. **random_score**: Randomize results

---

## Field Value Factor

```json
{
  "function_score": {
    "field_value_factor": {
      "field": "popularity",
      "factor": 1.2,
      "modifier": "sqrt",
      "missing": 1
    }
  }
}
```

---

## Decay Functions

```json
{
  "function_score": {
    "functions": [{
      "gauss": {
        "created_at": {
          "origin": "now",
          "scale": "10d",
          "decay": 0.5
        }
      }
    }]
  }
}
```

Types: `gauss`, `linear`, `exp`

---

## Explain API

```json
GET /products/_explain/1
{
  "query": {
    "match": {
      "name": "laptop"
    }
  }
}
```

Shows scoring breakdown

---

## Search Performance Tips

1. Use filters for yes/no criteria
1. Place filters in bool filter clause
1. Most selective filters first
1. Avoid wildcard queries on large fields
1. Use match for analyzed text

---

## Common Patterns

1. **Search + Filter**: Bool query
1. **Autocomplete**: Prefix or edge n-grams
1. **Fuzzy Search**: Match with fuzziness
1. **Exact + Full-text**: Multi-field mapping

---

## Query Validation

```json
GET /products/_validate/query?explain=true
{
  "query": {
    "match": {
      "non_existent_field": "value"
    }
  }
}
```
