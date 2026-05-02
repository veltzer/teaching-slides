---
tags:
  - databases:elasticsearch
level: intermediate
category: databases
audience:
  - audiences:developers

---
# Advanced Search Features

---
## What This Chapter Covers

- Multi-match
- Function scores
- Suggesters
- Highlighting
- Fuzzy matching
- Synonyms

---
## Relevance Levers

![relevance_features](svg/courses/databases/elasticsearch-for-developers/06_advanced_search_features/relevance_features.svg)

---
## Multi-Match

```json
{
  "multi_match": {
    "query": "phone",
    "fields": ["title^2", "description"]
  }
}
```

- Search multiple fields
- `^2` boosts
- Many strategy options

---
## Function Scores

- Modify relevance with custom functions
- Boost recent documents
- Boost popular documents
- Combine: `score = match_score * popularity * recency_decay`

---
## Function Score Example

```json
{
  "function_score": {
    "query": {"match_all": {}},
    "functions": [{
      "filter": {"range": {"created_at": {"gte": "now-7d"}}},
      "weight": 2
    }]
  }
}
```

---
## Suggesters

- "Did you mean?" suggestions
- Term suggester: spelling correction
- Phrase suggester: better; uses bigrams
- Completion suggester: autocomplete

---
## Completion Suggester

- Optimised for autocomplete
- Pre-built data structure
- Sub-millisecond latency
- Requires special field type

---
## Highlighting

```json
{
  "query": {...},
  "highlight": {
    "fields": {"description": {}}
  }
}
```

- Returns matched snippets with HTML markup
- Show users *why* the document matched

---
## Fuzzy Matching

```json
{ "match": { "title": { "query": "phon", "fuzziness": "AUTO" } } }
```

- Edit distance (Levenshtein)
- Catches typos
- Slower than exact

---
## Synonyms

- Map equivalent terms
- "USA" = "United States" = "US"
- Index-time or query-time
- Loaded from file or API

---
## Stop Words

- Common words filtered out: the, a, is
- Reduce index size
- Lose some precision
- Per-language

---
## Stemming

- Reduce words to roots: "running" &#8594; "run"
- Per-language analyzers
- Increases recall
- Built-in for many languages

---
## More Like This

- Find documents similar to a given one
- Useful for recommendations
- "Customers who viewed this..."

---
## Percolator

- Reverse search: index queries, search documents
- "Match this incoming document against saved queries"
- Use case: alerting on patterns

---
## Boosting

- Per-term, per-field, per-document
- Combined into final score
- Tuning relevance is an art
- A/B test changes

---
## Common Advanced Mistakes

- Heavy boosting without measuring
- Synonyms file with mistakes (recall problems)
- Fuzzy on expensive fields
- Highlighting whole documents (large response)
- More-like-this on sparse fields
