---
tags:
  - practices:code-review
  - practices:automation
level: beginner
category: methodology
audience:
  - audiences:developers

---

# Automated Checks

---

## Automated Check Layers

![automation_layers](svg/courses/development_methodologies/code-review-best-practices/09_automated_checks/automation_layers.svg)

---

## What This Chapter Covers

- Linters and formatters
- CI pipelines in reviews
- Static analysis tools
- Automated security scanning
- Bot-assisted reviews
- The right division of labour: bots and humans

---

## Why Automate

- Robots catch rote issues fast
- Humans focus on substance
- Consistent enforcement across PRs and time
- 24/7 review without timezone friction
- Free up your senior engineers

---

## CI Checks

![ci_checks](svg/courses/development_methodologies/code-review-best-practices/09_automated_checks/ci_checks.svg)

---

## Linters

- Tools that flag suspicious patterns
- Examples: ESLint, Pylint, Rubocop, Clippy, SwiftLint
- Catch: dead code, naming issues, common bugs, complexity
- Run in CI; fail builds on errors
- Configurable to your team's standards

---

## Formatters

- Auto-format code to a standard
- Examples: Prettier, Black, gofmt, rustfmt, clang-format
- Settle the bikeshed: tabs vs spaces, brace style, line length
- Run on save, pre-commit, or in CI
- "Done" if formatter is clean; no human review needed for style

---

## Pre-Commit Hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 24.0.0
    hooks: [{ id: black }]
  - repo: https://github.com/charliermarsh/ruff-pre-commit
    rev: v0.5.0
    hooks: [{ id: ruff }]
```

- Run automatically before each commit
- `pre-commit` framework manages many tools
- Fix issues before they reach CI
- Faster feedback loop

---

## Static Analysis

- Deeper than linting; analyses code paths and types
- Examples: SonarQube, CodeClimate, mypy, pyright, Coverity
- Catch: data flow issues, unhandled errors, type mismatches
- Run in CI; surface results in the PR
- Good for catching issues that lint doesn't see

---

## Type Checkers

- mypy, pyright (Python); TypeScript; Flow (JS); Sorbet (Ruby)
- Find: wrong argument types, missing return values, null deref
- Best when type annotations are required
- Project-level rollout: gradual is fine
- Modern teams treat type errors like compile errors

---

## Security Scanning

- **SAST** (Static): scans source code for vulnerabilities
- **SCA** (Software Composition Analysis): vulnerable dependencies
- **DAST** (Dynamic): runs the app and probes
- **Secret scanning**: API keys, passwords in source
- All can run in CI

---

## Common Security Tools

- Snyk: deps + container scanning
- Dependabot / Renovate: dep updates + CVE alerts
- CodeQL: deep static analysis (GitHub-native)
- Trivy: container + filesystem scanning
- TruffleHog: secret scanning

---

## CI Pipelines

- Build, test, lint, scan
- All run on every PR
- All must pass before merge (or with explicit override)
- Fast pipelines (under 10 min) keep developers engaged
- Slow pipelines lead to "merge anyway" pressure

---

## What CI Should Block

- Failing tests
- Linter errors
- Type errors
- Security high-severity findings
- License compliance failures
- Build failures (obviously)

---

## What CI Should Warn

- New low-severity findings
- Coverage drops
- Performance regressions
- Style nits the formatter didn't catch
- Warnings keep visibility without blocking

---

## Review Bots

- Comment on PRs automatically
- "PR is too large", "test coverage dropped", "this dep has a CVE"
- Each bot should add value, not just noise
- If everyone ignores a bot's comments, retire it
- Pull-request-bot review systems (CodeRabbit, Greptile) exist

---

## Bot Configuration

- Severity thresholds (only comment on important issues)
- Path filters (don't lint generated code)
- Owner-only comments (don't notify everyone)
- Per-team rules
- Bots well-tuned save hours; bots ignored waste them

---

## Auto-Merge

- PRs merge automatically when conditions met
- Useful for: dependency bumps, doc-only changes
- Combined with required reviews and CI
- Reduces "merge it and forget" backlog
- Configure carefully; auto-merging the wrong thing is bad

---

## The Limits of Automation

- Bots don't catch design issues
- Bots don't ask "should this exist?"
- Bots can't mentor
- Bots don't replace knowledge sharing
- Use them for what they're good at; humans for the rest

---

## Common Mistakes

- Disabling failing checks instead of fixing the issues
- Bots that comment on every change &#8594; drowned signal
- No CI &#8594; slow feedback &#8594; "ship it" pressure
- Trusting bots blindly &#8594; missed real issues
- Treating green CI as "good code" — it's necessary, not sufficient
