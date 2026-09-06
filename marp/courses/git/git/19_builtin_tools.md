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

# Built-in Tools

---

## What We'll Cover

1. `git instaweb` - Quick repository web interface
1. `git daemon` - Git protocol server
1. `git http-backend` - HTTP protocol support
1. `git shell` - Restricted shell for Git users
1. `git export` - Repository export functionality
1. `git bisect` - Binary search for bugs
1. `git describe` - Human-readable commit names
1. `git archive` - Create project archives
1. `git bundle` - Repository bundles
1. `git submodule` - Subproject management
1. `git notes` - Attach notes to commits

---

## Git Built-in Tools Overview

![git_tools_overview](svg/courses/git/git/19_builtin_tools/git_tools_overview.svg)

---

## Git Instaweb

Quickly start a web interface for your repository:

```bash
# Start web interface (default: lighttpd on port 1234)
git instaweb

# Start with specific web server
git instaweb --httpd=webrick     # Ruby WEBrick
git instaweb --httpd=apache2     # Apache
git instaweb --httpd=nginx       # Nginx

# Specify port
git instaweb --port=8080

# Start and browse automatically
git instaweb --start --browser=firefox

# Stop web interface
git instaweb --stop
```

**What instaweb provides:**
- Repository browsing interface
- Commit history viewing
- File content inspection
- Diff visualization
- Branch and tag navigation

**Use cases:**
- Quick repository sharing
- Code review in web interface
- Demo repository contents
- Temporary web access

---

## Git Daemon

Run a Git protocol server for repository sharing:

```bash
# Basic daemon (serves current directory)
git daemon --verbose --export-all

# Serve specific directory
git daemon --base-path=/var/git --export-all

# Enable upload-pack (clone/fetch)
git daemon --export-all --enable=upload-pack

# Enable receive-pack (push) - DANGEROUS
git daemon --export-all --enable=receive-pack

# Run on specific port and interface
git daemon --port=9418 --listen=192.168.1.100

# Run as system daemon
git daemon --detach --syslog --export-all --base-path=/var/git
```

**Daemon configuration:**
- Uses Git protocol (port 9418)
- Read-only by default
- No authentication built-in
- Fast for local networks

---

## Git HTTP Backend

CGI program for serving Git over HTTP:

```bash
# Apache configuration example
# /etc/apache2/sites-available/git.conf

<VirtualHost *:80>
    ServerName git.example.com
    DocumentRoot /var/git

    SetEnv GIT_PROJECT_ROOT /var/git
    SetEnv GIT_HTTP_EXPORT_ALL

    ScriptAlias /git/ /usr/lib/git-core/git-http-backend/

    <Directory "/usr/lib/git-core">
        Options ExecCGI
        AllowOverride None
        Require all granted
    </Directory>

    <LocationMatch "^/git/.*/git-receive-pack$">
        AuthType Basic
        AuthName "Git Push"
        AuthUserFile /etc/git-auth
        Require valid-user
    </LocationMatch>
</VirtualHost>
```

**HTTP backend features:**
- Standard HTTP/HTTPS protocols
- Authentication support
- Firewall-friendly
- Web server integration

---

## Git Shell

Restricted shell for Git-only access:

```bash
# Install git-shell
which git-shell
# /usr/bin/git-shell

# Create Git user with git-shell
sudo useradd -m -s /usr/bin/git-shell git

# Set up SSH key access
sudo -u git mkdir /home/git/.ssh
sudo -u git chmod 700 /home/git/.ssh

# Add user's public key
echo "ssh-rsa AAAAB3N... user@host" | sudo -u git tee /home/git/.ssh/authorized_keys

# Create repository directory
sudo -u git mkdir /home/git/repositories
sudo -u git git init --bare /home/git/repositories/project.git
```

**Git shell customization:**

```bash
# Create git-shell-commands directory
sudo -u git mkdir /home/git/git-shell-commands

# Add custom commands
sudo -u git cat > /home/git/git-shell-commands/list << 'EOF'
#!/bin/sh
ls -la /home/git/repositories/
EOF

sudo -u git chmod +x /home/git/git-shell-commands/list
```

---

## Git Bisect

Binary search to find bug-introducing commits:

```bash
# Start bisect session
git bisect start

# Mark current commit as bad
git bisect bad

# Mark known good commit
git bisect good v1.0

# Git will checkout middle commit
# Test the commit, then mark as good or bad
git bisect good    # Current commit is good
# or
git bisect bad     # Current commit is bad

# Continue until bug is found
# Git will show the first bad commit

# End bisect session
git bisect reset
```

---

## Git Bisect: Automated

**Automated bisect:**

```bash
# Use script for automated testing
git bisect start HEAD v1.0
git bisect run ./test-script.sh

# Example test script
#!/bin/sh
# test-script.sh
make clean && make
if [ $? -ne 0 ]; then
    exit 125  # Skip this commit (build failed)
fi

./run-tests
if [ $? -eq 0 ]; then
    exit 0    # Good commit
else
    exit 1    # Bad commit
fi
```

---

## Git Describe

Generate human-readable names for commits:

```bash
# Describe current commit
git describe
# Output: v1.2.0-14-g2414721

# Describe specific commit
git describe a1b2c3d

# Always use long format
git describe --long
# Output: v1.2.0-14-g2414721-dirty

# Use abbreviated commit hash
git describe --abbrev=10

# Include all refs (not just tags)
git describe --all

# Only use annotated tags
git describe --tags

# Describe with dirty working directory
git describe --dirty
# Output: v1.2.0-14-g2414721-dirty
```

**Describe format explanation:**
- `v1.2.0`: Most recent tag
- `14`: Number of commits since tag
- `g2414721`: 'g' + abbreviated commit hash
- `dirty`: Working directory has changes

---

## Git Archive

Create archives of repository contents:

```bash
# Create tar archive of current HEAD
git archive --format=tar HEAD | gzip > project.tar.gz

# Create zip archive
git archive --format=zip HEAD > project.zip

# Archive specific commit/tag
git archive --format=tar v1.0 | gzip > project-v1.0.tar.gz

# Archive with prefix (creates subdirectory)
git archive --prefix=project-1.0/ --format=tar HEAD > project.tar

# Archive specific subdirectory
git archive HEAD:src/ | tar -x

# Archive to stdout and extract directly
git archive HEAD | tar -x -C /tmp/extracted/
```

**Archive options:**
- Multiple formats (tar, zip, tar.gz)
- Specific commits, tags, or branches
- Directory prefixes
- Subdirectory selection
- Custom compression

---

## Git Bundle

Create portable repository bundles:

```bash
# Create bundle with all history
git bundle create project.bundle --all

# Create bundle with specific range
git bundle create recent.bundle HEAD~10..HEAD

# Create bundle with all branches
git bundle create all-branches.bundle --branches

# Create bundle with tags
git bundle create tagged.bundle --tags

# Verify bundle integrity
git bundle verify project.bundle

# List bundle contents
git bundle list-heads project.bundle

# Clone from bundle
git clone project.bundle cloned-repo

# Fetch from bundle
git remote add bundle-origin project.bundle
git fetch bundle-origin
```

**Bundle use cases:**
- Offline repository transfer
- Backup creation
- Air-gapped environments
- Large repository distribution

---

## Git Submodule (Built-in Commands)

Manage subprojects within repositories:

```bash
# Add submodule
git submodule add https://github.com/user/lib.git lib

# Initialize submodules after clone
git submodule init

# Update submodules to latest
git submodule update

# Initialize and update in one command
git submodule update --init --recursive

# Execute command in all submodules
git submodule foreach 'git checkout main'

# Check submodule status
git submodule status

# Sync submodule URLs
git submodule sync

# Remove submodule
git submodule deinit lib
git rm lib
```

**Submodule workflow integration:**

```bash
# Update all submodules to latest remote
git submodule foreach git pull origin main

# Push all submodules
git submodule foreach git push

# Show summary of submodule changes
git submodule summary
```

---

## Git Notes

Attach notes to commits without changing commit history:

```bash
# Add note to current commit
git notes add -m "This commit fixes memory leak"

# Add note to specific commit
git notes add -m "Performance improvement" a1b2c3d

# Edit note with editor
git notes edit

# Show notes for commit
git notes show
git notes show a1b2c3d

# List all notes
git notes list

# Remove note
git notes remove
git notes remove a1b2c3d

# Copy note from one commit to another
git notes copy a1b2c3d d4e5f6g
```

**Notes namespaces:**

```bash
# Use different note namespaces
git notes --ref=bugs add -m "Bug report #123" a1b2c3d
git notes --ref=review add -m "Code review passed" a1b2c3d

# Show notes from specific namespace
git notes --ref=bugs show a1b2c3d

# Configure default notes display
git config notes.displayRef refs/notes/bugs
git config --add notes.displayRef refs/notes/review
```

---

## Git Maintenance Tools

Built-in repository maintenance utilities:

**Git GC (Garbage Collection):**

```bash
# Basic garbage collection
git gc

# Aggressive garbage collection
git gc --aggressive

# Auto garbage collection
git gc --auto

# Prune objects older than date
git gc --prune=1.week.ago

# Show what would be removed
git gc --dry-run
```

**Git FSCK (File System Check):**

```bash
# Check repository integrity
git fsck

# Verbose output
git fsck --verbose

# Check connectivity only
git fsck --connectivity-only

# Show dangling objects
git fsck --dangling

# Full check including unreachable objects
git fsck --full
```

---

## Git Clean

Remove untracked files and directories:

```bash
# Show what would be removed (dry run)
git clean -n

# Remove untracked files
git clean -f

# Remove untracked files and directories
git clean -fd

# Interactive cleaning
git clean -i

# Remove ignored files too
git clean -fx

# Clean specific paths
git clean -f path/to/directory/

# Exclude files from cleaning
git clean -f -e "*.log"
```

**Clean safety features:**
- Requires `-f` flag for actual removal
- Dry run mode for preview
- Interactive mode for selection
- Pattern exclusions

---

## Git Reflog

Reference logs for recovery and debugging:

```bash
# Show reflog for current branch
git reflog

# Show reflog for specific reference
git reflog main
git reflog HEAD

# Show reflog with dates
git reflog --date=iso

# Expire old reflog entries
git reflog expire --expire=30.days.ago --all

# Delete reflog for branch
git reflog delete main@{5}

# Show reflog for all references
git reflog --all

# Use reflog for recovery
git reset --hard HEAD@{2}
```

**Reflog use cases:**
- Recover lost commits
- Undo dangerous operations
- Debug reference changes
- Audit repository activity

---

## Git Filter-Branch

Rewrite repository history:

```bash
# Remove file from all history
git filter-branch --tree-filter 'rm -f passwords.txt' HEAD

# Rewrite author information
git filter-branch --env-filter '
    if [ "$GIT_COMMITTER_EMAIL" = "old@example.com" ]; then
        export GIT_COMMITTER_EMAIL="new@example.com"
        export GIT_AUTHOR_EMAIL="new@example.com"
    fi
' HEAD

# Keep only specific subdirectory
git filter-branch --subdirectory-filter src HEAD

# Remove empty commits
git filter-branch --prune-empty HEAD
```

**Warning:** Filter-branch is deprecated in favor of `git filter-repo` (external tool).

---

## Git Worktree Management

Advanced worktree operations:

```bash
# List worktrees
git worktree list

# Add new worktree
git worktree add ../feature-branch feature-branch

# Remove worktree
git worktree remove ../feature-branch

# Prune stale worktrees
git worktree prune

# Move worktree
git worktree move ../old-path ../new-path

# Lock worktree to prevent removal
git worktree lock ../important-work
```

**Worktree maintenance:**

```bash
# Repair worktree after manual move
git worktree repair ../moved-worktree

# Show worktree information
git worktree list --porcelain

# Unlock worktree
git worktree unlock ../important-work
```

---

## Git Remote Helpers

Extend Git with custom protocols:

**Custom remote helper structure:**

```bash
#!/bin/sh
# git-remote-custom

# Handle capabilities query
if [ "$1" = "capabilities" ]; then
    echo "connect"
    echo ""
    exit 0
fi

# Handle connect command
if [ "$1" = "connect" ]; then
    service="$2"
    url="$3"

    # Custom protocol handling
    exec /path/to/custom-transport "$service" "$url"
fi
```

**Using remote helpers:**

```bash
# Add remote with custom protocol
git remote add origin custom://server/repository

# Git will call git-remote-custom helper
git fetch origin
```

---

## Performance and Debugging Tools

Built-in tools for optimization and troubleshooting:

**Git Count-Objects:**

```bash
# Show object count and size
git count-objects -v

# Output includes:
# count: loose objects
# size: disk space used by loose objects
# in-pack: objects in packfiles
# packs: number of packfiles
# size-pack: disk space used by packfiles
# prune-packable: loose objects also in packs
# garbage: files in object db that aren't objects
```

**Git Verify-Pack:**

```bash
# Verify and show packfile contents
git verify-pack -v .git/objects/pack/pack-*.idx

# Show only statistics
git verify-pack -s .git/objects/pack/pack-*.idx

# Sort by size
git verify-pack -v .git/objects/pack/pack-*.idx | sort -k3 -n
```

**Git Hash-Object:**

```bash
# Create object from file
git hash-object file.txt

# Write object to database
git hash-object -w file.txt

# Create object from stdin
echo "content" | git hash-object --stdin

# Show object type
git cat-file -t a1b2c3d
```

---

## Configuration and Help Tools

Built-in configuration and documentation:

**Git Config Management:**

```bash
# List all configuration
git config --list

# Show configuration with origins
git config --list --show-origin

# Edit configuration file
git config --global --edit

# Get specific configuration
git config user.name

# Set configuration
git config --global user.email "user@example.com"

# Unset configuration
git config --global --unset user.signingkey
```

**Git Help System:**

```bash
# Show help for command
git help commit
git commit --help

# Show available commands
git help -a

# Show Git guides
git help -g

# Show help in web browser
git help -w log

# Show concept guides
git help revisions
git help workflows
```

---

## Integration Examples

Combining built-in tools for workflows:

**Release script using multiple tools:**

```bash
#!/bin/bash
# release.sh

VERSION=$1
if [ -z "$VERSION" ]; then
    echo "Usage: $0 <version>"
    exit 1
fi

# Clean repository
git clean -fd
git gc

# Create and verify bundle for backup
git bundle create "release-$VERSION.bundle" --all
git bundle verify "release-$VERSION.bundle"

# Create archive
git archive --format=tar --prefix="project-$VERSION/" HEAD | gzip > "project-$VERSION.tar.gz"

# Tag release
git tag -a "v$VERSION" -m "Release version $VERSION"

# Generate release notes using describe
PREV_TAG=$(git describe --tags --abbrev=0 HEAD^)
echo "Changes since $PREV_TAG:"
git log --oneline "$PREV_TAG"..HEAD

# Start instaweb for release review
git instaweb --start
```

---

## Security Considerations

Security aspects of built-in tools:

**Daemon security:**

```bash
# Run daemon with restricted access
git daemon --export-all --base-path=/var/git \
           --user=git --group=git \
           --strict-paths \
           --forbid-override=daemon

# Use git-shell for SSH access
echo "git:x:1001:1001:Git User:/home/git:/usr/bin/git-shell" >> /etc/passwd
```

**HTTP backend security:**

```apache
# Secure HTTP backend configuration
<Location "/git">
    AuthType Basic
    AuthName "Git Access"
    AuthUserFile /etc/git-passwd
    Require valid-user

    # Disable receive-pack for read-only access
    <LocationMatch ".*/git-receive-pack$">
        Require group git-writers
    </LocationMatch>
</Location>
```

---

## Lab Exercise: Built-in Tools Mastery

**Scenario:** Set up a complete Git infrastructure using only built-in tools for a small development team.

**Setup tasks:**
1. **Repository server setup:**
    - Configure git daemon for local network access
    - Set up HTTP backend with authentication
    - Create restricted git-shell users

1. **Workflow tools:**
    - Use git bisect to find a bug
    - Create release archives and bundles
    - Implement git notes for code reviews

1. **Maintenance procedures:**
    - Set up automated garbage collection
    - Create repository integrity checks
    - Implement backup strategies using bundles

**Advanced tasks:**
1. **Integration scripting:**
    - Combine multiple tools in release scripts
    - Create monitoring and reporting tools
    - Implement automated maintenance

1. **Performance optimization:**
    - Analyze repository performance
    - Optimize pack files and objects
    - Create performance monitoring

**Deliverables:** Complete Git infrastructure setup, workflow automation scripts, maintenance procedures, security configuration, and team documentation.

---

## Summary: Leveraging Git's Built-in Tools

**Key takeaways:**

1. **Rich toolset included:**
    - Git includes comprehensive tools for most needs
    - Built-in tools are well-tested and reliable
    - Often more efficient than external alternatives

1. **Server and sharing capabilities:**
    - Multiple protocols (Git, HTTP, SSH)
    - Authentication and access control
    - Portable bundles for offline sharing

1. **Maintenance and debugging:**
    - Repository health monitoring
    - Performance optimization tools
    - Recovery and troubleshooting utilities

1. **Workflow integration:**
    - Tools can be combined effectively
    - Scripting enables automation
    - Built-in help and documentation

**Remember:** Git's built-in tools provide a comprehensive foundation for version control workflows. While external tools can add convenience and features, understanding and leveraging Git's built-in capabilities ensures you can work effectively in any environment and provides a solid foundation for building custom solutions.
