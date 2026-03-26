# Showing Git Data

---

## What We'll Cover

1. Using `git log` effectively
1. Exploring files with `git ls-files`
1. Examining commits with `git show`
1. Comparing changes with `git diff`
1. Branch visualization with `git show-branch`
1. Code archaeology with `git blame` and `git annotate`
1. Change tracking with `git whatchanged`
1. Visual tools overview

---

## The Power of Git Log

`git log` is your primary tool for exploring repository history:

```bash
# Basic log
git log

# Compact one-line format
git log --oneline

# Show last 5 commits
git log -5

# Log with graph visualization
git log --graph --oneline --all
```

**Common options:**
- `--oneline`: Condensed format
- `--graph`: ASCII graph of branches
- `--all`: Show all branches
- `--stat`: Show file change statistics
- `--patch`: Show actual changes

---

## Advanced Git Log Formatting

Customize log output for specific needs:

```bash
# Custom format
git log --pretty=format:"%h %an %ar %s"

# Show commits with files changed
git log --name-only

# Show commits with change statistics
git log --stat

# Show commits affecting specific file
git log -- path/to/file.txt
```

**Format placeholders:**
- `%h`: Short hash
- `%H`: Full hash
- `%an`: Author name
- `%ad`: Author date
- `%s`: Subject (commit message)
- `%b`: Body

---

## Filtering Git Log Output

Find specific commits efficiently:

```bash
# Commits by author
git log --author="John Smith"

# Commits in date range
git log --since="2 weeks ago"
git log --until="2023-12-01"

# Commits containing string in message
git log --grep="bug fix"

# Commits that added/removed specific text
git log -S"function_name"

# Commits affecting specific paths
git log -- src/ docs/
```

**Combining filters:**
```bash
git log --author="Jane" --since="1 month ago" --grep="feature"
```

---

## Git Log with Visual Elements

Create informative visual representations:

```bash
# Beautiful graph view
git log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit --all

# Show branch merge history
git log --graph --oneline --decorate --all

# Compact branch view
git log --oneline --graph --all -10
```

<svg viewBox="0 0 600 200" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="20" text-anchor="middle" font-size="14" font-weight="bold">Git Log Graph Visualization</text>

  <!-- Main branch line -->
  <line x1="50" y1="80" x2="550" y2="80" stroke="#2ecc71" stroke-width="2"/>

  <!-- Feature branch -->
  <line x1="150" y1="80" x2="200" y2="120" stroke="#e74c3c" stroke-width="2"/>
  <line x1="200" y1="120" x2="300" y2="120" stroke="#e74c3c" stroke-width="2"/>
  <line x1="300" y1="120" x2="350" y2="80" stroke="#e74c3c" stroke-width="2"/>

  <!-- Commits -->
  <circle cx="100" cy="80" r="4" fill="#3498db"/>
  <circle cx="200" cy="80" r="4" fill="#3498db"/>
  <circle cx="250" cy="120" r="4" fill="#e74c3c"/>
  <circle cx="350" cy="80" r="4" fill="#9b59b6"/>
  <circle cx="450" cy="80" r="4" fill="#3498db"/>

  <text x="100" y="100" text-anchor="middle" font-size="8">a1b2c3d</text>
  <text x="200" y="100" text-anchor="middle" font-size="8">d4e5f6g</text>
  <text x="250" y="140" text-anchor="middle" font-size="8">g7h8i9j</text>
  <text x="350" y="100" text-anchor="middle" font-size="8">j1k2l3m</text>
  <text x="450" y="100" text-anchor="middle" font-size="8">m4n5o6p</text>

  <text x="50" y="75" font-size="10" fill="#2ecc71">main</text>
  <text x="250" y="140" font-size="10" fill="#e74c3c">feature</text>
</svg>

---

## Exploring Files with Git Ls-Files

Understand what files `Git` is tracking:

```bash
# List all tracked files
git ls-files

# List files in staging area
git ls-files --cached

# List modified files
git ls-files --modified

# List deleted files
git ls-files --deleted

# List ignored files
git ls-files --ignored --exclude-standard
```

**Useful patterns:**

```bash
# Find all Python files
git ls-files "*.py"

# List files in specific directory
git ls-files src/

# Show file metadata
git ls-files --stage
```

---

## Examining Commits with Git Show

Deep dive into specific commits:

```bash
# Show latest commit
git show

# Show specific commit
git show a1b2c3d

# Show only commit message and stats
git show --stat a1b2c3d

# Show specific file from commit
git show a1b2c3d:path/to/file.txt

# Show commit without diff
git show --no-patch a1b2c3d
```

**Show different objects:**

```bash
# Show tag details
git show v1.0.0

# Show tree object
git show HEAD^{tree}

# Show blob content
git show HEAD:README.md
```

---

## Mastering Git Diff

Compare changes between different states:

```bash
# Changes in working directory
git diff

# Changes in staging area
git diff --cached

# Changes between commits
git diff HEAD~1 HEAD

# Changes between branches
git diff main feature-branch

# Changes for specific file
git diff HEAD~1 -- file.txt
```

**Diff output options:**

```bash
# Word-level diff
git diff --word-diff

# Show statistics only
git diff --stat

# Ignore whitespace changes
git diff --ignore-space-change
```

---

## Advanced Git Diff Techniques

**Context and formatting:**

```bash
# More context lines
git diff -U10

# Side-by-side comparison
git diff --color-words

# Show function names
git diff -p

# Diff between specific commits
git diff a1b2c3d..d4e5f6g
```

**Filtering diffs:**

```bash
# Only show added files
git diff --diff-filter=A

# Only show modified files
git diff --diff-filter=M

# Exclude specific paths
git diff -- . ':(exclude)*.log'
```

---

## Branch Visualization with Git Show-Branch

Compare branches and their relationships:

```bash
# Show relationship between branches
git show-branch

# Show specific branches
git show-branch main develop feature-a

# Show more commits
git show-branch --more=10

# Show all branches
git show-branch --all
```

**Understanding show-branch output:**

```txt
* [main] Latest commit on main
 ! [develop] Latest commit on develop
  * [feature] Latest commit on feature
---
  * [feature] Add new feature
  * [feature^] Start feature work
 !  [develop] Merge hotfix
*+  [main] Important bug fix
```

Legend: `*` = main, `!` = develop, `+` = common commit

---

## Code Archaeology with Git Blame

Discover who changed what and when:

```bash
# Basic blame
git blame file.txt

# Blame specific lines
git blame -L 10,20 file.txt

# Follow renames
git blame -M file.txt

# Follow copies
git blame -C file.txt

# Show email addresses
git blame -e file.txt
```

**Blame output format:**

```txt
a1b2c3d (John Smith 2023-10-15 14:30:22 +0200  1) function calculate() {
d4e5f6g (Jane Doe   2023-10-16 09:15:33 +0200  2)     return x + y;
a1b2c3d (John Smith 2023-10-15 14:30:22 +0200  3) }
```

Elements: commit hash, author, date, timezone, line number, content

---

## Git Annotate vs Git Blame

Both show line-by-line authorship information:

**Git blame (more common):**
```bash
git blame file.txt
# Shows compact format by default
```

**Git annotate (more detailed):**
```bash
git annotate file.txt
# Shows more verbose format
# Includes commit message snippets
```

**Key differences:**
- `annotate` shows more context
- `blame` is more commonly used
- Both support similar options
- Output format slightly different

---

## Tracking Changes with Git Whatchanged

Historical command for viewing changes:

```bash
# Basic whatchanged
git whatchanged

# Last 5 changes
git whatchanged -5

# Changes with patches
git whatchanged -p

# Changes for specific path
git whatchanged -- src/
```

**Note:** `git whatchanged` is largely superseded by `git log --raw` or `git log --stat`, but still useful in some scripts.

**Modern equivalent:**
```bash
git log --name-status
git log --stat
```

---

## Visual Git Tools Overview

**Command-line tools:**

1. **Gitk** - Built-in Git GUI
    ```bash
    gitk --all
    ```
    - Repository browser
    - Commit history visualization
    - Built into Git

1. **Tig** - Text-mode interface
    ```bash
    tig
    ```
    - Terminal-based
    - Interactive browsing
    - Efficient for SSH environments

---

## Desktop Git Clients

**Popular GUI applications:**

1. **SourceTree**
    - Visual branch management
    - Built-in Git Flow support
    - Free from Atlassian

1. **Git Kraken**
    - Beautiful interface
    - Merge conflict resolution
    - Team collaboration features

1. **GitHub Desktop**
    - Simple interface
    - GitHub integration
    - Good for beginners

**Benefits of visual tools:**
- Easier branch visualization
- Intuitive merge conflict resolution
- Better for complex repository layouts
- Helpful for Git beginners

---

## Git Cola and Other Linux Tools

**Git Cola:**
```bash
git cola
```
- Python-based GUI
- Cross-platform
- Good for commit preparation

**Other tools:**
- **SmartGit**: Commercial Git client
- **GitEye**: Eclipse-based
- **QGit**: Qt-based browser
- **GitG**: GNOME Git browser

**IDE Integration:**
- VS Code Git extensions
- IntelliJ Git support
- Vim Git plugins
- Emacs Magit

---

## Combining Data Viewing Commands

**Powerful command combinations:**

```bash
# Find commits that modified specific function
git log -S"functionName" --oneline

# Show what changed in each commit affecting a file
git log -p -- file.txt

# Find merge commits
git log --merges --oneline

# Show branch points
git log --graph --simplify-by-decoration --oneline

# Find commits by specific author in date range
git log --author="John" --since="2 weeks ago" --stat
```

---

## Searching Git History

**Content-based searches:**

```bash
# Find commits that introduced specific text
git log -S"search_term" --source --all

# Find commits with specific text in message
git log --grep="bug.*fix" --all

# Find commits that changed specific files
git log --follow -- old_filename.txt

# Find when a line was deleted
git log --full-history -S"deleted_line" -- file.txt
```

**Case studies:**
- When was this function introduced?
- Who last modified this configuration?
- What commits affected the login system?

---

## Performance Tips for Large Repositories

**Optimize data viewing commands:**

```bash
# Limit commit range
git log --since="1 month ago"

# Use shallow clones for browsing
git clone --depth 50 <repository>

# Index-only operations when possible
git ls-files instead of ls

# Use specific paths
git log -- specific/directory/
```

**For very large repositories:**
- Use `--first-parent` for simpler history
- Limit with `--max-count=N`
- Consider partial clones with `--filter`

---

## Customizing Git Output

**Create aliases for common views:**

```bash
# Add to ~/.gitconfig
[alias]
    lg = log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit
    st = status --short
    co = checkout
    br = branch
    unstage = reset HEAD --
    last = log -1 HEAD
    visual = !gitk
```

**Environment variables:**

```bash
# Set default pager
export GIT_PAGER="less -R"

# Set default editor
export GIT_EDITOR="vim"
```

---

## Troubleshooting with Git Data Commands

**Common debugging scenarios:**

1. **"Where did my changes go?"**
    ```bash
    git reflog
    git log --all --full-history -- path/to/file
    ```

1. **"Who broke the build?"**
    ```bash
    git bisect start
    git bisect bad HEAD
    git bisect good v1.0
    ```

1. **"What changed between releases?"**
    ```bash
    git log v1.0..v2.0 --oneline
    git diff v1.0..v2.0 --stat
    ```

1. **"When was this bug introduced?"**
    ```bash
    git log -S"buggy_code" --oneline
    git blame file.txt | grep -n "buggy_line"
    ```

---

## Git Data Export and Reporting

**Generate reports from Git data:**

```bash
# Activity report
git shortlog -sn --since="1 month ago"

# Files changed most frequently
git log --name-only --pretty=format: | sort | uniq -c | sort -rg

# Commit activity by day
git log --date=short --pretty=format:%ad | sort | uniq -c

# Lines of code by author
git log --author="John" --pretty=tformat: --numstat | awk '{add+=$1; del+=$2} END {print "Added:", add, "Deleted:", del}'
```

**Export formats:**

```bash
# JSON format (with additional tools)
git log --pretty=format:'{"commit":"%H","author":"%an","date":"%ad","message":"%s"},' --date=iso

# CSV format
git log --pretty=format:'%H,%an,%ad,%s' --date=short
```

---

## Security Considerations

**Sensitive information in Git history:**

```bash
# Search for potential secrets
git log -p --all | grep -i "password\|secret\|key"

# Find large files that shouldn't be tracked
git rev-list --objects --all | grep "$(git verify-pack -v .git/objects/pack/*.idx | sort -k 3 -nr | head -10 | awk '{print $1}')"

# Check for sensitive files
git log --name-only --pretty=format: | sort -u | grep -E '\.(pem|key|p12)$'
```

**Best practices:**
- Regularly audit repository contents
- Use `.gitignore` for sensitive files
- Consider Git-crypt for encrypted storage
- Remove secrets with BFG Repo-Cleaner

---

## Advanced Data Analysis

**Statistical analysis of repository:**

```bash
# Commit frequency analysis
git log --format=format:%ad --date=short | sort | uniq -c | sort -nr

# Most active files
git log --name-only --pretty=format: | sort | uniq -c | sort -rg | head -20

# Author contribution analysis
git log --format='%aN' | sort -u | while read name; do echo -en "$name\t"; git log --author="$name" --pretty=tformat: --numstat | awk '{a+=$1; d+=$2} END {print a-d}'; done | sort -k2 -nr

# Complexity trends
git log --oneline --since="6 months ago" | wc -l
```

**Visualization ideas:**
- Commit frequency over time
- Code churn by author
- File modification hotspots
- Branch merge patterns

---

## Integration with External Tools

**Pipe Git data to external tools:**

```bash
# Generate graphs with gnuplot
git log --pretty=format:%ad --date=short | sort | uniq -c > commits_per_day.dat

# Export to spreadsheet format
git log --pretty=format:'%ad,%an,%s' --date=short > commits.csv

# Integration with jq for JSON processing
git log --pretty=format:'{"date":"%ad","author":"%an","message":"%s"}' --date=iso | jq -s '.'

# Send to analysis tools
git log --numstat --pretty=format: | python analyze_code_changes.py
```

---

## Lab Exercise: Repository Analysis

**Scenario:** Analyze a repository to understand development patterns and identify potential issues.

**Tasks:**
1. **Historical analysis:**
    - Find the most active contributors
    - Identify most frequently changed files
    - Analyze commit frequency patterns

1. **Code archaeology:**
    - Use `git blame` to understand code ownership
    - Find when specific features were introduced
    - Track the evolution of important files

1. **Quality assessment:**
    - Look for commits that might indicate problems
    - Find unusually large commits
    - Identify potential security issues

1. **Visualization:**
    - Create visual representations of the data
    - Generate reports for stakeholders
    - Recommend improvements based on findings

**Deliverables:** Analysis report with visualizations, identified issues, and recommended actions.

---

## Summary: Effective Git Data Exploration

**Key takeaways:**

1. **Master the basics:**
    - `git log` with various options
    - `git show` for detailed examination
    - `git diff` for comparing changes

1. **Use the right tool for the job:**
    - Command-line for automation
    - Visual tools for complex analysis
    - Combination approaches for best results

1. **Develop systematic approaches:**
    - Start with broad views, then narrow focus
    - Combine multiple commands for insights
    - Document findings and patterns

1. **Automate common tasks:**
    - Create aliases for frequent operations
    - Build scripts for complex analyses
    - Integrate with external tools when needed

**Remember:** Git data exploration is both an art and a science - the more you practice, the more insights you'll uncover about your codebase and development patterns.
