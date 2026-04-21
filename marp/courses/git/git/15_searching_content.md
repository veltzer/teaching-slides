---
tags:
  - tools:git
  - concepts:version-control
level: intermediate
category: version-control
audience:
  - audiences:developers
  - audiences:sysadmins
  - audiences:devops

---
# Searching by Content

---

## What We'll Cover

1. Using `git grep` for content search
1. Combining `git grep` with `git rev-list`
1. Advanced `git log` search techniques
1. Searching across repository history
1. Performance optimization for large repositories
1. Integration with external search tools

---

## Introduction to Content Search

Git provides powerful tools for searching content across:

**Current working directory:**
- Search files in current state
- Include or exclude specific file types
- Pattern matching and regular expressions

**Repository history:**
- Search content across all commits
- Find when specific code was introduced
- Track evolution of functions or variables

**Multiple branches:**
- Search across different branches
- Compare content between branches
- Find code that exists in some branches but not others

**Why content search matters:**
- Code archaeology and debugging
- Finding examples of API usage
- Locating security vulnerabilities
- Understanding codebase evolution

---

## Basic Git Grep

`git grep` is Git's built-in content search tool:

```bash
# Basic search in working directory
git grep "function_name"

# Search for pattern
git grep "TODO"
git grep "FIXME"

# Case-insensitive search
git grep -i "error"

# Show line numbers
git grep -n "import"

# Show only filenames
git grep -l "class.*User"
```

**Basic options:**
- `-i`: Case-insensitive search
- `-n`: Show line numbers
- `-l`: Show only filenames with matches
- `-c`: Count matches per file
- `-v`: Invert match (show non-matching lines)

---

## Advanced Git Grep Options

More sophisticated search patterns:

```bash
# Word boundaries
git grep -w "user"              # Match whole word only
git grep "\buser\b"             # Same using regex

# Extended regular expressions
git grep -E "class|function"    # Match either pattern
git grep -P "(?<=class\s)\w+"   # Perl regex (class names)

# Fixed strings (no regex)
git grep -F "literal.string"    # Treat as literal text

# Context around matches
git grep -A 3 -B 2 "function"   # 3 lines after, 2 before
git grep -C 5 "TODO"            # 5 lines context both sides
```

**Pattern types:**
- Basic regex (default)
- Extended regex (`-E`)
- Perl regex (`-P`)
- Fixed strings (`-F`)
- Word boundaries (`-w`)

---

## File and Path Filtering

Limit search scope with path specifications:

```bash
# Search specific file types
git grep "error" -- "*.py"
git grep "function" -- "*.js" "*.ts"

# Search specific directories
git grep "TODO" -- src/
git grep "FIXME" -- src/ docs/

# Exclude paths
git grep "debug" -- . ':!test/'
git grep "config" -- . ':!*.min.js'

# Search only tracked files
git grep "pattern" HEAD

# Search including untracked files
git grep --untracked "pattern"
```

**Path specifications:**
- Glob patterns for file matching
- Directory-specific searches
- Exclusion patterns
- Tracked vs untracked files

---

## Searching Repository History

Search content across all commits:

```bash
# Search all commits
git grep "function_name" $(git rev-list --all)

# Search specific branch history
git grep "TODO" $(git rev-list main)

# Search between commits
git grep "error" $(git rev-list HEAD~10..HEAD)

# Search specific time range
git grep "config" $(git rev-list --since="1 month ago" --all)
```

**Historical search patterns:**
- All repository history
- Specific branch history
- Time-based ranges
- Commit ranges

---
## Git Grep with Rev-List

Powerful combination for historical searches:

```bash
# Find when text was introduced
git log -S"function_name" --oneline

# Find when text was removed
git log -S"old_function" --oneline

# Search commit messages and content
git log --grep="fix" -S"bug" --oneline

# Find commits that changed specific text
git log -G"regex_pattern" --oneline
```

**Search types:**
- `-S`: Pickaxe search (additions/deletions)
- `-G`: Regex search in diff content
- `--grep`: Search commit messages
- Combined searches for precision

---
## Git Grep with Rev-List

![find_commits_that_changed_specific_text](svg/courses/git/git/15_searching_content/find_commits_that_changed_specific_text.svg)

---

## Advanced Log Search Techniques

Sophisticated searching with `git log`:

```bash
# Search commit messages
git log --grep="fix.*bug" --oneline
git log --grep="feature" --grep="auth" --all-match

# Search author and committer
git log --author="John" --grep="fix"
git log --committer="jenkins" --since="1 week ago"

# Combine content and message search
git log --grep="feature" -S"new_function" --oneline

# Search with date ranges
git log --since="2023-01-01" --until="2023-12-31" -S"deprecated"

# Complex boolean search
git log --grep="bug" --grep="fix" --all-match -S"critical"
```

**Log search options:**
- `--grep`: Commit message patterns
- `--author`: Author name patterns
- `--committer`: Committer name patterns
- `--all-match`: Require all grep patterns to match
- Date range filtering

---

## Pickaxe Search (-S and -G)

Deep content change analysis:

```bash
# Find commits that changed occurrence count of string
git log -S"function_name" --oneline

# Show actual changes
git log -S"function_name" -p

# Regex-based change search
git log -G"class.*Controller" --oneline

# Find file renames with content
git log -S"content" --follow -- filename

# Pickaxe with file paths
git log -S"API_KEY" -- "*.py" "*.js"
```

**Pickaxe vs Grep differences:**
- `-S`: Finds commits that change occurrence count
- `-G`: Finds commits where diff matches regex
- `-S` is faster for simple string searches
- `-G` is more flexible for pattern matching

---

## Multi-Branch Content Search

Search across different branches:

```bash
# Search all branches
git grep "pattern" $(git for-each-ref --format='%(refname)' refs/heads/)

# Search specific branches
git grep "function" main develop feature/*

# Find branches containing specific content
for branch in $(git branch -r | sed 's/origin\///'); do
    if git grep -q "search_term" origin/$branch 2>/dev/null; then
        echo "Found in: $branch"
    fi
done

# Compare content between branches
git diff main..develop -- | grep -E "^\+.*search_term"
```

**Branch search strategies:**
- All local branches
- Remote branches
- Branch pattern matching
- Differential content analysis

---

## Performance Optimization

Optimize searches for large repositories:

```bash
# Limit search depth
git grep "pattern" HEAD~10..HEAD

# Use index for speed
git grep --cached "pattern"

# Parallel processing
git grep --threads=4 "pattern"

# Exclude large files
git grep "pattern" -- . ':!*.min.js' ':!*.bundle.*'

# Search only specific file types
git grep "pattern" -- "*.py" "*.js" | head -20
```

**Performance tips:**
- Limit scope when possible
- Use specific file patterns
- Exclude generated files
- Leverage Git's indexing
- Consider parallel processing

---

## Binary File Handling

Handle binary files in searches:

```bash
# Skip binary files (default)
git grep "text"

# Search binary files as text
git grep -a "pattern"

# Show binary file matches
git grep --binary "pattern"

# List binary files
git grep -I "." -- | head -5  # Will show text files only
```

**Binary considerations:**
- Git automatically detects binary files
- Text search in binaries usually not useful
- May want to exclude common binary types
- Consider file type filtering

---

## Output Formatting and Processing

Customize search output:

```bash
# JSON-like output (for scripting)
git grep --show-function "pattern"

# Show function context
git grep -p "pattern" -- "*.py"

# Color output control
git grep --color=always "pattern"
git grep --color=never "pattern"

# Null-terminated output (for scripts)
git grep -z "pattern"

# Count matches
git grep -c "TODO" -- "*.py" | sort -t: -k2 -n
```

**Output customization:**
- Function context display
- Color control for terminals
- Script-friendly formats
- Statistical summaries

---

## Integration with External Tools

Combine Git search with system tools:

```bash
# Pipe to other tools
git grep "TODO" | wc -l
git grep "FIXME" | sort
git grep -l "deprecated" | xargs git log --oneline

# Use with find and grep
find . -name "*.py" -exec git grep "pattern" {} \;

# Integration with ripgrep
rg "pattern" --vimgrep | while read line; do
    echo "Git status: $(git status --porcelain ${line%%:*})"
done

# Use with ag (silver searcher)
ag "pattern" --files-with-matches | xargs git log --oneline --
```

**Tool combinations:**
- System utilities (wc, sort, uniq)
- Modern search tools (rg, ag)
- File processing tools
- Git command chaining

---

## Search Result Analysis

Analyze and process search results:

```bash
# Most common matches
git grep -oh "TODO.*" | sort | uniq -c | sort -nr

# Files with most matches
git grep -c "console.log" -- "*.js" | sort -t: -k2 -nr | head -10

# Search result statistics
echo "Total TODO items: $(git grep -c TODO | awk -F: '{sum+=$2} END {print sum}')"

# Authors of matching lines (with git blame)
git grep -l "deprecated" | xargs -I {} sh -c 'echo "=== {} ==="; git blame {} | grep "deprecated"'
```

**Analysis techniques:**
- Frequency counting
- Statistical summaries
- Cross-referencing with blame
- Pattern extraction

---

## Historical Content Evolution

Track how content changes over time:

```bash
# Show when function was added/removed
git log --follow -S"function_name" --oneline -- file.py

# Show evolution of specific line
git log -L 10,20:file.py

# Track function evolution
git log -L :function_name:file.py

# Show changes to specific pattern
git log --follow -G"class.*User" --oneline
```

**Evolution tracking:**
- Line-specific history
- Function-level tracking
- Pattern evolution
- File following across renames

---

## Security-Focused Searches

Find potential security issues:

```bash
# Search for potential secrets
git grep -E "(password|secret|key|token)" --all

# Find hardcoded credentials
git grep -E "(api_key|secret_key)" $(git rev-list --all)

# Search for security patterns
git grep -E "(eval|exec|system|shell_exec)" -- "*.php"

# Find TODO/FIXME in security context
git grep -E "(TODO|FIXME).*security" -i
```

**Security search patterns:**
- Credential detection
- Dangerous function usage
- Security-related comments
- Historical vulnerability tracking

---

## Code Quality Searches

Find code quality issues:

```bash
# Find debug code
git grep -E "(console\.log|debugger|print\()" -- "*.js" "*.py"

# Locate commented code
git grep -E "^\s*#.*[{}();]" -- "*.py"
git grep -E "^\s*//.*[{}();]" -- "*.js"

# Find magic numbers
git grep -E "[^a-zA-Z_][0-9]{3,}[^a-zA-Z_0-9]" -- "*.py"

# Locate long lines
git grep "^.{120,}$" -- "*.py"
```

**Quality indicators:**
- Debug statements
- Commented code blocks
- Magic numbers
- Code style violations

---

## Search Automation and Scripting

Automate common search tasks:

```bash
#!/bin/bash
# search-repo.sh - Comprehensive repository search script

PATTERN="$1"
if [ -z "$PATTERN" ]; then
    echo "Usage: $0 <pattern>"
    exit 1
fi

echo "=== Current Files ==="
git grep -n "$PATTERN" 2>/dev/null || echo "Not found in current files"

echo "=== History ==="
git log -S"$PATTERN" --oneline | head -5

echo "=== All Branches ==="
for branch in $(git branch -r | sed 's/origin\///'); do
    if git grep -q "$PATTERN" origin/$branch 2>/dev/null; then
        echo "Found in branch: $branch"
    fi
done
```

**Automation benefits:**
- Consistent search procedures
- Combined search strategies
- Repeatable analysis
- Team standardization

---

## Search Performance Benchmarking

Measure and optimize search performance:

```bash
# Time different search approaches
time git grep "pattern"
time git grep "pattern" $(git rev-list --all)
time git log -S"pattern" --oneline

# Profile search with limited scope
time git grep "pattern" -- "*.py"
time git grep "pattern" HEAD~100..HEAD

# Compare tools
time git grep "pattern"
time rg "pattern"
time ag "pattern"
```

**Performance considerations:**
- Repository size impact
- Search scope optimization
- Tool comparison
- Indexing benefits

---

## Troubleshooting Search Issues

Common problems and solutions:

### Issue: Search too slow

```bash
# Solution: Limit scope
git grep "pattern" HEAD~10..HEAD
git grep "pattern" -- "*.py" "*.js"
```

### Issue: Binary file interference

```bash
# Solution: Exclude binary files
git grep "pattern" -- . ':!*.pdf' ':!*.jpg'
```

### Issue: Case sensitivity problems

```bash
# Solution: Use appropriate flags
git grep -i "pattern"           # Case insensitive
git grep -w "pattern"           # Word boundaries
```

### Issue: Regex not working

```bash
# Solution: Check regex type
git grep -E "pattern"           # Extended regex
git grep -P "pattern"           # Perl regex
git grep -F "literal.string"   # Fixed string
```

---

## Search Best Practices

Guidelines for effective content searching:

**Search strategy:**
1. Start with current files
1. Expand to recent history if needed
1. Use specific file patterns when possible
1. Combine multiple search methods

**Performance:**
1. Limit search scope appropriately
1. Use specific patterns over broad ones
1. Exclude unnecessary file types
1. Consider using external tools for large repos

**Accuracy:**
1. Test regex patterns carefully
1. Use word boundaries for exact matches
1. Consider case sensitivity needs
1. Validate results with different approaches

---

## Lab Exercise: Content Search Mastery

**Scenario:** Implement comprehensive content search strategies for a large codebase with security and code quality requirements.

**Basic tasks:**
1. **Current content analysis:**
   - Find all TODO/FIXME items with context
   - Locate debug statements across file types
   - Identify potential hardcoded credentials

1. **Historical analysis:**
   - Track when specific functions were introduced
   - Find commits that removed deprecated code
   - Analyze security-related changes over time

1. **Cross-branch analysis:**
   - Compare content between development branches
   - Find features that exist in some branches but not others
   - Identify merge conflicts in advance

**Advanced tasks:**
1. **Automation development:**
   - Create scripts for common search patterns
   - Implement automated security scanning
   - Build code quality assessment tools

1. **Performance optimization:**
   - Benchmark different search approaches
   - Optimize searches for large repositories
   - Integrate with external search tools

**Deliverables:** Comprehensive search scripts, security scanning automation, code quality analysis tools, and performance optimization guide.

---

## Summary: Mastering Git Content Search

**Key takeaways:**

1. **Choose the right tool:**
   - `git grep` for current content
   - `git log -S/-G` for historical changes
   - Combined approaches for comprehensive analysis

1. **Optimize for performance:**
   - Limit search scope appropriately
   - Use specific file patterns
   - Consider external tools for large repositories
   - Leverage Git's indexing capabilities

1. **Develop systematic approaches:**
   - Start broad, then narrow focus
   - Combine multiple search methods
   - Automate common patterns
   - Document successful strategies

1. **Focus on practical applications:**
   - Code archaeology and debugging
   - Security vulnerability detection
   - Code quality assessment
   - Historical analysis and trends

**Remember:** Effective content searching is both an art and a science. The combination of Git's built-in tools with external utilities and systematic approaches enables powerful analysis of codebases. Master these techniques to become more effective at code maintenance, security analysis, and understanding large software projects.
