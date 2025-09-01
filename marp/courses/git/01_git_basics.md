# Git Basics
---
## Setting Up Git
- Initial installation and configuration
- Setting username and email
- Configuring default editor
- Setting up SSH keys for remote access
---
## Creating a Repository
![0](../../../out/mermaid/marp/courses/git/01_git_basics.md/0.png)

---
## Local Repository Setup
- `git init` creates new repository
- Creates .git directory
- Initializes required data structures
- Sets up master/main branch
---
## Remote Repository Setup
- `git clone [url]` copies remote repository
- Creates local copy of all history
- Sets up remote tracking
- Establishes connection to origin
---
## The Staging Area
![1](../../../out/mermaid/marp/courses/git/01_git_basics.md/1.png)

---
## Working with git status
- Shows current repository state
- Displays tracked/untracked files
- Shows staged changes
- Indicates current branch
---
## Understanding git add
- Adds files to staging area
- Can add specific files or directories
- Supports wildcards and patterns
- Prepares content for commit
---
## Git Stage Command
- Alternative to git add
- Same functionality, different name
- Part of Git's command consistency
- Used in some workflows
---
## File Operations
- `git rm` removes files
- `git mv` moves/renames files
- Updates both working directory and index
- Prepares changes for commit
---
## The git diff Command
- Shows changes between commits
- Compares working directory and staging
- Displays staged vs committed changes
- Helps review modifications
---
## Working Directory vs Staged
![2](../../../out/mermaid/marp/courses/git/01_git_basics.md/2.png)

---
## Creating Commits
- `git commit` creates new commit
- Records staged changes
- Requires commit message
- Creates unique SHA-1 hash
---
## Writing Good Commit Messages
- Short, descriptive first line
- Detailed explanation if needed
- Reference issues/tickets
- Be clear and specific
---
## Viewing History
- `git log` shows commit history
- Various output formats
- Filtering and searching
- Visualizing branches
---
## Log Visualization
- Graph view of history
- Branch and merge visualization
- Time-based filtering
- Author-based filtering
---
## Searching Code
- `git grep` searches repository
- Regular expression support
- Search in specific commits
- Search in specific paths
---
## Undoing Staged Changes
- `git restore --staged` unstages
- Keeps working directory unchanged
- Safe operation
- Modern Git command
---
## Using git reset
- Moves HEAD and branch
- Can affect staging area
- Can affect working directory
- Different modes available
---
## Reset Modes
![3](../../../out/mermaid/marp/courses/git/01_git_basics.md/3.png)

---
## File-level Reset
- Reset specific files
- Updates staging area
- Leaves working directory unchanged
- `git reset [ref] [file]`
---
## Hard Reset
- Most aggressive reset
- Updates everything to target
- Discards all changes
- Use with caution
---
## Comparing Changes
- Between commits
- Between branches
- Between staged and unstaged
- Between local and remote
---
## Basic Workflow
1. Make changes in working directory
1. Stage changes with git add
1. Review changes with git status/diff
1. Commit changes with git commit
---
## Best Practices
- Commit atomic changes
- Write clear messages
- Stage related changes together
- Review before committing
---
## Common Patterns
- Feature development
- Bug fixing
- Code review preparation
- Release management
---
## Command Line Tools
- Basic command syntax
- Common options
- Help and documentation
- Command aliases
---
## GUI Tools
- Built-in git gui
- Third-party tools
- IDE integration
- Visualization tools
---
## Troubleshooting
- Common errors
- Error messages
- Recovery options
- Getting help
---
## Security Considerations
- File permissions
- SSH keys
- Credential storage
- Sensitive data
---
## Performance
- Local operations
- Remote operations
- Large repositories
- Optimization tips
