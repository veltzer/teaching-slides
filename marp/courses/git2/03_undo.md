# Undoing Things

---

## What We'll Cover

1. Why you should not rewrite history
1. When it's safe to rewrite history
1. Amending commits
1. Reset vs Revert
1. Interactive rebase
1. Cherry-picking changes
1. Restoring files
1. Recovering "lost" commits
1. Extreme undoing techniques

---

## The Golden Rule of Git

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="60" text-anchor="middle" font-size="28" font-weight="bold" fill="#D32F2F">The Golden Rule</text>
  <rect x="100" y="100" width="600" height="120" fill="#FFEBEE" stroke="#C62828" stroke-width="3" rx="10"/>
  <text x="400" y="150" text-anchor="middle" font-size="24" font-weight="bold">Never Rewrite Public History</text>
  <text x="400" y="190" text-anchor="middle" font-size="18">If it's been pushed and others might have it,</text>
  <text x="400" y="210" text-anchor="middle" font-size="18">don't change it!</text>
  <rect x="150" y="250" width="200" height="80" fill="#C8E6C9" stroke="#388E3C" stroke-width="2" rx="5"/>
  <text x="250" y="280" text-anchor="middle" font-size="14" font-weight="bold">Safe to Rewrite</text>
  <text x="250" y="305" text-anchor="middle" font-size="12">Local commits</text>
  <text x="250" y="320" text-anchor="middle" font-size="12">Feature branches (solo)</text>
  <rect x="450" y="250" width="200" height="80" fill="#FFCDD2" stroke="#D32F2F" stroke-width="2" rx="5"/>
  <text x="550" y="280" text-anchor="middle" font-size="14" font-weight="bold">Never Rewrite</text>
  <text x="550" y="305" text-anchor="middle" font-size="12">main/master branch</text>
  <text x="550" y="320" text-anchor="middle" font-size="12">Shared branches</text>
</svg>

---

## Why Not Rewrite Public History?

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="40" text-anchor="middle" font-size="24" font-weight="bold">The Chaos of Rewriting</text>
  <text x="150" y="80" text-anchor="middle" font-size="14" font-weight="bold">Before (Everyone Synchronized)</text>
  <circle cx="100" cy="120" r="20" fill="#4CAF50"/>
  <text x="100" y="125" text-anchor="middle" font-size="10" fill="white">A</text>
  <circle cx="150" cy="120" r="20" fill="#4CAF50"/>
  <text x="150" y="125" text-anchor="middle" font-size="10" fill="white">B</text>
  <circle cx="200" cy="120" r="20" fill="#4CAF50"/>
  <text x="200" y="125" text-anchor="middle" font-size="10" fill="white">C</text>
  <line x1="120" y1="120" x2="130" y2="120" stroke="#333" stroke-width="2"/>
  <line x1="170" y1="120" x2="180" y2="120" stroke="#333" stroke-width="2"/>
  <text x="100" y="155" font-size="11">Dev 1 ✓</text>
  <text x="150" y="155" font-size="11">Dev 2 ✓</text>
  <text x="200" y="155" font-size="11">Dev 3 ✓</text>
  <text x="150" y="200" text-anchor="middle" font-size="14" font-weight="bold">After Rewrite (Chaos!)</text>
  <circle cx="100" cy="240" r="20" fill="#4CAF50"/>
  <text x="100" y="245" text-anchor="middle" font-size="10" fill="white">A</text>
  <circle cx="150" cy="240" r="20" fill="#FF9800"/>
  <text x="150" y="245" text-anchor="middle" font-size="10" fill="white">B'</text>
  <circle cx="200" cy="240" r="20" fill="#FF9800"/>
  <text x="200" y="245" text-anchor="middle" font-size="10" fill="white">C'</text>
  <text x="150" y="275" font-size="11">Dev 1 (rewritten)</text>
  <circle cx="100" cy="320" r="20" fill="#4CAF50"/>
  <text x="100" y="325" text-anchor="middle" font-size="10" fill="white">A</text>
  <circle cx="150" cy="320" r="20" fill="#F44336"/>
  <text x="150" y="325" text-anchor="middle" font-size="10" fill="white">B</text>
  <circle cx="200" cy="320" r="20" fill="#F44336"/>
  <text x="200" y="325" text-anchor="middle" font-size="10" fill="white">C</text>
  <circle cx="250" cy="320" r="20" fill="#9C27B0"/>
  <text x="250" y="325" text-anchor="middle" font-size="10" fill="white">D</text>
  <text x="175" y="355" font-size="11">Dev 2 (conflicted!)</text>
  <rect x="400" y="100" width="350" height="250" fill="#FFF3E0" stroke="#F57C00" stroke-width="2" rx="5"/>
  <text x="575" y="130" text-anchor="middle" font-size="16" font-weight="bold">Problems Created:</text>
  <text x="420" y="160" font-size="13">• Duplicate commits (B and B')</text>
  <text x="420" y="185" font-size="13">• Merge conflicts everywhere</text>
  <text x="420" y="210" font-size="13">• Lost work (commit D orphaned)</text>
  <text x="420" y="235" font-size="13">• Confused team members</text>
  <text x="420" y="260" font-size="13">• Broken CI/CD pipelines</text>
  <text x="420" y="285" font-size="13">• History divergence</text>
  <text x="575" y="320" text-anchor="middle" font-size="14" font-style="italic">Everyone must force pull and resolve!</text>
</svg>

---

## The Consequences of Rewriting

```bash
# Developer 1 rewrites and force pushes
git rebase -i HEAD~3
git push --force origin main

# Developer 2 tries to pull
git pull
# ERROR: Merge conflicts!

# Developer 3 tries to push new work
git push
# ERROR: Updates were rejected

# CI/CD pipeline
# ERROR: Referenced commit SHA no longer exists!
```

### The entire team stops to fix the mess

---

## Safe History Modification

```bash
# Safe: Local commits not pushed
git commit -m "typo"
git commit --amend -m "Fixed typo"  # Safe!

# Safe: Your own feature branch
git push origin feature
# Work alone on it
git rebase main
git push --force-lease origin feature  # Safe with force-lease

# UNSAFE: Shared branches
git checkout main
git reset --hard HEAD~3
git push --force  # NEVER DO THIS!
```

### Use `--force-lease` instead of `--force` for safety

---

## Force vs Force-Lease

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="40" text-anchor="middle" font-size="24" font-weight="bold">Safer Force Pushing</text>
  <rect x="50" y="80" width="320" height="280" fill="#FFEBEE" stroke="#C62828" stroke-width="2" rx="5"/>
  <text x="210" y="115" text-anchor="middle" font-size="18" font-weight="bold">--force</text>
  <text x="210" y="145" text-anchor="middle" font-size="14">⚠️ Dangerous!</text>
  <text x="70" y="180" font-size="13">• Overwrites remote</text>
  <text x="70" y="205" font-size="13">• No safety checks</text>
  <text x="70" y="230" font-size="13">• Loses others' commits</text>
  <text x="70" y="255" font-size="13">• Can't be undone</text>
  <rect x="70" y="285" width="280" height="50" fill="#D32F2F" rx="5"/>
  <text x="210" y="315" text-anchor="middle" font-size="14" fill="white">Will destroy teammates' work!</text>
  <rect x="430" y="80" width="320" height="280" fill="#E8F5E9" stroke="#388E3C" stroke-width="2" rx="5"/>
  <text x="590" y="115" text-anchor="middle" font-size="18" font-weight="bold">--force-lease</text>
  <text x="590" y="145" text-anchor="middle" font-size="14">✓ Safer option</text>
  <text x="450" y="180" font-size="13">• Checks remote first</text>
  <text x="450" y="205" font-size="13">• Fails if others pushed</text>
  <text x="450" y="230" font-size="13">• Protects team's work</text>
  <text x="450" y="255" font-size="13">• Requires pull first</text>
  <rect x="450" y="285" width="280" height="50" fill="#4CAF50" rx="5"/>
  <text x="590" y="315" text-anchor="middle" font-size="14" fill="white">Fails safely if remote changed</text>
</svg>

---

## Amending the Last Commit

```bash
# Fix commit message only
git commit --amend -m "Better message"

# Add forgotten file to last commit
git add forgotten_file.txt
git commit --amend --no-edit

# Change author
git commit --amend --author="Name <email@example.com>"

# Interactive amend (opens editor)
git commit --amend

# Amend with different date
git commit --amend --date="2024-01-15 10:00:00"
```

---

## Amend Workflow

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="40" text-anchor="middle" font-size="24" font-weight="bold">Amending Commits</text>
  <text x="200" y="80" text-anchor="middle" font-size="14" font-weight="bold">Before Amend</text>
  <circle cx="100" cy="120" r="25" fill="#4CAF50"/>
  <text x="100" y="125" text-anchor="middle" font-size="12" fill="white">A</text>
  <circle cx="200" cy="120" r="25" fill="#4CAF50"/>
  <text x="200" y="125" text-anchor="middle" font-size="12" fill="white">B</text>
  <circle cx="300" cy="120" r="25" fill="#FF9800"/>
  <text x="300" y="125" text-anchor="middle" font-size="12" fill="white">C</text>
  <text x="300" y="155" text-anchor="middle" font-size="11" fill="#FF9800">Oops! Typo</text>
  <line x1="125" y1="120" x2="175" y2="120" stroke="#333" stroke-width="2"/>
  <line x1="225" y1="120" x2="275" y2="120" stroke="#333" stroke-width="2"/>
  <text x="200" y="210" text-anchor="middle" font-size="14" font-weight="bold">After Amend</text>
  <circle cx="100" cy="250" r="25" fill="#4CAF50"/>
  <text x="100" y="255" text-anchor="middle" font-size="12" fill="white">A</text>
  <circle cx="200" cy="250" r="25" fill="#4CAF50"/>
  <text x="200" y="255" text-anchor="middle" font-size="12" fill="white">B</text>
  <circle cx="300" cy="250" r="25" fill="#2196F3"/>
  <text x="300" y="255" text-anchor="middle" font-size="12" fill="white">C'</text>
  <text x="300" y="285" text-anchor="middle" font-size="11" fill="#2196F3">Fixed!</text>
  <line x1="125" y1="250" x2="175" y2="250" stroke="#333" stroke-width="2"/>
  <line x1="225" y1="250" x2="275" y2="250" stroke="#333" stroke-width="2"/>
  <rect x="450" y="100" width="300" height="200" fill="#E3F2FD" stroke="#1976D2" stroke-width="2" rx="5"/>
  <text x="600" y="130" text-anchor="middle" font-size="16" font-weight="bold">What Happens:</text>
  <text x="470" y="160" font-size="12">1. Creates new commit C'</text>
  <text x="470" y="185" font-size="12">2. Moves branch pointer to C'</text>
  <text x="470" y="210" font-size="12">3. Old C becomes unreachable</text>
  <text x="470" y="235" font-size="12">4. Same tree, new SHA</text>
  <text x="600" y="270" text-anchor="middle" font-size="13" font-style="italic">C still exists in reflog!</text>
</svg>

---

## Common Amend Scenarios

```bash
# Scenario 1: Forgot to add a file
git commit -m "Add new feature"
# Oops! Forgot config.json
git add config.json
git commit --amend --no-edit

# Scenario 2: Wrong commit message
git commit -m "Fix bug in login"
# Actually fixed registration
git commit --amend -m "Fix bug in registration"

# Scenario 3: Need to remove a file
git commit -m "Update dependencies"
# Accidentally included debug.log
git rm debug.log
git commit --amend --no-edit
```

---

## Reset: Three Modes

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="40" text-anchor="middle" font-size="24" font-weight="bold">Git Reset Modes</text>
  <rect x="50" y="80" width="220" height="280" fill="#E8F5E9" stroke="#388E3C" stroke-width="2" rx="5"/>
  <text x="160" y="115" text-anchor="middle" font-size="18" font-weight="bold">--soft</text>
  <circle cx="100" cy="150" r="20" fill="#4CAF50"/>
  <text x="100" y="155" text-anchor="middle" font-size="10" fill="white">HEAD</text>
  <text x="140" y="155" font-size="14">✓ Moves</text>
  <rect x="80" y="180" width="40" height="30" fill="#81C784"/>
  <text x="100" y="200" text-anchor="middle" font-size="10" fill="white">Index</text>
  <text x="140" y="195" font-size="14">✗ Unchanged</text>
  <rect x="80" y="220" width="40" height="30" fill="#81C784"/>
  <text x="100" y="240" text-anchor="middle" font-size="10" fill="white">Work</text>
  <text x="140" y="235" font-size="14">✗ Unchanged</text>
  <text x="160" y="280" text-anchor="middle" font-size="12" font-style="italic">Changes stay staged</text>
  <text x="160" y="300" text-anchor="middle" font-size="12">Use: Squash commits</text>
  <rect x="290" y="80" width="220" height="280" fill="#FFF3E0" stroke="#F57C00" stroke-width="2" rx="5"/>
  <text x="400" y="115" text-anchor="middle" font-size="18" font-weight="bold">--mixed (default)</text>
  <circle cx="340" cy="150" r="20" fill="#FF9800"/>
  <text x="340" y="155" text-anchor="middle" font-size="10" fill="white">HEAD</text>
  <text x="380" y="155" font-size="14">✓ Moves</text>
  <rect x="320" y="180" width="40" height="30" fill="#FFB74D"/>
  <text x="340" y="200" text-anchor="middle" font-size="10" fill="white">Index</text>
  <text x="380" y="195" font-size="14">✓ Updates</text>
  <rect x="320" y="220" width="40" height="30" fill="#81C784"/>
  <text x="340" y="240" text-anchor="middle" font-size="10" fill="white">Work</text>
  <text x="380" y="235" font-size="14">✗ Unchanged</text>
  <text x="400" y="280" text-anchor="middle" font-size="12" font-style="italic">Changes unstaged</text>
  <text x="400" y="300" text-anchor="middle" font-size="12">Use: Unstage files</text>
  <rect x="530" y="80" width="220" height="280" fill="#FFEBEE" stroke="#C62828" stroke-width="2" rx="5"/>
  <text x="640" y="115" text-anchor="middle" font-size="18" font-weight="bold">--hard</text>
  <circle cx="580" cy="150" r="20" fill="#F44336"/>
  <text x="580" y="155" text-anchor="middle" font-size="10" fill="white">HEAD</text>
  <text x="620" y="155" font-size="14">✓ Moves</text>
  <rect x="560" y="180" width="40" height="30" fill="#EF5350"/>
  <text x="580" y="200" text-anchor="middle" font-size="10" fill="white">Index</text>
  <text x="620" y="195" font-size="14">✓ Updates</text>
  <rect x="560" y="220" width="40" height="30" fill="#EF5350"/>
  <text x="580" y="240" text-anchor="middle" font-size="10" fill="white">Work</text>
  <text x="620" y="235" font-size="14">✓ Updates</text>
  <text x="640" y="280" text-anchor="middle" font-size="12" font-style="italic">⚠️ Loses changes!</text>
  <text x="640" y="300" text-anchor="middle" font-size="12">Use: Discard work</text>
</svg>

---

## Understanding Reset Modes

```bash
# Starting point: 3 commits, modified file
A -- B -- C (HEAD)
         Working: file.txt (modified)
         Staged: file.txt

# git reset --soft HEAD~1
A -- B (HEAD)
     C's changes are staged
     Working: file.txt (still modified)

# git reset --mixed HEAD~1  (or just git reset HEAD~1)
A -- B (HEAD)
     C's changes are in working directory
     Working: file.txt (modified + C's changes)

# git reset --hard HEAD~1
A -- B (HEAD)
     C is gone
     Working: clean (changes LOST!)
```

---

## Reset Examples

```bash
# Undo last commit, keep changes staged
git reset --soft HEAD~1

# Undo last commit, unstage changes
git reset HEAD~1  # or --mixed

# Completely remove last 2 commits
git reset --hard HEAD~2

# Reset to specific commit
git reset --hard abc123

# Unstage specific file (mixed reset)
git reset HEAD file.txt

# Reset single file to previous version
git reset HEAD~1 -- file.txt
```

---

## Reset Use Cases

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="40" text-anchor="middle" font-size="24" font-weight="bold">When to Use Each Reset Mode</text>
  <rect x="50" y="80" width="700" height="80" fill="#E8F5E9" stroke="#388E3C" stroke-width="2" rx="5"/>
  <text x="400" y="105" text-anchor="middle" font-size="16" font-weight="bold">--soft: "I want to redo my commit"</text>
  <text x="70" y="130" font-size="13">Use case: Made 3 commits but want to combine them into one</text>
  <text x="70" y="150" font-size="12" font-family="monospace">git reset --soft HEAD~3 && git commit -m "Feature complete"</text>
  <rect x="50" y="170" width="700" height="80" fill="#FFF3E0" stroke="#F57C00" stroke-width="2" rx="5"/>
  <text x="400" y="195" text-anchor="middle" font-size="16" font-weight="bold">--mixed: "I want to unstage everything"</text>
  <text x="70" y="220" font-size="13">Use case: Added wrong files to staging, want to start over</text>
  <text x="70" y="240" font-size="12" font-family="monospace">git reset HEAD  # Unstages all files</text>
  <rect x="50" y="260" width="700" height="80" fill="#FFEBEE" stroke="#C62828" stroke-width="2" rx="5"/>
  <text x="400" y="285" text-anchor="middle" font-size="16" font-weight="bold">--hard: "I want to throw everything away"</text>
  <text x="70" y="310" font-size="13">Use case: Experiment failed, go back to clean state</text>
  <text x="70" y="330" font-size="12" font-family="monospace">git reset --hard HEAD  # ⚠️ Loses all uncommitted work!</text>
</svg>

---

## Reset vs Checkout vs Restore

| Command | Scope | Working Dir | Staging | HEAD |
|---------|-------|-------------|---------|------|
| `reset --soft` | Commit | No change | No change | Moves |
| `reset --mixed` | Commit | No change | Updates | Moves |
| `reset --hard` | Commit | Updates | Updates | Moves |
| `checkout` | Branch/Commit | Updates | No change | Moves |
| `restore` | File | Updates | Optional | No change |

### Modern Git prefers `restore` and `switch` over `checkout`

---

## Revert: The Safe Undo

```bash
# Revert creates a new commit that undoes changes
git revert HEAD      # Revert last commit
git revert HEAD~2    # Revert third-last commit
git revert abc123    # Revert specific commit

# Revert merge commit
git revert -m 1 merge_commit  # -m specifies parent

# Revert multiple commits
git revert HEAD~3..HEAD  # Reverts last 3 commits

# Revert without committing
git revert -n HEAD  # Stage the revert, don't commit
```

---

## How Revert Works

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="40" text-anchor="middle" font-size="24" font-weight="bold">Revert Creates Inverse Commits</text>
  <rect x="100" y="80" width="600" height="100" fill="#E3F2FD" stroke="#1976D2" stroke-width="2" rx="5"/>
  <text x="400" y="110" text-anchor="middle" font-size="16" font-weight="bold">Original Commit</text>
  <text x="120" y="140" font-size="12" font-family="monospace">+ Added line 10</text>
  <text x="120" y="160" font-size="12" font-family="monospace">- Removed line 5</text>
  <rect x="100" y="200" width="600" height="100" fill="#FFEBEE" stroke="#C62828" stroke-width="2" rx="5"/>
  <text x="400" y="230" text-anchor="middle" font-size="16" font-weight="bold">Revert Commit (Inverse)</text>
  <text x="120" y="260" font-size="12" font-family="monospace">- Removed line 10  (opposite of add)</text>
  <text x="120" y="280" font-size="12" font-family="monospace">+ Added line 5     (opposite of remove)</text>
  <text x="400" y="340" text-anchor="middle" font-size="14" font-style="italic">Result: Changes are undone but history is preserved</text>
</svg>

---

## Reset vs Revert

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="40" text-anchor="middle" font-size="24" font-weight="bold">Reset vs Revert</text>
  <text x="200" y="80" text-anchor="middle" font-size="16" font-weight="bold">Reset (Rewrites History)</text>
  <circle cx="100" cy="120" r="20" fill="#4CAF50"/>
  <text x="100" y="125" text-anchor="middle" font-size="10" fill="white">A</text>
  <circle cx="150" cy="120" r="20" fill="#4CAF50"/>
  <text x="150" y="125" text-anchor="middle" font-size="10" fill="white">B</text>
  <circle cx="200" cy="120" r="20" fill="#FF9800" stroke-dasharray="3,3" stroke="#999" stroke-width="2"/>
  <text x="200" y="125" text-anchor="middle" font-size="10" fill="white">C</text>
  <circle cx="250" cy="120" r="20" fill="#FF9800" stroke-dasharray="3,3" stroke="#999" stroke-width="2"/>
  <text x="250" y="125" text-anchor="middle" font-size="10" fill="white">D</text>
  <line x1="120" y1="120" x2="130" y2="120" stroke="#333" stroke-width="2"/>
  <line x1="170" y1="120" x2="180" y2="120" stroke="#333" stroke-width="2"/>
  <line x1="220" y1="120" x2="230" y2="120" stroke="#999" stroke-width="2" stroke-dasharray="3,3"/>
  <text x="150" y="155" text-anchor="middle" font-size="12">HEAD after reset</text>
  <path d="M 150 145 L 150 130" stroke="#F44336" stroke-width="2" marker-end="url(#arrow1)"/>
  <text x="200" y="200" text-anchor="middle" font-size="16" font-weight="bold">Revert (Adds History)</text>
  <circle cx="100" cy="250" r="20" fill="#4CAF50"/>
  <text x="100" y="255" text-anchor="middle" font-size="10" fill="white">A</text>
  <circle cx="150" cy="250" r="20" fill="#4CAF50"/>
  <text x="150" y="255" text-anchor="middle" font-size="10" fill="white">B</text>
  <circle cx="200" cy="250" r="20" fill="#4CAF50"/>
  <text x="200" y="255" text-anchor="middle" font-size="10" fill="white">C</text>
  <circle cx="250" cy="250" r="20" fill="#4CAF50"/>
  <text x="250" y="255" text-anchor="middle" font-size="10" fill="white">D</text>
  <circle cx="300" cy="250" r="20" fill="#2196F3"/>
  <text x="300" y="255" text-anchor="middle" font-size="10" fill="white">!C</text>
  <line x1="120" y1="250" x2="130" y2="250" stroke="#333" stroke-width="2"/>
  <line x1="170" y1="250" x2="180" y2="250" stroke="#333" stroke-width="2"/>
  <line x1="220" y1="250" x2="230" y2="250" stroke="#333" stroke-width="2"/>
  <line x1="270" y1="250" x2="280" y2="250" stroke="#333" stroke-width="2"/>
  <text x="300" y="285" text-anchor="middle" font-size="12">Revert of C</text>
  <rect x="450" y="100" width="300" height="200" fill="#F5F5F5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="600" y="130" text-anchor="middle" font-size="16" font-weight="bold">When to Use:</text>
  <text x="470" y="160" font-size="13" font-weight="bold">Reset:</text>
  <text x="470" y="180" font-size="12">• Local commits only</text>
  <text x="470" y="200" font-size="12">• Clean up before push</text>
  <text x="470" y="230" font-size="13" font-weight="bold">Revert:</text>
  <text x="470" y="250" font-size="12">• Public commits</text>
  <text x="470" y="270" font-size="12">• Preserving history</text>
  <defs>
    <marker id="arrow1" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#F44336"/>
    </marker>
  </defs>
</svg>

---

## Revert in Practice

```bash
# Scenario: Bad commit pushed to production
git log --oneline
# abc123 Fix critical bug
# def456 Add feature (BROKEN!)
# ghi789 Update docs

# Can't reset (others have pulled)
# Solution: Revert!
git revert def456

# Creates new commit
# jkl012 Revert "Add feature (BROKEN!)"
# abc123 Fix critical bug  
# def456 Add feature (BROKEN!)
# ghi789 Update docs

# History preserved, change undone
```

---

## Reverting Merge Commits

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="40" text-anchor="middle" font-size="24" font-weight="bold">Reverting Merges is Special</text>
  <circle cx="200" cy="150" r="20" fill="#4CAF50"/>
  <text x="200" y="155" text-anchor="middle" font-size="10" fill="white">A</text>
  <circle cx="280" cy="100" r="20" fill="#2196F3"/>
  <text x="280" y="105" text-anchor="middle" font-size="10" fill="white">B</text>
  <circle cx="280" cy="200" r="20" fill="#FF9800"/>
  <text x="280" y="205" text-anchor="middle" font-size="10" fill="white">C</text>
  <circle cx="360" cy="150" r="25" fill="#9C27B0"/>
  <text x="360" y="155" text-anchor="middle" font-size="12" fill="white">M</text>
  <text x="360" y="180" text-anchor="middle" font-size="10">Merge</text>
  <line x1="220" y1="150" x2="335" y2="150" stroke="#333" stroke-width="2"/>
  <line x1="300" y1="100" x2="340" y2="135" stroke="#333" stroke-width="2"/>
  <line x1="300" y1="200" x2="340" y2="165" stroke="#333" stroke-width="2"/>
  <text x="280" y="85" text-anchor="middle" font-size="10">Parent 1</text>
  <text x="280" y="235" text-anchor="middle" font-size="10">Parent 2</text>
  <rect x="450" y="100" width="300" height="150" fill="#FFF3E0" stroke="#F57C00" stroke-width="2" rx="5"/>
  <text x="600" y="130" text-anchor="middle" font-size="14" font-weight="bold">Reverting Merge Commit</text>
  <text x="470" y="160" font-size="12" font-family="monospace">git revert -m 1 M</text>
  <text x="470" y="180" font-size="11">Keeps changes from Parent 1</text>
  <text x="470" y="200" font-size="12" font-family="monospace">git revert -m 2 M</text>
  <text x="470" y="220" font-size="11">Keeps changes from Parent 2</text>
  <text x="600" y="300" text-anchor="middle" font-size="13" font-style="italic">Must specify which parent to keep!</text>
</svg>

---

## Interactive Rebase Introduction

```bash
# Rebase last 3 commits interactively
git rebase -i HEAD~3

# Opens editor with:
pick abc123 First commit
pick def456 Second commit
pick ghi789 Third commit

# Commands available:
# p, pick = use commit
# r, reword = use commit, but edit message
# e, edit = use commit, but stop for amending
# s, squash = use commit, meld into previous
# f, fixup = like squash, but discard message
# x, exec = run command
# d, drop = remove commit
```

---

## Rebase Interactive Commands

<svg viewBox="0 0 800 450" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="40" text-anchor="middle" font-size="24" font-weight="bold">Interactive Rebase Options</text>
  <rect x="50" y="70" width="350" height="60" fill="#E8F5E9" stroke="#388E3C" stroke-width="2" rx="5"/>
  <text x="225" y="95" text-anchor="middle" font-size="14" font-weight="bold">pick - Keep commit as is</text>
  <text x="225" y="115" text-anchor="middle" font-size="12">Default option, no changes</text>
  <rect x="420" y="70" width="330" height="60" fill="#E3F2FD" stroke="#1976D2" stroke-width="2" rx="5"/>
  <text x="585" y="95" text-anchor="middle" font-size="14" font-weight="bold">reword - Edit commit message</text>
  <text x="585" y="115" text-anchor="middle" font-size="12">Fix typos, improve clarity</text>
  <rect x="50" y="140" width="350" height="60" fill="#FFF3E0" stroke="#F57C00" stroke-width="2" rx="5"/>
  <text x="225" y="165" text-anchor="middle" font-size="14" font-weight="bold">edit - Stop to amend commit</text>
  <text x="225" y="185" text-anchor="middle" font-size="12">Add files, split commit</text>
  <rect x="420" y="140" width="330" height="60" fill="#F3E5F5" stroke="#7B1FA2" stroke-width="2" rx="5"/>
  <text x="585" y="165" text-anchor="middle" font-size="14" font-weight="bold">squash - Combine with previous</text>
  <text x="585" y="185" text-anchor="middle" font-size="12">Keep both messages</text>
  <rect x="50" y="210" width="350" height="60" fill="#E0F2F1" stroke="#00796B" stroke-width="2" rx="5"/>
  <text x="225" y="235" text-anchor="middle" font-size="14" font-weight="bold">fixup - Combine, discard message</text>
  <text x="225" y="255" text-anchor="middle" font-size="12">Clean up WIP commits</text>
  <rect x="420" y="210" width="330" height="60" fill="#FFEBEE" stroke="#C62828" stroke-width="2" rx="5"/>
  <text x="585" y="235" text-anchor="middle" font-size="14" font-weight="bold">drop - Remove commit entirely</text>
  <text x="585" y="255" text-anchor="middle" font-size="12">Delete unwanted changes</text>
  <rect x="50" y="280" width="350" height="60" fill="#FCE4EC" stroke="#C2185B" stroke-width="2" rx="5"/>
  <text x="225" y="305" text-anchor="middle" font-size="14" font-weight="bold">exec - Run shell command</text>
  <text x="225" y="325" text-anchor="middle" font-size="12">exec npm test</text>
  <rect x="420" y="280" width="330" height="60" fill="#E1BEE7" stroke="#6A1B9A" stroke-width="2" rx="5"/>
  <text x="585" y="305" text-anchor="middle" font-size="14" font-weight="bold">break - Pause rebase here</text>
  <text x="585" y="325" text-anchor="middle" font-size="12">Manual intervention needed</text>
  <text x="400" y="380" text-anchor="middle" font-size="14" font-style="italic">Tip: You can reorder lines to reorder commits!</text>
</svg>

---

## Rebase Workflow: Squashing

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="40" text-anchor="middle" font-size="24" font-weight="bold">Interactive Rebase: Squashing</text>
  <text x="200" y="80" text-anchor="middle" font-size="14" font-weight="bold">Before</text>
  <circle cx="100" cy="120" r="20" fill="#4CAF50"/>
  <text x="100" y="125" text-anchor="middle" font-size="10" fill="white">main</text>
  <circle cx="180" cy="120" r="20" fill="#2196F3"/>
  <text x="180" y="125" text-anchor="middle" font-size="10" fill="white">WIP</text>
  <circle cx="260" cy="120" r="20" fill="#2196F3"/>
  <text x="260" y="125" text-anchor="middle" font-size="10" fill="white">typo</text>
  <circle cx="340" cy="120" r="20" fill="#2196F3"/>
  <text x="340" y="125" text-anchor="middle" font-size="10" fill="white">done</text>
  <line x1="120" y1="120" x2="160" y2="120" stroke="#333" stroke-width="2"/>
  <line x1="200" y1="120" x2="240" y2="120" stroke="#333" stroke-width="2"/>
  <line x1="280" y1="120" x2="320" y2="120" stroke="#333" stroke-width="2"/>
  <rect x="450" y="90" width="300" height="80" fill="#FFF3E0" stroke="#F57C00" stroke-width="2" rx="5"/>
  <text x="600" y="115" text-anchor="middle" font-size="12" font-family="monospace">git rebase -i HEAD~3</text>
  <text x="470" y="135" font-size="11" font-family="monospace">pick WIP</text>
  <text x="470" y="150" font-size="11" font-family="monospace">squash typo</text>
  <text x="470" y="165" font-size="11" font-family="monospace">squash done</text>
  <text x="200" y="220" text-anchor="middle" font-size="14" font-weight="bold">After</text>
  <circle cx="100" cy="260" r="20" fill="#4CAF50"/>
  <text x="100" y="265" text-anchor="middle" font-size="10" fill="white">main</text>
  <circle cx="200" cy="260" r="25" fill="#9C27B0"/>
  <text x="200" y="265" text-anchor="middle" font-size="12" fill="white">Feature</text>
  <line x1="120" y1="260" x2="175" y2="260" stroke="#333" stroke-width="2"/>
  <text x="200" y="295" text-anchor="middle" font-size="12">Clean single commit!</text>
  <rect x="350" y="240" width="400" height="120" fill="#E8F5E9" stroke="#388E3C" stroke-width="2" rx="5"/>
  <text x="550" y="270" text-anchor="middle" font-size="14" font-weight="bold">Benefits:</text>
  <text x="370" y="295" font-size="12">• Clean, logical history</text>
  <text x="370" y="315" font-size="12">• Easier code review</text>
  <text x="370" y="335" font-size="12">• Better git blame/bisect</text>
</svg>

---

## First Half Summary

## What We've Learned So Far

1. ✅ The golden rule: Never rewrite public history
1. ✅ Safe vs unsafe history modification
1. ✅ Amending commits for quick fixes
1. ✅ Three reset modes and when to use each
1. ✅ Revert for safe public undoing
1. ✅ Interactive rebase basics

## Coming Up Next

1. Advanced rebase techniques
1. Cherry-picking specific commits
1. Recovering lost work
1. Extreme history rewriting
