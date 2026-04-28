---
tags:
  - tools:git
  - concepts:multi-repo
level: advanced
category: version-control
audience:
  - audiences:developers

---
# Subtrees and Submodules

---
## What This Chapter Covers

- The need for embedding one repo inside another
- Submodules: how they work, how they break
- Subtrees: how they differ, when they're cleaner
- Day-to-day workflows for both
- Choosing between them for a real project

---
## Why Embed Repos?

- Vendored third-party code that you patch locally
- A library you own, used by multiple projects
- A deployment configuration repo that lives alongside the app
- Sometimes a monorepo would be ideal — but you're not there
- Submodules and subtrees both solve this; very differently

---
## Submodule Mechanics

- A submodule is a *pointer* to a specific commit in another repo
- Stored in `.gitmodules` (URL, path) and as a special tree entry
- The outer repo records: "at this path, check out this SHA"
- Cloning the outer repo doesn't clone the inner — separate command
- Each submodule is a full clone with its own `.git`

---
## Submodule vs Subtree Visualized

![submodule_vs_subtree](svg/courses/git/advanced-git/05_subtrees_and_submodules/submodule_vs_subtree.svg)

---
## Adding a Submodule

```bash
git submodule add https://github.com/example/lib lib/example
git commit -m "add example library as submodule"
```

- Creates `.gitmodules` and the linked path
- The path is recorded as a "gitlink" — a tree entry pointing to a commit
- Other clones use `git submodule update --init`
- Or clone with `--recurse-submodules` from the start

---
## Updating a Submodule

```bash
cd lib/example
git fetch origin
git checkout v2.1.0
cd ..
git add lib/example
git commit -m "bump example to v2.1.0"
```

- Each submodule is a real repo: pull, checkout, commit there
- The outer repo only tracks the SHA — commit it after updating
- This separation is the source of most submodule confusion

---
## The Submodule Pitfall

- After pulling the outer repo, submodules don't auto-update
- Developer sees "modified: lib/example (new commits)" — and panics
- They commit the old SHA back, undoing your update
- Always run `git submodule update --recursive` after pull
- Or set `submodule.recurse=true` in config

---
## Submodule Update Modes

- `git submodule update --init` — initialize and check out the recorded SHA
- `git submodule update --remote` — pull the latest from the submodule's branch
- `--remote` is for "always use the latest" workflows
- Default mode pins exactly to the recorded SHA — what most teams want
- Mixing the two confuses team members — pick one and document it

---
## Removing a Submodule

```bash
git submodule deinit -f lib/example
git rm lib/example
rm -rf .git/modules/lib/example
git commit -m "remove example library"
```

- Three steps: deinit, remove from index, clean up the worktree
- Forgetting any step leaves orphan state
- Use a script if your team does this often

---
## Subtree Mechanics

- A subtree merges another repo's history into a subdirectory of yours
- No pointers, no special files — just regular commits
- Cloning the outer repo gets everything, no extra setup
- The subtree's history is part of the outer repo's history
- Pulling updates uses `git subtree pull`

---
## Adding a Subtree

```bash
git subtree add --prefix=lib/example \
    https://github.com/example/lib v2.1.0 --squash
```

- `--prefix` — destination directory inside your repo
- `--squash` — collapse the imported history into one commit
- Without `--squash`, every commit from the source becomes part of yours
- Most teams use `--squash` to avoid history bloat

---
## Pulling Subtree Updates

```bash
git subtree pull --prefix=lib/example \
    https://github.com/example/lib main --squash
```

- Fetches the upstream and merges new changes under the prefix
- Uses the merge machinery you already know
- Conflicts behave like any other merge conflict
- No special "submodule update" dance for collaborators

---
## Pushing Subtree Changes Back

```bash
git subtree push --prefix=lib/example \
    https://github.com/example/lib pr-branch
```

- Extracts subtree commits and pushes them to the source repo
- Useful when you fix a bug in the subtree and want it upstream
- Source repo sees real commits, not synthetic ones
- Slower than submodule equivalent — git rewalks history

---
## Submodules: When They Fit

- The inner repo evolves independently and you pin specific versions
- You contribute to the inner repo as a separate project
- The inner repo is large — you don't want every clone to fetch it
- You need explicit, audited version updates
- Strong organizational boundary between repos

---
## Subtrees: When They Fit

- You want clones to "just work" without extra commands
- The team finds submodules confusing
- The inner repo is small enough to live inside yours
- You rarely contribute upstream
- Onboarding speed matters more than version isolation

---
## Common Submodule Mistakes

- Forgetting `--recurse-submodules` on clone
- Forgetting `git submodule update` after pull
- Committing the outer repo with a "dirty" submodule pointer
- Pushing changes inside the submodule but not the pointer in the outer repo
- Branching strategies that don't account for submodule SHAs

---
## Common Subtree Mistakes

- Forgetting `--squash` and importing thousands of commits
- Mixing changes to your code with subtree imports in one commit
- Trying to use subtrees with binary files that don't merge well
- Pushing subtree changes upstream when conflicts exist
- Treating subtrees like submodules and over-thinking version pinning

---
## Submodule Tooling

- `git submodule foreach 'git pull'` — run a command in every submodule
- `git config diff.submodule log` — show submodule diffs as commit lists
- `git config status.submodulesummary 1` — show submodule changes in `git status`
- These flags make daily work much less painful
- Most submodule complaints come from missing this config

---
## A Hybrid Pattern

- Use submodules for large dependencies you pin (compilers, big libs)
- Use subtrees for small dependencies you patch frequently
- Document which is which and why in your repo
- Don't switch types lightly — history rewrites are involved
- Both can coexist in the same repo

---
## Migration Considerations

- Submodule to subtree: rewrite history is required to flatten
- Subtree to submodule: extract the path's history into a new repo
- Both migrations are disruptive — coordinate with the whole team
- Sometimes the right answer is "live with what you have"
- Reach for migration only when the pain is concrete

---
## Best Practices

- Document the choice and the workflow in the repo's README
- Add hooks that warn on inconsistent submodule states
- Pin submodule versions; don't track moving branches
- Use `--shallow-submodules` for CI to save bandwidth
- Test the clone-and-build flow regularly — it's where new contributors fail

---
## Summary

- Submodules: pointers to specific SHAs in independent repos
- Subtrees: actual content merged into a subdirectory
- Submodules need discipline; subtrees need disk space
- Both solve embedding — pick based on team and update cadence
- Document your choice — silent assumptions break collaborators
