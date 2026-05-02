---
tags:
  - data-and-ai:llm
level: intermediate
category: machine-learning
audience:
  - audiences:developers
  - audiences:data-scientists

---
# Prompting and Evaluation

---
## What This Chapter Covers

- Prompt structure
- Citations
- Refusal behavior
- Evaluation
- Metrics

---
## Prompt Structure

- System: role and rules
- Context: retrieved chunks
- Question: user input
- Format: how to answer

---
## Layout Example

![prompt_layout](svg/courses/ai/rag-applications/04_prompting_and_evaluation/prompt_layout.svg)

---
## Quoting Sources

- Number each chunk
- Ask model to cite by number
- Include source URL in metadata
- Render citations in UI

---
## Refusing Gracefully

- "Say I do not know if context lacks the answer"
- Avoid hallucinated citations
- Distinguish missing from contradictory
- Test refusal cases

---
## Format Constraints

- JSON for downstream code
- Markdown for users
- Hard structure helps consistency
- Validate after model output

---
## Context Order

- Most relevant first
- Or last (lost in middle effect)
- Test with your model
- Vary by length

---
## Context Window Budget

- Reserve room for answer
- Reserve room for system prompt
- Trim chunks if needed
- Smaller model means tighter budget

---
## Evaluation Sets

- Curate question, ground truth pairs
- Cover happy and edge cases
- Refresh as content changes
- Tag by category

---
## Retrieval Metrics

- Recall at K
- Discounted cumulative gain
- Mean reciprocal rank
- Are right chunks in top K

---
## Eval Metrics Overview

![eval_metrics](svg/courses/ai/rag-applications/04_prompting_and_evaluation/eval_metrics.svg)

---
## Generation Metrics

- Faithfulness: matches sources
- Answer relevance
- Context relevance
- Use LLM-as-judge

---
## End-to-End Metrics

- Task success
- Time to answer
- Cost per query
- User feedback

---
## A/B Testing

- Compare retrievers
- Compare prompts
- Compare models
- Measure on real traffic

---
## Online Feedback

- Thumbs up or down
- "Was this answer correct"
- Use to grow eval set
- Watch for selection bias

---
## Common Prompting Mistakes

- No citation
- No refusal path
- Too much context
- Free-form output where structure was needed
- Eval set never updated
