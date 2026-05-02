---
tags:
  - data-and-ai:nlp
  - concepts:tokenization
level: advanced
category: ai
audience:
  - audiences:developers
  - audiences:data-scientists

---
# Text Preprocessing and Tokenization

---
## Tokenization Strategies

![tokenization](svg/courses/ai/natural-language-processing/02_text_preprocessing_and_tokenization/tokenization.svg)

---
## What This Chapter Covers

- Character encoding and the realities of `Unicode`
- Sentence and word segmentation across languages
- Subword tokenization: `BPE`, `WordPiece`, `SentencePiece`
- Normalization choices and their downstream effects
- Where preprocessing helps and where it silently destroys signal

---
## Why Preprocessing Matters

- Garbage in, garbage out — the metaphor is more literal here than elsewhere
- Tokens are what models actually see; getting them wrong corrupts everything downstream
- Many "model bugs" turn out to be preprocessing bugs
- The deeper the model, the easier it is to hide preprocessing mistakes — until production

---
## Character Encoding: The Foundation

- All text is bytes; encoding tells us which characters those bytes represent
- `UTF-8` is the modern default — variable-length, backward-compatible with ASCII
- Older encodings (`Latin-1`, `Shift-JIS`, `GB18030`) still appear in the wild
- A misidentified encoding produces silent corruption, not a hard error

---
## The Encoding Landscape

![encoding_landscape](svg/courses/ai/natural-language-processing/02_text_preprocessing_and_tokenization/encoding_landscape.svg)

---
## Unicode in Practice

- `Unicode` assigns each character a code point (e.g., U+00E9 for `e` with acute accent)
- A single visible character can be one or many code points
- The same visible string can have multiple internal representations
- Equality of "the same word" depends on which representation you compare

---
## Normalization Forms

- `NFC` — composed: each character is one code point where possible
- `NFD` — decomposed: base character plus combining marks
- `NFKC` and `NFKD` — also collapse compatibility characters
- Pick one and apply it everywhere; mixing them silently breaks string equality

---
## Common Encoding Pitfalls

- Invisible zero-width characters appear in copied text from rich editors
- Mixed scripts: Cyrillic `а` and Latin `a` look identical and are different code points
- Right-to-left marks reorder how text displays without changing the bytes
- Emoji modifiers and ZWJ sequences make a single grapheme span many code points

---
## Sentence Segmentation

- Splitting a paragraph into sentences sounds trivial; it isn't
- Punctuation-based rules fail on `Mr. Smith`, `i.e.`, `St. Paul`
- Statistical segmenters (e.g., `Punkt`) learn the abbreviation patterns from data
- Some languages don't use the same punctuation system at all

---
## Sentence Segmentation Across Languages

- Chinese and Japanese use different sentence-ending characters
- Thai writes without spaces between words and limited sentence punctuation
- Arabic uses different question and comma marks
- A pipeline tuned for English will misbehave silently on most other languages

---
## Word Tokenization

- Splitting a sentence into words sounds trivial; it isn't
- English: split on whitespace, then handle punctuation, contractions, hyphens
- Chinese, Japanese, Thai: no spaces — segmentation is a model in itself
- Arabic: rich morphology means a single token can carry several morphemes

---
## English Tokenization Edge Cases

- Contractions: `don't` → `do n't` or `don't` or `do not`?
- Hyphens: `state-of-the-art` is one term or four?
- URLs and emails: `john@example.com` should not be split on `@`
- Emoji and emoticons: `:-)` is one token or three?
- Hashtags and mentions: `#NLP` and `@user` are first-class on social media

---
## Subword Tokenization Motivation

- Word-level vocabularies are huge and miss rare words
- Character-level vocabularies are tiny but lose word structure
- Subword tokenization sits between: a vocabulary of frequent fragments
- Out-of-vocabulary tokens disappear — every input is representable

---
## Byte-Pair Encoding

- Start with characters as the initial vocabulary
- Repeatedly merge the most frequent adjacent pair into a new token
- Stop when the vocabulary reaches the desired size
- The result: common words become single tokens; rare words split into pieces

---
## BPE Walkthrough

```diagram
corpus: low low lower newest widest
init  : l o w </w>  l o w </w>  l o w e r </w>
merge1: lo (most frequent pair)
merge2: low
merge3: ne, then nest
final : low, lower, newest, widest as compact tokens
```

- Each merge captures a piece of recurring structure
- Final vocabulary mixes characters, common subwords, common whole words

---
## WordPiece

- Same idea as `BPE`; different scoring function
- Merges the pair that maximizes the likelihood of the training corpus
- Used by `BERT` and many of its descendants
- A `##` prefix marks subword continuations: `playing` → `play ##ing`

---
## SentencePiece

- Treats raw text as a sequence of bytes — no preliminary whitespace splitting
- Learns the vocabulary including the space character itself
- Works the same way for English, Chinese, and code
- The default for many multilingual models (`mT5`, `XLM-RoBERTa`)

---
## Subword Tokenizers Compared

![subword_tokenizers](svg/courses/ai/natural-language-processing/02_text_preprocessing_and_tokenization/subword_tokenizers.svg)

---
## Unigram Language Model Tokenization

- Starts with a large vocabulary of subwords and prunes
- Each token has a probability under a unigram language model
- Pruning removes the tokens whose loss penalty is smallest
- Used by `SentencePiece` in unigram mode; gives multiple valid tokenizations of the same string

---
## Vocabulary Size Trade-offs

- Small vocabulary: more tokens per sentence, longer sequences, less memorization
- Large vocabulary: fewer tokens per sentence, shorter sequences, larger embedding tables
- Typical sizes: 30k for `BERT`, 50k for `GPT-2`, 100k+ for modern multilingual models
- The right size depends on languages, scripts, and downstream sequence length

---
## Tokenization at Inference

- The same tokenizer used in training must be used at inference
- A vocabulary mismatch corrupts inputs in subtle ways
- Tokenizers are versioned alongside model weights — keep them paired
- Custom preprocessing on top of a pretrained tokenizer is almost always a mistake

---
## Tokenizer Pipeline

![tokenizer_pipeline](svg/courses/ai/natural-language-processing/02_text_preprocessing_and_tokenization/tokenizer_pipeline.svg)

---
## Normalization: Case Folding

- Lowercasing was a default in classical NLP
- Modern subword tokenizers often keep case — `Apple` and `apple` differ
- The right choice depends on whether case carries meaning in your domain
- Mixed: lowercase queries, preserve case in entities

---
## Normalization: Accent and Diacritic Handling

- Stripping accents: `café` → `cafe`
- Helpful for noisy user input, harmful for languages where accents distinguish words
- French `ou` (or) vs `où` (where) — stripping the accent merges them
- Decide per language and per task

---
## Stop Words

- Frequent function words: `the`, `a`, `of`, `is`
- Removing them reduces dimension and noise for some classical methods
- Modern transformers benefit from keeping them — they carry syntactic information
- Stop word lists are language-specific and domain-specific

---
## Spelling Correction as Preprocessing

- Helpful for noisy text from search queries or social media
- Risky: corrects domain-specific terms into common English words
- Modern subword tokenizers absorb misspellings into their normal token stream
- Use with care; measure the downstream effect, not just the surface accuracy

---
## A Complete Preprocessing Pipeline

```python
def preprocess(text: str) -> list[int]:
    text = unicodedata.normalize("NFC", text)
    text = text.replace("​", "")
    text = text.casefold() if lowercase else text
    tokens = tokenizer.encode(text)
    return tokens
```

- Each step is explicit; each step is reversible enough for debugging
- Same code path at training and inference

---
## Detokenization

- Going from tokens back to readable text
- Subword tokenizers know how to glue pieces back together
- Spaces, casing, and special tokens (`<bos>`, `<eos>`) need explicit handling
- A round-trip test (text → tokens → text) catches many bugs

---
## Preprocessing Anti-Patterns

- Different normalization in training and inference — silent quality drop
- Stripping characters the model needs to see (newlines, punctuation, casing)
- Over-aggressive stop-word removal that erases sentence structure
- "Just lowercase everything" without checking the script

---
## When To Skip Preprocessing

- Modern large models often perform better on raw text than aggressively cleaned text
- Casing, punctuation, and numbers all carry signal a strong model can use
- Skip the cleaning unless you have measured evidence that it helps
- Trust the tokenizer to do its job

---
## Diagnosing Tokenization Issues

- Inspect the token stream — print what the model actually sees
- Watch for excessive splitting on a domain term — add it to the vocabulary if needed
- Watch for the same word producing different token sequences in different contexts
- Tokenization debugging is unglamorous and often the highest-impact fix

---
## Token Counts and Costs

- Many APIs charge per token — tokenization decisions become billing decisions
- Languages tokenize at very different rates
- Code, math, and structured text often inflate token counts
- Always measure tokens per sentence on your real data

---
## Tokens Per Language

![tokens_per_language](svg/courses/ai/natural-language-processing/02_text_preprocessing_and_tokenization/tokens_per_language.svg)

---
## Special Tokens

- Models reserve a few tokens for structural roles: `<bos>`, `<eos>`, `<pad>`, `<sep>`, `<unk>`
- Use them only as documented; user text containing them is usually escaped or stripped
- Never feed `<eos>` into the middle of a sequence the model expects to continue
- Special tokens are part of the vocabulary; they have weights

---
## Anti-Patterns Summary

- Mixing normalization forms across components
- Tokenizing with one tokenizer, embedding with another
- "Cleaning" data into uselessness
- Ignoring multilingual realities until non-English data shows up

---
## Summary

- Encoding and normalization choices are quiet but consequential
- Subword tokenization is the modern default and resolves the OOV problem
- Vocabulary size, normalization form, and special tokens are versioned with the model
- Diagnose tokenization first when a model misbehaves on a specific domain
- Trust tokenizers; do not preprocess around them
