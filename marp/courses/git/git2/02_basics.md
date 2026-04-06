# Git Basics

---

## What We'll Cover

1. Setting up a local repository
1. Working with clients (local and remote)
1. Understanding the staging area
1. Essential Git commands
1. Undoing changes
1. Viewing differences
1. Making commits
1. Exploring history

---

## Installing Git

### Linux (Debian/Ubuntu)
```bash
sudo apt-get update
sudo apt-get install git
```

### Linux (Fedora/RHEL)
```bash
sudo dnf install git
# or
sudo yum install git
```

### macOS
```bash
# With Homebrew
brew install git
# Or install Xcode Command Line Tools
```

### Windows
- Download from https://git-scm.com
- Or use Git Bash / WSL

---

## Verify Installation

```bash
$ git --version
git version 2.42.0
```

**First-time setup is crucial!**

```bash
# Set your identity
git config --global user.name "Your Name"
git config --global user.email "you@example.com"

# Check your settings
git config --list
```

### These will be attached to every commit you make

---

## Creating a Repository

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="40" text-anchor="middle" font-size="24" font-weight="bold">Two Ways to Start</text>
  <rect x="50" y="80" width="300" height="280" fill="#E8F5E9" stroke="#2E7D32" stroke-width="2" rx="5"/>
  <text x="200" y="120" text-anchor="middle" font-size="20" font-weight="bold">Option 1: New Repo</text>
  <rect x="75" y="150" width="250" height="40" fill="#4CAF50" rx="3"/>
  <text x="200" y="175" text-anchor="middle" font-size="14" fill="white">mkdir myproject</text>
  <rect x="75" y="200" width="250" height="40" fill="#4CAF50" rx="3"/>
  <text x="200" y="225" text-anchor="middle" font-size="14" fill="white">cd myproject</text>
  <rect x="75" y="250" width="250" height="40" fill="#4CAF50" rx="3"/>
  <text x="200" y="275" text-anchor="middle" font-size="14" fill="white">git init</text>
  <text x="200" y="320" text-anchor="middle" font-size="14" font-style="italic">Creates .git directory</text>
  <rect x="450" y="80" width="300" height="280" fill="#E3F2FD" stroke="#1565C0" stroke-width="2" rx="5"/>
  <text x="600" y="120" text-anchor="middle" font-size="20" font-weight="bold">Option 2: Clone</text>
  <rect x="475" y="150" width="250" height="60" fill="#2196F3" rx="3"/>
  <text x="600" y="185" text-anchor="middle" font-size="14" fill="white">git clone [url]</text>
  <text x="600" y="250" text-anchor="middle" font-size="14" font-style="italic">Downloads entire</text>
  <text x="600" y="270" text-anchor="middle" font-size="14" font-style="italic">repository with history</text>
</svg>

---

## The `.git` Directory

```bash
$ ls -la
total 12
drwxr-xr-x  3 user user 4096 Jan 15 10:00 .
drwxr-xr-x 10 user user 4096 Jan 15 09:59 ..
drwxr-xr-x  7 user user 4096 Jan 15 10:00 .git
```

**What's inside `.git`?**
- `HEAD` - Points to current branch
- `config` - Repository configuration
- `objects/` - All your data (commits, files)
- `refs/` - Pointers to commits (branches, tags)
- `index` - Staging area

*Don't manually edit these files unless you know what you're doing!*

---

## Git Init vs Clone

| `git init` | `git clone` |
|------------|-------------|
| Creates new repository | Copies existing repository |
| Empty history | Full history included |
| No remote configured | Remote "origin" configured |
| No files | All files from source |
| Local only | Ready to push/pull |

**When to use which?**
- `init`: Starting a brand new project
- `clone`: Contributing to existing project

---

## Understanding Working Directory

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="40" text-anchor="middle" font-size="24" font-weight="bold">File Status Lifecycle</text>
  <circle cx="150" cy="150" r="40" fill="#9E9E9E"/>
  <text x="150" y="155" text-anchor="middle" font-size="14" fill="white">Untracked</text>
  <circle cx="350" cy="150" r="40" fill="#4CAF50"/>
  <text x="350" y="155" text-anchor="middle" font-size="14" fill="white">Unmodified</text>
  <circle cx="550" cy="150" r="40" fill="#FF9800"/>
  <text x="550" y="155" text-anchor="middle" font-size="14" fill="white">Modified</text>
  <circle cx="650" cy="250" r="40" fill="#2196F3"/>
  <text x="650" y="255" text-anchor="middle" font-size="14" fill="white">Staged</text>
  <path d="M 190 150 L 310 150" stroke="#333" stroke-width="2" marker-end="url(#arrow4)"/>
  <text x="250" y="140" text-anchor="middle" font-size="12">Add file</text>
  <path d="M 390 150 L 510 150" stroke="#333" stroke-width="2" marker-end="url(#arrow4)"/>
  <text x="450" y="140" text-anchor="middle" font-size="12">Edit file</text>
  <path d="M 570 180 L 630 220" stroke="#333" stroke-width="2" marker-end="url(#arrow4)"/>
  <text x="600" y="195" text-anchor="middle" font-size="12">Stage file</text>
  <path d="M 610 250 Q 450 320 350 190" stroke="#333" stroke-width="2" marker-end="url(#arrow4)"/>
  <text x="480" y="310" text-anchor="middle" font-size="12">Commit</text>
  <path d="M 530 120 Q 450 50 170 120" stroke="#FF5722" stroke-width="2" marker-end="url(#arrow4)"/>
  <text x="350" y="70" text-anchor="middle" font-size="12" fill="#FF5722">Remove file</text>
  <defs>
    <marker id="arrow4" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Checking Status

```bash
$ git status
On branch main
Your branch is up to date with 'origin/main'.

Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
        modified:   README.md

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
        modified:   app.js

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        config.json
```

**Three sections to watch:**
1. Changes to be committed (staged)
1. Changes not staged (modified but not staged)
1. Untracked files (new files)

---

## Short Status

```bash
$ git status -s
 M README.md    # Modified in working directory
M  index.html   # Modified and staged
MM styles.css   # Modified, staged, then modified again
A  new.js       # New file, staged
?? config.json  # Untracked
```

**Left column**: Staging area status
**Right column**: Working directory status

---

## The Staging Area (Index)

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="40" text-anchor="middle" font-size="24" font-weight="bold">Why Stage Files?</text>
  <rect x="50" y="80" width="200" height="250" fill="#FFEBEE" stroke="#C62828" stroke-width="2" rx="5"/>
  <text x="150" y="110" text-anchor="middle" font-size="16" font-weight="bold">Working Directory</text>
  <rect x="70" y="130" width="160" height="30" fill="#EF5350"/>
  <text x="150" y="150" text-anchor="middle" font-size="12" fill="white">feature.js (500 lines)</text>
  <rect x="70" y="170" width="160" height="30" fill="#EF5350"/>
  <text x="150" y="190" text-anchor="middle" font-size="12" fill="white">bugfix.js (50 lines)</text>
  <rect x="70" y="210" width="160" height="30" fill="#EF5350"/>
  <text x="150" y="230" text-anchor="middle" font-size="12" fill="white">README.md (docs)</text>
  <rect x="70" y="250" width="160" height="30" fill="#EF5350"/>
  <text x="150" y="270" text-anchor="middle" font-size="12" fill="white">debug.log (testing)</text>
  <rect x="300" y="80" width="200" height="250" fill="#E8F5E9" stroke="#2E7D32" stroke-width="2" rx="5"/>
  <text x="400" y="110" text-anchor="middle" font-size="16" font-weight="bold">Staging Area</text>
  <rect x="320" y="170" width="160" height="30" fill="#66BB6A"/>
  <text x="400" y="190" text-anchor="middle" font-size="12" fill="white">bugfix.js</text>
  <text x="400" y="250" text-anchor="middle" font-size="14" font-style="italic">Only commit</text>
  <text x="400" y="270" text-anchor="middle" font-size="14" font-style="italic">the bugfix!</text>
  <rect x="550" y="80" width="200" height="250" fill="#E3F2FD" stroke="#1565C0" stroke-width="2" rx="5"/>
  <text x="650" y="110" text-anchor="middle" font-size="16" font-weight="bold">Repository</text>
  <rect x="570" y="170" width="160" height="30" fill="#42A5F5"/>
  <text x="650" y="190" text-anchor="middle" font-size="12" fill="white">Commit: Fix bug #123</text>
  <path d="M 250 185 L 300 185" stroke="#333" stroke-width="3" marker-end="url(#arrow5)"/>
  <text x="275" y="175" text-anchor="middle" font-size="11">git add</text>
  <path d="M 500 185 L 550 185" stroke="#333" stroke-width="3" marker-end="url(#arrow5)"/>
  <text x="525" y="175" text-anchor="middle" font-size="11">git commit</text>
  <defs>
    <marker id="arrow5" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Git Add - Adding to Stage

```bash
# Add specific file
git add README.md

# Add multiple files
git add file1.js file2.js

# Add all files in directory
git add .

# Add all modified files (not new ones)
git add -u

# Add everything (modified, new, deleted)
git add -A

# Interactive add (choose chunks)
git add -p
```

**Pro tip**: Use `git add -p` to review and stage specific changes

---

## Interactive Staging

```bash
$ git add -p
diff --git a/app.js b/app.js
@@ -10,6 +10,8 @@ function main() {
     console.log("Starting app");
+    // New feature code
+    processData();
 }

Stage this hunk [y,n,q,a,d,e,?]?
```

**Options:**
- `y` - Stage this hunk
- `n` - Don't stage this hunk
- `s` - Split into smaller hunks
- `e` - Manually edit the hunk
- `q` - Quit

---

## Git Stage (Synonym)

```bash
# These are equivalent
git add file.txt
git stage file.txt

# Both work the same way
git add -p
git stage -p
```

**Note**: `git stage` was added for clarity, but `git add` is more commonly used

---

## Removing Files

```bash
# Remove file from working directory AND stage removal
git rm file.txt

# Keep file in working directory but remove from tracking
git rm --cached file.txt

# Remove directory
git rm -r directory/

# Remove with pattern
git rm '*.log'
```

**Important**: `git rm` removes the file from your filesystem!

---

## Moving/Renaming Files

```bash
# Rename file
git mv old_name.txt new_name.txt

# Move to different directory
git mv file.txt directory/file.txt

# This is equivalent to:
mv old_name.txt new_name.txt
git rm old_name.txt
git add new_name.txt
```

### Git tracks this as a rename, preserving history

---

## Undoing Staged Changes

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="40" text-anchor="middle" font-size="24" font-weight="bold">Unstaging Files</text>
  <rect x="100" y="100" width="250" height="60" fill="#FFCDD2" stroke="#D32F2F" stroke-width="2" rx="5"/>
  <text x="225" y="135" text-anchor="middle" font-size="16">git restore --staged file</text>
  <text x="225" y="190" text-anchor="middle" font-size="14">Removes from staging area</text>
  <text x="225" y="210" text-anchor="middle" font-size="14">Keeps changes in working dir</text>
  <rect x="450" y="100" width="250" height="60" fill="#FFE0B2" stroke="#F57C00" stroke-width="2" rx="5"/>
  <text x="575" y="135" text-anchor="middle" font-size="16">git reset HEAD file</text>
  <text x="575" y="190" text-anchor="middle" font-size="14">Alternative method</text>
  <text x="575" y="210" text-anchor="middle" font-size="14">Same effect</text>
  <rect x="275" y="250" width="250" height="60" fill="#C8E6C9" stroke="#388E3C" stroke-width="2" rx="5"/>
  <text x="400" y="285" text-anchor="middle" font-size="16">git reset</text>
  <text x="400" y="330" text-anchor="middle" font-size="14">Unstages ALL files</text>
</svg>

---

## Viewing Differences

```bash
# Changes in working directory (not staged)
git diff

# Changes staged for commit
git diff --staged
# or
git diff --cached

# Compare with specific commit
git diff HEAD

# Compare two branches
git diff main feature-branch

# Show only file names
git diff --name-only
```

---

## Understanding Git Diff Output

```diff
diff --git a/README.md b/README.md
index 3b18e51..2f4e349 100644
--- a/README.md
+++ b/README.md
@@ -1,4 +1,5 @@
 # My Project

-This is my project
+This is my awesome project
+Now with more features!

```

**Reading the diff:**
- `---` Old version
- `+++` New version
- `@@ -1,4 +1,5 @@` Line numbers (old and new)
- `-` Line removed
- `+` Line added

---

## Making Commits

```bash
# Commit with message
git commit -m "Add user authentication"

# Commit with detailed message (opens editor)
git commit

# Commit all modified tracked files (skip staging)
git commit -a -m "Update all files"

# Amend last commit
git commit --amend

# Commit with signature
git commit -S -m "Signed commit"
```

---

## Writing Good Commit Messages

<svg viewBox="0 0 800 450" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="40" text-anchor="middle" font-size="24" font-weight="bold">Commit Message Format</text>
  <rect x="100" y="80" width="600" height="320" fill="#F5F5F5" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="120" y="100" width="560" height="40" fill="#4CAF50"/>
  <text x="400" y="125" text-anchor="middle" font-size="16" fill="white">Subject line (50 chars or less)</text>
  <line x1="120" y1="160" x2="680" y2="160" stroke="#999" stroke-width="1" stroke-dasharray="5,5"/>
  <text x="400" y="155" text-anchor="middle" font-size="12" fill="#666">Blank line</text>
  <rect x="120" y="180" width="560" height="120" fill="#E3F2FD"/>
  <text x="130" y="205" font-size="14">Detailed explanation of what and why (72 char wrap)</text>
  <text x="130" y="230" font-size="14">- Explain the problem this commit solves</text>
  <text x="130" y="255" font-size="14">- Justify the approach taken</text>
  <text x="130" y="280" font-size="14">- Reference issues: Fixes #123</text>
  <rect x="120" y="320" width="200" height="60" fill="#C8E6C9" stroke="#388E3C" stroke-width="2" rx="3"/>
  <text x="220" y="345" text-anchor="middle" font-size="14" font-weight="bold">DO</text>
  <text x="220" y="365" text-anchor="middle" font-size="12">Imperative mood</text>
  <rect x="340" y="320" width="200" height="60" fill="#C8E6C9" stroke="#388E3C" stroke-width="2" rx="3"/>
  <text x="440" y="345" text-anchor="middle" font-size="14" font-weight="bold">DO</text>
  <text x="440" y="365" text-anchor="middle" font-size="12">Explain why</text>
  <rect x="560" y="320" width="120" height="60" fill="#FFCDD2" stroke="#D32F2F" stroke-width="2" rx="3"/>
  <text x="620" y="345" text-anchor="middle" font-size="14" font-weight="bold">DON'T</text>
  <text x="620" y="365" text-anchor="middle" font-size="12">Just say what</text>
</svg>

---

## Commit Message Examples

## Good ✅
```template
Fix race condition in user session handler

The session handler was not thread-safe when multiple
requests tried to update the same session. Added mutex
locks around critical sections.

Fixes #456
```

## Bad ❌
```template
updated stuff
```
```template
Fixed bug
```
```template
Changes
```

---

## Viewing Commit History

```bash
# Basic log
git log

# One line per commit
git log --oneline

# With graph
git log --graph --oneline

# Show last n commits
git log -3

# Show commits by author
git log --author="John"

# Show commits since date
git log --since="2 weeks ago"

# Show commits with stats
git log --stat
```

---

## Customizing Log Output

```bash
# Pretty formats
git log --pretty=oneline
git log --pretty=short
git log --pretty=full

# Custom format
git log --pretty=format:"%h - %an, %ar : %s"

# With decorations (branch/tag names)
git log --oneline --decorate

# Follow file history through renames
git log --follow file.txt
```

### Output example:
```output
a3d8f2c - John Doe, 2 hours ago : Add login feature
b7c9e1a - Jane Smith, 5 hours ago : Fix database connection
```

---

## Searching History

```bash
# Search commit messages
git log --grep="bugfix"

# Search code changes
git log -S"function_name"

# Search with regex
git log -G"regex.*pattern"

# Find commits that changed specific lines
git log -L 10,20:file.txt

# Combine searches
git log --author="John" --since="2024-01-01" --grep="feature"
```

---

## Git Grep - Search Working Directory

```bash
# Search for pattern in tracked files
git grep "TODO"

# Search with line numbers
git grep -n "pattern"

# Search only in specific files
git grep "pattern" -- "*.js"

# Count matches
git grep -c "pattern"

# Search in specific commit
git grep "pattern" HEAD~3
```

**Advantages over regular `grep`:**
- Only searches tracked files
- Faster for large repositories
- Can search in any commit

---

## Understanding References

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="40" text-anchor="middle" font-size="24" font-weight="bold">Git References</text>
  <circle cx="150" cy="200" r="30" fill="#4CAF50"/>
  <text x="150" y="207" text-anchor="middle" font-size="12" fill="white">C1</text>
  <circle cx="250" cy="200" r="30" fill="#4CAF50"/>
  <text x="250" y="207" text-anchor="middle" font-size="12" fill="white">C2</text>
  <circle cx="350" cy="200" r="30" fill="#4CAF50"/>
  <text x="350" y="207" text-anchor="middle" font-size="12" fill="white">C3</text>
  <circle cx="450" cy="200" r="30" fill="#4CAF50"/>
  <text x="450" y="207" text-anchor="middle" font-size="12" fill="white">C4</text>
  <line x1="180" y1="200" x2="220" y2="200" stroke="#333" stroke-width="2"/>
  <line x1="280" y1="200" x2="320" y2="200" stroke="#333" stroke-width="2"/>
  <line x1="380" y1="200" x2="420" y2="200" stroke="#333" stroke-width="2"/>
  <rect x="400" y="100" width="100" height="30" fill="#2196F3" rx="3"/>
  <text x="450" y="120" text-anchor="middle" font-size="12" fill="white">HEAD</text>
  <line x1="450" y1="130" x2="450" y2="170" stroke="#2196F3" stroke-width="2" marker-end="url(#arrow6)"/>
  <rect x="500" y="140" width="100" height="30" fill="#FF9800" rx="3"/>
  <text x="550" y="160" text-anchor="middle" font-size="12" fill="white">main</text>
  <line x1="520" y1="170" x2="470" y2="185" stroke="#FF9800" stroke-width="2" marker-end="url(#arrow6)"/>
  <text x="150" y="260" text-anchor="middle" font-size="12">HEAD~3</text>
  <text x="250" y="260" text-anchor="middle" font-size="12">HEAD~2</text>
  <text x="350" y="260" text-anchor="middle" font-size="12">HEAD~1</text>
  <text x="450" y="260" text-anchor="middle" font-size="12">HEAD</text>
  <rect x="100" y="300" width="600" height="60" fill="#FFF9C4" stroke="#F57F17" stroke-width="2" rx="5"/>
  <text x="400" y="335" text-anchor="middle" font-size="14">HEAD^ = parent commit, HEAD~n = n commits back</text>
  <defs>
    <marker id="arrow6" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Relative References

```bash
# Parent commits
HEAD^   # Parent of HEAD
HEAD^^  # Grandparent of HEAD
HEAD~1  # Same as HEAD^
HEAD~2  # Same as HEAD^^
HEAD~10 # 10 commits back

# Branch references
main^       # Parent of main tip
feature~3   # 3 commits back from feature

# Combining references
HEAD^2  # Second parent (for merge commits)
HEAD~3^2  # Complex navigation
```

---

## Undoing Working Directory Changes

```bash
# Discard changes in working directory
git restore file.txt

# Restore to specific version
git restore --source HEAD~2 file.txt

# Restore all files
git restore .

# Old way (still works)
git checkout -- file.txt
```

**⚠️ Warning**: This permanently discards uncommitted changes!

---

## The Reset Command

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="40" text-anchor="middle" font-size="24" font-weight="bold">Three Types of Reset</text>
  <rect x="50" y="80" width="220" height="280" fill="#E8F5E9" stroke="#388E3C" stroke-width="2" rx="5"/>
  <text x="160" y="115" text-anchor="middle" font-size="18" font-weight="bold">--soft</text>
  <text x="160" y="145" text-anchor="middle" font-size="12">Moves HEAD</text>
  <rect x="80" y="170" width="160" height="40" fill="#81C784"/>
  <text x="160" y="195" text-anchor="middle" font-size="12" fill="white">✓ Keep changes staged</text>
  <rect x="80" y="220" width="160" height="40" fill="#81C784"/>
  <text x="160" y="245" text-anchor="middle" font-size="12" fill="white">✓ Keep working dir</text>
  <text x="160" y="290" text-anchor="middle" font-size="12">Use: Redo commit message</text>
  <rect x="290" y="80" width="220" height="280" fill="#FFF3E0" stroke="#F57C00" stroke-width="2" rx="5"/>
  <text x="400" y="115" text-anchor="middle" font-size="18" font-weight="bold">--mixed (default)</text>
  <text x="400" y="145" text-anchor="middle" font-size="12">Moves HEAD + Index</text>
  <rect x="320" y="170" width="160" height="40" fill="#EF6C00"/>
  <text x="400" y="195" text-anchor="middle" font-size="12" fill="white">✗ Unstage changes</text>
  <rect x="320" y="220" width="160" height="40" fill="#81C784"/>
  <text x="400" y="245" text-anchor="middle" font-size="12" fill="white">✓ Keep working dir</text>
  <text x="400" y="290" text-anchor="middle" font-size="12">Use: Unstage everything</text>
  <rect x="530" y="80" width="220" height="280" fill="#FFEBEE" stroke="#C62828" stroke-width="2" rx="5"/>
  <text x="640" y="115" text-anchor="middle" font-size="18" font-weight="bold">--hard</text>
  <text x="640" y="145" text-anchor="middle" font-size="12">Moves everything</text>
  <rect x="560" y="170" width="160" height="40" fill="#D32F2F"/>
  <text x="640" y="195" text-anchor="middle" font-size="12" fill="white">✗ Discard staged</text>
  <rect x="560" y="220" width="160" height="40" fill="#D32F2F"/>
  <text x="640" y="245" text-anchor="middle" font-size="12" fill="white">✗ Discard working dir</text>
  <text x="640" y="290" text-anchor="middle" font-size="12">⚠️ DESTRUCTIVE!</text>
</svg>

---

## Reset Examples

```bash
# Undo last commit, keep changes staged
git reset --soft HEAD~1

# Undo last commit, unstage changes
git reset HEAD~1
# or
git reset --mixed HEAD~1

# Completely undo last 2 commits (DANGEROUS!)
git reset --hard HEAD~2

# Unstage specific file
git reset HEAD file.txt

# Reset to specific commit
git reset abc123def
```

---

## Clean - Remove Untracked Files

```bash
# Show what would be removed (dry run)
git clean -n

# Remove untracked files
git clean -f

# Remove untracked files and directories
git clean -fd

# Remove ignored files too
git clean -fx

# Interactive mode
git clean -i
```

**⚠️ Be careful**: `git clean` permanently deletes files!

---

## Stashing Changes

```bash
# Save current changes to stash
git stash

# Stash with message
git stash save "Work in progress on feature X"

# List stashes
git stash list

# Apply most recent stash
git stash apply

# Apply and remove from stash
git stash pop

# Apply specific stash
git stash apply stash@{2}
```

---

## Working with Stash

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="40" text-anchor="middle" font-size="24" font-weight="bold">Stash Workflow</text>
  <rect x="50" y="80" width="200" height="100" fill="#FFCDD2" stroke="#D32F2F" stroke-width="2" rx="5"/>
  <text x="150" y="115" text-anchor="middle" font-size="14" font-weight="bold">Working on Feature</text>
  <text x="150" y="140" text-anchor="middle" font-size="12">Uncommitted changes</text>
  <text x="150" y="160" text-anchor="middle" font-size="12">Boss: "Fix bug NOW!"</text>
  <rect x="300" y="80" width="200" height="100" fill="#E3F2FD" stroke="#1976D2" stroke-width="2" rx="5"/>
  <text x="400" y="115" text-anchor="middle" font-size="14" font-weight="bold">git stash</text>
  <text x="400" y="140" text-anchor="middle" font-size="12">Save work temporarily</text>
  <text x="400" y="160" text-anchor="middle" font-size="12">Clean working directory</text>
  <rect x="550" y="80" width="200" height="100" fill="#C8E6C9" stroke="#388E3C" stroke-width="2" rx="5"/>
  <text x="650" y="115" text-anchor="middle" font-size="14" font-weight="bold">Fix Bug</text>
  <text x="650" y="140" text-anchor="middle" font-size="12">Switch branch</text>
  <text x="650" y="160" text-anchor="middle" font-size="12">Commit fix</text>
  <rect x="300" y="220" width="200" height="100" fill="#E1BEE7" stroke="#7B1FA2" stroke-width="2" rx="5"/>
  <text x="400" y="255" text-anchor="middle" font-size="14" font-weight="bold">git stash pop</text>
  <text x="400" y="280" text-anchor="middle" font-size="12">Restore work</text>
  <text x="400" y="300" text-anchor="middle" font-size="12">Continue feature</text>
  <path d="M 250 130 L 300 130" stroke="#333" stroke-width="2" marker-end="url(#arrow7)"/>
  <path d="M 500 130 L 550 130" stroke="#333" stroke-width="2" marker-end="url(#arrow7)"/>
  <path d="M 650 180 Q 650 200 500 220" stroke="#333" stroke-width="2" marker-end="url(#arrow7)"/>
  <path d="M 300 270 Q 150 270 150 180" stroke="#333" stroke-width="2" marker-end="url(#arrow7)"/>
  <defs>
    <marker id="arrow7" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Advanced Stash Operations

```bash
# Stash including untracked files
git stash -u

# Stash including ignored files
git stash -a

# Create branch from stash
git stash branch new-branch stash@{0}

# Show stash contents
git stash show stash@{0}
git stash show -p stash@{0}  # with diff

# Drop specific stash
git stash drop stash@{1}

# Clear all stashes
git stash clear
```

---

## Git Aliases - Work Faster

```bash
# Set up useful aliases
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.cm commit
git config --global alias.unstage 'restore --staged'

# Complex alias example
git config --global alias.lg "log --oneline --graph --decorate"

# Now use them
git st      # Same as: git status
git cm -m "message"  # Same as: git commit -m "message"
git lg      # Pretty log output
```

---

## Ignoring Files

```bash
# Create .gitignore file
touch .gitignore
```

### `.gitignore` patterns:

```gitignore
# Ignore all .log files
*.log

# Ignore node_modules directory
node_modules/

# Ignore all .txt files in doc/ directory
doc/**/*.txt

# But track important.log even though *.log is ignored
!important.log

# Ignore file in root only
/TODO
```

---

## Gitignore Patterns

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="40" text-anchor="middle" font-size="24" font-weight="bold">.gitignore Patterns</text>
  <rect x="50" y="80" width="170" height="60" fill="#E3F2FD" stroke="#1976D2" stroke-width="2" rx="5"/>
  <text x="135" y="105" text-anchor="middle" font-size="14" font-weight="bold">*.log</text>
  <text x="135" y="125" text-anchor="middle" font-size="12">All .log files</text>
  <rect x="240" y="80" width="170" height="60" fill="#E8F5E9" stroke="#388E3C" stroke-width="2" rx="5"/>
  <text x="325" y="105" text-anchor="middle" font-size="14" font-weight="bold">build/</text>
  <text x="325" y="125" text-anchor="middle" font-size="12">build directory</text>
  <rect x="430" y="80" width="170" height="60" fill="#FFF3E0" stroke="#F57C00" stroke-width="2" rx="5"/>
  <text x="515" y="105" text-anchor="middle" font-size="14" font-weight="bold">!keep.log</text>
  <text x="515" y="125" text-anchor="middle" font-size="12">Exception to rule</text>
  <rect x="620" y="80" width="130" height="60" fill="#FFEBEE" stroke="#C62828" stroke-width="2" rx="5"/>
  <text x="685" y="105" text-anchor="middle" font-size="14" font-weight="bold">/TODO</text>
  <text x="685" y="125" text-anchor="middle" font-size="12">Root only</text>
  <rect x="50" y="160" width="170" height="60" fill="#F3E5F5" stroke="#7B1FA2" stroke-width="2" rx="5"/>
  <text x="135" y="185" text-anchor="middle" font-size="14" font-weight="bold">doc/*.txt</text>
  <text x="135" y="205" text-anchor="middle" font-size="12">Direct children</text>
  <rect x="240" y="160" width="170" height="60" fill="#E0F2F1" stroke="#00796B" stroke-width="2" rx="5"/>
  <text x="325" y="185" text-anchor="middle" font-size="14" font-weight="bold">doc/**/*.pdf</text>
  <text x="325" y="205" text-anchor="middle" font-size="12">All descendants</text>
  <rect x="430" y="160" width="170" height="60" fill="#FCE4EC" stroke="#C2185B" stroke-width="2" rx="5"/>
  <text x="515" y="185" text-anchor="middle" font-size="14" font-weight="bold">[Dd]ebug/</text>
  <text x="515" y="205" text-anchor="middle" font-size="12">Debug or debug</text>
  <rect x="620" y="160" width="130" height="60" fill="#EFEBE9" stroke="#5D4037" stroke-width="2" rx="5"/>
  <text x="685" y="185" text-anchor="middle" font-size="14" font-weight="bold">#comment</text>
  <text x="685" y="205" text-anchor="middle" font-size="12">Comments</text>
  <rect x="200" y="250" width="400" height="100" fill="#F5F5F5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="400" y="280" text-anchor="middle" font-size="14" font-weight="bold">Check what's ignored:</text>
  <text x="400" y="305" text-anchor="middle" font-size="13" font-family="monospace">git check-ignore -v filename</text>
  <text x="400" y="330" text-anchor="middle" font-size="13" font-family="monospace">git status --ignored</text>
</svg>

---

## Global vs Local Gitignore

```bash
# Local (per-repository)
.gitignore                 # Tracked, shared with team

# Global (per-user)
~/.gitignore_global       # Your personal ignores

# Set global gitignore
git config --global core.excludesfile ~/.gitignore_global

# Per-repository (not tracked)
.git/info/exclude         # Local only, not shared
```

**Use cases:**
- **Local**: Project-specific (node_modules, *.pyc)
- **Global**: Your editor files (.vscode, .idea)
- **Exclude**: Temporary personal files

---

## Common Gitignore Templates

**Node.js project:**
```gitignore
node_modules/
npm-debug.log*
.env
dist/
*.log
```

**Python project:**
```gitignore
__pycache__/
*.py[cod]
venv/
.env
*.sqlite3
```

**IDE/Editor:**
```gitignore
.vscode/
.idea/
*.swp
.DS_Store
```

### Find more at: https://github.com/github/gitignore

---

## Tracking Empty Directories

Git doesn't track empty directories. Solution:

```bash
# Add .gitkeep file
mkdir empty_dir
touch empty_dir/.gitkeep
git add empty_dir/.gitkeep

# Or use .gitignore
echo "*" > empty_dir/.gitignore
echo "!.gitignore" >> empty_dir/.gitignore
```

**Convention**: Use `.gitkeep` for clarity

---

## File Attributes

### `.gitattributes` file:

```gitattributes
# Set default behavior
* text=auto

# Explicitly set file types
*.txt text
*.jpg binary
*.sh text eol=lf
*.bat text eol=crlf

# Language statistics
docs/* linguist-documentation
*.generated linguist-generated=true

# Diff settings
*.min.js -diff
```

**Controls**: Line endings, diff behavior, merge strategies

---

## Reviewing Your Work

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="40" text-anchor="middle" font-size="24" font-weight="bold">Before You Commit Checklist</text>
  <rect x="100" y="80" width="600" height="280" fill="#F5F5F5" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="130" y="100" width="540" height="40" fill="#E3F2FD" stroke="#1976D2" stroke-width="1" rx="3"/>
  <text x="150" y="125" font-size="14">☐ git status - Check what's changed</text>
  <rect x="130" y="150" width="540" height="40" fill="#E8F5E9" stroke="#388E3C" stroke-width="1" rx="3"/>
  <text x="150" y="175" font-size="14">☐ git diff - Review unstaged changes</text>
  <rect x="130" y="200" width="540" height="40" fill="#FFF3E0" stroke="#F57C00" stroke-width="1" rx="3"/>
  <text x="150" y="225" font-size="14">☐ git diff --staged - Review what you're committing</text>
  <rect x="130" y="250" width="540" height="40" fill="#F3E5F5" stroke="#7B1FA2" stroke-width="1" rx="3"/>
  <text x="150" y="275" font-size="14">☐ Tests pass? Documentation updated?</text>
  <rect x="130" y="300" width="540" height="40" fill="#FFEBEE" stroke="#C62828" stroke-width="1" rx="3"/>
  <text x="150" y="325" font-size="14">☐ Good commit message ready?</text>
</svg>

---

## Common Workflow Example

```bash
# Start work
git status                    # Check current state
git pull                      # Get latest changes

# Make changes
edit file1.js file2.js
git diff                      # Review changes

# Stage and commit
git add file1.js
git diff --staged            # Review what's staged
git commit -m "Add feature X"

# Share work
git push origin main
```

---

## Troubleshooting Common Issues

### Changes not staged for commit
```bash
git add <files>  # Stage the files
```

### Your branch is ahead of origin
```bash
git push  # Push your commits
```

### Your branch is behind origin
```bash
git pull  # Get remote changes
```

### Merge conflict
```bash
# Fix conflicts in files, then:
git add <fixed-files>
git commit
```

---

## The Reflog - Your Safety Net

```bash
# Show reflog
git reflog

# Example output:
# a3f8d9c HEAD@{0}: commit: Fix bug
# b8e7a2d HEAD@{1}: checkout: moving from feature to main
# c9d6b3e HEAD@{2}: commit: Add feature

# Recover lost commit
git checkout HEAD@{2}
# or
git reset --hard HEAD@{2}
```

**Reflog tracks ALL movements of HEAD - even "lost" commits!**

---

## Summary

## What We Learned

1. ✅ Creating and cloning repositories
1. ✅ The working directory, staging area, and repository
1. ✅ Essential commands: `add`, `commit`, `status`, `diff`
1. ✅ Viewing and searching history
1. ✅ Undoing changes safely
1. ✅ Using `.gitignore` effectively
1. ✅ Stashing work temporarily

---

## Key Commands Reference

| Command | Purpose |
|---------|---------|
| `git init` | Create repository |
| `git add` | Stage changes |
| `git commit` | Save snapshot |
| `git status` | Check state |
| `git diff` | View changes |
| `git log` | View history |
| `git restore` | Undo changes |
| `git stash` | Save work temporarily |

---

## Best Practices Recap

1. **Commit often** - Small, logical commits
1. **Write meaningful messages** - Future you will thank you
1. **Review before committing** - Use `git diff --staged`
1. **Use `.gitignore`** - Don't track generated files
1. **Don't commit secrets** - Use environment variables
1. **Pull before push** - Stay synchronized

---

## Practice Exercises

1. Create a new repository and make 5 commits
1. Practice staging partial changes with `git add -p`
1. Use `git stash` to switch contexts
1. Write a comprehensive `.gitignore` for your project
1. Explore history with different `git log` options
1. Practice undoing changes with `restore` and `reset`

---

## Next Up: Configuration

In the next session, we'll explore:

1. Configuring Git for your workflow
1. Setting up aliases for efficiency
1. Understanding config scopes
1. SSH keys and authentication
1. Hooks and automation
1. Advanced `.gitignore` patterns

---

## Git Basics Complete! 🎉

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="80" text-anchor="middle" font-size="32" font-weight="bold" fill="#4CAF50">You've Mastered the Fundamentals!</text>
  <rect x="250" y="120" width="300" height="150" fill="#E8F5E9" stroke="#388E3C" stroke-width="3" rx="10"/>
  <text x="400" y="165" text-anchor="middle" font-size="20">Ready to:</text>
  <text x="400" y="195" text-anchor="middle" font-size="16">• Track changes effectively</text>
  <text x="400" y="220" text-anchor="middle" font-size="16">• Commit with confidence</text>
  <text x="400" y="245" text-anchor="middle" font-size="16">• Navigate Git's three states</text>
  <circle cx="200" cy="320" r="30" fill="#FFC107"/>
  <text x="200" y="327" text-anchor="middle" font-size="24">✓</text>
  <circle cx="400" cy="320" r="30" fill="#FFC107"/>
  <text x="400" y="327" text-anchor="middle" font-size="24">✓</text>
  <circle cx="600" cy="320" r="30" fill="#FFC107"/>
  <text x="600" y="327" text-anchor="middle" font-size="24">✓</text>
</svg>
