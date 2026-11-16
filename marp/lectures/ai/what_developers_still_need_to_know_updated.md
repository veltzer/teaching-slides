---
tags:
  - data-and-ai:ai
  - data-and-ai:llm
  - data-and-ai:agents
  - concepts:best-practices
  - concepts:architecture
  - practices:development-workflow
  - practices:documentation
  - practices:testing
  - databases:choosing
level: intermediate
category: ai
audience:
  - audiences:developers
  - audiences:senior-developers
  - audiences:architects
  - audiences:team-leads

---

# What Every Developer Needs to Know About Working with AI
## Context, Feedback and Limits
## Mark Veltzer
## [mark.veltzer@gmail.com](mailto:mark.veltzer@gmail.com)

---

## Overview

![title](svg/lectures/ai/what_developers_still_need_to_know_updated/title.svg)

---

## What This Lecture Covers

1. What changed for developers, and what did not
1. The context window: what the machine can actually see
1. Documentation: what the machine is told
1. Tests: how the machine knows it is done
1. Guardrails: what the machine is not allowed to do
1. `AI` and data: showing it, creating it, choosing where it lives
1. Architecture that an `AI` can work in without slowly wrecking it

---

## From Autocomplete to Agents

- The first assistants completed the line you were typing
- Today's agents work on the whole task:
    - Read the repository and run the build
    - Query the database
    - Write the code and the tests
    - Open the pull request
- The unit of work moved from a line to a change
- Your editor is no longer where most of the work happens

---

## The Job Moved

- Before: you wrote the code, and the tool helped
- Now: the tool writes the code, and you do three other things
    - **Specify**: say what is wanted, precisely enough to be checked
    - **Steer**: set up what the agent sees and what it may do
    - **Judge**: decide whether what came back is right
- An agent in a badly prepared repository produces mistakes faster
- An agent in a well prepared repository produces working changes faster
- The difference is the repository, not the model

---

## What the Model Is and Is Not

- It is a colleague with tools and memory, not an autocomplete
- Its knowledge is frozen at a training cutoff
    - Newer library versions and newer `APIs` are unknown to it unless it reads them
- It is fluent and confident, and sometimes wrong
    - The confidence is the same in both cases
- It knows nothing about your project except what is in front of it
- It does not get tired, bored, or offended by being asked to redo the work

---

## The Failure Modes Worth Knowing by Name

| Failure | What it looks like |
|---------|--------------------|
| Hallucination | An `API`, a package or a fact that does not exist |
| Plausible code | Works on the happy path, misses the edge cases |
| Wrong problem | A good solution to a problem you did not have |
| Gaming the check | The test passes; the code is still wrong |

- Naming the failure tells you which lever to pull
- None of these are fixed by a better prompt alone

---

## Responsibility Does Not Move

- You own what you merge, whoever or whatever typed it
- "The `AI` wrote it" is not an answer in a post-mortem
- Review is not optional because the author is a machine
- If you cannot explain the change, you are not ready to merge it
- Everything that follows exists to make that ownership affordable

---

## The Three Levers You Control

![three_levers](svg/lectures/ai/what_developers_still_need_to_know_updated/three_levers.svg)

---

## The Context Window Is Everything the Model Knows

- The model has no access to your project, only to its context window
- Whatever is not in the window does not exist for the model
    - Not the design meeting, not the ticket, not what you said in the previous session
- The window is finite, and everything in it costs money
- Most "the `AI` is stupid" moments are context problems:
    - It was missing something, or it was drowning in something else

---

## What Fills the Window

![context_window](svg/lectures/ai/what_developers_still_need_to_know_updated/context_window.svg)

---

## Tokens, Limits and a Filling Window

- The window is measured in tokens: roughly three quarters of a word each
- Every token is paid for again on each turn of the conversation
- Quality drops well before the window is full
    - Early instructions get less attention
    - Old, abandoned approaches keep pulling the model back
- Compaction summarizes the history to free space
    - Exact error messages, file paths and the reasons behind decisions get lost
- A long session is not a better informed session

---

## Memory Between Sessions

- A new session starts empty; agent memory is what makes it look otherwise
- The agent saves preferences, corrections and project facts as notes
- Those notes are loaded back into the window when a session starts
- You can read, correct and delete what the agent remembers
    - Do it: a stale or wrong memory is repeated with full confidence
- Memory belongs to you alone and is not shared with your team

---

## Managing Context Deliberately

- One task per session
- Point at files instead of pasting them
    - The agent reads the part it needs
- Use sub-agents to isolate context
    - The search happens in their window; only the conclusion comes back to yours
- Make builds quiet and tool output terse
    - A build that prints thousands of lines on success spends your window on nothing
- Treat the window as a budget, because it is one

---

## When to Restart Instead of Correct

- Signs that a session is spent:
    - The agent repeats a mistake you already corrected
    - It forgets a rule it followed earlier
    - It keeps returning to an approach you rejected
- Each new correction adds more text to a window that is already confused
- Ask for a short summary of what was learned, and start a new session with it
- Restarting is cheap; arguing with a full window is not

---

## Documentation Is the Memory the Whole Team Shares

- A new colleague asks questions; an agent reads what is written and guesses the rest
- What you write for the `AI` is what you should have written for people
- Documentation now has a reader that reads all of it, every session
- It is the one place where a decision reaches every developer and every agent

---

## Agent Memory Versus Documentation

| | Agent memory | Documentation |
|---|--------------|---------------|
| Written by | The agent, automatically | People and agents, deliberately |
| Seen by | One developer | The whole team |
| Reviewed | No | Yes, like code |
| Versioned | No | Yes |
| Survives a new machine | No | Yes |

- A rule that matters belongs in the repository, not only in memory

---

## Instruction Files in the Repository

- A file the agent reads at the start of every session
- What belongs in it:
    - How to build, test and run
    - Conventions the code does not make obvious
    - Things that must never be done
- What does not belong in it:
    - Anything the agent can see by reading the code
    - Long tutorials
- Keep it short: a long instruction file gets ignored, by people and by models

---

## Write the Reason Next to the Rule

```markdown
# Project rules

- Build with `make check`. It runs the linters and the tests.
- Never edit files under `generated/`. They are overwritten
  by `make codegen`; change the templates instead.
- Never disable a failing check. A red build means the code
  is wrong, not the check.
- All timestamps are `UTC`. The reporting service breaks on
  local time.
```

- A rule with a reason is applied correctly to cases the rule did not foresee
- A rule without a reason is followed literally or dropped

---

## If It Is Not in the Repository, It Does Not Exist

- The agent cannot read the wiki you forgot, the chat thread, or your head
- Keep as files, next to the code:
    - Specifications: what is wanted
    - Plans: how it will be done
    - Decision records: what was chosen, and why
- Plan first, code second
    - Reviewing a plan is cheaper than reviewing a diff
    - A wrong plan costs a paragraph; a wrong implementation costs a branch

---

## Stale Documentation Is Now a Bug

- People skim documentation and distrust it; the `AI` believes what it reads
- An outdated instruction produces outdated code, confidently
- Let the `AI` write and maintain documentation
    - It is good at it, and it does not find it boring
    - Make updating the documentation part of the change, not a later chore
- Review documentation changes the way you review code changes

---

## Tests as the Definition of Done

- "Done" in prose is an opinion; "done" as a test is something a machine can check
- An agent without tests stops when the code looks right
- An agent with tests stops when the code is right, as far as the tests can tell
- Tests are the feedback the agent can get by itself, without waiting for you
- The quality of that feedback sets the ceiling on what you can delegate

---

## The Feedback Loop

- The `AI` must be able to run the tests alone
- What the loop needs:
    - **One command**: no manual steps, no tribal knowledge
    - **Fast**: the agent runs it dozens of times per task
    - **Deterministic**: a flaky test teaches the agent to ignore failures
    - **Loud on failure**: a clear message and a non-zero exit code
- A test suite that only passes on one machine is not a feedback loop

---

## Changing Existing Code

- Pin down existing behavior before letting the `AI` change it
    - Characterization tests record what the code does now
    - Then every behavior change is a visible, deliberate test change
- Let the `AI` write tests, but do not let it grade its own homework
    - Code and tests written together share the same misunderstanding
    - Write the tests from the specification, in a separate session
    - Or have the tests reviewed before any code is written

---

## Warning Signs in Tests

- Tests that assert what the code does rather than what it should do
    - The expected value was copied from the output
- Tests weakened, skipped or deleted to get to green
    - Look for this in every diff
- Mocks that test the mock
    - Everything real is replaced, and the test proves that the mock returns what it was told to return
- A green build with any of these is worth less than a red one

---

## Checking the Tests Themselves

- Review the tests more carefully than the code
    - Wrong code with good tests gets caught
    - Wrong tests let everything through
- Property-based testing
    - State a rule that holds for all inputs; the tool searches for a counterexample
- Mutation testing
    - The tool breaks the code on purpose
    - A suite that still passes was not checking that code
- Both are cheap to set up now: the `AI` writes the scaffolding

---

## Instructions Are Requests; Checks Are Rules

- An instruction is followed most of the time
- "Most of the time" is not good enough for anything that matters
- A check either passes or fails, and the agent sees the failure and fixes it
- Anything you find yourself telling the agent twice should become a check
- Guardrails are what holds when the `AI` ignores its instructions

---

## Layers of Guardrails

![guardrail_layers](svg/lectures/ai/what_developers_still_need_to_know_updated/guardrail_layers.svg)

---

## Deterministic Checks, Strict by Default

- Compilers, type checkers, linters and formatters
    - Cheap, fast, and impossible to argue with
- Strict by default: a check fails loudly and is never switched off to pass
- The classic shortcuts, all of which an agent will try:
    - Disable the lint rule
    - Catch the exception and continue
    - Mark the test as skipped
- The pipeline is the last gate, and the `AI` cannot talk its way past it
    - Provided the agent has no permission to edit the gate

---

## Limiting What the Agent Can Do

- Permissions and allow lists
    - Reading is cheap to allow; writing outside the repository is not
- Sandboxes and containers
    - No access to your home directory, your keys, or the production network
- Hooks that run before and after the agent acts
    - Block a command, format a file, run the tests after every edit
- The limit must be enforced by the tool, not requested in the prompt

---

## Secrets and Irreversible Actions

- Secrets
    - The agent must never see them: whatever enters the window may leave your network
    - The agent must never write them: no keys in code, configuration or logs
    - Scan for secrets in the pipeline
- Irreversible actions need a human
    - Pushing, deleting, deploying, migrating
- Approving one such action is not approving the next one
- Keep such actions rare, so that approving them never becomes a reflex

---

## Untrusted Text and Invented Dependencies

- Prompt injection: untrusted text that the `AI` reads as instructions
    - A web page, an issue comment, a file in a dependency, a row in a database
    - The model cannot reliably tell data from commands
    - Defense: limit what the agent can do, not what it can read
- Invented dependencies
    - The `AI` suggests a package name that sounds right
    - Attackers register such names in advance
    - Check that every new dependency exists, is maintained, and is the one you meant

---

## Version Control Is the Undo Button

- Small commits: each one is a state you can return to
- A branch per task: the main branch never sees a half-finished idea
- Worktrees: several agents work on the same repository without colliding
- Commit before a risky step, not after it
- The cheaper the undo, the more freedom you can safely give the agent

---

## The Working Loop

![working_loop](svg/lectures/ai/what_developers_still_need_to_know_updated/working_loop.svg)

---

## Working in Small Steps

- Small verifiable steps over giant leaps
    - A small diff can be read; a huge one gets approved unread
- Reading a diff you did not write
    - Start with the tests, then the interfaces, then the bodies
    - Look for what was removed, not only for what was added
- Running several agents in parallel
    - Writing scales with the number of agents
    - Review does not: it still passes through you
- Turn every repeated correction into documentation or a check

---

## Showing Data to the AI

- Data does not fit in the context window, and should not try to
- Show the shape, not the rows:
    - The schema
    - A handful of sample rows
    - Statistics: counts, ranges, distinct values, share of nulls
- Formats cost differently in tokens
    - `JSON` repeats every key on every row; `CSV` names the columns once
- Let the `AI` write the query instead of reading the table
    - The database does the work, and the answer is a few rows

---

## Natural Language to SQL

- Where it works
    - A documented schema, clear names, questions with one obvious meaning
- Where it quietly lies
    - A join that duplicates rows and inflates a sum
    - A filter on the wrong date column
    - "Active customers" defined differently than your business defines it
- The query runs and returns a number, and nothing tells you it is the wrong number
- Read the generated `SQL`, and check the result against a figure you already know

---

## Giving an Agent Database Access

![db_access](svg/lectures/ai/what_developers_still_need_to_know_updated/db_access.svg)

---

## The Schema Is Documentation

- The `AI` reads the schema the way it reads code
- What helps it get queries right:
    - Meaningful table and column names
    - Comments on columns
    - Constraints and foreign keys
    - A data dictionary for the terms the business uses
- A column called `flag2` gets guessed at, by people and by models
- Privacy
    - Personal data sent to a model has left your network
    - Mask or synthesize before the agent sees anything

---

## Documents and Unstructured Data

- Documents do not fit in the window either
- Retrieval: search first, then show the model only the relevant passages
- Embeddings turn text into vectors, so that similar meaning sits close together
- Keyword search still wins for exact names, codes and identifiers
- The answer can only be as good as what was retrieved
    - Check what the search returned before blaming the model

---

## Creating Test Data

- Test data and fixtures on demand
- Ask for a generator, not for rows
    - Rows are produced once and cost tokens every time
    - A generator is code: reviewed, versioned, run at any size
- Realistic versus merely plausible
    - Distributions, relations between tables, and the edge cases that matter
- Reproducibility
    - A fixed seed, and the generator kept in the repository

---

## Extracting and Cleaning Data

- The `AI` turns free text and documents into structured records
- Validate every extraction against a schema
    - Types, required fields, allowed values
    - Reject what does not fit; do not repair it silently
- Cleaning, classifying and labeling at scale works well
- Sample and measure quality instead of trusting it
    - Label a few hundred records by hand and compare
    - An error rate you measured can be managed; one you assumed cannot

---

## Transformations and Migrations

- The `AI` writes transformation and migration code well
- Run it as code, not through the model: the same input must give the same output
- Reconcile every run
    - Counts: rows in, rows out, rows rejected
    - Checksums on the columns that must not change
    - Round trips: convert there and back, then compare
- A migration that was not reconciled was not verified, it was merely executed

---

## Choosing Databases with AI

- Use the `AI` as a research assistant, not as an oracle
- Its biases
    - The popular: whatever has the most text written about it
    - The old: whatever existed before its training cutoff
    - Whatever you hinted at: mention a product and it will recommend it
- Describe the workload first
    - Access patterns, volume, consistency needs, growth
- Ask for trade-offs, and for the case against each option

---

## What Changed in Choosing a Database

- Prototyping and benchmarking are now cheap, so do them
    - Load realistic data into two candidates and measure
- How well the `AI` knows a technology is now a selection criterion
- Boring relational databases gained from `AI`
    - Decades of `SQL` in the training data
    - A schema the agent can read, and constraints that catch its mistakes
- Vector search
    - Often a feature of the database you already run
    - A product of its own only when the scale demands it

---

## Schema Design with AI

- Good at: normalization, index suggestions, constraints, spotting missing keys
- Read query plans together with the `AI`
    - Paste the plan and ask where the time goes
    - Then verify by measuring: it can misread a plan as confidently as it reads one
- Schema changes are code
    - Reviewed
    - Versioned
    - Reversible
- An agent never changes a production schema directly

---

## What AI Changes in Architecture

- Code became cheap; wrong boundaries did not
- A wrong module boundary is now multiplied by the speed at which code is written
- Decisions that are hard to reverse stay human decisions
    - Data models, public interfaces, technology choices, service boundaries
- The `AI` will happily build on a bad foundation
    - It optimizes the task in front of it, not the system

---

## Designing with the AI

- A sparring partner: alternatives, trade-offs, objections
- Make it argue against your preferred design
    - Left alone, it agrees with whatever you seem to want
- Record decisions and their reasons where the `AI` will find them
    - Otherwise the next session re-opens the decision, or silently reverses it
- Generate diagrams and documentation from the code
    - A diagram derived from the code cannot drift from it

---

## Architecture That AI Can Work In

- Modules small enough to fit in a context window
- Explicit interfaces, types and contracts
- Consistency over cleverness: one way to do each thing
- Locality: a change should touch few files
- Mainstream technology the model already knows well
- Fast builds and fast tests, as an architectural requirement
- One repository or many
    - The agent only sees what is checked out in front of it

---

## Enforcing Architecture Mechanically

- Dependency rules and layering, checked by tools
    - "The domain layer does not import the web layer" as a failing build
- Architecture tests and fitness functions
    - Size limits, forbidden imports, response time budgets
- A described rule drifts
    - Every agent, in every session, has to read it, understand it and choose to follow it
- A checked rule holds
    - It does not depend on anyone remembering it

---

## How the Economics Shift

- Build versus buy, when building is cheap
    - A small, exact, owned solution can beat a large, general dependency
- Fewer dependencies, more owned code
    - Every dependency is a supply chain risk and a version to chase
- Disposable prototypes and cheap rewrites
    - Build it twice to learn; keep the second one
- Duplication versus abstraction, reconsidered
    - Duplicated code is easy for an agent to edit and easy to leave inconsistent
    - A wrong abstraction is still worse than either

---

## Architectural Drift and Legacy Systems

- Drift: locally reasonable changes that add up to a mess
    - Duplicated logic and parallel implementations of the same idea
    - The agent did not find the existing helper, so it wrote another one
- Periodic audits, with the `AI` doing the reading
- Legacy systems
    - Use the `AI` to understand code nobody remembers
    - Tests first, then modernization in small steps
    - Never a rewrite of code whose behavior nobody pinned down

---

## Putting a Model Inside the System

- A model is a component that is slow, costly and not deterministic
- Evaluation instead of unit tests
    - A set of inputs with expected properties, scored on every change
- Fallbacks, limits and observability
    - Timeouts, budgets, a path that works when the model does not
    - Log the prompts and the answers
- Ordinary code is often the better choice
    - If a rule can be written down, write the rule

---

## What to Change in Your Repository First

1. Add a short instruction file: how to build, how to test, what never to do
1. Make the tests run with one command, fast and loud
1. Make the pipeline strict, and deny the agent permission to weaken it
1. Give the agent a sandbox and a read-only database role
1. Move decisions and plans into files next to the code
1. Add one mechanical check for an architecture rule you keep repeating
1. Turn the next correction you make twice into documentation or a check
