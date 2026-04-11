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
# Merging Changes

---

## What We'll Cover

1. Understanding merges in depth
1. Fast-forward merges
1. Three-way merge mechanics
1. Merge strategies and options
1. Handling conflicts like a pro
1. Using merge tools effectively
1. Cherry-picking vs merging
1. Advanced merge techniques

---

## What is a Merge?

![what_is_a_merge](svg/courses/git/git2/07_merging/what_is_a_merge.svg)

---

## Fast-Forward Merge

![fast_forward_merge](svg/courses/git/git2/07_merging/fast_forward_merge.svg)

---

## Fast-Forward in Practice

```bash
# Check if fast-forward is possible
git merge-base main feature
git rev-parse main
# If merge-base equals main, FF is possible

# Perform fast-forward merge
git checkout main
git merge feature
# Updating abc123..def456
# Fast-forward

# Force fast-forward only (fail if not possible)
git merge --ff-only feature

# Prevent fast-forward (create merge commit)
git merge --no-ff feature

# Configure default behavior
git config merge.ff false  # Never fast-forward
git config merge.ff only   # Only fast-forward
```

---

## Why Prevent Fast-Forward?

![why_prevent_fast_forward](svg/courses/git/git2/07_merging/why_prevent_fast_forward.svg)

---

## Three-Way Merge Explained

![three_way_merge_explained](svg/courses/git/git2/07_merging/three_way_merge_explained.svg)

---

## How Git Decides What to Merge

```bash
# Git's merge decision tree:

# 1. Find merge base
git merge-base main feature

# 2. Compare each file:
# Base → Ours → Theirs → Action
# Same → Same → Same  → No change
# X    → Y    → X     → Take Y (ours changed)
# X    → X    → Y     → Take Y (theirs changed)
# X    → Y    → Z     → CONFLICT!
# X    → Y    → Y     → Take Y (same change)

# 3. For text files, compare line by line
# 4. For binary files, compare whole file
```

---

## Merge Strategies

```bash
# Default strategy (recursive/ort)
git merge feature

# Resolve strategy (older, simpler)
git merge -s resolve feature

# Ours strategy (ignore other branch entirely)
git merge -s ours feature

# Octopus (merge multiple branches)
git merge feature1 feature2 feature3

# Subtree (merge as subdirectory)
git merge -s subtree feature

# Custom strategy
git merge -s custom feature
```

---

## Strategy Options (-X)

![strategy_options_x](svg/courses/git/git2/07_merging/strategy_options_x.svg)

---

## Understanding Merge Conflicts

![understanding_merge_conflicts](svg/courses/git/git2/07_merging/understanding_merge_conflicts.svg)

---

## Conflict Markers

```bash
# Conflict markers in file:
<<<<<<< HEAD
function greet(name) {
  return `Hi ${name}`;
}
=======
function greet() {
  return "Bonjour";
}
>>>>>>> feature

# What they mean:
# <<<<<<< HEAD        - Start of your version
# =======             - Separator
# >>>>>>> feature     - End of their version

# After resolution (remove all markers):
function greet(name = "World") {
  return `Bonjour ${name}`;
}
```

---

## Resolving Conflicts Step by Step

![resolving_conflicts_step_by_step](svg/courses/git/git2/07_merging/resolving_conflicts_step_by_step.svg)

---

## Conflict Resolution Strategies

```bash
# Strategy 1: Accept theirs
git checkout --theirs file.txt
git add file.txt

# Strategy 2: Accept ours
git checkout --ours file.txt
git add file.txt

# Strategy 3: Use mergetool
git mergetool

# Strategy 4: Manual resolution
# Edit file, remove markers, save
git add file.txt

# Strategy 5: Postpone file
git rm file.txt  # Remove from merge
# Handle separately later
```

---

## Viewing Conflicts

```bash
# See conflict details
git diff
# Shows conflict markers

# See common ancestor version
git show :1:file.txt  # Base

# See our version
git show :2:file.txt  # Ours

# See their version
git show :3:file.txt  # Theirs

# List conflicted files
git diff --name-only --diff-filter=U

# Check if conflicts remain
git diff --check
```

---

## Using Merge Tools

External tools can simplify conflict resolution:

```bash
# Configure a merge tool
git config --global merge.tool vimdiff
git config --global merge.tool meld
git config --global merge.tool kdiff3

# Use the configured tool
git mergetool
```

**Popular merge tools:**
- `vimdiff` - Terminal-based, comes with vim
- `meld` - Visual diff tool for Linux
- `kdiff3` - Cross-platform GUI tool
- VS Code - Modern editor with excellent diff support

---

## Git Fetch vs Git Pull

Understanding the difference between `fetch` and `pull`:

**`git fetch`:**
- Downloads commits from remote
- Updates remote tracking branches
- Does NOT modify your working directory
- Safe operation, never causes conflicts

**`git pull`:**
- Combines `git fetch` + `git merge`
- Downloads AND integrates changes
- Can cause merge conflicts
- Modifies your working directory

```bash
# Safer approach
git fetch origin
git merge origin/main

# Equivalent to
git pull origin main
```

---
## Pull with Rebase

Use `--rebase` to maintain linear history:

```bash
# Instead of merge, rebase your changes
git pull --rebase origin main

# Configure as default
git config --global pull.rebase true
```

**Benefits:**
- Cleaner, linear history
- Easier to follow project timeline
- Reduces "merge commits" clutter
- Better for code reviews

---
## Pull with Rebase

![configure_as_default](svg/courses/git/git2/07_merging/configure_as_default.svg)

---

## Cherry Picking During Merge

Sometimes you need specific commits from another branch:

```bash
# Pick a specific commit
git cherry-pick <commit-hash>

# Pick multiple commits
git cherry-pick <commit1> <commit2>

# Pick a range of commits
git cherry-pick <start-commit>..<end-commit>
```

**Use cases:**
- Apply hotfixes to multiple branches
- Select features from experimental branches
- Backport changes to older versions
- Fix merge mistakes

---

## Merge Commit Messages

Customize merge commit messages for better history:

```bash
# Custom merge message
git merge feature-branch -m "Merge feature: Add user authentication"

# Edit merge message interactively
git merge feature-branch --edit

# No commit message (fast-forward only)
git merge feature-branch --ff-only
```

**Best practices:**
- Describe what the merge accomplishes
- Reference ticket/issue numbers
- Mention breaking changes
- Keep it concise but informative

---

## Aborting Merges

When merges go wrong, you can abort:

```bash
# Abort current merge
git merge --abort

# Reset to pre-merge state
git reset --hard HEAD

# Check merge status
git status
```

**When to abort:**
- Too many conflicts to resolve
- Wrong branch merged
- Merge was started accidentally
- Need to prepare better strategy

---

## Merge vs Rebase Decision Tree

![merge_vs_rebase_decision_tree](svg/courses/git/git2/07_merging/merge_vs_rebase_decision_tree.svg)

---

## Understanding Merge Base

The merge base is the common ancestor of branches being merged:

```bash
# Find merge base between branches
git merge-base main feature-branch

# Show merge base commit details
git show $(git merge-base main feature-branch)

# Find multiple merge bases (octopus merges)
git merge-base --all main feature-branch
```

**Why it matters:**
- Determines what changes to compare
- Affects conflict resolution
- Influences merge strategy selection
- Critical for understanding merge behavior

---

## Octopus Merges

Merging more than two branches simultaneously:

```bash
# Merge multiple branches at once
git merge branch1 branch2 branch3

# Only works if no conflicts exist
# Creates single merge commit with multiple parents
```

**Limitations:**
- No conflict resolution allowed
- All branches must merge cleanly
- Rarely used in practice
- Complex to understand and debug

**Better approach:**
- Merge branches one at a time
- Resolve conflicts individually
- Clearer history and attribution

---

## Merge Hooks

Automate merge-related tasks with `Git` hooks:

**`pre-merge-commit`:**
```bash
#!/bin/sh
# Run tests before creating merge commit
npm test || exit 1
```

**`post-merge`:**
```bash
#!/bin/sh
# Update dependencies after merge
npm install
bundle install
```

**Common uses:**
- Run automated tests
- Update dependencies
- Send notifications
- Generate documentation

---

## Advanced Merge Scenarios

**Merge with custom strategy:**
```bash
# Use specific strategy
git merge -s recursive -X theirs feature-branch
git merge -s octopus branch1 branch2 branch3
```

**Squash merge:**
```bash
# Combine all commits into one
git merge --squash feature-branch
git commit -m "Implement complete feature"
```

**No-commit merge:**
```bash
# Merge but don't commit
git merge --no-commit feature-branch
# Review changes, then commit manually
```

---

## Merge Performance Tips

1. **Keep branches small:**
    - Frequent integration reduces conflicts
    - Easier to review and test
    - Faster merge operations

1. **Use `.gitattributes` for merge strategies:**
    ```config
    *.generated merge=ours
    package-lock.json merge=union
    ```

1. **Clean up before merging:**
    ```bash
    git clean -fd
    git reset --hard HEAD
    ```

1. **Use merge commits strategically:**
    - Preserve feature branch context
    - Group related changes
    - Maintain release points

---

## Troubleshooting Common Merge Issues

**"Already up to date" message:**
- Target branch has no new commits
- All changes already integrated
- Check branch relationships with `git log --graph`

**"Automatic merge failed":**
- Conflicts exist in files
- Manual resolution required
- Use `git status` to identify conflicted files

**"fatal: refusing to merge unrelated histories":**
```bash
# Force merge of unrelated repositories
git merge --allow-unrelated-histories other-branch
```

**Large binary file conflicts:**
- Choose one version explicitly
- Use `.gitattributes` for binary files
- Consider `Git LFS` for large files

---

## Merge Best Practices Summary

1. **Before merging:**
    - Update your local main branch
    - Test your feature branch thoroughly
    - Review the changes you're merging

1. **During merging:**
    - Read conflict markers carefully
    - Test after resolving each conflict
    - Commit with descriptive messages

1. **After merging:**
    - Delete merged feature branches
    - Push the updated main branch
    - Verify the merge in your CI/CD system

1. **Team practices:**
    - Establish merge policies
    - Use pull requests for code review
    - Maintain a clean, readable history

---

## Lab Exercise: Complex Merge Scenario

**Setup:**
1. Create a repository with conflicting changes
1. Practice different merge strategies
1. Resolve conflicts using various tools
1. Compare merge vs rebase outcomes

**Tasks:**
1. Create merge conflicts intentionally
1. Use `git mergetool` to resolve conflicts
1. Abort and retry merges with different strategies
1. Practice cherry-picking specific commits

**Goal:** Build confidence in handling any merge situation you encounter in real projects.
