---
tags:
  - data-and-ai:nlp
  - concepts:machine-translation
level: advanced
category: ai
audience:
  - audiences:developers
  - audiences:data-scientists

---
# Machine Translation

---
## What This Chapter Covers

- A brief history from rule-based to neural translation
- Statistical phrase-based `MT` and what it taught us
- Sequence-to-sequence models and why attention was the breakthrough
- Transformer-based `NMT` and the rise of multilingual models
- Decoding, evaluation, and the metrics that ship modern systems
- Where large language models fit into the translation stack today

---
## Why Machine Translation Matters

- The original `NLP` task and its longest-running benchmark
- Drives downstream tasks: cross-lingual search, accessibility, content localization
- A natural test for general language understanding under tight surface constraints
- Each generation of `MT` defined the state of the art for sequence modeling
- Modern `MT` pipelines remain the workhorse of multilingual products

---
## A Short History of MT

![mt_history](svg/courses/ai/natural-language-processing/16_machine_translation/mt_history.svg)

---
## Rule-Based Translation

- Hand-crafted dictionaries and transfer rules per language pair
- Three families: direct, transfer, and interlingua approaches
- Strong on closed-domain technical translation, brittle elsewhere
- Linguistic insight is encoded explicitly in grammar formalisms
- Replaced by data-driven methods once parallel corpora became available

---
## Statistical MT: The IBM Models

- Treat translation as a noisy-channel problem: argmax_e P(e) P(f | e)
- `IBM` Models 1-5 introduced word alignment with growing complexity
- `Model 1` is uniform; later models add fertility and distortion
- Trained with `EM` over sentence-aligned bilingual corpora
- Still the conceptual base layer under phrase-based systems

---
## Phrase-Based Translation

- Translate contiguous phrases rather than individual words
- A phrase table stores translation probabilities for source phrases
- A language model on the target side scores fluency
- A log-linear combination of features, weights tuned with `MERT`
- `Moses` was the dominant open-source toolkit for over a decade

---
## Phrase-Based MT Pipeline

![phrase_based_pipeline](svg/courses/ai/natural-language-processing/16_machine_translation/phrase_based_pipeline.svg)

---
## Limits of Phrase-Based MT

- Long-range reordering is poorly captured by local phrases
- Morphologically rich target languages produce many unseen forms
- Feature engineering plateaued by the early 2010s
- Coverage of rare words and idioms required ever larger phrase tables
- Neural sequence-to-sequence models bypassed the entire pipeline

---
## Sequence-to-Sequence with RNNs

- An encoder reads the source sentence into a fixed vector
- A decoder generates the target one token at a time
- Loss is teacher-forced cross-entropy on aligned pairs
- The fixed bottleneck loses information for long sentences
- Attention was the fix that made `NMT` competitive at scale

---
## Bahdanau Attention

- The decoder produces a weighted sum over all encoder states at every step
- Attention weights come from a small alignment network
- Solves the bottleneck and emerges as soft word alignment for free
- The first paper that made `NMT` beat phrase-based systems on `WMT`
- The same attention mechanism reappears in transformers

---
## Transformer NMT

- The original transformer paper was an `NMT` paper
- Encoder-decoder model with self-attention and cross-attention
- Parallel training over the entire source and target at once
- Residual connections, layer normalization, sinusoidal positional encodings
- Set the architecture that the rest of `NLP` would adopt

---
## Tokenization and Vocabulary

- Subword tokenization is a near-requirement for `NMT`
- `BPE` and `SentencePiece` handle morphology and rare words gracefully
- Joint vocabularies across source and target enable parameter sharing
- A shared vocabulary is essential for multilingual models
- Tokenizer mismatch is a common silent source of quality loss

---
## Multilingual NMT

- One model serving many language pairs with shared parameters
- A target language token at the start of the source signals direction
- Zero-shot translation between unseen pairs becomes possible
- `mBART`, `M2M-100`, `NLLB-200` cover hundreds of languages
- Quality is uneven — the head of the distribution dominates training

---
## Beam Search Decoding

- Maintain a beam of `k` partial translations and extend each step
- Score with the model log-probability plus a length penalty
- Beam sizes of 4-10 are typical; bigger is rarely better
- Length normalization prevents the model from preferring short outputs
- Beam search is still the default at inference time for `NMT`

---
## Decoding in Practice

```python
from transformers import MarianMTModel, MarianTokenizer

src = "Helsinki-NLP/opus-mt-en-de"
tok = MarianTokenizer.from_pretrained(src)
model = MarianMTModel.from_pretrained(src)

inputs = tok(["The cat sat on the mat."], return_tensors="pt")
out = model.generate(**inputs, num_beams=5, length_penalty=1.0)
print(tok.batch_decode(out, skip_special_tokens=True))
# ['Die Katze saß auf der Matte.']
```

- A pretrained `MarianMT` checkpoint is one line away
- For most language pairs there is already a competitive starting point

---
## Sampling and Diverse Decoding

- Beam search produces fluent but bland translations
- Nucleus sampling and minimum Bayes risk decoding restore diversity
- Helpful for paraphrase generation, less so for product translation
- Domain decides the trade-off between safety and variety
- Beam search remains the default when a single best output is needed

---
## Evaluation: BLEU

- N-gram precision against one or more reference translations
- A brevity penalty prevents reward-hacking by emitting short outputs
- Easy to compute, decades of accumulated baselines
- Notoriously coarse on a per-sentence basis; only meaningful on corpora
- Should report `sacreBLEU` with version and signature

---
## Evaluation: chrF and METEOR

- `chrF` is character-level F-score; better for morphologically rich languages
- `METEOR` adds stem and synonym matching with explicit alignment
- Both correlate better than `BLEU` with human judgment in many settings
- Modern papers report multiple metrics rather than `BLEU` alone
- Each metric captures a different aspect of similarity

---
## Evaluation: Learned Metrics

- `COMET` and `BLEURT` train regressors from human ratings
- Inputs include source, reference, and hypothesis simultaneously
- Top-rated metrics in `WMT` evaluation campaigns
- Better correlation with humans than n-gram metrics, but less interpretable
- Pair them with `BLEU` for backward comparability

---
## Evaluation Choice

![mt_evaluation](svg/courses/ai/natural-language-processing/16_machine_translation/mt_evaluation.svg)

---
## Domain Adaptation

- Fine-tune a generic checkpoint on in-domain bilingual data
- Even a few thousand sentences shift quality noticeably
- Backtranslation augments scarce parallel data with monoligual target text
- Glossary-based decoding constrains terminology in regulated domains
- Domain mismatch is the single biggest production-time risk

---
## Backtranslation

- Translate target-language monolingual data into the source language
- Use the synthetic source plus the real target as additional training data
- Surprisingly effective when parallel data is scarce
- Iterating multiple rounds compounds the gains
- A standard trick in low-resource and out-of-domain settings

---
## Document-Level Translation

- Sentence-by-sentence `NMT` loses cross-sentence cohesion
- Pronouns, terminology, and discourse markers drift across sentences
- Document-level models condition on prior context within a window
- Evaluation lags: most metrics only see one sentence at a time
- A growing area as `LLMs` translate full documents in context

---
## Quality Estimation

- Predict translation quality without a reference
- Used to triage outputs for human post-editing
- Trained on human ratings or synthetic perturbations of references
- The deployed counterpart of learned metrics like `COMET`
- Critical for production pipelines that route uncertain outputs to humans

---
## LLMs for Translation

- General-purpose `LLMs` translate competitively without `MT`-specific training
- Few-shot prompting matches dedicated systems on high-resource pairs
- Style transfer and tone control come almost for free
- Latency and cost are higher than dedicated `NMT` checkpoints
- The choice depends on volume, quality bar, and language coverage

---
## Hybrid Translation Stacks

- A specialized `NMT` model for high-volume bulk translation
- An `LLM` for hard sentences flagged by quality estimation
- Glossary lookup before decoding to lock terminology
- Post-editing tools that learn from human corrections
- Modern translation products are pipelines, not single models

---
## Common Production Pitfalls

- Mixing tokenizers between training and inference
- Reporting `BLEU` from different tokenizations and pretending they match
- Skipping length normalization in beam search
- Forgetting that subword vocabularies need to match the checkpoint
- Treating `MT` as solved when one direction works and the others do not

---
## Anti-Patterns

- Training on web-scraped pseudo-parallel data without quality filtering
- Reporting only single-reference `BLEU` on a tiny test set
- Ignoring document-level coherence in long-form translation
- Treating low-resource pairs as zero-shot without testing them
- Promising real-time translation without measuring tail latency

---
## Summary

- Machine translation evolved from rules to phrases to attention to transformers
- Modern `NMT` is transformer-based, often multilingual, and trained on web-scale data
- Evaluation requires multiple metrics — `BLEU`, `chrF`, and learned metrics together
- `LLMs` complement specialized `NMT` rather than replacing it everywhere
- The hard parts are no longer in core training — they live at the edges of production
