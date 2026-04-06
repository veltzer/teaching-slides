# Introduction to GitHub Actions and Workflows

---

## What is CI/CD?

- **Continuous Integration (CI)**: Automatically build and test code on every change
- **Continuous Delivery (CD)**: Automatically deploy code to production
- Benefits:
    - Catch bugs early
    - Reduce manual effort
    - Faster release cycles
    - Consistent and reproducible builds

---

## Why CI/CD Matters

```text
Without CI/CD:
  Developer -> Manual Build -> Manual Test -> Manual Deploy -> Production
                  (hours)        (hours)         (hours)

With CI/CD:
  Developer -> git push -> Automated Pipeline -> Production
                              (minutes)
```

- Reduces human error
- Enables rapid iteration
- Provides immediate feedback to developers

---

## What is GitHub Actions?

- GitHub's built-in CI/CD platform
- Launched in November 2019
- Deeply integrated with GitHub repositories
- Key features:
    - Event-driven automation
    - Multi-platform support (Linux, Windows, macOS)
    - Rich ecosystem of pre-built actions
    - Free tier for public repositories

---

## GitHub Actions Architecture

```diagram
+-------------------+
|    GitHub Event    |  (push, PR, schedule, etc.)
+--------+----------+
         |
         v
+--------+----------+
|     Workflow       |  (.github/workflows/*.yml)
+--------+----------+
         |
    +----+----+
    |         |
    v         v
+---+---+ +--+----+
| Job 1 | | Job 2 |  (run in parallel or sequentially)
+---+---+ +--+----+
    |         |
    v         v
+---+---+ +--+----+
| Steps | | Steps |  (individual commands or actions)
+-------+ +-------+
```

---

## Core Components Overview

| Component  | Description                                      |
|------------|--------------------------------------------------|
| Workflow   | Automated process defined in YAML                |
| Event      | Trigger that starts a workflow                   |
| Job        | Set of steps running on the same runner           |
| Step       | Individual task within a job                     |
| Action     | Reusable unit of code for a step                 |
| Runner     | Server that executes the workflow                |

---

## Workflows, Jobs, Steps Relationship

```yaml
# Workflow
name: My CI Pipeline
on: push
jobs:
  # Job
  build:
    runs-on: ubuntu-latest
    steps:
      # Step using an action
      - uses: actions/checkout@v4
      # Step running a command
      - run: npm install
      - run: npm test
```

- A workflow contains one or more **jobs**
- Each job contains one or more **steps**
- Steps run **sequentially** within a job

---

## What Are Actions?

- Reusable building blocks for workflow steps
- Three types:
    - **JavaScript actions** - run directly on the runner
    - **Docker container actions** - run inside a container
    - **Composite actions** - combine multiple steps
- Found on the GitHub Marketplace
- Can be official, community, or custom-built

---

## GitHub Actions vs Other CI/CD Platforms

| Feature          | GitHub Actions | Jenkins    | GitLab CI  | CircleCI   |
|------------------|---------------|------------|------------|------------|
| Hosting          | Cloud/Self    | Self-hosted| Cloud/Self | Cloud      |
| Config Format    | YAML          | Groovy     | YAML       | YAML       |
| GitHub Integration| Native       | Plugin     | Limited    | Good       |
| Marketplace      | Yes           | Plugins    | Limited    | Orbs       |
| Free Tier        | Generous      | Free OSS   | Limited    | Limited    |

---

## GitHub Actions Pricing

- **Public repositories**: Free and unlimited
- **Private repositories**:
    - Free plan: 2,000 minutes/month
    - Team plan: 3,000 minutes/month
    - Enterprise: 50,000 minutes/month
- Runner minute multipliers:
    - Linux: 1x
    - Windows: 2x
    - macOS: 10x

---

## Setting Up Your First Workflow

1. Navigate to your GitHub repository
1. Click the **Actions** tab
1. Choose a starter workflow or create from scratch
1. The workflow file is created at:

```tree
your-repo/
  .github/
    workflows/
      my-workflow.yml
```

---

## The `.github/workflows` Directory

- All workflow files live in `.github/workflows/`
- Files must have `.yml` or `.yaml` extension
- Multiple workflow files can coexist
- Each file defines an independent workflow

```tree
.github/
  workflows/
    ci.yml          # Runs tests on push
    deploy.yml      # Deploys to production
    lint.yml        # Code linting
    release.yml     # Creates releases
```

---

## Basic YAML Syntax for Workflows

```yaml
# Strings
name: Build and Test

# Lists
branches:
  - main
  - develop

# Maps (key-value pairs)
env:
  NODE_VERSION: "18"
  CI: true

# Multi-line strings
run: |
  echo "Line 1"
  echo "Line 2"
```

---

## YAML Gotchas in Workflows

- Indentation matters - use **spaces**, never tabs
- Strings with special characters need quoting:

```yaml
# Wrong - YAML interprets this incorrectly
run: echo ${{ github.ref }}

# Correct - quote the expression
run: echo "${{ github.ref }}"

# Boolean gotcha
env:
  value: "true"    # string
  value: true      # boolean
```

---

## Your First Complete Workflow

```yaml
name: Hello World
on:
  push:
    branches:
      - main
jobs:
  greet:
    runs-on: ubuntu-latest
    steps:
      - name: Say Hello
        run: echo "Hello, GitHub Actions!"
      - name: Show Date
        run: date
      - name: Show Runner Info
        run: uname -a
```

- Save as `.github/workflows/hello.yml`
- Push to `main` to trigger it
