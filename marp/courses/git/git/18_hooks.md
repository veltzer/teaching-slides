---
tags:
  - tools:git
  - concepts:version-control
level: advanced
category: version-control
audience:
  - audiences:developers
  - audiences:sysadmins
  - audiences:devops

---
# Git Hooks

---

## What We'll Cover

1. How to set up Git hooks
1. What guarantees Git hooks provide
1. Client-side vs server-side hooks
1. Common hook use cases and examples
1. Hook development best practices
1. Troubleshooting and debugging hooks

---

## What Are Git Hooks?

Git hooks are scripts that run automatically at specific points in Git operations:

**Core concepts:**
- **Event-driven:** Triggered by Git operations
- **Customizable:** Write scripts in any language
- **Automatic:** Run without manual intervention
- **Enforceable:** Can prevent operations from completing

**Hook locations:**
- **Client-side:** Run on developer's machine
- **Server-side:** Run on Git server (GitHub, GitLab, etc.)
- **Local only:** Not transferred with clone/push

**Common use cases:**
- Code quality enforcement
- Automated testing
- Message formatting
- Deployment triggers
- Security checks

---
## Git Hook Types Overview: Overview

Two main categories of hooks:

---

## Git Hook Types Overview

![git_hook_types_overview](svg/courses/git/git/18_hooks/git_hook_types_overview.svg)

---

## How to Set Up Hooks

Hooks are executable scripts in the `.git/hooks` directory:

```bash
# Navigate to hooks directory
cd .git/hooks

# List sample hooks (disabled by default)
ls -la
# pre-commit.sample
# commit-msg.sample
# post-update.sample
# etc.

# Create a new hook
touch pre-commit
chmod +x pre-commit

# Edit the hook
vim pre-commit
```

**Basic hook structure:**

```bash
#!/bin/sh
# pre-commit hook example

echo "Running pre-commit hook..."

# Your custom logic here
if [ some_condition ]; then
    echo "Pre-commit check failed!"
    exit 1  # Prevent commit
fi

echo "Pre-commit check passed!"
exit 0      # Allow commit to proceed
```

---

## What Guarantees Do You Get?

Understanding hook reliability and limitations:

**What hooks guarantee:**
- Execute at specific Git operation points
- Can prevent operations from completing (pre-hooks)
- Receive relevant information as parameters
- Run with repository context

**What hooks DON'T guarantee:**
- **Not shared:** Hooks are local, not cloned/pushed
- **Can be bypassed:** `git commit --no-verify`
- **No execution order:** Multiple hooks run in filename order
- **Environment dependent:** May behave differently across systems

**Security implications:**

```bash
# Hooks can be bypassed
git commit --no-verify -m "Skip all hooks"
git push --no-verify

# Server-side hooks are more reliable for enforcement
# Client-side hooks are developer convenience tools
```

---

## Client-Side Hooks: Pre-Commit

Run before commit is created:

```bash
#!/bin/sh
# .git/hooks/pre-commit

echo "Running pre-commit checks..."

# Check for debugging statements
if grep -r "console.log\|debugger" src/; then
    echo "Error: Debug statements found in code"
    echo "Remove debugging code before committing"
    exit 1
fi

# Run linting
if command -v eslint >/dev/null 2>&1; then
    echo "Running ESLint..."
    eslint src/ || exit 1
fi

# Run tests
if [ -f "package.json" ]; then
    echo "Running tests..."
    npm test || exit 1
fi

echo "Pre-commit checks passed!"
```

**Pre-commit use cases:**
- Code linting and formatting
- Running unit tests
- Security scans
- Documentation checks
- File permission validation

---

## Client-Side Hooks: Commit Message

Validate and format commit messages:

```bash
#!/bin/sh
# .git/hooks/commit-msg

commit_msg_file=$1
commit_msg=$(cat "$commit_msg_file")

# Check minimum message length
if [ ${#commit_msg} -lt 10 ]; then
    echo "Error: Commit message too short (minimum 10 characters)"
    echo "Current message: '$commit_msg'"
    exit 1
fi

# Check for ticket number
if ! echo "$commit_msg" | grep -q "JIRA-[0-9]\+"; then
    echo "Error: Commit message must include ticket number (JIRA-XXX)"
    exit 1
fi

# Check commit message format
if ! echo "$commit_msg" | grep -q "^(feat|fix|docs|style|refactor|test|chore):"; then
    echo "Error: Commit message must start with type: (feat|fix|docs|style|refactor|test|chore)"
    echo "Example: 'feat: add user authentication'"
    exit 1
fi

echo "Commit message format is valid"
```

---

## Client-Side Hooks: Prepare Commit Message

Automatically modify commit messages:

```bash
#!/bin/sh
# .git/hooks/prepare-commit-msg

commit_msg_file=$1
commit_source=$2
sha1=$3

# Get current branch name
branch_name=$(git symbolic-ref --short HEAD 2>/dev/null)

# Add branch name to commit message if not already present
if [ -n "$branch_name" ] && [ "$branch_name" != "main" ] && [ "$branch_name" != "master" ]; then
    if ! grep -q "\[$branch_name\]" "$commit_msg_file"; then
        # Prepend branch name to commit message
        original_msg=$(cat "$commit_msg_file")
        echo "[$branch_name] $original_msg" > "$commit_msg_file"
    fi
fi

# Add ticket number from branch name
if echo "$branch_name" | grep -q "JIRA-[0-9]\+"; then
    ticket=$(echo "$branch_name" | grep -o "JIRA-[0-9]\+")
    if ! grep -q "$ticket" "$commit_msg_file"; then
        echo "" >> "$commit_msg_file"
        echo "Refs: $ticket" >> "$commit_msg_file"
    fi
fi
```

---

## Client-Side Hooks: Post-Commit

Run after successful commit:

```bash
#!/bin/sh
# .git/hooks/post-commit

echo "Commit successful: $(git log -1 --format='%h %s')"

# Send notification
if command -v notify-send >/dev/null 2>&1; then
    notify-send "Git Commit" "Successfully committed: $(git log -1 --format='%s')"
fi

# Update documentation
if git diff --name-only HEAD^ HEAD | grep -q "src/"; then
    echo "Source code changed, consider updating documentation"
fi

# Trigger CI build (example)
if [ -f ".ci-trigger" ]; then
    echo "Triggering CI build..."
    curl -X POST "https://ci.example.com/trigger" \
         -d "commit=$(git rev-parse HEAD)" \
         -d "branch=$(git branch --show-current)"
fi

# Log commit for analytics
echo "$(date): $(git log -1 --format='%H %an %s')" >> .git/commit-log
```

---

## Client-Side Hooks: Pre-Push

Run before pushing to remote:

```bash
#!/bin/sh
# .git/hooks/pre-push

remote_name=$1
remote_url=$2

echo "Preparing to push to $remote_name ($remote_url)"

# Check if on protected branch
current_branch=$(git branch --show-current)
if [ "$current_branch" = "main" ] || [ "$current_branch" = "master" ]; then
    echo "Warning: Pushing to protected branch $current_branch"
    echo "Continue? (y/N)"
    read -r response
    if [ "$response" != "y" ] && [ "$response" != "Y" ]; then
        echo "Push cancelled"
        exit 1
    fi
fi

# Run final tests before push
if [ -f "package.json" ]; then
    echo "Running full test suite before push..."
    npm run test:full || {
        echo "Tests failed! Push cancelled."
        exit 1
    }
fi

# Check for sensitive data
if git log --oneline @{u}.. | xargs git show | grep -E "(password|secret|api_key)" >/dev/null; then
    echo "Warning: Potential sensitive data found in commits to be pushed"
    echo "Review commits before pushing"
    exit 1
fi

echo "Pre-push checks completed successfully"
```

---

## Server-Side Hooks: Pre-Receive

Control what gets pushed to server:

```bash
#!/bin/sh
# hooks/pre-receive (on server)

echo "Processing incoming push..."

while read oldrev newrev refname; do
    echo "Checking $refname: $oldrev -> $newrev"

    # Get branch name
    branch_name=$(echo "$refname" | sed 's/refs\/heads\///')

    # Protect main branch
    if [ "$branch_name" = "main" ]; then
        # Ensure only fast-forward merges
        if [ "$oldrev" != "0000000000000000000000000000000000000000" ]; then
            if ! git merge-base --is-ancestor "$oldrev" "$newrev"; then
                echo "Error: Non-fast-forward push to main branch rejected"
                echo "Please rebase your changes and try again"
                exit 1
            fi
        fi
    fi

    # Check commit message format
    for commit in $(git rev-list "$oldrev".."$newrev"); do
        msg=$(git log -1 --format='%s' "$commit")
        if ! echo "$msg" | grep -q "^(feat|fix|docs|style|refactor|test|chore):"; then
            echo "Error: Invalid commit message format in $commit"
            echo "Message: $msg"
            exit 1
        fi
    done

    echo "Branch $branch_name accepted"
done

echo "All pushed refs are valid"
```

---

## Server-Side Hooks: Post-Receive

Trigger actions after successful push:

```bash
#!/bin/sh
# hooks/post-receive (on server)

echo "Push received successfully"

while read oldrev newrev refname; do
    branch_name=$(echo "$refname" | sed 's/refs\/heads\///')

    echo "Processing updates for $branch_name"

    # Deploy main branch
    if [ "$branch_name" = "main" ]; then
        echo "Triggering deployment for main branch..."

        # Update working directory (for bare repositories)
        cd /var/www/production
        git --git-dir=/var/git/project.git --work-tree=/var/www/production checkout -f

        # Run deployment script
        ./deploy.sh production

        # Send notification
        curl -X POST "https://slack.com/webhook" \
             -d "{\"text\":\"Deployed main branch to production\"}"
    fi

    # Update documentation
    if [ "$branch_name" = "docs" ]; then
        echo "Rebuilding documentation..."
        cd /var/www/docs
        git --git-dir=/var/git/project.git --work-tree=/var/www/docs checkout -f docs
        make html
    fi

    # Log the push
    echo "$(date): Push to $branch_name by $USER" >> /var/log/git-pushes.log
done
```

---

## Hook Development Best Practices

Guidelines for creating reliable hooks:

**Script reliability:**

```bash
#!/bin/sh
# Always use proper shebang
set -e  # Exit on first error
set -u  # Exit on undefined variables

# Check dependencies
if ! command -v required_tool >/dev/null 2>&1; then
    echo "Error: required_tool not found"
    exit 1
fi

# Provide helpful error messages
check_condition() {
    if [ ! some_condition ]; then
        echo "Error: Condition not met"
        echo "To fix: run 'command_to_fix'"
        return 1
    fi
}
```

**Performance considerations:**

```bash
# Cache expensive operations
if [ ! -f ".hook-cache/lint-result" ] || [ "src/" -nt ".hook-cache/lint-result" ]; then
    run_linter
    touch ".hook-cache/lint-result"
fi

# Run checks in parallel when possible
run_tests &
TEST_PID=$!
run_linter &
LINT_PID=$!

wait $TEST_PID || exit 1
wait $LINT_PID || exit 1
```

---

## Hook Sharing and Distribution

Share hooks across team:

**Template approach:**

```bash
# Create hooks template directory
mkdir .githooks
cp .git/hooks/pre-commit .githooks/

# Configure Git to use template
git config core.hooksPath .githooks

# Make executable
chmod +x .githooks/pre-commit

# Add to version control
git add .githooks/pre-commit
git commit -m "Add shared pre-commit hook"
```

**Installation script:**

```bash
#!/bin/sh
# install-hooks.sh

HOOKS_DIR=".githooks"
GIT_HOOKS_DIR=".git/hooks"

if [ ! -d "$HOOKS_DIR" ]; then
    echo "Error: $HOOKS_DIR directory not found"
    exit 1
fi

echo "Installing Git hooks..."
for hook in "$HOOKS_DIR"/*; do
    hook_name=$(basename "$hook")
    echo "Installing $hook_name..."
    cp "$hook" "$GIT_HOOKS_DIR/$hook_name"
    chmod +x "$GIT_HOOKS_DIR/$hook_name"
done

echo "Hooks installed successfully"
```

---

## Advanced Hook Techniques

Sophisticated hook implementations:

**Conditional execution:**

```bash
#!/bin/sh
# Conditional pre-commit based on branch

branch=$(git symbolic-ref --short HEAD)

case "$branch" in
    "main"|"master")
        echo "Running strict checks for main branch"
        run_full_test_suite
        run_security_scan
        ;;
    "develop")
        echo "Running standard checks for develop branch"
        run_unit_tests
        run_linter
        ;;
    "feature/"*)
        echo "Running basic checks for feature branch"
        run_linter
        ;;
    *)
        echo "No specific checks for branch $branch"
        ;;
esac
```

**Multi-language support:**

```bash
#!/bin/sh
# Language-specific checks

check_python_files() {
    if ls *.py >/dev/null 2>&1; then
        echo "Checking Python files..."
        python -m flake8 . || return 1
        python -m pytest tests/ || return 1
    fi
}

check_javascript_files() {
    if [ -f "package.json" ]; then
        echo "Checking JavaScript files..."
        npm run lint || return 1
        npm test || return 1
    fi
}

check_python_files
check_javascript_files
```

---

## Hook Integration with CI/CD

Connect hooks with continuous integration:

**GitHub Actions integration:**

```bash
#!/bin/sh
# pre-push hook that mirrors CI checks

echo "Running local CI checks..."

# Run the same checks as GitHub Actions
if [ -f ".github/workflows/ci.yml" ]; then
    echo "Simulating CI pipeline locally..."

    # Extract and run test commands
    grep -A 10 "run:" .github/workflows/ci.yml | \
    grep -E "^\s+run:" | \
    sed 's/^.*run: //' | \
    while read -r cmd; do
        echo "Running: $cmd"
        eval "$cmd" || exit 1
    done
fi
```

**Jenkins integration:**

```bash
#!/bin/sh
# post-commit hook that triggers Jenkins build

JENKINS_URL="https://jenkins.company.com"
JOB_NAME="project-ci"
TOKEN="your-jenkins-token"

curl -X POST "$JENKINS_URL/job/$JOB_NAME/buildWithParameters" \
     --user "user:$TOKEN" \
     --data "BRANCH=$(git branch --show-current)" \
     --data "COMMIT=$(git rev-parse HEAD)"
```

---

## Troubleshooting Git Hooks

Common issues and solutions:

**Hook not executing:**

```bash
# Check if hook is executable
ls -la .git/hooks/pre-commit

# Make executable if needed
chmod +x .git/hooks/pre-commit

# Check shebang line
head -1 .git/hooks/pre-commit
```

**Permission issues:**

```bash
# Fix ownership
chown $USER:$USER .git/hooks/*

# Set proper permissions
chmod 755 .git/hooks/*
```

**Environment problems:**

```bash
#!/bin/sh
# Debug hook environment

echo "Current working directory: $(pwd)"
echo "Current user: $(whoami)"
echo "PATH: $PATH"
echo "Git version: $(git --version)"

# Set explicit PATH if needed
export PATH="/usr/local/bin:/usr/bin:/bin:$PATH"
```

**Hook debugging:**

```bash
#!/bin/sh
# Add debugging to hooks

DEBUG_LOG=".git/hook-debug.log"

debug_log() {
    echo "$(date): $1" >> "$DEBUG_LOG"
}

debug_log "Hook started with args: $*"
debug_log "Current branch: $(git branch --show-current)"
debug_log "Working directory: $(pwd)"

# Your hook logic here

debug_log "Hook completed successfully"
```

---

## Hook Security Considerations

Security aspects of Git hooks:

**Input validation:**

```bash
#!/bin/sh
# Validate hook inputs

validate_input() {
    local input="$1"

    # Check for command injection attempts
    if echo "$input" | grep -q "[;&|]"; then
        echo "Error: Invalid characters in input"
        exit 1
    fi

    # Limit input length
    if [ ${#input} -gt 100 ]; then
        echo "Error: Input too long"
        exit 1
    fi
}

# Validate all inputs
for arg in "$@"; do
    validate_input "$arg"
done
```

**Secure execution:**

```bash
#!/bin/sh
# Secure hook execution

# Use full paths for commands
GREP="/bin/grep"
SED="/bin/sed"
GIT="/usr/bin/git"

# Sanitize environment
unset IFS
export PATH="/usr/local/bin:/usr/bin:/bin"

# Use safe temporary files
TEMP_DIR=$(mktemp -d)
trap "rm -rf '$TEMP_DIR'" EXIT
```

---

## Performance Optimization

Make hooks faster:

**Caching strategies:**

```bash
#!/bin/sh
# Cache-enabled pre-commit hook

CACHE_DIR=".git/hook-cache"
mkdir -p "$CACHE_DIR"

# Check if files changed since last run
if [ -f "$CACHE_DIR/last-run" ]; then
    last_run=$(cat "$CACHE_DIR/last-run")
    if [ "$last_run" = "$(git rev-parse HEAD)" ]; then
        echo "No changes since last successful run"
        exit 0
    fi
fi

# Run checks
run_expensive_checks || exit 1

# Cache successful run
git rev-parse HEAD > "$CACHE_DIR/last-run"
```

**Parallel execution:**

```bash
#!/bin/sh
# Parallel hook execution

run_linter &
LINT_PID=$!

run_tests &
TEST_PID=$!

run_security_scan &
SECURITY_PID=$!

# Wait for all processes
wait $LINT_PID
LINT_EXIT=$?

wait $TEST_PID
TEST_EXIT=$?

wait $SECURITY_PID
SECURITY_EXIT=$?

# Check all exit codes
if [ $LINT_EXIT -ne 0 ] || [ $TEST_EXIT -ne 0 ] || [ $SECURITY_EXIT -ne 0 ]; then
    echo "One or more checks failed"
    exit 1
fi
```

---

## Lab Exercise: Comprehensive Hook System

**Scenario:** Implement a complete Git hook system for a development team with quality gates, automation, and security checks.

**Setup tasks:**
1. **Client-side hook development:**
   - Create pre-commit hooks for code quality
   - Implement commit message validation
   - Set up pre-push security checks

1. **Server-side hook implementation:**
   - Configure pre-receive branch protection
   - Set up post-receive deployment triggers
   - Implement automated notifications

1. **Hook sharing and distribution:**
   - Create shared hook templates
   - Develop installation and update scripts
   - Document hook requirements

**Advanced tasks:**
1. **Integration development:**
   - Connect hooks with CI/CD systems
   - Implement performance optimizations
   - Create debugging and monitoring tools

1. **Security and reliability:**
   - Add input validation and security checks
   - Implement error handling and recovery
   - Create backup and rollback procedures

**Deliverables:** Complete hook system with documentation, installation scripts, security guidelines, performance benchmarks, and team training materials.

---

## Summary: Mastering Git Hooks

**Key takeaways:**

1. **Understand hook limitations:**
   - Client-side hooks can be bypassed
   - Server-side hooks provide better enforcement
   - Hooks are not shared via Git operations
   - Environment dependencies can cause issues

1. **Design for reliability:**
   - Use proper error handling
   - Validate inputs and environment
   - Provide clear error messages
   - Test hooks thoroughly

1. **Focus on team adoption:**
   - Make hooks easy to install and update
   - Provide clear documentation
   - Balance strictness with usability
   - Consider performance impact

1. **Security and best practices:**
   - Validate all inputs
   - Use secure coding practices
   - Regular security audits
   - Monitor hook performance

**Remember:** Git hooks are powerful automation tools that can significantly improve code quality, security, and development workflows. However, they require careful design, testing, and maintenance. Start simple, iterate based on team feedback, and always consider the balance between automation benefits and development friction.
