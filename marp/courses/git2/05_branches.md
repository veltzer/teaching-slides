# Branches

---

## What We'll Cover

1. Theory: Why we need branches
1. How branches work internally
1. Creating and managing branches
1. Moving between branches
1. Visualizing branch activity
1. Merging strategies
1. Handling conflicts
1. Branch workflows and best practices

---

## Why Do We Need Branches?

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="40" text-anchor="middle" font-size="24" font-weight="bold">Life Without Branches</text>
  <rect x="100" y="80" width="600" height="100" fill="#FFEBEE" stroke="#C62828" stroke-width="2" rx="5"/>
  <circle cx="150" cy="130" r="20" fill="#F44336"/>
  <text x="150" y="135" text-anchor="middle" font-size="10" fill="white">v1.0</text>
  <circle cx="250" cy="130" r="20" fill="#EF5350"/>
  <text x="250" y="135" text-anchor="middle" font-size="10" fill="white">bug?</text>
  <circle cx="350" cy="130" r="20" fill="#E57373"/>
  <text x="350" y="135" text-anchor="middle" font-size="10" fill="white">feat?</text>
  <circle cx="450" cy="130" r="20" fill="#FFCDD2"/>
  <text x="450" y="135" text-anchor="middle" font-size="10">broken!</text>
  <circle cx="550" cy="130" r="20" fill="#FFEBEE"/>
  <text x="550" y="135" text-anchor="middle" font-size="10">fix?</text>
  <line x1="170" y1="130" x2="230" y2="130" stroke="#333" stroke-width="2"/>
  <line x1="270" y1="130" x2="330" y2="130" stroke="#333" stroke-width="2"/>
  <line x1="370" y1="130" x2="430" y2="130" stroke="#333" stroke-width="2"/>
  <line x1="470" y1="130" x2="530" y2="130" stroke="#333" stroke-width="2"/>
  <text x="400" y="165" text-anchor="middle" font-size="14" font-style="italic">Everything mixed together - chaos!</text>
  <rect x="100" y="200" width="600" height="150" fill="#F5F5F5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="400" y="230" text-anchor="middle" font-size="16" font-weight="bold">Problems:</text>
  <text x="120" y="260" font-size="12">• Can't work on features independently</text>
  <text x="120" y="280" font-size="12">• Broken code affects everyone</text>
  <text x="120" y="300" font-size="12">• No way to isolate experiments</text>
  <text x="120" y="320" font-size="12">• Difficult to maintain stable version</text>
</svg>

---

## The Power of Branches

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="40" text-anchor="middle" font-size="24" font-weight="bold">Life With Branches</text>
  <circle cx="100" cy="200" r="20" fill="#4CAF50"/>
  <text x="100" y="205" text-anchor="middle" font-size="10" fill="white">v1.0</text>
  <circle cx="200" cy="200" r="20" fill="#4CAF50"/>
  <text x="200" y="205" text-anchor="middle" font-size="10" fill="white">stable</text>
  <text x="150" y="180" text-anchor="middle" font-size="12">main</text>
  <circle cx="200" cy="120" r="20" fill="#2196F3"/>
  <text x="200" y="125" text-anchor="middle" font-size="10" fill="white">feat</text>
  <circle cx="300" cy="120" r="20" fill="#2196F3"/>
  <text x="300" y="125" text-anchor="middle" font-size="10" fill="white">test</text>
  <circle cx="400" cy="120" r="20" fill="#2196F3"/>
  <text x="400" y="125" text-anchor="middle" font-size="10" fill="white">done</text>
  <text x="300" y="100" text-anchor="middle" font-size="12">feature</text>
  <circle cx="200" cy="280" r="20" fill="#FF9800"/>
  <text x="200" y="285" text-anchor="middle" font-size="10" fill="white">fix</text>
  <circle cx="300" cy="280" r="20" fill="#FF9800"/>
  <text x="300" y="285" text-anchor="middle" font-size="10" fill="white">test</text>
  <text x="250" y="305" text-anchor="middle" font-size="12">hotfix</text>
  <line x1="120" y1="200" x2="180" y2="200" stroke="#333" stroke-width="2"/>
  <line x1="200" y1="180" x2="200" y2="140" stroke="#333" stroke-width="2"/>
  <line x1="220" y1="120" x2="280" y2="120" stroke="#333" stroke-width="2"/>
  <line x1="320" y1="120" x2="380" y2="120" stroke="#333" stroke-width="2"/>
  <line x1="200" y1="220" x2="200" y2="260" stroke="#333" stroke-width="2"/>
  <line x1="220" y1="280" x2="280" y2="280" stroke="#333" stroke-width="2"/>
  <rect x="450" y="100" width="300" height="200" fill="#E8F5E9" stroke="#388E3C" stroke-width="2" rx="5"/>
  <text x="600" y="130" text-anchor="middle" font-size="16" font-weight="bold">Benefits:</text>
  <text x="470" y="160" font-size="12">✓ Parallel development</text>
  <text x="470" y="180" font-size="12">✓ Isolated experiments</text>
  <text x="470" y="200" font-size="12">✓ Stable main branch</text>
  <text x="470" y="220" font-size="12">✓ Easy collaboration</text>
  <text x="470" y="240" font-size="12">✓ Feature toggles</text>
  <text x="470" y="260" font-size="12">✓ Clean history</text>
</svg>

---

## What is a Branch?

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="40" text-anchor="middle" font-size="24" font-weight="bold">Branches are Lightweight Pointers</text>
  <rect x="100" y="80" width="600" height="120" fill="#E3F2FD" stroke="#1976D2" stroke-width="2" rx="5"/>
  <text x="400" y="110" text-anchor="middle" font-size="16">A branch is just a movable pointer to a commit</text>
  <text x="400" y="135" text-anchor="middle" font-size="14">Creating a branch = Creating a 41-byte file</text>
  <text x="400" y="160" text-anchor="middle" font-size="14">Switching branches = Moving HEAD pointer</text>
  <text x="400" y="185" text-anchor="middle" font-size="14" font-weight="bold">That's why Git branches are so fast!</text>
  <rect x="150" y="220" width="120" height="60" fill="#4CAF50" rx="5"/>
  <text x="210" y="255" text-anchor="middle" font-size="14" fill="white">Commit A</text>
  <rect x="340" y="220" width="120" height="60" fill="#4CAF50" rx="5"/>
  <text x="400" y="255" text-anchor="middle" font-size="14" fill="white">Commit B</text>
  <rect x="530" y="220" width="120" height="60" fill="#4CAF50" rx="5"/>
  <text x="590" y="255" text-anchor="middle" font-size="14" fill="white">Commit C</text>
  <line x1="270" y1="250" x2="340" y2="250" stroke="#333" stroke-width="2" marker-end="url(#arrow1)"/>
  <line x1="460" y1="250" x2="530" y2="250" stroke="#333" stroke-width="2" marker-end="url(#arrow1)"/>
  <rect x="530" y="150" width="60" height="30" fill="#2196F3" rx="3"/>
  <text x="560" y="170" text-anchor="middle" font-size="12" fill="white">main</text>
  <line x1="560" y1="180" x2="590" y2="220" stroke="#2196F3" stroke-width="2" marker-end="url(#arrow1)"/>
  <rect x="600" y="150" width="60" height="30" fill="#FF9800" rx="3"/>
  <text x="630" y="170" text-anchor="middle" font-size="12" fill="white">feature</text>
  <line x1="630" y1="180" x2="590" y2="220" stroke="#FF9800" stroke-width="2" marker-end="url(#arrow1)"/>
  <text x="400" y="330" text-anchor="middle" font-size="12" font-style="italic">Both branches point to same commit - cost: 41 bytes each!</text>
  <defs>
    <marker id="arrow1" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Branch Internals

```bash
# A branch is stored in .git/refs/heads/
$ cat .git/refs/heads/main
a3f8d9c6b7e5d4c2a1b0e9f8d7c6b5a4e3d2c1b0

# That's it! Just a SHA-1 hash

# HEAD points to current branch
$ cat .git/HEAD
ref: refs/heads/main

# When on detached HEAD
$ cat .git/HEAD
a3f8d9c6b7e5d4c2a1b0e9f8d7c6b5a4e3d2c1b0

# Creating a branch is instant
$ time git branch feature
real    0m0.001s

# Even with millions of commits!
```

---

## Creating Branches

```bash
# Create new branch (doesn't switch to it)
git branch feature

# Create and switch to new branch
git checkout -b feature
# or (Git 2.23+)
git switch -c feature

# Create branch from specific commit
git branch hotfix abc123

# Create branch from tag
git branch release v1.0.0

# Create branch tracking remote
git branch --track feature origin/feature
# or
git checkout -b feature origin/feature
```

---

## Branch Naming Conventions

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="40" text-anchor="middle" font-size="24" font-weight="bold">Branch Naming Best Practices</text>
  <rect x="50" y="80" width="350" height="80" fill="#E8F5E9" stroke="#388E3C" stroke-width="2" rx="5"/>
  <text x="225" y="105" text-anchor="middle" font-size="14" font-weight="bold">Good Names ✓</text>
  <text x="70" y="130" font-size="12" font-family="monospace">feature/user-authentication</text>
  <text x="70" y="150" font-size="12" font-family="monospace">bugfix/login-error-handling</text>
  <rect x="420" y="80" width="330" height="80" fill="#FFEBEE" stroke="#C62828" stroke-width="2" rx="5"/>
  <text x="585" y="105" text-anchor="middle" font-size="14" font-weight="bold">Bad Names ✗</text>
  <text x="440" y="130" font-size="12" font-family="monospace">my-branch</text>
  <text x="440" y="150" font-size="12" font-family="monospace">test123</text>
  <rect x="50" y="180" width="700" height="180" fill="#FFF3E0" stroke="#F57C00" stroke-width="2" rx="5"/>
  <text x="400" y="210" text-anchor="middle" font-size="16" font-weight="bold">Common Prefixes</text>
  <text x="70" y="240" font-size="12"><tspan font-family="monospace">feature/</tspan> - New features</text>
  <text x="70" y="260" font-size="12"><tspan font-family="monospace">bugfix/</tspan> - Bug fixes</text>
  <text x="70" y="280" font-size="12"><tspan font-family="monospace">hotfix/</tspan> - Urgent fixes for production</text>
  <text x="70" y="300" font-size="12"><tspan font-family="monospace">release/</tspan> - Release preparation</text>
  <text x="400" y="240" font-size="12"><tspan font-family="monospace">chore/</tspan> - Maintenance tasks</text>
  <text x="400" y="260" font-size="12"><tspan font-family="monospace">docs/</tspan> - Documentation</text>
  <text x="400" y="280" font-size="12"><tspan font-family="monospace">refactor/</tspan> - Code refactoring</text>
  <text x="400" y="300" font-size="12"><tspan font-family="monospace">test/</tspan> - Test additions/changes</text>
  <text x="400" y="340" text-anchor="middle" font-size="13" font-style="italic">Use lowercase, hyphens, and be descriptive!</text>
</svg>

---

## Listing Branches

```bash
# List local branches
git branch
# * main
#   feature
#   hotfix

# List with last commit
git branch -v
# * main    a3f8d9c Latest update
#   feature b7c9e1a Add new feature
#   hotfix  c2d3e4f Fix critical bug

# List remote branches
git branch -r
# origin/main
# origin/feature

# List all branches (local + remote)
git branch -a

# List merged branches
git branch --merged

# List unmerged branches
git branch --no-merged
```

---

## Switching Branches

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="40" text-anchor="middle" font-size="24" font-weight="bold">Switching Branches Changes Working Directory</text>
  <rect x="50" y="80" width="320" height="120" fill="#E8F5E9" stroke="#388E3C" stroke-width="2" rx="5"/>
  <text x="210" y="110" text-anchor="middle" font-size="16" font-weight="bold">On main branch</text>
  <text x="70" y="135" font-size="12" font-family="monospace">index.html (v1)</text>
  <text x="70" y="155" font-size="12" font-family="monospace">style.css (v1)</text>
  <text x="70" y="175" font-size="12" font-family="monospace">app.js (v1)</text>
  <rect x="430" y="80" width="320" height="120" fill="#E3F2FD" stroke="#1976D2" stroke-width="2" rx="5"/>
  <text x="590" y="110" text-anchor="middle" font-size="16" font-weight="bold">After switch to feature</text>
  <text x="450" y="135" font-size="12" font-family="monospace">index.html (v2)</text>
  <text x="450" y="155" font-size="12" font-family="monospace">style.css (v2)</text>
  <text x="450" y="175" font-size="12" font-family="monospace">app.js (v2)</text>
  <text x="450" y="195" font-size="12" font-family="monospace">new-file.js (new!)</text>
  <path d="M 370 140 L 430 140" stroke="#333" stroke-width="3" marker-end="url(#arrow2)"/>
  <text x="400" y="130" text-anchor="middle" font-size="12">git switch feature</text>
  <rect x="200" y="240" width="400" height="120" fill="#FFEBEE" stroke="#C62828" stroke-width="2" rx="5"/>
  <text x="400" y="270" text-anchor="middle" font-size="16" font-weight="bold">⚠️ Warning: Uncommitted Changes</text>
  <text x="220" y="300" font-size="12">Git will prevent switching if you have changes that</text>
  <text x="220" y="320" font-size="12">would be overwritten. Options:</text>
  <text x="220" y="340" font-size="12">• Commit changes • Stash changes • Force switch (lose changes)</text>
  <defs>
    <marker id="arrow2" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Switch vs Checkout

```bash
# Modern way (Git 2.23+)
git switch main              # Switch to branch
git switch -c new-feature    # Create and switch
git switch -                 # Switch to previous branch

# Traditional way (still works)
git checkout main            # Switch to branch
git checkout -b new-feature  # Create and switch
git checkout -               # Switch to previous branch

# Checkout does more (can be confusing)
git checkout -- file.txt     # Discard changes (file operation)
git checkout HEAD~2          # Detached HEAD state
git checkout abc123          # Checkout specific commit

# Switch is clearer - only for branches
# Restore is for files
```

---

## HEAD and Branches

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="40" text-anchor="middle" font-size="24" font-weight="bold">Understanding HEAD</text>
  <circle cx="200" cy="200" r="30" fill="#4CAF50"/>
  <text x="200" y="205" text-anchor="middle" font-size="12" fill="white">A</text>
  <circle cx="300" cy="200" r="30" fill="#4CAF50"/>
  <text x="300" y="205" text-anchor="middle" font-size="12" fill="white">B</text>
  <circle cx="400" cy="200" r="30" fill="#4CAF50"/>
  <text x="400" y="205" text-anchor="middle" font-size="12" fill="white">C</text>
  <circle cx="500" cy="200" r="30" fill="#4CAF50"/>
  <text x="500" y="205" text-anchor="middle" font-size="12" fill="white">D</text>
  <line x1="230" y1="200" x2="270" y2="200" stroke="#333" stroke-width="2"/>
  <line x1="330" y1="200" x2="370" y2="200" stroke="#333" stroke-width="2"/>
  <line x1="430" y1="200" x2="470" y2="200" stroke="#333" stroke-width="2"/>
  <rect x="460" y="120" width="80" height="30" fill="#2196F3" rx="3"/>
  <text x="500" y="140" text-anchor="middle" font-size="12" fill="white">main</text>
  <line x1="500" y1="150" x2="500" y2="170" stroke="#2196F3" stroke-width="2" marker-end="url(#arrow3)"/>
  <rect x="360" y="280" width="80" height="30" fill="#FF9800" rx="3"/>
  <text x="400" y="300" text-anchor="middle" font-size="12" fill="white">feature</text>
  <line x1="400" y1="280" x2="400" y2="230" stroke="#FF9800" stroke-width="2" marker-end="url(#arrow3)"/>
  <rect x="320" y="80" width="80" height="30" fill="#9C27B0" rx="3"/>
  <text x="360" y="100" text-anchor="middle" font-size="14" fill="white">HEAD</text>
  <line x1="360" y1="110" x2="400" y2="280" stroke="#9C27B0" stroke-width="3" marker-end="url(#arrow3)"/>
  <text x="400" y="350" text-anchor="middle" font-size="14">HEAD → feature → Commit C</text>
  <text x="400" y="370" text-anchor="middle" font-size="12" font-style="italic">HEAD points to current branch, branch points to commit</text>
  <defs>
    <marker id="arrow3" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6"/>
    </marker>
  </defs>
</svg>

---

## Detached HEAD State

```bash
# Checkout specific commit (not branch)
git checkout abc123
# Warning: You are in 'detached HEAD' state

# What happened?
# HEAD -> abc123 (not HEAD -> branch -> commit)

# You can look around, make experimental changes
git add experimental.txt
git commit -m "Experimental change"

# To save work, create a branch
git switch -c experiment-branch

# To discard and return to branch
git switch main

# Find lost commits from detached HEAD
git reflog
```

---

## Visualizing Branches

```bash
# Simple text graph
git log --oneline --graph --all
# * a3f8d9c (HEAD -> main) Latest on main
# | * b7c9e1a (feature) Feature work
# |/
# * c2d3e4f Common ancestor

# Decorated output
git log --oneline --decorate --graph --all

# Pretty graph alias
git config --global alias.graph \
  "log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset'"

# Visual tools
gitk --all          # Built-in GUI
git gui             # Built-in GUI
# Or use: SourceTree, GitKraken, Git Graph (VS Code)
```

---

## Branch Divergence

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="40" text-anchor="middle" font-size="24" font-weight="bold">Branches Diverge Over Time</text>
  <circle cx="100" cy="200" r="25" fill="#4CAF50"/>
  <text x="100" y="205" text-anchor="middle" font-size="12" fill="white">A</text>
  <circle cx="200" cy="200" r="25" fill="#4CAF50"/>
  <text x="200" y="205" text-anchor="middle" font-size="12" fill="white">B</text>
  <circle cx="300" cy="200" r="25" fill="#4CAF50"/>
  <text x="300" y="205" text-anchor="middle" font-size="12" fill="white">C</text>
  <text x="200" y="240" text-anchor="middle" font-size="12">Common history</text>
  <circle cx="400" cy="140" r="25" fill="#2196F3"/>
  <text x="400" y="145" text-anchor="middle" font-size="12" fill="white">D</text>
  <circle cx="500" cy="140" r="25" fill="#2196F3"/>
  <text x="500" y="145" text-anchor="middle" font-size="12" fill="white">E</text>
  <text x="450" y="115" text-anchor="middle" font-size="12">main</text>
  <circle cx="400" cy="260" r="25" fill="#FF9800"/>
  <text x="400" y="265" text-anchor="middle" font-size="12" fill="white">F</text>
  <circle cx="500" cy="260" r="25" fill="#FF9800"/>
  <text x="500" y="265" text-anchor="middle" font-size="12" fill="white">G</text>
  <circle cx="600" cy="260" r="25" fill="#FF9800"/>
  <text x="600" y="265" text-anchor="middle" font-size="12" fill="white">H</text>
  <text x="500" y="290" text-anchor="middle" font-size="12">feature</text>
  <line x1="125" y1="200" x2="175" y2="200" stroke="#333" stroke-width="2"/>
  <line x1="225" y1="200" x2="275" y2="200" stroke="#333" stroke-width="2"/>
  <line x1="325" y1="190" x2="375" y2="150" stroke="#333" stroke-width="2"/>
  <line x1="325" y1="210" x2="375" y2="250" stroke="#333" stroke-width="2"/>
  <line x1="425" y1="140" x2="475" y2="140" stroke="#333" stroke-width="2"/>
  <line x1="425" y1="260" x2="475" y2="260" stroke="#333" stroke-width="2"/>
  <line x1="525" y1="260" x2="575" y2="260" stroke="#333" stroke-width="2"/>
  <rect x="200" y="320" width="400" height="60" fill="#F5F5F5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="400" y="350" text-anchor="middle" font-size="14">Branches contain different commits</text>
  <text x="400" y="370" text-anchor="middle" font-size="12">Need to merge or rebase to combine</text>
</svg>

---

## Comparing Branches

```bash
# See commits in feature not in main
git log main..feature

# See commits in main not in feature
git log feature..main

# See commits unique to each branch
git log main...feature

# Compare files between branches
git diff main..feature

# Show files changed
git diff --name-only main..feature

# Statistics
git diff --stat main..feature

# Check if branches have diverged
git merge-base main feature  # Shows common ancestor
```

---

## Deleting Branches

```bash
# Delete local branch (must not be checked out)
git branch -d feature       # Safe delete (only if merged)
git branch -D feature       # Force delete (even if unmerged)

# Delete remote branch
git push origin --delete feature
# or
git push origin :feature

# Clean up tracking branches
git remote prune origin
# or
git fetch --prune

# Delete multiple branches
git branch | grep "feature-" | xargs git branch -d

# Archive branch before deleting
git tag archive/feature feature
git branch -d feature
```
---

## Branch Management

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="40" text-anchor="middle" font-size="24" font-weight="bold">Branch Lifecycle</text>
  <rect x="50" y="80" width="150" height="80" fill="#E8F5E9" stroke="#388E3C" stroke-width="2" rx="5"/>
  <text x="125" y="110" text-anchor="middle" font-size="14" font-weight="bold">1. Create</text>
  <text x="125" y="135" text-anchor="middle" font-size="11">Branch from main</text>
  <text x="125" y="150" text-anchor="middle" font-size="10" font-family="monospace">git branch feature</text>
  <rect x="220" y="80" width="150" height="80" fill="#E3F2FD" stroke="#1976D2" stroke-width="2" rx="5"/>
  <text x="295" y="110" text-anchor="middle" font-size="14" font-weight="bold">2. Develop</text>
  <text x="295" y="135" text-anchor="middle" font-size="11">Make commits</text>
  <text x="295" y="150" text-anchor="middle" font-size="10" font-family="monospace">git commit</text>
  <rect x="390" y="80" width="150" height="80" fill="#FFF3E0" stroke="#F57C00" stroke-width="2" rx="5"/>
  <text x="465" y="110" text-anchor="middle" font-size="14" font-weight="bold">3. Merge</text>
  <text x="465" y="135" text-anchor="middle" font-size="11">Integrate changes</text>
  <text x="465" y="150" text-anchor="middle" font-size="10" font-family="monospace">git merge feature</text>
  <rect x="560" y="80" width="150" height="80" fill="#FFEBEE" stroke="#C62828" stroke-width="2" rx="5"/>
  <text x="635" y="110" text-anchor="middle" font-size="14" font-weight="bold">4. Delete</text>
  <text x="635" y="135" text-anchor="middle" font-size="11">Clean up</text>
  <text x="635" y="150" text-anchor="middle" font-size="10" font-family="monospace">git branch -d feature</text>
  <path d="M 200 120 L 220 120" stroke="#333" stroke-width="2" marker-end="url(#arrow1)"/>
  <path d="M 370 120 L 390 120" stroke="#333" stroke-width="2" marker-end="url(#arrow1)"/>
  <path d="M 540 120 L 560 120" stroke="#333" stroke-width="2" marker-end="url(#arrow1)"/>
  <rect x="200" y="200" width="400" height="140" fill="#F5F5F5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="400" y="230" text-anchor="middle" font-size="14" font-weight="bold">Best Practices</text>
  <text x="220" y="255" font-size="12">• Keep branches short-lived (days, not months)</text>
  <text x="220" y="275" font-size="12">• Delete merged branches promptly</text>
  <text x="220" y="295" font-size="12">• Use descriptive names</text>
  <text x="220" y="315" font-size="12">• One feature per branch</text>
  <defs>
    <marker id="arrow1" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Renaming Branches

```bash
# Rename current branch
git branch -m new-name

# Rename any branch
git branch -m old-name new-name

# Rename and push to remote
git branch -m old-name new-name
git push origin :old-name                # Delete old
git push origin new-name                 # Push new
git push origin -u new-name              # Set tracking

# Rename main to master (or vice versa)
git branch -m master main
git push -u origin main
git push origin --delete master

# Update local repo to use new default
git symbolic-ref refs/remotes/origin/HEAD refs/remotes/origin/main
```

---

## Branch Descriptions

```bash
# Add description to branch
git branch --edit-description feature
# Opens editor to write description

# View branch description
git config branch.feature.description

# Use in scripts/automation
#!/bin/bash
for branch in $(git branch --format='%(refname:short)'); do
    desc=$(git config branch.$branch.description)
    echo "$branch: ${desc:-No description}"
done

# Descriptions help team understand branch purpose
# Especially useful for long-running branches
```

---

## The Reflog and Branches

```bash
# See branch history
git reflog show feature
# a3f8d9c feature@{0}: commit: Add new feature
# b7c9e1a feature@{1}: branch: Created from main

# Recover deleted branch
git branch -D important-feature  # Oops!
git reflog                       # Find the SHA
git branch important-feature abc123  # Recovered!

# See when branches were updated
git for-each-ref --sort=-committerdate --format='%(committerdate:short) %(refname:short)' refs/heads/

# Find old branch positions
git log -g --grep-reflog="branch:" --oneline
```

---

## Merging Branches

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="40" text-anchor="middle" font-size="24" font-weight="bold">Types of Merges</text>
  <rect x="50" y="80" width="350" height="140" fill="#E8F5E9" stroke="#388E3C" stroke-width="2" rx="5"/>
  <text x="225" y="110" text-anchor="middle" font-size="16" font-weight="bold">Fast-Forward Merge</text>
  <circle cx="120" cy="150" r="15" fill="#4CAF50"/>
  <circle cx="180" cy="150" r="15" fill="#4CAF50"/>
  <circle cx="240" cy="150" r="15" fill="#81C784"/>
  <circle cx="300" cy="150" r="15" fill="#81C784"/>
  <line x1="135" y1="150" x2="165" y2="150" stroke="#333" stroke-width="2"/>
  <line x1="195" y1="150" x2="225" y2="150" stroke="#333" stroke-width="2"/>
  <line x1="255" y1="150" x2="285" y2="150" stroke="#333" stroke-width="2"/>
  <text x="210" y="130" font-size="10">main</text>
  <text x="270" y="130" font-size="10">feature</text>
  <text x="225" y="195" text-anchor="middle" font-size="12">Linear history - just moves pointer</text>
  <rect x="420" y="80" width="330" height="140" fill="#E3F2FD" stroke="#1976D2" stroke-width="2" rx="5"/>
  <text x="585" y="110" text-anchor="middle" font-size="16" font-weight="bold">3-Way Merge</text>
  <circle cx="480" cy="140" r="15" fill="#2196F3"/>
  <circle cx="540" cy="140" r="15" fill="#2196F3"/>
  <circle cx="540" cy="180" r="15" fill="#64B5F6"/>
  <circle cx="600" cy="160" r="15" fill="#1976D2"/>
  <line x1="495" y1="140" x2="525" y2="140" stroke="#333" stroke-width="2"/>
  <line x1="540" y1="155" x2="540" y2="165" stroke="#333" stroke-width="2"/>
  <line x1="555" y1="140" x2="585" y2="155" stroke="#333" stroke-width="2"/>
  <line x1="555" y1="180" x2="585" y2="165" stroke="#333" stroke-width="2"/>
  <text x="585" y="195" text-anchor="middle" font-size="12">Creates merge commit</text>
</svg>

---

## Fast-Forward Merge

```bash
# Scenario: feature branch is ahead of main
#   main:    A---B
#   feature:     └---C---D

git checkout main
git merge feature

# Result: Fast-forward
#   main:    A---B---C---D

# Prevent fast-forward (create merge commit)
git merge --no-ff feature

# Result:
#   main:    A---B-------M
#                 \     /
#   feature:       C---D
```

---

## Three-Way Merge

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="40" text-anchor="middle" font-size="24" font-weight="bold">Three-Way Merge Process</text>
  <circle cx="200" cy="200" r="30" fill="#4CAF50"/>
  <text x="200" y="205" text-anchor="middle" font-size="12" fill="white">Base</text>
  <text x="200" y="240" text-anchor="middle" font-size="12">Common ancestor</text>
  <circle cx="350" cy="120" r="30" fill="#2196F3"/>
  <text x="350" y="125" text-anchor="middle" font-size="12" fill="white">Ours</text>
  <text x="350" y="90" text-anchor="middle" font-size="12">main branch</text>
  <circle cx="350" cy="280" r="30" fill="#FF9800"/>
  <text x="350" y="285" text-anchor="middle" font-size="12" fill="white">Theirs</text>
  <text x="350" y="320" text-anchor="middle" font-size="12">feature branch</text>
  <circle cx="550" cy="200" r="35" fill="#9C27B0"/>
  <text x="550" y="205" text-anchor="middle" font-size="14" fill="white">Merge</text>
  <text x="550" y="250" text-anchor="middle" font-size="12">Combined result</text>
  <path d="M 230 185 L 320 135" stroke="#333" stroke-width="2" marker-end="url(#arrow2)"/>
  <path d="M 230 215 L 320 265" stroke="#333" stroke-width="2" marker-end="url(#arrow2)"/>
  <path d="M 380 120 L 515 185" stroke="#333" stroke-width="2" marker-end="url(#arrow2)"/>
  <path d="M 380 280 L 515 215" stroke="#333" stroke-width="2" marker-end="url(#arrow2)"/>
  <rect x="200" y="340" width="400" height="40" fill="#F5F5F5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="400" y="365" text-anchor="middle" font-size="12">Git finds common ancestor and combines changes from both branches</text>
  <defs>
    <marker id="arrow2" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Merge Strategies

```bash
# Default (recursive/ort)
git merge feature

# Ours - keep our version in conflicts
git merge -s ours feature

# Theirs option (not strategy)
git merge -X theirs feature

# Octopus - merge multiple branches
git merge feature1 feature2 feature3

# Subtree - merge into subdirectory
git merge -s subtree=path/to/dir feature

# No commit - prepare merge but don't commit
git merge --no-commit feature
# Review changes, then:
git commit
```

---

## Merge Conflicts

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="40" text-anchor="middle" font-size="24" font-weight="bold">Merge Conflict Anatomy</text>
  <rect x="100" y="80" width="600" height="180" fill="#FFEBEE" stroke="#C62828" stroke-width="2" rx="5"/>
  <text x="400" y="105" text-anchor="middle" font-size="14" font-weight="bold">Conflicted File</text>
  <text x="120" y="130" font-family="monospace" font-size="12">&lt;&lt;&lt;&lt;&lt;&lt;&lt; HEAD</text>
  <text x="120" y="150" font-family="monospace" font-size="12">console.log("main branch code");</text>
  <text x="120" y="170" font-family="monospace" font-size="12">=======</text>
  <text x="120" y="190" font-family="monospace" font-size="12">console.log("feature branch code");</text>
  <text x="120" y="210" font-family="monospace" font-size="12">&gt;&gt;&gt;&gt;&gt;&gt;&gt; feature</text>
  <text x="500" y="150" font-size="11">← Your current branch (HEAD)</text>
  <text x="500" y="170" font-size="11">← Separator</text>
  <text x="500" y="190" font-size="11">← Incoming branch</text>
  <rect x="150" y="280" width="500" height="80" fill="#E8F5E9" stroke="#388E3C" stroke-width="2" rx="5"/>
  <text x="400" y="310" text-anchor="middle" font-size="14" font-weight="bold">Resolution: Choose or Combine</text>
  <text x="170" y="335" font-family="monospace" font-size="12">console.log("combined solution");</text>
  <text x="170" y="350" font-family="monospace" font-size="12">// or pick one side, or write new code</text>
</svg>

---

## Resolving Merge Conflicts

```bash
# Start merge
git merge feature
# CONFLICT in file.js

# 1. Check status
git status
# Unmerged paths:
#   both modified: file.js

# 2. Open file, resolve conflicts
# Remove <<<, ===, >>> markers
# Keep desired code

# 3. Stage resolved files
git add file.js

# 4. Complete merge
git commit
# or abort:
git merge --abort
```

---

## Merge Tools

```bash
# Configure merge tool
git config --global merge.tool vimdiff

# Use merge tool during conflict
git mergetool

# Popular merge tools:
# - vimdiff      (Terminal)
# - meld         (Linux/Mac)
# - kdiff3       (Cross-platform)
# - p4merge      (Perforce, free)
# - Beyond Compare (Commercial)
# - VS Code      (Built-in)

# VS Code as merge tool
git config --global merge.tool vscode
git config --global mergetool.vscode.cmd \
  'code --wait $MERGED'
```

---

## Merge vs Rebase

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="40" text-anchor="middle" font-size="24" font-weight="bold">Merge vs Rebase</text>
  <rect x="50" y="80" width="350" height="280" fill="#E8F5E9" stroke="#388E3C" stroke-width="2" rx="5"/>
  <text x="225" y="110" text-anchor="middle" font-size="18" font-weight="bold">Merge</text>
  <circle cx="120" cy="160" r="15" fill="#4CAF50"/>
  <circle cx="180" cy="160" r="15" fill="#4CAF50"/>
  <circle cx="180" cy="210" r="15" fill="#81C784"/>
  <circle cx="240" cy="210" r="15" fill="#81C784"/>
  <circle cx="300" cy="160" r="15" fill="#66BB6A"/>
  <text x="300" y="165" text-anchor="middle" font-size="10" fill="white">M</text>
  <line x1="135" y1="160" x2="165" y2="160" stroke="#333" stroke-width="2"/>
  <line x1="180" y1="175" x2="180" y2="195" stroke="#333" stroke-width="2"/>
  <line x1="195" y1="210" x2="225" y2="210" stroke="#333" stroke-width="2"/>
  <line x1="195" y1="160" x2="285" y2="160" stroke="#333" stroke-width="2"/>
  <line x1="255" y1="210" x2="285" y2="170" stroke="#333" stroke-width="2"/>
  <text x="225" y="250" text-anchor="middle" font-size="12">✓ Preserves history</text>
  <text x="225" y="270" text-anchor="middle" font-size="12">✓ Shows branches</text>
  <text x="225" y="290" text-anchor="middle" font-size="12">✗ Merge commits</text>
  <text x="225" y="310" text-anchor="middle" font-size="12">✗ Complex history</text>
  <rect x="420" y="80" width="330" height="280" fill="#E3F2FD" stroke="#1976D2" stroke-width="2" rx="5"/>
  <text x="585" y="110" text-anchor="middle" font-size="18" font-weight="bold">Rebase</text>
  <circle cx="480" cy="160" r="15" fill="#2196F3"/>
  <circle cx="540" cy="160" r="15" fill="#2196F3"/>
  <circle cx="600" cy="160" r="15" fill="#64B5F6"/>
  <circle cx="660" cy="160" r="15" fill="#64B5F6"/>
  <line x1="495" y1="160" x2="525" y2="160" stroke="#333" stroke-width="2"/>
  <line x1="555" y1="160" x2="585" y2="160" stroke="#333" stroke-width="2"/>
  <line x1="615" y1="160" x2="645" y2="160" stroke="#333" stroke-width="2"/>
  <text x="585" y="250" text-anchor="middle" font-size="12">✓ Linear history</text>
  <text x="585" y="270" text-anchor="middle" font-size="12">✓ Clean timeline</text>
  <text x="585" y="290" text-anchor="middle" font-size="12">✗ Rewrites history</text>
  <text x="585" y="310" text-anchor="middle" font-size="12">✗ Loses branch context</text>
</svg>

---

## Rebase Workflow

```bash
# Rebase feature onto main
git checkout feature
git rebase main

# Interactive rebase to clean history
git rebase -i main

# If conflicts occur:
# 1. Fix conflicts
git add fixed-file.js
# 2. Continue rebase
git rebase --continue
# Or abort:
git rebase --abort

# Pull with rebase (avoid merge commits)
git pull --rebase origin main

# Configure pull to always rebase
git config pull.rebase true
```

---

## When to Merge vs Rebase

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="40" text-anchor="middle" font-size="24" font-weight="bold">Choosing Between Merge and Rebase</text>
  <rect x="50" y="80" width="350" height="120" fill="#E8F5E9" stroke="#388E3C" stroke-width="2" rx="5"/>
  <text x="225" y="110" text-anchor="middle" font-size="16" font-weight="bold">Use Merge When:</text>
  <text x="70" y="135" font-size="12">• Working on shared branches</text>
  <text x="70" y="155" font-size="12">• Want to preserve branch history</text>
  <text x="70" y="175" font-size="12">• After pushing to remote</text>
  <rect x="420" y="80" width="330" height="120" fill="#E3F2FD" stroke="#1976D2" stroke-width="2" rx="5"/>
  <text x="585" y="110" text-anchor="middle" font-size="16" font-weight="bold">Use Rebase When:</text>
  <text x="440" y="135" font-size="12">• Cleaning local commits</text>
  <text x="440" y="155" font-size="12">• Before pushing feature branch</text>
  <text x="440" y="175" font-size="12">• Want linear history</text>
  <rect x="150" y="220" width="500" height="140" fill="#FFEBEE" stroke="#C62828" stroke-width="2" rx="5"/>
  <text x="400" y="250" text-anchor="middle" font-size="16" font-weight="bold">⚠️ Golden Rule of Rebase</text>
  <text x="400" y="280" text-anchor="middle" font-size="14" font-weight="bold">Never rebase public branches!</text>
  <text x="170" y="310" font-size="12">If others have based work on your commits,</text>
  <text x="170" y="330" font-size="12">rebase will cause problems. Use merge instead.</text>
</svg>

---

## Advanced Branch Patterns

```bash
# Create orphan branch (no parent)
git checkout --orphan new-root
git rm -rf .
# Add new files
git add .
git commit -m "New root commit"

# Track different remote branch
git branch -u origin/different-branch

# Push to different remote branch name
git push origin local-branch:remote-branch

# Create branch from stash
git stash branch new-feature stash@{1}

# Backup branch before dangerous operation
git branch backup-$(date +%Y%m%d-%H%M%S)
```

---

## Branch Protection Strategies

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="40" text-anchor="middle" font-size="24" font-weight="bold">Protecting Important Branches</text>
  <rect x="100" y="80" width="600" height="60" fill="#4CAF50" rx="5"/>
  <text x="400" y="105" text-anchor="middle" font-size="16" fill="white" font-weight="bold">Protected: main branch</text>
  <text x="400" y="125" text-anchor="middle" font-size="12" fill="white">Requires pull request, reviews, passing tests</text>
  <rect x="50" y="160" width="320" height="180" fill="#E8F5E9" stroke="#388E3C" stroke-width="2" rx="5"/>
  <text x="210" y="190" text-anchor="middle" font-size="14" font-weight="bold">Local Protection</text>
  <text x="70" y="215" font-size="11">Pre-push hook example:</text>
  <text x="70" y="235" font-family="monospace" font-size="10">#!/bin/sh</text>
  <text x="70" y="250" font-family="monospace" font-size="10">branch=$(git symbolic-ref HEAD)</text>
  <text x="70" y="265" font-family="monospace" font-size="10">if [ "$branch" = "refs/heads/main" ]</text>
  <text x="70" y="280" font-family="monospace" font-size="10">then</text>
  <text x="70" y="295" font-family="monospace" font-size="10">  echo "Direct push to main blocked"</text>
  <text x="70" y="310" font-family="monospace" font-size="10">  exit 1</text>
  <text x="70" y="325" font-family="monospace" font-size="10">fi</text>
  <rect x="430" y="160" width="320" height="180" fill="#FFF3E0" stroke="#F57C00" stroke-width="2" rx="5"/>
  <text x="590" y="190" text-anchor="middle" font-size="14" font-weight="bold">Remote Protection (GitHub/GitLab)</text>
  <text x="450" y="215" font-size="11">• Require pull request reviews</text>
  <text x="450" y="235" font-size="11">• Dismiss stale reviews</text>
  <text x="450" y="255" font-size="11">• Require status checks</text>
  <text x="450" y="275" font-size="11">• Include administrators</text>
  <text x="450" y="295" font-size="11">• Restrict who can push</text>
  <text x="450" y="315" font-size="11">• Prevent force pushes</text>
</svg>

---

## Gitflow Workflow

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="40" text-anchor="middle" font-size="24" font-weight="bold">Gitflow Branch Model</text>
  <line x1="100" y1="100" x2="700" y2="100" stroke="#4CAF50" stroke-width="3"/>
  <text x="50" y="105" font-size="12">main</text>
  <circle cx="150" cy="100" r="8" fill="#4CAF50"/>
  <circle cx="650" cy="100" r="8" fill="#4CAF50"/>
  <line x1="100" y1="160" x2="700" y2="160" stroke="#2196F3" stroke-width="3"/>
  <text x="50" y="165" font-size="12">develop</text>
  <line x1="200" y1="160" x2="250" y2="220" stroke="#FF9800" stroke-width="2"/>
  <line x1="250" y1="220" x2="350" y2="220" stroke="#FF9800" stroke-width="2"/>
  <line x1="350" y1="220" x2="400" y2="160" stroke="#FF9800" stroke-width="2"/>
  <text x="300" y="240" text-anchor="middle" font-size="11">feature/</text>
  <line x1="450" y1="160" x2="500" y2="100" stroke="#9C27B0" stroke-width="2"/>
  <line x1="500" y1="100" x2="550" y2="100" stroke="#9C27B0" stroke-width="2"/>
  <line x1="550" y1="100" x2="600" y2="160" stroke="#9C27B0" stroke-width="2"/>
  <text x="525" y="90" text-anchor="middle" font-size="11">release/</text>
  <line x1="300" y1="100" x2="320" y2="70" stroke="#F44336" stroke-width="2"/>
  <line x1="320" y1="70" x2="340" y2="70" stroke="#F44336" stroke-width="2"/>
  <line x1="340" y1="70" x2="360" y2="100" stroke="#F44336" stroke-width="2"/>
  <text x="330" y="60" text-anchor="middle" font-size="11">hotfix/</text>
  <rect x="150" y="280" width="500" height="80" fill="#F5F5F5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="400" y="305" text-anchor="middle" font-size="12" font-weight="bold">Branch Types:</text>
  <text x="170" y="325" font-size="11">• main: Production-ready code</text>
  <text x="170" y="345" font-size="11">• develop: Integration branch</text>
  <text x="420" y="325" font-size="11">• feature/: New features</text>
  <text x="420" y="345" font-size="11">• release/: Release prep • hotfix/: Emergency fixes</text>
</svg>
