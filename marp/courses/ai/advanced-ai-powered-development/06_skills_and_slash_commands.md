# Skills and Slash Commands

## Overview
- What are skills in AI development tools
- Built-in vs custom skills
- Creating and parameterizing custom skills
- Practical skill examples for real workflows
- Sharing skills across teams
- Hooks: automating actions around tool calls

---

## What Are Skills?

## Reusable AI Capabilities
- Skills are packaged instructions that extend an AI tool's behavior
- Think of them as "macros" or "plugins" for your AI assistant
- Invoked via slash commands (e.g., `/commit`, `/review-pr`)
- Encapsulate domain knowledge, team conventions, and workflows

```misc
User types:  /review-pr 1234
             ^^^^^^^^^^
             skill name
```

- Skills bridge the gap between generic AI and team-specific needs
- They reduce prompt repetition and enforce consistency

---

## Built-in vs Custom Skills

## Two Tiers of Capability

| Aspect | Built-in Skills | Custom Skills |
|--------|----------------|---------------|
| Source | Ships with the tool | Defined by your team |
| Scope | Generic workflows | Domain-specific |
| Update | Tool vendor | You control |
| Examples | `/commit`, `/help` | `/deploy-staging`, `/db-migrate` |

- Built-in skills cover common developer tasks
- Custom skills encode your organization's specific processes
- Custom skills live in project config (e.g., `.claude/skills/`)

---

## Skill Discovery and Self-Documentation

## Finding and Understanding Available Skills

```bash
# List all available skills (built-in and custom)
claude skills list
# Get detailed info on a specific skill
claude skills info review
# Show auto-generated help with parameters
claude skills help /deploy --verbose
```

- Every skill auto-generates help from its `description` and `parameters`
- Use `claude skills list --format=json` for programmatic discovery
- Teams can add a `docs` field for extended usage examples

```yaml
name: deploy
description: "Run deployment checklist"
docs: |
  ## Usage Examples
  /deploy env=staging
  /deploy env=production --dry-run
```

---

## Skill Definition and Structure

## Anatomy of a Custom Skill

```yaml
# .claude/skills/review.yaml
name: review
description: "Review code for security and performance"
trigger: /review
parameters:
  - name: focus
    type: string
    default: "all"
    description: "Area to focus on: security|perf|all"
instructions: |
  Review the staged changes with focus on {{ focus }}.
  Check for:
  - SQL injection and XSS vulnerabilities
  - N+1 query patterns
  - Missing error handling
  Output a structured report with severity levels.
```

- `trigger` maps to the slash command
- `parameters` accept user input
- `instructions` use templating for dynamic prompts

---

## Context Variables and Templating

## Dynamic Instructions with Jinja Syntax

Available context variables in skill instructions:

| Variable | Description |
|----------|-------------|
| `$FILE` | Current file path being operated on |
| `$COMMIT_SHA` | Latest commit hash |
| `$BRANCH` | Current git branch name |
| `$PR_NUMBER` | Pull request number (in PR context) |
| `$DIFF` | Staged or current diff content |

```yaml
instructions: |
  {% if BRANCH.startswith("hotfix/") %}
  Apply stricter review criteria for hotfix branches.
  {% endif %}
  Reviewing changes on `{{ BRANCH }}` at commit `{{ COMMIT_SHA }}`:
  {% for file in changed_files %}
  - Analyze {{ file }} for {{ focus }} issues
  {% endfor %}
```

- Jinja2 templating supports conditionals, loops, and filters
- Variables are injected automatically by the runtime

---

## Parameterized Skills

## Making Skills Flexible

```yaml
name: test-gen
trigger: /test-gen
parameters:
  - name: file
    type: string
    required: true
  - name: framework
    type: enum
    values: [pytest, jest, vitest]
    default: pytest
  - name: coverage
    type: number
    default: 80
instructions: |
  Generate tests for {{ file }} using {{ framework }}.
  Target {{ coverage }}% branch coverage.
  Follow AAA pattern (Arrange, Act, Assert).
```

Usage:

```bash
/test-gen file=src/auth/login.py framework=pytest coverage=90
```

---

## Conditional Skills

## Skills That Activate Based on Context

```yaml
name: style-check
trigger: /style
conditions:
  file_type: ["*.py", "*.js", "*.ts"]
  branch: ["feature/*", "fix/*"]
  context:
    has_staged_changes: true
instructions: |
  {% if file_type == "py" %}
  Check PEP 8 compliance and type hints.
  {% elif file_type in ["js", "ts"] %}
  Check ESLint rules and TypeScript strictness.
  {% endif %}
```

- `conditions` gate when a skill is available or relevant
- File-type conditions auto-select the right linter or formatter
- Branch conditions enforce different rigor levels per workflow
- Context conditions check for staged changes, open PRs, or CI status

---

## Skill Composition and Chaining

## Building Complex Workflows from Simple Skills

![building_complex_workflows_from_simple_skills](/svg/courses/ai/advanced-ai-powered-development/06_skills_and_slash_commands/building_complex_workflows_from_simple_skills.svg)

```yaml
name: ship-it
trigger: /ship-it
chain:
  - skill: lint
    on_fail: abort
  - skill: review
    params: { focus: "security" }
  - skill: commit
    params: { message: "auto" }
  - skill: create-pr
    params: { draft: false }
```

- Each step receives context from the previous one
- `on_fail` controls flow: `abort`, `skip`, or `warn`

---

## Error Handling and Resilience

## Strategies When Skills Fail

| Strategy | Behavior |
|----------|----------|
| `abort` | Stop the entire chain immediately |
| `skip` | Log the failure and continue to next step |
| `warn` | Display a warning and continue |
| `retry` | Retry up to N times with backoff |

```yaml
chain:
  - skill: lint
    on_fail: abort
  - skill: test-gen
    on_fail: retry
    retry:
      max_attempts: 3
      backoff: exponential
  - skill: deploy
    on_fail: warn
    timeout: 300s
```

- Set `timeout` to prevent skills from hanging indefinitely
- Combine `on_fail` with `fallback` to try an alternative skill
- Log all failures to `$PROJECT/.claude/logs/` for post-mortem analysis

---

## Debugging and Testing Skills

## Validating Skills Before Production Use

```bash
# Dry-run: see what the skill would do without executing
claude skills run /deploy env=staging --dry-run
# Verbose mode: show template expansion and variable values
claude skills run /review --verbose
# Test against a known diff for deterministic output
claude skills test /sec-review \
  --input fixtures/known_vuln.diff \
  --expected fixtures/expected_report.md
```

- `--dry-run` expands templates and shows the resolved prompt
- `--verbose` logs each step, variable binding, and tool call
- Snapshot testing catches regressions in skill behavior

```yaml
# .claude/skills/tests/review_test.yaml
skill: security-review
input:
  diff: "fixtures/sql_injection.diff"
expect:
  contains: ["SQL injection", "HIGH"]
```

---

## Practical Skill: Code Review

## Structured, Repeatable Reviews

```yaml
name: security-review
trigger: /sec-review
instructions: |
  Analyze the current diff for:
  1. Input validation gaps
  1. Authentication/authorization flaws
  1. Secrets or credentials in code
  1. Dependency vulnerabilities
  Output format:
  ## Findings
  | Severity | File | Line | Issue |
  |----------|------|------|-------|
  ...
  ## Recommendations
  - Actionable fix for each finding
```

- Enforces a consistent review checklist
- Output format integrates with issue trackers
- Can be extended with `parameters` for scope control

---

## Practical Skill: Commit and PR Workflows

## Automating Git Conventions

```yaml
name: smart-commit
trigger: /commit
instructions: |
  Analyze staged changes. Generate a commit message:
  - Use conventional commits (feat/fix/refactor/docs/test)
  - First line under 72 chars
  - Add body explaining "why" not "what"
  - Reference related issue numbers if detectable
```

```yaml
name: create-pr
trigger: /pr
parameters:
  - name: base
    type: string
    default: main
instructions: |
  Create a PR against {{ base }}:
  - Title: conventional format, under 70 chars
  - Body: summary bullets, test plan, breaking changes
  - Add labels based on file paths changed
```

---

## Practical Skill: Deployment and Migration

## Encoding Operational Knowledge

```yaml
name: deploy
trigger: /deploy
parameters:
  - name: env
    type: enum
    values: [staging, production]
instructions: |
  Run deployment checklist for {{ env }}:
  1. Verify all tests pass on current branch
  1. Check for pending migrations
  1. Validate env-specific config files exist
  1. Generate deployment manifest
  {% if env == "production" %}
  1. Require explicit confirmation
  1. Check rollback plan exists
  {% endif %}
```

```yaml
name: db-migrate
trigger: /db-migrate
instructions: |
  Generate a migration file for the described schema change.
  - Use the project's migration framework (detect automatically)
  - Include both up and down migrations
  - Add a data migration step if column rename detected
```

---

## Skills for CI/CD Integration

## Triggering Skills from Pipelines

```yaml
# .github/workflows/ai-review.yml
on:
  pull_request:
    types: [opened, synchronize]
jobs:
  ai-review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: claude skills run /sec-review --ci
        env:
          CLAUDE_API_KEY: ${{ secrets.CLAUDE_API_KEY }}
```

- Use `--ci` flag to suppress interactive prompts
- Skills can post results as PR comments via `$PR_NUMBER`
- Chain skills in pipelines: lint, review, then gate deployment

```yaml
# Post-merge: auto-generate changelog
on:
  push:
    branches: [main]
steps:
  - run: claude skills run /changelog --since=$PREV_TAG
```

---

## Sharing Skills Across Teams

## Skills as Code

```tree
.claude/
  skills/
    review.yaml
    commit.yaml
    deploy.yaml
  teams/
    backend/
      db-migrate.yaml
    frontend/
      component-gen.yaml
```

- Skills live in version control alongside the codebase
- Team-scoped directories allow role-specific skills
- Share across repos via git submodules or a central skills registry

```bash
# Install shared skills from a central repo
claude skills install git@github.com:acme/ai-skills.git
# Override a shared skill locally
claude skills override review --local
```

- Versioned skills ensure reproducibility across environments

---

## Skill Inheritance and Overrides

## Project-Level vs User-Level vs Team-Level

![project_level_vs_user_level_vs_team_level](/svg/courses/ai/advanced-ai-powered-development/06_skills_and_slash_commands/project_level_vs_user_level_vs_team_level.svg)

- Resolution order: project > team > user (most specific wins)
- User-level skills provide personal defaults across all projects
- Team-level skills target role-specific workflows
- Override any inherited skill with a local definition

```yaml
# .claude/skills/review.yaml (project override)
extends: shared/review
instructions: |
  {{ parent.instructions }}
  Additionally, check for Django-specific ORM issues.
```

---

## Skill Versioning and Breaking Changes

## Semantic Versioning for Skills

```yaml
name: deploy
version: "2.1.0"
min_tool_version: "1.5.0"
deprecated_params:
  - name: target
    removed_in: "3.0.0"
    use_instead: env
    message: "Use 'env' parameter instead of 'target'"
```

- Follow semver: `MAJOR.MINOR.PATCH`
    - Major: breaking changes to parameters or output format
    - Minor: new optional parameters, backward-compatible
    - Patch: bug fixes and prompt improvements
- `deprecated_params` warns users before removal
- `min_tool_version` prevents running on incompatible runtimes

```bash
# Check for outdated skills in the project
claude skills audit --check-versions
```

---

## Hooks: Pre and Post-Execution

## Automating Actions Around Tool Calls

![automating_actions_around_tool_calls](/svg/courses/ai/advanced-ai-powered-development/06_skills_and_slash_commands/automating_actions_around_tool_calls.svg)

```yaml
# .claude/hooks.yaml
hooks:
  pre:
    - event: file_edit
      run: "scripts/check_file_lock.sh $FILE"
      on_fail: block
    - event: bash_command
      match: "rm -rf *"
      action: block
      message: "Destructive command blocked by policy"
  post:
    - event: commit
      run: "scripts/notify_slack.sh $COMMIT_SHA"
```

---

## Hook Ordering, Priority, and Conflicts

## Controlling Execution Order

```yaml
hooks:
  pre:
    - event: file_edit
      priority: 10
      run: "scripts/check_permissions.sh $FILE"
      on_fail: block
    - event: file_edit
      priority: 20
      run: "scripts/validate_schema.sh $FILE"
      on_fail: warn
    - event: file_edit
      priority: 30
      run: "scripts/format_check.sh $FILE"
      short_circuit: true
```

- Hooks execute in ascending `priority` order (lower runs first)
- `short_circuit: true` stops remaining hooks if this one fails
- When two hooks conflict, the higher-priority hook wins
- Use `group` to bundle related hooks for easier management

```yaml
    - event: file_edit
      group: security
      priority: 5
```

---

## Security and Sandboxing

## Permission Scoping and Audit Logging

```yaml
# .claude/security.yaml
permissions:
  skills:
    deploy:
      allowed_commands: ["kubectl", "helm", "docker"]
      blocked_commands: ["rm", "curl", "wget"]
      allowed_paths: ["deploy/", "k8s/"]
      require_approval: true
  hooks:
    audit_log: ".claude/logs/audit.jsonl"
    max_execution_time: 30s
```

- Restrict which shell commands a skill can invoke
- Limit file access to specific directories
- `require_approval` forces user confirmation before execution
- All skill and hook actions are logged for audit trails

```jsonl
{"ts":"2026-03-09T10:15:00Z","skill":"deploy","cmd":"kubectl apply","user":"ci","status":"approved"}
```

---

## Notification and Validation Hooks

## Guard Rails for AI-Assisted Development

```yaml
hooks:
  pre:
    # Validate before any database tool call
    - event: bash_command
      match: "psql.*DROP|migrate.*down"
      action: confirm
      message: "Destructive DB operation detected. Proceed?"

    # Block secrets from being written
    - event: file_edit
      run: "scripts/scan_secrets.sh $FILE"
      on_fail: block

  post:
    # Notify on PR creation
    - event: pr_create
      run: |
        curl -X POST $SLACK_WEBHOOK \
          -d "{\"text\": \"PR #$PR_NUMBER created by AI assistant\"}"

    # Auto-run tests after file changes
    - event: file_edit
      match: "src/**/*.ts"
      run: "npm test -- --related $FILE"
```

- `confirm` pauses and asks the user before proceeding
- `block` prevents the action entirely
- Hooks compose with skills for full workflow control

---

## Monitoring Skill Effectiveness

## Tracking Usage, Success Rates, and Time Saved

```bash
# View skill usage statistics
claude skills stats --last 30d
# Output:
# Skill          | Runs | Success | Avg Time | Est. Saved
# /commit        |  142 |   98%   |   4.2s   |  11.8 hrs
# /sec-review    |   87 |   94%   |  12.1s   |   7.3 hrs
# /deploy        |   23 |   91%   |  45.3s   |   3.1 hrs
```

- Track `success_rate` to identify skills that need refinement
- Compare `avg_time` against manual baselines to quantify ROI
- Set alerts for skills dropping below a success threshold

```yaml
# .claude/monitoring.yaml
alerts:
  - skill: "*"
    condition: success_rate < 0.85
    notify: "slack:#ai-tools"
  - skill: deploy
    condition: avg_time > 120s
    notify: "email:ops@acme.com"
```

---

## Adoption Patterns and Anti-Patterns

## Getting Skills Right in Your Organization

**Start small, iterate fast:**
1. Begin with one or two high-value, low-risk skills (e.g., `/commit`)
1. Measure usage and gather feedback before expanding
1. Promote successful experiments to team-wide standards

**Common anti-patterns to avoid:**

| Anti-Pattern | Problem | Better Approach |
|-------------|---------|-----------------|
| Mega-skill | One skill does everything | Compose small, focused skills |
| No parameters | Hardcoded values everywhere | Use parameters with sensible defaults |
| No testing | Skills break silently | Add snapshot tests and `--dry-run` |
| Copy-paste skills | Drift between copies | Use inheritance and shared registries |

- Treat skills like code: review, test, version, and document them
- Assign skill ownership to prevent orphaned definitions

---

## Putting It All Together

## A Complete Skill + Hook Workflow

```yaml
# .claude/skills/ship-feature.yaml
name: ship-feature
trigger: /ship
chain:
  - skill: lint
  - skill: security-review
  - skill: smart-commit
  - skill: create-pr
```

```yaml
# .claude/hooks.yaml
hooks:
  pre:
    - event: commit
      run: "npm run lint && npm test"
      on_fail: block
  post:
    - event: pr_create
      run: "scripts/assign_reviewers.sh $PR_NUMBER"
```

Key takeaways:
- Skills encode **what** to do; hooks enforce **when** and **how**
- Both live in version control and travel with the project
- Start with built-in skills, then customize as patterns emerge

---

## Hands-On: Create a Custom Review Skill

## Exercise: Build a `/team-review` Skill

**Step 1:** Create the skill file

```bash
mkdir -p .claude/skills && touch .claude/skills/team-review.yaml
```

**Step 2:** Define the skill structure

```yaml
name: team-review
trigger: /team-review
parameters:
  - name: focus
    type: enum
    values: [security, performance, readability, all]
    default: all
instructions: |
  Review the current diff focusing on {{ focus }}.
  Flag issues with severity: CRITICAL, WARN, INFO.
```

**Step 3:** Test with `--dry-run` and iterate

```bash
claude skills run /team-review focus=security --dry-run
```

**Goal:** Produce a working review skill tailored to your team's checklist

---

## Hands-On: Set Up Project Hooks

## Exercise: Configure Pre and Post Hooks

**Step 1:** Create the hooks file

```bash
touch .claude/hooks.yaml
```

**Step 2:** Add a pre-hook to block dangerous commands

```yaml
hooks:
  pre:
    - event: bash_command
      match: "rm -rf|DROP TABLE|truncate"
      action: block
      message: "Destructive operation blocked by project policy"
    - event: file_edit
      run: "scripts/check_format.sh $FILE"
      on_fail: warn
```

**Step 3:** Add a post-hook for notifications

```yaml
  post:
    - event: commit
      run: "echo Commit $COMMIT_SHA by AI assistant >> .claude/logs/activity.log"
```

**Goal:** Verify hooks trigger correctly using `claude hooks test --event file_edit`
