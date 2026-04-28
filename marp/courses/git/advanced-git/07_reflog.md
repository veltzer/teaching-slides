---
tags:
  - tools:git
  - concepts:reflog
  - concepts:recovery
level: advanced
category: version-control
audience:
  - audiences:developers

---
# Reflog

---
## What This Chapter Covers

- What the reflog records and why it exists
- Reading reflog entries and HEAD@{N} syntax
- Recovering lost commits, branches, and stashes
- Reflog expiration and how to extend it
- Day-to-day uses beyond emergency recovery

---
## What Is the Reflog?

- A per-reference log of every position the reference has held
- Local-only — never pushed, never shared
- Records: when, what command, old SHA, new SHA
- HEAD has a reflog; every branch has its own reflog
- Your private "undo history" for Git operations

---
## Why Reflog Exists

- Git's data model never deletes commits, only references
- An "abandoned" commit is unreachable, not erased
- Without a reflog, you'd have no way to find unreachable commits
- Reflog gives you the SHA back so you can re-reference it
- Recovery is finding the SHA, not undeleting data

---
## Reflog Visualized

![reflog_recovery](svg/courses/git/advanced-git/07_reflog/reflog_recovery.svg)

---
## Reading the Reflog

```bash
git reflog
abc1234 HEAD@{0}: commit: Add new feature
def5678 HEAD@{1}: rebase: Fix typo
ghi9012 HEAD@{2}: checkout: moving from main to feature
jkl3456 HEAD@{3}: commit: Initial work
```

- Entries listed newest first
- `HEAD@{N}` — N positions ago
- Action verb shows what command moved HEAD
- Use this to spot when you went off course

---
## HEAD@{N} vs HEAD~N

- `HEAD~N` — N commits back in current branch's *parent chain*
- `HEAD@{N}` — N reflog entries back in *time*
- They are different and produce different SHAs after rebases
- Reflog is what *happened*; parent chain is what *is*
- Use `HEAD@{N}` to undo command sequences

---
## Time-Based References

```bash
git checkout main@{yesterday}
git diff HEAD@{1.hour.ago}
git log feature@{2.weeks.ago}..feature
```

- Reflog supports time-based queries
- "What did this branch look like yesterday?"
- Useful for "I broke something this morning, what was here last night?"
- Times are local-only — the reflog you query is your local one

---
## Recovering a Lost Commit

```bash
git reflog
# Spot the SHA you want
git checkout abc1234
# Or restore as a branch
git branch recovered abc1234
```

- A commit is "lost" when no branch or tag references it
- Reflog still holds the SHA
- Create a branch from it to make it permanent
- Garbage collection only removes commits the reflog has forgotten

---
## Recovering a Deleted Branch

```bash
git branch -d feature       # accidentally deleted
git reflog show HEAD        # or look at all reflog
git branch feature abc1234  # restore from the SHA
```

- Branch deletion removes a ref, not commits
- The reflog of HEAD shows when you switched off it
- Reflog of the branch itself may also be searchable: `git reflog show feature`
- Even after deletion, the per-branch reflog is in `.git/logs/refs/heads/feature` for a while

---
## Recovering a Bad Reset

```bash
git reset --hard abc1234       # oops, lost a commit
git reflog
# def5678 HEAD@{1}: reset: moving to abc1234
git reset --hard HEAD@{1}
```

- `reset --hard` moves the branch and discards working tree changes
- Reflog records the previous position
- One command to undo a destructive reset
- Test before celebrating — make sure you got the right entry

---
## Recovering From a Bad Rebase

```bash
git rebase main          # merged a mess
git reflog
# Look for "rebase (start): checkout main"
git reset --hard HEAD@{N}
```

- Rebase produces many reflog entries — one per replayed commit
- The "start" entry is your pre-rebase state
- `reset --hard` to that entry restores the original branch
- Better than re-rebasing from scratch when you know the prior state was correct

---
## Recovering a Lost Stash

```bash
git stash drop             # whoops
git fsck --no-reflogs --unreachable | grep commit
# Find dangling commits
git show <sha>
git stash apply <sha>
```

- Stashes have their own reflog: `git stash list`
- Once dropped, only `git fsck` and the reflog can find them
- `fsck` with `--unreachable` lists dangling objects
- Identify the stash by its commit message and contents

---
## Per-Branch Reflog

```bash
git reflog show feature
abc1234 feature@{0}: commit: Recent work
def5678 feature@{1}: branch: created
```

- Each branch has its own reflog
- Records every move of *that specific branch*
- Useful when investigating a single branch's evolution
- Stored in `.git/logs/refs/heads/<branch>`

---
## Reflog Expiration

- Reachable reflog entries expire after 90 days (default)
- Unreachable entries expire after 30 days
- Configurable via `gc.reflogExpire` and `gc.reflogExpireUnreachable`
- After expiration, garbage collection can remove the commits
- For recovery, time matters — act sooner rather than later

---
## Extending Reflog Lifetime

```bash
git config gc.reflogExpire "180 days"
git config gc.reflogExpireUnreachable "60 days"
```

- Set per-repo or globally
- Useful in repos where you do risky surgery
- Trade-off: slightly more disk usage, much more recovery window
- Some teams set "never" for critical refs to forbid expiration

---
## Pruning the Reflog

```bash
git reflog expire --expire=now --all
git gc --prune=now
```

- Forcibly clears reflog and garbage-collects unreachable
- Use to genuinely delete data (e.g., committed a secret)
- Combine with rewriting history first — see `git filter-branch` or `git filter-repo`
- After this, recovery is *not* possible — no more reflog

---
## Day-to-Day Reflog Use

- "What was I working on last Friday?" — `git reflog` and look
- "I forgot which commit I cherry-picked from" — reflog records the source
- "What branches have I been on this week?" — reflog of HEAD shows checkouts
- Treat reflog as your "command history" with semantic meaning
- It's not just for recovery; it's for orientation

---
## Reflog Is Local Only

- Pushing a branch does *not* push its reflog
- Pulling a branch does *not* fetch its reflog
- Each clone has its own reflog from the moment of cloning
- A teammate's destructive command never shows in your reflog
- Don't rely on reflog for cross-machine forensics

---
## Reflog and Bare Repos

- Bare repos (servers) typically don't keep reflogs by default
- Set `core.logAllRefUpdates=true` to enable
- Useful for hosted servers that want to recover from accidental force-pushes
- GitHub, GitLab keep their own server-side equivalents
- For self-hosted, configure deliberately

---
## Common Pitfalls

- Forgetting reflog exists during a panic — `git reflog` first, every time
- Letting too much time pass before recovery — expiration kicks in
- Using `HEAD~N` when you meant `HEAD@{N}`
- Running `git gc --prune=now` then realizing you needed the data
- Treating force-push as harmless because "we have reflog" — only locally

---
## Best Practices

- Make `git reflog` your first instinct after a destructive command
- Extend `gc.reflogExpire` if you do risky operations
- Document your team's recovery procedures
- Train new contributors to use reflog before panicking
- Pair reflog with backups for true safety nets

---
## Summary

- Reflog records every reference movement locally
- Recovery is finding a SHA, not undeleting data
- HEAD@{N} navigates by reflog position, not by parent chain
- Default expiration is 30/90 days — extend if needed
- Reflog is your private undo history — use it before panicking
