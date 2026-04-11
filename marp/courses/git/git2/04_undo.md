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
# Undoing Things

---

## What We'll Cover

1. Why you should not rewrite history
1. When it's safe to rewrite history
1. Amending commits
1. Reset vs Revert
1. Interactive rebase
1. Cherry-picking changes
1. Restoring files
1. Recovering "lost" commits
1. Extreme undoing techniques

---

## The Golden Rule of Git

![the_golden_rule_of_git](svg/courses/git/git2/04_undo/the_golden_rule_of_git.svg)

---

## Why Not Rewrite Public History?

![why_not_rewrite_public_history](svg/courses/git/git2/04_undo/why_not_rewrite_public_history.svg)

---

## The Consequences of Rewriting

```bash
# Developer 1 rewrites and force pushes
git rebase -i HEAD~3
git push --force origin main

# Developer 2 tries to pull
git pull
# ERROR: Merge conflicts!

# Developer 3 tries to push new work
git push
# ERROR: Updates were rejected

# CI/CD pipeline
# ERROR: Referenced commit SHA no longer exists!
```

### The entire team stops to fix the mess

---

## Safe History Modification

```bash
# Safe: Local commits not pushed
git commit -m "typo"
git commit --amend -m "Fixed typo"  # Safe!

# Safe: Your own feature branch
git push origin feature
# Work alone on it
git rebase main
git push --force-with-lease origin feature  # Safe with force-with-lease

# UNSAFE: Shared branches
git checkout main
git reset --hard HEAD~3
git push --force  # NEVER DO THIS!
```

### Use `--force-with-lease` instead of `--force` for safety

---

## Force vs Force-Lease

![force_vs_force_lease](svg/courses/git/git2/04_undo/force_vs_force_lease.svg)

---

## Amending the Last Commit

```bash
# Fix commit message only
git commit --amend -m "Better message"

# Add forgotten file to last commit
git add forgotten_file.txt
git commit --amend --no-edit

# Change author
git commit --amend --author="Name <email@example.com>"

# Interactive amend (opens editor)
git commit --amend

# Amend with different date
git commit --amend --date="2024-01-15 10:00:00"
```

---

## Amend Workflow

![amend_workflow](svg/courses/git/git2/04_undo/amend_workflow.svg)

---

## Common Amend Scenarios

```bash
# Scenario 1: Forgot to add a file
git commit -m "Add new feature"
# Oops! Forgot config.json
git add config.json
git commit --amend --no-edit

# Scenario 2: Wrong commit message
git commit -m "Fix bug in login"
# Actually fixed registration
git commit --amend -m "Fix bug in registration"

# Scenario 3: Need to remove a file
git commit -m "Update dependencies"
# Accidentally included debug.log
git rm debug.log
git commit --amend --no-edit
```

---

## Reset: Three Modes

![reset_three_modes](svg/courses/git/git2/04_undo/reset_three_modes.svg)

---

## Understanding Reset Modes

```bash
# Starting point: 3 commits, modified file
A -- B -- C (HEAD)
         Working: file.txt (modified)
         Staged: file.txt

# git reset --soft HEAD~1
A -- B (HEAD)
     C's changes are staged
     Working: file.txt (still modified)

# git reset --mixed HEAD~1  (or just git reset HEAD~1)
A -- B (HEAD)
     C's changes are in working directory
     Working: file.txt (modified + C's changes)

# git reset --hard HEAD~1
A -- B (HEAD)
     C is gone
     Working: clean (changes LOST!)
```

---

## Reset Examples

```bash
# Undo last commit, keep changes staged
git reset --soft HEAD~1

# Undo last commit, unstage changes
git reset HEAD~1  # or --mixed

# Completely remove last 2 commits
git reset --hard HEAD~2

# Reset to specific commit
git reset --hard abc123

# Unstage specific file (mixed reset)
git reset HEAD file.txt

# Reset single file to previous version
git reset HEAD~1 -- file.txt
```

---

## Reset Use Cases

![reset_use_cases](svg/courses/git/git2/04_undo/reset_use_cases.svg)

---

## Reset vs Checkout vs Restore

| Command | Scope | Working Dir | Staging | HEAD |
|---------|-------|-------------|---------|------|
| `reset --soft` | Commit | No change | No change | Moves |
| `reset --mixed` | Commit | No change | Updates | Moves |
| `reset --hard` | Commit | Updates | Updates | Moves |
| `checkout` | Branch/Commit | Updates | No change | Moves |
| `restore` | File | Updates | Optional | No change |

### Modern Git prefers `restore` and `switch` over `checkout`

---

## Revert: The Safe Undo

```bash
# Revert creates a new commit that undoes changes
git revert HEAD      # Revert last commit
git revert HEAD~2    # Revert third-last commit
git revert abc123    # Revert specific commit

# Revert merge commit
git revert -m 1 merge_commit  # -m specifies parent

# Revert multiple commits
git revert HEAD~3..HEAD  # Reverts last 3 commits

# Revert without committing
git revert -n HEAD  # Stage the revert, don't commit
```

---

## How Revert Works

![how_revert_works](svg/courses/git/git2/04_undo/how_revert_works.svg)

---

## Reset vs Revert

![reset_vs_revert](svg/courses/git/git2/04_undo/reset_vs_revert.svg)

---

## Revert in Practice

```bash
# Scenario: Bad commit pushed to production
git log --oneline
# abc123 Fix critical bug
# def456 Add feature (BROKEN!)
# ghi789 Update docs

# Can't reset (others have pulled)
# Solution: Revert!
git revert def456

# Creates new commit
# jkl012 Revert "Add feature (BROKEN!)"
# abc123 Fix critical bug
# def456 Add feature (BROKEN!)
# ghi789 Update docs

# History preserved, change undone
```

---

## Reverting Merge Commits

![reverting_merge_commits](svg/courses/git/git2/04_undo/reverting_merge_commits.svg)

---

## Interactive Rebase Introduction

```bash
# Rebase last 3 commits interactively
git rebase -i HEAD~3

# Opens editor with:
pick abc123 First commit
pick def456 Second commit
pick ghi789 Third commit

# Commands available:
# p, pick = use commit
# r, reword = use commit, but edit message
# e, edit = use commit, but stop for amending
# s, squash = use commit, meld into previous
# f, fixup = like squash, but discard message
# x, exec = run command
# d, drop = remove commit
```

---

## Rebase Interactive Commands

![rebase_interactive_commands](svg/courses/git/git2/04_undo/rebase_interactive_commands.svg)

---

## Rebase Workflow: Squashing

![rebase_workflow_squashing](svg/courses/git/git2/04_undo/rebase_workflow_squashing.svg)

---

## First Half Summary

## What We've Learned So Far

1. ✅ The golden rule: Never rewrite public history
1. ✅ Safe vs unsafe history modification
1. ✅ Amending commits for quick fixes
1. ✅ Three reset modes and when to use each
1. ✅ Revert for safe public undoing
1. ✅ Interactive rebase basics

## Coming Up Next

1. Advanced rebase techniques
1. Cherry-picking specific commits
1. Recovering lost work
1. Extreme history rewriting

---

## Splitting Commits with Rebase

```bash
# Start interactive rebase
git rebase -i HEAD~2

# Mark commit to edit
# Change 'pick' to 'edit' for the commit to split

# When Git stops at that commit:
# Reset to uncommit but keep changes
git reset HEAD^

# Stage and commit first logical change
git add file1.txt
git commit -m "First logical change"

# Stage and commit second logical change
git add file2.txt
git commit -m "Second logical change"

# Continue rebase
git rebase --continue
```

---

## Reordering Commits

![reordering_commits](svg/courses/git/git2/04_undo/reordering_commits.svg)

---

## Rebase Conflicts

```bash
# During rebase, conflicts may occur
git rebase -i HEAD~3
# CONFLICT (content): Merge conflict in file.txt

# Fix the conflict in your editor
vim file.txt

# Stage the resolved file
git add file.txt

# Continue rebase
git rebase --continue

# Or abort if things go wrong
git rebase --abort

# Skip problematic commit
git rebase --skip
```

---

## Cherry-pick: Selective Changes

```bash
# Apply specific commit to current branch
git cherry-pick abc123

# Cherry-pick multiple commits
git cherry-pick abc123 def456

# Cherry-pick range
git cherry-pick abc123..def456

# Cherry-pick without committing
git cherry-pick -n abc123

# Cherry-pick with edit
git cherry-pick -e abc123

# Continue after conflict
git cherry-pick --continue

# Abort cherry-pick
git cherry-pick --abort
```

---

## Cherry-pick Use Cases

![cherry_pick_use_cases](svg/courses/git/git2/04_undo/cherry_pick_use_cases.svg)

---

## Cherry-pick with Conflicts

```bash
# Cherry-pick may cause conflicts
git cherry-pick abc123
# CONFLICT: Merge conflict in app.js

# Option 1: Resolve and continue
vim app.js  # Fix conflicts
git add app.js
git cherry-pick --continue

# Option 2: Abort
git cherry-pick --abort

# Option 3: Use theirs/ours
git checkout --theirs app.js  # Take their version
git checkout --ours app.js    # Keep our version
git add app.js
git cherry-pick --continue
```

---

## Cherry vs Cherry-pick

```bash
# See which commits are in branch2 but not branch1
git cherry branch1 branch2

# Output:
# + abc123 Commit in branch2 not in branch1
# - def456 Commit in branch2 already in branch1

# Find commits to cherry-pick
git log --left-right --graph --cherry-pick --oneline branch1...branch2

# Cherry-pick with original author info
git cherry-pick -x abc123  # Adds "(cherry picked from...)" to message

# Record cherry-pick origin
git cherry-pick --ff abc123  # Fast-forward if possible
```

---

## Restore Command (Git 2.23+)

```bash
# Restore file in working directory
git restore file.txt

# Restore file from specific commit
git restore --source HEAD~2 file.txt

# Restore staged file (unstage)
git restore --staged file.txt

# Restore both staged and working
git restore --staged --worktree file.txt

# Restore all files
git restore .

# Interactive restore
git restore -p file.txt
```

### `restore` is clearer than the old `checkout -- file`

---

## Restore vs Reset vs Checkout

![restore_vs_reset_vs_checkout](svg/courses/git/git2/04_undo/restore_vs_reset_vs_checkout.svg)

---

## The Reflog: Your Safety Net

```bash
# View reflog
git reflog
# or
git log -g

# Show specific ref's log
git reflog show main

# Reflog with dates
git reflog --date=relative

# Recover "lost" commit
git reflog
# Find the SHA you want
git checkout abc123
# or create branch from it
git checkout -b recovered-branch abc123

# Reset to previous state
git reset --hard HEAD@{2}
```

---

## Understanding Reflog

![understanding_reflog](svg/courses/git/git2/04_undo/understanding_reflog.svg)

---

## Reflog Recovery Examples

```bash
# Scenario 1: Accidental hard reset
git reset --hard HEAD~5  # Oops, too many!
git reflog               # Find previous state
git reset --hard HEAD@{1}  # Recovered!

# Scenario 2: Lost branch
git branch -D feature    # Deleted branch
git reflog               # Find last commit
git checkout -b feature HEAD@{3}  # Recreated!

# Scenario 3: Bad rebase
git rebase -i HEAD~10   # Messed up
git reflog              # Find pre-rebase state
git reset --hard HEAD@{5}  # Back to safety!
```

---

## Recovering Lost Commits

![recovering_lost_commits](svg/courses/git/git2/04_undo/recovering_lost_commits.svg)

---

## Finding Dangling Objects

```bash
# Find dangling commits
git fsck --lost-found

# Show dangling commits
git fsck --no-reflog | grep commit

# View a dangling commit
git show abc123

# Find specific lost content
git log --all --full-history -- "**/my-file.*"

# Search all objects for text
git grep "search text" $(git rev-list --all)

# Recover dangling blob
git fsck --lost-found
# Check .git/lost-found/other/
```

---

## Bisect: Finding Bad Commits

```bash
# Start bisect
git bisect start

# Mark current commit as bad
git bisect bad

# Mark known good commit
git bisect good v1.0

# Git checks out middle commit
# Test it, then mark:
git bisect good  # or
git bisect bad

# Continue until found
# Git finds first bad commit

# End bisect
git bisect reset

# Automated bisect
git bisect start HEAD v1.0
git bisect run npm test
```

---

## Bisect Visualization

![bisect_visualization](svg/courses/git/git2/04_undo/bisect_visualization.svg)

---

## Extreme: Filter-branch

```bash
# WARNING: Rewrites entire history!

# Remove file from all history
git filter-branch --tree-filter \
  'rm -f passwords.txt' HEAD

# Change email in all commits
git filter-branch --env-filter '
  if [ "$GIT_AUTHOR_EMAIL" = "old@email.com" ]; then
    export GIT_AUTHOR_EMAIL="new@email.com"
  fi
' HEAD

# Move directory to root in all commits
git filter-branch --subdirectory-filter src HEAD

# After filter-branch
git push --force-with-lease  # Force required!
```

### Consider `git filter-repo` (newer, faster alternative)

---

## BFG Repo Cleaner

```bash
# Faster alternative to filter-branch
# Install: brew install bfg (or download jar)

# Remove large files
bfg --strip-blobs-bigger-than 100M repo.git

# Remove passwords
bfg --replace-text passwords.txt repo.git

# Delete files
bfg --delete-files id_{dsa,rsa} repo.git

# Delete folders
bfg --delete-folders .git repo.git

# Clean up
cd repo.git
git reflog expire --expire=now --all
git gc --prune=now --aggressive
```

### Much faster than filter-branch for repository cleaning

---

## Rewriting Commit Messages in History

```bash
# Last commit
git commit --amend -m "New message"

# Older commits (interactive rebase)
git rebase -i HEAD~3
# Change 'pick' to 'reword' for commits to edit

# Filter-branch for all commits
git filter-branch --msg-filter \
  'sed "s/old text/new text/g"' HEAD

# Multiple commits non-interactively
GIT_SEQUENCE_EDITOR="sed -i 's/pick/reword/g'" \
  git rebase -i HEAD~3
```

---

## Cleaning Repository Size

![cleaning_repository_size](svg/courses/git/git2/04_undo/cleaning_repository_size.svg)

---

## Undo Strategies by Scenario

![undo_strategies_by_scenario](svg/courses/git/git2/04_undo/undo_strategies_by_scenario.svg)

---

## Best Practices for Undoing

1. **Think before you act** - Understand what each command does
1. **Use reflog as safety net** - Check reflog before panic
1. **Prefer revert for public commits** - Maintains history
1. **Test in a branch first** - Create a backup branch
1. **Communicate with team** - Before rewriting shared history
1. **Use --force-with-lease** - Safer than --force
1. **Keep backups** - Clone before dangerous operations
1. **Document your changes** - Explain why history was rewritten

---

## Common Pitfalls to Avoid

❌ **Force pushing to main**
```bash
git push --force origin main  # NEVER!
```

❌ **Resetting without checking**
```bash
git reset --hard  # Check git status first!
```

❌ **Rebasing public branches**
```bash
git checkout main
git rebase feature  # Don't rebase shared branches
```

❌ **Amending pushed commits**
```bash
git push
git commit --amend  # Too late!
```

---

## Recovery Checklist

![recovery_checklist](svg/courses/git/git2/04_undo/recovery_checklist.svg)

---

## Advanced Recovery Techniques

```bash
# Find deleted file in history
git log --all --full-history -- "**/deleted-file.txt"

# Show file content from specific commit
git show abc123:path/to/file.txt > recovered-file.txt

# Find commit that deleted a file
git log --diff-filter=D --summary | grep delete

# Recover file deleted in commit
git checkout abc123^ -- path/to/file.txt

# Find large files in history
git rev-list --objects --all | \
  git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' | \
  sort -k3 -n -r | head -20
```

---

## Emergency Recovery Commands

```bash
# EMERGENCY: Undo last action (ANY action)
git reset --hard HEAD@{1}

# EMERGENCY: Get back to clean state
git reset --hard origin/main
git clean -fd

# EMERGENCY: Abort ongoing operation
git merge --abort
git rebase --abort
git cherry-pick --abort
git revert --abort

# EMERGENCY: Stash everything
git stash --all  # Including untracked and ignored

# EMERGENCY: Create backup branch
git branch backup-$(date +%Y%m%d-%H%M%S)
```

---

## Summary

## What We Learned

1. ✅ The golden rule: Don't rewrite public history
1. ✅ Amending commits safely
1. ✅ Reset vs Revert strategies
1. ✅ Interactive rebase for history cleanup
1. ✅ Cherry-picking specific changes
1. ✅ Using reflog for recovery
1. ✅ Finding and recovering lost commits
1. ✅ Extreme history rewriting techniques
1. ✅ Bisect for finding bugs

---

## Key Takeaways

1. **Reflog is your friend** - Nothing is truly lost for 90 days
1. **Revert for public, reset for private** - Choose the right tool
1. **Interactive rebase is powerful** - Clean history before sharing
1. **Force-lease over force** - Safer forced pushes
1. **Think before rewriting** - Some actions can't be undone
1. **Communicate with your team** - Coordinate history changes
1. **Keep calm when things go wrong** - Git usually has a way to recover

---

## Quick Reference Card

| Problem | Local | Public |
|---------|-------|--------|
| Wrong message | `commit --amend` | `revert` + new commit |
| Bad commit | `reset` | `revert` |
| Multiple fixes | `rebase -i` | separate commits |
| Need specific change | `cherry-pick` | `cherry-pick` |
| Lost work | `reflog` | `reflog` |
| File in history | `filter-branch`/BFG | coordinate with team |

---

## Practice Exercises

1. Create commits and practice amending them
1. Use interactive rebase to squash commits
1. Cherry-pick a commit between branches
1. Recover a "lost" commit using reflog
1. Practice bisect to find a breaking change
1. Try different reset modes and observe effects
1. Clean up a messy history with rebase
1. Remove a large file from history with BFG

---

## Next Up: Remote Repositories

In the next session, we'll explore:

1. Working with remote repositories
1. Setting up and publishing repositories
1. Understanding repository structure
1. Working with multiple remotes
1. GitHub, GitLab, and other platforms
1. Collaboration workflows
1. Pull requests and code reviews

---

## Undoing Things Complete! 🎉

![undoing_things_complete](svg/courses/git/git2/04_undo/undoing_things_complete.svg)
