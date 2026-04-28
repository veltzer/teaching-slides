---
tags:
  - tools:git
  - concepts:worktree
level: advanced
category: version-control
audience:
  - audiences:developers

---
# Worktrees

---
## What This Chapter Covers

- The problem: needing two checkouts of one repo
- Worktree mechanics — one repo, many working trees
- Adding, listing, removing worktrees
- Detached HEAD worktrees and bare-repo worktrees
- Workflow patterns that worktrees enable

---
## The Problem

- You're deep in a feature branch
- Production has an emergency — fix it on main, now
- Stash, switch, fix, push, switch back, unstash — error-prone
- Or: clone the repo a second time — wastes disk and bandwidth
- Worktrees solve this elegantly

---
## What Is a Worktree?

- An additional working directory linked to your repo
- Each worktree has its own checked-out branch and working tree
- All worktrees share one `.git` (objects, refs, reflog)
- Each branch can only be checked out in one worktree at a time
- One repo, many simultaneous checkouts

---
## Worktrees Visualized

![worktree_layout](svg/courses/git/advanced-git/08_worktrees/worktree_layout.svg)

---
## Adding a Worktree

```bash
git worktree add ../hotfix-tree main
cd ../hotfix-tree
# now checked out on main, separate working tree
```

- Path is relative to current dir or absolute
- The branch is checked out fresh in the new directory
- Operations there don't affect your other tree
- Same repo metadata, separate filesystem

---
## Listing Worktrees

```bash
git worktree list
/home/me/repo                abc1234 [main]
/home/me/hotfix-tree         def5678 [hotfix]
/home/me/review-pr-42        ghi9012 [review/pr-42]
```

- Shows path, current SHA, and branch
- Run from any worktree — sees all of them
- Quick way to remember "what was I working on where?"

---
## Removing a Worktree

```bash
git worktree remove ../hotfix-tree
```

- Cleans up the working directory and the `worktrees/` metadata
- Refuses if the working tree has uncommitted changes
- `--force` to override
- Better: clean up via `git worktree prune` after manual rm

---
## Why Not Just Branch and Stash?

- Stash + branch switch loses focus on long-running operations
- Long compiles, dev servers, file watchers all reset
- Worktree keeps each branch's environment separate
- Switch between them with `cd`, not with `git`
- Workflows scale naturally to many parallel tasks

---
## Use Case: Long-Running Builds

- Branch A is in the middle of a 20-minute build
- Need to make a quick edit on branch B
- Open a new worktree on branch B; edit and commit
- Branch A's build keeps running
- No "kill it and restart" — context preserved on both

---
## Use Case: PR Review

```bash
git worktree add ../review-pr-42 origin/pr-42
cd ../review-pr-42
# build, run, test the PR's branch independently
```

- Reviewing means running the code, not just reading it
- A worktree gives you a clean environment to test
- No risk of polluting your own branch
- Delete the worktree when review is done

---
## Use Case: Comparing Builds

- Build branch A in `~/repo`
- Build branch B in `~/repo-other` (worktree)
- Run benchmarks on both side by side
- No flag-toggling, no time-multiplexing
- The cleanest way to compare two versions empirically

---
## Detached HEAD Worktrees

```bash
git worktree add ../inspect abc1234
```

- Provide a SHA or tag instead of a branch
- New worktree is on detached HEAD at that SHA
- Look at history without committing to a branch
- Commits there are unreferenced unless you create a branch

---
## The Branch Lock Rule

- A branch can be checked out in only one worktree
- If `feature` is in `~/repo`, you can't add a worktree on `feature` elsewhere
- `--force` overrides the lock — only do this knowingly
- Try to detach (`add ../tree --detach branch`) for read-only inspection
- Or check out a different branch and create a copy

---
## Bare Repos and Worktrees

- A bare repo has no working tree at all
- Common pattern: clone bare, then add worktrees per branch
- Each branch gets its own dedicated directory
- Some teams use this for production deployments
- Mental model shift: the repo is metadata, worktrees are the work

---
## Bare Repo + Worktree Pattern

```bash
git clone --bare https://example/repo repo.git
cd repo.git
git worktree add ../main main
git worktree add ../staging staging
git worktree add ../prod prod
```

- Three branches, three deploy targets
- Push to a branch — pull in its worktree to update
- Clean separation between repo metadata and deployments
- Avoids "wrong branch deployed" by construction

---
## Worktrees and Hooks

- Hooks live in the bare repo or main `.git/hooks/`
- All worktrees share the same hooks
- Server-side hooks fire once for all worktrees on push
- Client hooks fire from whichever worktree triggered them
- Configure once, applies everywhere

---
## Worktrees and Submodules

- Submodules per worktree are tricky
- By default, submodules are linked from the main `.git/modules/`
- Each worktree may need to update submodule SHAs independently
- Test before relying on it — edge cases exist
- Subtrees behave more cleanly across worktrees

---
## Worktree Pruning

- A removed directory still leaves metadata behind
- `git worktree prune` cleans up stale worktree records
- `git worktree list` shows them as `(prunable)`
- Run periodically if you delete worktrees by `rm -rf`
- Better: always use `git worktree remove`

---
## Performance Considerations

- Worktrees share the object database — no duplicate storage
- Disk use grows linearly with checked-out files, not history
- Operations across worktrees are generally fast
- Building in two worktrees can overlap CPU cleanly
- Lighter than two full clones; heavier than nothing

---
## Common Pitfalls

- Trying to check out a branch already in another worktree
- Forgetting which worktree you're in (`pwd` in your prompt helps)
- Removing a worktree directory by hand without `prune`
- Hooks that assume one worktree exists
- Tools that hardcode `.git` as a directory — worktrees use `.git` *files*

---
## Worktrees and IDEs

- Some IDEs index per project root — point each at its worktree
- Don't open the bare repo as a project — open the worktree
- Reload after creating a worktree if file watchers don't notice
- Most modern IDEs handle worktrees correctly
- One IDE window per worktree avoids confusion

---
## Best Practices

- Name worktree directories for the branch or task: `../feat-login`, `../hotfix-3.2`
- Remove worktrees you're done with — they're cheap, but they pile up
- Use a consistent parent directory: `~/work/<project>/<task>`
- Combine with shell aliases for fast switching
- Treat worktrees as "task workspaces"

---
## Summary

- Worktrees: many simultaneous checkouts of one repo
- Each worktree has its own branch and working tree
- A branch can be in only one worktree at a time
- Use them for hotfixes, PR review, parallel builds, deployments
- Cheap, fast, and they replace most stash-and-switch workflows
