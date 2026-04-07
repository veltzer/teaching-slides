# Work Trees

---

## What We'll Cover

1. Why worktrees are needed
1. Creating and managing worktrees
1. Working with multiple worktrees
1. Pruning and cleaning up worktrees
1. Advanced worktree scenarios
1. Best practices and limitations

---

## Why Are Worktrees Needed?

Traditional Git workflow limitations:

**Single working directory problem:**
- Can only work on one branch at a time
- Switching branches affects entire working directory
- Context switching is expensive
- Parallel work requires multiple clones

**Common scenarios requiring worktrees:**
- Testing a feature while developing another
- Quick hotfixes without losing current work
- Code review of different branches
- Parallel builds or testing
- Long-running experiments

```bash
# Traditional approach (problematic)
git stash                    # Save current work
git checkout hotfix-branch   # Switch context
# Make hotfix
git checkout feature-branch  # Switch back
git stash pop               # Restore work
```

---

## What Are Git Worktrees?

Worktrees allow multiple working directories for a single repository:

**Key concepts:**
- **Main worktree:** Original repository location
- **Linked worktrees:** Additional working directories
- **Shared repository:** Common `.git` directory
- **Separate branches:** Each worktree can be on different branch

![what_are_git_worktrees](/svg/courses/git/git2/12_work_trees/what_are_git_worktrees.svg)

---

## Creating Your First Worktree

Basic worktree creation:

```bash
# Create worktree from existing branch
git worktree add ../feature-login feature-login

# Create worktree with new branch
git worktree add ../hotfix-security -b hotfix-security

# Create worktree from specific commit
git worktree add ../experiment a1b2c3d

# Create worktree in subdirectory
git worktree add worktrees/testing testing-branch
```

**What happens during creation:**
1. New directory created at specified path
1. Branch checked out in new directory
1. Worktree registered in `.git/worktrees/`
1. `.git` file created pointing to main repository

---

## Worktree Directory Structure

Understanding the layout:

**Main repository:**

```tree
project/
├── .git/                    # Main Git directory
│   ├── worktrees/          # Worktree metadata
│   │   ├── feature-login/  # Worktree-specific data
│   │   └── hotfix/
├── src/
└── README.md
```

**Linked worktree:**

```tree
feature-login/              # Worktree directory
├── .git                   # File pointing to main .git
├── src/                   # Working files (different from main)
└── README.md
```

**Worktree metadata:**

```tree
.git/worktrees/feature-login/
├── HEAD                   # Current branch/commit
├── gitdir                # Path to worktree directory
├── commondir             # Path to shared Git data
└── logs/                 # Worktree-specific logs
```

---

## Working with Multiple Worktrees

Managing multiple development contexts:

```bash
# List all worktrees
git worktree list

# Output:
/home/user/project           a1b2c3d [main]
/home/user/feature-login     d4e5f6g [feature-login]
/home/user/hotfix           g7h8i9j [hotfix-security]

# Detailed worktree information
git worktree list --porcelain

# Navigate between worktrees
cd ../feature-login    # Switch to different worktree
git status            # Shows status for this worktree only
```

**Each worktree maintains:**
- Separate working directory
- Independent HEAD pointer
- Own staging area (index)
- Individual file modifications
- Separate stash (if any)

---

## Branch Management with Worktrees

Worktrees and branches have special relationships:

```bash
# Create worktree with new branch
git worktree add ../new-feature -b new-feature origin/main

# Check out existing branch (if not already checked out)
git worktree add ../existing-feature existing-feature

# Error: branch already checked out
git worktree add ../duplicate main
# fatal: 'main' is already checked out at '/home/user/project'
```

**Important restrictions:**
- Same branch cannot be checked out in multiple worktrees
- Prevents conflicts and confusion
- Use different branches for different worktrees
- Exception: detached HEAD state

**Working around restrictions:**
```bash
# Create new branch based on existing one
git worktree add ../main-copy -b main-copy main
```

---

## Moving and Renaming Worktrees

Relocating worktrees:

```bash
# Move worktree to new location
git worktree move ../feature-login ../renamed-feature

# Update worktree path after manual move
mv ../feature-login ../new-location
git worktree repair ../new-location

# List worktrees to verify
git worktree list
```

**When to move worktrees:**
- Better organization of directories
- Different filesystem or drive
- Renaming for clarity
- Temporary relocation

**What gets updated:**
- Worktree registration in `.git/worktrees/`
- Path references in metadata
- `.git` file in worktree directory

---

## Removing Worktrees

Clean removal of worktrees:

```bash
# Remove worktree (safe method)
git worktree remove ../feature-login

# Force removal (even with uncommitted changes)
git worktree remove --force ../feature-login

# Remove after manual deletion
rm -rf ../feature-login
git worktree prune
```

**Removal checks:**
- Uncommitted changes (blocks removal unless forced)
- Untracked files (warning but allows removal)
- Current worktree (cannot remove current location)

**What gets cleaned up:**
- Worktree directory and files
- Worktree metadata from `.git/worktrees/`
- Associated branch (if orphaned)

---

## Pruning Worktrees

Cleaning up stale worktree references:

```bash
# Show what would be pruned
git worktree prune --dry-run

# Actually prune stale worktrees
git worktree prune

# Prune with custom expiry time
git worktree prune --expire=7.days.ago

# Verbose pruning
git worktree prune --verbose
```

**When pruning is needed:**
- Worktree directories manually deleted
- Network shares become unavailable
- System crashes or interruptions
- Storage device failures

**Prune criteria:**
- Worktree directory no longer exists
- Worktree directory not accessible
- Worktree corrupted or invalid

---

## Worktree Locking and Unlocking

Protecting worktrees from automatic cleanup:

```bash
# Lock a worktree with reason
git worktree lock ../important-feature --reason "Long-running experiment"

# Unlock worktree
git worktree unlock ../important-feature

# List locked worktrees
git worktree list
# Output shows [locked] status

# Force operations on locked worktrees
git worktree prune # Won't remove locked worktrees
git worktree remove --force ../important-feature # Still respects lock
```

**Use cases for locking:**
- Prevent accidental removal
- Network-mounted worktrees
- Shared development environments
- Long-term experimental branches
- CI/CD working directories

---

## Bare Repository Worktrees

Using worktrees with bare repositories:

```bash
# Clone as bare repository
git clone --bare https://github.com/user/repo.git project.git

# Create worktrees from bare repo
cd project.git
git worktree add ../main main
git worktree add ../develop develop
git worktree add ../feature-new -b feature-new

# All development in worktrees, no main working directory
```

**Benefits of bare + worktrees:**
- No "main" working directory confusion
- All branches equal status
- Cleaner organization
- Server-like setup locally
- Better for multiple simultaneous branches

---

## Worktree-Specific Configuration

Some Git settings can be worktree-specific:

```bash
# Set worktree-specific configuration
cd feature-worktree
git config user.email "feature-dev@company.com"

# Check configuration scope
git config --show-origin user.email

# Worktree-specific gitignore (not standard)
# Use .git/info/exclude in main repo
echo "*.local" >> .git/info/exclude
```

**Configuration hierarchy in worktrees:**
1. Worktree-specific (if supported)
1. Repository-local (shared across worktrees)
1. User global
1. System

**Shared vs separate:**
- **Shared:** Most configuration, hooks, references
- **Separate:** HEAD, index, working files, some logs

---

## Advanced Worktree Scenarios

**Cross-platform development:**
```bash
# Different worktrees for different platforms
git worktree add ../linux-build -b linux-build
git worktree add ../windows-build -b windows-build
git worktree add ../macos-build -b macos-build
```

**Testing different versions:**

```bash
# Worktrees for different releases
git worktree add ../v1.0-test v1.0
git worktree add ../v2.0-test v2.0
git worktree add ../main-test main

# Run tests in parallel
cd ../v1.0-test && npm test &
cd ../v2.0-test && npm test &
cd ../main-test && npm test &
```

**Code review workflow:**

```bash
# Create worktree for PR review
git fetch origin pull/123/head:pr-123
git worktree add ../pr-123-review pr-123

# Review in separate environment
cd ../pr-123-review
# Test, review, make notes
```

---

## Performance Considerations

**Storage efficiency:**
- Object database shared across worktrees
- Only working files duplicated
- Significant space savings vs multiple clones

**Operation speed:**
- Faster than cloning for new branches
- No network operations needed
- Instant branch switching between worktrees

**Memory usage:**
- Each worktree needs separate index
- File system cache for each working directory
- Consider system resources with many worktrees

**Comparison with alternatives:**

| Operation | Multiple Clones | Worktrees | Stash/Switch |
|-----------|----------------|-----------|--------------|
| Disk Usage | High | Low | Lowest |
| Setup Time | Slow | Fast | Fastest |
| Parallel Work | Excellent | Excellent | Poor |
| Network Deps | Required | None | None |

---

## Worktree Limitations and Gotchas

**Branch restrictions:**

```bash
# This fails if main is already checked out
git worktree add ../duplicate main
# fatal: 'main' is already checked out

# Workaround: create new branch
git worktree add ../main-copy -b main-copy main
```

**Path requirements:**
- Worktrees must be outside main repository
- Cannot be subdirectories of main repo
- Paths must not exist or be empty directories

**Submodule considerations:**
- Submodules need separate initialization in each worktree
- Submodule paths relative to each worktree
- More complex setup and maintenance

**Hook behavior:**
- Hooks shared across all worktrees
- May cause unexpected behavior
- Consider worktree-aware hooks

---

## Worktree Maintenance

**Regular maintenance tasks:**

```bash
# Weekly cleanup routine
git worktree prune --dry-run    # Check what would be pruned
git worktree prune             # Remove stale worktrees
git worktree list              # Verify active worktrees

# Monthly deep clean
git gc                         # Cleanup shared object database
git fsck                       # Verify repository integrity

# Monitor disk usage
du -sh .git                    # Main repository size
du -sh ../worktree-*          # Individual worktree sizes
```

**Backup considerations:**
- Main `.git` directory contains everything critical
- Worktree directories contain only working files
- Include `.git/worktrees/` metadata in backups
- Can recreate worktrees from metadata

---

## Troubleshooting Worktrees

**Common issues and solutions:**

### Issue: "Worktree directory not found"

```bash
# Solution: Repair or prune
git worktree repair ../missing-worktree
# or
git worktree prune
```

### Issue: "Cannot remove worktree with changes"

```bash
# Solution: Force removal or commit changes
git worktree remove --force ../worktree-name
# or commit/stash changes first
```

### Issue: "Branch already checked out"

```bash
# Solution: Use different branch or create new one
git worktree add ../new-location -b new-branch existing-branch
```

### Issue: "Worktree appears corrupted"

```bash
# Solution: Remove and recreate
git worktree remove --force ../corrupted
git worktree add ../recreated branch-name
```

---

## Integration with Development Tools

**IDE support:**
- VS Code: Can open different worktrees in separate windows
- IntelliJ: Project-level awareness of worktrees
- Vim: Works naturally with different directories

**Build system integration:**
```bash
# Parallel builds in different worktrees
cd ../feature-worktree && make build &
cd ../main-worktree && make build &
wait  # Wait for both builds
```

**CI/CD considerations:**
- Use worktrees for parallel testing
- Separate build environments
- Isolated dependency installation

**Script automation:**
```bash
#!/bin/bash
# Create worktree for each active PR
for pr in $(gh pr list --json number --jq '.[].number'); do
    git fetch origin pull/$pr/head:pr-$pr
    git worktree add ../pr-$pr pr-$pr
done
```

---

## Worktree Best Practices

**Naming conventions:**

```bash
# Consistent naming scheme
git worktree add ../feature-user-auth feature-user-auth
git worktree add ../hotfix-security-fix hotfix-security-fix
git worktree add ../pr-123-review pr-123

# Avoid spaces and special characters
# Use descriptive names
# Include branch name or purpose
```

**Organization strategies:**

```tree
project/                    # Main repository
├── .git/
├── src/
worktrees/                 # Dedicated worktree directory
├── feature-auth/
├── hotfix-security/
└── experiment-ai/
```

**Cleanup routine:**
1. Remove completed worktrees promptly
1. Lock long-term worktrees
1. Regular pruning of stale references
1. Monitor disk usage
1. Document active worktrees for team

---

## Team Workflows with Worktrees

**Individual developer benefits:**
- Work on multiple features simultaneously
- Quick context switching
- Parallel testing
- Isolated experiments

**Team considerations:**
- Worktrees are local to each developer
- Shared workflows still use branches
- Documentation of worktree usage
- Consistent naming conventions

**Communication strategies:**
```bash
# Document active worktrees
git worktree list > WORKTREES.md
# Include worktree purpose and timeline
```

**Collaboration patterns:**
- Use worktrees for local development
- Share branches through normal Git workflows
- Coordinate branch usage to avoid conflicts
- Document worktree-specific processes

---

## Migrating to Worktree Workflows

**From multiple clones:**

```bash
# Old approach
git clone repo.git feature-1
git clone repo.git feature-2
git clone repo.git hotfix

# New approach
git clone repo.git main-repo
cd main-repo
git worktree add ../feature-1 feature-1
git worktree add ../feature-2 feature-2
git worktree add ../hotfix hotfix
```

**Migration steps:**
1. Identify current multiple clone usage
1. Consolidate to single main repository
1. Create worktrees for active branches
1. Update development scripts and tools
1. Train team on new workflow

**Benefits of migration:**
- Reduced disk usage
- Faster branch creation
- Simplified maintenance
- Better resource utilization

---

## Lab Exercise: Worktree Workflow Implementation

**Scenario:** Implement a complete worktree-based development workflow for a team project with multiple concurrent features.

**Setup tasks:**
1. **Create main repository structure:**
   - Initialize repository with sample project
   - Create multiple feature branches
   - Set up directory structure for worktrees

1. **Implement worktree workflow:**
   - Create worktrees for different features
   - Practice switching between contexts
   - Test parallel development scenarios

1. **Maintenance procedures:**
   - Implement cleanup routines
   - Practice troubleshooting scenarios
   - Document worktree management processes

**Advanced tasks:**
1. **Integration testing:**
   - Set up parallel build environments
   - Test different feature combinations
   - Implement automated worktree management

1. **Team coordination:**
   - Develop naming conventions
   - Create documentation templates
   - Design sharing and communication strategies

**Deliverables:** Complete worktree-based development environment, maintenance scripts, team workflow documentation, and troubleshooting guide.

---

## When NOT to Use Worktrees

**Inappropriate scenarios:**
- Single feature development
- Infrequent branch switching
- Limited disk space
- Simple projects
- Learning Git basics

**Alternative approaches:**

```bash
# Simple stash/switch for quick changes
git stash
git checkout other-branch
# Quick fix
git checkout original-branch
git stash pop

# Use branches normally for sequential work
git checkout -b new-feature
# Complete feature
git checkout main
git merge new-feature
```

**Resource constraints:**
- Limited disk space
- Slow file system
- Memory-constrained systems
- Network-mounted storage

---

## Summary: Effective Worktree Usage

**Key takeaways:**

1. **Worktrees solve real problems:**
   - Parallel development contexts
   - Faster than multiple clones
   - Efficient resource usage

1. **Best practices matter:**
   - Consistent naming and organization
   - Regular maintenance and cleanup
   - Proper documentation

1. **Know the limitations:**
   - Branch checkout restrictions
   - Path requirements
   - Submodule complexity

1. **Use appropriately:**
   - Great for complex projects
   - Overkill for simple workflows
   - Consider team needs and resources

**Remember:** Worktrees are a powerful feature that can significantly improve development workflows when used appropriately. They enable true parallel development while maintaining the benefits of a single repository. Master the basics first, then gradually incorporate advanced techniques as your needs grow.
