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

# SDD Tooling Today

## Overview
- `Spec Kit`: installation, the command sequence, the generated files, agent integrations
- `Kiro` and IDE-native `SDD`: requirements, design and tasks as first-class artifacts, hooks
- `SDD` without a framework: plain `Markdown` specs wired into instruction files
- Choosing a toolchain and migrating between tools

---

## Spec Kit: Installing and Initializing

- `Spec Kit` is GitHub's open source toolkit for `SDD`; it is a `Python` CLI plus templates
- The CLI scaffolds a project; the real work happens as slash commands inside your agent

```bash
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git
specify init audit-export --ai claude
cd audit-export
specify check
```

- The `--ai` flag selects the agent to generate command files for: `claude`, `copilot`, `cursor`, `gemini` and others
- `specify check` verifies that the agent CLI and `git` are available
- Run it in an existing repository with `--here` to add `SDD` to a brownfield project

---

## Spec Kit Command Flow

![spec_kit_command_flow](svg/courses/ai/spec-driven-development-with-ai/04_sdd_tooling_today/spec_kit_command_flow.svg)

---

## The Constitution and Specify Commands

- Commands are prefixed with `speckit.` in current releases; older versions used bare names

```markdown
/speckit.constitution Tests required for every behavior change,
typed public interfaces, no new dependencies without approval.

/speckit.specify Admins can export audit logs for a date range
as CSV; large exports run in the background.
```

- `/speckit.constitution` writes `.specify/memory/constitution.md`
- `/speckit.specify` creates a numbered feature branch and `specs/001-audit-export/spec.md`
- The spec template forces the sections from the previous chapter: stories, criteria, edge cases
- `/speckit.clarify` interviews you about the gaps before planning

---

## Plan, Tasks and Implement

```markdown
/speckit.plan FastAPI, SQLAlchemy, Celery for background jobs, S3 storage.

/speckit.tasks

/speckit.implement
```

- `/speckit.plan` produces `plan.md` plus `research.md`, `data-model.md`, `contracts/` and `quickstart.md`
- `/speckit.tasks` writes `tasks.md` with numbered, dependency-ordered tasks and parallel markers
- `/speckit.analyze` cross-checks spec, plan and tasks for contradictions before implementation
- `/speckit.implement` executes the tasks in order and ticks them off
- Every command is a `Markdown` prompt file you can read and edit; nothing is hidden

---

## The Generated Directory Structure

```tree
.specify/
    memory/constitution.md
    templates/        spec, plan and tasks templates
    scripts/          branch and file helpers
specs/
    001-audit-export/
        spec.md  plan.md  research.md  data-model.md  contracts/  tasks.md
.claude/commands/speckit.*.md   (or .github/prompts/, .cursor/commands/)
```

- Commit all of it; the `specs/` directories are the durable asset, the commands are replaceable glue

---

## Spec Kit With Claude Code, Copilot and Cursor

| Agent | Command files | How to invoke |
|---|---|---|
| `Claude Code` | `.claude/commands/speckit.*.md` | `/speckit.specify ...` in the CLI |
| `GitHub Copilot` | `.github/prompts/speckit.*.prompt.md` | `/speckit.specify` in agent mode |
| Cursor | `.cursor/commands/speckit.*.md` | `/speckit.specify` in chat |

- Same templates, same output files; only the launcher differs
- Multiple agents in one repository are fine: `specify init --ai` can be run per agent
- Claude Code additionally reads `CLAUDE.md`; point it at the constitution there
- Copilot reads `.github/copilot-instructions.md`; Cursor reads `.cursor/rules/`

---

## Kiro and IDE-Native SDD

![kiro_artifacts_and_hooks](svg/courses/ai/spec-driven-development-with-ai/04_sdd_tooling_today/kiro_artifacts_and_hooks.svg)

---

## Kiro Artifacts in Practice

- `Kiro` is an `AI` IDE from AWS built around specs rather than chat
- Choosing "Spec" instead of "Vibe" starts a three-stage flow, each stage waiting for approval:
    - `requirements.md`: user stories with `EARS` acceptance criteria, generated from one sentence
    - `design.md`: architecture, sequence diagrams, interfaces, data model
    - `tasks.md`: checkbox tasks, each linked to the requirement it satisfies
- Files live in `.kiro/specs/<feature>/` and are ordinary `Markdown` in your repository
- `.kiro/steering/` holds always-on context: the constitution, conventions, product facts
- You start a task from the `tasks.md` file itself; the IDE tracks completion

---

## Kiro Hooks

- Hooks run an agent action on an IDE event, keeping artifacts and code in sync

```json
{
  "name": "Sync tests on save",
  "when": { "type": "fileEdited", "patterns": ["src/**/*.py"] },
  "then": {
    "type": "askAgent",
    "prompt": "Update the tests for the edited module; keep tasks.md accurate."
  }
}
```

- Typical hooks: refresh docs on save, run a security review on demand, tick tasks when tests pass
- Hooks are the answer to "who updates the spec when the code changes?" - the tool does
- Similar automation is possible elsewhere with `git` hooks or `Claude Code` hooks, with more wiring

---

## SDD Without a Framework

![diy_spec_layout](svg/courses/ai/spec-driven-development-with-ai/04_sdd_tooling_today/diy_spec_layout.svg)

---

## Wiring Specs Into Agent Instruction Files

- Every agent reads an instruction file at start; that is where the workflow is enforced

```markdown
# CLAUDE.md (excerpt)
## Spec-driven workflow
- Before any change, read docs/specs/README.md (the constitution).
- Each feature lives in docs/specs/NNN-name/: spec.md, plan.md, tasks.md.
- Work on exactly one unchecked task from tasks.md, then stop and report.
- Never edit spec.md. If a requirement cannot be met, say so and propose
  an amendment in your report.
- Tick a task only after its named test passes.
```

- The same text goes into `.github/copilot-instructions.md` or `.cursor/rules/sdd.mdc`
- Add slash commands or prompt files for `specify`, `plan`, `tasks` if the agent supports them

---

## A Minimal Template That Covers the Essentials

```markdown
# <Feature name>          (spec.md)
## Goal / Non-goals
## Stories and acceptance criteria   (EARS, numbered AC-n.m)
## Edge cases, errors, limits
## Open questions                   (owner, due)

# Plan                    (plan.md)
## Constraints  ## Interfaces  ## Data model
## Decisions and rejected alternatives  ## Traceability (AC -> section)

# Tasks                   (tasks.md)
- [ ] Tn: <change> (<AC or plan ref>)  done when: <test>
```

- Twelve headings are enough; every framework template is a superset of this
- Keep the template in the repository so the agent can copy it

---

## When DIY Beats the Frameworks

- The team already has strong conventions the framework templates fight
- Several different agents in use; one set of `Markdown` files serves all of them
- Monorepo or unusual layout where `specs/` at the root makes no sense
- Regulated environments that need to control every prompt the agent runs
- Small teams who want three files, not thirty
- The frameworks win when:
    - The team is new to `SDD` and wants the order enforced
    - Nobody has time to write and maintain templates
    - The built-in analysis and clarification steps add value

---

## Choosing a Toolchain

| Constraint | Leans toward |
|---|---|
| Team standardized on one IDE | `Kiro` or Cursor rules |
| Mixed agents across the team | `Spec Kit` or DIY `Markdown` |
| Enterprise `Copilot` license only | `Spec Kit` with `Copilot` prompts |
| Heavy CLI and CI usage | `Spec Kit` with `Claude Code` |
| Strict prompt governance | DIY, prompts reviewed like code |

- Decide on the artifacts first, the tool second; artifacts outlive tools
- Licensing, data residency and which models are approved usually decide before features do
- Pilot with one feature per candidate; compare the specs produced, not the demos

---

## Migrating Between Tools: The Artifacts Are the Asset

- Every approach produces the same `Markdown` trio, so migration is a file move plus a re-pointed instruction file

| From | To | What moves | What is rewritten |
|---|---|---|---|
| `Spec Kit` | `Kiro` | `specs/*` into `.kiro/specs/*` | constitution into steering |
| `Kiro` | DIY | `.kiro/specs/*` into `docs/specs/*` | hooks into `git` or agent hooks |
| DIY | `Spec Kit` | `docs/specs/*` into `specs/*` | template headings aligned |

- Hands-on: drive the spec you repaired earlier through your team's agent: wire, plan, tasks, one task, audit
