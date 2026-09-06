---
tags:
  - data-and-ai:nlp
  - concepts:pos-tagging
  - concepts:sequence-labeling
level: advanced
category: ai
audience:
  - audiences:developers
  - audiences:data-scientists

---

# Part-of-Speech Tagging

---

## What This Chapter Covers

- POS tagging concepts and tag set design
- Classical taggers: rule-based, `HMM`, and the Brill transformation-based approach
- Neural taggers: character-level features, transformers, multi-task setups
- Evaluation, error analysis, and out-of-vocabulary tokens
- POS tagging across morphologically rich and low-resource languages

---

## Why Part-of-Speech Tagging Still Matters

- A foundational sequence labeling task — every word gets a syntactic category
- Feeds parsing, named entity recognition, and information extraction
- A useful diagnostic when end-to-end models behave oddly
- Cheap, fast, and surprisingly informative for downstream features

---

## What a POS Tagger Produces

- Input: a tokenized sentence
- Output: one tag per token, drawn from a fixed inventory
- Example: `the/DET cat/NOUN sleeps/VERB ./PUNCT`
- The tag inventory is the design choice that shapes everything else

---

## Universal Dependencies Tag Set

- A coarse, language-agnostic inventory of seventeen tags
- Categories like `NOUN`, `VERB`, `ADJ`, `ADV`, `DET`, `ADP`, `PRON`
- Function categories like `AUX`, `CCONJ`, `SCONJ`, `PART`, `INTJ`
- Symbol categories like `PUNCT`, `SYM`, `NUM`, `X`
- Designed for cross-lingual consistency, not linguistic depth

---

## Language-Specific Fine-Grained Tags

- Penn Treebank uses 36 tags for English alone
- Distinguishes verb forms: `VB`, `VBD`, `VBG`, `VBN`, `VBP`, `VBZ`
- Captures subtle distinctions: `NN` versus `NNS` versus `NNP`
- Many treebanks add morphological features beyond the bare tag

---

## Tag Set Design Trade-offs

- Coarse tags are easier to learn and easier to evaluate consistently
- Fine tags capture more linguistic structure but suffer from data sparsity
- Cross-lingual systems prefer coarse tags
- Monolingual production systems often want the fine ones

---

## Tag Set Comparison

![tag_set_comparison](svg/courses/ai/natural-language-processing/12_part_of_speech_tagging/tag_set_comparison.svg)

---

## Tagging as Sequence Labeling

- Each token gets a label that depends on its context, not just its form
- The same word can take different tags: `book/NOUN` versus `book/VERB`
- Decisions are correlated — adjacent tags follow grammatical patterns
- Joint decoding over the whole sentence beats independent per-token guesses

---

## Ambiguity Is the Whole Problem

- Most frequent English words have more than one possible tag
- `that` can be `DET`, `PRON`, or `SCONJ` depending on context
- `running` can be `VERB`, `ADJ`, or `NOUN`
- Local context usually disambiguates; sometimes long-range context is required

---

## Rule-Based Tagging

- Hand-written rules of the form "if context matches, assign tag"
- Lexicon plus disambiguation rules: `ENGTWOL` and similar systems
- Excellent precision when the rules fit; brittle when they do not
- Still useful as a baseline and for low-resource languages with grammars but no data

---

## Hidden Markov Model Tagging

- Tags are hidden states; words are observations
- Transition probability `P(tag_i | tag_{i-1})` captures grammar
- Emission probability `P(word_i | tag_i)` captures lexical preferences
- Viterbi decoding finds the most likely tag sequence in linear time

---

## HMM in Practice

```python
def viterbi(words, tags, transition, emission):
    V = [{}]
    for t in tags:
        V[0][t] = transition["<s>"][t] * emission[t].get(words[0], 1e-9)
    for i in range(1, len(words)):
        V.append({})
        for t in tags:
            V[i][t] = max(
                V[i-1][p] * transition[p][t] * emission[t].get(words[i], 1e-9)
                for p in tags
            )
    return V
```

- Smoothing the emission probabilities is the difference between working and useless
- Unknown words need a fallback distribution

---

## The Brill Tagger

- Start with a baseline: tag each word with its most frequent tag
- Learn transformation rules that fix systematic errors on training data
- Each rule has a trigger context and a tag change to apply
- Apply the learned rules in order at inference

---

## Transformation-Based Learning

- Greedy: at each step pick the rule that reduces error the most
- Rules are interpretable — humans can read and audit them
- A typical rule: "change `NN` to `VB` if the previous tag is `TO`"
- Slow to train, fast to apply, transparent to debug

---

## Classical Taggers Compared

![classical_taggers](svg/courses/ai/natural-language-processing/12_part_of_speech_tagging/classical_taggers.svg)

---

## Why Neural Taggers Won

- Hand-crafted features cap at the imagination of the engineer
- Neural models learn rich token representations from raw text
- Bidirectional context becomes free with `BiLSTM` or transformer encoders
- Subword and character signals dissolve the unknown-word problem

---

## Character-Level Features

- Word embeddings miss the morphology inside the word
- A character-level encoder reads the letters of each token in turn
- Captures suffixes like `-ing`, `-ed`, `-ly` automatically
- The character vector concatenates with the word vector before tagging

---

## BiLSTM Tagger Architecture

- Embed each token, optionally with character features
- Run a bidirectional `LSTM` over the embedded sequence
- Project each hidden state to tag-space logits
- Decode greedily or with a `CRF` layer on top

---

## CRF Decoding Layer

- A linear-chain `CRF` learns transition scores between tag pairs
- Discourages illegal sequences like `DET` followed by `DET`
- Decoding still uses Viterbi over the learned scores
- Trained jointly with the encoder — backprop through the dynamic program

---

## Transformer-Based Taggers

- Replace the `BiLSTM` with a pretrained transformer encoder
- Each subword gets a contextual vector; project the first subword of each word
- Fine-tune end-to-end with a small classification head
- State of the art on most languages with small effort

---

## Subword Alignment

- Tokenizers split words; tags are assigned per word
- Train and predict on the first subword of each token, ignore the rest
- Or pool subword representations and predict per word
- The alignment code is unglamorous but easy to get wrong

---

## Multi-Task Tagging

- Joint training of POS, morphology, and sometimes parsing
- Shared encoder, separate heads per task
- Auxiliary tasks regularize and improve the main task
- Common in modern toolkits like `Stanza`, `Trankit`, `spaCy`

---

## Neural Tagger Architecture

![neural_tagger](svg/courses/ai/natural-language-processing/12_part_of_speech_tagging/neural_tagger.svg)

---

## Token Accuracy

- Fraction of tokens tagged correctly
- The default headline metric; easy to compute and easy to report
- Strong English models reach 97 percent and above
- Modest absolute gains hide a lot of qualitative improvement

---

## Sentence Accuracy

- Fraction of sentences with every token tagged correctly
- Far more demanding — one mistake fails the whole sentence
- Useful for tasks that consume tag sequences as a whole
- Often sits in the 50 to 70 percent range even for excellent models

---

## Confusion Analysis

- Which tag pairs does the model swap most often?
- Common confusions: `NN` versus `JJ`, `VBN` versus `VBD`, `IN` versus `RB`
- A confusion matrix often reveals tag set ambiguities, not model bugs
- Fixing the data label guideline beats tweaking the model

---

## Out-of-Vocabulary Tokens

- Words the tagger never saw during training
- Rule of thumb: accuracy drops by 5 to 15 points on unseen tokens
- Character features and subword tokenizers shrink the gap
- Track OOV accuracy separately from overall accuracy

---

## Error Analysis Workflow

- Bucket errors by tag, by frequency, by sentence length, by domain
- Sample misclassified sentences and read them
- Distinguish annotation errors from model errors
- Most production gains come from cleaning the data, not retraining

---

## Morphologically Rich Languages

- Turkish, Finnish, Hungarian, Arabic, Russian — many forms per lemma
- A single token carries person, number, tense, case, and more
- Pure POS tagging undersells the linguistic content
- Joint POS plus morphological feature tagging is standard practice

---

## Low-Resource Languages

- Few hundred to few thousand tagged sentences, if any
- Cross-lingual transfer from related high-resource languages helps
- Multilingual encoders like `XLM-RoBERTa` give a strong starting point
- Annotation projection from parallel text is a useful supplement

---

## Cross-Lingual Tagger Approaches

- Train on a high-resource source, evaluate on a low-resource target
- Universal Dependencies tags make the source and target labels comparable
- Add a few hundred target-language examples and accuracy jumps
- The Universal Dependencies treebanks were built for this kind of work

---

## When To Use POS Tags Today

- As features for downstream classifiers when data is small
- As filters: extract noun phrases, count verbs, find adjectives
- As regularization signal in multi-task training
- As a debugging aid when something downstream looks wrong

---

## When Not To Bother

- End-to-end neural models often need no explicit tags
- A pretrained transformer encodes syntactic information internally
- Adding POS features rarely helps a strong model and can hurt
- Use POS when the consumer is a rule-based system or a feature-based classifier

---

## Anti-Patterns

- Mixing tag sets across training and evaluation
- Reporting only token accuracy and ignoring OOV behavior
- Training on news, deploying on tweets, hoping for the best
- Treating fine-grained tags as if they were coarse without remapping

---

## Summary

- POS tagging is the canonical sequence labeling task
- Tag set choice matters more than model architecture for many problems
- Neural taggers with character or subword features are the default
- Evaluate token and sentence accuracy and inspect the confusion matrix
- Multilingual taggers built on Universal Dependencies open up low-resource work
