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
# Introduction to Git

---

## What We'll Cover Today

1. History of Git
1. Why Git was created
1. Who is using Git
1. Git vs other version control systems
1. Key concepts and terminology
1. Adopting Git in your organization

---

## A Brief History of Version Control

1. **No Version Control** - Copy folders, rename files
1. **Local Version Control** - RCS (1982)
1. **Centralized Version Control** - CVS, Subversion, Perforce
1. **Distributed Version Control** - Git, Mercurial, Bazaar

---

## The Linux Kernel Problem

![the_linux_kernel_problem](svg/courses/git/git/01_introduction/the_linux_kernel_problem.svg)

---
## The Birth of Git (2005)

![bg left](jpg/courses/git/git/linus_torvalds.jpg)

**Linus Torvalds** created Git in April 2005

Requirements:
1. **Speed** - Must be fast for large projects
1. **Simple design** - Easy to understand and extend
1. **Strong support for non-linear development** - Thousands of parallel branches
1. **Fully distributed** - No single point of failure
1. **Able to handle large projects** - Like the Linux kernel

---

## Git Timeline

1. **April 3, 2005** - Development begins
1. **April 7, 2005** - Git becomes self-hosting
1. **April 18, 2005** - First merge of multiple branches
1. **April 29, 2005** - Performance matches BitKeeper
1. **June 16, 2005** - Linux 2.6.12 released using Git
1. **2008** - GitHub launches
1. **Today** - Most popular version control system

---

## Why "Git"?

Linus Torvalds quipped:

> "I'm an egotistical bastard, and I name all my projects after myself. First 'Linux', now 'git'."

**git** (British slang): an unpleasant or contemptible person

But also:
1. **Simple** - Three letter command
1. **Not taken** - Available as a command name
1. **Memorable** - Easy to remember

---

## Who is Using Git?

![who_is_using_git](svg/courses/git/git/01_introduction/who_is_using_git.svg)

---

## Git Market Share

According to Stack Overflow Developer Survey:

1. **Git** - 93.87%
1. **SVN** - 4.69%
1. **Mercurial** - 1.13%
1. **Others** - 0.31%

## Git has become the de-facto standard

---

## Git vs Centralized VCS

![git_vs_centralized_vcs](svg/courses/git/git/01_introduction/git_vs_centralized_vcs.svg)

---

## Key Differences from SVN

| Feature | SVN | Git |
|---------|-----|-----|
| **Architecture** | Centralized | Distributed |
| **Speed** | Slower (network) | Fast (local) |
| **Offline work** | Limited | Full capability |
| **Branching** | Expensive | Cheap and fast |
| **Storage** | Delta-based | Snapshot-based |
| **History** | Linear | DAG (Directed Acyclic Graph) |

---

## Git's Distributed Nature

1. **Every clone is a full repository**
    - Complete history
    - All branches and tags
    - Can work offline
1. **No single point of failure**
    - Any repository can be the "master"
    - Easy backup and recovery
1. **Flexible workflows**
    - Centralized workflow
    - Feature branch workflow
    - Gitflow workflow
    - Forking workflow

---

## Key Git Concepts

![key_git_concepts](svg/courses/git/git/01_introduction/key_git_concepts.svg)

---

## Git's Architecture

![git_s_architecture](svg/courses/git/git/01_introduction/git_s_architecture.svg)

---

## Understanding Git Areas

1. **Working Directory** - where you edit files
1. **Staging Area** - prepared changes
1. **Local Repository** - committed changes
1. **Remote Repository** - shared changes

---

## The Git Data Model

![the_git_data_model](svg/courses/git/git/01_introduction/the_git_data_model.svg)

---
## Snapshots, Not Differences

**SVN/CVS** - Stores differences (deltas)

---
## Snapshots, Not Differences

![snapshots_not_differences_1](svg/courses/git/git/01_introduction/snapshots_not_differences_1.svg)

---
## Snapshots, Not Differences

**Git** - Stores snapshots

---
## Snapshots, Not Differences

![snapshots_not_differences_2](svg/courses/git/git/01_introduction/snapshots_not_differences_2.svg)

---
## Snapshots, Not Differences

## If files don't change, Git just links to the previous identical file

---

## The Three States

![the_three_states](svg/courses/git/git/01_introduction/the_three_states.svg)

---

## Basic Git Workflow

1. **Modify** files in your working directory
1. **Stage** the changes you want to include in the next commit
1. **Commit** the staged changes to the repository

```bash
# Edit files
vim README.md

# Stage changes
git add README.md

# Commit changes
git commit -m "Update README"
```

---

## Why Use a Staging Area?

1. **Selective commits** - Choose exactly what to commit
1. **Review changes** - See what you're about to commit
1. **Split work** - Separate logical changes into multiple commits
1. **Clean history** - Create meaningful commit history

Example:
```bash
# You changed 3 files but want to commit only 2
git add file1.txt file2.txt
git commit -m "Feature A implementation"
# file3.txt remains uncommitted for a separate commit
```

---

## Git's Integrity

### Everything in Git is checksummed

1. Git uses **SHA-1** hash (moving to SHA-256)
1. 40-character hexadecimal string
1. Calculated based on contents + metadata
1. **Impossible to change anything without Git knowing**

Example SHA-1:
```misc
24b9da6552252987aa493b52f8696cd6d3b00373
```

### You'll see these everywhere in Git

---

## Git Generally Only Adds Data

1. **Almost all operations add data** to the Git database
1. **Very hard to lose data** once committed
1. **Can experiment without fear** of losing work

After committing:
1. Snapshot is safely stored
1. Can always revert to that state
1. History is preserved

### This makes Git forgiving and encourages experimentation

---

## Branches in Git

![branches_in_git](svg/courses/git/git/01_introduction/branches_in_git.svg)

---

## Why Branches Matter

1. **Parallel development** - Work on multiple features simultaneously
1. **Isolation** - Changes don't affect other branches
1. **Experimentation** - Try ideas without breaking main code
1. **Collaboration** - Multiple developers work independently
1. **Clean history** - Organize commits logically

### In Git, branches are just pointers to commits (41 bytes!)

---

## Git vs GitHub/GitLab/Bitbucket

**Git** is the version control system:
1. Command-line tool
1. Manages repositories locally
1. Free and open source

**GitHub/GitLab/Bitbucket** are hosting platforms:
1. Store repositories online
1. Add collaboration features
1. Provide web interface
1. Issue tracking, CI/CD, wikis

*You can use Git without any hosting platform!*

---

## Common Misconceptions

❌ **"Git is GitHub"**
✅ Git is the tool, GitHub is a hosting service

❌ **"Git is only for code"**
✅ Git can version any files (docs, configs, data)

❌ **"Git is too complex"**
✅ Daily use requires ~10 commands

❌ **"Branches are scary"**
✅ Branches are Git's superpower

---

## When to Use Git

**Perfect for:**
1. Source code (any language)
1. Configuration files
1. Documentation (Markdown, LaTeX)
1. Small data files
1. Scripts and automation

**Not ideal for:**
1. Large binary files (videos, images)
1. Generated files (build artifacts)
1. Sensitive data (passwords, keys)

---

## Git Hosting Options

1. **Cloud Platforms**
    - GitHub (Microsoft)
    - GitLab (SaaS or self-hosted)
    - Bitbucket (Atlassian)
    - Azure Repos
1. **Self-Hosted**
    - GitLab CE
    - Gitea
    - Gogs
1. **Simple Hosting**
    - SSH server
    - Network share
    - Even Dropbox (not recommended)

---

## Adopting Git in Your Organization

## Start Small

1. **Pilot project** - Start with one team
1. **Training** - Invest in proper training
1. **Documentation** - Create workflow guides
1. **Champions** - Identify Git advocates

---

## Migration Strategies

1. **Fresh start** - New projects use Git
1. **Gradual migration** - Move projects one by one
1. **Big bang** - Convert everything at once (risky!)

**Tools for migration:**
- `git svn` - Import from SVN
- `git cvsimport` - Import from CVS
- `git p4` - Import from Perforce

---

## Define Your Workflow

![define_your_workflow](svg/courses/git/git/01_introduction/define_your_workflow.svg)

---

## Common Challenges

1. **Learning curve**
    - Solution: Proper training and documentation
1. **Merge conflicts**
    - Solution: Communicate and merge frequently
1. **Large files**
    - Solution: Use Git LFS (Large File Storage)
1. **Messy history**
    - Solution: Establish commit message conventions

---

## Best Practices from Day One

1. **Write good commit messages**
    - What changed and why
    - Present tense, imperative mood
1. **Commit frequently**
    - Small, logical units
    - Easier to review and revert
1. **Use branches**
    - Keep `main` stable
    - Feature branches for development
1. **Pull before push**
    - Avoid conflicts
    - Stay synchronized

---

## Git Commit Messages

## Good ✅
```template
Add user authentication module

- Implement login/logout functionality
- Add password hashing with bcrypt
- Create session management
```

## Bad ❌
```template
fixed stuff
```
```template
asdfasdf
```
```template
WIP
```

---

## The Power of Git History

![the_power_of_git_history](svg/courses/git/git/01_introduction/the_power_of_git_history.svg)

---

## Security Considerations

1. **Never commit secrets**
    - Passwords, API keys, tokens
    - Use environment variables
    - Use `.gitignore` for sensitive files
1. **Sign commits** (optional)
    - GPG signatures
    - Verify authenticity
1. **Access control**
    - Who can push to main?
    - Protected branches
1. **Audit trail**
    - Git logs everything
    - Cannot delete history silently

---

## Git is More Than Version Control

1. **Collaboration platform**
    - Code reviews via pull requests
    - Discussions on commits
1. **Documentation system**
    - History tells the story
    - Commit messages explain decisions
1. **Backup solution**
    - Every clone is a full backup
    - Distributed = resilient
1. **Time machine**
    - Go back to any point
    - See what changed when

---

## Real-World Git Success Stories

- Linux Kernel
    - 30+ million lines of code
    - 1000+ contributors per release
    - 10+ commits per hour
- Windows
    - 3.5 million files
    - 300 GB repository
    - Moved from Source Depot to Git
- Android
    - 800+ Git repositories
    - Managed with repo tool
    - Millions of devices updated

---

## Summary

## What We Learned

1. ✅ Git's history and creation
1. ✅ Distributed vs centralized VCS
1. ✅ Git's core concepts (commits, trees, blobs)
1. ✅ The three states (working, staging, repository)
1. ✅ Why branches are powerful
1. ✅ Adopting Git in organizations
1. ✅ Best practices and workflows

---

## Key Takeaways

1. **Git is distributed** - Every clone is complete
1. **Git is fast** - Most operations are local
1. **Git is safe** - Very hard to lose committed data
1. **Git is flexible** - Multiple workflows possible
1. **Git is the standard** - 90%+ adoption rate

---

## What's Next?

In the upcoming sessions, we'll dive into:

1. **Git Basics** - Hands-on with essential commands
1. **Configuration** - Customizing Git for your needs
1. **Branching & Merging** - Advanced workflows
1. **Collaboration** - Working with remotes
1. **Under the Hood** - How Git really works
1. **Advanced Topics** - Rebase, cherry-pick, and more

---

## Resources

1. **Official Documentation**
    - https://git-scm.com/doc
1. **Pro Git Book** (free online)
    - https://git-scm.com/book
1. **Interactive Tutorials**
    - https://learngitbranching.js.org
1. **Git Cheat Sheet**
    - https://education.github.com/git-cheat-sheet-education.pdf

---

## Ready to Master Git?

![ready_to_master_git](svg/courses/git/git/01_introduction/ready_to_master_git.svg)
