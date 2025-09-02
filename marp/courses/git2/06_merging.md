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
