# Merging Changes

---

## What We'll Cover

1. Understanding merges in depth
1. Fast-forward merges
1. Three-way merge mechanics
1. Merge strategies and options
1. Handling conflicts like a pro
1. Using merge tools effectively
1. Cherry-picking vs merging
1. Advanced merge techniques

---

## What is a Merge?

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="40" text-anchor="middle" font-size="24" font-weight="bold">Merging Combines Histories</text>
  <rect x="100" y="80" width="600" height="100" fill="#E3F2FD" stroke="#1976D2" stroke-width="2" rx="5"/>
  <text x="400" y="110" text-anchor="middle" font-size="16">A merge combines changes from different branches</text>
  <text x="400" y="135" text-anchor="middle" font-size="14">Creating a unified history with all changes</text>
  <text x="400" y="160" text-anchor="middle" font-size="14">Preserves the complete development timeline</text>
  <circle cx="200" cy="250" r="25" fill="#4CAF50"/>
  <text x="200" y="255" text-anchor="middle" font-size="12" fill="white">Base</text>
  <circle cx="300" cy="210" r="25" fill="#2196F3"/>
  <text x="300" y="215" text-anchor="middle" font-size="12" fill="white">A</text>
  <circle cx="400" cy="210" r="25" fill="#2196F3"/>
  <text x="400" y="215" text-anchor="middle" font-size="12" fill="white">B</text>
  <circle cx="300" cy="290" r="25" fill="#FF9800"/>
  <text x="300" y="295" text-anchor="middle" font-size="12" fill="white">C</text>
  <circle cx="400" cy="290" r="25" fill="#FF9800"/>
  <text x="400" y="295" text-anchor="middle" font-size="12" fill="white">D</text>
  <circle cx="500" cy="250" r="30" fill="#9C27B0"/>
  <text x="500" y="255" text-anchor="middle" font-size="14" fill="white">M</text>
  <line x1="225" y1="240" x2="275" y2="220" stroke="#333" stroke-width="2"/>
  <line x1="225" y1="260" x2="275" y2="280" stroke="#333" stroke-width="2"/>
  <line x1="325" y1="210" x2="375" y2="210" stroke="#333" stroke-width="2"/>
  <line x1="325" y1="290" x2="375" y2="290" stroke="#333" stroke-width="2"/>
  <line x1="425" y1="210" x2="470" y2="235" stroke="#333" stroke-width="2"/>
  <line x1="425" y1="290" x2="470" y2="265" stroke="#333" stroke-width="2"/>
  <text x="500" y="320" text-anchor="middle" font-size="12">Merge commit</text>
  <text x="500" y="340" text-anchor="middle" font-size="11">Has two parents</text>
</svg>

---

## Fast-Forward Merge

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="40" text-anchor="middle" font-size="24" font-weight="bold">Fast-Forward: The Simple Case</text>
  <text x="200" y="90" text-anchor="middle" font-size="14" font-weight="bold">Before Merge</text>
  <circle cx="100" cy="130" r="20" fill="#4CAF50"/>
  <text x="100" y="135" text-anchor="middle" font-size="10" fill="white">A</text>
  <circle cx="180" cy="130" r="20" fill="#4CAF50"/>
  <text x="180" y="135" text-anchor="middle" font-size="10" fill="white">B</text>
  <circle cx="260" cy="130" r="20" fill="#2196F3"/>
  <text x="260" y="135" text-anchor="middle" font-size="10" fill="white">C</text>
  <circle cx="340" cy="130" r="20" fill="#2196F3"/>
  <text x="340" y="135" text-anchor="middle" font-size="10" fill="white">D</text>
  <rect x="140" y="80" width="60" height="25" fill="#4CAF50" rx="3"/>
  <text x="170" y="98" text-anchor="middle" font-size="10" fill="white">main</text>
  <rect x="320" y="80" width="60" height="25" fill="#2196F3" rx="3"/>
  <text x="350" y="98" text-anchor="middle" font-size="10" fill="white">feature</text>
  <line x1="120" y1="130" x2="160" y2="130" stroke="#333" stroke-width="2"/>
  <line x1="200" y1="130" x2="240" y2="130" stroke="#333" stroke-width="2"/>
  <line x1="280" y1="130" x2="320" y2="130" stroke="#333" stroke-width="2"/>
  <text x="200" y="200" text-anchor="middle" font-size="14" font-weight="bold">After Fast-Forward</text>
  <circle cx="100" cy="240" r="20" fill="#4CAF50"/>
  <text x="100" y="245" text-anchor="middle" font-size="10" fill="white">A</text>
  <circle cx="180" cy="240" r="20" fill="#4CAF50"/>
  <text x="180" y="245" text-anchor="middle" font-size="10" fill="white">B</text>
  <circle cx="260" cy="240" r="20" fill="#4CAF50"/>
  <text x="260" y="245" text-anchor="middle" font-size="10" fill="white">C</text>
  <circle cx="340" cy="240" r="20" fill="#4CAF50"/>
  <text x="340" y="245" text-anchor="middle" font-size="10" fill="white">D</text>
  <rect x="320" y="190" width="60" height="25" fill="#4CAF50" rx="3"/>
  <text x="350" y="208" text-anchor="middle" font-size="10" fill="white">main</text>
  <line x1="120" y1="240" x2="160" y2="240" stroke="#333" stroke-width="2"/>
  <line x1="200" y1="240" x2="240" y2="240" stroke="#333" stroke-width="2"/>
  <line x1="280" y1="240" x2="320" y2="240" stroke="#333" stroke-width="2"/>
  <rect x="450" y="120" width="300" height="140" fill="#E8F5E9" stroke="#388E3C" stroke-width="2" rx="5"/>
  <text x="600" y="150" text-anchor="middle" font-size="14" font-weight="bold">Fast-Forward Characteristics</text>
  <text x="470" y="175" font-size="12">✓ No merge commit created</text>
  <text x="470" y="195" font-size="12">✓ Linear history maintained</text>
  <text x="470" y="215" font-size="12">✓ Branch pointer just moves</text>
  <text x="470" y="235" font-size="12">✓ Possible when no divergence</text>
</svg>

---

## Fast-Forward in Practice

```bash
# Check if fast-forward is possible
git merge-base main feature
git rev-parse main
# If merge-base equals main, FF is possible

# Perform fast-forward merge
git checkout main
git merge feature
# Updating abc123..def456
# Fast-forward

# Force fast-forward only (fail if not possible)
git merge --ff-only feature

# Prevent fast-forward (create merge commit)
git merge --no-ff feature

# Configure default behavior
git config merge.ff false  # Never fast-forward
git config merge.ff only   # Only fast-forward
```

---

## Why Prevent Fast-Forward?

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="40" text-anchor="middle" font-size="24" font-weight="bold">--no-ff: Preserving Branch Context</text>
  <rect x="50" y="80" width="350" height="150" fill="#FFEBEE" stroke="#C62828" stroke-width="2" rx="5"/>
  <text x="225" y="105" text-anchor="middle" font-size="14" font-weight="bold">With Fast-Forward</text>
  <circle cx="100" cy="150" r="15" fill="#4CAF50"/>
  <circle cx="160" cy="150" r="15" fill="#4CAF50"/>
  <circle cx="220" cy="150" r="15" fill="#4CAF50"/>
  <circle cx="280" cy="150" r="15" fill="#4CAF50"/>
  <circle cx="340" cy="150" r="15" fill="#4CAF50"/>
  <line x1="115" y1="150" x2="145" y2="150" stroke="#333" stroke-width="2"/>
  <line x1="175" y1="150" x2="205" y2="150" stroke="#333" stroke-width="2"/>
  <line x1="235" y1="150" x2="265" y2="150" stroke="#333" stroke-width="2"/>
  <line x1="295" y1="150" x2="325" y2="150" stroke="#333" stroke-width="2"/>
  <text x="225" y="190" text-anchor="middle" font-size="12">❌ Can't see where feature was</text>
  <text x="225" y="210" text-anchor="middle" font-size="12">❌ Loses branch information</text>
  <rect x="420" y="80" width="330" height="150" fill="#E8F5E9" stroke="#388E3C" stroke-width="2" rx="5"/>
  <text x="585" y="105" text-anchor="middle" font-size="14" font-weight="bold">With --no-ff</text>
  <circle cx="470" cy="150" r="15" fill="#4CAF50"/>
  <circle cx="530" cy="150" r="15" fill="#4CAF50"/>
  <circle cx="560" cy="120" r="15" fill="#2196F3"/>
  <circle cx="620" cy="120" r="15" fill="#2196F3"/>
  <circle cx="650" cy="150" r="15" fill="#9C27B0"/>
  <text x="650" y="155" text-anchor="middle" font-size="10" fill="white">M</text>
  <line x1="485" y1="150" x2="515" y2="150" stroke="#333" stroke-width="2"/>
  <line x1="545" y1="135" x2="545" y2="135" stroke="#333" stroke-width="2"/>
  <line x1="530" y1="140" x2="545" y2="130" stroke="#333" stroke-width="2"/>
  <line x1="575" y1="120" x2="605" y2="120" stroke="#333" stroke-width="2"/>
  <line x1="635" y1="130" x2="635" y2="140" stroke="#333" stroke-width="2"/>
  <line x1="545" y1="150" x2="635" y2="150" stroke="#333" stroke-width="2"/>
  <text x="585" y="190" text-anchor="middle" font-size="12">✓ Feature branch visible</text>
  <text x="585" y="210" text-anchor="middle" font-size="12">✓ Clear project history</text>
  <rect x="200" y="250" width="400" height="100" fill="#FFF3E0" stroke="#F57C00" stroke-width="2" rx="5"/>
  <text x="400" y="280" text-anchor="middle" font-size="14" font-weight="bold">Use --no-ff when:</text>
  <text x="220" y="305" font-size="12">• Want to preserve feature branch context</text>
  <text x="220" y="325" font-size="12">• Following GitFlow or similar workflow</text>
</svg>

---

## Three-Way Merge Explained

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="40" text-anchor="middle" font-size="24" font-weight="bold">Three-Way Merge Algorithm</text>
  <circle cx="400" cy="150" r="30" fill="#4CAF50"/>
  <text x="400" y="155" text-anchor="middle" font-size="12" fill="white">Base</text>
  <text x="400" y="120" text-anchor="middle" font-size="12">Common Ancestor</text>
  <circle cx="250" cy="250" r="30" fill="#2196F3"/>
  <text x="250" y="255" text-anchor="middle" font-size="12" fill="white">Ours</text>
  <text x="250" y="290" text-anchor="middle" font-size="12">Current Branch</text>
  <circle cx="550" cy="250" r="30" fill="#FF9800"/>
  <text x="550" y="255" text-anchor="middle" font-size="12" fill="white">Theirs</text>
  <text x="550" y="290" text-anchor="middle" font-size="12">Merging Branch</text>
  <path d="M 375 170 L 275 230" stroke="#333" stroke-width="2" marker-end="url(#arrow1)"/>
  <path d="M 425 170 L 525 230" stroke="#333" stroke-width="2" marker-end="url(#arrow1)"/>
  <rect x="300" y="320" width="200" height="60" fill="#9C27B0" rx="5"/>
  <text x="400" y="355" text-anchor="middle" font-size="14" fill="white">Merge Result</text>
  <path d="M 280 265 L 350 320" stroke="#333" stroke-width="2" marker-end="url(#arrow1)"/>
  <path d="M 520 265 L 450 320" stroke="#333" stroke-width="2" marker-end="url(#arrow1)"/>
  <rect x="50" y="100" width="120" height="200" fill="#F5F5F5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="110" y="125" text-anchor="middle" font-size="12" font-weight="bold">File: app.js</text>
  <text x="110" y="150" text-anchor="middle" font-size="10">Base: line A</text>
  <text x="110" y="170" text-anchor="middle" font-size="10">Ours: line B</text>
  <text x="110" y="190" text-anchor="middle" font-size="10">Theirs: line A</text>
  <text x="110" y="220" text-anchor="middle" font-size="11" font-weight="bold">Result: line B</text>
  <text x="110" y="240" text-anchor="middle" font-size="10">(Ours changed,</text>
  <text x="110" y="255" text-anchor="middle" font-size="10">theirs didn't)</text>
  <defs>
    <marker id="arrow1" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## How Git Decides What to Merge

```bash
# Git's merge decision tree:

# 1. Find merge base
git merge-base main feature

# 2. Compare each file:
# Base → Ours → Theirs → Action
# Same → Same → Same  → No change
# X    → Y    → X     → Take Y (ours changed)
# X    → X    → Y     → Take Y (theirs changed)
# X    → Y    → Z     → CONFLICT!
# X    → Y    → Y     → Take Y (same change)

# 3. For text files, compare line by line
# 4. For binary files, compare whole file
```

---

## Merge Strategies

```bash
# Default strategy (recursive/ort)
git merge feature

# Resolve strategy (older, simpler)
git merge -s resolve feature

# Ours strategy (ignore other branch entirely)
git merge -s ours feature

# Octopus (merge multiple branches)
git merge feature1 feature2 feature3

# Subtree (merge as subdirectory)
git merge -s subtree feature

# Custom strategy
git merge -s custom feature
```

---

## Strategy Options (-X)

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="40" text-anchor="middle" font-size="24" font-weight="bold">Merge Strategy Options</text>
  <rect x="50" y="80" width="350" height="120" fill="#E8F5E9" stroke="#388E3C" stroke-width="2" rx="5"/>
  <text x="225" y="110" text-anchor="middle" font-size="16" font-weight="bold">-X ours</text>
  <text x="70" y="135" font-size="12">Auto-resolve conflicts using our version</text>
  <text x="70" y="155" font-size="11" font-family="monospace">git merge -X ours feature</text>
  <text x="70" y="180" font-size="11">⚠️ Not same as -s ours</text>
  <rect x="420" y="80" width="330" height="120" fill="#E3F2FD" stroke="#1976D2" stroke-width="2" rx="5"/>
  <text x="585" y="110" text-anchor="middle" font-size="16" font-weight="bold">-X theirs</text>
  <text x="440" y="135" font-size="12">Auto-resolve conflicts using their version</text>
  <text x="440" y="155" font-size="11" font-family="monospace">git merge -X theirs feature</text>
  <text x="440" y="180" font-size="11">⚠️ No -s theirs strategy exists</text>
  <rect x="50" y="220" width="350" height="120" fill="#FFF3E0" stroke="#F57C00" stroke-width="2" rx="5"/>
  <text x="225" y="250" text-anchor="middle" font-size="16" font-weight="bold">-X patience</text>
  <text x="70" y="275" font-size="12">Better algorithm for similar lines</text>
  <text x="70" y="295" font-size="11" font-family="monospace">git merge -X patience feature</text>
  <text x="70" y="315" font-size="11">Good for refactored code</text>
  <rect x="420" y="220" width="330" height="120" fill="#FFEBEE" stroke="#C62828" stroke-width="2" rx="5"/>
  <text x="585" y="250" text-anchor="middle" font-size="16" font-weight="bold">-X ignore-space-change</text>
  <text x="440" y="275" font-size="12">Ignore whitespace in conflicts</text>
  <text x="440" y="295" font-size="11" font-family="monospace">git merge -X ignore-space-change</text>
  <text x="440" y="315" font-size="11">Useful for different formatting</text>
</svg>

---

## Understanding Merge Conflicts

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="40" text-anchor="middle" font-size="24" font-weight="bold">Why Conflicts Happen</text>
  <rect x="100" y="80" width="600" height="60" fill="#FFEBEE" stroke="#C62828" stroke-width="2" rx="5"/>
  <text x="400" y="115" text-anchor="middle" font-size="16">Conflict = Both branches changed the same part differently</text>
  <rect x="50" y="160" width="220" height="120" fill="#E8F5E9" stroke="#388E3C" stroke-width="2" rx="5"/>
  <text x="160" y="185" text-anchor="middle" font-size="14" font-weight="bold">Base Version</text>
  <text x="60" y="210" font-family="monospace" font-size="10">function greet() {</text>
  <text x="60" y="230" font-family="monospace" font-size="10">  return "Hello";</text>
  <text x="60" y="250" font-family="monospace" font-size="10">}</text>
  <rect x="290" y="160" width="220" height="120" fill="#E3F2FD" stroke="#1976D2" stroke-width="2" rx="5"/>
  <text x="400" y="185" text-anchor="middle" font-size="14" font-weight="bold">Our Version</text>
  <text x="300" y="210" font-family="monospace" font-size="10">function greet(name) {</text>
  <text x="300" y="230" font-family="monospace" font-size="10">  return `Hi ${name}`;</text>
  <text x="300" y="250" font-family="monospace" font-size="10">}</text>
  <rect x="530" y="160" width="220" height="120" fill="#FFF3E0" stroke="#F57C00" stroke-width="2" rx="5"/>
  <text x="640" y="185" text-anchor="middle" font-size="14" font-weight="bold">Their Version</text>
  <text x="540" y="210" font-family="monospace" font-size="10">function greet() {</text>
  <text x="540" y="230" font-family="monospace" font-size="10">  return "Bonjour";</text>
  <text x="540" y="250" font-family="monospace" font-size="10">}</text>
  <rect x="250" y="300" width="300" height="60" fill="#F44336" rx="5"/>
  <text x="400" y="335" text-anchor="middle" font-size="16" fill="white">CONFLICT!</text>
  <text x="400" y="355" text-anchor="middle" font-size="12" fill="white">Git can't auto-merge</text>
</svg>

---

## Conflict Markers

```bash
# Conflict markers in file:
<<<<<<< HEAD
function greet(name) {
  return `Hi ${name}`;
}
=======
function greet() {
  return "Bonjour";
}
>>>>>>> feature

# What they mean:
# <<<<<<< HEAD        - Start of your version
# =======             - Separator
# >>>>>>> feature     - End of their version

# After resolution (remove all markers):
function greet(name = "World") {
  return `Bonjour ${name}`;
}
```

---

## Resolving Conflicts Step by Step

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="40" text-anchor="middle" font-size="24" font-weight="bold">Conflict Resolution Workflow</text>
  <rect x="50" y="80" width="150" height="60" fill="#F44336" rx="5"/>
  <text x="125" y="115" text-anchor="middle" font-size="14" fill="white">1. Merge Attempt</text>
  <text x="125" y="160" text-anchor="middle" font-size="11">CONFLICT!</text>
  <rect x="220" y="80" width="150" height="60" fill="#FF9800" rx="5"/>
  <text x="295" y="115" text-anchor="middle" font-size="14" fill="white">2. Identify Files</text>
  <text x="295" y="160" text-anchor="middle" font-size="10" font-family="monospace">git status</text>
  <rect x="390" y="80" width="150" height="60" fill="#FFC107" rx="5"/>
  <text x="465" y="115" text-anchor="middle" font-size="14" fill="white">3. Open & Edit</text>
  <text x="465" y="160" text-anchor="middle" font-size="11">Remove markers</text>
  <rect x="560" y="80" width="150" height="60" fill="#4CAF50" rx="5"/>
  <text x="635" y="115" text-anchor="middle" font-size="14" fill="white">4. Stage Files</text>
  <text x="635" y="160" text-anchor="middle" font-size="10" font-family="monospace">git add</text>
  <path d="M 200 110 L 220 110" stroke="#333" stroke-width="2" marker-end="url(#arrow2)"/>
  <path d="M 370 110 L 390 110" stroke="#333" stroke-width="2" marker-end="url(#arrow2)"/>
  <path d="M 540 110 L 560 110" stroke="#333" stroke-width="2" marker-end="url(#arrow2)"/>
  <rect x="300" y="180" width="200" height="60" fill="#2196F3" rx="5"/>
  <text x="400" y="215" text-anchor="middle" font-size="14" fill="white">5. Complete Merge</text>
  <text x="400" y="235" text-anchor="middle" font-size="10" font-family="monospace" fill="white">git commit</text>
  <path d="M 635 140 L 500 180" stroke="#333" stroke-width="2" marker-end="url(#arrow2)"/>
  <rect x="200" y="270" width="400" height="100" fill="#F5F5F5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="400" y="300" text-anchor="middle" font-size="14" font-weight="bold">Alternative: Abort Merge</text>
  <text x="220" y="325" font-size="12" font-family="monospace">git merge --abort</text>
  <text x="220" y="345" font-size="11">Returns to state before merge attempt</text>
  <defs>
    <marker id="arrow2" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Conflict Resolution Strategies

```bash
# Strategy 1: Accept theirs
git checkout --theirs file.txt
git add file.txt

# Strategy 2: Accept ours
git checkout --ours file.txt
git add file.txt

# Strategy 3: Use mergetool
git mergetool

# Strategy 4: Manual resolution
# Edit file, remove markers, save
git add file.txt

# Strategy 5: Postpone file
git rm file.txt  # Remove from merge
# Handle separately later
```

---

## Viewing Conflicts

```bash
# See conflict details
git diff
# Shows conflict markers

# See common ancestor version
git show :1:file.txt  # Base

# See our version
git show :2:file.txt  # Ours

# See their version
git show :3:file.txt  # Theirs

# List conflicted files
git diff --name-only --diff-filter=U

# Check if conflicts remain
git diff --check
```

## Using Merge Tools

External tools can simplify conflict resolution:

```bash
# Configure a merge tool
git config --global merge.tool vimdiff
git config --global merge.tool meld
git config --global merge.tool kdiff3

# Use the configured tool
git mergetool
```

**Popular merge tools:**
- `vimdiff` - Terminal-based, comes with vim
- `meld` - Visual diff tool for Linux
- `kdiff3` - Cross-platform GUI tool
- VS Code - Modern editor with excellent diff support

---

## Git Fetch vs Git Pull

Understanding the difference between `fetch` and `pull`:

**`git fetch`:**
- Downloads commits from remote
- Updates remote tracking branches
- Does NOT modify your working directory
- Safe operation, never causes conflicts

**`git pull`:**
- Combines `git fetch` + `git merge`
- Downloads AND integrates changes
- Can cause merge conflicts
- Modifies your working directory

```bash
# Safer approach
git fetch origin
git merge origin/main

# Equivalent to
git pull origin main
```

---

## Pull with Rebase

Use `--rebase` to maintain linear history:

```bash
# Instead of merge, rebase your changes
git pull --rebase origin main

# Configure as default
git config --global pull.rebase true
```

**Benefits:**
- Cleaner, linear history
- Easier to follow project timeline
- Reduces "merge commits" clutter
- Better for code reviews

<svg viewBox="0 0 600 250" xmlns="http://www.w3.org/2000/svg">
  <text x="150" y="30" text-anchor="middle" font-size="14" font-weight="bold">git pull (merge)</text>
  <text x="450" y="30" text-anchor="middle" font-size="14" font-weight="bold">git pull --rebase</text>

  <!-- Merge example -->
  <circle cx="50" cy="70" r="8" fill="#3498db"/>
  <circle cx="120" cy="70" r="8" fill="#e74c3c"/>
  <circle cx="190" cy="70" r="8" fill="#2ecc71"/>
  <circle cx="120" cy="120" r="8" fill="#f39c12"/>
  <circle cx="190" cy="120" r="8" fill="#9b59b6"/>
  <circle cx="260" cy="95" r="8" fill="#34495e"/>

  <!-- Rebase example -->
  <circle cx="350" cy="70" r="8" fill="#3498db"/>
  <circle cx="420" cy="70" r="8" fill="#e74c3c"/>
  <circle cx="490" cy="70" r="8" fill="#f39c12"/>
  <circle cx="560" cy="70" r="8" fill="#9b59b6"/>
  <circle cx="560" cy="120" r="8" fill="#2ecc71"/>

  <line x1="58" y1="70" x2="112" y2="70" stroke="#333"/>
  <line x1="128" y1="70" x2="182" y2="70" stroke="#333"/>
  <line x1="128" y1="70" x2="112" y2="112" stroke="#333"/>
  <line x1="128" y1="120" x2="182" y2="120" stroke="#333"/>
  <line x1="198" y1="70" x2="245" y2="88" stroke="#333"/>
  <line x1="198" y1="120" x2="245" y2="102" stroke="#333"/>

  <line x1="358" y1="70" x2="412" y2="70" stroke="#333"/>
  <line x1="428" y1="70" x2="482" y2="70" stroke="#333"/>
  <line x1="498" y1="70" x2="552" y2="70" stroke="#333"/>
  <line x1="560" y1="78" x2="560" y2="112" stroke="#333"/>
</svg>

---

## Cherry Picking During Merge

Sometimes you need specific commits from another branch:

```bash
# Pick a specific commit
git cherry-pick <commit-hash>

# Pick multiple commits
git cherry-pick <commit1> <commit2>

# Pick a range of commits
git cherry-pick <start-commit>..<end-commit>
```

**Use cases:**
- Apply hotfixes to multiple branches
- Select features from experimental branches
- Backport changes to older versions
- Fix merge mistakes

---

## Merge Commit Messages

Customize merge commit messages for better history:

```bash
# Custom merge message
git merge feature-branch -m "Merge feature: Add user authentication"

# Edit merge message interactively
git merge feature-branch --edit

# No commit message (fast-forward only)
git merge feature-branch --ff-only
```

**Best practices:**
- Describe what the merge accomplishes
- Reference ticket/issue numbers
- Mention breaking changes
- Keep it concise but informative

---

## Aborting Merges

When merges go wrong, you can abort:

```bash
# Abort current merge
git merge --abort

# Reset to pre-merge state
git reset --hard HEAD

# Check merge status
git status
```

**When to abort:**
- Too many conflicts to resolve
- Wrong branch merged
- Merge was started accidentally
- Need to prepare better strategy

---

## Merge vs Rebase Decision Tree

<svg viewBox="0 0 700 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="300" y="20" width="100" height="40" fill="#3498db" rx="5"/>
  <text x="350" y="45" text-anchor="middle" fill="white" font-size="12">Start Merge?</text>

  <rect x="150" y="100" width="120" height="40" fill="#e74c3c" rx="5"/>
  <text x="210" y="115" text-anchor="middle" fill="white" font-size="10">Public Branch?</text>
  <text x="210" y="130" text-anchor="middle" fill="white" font-size="10">(Shared)</text>

  <rect x="430" y="100" width="120" height="40" fill="#2ecc71" rx="5"/>
  <text x="490" y="115" text-anchor="middle" fill="white" font-size="10">Private Branch?</text>
  <text x="490" y="130" text-anchor="middle" fill="white" font-size="10">(Local Only)</text>

  <rect x="80" y="200" width="80" height="30" fill="#f39c12" rx="5"/>
  <text x="120" y="220" text-anchor="middle" fill="white" font-size="11">USE MERGE</text>

  <rect x="520" y="200" width="80" height="30" fill="#9b59b6" rx="5"/>
  <text x="560" y="220" text-anchor="middle" fill="white" font-size="11">USE REBASE</text>

  <line x1="320" y1="60" x2="240" y2="100" stroke="#333" stroke-width="2"/>
  <line x1="380" y1="60" x2="460" y2="100" stroke="#333" stroke-width="2"/>
  <line x1="180" y1="140" x2="130" y2="200" stroke="#333" stroke-width="2"/>
  <line x1="520" y1="140" x2="570" y2="200" stroke="#333" stroke-width="2"/>

  <text x="280" y="85" font-size="10">Yes</text>
  <text x="420" y="85" font-size="10">No</text>
</svg>

---

## Understanding Merge Base

The merge base is the common ancestor of branches being merged:

```bash
# Find merge base between branches
git merge-base main feature-branch

# Show merge base commit details
git show $(git merge-base main feature-branch)

# Find multiple merge bases (octopus merges)
git merge-base --all main feature-branch
```

**Why it matters:**
- Determines what changes to compare
- Affects conflict resolution
- Influences merge strategy selection
- Critical for understanding merge behavior

---

## Octopus Merges

Merging more than two branches simultaneously:

```bash
# Merge multiple branches at once
git merge branch1 branch2 branch3

# Only works if no conflicts exist
# Creates single merge commit with multiple parents
```

**Limitations:**
- No conflict resolution allowed
- All branches must merge cleanly
- Rarely used in practice
- Complex to understand and debug

**Better approach:**
- Merge branches one at a time
- Resolve conflicts individually
- Clearer history and attribution

---

## Merge Hooks

Automate merge-related tasks with `Git` hooks:

**`pre-merge-commit`:**
```bash
#!/bin/sh
# Run tests before creating merge commit
npm test || exit 1
```

**`post-merge`:**
```bash
#!/bin/sh
# Update dependencies after merge
npm install
bundle install
```

**Common uses:**
- Run automated tests
- Update dependencies
- Send notifications
- Generate documentation

---

## Advanced Merge Scenarios

**Merge with custom strategy:**
```bash
# Use specific strategy
git merge -s recursive -X theirs feature-branch
git merge -s octopus branch1 branch2 branch3
```

**Squash merge:**
```bash
# Combine all commits into one
git merge --squash feature-branch
git commit -m "Implement complete feature"
```

**No-commit merge:**
```bash
# Merge but don't commit
git merge --no-commit feature-branch
# Review changes, then commit manually
```

---

## Merge Performance Tips

1. **Keep branches small:**
    - Frequent integration reduces conflicts
    - Easier to review and test
    - Faster merge operations

1. **Use `.gitattributes` for merge strategies:**
    ```txt
    *.generated merge=ours
    package-lock.json merge=union
    ```

1. **Clean up before merging:**
    ```bash
    git clean -fd
    git reset --hard HEAD
    ```

1. **Use merge commits strategically:**
    - Preserve feature branch context
    - Group related changes
    - Maintain release points

---

## Troubleshooting Common Merge Issues

**"Already up to date" message:**
- Target branch has no new commits
- All changes already integrated
- Check branch relationships with `git log --graph`

**"Automatic merge failed":**
- Conflicts exist in files
- Manual resolution required
- Use `git status` to identify conflicted files

**"fatal: refusing to merge unrelated histories":**
```bash
# Force merge of unrelated repositories
git merge --allow-unrelated-histories other-branch
```

**Large binary file conflicts:**
- Choose one version explicitly
- Use `.gitattributes` for binary files
- Consider `Git LFS` for large files

---

## Merge Best Practices Summary

1. **Before merging:**
    - Update your local main branch
    - Test your feature branch thoroughly
    - Review the changes you're merging

1. **During merging:**
    - Read conflict markers carefully
    - Test after resolving each conflict
    - Commit with descriptive messages

1. **After merging:**
    - Delete merged feature branches
    - Push the updated main branch
    - Verify the merge in your CI/CD system

1. **Team practices:**
    - Establish merge policies
    - Use pull requests for code review
    - Maintain a clean, readable history

---

## Lab Exercise: Complex Merge Scenario

**Setup:**
1. Create a repository with conflicting changes
1. Practice different merge strategies
1. Resolve conflicts using various tools
1. Compare merge vs rebase outcomes

**Tasks:**
1. Create merge conflicts intentionally
1. Use `git mergetool` to resolve conflicts
1. Abort and retry merges with different strategies
1. Practice cherry-picking specific commits

**Goal:** Build confidence in handling any merge situation you encounter in real projects.
