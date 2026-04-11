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
# Best Practices and Optimization

---

## Workflow Best Practices

![GitHub Workflow best practices: reusable workflows, caching, concurrency, security, matrix](svg/courses/devops/github-workflows/08_best_practices_and_optimization/workflow_best_practices.svg)

---

## Workflow Organization

```tree
.github/
  workflows/
    ci.yml              # Continuous Integration
    cd-staging.yml      # Deploy to staging
    cd-production.yml   # Deploy to production
    codeql.yml          # Security scanning
    release.yml         # Release automation
    dependabot-merge.yml# Auto-merge dependabot PRs
  actions/
    setup-env/          # Shared composite action
      action.yml
```

- Use descriptive file names
- Separate CI from CD workflows
- Group related logic into reusable workflows or composite actions

---

## Naming Conventions

```yaml
# Workflow name - descriptive and consistent
name: "CI: Build and Test"

# Job names - describe what they do
jobs:
  lint-and-format:
    name: "Lint and Format Check"
    runs-on: ubuntu-latest
    steps:
      # Step names - action-oriented
      - name: Checkout repository
        uses: actions/checkout@v4
      - name: Install dependencies
        run: npm ci
      - name: Run ESLint
        run: npm run lint
```

---

## Security Best Practices

```yaml
# Restrict GITHUB_TOKEN permissions
permissions:
  contents: read
  pull-requests: write

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      # Pin actions to SHA
      - uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11

      # Never echo secrets
      - run: ./deploy.sh
        env:
          TOKEN: ${{ secrets.DEPLOY_TOKEN }}
```

- Set minimum required permissions
- Never use `permissions: write-all` unless absolutely needed

---

## Protecting Against Script Injection

```yaml
# VULNERABLE - user input in run command
steps:
  - run: echo "Title: ${{ github.event.issue.title }}"

# SAFE - use environment variable
steps:
  - run: echo "Title: $ISSUE_TITLE"
    env:
      ISSUE_TITLE: ${{ github.event.issue.title }}
```

- User-controlled values can contain shell metacharacters
- Always pass untrusted input through environment variables
- Avoid interpolating `${{ }}` directly in `run` scripts

---

## `GITHUB_TOKEN` Permissions

| Permission       | Read              | Write                          |
|------------------|-------------------|-------------------------------|
| `contents`       | Clone, read files | Push commits, create releases  |
| `pull-requests`  | Read PRs          | Comment, approve, merge PRs    |
| `issues`         | Read issues       | Create, label, close issues    |
| `packages`       | Download packages | Publish packages               |
| `actions`        | Read workflows    | Manage workflow runs           |
| `deployments`    | Read deployments  | Create deployments             |

---

## Performance Optimization

```yaml
steps:
  # Cache dependencies
  - uses: actions/cache@v4
    with:
      path: node_modules
      key: modules-${{ hashFiles('package-lock.json') }}

  # Skip unnecessary steps
  - name: Run expensive analysis
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    run: npm run full-analysis

  # Use shallow clones
  - uses: actions/checkout@v4
    with:
      fetch-depth: 1
```

---

## Reducing Build Times

| Strategy                    | Savings              |
|-----------------------------|----------------------|
| Cache dependencies          | 30-60%               |
| Shallow clone (depth=1)     | 10-30%               |
| Path filtering              | Skip entire runs     |
| Matrix fail-fast            | Stops on first failure |
| Smaller runner images       | Faster provisioning  |
| Conditional expensive steps | Varies               |

- Measure before optimizing: check the **timing** tab in workflow runs
- Focus on the slowest steps first

---

## Debugging Workflows

```yaml
# Enable debug logging
# Set repository secret: ACTIONS_STEP_DEBUG = true

steps:
  - name: Debug info
    run: |
      echo "Event: ${{ toJSON(github.event) }}"
      echo "Runner: ${{ toJSON(runner) }}"
      echo "Job: ${{ toJSON(job) }}"

  - name: Debug with tmate (interactive SSH)
    if: failure()
    uses: mxschmitt/action-tmate@v3
    with:
      limit-access-to-actor: true
```

---

## Troubleshooting Common Issues

| Problem                          | Solution                                   |
|----------------------------------|--------------------------------------------|
| Workflow not triggering          | Check branch filters and event types       |
| Permission denied                | Review `permissions` and `GITHUB_TOKEN`    |
| Secret not available             | Verify secret name and scope               |
| Cache not restoring              | Check `key` and `restore-keys` patterns    |
| Action version error             | Pin to a specific tag or SHA               |
| Job timeout                      | Increase `timeout-minutes` (default: 360)  |
| Scheduled workflow not running   | Only runs on default branch                |

---

## Monitoring Usage and Billing

```bash
# Check usage via GitHub CLI
gh api /repos/OWNER/REPO/actions/workflows \
  --jq '.workflows[] | {name, state}'

# List recent runs with timing
gh run list --limit 10 --json name,status,conclusion,updatedAt
```

- Monitor in: Settings -> Billing and plans -> Actions
- Set spending limits to avoid unexpected charges
- Use `timeout-minutes` to prevent runaway jobs:

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    timeout-minutes: 15
```
