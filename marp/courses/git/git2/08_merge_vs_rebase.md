# Merge vs Rebase

---

## What We'll Cover

1. Understanding the fundamental differences
1. When to use merge vs rebase
1. The golden rule of rebasing
1. Practical examples and workflows
1. Team collaboration considerations

---

## The Fundamental Question

**Which should you choose?**

**Answer: Rebase** (in most cases)

But understanding *why* and *when* is crucial for effective `Git` workflows and team collaboration.

---

## What is Rebasing?

Rebasing rewrites commit history by moving commits to a new base:

```bash
# Rebase current branch onto main
git rebase main

# Interactive rebase to edit commits
git rebase -i HEAD~3
```

![interactive_rebase_to_edit_commits](/svg/courses/git/git2/08_merge_vs_rebase/interactive_rebase_to_edit_commits.svg)

---

## History Comparison: Merge vs Rebase

**Merge preserves context:**
- Shows when branches diverged and merged
- Maintains original commit timestamps
- Creates merge commits
- History reflects actual development process

**Rebase creates linear history:**
- Appears as if work was done sequentially
- Cleaner, easier to follow timeline
- No merge commits
- History optimized for understanding

---

## The Golden Rule of Rebasing

### Never rebase commits that have been pushed to a shared repository and others may have based work on

Why this rule exists:
- Rebasing changes commit SHA hashes
- Other developers' work becomes "orphaned"
- Causes confusion and potential data loss
- Breaks collaborative workflows

```bash
# Safe - private branch
git rebase main

# Dangerous - shared branch
git push origin feature
# Other developers pull and work on it
git rebase main  # DON'T DO THIS!
```

---

## When to Use Merge

1. **Integrating feature branches into main:**
    ```bash
    git checkout main
    git merge --no-ff feature-branch
    ```

1. **Preserving collaboration context:**
    - Multiple developers worked on the branch
    - Important to show parallel development
    - Feature has significant scope/complexity

1. **Following team policies:**
    - Organization requires merge commits
    - Compliance or audit requirements
    - Automated tooling expects merges

1. **Working with public/shared branches:**
    - Branch has been pushed and shared
    - Others have based work on the commits
    - Breaking the golden rule would cause problems

---

## When to Use Rebase

1. **Updating private feature branches:**
    ```bash
    git checkout feature-branch
    git rebase main
    ```

1. **Cleaning up commit history:**
    - Remove "work in progress" commits
    - Combine related changes
    - Fix commit messages
    - Create logical, atomic commits

1. **Maintaining linear project history:**
    - Easier code reviews
    - Simpler bisect operations
    - Cleaner release notes
    - Better understanding of project evolution

1. **Before sharing work:**
    - Polish commits before pushing
    - Organize work logically
    - Remove experimental commits

---

## Interactive Rebase Power

Interactive rebase lets you edit history:

```bash
git rebase -i HEAD~4
```

**Available actions:**
- `pick` - keep commit as-is
- `reword` - change commit message
- `edit` - modify commit content
- `squash` - combine with previous commit
- `fixup` - like squash, discard commit message
- `drop` - remove commit entirely

---

## Squashing Commits Example

**Before squash:**

```misc
pick a1b2c3d Add user model
pick d4e5f6g Fix typo in user model
pick g7h8i9j Add validation to user model
pick j1k2l3m Fix validation bug
```

**After squash:**

```misc
pick a1b2c3d Add user model
squash d4e5f6g Fix typo in user model
squash g7h8i9j Add validation to user model
squash j1k2l3m Fix validation bug
```

**Result:** Single commit with combined changes and new message.

---

## Rebase vs Merge: Team Workflow Impact

**Merge-based workflow:**
- Natural reflection of development process
- Preserves all historical context
- Can become cluttered with merge commits
- Harder to identify feature boundaries

**Rebase-based workflow:**
- Clean, linear history
- Easy to follow feature development
- Requires discipline and understanding
- Better for code archaeology

![rebase_vs_merge_team_workflow_impact](/svg/courses/git/git2/08_merge_vs_rebase/rebase_vs_merge_team_workflow_impact.svg)

---

## Handling Rebase Conflicts

When rebasing encounters conflicts:

```bash
git rebase main
# CONFLICT (content): Merge conflict in file.txt

# 1. Fix conflicts in files
# 2. Stage the fixed files
git add file.txt

# 3. Continue the rebase
git rebase --continue

# Or abort if needed
git rebase --abort
```

**Key differences from merge conflicts:**
- Each commit is applied individually
- May encounter multiple conflict points
- Can skip commits with `--skip`
- More granular conflict resolution

---

## Rebase Strategies

**Different rebase approaches:**

```bash
# Standard rebase
git rebase main

# Preserve merge commits
git rebase --preserve-merges main

# Rebase with strategy
git rebase -X theirs main

# Onto a specific commit
git rebase --onto main~2 main feature
```

**When to use each:**
- Standard: Most common case
- Preserve merges: Complex branch structures
- Strategy options: Automated conflict resolution
- Onto: Moving branches to different bases

---

## The Rebase Workflow

1. **Start with updated main:**
    ```bash
    git checkout main
    git pull origin main
    ```

1. **Rebase your feature branch:**
    ```bash
    git checkout feature-branch
    git rebase main
    ```

1. **Handle any conflicts:**
    ```bash
    # Fix conflicts, stage files, continue
    git add .
    git rebase --continue
    ```

1. **Force push if already shared:**
    ```bash
    git push --force-with-lease origin feature-branch
    ```

---

## Force Push Safety

When rebasing shared branches, use `--force-with-lease`:

```bash
# Dangerous - overwrites any changes
git push --force origin feature-branch

# Safer - checks for unexpected changes
git push --force-with-lease origin feature-branch
```

**What `--force-with-lease` does:**
- Checks if remote branch matches your expectation
- Fails if someone else pushed changes
- Prevents accidental overwrites
- Still requires careful coordination

---

## Team Policies and Agreements

**Establish clear guidelines:**

1. **Branch types and policies:**
    - `main/master`: merge only, no direct commits
    - Feature branches: rebase before merge
    - Release branches: merge only
    - Hotfix branches: specific policies

1. **Workflow agreements:**
    - Who can rebase shared branches?
    - When is force-pushing acceptable?
    - Code review requirements
    - Testing before integration

1. **Communication protocols:**
    - Notify team before rebasing shared work
    - Use descriptive commit messages
    - Document complex rebase operations
    - Coordinate during major refactoring

---

## Performance Considerations

**Merge advantages:**
- Fast operation, no history rewriting
- Preserves all commit metadata
- No risk of introducing bugs during rebase
- Works well with automated tools

**Rebase advantages:**
- Cleaner history for debugging
- Easier to identify when bugs were introduced
- Better for `git bisect` operations
- Simplified release notes and changelogs

**Choose based on:**
- Team size and collaboration patterns
- Project complexity and history importance
- Tooling and automation requirements
- Long-term maintenance needs

---

## Practical Decision Framework

![practical_decision_framework](/svg/courses/git/git2/08_merge_vs_rebase/practical_decision_framework.svg)

---

## Common Mistakes and How to Avoid Them

### Mistake 1: Rebasing public branches

```bash
# DON'T DO THIS
git checkout main
git rebase feature  # main is public!
```
**Solution:** Use merge for public branches

### Mistake 2: Not updating before rebasing

```bash
# Missing step
git rebase main  # main might be outdated
```
**Solution:** Always `git fetch` or `git pull` main first

### Mistake 3: Force pushing without checking

```bash
# Dangerous
git push --force
```
**Solution:** Use `--force-with-lease` and communicate with team

### Mistake 4: Rebasing too frequently
- Creates unnecessary churn
- Confuses team members
- Makes debugging harder

**Solution:** Rebase at logical points, not after every commit

---

## Next Steps

In the next half of this chapter, we'll cover:
- Advanced rebase techniques
- Handling complex scenarios
- Tooling and automation
- Real-world case studies
- Troubleshooting common issues
