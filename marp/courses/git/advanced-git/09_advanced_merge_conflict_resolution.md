---
tags:
  - tools:git
  - concepts:merge
  - concepts:conflict-resolution
level: advanced
category: version-control
audience:
  - audiences:developers

---

# Advanced Merge Conflict Resolution

---

## What This Chapter Covers

- The three-way merge: what Git is actually computing
- Reading conflict markers, including diff3 style
- Strategy options that bias resolution
- Using merge tools effectively
- Rerere — Git remembers your resolutions

---

## The Three-Way Merge

- Two commits to combine: yours and theirs
- A common ancestor: the base
- Git compares both sides to the base
- Each side's changes are independent — apply both
- A "conflict" is when both sides changed the same lines

---

## Why Three-Way Beats Two-Way

- Two-way: "your file vs theirs" — no idea what changed
- Three-way: "what did each side change since the base?"
- Knowing the base lets Git auto-merge non-overlapping changes
- The base is the merge-base — the most recent common ancestor
- Choosing the right base is most of merge's intelligence

---

## Three-Way Merge Visualized

![three_way_merge](svg/courses/git/advanced-git/09_advanced_merge_conflict_resolution/three_way_merge.svg)

---

## Default Conflict Markers

```output
<<<<<<< HEAD
Our version of the line.
=======
Their version of the line.
>>>>>>> feature
```

- `<<<<<<< HEAD` to `=======` — what's currently in your branch
- `=======` to `>>>>>>>` — what's in the incoming branch
- Edit to the desired final state and remove all markers
- Save and `git add` to mark resolved

---

## diff3 Conflict Style

```bash
git config merge.conflictstyle diff3
```

```output
<<<<<<< HEAD
Our version
||||||| merged common ancestors
The original line
=======
Their version
>>>>>>> feature
```

- Adds the *base* between markers
- See what the common ancestor said
- Often makes resolution obvious — "the base is what we both started from"
- Strongly recommended: enable this globally

---

## Why diff3 Matters

- Default markers don't show *intent* — just the two outcomes
- With base, you can see what each side *changed*
- "Both sides removed the same line" — clear from base
- "Both sides edited but in different ways" — reconcile both edits
- Many "tricky" conflicts vanish with diff3

---

## Aborting and Restarting a Merge

- `git merge --abort` — restore pre-merge state
- `git merge --continue` — proceed after resolving
- Mid-merge, working tree is mixed; commit only when done
- `git status` shows what's resolved and what isn't
- Don't commit until all markers are gone

---

## Conflict Resolution Strategies

![conflict_strategies](svg/courses/git/advanced-git/09_advanced_merge_conflict_resolution/conflict_strategies.svg)

---

## Strategy Options: ours and theirs

```bash
git merge -X ours feature
git merge -X theirs feature
```

- `-X ours` — favor our side on conflict
- `-X theirs` — favor their side on conflict
- Auto-resolves only the conflict — non-conflicting changes still merged
- Use deliberately — silent loss of changes is the cost

---

## Strategy: ours (uppercase)

```bash
git merge -s ours feature
```

- The `-s` (strategy) is different from `-X` (option)
- `-s ours` — keep our entire tree, ignore feature's content
- Records the merge in history but keeps no incoming code
- Use to "merge but don't take the changes"
- Common for stale branches you don't want to revisit

---

## Configuring a Merge Tool

```bash
git config merge.tool meld
git config merge.tool kdiff3
git config merge.tool vimdiff
```

- Many GUI and TUI tools available: meld, kdiff3, p4merge, vimdiff
- `git mergetool` opens the configured tool per-conflicted-file
- Tool shows local, remote, base, and result panes
- Save and exit — git verifies the conflict is resolved

---

## Using git mergetool

- Run after a merge produces conflicts
- Iterates over conflicted files
- Backs up `.orig` files unless `mergetool.keepBackup=false`
- Modern tools highlight only the conflict regions
- Faster than hand-editing for complex multi-region conflicts

---

## Conflicts in Rebases

- Same machinery: three-way merge applied per replayed commit
- May see *the same* conflict multiple times if you rebase often
- Resolution applies to that one replay; the next one starts fresh
- `git rebase --continue` after each resolution
- This is where rerere becomes valuable

---

## Conflicts in Cherry-Pick

- Cherry-pick computes a three-way merge: source's parent, source's tree, your tree
- Same conflict markers, same resolution flow
- `git cherry-pick --continue` once resolved
- Strategy options work: `-X theirs`, `-X ours`
- For repeated patterns, write a small script

---

## Rerere: Reuse Recorded Resolution

```bash
git config rerere.enabled true
```

- Git records how you resolved each conflict
- Next time the same conflict appears, Git replays your resolution
- Auto-applies on identical conflict text
- Massive time saver during long rebases or sticky merges
- Free undo: `git rerere clear` to forget

---

## Rerere in Action

- First time: you resolve `<<<<<<< auth.py ... >>>>>>>` manually
- Second time: same conflict, Git auto-resolves, you confirm with `git add`
- Ten times: never see that conflict again
- Pair with diff3 for the best experience
- Critical for long-lived branches that rebase often

---

## When Rerere Misleads

- Rerere applies based on conflict *text*, not on intent
- If the right resolution depends on the surrounding code, rerere may be wrong
- Always inspect what rerere did — `git diff` the resolved file
- Clear rerere if you regret a recorded resolution
- It's a pattern matcher, not a thinker

---

## Renames and Conflicts

- Git tracks renames heuristically — same content, different path
- Renames + edits on both sides can produce surprising conflicts
- `git diff -M` and `git log --follow` help analyze
- Sometimes you must "merge" two files into one manually
- Rename conflicts are the trickiest — be deliberate

---

## Binary Conflicts

- Git can't text-merge binaries (images, PDFs)
- Both versions are presented; pick one with `git checkout --ours` or `--theirs`
- Or merge externally and `git add` the result
- Use `git lfs` for repos with many large binaries
- Avoid binaries in source — store generated assets elsewhere

---

## Resolving Conflicts in Bulk

- For trivial all-ours or all-theirs cases:
- `git checkout --ours -- path/` then `git add path/`
- `git checkout --theirs -- path/` similarly
- Useful when one side's changes are clearly to be discarded
- Always verify before committing

---

## Tools That Help

- `git diff --check` — find leftover conflict markers before commit
- A pre-commit hook can refuse commits with markers
- `git log --merge` — show commits that contributed to the conflict
- `git diff @{1}` — see what the merge changed since the previous state
- These tools shrink resolution time

---

## Common Pitfalls

- Committing with conflict markers still in the file
- Resolving "wrong side wins" without realizing
- Re-resolving the same conflict every rebase (turn on rerere)
- Using `--theirs` and accidentally meaning `--ours`
- Skipping the test run after resolution

---

## Best Practices

- Enable diff3 globally — `git config --global merge.conflictstyle diff3`
- Enable rerere — `git config --global rerere.enabled true`
- Run tests after every merge resolution
- Pair on tricky conflicts — two sets of eyes catch bad resolutions
- Keep merges small — the longer the divergence, the worse the conflict

---

## Summary

- Three-way merge uses a common ancestor for intent inference
- diff3 conflict style shows the base — much easier resolution
- Strategy options bias auto-resolution; mergetool drives a GUI
- Rerere remembers your resolutions and reapplies them
- Tooling and discipline turn conflict resolution from dread to routine
