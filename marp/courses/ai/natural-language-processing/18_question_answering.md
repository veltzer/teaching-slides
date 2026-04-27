---
tags:
  - data-and-ai:nlp
  - concepts:question-answering
level: advanced
category: ai
audience:
  - audiences:developers
  - audiences:data-scientists

---
# Question Answering

---
## What This Chapter Covers

- The QA landscape from extractive spans to open-domain generation
- Reading comprehension with `SQuAD`-style models
- Open-domain QA and the rise of dense retrieval
- Knowledge-base QA and structured queries over graphs
- Conversational QA where context spans turns
- Evaluation that survives different answer formats

---
## Why QA Matters

- The most natural way humans extract information from text
- A demanding test of reading and reasoning together
- Drives search engines, voice assistants, and customer support bots
- The starting point for modern `RAG` and agentic systems
- A clean evaluation target where correctness is usually well-defined

---
## QA Task Families

![qa_taxonomy](svg/courses/ai/natural-language-processing/18_question_answering/qa_taxonomy.svg)

---
## Reading Comprehension

- Given a passage and a question, return an answer span from the passage
- The classic `SQuAD` setup: every answer is contiguous text in the context
- Strong baselines hit human-level F1 on `SQuAD 1.1` by 2018
- Trained with start and end position cross-entropy
- The simplest variant of QA and a foundational building block

---
## SQuAD-Style Models

- Encode question and passage jointly with a transformer
- Two heads predict the start and end positions of the answer
- Negative log-likelihood loss over gold positions
- Decoding picks the span with the highest combined probability
- Pretrained `BERT` and `RoBERTa` are the default backbones

---
## A Span Predictor

```python
from transformers import pipeline

qa = pipeline("question-answering", model="deepset/roberta-base-squad2")
answer = qa({
    "question": "When was Marie Curie born?",
    "context": "Marie Curie was a Polish physicist born in 1867 in Warsaw."
})
print(answer)
# {'answer': '1867', 'start': 47, 'end': 51, 'score': 0.99}
```

- A few lines and you have a competitive extractive QA system
- For closed domains a fine-tune on 1k examples often pushes accuracy further

---
## SQuAD 2.0 and Unanswerable Questions

- The original `SQuAD` assumed every question had an answer in the passage
- `SQuAD 2.0` adds questions with no valid span as a third class
- Models must predict "no answer" with calibrated confidence
- Trains the system to abstain instead of guessing
- A more realistic evaluation for production systems

---
## Beyond Extractive: Generative QA

- Some questions need rephrasing or composition across multiple spans
- Generative models output free-form answers token by token
- `T5` and `BART` fine-tunes outperform extractive models on these
- Risk: hallucinated answers when context is ambiguous
- Evaluation gets harder when many surface forms are correct

---
## Open-Domain QA

- The corpus is too large to fit into one model context
- Pipeline: retrieve a few relevant passages, then read them
- Retriever and reader trained separately or jointly
- The starting point for everything we now call `RAG`
- Wikipedia is the default corpus for benchmark evaluation

---
## DrQA and Classical Pipelines

- Sparse `BM25` or `TF-IDF` retrieval over passages
- Neural reader on top of retrieved snippets
- Simple, strong baseline that still works
- The architecture that defined open-domain QA before dense retrieval
- Easy to debug because each stage has interpretable outputs

---
## Dense Passage Retrieval

- Encode questions and passages into the same vector space
- Train with contrastive loss on (question, positive passage) pairs
- Approximate nearest neighbor index over the passage embeddings
- `DPR` showed that dense retrieval beats `BM25` on natural questions
- Modern hybrid retrievers combine sparse and dense signals

---
## Open-Domain QA Pipeline

![open_domain_qa](svg/courses/ai/natural-language-processing/18_question_answering/open_domain_qa.svg)

---
## End-to-End Models

- `Fusion-in-Decoder` and `RAG` train retriever and reader jointly
- Reader sees multiple retrieved passages at once
- Joint training improves quality at the cost of complexity
- The scaffold for modern instruction-tuned `RAG` systems
- Architecture matters less when the model is large enough

---
## Knowledge-Base QA

- Answer questions against a structured graph like `Wikidata`
- Translate the question into a `SPARQL` or graph query
- Sub-tasks: entity linking, relation extraction, query construction
- Strong on factoid questions with crisp entities
- Weak when the question requires reading paragraphs of text

---
## Semantic Parsing for KBQA

- Treat question-to-query as a sequence-to-sequence task
- Train on (question, logical form) pairs from `WebQuestions` or `LC-QuAD`
- Decode constraints ensure the query is executable on the graph
- Hybrid systems use a parser plus a retrieval reader as fallback
- A controlled, auditable answer path when accuracy matters

---
## Multi-Hop QA

- Answer requires combining facts from multiple passages
- `HotpotQA` is the canonical benchmark for this setup
- Iterative retrieval: retrieve, read, generate a new query, retrieve again
- The model has to plan its search across documents
- A natural fit for agentic frameworks today

---
## Conversational QA

- Questions arrive in turns and depend on prior context
- `CoQA` and `QuAC` benchmark this setting
- Coreference and ellipsis make every question implicit on what came before
- A common production case for support and assistant products
- Long-context models simplify this versus pre-2020 architectures

---
## Conversational QA Architecture

![conversational_qa](svg/courses/ai/natural-language-processing/18_question_answering/conversational_qa.svg)

---
## Long-Form QA

- Answers are full paragraphs, not extracted spans
- `ELI5` is the famous benchmark — Reddit's "Explain Like I'm Five"
- Generation requires synthesis across many sources
- Evaluation is hard because there is no single correct answer
- The closest classical task to what `LLMs` now do conversationally

---
## QA Decoding Strategies

- Span QA: argmax over (start, end) products of probabilities
- Generative QA: greedy or beam search; sometimes constrained decoding
- Open-domain: rerank retrieval candidates with a reader score
- Calibration matters when the system can abstain
- Tool-augmented decoding can call retrievers mid-generation

---
## Evaluation: Exact Match and F1

- `Exact Match`: the predicted answer matches a reference exactly
- `F1`: token-level overlap between predicted and reference answers
- The two `SQuAD` headline metrics for over a decade
- Both reward extraction and punish paraphrase
- Less useful for generative answers with many valid forms

---
## Evaluation: Beyond EM and F1

- `BERTScore` for paraphrase-aware comparison
- `ROUGE-L` for long-form answers, with caveats
- Human preference rating for conversational evaluation
- Faithfulness checks against the retrieved passages
- Multiple metrics give a more honest view of system quality

---
## Hallucination in QA

- A confident wrong answer is worse than no answer
- Closed-book QA models hallucinate when the question goes outside training
- Open-domain QA hallucinates when retrieval fails silently
- Calibrated abstention is a key engineering goal
- "I don't know" is a feature, not a regression

---
## QA Production Patterns

- Always retrieve when the answer might not be in the parametric model
- Cite sources back to the user when possible
- Calibrate confidence to choose abstain vs answer
- Cache answers to popular questions where retrieval is expensive
- Monitor drift as the underlying corpus changes

---
## QA with Tool Use

- The model decides when to call a search tool, calculator, or database
- Reasoning and execution interleave across multiple turns
- A shift from monolithic models to orchestration over capabilities
- Modern agentic systems are essentially generalized QA pipelines
- Evaluation must include the tool-use trajectory, not just the final answer

---
## Common Production Pitfalls

- Treating retrieval failures as model failures
- Reporting `EM` when the answer is naturally paraphrased
- Skipping abstention training and shipping a system that always answers
- Letting the reader hallucinate when retrieval returns nothing
- Forgetting that conversational context changes the question

---
## Anti-Patterns

- Evaluating extractive systems on generative benchmarks and vice versa
- Single-passage QA shipped as if it were open-domain
- Ignoring entity linking quality in `KBQA`
- Training on `SQuAD` and deploying on legal documents
- Treating "I don't know" as failure when the alternative is a wrong answer

---
## Summary

- QA spans extractive, generative, open-domain, and conversational settings
- Modern systems are pipelines: retrieve, read, optionally rewrite
- `RAG` is the natural extension when knowledge is too large to fit a model
- Calibrated abstention is the underrated production requirement
- The frontier is multi-hop reasoning and tool-augmented QA agents
