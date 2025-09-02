# Workflows

---

## What We'll Cover

1. Understanding that `Git` does not force a workflow
1. Feature branch workflows
1. Development vs production strategies
1. Back porting changes
1. Working with your own workflow
1. Popular workflow examples

---

## Git Does Not Force a Workflow

`Git` is a tool, not a process. It provides primitives that can support many different workflows:

**What `Git` provides:**
- Branching and merging capabilities
- Distributed development support
- History tracking and manipulation
- Conflict resolution mechanisms

**What `Git` does NOT dictate:**
- How many branches to use
- When to merge vs rebase
- Code review processes
- Release management strategies

**Your team decides:** workflow, policies, and collaboration patterns.

---

## Why Workflows Matter

Without established workflows, teams face:

1. **Inconsistent practices:**
    - Some developers merge, others rebase
    - Unclear branching strategies
    - Mixed commit message formats

1. **Integration problems:**
    - Conflicting changes
    - Broken builds on main branch
    - Difficulty tracking features

1. **Release challenges:**
    - Unclear what's ready for production
    - Hard to rollback problematic changes
    - No clear versioning strategy

**Solution:** Establish clear, documented workflows that fit your team and project needs.

---

## Core Workflow Concepts

**Branching strategy:**
- How branches are created and named
- Which branches are long-lived vs short-lived
- Branch protection rules

**Integration patterns:**
- How changes get into main branches
- Code review requirements
- Automated testing integration

**Release management:**
- How production releases are created
- Versioning and tagging strategies
- Hotfix procedures

---

## Feature Branches

The foundation of most modern `Git` workflows:

```bash
# Create feature branch
git checkout -b feature/user-authentication

# Work on feature
git add .
git commit -m "Add login functionality"
git commit -m "Add password validation"

# Integration back to main
git checkout main
git pull origin main
git merge feature/user-authentication
```

**Benefits:**
- Isolate feature development
- Enable parallel work
- Facilitate code reviews
- Allow feature rollback

---

## Feature Branch Naming Conventions

**Common patterns:**

```bash
# By type
feature/user-login
bugfix/memory-leak
hotfix/security-patch

# By ticket/issue
feature/JIRA-123-user-auth
bug/GH-456-login-error

# By developer (small teams)
john/user-profile-page
sarah/api-optimization
```

**Best practices:**
- Be consistent across the team
- Include context (type, ticket, description)
- Use lowercase and hyphens
- Keep names descriptive but concise

---

## Development vs Production Branches

**Development branch (`develop`):**
- Integration branch for features
- Contains latest development work
- May be unstable
- Used for testing and QA

**Production branch (`main`/`master`):**
- Always production-ready
- Only stable, tested code
- Protected from direct pushes
- Source for releases

<svg viewBox="0 0 600 250" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="20" text-anchor="middle" font-size="16" font-weight="bold">Development vs Production Flow</text>

  <!-- Main branch -->
  <line x1="50" y1="80" x2="550" y2="80" stroke="#2ecc71" stroke-width="3"/>
  <text x="30" y="85" font-size="12" fill="#2ecc71">main</text>

  <!-- Develop branch -->
  <line x1="50" y1="130" x2="550" y2="130" stroke="#3498db" stroke-width="3"/>
  <text x="20" y="135" font-size="12" fill="#3498db">develop</text>

  <!-- Feature branches -->
  <line x1="150" y1="130" x2="150" y2="180" stroke="#e74c3c" stroke-width="2"/>
  <line x1="150" y1="180" x2="250" y2="180" stroke="#e74c3c" stroke-width="2"/>
  <line x1="250" y1="180" x2="250" y2="130" stroke="#e74c3c" stroke-width="2"/>

  <line x1="300" y1="130" x2="300" y2="200" stroke="#f39c12" stroke-width="2"/>
  <line x1="300" y1="200" x2="400" y2="200" stroke="#f39c12" stroke-width="2"/>
  <line x1="400" y1="200" x2="400" y2="130" stroke="#f39c12" stroke-width="2"/>

  <!-- Release points -->
  <circle cx="200" cy="80" r="5" fill="#9b59b6"/>
  <circle cx="350" cy="80" r="5" fill="#9b59b6"/>
  <circle cx="500" cy="80" r="5" fill="#9b59b6"/>

  <text x="200" y="100" text-anchor="middle" font-size="10">v1.0</text>
  <text x="350" y="100" text-anchor="middle" font-size="10">v1.1</text>
  <text x="500" y="100" text-anchor="middle" font-size="10">v1.2</text>

  <text x="200" y="195" font-size="10" fill="#e74c3c">feature-A</text>
  <text x="350" y="215" font-size="10" fill="#f39c12">feature-B</text>
</svg>

---

## Back Porting Changes

Moving changes from newer versions to older versions:

**Common scenarios:**
- Security fixes to older releases
- Critical bug fixes
- Customer-specific patches

**Cherry-pick approach:**
```bash
# Apply specific commit to older branch
git checkout release/v1.0
git cherry-pick <commit-hash-from-main>
```

**Merge approach:**
```bash
# Create patch branch from older version
git checkout -b hotfix/security-patch release/v1.0
# Make changes
git checkout release/v1.0
git merge hotfix/security-patch
```

---

## Working with Your Own Workflow

**For solo projects:**

```bash
# Simple workflow
git checkout -b feature/new-functionality
# Work and commit
git checkout main
git merge feature/new-functionality
git branch -d feature/new-functionality
```

**Personal best practices:**
- Use meaningful commit messages
- Create atomic commits
- Test before merging to main
- Tag important versions
- Keep main branch clean

---

## Centralized Workflow

Similar to traditional version control systems:

**Characteristics:**
- Everyone works on the main branch
- Linear history
- Simple to understand
- Good for small, co-located teams

```bash
# Daily workflow
git pull origin main
# Make changes
git add .
git commit -m "Add new feature"
git push origin main
```

**Limitations:**
- No isolation between features
- Conflicts more frequent
- Hard to review changes
- Risk of breaking main branch

---

## Feature Branch Workflow

Most common modern approach:

**Process:**
1. Create feature branch from main
1. Develop feature in isolation
1. Push branch to remote
1. Create pull/merge request
1. Code review and discussion
1. Merge to main after approval

```bash
# Complete feature workflow
git checkout main
git pull origin main
git checkout -b feature/user-profiles
# Develop feature
git push -u origin feature/user-profiles
# Create pull request via web interface
# After review and approval, merge
```

---

## Git Flow Workflow

Structured workflow with specific branch types:

**Branch types:**
- `main`: production releases
- `develop`: integration branch
- `feature/*`: individual features
- `release/*`: preparation for releases
- `hotfix/*`: urgent production fixes

**Commands:**

```bash
# Start new feature
git flow feature start user-auth

# Finish feature (merges to develop)
git flow feature finish user-auth

# Start release
git flow release start 1.2.0

# Finish release (merges to main and develop)
git flow release finish 1.2.0
```

---

## GitHub Flow

Simplified workflow popular with continuous deployment:

**Process:**
1. Create branch from main
1. Add commits
1. Open pull request
1. Discuss and review
1. Deploy and test
1. Merge to main

**Benefits:**
- Simple and straightforward
- Good for continuous deployment
- Fast iteration cycles
- Web-based collaboration

**Best for:** Web applications, frequent deployments, small teams

---

## GitLab Flow

Combines feature branches with environment branches:

**Structure:**
- `main`: latest development
- `production`: current production code
- `pre-production`: staging environment
- Feature branches for development

**Workflow:**

```bash
# Development
git checkout -b feature/new-ui
# Work and create merge request to main

# Deploy to production
git checkout production
git merge main
```

**Benefits:** Clear separation of environments, controlled releases

---

## Forking Workflow

Used in open source projects:

**Process:**
1. Fork repository to personal account
1. Clone personal fork
1. Create feature branch
1. Push to personal fork
1. Create pull request to original repository

```bash
# Clone your fork
git clone git@github.com:yourusername/project.git
cd project

# Add upstream remote
git remote add upstream git@github.com:originalowner/project.git

# Create feature branch
git checkout -b feature/improvement

# Work and push to your fork
git push origin feature/improvement
# Create pull request via web interface
```

---

## Release Branch Workflow

For projects with scheduled releases:

**Branch structure:**
- `main`: ongoing development
- `release/v1.0`: release preparation
- `release/v1.1`: next release
- Feature branches merge to main

**Process:**

```bash
# Create release branch
git checkout -b release/v1.2 main

# Bug fixes and final preparations
git commit -m "Fix release blocking bug"

# Merge to production
git checkout production
git merge release/v1.2

# Tag the release
git tag -a v1.2 -m "Release version 1.2"
```

---

## Environment-Based Workflows

**Multiple environment branches:**

```bash
# Environment progression
development → staging → production
```

**Deployment workflow:**

```bash
# Promote to staging
git checkout staging
git merge development

# After testing, promote to production
git checkout production
git merge staging
```

**Benefits:**
- Clear promotion path
- Environment-specific configurations
- Controlled release process
- Easy rollback capabilities

---

## Continuous Integration Workflows

Integrating automated testing and deployment:

**Branch protection rules:**
- Require pull request reviews
- Require status checks to pass
- Require branches to be up to date
- Restrict pushes to main

**CI/CD pipeline:**
1. Developer pushes to feature branch
1. Automated tests run
1. Code review required
1. Merge only if tests pass
1. Automatic deployment to staging
1. Manual promotion to production

---

## Workflow Selection Criteria

**Team size:**
- Small (1-5): Simple feature branch or GitHub flow
- Medium (5-20): Git flow or GitLab flow
- Large (20+): Forking workflow or custom enterprise workflow

**Release frequency:**
- Continuous: GitHub flow
- Weekly/Monthly: Git flow
- Scheduled major releases: Release branch workflow

**Project type:**
- Web applications: GitHub flow
- Desktop software: Git flow
- Open source: Forking workflow
- Enterprise: Custom workflow with governance

---

## Adapting Workflows to Your Needs

**Questions to consider:**

1. **How often do you release?**
    - Continuous deployment needs simple workflows
    - Scheduled releases need more structure

1. **How many environments do you have?**
    - More environments need more branches
    - Simple projects can use main + feature branches

1. **What's your team's `Git` experience?**
    - Beginners need simple workflows
    - Experienced teams can handle complexity

1. **What are your quality requirements?**
    - High-quality needs mandatory reviews
    - Fast iteration allows more flexibility

---

## Common Workflow Pitfalls

**Over-engineering:**
- Too many branch types
- Overly complex rules
- Unnecessary bureaucracy

**Under-engineering:**
- No code review process
- Direct pushes to production
- No testing integration

**Inconsistent application:**
- Team members using different approaches
- Partial adoption of workflow rules
- No documentation or training

**Solution:** Start simple, iterate based on team needs, document clearly, and ensure consistent adoption.
