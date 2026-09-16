---
tags:
- concepts:ai
- concepts:agents
- concepts:llm
- concepts:prompting
- concepts:best-practices
level: intermediate
category: ai
audience:
- audiences:developers

---

# Working with AI Coding Agents
## Mark Veltzer
## [mark.veltzer@gmail.com](mailto:mark.veltzer@gmail.com)

---

## Overview

![title](svg/lectures/ai/ai_best_practices/title.svg)

---

## What This Lecture Covers

1. The common thread: artifacts over prose, checks over claims
1. Working through a list of tasks — files, commits, and hashes
1. Why handing over the previous commit works so well
1. Setting up the work: examples, gates, plans, and rules
1. During the work: verification, diagnosis, and interruption
1. Scoping and boundaries — what to name and what to delegate
1. Reviewing the output: diffs, counter-arguments, and evidence

---

## The Common Thread

- Small, mechanical habits that make AI-assisted work predictable
- Replace prose the AI must **interpret** with artifacts it can **inspect**
- Replace claims the AI **makes** with checks it must **run**
- A file beats a paragraph; a command beats a promise
- Every practice in this lecture is one of these two moves in disguise

---

## Artifacts Over Prose, Checks Over Claims

![artifacts_over_claims](svg/lectures/ai/ai_best_practices/artifacts_over_claims.svg)

---

## Working Through a List of Tasks

- Most real work is a sequence of related changes, not a single prompt
- The transcript is a poor place to keep the plan: it compresses and drifts
- Put the list in a file, tie each item to a commit, review at every boundary
- The list becomes the plan, the log, and the handoff at the same time

---

## Write the Whole List Down First

- A tasks file in the repo or scratchpad, before any code is written
- Every turn refers to the same plan instead of a paraphrase of it
- Prose lists in chat drift as the transcript gets summarized
- Order tasks so that **each one leaves the build green**
    - If task 3 needs task 5's helper, reorder
    - A red intermediate state forces the AI to fix things that are not its task

---

## An Example Tasks File

```markdown
# Tasks: move config loading to a typed model

1. [x] Add `Settings` next to the old loader           (a1b2c3d)
1. [x] Route `load_config()` through `Settings`        (e4f5a6b)
1. [ ] Delete the old dict-based loader
1. [ ] Update the two callers in `cli/`
1. [ ] Remove the compatibility shim

Gate: `rsconstruct build --verbose -j10` is green after every item.
```

---

## One Commit Per Task

- A task that needs two commits was two tasks: split the list
- A commit that covers two tasks hides which one broke the build
- Mark each task done with its **commit hash** in the tasks file
- The list then doubles as a log
- A fresh session can resume from it without re-reading history

---

## The Task Loop

![task_loop](svg/lectures/ai/ai_best_practices/task_loop.svg)

---

## Show the Previous Task and Its Commit

- Before describing task N, hand the AI task N-1 and the diff of commit N-1
- The commit is **ground truth** for what now exists
- It is a **template** for scope, style, and granularity
- It is a **boundary** that keeps commit N from re-touching earlier files
- Task text plus one diff is a small, high-signal prompt

---

## Why the Previous Commit Works

- **Calibration by example**: a concrete, accepted sample of "done" in this repo
    - Commit message style, file layout, test conventions, scope size
- **Continuity of intent**: the diff shows which helpers and names now exist
    - The AI reuses them instead of inventing parallel ones
- **Ground truth over stale summary**: in a long session, memory is compressed
- **Detecting drift early**: a plan that contradicts commit N-1 shows before code

---

## Cleaner Diffs and Consistent Scale

- **Smaller, cleaner diffs**: the prior commit is a boundary, so cleanup stays out
- **Consistent granularity**: a 40-line commit is rarely followed by a 600-line one
- **Cheap context**: cheaper than re-reading the repo, more relevant than a style guide
- The cost: a bad commit N-1 becomes a bad template for commit N
- So **review each commit before moving on**

---

## Review at Each Boundary

- Catching a bad commit before the next task starts costs one review
- Catching it at the end costs a rebase
- **Re-plan when a task surprises you**
    - If task N is larger or different than listed, stop and revise the rest
    - The original ordering assumed the original scope
- **Keep refactors and behavior changes as separate items**
    - "Rename X" and "change what X does" are different commits, even on the same lines

---

## Finishing the List

- **Start a fresh session for a long list**
    - After several tasks the transcript carries stale beliefs about file state
    - The tasks file plus the last commit is a complete handoff
- **Run the full gate at the end, cold**
    - Per-task checks may be warm and partial
    - The final pass runs exactly what CI runs, caches cleared, before any push

---

## Setting Up the Work

- **Give the example, not the adjective**
    - "Match this file" beats "write clean code"
    - Point at a real function, test, or commit that already looks right
- **Write the acceptance check first**
    - State the command that must pass before describing the change
    - The AI then optimizes for the gate instead of for looking done

---

## Anatomy of a Good Task Prompt

![prompt_anatomy](svg/lectures/ai/ai_best_practices/prompt_anatomy.svg)

---

## Adjective vs Example

| Vague ask | Inspectable ask |
|-----------|-----------------|
| "Write clean code" | "Match the style of `src/parser.py`" |
| "Add good tests" | "Follow `tests/test_loader.py`, then run `pytest tests/`" |
| "Make it fast" | "`bench.sh` must report under 200 ms" |
| "Be careful with dependencies" | "Never pin versions, because the lockfile owns them" |
| "Don't break CI" | "`rsconstruct build` must be green; paste the output" |

---

## One Task Per Turn

- A message with three asks gets three half-answers
- Sequence them; let each turn end in a **verifiable state**
- **Ask for a plan before code on anything non-trivial**
    - Reviewing five lines of plan is cheaper than two hundred lines of wrong diff
- **State constraints as rules with a reason**
    - "Never pin versions, because the lockfile owns them" survives edge cases
    - "Never pin versions" gets rationalized away the first time a pin looks convenient

---

## During the Work

- **Make the AI verify, not you**
    - End tasks with "run the real CI command and paste the output"
    - Claims of success without output are worth nothing
- **Prefer questions to fixes when diagnosing**
    - "Why does this fail?" gets an assessment
    - "Fix this" gets a change to whatever the AI guessed first

---

## Correct the Rule, Not the Instance

- When it does something wrong, state the **general rule**
- Put the rule in `CLAUDE.md` or memory, where the next session reads it
- Otherwise the same thing gets fixed again next week
- A rule with its reason survives the edge case the instance never showed

---

## Instance Fix vs Rule Fix

![rule_not_instance](svg/lectures/ai/ai_best_practices/rule_not_instance.svg)

---

## Environment and Interruption

- **Keep the AI in the right environment**
    - Enter the `venv`, the branch, the directory yourself
    - Tools that switch environments silently are where wrong-version bugs come from
- **Interrupt early**
    - If the first few actions head the wrong way, stop it
    - Sunk work in a transcript makes later turns worse, not better

---

## Scoping and Boundaries

- **Name what is out of scope**
    - "Do not touch the workflow `yml`" beats hoping it infers that from context
- **Separate refactor commits from behavior commits**
    - Ask for the mechanical rename first, review it, then the real change
    - Mixed diffs hide bugs
- **Fresh session for a fresh task**
    - Starting clean with the commit as ground truth beats a summarized memory of it

---

## Delegate Reading, Keep Deciding

- Let a subagent sweep twenty files and report the conclusion
- Keep the judgment call in the main thread where you can see it
- Reading is cheap to delegate and easy to redo
- Deciding is where errors compound, so keep it visible

---

## Reading in the Background, Deciding in the Open

![delegate_reading](svg/lectures/ai/ai_best_practices/delegate_reading.svg)

---

## Reviewing the Output

- **Read the diff, not the summary**
    - The description is the AI's intent; the diff is what happened
    - They diverge more often than expected
- **Ask it to argue against its own change**
    - "What could this break?" after a diff surfaces the cases it skipped

---

## Green Is Necessary, Not Sufficient

- A passing build proves the tests pass, not that the change is right
- Ask what the tests **do not cover** before merging
- **Demand evidence for severity claims**
    - "This is exposed" should come with the command that proved it
    - A finding without a reproduction is a hypothesis

---

## Review Questions for Every Diff

1. Does the diff match the stated intent?
1. What could this break?
1. What do the tests not cover?
1. Where is the evidence for each claim?
1. Did it stay within the named scope?

---

## Summary

- Write the plan in a file; one task, one commit, one hash
- Hand over task N-1 and commit N-1 before describing task N
- Give examples and gates, not adjectives
- Make the AI run the check and paste the output
- Fix the rule, not the instance; read the diff, not the summary
