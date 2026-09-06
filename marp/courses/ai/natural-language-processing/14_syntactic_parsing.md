---
tags:
  - data-and-ai:nlp
  - concepts:parsing
level: advanced
category: ai
audience:
  - audiences:developers
  - audiences:data-scientists

---

# Syntactic Parsing

---

## What This Chapter Covers

- Constituency parsing and phrase-structure grammars
- Dependency parsing and Universal Dependencies
- Transition-based and graph-based parsing algorithms
- Neural parsers from stack `LSTM` to biaffine attention
- Extracting structured information from parse trees
- Evaluation metrics that survive cross-corpus comparison

---

## Why Parse Syntax At All

- Tokenization gives us words; tagging gives us labels; parsing gives us structure
- Many downstream tasks need to know who did what to whom
- Relation extraction, question answering, and grammar checking all benefit
- Modern transformers learn syntax implicitly, but explicit parses remain useful for audit and control

---

## Two Views of Syntax

- Constituency: sentences are nested phrases (NP inside VP inside S)
- Dependency: sentences are head-and-modifier relations between words
- Both views capture useful structure; they emphasize different things
- Modern pipelines lean toward dependency for its compactness and cross-lingual portability

---

## Two Views Compared

![constituency_vs_dependency](svg/courses/ai/natural-language-processing/14_syntactic_parsing/constituency_vs_dependency.svg)

---

## Phrase-Structure Grammars

- A phrase-structure grammar rewrites a non-terminal into a sequence of symbols
- `S -> NP VP`, `NP -> Det N`, `VP -> V NP`
- The terminals are the words; the non-terminals are phrase categories
- A parse tree is a derivation that yields the input sentence

---

## Context-Free Grammars

- A `CFG` is a tuple of non-terminals, terminals, productions, and a start symbol
- Each production rewrites a single non-terminal independently of context
- Real natural language is not exactly context-free, but `CFG` is a useful approximation
- Most parsing algorithms assume the grammar is in Chomsky Normal Form

---

## Chomsky Normal Form

- Every production is either `A -> B C` or `A -> a`
- Any `CFG` can be converted to `CNF` with the same language
- The transformation preserves derivations modulo bookkeeping
- `CNF` makes dynamic programming over spans clean to express

---

## The CKY Algorithm

- Bottom-up parsing for grammars in Chomsky Normal Form
- Fill a chart indexed by spans; entry `chart[i][j]` lists symbols deriving `words[i:j]`
- For each split point, combine compatible left and right symbols using productions
- Time is cubic in sentence length, quadratic in grammar size

---

## CKY In Pseudocode

```python
def cky(words, grammar):
    n = len(words)
    chart = [[set() for _ in range(n + 1)] for _ in range(n + 1)]
    for i, w in enumerate(words):
        for A in grammar.preterminals(w):
            chart[i][i + 1].add(A)
    for span in range(2, n + 1):
        for i in range(n - span + 1):
            j = i + span
            for k in range(i + 1, j):
                for A, B, C in grammar.binary_rules():
                    if B in chart[i][k] and C in chart[k][j]:
                        chart[i][j].add(A)
    return grammar.start in chart[0][n]
```

---

## Probabilistic CFGs

- Each production carries a probability conditioned on its left-hand side
- The probability of a tree is the product of the probabilities of its productions
- Train by counting productions in a treebank and normalizing
- Decode by scoring all trees and returning the most probable one

---

## PCFG Decoding With CKY

- Replace set union with max over scored derivations
- `chart[i][j][A]` stores the best score for deriving `A` over the span
- Backpointers record which split and which child symbols achieved that score
- Reconstruct the tree by following backpointers from the root span

---

## Limits of Vanilla PCFGs

- Independence assumptions are too strong; lexical preferences are lost
- Lexicalization attaches a head word to each non-terminal to recover them
- Latent-variable grammars split categories into finer subtypes automatically
- Even so, neural parsers eventually overtook all hand-engineered variants

---

## Dependency Parsing Basics

- A dependency parse is a directed tree over the words of a sentence
- Each word has exactly one head; the root has a synthetic root pseudo-token
- Edges carry labels naming the syntactic relation (subject, object, modifier)
- The tree captures who modifies what without intermediate phrase nodes

---

## Universal Dependencies

- A cross-lingual annotation standard with a shared inventory of labels
- Common labels: `nsubj`, `obj`, `iobj`, `amod`, `nmod`, `advmod`, `det`, `aux`, `mark`
- The same dependency scheme applies across more than a hundred languages
- Treebanks are released yearly; the same parser code can train on any of them

---

## A UD Example

```diagram
The quick brown fox jumps over the lazy dog
   det   amod  amod nsubj root  case  det amod obl
fox -det-> The
fox -amod-> quick
fox -amod-> brown
jumps -nsubj-> fox
dog -case-> over
dog -det-> the
dog -amod-> lazy
jumps -obl-> dog
```

---

## Projective Versus Non-Projective

- A parse is projective if dependency arcs do not cross when drawn above the sentence
- English is mostly projective; freer-word-order languages are often not
- Many efficient algorithms assume projectivity and break on languages that violate it
- Non-projective parsers handle the general case at extra computational cost

---

## Crossing Arcs

![projective_vs_nonprojective](svg/courses/ai/natural-language-processing/14_syntactic_parsing/projective_vs_nonprojective.svg)

---

## Transition-Based Parsing

- Build the parse incrementally with a buffer of remaining words and a stack
- A small set of transitions either shift a word, attach a head, or attach a dependent
- A classifier picks the next transition from the current configuration
- Linear time in the sentence length; greedy or beam decoding

---

## Arc-Standard Transitions

- `SHIFT`: move the front of the buffer onto the stack
- `LEFT-ARC(label)`: attach the second-stack item as a dependent of the top, then pop the second
- `RIGHT-ARC(label)`: attach the top of the stack as a dependent of the second, then pop the top
- A correct sequence of transitions yields a projective parse

---

## Arc-Eager Transitions

- Adds `REDUCE`, which pops the stack when its top has a head
- `RIGHT-ARC` becomes non-popping so further dependents can still attach
- Encodes attachment decisions earlier than arc-standard
- A common default for high-throughput dependency parsers

---

## Transition Parser Loop

```python
def parse(words, classifier):
    config = Config(stack=[ROOT], buffer=list(words), arcs=[])
    while not config.is_terminal():
        action = classifier.predict(config)
        config = action.apply(config)
    return config.arcs
```

- Each step is a feature extraction plus a classifier call
- Errors compound; a bad shift early on cannot be undone in greedy mode

---

## Graph-Based Parsing

- Score every possible head-dependent edge in the sentence
- Search for the highest-scoring spanning tree over those scores
- For projective parses, the Eisner algorithm finds the optimum in cubic time
- For non-projective parses, Chu-Liu-Edmonds finds the maximum spanning tree

---

## Maximum Spanning Tree Parsers

- Build a complete directed graph over the words plus the root
- Edge weights come from a learned scoring function
- Run a maximum spanning tree algorithm to extract the best parse
- Naturally handles non-projective trees with no extra machinery

---

## Biaffine Attention Parsers

- Two `MLP`s project each token into head and dependent representations
- A bilinear form scores every (head, dependent) pair
- A separate biaffine head scores the label for each chosen edge
- Dozat and Manning showed this beats earlier transition-based parsers on `UD`

---

## Biaffine Scoring

![biaffine_parser](svg/courses/ai/natural-language-processing/14_syntactic_parsing/biaffine_parser.svg)

---

## Stack LSTM Parsers

- An older neural transition-based parser that encodes the stack with an `LSTM`
- A separate `LSTM` encodes the buffer; another encodes the action history
- Concatenated states feed a classifier that picks the next transition
- Elegant idea, but biaffine graph-based parsers won the accuracy race

---

## Transformer-Based Parsing

- Replace the encoder of a biaffine parser with a pretrained transformer
- Token embeddings come from `BERT`, `RoBERTa`, or a multilingual variant
- Per-token contextual vectors feed the same biaffine head as before
- Current state-of-the-art parsers across most `UD` treebanks

---

## Subject-Verb-Object Extraction

- Find the verb token whose head is `ROOT`
- Walk its dependents; the `nsubj` child is the subject, the `obj` child is the object
- Optionally include `obl` and clausal complements for richer extractions
- A parse-driven `SVO` extractor is more robust than regex on real text

---

## Relation Extraction With Parse Paths

- Connect two entities by the shortest path of dependency edges between them
- The path tokens and labels become features for a relation classifier
- Captures syntactic relationships that surface order alone misses
- Especially useful when entities are far apart in the sentence

---

## Linguistic Queries Over Parsed Text

- Tools like `Semgrex` and `grew-match` run patterns over dependency trees
- A query says "find a verb whose subject is a person and whose object is an organization"
- Parse-aware search powers legal, medical, and scientific text mining
- Faster than running a full relation extractor on every sentence

---

## Evaluation: Attachment Scores

- Unlabeled attachment score (`UAS`): fraction of words assigned the correct head
- Labeled attachment score (`LAS`): correct head and correct label
- Punctuation is sometimes excluded; report the convention you use
- `LAS` is the headline metric for most modern dependency parsers

---

## Evaluation: Constituency Bracketing

- Treat each non-terminal as a labeled bracket spanning a token range
- Precision, recall, and F1 over the set of brackets in the gold tree
- Reported by `evalb` with a long-standing convention for ignored categories
- For `PCFG` and neural constituency parsers, F1 is the headline metric

---

## Cross-Corpus Consistency

- Treebanks differ in tokenization, head-finding rules, and label inventories
- A parser trained on one and evaluated on another can drop by ten points or more
- Always evaluate against the same scheme used at training time
- For deployment, retrain or fine-tune on a treebank that matches your text

---

## Choosing A Parser

![parser_decision](svg/courses/ai/natural-language-processing/14_syntactic_parsing/parser_decision.svg)

---

## Practical Tips

- Use a pretrained `UD` parser unless you have annotated data for a custom scheme
- Cache parses; parsing is one of the slower steps in a typical pipeline
- Sentence segmentation upstream matters a lot; a wrong split corrupts every parse below
- Evaluate end-to-end, not just on the syntactic metric

---

## Anti-Patterns

- Hand-rolling a regex pipeline when a parse would be more robust
- Mixing parsers from different schemes within one project
- Reporting `UAS` without `LAS` and pretending the gap does not exist
- Treating a parse tree as ground truth instead of a model output

---

## Summary

- Constituency and dependency are two complementary views of syntactic structure
- `CKY` and `PCFG` provide the classical foundation for constituency parsing
- Transition-based and graph-based methods cover dependency parsing cleanly
- Biaffine transformer parsers are the current default for `UD` treebanks
- Use `UAS`, `LAS`, and bracketing F1 with awareness of corpus-specific conventions
