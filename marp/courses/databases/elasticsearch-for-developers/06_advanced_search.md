---
tags:
  - tools:elasticsearch
  - data-and-ai:search
  - concepts:text-analysis
level: intermediate
category: database
audience:
  - audiences:developers

---
# Advanced Search Features

## Text Analysis and Relevance Tuning

---

## Text Analysis Pipeline

![text_analysis_pipeline](svg/courses/databases/elasticsearch-for-developers/06_advanced_search/text_analysis_pipeline.svg)

---

## Analyzer Components

1. **Character Filters**: Preprocess text
1. **Tokenizer**: Break into tokens
1. **Token Filters**: Transform tokens

---

## Built-in Analyzers

```json
{
  "mappings": {
    "properties": {
      "title": {
        "type": "text",
        "analyzer": "standard"
      }
    }
  }
}
```

Options: `standard`, `simple`, `whitespace`, `keyword`, `stop`, `pattern`

---

## Standard Analyzer

```json
POST /_analyze
{
  "analyzer": "standard",
  "text": "The 2 QUICK Brown-Foxes jumped."
}
```

Output: `["the", "2", "quick", "brown", "foxes", "jumped"]`

---

## Custom Analyzer

```json
PUT /products
{
  "settings": {
    "analysis": {
      "analyzer": {
        "my_analyzer": {
          "tokenizer": "standard",
          "filter": ["lowercase", "stop", "porter_stem"]
        }
      }
    }
  }
}
```

---

## Character Filters

```json
{
  "char_filter": {
    "my_char_filter": {
      "type": "mapping",
      "mappings": [
        "& => and",
        "@ => at"
      ]
    }
  }
}
```

Types: `html_strip`, `mapping`, `pattern_replace`

---

## Tokenizers

1. **standard**: Grammar-based
1. **letter**: Non-letters as breaks
1. **whitespace**: Space-separated
1. **keyword**: No tokenization
1. **pattern**: Regex-based

---

## Custom Tokenizer

```json
{
  "tokenizer": {
    "my_tokenizer": {
      "type": "pattern",
      "pattern": "[,.]"
    }
  }
}
```

Split on commas and periods

---

## Token Filters

Common filters:
1. **lowercase**: Convert to lowercase
1. **stop**: Remove stop words
1. **synonym**: Add synonyms
1. **stemmer**: Reduce to root
1. **shingle**: Create n-grams

---

## Synonym Filter

```json
{
  "filter": {
    "my_synonyms": {
      "type": "synonym",
      "synonyms": [
        "laptop, notebook",
        "fast, quick, speedy",
        "i-pod, ipod => ipod"
      ]
    }
  }
}
```

---

## Synonym File

```json
{
  "filter": {
    "synonym_filter": {
      "type": "synonym",
      "synonyms_path": "analysis/synonyms.txt",
      "updateable": true
    }
  }
}
```

External synonym management

---

## Stemming

```json
{
  "filter": {
    "english_stemmer": {
      "type": "stemmer",
      "language": "english"
    }
  }
}
```

`running`, `runs`, `ran` → `run`

---

## Edge N-grams

```json
{
  "filter": {
    "edge_ngram_filter": {
      "type": "edge_ngram",
      "min_gram": 2,
      "max_gram": 10
    }
  }
}
```

"search" → `["se", "sea", "sear", "searc", "search"]`

---

## N-grams

```json
{
  "filter": {
    "ngram_filter": {
      "type": "ngram",
      "min_gram": 3,
      "max_gram": 4
    }
  }
}
```

"hello" → `["hel", "ell", "llo", "hell", "ello"]`

---

## Phonetic Matching

```json
{
  "filter": {
    "phonetic_filter": {
      "type": "phonetic",
      "encoder": "metaphone"
    }
  }
}
```

Match similar-sounding words

---

## Language Analyzers

```json
{
  "properties": {
    "content": {
      "type": "text",
      "analyzer": "english"
    },
    "contenido": {
      "type": "text",
      "analyzer": "spanish"
    }
  }
}
```

Language-specific processing

---

## Analyzer Testing

```json
POST /_analyze
{
  "tokenizer": "standard",
  "filter": ["lowercase", "stop"],
  "text": "The Quick Brown Fox"
}
```

Test analysis chain

---

## Search-time Analysis

```json
{
  "query": {
    "match": {
      "title": {
        "query": "running",
        "analyzer": "english"
      }
    }
  }
}
```

Override default analyzer

---

## Relevance Scoring

BM25 algorithm factors:
1. **Term Frequency**: More occurrences = higher score
1. **Inverse Document Frequency**: Rare terms score higher
1. **Field Length**: Shorter fields score higher
1. **Query Normalization**: Consistent scoring

---

## Field Boosting

```json
{
  "query": {
    "multi_match": {
      "query": "laptop",
      "fields": [
        "title^3",
        "description^2",
        "category"
      ]
    }
  }
}
```

Title 3x more important

---

## Query-time Boosting

```json
{
  "query": {
    "bool": {
      "should": [
        {
          "match": {
            "title": {
              "query": "laptop",
              "boost": 2
            }
          }
        }
      ]
    }
  }
}
```

---

## Index-time Boosting

```json
{
  "properties": {
    "important_field": {
      "type": "text",
      "boost": 2  // Deprecated!
    }
  }
}
```

Use query-time boosting instead

---

## Explain Score

```json
GET /products/_search
{
  "explain": true,
  "query": {
    "match": {
      "title": "laptop"
    }
  }
}
```

Detailed scoring breakdown

---

## Highlighting

```json
{
  "query": {
    "match": { "content": "elasticsearch" }
  },
  "highlight": {
    "fields": {
      "content": {}
    }
  }
}
```

Result: `"<em>Elasticsearch</em> is a search engine"`

---

## Highlight Options

```json
{
  "highlight": {
    "fields": {
      "content": {
        "fragment_size": 150,
        "number_of_fragments": 3,
        "pre_tags": ["<mark>"],
        "post_tags": ["</mark>"]
      }
    }
  }
}
```

---

## Highlighter Types

1. **plain**: Default, simple
1. **unified**: Recommended, accurate
1. **fvh**: Fast vector highlighter

```json
{
  "highlight": {
    "fields": {
      "content": {
        "type": "unified"
      }
    }
  }
}
```

---

## Term Suggester

```json
{
  "suggest": {
    "text": "tset",
    "my_suggestion": {
      "term": {
        "field": "title"
      }
    }
  }
}
```

Suggests: "test"

---

## Phrase Suggester

```json
{
  "suggest": {
    "text": "quick brwn fox",
    "my_suggestion": {
      "phrase": {
        "field": "title",
        "max_errors": 2
      }
    }
  }
}
```

Suggests: "quick brown fox"

---

## Completion Suggester

```json
{
  "mappings": {
    "properties": {
      "suggest": {
        "type": "completion"
      }
    }
  }
}
```

For autocomplete functionality

---

## Index Completion Data

```json
PUT /products/_doc/1
{
  "name": "Apple iPhone",
  "suggest": {
    "input": ["Apple", "iPhone", "Apple iPhone"],
    "weight": 10
  }
}
```

---

## Query Completion

```json
{
  "suggest": {
    "product_suggest": {
      "prefix": "app",
      "completion": {
        "field": "suggest",
        "size": 5
      }
    }
  }
}
```

---

## Context Suggester

```json
{
  "mappings": {
    "properties": {
      "suggest": {
        "type": "completion",
        "contexts": [{
          "name": "category",
          "type": "category"
        }]
      }
    }
  }
}
```

Category-aware suggestions

---

## Did You Mean

```json
{
  "suggest": {
    "text": "elasticsearh",
    "did_you_mean": {
      "phrase": {
        "field": "title.trigram",
        "direct_generator": [{
          "field": "title.trigram",
          "suggest_mode": "popular"
        }]
      }
    }
  }
}
```

---

## Search Templates

```json
PUT /_scripts/product_search
{
  "script": {
    "lang": "mustache",
    "source": {
      "query": {
        "match": {
          "{{field}}": "{{query}}"
        }
      }
    }
  }
}
```

---

## Use Search Template

```json
GET /products/_search/template
{
  "id": "product_search",
  "params": {
    "field": "name",
    "query": "laptop"
  }
}
```

---

## Relevance Tuning Workflow

1. Identify key search terms
1. Analyze current results
1. Adjust analyzers/boosting
1. Test with explain API
1. Measure improvements

---

## A/B Testing

```json
{
  "query": {
    "function_score": {
      "random_score": {
        "seed": "{{user_id}}",
        "field": "_seq_no"
      }
    }
  }
}
```

Consistent random ordering per user

---

## Search Profiling

```json
GET /products/_search
{
  "profile": true,
  "query": {
    "match": {
      "title": "laptop"
    }
  }
}
```

Performance breakdown
