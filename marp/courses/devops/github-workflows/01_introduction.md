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

```misc
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

<svg xmlns="http://www.w3.org/2000/svg" width="640" height="295" font-family="sans-serif">
<defs>
  <marker id="arrow" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
    <polygon points="0 0, 10 3.5, 0 7" fill="#555"/>
  </marker>
</defs>
<rect x="200" y="10" width="240" height="45" fill="#c5cae9" stroke="#333" stroke-width="1.5" rx="4"/>
<text x="320" y="28" font-size="13" font-weight="bold" fill="#222" text-anchor="middle">GitHub Event</text>
<text x="320" y="43" font-size="10" font-weight="normal" fill="#222" text-anchor="middle">(push, PR, schedule, etc.)</text>
<line x1="320" y1="55" x2="320" y2="80" stroke="#555" stroke-width="1.5" marker-end="url(#arrow)"/>
<rect x="200" y="80" width="240" height="45" fill="#e3f2fd" stroke="#333" stroke-width="1.5" rx="4"/>
<text x="320" y="98" font-size="13" font-weight="bold" fill="#222" text-anchor="middle">Workflow</text>
<text x="320" y="113" font-size="10" font-weight="normal" fill="#222" text-anchor="middle">(.github/workflows/*.yml)</text>
<line x1="320" y1="125" x2="320" y2="145" stroke="#555" stroke-width="1.5"/>
<line x1="320" y1="145" x2="170" y2="145" stroke="#555" stroke-width="1.5"/>
<line x1="320" y1="145" x2="470" y2="145" stroke="#555" stroke-width="1.5"/>
<line x1="170" y1="145" x2="170" y2="165" stroke="#555" stroke-width="1.5" marker-end="url(#arrow)"/>
<line x1="470" y1="145" x2="470" y2="165" stroke="#555" stroke-width="1.5" marker-end="url(#arrow)"/>
<rect x="100" y="165" width="140" height="45" fill="#e8f5e9" stroke="#333" stroke-width="1.5" rx="4"/>
<text x="170" y="183" font-size="13" font-weight="bold" fill="#222" text-anchor="middle">Job 1</text>
<text x="170" y="198" font-size="9" font-weight="normal" fill="#222" text-anchor="middle">(parallel or sequential)</text>
<line x1="170" y1="210" x2="170" y2="240" stroke="#555" stroke-width="1.5" marker-end="url(#arrow)"/>
<rect x="100" y="240" width="140" height="40" fill="#fff3e0" stroke="#333" stroke-width="1.5" rx="4"/>
<text x="170" y="255" font-size="12" font-weight="bold" fill="#222" text-anchor="middle">Steps</text>
<text x="170" y="270" font-size="9" font-weight="normal" fill="#222" text-anchor="middle">(commands/actions)</text>
<rect x="400" y="165" width="140" height="45" fill="#e8f5e9" stroke="#333" stroke-width="1.5" rx="4"/>
<text x="470" y="183" font-size="13" font-weight="bold" fill="#222" text-anchor="middle">Job 2</text>
<text x="470" y="198" font-size="9" font-weight="normal" fill="#222" text-anchor="middle">(parallel or sequential)</text>
<line x1="470" y1="210" x2="470" y2="240" stroke="#555" stroke-width="1.5" marker-end="url(#arrow)"/>
<rect x="400" y="240" width="140" height="40" fill="#fff3e0" stroke="#333" stroke-width="1.5" rx="4"/>
<text x="470" y="255" font-size="12" font-weight="bold" fill="#222" text-anchor="middle">Steps</text>
<text x="470" y="270" font-size="9" font-weight="normal" fill="#222" text-anchor="middle">(commands/actions)</text>
</svg>

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
