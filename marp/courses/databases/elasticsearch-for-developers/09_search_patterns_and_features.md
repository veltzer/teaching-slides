---
tags:
  - databases:elasticsearch
level: intermediate
category: databases
audience:
  - audiences:developers

---

# Search Patterns and Features

---

## Search Pattern Uses

![pattern_uses](svg/courses/databases/elasticsearch-for-developers/09_search_patterns_and_features/pattern_uses.svg)

---

## What This Chapter Covers

- Faceting
- Search-as-you-type
- Did-you-mean
- Personalisation
- Boosting
- Common patterns

---

## Common Patterns

![search_patterns](svg/courses/databases/elasticsearch-for-developers/09_search_patterns_and_features/search_patterns.svg)

---

## Faceting

- Show counts of matching values
- "Filter by category" sidebar
- Done with terms aggregation
- Standard e-commerce pattern

---

## Search-As-You-Type

- User types &#8594; suggestions appear
- Prefix matching, edge n-grams
- Completion suggester for autocomplete
- Sub-100ms latency target

---

## Did-You-Mean

- Suggest correction for typos
- Phrase suggester
- "Did you mean *photography*?"
- Increases recovery from typos

---

## Personalisation

- Boost results based on user profile
- Function score with user signals
- Multi-armed bandit for tuning
- Privacy considerations

---

## Boosting Recent

```json
{
  "function_score": {
    "query": {...},
    "gauss": {
      "created_at": {
        "origin": "now",
        "scale": "7d",
        "decay": 0.5
      }
    }
  }
}
```

---

## Boosting Popular

- Maintain a popularity score per document
- Multiply / add to relevance
- Update periodically
- Combine signals

---

## Geo-Boosting

- Boost results near the user
- Distance decay
- Combine with relevance

---

## Multi-Lingual Search

- One index per language; or analyzers per field
- Detect language at index time
- Per-language synonyms, stemming
- Common in global products

---

## Filtering UI Patterns

- Active filters as chips
- Counts per filter (faceting)
- Clearable
- Persistent in URL

---

## Result Diversification

- Avoid: 10 results from same merchant
- Group by field; one per group
- collapse / aggregations
- Better UX

---

## Long-Tail Queries

- Most queries have many results
- "Phone" matches thousands
- Rank carefully; show fewer per page

---

## No-Result Pages

- Helpful messaging
- Spelling suggestions
- Related searches
- Don't just say "no results"

---

## A/B Testing Search

- Try new ranking; measure click-through
- Compare to baseline
- Roll out winner
- Standard for serious search products

---

## Common Search Pattern Mistakes

- All boosts; no clear baseline
- Personalisation that filter-bubbles users
- No fallback when filters return nothing
- Slow autocomplete (over 100ms)
- One global ranking for all users
