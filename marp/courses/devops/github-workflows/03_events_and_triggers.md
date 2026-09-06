---
tags:
  - tools:github
  - practices:ci-cd
  - practices:automation
  - practices:devops
level: intermediate
category: devops
audience:
  - audiences:developers
  - audiences:devops
  - audiences:managers

---

# Events and Triggers

---

## Workflow Trigger Types

![trigger_types](svg/courses/devops/github-workflows/03_events_and_triggers/trigger_types.svg)

---

## Push Event Trigger

```yaml
on:
  push:
    branches:
      - main
      - develop
      - "release/**"
    tags:
      - "v*"
```

- Triggers when commits are pushed
- Filter by branches and tags
- Supports glob patterns with `**`

---

## Pull Request Event Trigger

```yaml
on:
  pull_request:
    branches:
      - main
    types:
      - opened
      - synchronize
      - reopened
      - closed
```

- Defaults to `opened`, `synchronize`, `reopened`
- Use `types` to specify exact activity types
- PR workflows run on the **merge commit**

---

## Push vs Pull Request Events

| Aspect              | `push`                    | `pull_request`           |
|---------------------|---------------------------|--------------------------|
| Trigger             | Direct push to branch     | PR opened/updated        |
| Runs on             | Pushed commit             | Merge commit             |
| Secrets access      | Full access               | Limited for forks        |
| Common use          | Deploy, publish           | CI checks, code review   |
| `GITHUB_REF`        | `refs/heads/branch`       | `refs/pull/N/merge`      |

---

## Scheduled Workflows with Cron

```yaml
on:
  schedule:
    - cron: "0 6 * * 1"
```

- Uses standard cron syntax (UTC timezone)

```cron
 ┌───────────── minute (0-59)
 │ ┌───────────── hour (0-23)
 │ │ ┌───────────── day of month (1-31)
 │ │ │ ┌───────────── month (1-12)
 │ │ │ │ ┌───────────── day of week (0-6, Sun=0)
 │ │ │ │ │
 * * * * *
```

---

## Cron Expression Examples

| Expression       | Schedule                        |
|------------------|---------------------------------|
| `0 0 * * *`      | Every day at midnight UTC       |
| `30 5 * * 1-5`   | Weekdays at 5:30 AM UTC        |
| `0 */6 * * *`    | Every 6 hours                   |
| `0 12 1 * *`     | First day of month at noon      |
| `0 0 * * 0`      | Every Sunday at midnight        |

- Minimum interval: once every 5 minutes
- Scheduled workflows run on the default branch only

---

## Manual Workflow Dispatch

```yaml
on:
  workflow_dispatch:
    inputs:
      environment:
        description: "Target environment"
        required: true
        type: choice
        options:
          - staging
          - production
      debug:
        description: "Enable debug logging"
        required: false
        type: boolean
        default: false
```

- Adds a "Run workflow" button in the Actions tab

---

## Using `workflow_dispatch` Inputs

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to environment
        run: |
          echo "Deploying to ${{ inputs.environment }}"
          if [ "${{ inputs.debug }}" = "true" ]; then
            echo "Debug mode enabled"
          fi
```

- Input types: `string`, `boolean`, `choice`, `environment`
- Access via `${{ inputs.input_name }}`

---

## Repository Events

```yaml
on:
  issues:
    types: [opened, labeled]
  release:
    types: [published]
  fork:
  watch:
    types: [started]
  create:
  delete:
```

- Automate responses to repository activities
- Each event type has specific `types` you can filter on

---

## Issue and PR Automation Example

```yaml
name: Auto-label Issues
on:
  issues:
    types: [opened]
jobs:
  label:
    runs-on: ubuntu-latest
    steps:
      - name: Add triage label
        uses: actions/github-script@v7
        with:
          script: |
            await github.rest.issues.addLabels({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: context.issue.number,
              labels: ['triage']
            })
```

---

## Repository Dispatch (External Triggers)

```yaml
on:
  repository_dispatch:
    types: [deploy-event]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - run: echo "${{ github.event.client_payload.env }}"
```

- Trigger from external systems via API:

```bash
curl -X POST \
  -H "Authorization: token $TOKEN" \
  -d '{"event_type":"deploy-event","client_payload":{"env":"prod"}}' \
  https://api.github.com/repos/OWNER/REPO/dispatches
```

---

## Conditional Execution with `if`

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - name: Run only on Linux
        if: runner.os == 'Linux'
        run: echo "Linux only step"

      - name: Run on tag push
        if: startsWith(github.ref, 'refs/tags/')
        run: echo "Tagged release"
```

- Apply `if` to jobs or individual steps
- Uses GitHub Actions expression syntax

---

## Common `if` Conditions

| Condition                                    | Meaning                     |
|----------------------------------------------|-----------------------------|
| `github.ref == 'refs/heads/main'`            | Only on main branch         |
| `github.event_name == 'pull_request'`        | Only on pull requests       |
| `contains(github.event.head_commit.message, '[skip ci]')` | Commit message check |
| `success()`                                  | Previous steps succeeded    |
| `failure()`                                  | A previous step failed      |
| `always()`                                   | Run regardless of status    |
| `cancelled()`                                | Workflow was cancelled      |

---

## Path-Based Filtering

```yaml
on:
  push:
    paths:
      - "src/**"
      - "tests/**"
      - "package.json"
    paths-ignore:
      - "docs/**"
      - "**.md"
      - ".gitignore"
```

- `paths`: only run when matching files change
- `paths-ignore`: skip when only these files change
- Cannot use both `paths` and `paths-ignore` together

---

## Branch and Tag Targeting

```yaml
on:
  push:
    branches:
      - main
      - "release/*"
      - "!release/beta*"
    tags:
      - "v[0-9]+.[0-9]+.[0-9]+"
  pull_request:
    branches-ignore:
      - "draft/**"
```

- Use `!` prefix to exclude patterns
- `branches` and `branches-ignore` cannot be used together
- Tag patterns support glob matching
