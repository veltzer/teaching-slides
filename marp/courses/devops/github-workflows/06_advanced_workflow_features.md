# Advanced Workflow Features

---

## Matrix Builds Overview

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [18, 20, 22]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
      - run: npm ci
      - run: npm test
```

- Automatically creates multiple job instances
- Each combination runs in parallel

---

## Multi-Dimensional Matrix

```yaml
jobs:
  test:
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        python: ["3.10", "3.11", "3.12"]
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python }}
      - run: python -m pytest
```

- This creates 3 x 3 = **9 parallel jobs**

---

## Matrix Include and Exclude

```yaml
strategy:
  matrix:
    os: [ubuntu-latest, windows-latest]
    node: [18, 20]
    exclude:
      - os: windows-latest
        node: 18
    include:
      - os: ubuntu-latest
        node: 22
        experimental: true
```

- `exclude`: remove specific combinations
- `include`: add extra combinations or properties
- `experimental` becomes `${{ matrix.experimental }}`

---

## Matrix with `fail-fast`

```yaml
strategy:
  fail-fast: false
  max-parallel: 3
  matrix:
    version: [14, 16, 18, 20]
```

- `fail-fast: true` (default) cancels all jobs if one fails
- `fail-fast: false` lets all jobs complete
- `max-parallel` limits concurrent jobs

---

## Conditional Jobs and Steps

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm test

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    steps:
      - name: Deploy to production
        run: ./deploy.sh

      - name: Notify on failure
        if: failure()
        run: echo "Deployment failed!"
```

---

## Status Check Functions

```yaml
steps:
  - name: Always run cleanup
    if: always()
    run: ./cleanup.sh

  - name: Run only on success
    if: success()
    run: echo "All good!"

  - name: Run only on failure
    if: failure()
    run: echo "Something went wrong"

  - name: Run if cancelled
    if: cancelled()
    run: echo "Workflow was cancelled"
```

- `success()` is the **implicit default** for steps

---

## Job Outputs

```yaml
jobs:
  version:
    runs-on: ubuntu-latest
    outputs:
      app_version: ${{ steps.get_ver.outputs.version }}
    steps:
      - id: get_ver
        run: echo "version=1.2.3" >> "$GITHUB_OUTPUT"

  deploy:
    needs: version
    runs-on: ubuntu-latest
    steps:
      - run: echo "Deploying v${{ needs.version.outputs.app_version }}"
```

- Use `$GITHUB_OUTPUT` to set step outputs
- Map step outputs to job outputs
- Reference via `needs.<job>.outputs.<name>`

---

## Passing Data Between Jobs

<svg xmlns="http://www.w3.org/2000/svg" width="430" height="260" font-family="sans-serif">
<defs>
  <marker id="arrow" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
    <polygon points="0 0, 10 3.5, 0 7" fill="#555"/>
  </marker>
</defs>
<rect x="20" y="20" width="150" height="100" fill="#e3f2fd" stroke="#333" stroke-width="1.5" rx="4"/>
<text x="95" y="40" font-size="13" font-weight="bold" fill="#222" text-anchor="middle">Job A</text>
<text x="95" y="58" font-size="11" font-weight="normal" fill="#222" text-anchor="middle">steps:</text>
<text x="95" y="74" font-size="11" font-weight="normal" fill="#222" text-anchor="middle">- set output</text>
<line x1="170" y1="70" x2="248" y2="70" stroke="#555" stroke-width="1.5" marker-end="url(#arrow)"/>
<text x="209" y="60" font-size="10" font-weight="normal" fill="#555" text-anchor="middle">outputs</text>
<rect x="250" y="20" width="150" height="100" fill="#e8f5e9" stroke="#333" stroke-width="1.5" rx="4"/>
<text x="325" y="40" font-size="13" font-weight="bold" fill="#222" text-anchor="middle">Job B</text>
<text x="325" y="58" font-size="11" font-weight="normal" fill="#222" text-anchor="middle">needs: a</text>
<text x="325" y="74" font-size="11" font-weight="normal" fill="#222" text-anchor="middle">steps:</text>
<text x="325" y="90" font-size="11" font-weight="normal" fill="#222" text-anchor="middle">- use output</text>
<line x1="10" y1="140" x2="420" y2="140" stroke="#ccc" stroke-width="1" stroke-dasharray="4,3"/>
<text x="215" y="160" font-size="11" font-weight="normal" fill="#666" text-anchor="middle">Alternative: Use artifacts for large data</text>
<rect x="20" y="175" width="150" height="70" fill="#fff3e0" stroke="#333" stroke-width="1.5" rx="4"/>
<text x="95" y="198" font-size="13" font-weight="bold" fill="#222" text-anchor="middle">Job A</text>
<text x="95" y="215" font-size="11" font-weight="normal" fill="#222" text-anchor="middle">upload artifact</text>
<line x1="170" y1="210" x2="248" y2="210" stroke="#555" stroke-width="1.5" marker-end="url(#arrow)"/>
<text x="209" y="200" font-size="10" font-weight="normal" fill="#555" text-anchor="middle">artifact</text>
<text x="209" y="215" font-size="10" font-weight="normal" fill="#555" text-anchor="middle">(files)</text>
<rect x="250" y="175" width="150" height="70" fill="#fce4ec" stroke="#333" stroke-width="1.5" rx="4"/>
<text x="325" y="198" font-size="13" font-weight="bold" fill="#222" text-anchor="middle">Job B</text>
<text x="325" y="215" font-size="11" font-weight="normal" fill="#222" text-anchor="middle">download artifact</text>
</svg>

---

## Reusable Workflows

```yaml
# .github/workflows/reusable-test.yml
name: Reusable Test Workflow
on:
  workflow_call:
    inputs:
      node-version:
        required: true
        type: string
    secrets:
      npm-token:
        required: false
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ inputs.node-version }}
      - run: npm test
```

---

## Calling Reusable Workflows

```yaml
# .github/workflows/ci.yml
name: CI
on: push
jobs:
  run-tests:
    uses: ./.github/workflows/reusable-test.yml
    with:
      node-version: "20"
    secrets:
      npm-token: ${{ secrets.NPM_TOKEN }}

  run-tests-cross-repo:
    uses: owner/repo/.github/workflows/test.yml@main
    with:
      node-version: "20"
```

- Call with `uses` at the **job level**
- Can reference local or cross-repository workflows

---

## Composite Actions

```yaml
# .github/actions/setup-and-test/action.yml
name: "Setup and Test"
description: "Install dependencies and run tests"
inputs:
  node-version:
    description: "Node.js version"
    default: "20"
runs:
  using: "composite"
  steps:
    - uses: actions/setup-node@v4
      with:
        node-version: ${{ inputs.node-version }}
    - run: npm ci
      shell: bash
    - run: npm test
      shell: bash
```

---

## Using Composite Actions

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: ./.github/actions/setup-and-test
        with:
          node-version: "20"
```

- Composite actions bundle multiple steps
- Must specify `shell` for each `run` step
- Stored as directories with `action.yml`

---

## Service Containers

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_PASSWORD: testpass
          POSTGRES_DB: testdb
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    steps:
      - uses: actions/checkout@v4
      - run: npm test
        env:
          DATABASE_URL: postgres://postgres:testpass@localhost:5432/testdb
```

---

## Service Containers: Redis Example

```yaml
services:
  redis:
    image: redis:7
    ports:
      - 6379:6379
    options: >-
      --health-cmd "redis-cli ping"
      --health-interval 10s
      --health-timeout 5s
      --health-retries 5
```

- Services run as Docker containers alongside your job
- Use `ports` to map container ports to the runner
- Health checks ensure services are ready before steps run

---

## Self-Hosted Runners

```yaml
jobs:
  build:
    runs-on: self-hosted
    steps:
      - uses: actions/checkout@v4
      - run: ./build.sh
```

- Install on your own machines for:
    - Custom hardware requirements
    - Access to internal networks
    - Cost savings for high-volume usage
    - Persistent tool installations
- Setup: Settings -> Actions -> Runners -> New self-hosted runner
- Use custom labels: `runs-on: [self-hosted, linux, gpu]`
