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

<svg viewBox="0 0 600 300" xmlns="http://www.w3.org/2000/svg">
  <text x="150" y="30" text-anchor="middle" font-size="14" font-weight="bold">Before Rebase</text>
  <text x="450" y="30" text-anchor="middle" font-size="14" font-weight="bold">After Rebase</text>

  <!-- Before rebase -->
  <circle cx="50" cy="80" r="10" fill="#3498db"/>
  <text x="50" y="85" text-anchor="middle" fill="white" font-size="8">A</text>

  <circle cx="120" cy="80" r="10" fill="#e74c3c"/>
  <text x="120" y="85" text-anchor="middle" fill="white" font-size="8">B</text>

  <circle cx="190" cy="80" r="10" fill="#2ecc71"/>
  <text x="190" y="85" text-anchor="middle" fill="white" font-size="8">C</text>

  <circle cx="120" cy="140" r="10" fill="#f39c12"/>
  <text x="120" y="145" text-anchor="middle" fill="white" font-size="8">X</text>

  <circle cx="190" cy="140" r="10" fill="#9b59b6"/>
  <text x="190" y="145" text-anchor="middle" fill="white" font-size="8">Y</text>

  <!-- After rebase -->
  <circle cx="350" cy="80" r="10" fill="#3498db"/>
  <text x="350" y="85" text-anchor="middle" fill="white" font-size="8">A</text>

  <circle cx="420" cy="80" r="10" fill="#e74c3c"/>
  <text x="420" y="85" text-anchor="middle" fill="white" font-size="8">B</text>

  <circle cx="490" cy="80" r="10" fill="#2ecc71"/>
  <text x="490" y="85" text-anchor="middle" fill="white" font-size="8">C</text>

  <circle cx="560" cy="80" r="10" fill="#f39c12"/>
  <text x="560" y="85" text-anchor="middle" fill="white" font-size="8">X'</text>

  <circle cx="560" cy="140" r="10" fill="#9b59b6"/>
  <text x="560" y="145" text-anchor="middle" fill="white" font-size="8">Y'</text>

  <line x1="60" y1="80" x2="110" y2="80" stroke="#333"/>
  <line x1="130" y1="80" x2="180" y2="80" stroke="#333"/>
  <line x1="120" y1="90" x2="120" y2="130" stroke="#333"/>
  <line x1="130" y1="140" x2="180" y2="140" stroke="#333"/>

  <line x1="360" y1="80" x2="410" y2="80" stroke="#333"/>
  <line x1="430" y1="80" x2="480" y2="80" stroke="#333"/>
  <line x1="500" y1="80" x2="550" y2="80" stroke="#333"/>
  <line x1="560" y1="90" x2="560" y2="130" stroke="#333"/>

  <text x="120" y="110" text-anchor="middle" font-size="10">main</text>
  <text x="190" y="170" text-anchor="middle" font-size="10">feature</text>
  <text x="420" y="110" text-anchor="middle" font-size="10">main</text>
  <text x="560" y="170" text-anchor="middle" font-size="10">feature</text>
</svg>

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

```text
pick a1b2c3d Add user model
pick d4e5f6g Fix typo in user model
pick g7h8i9j Add validation to user model
pick j1k2l3m Fix validation bug
```

**After squash:**

```text
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

<svg viewBox="0 0 700 250" xmlns="http://www.w3.org/2000/svg">
  <text x="175" y="20" text-anchor="middle" font-size="14" font-weight="bold">Merge Workflow</text>
  <text x="525" y="20" text-anchor="middle" font-size="14" font-weight="bold">Rebase Workflow</text>

  <!-- Merge workflow -->
  <circle cx="50" cy="60" r="8" fill="#3498db"/>
  <circle cx="120" cy="60" r="8" fill="#e74c3c"/>
  <circle cx="190" cy="60" r="8" fill="#2ecc71"/>
  <circle cx="260" cy="60" r="8" fill="#f39c12"/>
  <circle cx="120" cy="120" r="8" fill="#9b59b6"/>
  <circle cx="190" cy="120" r="8" fill="#34495e"/>
  <circle cx="260" cy="120" r="8" fill="#e67e22"/>
  <circle cx="300" cy="90" r="8" fill="#95a5a6"/>

  <!-- Rebase workflow -->
  <circle cx="400" cy="60" r="8" fill="#3498db"/>
  <circle cx="470" cy="60" r="8" fill="#e74c3c"/>
  <circle cx="540" cy="60" r="8" fill="#2ecc71"/>
  <circle cx="610" cy="60" r="8" fill="#f39c12"/>
  <circle cx="610" cy="120" r="8" fill="#9b59b6"/>
  <circle cx="610" cy="180" r="8" fill="#34495e"/>

  <text x="175" y="200" text-anchor="middle" font-size="12">Complex, branched</text>
  <text x="525" y="200" text-anchor="middle" font-size="12">Simple, linear</text>
</svg>

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

<svg viewBox="0 0 600 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="250" y="20" width="100" height="30" fill="#3498db" rx="5"/>
  <text x="300" y="40" text-anchor="middle" fill="white" font-size="12">Need to integrate?</text>

  <rect x="100" y="100" width="120" height="40" fill="#e74c3c" rx="5"/>
  <text x="160" y="115" text-anchor="middle" fill="white" font-size="10">Private branch?</text>
  <text x="160" y="130" text-anchor="middle" fill="white" font-size="10">Clean history needed?</text>

  <rect x="380" y="100" width="120" height="40" fill="#2ecc71" rx="5"/>
  <text x="440" y="115" text-anchor="middle" fill="white" font-size="10">Shared branch?</text>
  <text x="440" y="130" text-anchor="middle" fill="white" font-size="10">Preserve context?</text>

  <rect x="50" y="200" width="60" height="25" fill="#9b59b6" rx="5"/>
  <text x="80" y="217" text-anchor="middle" fill="white" font-size="10">REBASE</text>

  <rect x="170" y="200" width="60" height="25" fill="#f39c12" rx="5"/>
  <text x="200" y="217" text-anchor="middle" fill="white" font-size="10">MERGE</text>

  <rect x="410" y="200" width="60" height="25" fill="#f39c12" rx="5"/>
  <text x="440" y="217" text-anchor="middle" fill="white" font-size="10">MERGE</text>

  <line x1="270" y1="50" x2="180" y2="100" stroke="#333" stroke-width="2"/>
  <line x1="330" y1="50" x2="420" y2="100" stroke="#333" stroke-width="2"/>
  <line x1="140" y1="140" x2="90" y2="200" stroke="#333" stroke-width="2"/>
  <line x1="180" y1="140" x2="210" y2="200" stroke="#333" stroke-width="2"/>
  <line x1="440" y1="140" x2="440" y2="200" stroke="#333" stroke-width="2"/>

  <text x="220" y="80" font-size="10">Yes</text>
  <text x="380" y="80" font-size="10">No</text>
  <text x="100" y="175" font-size="10">Yes</text>
  <text x="190" y="175" font-size="10">No</text>

  <text x="80" y="250" font-size="9">• Clean up commits</text>
  <text x="80" y="265" font-size="9">• Linear history</text>
  <text x="80" y="280" font-size="9">• Easy to follow</text>

  <text x="200" y="250" font-size="9">• Preserve context</text>
  <text x="200" y="265" font-size="9">• Safe collaboration</text>
  <text x="200" y="280" font-size="9">• No history rewriting</text>

  <text x="440" y="250" font-size="9">• Multiple contributors</text>
  <text x="440" y="265" font-size="9">• Complex features</text>
  <text x="440" y="280" font-size="9">• Audit requirements</text>
</svg>

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
