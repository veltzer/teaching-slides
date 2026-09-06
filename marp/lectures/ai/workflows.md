---
tags:
- concepts:ai
- concepts:workflows
- concepts:agents
- concepts:llm
- concepts:orchestration
level: intermediate
category: ai
audience:
- audiences:developers

---

# Workflows and Dynamic Workflows
## Mark Veltzer
## [mark.veltzer@gmail.com](mailto:mark.veltzer@gmail.com)

---

## Overview

![title](svg/lectures/ai/workflows/title.svg)

---

## What This Lecture Covers

1. What a workflow is — and how it differs from an agent
1. The classic workflow patterns: chaining, routing, parallelization
1. Evaluator loops and orchestrator–worker structures
1. Pipelines versus barriers — the wall-clock question
1. Dynamic workflows: deciding the shape at runtime
1. Discovery loops, verification panels, and budgets
1. Reliability: determinism, resume, and observability

---

## The Spectrum of Autonomy

- **One model call**: a single prompt in, a single answer out
- **Workflow**: several calls wired into a graph that *you* designed
- **Dynamic workflow**: code that decides the graph's shape at runtime
- **Agent**: the model itself chooses the next step in a loop
- Each step trades predictability for flexibility — move right only when forced

---

## What Is a Workflow?

- A workflow is a **fixed composition** of model calls and plain code
- The control flow lives in your program: sequence, branch, fan-out
- The model fills in judgement at each node; it never picks the path
- Every run visits the same structure, so behavior is predictable
- Think of model calls as functions and the workflow as the program

---

## Workflows vs Agents

![workflow_vs_agent](svg/lectures/ai/workflows/workflow_vs_agent.svg)

---

## Why Start with a Workflow?

- **Predictable**: same structure every run — no surprise detours
- **Testable**: each stage is a function you can unit test in isolation
- **Debuggable**: a failure points at one named stage, not "somewhere in the loop"
- **Cheap**: no wasted turns deciding what to do — the code already knows
- Reach for an agent only when the path genuinely cannot be known in advance

---

## The Unit of Work: One Model Call

- Each stage is one call: prompt in, result out, no hidden state
- Give the stage everything it needs — it cannot ask follow-up questions
- Keep stages **single-purpose**: summarize, classify, extract, draft
- A stage that does three things fails in three ways — split it
- Sharp stage boundaries are what make the whole graph composable

---

## Structured Output: The Glue Between Stages

- Free text between stages forces fragile parsing at every joint
- Instead, each stage returns JSON matching a schema you define
- Validate at the boundary; on failure, return the error and retry the stage
- Downstream code routes on typed fields, never on prose
- The schema *is* the contract between stages — version it like an API

---

## A Stage Contract Example

```python
TRIAGE_SCHEMA = {
    "type": "object",
    "properties": {
        "category": {"enum": ["bug", "feature", "question"]},
        "severity": {"enum": ["low", "medium", "high"]},
        "summary": {"type": "string"},
    },
    "required": ["category", "severity", "summary"],
}

result = call_model(prompt, schema=TRIAGE_SCHEMA)
route_ticket(result["category"], result["severity"])
```

---

## Prompt Chaining

![prompt_chaining](svg/lectures/ai/workflows/prompt_chaining.svg)

---

## Prompt Chaining in Practice

- Decompose one hard prompt into a sequence of easy ones
- Each step consumes the previous step's output as its input
- Example: outline the document → write each section → polish the tone
- Each call is simpler, so each call is more reliable
- The price is latency: steps run one after another

---

## Gates Between Steps

- A **gate** is plain code that checks a step's output before continuing
- Schema valid? Word count in range? All required sections present?
- A failed gate retries the step or aborts the chain — loudly
- Gates catch drift early, before it contaminates downstream steps
- Cheap deterministic checks between expensive model calls: always worth it

---

## Routing

![routing](svg/lectures/ai/workflows/routing.svg)

---

## Routing in Practice

- A classifier stage picks **one** of several specialized handlers
- Each handler has its own prompt, tools, and even its own model
- Easy inputs go to a cheap model; hard ones to a strong model
- Separation keeps each handler's prompt short and focused
- Log the routing decision — misroutes are your main failure mode

---

## Parallelization

![parallelization](svg/lectures/ai/workflows/parallelization.svg)

---

## Sectioning and Voting

- **Sectioning**: split the input into independent parts, process concurrently
    - review five files with five parallel calls, then merge
- **Voting**: run the *same* task several times, compare the answers
    - majority vote for classification; union for finding bugs
- Both trade tokens for wall-clock time or for confidence
- Merging is plain code — keep the intelligence in the branches

---

## Orchestrator and Workers

- A central stage breaks the task into subtasks it discovers in the input
- Workers execute the subtasks — in parallel where independence allows
- The orchestrator merges worker results into the final answer
- Unlike sectioning, the *split itself* is decided by a model at runtime
- This is the doorway pattern: one step further and you have a dynamic workflow

---

## Evaluator and Optimizer

![evaluator_optimizer](svg/lectures/ai/workflows/evaluator_optimizer.svg)

---

## Evaluator–Optimizer in Practice

- One stage **generates**; a second stage **criticizes** against explicit criteria
- The critique loops back; the generator revises; repeat until accepted
- Works when you can state what "good" means better than you can produce it
- Always cap the rounds — two stages can politely disagree forever
- Keep the evaluator blind to the generator's excuses: judge the artifact only

---

## Choosing a Pattern

- Known fixed steps, each simpler than the whole → **chaining**
- Distinct input categories needing distinct handling → **routing**
- Independent parts, or need for multiple opinions → **parallelization**
- Quality bar you can describe but not hit in one shot → **evaluator–optimizer**
- Subtasks only discoverable from the input itself → **orchestrator–workers**

---

## Pipelines vs Barriers

![pipeline_vs_barrier](svg/lectures/ai/workflows/pipeline_vs_barrier.svg)

---

## Why Barriers Hurt

- A barrier makes every item wait for the slowest item in the stage
- With five branches, one straggler idles the other four
- A **pipeline** lets each item flow through all stages independently
- Wall-clock becomes the slowest single chain, not the sum of slowest stages
- Default to pipelines; make every barrier justify itself

---

## When a Barrier Is Right

- The next stage genuinely needs **all** previous results together
- Deduplicating findings across branches before expensive verification
- Early exit: "zero candidates found — skip the whole next stage"
- A synthesis prompt that compares results *against each other*
- "The stages feel separate" is not a reason — that is what pipelines model

---

## Error Handling in Workflows

- Every stage can fail: bad output, timeout, rate limit, empty result
- Transient failures retry with backoff; semantic failures do not
- A stage that returns nothing where results are expected must **raise**
- Passing empty output silently downstream corrupts the whole run
- Decide per stage: retry, skip the item, or abort the workflow

---

## Testing Workflows

- Each stage is a function — test it with recorded inputs and outputs
- Test the gates hardest: they are your correctness boundary
- Replay whole runs from logged stage outputs without paying for model calls
- Golden tasks: a small set of end-to-end runs scored on every change
- A workflow you cannot replay is a workflow you cannot debug

---

## Where Fixed Workflows Break

- The work list is **unknown**: which files? which tickets? how many?
- The depth is unknown: keep searching until nothing new appears
- The effort should scale with a budget, not a hard-coded count
- Results of one stage should decide whether later stages run at all
- You need the structure of a workflow with decisions made at runtime

---

## What Is a Dynamic Workflow?

- A **script** that builds the workflow shape while it runs
- Plain code: loops, conditionals, fan-out — driven by intermediate results
- The code owns control flow; model calls own judgement at each node
- Deterministic orchestration around nondeterministic workers
- More flexible than a fixed graph, more governable than a free agent

---

## Dynamic Workflow

![dynamic_workflow](svg/lectures/ai/workflows/dynamic_workflow.svg)

---

## Code Decides, Model Judges

- The script asks questions; model calls answer them
- "How many findings?" — code counts; "Is this finding real?" — model judges
- Never ask a model something code can compute: counts, dedup, sorting
- Never hard-code what only the model can see: relevance, quality, meaning
- This division of labor is the core discipline of dynamic workflows

---

## Scout, Then Orchestrate

- You rarely know the work list before the task — so **discover it first**
- A cheap scout pass lists the targets: files, endpoints, tickets, channels
- Then the script fans out one worker per discovered item
- Scouting is often plain code: a glob, a query, a directory walk
- Plan the orchestration step, not the whole task, in advance

---

## Fan-Out over a Discovered List

```python
targets = discover_targets(repo)      # scout: plain code
if not targets:
    raise RuntimeError("no targets found — refusing to continue")

results = []
for batch in chunks(targets, PARALLELISM):
    results += run_parallel(
        review_worker(t) for t in batch
    )
report = merge(results)               # merge: plain code
```

---

## Loop Until Dry

![loop_until_dry](svg/lectures/ai/workflows/loop_until_dry.svg)

---

## Making Discovery Converge

- Fixed counts miss the tail: "find 10 bugs" stops at 10, or pads to 10
- Instead, loop rounds of finders until **nothing new** appears
- Deduplicate against everything *seen*, not everything *accepted*
    - otherwise rejected findings resurface every round, forever
- Stop after N consecutive empty rounds — two is a good default
- Always pair the loop with a hard cap: rounds, workers, or tokens

---

## Adversarial Verification

- Finders are optimists: plausible-but-wrong results survive one pass
- Send each finding to independent **skeptics** prompted to refute it
- A finding survives only if a majority fails to refute it
- Verification is where dynamic workflows earn their token bill
- Cheap to add in a script: one more fan-out stage per finding

---

## Judge Panels and Diverse Lenses

- N identical judges share blind spots — diversity beats redundancy
- Give each judge a different lens: correctness, security, performance
- Or different strategies: reproduce it, read the spec, check the history
- Aggregate with plain code: majority, veto, or weighted score
- Panels also rank competing drafts: generate N, judge all, synthesize from the winner

---

## Scaling to a Budget

![budget_scaling](svg/lectures/ai/workflows/budget_scaling.svg)

---

## Budgets in Practice

- The user states effort: "quick check" versus "thorough audit"
- The script converts budget to structure: worker count, rounds, panel size
- Loop shape: `while remaining_budget > cost_of_one_round: run_round()`
- Treat the budget as a **hard ceiling** enforced in code, not a hint
- Report what was skipped when the budget ran out — silent truncation lies

---

## Concurrency Caps

- Parallel is not free: API rate limits and machine resources are shared
- Cap concurrent workers; queue the rest — the script keeps submitting
- A cap of ten still completes a hundred items, just in waves
- Put the cap in one config point, never scattered per call site
- Watch the queue depth: a growing queue means the cap is your bottleneck

---

## Determinism and Resume

- Long workflows crash: machines restart, limits hit, networks fail
- Make the *script* deterministic: no wall-clock, no randomness in control flow
- Then a resume can replay: completed stages return cached results instantly
- Only the first changed or missing stage onward runs live
- Same script plus same inputs should mean same structure, every time

---

## Checkpoints and Journals

- Journal every stage: inputs, outputs, timing, tokens — as it happens
- The journal is the source of truth for resume and for debugging
- Before blaming a stage, **read its journal entry** — not your assumption
- Persist at stage boundaries; a crash then costs one stage, not the run
- A dynamic workflow without a journal is a black box with a bill

---

## Observability

- Name your phases; report which phase is running and what remains
- Progress must be visible: items done, items queued, budget spent
- Log every capped or dropped item — bounded coverage must be explicit
- Silence reads as failure to whoever is waiting on the run
- The transcript of workers plus the journal answers "why did it do that?"

---

## The Cost Model

- Cost = number of calls × context per call — fan-out multiplies both
- Every worker re-pays the fixed costs: system prompt, schemas, instructions
- Verification often costs more than discovery — budget for it
- Route bulk stages to cheap models; save the strong model for judging
- Measure cost **per task**, and per phase within the task

---

## Anti-Patterns

- **The secret agent**: a "workflow" whose stages quietly decide the path
- **The barrier farm**: every stage waits for every other stage
- **The optimist**: findings shipped without a verification pass
- **The infinite scout**: discovery loops with no dry-round stop or cap
- **The silent trim**: top-N sampling nobody was told about

---

## Design Principles

1. Start fixed; go dynamic only when the work list or depth is unknown
1. Keep control flow in code and judgement in model calls
1. Structured contracts at every boundary; validate loudly
1. Pipeline by default; make every barrier justify itself
1. Verify adversarially; scale effort to an explicit budget

---

## Summary

- A workflow is a fixed graph of model calls — predictable, testable, cheap
- The classic patterns: chain, route, parallelize, evaluate, orchestrate
- Dynamic workflows keep code in charge while deciding shape at runtime
- Discovery loops, verification panels, and budgets are the core moves
- Determinism, journals, and caps turn clever scripts into reliable systems

---

## Questions?

- Fixed structure where you can, runtime structure where you must
- The model judges; the code decides; the journal remembers
- The best workflow is the one whose failures are boring

## Thank You
## [mark.veltzer@gmail.com](mailto:mark.veltzer@gmail.com)
