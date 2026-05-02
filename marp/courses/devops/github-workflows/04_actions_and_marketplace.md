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
# Actions and Marketplace

---

## GitHub Actions Marketplace

![GitHub Actions Marketplace: action types, uses syntax, parameters, popular categories](svg/courses/devops/github-workflows/04_actions_and_marketplace/github_actions_marketplace.svg)

---

## What is the GitHub Marketplace?

- Central directory for sharing GitHub Actions
- Browse at: `https://github.com/marketplace?type=actions`
- Contains thousands of pre-built actions
- Categories include:
    - CI/CD
    - Code quality
    - Security
    - Deployment
    - Notifications

---

## Using Pre-Built Actions

```yaml
steps:
  # Use an action with 'uses' keyword
  - uses: actions/checkout@v4

  # Action with parameters
  - uses: actions/setup-node@v4
    with:
      node-version: "20"
      cache: "npm"

  # Action with a name for readability
  - name: Upload test results
    uses: actions/upload-artifact@v4
    with:
      name: test-results
      path: ./results/
```

---

## Essential Actions: `actions/checkout`

```yaml
steps:
  # Basic checkout
  - uses: actions/checkout@v4

  # Checkout with options
  - uses: actions/checkout@v4
    with:
      ref: develop
      fetch-depth: 0
      token: ${{ secrets.PAT_TOKEN }}
      submodules: recursive
```

- Required for almost every workflow
- `fetch-depth: 0` fetches full history (needed for changelogs)
- Default `fetch-depth: 1` is a shallow clone

---

## Essential Actions: `actions/setup-*`

```yaml
steps:
  # Node.js
  - uses: actions/setup-node@v4
    with:
      node-version: "20"

  # Python
  - uses: actions/setup-python@v5
    with:
      python-version: "3.12"

  # Java
  - uses: actions/setup-java@v4
    with:
      distribution: "temurin"
      java-version: "21"

  # Go
  - uses: actions/setup-go@v5
    with:
      go-version: "1.22"
```

---

## Essential Actions: Artifacts

```yaml
steps:
  # Upload artifacts
  - uses: actions/upload-artifact@v4
    with:
      name: build-output
      path: dist/
      retention-days: 7

  # Download artifacts (in another job)
  - uses: actions/download-artifact@v4
    with:
      name: build-output
      path: ./dist
```

- Share files between jobs
- Store build outputs, test reports, logs

---

## Action Versioning

```yaml
steps:
  # Major version tag (recommended)
  - uses: actions/checkout@v4

  # Exact version tag
  - uses: actions/checkout@v4.1.7

  # Commit SHA (most secure)
  - uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11

  # Branch reference (not recommended)
  - uses: actions/checkout@main
```

---

## Version Pinning

![version_pinning](svg/courses/devops/github-workflows/04_actions_and_marketplace/version_pinning.svg)

---

## Version Pinning Strategies

| Strategy        | Example              | Security | Updates     |
|-----------------|----------------------|----------|-------------|
| Major version   | `@v4`                | Medium   | Auto minor  |
| Exact tag       | `@v4.1.7`            | High     | Manual      |
| Commit SHA      | `@b4ffde6...`        | Highest  | Manual      |
| Branch          | `@main`              | Low      | Always      |

- **Production**: use SHA pinning with Dependabot for updates
- **Development**: major version tags are convenient
- Tools like `pin-github-action` can help

---

## Reading Action Documentation

```yaml
# Every action has an action.yml defining its interface
name: "Setup Node.js"
description: "Set up Node.js environment"
inputs:
  node-version:
    description: "Version of Node.js to use"
    required: false
  cache:
    description: "Package manager for caching"
    required: false
outputs:
  node-version:
    description: "Installed Node.js version"
```

- Check the action's `README.md` and `action.yml`
- Look at the **Inputs** and **Outputs** sections

---

## Community vs Official Actions

```misc
Official Actions:
  actions/checkout         - GitHub maintained
  actions/setup-node       - GitHub maintained
  actions/cache            - GitHub maintained
  github/codeql-action     - GitHub Security

Community Actions:
  docker/build-push-action - Docker Inc.
  aws-actions/configure-aws-credentials - AWS
  JamesIves/github-pages-deploy-action  - Individual

Verified creators show a blue checkmark in Marketplace
```

---

## Action Security Considerations

- **Supply chain attacks**: malicious code in third-party actions
- Best practices:
    - Pin actions to specific SHA hashes
    - Review action source code before using
    - Use `permissions` to limit `GITHUB_TOKEN` scope
    - Enable Dependabot for action updates
    - Prefer official and verified actions

```yaml
permissions:
  contents: read
  issues: write
```

---

## Using Actions from Different Sources

```yaml
steps:
  # Public action from GitHub Marketplace
  - uses: actions/checkout@v4

  # Action from a different repository
  - uses: owner/repo-name@v1

  # Action from a subdirectory
  - uses: owner/repo-name/path/to/action@v1

  # Local action from your repository
  - uses: ./.github/actions/my-action

  # Docker Hub image as an action
  - uses: docker://alpine:3.19
```

---

## Finding the Right Action

1. Check the **GitHub Marketplace** first
1. Look for actions with:
    - High number of stars
    - Active maintenance
    - Verified creator badge
    - Good documentation
1. Search with `gh` CLI:

```bash
# Search marketplace
gh search repos "actions setup-python" --sort stars

# Browse a specific action
gh browse actions/setup-python
```
