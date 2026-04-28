---
tags:
  - tools:git
  - concepts:debugging
level: advanced
category: version-control
audience:
  - audiences:developers

---
# Bisect

---
## What This Chapter Covers

- The binary search idea behind `git bisect`
- Manual bisect: start, good, bad, reset
- Automated bisect with `run`
- Writing test scripts that bisect can drive
- When bisect helps and when it doesn't

---
## The Problem Bisect Solves

- A bug exists today; the codebase worked fine some time ago
- Somewhere in between, a commit introduced the regression
- Reading every commit by hand is impractical
- Bisect finds the offending commit in O(log N) steps
- 1024 commits become 10 tests, not 1024

---
## How Binary Search Applies to Commits

- Mark a known-good commit and a known-bad commit
- Git checks out a commit halfway between them
- You test and label it good or bad
- Git narrows the range and picks the new midpoint
- Continue until exactly one commit is left — the culprit

---
## Bisect Visualized

![bisect_search](svg/courses/git/advanced-git/03_bisect/bisect_search.svg)

---
## Starting a Manual Bisect

```bash
git bisect start
git bisect bad                    # current HEAD has the bug
git bisect good v2.3.0            # this older release was fine
```

- Git checks out a commit roughly in the middle
- Working tree is set to that commit's state
- You then test and report

---
## Reporting Results

```bash
git bisect good        # this commit is fine, bug is later
git bisect bad         # this commit has the bug, look earlier
git bisect skip        # cannot test (e.g., build broken)
```

- After each report, git picks the next commit to test
- Git prints how many revisions remain and the current commit
- Continues until it identifies the first bad commit

---
## Skip: When You Cannot Test

- Sometimes the midpoint commit doesn't compile
- Sometimes the test infrastructure of that era is broken
- `git bisect skip` tells git to choose another commit nearby
- Multiple skips are allowed
- Final result may be a range if skipped commits cannot be ruled out

---
## Ending a Bisect

```bash
git bisect reset
```

- Restores HEAD to where you were before bisect started
- All bisect state is cleared
- Always run this when done — bisect leaves you on a detached HEAD
- `git bisect log` saves a record of the search

---
## Automated Bisect With Run

```bash
git bisect start HEAD v2.3.0
git bisect run ./test_for_bug.sh
```

- Bisect runs the script for each candidate commit
- Exit 0 — good
- Exit 1-124 or 126-127 — bad
- Exit 125 — skip this commit
- Exit 128+ — abort the bisect

---
## Writing a Bisect Script

```bash
#!/bin/bash
make >/dev/null 2>&1 || exit 125    # build failed: skip
./run_test || exit 1                 # test fails: bad
exit 0                               # test passes: good
```

- Build failures should produce exit 125 (skip), not 1 (bad)
- Otherwise build-broken commits pollute the result
- Keep the script in your repo — every bisect can use it

---
## Bisect Output: Reading the Result

```output
abc1234 is the first bad commit
commit abc1234
Author: ...
Date:   ...
    Refactor caching layer
```

- That's the commit that introduced the regression
- Read its diff carefully — fix is usually local
- Sometimes the "first bad" is an innocent merge commit; investigate its parents

---
## Using Bisect on a Subset

```bash
git bisect start HEAD v2.3.0 -- src/auth/
```

- Restrict the search to commits that touch a path
- Git skips commits that don't change anything in `src/auth/`
- Drastically narrows the search when you suspect a subsystem
- Useful for monorepos

---
## Bisecting Through Merges

- Bisect handles merge commits naturally
- A merge can be the "first bad" if conflict resolution introduced the bug
- Investigate the diff `git show -m <merge>` to see what the merge changed
- Don't dismiss merges — they are real commits with real changes

---
## Bisect Tips That Save Time

- Write the test script before starting bisect — half the work is reproducing the bug reliably
- Keep `git bisect log` output for the postmortem
- Re-run bisect with the same log via `git bisect replay`
- When the test is flaky, run it multiple times in the script
- A flaky test makes bisect lie

---
## Common Pitfalls

- Forgetting `git bisect reset` — leaves HEAD detached
- Reporting the wrong endpoint as "good" or "bad"
- Test script returns 1 when it meant to skip — wrong commit blamed
- Test that depends on outside state (DB schema, env vars) drifts during bisect
- Build environment differences between commits cause false positives

---
## Bisect vs Other Tools

- Bisect — finds the *first* commit that broke something
- `git log -p` — searches for keywords or patterns
- `git blame` — finds who last changed a specific line
- `git pickaxe` (`git log -S"text"`) — finds when a string appeared/disappeared
- Bisect is unique: it's the only tool that uses behavior, not text, as the predicate

---
## Bisect Beyond Bugs

- Find the commit that improved performance — bad means "fast", good means "slow"
- Find when a feature first worked — invert good/bad
- Find when test coverage dropped below a threshold
- Any binary signal can drive a bisect
- The script defines what "good" means for your search

---
## Bisect at Scale

- Works on long histories without slowing down
- Skip count grows with chaos in the history (build breakage)
- For very long ranges, `--first-parent` reduces the search to mainline merges
- For monorepos, restrict by path
- For huge repos, partial clone or sparse checkout helps each step

---
## Best Practices

- Reproduce the bug *before* starting bisect
- Always exit 125 from your script when build fails
- Keep test scripts small and deterministic
- Document the bisect result in the eventual fix's commit message
- Review the "first bad" commit before celebrating — sometimes it's misleading

---
## Summary

- Bisect performs binary search across commits
- Manual mode for ad-hoc debugging; automated for repeatability
- Exit codes drive the search: 0 good, 1 bad, 125 skip
- It's the most powerful regression-finder in Git
- Script the test, automate the search, save hours
