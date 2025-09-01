# Configuring Git

---

## What We'll Cover

1. Local and global config files
1. Configuration scopes and precedence
1. Essential Git configurations
1. Configuring Git commands
1. Setting up signing
1. Creating powerful aliases
1. Advanced `.gitignore` patterns
1. Hooks and automation

---

## Configuration Levels

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="40" text-anchor="middle" font-size="24" font-weight="bold">Git Configuration Scopes</text>
  <rect x="50" y="80" width="200" height="250" fill="#FFEBEE" stroke="#C62828" stroke-width="2" rx="5"/>
  <text x="150" y="115" text-anchor="middle" font-size="18" font-weight="bold">System</text>
  <text x="150" y="140" text-anchor="middle" font-size="12">/etc/gitconfig</text>
  <text x="150" y="165" text-anchor="middle" font-size="11">All users</text>
  <text x="150" y="185" text-anchor="middle" font-size="11">All repositories</text>
  <rect x="90" y="210" width="120" height="30" fill="#EF5350" rx="3"/>
  <text x="150" y="230" text-anchor="middle" font-size="11" fill="white">--system</text>
  <text x="150" y="270" text-anchor="middle" font-size="14">Lowest Priority</text>
  <rect x="300" y="80" width="200" height="250" fill="#FFF3E0" stroke="#F57C00" stroke-width="2" rx="5"/>
  <text x="400" y="115" text-anchor="middle" font-size="18" font-weight="bold">Global</text>
  <text x="400" y="140" text-anchor="middle" font-size="12">~/.gitconfig</text>
  <text x="400" y="165" text-anchor="middle" font-size="11">Current user</text>
  <text x="400" y="185" text-anchor="middle" font-size="11">All repositories</text>
  <rect x="340" y="210" width="120" height="30" fill="#FF9800" rx="3"/>
  <text x="400" y="230" text-anchor="middle" font-size="11" fill="white">--global</text>
  <text x="400" y="270" text-anchor="middle" font-size="14">Medium Priority</text>
  <rect x="550" y="80" width="200" height="250" fill="#E8F5E9" stroke="#388E3C" stroke-width="2" rx="5"/>
  <text x="650" y="115" text-anchor="middle" font-size="18" font-weight="bold">Local</text>
  <text x="650" y="140" text-anchor="middle" font-size="12">.git/config</text>
  <text x="650" y="165" text-anchor="middle" font-size="11">Current repository</text>
  <text x="650" y="185" text-anchor="middle" font-size="11">Only this repo</text>
  <rect x="590" y="210" width="120" height="30" fill="#4CAF50" rx="3"/>
  <text x="650" y="230" text-anchor="middle" font-size="11" fill="white">--local (default)</text>
  <text x="650" y="270" text-anchor="middle" font-size="14">Highest Priority</text>
  <path d="M 250 200 L 290 200" stroke="#333" stroke-width="2" marker-end="url(#arrow1)"/>
  <path d="M 500 200 L 540 200" stroke="#333" stroke-width="2" marker-end="url(#arrow1)"/>
  <defs>
    <marker id="arrow1" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Configuration Precedence

```bash
# System level (all users, all repos)
git config --system user.name "Default User"

# Global level (current user, all repos)
git config --global user.name "John Doe"

# Local level (current repo only)
git config --local user.name "Project Contributor"

# Check which value wins
git config user.name
# Output: Project Contributor (local wins!)
```

**Priority**: Local > Global > System

---

## Essential First-Time Setup

```bash
# Identity (REQUIRED)
git config --global user.name "Your Name"
git config --global user.email "you@example.com"

# Editor preference
git config --global core.editor "vim"
# or
git config --global core.editor "code --wait"  # VS Code
git config --global core.editor "nano"         # Nano

# Default branch name
git config --global init.defaultBranch main

# Line ending handling
git config --global core.autocrlf input  # Mac/Linux
git config --global core.autocrlf true   # Windows
```

---

## Viewing Configuration

```bash
# List all settings and their sources
git config --list --show-origin

# List all settings
git config --list

# List only global settings
git config --global --list

# Get specific value
git config user.name

# Show where a setting comes from
git config --show-origin user.email
```

---

## Configuration File Format

**~/.gitconfig example:**
```ini
[user]
    name = John Doe
    email = john@example.com
[core]
    editor = vim
    autocrlf = input
    excludesfile = ~/.gitignore_global
[color]
    ui = auto
[alias]
    st = status
    co = checkout
    br = branch
[push]
    default = simple
[pull]
    rebase = true
```

---

## Color Configuration

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="40" text-anchor="middle" font-size="24" font-weight="bold">Git Color Output</text>
  <rect x="100" y="80" width="600" height="280" fill="#263238" stroke="#37474F" stroke-width="2" rx="5"/>
  <text x="120" y="110" font-family="monospace" font-size="14" fill="#4CAF50">$ git status</text>
  <text x="120" y="135" font-family="monospace" font-size="14" fill="#FFFFFF">On branch</text>
  <text x="220" y="135" font-family="monospace" font-size="14" fill="#4CAF50">main</text>
  <text x="120" y="160" font-family="monospace" font-size="14" fill="#FFFFFF">Your branch is up to date with 'origin/main'.</text>
  <text x="120" y="195" font-family="monospace" font-size="14" fill="#FFFFFF">Changes to be committed:</text>
  <text x="140" y="220" font-family="monospace" font-size="14" fill="#4CAF50">modified:   README.md</text>
  <text x="120" y="255" font-family="monospace" font-size="14" fill="#FFFFFF">Changes not staged for commit:</text>
  <text x="140" y="280" font-family="monospace" font-size="14" fill="#F44336">modified:   app.js</text>
  <text x="120" y="315" font-family="monospace" font-size="14" fill="#FFFFFF">Untracked files:</text>
  <text x="140" y="340" font-family="monospace" font-size="14" fill="#FF9800">test.txt</text>
</svg>

---

## Configuring Colors

```bash
# Enable colors (auto = only in terminal)
git config --global color.ui auto

# Specific color settings
git config --global color.status.added green
git config --global color.status.changed yellow
git config --global color.status.untracked red

# Branch colors
git config --global color.branch.current "yellow reverse"
git config --global color.branch.local yellow
git config --global color.branch.remote green

# Diff colors
git config --global color.diff.meta "yellow bold"
git config --global color.diff.old "red bold"
git config --global color.diff.new "green bold"
```

---

## Useful Core Configurations

```bash
# Set default pager (less, more, cat)
git config --global core.pager less

# Number of threads for packing
git config --global pack.threads 0  # Auto-detect

# Whitespace handling
git config --global core.whitespace \
    trailing-space,space-before-tab,indent-with-non-tab

# File permissions (ignore chmod changes)
git config --global core.fileMode false

# Case sensitivity
git config --global core.ignoreCase false  # Be case-sensitive

# Compression level (0-9)
git config --global core.compression 9
```

---

## Diff and Merge Tools

```bash
# External diff tool
git config --global diff.tool vimdiff
git config --global difftool.prompt false

# External merge tool
git config --global merge.tool vimdiff
git config --global mergetool.keepBackup false

# VS Code as diff/merge tool
git config --global diff.tool vscode
git config --global difftool.vscode.cmd \
    'code --wait --diff $LOCAL $REMOTE'

# Use tools
git difftool              # Instead of git diff
git mergetool             # During merge conflicts
```

---

## Push and Pull Behavior

```bash
# Push only current branch
git config --global push.default current

# Push to branch with same name
git config --global push.default simple  # Git 2.0+ default

# Always push tags
git config --global push.followTags true

# Pull strategy
git config --global pull.rebase true     # Rebase instead of merge
git config --global pull.ff only         # Fast-forward only

# Auto-stash before rebase
git config --global rebase.autoStash true
```

---

## Creating Aliases

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="40" text-anchor="middle" font-size="24" font-weight="bold">Git Aliases Save Time</text>
  <rect x="50" y="80" width="300" height="60" fill="#FFEBEE" stroke="#C62828" stroke-width="2" rx="5"/>
  <text x="200" y="105" text-anchor="middle" font-size="14" font-weight="bold">Without Alias</text>
  <text x="200" y="125" text-anchor="middle" font-size="12" font-family="monospace">git log --oneline --graph --all</text>
  <rect x="450" y="80" width="300" height="60" fill="#E8F5E9" stroke="#388E3C" stroke-width="2" rx="5"/>
  <text x="600" y="105" text-anchor="middle" font-size="14" font-weight="bold">With Alias</text>
  <text x="600" y="125" text-anchor="middle" font-size="12" font-family="monospace">git lol</text>
  <path d="M 350 110 L 450 110" stroke="#333" stroke-width="2" marker-end="url(#arrow2)"/>
  <text x="400" y="100" text-anchor="middle" font-size="12">Define once</text>
  <rect x="200" y="180" width="400" height="180" fill="#F5F5F5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="400" y="210" text-anchor="middle" font-size="16" font-weight="bold">Common Aliases</text>
  <text x="220" y="240" font-size="13" font-family="monospace">st = status</text>
  <text x="420" y="240" font-size="13" font-family="monospace">co = checkout</text>
  <text x="220" y="265" font-size="13" font-family="monospace">br = branch</text>
  <text x="420" y="265" font-size="13" font-family="monospace">cm = commit</text>
  <text x="220" y="290" font-size="13" font-family="monospace">unstage = restore --staged</text>
  <text x="220" y="315" font-size="13" font-family="monospace">last = log -1 HEAD</text>
  <text x="220" y="340" font-size="13" font-family="monospace">visual = !gitk</text>
  <defs>
    <marker id="arrow2" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Basic Aliases

```bash
# Short commands
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.cm commit
git config --global alias.df diff
git config --global alias.lg log

# Common operations
git config --global alias.unstage 'restore --staged'
git config --global alias.discard 'checkout --'
git config --global alias.last 'log -1 HEAD'
git config --global alias.branches 'branch -a'
git config --global alias.remotes 'remote -v'
git config --global alias.tags 'tag -l'
```

---

## Advanced Aliases

```bash
# Pretty log
git config --global alias.lol \
    "log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit"

# Show recent branches
git config --global alias.recent \
    "for-each-ref --sort=-committerdate refs/heads/ --format='%(committerdate:short) %(refname:short)'"

# Undo last commit (keep changes)
git config --global alias.undo 'reset HEAD~1 --mixed'

# Amend without editing message
git config --global alias.amend 'commit -a --amend --no-edit'

# Show aliases
git config --global alias.aliases \
    "config --get-regexp alias"
```

---

## Shell Command Aliases

```bash
# Aliases can run shell commands with !
git config --global alias.visual '!gitk'
git config --global alias.gui '!git gui'

# Complex shell alias
git config --global alias.cleanup \
    '!git branch --merged | grep -v "\*" | xargs -n 1 git branch -d'

# Interactive rebase last n commits
git config --global alias.rebase-n \
    '!f() { git rebase -i HEAD~$1; }; f'

# Open repository in browser (GitHub)
git config --global alias.browse \
    '!open $(git config remote.origin.url | sed "s/git@/https:\\/\\//;s/.git$//;s/com:/com\\//g")'
```

---

## Credential Management

```bash
# Cache credentials in memory (15 minutes default)
git config --global credential.helper cache

# Cache for specific time (1 hour = 3600 seconds)
git config --global credential.helper 'cache --timeout=3600'

# Store credentials on disk (plaintext - not secure!)
git config --global credential.helper store

# macOS Keychain
git config --global credential.helper osxkeychain

# Windows Credential Manager
git config --global credential.helper manager

# Linux (using libsecret)
git config --global credential.helper libsecret
```

---

## SSH Configuration

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="40" text-anchor="middle" font-size="24" font-weight="bold">SSH vs HTTPS</text>
  <rect x="50" y="80" width="300" height="250" fill="#E3F2FD" stroke="#1976D2" stroke-width="2" rx="5"/>
  <text x="200" y="115" text-anchor="middle" font-size="18" font-weight="bold">SSH</text>
  <text x="200" y="145" text-anchor="middle" font-size="12">git@github.com:user/repo.git</text>
  <text x="70" y="180" font-size="13">✓ No password after setup</text>
  <text x="70" y="205" font-size="13">✓ More secure</text>
  <text x="70" y="230" font-size="13">✓ Per-machine keys</text>
  <text x="70" y="255" font-size="13">✗ Initial setup required</text>
  <text x="70" y="280" font-size="13">✗ Firewall issues (port 22)</text>
  <rect x="450" y="80" width="300" height="250" fill="#FFF3E0" stroke="#F57C00" stroke-width="2" rx="5"/>
  <text x="600" y="115" text-anchor="middle" font-size="18" font-weight="bold">HTTPS</text>
  <text x="600" y="145" text-anchor="middle" font-size="12">https://github.com/user/repo.git</text>
  <text x="470" y="180" font-size="13">✓ Works everywhere</text>
  <text x="470" y="205" font-size="13">✓ No setup needed</text>
  <text x="470" y="230" font-size="13">✓ Firewall friendly</text>
  <text x="470" y="255" font-size="13">✗ Need credentials often</text>
  <text x="470" y="280" font-size="13">✗ Less secure (if no 2FA)</text>
</svg>

---

## Setting Up SSH Keys

```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "your.email@example.com"
# or for legacy systems
ssh-keygen -t rsa -b 4096 -C "your.email@example.com"

# Start SSH agent
eval "$(ssh-agent -s)"

# Add key to agent
ssh-add ~/.ssh/id_ed25519

# Copy public key to clipboard
# macOS
pbcopy < ~/.ssh/id_ed25519.pub
# Linux
xclip -sel clip < ~/.ssh/id_ed25519.pub
# Windows
cat ~/.ssh/id_ed25519.pub | clip

# Add to GitHub/GitLab/Bitbucket settings
```

---

## Multiple SSH Keys

**~/.ssh/config:**

```txt
# Personal GitHub
Host github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_personal

# Work GitHub
Host github-work
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_work

# GitLab
Host gitlab.com
    HostName gitlab.com
    User git
    IdentityFile ~/.ssh/id_gitlab
```

**Usage:**
```bash
git clone git@github-work:company/repo.git
```

---

## GPG Signing

```bash
# List GPG keys
gpg --list-secret-keys --keyid-format=long

# Generate GPG key
gpg --full-generate-key

# Get key ID
gpg --list-secret-keys --keyid-format=long
# sec   4096R/3AA5C34371567BD2 2016-03-10

# Configure Git to use GPG key
git config --global user.signingkey 3AA5C34371567BD2

# Sign commits
git config --global commit.gpgsign true

# Sign tags
git config --global tag.gpgsign true

# Verify signatures
git log --show-signature
```

---

## Advanced Gitignore Patterns

```gitignore
# Negation patterns
*.log
!important.log

# Directory specific
/build/          # Only root build directory
build/           # Any build directory
**/build/        # Explicit any build directory

# Wildcards
*.py[cod]        # .pyc, .pyo, .pyd
*.[oa]           # .o and .a files
*~               # Backup files

# Character ranges
*.[0-9]          # .0, .1, .2, etc.
[Dd]ebug/        # Debug or debug

# Complex patterns
doc/**/*.pdf     # All PDFs in doc tree
!doc/keep/*.pdf  # Except in doc/keep
```

---

## Global Gitignore

```bash
# Set global gitignore
git config --global core.excludesfile ~/.gitignore_global
```

**~/.gitignore_global:**

```gitignore
# OS generated
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
Thumbs.db
Desktop.ini

# Editor files
*.swp
*.swo
*~
.idea/
.vscode/
*.sublime-*

# Credentials
.env
.env.local
```

---

## Gitignore Debugging

```bash
# Check why file is ignored
git check-ignore -v filename.txt

# List all ignored files
git ls-files --others --ignored --exclude-standard

# Show ignored files in status
git status --ignored

# Clean ignored files (CAREFUL!)
git clean -fX     # Only ignored files
git clean -fx     # Ignored and untracked
```

---

## Whitespace Configuration

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="40" text-anchor="middle" font-size="24" font-weight="bold">Whitespace Issues</text>
  <rect x="100" y="80" width="600" height="250" fill="#263238" stroke="#37474F" stroke-width="2" rx="5"/>
  <text x="120" y="110" font-family="monospace" font-size="14" fill="#4CAF50">def hello():</text>
  <text x="120" y="135" font-family="monospace" font-size="14" fill="#FFFFFF">····print("Hello")</text>
  <rect x="330" y="120" width="40" height="20" fill="#F44336" opacity="0.5"/>
  <text x="350" y="155" font-size="10" fill="#F44336">trailing space</text>
  <text x="120" y="160" font-family="monospace" font-size="14" fill="#FFFFFF">····</text>
  <rect x="160" y="145" width="40" height="20" fill="#FF9800" opacity="0.5"/>
  <text x="180" y="180" font-size="10" fill="#FF9800">tab after space</text>
  <text x="160" y="160" font-family="monospace" font-size="14" fill="#FFFFFF">    return</text>
  <text x="120" y="220" font-family="monospace" font-size="14" fill="#4CAF50"># Configure Git to highlight these:</text>
  <text x="120" y="245" font-family="monospace" font-size="14" fill="#FFFFFF">git config core.whitespace \</text>
  <text x="140" y="270" font-family="monospace" font-size="14" fill="#FFFFFF">trailing-space,space-before-tab,indent-with-non-tab</text>
  <text x="120" y="305" font-family="monospace" font-size="14" fill="#4CAF50"># Show whitespace errors:</text>
  <text x="120" y="330" font-family="monospace" font-size="14" fill="#FFFFFF">git diff --check</text>
</svg>

---

## Hooks Overview

```bash
# Hook locations
.git/hooks/

# Available hooks
pre-commit      # Before commit is created
prepare-commit-msg  # Customize default message
commit-msg      # Validate commit message
post-commit     # After commit is created
pre-push        # Before push
post-receive    # Server-side after push
pre-rebase      # Before rebase
post-checkout   # After checkout
post-merge      # After merge
```

### Hooks are shell scripts that Git executes at specific points

---

## Pre-commit Hook Example

```bash
#!/bin/sh
# .git/hooks/pre-commit

# Check for debugging code
if git diff --cached | grep -q "console.log\|debugger"; then
    echo "Error: Debugging code detected!"
    echo "Remove console.log and debugger statements"
    exit 1
fi

# Run tests
npm test
if [ $? -ne 0 ]; then
    echo "Error: Tests must pass before commit!"
    exit 1
fi

# Check formatting
npm run lint
exit $?
```

**Make executable:** `chmod +x .git/hooks/pre-commit`

---

## Commit-msg Hook Example

```bash
#!/bin/sh
# .git/hooks/commit-msg

# Check commit message format
commit_regex='^(feat|fix|docs|style|refactor|test|chore)(\(.+\))?: .{1,50}'

if ! grep -qE "$commit_regex" "$1"; then
    echo "Invalid commit message format!"
    echo "Format: type(scope): subject"
    echo "Example: feat(auth): add login endpoint"
    echo ""
    echo "Types: feat|fix|docs|style|refactor|test|chore"
    exit 1
fi
```

### Enforces conventional commits format

---

## Sharing Hooks

```bash
# Hooks aren't versioned by default
# Solution 1: Use a hooks directory

mkdir .githooks
# Add hooks to .githooks/
git add .githooks

# Configure Git to use them
git config core.hooksPath .githooks

# Solution 2: Setup script
# create setup.sh
#!/bin/sh
cp .githooks/* .git/hooks/
chmod +x .git/hooks/*

# Solution 3: Use tools
# husky (Node.js projects)
npm install --save-dev husky
npx husky init
```

---

## Configuration for Large Files

```bash
# Install Git LFS
git lfs install

# Track large files
git lfs track "*.psd"
git lfs track "*.zip"
git lfs track "assets/**/*.png"

# View tracked patterns
git lfs track

# Add .gitattributes (created by LFS)
git add .gitattributes
```

**.gitattributes:**

```txt
*.psd filter=lfs diff=lfs merge=lfs -text
*.zip filter=lfs diff=lfs merge=lfs -text
assets/**/*.png filter=lfs diff=lfs merge=lfs -text
```

---

## Performance Configuration

```bash
# Enable parallel processing
git config --global core.preloadIndex true
git config --global core.fscache true
git config --global gc.auto 256

# Optimize for large repos
git config --global feature.manyFiles true
git config --global pack.threads 0  # Use all CPU cores
git config --global pack.windowMemory 256m

# Reduce stat calls on Windows
git config --global core.untrackedCache true
git config --global core.fsmonitor true

# Partial clone for huge repos
git clone --filter=blob:none <url>  # Omit blobs
git clone --filter=tree:0 <url>     # Omit trees
```

---

## Conditional Configuration

```bash
# Different configs for different directories
# ~/.gitconfig
[includeIf "gitdir:~/work/"]
    path = ~/.gitconfig-work
[includeIf "gitdir:~/personal/"]
    path = ~/.gitconfig-personal
```

**~/.gitconfig-work:**
```ini
[user]
    email = john@company.com
    signingkey = WORK_KEY
[commit]
    gpgsign = true
```

**~/.gitconfig-personal:**
```ini
[user]
    email = john@personal.com
```

---

## Configuration Best Practices

<svg viewBox="0 0 800 450" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="40" text-anchor="middle" font-size="24" font-weight="bold">Configuration Strategy</text>
  <rect x="50" y="80" width="320" height="150" fill="#E8F5E9" stroke="#388E3C" stroke-width="2" rx="5"/>
  <text x="210" y="110" text-anchor="middle" font-size="16" font-weight="bold">Global Settings</text>
  <text x="70" y="140" font-size="12">• User identity</text>
  <text x="70" y="160" font-size="12">• Editor preference</text>
  <text x="70" y="180" font-size="12">• Common aliases</text>
  <text x="70" y="200" font-size="12">• Color preferences</text>
  <rect x="430" y="80" width="320" height="150" fill="#E3F2FD" stroke="#1976D2" stroke-width="2" rx="5"/>
  <text x="590" y="110" text-anchor="middle" font-size="16" font-weight="bold">Local Settings</text>
  <text x="450" y="140" font-size="12">• Project-specific user</text>
  <text x="450" y="160" font-size="12">• Special workflows</text>
  <text x="450" y="180" font-size="12">• Hooks configuration</text>
  <text x="450" y="200" font-size="12">• Signing requirements</text>
  <rect x="50" y="250" width="320" height="150" fill="#FFF3E0" stroke="#F57C00" stroke-width="2" rx="5"/>
  <text x="210" y="280" text-anchor="middle" font-size="16" font-weight="bold">Team Settings</text>
  <text x="70" y="310" font-size="12">• .gitignore (tracked)</text>
  <text x="70" y="330" font-size="12">• .gitattributes (tracked)</text>
  <text x="70" y="350" font-size="12">• .editorconfig (tracked)</text>
  <text x="70" y="370" font-size="12">• Hooks in repo</text>
  <rect x="430" y="250" width="320" height="150" fill="#FFEBEE" stroke="#C62828" stroke-width="2" rx="5"/>
  <text x="590" y="280" text-anchor="middle" font-size="16" font-weight="bold">Never Share</text>
  <text x="450" y="310" font-size="12">• Credentials</text>
  <text x="450" y="330" font-size="12">• Personal paths</text>
  <text x="450" y="350" font-size="12">• IDE-specific configs</text>
  <text x="450" y="370" font-size="12">• Local experiments</text>
</svg>

---

## Template Directory

```bash
# Set up template directory
git config --global init.templateDir ~/.git-templates

# Create template structure
mkdir -p ~/.git-templates/hooks
mkdir -p ~/.git-templates/info

# Add default hooks
cp my-pre-commit ~/.git-templates/hooks/pre-commit
chmod +x ~/.git-templates/hooks/pre-commit

# Add default excludes
echo "*.swp" > ~/.git-templates/info/exclude

# Now every 'git init' copies these templates
git init new-project
# Automatically includes your hooks and excludes!
```

---

## Custom Git Commands

```bash
# Create custom Git command
# Save as: /usr/local/bin/git-standup
#!/bin/bash
git log --since=yesterday --author="$(git config user.name)" \
    --pretty=format:"%Cred%h%Creset - %s %Cgreen(%cr)%Creset"

# Make executable
chmod +x /usr/local/bin/git-standup

# Use it
git standup  # Shows your commits since yesterday
```

**Any executable named `git-*` becomes a Git subcommand!**

---

## Configuration Security

```bash
# Never commit sensitive data
# Use environment variables instead

# Bad - credentials in config
git config --global github.token "ghp_xxxxxxxxxxxx"

# Good - reference environment variable
export GITHUB_TOKEN="ghp_xxxxxxxxxxxx"
# Use in scripts: $GITHUB_TOKEN

# Protect local config
chmod 600 ~/.gitconfig
chmod 600 ~/.git-credentials

# Audit your configuration
git config --list | grep -i token
git config --list | grep -i password
```

---

## Debugging Configuration

```bash
# See where each setting comes from
git config --list --show-origin

# Debug specific command
GIT_TRACE=1 git status

# Debug configuration loading
GIT_TRACE_CONFIG=1 git status

# Debug performance
GIT_TRACE_PERFORMANCE=1 git status

# Debug pack operations
GIT_TRACE_PACK_ACCESS=1 git gc

# Debug curl (for HTTPS)
GIT_CURL_VERBOSE=1 git fetch
```

---

## Common Configuration Issues

**Problem**: Wrong email in commits

```bash
# Fix for future commits
git config user.email "correct@email.com"

# Fix last commit
git commit --amend --author="Name <correct@email.com>"
```

**Problem**: Line ending issues
```bash
# Windows
git config --global core.autocrlf true
# Mac/Linux
git config --global core.autocrlf input
```

**Problem**: SSL certificate errors
```bash
# Temporary fix (NOT RECOMMENDED)
git config --global http.sslVerify false
# Better: Add certificate to system
```

---

## Backup Your Configuration

```bash
# Backup global config
cp ~/.gitconfig ~/.gitconfig.backup

# Version control your dotfiles
mkdir ~/dotfiles
cp ~/.gitconfig ~/dotfiles/
cp ~/.gitignore_global ~/dotfiles/
cd ~/dotfiles
git init
git add .
git commit -m "Initial dotfiles"

# Restore on new machine
cp ~/dotfiles/.gitconfig ~/
cp ~/dotfiles/.gitignore_global ~/
```

---

## EditorConfig Integration

**.editorconfig:**
```ini
# EditorConfig helps maintain consistent coding styles
root = true

[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
trim_trailing_whitespace = true
indent_style = space
indent_size = 4

[*.{js,json,yml}]
indent_size = 2

[*.md]
trim_trailing_whitespace = false

[Makefile]
indent_style = tab
```

### Works with most editors and IDEs automatically

---

## Configuration Examples by Role

## For Developers
```bash
git config --global core.editor "code --wait"
git config --global merge.tool vscode
git config --global pull.rebase true
```

## For DevOps
```bash
git config --global alias.deploy '!git push production main'
git config --global push.followTags true
git config --global tag.sort -version:refname
```

## For Team Leads
```bash
git config --global alias.team-log 'shortlog -sn --all'
git config --global alias.recent-branches \
    'for-each-ref --sort=-committerdate refs/heads/'
```

---

## Summary

## What We Learned

1. ✅ Three configuration levels (system, global, local)
1. ✅ Essential configurations for daily use
1. ✅ Creating powerful aliases
1. ✅ SSH and GPG setup
1. ✅ Advanced `.gitignore` patterns
1. ✅ Git hooks for automation
1. ✅ Performance optimizations
1. ✅ Security best practices

---

## Key Takeaways

1. **Start with essentials** - Name, email, editor
1. **Use aliases** - Save time with shortcuts
1. **Leverage hooks** - Automate quality checks
1. **Secure credentials** - Never commit secrets
1. **Share team settings** - Use `.gitignore` and `.gitattributes`
1. **Customize per project** - Local configs override global

---

## Configuration Checklist

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="40" text-anchor="middle" font-size="24" font-weight="bold">Your Git Setup Checklist</text>
  <rect x="100" y="70" width="600" height="300" fill="#F5F5F5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="120" y="100" font-size="14">☐ Set user.name and user.email</text>
  <text x="120" y="125" font-size="14">☐ Configure preferred editor</text>
  <text x="120" y="150" font-size="14">☐ Set up SSH keys</text>
  <text x="120" y="175" font-size="14">☐ Create essential aliases</text>
  <text x="120" y="200" font-size="14">☐ Configure credential helper</text>
  <text x="120" y="225" font-size="14">☐ Set up global .gitignore</text>
  <text x="120" y="250" font-size="14">☐ Configure line endings</text>
  <text x="120" y="275" font-size="14">☐ Enable colors</text>
  <text x="120" y="300" font-size="14">☐ Set default branch name</text>
  <text x="120" y="325" font-size="14">☐ Configure pull strategy</text>
  <text x="120" y="350" font-size="14">☐ Optional: Set up GPG signing</text>
</svg>

---

## Practice Exercises

1. Create a complete Git configuration for your workflow
1. Set up 10 useful aliases for common operations
1. Create a pre-commit hook that checks code quality
1. Configure different emails for work and personal projects
1. Set up SSH keys for GitHub/GitLab
1. Create a global `.gitignore` for your development environment

---

## Next Up: Undoing Things

In the next session, we'll explore:

1. Why and when to rewrite history
1. Amending commits
1. Reset vs revert
1. Interactive rebase
1. Cherry-picking changes
1. Recovering "lost" commits
1. Extreme undoing techniques

---

## Configuration Complete! 🎉

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="80" text-anchor="middle" font-size="32" font-weight="bold" fill="#4CAF50">Git is Now Your Tool!</text>
  <rect x="200" y="120" width="400" height="200" fill="#E8F5E9" stroke="#388E3C" stroke-width="3" rx="10"/>
  <text x="400" y="165" text-anchor="middle" font-size="20">Configured for:</text>
  <text x="400" y="195" text-anchor="middle" font-size="16">• Maximum efficiency</text>
  <text x="400" y="220" text-anchor="middle" font-size="16">• Your workflow</text>
  <text x="400" y="245" text-anchor="middle" font-size="16">• Team collaboration</text>
  <text x="400" y="270" text-anchor="middle" font-size="16">• Security & performance</text>
  <circle cx="300" cy="350" r="25" fill="#2196F3"/>
  <text x="300" y="357" text-anchor="middle" font-size="20" fill="white">⚙️</text>
  <circle cx="400" cy="350" r="25" fill="#FF9800"/>
  <text x="400" y="357" text-anchor="middle" font-size="20" fill="white">🚀</text>
  <circle cx="500" cy="350" r="25" fill="#9C27B0"/>
  <text x="500" y="357" text-anchor="middle" font-size="20" fill="white">✨</text>
</svg>
