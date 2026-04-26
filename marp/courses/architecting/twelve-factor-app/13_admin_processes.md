---
tags:
  - concepts:architecture
  - practices:devops
level: intermediate
category: architecture
audience:
  - audiences:developers
  - audiences:devops

---
# Factor XII: Admin Processes

---
## The Rule

- Run admin and management tasks as one-off processes
- Same codebase, same dependencies, same release as the running app
- Triggered manually or by automation, not embedded in the running app

---
## What Counts as Admin

- Database migrations
- Data fixes (one-time scripts)
- Backfills
- One-off data exports
- Interactive REPLs for debugging
- Diagnostic tasks (cleanup, integrity checks)

---
## Same Codebase, Same Release

- Admin scripts live in the app's repo
- They use the app's domain code, not parallel copies
- They run against the same release that's in production
- "I ran my fix against last week's code" → bugs

---
## Same Environment

- Admin scripts read the same config (env vars)
- Connect to the same backing services
- Run on a host with the same image
- The only thing different: the entry point

---
## Examples

- `python manage.py migrate` (Django)
- `rails db:migrate` (Rails)
- `npx knex migrate:latest` (Node + Knex)
- A Kubernetes Job that runs the same image with a different command

---
## Why It Matters

- Production fixes that diverge from production code are how outages happen
- "I tested it on my laptop" is not enough for a fix that touches production data
- One-off scripts in the repo + reviewed = much safer
- Automation can rerun them; ad-hoc scripts can't

---
## Migrations as Admin Processes

- Migrations are the canonical example
- Versioned, reversible, auditable
- Run as a separate process, not embedded in the app's startup
- The app's startup might wait until migrations have completed

---
## REPLs

- An interactive shell with the app's code loaded
- For debugging production data, exploring state, running ad-hoc queries
- `python manage.py shell`, `rails console`, etc.
- Same codebase, same env — just an interactive entry point

---
## Anti-Patterns

- Admin script copy-pasted from a notebook, never reviewed
- Migrations run from a developer laptop against production
- One-off scripts that depend on a special environment that nobody documents
- Running ad-hoc SQL through a database GUI when the app has a domain function

---
## Automation

- Common admin tasks should be automatable
- A backfill script that runs once a year should still be in the repo, not lost in someone's notes
- "What did I run last time we had this incident?" should be answerable from git log

---
## Summary

- Admin tasks are one-off processes
- Same codebase, same release, same environment as the running app
- Migrations and REPLs are the canonical examples
- Reviewed, repeatable, in version control — not ad-hoc
