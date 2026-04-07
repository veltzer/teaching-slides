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

![configuration_levels](/svg/courses/git/git2/03_config/configuration_levels.svg)

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

![color_configuration](/svg/courses/git/git2/03_config/color_configuration.svg)

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

![creating_aliases](/svg/courses/git/git2/03_config/creating_aliases.svg)

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

![ssh_configuration](/svg/courses/git/git2/03_config/ssh_configuration.svg)

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

```config
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

![whitespace_configuration](/svg/courses/git/git2/03_config/whitespace_configuration.svg)

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

```config
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

![configuration_best_practices](/svg/courses/git/git2/03_config/configuration_best_practices.svg)

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

![configuration_checklist](/svg/courses/git/git2/03_config/configuration_checklist.svg)

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

![configuration_complete](/svg/courses/git/git2/03_config/configuration_complete.svg)
