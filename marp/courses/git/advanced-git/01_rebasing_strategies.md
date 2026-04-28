---
tags:
  - tools:git
  - concepts:rebase
level: advanced
category: version-control
audience:
  - audiences:developers

---
# Rebasing Strategies

---
## What This Chapter Covers

- Rebase vs merge — what each actually does to history
- Interactive rebase: squash, reorder, edit, split, drop
- `--onto` for surgical history rewrites
- The golden rule of rebasing
- Recovering when a rebase goes wrong

---
## Merge: Preserves History As-It-Happened

- A merge commit records two parents
- The branch's commits stay where they were authored
- History is true: shows the actual ordering of work
- The cost: many merge commits clutter the log
- Cannot easily get a linear, readable history

---
## Rebase: Replays Commits On Top of Another Branch

- Picks each commit from your branch
- Replays it on top of the target branch
- Each replayed commit is a new commit (different SHA)
- The original commits are abandoned
- The result is a linear history, as if you started from the target tip

---
## Rebase vs Merge Visualized

![rebase_vs_merge](svg/courses/git/advanced-git/01_rebasing_strategies/rebase_vs_merge.svg)

---
## When to Rebase

- Your local feature branch before opening a PR
- Keeping your topic branch up-to-date with main
- Cleaning up a messy commit series before review
- When your team's workflow values linear history

---
## When to Merge

- Integrating a long-lived branch where the merge point matters
- Preserving the historical fact that a feature was developed in parallel
- When the branch is shared and rewriting history would harm collaborators
- Release branches and hotfix integration

---
## Interactive Rebase: The Power Tool

- `git rebase -i HEAD~5` opens an editor with the last 5 commits
- Each line is one commit and an action
- Reorder lines, change actions, save and quit
- Git replays commits per your script
- Conflicts pause the rebase for resolution

---
## Interactive Rebase Actions

- `pick` — keep the commit as-is
- `reword` — keep but edit the commit message
- `edit` — pause to amend the commit (split, fix, etc.)
- `squash` — fold into the previous commit, combine messages
- `fixup` — fold into the previous commit, drop this message
- `drop` — remove the commit entirely

---
## Squashing: A Practical Example

```bash
git rebase -i HEAD~4
# pick   abc123 Add login form
# squash def456 Fix typo in login form
# squash ghi789 Adjust login form padding
# squash jkl012 Tweak login form colors
```

- Four messy commits become one clean commit
- The combined message is editable in the next step
- Result: reviewers see one logical change, not the journey

---
## Splitting a Commit

- Use `edit` action in interactive rebase
- Git pauses with the commit applied
- `git reset HEAD^` un-stages everything
- Stage and commit pieces separately
- `git rebase --continue` to resume

---
## Rebase Onto: Surgical Rewrites

- `git rebase --onto NEW_BASE OLD_BASE BRANCH`
- Take commits between OLD_BASE..BRANCH
- Replay them on top of NEW_BASE
- Use case: extracted feature branch from the wrong base
- Use case: dropping merged commits from a long-running branch

---
## Rebase Onto Example

```bash
# topic was branched from feature, but should sit on main
git rebase --onto main feature topic
```

- Result: topic now sits on main, no longer dependent on feature
- Critical when feature gets dropped or significantly rewritten
- The cleanest way to relocate a branch

---
## The Golden Rule of Rebasing

- Never rebase commits that exist outside your local repo
- Once pushed and pulled by others, those commits belong to history
- Rebasing them rewrites their identity — collaborators get conflicts
- Local cleanup before pushing is fine
- Public branches are immutable

---
## Force-Push After Rebase

- Rebasing changes commit SHAs
- A normal `git push` is rejected (non-fast-forward)
- `git push --force-with-lease` is the safer alternative
- It refuses to overwrite commits you have not seen
- Plain `--force` overwrites unconditionally — dangerous

---
## Rebasing Shared Branches

- If you must rebase a shared branch, coordinate first
- Tell collaborators before force-pushing
- They will need to reset their local copies
- Provide the new tip SHA so they can verify
- Better: use merge for branches with many contributors

---
## Recovering From a Bad Rebase

- The original commits are not deleted — only unreferenced
- `git reflog` shows every HEAD movement
- `git reset --hard HEAD@{5}` restores a previous state
- Reflog entries persist for 90 days by default
- A bad rebase is recoverable, not catastrophic

---
## Aborting an In-Progress Rebase

- During conflict resolution, you can bail out
- `git rebase --abort` returns to the pre-rebase state
- `git rebase --skip` drops the current commit and continues
- `git rebase --continue` proceeds after resolving conflicts
- Never edit files manually and run `--continue` without `git add`

---
## Auto-Squash for Fixup Commits

- Make a commit with `git commit --fixup=<sha>`
- The commit is named `fixup! <original message>`
- Run `git rebase -i --autosquash HEAD~N`
- Git automatically reorders fixup commits next to their target
- Ideal workflow: review feedback as fixup commits, autosquash before merge

---
## Rebase Strategy Options

- `--strategy=recursive` (default) — three-way merge per commit
- `--strategy-option=theirs` — favor incoming changes on conflict
- `--strategy-option=ours` — favor existing changes on conflict
- `--strategy=ours` — keep our tree entirely, ignore incoming
- Strategy options apply to every replayed commit

---
## Rebase With Merge Commits Preserved

- `git rebase --rebase-merges` (or `-r`)
- Preserves the topology of merge commits in your branch
- Useful when your branch itself contains merges from sub-features
- Without it, merges are flattened into linear commits
- Read the output carefully — the todo list shows the planned topology

---
## Common Rebase Mistakes

- Rebasing the wrong direction (rebase onto your branch by mistake)
- Force-pushing without `--force-with-lease`
- Resolving conflicts incorrectly and continuing without testing
- Squashing commits that should remain separate for bisect
- Rebasing a branch others have already based work on

---
## Summary

- Rebase rewrites history; merge preserves it
- Interactive rebase is your editing tool for local history
- `--onto` lets you relocate branches with precision
- Never rewrite public history without coordination
- Reflog is your safety net — a bad rebase is always recoverable
