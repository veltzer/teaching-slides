# Git Basics
---
## Setting Up Git
- Initial installation and configuration
- Setting username and email
- Configuring default editor
- Setting up SSH keys for remote access
---
## Creating a Repository
<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd0_02_git_basics" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <!-- git init box -->
  <rect x="100" y="20" width="120" height="40" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="160" y="45" text-anchor="middle" font-size="12" font-weight="bold">git init</text>
  <!-- git clone box -->
  <rect x="380" y="20" width="120" height="40" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="440" y="45" text-anchor="middle" font-size="12" font-weight="bold">git clone URL</text>
  <!-- arrows down -->
  <line x1="160" y1="60" x2="300" y2="130" stroke="#333" stroke-width="2" marker-end="url(#arrowd0_02_git_basics)"/>
  <line x1="440" y1="60" x2="300" y2="130" stroke="#333" stroke-width="2" marker-end="url(#arrowd0_02_git_basics)"/>
  <!-- labels on arrows -->
  <text x="200" y="90" text-anchor="middle" font-size="11" fill="#555">creates new</text>
  <text x="400" y="90" text-anchor="middle" font-size="11" fill="#555">copies from remote</text>
  <!-- Local Repository box -->
  <rect x="200" y="130" width="200" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="152" text-anchor="middle" font-size="12" font-weight="bold">Local Repository</text>
  <text x="300" y="170" text-anchor="middle" font-size="11" fill="#555">(.git directory)</text>
</svg>

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
<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd1_02_git_basics" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <!-- Working Directory -->
  <rect x="20" y="60" width="150" height="80" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="95" y="90" text-anchor="middle" font-size="12" font-weight="bold">Working</text>
  <text x="95" y="108" text-anchor="middle" font-size="12" font-weight="bold">Directory</text>
  <text x="95" y="128" text-anchor="middle" font-size="11" fill="#555">edit files here</text>
  <!-- Staging Area -->
  <rect x="225" y="60" width="150" height="80" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="90" text-anchor="middle" font-size="12" font-weight="bold">Staging Area</text>
  <text x="300" y="108" text-anchor="middle" font-size="12" font-weight="bold">(Index)</text>
  <text x="300" y="128" text-anchor="middle" font-size="11" fill="#555">prepare commits</text>
  <!-- Repository -->
  <rect x="430" y="60" width="150" height="80" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="505" y="95" text-anchor="middle" font-size="12" font-weight="bold">Repository</text>
  <text x="505" y="115" text-anchor="middle" font-size="11" fill="#555">permanent history</text>
  <!-- Arrows -->
  <line x1="170" y1="100" x2="222" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd1_02_git_basics)"/>
  <text x="196" y="88" text-anchor="middle" font-size="11" font-weight="bold" fill="#1565c0">git add</text>
  <line x1="375" y1="100" x2="427" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd1_02_git_basics)"/>
  <text x="401" y="88" text-anchor="middle" font-size="11" font-weight="bold" fill="#2e7d32">git commit</text>
</svg>

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
<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd2_02_right" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#1565c0"/>
    </marker>
    <marker id="arrowd2_02_left" markerWidth="10" markerHeight="10" refX="0" refY="3" orient="auto">
      <path d="M9,0 L9,6 L0,3 z" fill="#c62828"/>
    </marker>
  </defs>
  <!-- Working Directory -->
  <rect x="30" y="40" width="200" height="120" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="130" y="65" text-anchor="middle" font-size="12" font-weight="bold">Working Directory</text>
  <rect x="55" y="78" width="150" height="24" fill="#fff" stroke="#90caf9" stroke-width="1" rx="3"/>
  <text x="130" y="95" text-anchor="middle" font-size="11" fill="#555">file1.js (modified)</text>
  <rect x="55" y="108" width="150" height="24" fill="#fff" stroke="#90caf9" stroke-width="1" rx="3"/>
  <text x="130" y="125" text-anchor="middle" font-size="11" fill="#555">file2.css (modified)</text>
  <!-- Staging Area -->
  <rect x="370" y="40" width="200" height="120" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="470" y="65" text-anchor="middle" font-size="12" font-weight="bold">Staging Area</text>
  <rect x="395" y="78" width="150" height="24" fill="#fff" stroke="#ffb74d" stroke-width="1" rx="3"/>
  <text x="470" y="95" text-anchor="middle" font-size="11" fill="#555">file1.js (staged)</text>
  <!-- git add arrow (right) -->
  <line x1="230" y1="85" x2="367" y2="85" stroke="#1565c0" stroke-width="2" marker-end="url(#arrowd2_02_right)"/>
  <text x="298" y="78" text-anchor="middle" font-size="12" font-weight="bold" fill="#1565c0">git add</text>
  <!-- git restore --staged arrow (left) -->
  <line x1="370" y1="130" x2="233" y2="130" stroke="#c62828" stroke-width="2" marker-end="url(#arrowd2_02_left)"/>
  <text x="298" y="152" text-anchor="middle" font-size="11" font-weight="bold" fill="#c62828">git restore --staged</text>
</svg>

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
<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <!-- Header row -->
  <text x="170" y="20" text-anchor="middle" font-size="12" font-weight="bold" fill="#333">Mode</text>
  <text x="330" y="20" text-anchor="middle" font-size="12" font-weight="bold" fill="#333">HEAD</text>
  <text x="430" y="20" text-anchor="middle" font-size="12" font-weight="bold" fill="#333">Staging</text>
  <text x="540" y="20" text-anchor="middle" font-size="12" font-weight="bold" fill="#333">Working Dir</text>
  <!-- --soft row (green = safe) -->
  <rect x="70" y="32" width="200" height="38" fill="#e8f5e9" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="170" y="56" text-anchor="middle" font-size="12" font-weight="bold" fill="#2e7d32">--soft</text>
  <text x="330" y="56" text-anchor="middle" font-size="13" fill="#2e7d32">&#x2714;</text>
  <text x="430" y="56" text-anchor="middle" font-size="12" fill="#888">unchanged</text>
  <text x="540" y="56" text-anchor="middle" font-size="12" fill="#888">unchanged</text>
  <!-- --mixed row (yellow = caution) -->
  <rect x="70" y="78" width="200" height="38" fill="#fff3e0" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="170" y="102" text-anchor="middle" font-size="12" font-weight="bold" fill="#e65100">--mixed (default)</text>
  <text x="330" y="102" text-anchor="middle" font-size="13" fill="#e65100">&#x2714;</text>
  <text x="430" y="102" text-anchor="middle" font-size="13" fill="#e65100">&#x2714; cleared</text>
  <text x="540" y="102" text-anchor="middle" font-size="12" fill="#888">unchanged</text>
  <!-- --hard row (red = dangerous) -->
  <rect x="70" y="124" width="200" height="38" fill="#ffebee" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="170" y="148" text-anchor="middle" font-size="12" font-weight="bold" fill="#c62828">--hard</text>
  <text x="330" y="148" text-anchor="middle" font-size="13" fill="#c62828">&#x2714;</text>
  <text x="430" y="148" text-anchor="middle" font-size="13" fill="#c62828">&#x2714; cleared</text>
  <text x="540" y="148" text-anchor="middle" font-size="13" fill="#c62828">&#x2714; cleared</text>
  <!-- Safety labels -->
  <text x="40" y="56" text-anchor="middle" font-size="11" fill="#2e7d32">safe</text>
  <text x="40" y="102" text-anchor="middle" font-size="11" fill="#e65100">caution</text>
  <text x="40" y="148" text-anchor="middle" font-size="11" fill="#c62828">danger!</text>
  <!-- Separator lines -->
  <line x1="70" y1="26" x2="580" y2="26" stroke="#ccc" stroke-width="1"/>
  <line x1="70" y1="72" x2="580" y2="72" stroke="#ccc" stroke-width="1" stroke-dasharray="4"/>
  <line x1="70" y1="118" x2="580" y2="118" stroke="#ccc" stroke-width="1" stroke-dasharray="4"/>
  <!-- Bottom note -->
  <text x="300" y="185" text-anchor="middle" font-size="11" fill="#555" font-style="italic">&#x26a0; --hard discards uncommitted changes permanently</text>
</svg>

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
