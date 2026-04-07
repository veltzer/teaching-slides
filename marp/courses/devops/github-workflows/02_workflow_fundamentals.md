# Workflow Fundamentals

---

## Workflow File Structure

```yaml
name: CI Pipeline          # Workflow name (optional)

on: push                   # Trigger event(s)

env:                       # Global environment variables
  APP_ENV: production

jobs:                      # One or more jobs
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: make build
```

- Every workflow needs at least `on` and `jobs`

---

## The `name` Field

```yaml
# Simple name
name: Build and Test

# Without name, GitHub uses the file name
# No name field -> shows as "ci.yml" in the UI
```

- Displayed in the Actions tab of your repository
- Displayed in status badges and checks
- Best practice: use descriptive, unique names

---

## The `on` Field - Triggers

```yaml
# Single event
on: push

# Multiple events
on: [push, pull_request]

# Detailed event configuration
on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main
```

- Controls **when** the workflow runs
- Can be a single event, list, or detailed map

---

## The `jobs` Field

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Building..."

  test:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Testing..."

  deploy:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Deploying..."
```

- Jobs run in **parallel** by default
- Each job gets a fresh runner instance

---

## Understanding Runners

| Runner Label       | Operating System        | CPU  | RAM   |
|--------------------|------------------------|------|-------|
| `ubuntu-latest`    | Ubuntu 22.04 or 24.04  | 2    | 7 GB  |
| `ubuntu-24.04`     | Ubuntu 24.04           | 2    | 7 GB  |
| `windows-latest`   | Windows Server 2022    | 2    | 7 GB  |
| `macos-latest`     | macOS 14 (Sonoma)      | 3    | 14 GB |
| `macos-13`         | macOS 13 (Ventura)     | 3    | 14 GB |

- GitHub-hosted runners come pre-installed with common tools
- `-latest` tags may change over time

---

## Software on GitHub Runners

- `ubuntu-latest` includes:
    - `git`, `curl`, `wget`, `jq`
    - `docker`, `docker-compose`
    - `node`, `python`, `java`, `go`, `ruby`
    - `gcc`, `make`, `cmake`
    - `aws-cli`, `az`, `gcloud`
- Full list available at:

```misc
https://github.com/actions/runner-images
```

---

## Job Dependencies and Execution Order

```yaml
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Linting..."

  test:
    needs: lint
    runs-on: ubuntu-latest
    steps:
      - run: echo "Testing..."

  deploy:
    needs: [lint, test]
    runs-on: ubuntu-latest
    steps:
      - run: echo "Deploying..."
```

- Use `needs` to create dependencies between jobs

---

## Job Dependency Flow

![job_dependency_flow](svg/courses/devops/github-workflows/02_workflow_fundamentals/job_dependency_flow.svg)

---

## Workflow Status Badges

- Add a badge to your `README.md`:

```markdown
![CI](https://github.com/OWNER/REPO/actions/workflows/ci.yml/badge.svg)
```

- Badge shows the status of the latest run:
    - Green: passing
    - Red: failing
    - Gray: no runs yet
- You can filter by branch:

```markdown
![CI](https://github.com/OWNER/REPO/actions/workflows/ci.yml/badge.svg?branch=main)
```

---

## Monitoring Workflow Runs

- **Actions tab**: View all workflow runs
- **Pull request checks**: See status on PRs
- **Email notifications**: Configure in settings
- **GitHub API**: Query run status programmatically

```bash
# List workflow runs via CLI
gh run list --workflow=ci.yml

# View a specific run
gh run view 12345

# Watch a run in real-time
gh run watch 12345
```

---

## A Practical CI Workflow

```yaml
name: Node.js CI
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: "20"
      - run: npm ci
      - run: npm test
```

---

## A Python CI Workflow

```yaml
name: Python CI
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -r requirements.txt
      - run: pytest
```
