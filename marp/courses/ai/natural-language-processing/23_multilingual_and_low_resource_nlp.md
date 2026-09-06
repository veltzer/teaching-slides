---
tags:
  - data-and-ai:nlp
  - concepts:multilingual
level: advanced
category: ai
audience:
  - audiences:developers
  - audiences:data-scientists

---

# Multilingual and Low-Resource NLP

---

## What This Chapter Covers

- The shape of the world's languages and where data lives
- Multilingual models from `mBERT` to `XLM-R` to `NLLB` and beyond
- Cross-lingual transfer and the surprises that emerge
- Low-resource techniques: backtranslation, weak supervision, data augmentation
- Tokenization and morphology in non-English settings
- Evaluation that survives across languages and writing systems

---

## Why This Matters

- More than 7000 living languages; `NLP` covers a small fraction well
- The economic and informational value of `NLP` is concentrated in a few languages
- The technical interest is in what happens when data runs out
- Cross-lingual transfer is one of the cleanest "free lunch" stories in `NLP`
- Bias, equity, and access shape what gets built

---

## The Long Tail of Languages

![language_long_tail](svg/courses/ai/natural-language-processing/23_multilingual_and_low_resource_nlp/language_long_tail.svg)

---

## High-Resource vs Low-Resource

- High-resource: English, Mandarin, Spanish, Arabic, French, German
- Mid-resource: Hindi, Vietnamese, Indonesian, Polish, Turkish
- Low-resource: most African, Indigenous Australian, Pacific languages
- The line moves: today's low-resource is tomorrow's mid-resource if data appears
- The right architecture depends on which side of the line you are on

---

## Why English Dominates Datasets

- Web scale plus historical accidents of computing infrastructure
- Annotation labor markets concentrated in English-speaking communities
- Benchmark culture entrenched English first
- This is structural, not natural — it shapes what models are good at
- The cost falls disproportionately on speakers of underrepresented languages

---

## Tokenization Across Languages

- English-trained `BPE` produces excessive splits on many other languages
- Tokens-per-word varies by orders of magnitude across writing systems
- Models trained mostly on English over-fragment Korean, Tamil, Amharic
- Multilingual `SentencePiece` reduces but does not eliminate the gap
- Cost and accuracy both suffer when tokenization is mismatched

---

## Tokens per Language

- 1 English word ≈ 1 to 1.3 tokens with English-tuned `BPE`
- 1 Hindi word ≈ 2 to 3 tokens with the same tokenizer
- 1 Burmese or Tibetan word ≈ 5 to 10 tokens or more
- Long-tail languages pay double: more tokens, less training data
- An overlooked fairness issue in `LLM` pricing

---

## Multilingual BERT

- Trained on Wikipedia in 104 languages with shared subword vocabulary
- No explicit cross-lingual supervision — alignment emerges from joint training
- Good zero-shot transfer to many tasks, weaker on truly low-resource languages
- The first widely usable multilingual encoder
- Largely superseded by `XLM-R`

---

## XLM-R

- Trained on `CommonCrawl` in 100 languages with much more data per language
- Substantially stronger transfer than `mBERT`
- Standard backbone for many multilingual classification tasks
- Vocabulary still skewed toward European and East Asian languages
- A de facto baseline for non-English encoder tasks

---

## Cross-Lingual Transfer

![cross_lingual_transfer](svg/courses/ai/natural-language-processing/23_multilingual_and_low_resource_nlp/cross_lingual_transfer.svg)

---

## Zero-Shot Transfer

- Fine-tune on a high-resource language, evaluate on others
- Surprisingly strong for many classification and labeling tasks
- The model never saw labeled data in the target language
- Works because shared embeddings carry cross-lingual structure
- Fails on language-specific phenomena like morphology and word order

---

## Few-Shot Transfer

- Add a small number of target-language examples to the fine-tune
- A few hundred examples often closes most of the cross-lingual gap
- Active learning chooses which examples to annotate
- The pragmatic middle ground for production systems
- Cheaper than full localization, more reliable than zero-shot

---

## Translation as Augmentation

- Translate high-resource training data into the target language
- Train on the translation; evaluate on real target-language test data
- Quality of translation determines how much this helps
- Often more effective than pure zero-shot transfer
- Can introduce translation artifacts the model latches onto

---

## Backtranslation in Low-Resource MT

- Translate target-language monolingual text into the source
- Pair with the original target text to create synthetic parallel data
- Standard trick to bootstrap `MT` from monolingual corpora
- Works because monolingual data is much easier to find
- Iterating multiple rounds compounds the gains

---

## Backtranslation Loop

![backtranslation_loop](svg/courses/ai/natural-language-processing/23_multilingual_and_low_resource_nlp/backtranslation_loop.svg)

---

## Multilingual NMT

- One model translates between many language pairs
- Shared parameters help low-resource directions inherit from high-resource ones
- `M2M-100`, `NLLB-200` cover 100+ and 200+ languages respectively
- Quality is uneven; the head dominates training
- Per-direction fine-tuning often improves a chosen low-resource pair

---

## NLLB and the African Languages Push

- `No Language Left Behind` targeted 200+ languages including many African ones
- Curated bitext from human translators and aligned monolingual data
- Substantially improved translation for previously unsupported languages
- Showed that scale plus careful data curation extends coverage
- Still a long tail of completely unserved languages

---

## Massively Multilingual LLMs

- Modern `LLMs` train on data from many languages without explicit balancing
- Strong performance on widely-spoken languages, weaker further down the tail
- Few-shot prompting in any language often works for major tasks
- Code-switching is sometimes handled implicitly
- Quality varies wildly by language and task — always test on your target

---

## Code-Switching

- Speakers mix two or more languages within a single utterance or sentence
- Common in many bilingual communities (Hinglish, Spanglish, Singlish)
- Tokenizers and models trained on monolingual data fail badly
- A growing area of research with `LLMs` showing surprising competence
- Annotation is hard because conventions for tagging code-switched data vary

---

## Morphologically Rich Languages

- Finnish, Turkish, Arabic, Hindi, Tamil have rich inflection and agglutination
- One word can carry information that English uses several words for
- Subword tokenization helps but does not solve the problem
- Morphologically aware tokenizers (`SentencePiece` with high vocab) work better
- A reminder that "natural language" is not a homogeneous thing

---

## Writing Systems and Scripts

- Latin, Cyrillic, Greek, Devanagari, Arabic, Hangul, CJK ideographs
- Right-to-left scripts need special tokenization and rendering
- Logographic scripts need different vocabulary sizes
- Mixed-script content (Latin code in Devanagari prose) complicates everything
- Modern Unicode handling is necessary but not sufficient

---

## Low-Resource Data Sources

- Religious texts, especially Bible translations, exist in thousands of languages
- News in major outlets is often translated to dozens of languages
- Government and NGO documents bridge official languages
- Crowdsourced platforms like `Common Voice` cover speech
- Each source has biases that show up in trained models

---

## Weak Supervision

- Use heuristics to label data when human annotators are scarce
- `Snorkel` and similar frameworks combine multiple weak signals
- A handful of labeling functions can produce thousands of training examples
- Quality is lower than human annotation but coverage is wider
- A practical bridge for low-resource languages

---

## Active Learning

- Use a model's uncertainty to choose what to annotate next
- Annotators focus on the most informative examples
- Reduces annotation cost by 5-10x in many setups
- Effective when data is plentiful but labels are not
- Requires a working model already to bootstrap

---

## Data Augmentation Techniques

- Token replacement using language-specific lexicons
- Backtranslation through a pivot language
- `EDA`: random swap, deletion, insertion at the token level
- Paraphrase generation with an existing `LLM`
- Augmentation needs to be tested per language — what works in English often does not transfer

---

## Multilingual Evaluation

- `XNLI`, `XCOPA`, `XQuAD` benchmark cross-lingual `NLU`
- `FLORES-200` benchmarks `MT` across 200 languages
- `Universal Dependencies` benchmarks parsing across 100+ languages
- Many languages still have no benchmark at all
- Average scores hide enormous per-language variance

---

## Bias in Multilingual Systems

- Translation systems sometimes mistranslate gender across languages
- Cultural references break under literal translation
- Class and dialect markers vary by language and rarely transfer
- Names, food, and concepts encode different connotations
- Auditing requires speakers of each target language, not just developers

---

## Practical Multilingual Engineering

- Test on real target-language data, not translated benchmarks
- Validate tokenization quality before training or fine-tuning
- Budget more compute and data per low-resource language, not less
- Pair native speakers with `NLP` engineers for quality control
- Plan for ongoing data collection, not a one-shot release

---

## Common Production Pitfalls

- Shipping English-tuned models to non-English markets without retesting
- Underestimating tokenization cost in token-priced APIs
- Treating zero-shot transfer as a free pass on quality
- Using machine-translated benchmarks and reporting them as authentic evaluation
- Ignoring code-switching in markets where it is the norm

---

## Anti-Patterns

- "Multilingual" features that only support five European languages
- Quality gates measured only on the highest-resource language
- Single tokenizer for radically different writing systems
- Evaluation pipelines that crash on right-to-left scripts
- Treating low-resource languages as low-priority rather than high-leverage

---

## Summary

- The world's languages are unevenly served by `NLP` data and tools
- Cross-lingual transfer makes high-resource models partially usable elsewhere
- Backtranslation and weak supervision extend coverage to low-resource settings
- Tokenization, morphology, and scripts demand language-specific care
- Evaluation must be per-language and per-domain, never just an average
