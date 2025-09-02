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
