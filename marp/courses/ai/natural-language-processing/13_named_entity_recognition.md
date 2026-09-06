---
tags:
  - data-and-ai:nlp
  - concepts:named-entity-recognition
level: advanced
category: ai
audience:
  - audiences:developers
  - audiences:data-scientists

---

# Named Entity Recognition

---

## What This Chapter Covers

- The fundamentals of `NER`: standard and domain-specific entity types
- Classical approaches: rules, gazetteers, and `CRF` taggers
- Neural `NER`: `BiLSTM-CRF`, transformer encoders, span and biaffine models
- Few-shot, zero-shot, distantly supervised, and cross-lingual `NER`
- Evaluation: entity-level metrics, partial matches, and error analysis

---

## What Is Named Entity Recognition

- The task of locating spans of text that refer to entities in the world
- Each span is assigned a type: a person, an organization, a place, a date
- The output is structured: positions plus labels, not just a category per document
- A foundational building block for search, knowledge graphs, and information extraction

---

## Standard Entity Types

- `PER` — people, real or fictional, including aliases and titled forms
- `ORG` — organizations, companies, agencies, sports teams, bands
- `LOC` — geographic locations, countries, cities, landmarks, regions
- `MISC` — a catch-all in older corpora for nationalities, events, works of art
- The `CoNLL-2003` shared task fixed these four labels as a de facto baseline

---

## Entity Type Examples

![entity_types](svg/courses/ai/natural-language-processing/13_named_entity_recognition/entity_types.svg)

---

## Domain-Specific Entity Types

- Biomedical: `GENE`, `PROTEIN`, `DISEASE`, `DRUG`, `CELL_LINE`
- Legal: `STATUTE`, `CASE`, `COURT`, `JUDGE`, `JURISDICTION`
- Finance: `TICKER`, `INSTRUMENT`, `MONEY`, `PERCENT`, `DATE`
- Cybersecurity: `MALWARE`, `VULNERABILITY`, `ATTACKER`, `INDICATOR`
- The right schema is decided by the downstream consumer, not the modeler

---

## Nested and Overlapping Entities

- `Bank of America` is one `ORG` containing the `LOC` `America`
- `University of Tokyo` is an `ORG` whose substring `Tokyo` is a `LOC`
- Flat `BIO` tagging cannot represent these — only the outermost or innermost wins
- Nested `NER` requires span-based or stacked formulations to express both

---

## The BIO and BIOES Tag Schemes

- `BIO`: `B-` begins a span, `I-` continues it, `O` is outside
- `BIOES`: adds `E-` for the end of a span and `S-` for a single-token span
- `BIOES` makes single-token entities and span boundaries explicit
- A token-level classifier produces these tags; spans are recovered by decoding

---

## Tagging Schemes Compared

![tagging_schemes](svg/courses/ai/natural-language-processing/13_named_entity_recognition/tagging_schemes.svg)

---

## Rule-Based and Gazetteer-Driven NER

- A gazetteer is a curated list of known entity strings — cities, drug names, tickers
- Rules combine gazetteer matches with patterns: `Dr.` followed by a capitalized name
- Strengths: precise, interpretable, fast, no training data needed
- Weaknesses: brittle on variation, expensive to maintain, poor recall on novel entities

---

## When Rules Still Win

- The schema is small, closed, and stable
- The data is clean and the entities are well-formed identifiers
- Compliance demands an explainable extraction path
- A rule-based system is often the right baseline before any model is trained

---

## Feature Engineering for Classical NER

- Word identity, lowercase form, prefix and suffix character n-grams
- Shape features: `Xxxxx`, `XX-99`, all-caps, mixed digits
- Word context: previous and next tokens, part-of-speech tags
- Gazetteer lookups, capitalization in context, sentence position

---

## Conditional Random Fields

- A linear-chain `CRF` scores entire tag sequences, not single tokens
- Transition scores capture which tag can follow which: `B-PER` `I-PER` is allowed
- Decoding uses Viterbi to find the highest-scoring tag sequence
- For a long time the strongest non-neural method on `CoNLL-2003`

---

## CRF Strengths and Limits

- Exploits structural constraints between adjacent tags directly
- Trained discriminatively against the global sequence likelihood
- Rich features but linear capacity — long-range patterns are hard
- Outperformed by neural encoders, but still lives inside many neural taggers as the output layer

---

## BiLSTM-CRF

- A bidirectional `LSTM` produces a contextual vector per token
- A `CRF` layer on top scores valid label sequences and prevents inconsistent tags
- Often combined with character-level `CNN` or `LSTM` for spelling and shape signal
- The dominant architecture from roughly 2016 to the rise of pretrained transformers

---

## BiLSTM-CRF Architecture

![bilstm_crf_architecture](svg/courses/ai/natural-language-processing/13_named_entity_recognition/bilstm_crf_architecture.svg)

---

## Transformer-Based NER

- A pretrained encoder (`BERT`, `RoBERTa`, `DeBERTa`) produces token vectors
- A linear classification head over the tag set is added on top
- Optionally a `CRF` layer enforces tag consistency at inference time
- This is the modern default for supervised `NER` on a labeled corpus

---

## Subword Tokens and NER Labels

- Pretrained tokenizers split words into subwords; only one subword carries the gold label
- Common conventions: tag the first subword and ignore the rest, or tag all
- Misalignment between gold spans and subword boundaries is a frequent bug
- The alignment code is small, easy to get wrong, and silently degrades scores

---

## Span-Based NER

- Enumerate candidate spans up to a maximum length
- Classify each span directly into an entity type or "no entity"
- Naturally supports overlapping and nested entities — spans need not be disjoint
- Computational cost grows quadratically with sequence length

---

## Biaffine NER

- Two feed-forward heads project each token into a "start" and "end" representation
- A biaffine scorer assigns a label to every (start, end) pair in one matrix
- Captures span boundaries and type jointly with a single tensor operation
- A strong design for nested entities, popularized by Yu and colleagues in 2020

---

## Biaffine Scoring

```python
def biaffine_score(start_h, end_h, U, b):
    # start_h: [seq, dim], end_h: [seq, dim]
    # U: [dim, num_labels, dim], b: [num_labels]
    s = einsum("id,dlk,jk->ijl", start_h, U, end_h)
    return s + b  # shape [seq, seq, num_labels]
```

- Output: a score for each (start, end, label) triple
- Decoding picks the highest-scoring non-conflicting set of spans

---

## Choosing an NER Architecture

- Flat entities, plenty of labeled data: a transformer encoder with a softmax head
- Strict tag consistency required: add a `CRF` on top
- Nested or overlapping entities: span-based or biaffine formulations
- Latency-sensitive on a small schema: distilled encoder or even a `BiLSTM-CRF`

---

## Few-Shot NER with Prompts

- Frame extraction as a generation or filling task for a large language model
- "Extract all persons from the following text and return them as a list"
- Few demonstrations in the prompt teach the schema and the output format
- Quality depends heavily on prompt phrasing and on consistent post-processing

---

## Zero-Shot NER

- No labeled examples for the target schema — only label names and definitions
- Models such as `GLiNER` accept a list of labels and tag spans accordingly
- Useful when the schema changes often or labeling budget is zero
- Recall on rare types is uneven; a small validation set still pays for itself

---

## Distantly Supervised NER

- Use an external knowledge base to auto-label mentions in a large corpus
- Wikipedia anchor text and Wikidata types provide millions of weak labels
- The labels are noisy: incomplete coverage, type ambiguity, false positives
- Robust loss functions and partial labeling help the model learn from imperfect data

---

## Cross-Lingual NER

- Train on a high-resource language, evaluate on a low-resource one
- Multilingual encoders (`mBERT`, `XLM-R`) provide a shared embedding space
- Translation-based projection maps annotations from English to other languages
- Performance varies by script, by domain, and by typological distance

---

## Token-Level vs Entity-Level Evaluation

- Token-level: accuracy or `F1` over individual tag predictions
- Entity-level: a predicted entity is correct only if both span and type match exactly
- Token-level scores are easy to inflate — most tokens are `O`
- Entity-level `F1` is the standard reported metric for `NER`

---

## Evaluation Metrics

![evaluation_metrics](svg/courses/ai/natural-language-processing/13_named_entity_recognition/evaluation_metrics.svg)

---

## Partial-Match Scoring

- Strict match: span and type both exact — the `CoNLL` default
- Type match: type is correct, span overlaps the gold span
- Span match: span is exact, type may differ
- The `MUC` and `SemEval` schemes give partial credit; the choice changes the headline number

---

## Error Analysis

- Boundary errors: right type, wrong span — common with multi-token names
- Type errors: right span, wrong type — `ORG` versus `LOC` for `Washington`
- Missed entities: spans the model failed to detect at all
- Spurious entities: spans the model invented, common on rare-looking phrases

---

## Confusion Patterns to Watch

- `PER` versus `ORG` for company names that contain personal names
- `LOC` versus `ORG` for institutions named after places
- Boundary drift on titles: is `President Obama` a single `PER` or two tokens?
- Annotation guidelines determine the answer; the model can only follow them

---

## Annotation Quality Matters

- Inter-annotator agreement caps the achievable model score
- Boundary conventions (titles, conjunctions, possessives) need a written guide
- Active learning prioritizes uncertain examples for human review
- A small clean test set is worth more than a large noisy one

---

## NER in Production

- Schemas drift: new entity types appear, old ones become more granular
- Train and evaluation data must be regenerated, not patched in place
- Monitor entity rates per type; sudden shifts often mean upstream changes
- Reserve a held-out slice for regression checks at every model update

---

## Anti-Patterns

- Reporting token-level `F1` and calling it `NER` accuracy
- Ignoring subword-to-word alignment and silently truncating long entities
- Forcing a flat tagger onto inherently nested data
- Trusting distant supervision labels without measuring noise

---

## Summary

- `NER` finds typed spans in text, with `BIO` or span-based output formats
- Classical pipelines combine gazetteers, hand features, and a `CRF`
- Neural `NER` runs through `BiLSTM-CRF`, transformer heads, and span or biaffine models
- Few-shot, zero-shot, and distantly supervised methods extend `NER` beyond labeled corpora
- Evaluate at the entity level, separate boundary errors from type errors, watch the schema
