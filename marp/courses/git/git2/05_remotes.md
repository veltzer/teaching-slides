# Remote Repositories

---

## What We'll Cover

1. Understanding remote repositories
1. Setting up remotes
1. Cloning vs initializing
1. Fetching and pulling
1. Pushing changes
1. Working with multiple remotes
1. Repository hosting platforms
1. Collaboration workflows

---

## What is a Remote Repository?

![what_is_a_remote_repository](/svg/courses/git/git2/05_remotes/what_is_a_remote_repository.svg)

---

## Remote Repository Locations

![remote_repository_locations](/svg/courses/git/git2/05_remotes/remote_repository_locations.svg)

---

## Setting Up Your First Remote

```bash
# Method 1: Clone existing repository
git clone https://github.com/user/repo.git
# Automatically sets up 'origin' remote

# Method 2: Add remote to existing local repo
git init
git remote add origin https://github.com/user/repo.git

# View remotes
git remote -v
# origin  https://github.com/user/repo.git (fetch)
# origin  https://github.com/user/repo.git (push)

# Show remote details
git remote show origin
```

---

## Clone vs Init + Remote

![clone_vs_init_remote](/svg/courses/git/git2/05_remotes/clone_vs_init_remote.svg)

---

## Understanding Remote Names

```bash
# Default remote name is 'origin'
git clone https://github.com/user/repo.git
# Creates remote named 'origin'

# Custom remote name
git clone -o upstream https://github.com/original/repo.git
# Creates remote named 'upstream'

# Multiple remotes
git remote add origin https://github.com/me/repo.git
git remote add upstream https://github.com/original/repo.git
git remote add backup https://gitlab.com/me/repo.git

# Rename remote
git remote rename origin github

# Remove remote
git remote remove backup
```

---

## Remote Branches

![remote_branches](/svg/courses/git/git2/05_remotes/remote_branches.svg)

---

## Fetching Changes

```bash
# Fetch from default remote (origin)
git fetch

# Fetch from specific remote
git fetch upstream

# Fetch specific branch
git fetch origin main

# Fetch all remotes
git fetch --all

# Fetch and prune deleted branches
git fetch --prune

# See what fetch will do (dry run)
git fetch --dry-run
```

---

## Fetch vs Pull

![fetch_vs_pull](/svg/courses/git/git2/05_remotes/fetch_vs_pull.svg)

---

## Pull Strategies

```bash
# Default pull (merge)
git pull

# Pull with rebase
git pull --rebase

# Pull with fast-forward only
git pull --ff-only

# Configure default pull strategy
git config pull.rebase true    # Always rebase
git config pull.ff only        # Only fast-forward

# Pull from specific remote and branch
git pull upstream main

# Verbose output
git pull --verbose
```

---

## Pushing Changes

```bash
# Push current branch to origin
git push

# Push specific branch
git push origin main

# Push all branches
git push --all

# Push with tags
git push --follow-tags

# Push specific tag
git push origin v1.0.0

# Force push (DANGEROUS!)
git push --force

# Safer force push
git push --force-with-lease

# Set upstream branch
git push -u origin feature
```

---

## Push Scenarios

![push_scenarios](/svg/courses/git/git2/05_remotes/push_scenarios.svg)

---

## Tracking Branches

```bash
# Set upstream branch while pushing
git push -u origin feature
# Now 'git push' and 'git pull' work without arguments

# Set upstream for existing branch
git branch --set-upstream-to=origin/feature

# Create local branch tracking remote
git checkout -b feature origin/feature
# or
git checkout --track origin/feature

# See tracking relationships
git branch -vv
# * main     a3d8f2c [origin/main] Latest commit
#   feature  b7c9e1a [origin/feature: ahead 2] Local changes

# Remove tracking
git branch --unset-upstream
```

---

## Working with Multiple Remotes

![working_with_multiple_remotes](/svg/courses/git/git2/05_remotes/working_with_multiple_remotes.svg)

---

## Fork Workflow Example

```bash
# 1. Fork on GitHub (via web interface)

# 2. Clone your fork
git clone https://github.com/YOU/project.git

# 3. Add upstream remote
git remote add upstream https://github.com/ORIGINAL/project.git

# 4. Keep fork updated
git fetch upstream
git checkout main
git merge upstream/main
git push origin main

# 5. Create feature branch
git checkout -b feature

# 6. Push to your fork
git push origin feature

# 7. Create Pull Request (via web interface)
```

---

## Remote URLs: HTTPS vs SSH

![remote_urls_https_vs_ssh](/svg/courses/git/git2/05_remotes/remote_urls_https_vs_ssh.svg)

---

## Changing Remote URLs

```bash
# View current URL
git remote get-url origin

# Change from HTTPS to SSH
git remote set-url origin git@github.com:user/repo.git

# Change from SSH to HTTPS
git remote set-url origin https://github.com/user/repo.git

# Add push URL different from fetch
git remote set-url --push origin git@github.com:user/repo.git

# Verify change
git remote -v
# origin  https://github.com/user/repo.git (fetch)
# origin  git@github.com:user/repo.git (push)
```

---

## Understanding Publishing

![understanding_publishing](/svg/courses/git/git2/05_remotes/understanding_publishing.svg)

---

## Remote Repository Structure

![remote_repository_structure](/svg/courses/git/git2/05_remotes/remote_repository_structure.svg)

---

## Creating a Bare Repository

```bash
# Create bare repository for sharing
git init --bare myproject.git

# Structure of bare repo
ls myproject.git/
# HEAD  config  description  hooks/  info/  objects/  refs/

# Convert existing repo to bare
git clone --bare existing-repo bare-repo.git

# Push to bare repository
cd my-project
git remote add origin /path/to/bare-repo.git
git push origin main

# Serve bare repo over SSH
# Users can clone via:
git clone user@server:/path/to/bare-repo.git
```

---

## GitHub: The Platform

![github_the_platform](/svg/courses/git/git2/05_remotes/github_the_platform.svg)

---

## GitLab: The Alternative

![gitlab_the_alternative](/svg/courses/git/git2/05_remotes/gitlab_the_alternative.svg)

---

## Bitbucket: Enterprise Focus

```bash
# Bitbucket URLs
# HTTPS
https://bitbucket.org/workspace/repo.git
# SSH
git@bitbucket.org:workspace/repo.git

# Bitbucket-specific features
# - Jira integration
# - Confluence integration
# - Built-in CI/CD (Pipelines)
# - Mercurial support (deprecated)

# Clone from Bitbucket
git clone git@bitbucket.org:team/project.git

# Add Bitbucket remote
git remote add bitbucket git@bitbucket.org:team/project.git
```

---

## Collaboration Workflows

![collaboration_workflows](/svg/courses/git/git2/05_remotes/collaboration_workflows.svg)

---

## Pull Requests / Merge Requests

![pull_requests_merge_requests](/svg/courses/git/git2/05_remotes/pull_requests_merge_requests.svg)

---

## Creating a Pull Request

```bash
# 1. Create feature branch
git checkout -b feature/add-login

# 2. Make changes and commit
git add .
git commit -m "Add login functionality"

# 3. Push to your fork/origin
git push origin feature/add-login

# 4. GitHub CLI (optional)
gh pr create --title "Add login" --body "Description"

# Or use web interface:
# - Go to GitHub/GitLab
# - Click "New Pull Request"
# - Select base and compare branches
# - Add title and description
# - Request reviewers
# - Submit
```

---

## Code Review Process

![code_review_process](/svg/courses/git/git2/05_remotes/code_review_process.svg)

---

## Pull Request Best Practices

```bash
# Keep PRs small and focused
# ✓ One feature per PR
# ✓ Easy to review
# ✗ Multiple unrelated changes

# Write descriptive PR descriptions
# - What changed
# - Why it changed
# - How to test
# - Screenshots if UI changes

# Keep commits clean
git rebase -i main  # Before creating PR

# Update branch before merge
git fetch origin
git rebase origin/main
git push --force-lease

# Use draft PRs for work in progress
# Mark as "Draft" in GitHub/GitLab
```

---

## Handling Merge Conflicts

![handling_merge_conflicts](/svg/courses/git/git2/05_remotes/handling_merge_conflicts.svg)

---

## Sync Fork with Upstream

```bash
# Add upstream remote (one time)
git remote add upstream https://github.com/ORIGINAL/repo.git

# Sync fork with upstream
git fetch upstream
git checkout main
git merge upstream/main
git push origin main

# Alternative: rebase method
git fetch upstream
git checkout main
git rebase upstream/main
git push origin main --force-lease

# Sync all branches
git fetch upstream
git checkout main
git reset --hard upstream/main
git push origin main --force-lease
```

---

## Protected Branches

![protected_branches](/svg/courses/git/git2/05_remotes/protected_branches.svg)

---

## Tags and Releases

```bash
# Create lightweight tag
git tag v1.0.0

# Create annotated tag (recommended)
git tag -a v1.0.0 -m "Version 1.0.0 release"

# Tag specific commit
git tag -a v1.0.0 abc123 -m "Version 1.0.0"

# List tags
git tag
git tag -l "v1.*"  # Pattern matching

# Show tag details
git show v1.0.0

# Push tags to remote
git push origin v1.0.0      # Specific tag
git push origin --tags      # All tags
git push --follow-tags      # Annotated tags only

# Delete tag
git tag -d v1.0.0           # Local
git push origin :v1.0.0     # Remote
```

---

## Semantic Versioning

![semantic_versioning](/svg/courses/git/git2/05_remotes/semantic_versioning.svg)

---

## GitHub/GitLab Releases

```bash
# Create release with GitHub CLI
gh release create v1.0.0 \
  --title "Version 1.0.0" \
  --notes "Release notes" \
  --target main

# Upload assets to release
gh release upload v1.0.0 dist/*

# Create draft release
gh release create v2.0.0 --draft

# Auto-generate release notes
gh release create v1.0.0 --generate-notes

# GitLab releases (via API or UI)
# Usually done through CI/CD pipeline
```

---

## Remote Housekeeping

```bash
# Remove stale remote-tracking branches
git remote prune origin

# Fetch and prune in one command
git fetch --prune

# See stale branches before pruning
git remote prune origin --dry-run

# Clean up all remotes
git fetch --all --prune

# Delete remote branch
git push origin --delete feature-branch
# or
git push origin :feature-branch

# Remove all remote-tracking branches
git branch -r | grep -v main | xargs -n 1 git push --delete origin
```

---

## Mirror Repositories

![mirror_repositories](/svg/courses/git/git2/05_remotes/mirror_repositories.svg)

---

## Git Hooks for Remote Operations

```bash
# .git/hooks/pre-push
#!/bin/sh
# Prevent push to main branch
protected_branch='main'
current_branch=$(git symbolic-ref HEAD | sed -e 's,.*/\(.*\),\1,')

if [ $protected_branch = $current_branch ]; then
    echo "Direct push to main branch is not allowed"
    echo "Please create a pull request"
    exit 1
fi

# Run tests before push
npm test
if [ $? -ne 0 ]; then
    echo "Tests must pass before push"
    exit 1
fi
```

---

## Remote Performance Tips

```bash
# Shallow clone (faster for large repos)
git clone --depth 1 https://github.com/user/repo.git

# Clone specific branch only
git clone -b develop --single-branch https://github.com/user/repo.git

# Partial clone (Git 2.17+)
git clone --filter=blob:none https://github.com/user/repo.git

# Fetch only needed objects
git fetch --filter=tree:0 origin

# Bundle for offline transfer
git bundle create repo.bundle --all
# Transfer bundle file
git clone repo.bundle new-repo

# Use SSH connection multiplexing
# ~/.ssh/config
Host github.com
    ControlMaster auto
    ControlPath ~/.ssh/sockets/%r@%h-%p
    ControlPersist 600
```

---

## Submodules vs Subtrees

![submodules_vs_subtrees](/svg/courses/git/git2/05_remotes/submodules_vs_subtrees.svg)

---

## Working with Submodules

```bash
# Add submodule
git submodule add https://github.com/lib/library.git libs/library

# Clone repo with submodules
git clone --recurse-submodules https://github.com/user/repo.git

# Initialize submodules after clone
git submodule init
git submodule update

# Update all submodules
git submodule update --remote --merge

# Remove submodule
git submodule deinit path/to/submodule
git rm path/to/submodule
rm -rf .git/modules/path/to/submodule
```

---

## CI/CD Integration

![ci_cd_integration](/svg/courses/git/git2/05_remotes/ci_cd_integration.svg)

---

## GitHub Actions Example

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v2

    - name: Setup Node.js
      uses: actions/setup-node@v2
      with:
        node-version: '16'

    - name: Install dependencies
      run: npm ci

    - name: Run tests
      run: npm test

    - name: Build
      run: npm run build
```

---

## GitLab CI Example

```yaml
# .gitlab-ci.yml
stages:
  - test
  - build
  - deploy

variables:
  NODE_VERSION: "16"

test:
  stage: test
  image: node:${NODE_VERSION}
  script:
    - npm ci
    - npm test
  only:
    - merge_requests
    - main
    - develop

build:
  stage: build
  image: node:${NODE_VERSION}
  script:
    - npm ci
    - npm run build
  artifacts:
    paths:
      - dist/
  only:
    - main
```

---

## Remote Repository Security

![remote_repository_security](/svg/courses/git/git2/05_remotes/remote_repository_security.svg)

---

## Summary

## What We Learned

1. ✅ Understanding remote repositories
1. ✅ Working with multiple remotes
1. ✅ Push, pull, and fetch strategies
1. ✅ Collaboration workflows
1. ✅ Pull requests and code review
1. ✅ Conflict resolution
1. ✅ Tags and releases
1. ✅ Repository mirroring and security

---

## Key Takeaways

1. **Remotes are references** - Not the actual repository
1. **Fetch is safe, pull merges** - Fetch to review first
1. **Use branches for features** - Keep main stable
1. **Pull requests enable review** - Quality through collaboration
1. **Tags mark milestones** - Version your releases
1. **Multiple remotes are powerful** - Fork, upstream, backup
1. **Security matters** - Protect branches, sign commits, use SSH

---

## Practice Exercises

1. Set up a repository with multiple remotes
1. Create and merge a pull request
1. Resolve a merge conflict
1. Sync a fork with upstream
1. Create and push tags
1. Set up branch protection rules
1. Configure CI/CD for your repository
1. Mirror a repository between platforms

---

## Next Up: Branches

In the next session, we'll deep dive into:

1. Branch theory and internals
1. Creating and managing branches
1. Branching strategies
1. Merge vs rebase
1. Advanced branching workflows
1. Branch maintenance
1. Troubleshooting branch issues

---

## Remote Repositories Complete! 🎉

![remote_repositories_complete](/svg/courses/git/git2/05_remotes/remote_repositories_complete.svg)
