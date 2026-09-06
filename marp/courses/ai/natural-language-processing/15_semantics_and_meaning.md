---
tags:
  - data-and-ai:nlp
  - concepts:semantics
level: advanced
category: ai
audience:
  - audiences:developers
  - audiences:data-scientists

---

# Semantics and Meaning

---

## What This Chapter Covers

- Lexical semantics — word senses, relations, and lexical knowledge bases
- Word sense disambiguation from `Lesk` to contextual embeddings
- Compositional semantics and why deep learning sidesteps it
- Semantic role labeling with `PropBank` and `FrameNet`
- Coreference resolution and textual entailment

---

## Why Semantics Is Hard

- Syntax tells you the structure; semantics tells you the meaning
- Words have multiple senses, and context picks the right one
- The same meaning can be expressed in many surface forms
- Meaning composes — but not in the simple way logic suggests
- Modern systems learn meaning implicitly rather than building it explicitly

---

## Lexical Semantics

- The meaning of individual words and the relations between them
- A word is a form; a sense is a meaning attached to that form
- One form can carry many senses (`bank` of a river, `bank` for money)
- One sense can be carried by many forms (`car`, `automobile`, `vehicle`)
- The mapping is many-to-many and changes over time

---

## Word Senses and Polysemy

- Polysemy: one word, multiple related senses (`paper` as material, document, journal)
- Homonymy: one form, unrelated senses (`bat` as animal, `bat` as club)
- The boundary between polysemy and homonymy is fuzzy and dictionary-dependent
- Sense inventories vary across resources — there is no canonical truth
- Granularity matters: too fine, and disambiguation is impossible; too coarse, and distinctions are lost

---

## Lexical Relations

- Synonymy — same meaning in some context (`big` and `large`)
- Antonymy — opposite meaning (`hot` and `cold`)
- Hypernymy — `dog` is a hypernym of `poodle`; `poodle` is a hyponym of `dog`
- Meronymy — part-whole relation (`wheel` is a meronym of `car`)
- These relations form a graph that powers reasoning over language

---

## Lexical Relations Map

![lexical_relations](svg/courses/ai/natural-language-processing/15_semantics_and_meaning/lexical_relations.svg)

---

## WordNet

- A large lexical database for English organized around synsets
- A synset is a set of synonymous word senses sharing one meaning
- Synsets are linked by hypernymy, meronymy, antonymy, and other relations
- Built by hand by lexicographers since the 1980s at Princeton
- The reference resource for symbolic semantic processing

---

## What WordNet Looks Like

```python
from nltk.corpus import wordnet as wn

senses = wn.synsets("bank")
for s in senses:
    print(s.name(), "-", s.definition())

# bank.n.01 - sloping land beside a body of water
# depository_financial_institution.n.01 - a financial institution
# bank.n.03 - a long ridge or pile
```

- Each synset has a definition, examples, and links to other synsets
- A starting point for symbolic and hybrid systems

---

## Other Lexical Knowledge Bases

- `FrameNet` — words organized by the situational frames they evoke
- `VerbNet` — verbs grouped by syntactic and semantic behavior
- `BabelNet` — multilingual extension that aligns `WordNet` with `Wikipedia`
- `ConceptNet` — broader common-sense relations beyond strict lexical ties
- Each resource encodes a different slice of meaning

---

## Word Sense Disambiguation

- Given a word in context, choose the right sense from a sense inventory
- Classical task: `I deposited money at the bank` — financial sense
- Useful for translation, information retrieval, and structured reasoning
- Hard because senses overlap and context can be subtle
- Modern systems often disambiguate implicitly without naming senses

---

## The Lesk Algorithm

- A simple, knowledge-based disambiguation method from 1986
- For each candidate sense, look up its dictionary definition
- Score the overlap between the definition and the surrounding context
- Pick the sense with the highest overlap
- Surprisingly hard to beat with no training data

---

## Lesk in Practice

```python
def lesk(word, context, senses):
    best, best_score = None, -1
    ctx = set(context.lower().split())
    for sense in senses:
        gloss = set(sense.definition().lower().split())
        score = len(ctx & gloss)
        if score > best_score:
            best, best_score = sense, score
    return best
```

- The simplest possible word sense disambiguator
- Variants weight rarer overlapping words more heavily

---

## Supervised Disambiguation

- Treat sense selection as a classifier over labeled examples
- Features: surrounding words, syntactic role, named entities nearby
- Requires sense-annotated corpora — `SemCor`, `OntoNotes`
- A separate model per ambiguous word, or a multi-task model
- Strong baselines for years; eclipsed by contextual embeddings

---

## Contextual Embeddings as Implicit Disambiguation

- A `BERT` embedding for `bank` in a financial sentence differs from `bank` near a river
- The model never named the sense; the vector encodes it implicitly
- Probing studies show contextual embeddings cluster by sense
- Most modern pipelines skip explicit disambiguation entirely
- The downside: there is no symbolic label to reason over

---

## Compositional Semantics

- The meaning of a phrase is a function of the meanings of its parts
- Frege's principle of compositionality, stated formally by Montague
- Logical forms compose along the syntax tree
- `every dog barks` becomes a quantified logical formula
- The classical bridge between syntax and meaning

---

## Compositional Semantics Pipeline

![compositional_semantics](svg/courses/ai/natural-language-processing/15_semantics_and_meaning/compositional_semantics.svg)

---

## Combinators and Tree Composition

- Each syntactic rule has a corresponding semantic combinator
- Lambda calculus expresses these combinators precisely
- Bottom-up over the parse tree: combine child meanings into parent meaning
- `Combinatory Categorial Grammar` packages syntax and semantics together
- Elegant, but brittle when grammar coverage breaks

---

## Why Deep Learning Sidesteps Composition

- Vector embeddings combine via attention rather than logical rules
- A transformer never builds a parse tree or a logical form explicitly
- Composition is learned end-to-end from text
- The model often does the right thing without naming what it did
- The cost: no symbolic handle on the meaning the model produced

---

## Semantic Role Labeling

- Identify the predicate of a sentence and label its arguments
- For `Mary gave John a book`, the predicate is `give`
- Arguments: agent (Mary), recipient (John), theme (book)
- Roles abstract over surface form — passive and active share roles
- A bridge between syntax and structured meaning

---

## Predicates and Arguments

- Predicate: typically a verb, sometimes a noun or adjective
- Arguments: the entities that fill the slots the predicate opens
- Core arguments — required by the predicate's lexical frame
- Modifiers — optional adjuncts (location, time, manner)
- Same predicate, different argument structures across languages

---

## PropBank

- Annotates predicate-argument structure on top of the `Penn Treebank`
- Uses generic role labels: `Arg0`, `Arg1`, `Arg2`, plus modifiers
- `Arg0` typically aligns with agent, `Arg1` with patient or theme
- Verb-specific frame files describe what each argument means
- The standard training resource for English `SRL` systems

---

## FrameNet

- Builds on Fillmore's frame semantics
- Each frame represents a situation type with named roles
- The `Commerce_buy` frame has roles: `Buyer`, `Seller`, `Goods`, `Money`
- Frames are linked: buying and selling share the same scene from different views
- Richer than `PropBank` but with smaller corpus coverage

---

## SRL System Architectures

![srl_architecture](svg/courses/ai/natural-language-processing/15_semantics_and_meaning/srl_architecture.svg)

---

## Neural SRL Systems

- Encode the sentence with a pretrained transformer
- Tag each token with a role label using a sequence labeling head
- Joint models predict predicates and arguments together
- Span-based variants predict argument boundaries directly
- Modern `SRL` exceeds 90% F1 on `OntoNotes` benchmarks

---

## Coreference Resolution

- Determine which mentions in a text refer to the same entity
- `Alice picked up her book. She opened it.` — `her` and `She` corefer with `Alice`
- A foundational task for reading comprehension and dialogue
- Combines syntactic, semantic, and pragmatic cues
- Critical when downstream tasks need to track entities across sentences

---

## Anaphora and Cataphora

- Anaphora — a mention refers backward (`Alice ... she`)
- Cataphora — a mention refers forward (`Before she left, Alice ...`)
- Pronouns are the canonical anaphors but not the only kind
- Definite noun phrases (`the dog`) often refer back too
- Zero anaphora — the referent is implicit, common in pro-drop languages

---

## Mention Detection and Clustering

- Two-stage pipeline: find mentions, then cluster mentions that corefer
- Mentions: pronouns, named entities, definite noun phrases
- Clustering can be pairwise (does mention X corefer with mention Y) or global
- The output is a partition of mentions into entity clusters
- Errors in mention detection cascade into clustering errors

---

## Neural Coreference Systems

- End-to-end models score every span pair in a document
- Antecedent ranking: for each mention, choose the best preceding mention or none
- Higher-order inference refines decisions iteratively
- Long documents need attention restricted by distance or coarse-to-fine pruning
- `OntoNotes` is the standard English benchmark

---

## Coreference Challenges

- Pronoun ambiguity: `The trophy doesn't fit in the suitcase because it is too big`
- World knowledge required: which `it` is too big depends on physics
- Long-range coreference across paragraphs is genuinely hard
- Singletons (mentions with no coreferent) are easy to over-cluster
- Nested mentions: `the President of the company` contains `the company`

---

## Textual Entailment

- Given a premise and a hypothesis, decide if the premise implies the hypothesis
- Three labels: entailment, contradiction, neutral
- `A man is playing piano` entails `A person is making music`
- A unifying task — many semantic phenomena reduce to entailment
- Also called natural language inference

---

## NLI Datasets

- `SNLI` — image-caption pairs labeled by crowd workers
- `MultiNLI` — multi-genre extension covering more text styles
- `ANLI` — adversarial examples designed to break strong models
- `XNLI` — multilingual extension across 15 languages
- Models that hit 90%+ on `SNLI` still struggle on `ANLI`

---

## NLI in Practice

```python
from transformers import pipeline

nli = pipeline("text-classification", model="roberta-large-mnli")
result = nli({
    "text": "A man is eating pizza.",
    "text_pair": "A person is having food."
})
# label: ENTAILMENT, score: 0.98
```

- Pretrained `NLI` models are off-the-shelf for many semantic checks
- Often used as a building block for fact-checking and zero-shot classification

---

## NLI Challenges

- Annotation artifacts — models learn shortcuts in the hypothesis alone
- World knowledge gaps — entailment often needs facts not in the premise
- Definitional vagueness — annotators disagree on neutral vs entailment
- Adversarial examples expose brittle reasoning behind strong scores
- Multilingual `NLI` is harder than the leaderboards suggest

---

## Where Semantics Meets Generation

- Modern large language models do not output logical forms
- They generate text that behaves as if it understands meaning
- Faithfulness — does the output reflect the input meaning faithfully
- Hallucination — fluent text untethered from any meaning the input supports
- Evaluation increasingly uses `NLI` models to score faithfulness automatically

---

## Anti-Patterns

- Treating word senses as fixed categories when context defines them
- Using `WordNet` glosses as ground truth for modern domains
- Building elaborate compositional pipelines a transformer would replace
- Evaluating coreference on toy pronouns and shipping for full documents
- Trusting a single high `NLI` score across very different domains

---

## Summary

- Lexical semantics organizes word meaning into senses and relations
- `WordNet` and `FrameNet` remain useful even when models do not need them
- Word sense disambiguation has largely been absorbed by contextual embeddings
- Compositional semantics is bypassed by deep learning, not solved by it
- `SRL`, coreference, and `NLI` remain active tasks with strong neural systems
