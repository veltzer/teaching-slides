---
tags:
  - tools:git
  - concepts:cherry-pick
level: advanced
category: version-control
audience:
  - audiences:developers

---

# Cherry-Pick

---

## What This Chapter Covers

- What cherry-pick really does
- Picking a single commit, a range, and from any branch
- Conflict resolution during cherry-pick
- Use cases: hotfixes, backports, retrieving lost work
- When cherry-pick is the wrong tool

---

## What Is Cherry-Pick?

- Take an existing commit from anywhere
- Apply it as a new commit on the current branch
- The new commit has a different SHA from the original
- The change set is reproduced; the metadata is preserved
- It's a copy, not a move

---

## Basic Cherry-Pick

```bash
git checkout main
git cherry-pick abc1234
```

- Applies commit `abc1234` as a new commit on `main`
- New SHA, same diff, same author and message
- Working tree must be clean before cherry-picking

---

## Cherry-Pick a Range

- `git cherry-pick A..B` — picks commits *after* A through B
- `git cherry-pick A^..B` — includes A itself
- Each commit is applied in order as a separate commit
- Stops at the first conflict — resolve and continue
- Use `--no-commit` to apply without committing each one

---

## Cherry-Pick Visualized

![cherry_pick_flow](svg/courses/git/advanced-git/02_cherry_pick/cherry_pick_flow.svg)

---

## Cherry Pick Use Cases

![cherry_pick_uses](svg/courses/git/advanced-git/02_cherry_pick/cherry_pick_uses.svg)

---

## The Hotfix Use Case

- Bug discovered on `main`
- Fixed and merged into `main`
- Same bug exists on the active release branch
- Cherry-pick the fix commit onto the release branch
- The release ships without pulling in unrelated `main` work

---

## The Backport Use Case

- Active development is on `main`
- Older versions are maintained on `release/v1`, `release/v2`
- Critical fixes need to land on every supported branch
- Cherry-pick from main onto each release branch
- Some teams script this for predictable backports

---

## Recovering Lost Commits

- A branch was deleted, but commits are still in reflog
- `git reflog` finds the lost commit SHA
- Cherry-pick onto your current branch to recover it
- Faster than recreating the branch entirely
- Effective for "I deleted that branch, but I want one of its commits back"

---

## Cherry-Pick With Conflicts

- Cherry-pick stops mid-operation on conflict
- Resolve conflicts in the working tree
- `git add` the resolved files
- `git cherry-pick --continue` to commit and proceed
- `git cherry-pick --abort` to bail out entirely

---

## The -x Flag: Trace Back to the Source

```bash
git cherry-pick -x abc1234
```

- Adds a line to the commit message: `(cherry picked from commit abc1234)`
- Crucial for backports — tells reviewers where the fix came from
- Makes auditing easier across long-lived release branches
- Habit-forming: always use `-x` for cross-branch cherry-picks

---

## Cherry-Pick a Merge Commit

- Merge commits have multiple parents
- Cherry-pick needs to know which parent to diff against
- `git cherry-pick -m 1 <merge-sha>` — relative to first parent
- `-m 2` — relative to second parent (the merged-in branch)
- Usually `-m 1` for "pick what this merge introduced"

---

## Cherry-Pick Without Committing

```bash
git cherry-pick --no-commit A B C
```

- Applies all changes to the working tree and index
- Does not create commits
- You commit once at the end with your own message
- Useful when picking several commits that should become one

---

## The Empty Commit Trap

- Cherry-picking a commit whose change is already present produces an empty commit
- `git cherry-pick` errors out by default
- `--allow-empty` permits the empty commit
- `--keep-redundant-commits` keeps it without complaint
- Usually a sign that the cherry-pick wasn't needed

---

## When NOT to Cherry-Pick

- Long-running parallel branches that drift apart
- More than a handful of commits at once — use rebase or merge
- When the commit depends on others not being picked
- When the branches share so much that a real merge is cleaner
- Cherry-picking instead of forward-porting via merge creates duplicate-effort divergence

---

## Cherry-Pick vs Rebase --onto

- Cherry-pick: copies one or more commits, keeps both copies in history
- Rebase --onto: moves a series, the original copies are abandoned
- Cherry-pick when both source and destination keep their history
- Rebase --onto when you want to relocate a branch
- They overlap; pick the one that matches your intent

---

## Cherry-Pick With Strategy Options

- `git cherry-pick -X theirs <sha>` — favor incoming on conflict
- `git cherry-pick -X ours <sha>` — favor current on conflict
- Useful for recurring conflict patterns during bulk backports
- Verify the result — strategies don't always do what you expect
- Mostly used in scripted backport pipelines

---

## Tracking Cherry-Picks Over Time

- `git log --grep="cherry picked from"` — finds annotated cherry-picks
- `git cherry main feature` — shows commits in feature not in main
- `git cherry -v` — shows the full message
- Both help answer "is this fix already in that branch?"
- Build into release checklists for predictability

---

## Common Pitfalls

- Forgetting `-x` when backporting
- Picking a commit that depends on prerequisites you haven't picked
- Resolving conflicts incorrectly — the cherry-pick succeeds, the code is wrong
- Picking merge commits without `-m`
- Treating cherry-pick as a substitute for proper branch management

---

## Best Practices

- Always test after cherry-pick — conflicts can mask logic errors
- Use `-x` for any cross-branch pick
- Pick logical groups in order, not random isolated commits
- Document the picked SHAs in PR descriptions for backports
- For repeated backport patterns, automate with a script

---

## Summary

- Cherry-pick copies a commit from anywhere onto your branch
- Use it for hotfixes, backports, and recovering specific commits
- `-x` annotates the source for traceability
- Conflicts pause the operation — resolve, add, continue
- It's a precision tool — not a substitute for merge or rebase
