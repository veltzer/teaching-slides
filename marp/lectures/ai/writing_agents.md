---
tags:
- concepts:ai
- concepts:agents
- concepts:llm
- concepts:tools
level: intermediate
category: ai
audience:
- audiences:developers

---

# Writing Agents
## Designing and Building LLM Agents That Work
## Mark Veltzer
## [mark.veltzer@gmail.com](mailto:mark.veltzer@gmail.com)

---

## Overview

![title](svg/lectures/ai/writing_agents/title.svg)

---

## What This Lecture Covers

1. What an agent is — and when you actually need one
1. The agent loop: the heart of every agent
1. Building blocks: model, prompt, tools, context, memory
1. Planning, reasoning, and multi-agent systems
1. Reliability: retries, budgets, checkpoints
1. Safety: sandboxing, permissions, prompt injection
1. Evaluation, observability, and running in production

---

## Where We Start: One Call to a Model

- You send a prompt, the model sends back text — that is the whole API
- One request in, one response out; the model keeps no state between calls
- This is already useful: summarize, translate, classify, draft
- But it cannot *do* anything — it can only describe what should be done
- Everything in this lecture is built on top of this single primitive

---

## Why One Call Is Not Enough

- Real tasks need **actions**: read files, query databases, call services
- Real tasks need **iteration**: try, observe the result, adjust
- Real tasks need **state**: remember what was already done
- Real tasks need **verification**: check the work before declaring victory
- A single stateless completion offers none of these

---

## What Is an Agent?

> An agent is a language model that runs in a loop, using tools to act on its environment and observing the results, until a goal is reached.

- The **model** decides what to do next
- The **tools** carry out the decision
- The **loop** feeds the outcome back for the next decision
- The goal — not a fixed script — determines when it stops

---

## From Chatbot to Agent

![from_chatbot_to_agent](svg/lectures/ai/writing_agents/from_chatbot_to_agent.svg)

---

## Workflows vs Agents

- A **workflow** wires model calls into a fixed graph *you* designed
- An **agent** lets the model choose the path at runtime
- Workflows: predictable, testable, cheap — but rigid
- Agents: flexible, handle the unforeseen — but harder to bound
- Most production systems are a blend: workflow skeleton, agent joints

---

## When You Do Not Need an Agent

- The task has a **known, fixed sequence** of steps — write a workflow
- One prompt with good instructions already solves it — keep it simple
- Latency or cost budgets are tight and the task is repetitive
- The output must be identical every run — agents add variance
- Start with the simplest thing that works; add autonomy only when forced

---

## When an Agent Pays Off

- The path to the goal is **unknown in advance** and varies per task
- The task needs many tools combined in unpredictable ways
- Intermediate results must steer what happens next
- Humans currently do the task by "poking around" — exploring, checking
- Examples: debugging code, deep research, operating a browser, triage

---

## The Agent Loop

![agent_loop](svg/lectures/ai/writing_agents/agent_loop.svg)

---

## The Loop in Words

1. Build the context: system prompt, task, history, tool definitions
1. Call the model — it replies with text, a tool call, or both
1. If it called a tool: execute it, append the result to the history
1. Go back to step 2
1. If it replied with a final answer: stop and return it

The entire agent is this loop plus careful bookkeeping.

---

## The Loop in Code

```python
def run_agent(task: str, tools: dict) -> str:
    messages = [{"role": "user", "content": task}]
    while True:
        reply = model.call(messages, tool_defs(tools))
        messages.append(reply.as_message())
        if not reply.tool_calls:
            return reply.text
        for call in reply.tool_calls:
            result = execute(tools, call)
            messages.append(tool_result(call.id, result))
```

---

## Stop Conditions

- **Natural stop** — the model answers without requesting a tool
- **Turn limit** — a hard cap on loop iterations, always have one
- **Token budget** — stop when cost crosses a threshold
- **Wall-clock timeout** — stop when time runs out
- **Goal check** — an external test confirms the task is done

The natural stop is the happy path; the others are your safety net.

---

## The Harness

- The code around the loop is called the **harness**
- It owns: message history, tool execution, limits, error handling
- The model supplies judgement; the harness supplies discipline
- A good harness is boring: small, explicit, observable
- Most agent quality problems are harness problems, not model problems

---

## The Building Blocks

![building_blocks](svg/lectures/ai/writing_agents/building_blocks.svg)

---

## The Model Is the Engine

- Every capability of your agent is bounded by the model's ability
- Stronger models: better tool choice, longer coherent plans, fewer loops
- Weaker models: cheaper and faster, fine for narrow, well-guided steps
- No harness can fully compensate for a model that cannot reason the task
- Upgrade the model before adding clever machinery around a weak one

---

## Choosing a Model

- **Capability**: can it reliably plan and call tools for *your* task?
- **Cost**: agents multiply tokens — a loop of 30 calls is 30 bills
- **Latency**: users wait for the whole loop, not one call
- **Context size**: long tasks need long windows or good compaction
- Mix models: a strong one for planning, a cheap one for bulk steps

---

## The System Prompt

- The system prompt is the agent's **job description**
- It sets: role, goal, constraints, tone, tool usage rules
- It is read on *every* call — it anchors the whole loop
- Treat it as source code: version it, review it, test changes
- Small wording changes can visibly change agent behavior

---

## What Goes in a System Prompt

1. **Identity**: what the agent is and who it serves
1. **Goal**: what "done" means, stated precisely
1. **Constraints**: what it must never do, hard limits
1. **Tool guidance**: when to use which tool, and when not to
1. **Output contract**: format and style of the final answer

Keep it short: every sentence competes for the model's attention.

---

## A System Prompt Example

```python
SYSTEM = """You are a release engineer assistant.
Goal: diagnose failing CI builds and propose a fix.

Rules:
- Read logs before proposing anything.
- Never push commits; propose a patch instead.
- If the failure is flaky, say so and stop.

Output: a short diagnosis, then the patch."""
```

---

## Structured Output

- Free text is fine for humans; code needs **structure**
- Ask the model for JSON matching a schema you define
- Validate the output against the schema — never trust, always parse
- On validation failure, send the error back and let the model retry
- Structured output turns the model into a callable function

---

## Structured Output Example

```json
{
  "diagnosis": "test_login times out waiting for the mock server",
  "confidence": 0.85,
  "patch_files": ["tests/conftest.py"],
  "needs_human": false
}
```

- Every field is typed and machine-checkable
- The harness routes on `needs_human` without parsing prose

---

## Tools: The Agent's Hands

- A tool is a function you expose to the model, with a name and a schema
- The model *requests* a call; **your code** executes it
- Tools are the only way the agent touches the world
- The tool set defines what the agent *can* do; the prompt defines what it *should* do
- Design tools first — they are the agent's real interface

---

## A Tool Definition

```json
{
  "name": "read_log",
  "description": "Read the tail of a CI build log. Use before diagnosing any failure.",
  "input_schema": {
    "type": "object",
    "properties": {
      "build_id": { "type": "string" },
      "lines": { "type": "integer", "default": 200 }
    },
    "required": ["build_id"]
  }
}
```

---

## Writing Tool Descriptions

- The description is a **prompt**, not documentation
- Say what the tool does *and when to use it*
- Name tools by intent: `read_log`, not `get_data_v2`
- Describe arguments in the schema, with examples
- If the model misuses a tool, fix the description before fixing the model

---

## The Tool Execution Path

![tool_execution](svg/lectures/ai/writing_agents/tool_execution.svg)

---

## Validate Before You Execute

- Check the arguments against the schema — types, ranges, enums
- Check **permissions**: is this call allowed for this task and user?
- Check **paths and targets**: no escaping the workspace, no wildcards on delete
- Reject with a clear message; the model reads it and corrects course
- Validation is the harness's veto power — use it

---

## Returning Tool Results

- The result goes back into the context — the model reads it as text
- Return what the *next decision* needs, not everything you have
- Truncate huge outputs; summarize or paginate instead of dumping
- Include enough identifiers for follow-up calls (IDs, paths, cursors)
- A noisy result buries the signal the model needs

---

## Error Messages Are Prompts Too

- When a tool fails, the error text is what the model reasons with
- Bad: `Error 500` — the model can only guess or retry blindly
- Good: `file not found: config.yaml — directory contains: config.yml`
- Tell the model what went wrong *and what to try instead*
- Well-written errors make agents self-correcting

---

## How Many Tools?

- Every tool definition costs context tokens on **every call**
- Too few tools: the agent improvises with what it has — badly
- Too many tools: choice paralysis, wrong picks, wasted context
- A dozen sharp tools beat fifty vague ones
- Group niche tools behind a search or a gateway when the list grows

---

## Designing the Tool Set

1. List the actions a human expert takes to do the task
1. Turn each recurring action into one tool with one purpose
1. Make destructive actions separate, explicit tools — never a flag
1. Give read tools generous output; give write tools narrow input
1. Watch real transcripts and split or merge tools based on misuse

---

## The Context Window

![context_window](svg/lectures/ai/writing_agents/context_window.svg)

---

## Context Is a Budget

- The window holds everything: prompt, tools, history, results
- Every token there is paid for on **every** model call in the loop
- Long histories slow the loop down and cost real money
- Worse: irrelevant context actively degrades decisions
- Managing context is a core engineering task, not an afterthought

---

## What Fills the Window

- **System prompt** — fixed cost, every call
- **Tool definitions** — fixed cost, grows with the tool set
- **Conversation history** — grows every turn
- **Tool results** — usually the biggest and noisiest part
- The history grows monotonically; without care, it wins

---

## Compaction

- When the window nears its limit, **summarize** the older history
- Keep: the task, decisions made, open questions, key facts and paths
- Drop: raw tool outputs, dead ends, resolved back-and-forth
- The agent continues from the summary plus recent turns
- Compaction is lossy — design the summary to preserve what matters

---

## Memory Beyond the Window

![memory_types](svg/lectures/ai/writing_agents/memory_types.svg)

---

## Short-Term Memory

- The message history *is* the short-term memory
- It lives exactly as long as the task
- Cheap to use, but bounded by the window and lost at the end
- Scratch files are its overflow: let the agent write notes to disk
- A to-do file the agent updates beats re-deriving the plan every turn

---

## Long-Term Memory

- Facts that must survive across tasks: preferences, lessons, project state
- Stored outside the model: files, databases, key-value stores
- Loaded selectively into context at the start of a task
- Written explicitly: the agent decides "this is worth remembering"
- Keep it small and curated — stale memory is worse than no memory

---

## Retrieval: Search Instead of Stuffing

- Do not preload everything the agent *might* need
- Give it search tools and let it **pull** what the task requires
- Retrieval sources: code search, document search, embeddings, SQL
- Just-in-time context keeps the window small and the signal high
- The agent that can search does not need to memorize

---

## What to Remember, What to Forget

- Remember: decisions, constraints discovered, user corrections
- Remember: what failed and *why* — to avoid repeating it
- Forget: raw dumps, intermediate noise, anything re-derivable
- Prefer pointers over payloads: store the path, not the file
- Ask: "will a future task act differently because of this?" — if not, drop it

---

## Making the Model Think

- Models decide better when they reason **before** acting
- Give the model room to think out loud ahead of each tool call
- Thinking costs tokens but prevents far more expensive wrong actions
- Ask for a short plan up front; ask for reflection after surprises
- The transcript of thoughts is also your best debugging record

---

## The ReAct Pattern

![react_pattern](svg/lectures/ai/writing_agents/react_pattern.svg)

---

## ReAct: A Worked Example

```output
Thought: the build fails in test_login; I should read the log.
Action:  read_log(build_id="8841", lines=200)
Observation: TimeoutError waiting for mock server on port 8443
Thought: the mock server port is taken; check the fixture.
Action:  read_file("tests/conftest.py")
Observation: fixture binds port 8443 unconditionally
Thought: I have enough to propose the fix.
```

---

## Plan, Then Execute

![plan_then_execute](svg/lectures/ai/writing_agents/plan_then_execute.svg)

---

## Task Decomposition

- Big tasks fail as one prompt; split them into steps with visible outputs
- Let the model propose the split — then hold it to the list
- Each step should be checkable: a file exists, a test passes, a fact found
- Decomposition converts "vague and long" into "small and verifiable"
- The plan is allowed to change — but changes should be explicit

---

## To-Do Lists as State

- Keep the plan as a live artifact: a list with pending / done states
- The agent updates it as steps finish — progress becomes observable
- After compaction or a crash, the list is how the agent re-orients
- Users see it too: trust grows when progress is visible
- One list, one owner: the agent maintains it, the harness displays it

---

## Reflection and Self-Correction

- After a failure, make the agent *analyze* before retrying
- "The test still fails — what does that rule out?" beats blind retry
- Periodic self-checks: "does the current state match the plan?"
- A verify step at the end catches almost-right work before delivery
- Reflection is cheap insurance against confident nonsense

---

## Knowing When to Stop

- Agents fail in both directions: quitting early and never quitting
- Anchor "done" to something checkable, stated in the system prompt
- Require the agent to demonstrate completion — run the test, show output
- Diminishing returns are real: cap attempts per obstacle
- When stuck, stopping with a good summary *is* a successful outcome

---

## Why More Than One Agent?

- One context window cannot hold every concern of a large task
- Different steps want different prompts, tools, or even models
- Independent subtasks can run in **parallel**
- Specialists with narrow prompts outperform one generalist mega-prompt
- The price: coordination, and it is steep — more on that shortly

---

## Orchestrator and Workers

![orchestrator_workers](svg/lectures/ai/writing_agents/orchestrator_workers.svg)

---

## Subagents

- A subagent is an agent launched *by* an agent, with its own fresh context
- The parent writes the brief; the child returns only its final result
- Intermediate noise stays in the child — the parent's window stays clean
- Ideal for research, review, and search tasks with a compact answer
- The child inherits tools but not history: the brief must stand alone

---

## Handoffs Are Contracts

- What the parent sends: goal, constraints, needed context, output format
- What the child returns: the result — structured whenever possible
- If the brief is vague, the child solves the wrong problem *in parallel*
- Write briefs like tickets for a contractor who cannot ask questions
- Weak handoffs are the number one multi-agent failure mode

---

## Parallelism

- Fan out independent work: review five files with five subagents
- Barriers are expensive: the slowest child gates the whole stage
- Prefer pipelines — each item flows through stages independently
- Watch shared state: two agents editing one file is a race
- Isolate writers (separate copies, separate branches) and merge results

---

## The Cost of Multi-Agent

- Every child repeats the fixed costs: system prompt, tool definitions
- Token spend multiplies; a fleet of ten is ten meters running
- Debugging is harder: the failure is in *some* child's transcript
- Coordination bugs (stale briefs, lost results) replace reasoning bugs
- Multi-agent is a scaling tool, not a quality tool

---

## Rule: Single Agent First

1. Build the single-agent version and measure where it breaks
1. If context overflows — add compaction before adding agents
1. If one step needs different tools — consider a mode switch first
1. Only split when a boundary is clean: brief in, result out
1. Keep the orchestrator dumb; put intelligence in the workers

---

## Agents Fail — Plan for It

- The model call fails: rate limits, overloads, network errors
- The tool fails: bad arguments, missing files, external outages
- The *reasoning* fails: wrong conclusions from correct data
- The task fails: genuinely impossible or underspecified
- Each failure class needs a different response — do not treat them alike

---

## Failure Modes

![failure_modes](svg/lectures/ai/writing_agents/failure_modes.svg)

---

## Retries and Backoff

- Transient errors (rate limit, timeout, overload) deserve a retry
- Use exponential backoff with jitter — never a tight retry loop
- Cap the attempts; after the cap, fail loudly with context
- Do **not** retry semantic failures — the same input gives the same wrong answer
- Log every retry: silent retries hide systemic problems

---

## Timeouts and Budgets

- Give every tool call a timeout — a hung tool hangs the agent
- Give the whole task a budget: turns, tokens, money, minutes
- Budgets turn "it ran all night" into a clean, reportable failure
- Surface remaining budget to the model — it prioritizes when it knows
- Hard limits live in the harness, never in the prompt alone

---

## Idempotency

- The loop *will* replay actions: after crashes, retries, restarts
- Make tools safe to call twice: create-if-missing, overwrite-by-key
- Use idempotency keys for external side effects (payments, emails, tickets)
- Separate "compute the change" from "apply the change" where possible
- If a tool cannot be idempotent, guard it with a ledger of completed calls

---

## Checkpoint and Resume

- Persist the agent's state at safe points: history, plan, artifacts
- A crash then costs one step, not the whole task
- Resume = reload state, re-verify the world, continue the loop
- Re-verify matters: the world may have changed while you were down
- Long-running agents without checkpoints are gambling with hours

---

## Taming Nondeterminism

- The same prompt can yield different plans on different runs
- Pin what you can: model version, tool versions, fixed seeds where offered
- Move logic from prompt to code when it must be exact
- Contain the rest: validate outputs, verify results, bound the loop
- Aim for **reliable outcomes**, not identical transcripts

---

## Loops That Never End

- Symptom: the agent repeats the same action with the same failure
- Detect it in the harness: hash recent actions, flag repetition
- Break it: inject a nudge — "this approach failed twice; try another"
- Escalate after N nudges: stop and report, or ask a human
- An agent that knows it is stuck is far more useful than one that spins

---

## The Safety Problem

- An agent is code that writes its own next step at runtime
- It acts with *your* credentials on *real* systems
- Inputs it reads (files, web pages, tickets) may be adversarial
- The blast radius equals the power of the tools you handed it
- Safety is an architecture concern, not a prompt disclaimer

---

## Defense in Depth

![defense_in_depth](svg/lectures/ai/writing_agents/defense_in_depth.svg)

---

## Least Privilege for Tools

- Grant the minimum: read-only by default, writes behind approval
- Scope credentials per task: this repo, this bucket, this project
- Time-box tokens; a leaked one should expire before it matters
- Separate identities: the agent is not you — give it its own account
- Review the tool list like you review firewall rules

---

## Sandboxing

- Run tool execution inside a container, VM, or restricted user
- Filesystem: a private workspace; nothing above it is visible
- Network: allowlist the endpoints the task actually needs
- Resource limits: CPU, memory, disk — runaway work dies quietly
- The sandbox is what makes "let it try things" an acceptable policy

---

## Human in the Loop

- Some actions must wait for a person: deletes, payments, sending mail
- The harness pauses, presents the action and its context, and waits
- Approval fatigue is real: approve *classes* of safe actions, not each call
- Keep the queue reviewable: what, why, blast radius, undo story
- Autonomy is earned gradually — widen it as trust accumulates

---

## Prompt Injection

![prompt_injection](svg/lectures/ai/writing_agents/prompt_injection.svg)

---

## Defending Against Injection

- Treat all fetched content as **data**, never as instructions
- Mark tool results clearly so boundaries are visible to the model
- Strip or neutralize instruction-like content where you can
- Gate dangerous tools: injected text must not reach "send" or "delete"
- Assume some injection gets through — that is what least privilege is for

---

## The Confused Deputy

- The agent holds your keys and reads strangers' text
- Attacker's goal: make *your* agent use *your* authority for *their* task
- Classic path: poisoned web page → agent reads it → agent leaks secrets
- Mitigate: separate the browsing context from the credentialed context
- Never let one loop both read hostile input and hold powerful tools

---

## Logging and Audit

- Log every model call, every tool call, every result — with timestamps
- The transcript is your flight recorder: keep it complete and searchable
- Redact secrets *before* they enter the log, not after
- Retention: long enough to investigate, short enough to respect privacy
- When something goes wrong, the first question is "what did it do?"

---

## How Do You Know It Works?

- "It worked when I tried it" is not evidence — agents are stochastic
- One run tells you almost nothing; distributions tell you the truth
- You need: a task set, a grading method, and a habit of running both
- Evaluation is the difference between engineering and vibes
- Build the eval before you build the feature, when you can

---

## The Evaluation Loop

![evaluation_loop](svg/lectures/ai/writing_agents/evaluation_loop.svg)

---

## Building an Eval Set

- Collect real tasks: from users, transcripts, bug reports
- Each case: input, environment setup, and a definition of success
- Start with 20 cases you can run tonight — not 2000 someday
- Include the failures that hurt you; every incident becomes a case
- Keep a held-out slice — do not tune against your entire set

---

## Grading Agent Output

- **Exact checks**: the test passes, the file exists, the API returns 200
- **Rubric checks**: did it cite sources? did it stay under budget?
- **Model graders**: a second model scores quality against a rubric
- Grade *outcomes*, not transcripts — many paths reach a correct result
- Distrust a single number: read a sample of transcripts every week

---

## Tracing

- A trace records the full tree: calls, tool uses, timings, tokens, children
- Traces answer "why did it do that?" without reproducing the run
- Attach IDs so one user task links to all its model calls
- Great traces make failures boring: read, spot, fix
- If you cannot trace it, you cannot debug it — instrument from day one

---

## Observability in Production

- Dashboards: success rate, turns per task, cost per task, latency
- Alerts: budget overruns, stuck-loop detections, tool error spikes
- Watch drift: the same agent slowly degrading means the world changed
- Sample transcripts continuously — numbers hide qualitative rot
- Treat the agent like any service: SLOs, on-call, incident review

---

## Prompts Are Code

- Prompts, tool descriptions, and schemas live in version control
- Every change gets a diff, a review, and an eval run
- "Improved the prompt" without numbers is a superstition
- Keep a changelog: behavior shifts must be traceable to edits
- Rollback for prompts should be as easy as rollback for code

---

## From Demo to Production

![demo_to_production](svg/lectures/ai/writing_agents/demo_to_production.svg)

---

## Cost: Tokens Are Money

- Agent cost = calls × context size — both grow with task length
- The context is re-sent every turn; long histories dominate the bill
- Compaction, small tool sets, and lean results cut cost directly
- Route easy steps to cheap models; save the strong model for planning
- Measure cost **per task**, not per call — that is the number that matters

---

## Latency and Streaming

- Users experience the sum of every model call and tool run
- Stream text and progress as they happen; silence reads as failure
- Show the plan, the current step, and tool activity live
- Overlap work: start independent tool calls concurrently
- Perceived speed is a feature you build, not a model property

---

## Caching

- Prompt caching: reuse the unchanged prefix (system prompt, tools) cheaply
- Order the context stable-first, volatile-last, to maximize cache hits
- Cache tool results too: the same query need not hit the API twice
- Invalidate deliberately — a stale cache produces confident stale answers
- Caching often cuts both cost and latency by half or more

---

## Rate Limits and Queues

- Providers cap requests and tokens per minute — agents hit caps fast
- Put a queue between the loop and the API; smooth the bursts
- Prioritize: interactive tasks jump ahead of batch jobs
- Parallel agents share the same pool — coordinate or starve
- Design for backpressure from day one; retrofitting it hurts

---

## Surviving Model Upgrades

- Models are deprecated on a schedule you do not control
- New model ≠ better agent: behavior shifts break tuned prompts
- Keep the model name in one config point, never scattered
- Re-run the full eval set on every candidate model
- Budget a migration sprint per major model change — it is real work

---

## Versioning Everything

- One agent version = prompt + tools + model + harness, pinned together
- A change to any part is a new version with its own eval results
- Run old and new side by side on live traffic before switching
- Keep transcripts labeled by version — regressions become diffable
- "Which agent answered this?" must always have an exact answer

---

## Deployment Patterns

- **Interactive**: user watches and steers — an assistant in a session
- **Background**: fire-and-report — triage, migration, batch analysis
- **Scheduled**: cron-style routine work with a report at the end
- **Event-driven**: a webhook or alert wakes the agent
- The loop is identical; what changes is who is watching and when

---

## Frameworks: Build or Buy?

- The loop itself is fifty lines — you have seen it in this lecture
- Frameworks add: state graphs, retries, tracing, multi-agent plumbing
- The question is not "can they" but "do you understand what they hide"
- Debugging someone else's loop abstraction at 2 AM is the real price
- Whatever you choose: you must be able to read the raw transcript

---

## What Frameworks Give You

- Ready-made loop, tool dispatch, and structured output handling
- Integrations: providers, vector stores, common tools
- Observability hooks and replay tooling out of the box
- Patterns as library code: subagents, handoffs, graphs
- Faster start, shared vocabulary, community fixes

---

## What Frameworks Cost You

- Abstraction layers between you and the actual prompt
- Version churn: agent APIs are young and move fast
- Lock-in to their state model, their tool format, their tracing
- Debugging through the stack instead of through your code
- A simple harness you own often beats a powerful one you rent

---

## MCP: A Standard for Tools

- The Model Context Protocol standardizes how tools are served to agents
- A server exposes tools; any MCP-capable agent can discover and call them
- Write the integration once; every agent host can reuse it
- Servers exist for files, databases, browsers, and countless services
- Standard plumbing means your effort goes into the tools, not the wiring

---

## Design Principles

1. Start with the simplest harness that could work — grow it under pressure
1. Spend your effort on tools, context, and evals — not clever prompts
1. Make everything observable: plans, actions, budgets, failures
1. Put hard limits in code and soft judgement in the model
1. Let the model do the thinking; let the harness do the promising

---

## Anti-Patterns

- **The mega-prompt**: one giant prompt instead of tools and structure
- **The tool zoo**: eighty overlapping tools nobody curated
- **The silent agent**: no trace, no plan, no progress — just waiting
- **The infinite intern**: no budgets, no stop conditions, no escalation
- **The trusting deputy**: full credentials plus hostile input in one loop

---

## The Maturity Path

![maturity_path](svg/lectures/ai/writing_agents/maturity_path.svg)

---

## A Minimal Agent, Complete

```python
while turns < MAX_TURNS and tokens < BUDGET:
    reply = model.call(messages, tools)
    messages.append(reply.as_message())
    if not reply.tool_calls:
        break                      # natural stop
    for call in reply.tool_calls:
        check_permissions(call)    # harness veto
        out = run_sandboxed(call, timeout=60)
        messages.append(tool_result(call.id, clip(out)))
log_transcript(messages)           # flight recorder
```

---

## A Checklist Before You Ship

1. Turn, token, and time budgets enforced in the harness
1. Every tool validated, sandboxed, and least-privileged
1. Dangerous actions behind human approval
1. Full tracing with secrets redacted
1. An eval set that runs on every change
1. Checkpoints and a tested resume path

---

## Summary

- An agent = a model, in a **loop**, with **tools**, until a **goal**
- The harness carries the discipline: budgets, validation, logging
- Context is the scarce resource — curate it relentlessly
- Reliability and safety live in code, not in the prompt
- Evals turn agent development from folklore into engineering

---

## Where to Start

1. Pick one real task your team does by "poking around"
1. Write the fifty-line loop with three sharp tools
1. Add budgets, tracing, and a twenty-case eval set
1. Watch transcripts, fix tools and prompts, re-run the evals
1. Only then consider subagents, frameworks, and fleets

---

## Questions?

- The loop is simple; the engineering around it is the craft
- Start small, measure everything, and grow autonomy with trust
- The best agent is the one whose failures are boring

## Thank You
## [mark.veltzer@gmail.com](mailto:mark.veltzer@gmail.com)
