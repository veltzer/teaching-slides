---
tags:
  - tools:git
  - concepts:version-control
level: intermediate
category: version-control
audience:
  - audiences:developers
  - audiences:sysadmins
  - audiences:devops

---
# Git Tools

---

## What We'll Cover

1. Git and programming languages: GitPython
1. Git and development platforms: GitHub, BitBucket, GitLab
1. Git and IDEs: PyCharm, Eclipse, Spyder
1. Git and CI/CD tools: Jenkins, Bamboo
1. Command-line tools and extensions
1. Desktop applications and visual tools

---

## GitPython: Git for Python

Programmatic Git access in Python applications:

**Installation:**

```bash
pip install GitPython
```

**Basic repository operations:**

```python
from git import Repo

# Open existing repository
repo = Repo('/path/to/repo')

# Clone repository
repo = Repo.clone_from('https://github.com/user/repo.git', '/local/path')

# Check repository status
print(f"Active branch: {repo.active_branch}")
print(f"Is dirty: {repo.is_dirty()}")

# Get commit information
commit = repo.head.commit
print(f"Latest commit: {commit.hexsha[:8]}")
print(f"Author: {commit.author}")
print(f"Message: {commit.message}")
```

**Working with branches:**

```python
# List branches
for branch in repo.branches:
    print(f"Branch: {branch.name}")

# Create new branch
new_branch = repo.create_head('feature-branch')

# Switch branches
repo.heads.main.checkout()

# Merge branches
repo.git.merge('feature-branch')
```

---

## GitPython Advanced Operations

Complex Git operations through Python:

**Commit operations:**

```python
# Stage files
repo.index.add(['file1.py', 'file2.py'])

# Create commit
repo.index.commit('Add new features')

# Commit with author override
from git import Actor
author = Actor('John Doe', 'john@example.com')
repo.index.commit('Fix bug', author=author)

# Amend last commit
repo.index.commit('Updated commit message', amend=True)
```

**Repository analysis:**

```python
# Analyze commit history
commits = list(repo.iter_commits('main', max_count=100))

# Count commits by author
from collections import Counter
authors = [commit.author.name for commit in commits]
author_counts = Counter(authors)
print("Top contributors:", author_counts.most_common(5))

# Find files changed most frequently
changed_files = []
for commit in commits:
    for item in commit.stats.files:
        changed_files.append(item)

file_counts = Counter(changed_files)
print("Most changed files:", file_counts.most_common(10))
```

---

## GitHub Integration

Working with GitHub's platform and API:

**GitHub CLI (gh):**

```bash
# Install GitHub CLI
# brew install gh (macOS)
# sudo apt install gh (Ubuntu)

# Authenticate
gh auth login

# Repository operations
gh repo create my-project
gh repo clone user/repository
gh repo fork upstream/repository

# Pull request workflow
gh pr create --title "New feature" --body "Description"
gh pr list
gh pr view 123
gh pr merge 123

# Issue management
gh issue create --title "Bug report"
gh issue list --state open
gh issue close 456
```

**GitHub Actions integration:**

```yaml
# .github/workflows/ci.yml
name: CI Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Python
        uses: actions/setup-python@v3
        with:
          python-version: '3.9'

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run tests
        run: python -m pytest

      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

---

## BitBucket Integration

Atlassian's Git platform features:

**Bitbucket Pipelines:**
```yaml
# bitbucket-pipelines.yml
image: python:3.9

pipelines:
  default:
    - step:
        name: Run tests
        caches:
          - pip
        script:
          - pip install -r requirements.txt
          - python -m pytest --junitxml=test-results/junit.xml
        artifacts:
          - test-results/**

  branches:
    main:
      - step:
          name: Deploy to production
          deployment: production
          script:
            - ./deploy.sh production
```

**Bitbucket API access:**

```python
import requests

# API configuration
api_base = "https://api.bitbucket.org/2.0"
username = "your-username"
app_password = "your-app-password"

# List repositories
response = requests.get(
    f"{api_base}/repositories/{username}",
    auth=(username, app_password)
)

for repo in response.json()['values']:
    print(f"Repository: {repo['name']}")
    print(f"Language: {repo['language']}")
```

---

## GitLab Integration

GitLab's DevOps platform capabilities:

**GitLab CI/CD:**
```yaml
# .gitlab-ci.yml
stages:
  - test
  - build
  - deploy

variables:
  POSTGRES_DB: test_db
  POSTGRES_USER: runner
  POSTGRES_PASSWORD: ""

test:
  stage: test
  image: python:3.9
  services:
    - postgres:13
  before_script:
    - pip install -r requirements.txt
  script:
    - python -m pytest
  coverage: '/TOTAL.*\s+(\d+%)$/'

build:
  stage: build
  script:
    - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA .
    - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
  only:
    - main

deploy:
  stage: deploy
  script:
    - kubectl set image deployment/app app=$CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
  only:
    - main
```

**GitLab API integration:**

```python
import gitlab

# Connect to GitLab
gl = gitlab.Gitlab('https://gitlab.example.com', private_token='your-token')

# Project operations
project = gl.projects.get('project-id')
print(f"Project: {project.name}")

# List merge requests
mrs = project.mergerequests.list(state='opened')
for mr in mrs:
    print(f"MR: {mr.title} by {mr.author['name']}")

# Create issue
issue = project.issues.create({'title': 'Bug report',
                              'description': 'Something is broken'})
```

---

## PyCharm Git Integration

JetBrains IDE Git features:

**Version Control Tool Window:**
- **Local Changes:** View modified files
- **Log:** Interactive commit history
- **Console:** Git command execution
- **Branches:** Visual branch management

**Git operations in PyCharm:**

```python
# Git menu operations available:
# VCS → Git → Clone...
# VCS → Commit...
# VCS → Push...
# VCS → Pull...
# VCS → Branches...
# VCS → Merge Changes...
# VCS → Rebase...
```

**PyCharm Git workflow:**
1. **Clone repository:** VCS → Get from Version Control
1. **Make changes:** Edit files normally
1. **Review changes:** Version Control tool window
1. **Commit:** Ctrl+K (Windows/Linux) or Cmd+K (macOS)
1. **Push:** Ctrl+Shift+K or VCS → Push

**Advanced PyCharm features:**
- Visual merge conflict resolution
- Interactive rebase
- Shelve changes (similar to stash)
- Annotate (git blame integration)
- Compare branches and commits

---

## Eclipse Git Integration (EGit)

Eclipse IDE's Git plugin:

**EGit basic operations:**

```tree
Window → Show View → Other → Git → Git Repositories

Right-click project:
├── Team → Share Project → Git
├── Team → Commit...
├── Team → Push Branch...
├── Team → Pull...
├── Team → Switch To → [branch]
└── Team → Merge...
```

**Eclipse Git workflow:**
1. **Import Git project:** File → Import → Git → Projects from Git
1. **Stage changes:** Git Staging view
1. **Commit:** Enter message and commit
1. **Push/Pull:** Right-click → Team → Push/Pull

**EGit features:**
- Git Staging view for index management
- Git Repositories view for repository navigation
- History view for commit browsing
- Blame annotations
- Interactive rebase support

---

## Spyder Git Integration

Python IDE Git integration:

**Spyder Git plugin:**

```bash
# Install Git plugin for Spyder
pip install spyder-git

# Enable in Spyder:
# View → Panes → Git
```

**Git operations in Spyder:**
- **Git pane:** Shows repository status
- **File differences:** Compare working vs committed
- **Commit interface:** Stage and commit changes
- **Branch switching:** Dropdown branch selector

**Spyder workflow integration:**

```python
# Typical scientific workflow with version control
import numpy as np
import matplotlib.pyplot as plt

# Work on analysis
data = np.random.normal(0, 1, 1000)
plt.hist(data, bins=30)
plt.savefig('analysis_result.png')

# Commit analysis results through Spyder Git interface
# Stage: analysis_result.png, analysis_script.py
# Commit: "Add histogram analysis of random data"
```

---

## Jenkins Git Integration

Continuous Integration with Jenkins:

**Jenkinsfile (Pipeline as Code):**

```groovy
pipeline {
    agent any

    triggers {
        pollSCM('H/5 * * * *')  // Poll every 5 minutes
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build') {
            steps {
                sh 'make clean'
                sh 'make build'
            }
        }

        stage('Test') {
            steps {
                sh 'make test'
                publishTestResults testResultsPattern: 'test-results/*.xml'
            }
        }

        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                sh './deploy.sh production'
            }
        }
    }

    post {
        always {
            cleanWs()
        }
        failure {
            mail to: 'team@example.com',
                 subject: "Build Failed: ${env.JOB_NAME} - ${env.BUILD_NUMBER}",
                 body: "Build failed. Check console output at ${env.BUILD_URL}"
        }
    }
}
```

**Jenkins Git webhook setup:**

```bash
# GitHub webhook URL for Jenkins
https://jenkins.example.com/github-webhook/

# GitLab webhook URL
https://jenkins.example.com/project/PROJECT_NAME
```

---

## Bamboo Git Integration

Atlassian's CI/CD tool with Git:

**Bamboo build plan:**

```yaml
# bamboo-specs/bamboo.yml
version: 2

plan:
  key: PROJ-BUILD
  name: Project Build Plan

stages:
  - Test:
      jobs:
        - Test:
            tasks:
              - checkout:
                  repository: origin
              - script:
                  interpreter: SHELL
                  scripts:
                    - npm install
                    - npm test
            artifacts:
              - name: Test Results
                pattern: test-results/**
                shared: true

  - Deploy:
      jobs:
        - Deploy:
            tasks:
              - script:
                  interpreter: SHELL
                  scripts:
                    - ./deploy.sh
```

**Bamboo Git integration features:**
- Repository polling
- Branch detection
- Merge check builds
- Git flow integration
- Deployment environments

---

## Command-Line Git Tools

Enhanced command-line Git experience:

**Git aliases for productivity:**

```bash
# Add to ~/.gitconfig
[alias]
    st = status --short --branch
    co = checkout
    br = branch
    ci = commit
    unstage = reset HEAD --
    last = log -1 HEAD
    visual = !gitk

    # Advanced aliases
    lg = log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit
    find = "!git ls-files | grep -i"
    grep = grep -Ii
    la = "!git config -l | grep alias | cut -c 7-"
```

**Git prompt customization:**

```bash
# Add to ~/.bashrc or ~/.zshrc
parse_git_branch() {
    git branch 2> /dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/(\1)/'
}

export PS1="\u@\h \[\033[32m\]\w\[\033[33m\]\$(parse_git_branch)\[\033[00m\] $ "
```

**Tig - Text-mode Git interface:**

```bash
# Install tig
brew install tig        # macOS
sudo apt install tig    # Ubuntu

# Usage
tig                      # Browse repository
tig status              # Interactive status
tig log                 # Browse log
tig blame file.py       # File annotations
```

---

## Desktop Git Applications

Visual Git clients for different platforms:

**GitKraken:**

```tree
Features:
├── Visual commit graph
├── Drag-and-drop branch management
├── Built-in merge conflict editor
├── GitHub/GitLab/Bitbucket integration
├── Git flow and Git LFS support
└── Team collaboration features
```

**SourceTree:**

```tree
Features:
├── Atlassian integration
├── Git flow built-in
├── Interactive rebase
├── File history and blame
├── Submodule support
└── Free for personal/commercial use
```

**GitHub Desktop:**

```tree
Features:
├── Simplified Git workflow
├── GitHub integration
├── Visual diff viewer
├── Branch management
├── Conflict resolution
└── Beginner-friendly interface
```

---

## Specialized Git Tools

Domain-specific Git tools:

**Git LFS (Large File Storage):**

```bash
# Install Git LFS
git lfs install

# Track large files
git lfs track "*.psd"
git lfs track "*.zip"
git lfs track "data/*.csv"

# Check LFS status
git lfs status
git lfs ls-files

# Migrate existing files
git lfs migrate import --include="*.zip"
```

**Git Filter-Repo:**

```bash
# Install git-filter-repo
pip install git-filter-repo

# Remove sensitive data
git filter-repo --path passwords.txt --invert-paths

# Extract subdirectory
git filter-repo --subdirectory-filter src/

# Rewrite author information
git filter-repo --mailmap-from-file mailmap.txt
```

**Pre-commit hooks framework:**

```bash
# Install pre-commit
pip install pre-commit

# Create .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files

# Install hooks
pre-commit install

# Run on all files
pre-commit run --all-files
```

---

## Git Tool Integration Patterns

Common integration strategies:

**API-first approach:**

```python
# Generic Git platform abstraction
class GitPlatform:
    def __init__(self, platform_type, token):
        if platform_type == 'github':
            from github import Github
            self.client = Github(token)
        elif platform_type == 'gitlab':
            import gitlab
            self.client = gitlab.Gitlab(url, private_token=token)

    def create_issue(self, repo, title, description):
        if isinstance(self.client, Github):
            repo = self.client.get_repo(repo)
            return repo.create_issue(title, description)
        elif isinstance(self.client, gitlab.Gitlab):
            project = self.client.projects.get(repo)
            return project.issues.create({'title': title, 'description': description})
```

**Webhook integration:**

```python
from flask import Flask, request
import subprocess

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    payload = request.json

    if payload['ref'] == 'refs/heads/main':
        # Trigger deployment
        subprocess.run(['./deploy.sh'], cwd='/path/to/project')
        return 'Deployment triggered', 200

    return 'No action taken', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

---
## Tool Selection Criteria

![tool_selection_criteria](svg/courses/git/git2/20_tools/tool_selection_criteria.svg)

---

## Tool Performance Comparison

Benchmarking different Git tools:

**Command-line vs GUI performance:**

```bash
# Benchmark common operations
time git clone https://github.com/torvalds/linux.git
time git log --oneline | wc -l
time git status
time git diff HEAD~1..HEAD

# GUI tools typically:
# - Slower for bulk operations
# - Better for visual comparisons
# - More intuitive for beginners
# - Better merge conflict resolution
```

**Memory and CPU usage:**

| Tool Type | Memory Usage | CPU Usage | Startup Time |
|-----------|--------------|-----------|--------------|
| Command Line | Low | Low | Instant |
| IDE Integration | Medium | Medium | Fast |
| Desktop GUI | High | Medium | Medium |
| Web Interface | High | Low | Slow |

---

## Security Considerations for Git Tools

Security aspects of various Git tools:

**Authentication methods:**

```bash
# SSH keys (most secure)
ssh-keygen -t ed25519 -C "your_email@example.com"

# Personal access tokens
# GitHub: Settings → Developer settings → Personal access tokens
# GitLab: User Settings → Access Tokens

# App passwords (Bitbucket)
# Account settings → App passwords
```

**Tool security practices:**
- Use official tool repositories
- Keep tools updated
- Review tool permissions
- Use encrypted connections (HTTPS/SSH)
- Enable two-factor authentication
- Audit tool access regularly

**IDE security:**

```tree
IDE Security Checklist:
├── Keep IDE updated
├── Verify plugin sources
├── Review plugin permissions
├── Use secure credential storage
├── Enable IDE security features
└── Regular security audits
```

---

## Custom Tool Development

Building custom Git tools:

**Git command wrapper script:**

```bash
#!/bin/bash
# git-stats - Custom Git statistics tool

case "$1" in
    "authors")
        git log --format='%aN' | sort -u | wc -l
        echo "Total authors: $(git log --format='%aN' | sort -u | wc -l)"
        ;;
    "files")
        git ls-files | wc -l
        echo "Total files: $(git ls-files | wc -l)"
        ;;
    "commits")
        git rev-list --count HEAD
        echo "Total commits: $(git rev-list --count HEAD)"
        ;;
    *)
        echo "Usage: git stats [authors|files|commits]"
        ;;
esac
```

**Python Git tool:**

```python
#!/usr/bin/env python
# git-report - Generate repository report

import git
import sys
from datetime import datetime, timedelta

def generate_report(repo_path):
    repo = git.Repo(repo_path)

    # Recent activity (last 30 days)
    since_date = datetime.now() - timedelta(days=30)
    recent_commits = list(repo.iter_commits(since=since_date))

    print(f"Repository Report for {repo_path}")
    print("=" * 50)
    print(f"Active branch: {repo.active_branch}")
    print(f"Total commits: {repo.git.rev_list('--count', 'HEAD')}")
    print(f"Recent commits (30 days): {len(recent_commits)}")

    # Top contributors (recent)
    authors = {}
    for commit in recent_commits:
        author = commit.author.name
        authors[author] = authors.get(author, 0) + 1

    print("\nTop contributors (last 30 days):")
    for author, count in sorted(authors.items(), key=lambda x: x[1], reverse=True):
        print(f"  {author}: {count} commits")

if __name__ == "__main__":
    repo_path = sys.argv[1] if len(sys.argv) > 1 else "."
    generate_report(repo_path)
```

---

## Lab Exercise: Git Tool Ecosystem

**Scenario:** Set up a complete Git tool ecosystem for a development team with multiple platforms and automation requirements.

**Setup tasks:**
1. **Platform integration:**
   - Configure GitHub/GitLab repository with CI/CD
   - Set up IDE Git integration for team members
   - Install and configure desktop Git clients

1. **Automation setup:**
   - Create pre-commit hooks with quality checks
   - Set up automated testing with Jenkins/GitHub Actions
   - Configure deployment pipelines

1. **Developer experience:**
   - Customize Git command-line experience
   - Set up IDE-specific Git workflows
   - Create team Git aliases and configurations

**Advanced tasks:**
1. **Custom tool development:**
   - Build repository analysis tools
   - Create workflow automation scripts
   - Develop team-specific Git extensions

1. **Performance optimization:**
   - Benchmark different tools and workflows
   - Optimize CI/CD pipeline performance
   - Create monitoring and alerting

**Deliverables:** Complete Git tool ecosystem setup, custom automation tools, team configuration templates, performance benchmarks, and comprehensive documentation.

---

## Future of Git Tooling

Emerging trends in Git tools:

**AI-powered Git tools:**
- Intelligent commit message generation
- Automated code review suggestions
- Smart merge conflict resolution
- Predictive branch management

**Cloud-native Git platforms:**
- Serverless CI/CD pipelines
- Container-based development environments
- Distributed version control at scale
- Edge-computing for Git operations

**Integration trends:**
- DevSecOps integration
- Infrastructure as Code (GitOps)
- Machine learning model versioning
- Blockchain-based code integrity

**Developer experience improvements:**
- Better conflict resolution UIs
- Real-time collaboration features
- Voice-controlled Git operations
- AR/VR code visualization

---

## Summary: Mastering the Git Ecosystem

**Key takeaways:**

1. **Rich ecosystem available:**
   - Tools for every development environment
   - Integration options for all platforms
   - Automation possibilities are extensive

1. **Choose tools strategically:**
   - Consider team size and expertise
   - Match tools to workflow requirements
   - Balance features with complexity
   - Prioritize security and reliability

1. **Integrate thoughtfully:**
   - Combine tools for optimal workflow
   - Automate repetitive tasks
   - Maintain consistency across team
   - Monitor and optimize performance

1. **Stay current and adaptable:**
   - Tools evolve rapidly
   - New platforms emerge regularly
   - Team needs change over time
   - Invest in learning core concepts

**Remember:** The Git tool ecosystem is vast and constantly evolving. While it's important to leverage tools effectively, remember that they are means to an end. Focus on understanding Git fundamentals first, then choose tools that enhance your productivity without creating unnecessary complexity. The best Git workflow is one that your entire team can understand, use consistently, and maintain over time.
