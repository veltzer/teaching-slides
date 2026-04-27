---
tags:
  - data-and-ai:nlp
  - concepts:linguistics
level: advanced
category: ai
audience:
  - audiences:developers
  - audiences:data-scientists

---
# Foundations of Natural Language

---
## What This Chapter Covers

- Why human language is hard for computers
- The classical levels of linguistic analysis
- A brief history of NLP from rules to large language models
- The major task families and where each lives in real systems
- A vocabulary the rest of the course will assume

---
## Why Language Is Hard

- Computers handle structured data well; language is the opposite of structured
- Every sentence is shaped by context the listener carries in their head
- Producers and consumers of language constantly negotiate meaning, often without noticing
- A system that processes language without modeling that negotiation will misread it

---
## Ambiguity at Every Level

- Lexical: a word can mean many things — `bank` is a financial institution or a riverside
- Syntactic: a sentence can be parsed many ways — "I saw the man with the telescope"
- Semantic: a phrase can refer to many entities — "the president" depends on the year
- Pragmatic: an utterance can do many things — "Can you pass the salt?" is a request

---
## The Levels of Ambiguity

![ambiguity_levels](svg/courses/ai/natural-language-processing/01_foundations_of_natural_language/ambiguity_levels.svg)

---
## Productivity and the Long Tail

- Speakers constantly invent expressions that no corpus has seen before
- Frequencies follow Zipf's law — a few words dominate, most words are rare
- Even billion-word corpora miss most of the words a real user might type
- Any model has to generalize past the training data, not memorize it

---
## Context Dependence

- "It's freezing in here" can be a complaint, a request to close a window, or a joke
- "She didn't go because she was tired" — who is `she`? The text alone may not say
- Resolving these references requires world knowledge or conversation history
- A system that ignores context will produce confidently wrong answers

---
## Variation Across Languages

- Word order varies wildly: English is SVO, Japanese is SOV, Welsh is VSO
- Morphology varies: Chinese has almost none, Finnish has dozens of cases
- Scripts vary: Latin, Cyrillic, Devanagari, Hangul, Han, Arabic, mixed
- A pipeline tuned for English may not survive contact with other languages

---
## Variation Within a Language

- Dialects: American vs British vs Indian English — same name, different vocabulary
- Registers: legal text vs Twitter vs lyrics — same language, different rules
- Time: medical English in 1920 is not medical English in 2026
- Code-switching: real users mix languages in a single sentence

---
## The Levels of Linguistic Analysis

- **Phonology**: sounds and how they combine
- **Morphology**: word structure — stems, affixes, inflection
- **Syntax**: sentence structure — phrase grammar, dependency
- **Semantics**: meaning of words and how they compose
- **Pragmatics**: meaning in context — what the speaker is doing
- **Discourse**: structure beyond a single sentence — coherence, reference

---
## The Levels in a Pipeline

![linguistic_levels](svg/courses/ai/natural-language-processing/01_foundations_of_natural_language/linguistic_levels.svg)

---
## Why The Classical Levels Still Matter

- Modern systems compress most of these levels into one neural network
- But the levels are still how we **describe** what is hard or easy
- Error analysis often comes back to "the model got the morphology right but the discourse wrong"
- Knowing the levels lets you talk precisely about failure modes

---
## How Modern Systems Compress the Levels

- A transformer does not have a "syntax module" — syntax emerges from training
- A large model encodes morphology, syntax, and semantics in overlapping ways
- The boundary between the levels softens, but the phenomena remain
- The vocabulary remains useful even when the implementation hides it

---
## A Brief History of NLP

- 1950s-1980s: symbolic and rule-based systems
- 1990s-2000s: statistical methods take over
- 2013-2017: deep learning, word embeddings, sequence models
- 2018-2020: pre-trained language models change the workflow
- 2020-present: large language models redefine what is possible

---
## The Symbolic Era

- Hand-written grammars and lexicons encoded linguistic knowledge directly
- Systems like SHRDLU could parse and respond to limited domains
- Brittle: rules covered narrow slices, edge cases multiplied
- Knowledge engineering bottleneck: every new domain needed expert authoring

---
## The Statistical Revolution

- Corpora became large enough to estimate distributions
- Hidden Markov Models dominated tagging; PCFGs covered parsing
- The IBM models for translation introduced data-driven alignment
- Performance improved without hand-coded grammars — but feature engineering was still heavy

---
## The Deep Learning Era

- Word embeddings (`Word2Vec`, `GloVe`) gave words dense, learnable representations
- Recurrent networks could model sequences directly
- Encoder-decoder architectures with attention reframed translation
- Hand-engineered features started to disappear

---
## The Pre-Trained Model Era

- `BERT`, `GPT`, `T5` introduced large models trained on raw text
- Downstream tasks reduced to fine-tuning a head on top
- Evaluation benchmarks were saturating one after another
- The standard NLP workflow shifted from "build a model" to "adapt a pretrained one"

---
## The Large Language Model Era

- Models grew from millions to billions of parameters
- Few-shot and zero-shot generalization emerged at scale
- Instruction tuning made models follow natural-language requests
- Many traditional NLP tasks became one prompt away

---
## A Timeline at a Glance

![nlp_timeline](svg/courses/ai/natural-language-processing/01_foundations_of_natural_language/nlp_timeline.svg)

---
## Each Era Did Not Erase the Last

- Production systems still use stemming, tokenization, and rule-based normalization
- Hidden Markov Models still beat neural models on some low-resource tagging
- `BM25` is competitive with neural retrieval on some benchmarks
- Treat each era as a layer of tools, not a generation to be replaced

---
## NLP Tasks at a Glance

- **Classification**: assign a label to a piece of text
- **Tagging**: label each token in a sequence
- **Parsing**: build structure (tree, graph) over a sentence
- **Generation**: produce new text given an input
- **Retrieval**: find relevant text in a large collection

---
## The Five Task Families

![task_families](svg/courses/ai/natural-language-processing/01_foundations_of_natural_language/task_families.svg)

---
## Where Classification Shows Up

- Sentiment analysis: positive vs negative reviews
- Spam detection: legitimate vs spam emails
- Topic classification: news article into a section
- Intent detection in dialogue: what is the user trying to do
- The same machinery underneath; the data and labels differ

---
## Where Tagging Shows Up

- Part-of-speech tagging: noun, verb, adjective per token
- Named entity recognition: which spans are people, organizations, locations
- Slot filling in dialogue: which words are the destination, the date
- Anything where the answer is "label every token"

---
## Where Parsing Shows Up

- Dependency parsing: subject-verb-object extraction
- Constituency parsing: sentence structure for downstream linguistics
- Relation extraction: who did what to whom in a sentence
- Less central in modern NLP — large models often skip explicit parsing

---
## Where Generation Shows Up

- Machine translation
- Summarization
- Question answering with free-form answers
- Dialogue response generation
- Code generation
- Anything where the output is text the model invents

---
## Where Retrieval Shows Up

- Search engines
- Open-domain question answering
- Retrieval-augmented generation (RAG)
- Recommendation over text content
- Often paired with generation: retrieve facts, then write an answer

---
## What This Course Will and Will Not Cover

- Will: the linguistic foundations, classical methods, deep learning, modern transformers, evaluation, deployment
- Will not: speech recognition (a different field), vision-language models (a course of their own)
- Will: enough to understand the field and build things
- Will not: an exhaustive survey of every paper

---
## What To Hold Onto

- Language is structured but the structure is fuzzy and contextual
- Ambiguity is the rule, not the exception
- The classical levels of analysis remain a shared vocabulary
- Each historical era left lasting tools
- The five task families cover most of what NLP systems do

---
## Anti-Patterns

- Treating English as if it were the only language
- Assuming a clean tokenization step exists for every script
- Skipping error analysis because "the metric went up"
- Confusing scale with understanding — a bigger model is not always smarter

---
## Summary

- NLP exists because human language resists structured processing
- The classical levels of analysis are still the vocabulary of failure modes
- Each era of NLP left tools that the next era still uses
- Five task families cover most production systems
- The rest of the course builds on this foundation
