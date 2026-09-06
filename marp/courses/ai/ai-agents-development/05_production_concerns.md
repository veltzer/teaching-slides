---
tags:
  - data-and-ai:llm
level: advanced
category: machine-learning
audience:
  - audiences:developers

---

# Production Concerns

---

## What This Chapter Covers

- Observability
- Evaluation
- Safety
- Cost
- Deployment

---

## Logging Everything

- Prompts, completions, tool calls
- Latency per step
- Cost per step
- Trace ID across steps

---

## Tracing

- Tree of LLM and tool calls
- Tools like LangSmith, Phoenix
- Spot loops and dead ends
- Replay for debugging

---

## Evaluation

- Define success metrics
- Build a regression set
- Run on every model change
- Track pass rate over time

---

## Eval Strategies

- Exact-match for structured tasks
- LLM-as-judge for prose
- Human review for high stakes
- Sample real traffic

---

## Guardrails

- Input filters: PII, prompt injection
- Output filters: profanity, secrets
- Tool allow-list per role
- Hard caps on actions

---

## Defense in Depth

![guardrails_layers](svg/courses/ai/ai-agents-development/05_production_concerns/guardrails_layers.svg)

---

## Prompt Injection

- User input may try to override system
- Hostile inputs in retrieved docs
- Quote untrusted text clearly
- Strip control instructions

---

## Cost Management

- Tokens per request
- Cache static prompt prefixes
- Use smaller model when adequate
- Set per-user and per-tenant budgets

---

## Cost Levers

![cost_levers](svg/courses/ai/ai-agents-development/05_production_concerns/cost_levers.svg)

---

## Latency

- Streaming for perceived speed
- Parallel tool calls
- Smaller models for fast paths
- Async background work

---

## Versioning

- Pin model versions
- Version prompts in source
- Roll out behind a flag
- A/B test changes

---

## Rate Limits

- Provider quotas
- Backoff and retry
- Per-user throttling
- Queue spikes

---

## Deployment

- Stateless workers
- Externalized memory
- Idempotent tools
- Health checks include LLM call

---

## Common Production Mistakes

- No logging
- No eval set
- No cost cap
- No prompt-injection defense
- Pinning to a deprecated model
