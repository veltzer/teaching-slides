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
---

## Splitting Commits with Rebase

```bash
# Start interactive rebase
git rebase -i HEAD~2

# Mark commit to edit
# Change 'pick' to 'edit' for the commit to split

# When Git stops at that commit:
# Reset to uncommit but keep changes
git reset HEAD^

# Stage and commit first logical change
git add file1.txt
git commit -m "First logical change"

# Stage and commit second logical change  
git add file2.txt
git commit -m "Second logical change"

# Continue rebase
git rebase --continue
```

---

## Reordering Commits

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="40" text-anchor="middle" font-size="24" font-weight="bold">Reordering with Interactive Rebase</text>
  <text x="200" y="80" text-anchor="middle" font-size="14" font-weight="bold">Before</text>
  <circle cx="100" cy="120" r="20" fill="#4CAF50"/>
  <text x="100" y="125" text-anchor="middle" font-size="10" fill="white">main</text>
  <circle cx="180" cy="120" r="20" fill="#FF9800"/>
  <text x="180" y="125" text-anchor="middle" font-size="10" fill="white">docs</text>
  <circle cx="260" cy="120" r="20" fill="#2196F3"/>
  <text x="260" y="125" text-anchor="middle" font-size="10" fill="white">feat</text>
  <circle cx="340" cy="120" r="20" fill="#9C27B0"/>
  <text x="340" y="125" text-anchor="middle" font-size="10" fill="white">test</text>
  <text x="220" y="155" text-anchor="middle" font-size="11">Illogical order</text>
  <rect x="450" y="90" width="300" height="80" fill="#FFF3E0" stroke="#F57C00" stroke-width="2" rx="5"/>
  <text x="600" y="115" text-anchor="middle" font-size="12" font-family="monospace">git rebase -i HEAD~3</text>
  <text x="470" y="135" font-size="11" font-family="monospace">pick feat</text>
  <text x="470" y="150" font-size="11" font-family="monospace">pick test</text>
  <text x="470" y="165" font-size="11" font-family="monospace">pick docs</text>
  <text x="200" y="220" text-anchor="middle" font-size="14" font-weight="bold">After (Reordered)</text>
  <circle cx="100" cy="260" r="20" fill="#4CAF50"/>
  <text x="100" y="265" text-anchor="middle" font-size="10" fill="white">main</text>
  <circle cx="180" cy="260" r="20" fill="#2196F3"/>
  <text x="180" y="265" text-anchor="middle" font-size="10" fill="white">feat</text>
  <circle cx="260" cy="260" r="20" fill="#9C27B0"/>
  <text x="260" y="265" text-anchor="middle" font-size="10" fill="white">test</text>
  <circle cx="340" cy="260" r="20" fill="#FF9800"/>
  <text x="340" y="265" text-anchor="middle" font-size="10" fill="white">docs</text>
  <text x="220" y="295" text-anchor="middle" font-size="11">Logical order!</text>
  <line x1="120" y1="120" x2="320" y2="120" stroke="#333" stroke-width="2"/>
  <line x1="120" y1="260" x2="320" y2="260" stroke="#333" stroke-width="2"/>
</svg>

---

## Rebase Conflicts

```bash
# During rebase, conflicts may occur
git rebase -i HEAD~3
# CONFLICT (content): Merge conflict in file.txt

# Fix the conflict in your editor
vim file.txt

# Stage the resolved file
git add file.txt

# Continue rebase
git rebase --continue

# Or abort if things go wrong
git rebase --abort

# Skip problematic commit
git rebase --skip
```

---

## Cherry-pick: Selective Changes

```bash
# Apply specific commit to current branch
git cherry-pick abc123

# Cherry-pick multiple commits
git cherry-pick abc123 def456

# Cherry-pick range
git cherry-pick abc123..def456

# Cherry-pick without committing
git cherry-pick -n abc123

# Cherry-pick with edit
git cherry-pick -e abc123

# Continue after conflict
git cherry-pick --continue

# Abort cherry-pick
git cherry-pick --abort
```

---

## Cherry-pick Use Cases

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="40" text-anchor="middle" font-size="24" font-weight="bold">Cherry-pick Scenarios</text>
  <text x="200" y="80" text-anchor="middle" font-size="14" font-weight="bold">Hotfix from Development</text>
  <circle cx="100" cy="120" r="20" fill="#4CAF50"/>
  <text x="100" y="125" text-anchor="middle" font-size="10" fill="white">v1.0</text>
  <circle cx="180" cy="120" r="20" fill="#4CAF50"/>
  <text x="180" y="125" text-anchor="middle" font-size="10" fill="white">prod</text>
  <text x="140" y="105" font-size="10">main</text>
  <circle cx="100" cy="180" r="20" fill="#2196F3"/>
  <text x="100" y="185" text-anchor="middle" font-size="10" fill="white">feat</text>
  <circle cx="180" cy="180" r="20" fill="#FF5722"/>
  <text x="180" y="185" text-anchor="middle" font-size="10" fill="white">fix</text>
  <circle cx="260" cy="180" r="20" fill="#2196F3"/>
  <text x="260" y="185" text-anchor="middle" font-size="10" fill="white">feat2</text>
  <text x="180" y="165" font-size="10">develop</text>
  <path d="M 180 160 Q 230 130 180 140" stroke="#FF5722" stroke-width="2" marker-end="url(#arrow2)" fill="none"/>
  <text x="230" y="130" font-size="11" fill="#FF5722">cherry-pick</text>
  <line x1="120" y1="120" x2="160" y2="120" stroke="#333" stroke-width="2"/>
  <line x1="120" y1="180" x2="160" y2="180" stroke="#333" stroke-width="2"/>
  <line x1="200" y1="180" x2="240" y2="180" stroke="#333" stroke-width="2"/>
  <line x1="100" y1="140" x2="100" y2="160" stroke="#333" stroke-width="2"/>
  <rect x="450" y="100" width="300" height="200" fill="#F5F5F5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="600" y="130" text-anchor="middle" font-size="14" font-weight="bold">Common Scenarios:</text>
  <text x="470" y="160" font-size="12">• Hotfix to production branch</text>
  <text x="470" y="185" font-size="12">• Feature from abandoned branch</text>
  <text x="470" y="210" font-size="12">• Bug fix to multiple releases</text>
  <text x="470" y="235" font-size="12">• Selective feature merging</text>
  <text x="470" y="260" font-size="12">• Backporting to older versions</text>
  <defs>
    <marker id="arrow2" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#FF5722"/>
    </marker>
  </defs>
</svg>

---

## Cherry-pick with Conflicts

```bash
# Cherry-pick may cause conflicts
git cherry-pick abc123
# CONFLICT: Merge conflict in app.js

# Option 1: Resolve and continue
vim app.js  # Fix conflicts
git add app.js
git cherry-pick --continue

# Option 2: Abort
git cherry-pick --abort

# Option 3: Use theirs/ours
git checkout --theirs app.js  # Take their version
git checkout --ours app.js    # Keep our version
git add app.js
git cherry-pick --continue
```

---

## Cherry vs Cherry-pick

```bash
# See which commits are in branch2 but not branch1
git cherry branch1 branch2

# Output:
# + abc123 Commit in branch2 not in branch1
# - def456 Commit in branch2 already in branch1

# Find commits to cherry-pick
git log --left-right --graph --cherry-pick --oneline branch1...branch2

# Cherry-pick with original author info
git cherry-pick -x abc123  # Adds "(cherry picked from...)" to message

# Record cherry-pick origin
git cherry-pick --ff abc123  # Fast-forward if possible
```

---

## Restore Command (Git 2.23+)

```bash
# Restore file in working directory
git restore file.txt

# Restore file from specific commit
git restore --source HEAD~2 file.txt

# Restore staged file (unstage)
git restore --staged file.txt

# Restore both staged and working
git restore --staged --worktree file.txt

# Restore all files
git restore .

# Interactive restore
git restore -p file.txt
```

### `restore` is clearer than the old `checkout -- file`

---

## Restore vs Reset vs Checkout

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="40" text-anchor="middle" font-size="24" font-weight="bold">Modern Git Commands</text>
  <rect x="50" y="80" width="700" height="80" fill="#E8F5E9" stroke="#388E3C" stroke-width="2" rx="5"/>
  <text x="400" y="105" text-anchor="middle" font-size="16" font-weight="bold">git restore (files)</text>
  <text x="70" y="130" font-size="13">Replaces: git checkout -- file.txt</text>
  <text x="70" y="150" font-size="12" font-family="monospace">git restore file.txt           # Discard changes</text>
  <rect x="50" y="170" width="700" height="80" fill="#E3F2FD" stroke="#1976D2" stroke-width="2" rx="5"/>
  <text x="400" y="195" text-anchor="middle" font-size="16" font-weight="bold">git switch (branches)</text>
  <text x="70" y="220" font-size="13">Replaces: git checkout branch</text>
  <text x="70" y="240" font-size="12" font-family="monospace">git switch main                # Change branches</text>
  <rect x="50" y="260" width="700" height="80" fill="#FFF3E0" stroke="#F57C00" stroke-width="2" rx="5"/>
  <text x="400" y="285" text-anchor="middle" font-size="16" font-weight="bold">git reset (commits)</text>
  <text x="70" y="310" font-size="13">Still used for: Moving HEAD, changing staging</text>
  <text x="70" y="330" font-size="12" font-family="monospace">git reset HEAD~1               # Undo commits</text>
</svg>

---

## The Reflog: Your Safety Net

```bash
# View reflog
git reflog
# or
git log -g

# Show specific ref's log
git reflog show main

# Reflog with dates
git reflog --date=relative

# Recover "lost" commit
git reflog
# Find the SHA you want
git checkout abc123
# or create branch from it
git checkout -b recovered-branch abc123

# Reset to previous state
git reset --hard HEAD@{2}
```

---

## Understanding Reflog

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="40" text-anchor="middle" font-size="24" font-weight="bold">Reflog Tracks Everything</text>
  <rect x="100" y="80" width="600" height="250" fill="#263238" stroke="#37474F" stroke-width="2" rx="5"/>
  <text x="120" y="110" font-family="monospace" font-size="12" fill="#4CAF50">$ git reflog</text>
  <text x="120" y="135" font-family="monospace" font-size="11" fill="#FFD54F">a3f8d9c HEAD@{0}: reset: moving to HEAD~2</text>
  <text x="120" y="155" font-family="monospace" font-size="11" fill="#81C784">b8e7a2d HEAD@{1}: commit: Add feature</text>
  <text x="120" y="175" font-family="monospace" font-size="11" fill="#81C784">c9d6b3e HEAD@{2}: commit: Fix bug</text>
  <text x="120" y="195" font-family="monospace" font-size="11" fill="#64B5F6">d7a5c1f HEAD@{3}: checkout: from main to feature</text>
  <text x="120" y="215" font-family="monospace" font-size="11" fill="#81C784">e8b4a2c HEAD@{4}: commit: Update README</text>
  <text x="120" y="235" font-family="monospace" font-size="11" fill="#FFB74D">f9c3b1d HEAD@{5}: rebase: Add tests</text>
  <text x="120" y="255" font-family="monospace" font-size="11" fill="#E57373">g0d4e5f HEAD@{6}: merge: Merge branch 'hotfix'</text>
  <text x="120" y="275" font-family="monospace" font-size="11" fill="#A1887F">h1e5f6g HEAD@{7}: clone: from origin</text>
  <text x="400" y="355" text-anchor="middle" font-size="14" font-style="italic">Every HEAD movement is recorded for 90 days!</text>
</svg>

---

## Reflog Recovery Examples

```bash
# Scenario 1: Accidental hard reset
git reset --hard HEAD~5  # Oops, too many!
git reflog               # Find previous state
git reset --hard HEAD@{1}  # Recovered!

# Scenario 2: Lost branch
git branch -D feature    # Deleted branch
git reflog               # Find last commit
git checkout -b feature HEAD@{3}  # Recreated!

# Scenario 3: Bad rebase
git rebase -i HEAD~10   # Messed up
git reflog              # Find pre-rebase state
git reset --hard HEAD@{5}  # Back to safety!
```

---

## Recovering Lost Commits

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="40" text-anchor="middle" font-size="24" font-weight="bold">Nothing is Really Lost (for 90 days)</text>
  <rect x="100" y="80" width="600" height="100" fill="#E8F5E9" stroke="#388E3C" stroke-width="2" rx="5"/>
  <text x="400" y="110" text-anchor="middle" font-size="16" font-weight="bold">Git's Safety Features</text>
  <text x="120" y="140" font-size="13">• Reflog tracks ALL HEAD movements (90 days default)</text>
  <text x="120" y="160" font-size="13">• Dangling commits exist until garbage collection</text>
  <circle cx="150" cy="220" r="20" fill="#4CAF50"/>
  <text x="150" y="225" text-anchor="middle" font-size="10" fill="white">A</text>
  <circle cx="220" cy="220" r="20" fill="#4CAF50"/>
  <text x="220" y="225" text-anchor="middle" font-size="10" fill="white">B</text>
  <circle cx="290" cy="220" r="20" fill="#FF9800" stroke-dasharray="3,3" stroke="#999" stroke-width="2"/>
  <text x="290" y="225" text-anchor="middle" font-size="10" fill="white">C</text>
  <circle cx="360" cy="220" r="20" fill="#FF9800" stroke-dasharray="3,3" stroke="#999" stroke-width="2"/>
  <text x="360" y="225" text-anchor="middle" font-size="10" fill="white">D</text>
  <text x="325" y="255" text-anchor="middle" font-size="11" fill="#999">"Lost" after reset</text>
  <line x1="170" y1="220" x2="200" y2="220" stroke="#333" stroke-width="2"/>
  <line x1="240" y1="220" x2="270" y2="220" stroke="#999" stroke-width="2" stroke-dasharray="3,3"/>
  <line x1="310" y1="220" x2="340" y2="220" stroke="#999" stroke-width="2" stroke-dasharray="3,3"/>
  <rect x="450" y="200" width="280" height="150" fill="#FFF3E0" stroke="#F57C00" stroke-width="2" rx="5"/>
  <text x="590" y="230" text-anchor="middle" font-size="14" font-weight="bold">Recovery Methods:</text>
  <text x="470" y="255" font-size="12" font-family="monospace">git reflog</text>
  <text x="470" y="275" font-size="12" font-family="monospace">git fsck --lost-found</text>
  <text x="470" y="295" font-size="12" font-family="monospace">git log --all --oneline</text>
  <text x="470" y="315" font-size="12" font-family="monospace">  $( git fsck --no-reflog |</text>
  <text x="470" y="335" font-size="12" font-family="monospace">     awk '/dangling/ {print $3}' )</text>
</svg>

---

## Finding Dangling Objects

```bash
# Find dangling commits
git fsck --lost-found

# Show dangling commits
git fsck --no-reflog | grep commit

# View a dangling commit
git show abc123

# Find specific lost content
git log --all --full-history -- "**/my-file.*"

# Search all objects for text
git grep "search text" $(git rev-list --all)

# Recover dangling blob
git fsck --lost-found
# Check .git/lost-found/other/
```

---

## Bisect: Finding Bad Commits

```bash
# Start bisect
git bisect start

# Mark current commit as bad
git bisect bad

# Mark known good commit
git bisect good v1.0

# Git checks out middle commit
# Test it, then mark:
git bisect good  # or
git bisect bad

# Continue until found
# Git finds first bad commit

# End bisect
git bisect reset

# Automated bisect
git bisect start HEAD v1.0
git bisect run npm test
```

---

## Bisect Visualization

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="40" text-anchor="middle" font-size="24" font-weight="bold">Binary Search for Bugs</text>
  <circle cx="100" cy="150" r="20" fill="#4CAF50"/>
  <text x="100" y="155" text-anchor="middle" font-size="10" fill="white">v1.0</text>
  <text x="100" y="180" font-size="11" fill="#4CAF50">Good</text>
  <circle cx="180" cy="150" r="20" fill="#9E9E9E"/>
  <text x="180" y="155" text-anchor="middle" font-size="10" fill="white">?</text>
  <circle cx="260" cy="150" r="20" fill="#9E9E9E"/>
  <text x="260" y="155" text-anchor="middle" font-size="10" fill="white">?</text>
  <circle cx="340" cy="150" r="20" fill="#9E9E9E"/>
  <text x="340" y="155" text-anchor="middle" font-size="10" fill="white">?</text>
  <circle cx="420" cy="150" r="20" fill="#9E9E9E"/>
  <text x="420" y="155" text-anchor="middle" font-size="10" fill="white">?</text>
  <circle cx="500" cy="150" r="20" fill="#9E9E9E"/>
  <text x="500" y="155" text-anchor="middle" font-size="10" fill="white">?</text>
  <circle cx="580" cy="150" r="20" fill="#9E9E9E"/>
  <text x="580" y="155" text-anchor="middle" font-size="10" fill="white">?</text>
  <circle cx="660" cy="150" r="20" fill="#F44336"/>
  <text x="660" y="155" text-anchor="middle" font-size="10" fill="white">HEAD</text>
  <text x="660" y="180" font-size="11" fill="#F44336">Bad</text>
  <line x1="120" y1="150" x2="640" y2="150" stroke="#333" stroke-width="2"/>
  <path d="M 380 120 L 340 140" stroke="#2196F3" stroke-width="2" marker-end="url(#arrow3)"/>
  <text x="380" y="110" font-size="12" fill="#2196F3">Step 1: Test middle</text>
  <circle cx="340" cy="220" r="20" fill="#4CAF50"/>
  <text x="340" y="225" text-anchor="middle" font-size="10" fill="white">Good</text>
  <path d="M 500 250 L 500 230" stroke="#FF9800" stroke-width="2" marker-end="url(#arrow3)"/>
  <text x="500" y="270" font-size="12" fill="#FF9800">Step 2: Test between</text>
  <circle cx="500" cy="290" r="20" fill="#F44336"/>
  <text x="500" y="295" text-anchor="middle" font-size="10" fill="white">Bad</text>
  <path d="M 420 320 L 420 300" stroke="#9C27B0" stroke-width="2" marker-end="url(#arrow3)"/>
  <text x="420" y="340" font-size="12" fill="#9C27B0">Step 3: Narrow down</text>
  <text x="420" y="360" font-size="11" fill="#9C27B0">Found: First bad commit!</text>
  <defs>
    <marker id="arrow3" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6"/>
    </marker>
  </defs>
</svg>

---

## Extreme: Filter-branch

```bash
# WARNING: Rewrites entire history!

# Remove file from all history
git filter-branch --tree-filter \
  'rm -f passwords.txt' HEAD

# Change email in all commits
git filter-branch --env-filter '
  if [ "$GIT_AUTHOR_EMAIL" = "old@email.com" ]; then
    export GIT_AUTHOR_EMAIL="new@email.com"
  fi
' HEAD

# Move directory to root in all commits
git filter-branch --subdirectory-filter src HEAD

# After filter-branch
git push --force-with-lease  # Force required!
```

### Consider `git filter-repo` (newer, faster alternative)

---

## BFG Repo Cleaner

```bash
# Faster alternative to filter-branch
# Install: brew install bfg (or download jar)

# Remove large files
bfg --strip-blobs-bigger-than 100M repo.git

# Remove passwords
bfg --replace-text passwords.txt repo.git

# Delete files
bfg --delete-files id_{dsa,rsa} repo.git

# Delete folders
bfg --delete-folders .git repo.git

# Clean up
cd repo.git
git reflog expire --expire=now --all
git gc --prune=now --aggressive
```

### Much faster than filter-branch for repository cleaning

---

## Rewriting Commit Messages in History

```bash
# Last commit
git commit --amend -m "New message"

# Older commits (interactive rebase)
git rebase -i HEAD~3
# Change 'pick' to 'reword' for commits to edit

# Filter-branch for all commits
git filter-branch --msg-filter \
  'sed "s/old text/new text/g"' HEAD

# Multiple commits non-interactively
GIT_SEQUENCE_EDITOR="sed -i 's/pick/reword/g'" \
  git rebase -i HEAD~3
```

---

## Cleaning Repository Size

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="40" text-anchor="middle" font-size="24" font-weight="bold">Repository Cleanup Strategy</text>
  <rect x="50" y="80" width="320" height="120" fill="#FFEBEE" stroke="#C62828" stroke-width="2" rx="5"/>
  <text x="210" y="110" text-anchor="middle" font-size="16" font-weight="bold">Problem: Large Files</text>
  <text x="70" y="135" font-size="12">• Videos, images, binaries</text>
  <text x="70" y="155" font-size="12">• Generated files</text>
  <text x="70" y="175" font-size="12">• Dependencies checked in</text>
  <rect x="430" y="80" width="320" height="120" fill="#E8F5E9" stroke="#388E3C" stroke-width="2" rx="5"/>
  <text x="590" y="110" text-anchor="middle" font-size="16" font-weight="bold">Solution: Clean History</text>
  <text x="450" y="135" font-size="12">1. Use BFG or filter-repo</text>
  <text x="450" y="155" font-size="12">2. Remove from all commits</text>
  <text x="450" y="175" font-size="12">3. Force push (coordinate!)</text>
  <rect x="50" y="220" width="700" height="140" fill="#FFF3E0" stroke="#F57C00" stroke-width="2" rx="5"/>
  <text x="400" y="250" text-anchor="middle" font-size="16" font-weight="bold">Prevention</text>
  <text x="70" y="280" font-size="12">• Use .gitignore from start</text>
  <text x="70" y="300" font-size="12">• Git LFS for large files</text>
  <text x="70" y="320" font-size="12">• Code review before commits</text>
  <text x="70" y="340" font-size="12">• Pre-commit hooks</text>
</svg>

---

## Undo Strategies by Scenario

<svg viewBox="0 0 800 450" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="40" text-anchor="middle" font-size="24" font-weight="bold">Choose Your Undo Strategy</text>
  <rect x="50" y="70" width="350" height="80" fill="#E8F5E9" stroke="#388E3C" stroke-width="2" rx="5"/>
  <text x="225" y="95" text-anchor="middle" font-size="14" font-weight="bold">Scenario: Typo in last commit message</text>
  <text x="225" y="115" text-anchor="middle" font-size="12">Solution: git commit --amend</text>
  <text x="225" y="135" text-anchor="middle" font-size="11" font-style="italic">Safe if not pushed</text>
  <rect x="420" y="70" width="330" height="80" fill="#E3F2FD" stroke="#1976D2" stroke-width="2" rx="5"/>
  <text x="585" y="95" text-anchor="middle" font-size="14" font-weight="bold">Scenario: Wrong file in commit</text>
  <text x="585" y="115" text-anchor="middle" font-size="12">Solution: git reset HEAD~ --soft</text>
  <text x="585" y="135" text-anchor="middle" font-size="11" font-style="italic">Then recommit correctly</text>
  <rect x="50" y="160" width="350" height="80" fill="#FFF3E0" stroke="#F57C00" stroke-width="2" rx="5"/>
  <text x="225" y="185" text-anchor="middle" font-size="14" font-weight="bold">Scenario: Need to undo public commit</text>
  <text x="225" y="205" text-anchor="middle" font-size="12">Solution: git revert</text>
  <text x="225" y="225" text-anchor="middle" font-size="11" font-style="italic">Creates new commit, preserves history</text>
  <rect x="420" y="160" width="330" height="80" fill="#FFEBEE" stroke="#C62828" stroke-width="2" rx="5"/>
  <text x="585" y="185" text-anchor="middle" font-size="14" font-weight="bold">Scenario: Discard all local changes</text>
  <text x="585" y="205" text-anchor="middle" font-size="12">Solution: git reset --hard HEAD</text>
  <text x="585" y="225" text-anchor="middle" font-size="11" font-style="italic">⚠️ Destructive!</text>
  <rect x="50" y="250" width="350" height="80" fill="#F3E5F5" stroke="#7B1FA2" stroke-width="2" rx="5"/>
  <text x="225" y="275" text-anchor="middle" font-size="14" font-weight="bold">Scenario: Messy commit history</text>
  <text x="225" y="295" text-anchor="middle" font-size="12">Solution: git rebase -i</text>
  <text x="225" y="315" text-anchor="middle" font-size="11" font-style="italic">Squash, reorder, edit</text>
  <rect x="420" y="250" width="330" height="80" fill="#E0F2F1" stroke="#00796B" stroke-width="2" rx="5"/>
  <text x="585" y="275" text-anchor="middle" font-size="14" font-weight="bold">Scenario: Need specific fix from branch</text>
  <text x="585" y="295" text-anchor="middle" font-size="12">Solution: git cherry-pick</text>
  <text x="585" y="315" text-anchor="middle" font-size="11" font-style="italic">Apply single commit</text>
  <rect x="50" y="340" width="350" height="80" fill="#FCE4EC" stroke="#C2185B" stroke-width="2" rx="5"/>
  <text x="225" y="365" text-anchor="middle" font-size="14" font-weight="bold">Scenario: Committed sensitive data</text>
  <text x="225" y="385" text-anchor="middle" font-size="12">Solution: BFG or filter-branch</text>
  <text x="225" y="405" text-anchor="middle" font-size="11" font-style="italic">Rewrites entire history</text>
  <rect x="420" y="340" width="330" height="80" fill="#E1BEE7" stroke="#6A1B9A" stroke-width="2" rx="5"/>
  <text x="585" y="365" text-anchor="middle" font-size="14" font-weight="bold">Scenario: Lost commits after reset</text>
  <text x="585" y="385" text-anchor="middle" font-size="12">Solution: git reflog + checkout/branch</text>
  <text x="585" y="405" text-anchor="middle" font-size="11" font-style="italic">Recover within 90 days</text>
</svg>

---

## Best Practices for Undoing

1. **Think before you act** - Understand what each command does
1. **Use reflog as safety net** - Check reflog before panic
1. **Prefer revert for public commits** - Maintains history
1. **Test in a branch first** - Create a backup branch
1. **Communicate with team** - Before rewriting shared history
1. **Use --force-lease** - Safer than --force
1. **Keep backups** - Clone before dangerous operations
1. **Document your changes** - Explain why history was rewritten

---

## Common Pitfalls to Avoid

❌ **Force pushing to main**
```bash
git push --force origin main  # NEVER!
```

❌ **Resetting without checking**
```bash
git reset --hard  # Check git status first!
```

❌ **Rebasing public branches**
```bash
git checkout main
git rebase feature  # Don't rebase shared branches
```

❌ **Amending pushed commits**
```bash
git push
git commit --amend  # Too late!
```

---

## Recovery Checklist

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="40" text-anchor="middle" font-size="24" font-weight="bold">Lost Something? Don't Panic!</text>
  <rect x="100" y="70" width="600" height="300" fill="#F5F5F5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="400" y="100" text-anchor="middle" font-size="18" font-weight="bold">Recovery Steps</text>
  <rect x="130" y="120" width="540" height="35" fill="#E8F5E9" stroke="#388E3C" stroke-width="1" rx="3"/>
  <text x="150" y="142" font-size="14">1. Check git status - Is it just unstaged?</text>
  <rect x="130" y="160" width="540" height="35" fill="#E3F2FD" stroke="#1976D2" stroke-width="1" rx="3"/>
  <text x="150" y="182" font-size="14">2. Check git reflog - Find the SHA</text>
  <rect x="130" y="200" width="540" height="35" fill="#FFF3E0" stroke="#F57C00" stroke-width="1" rx="3"/>
  <text x="150" y="222" font-size="14">3. Check git fsck --lost-found - Dangling commits</text>
  <rect x="130" y="240" width="540" height="35" fill="#F3E5F5" stroke="#7B1FA2" stroke-width="1" rx="3"/>
  <text x="150" y="262" font-size="14">4. Check git stash list - Maybe you stashed it?</text>
  <rect x="130" y="280" width="540" height="35" fill="#FFEBEE" stroke="#C62828" stroke-width="1" rx="3"/>
  <text x="150" y="302" font-size="14">5. Check backups/clones - Other copies?</text>
  <rect x="130" y="320" width="540" height="35" fill="#E0F2F1" stroke="#00796B" stroke-width="1" rx="3"/>
  <text x="150" y="342" font-size="14">6. Act quickly - Garbage collection in 90 days</text>
</svg>

---

## Advanced Recovery Techniques

```bash
# Find deleted file in history
git log --all --full-history -- "**/deleted-file.txt"

# Show file content from specific commit
git show abc123:path/to/file.txt > recovered-file.txt

# Find commit that deleted a file
git log --diff-filter=D --summary | grep delete

# Recover file deleted in commit
git checkout abc123^ -- path/to/file.txt

# Find large files in history
git rev-list --objects --all | \
  git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' | \
  sort -k3 -n -r | head -20
```

---

## Emergency Recovery Commands

```bash
# EMERGENCY: Undo last action (ANY action)
git reset --hard HEAD@{1}

# EMERGENCY: Get back to clean state
git reset --hard origin/main
git clean -fd

# EMERGENCY: Abort ongoing operation
git merge --abort
git rebase --abort
git cherry-pick --abort
git revert --abort

# EMERGENCY: Stash everything
git stash --all  # Including untracked and ignored

# EMERGENCY: Create backup branch
git branch backup-$(date +%Y%m%d-%H%M%S)
```

---

## Summary

## What We Learned

1. ✅ The golden rule: Don't rewrite public history
1. ✅ Amending commits safely
1. ✅ Reset vs Revert strategies
1. ✅ Interactive rebase for history cleanup
1. ✅ Cherry-picking specific changes
1. ✅ Using reflog for recovery
1. ✅ Finding and recovering lost commits
1. ✅ Extreme history rewriting techniques
1. ✅ Bisect for finding bugs

---

## Key Takeaways

1. **Reflog is your friend** - Nothing is truly lost for 90 days
1. **Revert for public, reset for private** - Choose the right tool
1. **Interactive rebase is powerful** - Clean history before sharing
1. **Force-lease over force** - Safer forced pushes
1. **Think before rewriting** - Some actions can't be undone
1. **Communicate with your team** - Coordinate history changes
1. **Keep calm when things go wrong** - Git usually has a way to recover

---

## Quick Reference Card

| Problem | Local | Public |
|---------|-------|--------|
| Wrong message | `commit --amend` | `revert` + new commit |
| Bad commit | `reset` | `revert` |
| Multiple fixes | `rebase -i` | separate commits |
| Need specific change | `cherry-pick` | `cherry-pick` |
| Lost work | `reflog` | `reflog` |
| File in history | `filter-branch`/BFG | coordinate with team |

---

## Practice Exercises

1. Create commits and practice amending them
1. Use interactive rebase to squash commits
1. Cherry-pick a commit between branches
1. Recover a "lost" commit using reflog
1. Practice bisect to find a breaking change
1. Try different reset modes and observe effects
1. Clean up a messy history with rebase
1. Remove a large file from history with BFG

---

## Next Up: Remote Repositories

In the next session, we'll explore:

1. Working with remote repositories
1. Setting up and publishing repositories
1. Understanding repository structure
1. Working with multiple remotes
1. GitHub, GitLab, and other platforms
1. Collaboration workflows
1. Pull requests and code reviews

---

## Undoing Things Complete! 🎉

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="80" text-anchor="middle" font-size="32" font-weight="bold" fill="#4CAF50">Master of Time Travel!</text>
  <rect x="200" y="120" width="400" height="200" fill="#E8F5E9" stroke="#388E3C" stroke-width="3" rx="10"/>
  <text x="400" y="165" text-anchor="middle" font-size="20">You can now:</text>
  <text x="400" y="195" text-anchor="middle" font-size="16">• Fix mistakes confidently</text>
  <text x="400" y="220" text-anchor="middle" font-size="16">• Clean up messy history</text>
  <text x="400" y="245" text-anchor="middle" font-size="16">• Recover "lost" work</text>
  <text x="400" y="270" text-anchor="middle" font-size="16">• Choose the right undo strategy</text>
  <circle cx="250" cy="350" r="25" fill="#2196F3"/>
  <text x="250" y="357" text-anchor="middle" font-size="20">⏰</text>
  <circle cx="400" cy="350" r="25" fill="#FF9800"/>
  <text x="400" y="357" text-anchor="middle" font-size="20">🔄</text>
  <circle cx="550" cy="350" r="25" fill="#9C27B0"/>
  <text x="550" y="357" text-anchor="middle" font-size="20">✨</text>
</svg>
