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
  - audiences:managers

---
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
## Development vs Production Branches: Details

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

---
## Development vs Production Branches

![development_vs_production_branches](svg/courses/git/git/09_workflows/development_vs_production_branches.svg)

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

---

## Jenkins Integration Workflow

`Jenkins` can automate many `Git` workflow steps:

**Pipeline triggers:**
```groovy
pipeline {
    agent any
    triggers {
        githubPush()
    }
    stages {
        stage('Build') {
            when { branch 'main' }
            steps {
                sh 'make build'
            }
        }
        stage('Test') {
            steps {
                sh 'make test'
            }
        }
        stage('Deploy') {
            when { branch 'production' }
            steps {
                sh 'make deploy'
            }
        }
    }
}
```

**Branch-specific builds:**
- Feature branches: run tests only
- `develop`: run tests + integration tests
- `main`: full build + deploy to staging
- `production`: deploy to production

---

## Working with Pull Requests

Pull requests enable code review and discussion before integration:

**Creating effective pull requests:**
```bash
# Prepare your branch
git checkout feature/user-authentication
git rebase main
git push -u origin feature/user-authentication
```

**PR best practices:**
1. **Clear title and description**
1. **Small, focused changes**
1. **Include tests and documentation**
1. **Reference related issues**
1. **Request appropriate reviewers**

**Review process:**
- At least one approval required
- Address feedback promptly
- Keep discussions constructive
- Update branch if main advances

---

## Gerrit Code Review Workflow

`Gerrit` provides a different approach to code review:

**Key concepts:**
- Every commit becomes a change request
- Review before integration (not after)
- Score-based approval system
- Automatic testing integration

**Workflow:**

```bash
# Clone with commit-msg hook
git clone ssh://user@gerrit:29418/project
cd project
scp -p -P 29418 user@gerrit:hooks/commit-msg .git/hooks/

# Make changes and commit
git add .
git commit -m "Add user authentication

Change-Id: I1234567890abcdef..."

# Push for review
git push origin HEAD:refs/for/main
```

---

## Automated Testing Integration

Integrate testing at multiple workflow points:

**Pre-commit hooks:**
```bash
#!/bin/sh
# .git/hooks/pre-commit
npm test
if [ $? -ne 0 ]; then
    echo "Tests failed. Commit aborted."
    exit 1
fi
```

**CI/CD pipeline stages:**
1. **Unit tests:** Fast, isolated tests
1. **Integration tests:** Component interaction
1. **End-to-end tests:** Full system validation
1. **Performance tests:** Load and stress testing

**Quality gates:**
- Minimum test coverage
- No critical security vulnerabilities
- Code style compliance
- Documentation updates

---

## Release Management Workflows

**Semantic versioning with `Git` tags:**

```bash
# Major release (breaking changes)
git tag -a v2.0.0 -m "Release 2.0.0 - Breaking API changes"

# Minor release (new features)
git tag -a v1.5.0 -m "Release 1.5.0 - Add user profiles"

# Patch release (bug fixes)
git tag -a v1.4.1 -m "Release 1.4.1 - Fix login bug"

git push origin --tags
```

**Release branch workflow:**

```bash
# Start release
git checkout -b release/v1.5.0 develop

# Final preparations
git commit -m "Update version numbers"
git commit -m "Update changelog"

# Merge to main and tag
git checkout main
git merge --no-ff release/v1.5.0
git tag -a v1.5.0 -m "Release 1.5.0"

# Merge back to develop
git checkout develop
git merge --no-ff release/v1.5.0
```

---

## Hotfix Workflows

Handle urgent production fixes:

**Git Flow hotfix:**

```bash
# Start hotfix from main
git checkout -b hotfix/security-patch main

# Make the fix
git commit -m "Fix critical security vulnerability"

# Merge to main
git checkout main
git merge --no-ff hotfix/security-patch
git tag -a v1.4.2 -m "Hotfix v1.4.2"

# Merge to develop
git checkout develop
git merge --no-ff hotfix/security-patch

# Deploy immediately
git push origin main --tags
```

**Emergency deployment process:**
1. Create hotfix branch
1. Implement minimal fix
1. Test thoroughly
1. Deploy to production
1. Integrate back to development branches

---

## Multi-Repository Workflows

Managing workflows across multiple repositories:

**Microservices architecture:**
```bash
# Each service has its own repository
user-service/
payment-service/
notification-service/
```

**Coordination strategies:**
1. **Independent releases:** Each service deploys separately
1. **Synchronized releases:** All services deploy together
1. **Progressive deployment:** Gradual rollout across services

**Tools for multi-repo management:**
- `Git` submodules
- `Git` subtrees
- Monorepo tools (Lerna, Nx)
- Container orchestration

---

## Large Team Workflows

Scaling `Git` workflows for large organizations:

**Branch permissions:**

```bash
# Only maintainers can merge to main
main: requires reviews from CODEOWNERS

# Feature branches can be created by anyone
feature/*: open access

# Release branches restricted
release/*: requires release team approval
```

**Code ownership:**

```config
# CODEOWNERS file
/frontend/          @frontend-team
/backend/           @backend-team
/docs/              @docs-team
*.md                @docs-team
```

**Approval workflows:**
- Multiple reviewers required
- Domain expert approval
- Security team review for sensitive changes
- Automated compliance checks

---

## Monorepo vs Polyrepo Workflows

**Monorepo benefits:**
- Atomic changes across projects
- Shared tooling and configuration
- Easier dependency management
- Unified CI/CD pipeline

**Monorepo workflow:**

```bash
# Project structure
project/
├── frontend/
├── backend/
├── shared/
└── tools/

# Build specific components
npm run build:frontend
npm run build:backend
```

**Polyrepo benefits:**
- Independent team ownership
- Separate release cycles
- Isolated dependencies
- Smaller repository size

---

## Workflow Automation Tools

**GitHub Actions:**
```yaml
name: CI/CD Pipeline
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
    - name: Run tests
      run: npm test

  deploy:
    if: github.ref == 'refs/heads/main'
    needs: test
    runs-on: ubuntu-latest
    steps:
    - name: Deploy to production
      run: ./deploy.sh
```

---

## Workflow Automation Tools: GitLab CI

**GitLab CI/CD:**
```yaml
stages:
  - test
  - build
  - deploy

test:
  stage: test
  script:
    - npm test
  only:
    - branches

deploy_production:
  stage: deploy
  script:
    - ./deploy.sh production
  only:
    - main
```

---

## Workflow Documentation

**Essential documentation:**

1. **Workflow overview:**
    - Branch strategy explanation
    - Integration process
    - Release procedures

1. **Step-by-step guides:**
    - Creating feature branches
    - Code review process
    - Deployment procedures

1. **Troubleshooting guides:**
    - Common merge conflicts
    - Failed CI builds
    - Rollback procedures

**Documentation format:**
```markdown
# Development Workflow

## Feature Development
1. Create branch: `git checkout -b feature/TICKET-123`
1. Develop and test locally
1. Push and create pull request
1. Address review feedback
1. Merge after approval

## Code Review Checklist
- [ ] Tests included and passing
- [ ] Documentation updated
- [ ] No breaking changes
- [ ] Security considerations addressed
```

---

## Workflow Metrics and Monitoring

**Key metrics to track:**

1. **Development velocity:**
    - Time from branch creation to merge
    - Number of commits per feature
    - Code review turnaround time

1. **Quality metrics:**
    - Build failure rate
    - Test coverage trends
    - Post-deployment issues

1. **Collaboration metrics:**
    - Pull request review participation
    - Merge conflict frequency
    - Branch lifetime

**Tools for metrics:**
- GitHub/GitLab analytics
- Jenkins build metrics
- Custom dashboards
- Third-party tools (LinearB, Velocity)

---

## Workflow Troubleshooting

**Common workflow problems:**

1. **Merge conflicts increase:**
    - Solution: Smaller, more frequent merges
    - Solution: Better communication between teams
    - Solution: Automated conflict detection

1. **Long-lived feature branches:**
    - Solution: Break features into smaller chunks
    - Solution: Regular rebasing on main
    - Solution: Feature flags for partial completion

1. **Broken main branch:**
    - Solution: Mandatory pre-merge testing
    - Solution: Rollback procedures
    - Solution: Branch protection rules

1. **Slow code reviews:**
    - Solution: Smaller pull requests
    - Solution: Clear reviewer assignments
    - Solution: Review time targets

---

## Migrating Between Workflows

**From centralized to feature branch:**
```bash
# Train team on branching
# Implement branch protection
# Establish code review process
# Gradually enforce new workflow
```

**From Git Flow to GitHub Flow:**
```bash
# Simplify branch structure
# Remove unnecessary branches
# Focus on main branch
# Implement continuous deployment
```

**Migration best practices:**
1. Plan the transition carefully
1. Train team members
1. Run workflows in parallel initially
1. Document new processes clearly
1. Monitor and adjust based on feedback

---

## Custom Workflow Development

**Designing your own workflow:**

1. **Assess current needs:**
    - Team size and distribution
    - Release frequency
    - Quality requirements
    - Compliance needs

1. **Start with proven patterns:**
    - Adapt existing workflows
    - Don't reinvent unnecessarily
    - Learn from similar organizations

1. **Iterate and improve:**
    - Start simple
    - Add complexity gradually
    - Gather team feedback
    - Measure effectiveness

**Example custom workflow:**
```bash
# Company-specific branch naming
epic/PROJ-123-user-management
story/PROJ-124-login-form
task/PROJ-125-password-validation
```

---

## Workflow Training and Adoption

**Training program structure:**

1. **Git fundamentals:**
    - Basic commands
    - Branching concepts
    - Merge vs rebase

1. **Workflow specifics:**
    - Branch naming conventions
    - Code review process
    - Deployment procedures

1. **Tools and automation:**
    - CI/CD pipeline usage
    - Code review tools
    - Monitoring dashboards

**Adoption strategies:**
- Pair programming sessions
- Workflow champions
- Regular retrospectives
- Gradual enforcement

---

## Future Workflow Trends

**Emerging patterns:**

1. **Trunk-based development:**
    - Very short-lived branches
    - Feature flags for incomplete work
    - Continuous integration emphasis

1. **AI-assisted workflows:**
    - Automated code review
    - Intelligent conflict resolution
    - Predictive merge analysis

1. **Cloud-native workflows:**
    - Container-based development
    - Infrastructure as code
    - GitOps practices

**Preparing for change:**
- Stay flexible in workflow design
- Invest in automation
- Focus on principles over tools
- Continuous learning and adaptation

---

## Lab Exercise: Implementing a Workflow

**Scenario:** Small development team (5 developers) building a web application with weekly releases.

**Tasks:**
1. **Design a workflow:**
    - Choose branch strategy
    - Define integration process
    - Plan release procedures

1. **Implement branch protection:**
    - Set up repository rules
    - Configure automated testing
    - Establish code review requirements

1. **Create documentation:**
    - Write workflow guide
    - Document troubleshooting steps
    - Create team training materials

1. **Practice the workflow:**
    - Simulate feature development
    - Handle merge conflicts
    - Execute release process

**Deliverables:** Complete workflow documentation, configured repository, and team training presentation.

---

## Workflow Summary and Best Practices

**Key takeaways:**

1. **Choose workflows that fit your context:**
    - Team size and experience
    - Release requirements
    - Quality standards

1. **Start simple and evolve:**
    - Don't over-engineer initially
    - Add complexity as needed
    - Regular workflow retrospectives

1. **Automation is essential:**
    - Automated testing
    - CI/CD pipelines
    - Quality gates

1. **Documentation and training:**
    - Clear, up-to-date guides
    - Regular team training
    - Onboarding materials

**Remember:** The best workflow is one that your team actually follows consistently and that supports your business objectives.
