---
tags:
  - data-and-ai:nlp
  - languages:python
level: intermediate
category: machine-learning
audience:
  - audiences:data-scientists

---
# Production NLP

---
## What This Chapter Covers

- Serving
- Latency
- Cost
- Monitoring
- Multilingual reality

---
## Serving Patterns

- Batch nightly job
- Online API
- Streaming consumer
- Edge deployment

---
## Latency Budget

- Budget end-to-end
- Tokenization included
- GPU warm-up costs
- Network round trip

---
## Request Path

![serving_path](svg/courses/ai/nlp-with-python/05_production_nlp/serving_path.svg)

---
## Throughput

- Dynamic batching
- Concurrent request handling
- Async wrappers around models
- Vertical or horizontal scaling

---
## Cost Levers

- Smaller model
- Quantization
- Distillation
- Batch sizing
- Cache repeats

---
## Caching

- Hash inputs
- Memoize predictions
- Watch for stale answers when model changes
- Salt cache by model version

---
## Monitoring Signals

- p95 latency
- Error rate
- Confidence distribution
- Input length distribution

---
## Drift in NLP

- Vocabulary changes (slang, brand names)
- Topic distribution shifts
- New languages appear
- Retrain or re-evaluate

---
## Drift Signals

![drift_signals](svg/courses/ai/nlp-with-python/05_production_nlp/drift_signals.svg)

---
## Multilingual

- Detect language first
- Route to right model
- Beware shared scripts
- Test on each language

---
## Privacy

- Strip PII pre-inference
- Avoid logging raw text
- Respect deletion requests
- Encrypt at rest

---
## Safety Filters

- Toxicity classifiers
- Profanity lists
- Hard refusal of disallowed content
- Layer at input and output

---
## Versioning

- Pin model and tokenizer together
- Roll out behind a flag
- Keep old version warm
- One-line rollback

---
## Common Production Mistakes

- Different tokenizer in prod
- No latency monitor
- No drift signal
- Logging raw user text
- Mixed model versions across replicas
