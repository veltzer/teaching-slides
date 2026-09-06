---
tags:
  - tools:git
  - concepts:version-control
level: advanced
category: version-control
audience:
  - audiences:developers
  - audiences:sysadmins
  - audiences:devops

---

# Understanding Revisions (gitrevisions)

---

## What We'll Cover

1. Various things Git understands as revisions
1. Different object types (branch, object, commit, tree, etc.)
1. Commit-ish vs Tree-ish concepts
1. Using `git rev-parse` to understand revisions
1. Advanced revision specifications
1. Practical applications in Git commands

---

## What Are Git Revisions?

Git revisions are ways to specify commits, trees, and other objects:

**Core concept:**
- Revisions are expressions that resolve to Git objects
- Used throughout Git commands to specify what to operate on
- Flexible syntax allows many ways to reference the same object
- Foundation for understanding Git's power and flexibility

**Common revision types:**
- **SHA hashes:** Direct object references
- **Branch names:** References to commit objects
- **Tag names:** References to commits or other objects
- **Relative references:** Based on other revisions
- **Date-based:** Commits from specific times

```bash
# All of these are valid revisions
git show a1b2c3d              # SHA hash
git show main                 # Branch name
git show HEAD                 # Special reference
git show HEAD~2               # Relative reference
git show main@{yesterday}     # Date-based reference
```

---

## Object Types in Git

Understanding what different revision expressions refer to:

**`<object>`:**
- Any Git object (blob, tree, commit, tag)
- Can be referenced by SHA hash
- Most general object reference

**`<commit>`:**
- Specifically refers to commit objects
- Has author, committer, message, tree pointer
- Most commonly used in Git operations

**`<tree>`:**
- Directory snapshots
- Contains file and subdirectory references
- Represents project state at specific time

**`<blob>`:**
- File contents
- Raw data without filename or metadata
- Content-addressable by hash

---

## Branch References: Example

Branch names are the most common revision type:

```bash
# Branch references
git show main              # Latest commit on main
git show feature-auth      # Latest commit on feature-auth
git show origin/main       # Latest commit from remote main

# Branch with spaces (use quotes)
git show "feature/user auth"

# Branch starting with dash (use double dash)
git show -- -feature-branch
```

**How branches work as revisions:**
- Branch name resolves to commit SHA
- Always points to latest commit on branch
- Updates when new commits added
- Stored in `.git/refs/heads/`

---

## Branch References

![branch_starting_with_dash_use_double_dash](svg/courses/git/git/14_revisions/branch_starting_with_dash_use_double_dash.svg)

---

## SHA Hash References

Direct object references using SHA hashes:

```bash
# Full SHA hash
git show a1b2c3d4e5f6789012345678901234567890abcd

# Abbreviated SHA (minimum 4 characters, typically 7+)
git show a1b2c3d
git show a1b2c3d4

# Let Git choose abbreviation length
git show --abbrev-commit a1b2c3d4e5f6789012345678901234567890abcd
```

**SHA hash characteristics:**
- Globally unique identifiers
- Can be abbreviated if unambiguous
- Git auto-detects minimum length needed
- More reliable than branch names (don't change)

**Finding SHA hashes:**

```bash
# Get SHA of current commit
git rev-parse HEAD

# Get SHA of branch
git rev-parse main

# Get full SHA from abbreviated
git rev-parse a1b2c3d
```

---

## Special References

Git provides special reference names:

**`HEAD`:**

```bash
git show HEAD              # Current commit
git show HEAD~1            # Previous commit
git show HEAD^             # First parent of current commit
```

**`ORIG_HEAD`:**

```bash
# Previous value of HEAD before risky operation
git show ORIG_HEAD         # Before merge, reset, etc.
```

**`FETCH_HEAD`:**

```bash
# Tip of last fetched branch
git show FETCH_HEAD        # After git fetch
```

**`MERGE_HEAD`:**

```bash
# Other branch being merged (during merge)
git show MERGE_HEAD        # During merge conflict resolution
```

---

## Relative References with Tilde (~)

Navigate commit ancestry with tilde notation:

```bash
# Tilde (~) means "first parent"
git show HEAD~1            # 1 commit before HEAD
git show HEAD~2            # 2 commits before HEAD
git show HEAD~10           # 10 commits before HEAD

# Same as using multiple tildes
git show HEAD~~            # Same as HEAD~2
git show HEAD~~~           # Same as HEAD~3

# Works with any revision
git show main~5            # 5 commits before main
git show v1.0.0~1         # 1 commit before tag v1.0.0
```

**Tilde behavior:**
- Always follows first parent
- Linear traversal through history
- Ignores merge commit complexity
- Most common relative reference

---

## Relative References with Caret (^): Example

Navigate merge commit parents with caret notation:

```bash
# Caret (^) means "parent"
git show HEAD^             # First parent of HEAD
git show HEAD^1            # Same as HEAD^ (first parent)
git show HEAD^2            # Second parent of HEAD (merge commits)

# Multiple carets
git show HEAD^^            # First parent of first parent
git show HEAD^^^           # Same as HEAD~3

# Combining caret and tilde
git show HEAD^2~3          # 3rd ancestor of 2nd parent
```

**Caret vs Tilde:**
- `^` selects which parent
- `~` selects how many generations back
- Important for merge commits with multiple parents

---

## Relative References with Caret (^)

![combining_caret_and_tilde](svg/courses/git/git/14_revisions/combining_caret_and_tilde.svg)

---

## Commit-ish vs Tree-ish

Understanding what different revisions can represent:

**Commit-ish objects:**
- Resolve to commit objects
- Examples: branch names, commit SHAs, tags pointing to commits
- Can be used where Git expects a commit

**Tree-ish objects:**
- Resolve to tree objects (directory snapshots)
- Examples: commit-ish objects, tree SHAs, commit:path
- Can be used where Git expects a tree

```bash
# Commit-ish examples
git log main              # Branch name
git log HEAD~2            # Relative reference
git log a1b2c3d           # Commit SHA

# Tree-ish examples
git ls-tree HEAD          # Commit's tree
git ls-tree HEAD^{tree}   # Explicit tree reference
git ls-tree HEAD:src/     # Subtree at path
```

---

## Using git rev-parse

`git rev-parse` resolves and validates revisions:

```bash
# Resolve revision to SHA
git rev-parse HEAD
git rev-parse main
git rev-parse HEAD~2

# Resolve multiple revisions
git rev-parse HEAD main feature-branch

# Resolve to different object types
git rev-parse HEAD^{commit}    # Force to commit object
git rev-parse HEAD^{tree}      # Get tree SHA
git rev-parse HEAD:README.md   # Get blob SHA

# Verify revision exists
git rev-parse --verify HEAD~10 >/dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "HEAD~10 exists"
fi
```

**rev-parse options:**
- `--short`: Abbreviated SHA output
- `--verify`: Exit with error if revision invalid
- `--symbolic`: Keep symbolic names when possible
- `--abbrev-ref`: Show abbreviated reference names

---

## Date-based References

Reference commits by date and time:

```bash
# Reflog-based date references
git show HEAD@{yesterday}
git show HEAD@{2.days.ago}
git show HEAD@{1.week.ago}
git show HEAD@{2023-10-15}

# Branch-specific date references
git show main@{yesterday}
git show feature@{1.hour.ago}

# ISO date format
git show 'HEAD@{2023-10-15 14:30:00}'

# Relative time expressions
git show 'HEAD@{3.hours.ago}'
git show 'HEAD@{2.weeks.2.days.ago}'
```

**Date format flexibility:**
- Various formats supported
- Timezone handling
- Reflog-based resolution
- Approximate matching

---

## Branch and Reflog References

Access reflog history:

```bash
# Reflog position references
git show HEAD@{0}          # Current position
git show HEAD@{1}          # Previous position
git show HEAD@{5}          # 5 positions back

# Branch reflog references
git show main@{3}          # 3rd reflog entry for main
git show feature@{yesterday}

# Show reflog
git reflog                 # Show HEAD reflog
git reflog main           # Show branch reflog

# Reflog with dates
git reflog --date=iso
git reflog --date=relative
```

**Reflog characteristics:**
- Local to each repository
- Records reference movements
- Limited retention (default 90 days)
- Essential for recovery operations

---

## Path-based References

Reference specific files or directories:

```bash
# File at specific revision
git show HEAD:README.md
git show v1.0.0:src/main.py
git show main~2:docs/

# Directory at specific revision
git ls-tree HEAD:src/
git show HEAD:src/utils/

# File history
git log -- path/to/file.txt
git log HEAD~5..HEAD -- *.py
```

**Path reference syntax:**
- `revision:path` for file/directory at revision
- `--` to separate revisions from paths
- Supports glob patterns
- Works with relative and absolute paths

---

## Range Specifications: Example

Specify ranges of commits:

```bash
# Two-dot range (commits reachable from B but not A)
git log A..B
git log main..feature
git log HEAD~5..HEAD

# Three-dot range (commits reachable from either but not both)
git log A...B
git log main...feature

# Multiple references
git log ^A B C            # Reachable from B or C but not A
git log B C --not A       # Same as above
```

**Range use cases:**
- Show changes between branches
- Find commits to merge
- Generate release notes
- Review pending changes

---

## Range Specifications

![multiple_references](svg/courses/git/git/14_revisions/multiple_references.svg)

---

## Tag References and Dereferencing

Work with different tag types:

```bash
# Tag references
git show v1.0.0            # Show tag (annotated) or commit (lightweight)

# Dereference tags to different object types
git show v1.0.0^{commit}   # Force to commit object
git show v1.0.0^{tree}     # Get tree from tag
git show v1.0.0^{tag}      # Show tag object itself

# Lightweight vs annotated tag handling
git rev-parse v1.0.0       # SHA of tag object (annotated) or commit (lightweight)
git rev-parse v1.0.0^{commit}  # Always get commit SHA
```

**Tag dereferencing:**
- Handles annotated vs lightweight differences
- Explicit object type specification
- Consistent behavior across tag types

---

## Complex Revision Expressions

Combine different revision types:

```bash
# Complex combinations
git show HEAD~2^2~3        # 3rd ancestor of 2nd parent of HEAD~2
git log main..HEAD~5^2     # Range with complex endpoint
git diff HEAD@{1.week.ago}..HEAD^2~1

# Conditional expressions
git show HEAD~2 2>/dev/null || echo "Commit doesn't exist"

# Multiple object types
git rev-parse HEAD^{commit} HEAD^{tree} HEAD:README.md
```

**Expression building blocks:**
- Base reference (branch, SHA, tag)
- Ancestry operators (~, ^)
- Date specifications (@{})
- Path specifications (:)
- Object type forcing (^{type})

---

## Revision Validation

Check if revisions are valid:

```bash
# Test if revision exists
if git rev-parse --verify HEAD~10 >/dev/null 2>&1; then
    echo "HEAD~10 exists"
else
    echo "HEAD~10 does not exist"
fi

# Quiet verification
git rev-parse --verify --quiet HEAD~10

# Show what revision resolves to
git rev-parse --symbolic-full-name HEAD
git rev-parse --abbrev-ref HEAD
```

**Validation use cases:**
- Script safety checks
- User input validation
- Conditional operations
- Error prevention

---

## Practical Applications

Real-world usage of revision specifications:

**Release management:**

```bash
# Changes since last release
git log v1.0.0..HEAD --oneline

# Files changed between releases
git diff --name-only v1.0.0..v1.1.0

# Cherry-pick from specific point
git cherry-pick feature-branch~3..feature-branch~1
```

**Code review:**

```bash
# Review branch changes
git diff main...feature-branch

# Show branch commits
git log --oneline main..feature-branch

# Check if branch up to date
git merge-base --is-ancestor main feature-branch
```

**Bug hunting:**

```bash
# When was file last changed?
git log -1 --format="%H %ad" -- problematic-file.py

# What changed in specific commit?
git show a1b2c3d:src/main.py

# Find when bug was introduced
git bisect start HEAD v1.0.0
```

---

## Advanced Revision Syntax

Specialized revision syntax features:

**Object type specifiers:**

```bash
git show HEAD^{commit}     # Force commit object
git show HEAD^{tree}       # Get tree object
git show HEAD^{blob}       # Get blob object (if HEAD is blob)
git show HEAD^{}           # Dereference to non-tag object
```

**Upstream references:**

```bash
git show @{upstream}       # Upstream of current branch
git show @{u}              # Short form of upstream
git show main@{upstream}   # Upstream of specific branch
```

**Push destination:**

```bash
git show @{push}           # Where current branch would push
git show main@{push}       # Where specific branch would push
```

---

## Regular Expressions in Revisions

Pattern matching in revision specifications:

```bash
# Branch name patterns (with git for-each-ref)
git for-each-ref --format="%(refname:short)" "refs/heads/feature-*"

# Tag patterns
git tag -l "v1.*"
git tag -l "*beta*"

# Grep commit messages
git log --grep="^fix" --oneline
git log --grep="bug.*#[0-9]+" --oneline
```

**Pattern contexts:**
- Branch and tag listing
- Reference iteration
- Commit message searching
- Path matching

---

## Performance and Efficiency

Optimizing revision usage:

**Efficient practices:**

```bash
# Use SHA when possible (fastest)
git show a1b2c3d

# Avoid complex expressions in loops
# Bad:
for i in $(seq 1 100); do
    git show HEAD~$i
done

# Better:
git rev-list HEAD~100..HEAD | while read sha; do
    git show $sha
done
```

**Caching considerations:**
- Git caches resolution results
- Repeated complex expressions are optimized
- Rev-parse caches object lookups

---

## Debugging Revision Issues

Troubleshooting revision problems:

**Common issues:**

```bash
# Revision doesn't exist
git rev-parse --verify HEAD~20 2>/dev/null || echo "Not found"

# Ambiguous revision
git show a1b     # Might match multiple objects
git show a1b^{commit}  # Force specific type

# Wrong object type
git ls-tree HEAD:file.txt  # Error: file.txt is blob, not tree
git show HEAD:file.txt     # Correct: show blob content
```

**Debugging tools:**

```bash
# Show what revision means
git rev-parse --symbolic-full-name HEAD
git rev-parse HEAD

# Show object type
git cat-file -t a1b2c3d

# Show resolution steps
git log --oneline -1 HEAD~5  # Verify this exists first
```

---

## Revision Best Practices

Guidelines for effective revision usage:

**Readability:**

```bash
# Clear and descriptive
git diff main..feature-auth    # Good
git diff HEAD~5..HEAD^2~3     # Confusing

# Use meaningful names
git show release-candidate    # Good
git show a1b2c3d             # Less clear context
```

**Reliability:**

```bash
# Validate before use
git rev-parse --verify $REVISION >/dev/null 2>&1

# Use explicit forms for scripts
git show HEAD^{commit}        # Explicit
git show HEAD                 # Implicit
```

**Performance:**

```bash
# Cache frequently used resolutions
SHA=$(git rev-parse HEAD~10)
git show $SHA
git diff $SHA
```

---

## Integration with Scripting

Using revisions in automation:

```bash
#!/bin/bash
# Validate revision parameter
REVISION=${1:-HEAD}
if ! git rev-parse --verify "$REVISION" >/dev/null 2>&1; then
    echo "Error: Invalid revision '$REVISION'"
    exit 1
fi

# Get commit SHA
SHA=$(git rev-parse "$REVISION")
echo "Processing commit: $SHA"

# Get commit info
git show --format="Commit: %H%nAuthor: %an%nDate: %ad" --no-patch "$SHA"
```

**Scripting patterns:**
- Always validate input revisions
- Use rev-parse for normalization
- Handle edge cases gracefully
- Provide meaningful error messages

---

## Lab Exercise: Revision Mastery

**Scenario:** Master Git revision specifications through practical exercises covering all major syntax forms.

**Basic tasks:**
1. **Revision exploration:**
   - Use different ways to reference the same commit
   - Practice relative references (~, ^)
   - Work with date-based references

1. **Object type investigation:**
   - Distinguish commit-ish from tree-ish
   - Use rev-parse to understand resolutions
   - Explore object dereferencing

1. **Range operations:**
   - Create and analyze different range types
   - Compare two-dot vs three-dot ranges
   - Generate meaningful range queries

**Advanced tasks:**
1. **Complex expressions:**
   - Build multi-part revision expressions
   - Combine different reference types
   - Handle edge cases and validation

1. **Scripting integration:**
   - Create scripts using revision parameters
   - Implement proper validation and error handling
   - Build tools leveraging revision flexibility

**Deliverables:** Comprehensive revision reference guide, practical scripts demonstrating usage patterns, and troubleshooting documentation for common revision issues.

---

## Summary: Mastering Git Revisions

**Key takeaways:**

1. **Understand the fundamentals:**
   - Revisions are expressions that resolve to Git objects
   - Different syntax forms serve different purposes
   - Object types determine valid operations

1. **Master the syntax:**
   - Relative references for navigation
   - Date-based references for temporal queries
   - Range specifications for commit sets
   - Path-based references for specific files

1. **Use efficiently:**
   - Validate revisions in scripts
   - Choose appropriate forms for readability
   - Consider performance implications
   - Handle edge cases gracefully

1. **Apply practically:**
   - Integrate with daily Git workflows
   - Build automation using revision flexibility
   - Troubleshoot issues systematically
   - Document patterns for team use

**Remember:** Git revision syntax is incredibly powerful and flexible. Understanding these concepts deeply will make you much more effective at navigating Git history, building automation, and solving complex version control challenges. The investment in learning this syntax pays dividends in all aspects of Git usage.
