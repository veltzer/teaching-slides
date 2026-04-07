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

![creating_a_repository](svg/courses/git/git2/02_basics/creating_a_repository.svg)

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

![understanding_working_directory](svg/courses/git/git2/02_basics/understanding_working_directory.svg)

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

![the_staging_area_index](svg/courses/git/git2/02_basics/the_staging_area_index.svg)

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

![undoing_staged_changes](svg/courses/git/git2/02_basics/undoing_staged_changes.svg)

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

![writing_good_commit_messages](svg/courses/git/git2/02_basics/writing_good_commit_messages.svg)

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

![understanding_references](svg/courses/git/git2/02_basics/understanding_references.svg)

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

![the_reset_command](svg/courses/git/git2/02_basics/the_reset_command.svg)

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

![working_with_stash](svg/courses/git/git2/02_basics/working_with_stash.svg)

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

![gitignore_patterns](svg/courses/git/git2/02_basics/gitignore_patterns.svg)

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

![reviewing_your_work](svg/courses/git/git2/02_basics/reviewing_your_work.svg)

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

![git_basics_complete](svg/courses/git/git2/02_basics/git_basics_complete.svg)
