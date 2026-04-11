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
# Custom Actions Development

---

## Custom GitHub Action Types

![Custom GitHub Actions: JavaScript, Docker, Composite types and action.yml structure](svg/courses/devops/github-workflows/07_custom_actions_development/custom_action_types.svg)

---

## Types of Custom Actions

| Type        | Language      | Runs On          | Best For                   |
|-------------|--------------|------------------|----------------------------|
| JavaScript  | Node.js      | Runner directly  | Fast, cross-platform       |
| Docker      | Any language | Container        | Specific OS/tool needs     |
| Composite   | YAML         | Runner directly  | Combining existing actions |

```tree
Custom Action
  ├── action.yml        (required metadata)
  ├── index.js          (JavaScript action)
  ├── Dockerfile        (Docker action)
  └── README.md         (documentation)
```

---

## Action Metadata: `action.yml`

```yaml
name: "My Custom Action"
description: "A brief description of what this action does"
author: "Your Name"
branding:
  icon: "check-circle"
  color: "green"
inputs:
  name:
    description: "Name to greet"
    required: true
    default: "World"
outputs:
  greeting:
    description: "The greeting message"
runs:
  using: "node20"
  main: "index.js"
```

---

## Creating a JavaScript Action

```javascript
// index.js
const core = require("@actions/core");
const github = require("@actions/github");

async function run() {
    try {
        const name = core.getInput("name", { required: true });
        const greeting = `Hello, ${name}!`;

        core.info(`Greeting: ${greeting}`);
        core.setOutput("greeting", greeting);

        const context = github.context;
        core.info(`Repo: ${context.repo.owner}/${context.repo.repo}`);
    } catch (error) {
        core.setFailed(`Action failed: ${error.message}`);
    }
}

run();
```

---

## JavaScript Action Setup

```bash
# Initialize the project
mkdir my-action && cd my-action
npm init -y

# Install GitHub Actions toolkit
npm install @actions/core @actions/github

# Compile with ncc (bundle dependencies)
npm install -g @vercel/ncc
ncc build index.js -o dist
```

- Use `@vercel/ncc` to bundle into a single file
- Update `action.yml` to point to `dist/index.js`:

```yaml
runs:
  using: "node20"
  main: "dist/index.js"
```

---

## JavaScript Action Toolkit APIs

```javascript
const core = require("@actions/core");

// Inputs and outputs
const val = core.getInput("my-input");
core.setOutput("my-output", "value");

// Logging
core.debug("Debug message");
core.info("Info message");
core.warning("Warning message");
core.error("Error message");

// Fail the action
core.setFailed("Something went wrong");

// Export variable for subsequent steps
core.exportVariable("MY_VAR", "value");

// Mask a value in logs
core.setSecret("sensitive-value");
```

---

## Building a Docker Container Action

```dockerfile
# Dockerfile
FROM alpine:3.19

RUN apk add --no-cache bash curl jq

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
```

```bash
#!/bin/bash
# entrypoint.sh
NAME="${INPUT_NAME:-World}"
GREETING="Hello, ${NAME}!"
echo "greeting=${GREETING}" >> "$GITHUB_OUTPUT"
echo "${GREETING}"
```

---

## Docker Action `action.yml`

```yaml
name: "Docker Greeting Action"
description: "Greets someone using a Docker container"
inputs:
  name:
    description: "Name to greet"
    required: true
    default: "World"
outputs:
  greeting:
    description: "The greeting message"
runs:
  using: "docker"
  image: "Dockerfile"
  args:
    - ${{ inputs.name }}
  env:
    INPUT_NAME: ${{ inputs.name }}
```

---

## Docker vs JavaScript Actions

```misc
JavaScript Action:
  + Fast startup (no container build)
  + Cross-platform (Linux, Windows, macOS)
  + Access to GitHub toolkit
  - Limited to Node.js

Docker Action:
  + Any language or tool
  + Consistent environment
  + Complex dependencies
  - Linux runners only
  - Slower startup (build + pull)
```

---

## Input and Output Parameters

```yaml
# action.yml
inputs:
  version:
    description: "Version to deploy"
    required: true
  environment:
    description: "Target environment"
    required: false
    default: "staging"
  dry-run:
    description: "Simulate deployment"
    required: false
    default: "false"
outputs:
  deploy-url:
    description: "URL of the deployment"
  deploy-id:
    description: "Unique deployment identifier"
```

---

## Working with Outputs in Actions

```javascript
// JavaScript action - setting outputs
const core = require("@actions/core");

core.setOutput("deploy-url", "https://app.example.com");
core.setOutput("deploy-id", "dep-12345");
```

```bash
# Docker/shell action - setting outputs
echo "deploy-url=https://app.example.com" >> "$GITHUB_OUTPUT"
echo "deploy-id=dep-12345" >> "$GITHUB_OUTPUT"
```

```yaml
# Using outputs in a workflow
steps:
  - id: deploy
    uses: ./my-action
  - run: echo "${{ steps.deploy.outputs.deploy-url }}"
```

---

## Publishing Actions to GitHub Marketplace

1. Create a public repository for your action
1. Ensure `action.yml` has `name`, `description`, and `branding`
1. Create a release with a semantic version tag

```bash
git tag -a v1.0.0 -m "Initial release"
git push origin v1.0.0
```

1. On the release page, check "Publish this Action to GitHub Marketplace"
1. Maintain a major version tag:

```bash
git tag -fa v1 -m "Update v1 tag"
git push origin v1 --force
```

---

## Action Project Structure

```tree
my-custom-action/
  ├── action.yml          # Action metadata
  ├── src/
  │   └── index.js        # Source code
  ├── dist/
  │   └── index.js        # Bundled output (ncc)
  ├── tests/
  │   └── index.test.js   # Unit tests
  ├── package.json
  ├── README.md
  ├── LICENSE
  └── .github/
      └── workflows/
          └── test.yml    # CI for the action itself
```

- Test your action with a workflow in the same repo
- Bundle dependencies so users do not need `npm install`
