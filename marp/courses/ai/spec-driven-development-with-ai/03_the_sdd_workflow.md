---
tags:
  - data-and-ai:ai
  - data-and-ai:generative-ai
  - data-and-ai:agents
  - concepts:code-generation
  - practices:methodology
  - practices:productivity
level: intermediate
category: ai
audience:
  - audiences:developers
  - audiences:team-leads
  - audiences:architects

---

# The SDD Workflow

## Overview
- The loop end to end: specify, plan, tasks, implement, verify
- The human review gates and what each one catches
- Verifying against the spec: derived tests and a second-agent audit
- Iterating without drift: re-planning, amending, the spec as pull request description
- Failure modes in the loop and how to recover

---

## The Loop End to End

![the_sdd_loop](svg/courses/ai/spec-driven-development-with-ai/03_the_sdd_workflow/the_sdd_loop.svg)

---

## Specify: From Idea to Reviewed Requirements

- Input: one paragraph, a ticket, or a conversation with product
- The agent expands it into the requirements template; you correct it
- A useful first prompt:

```markdown
Read docs/specs/TEMPLATE.md. Draft docs/specs/042-export/spec.md
for this idea: "admins can export audit logs for a date range".
Write acceptance criteria in EARS form. Do not propose an
implementation. List every assumption you made under Open questions.
```

- Expect two or three rounds: the first draft is generic, the second is yours
- Stop when a reviewer can approve it without asking you anything

---

## Plan: Let the Agent Draft, Then Correct

- The agent knows the codebase better than your memory does; let it propose
- Prompt it with the spec and the constitution, ask for the plan template
- Correct in this order:
    - Wrong constraints: it picked a library or pattern the team does not use
    - Missing requirements: a criterion with no corresponding plan item
    - Scope creep: plan items no requirement asked for
    - Unrecorded decisions: it chose, but did not say what it rejected
- Ask it to list which requirement each plan section satisfies; gaps show immediately
- The plan is approved when the architect could hand it to a new hire

---

## Tasks: Decomposing the Plan

- Ask the agent to cut the plan into tasks and then check the cut
- A good task:
    - Fits in one agent run and one review sitting
    - Names the requirement it serves and the test that proves it
    - Leaves the build green when it ends
- A bad task: "implement the export feature" or "fix remaining issues"
- Order matters: data model, then interfaces, then logic, then edges
- Mark tasks that can run in parallel; they can go to parallel agents

```misc
- [ ] T1 migration + model        (D-1)      test: test_models.py
- [ ] T2 POST /exports            (AC-2.3)   test: test_api.py::test_queue
- [ ] T3 worker: generate CSV     (AC-2.1/2) test: test_worker.py
- [ ] T4 permissions              (AC-2.4)   test: test_api.py::test_403
```

---

## Implement: One Task at a Time vs Letting It Run

| | One task per run | Autonomous run over all tasks |
|---|---|---|
| Review | After each diff | At the end |
| Drift | Caught early | Compounds silently |
| Speed | Slower wall clock | Fast until it is wrong |
| Best for | New codebases, risky tasks | Well-tested, well-specified work |

- Start with one task per run; move to longer runs as the spec quality proves itself
- Even in an autonomous run, require a commit per task so review can bisect
- Instruct the agent to stop on any open question or failing constraint

---

## The Human Review Gates

![human_review_gates](svg/courses/ai/spec-driven-development-with-ai/03_the_sdd_workflow/human_review_gates.svg)

---

## Reviewing the Spec Before Any Code Exists

- The most valuable review in the whole loop, and the one most teams skip
- Checklist for the reviewer:
    - Every story has numbered acceptance criteria in observable terms
    - Every criterion could be turned into a test
    - Errors, limits and permissions are stated, not implied
    - Non-goals are listed
    - Open questions have owners
    - Nothing describes implementation
- Typical time: 20 minutes for a feature-sized spec
- Do it as a pull request review: comments on lines, approval to proceed

---

## Reviewing Each Task's Diff

- Review the diff *against the task*, not against your general taste
    - Does the diff do only what the task says?
    - Does the named test exist, and does it fail without the change?
    - Did the agent touch a file the plan does not mention? Ask why
    - Did it quietly relax a constraint to make a test pass?
- Ask the agent to summarize which criteria the diff satisfies; verify the claim
- Reject fast: a rejected task is re-run in minutes, a merged violation costs days
- Spec violations found at this gate are the loop working as designed

---

## Verification Against the Spec

![verification_against_the_spec](svg/courses/ai/spec-driven-development-with-ai/03_the_sdd_workflow/verification_against_the_spec.svg)

---

## Deriving Tests From Acceptance Criteria

- Every criterion in `EARS` form is already a test case description

```python
# AC-2.3: When an export exceeds 100,000 rows,
#         the system shall queue it and return 202 with a job id.
def test_large_export_is_queued(client, big_dataset):
    resp = client.post("/api/v2/exports", json=big_dataset.range())
    assert resp.status_code == 202
    assert "job_id" in resp.json()

# AC-2.4: If the caller is not an admin, then respond 403 and no file.
def test_non_admin_gets_403(client, user_token):
    resp = client.post("/api/v2/exports", headers=user_token)
    assert resp.status_code == 403
```

- Generate the tests from the spec *before* the implementation task runs
- Name the criterion in the test; coverage of the spec becomes visible in the test list

---

## Asking a Second Agent to Audit

- The implementing agent is biased toward its own work; a fresh context is not

```markdown
You are auditing an implementation against its specification.
Read docs/specs/042-export/spec.md and the diff in this branch.
For every acceptance criterion output: id, MET / NOT MET / UNCLEAR,
and the file and line that proves it. Then list any behavior in
the diff that no requirement asked for. Do not fix anything.
```

- Run it in a new session or a different tool, with no chat history
- Treat the audit like a static analyzer: cheap, repeatable, occasionally wrong
- Unclear verdicts usually mean the criterion itself needs rewriting

---

## When the Code Is Right and the Spec Was Wrong

- It happens on most features: implementation reveals a requirement that cannot hold
- Signs: a criterion is impossible, contradicts another, or costs far more than it is worth
- The wrong response: leave the code as is, let the spec drift
- The right response, in order:
    1. Amend the spec, with a one-line reason next to the change
    1. Re-run the plan step for the affected section
    1. Adjust or add tasks; keep the ones already done
    1. Only then change the code
- The amendment is part of the same pull request, so reviewers see both

---

## Iterating Without Drift

![re_plan_on_spec_change](svg/courses/ai/spec-driven-development-with-ai/03_the_sdd_workflow/re_plan_on_spec_change.svg)

---

## The Spec as the Pull Request Description

- The pull request needs no separate description: the spec is it
- Structure that works:
    - Link to `spec.md`, `plan.md`, `tasks.md` in the branch
    - The audit result: which criteria are met, with pointers
    - Amendments made during implementation, with reasons
    - Anything left open
- Reviewers read the spec first, then the diff; the order matters
- When the branch merges, the spec merges with it and stays next to the code
- Generating this from the artifacts is a one-prompt job for the agent

---

## Failure Modes in the Loop

- **The agent ignores the spec**
    - Symptom: generic code, wrong names, criteria unmentioned in its summary
    - Cause: spec not in context, or buried under a long chat
    - Fix: fresh session, spec loaded first, ask it to restate the criteria before coding
- **The plan silently contradicts the requirements**
    - Symptom: a plan item that no criterion explains, or a criterion with no plan item
    - Fix: require a traceability list in the plan; review it line by line
- **Scope expands mid-run**
    - Symptom: "I also refactored..." in the summary
    - Fix: non-goals in the spec, one task per run, reject diffs that exceed the task

---

## Recovering a Derailed Implementation Run

- A run is derailed when the diff no longer maps to the task list
- Do not argue with it in the same chat; the context that caused it is still there
- Recovery steps:
    1. Stop the run and commit or stash nothing yet
    1. Run the audit prompt on the current diff to see what is salvageable
    1. Keep tasks whose diffs pass their tests; revert the rest
    1. Fix the spec or task wording that allowed the drift
    1. Restart from the first failed task in a fresh session
- Hands-on: each pair gets a branch with a derailed run and its spec, 30 minutes to recover it
