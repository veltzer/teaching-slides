---
tags:
  - data-and-ai:nlp
  - concepts:summarization
level: advanced
category: ai
audience:
  - audiences:developers
  - audiences:data-scientists

---

# Summarization

---

## What This Chapter Covers

- Extractive vs abstractive summarization and when each fits
- Classical extractive methods from `Luhn` to `TextRank`
- Neural sequence-to-sequence summarization
- Transformer summarizers from `BART` to `Pegasus`
- Long-document summarization and the context-length problem
- Faithfulness, hallucination, and the metrics that catch them

---

## Why Summarize

- Information arrives faster than humans can read it
- Summaries enable triage: read the full document only when warranted
- Drives search, recommendation, and content generation pipelines
- A demanding test of language understanding: keep the meaning, drop the rest
- Legal, medical, and financial domains have hard requirements for faithfulness

---

## Extractive vs Abstractive

- Extractive: pick spans of the input verbatim and concatenate them
- Abstractive: generate new text that paraphrases or condenses the input
- Extractive is safer; abstractive is more flexible
- Real systems often hybridize: extract candidates, then rewrite

---

## Two Approaches Compared

![extractive_vs_abstractive](svg/courses/ai/natural-language-processing/17_summarization/extractive_vs_abstractive.svg)

---

## Luhn's Method

- Score each sentence by the density of significant words
- Significant words are frequent but not on a stop list
- Pick the top-scoring sentences in document order
- Published in 1958 and still surprisingly competitive
- A baseline that more elaborate systems rarely match by huge margins

---

## TextRank

- Build a graph where nodes are sentences and edges weight similarity
- Run `PageRank` over the graph; high-ranked sentences enter the summary
- Unsupervised, language-agnostic, no training required
- Strong baseline for news summarization
- Implementations available in `gensim`, `summa`, and other toolkits

---

## TextRank in Practice

```python
import networkx as nx
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def textrank(sentences, top_k=3):
    tfidf = TfidfVectorizer().fit_transform(sentences)
    sim = cosine_similarity(tfidf)
    graph = nx.from_numpy_array(sim)
    scores = nx.pagerank(graph)
    ranked = sorted(scores.items(), key=lambda x: -x[1])[:top_k]
    return [sentences[i] for i, _ in sorted(ranked)]
```

- Twenty lines of code; respectable summaries on news articles
- Graph-based methods scale linearly with document length

---

## Supervised Extractive Summarization

- Treat each sentence as a binary classifier: include or skip
- Features: position, length, overlap with title, named entities present
- Trained on datasets like `CNN/DM` with extractive oracle labels
- Modern variant: `BERT` encoder + sentence-level head
- `BertSum` was the strong baseline that displaced unsupervised methods

---

## Sequence-to-Sequence Summarization

- Encoder reads the document, decoder generates the summary
- Pointer networks let the decoder copy spans verbatim
- Coverage mechanisms penalize repeated attention to the same source span
- The `See et al. 2017` model was the first competitive abstractive system
- Largely superseded by transformer variants

---

## BART for Summarization

- A denoising autoencoder pretrained to reconstruct corrupted text
- Fine-tunes naturally to seq2seq tasks like summarization
- Strong on `CNN/DM`, `XSum`, and most short-document benchmarks
- The default abstractive baseline in modern papers
- Cheap to fine-tune given a few thousand labeled pairs

---

## Pegasus

- Pretrains by masking entire sentences and predicting them from the rest
- Designed specifically for summarization
- Outperforms generic seq2seq pretraining when fine-tuning data is small
- The Gap Sentence Generation objective mimics the actual task
- Still competitive on out-of-domain transfer

---

## T5 and the Text-to-Text View

- `T5` frames every task as text-to-text, including summarization
- Prefix the input with `summarize:` and the model knows what to do
- Multi-task pretraining gives a strong general baseline
- Encoder-decoder architecture matches the structure of summarization
- A common backbone for instruction-tuned summarizers

---

## Long Document Summarization

- Standard transformers cap at 512-2048 tokens of input
- Long documents need either sliding windows or sparse attention
- `Longformer`, `BigBird`, `LED` extend context to thousands of tokens
- Hierarchical models summarize sections then summarize summaries
- Modern `LLMs` with 100k+ context windows changed the trade-offs

---

## Hierarchical Summarization

![hierarchical_summarization](svg/courses/ai/natural-language-processing/17_summarization/hierarchical_summarization.svg)

---

## Query-Focused Summarization

- The summary should answer a specific question or focus on a topic
- Used in search snippets, expert digests, and retrieval pipelines
- Train with (document, query, summary) triples
- Evaluation needs to test relevance to the query, not just informativeness
- A natural fit for `RAG`-style systems with a generation step

---

## Multi-Document Summarization

- Synthesize one summary from many input documents
- Required for news clustering, scientific surveys, and meeting notes
- Redundancy detection becomes the central problem
- Maximal Marginal Relevance balances novelty and salience
- Modern systems concatenate documents and let attention sort it out

---

## Faithfulness and Hallucination

- An abstractive summary can be fluent and still wrong
- Hallucination: facts that contradict or extend beyond the input
- Especially common when the model has strong priors from pretraining
- A bigger problem in news, clinical, and scientific summarization
- The headline issue for production deployment

---

## Sources of Hallucination

- Pretraining data that confidently asserts the wrong fact
- Decoders that prefer fluent over accurate continuations
- Sparse fine-tuning signal that does not punish unfaithfulness
- Bias in training data that lets common patterns override the input
- Long contexts where the model loses track of what was actually said

---

## Hallucination Taxonomy

![hallucination_types](svg/courses/ai/natural-language-processing/17_summarization/hallucination_types.svg)

---

## Reducing Hallucination

- Constrain decoding with copy or pointer mechanisms
- Use faithfulness-aware training objectives
- Post-hoc verification with a separate `NLI` model or fact checker
- Retrieval grounding to reanchor the summary in the source
- Conservative system prompts with explicit "do not invent" instructions

---

## Evaluation: ROUGE

- N-gram recall against one or more reference summaries
- `ROUGE-1`, `ROUGE-2`, `ROUGE-L` are the headline numbers
- Easy to compute, decades of accumulated baselines
- Correlates poorly with faithfulness; rewards lexical overlap
- Should never be the only metric reported

---

## Evaluation: BERTScore

- Compares contextual embeddings of summary and reference tokens
- Captures paraphrasing that `ROUGE` misses
- Higher correlation with human ratings on most datasets
- Computationally heavier but worth it
- Pair with `ROUGE` for backward comparability

---

## Faithfulness Metrics

- `FactCC`, `DAE`, `QuestEval` directly score factual consistency
- Trained on perturbed summaries with known errors
- Catch hallucinations that lexical metrics miss
- Increasingly part of the standard evaluation kit
- Cost more to run but answer the question users actually care about

---

## LLMs as Summarizers

- Prompt an instruction-tuned `LLM` with the document and a directive
- Few-shot prompting matches fine-tuned baselines on many domains
- No training data needed; iteration cost is dollars not weeks
- Long context windows enable single-pass document summarization
- Faithfulness still has to be verified — fluent does not mean correct

---

## When to Fine-Tune vs Prompt

- Specialized domain with stable schema -> fine-tune
- Generic news or web content with low volume -> prompt
- Tight budget on inference -> fine-tune a smaller model
- High variability in output structure -> prompt with examples
- Compliance requirements -> fine-tune with audited data

---

## A Practical Summarization Stack

- Retrieve or chunk the input depending on length
- Optionally pre-extract key sentences to reduce drift
- Generate with a fine-tuned summarizer or instruction-tuned `LLM`
- Score the output with a faithfulness metric and reject below threshold
- Surface uncertainty to the user when the summary is unstable

---

## Common Production Pitfalls

- Reporting `ROUGE` and assuming faithfulness is fine
- Training on `CNN/DM` and deploying on legal documents
- Summarizing without a human-in-the-loop for high-stakes content
- Letting an `LLM` paraphrase critical numbers without verification
- Ignoring the cost of long context at inference time

---

## Anti-Patterns

- Treating extractive output as inherently faithful — it is not
- Showing summaries without links back to the source
- Training on summary-summary noise from web scrape pseudo-pairs
- Ignoring summary length distribution; degenerate short outputs are common
- Using the same prompt across very different document types

---

## Summary

- Extractive methods are simple, robust, and still competitive
- Abstractive transformers dominate when faithfulness can be controlled
- Long documents require sparse attention, hierarchy, or `LLM` context
- Faithfulness is the hard problem; lexical metrics do not catch it
- Production stacks combine retrieval, generation, and verification
