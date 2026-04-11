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
# Stashing

---

## What We'll Cover

1. Why you would want stashing
1. Creating and naming stashes
1. Applying specific stashes
1. Deleting stashes
1. Advanced stashing techniques
1. Stash workflows and best practices

---

## Why Would You Want Stashing?

Stashing temporarily saves your work when you need a clean working directory:

**Common scenarios:**
- **Emergency branch switches:** Urgent hotfix needed
- **Pull requirements:** Can't pull with uncommitted changes
- **Experimental work:** Try different approach temporarily
- **Context switching:** Quick task interruption
- **Clean state needed:** For builds, tests, or deployments

**What stashing saves:**
- Modified tracked files
- Staged changes (optional)
- Untracked files (optional)
- Working directory state

```bash
# Scenario: Working on feature when urgent bug reported
git stash                    # Save current work
git checkout main            # Switch to main branch
git checkout -b hotfix       # Create hotfix branch
# Fix the bug
git checkout feature         # Return to feature work
git stash pop                # Restore saved work
```

---
## Understanding the Stash

Git stash is a stack-based temporary storage:

**Stash characteristics:**
- **Stack structure:** Last In, First Out (LIFO)
- **Temporary storage:** Not meant for long-term use
- **Local only:** Stashes are not shared via push/pull
- **Branch independent:** Can apply stash to any branch

---
## Understanding the Stash

![understanding_the_stash](svg/courses/git/git2/17_stashing/understanding_the_stash.svg)

---

## Creating Your First Stash

Basic stashing operations:

```bash
# Simple stash (saves tracked modified files)
git stash

# Stash with descriptive message
git stash save "Work in progress on user authentication"
git stash push -m "Debugging login issue"

# Stash including untracked files
git stash -u
git stash --include-untracked

# Stash including ignored files
git stash -a
git stash --all

# Stash only staged changes
git stash --staged
```

**What gets stashed:**
- **Default:** Modified tracked files
- **With -u:** + untracked files
- **With -a:** + ignored files
- **With --staged:** Only staged changes

---

## Viewing Your Stashes

List and examine stashed changes:

```bash
# List all stashes
git stash list

# Output example:
stash@{0}: WIP on feature-auth: a1b2c3d Add login form
stash@{1}: On main: d4e5f6g Debugging session timeout
stash@{2}: WIP on hotfix: g7h8i9j Emergency fix

# Show stash contents
git stash show                    # Show files changed in latest stash
git stash show stash@{1}         # Show specific stash
git stash show -p                # Show patch (actual changes)
git stash show -p stash@{2}      # Show patch for specific stash

# Detailed stash information
git show stash@{0}               # Full commit-like view
```

**Stash reference format:**
- `stash@{0}`: Latest stash
- `stash@{1}`: Second most recent
- `stash@{n}`: nth stash from top

---

## Applying Stashes

Restore stashed changes to working directory:

```bash
# Apply latest stash (keeps stash in stack)
git stash apply

# Apply specific stash
git stash apply stash@{2}

# Apply and remove from stack (pop)
git stash pop
git stash pop stash@{1}

# Apply stash to different branch
git checkout other-branch
git stash apply stash@{0}
```

**Apply vs Pop:**
- **apply:** Restores changes, keeps stash in stack
- **pop:** Restores changes, removes stash from stack
- **pop fails:** If conflicts occur, stash remains in stack

---

## Naming and Organizing Stashes

Create meaningful stash descriptions:

```bash
# Descriptive stash messages
git stash push -m "Incomplete refactoring of user service"
git stash save "Experimental UI changes - not ready"
git stash push -m "WIP: Optimizing database queries"

# Include branch info in message
git stash push -m "$(git branch --show-current): Debug output added"

# Stash specific files only
git stash push -m "Config changes only" -- config.yml settings.json
```

**Naming best practices:**
1. Include branch context
1. Describe what was being worked on
1. Note if experimental or temporary
1. Use consistent format across team
1. Include ticket/issue numbers if relevant

---

## Partial Stashing

Stash only specific changes:

```bash
# Interactive stashing (choose hunks)
git stash -p
git stash --patch

# Stash specific files
git stash push -- file1.py file2.js
git stash push -m "Database config" -- db/config.yml

# Stash everything except specific files
git stash push -- . ':!dont-stash-this.log'

# Stash only staged changes
git stash --staged

# Stash only unstaged changes
git stash --keep-index
```

**Selective stashing use cases:**
- Separate unrelated changes
- Keep some changes for testing
- Stash only completed parts
- Exclude configuration files

---

## Advanced Stash Operations

Sophisticated stash management:

```bash
# Create stash without changing working directory
git stash create "Custom stash message"
# Returns stash SHA, but doesn't save to stack

# Store specific commit as stash
STASH_SHA=$(git stash create "My custom stash")
git stash store -m "Custom stash" $STASH_SHA

# Branch from stash (applies stash to new branch)
git stash branch new-feature-branch stash@{0}

# Show stash as diff
git diff stash@{1}
git diff stash@{1}^1 stash@{1}      # Compare with parent

# Apply stash with different strategy
git checkout --merge stash@{0} -- conflicted-file.py
```

---

## Deleting Stashes

Clean up stash stack:

```bash
# Delete specific stash
git stash drop stash@{1}

# Delete latest stash
git stash drop

# Clear entire stash stack
git stash clear

# Delete all stashes except most recent
git stash list | tail -n +2 | cut -d: -f1 | xargs -n1 git stash drop
```

**When to delete stashes:**
- After successfully applying changes
- When stash is no longer needed
- Regular cleanup to avoid clutter
- Before major repository operations

**Warning:** Deleted stashes are difficult to recover

---

## Handling Stash Conflicts

Resolve conflicts when applying stashes:

```bash
# Conflict occurs during stash pop/apply
git stash pop
# Auto-merging file.py
# CONFLICT (content): Merge conflict in file.py

# View conflicted files
git status

# Resolve conflicts manually (edit files)
# Then mark as resolved
git add file.py

# Complete the stash application (only needed after pop)
# Pop automatically removes stash on successful resolution
```

**Conflict resolution strategies:**
1. Edit files to resolve conflicts
1. Use merge tools: `git mergetool`
1. Choose one version: `git checkout --theirs file.py`
1. Abort stash application: `git reset --hard` (before adding)

---

## Stash Workflows

Different approaches to using stashes:

**Quick context switching:**
```bash
# Interrupted workflow
git stash push -m "WIP: $(git branch --show-current)"
git checkout main
# Handle interruption
git checkout -
git stash pop
```

**Experimental changes:**
```bash
# Try different approach
git stash push -m "Current approach - backup"
# Make experimental changes
# If experiment fails:
git reset --hard HEAD
git stash pop
```

**Collaborative development:**
```bash
# Before pulling updates
git stash
git pull origin main
git stash pop
# Resolve any conflicts
```

---

## Stash Best Practices

Guidelines for effective stash usage:

**Naming conventions:**
```bash
# Include context and purpose
git stash push -m "BRANCH: PURPOSE - DETAILS"
git stash push -m "feature-auth: WIP - password validation incomplete"
git stash push -m "main: DEBUG - added console logs for investigation"
```

**Regular cleanup:**
```bash
# Weekly stash audit
git stash list
# Review old stashes
git stash show stash@{5}
# Delete if no longer needed
git stash drop stash@{5}
```

**Team coordination:**
- Document stash usage in workflows
- Agree on naming conventions
- Regular cleanup reminders
- Share stash management scripts

---

## Stash Automation

Automate common stash operations:

```bash
#!/bin/bash
# auto-stash.sh - Smart stashing script

BRANCH=$(git branch --show-current)
DIRTY=$(git status --porcelain)

if [ -n "$DIRTY" ]; then
    MESSAGE="$BRANCH: Auto-stash $(date '+%Y-%m-%d %H:%M')"
    git stash push -m "$MESSAGE"
    echo "Changes stashed: $MESSAGE"
else
    echo "Working directory clean, nothing to stash"
fi
```

**Git hooks with stashing:**
```bash
#!/bin/bash
# pre-checkout hook
if [ "$3" = "1" ]; then  # Branch switch
    if ! git diff --quiet; then
        git stash push -m "Auto-stash before checkout"
        echo "Uncommitted changes automatically stashed"
    fi
fi
```

---

## Stash Inspection and Analysis

Analyze stash contents:

```bash
# Comprehensive stash analysis
git stash list --oneline
git stash list --stat
git stash list --patch

# Compare stashes
git diff stash@{0} stash@{1}

# Find stashes affecting specific files
git stash list --grep="config"
git stash show stash@{0} --name-only | grep "config"

# Show stash creation dates
git stash list --date=iso

# Statistics about stash
echo "Total stashes: $(git stash list | wc -l)"
git stash list --format="%gd: %gs" | head -5
```

---

## Recovery and Troubleshooting

Handle stash-related issues:

**Accidentally dropped stash:**

```bash
# Find dropped stash in reflog
git fsck --unreachable | grep commit | cut -d' ' -f3 | \
xargs git log --merges --no-walk --grep=WIP

# Or check reflog directly
git log --graph --oneline --all $(git fsck --no-reflogs 2>/dev/null | \
awk '/dangling commit/ {print $3}')
```

**Stash won't apply:**

```bash
# Check what would conflict
git stash show -p stash@{0} | git apply --check

# Apply with different strategy
git stash show -p stash@{0} | git apply --3way

# Apply to clean state then resolve
git reset --hard HEAD
git stash apply stash@{0}
```

**Corrupted stash:**

```bash
# Verify stash integrity
git stash show stash@{0} >/dev/null 2>&1 && echo "OK" || echo "Corrupted"

# Manually recreate from stash commit
git show stash@{0}^2 > stash-content.patch
git apply stash-content.patch
```

---

## Integration with Development Tools

Stash integration in different environments:

**IDE integration:**
- VS Code: Git stash commands in command palette
- IntelliJ: VCS → Git → Stash Changes
- Vim: Fugitive plugin stash commands
- Emacs: Magit stash interface

**Shell integration:**

```bash
# Add to ~/.bashrc or ~/.zshrc
alias gst='git stash'
alias gsta='git stash apply'
alias gstp='git stash pop'
alias gstl='git stash list'
alias gsts='git stash show'

# Function for smart stashing
smart_stash() {
    if git diff --quiet; then
        echo "Nothing to stash"
    else
        git stash push -m "$1"
    fi
}
```

---

## Stash vs Other Git Features

Compare stashing with alternatives:

**Stash vs Commit:**

```bash
# Temporary save with stash
git stash push -m "WIP"

# vs. Temporary commit
git add .
git commit -m "WIP - temporary commit"
# Later: git reset --soft HEAD~1
```

**Stash vs Worktree:**

```bash
# Stash approach
git stash
git checkout other-branch
# work
git checkout original-branch
git stash pop

# vs. Worktree approach
git worktree add ../other-work other-branch
cd ../other-work
# work
cd ../original-work
```

---

## Performance and Limitations

Understanding stash constraints:

**Performance characteristics:**
- Fast for small changes
- Slower with many files or large files
- Stack operations are O(1)
- Searching stashes is O(n)

**Limitations:**
- Local only (not shared)
- Not suitable for long-term storage
- Can't stash merge conflicts
- Binary files stored inefficiently
- Limited to current repository

**Size considerations:**
```bash
# Check stash sizes
git stash list --format="%gd" | while read stash; do
    echo -n "$stash: "
    git cat-file -s "$stash" 2>/dev/null | numfmt --to=iec
done
```

---

## Lab Exercise: Mastering Git Stash

**Scenario:** Implement a comprehensive stashing workflow for a development team with multiple concurrent tasks and frequent context switching.

**Basic tasks:**
1. **Stash creation and management:**
   - Create stashes with meaningful names
   - Practice selective stashing (files, hunks)
   - Apply stashes to different branches

1. **Conflict resolution:**
   - Simulate stash application conflicts
   - Practice different resolution strategies
   - Handle complex merge scenarios

1. **Workflow integration:**
   - Implement stashing in daily workflows
   - Practice context switching patterns
   - Use stashing for experimental changes

**Advanced tasks:**
1. **Automation development:**
   - Create scripts for smart stashing
   - Implement Git hooks with stashing
   - Build stash management utilities

1. **Team coordination:**
   - Develop stashing conventions
   - Create cleanup procedures
   - Document best practices

**Deliverables:** Comprehensive stashing workflows, automation scripts, team guidelines, troubleshooting procedures, and integration documentation.

---

## Advanced Stash Techniques

Expert-level stashing operations:

**Stash manipulation:**

```bash
# Modify stash message
git stash drop stash@{0}
git stash store -m "New message" STASH_SHA

# Combine stashes
git stash apply stash@{1}
git stash apply stash@{2}
git stash drop stash@{1}
git stash drop stash@{1}  # Note: indices shift
git stash push -m "Combined stash"

# Split stash into multiple commits
git stash pop
git add -p  # Interactively stage parts
git commit -m "First part"
git add -p  # Stage more parts
git commit -m "Second part"
```

---

## Stash Security and Privacy

Security considerations with stashes:

**Sensitive data in stashes:**

```bash
# Check for sensitive patterns
git stash show -p | grep -E "(password|secret|key|token)"

# Review all stashes for sensitive data
git stash list --format="%gd" | while read stash; do
    echo "=== $stash ==="
    git stash show -p "$stash" | grep -E "(password|secret|key)"
done
```

**Best practices:**
1. Don't stash credentials or secrets
1. Review stash contents before sharing repositories
1. Regular stash audits for sensitive data
1. Use .gitignore for sensitive files
1. Clear stashes before repository transfers

---

## Summary: Effective Stash Management

**Key takeaways:**

1. **Use stashes appropriately:**
   - Temporary storage for work interruptions
   - Context switching between tasks
   - Experimental change management
   - Not for long-term storage

1. **Maintain good stash hygiene:**
   - Use descriptive names
   - Regular cleanup of old stashes
   - Don't let stash stack grow too large
   - Document stashing conventions

1. **Master the techniques:**
   - Selective stashing for precision
   - Conflict resolution strategies
   - Recovery from stash problems
   - Integration with daily workflows

1. **Consider alternatives:**
   - Commits for permanent saves
   - Worktrees for parallel work
   - Branches for experimental features
   - External backup for important work

**Remember:** Git stash is a powerful tool for managing temporary work and context switching. Used properly, it enables fluid development workflows and helps manage the complexity of modern software development. However, stashes are meant to be temporary - don't use them as a replacement for proper version control practices with commits and branches.
