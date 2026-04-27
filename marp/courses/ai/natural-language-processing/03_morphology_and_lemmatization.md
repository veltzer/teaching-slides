---
tags:
  - data-and-ai:nlp
  - concepts:morphology
level: advanced
category: ai
audience:
  - audiences:developers
  - audiences:data-scientists

---
# Morphology and Lemmatization

---
## What This Chapter Covers

- The internal structure of words: stems, roots, affixes, clitics
- Stemming algorithms and where they break down
- Lemmatization with dictionaries and morphological analyzers
- Languages where morphology dominates the design of the pipeline
- Compounds, decompounding, and when modern systems make morphology less urgent

---
## Why Morphology Matters

- A word is rarely a single atom of meaning
- Inflection, derivation, and compounding multiply surface forms
- Treating every form as a separate token wastes vocabulary and data
- Treating them as identical erases distinctions the model needs

---
## Morphemes: The Building Blocks

- A morpheme is the smallest unit that carries meaning
- `cats` = `cat` + `-s`; two morphemes, one word
- `unbelievable` = `un-` + `believe` + `-able`; three morphemes
- Morphemes can be free (stand alone) or bound (must attach)

---
## Stems, Roots, and Affixes

- A `root` is the irreducible core of a word: `believe`
- A `stem` is what affixes attach to: `believ-` in `believing`
- `affixes` are bound morphemes: prefixes, suffixes, infixes, circumfixes
- `clitics` are reduced forms that attach phonologically: `'s`, `'ll`, `n't`

---
## Morpheme Anatomy

![morpheme_anatomy](svg/courses/ai/natural-language-processing/03_morphology_and_lemmatization/morpheme_anatomy.svg)

---
## Inflectional Morphology

- Modifies a word for grammatical role without changing its category
- English nouns: `cat` / `cats`
- English verbs: `walk` / `walks` / `walked` / `walking`
- The lemma stays the same; the part of speech stays the same

---
## Derivational Morphology

- Builds new words, often changing the part of speech
- `happy` (adj) -> `happiness` (noun); `happy` -> `unhappy` (still adj)
- `nation` -> `national` -> `nationalize` -> `nationalization`
- Each step is a different lexeme, often with a separate dictionary entry

---
## Productive vs Unproductive Processes

- A `productive` process applies freely to new bases: `-ness` attaches to almost any adjective
- An `unproductive` process is frozen: `-th` in `warmth`, `width`, `length` no longer extends to new words
- Productivity is a gradient, not a binary
- Modern coinages (`tweetable`, `googled`) reveal which suffixes still travel

---
## Stemming: The Idea

- Reduce a surface form to a crude common shape
- `running`, `runs`, `ran` -> `run` (ideally)
- The output is not required to be a real word
- Fast, rule-based, language-specific, and lossy

---
## The Porter Stemmer

- The classic English stemmer; published by Martin Porter in 1980
- A cascade of suffix-stripping rules applied in fixed order
- `caresses` -> `caress` -> `caress`; `ponies` -> `poni`
- The output is often not a word, but it is consistent

---
## The Snowball Stemmer

- Porter's later framework for writing stemmers in many languages
- Provides stemmers for English, French, German, Spanish, Russian, and more
- Cleaner rules and better behavior than the original Porter algorithm
- Still rule-based, still produces non-words, still language-specific

---
## Stemming Limitations

- `Over-stemming`: collapses words that should differ (`university` and `universe` -> `univers`)
- `Under-stemming`: leaves related words apart (`alumnus` and `alumni`)
- Output is a token, not a real word: harder to read and harder to look up
- Rules tuned for one language behave badly on another

---
## Stemming vs Lemmatization

![stemming_vs_lemmatization](svg/courses/ai/natural-language-processing/03_morphology_and_lemmatization/stemming_vs_lemmatization.svg)

---
## Lemmatization: The Idea

- Reduce a word to its dictionary form, the `lemma`
- `running`, `runs`, `ran` -> `run`; `better` -> `good`
- The output is a real word; the part of speech is preserved
- Requires more knowledge: a lexicon, morphological rules, often the part of speech

---
## Dictionary-Based Lemmatization

- Look the surface form up in a table mapping every inflected form to its lemma
- Works well for languages with a small inflection inventory
- Misses unseen forms unless the lexicon is exhaustive
- Disambiguation by part of speech: `saw` (verb) -> `see`; `saw` (noun) -> `saw`

---
## Morphological Analyzers

- Two-level finite-state transducers map surface forms to lemma plus features
- `running` -> `run+V+PresPart`
- The same transducer runs in reverse for generation
- Industrial tools: `HFST`, `Foma`, `XFST`, language-specific analyzers

---
## WordNet and Lexical Resources

- `WordNet` groups English words into synsets of near-synonyms
- Each synset records part of speech, glosses, and links to related senses
- `WordNetLemmatizer` in `NLTK` uses the lexicon to lemmatize
- Sister resources exist for many languages (`OpenMultilingualWordNet`, `BabelNet`)

---
## A Lemmatization Snippet

```python
from nltk.stem import WordNetLemmatizer
lemma = WordNetLemmatizer()

lemma.lemmatize("running", pos="v")  # -> "run"
lemma.lemmatize("better",  pos="a")  # -> "good"
lemma.lemmatize("mice",    pos="n")  # -> "mouse"
```

- Without the part of speech, the lemmatizer falls back to noun
- Part-of-speech tagging usually runs before lemmatization

---
## Morphologically Rich Languages

- English has a tiny inflectional system: a handful of suffixes per word class
- Many languages express case, tense, person, mood, and politeness on a single word
- Vocabulary explodes; classical word-level pipelines struggle
- Tokenization, lemmatization, and modeling all change shape

---
## Agglutinative Languages

- Each grammatical feature is a separate, stackable suffix
- Finnish: `taloissamme` = `talo` (house) + `i` (plural) + `ssa` (in) + `mme` (our)
- Turkish and Hungarian work similarly; Korean and Japanese have related patterns
- A single word can express what English needs a whole phrase for

---
## Templatic Morphology

- Roots are consonant skeletons; vowels are interleaved by a pattern
- Arabic root `k-t-b` (writing): `kataba` (he wrote), `kitaab` (book), `maktab` (office)
- Hebrew, Amharic, Maltese share this template-based structure
- Surface forms hide the root unless an analyzer extracts it

---
## Morphologically Rich Languages

![morph_rich_languages](svg/courses/ai/natural-language-processing/03_morphology_and_lemmatization/morph_rich_languages.svg)

---
## Why Subword Tokenization Helps

- Subword tokenizers fragment rare inflected forms into recurring pieces
- A Finnish word with five suffixes becomes a sequence of subword tokens
- The model sees the same suffix repeatedly across thousands of stems
- Vocabulary stays bounded even when surface forms are unbounded

---
## Compounding

- Two or more roots combine into a single word
- German: `Donaudampfschifffahrtsgesellschaftskapitän`
- Dutch, Swedish, Finnish, and Greek share this pattern
- A single token may carry the meaning of a five-word English phrase

---
## Decompounding Strategies

- Split a compound into its parts before further processing
- Dictionary-based: greedy longest-match against a word list
- Statistical: language-model scoring of candidate splits
- Subword tokenizers do this implicitly; explicit decompounding still helps for retrieval

---
## A Decompounding Example

```diagram
input : Donaudampfschifffahrtsgesellschaft
split : Donau + dampf + schiff + fahrts + gesellschaft
gloss : Danube + steam + ship + travel + company
```

- A retrieval index over the parts matches queries about Danube steamships
- A surface-only index misses every variant

---
## Morphology in Modern NLP Systems

- Subword tokenization absorbs much of what classical morphology handled
- Large pretrained models learn morphological regularities from raw text
- Explicit lemmatization is rarely needed for end-to-end transformer pipelines
- The places it still helps: search, classical IR, low-resource languages

---
## When Morphology Still Matters

- Information retrieval: matching `runs` to a query for `run`
- Lexicography and linguistic research
- Low-resource languages with little pretrained coverage
- Morphologically rich languages where subword tokens correspond to morphemes

---
## When To Skip Lemmatization

- Modern transformers tokenize at subword level and learn inflection in their embeddings
- Lemmatizing before feeding a `BERT`-style model usually hurts more than it helps
- Search engines built on dense retrieval rarely need it
- Trust the tokenizer; reach for lemmatization only when measurement says you should

---
## Anti-Patterns

- Stemming once at training and lemmatizing at inference
- Lemmatizing without supplying part-of-speech tags
- Applying an English Porter stemmer to multilingual text
- Decompounding before subword tokenization, then re-merging differently

---
## Morphology and Information Retrieval

- Stemming and lemmatization expand recall: a query for `run` retrieves `runs` and `running`
- The cost is precision: `university` and `universe` may collapse
- Modern dense retrieval relies on contextual embeddings instead
- Hybrid systems combine sparse (lemmatized) and dense (embedded) signals

---
## Diagnosing Morphological Errors

- Inspect the lemma stream alongside the token stream
- Watch for false collapses: two unrelated words mapped to the same lemma
- Watch for missed collapses: clearly related forms left apart
- A small evaluation set of (form, lemma) pairs catches most regressions

---
## Tools Across Languages

- English: `NLTK`, `spaCy`, `Stanza`, `WordNet`
- Multilingual: `Stanza`, `spaCy`, `UDPipe`, `TreeTagger`
- Arabic: `MADAMIRA`, `Farasa`, `CAMeL Tools`
- Finnish, Turkish, Hungarian: dedicated morphological analyzers in `HFST`

---
## Morphology and Evaluation

- Lemmatization accuracy is measured against gold-standard lexicons
- `Universal Dependencies` provides annotated lemmas in dozens of languages
- Per-language evaluation is essential; an English-only score hides multilingual failures
- Errors cluster on rare or irregular forms, the ones that matter most for users

---
## Summary

- Morphology decomposes words into stems, affixes, and clitics
- Stemming is fast, lossy, and produces non-words; lemmatization is slower and produces real ones
- Morphologically rich languages reshape the pipeline; subword tokenization absorbs most of the difficulty
- Compounds need explicit splitting only outside subword pipelines
- In modern transformer systems, explicit morphology is rarely the bottleneck; reach for it deliberately
