# Environment Management

---

## Environment Variables Overview

![environment_variables_overview](/svg/courses/devops/github-workflows/05_environment_management/environment_variables_overview.svg)

- More specific levels override broader ones

---

## Setting Environment Variables

```yaml
# Workflow-level
env:
  APP_NAME: my-app

jobs:
  build:
    runs-on: ubuntu-latest
    # Job-level
    env:
      NODE_ENV: production
    steps:
      - name: Build
        # Step-level
        env:
          DEBUG: "true"
        run: |
          echo "App: $APP_NAME"
          echo "Env: $NODE_ENV"
          echo "Debug: $DEBUG"
```

---

## Dynamic Environment Variables with `$GITHUB_ENV`

```yaml
steps:
  - name: Set dynamic variable
    run: echo "BUILD_TIME=$(date -u +%Y%m%d%H%M%S)" >> "$GITHUB_ENV"

  - name: Use dynamic variable
    run: echo "Build time is $BUILD_TIME"
```

- Append to `$GITHUB_ENV` to set variables for **subsequent** steps
- The variable is NOT available in the same step that sets it
- Format: `NAME=VALUE`

---

## Multi-Line Environment Variables

```yaml
steps:
  - name: Set multi-line variable
    run: |
      echo "CONFIG<<EOF" >> "$GITHUB_ENV"
      echo "host=localhost" >> "$GITHUB_ENV"
      echo "port=3000" >> "$GITHUB_ENV"
      echo "EOF" >> "$GITHUB_ENV"

  - name: Use multi-line variable
    run: echo "$CONFIG"
```

- Use heredoc-style delimiter for multi-line values
- Choose a unique delimiter (e.g., `EOF`)

---

## GitHub Secrets

- Encrypted variables stored in repository settings
- Never printed in logs (masked with `***`)
- Setting secrets:

```misc
Settings -> Secrets and variables -> Actions -> New repository secret
```

- Using secrets in workflows:

```yaml
steps:
  - name: Deploy
    env:
      API_KEY: ${{ secrets.API_KEY }}
    run: ./deploy.sh
```

---

## Types of Secrets

| Scope         | Set By          | Available To                   |
|---------------|-----------------|-------------------------------|
| Repository    | Repo admin      | All workflows in the repo      |
| Environment   | Repo admin      | Jobs targeting that environment|
| Organization  | Org admin       | Selected repositories          |

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production
    steps:
      - run: echo "Using prod secrets"
        env:
          DB_URL: ${{ secrets.DATABASE_URL }}
```

---

## Managing Secrets via CLI

```bash
# Set a repository secret
gh secret set API_KEY --body "my-secret-value"

# Set from a file
gh secret set SSH_KEY < ~/.ssh/id_rsa

# List secrets (values are never shown)
gh secret list

# Set an environment secret
gh secret set DB_URL --env production

# Delete a secret
gh secret delete API_KEY
```

---

## Context Variables

```yaml
steps:
  - name: Show context info
    run: |
      echo "Repo: ${{ github.repository }}"
      echo "Branch: ${{ github.ref_name }}"
      echo "SHA: ${{ github.sha }}"
      echo "Actor: ${{ github.actor }}"
      echo "Event: ${{ github.event_name }}"
      echo "Runner OS: ${{ runner.os }}"
      echo "Workspace: ${{ github.workspace }}"
```

- Contexts provide information about the workflow run

---

## Available Contexts

| Context    | Description                              | Example                        |
|------------|------------------------------------------|--------------------------------|
| `github`   | Workflow run information                 | `github.ref`, `github.sha`     |
| `env`      | Environment variables                   | `env.MY_VAR`                   |
| `vars`     | Repository/org variables                | `vars.APP_URL`                 |
| `job`      | Current job information                 | `job.status`                   |
| `steps`    | Step outputs and status                 | `steps.id.outputs.name`        |
| `runner`   | Runner machine information              | `runner.os`, `runner.arch`     |
| `secrets`  | Secrets available to the workflow       | `secrets.API_KEY`              |
| `inputs`   | Workflow dispatch inputs                | `inputs.environment`           |

---

## The `github` Context in Detail

```yaml
steps:
  - name: Useful github context values
    run: |
      echo "Repository: ${{ github.repository }}"
      echo "Owner: ${{ github.repository_owner }}"
      echo "Ref: ${{ github.ref }}"
      echo "Ref Name: ${{ github.ref_name }}"
      echo "SHA: ${{ github.sha }}"
      echo "Short SHA: ${GITHUB_SHA::7}"
      echo "Run ID: ${{ github.run_id }}"
      echo "Run Number: ${{ github.run_number }}"
      echo "Server URL: ${{ github.server_url }}"
```

---

## Artifact Upload and Download

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm run build
      - uses: actions/upload-artifact@v4
        with:
          name: dist-files
          path: dist/
          retention-days: 5

  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: dist-files
      - run: ls -la dist/
```

---

## Artifact Best Practices

- Set `retention-days` to avoid storage costs
- Use unique artifact names (especially in matrix builds)
- Compress large artifacts before uploading

```yaml
steps:
  - name: Compress artifacts
    run: tar -czf build.tar.gz dist/

  - uses: actions/upload-artifact@v4
    with:
      name: build-${{ github.sha }}
      path: build.tar.gz
      retention-days: 3
      if-no-files-found: error
```

---

## Cache Management with `actions/cache`

```yaml
steps:
  - uses: actions/cache@v4
    with:
      path: ~/.npm
      key: npm-${{ runner.os }}-${{ hashFiles('package-lock.json') }}
      restore-keys: |
        npm-${{ runner.os }}-
```

- Caches persist across workflow runs
- `key`: exact match for save and restore
- `restore-keys`: fallback keys for partial matches
- Cache size limit: 10 GB per repository

---

## Cache Examples for Popular Tools

```yaml
# Python pip
- uses: actions/cache@v4
  with:
    path: ~/.cache/pip
    key: pip-${{ runner.os }}-${{ hashFiles('requirements.txt') }}

# Maven
- uses: actions/cache@v4
  with:
    path: ~/.m2/repository
    key: maven-${{ runner.os }}-${{ hashFiles('pom.xml') }}

# Go modules
- uses: actions/cache@v4
  with:
    path: ~/go/pkg/mod
    key: go-${{ runner.os }}-${{ hashFiles('go.sum') }}
```
