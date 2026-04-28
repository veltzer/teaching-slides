---
tags:
  - tools:git
  - concepts:hooks
  - practices:automation
level: advanced
category: version-control
audience:
  - audiences:developers
  - audiences:devops

---
# Git Hooks

---
## What This Chapter Covers

- Where hooks live and how Git invokes them
- Client-side hooks: pre-commit, commit-msg, pre-push
- Server-side hooks: pre-receive, update, post-receive
- Sharing hooks across a team
- Integrating hooks with CI/CD

---
## What Are Git Hooks?

- Scripts in `.git/hooks/` that Git runs at lifecycle events
- Any executable file with the right name and `+x`
- Bash, Python, Ruby, anything with a shebang
- Exit non-zero to abort the action
- Per-repository by default — not pushed with the repo

---
## The Hooks Directory

```bash
ls .git/hooks/
applypatch-msg.sample  pre-applypatch.sample  pre-rebase.sample
commit-msg.sample      pre-commit.sample      pre-receive.sample
post-update.sample     pre-push.sample        update.sample
```

- Samples ship with every repo
- Strip `.sample` and add `+x` to activate
- Or replace entirely with your own script
- Local-only — not version-controlled

---
## Hook Lifecycle Visualized

![hook_lifecycle](svg/courses/git/advanced-git/04_hooks/hook_lifecycle.svg)

---
## pre-commit: Run Before Commit Is Created

- Fires when `git commit` is invoked
- Working tree is staged but commit object not yet made
- Exit non-zero — commit is aborted
- Use for linting, formatting, fast tests
- The most-used hook in practice

---
## A Practical pre-commit

```bash
#!/bin/bash
# Reject commits that fail lint or contain debug prints
if grep -nE "console\.log|TODO REMOVE" $(git diff --cached --name-only) ; then
    echo "Debug code detected — fix or unstage"
    exit 1
fi
npm run lint --silent || exit 1
```

- Runs only on staged changes
- Fast — slow hooks frustrate developers and get bypassed
- `--no-verify` skips hooks; treat that as a code smell

---
## commit-msg: Validate the Commit Message

- Fires after the message is written
- Receives the message file path as argument
- Exit non-zero — commit is aborted
- Use for enforcing message format (Conventional Commits, ticket IDs)
- Edit the file in-place to amend the message

---
## A commit-msg That Enforces Format

```bash
#!/bin/bash
msg=$(cat "$1")
pattern='^(feat|fix|docs|chore|refactor|test): .+'
if ! [[ "$msg" =~ $pattern ]]; then
    echo "Commit message must follow: type: subject"
    echo "Got: $msg"
    exit 1
fi
```

- Ensures consistent commit messages for changelog generation
- Rejects sloppy first-line summaries
- Pair with a tool like commitlint for richer validation

---
## pre-push: Last Chance Before Sharing

- Fires before any commits are sent to a remote
- Receives remote name and URL on stdin
- Receives ranges of commits being pushed
- Exit non-zero — push is aborted
- Use for slow checks: full test suites, security scans

---
## A pre-push That Runs Tests

```bash
#!/bin/bash
remote="$1"
url="$2"
if ! npm test ; then
    echo "Tests failed — push blocked"
    exit 1
fi
```

- Catches "I forgot to run tests" before the world sees it
- Runs even if the developer didn't think to run tests
- Skip with `--no-verify` if you really must

---
## post-commit and post-merge

- Fire *after* the action completes
- Cannot block anything (action is already done)
- Use for notifications, refreshing tags, regenerating files
- Common: `post-merge` regenerates dependency lockfiles
- Common: `post-commit` triggers documentation rebuilds

---
## Server-Side: pre-receive

- Fires on the *server* when a push arrives
- Receives the full list of refs being updated
- Exit non-zero — entire push is rejected
- Use for repository-wide policies: protected branches, signed commits, file size limits
- Cannot be bypassed by clients

---
## Server-Side: update

- Fires per-ref during a push
- Receives ref name, old SHA, new SHA
- Exit non-zero — that ref is rejected, others continue
- Finer-grained control than pre-receive
- Same use cases, different blast radius

---
## Server-Side: post-receive

- Fires after the push is accepted
- Cannot block anything
- Receives the updated refs on stdin
- Use for triggering CI/CD, deployments, notifications
- The hook hosting providers (GitHub, GitLab) expose

---
## Bypassing Hooks

- `git commit --no-verify` skips pre-commit and commit-msg
- `git push --no-verify` skips pre-push
- Server-side hooks cannot be bypassed
- A bypass is sometimes legitimate (broken environment)
- A bypass is usually a sign the hook is too slow or too strict

---
## The Sharing Problem

- `.git/hooks/` is per-repository, not version-controlled
- Every developer must install the same hooks
- Onboarding pain: clone, then remember to install hooks
- The fix: a hook framework managed via a manifest in the repo
- Pre-commit, husky, lefthook are common solutions

---
## Sharing Hooks With pre-commit

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: check-yaml
      - id: check-merge-conflict
```

- Manifest committed to the repo
- `pre-commit install` once per clone configures `.git/hooks/`
- Updates managed via `pre-commit autoupdate`
- Cross-language: hooks can be Python, Node, Go, Rust

---
## core.hooksPath: Out-of-Repo Hooks

```bash
git config core.hooksPath .githooks
```

- Tells Git to look in `.githooks/` instead of `.git/hooks/`
- The directory can be in the repo and version-controlled
- Every clone picks up the hooks automatically (after one config)
- Simpler than a hook framework for small teams

---
## Hooks vs CI/CD

- Hooks run on the developer's machine — fast, local feedback
- CI/CD runs on a server — authoritative, can't be skipped
- Use hooks for instant feedback (lint, format, fast tests)
- Use CI/CD for the source of truth (full suite, integration, security)
- Don't duplicate slow checks in both — pick the right layer

---
## Performance Matters

- A 30-second pre-commit destroys productivity
- Run only what's affected: lint changed files, not everything
- Cache results between runs when possible
- If a check is slow, move it to pre-push or CI
- Developers will bypass hooks they perceive as friction

---
## Common Pitfalls

- Hook script is not executable — silently skipped
- Hook depends on tools not installed in every environment
- Hook reads from stdin without consuming it — push hangs
- Working directory in server hooks is the bare repo, not a checkout
- `cd` to a known location in the script

---
## Best Practices

- Keep hooks fast — under a few seconds for pre-commit
- Hooks should fail loudly with clear messages
- Document required tools in the repo
- Use a hook framework when team size justifies it
- Server-side hooks for policy, client-side for productivity

---
## Summary

- Hooks are scripts at lifecycle points — flexible automation
- Client-side: pre-commit, commit-msg, pre-push for developer feedback
- Server-side: pre-receive, update, post-receive for policy and triggers
- Share hooks via a framework or `core.hooksPath`
- Hooks complement CI/CD; they don't replace it
