# Under the Hood

---

## What We'll Cover

1. Digital signatures overview
1. Core Git ideas and concepts
1. The three core structures: commit, tree, blob
1. Understanding the `.git` directory
1. Git object store mechanics
1. Branch and tag storage
1. What happens during common operations

---

## Digital Signatures Overview

`Git` uses cryptographic hashing to ensure data integrity:

**SHA-1 hashing (legacy):**
- 160-bit hash values
- Hexadecimal representation (40 characters)
- Content-addressable storage
- Collision detection

**SHA-256 (modern Git):**
- 256-bit hash values
- Enhanced security
- Backward compatibility considerations
- Future-proof design

```bash
# Example SHA-1 hash
commit a1b2c3d4e5f6789012345678901234567890abcd

# Example SHA-256 hash
commit a1b2c3d4e5f67890123456789012345678901234567890123456789012345678
```

---

## Core Git Ideas

**Three fundamental concepts:**

1. **Always on a branch:**
    - `HEAD` always points to current branch
    - Branches are just pointers to commits
    - No "working without branch" state

1. **SHA includes all history:**
    - Each commit hash represents entire history
    - Changing anything changes all subsequent hashes
    - Guarantees historical integrity

1. **SHA is globally unique:**
    - Same content = same hash everywhere
    - Enables distributed development
    - Natural deduplication

<svg viewBox="0 0 600 200" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="20" text-anchor="middle" font-size="16" font-weight="bold">Git's Core Concepts</text>

  <!-- Branch pointer -->
  <rect x="50" y="50" width="80" height="30" fill="#3498db" rx="5"/>
  <text x="90" y="70" text-anchor="middle" fill="white" font-size="12">main</text>

  <!-- Commits -->
  <circle cx="200" cy="65" r="15" fill="#e74c3c"/>
  <text x="200" y="70" text-anchor="middle" fill="white" font-size="10">A</text>

  <circle cx="300" cy="65" r="15" fill="#2ecc71"/>
  <text x="300" y="70" text-anchor="middle" fill="white" font-size="10">B</text>

  <circle cx="400" cy="65" r="15" fill="#f39c12"/>
  <text x="400" y="70" text-anchor="middle" fill="white" font-size="10">C</text>

  <!-- Arrows -->
  <line x1="130" y1="65" x2="185" y2="65" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="215" y1="65" x2="285" y2="65" stroke="#333" stroke-width="2"/>
  <line x1="315" y1="65" x2="385" y2="65" stroke="#333" stroke-width="2"/>

  <!-- Labels -->
  <text x="200" y="95" text-anchor="middle" font-size="8">a1b2c3d</text>
  <text x="300" y="95" text-anchor="middle" font-size="8">d4e5f6g</text>
  <text x="400" y="95" text-anchor="middle" font-size="8">g7h8i9j</text>

  <text x="300" y="130" text-anchor="middle" font-size="12">Each SHA represents complete history to that point</text>

  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## The Three Core Structures

`Git` stores all data in three types of objects:

**1. Blob (Binary Large Object):**
- Stores file content
- No filename or metadata
- Content-addressable by hash

**2. Tree:**
- Stores directory structure
- Points to blobs and other trees
- Contains filenames and permissions

**3. Commit:**
- Points to a tree (project snapshot)
- Contains metadata (author, date, message)
- Points to parent commit(s)

---

## Blob Objects

Blobs store pure file content without any metadata:

```bash
# Create a blob manually
echo "Hello, Git!" | git hash-object -w --stdin
# Output: 2b5e1e3...

# View blob content
git show 2b5e1e3
```

**Key characteristics:**
- Only file content, no filename
- Same content = same blob across entire repository
- Efficient storage through deduplication
- Binary-safe storage

**Example:**

```txt
blob 12
Hello, Git!
```

Size (12 bytes) + null byte + content

---

## Tree Objects

Trees represent directory snapshots:

```bash
# View tree structure
git cat-file -p HEAD^{tree}

# Output example:
100644 blob a1b2c3d    README.md
100644 blob d4e5f6g    index.html
040000 tree g7h8i9j    src
100755 blob j1k2l3m    deploy.sh
```

**Tree format:**
- Mode (permissions)
- Object type (blob/tree)
- SHA hash
- Filename

**Modes:**
- `100644`: Regular file
- `100755`: Executable file
- `040000`: Directory (tree)
- `120000`: Symbolic link

---

## Commit Objects

Commits tie everything together with metadata:

```bash
# View commit object
git cat-file -p HEAD

# Output example:
tree a1b2c3d4e5f6789012345678901234567890abcd
parent d4e5f6g7h8i9012345678901234567890abcdef12
author John Smith <john@example.com> 1634567890 +0200
committer John Smith <john@example.com> 1634567890 +0200

Add user authentication feature

Implemented login functionality with password validation
and session management.
```

**Commit components:**
- Tree pointer (project snapshot)
- Parent commit(s)
- Author information
- Committer information (can differ from author)
- Timestamp and timezone
- Commit message

---

## Object Relationships

How the three structures connect:

<svg viewBox="0 0 700 400" xmlns="http://www.w3.org/2000/svg">
  <text x="350" y="20" text-anchor="middle" font-size="16" font-weight="bold">Git Object Model</text>

  <!-- Commit -->
  <rect x="280" y="50" width="140" height="80" fill="#3498db" rx="5"/>
  <text x="350" y="70" text-anchor="middle" fill="white" font-size="12" font-weight="bold">Commit</text>
  <text x="350" y="85" text-anchor="middle" fill="white" font-size="10">g7h8i9j</text>
  <text x="350" y="100" text-anchor="middle" fill="white" font-size="10">Author: John</text>
  <text x="350" y="115" text-anchor="middle" fill="white" font-size="10">Message: "Add feature"</text>

  <!-- Root Tree -->
  <rect x="280" y="170" width="140" height="80" fill="#2ecc71" rx="5"/>
  <text x="350" y="190" text-anchor="middle" fill="white" font-size="12" font-weight="bold">Tree (root)</text>
  <text x="350" y="205" text-anchor="middle" fill="white" font-size="10">a1b2c3d</text>
  <text x="350" y="220" text-anchor="middle" fill="white" font-size="10">README.md</text>
  <text x="350" y="235" text-anchor="middle" fill="white" font-size="10">src/</text>

  <!-- Blobs and subtrees -->
  <rect x="50" y="300" width="100" height="60" fill="#e74c3c" rx="5"/>
  <text x="100" y="320" text-anchor="middle" fill="white" font-size="11" font-weight="bold">Blob</text>
  <text x="100" y="335" text-anchor="middle" fill="white" font-size="9">d4e5f6g</text>
  <text x="100" y="350" text-anchor="middle" fill="white" font-size="9">README content</text>

  <rect x="200" y="300" width="100" height="60" fill="#f39c12" rx="5"/>
  <text x="250" y="320" text-anchor="middle" fill="white" font-size="11" font-weight="bold">Tree (src)</text>
  <text x="250" y="335" text-anchor="middle" fill="white" font-size="9">j1k2l3m</text>
  <text x="250" y="350" text-anchor="middle" fill="white" font-size="9">main.py</text>

  <rect x="350" y="300" width="100" height="60" fill="#e74c3c" rx="5"/>
  <text x="400" y="320" text-anchor="middle" fill="white" font-size="11" font-weight="bold">Blob</text>
  <text x="400" y="335" text-anchor="middle" fill="white" font-size="9">m4n5o6p</text>
  <text x="400" y="350" text-anchor="middle" fill="white" font-size="9">Python code</text>

  <!-- Arrows -->
  <line x1="350" y1="130" x2="350" y2="170" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="320" y1="250" x2="120" y2="300" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="350" y1="250" x2="250" y2="300" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="250" y1="320" x2="380" y2="320" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/>

  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## The .git Directory Structure

Everything `Git` needs is stored in `.git`:

```txt
.git/
├── HEAD              # Current branch pointer
├── config            # Repository configuration
├── description       # Repository description
├── hooks/            # Git hooks
├── info/            # Global excludes
├── objects/         # Object database
│   ├── 12/          # First 2 chars of SHA
│   │   └── 34567... # Remaining 38 chars
├── refs/            # Branch and tag references
│   ├── heads/       # Branch pointers
│   ├── tags/        # Tag pointers
│   └── remotes/     # Remote branch pointers
├── logs/            # Reference logs (reflog)
└── index           # Staging area
```

---

## The Git Object Store

How `Git` stores objects efficiently:

**Object storage:**

```bash
# Objects stored by SHA
.git/objects/a1/b2c3d4e5f6789...

# Compressed with zlib
# Content format: "type size\0content"
```

**Loose vs packed objects:**
- **Loose**: Individual files per object
- **Packed**: Multiple objects in single file
- **Automatic packing**: Triggered by gc operations

```bash
# Manual packing
git gc

# View object type
git cat-file -t a1b2c3d

# View object size
git cat-file -s a1b2c3d

# View object content
git cat-file -p a1b2c3d
```

---

## Understanding HEAD

`HEAD` determines your current position:

```bash
# View HEAD
cat .git/HEAD
# Output: ref: refs/heads/main

# HEAD pointing to branch
HEAD → refs/heads/main → commit_sha

# Detached HEAD (pointing directly to commit)
HEAD → commit_sha
```

**HEAD states:**
- **Normal**: Points to branch reference
- **Detached**: Points directly to commit
- **During merge**: Special states during operations

```bash
# Check HEAD status
git symbolic-ref HEAD  # Current branch
git rev-parse HEAD     # Current commit SHA
```

---

## Branch Storage

Branches are just files containing commit SHAs:

```bash
# Branch file location
cat .git/refs/heads/main
# Output: a1b2c3d4e5f6789012345678901234567890abcd

# Create branch manually (don't do this!)
echo "d4e5f6g7h8i9012345678901234567890abcdef12" > .git/refs/heads/new-feature

# List all branches
ls .git/refs/heads/
```

**Branch operations:**
- Creating branch: Write commit SHA to file
- Switching branch: Update HEAD to point to branch
- Deleting branch: Remove the file

---

## Tag Storage

Tags come in two types:

**Lightweight tags:**
```bash
# Stored like branches
cat .git/refs/tags/v1.0
# Output: a1b2c3d4e5f6789012345678901234567890abcd
```

**Annotated tags:**
```bash
# Create tag object with metadata
git cat-file -p v2.0
# Output:
object a1b2c3d4e5f6789012345678901234567890abcd
type commit
tag v2.0
tagger John Smith <john@example.com> 1634567890 +0200

Release version 2.0
```

**Tag object structure:**
- Points to any Git object (usually commits)
- Contains metadata (tagger, date, message)
- Can be signed with GPG

---

## Remote References

Remote branches stored separately:

```bash
# Remote branch storage
.git/refs/remotes/origin/main
.git/refs/remotes/origin/develop

# View remote references
cat .git/refs/remotes/origin/main
# Output: commit SHA from remote

# Remote configuration
cat .git/config
[remote "origin"]
    url = https://github.com/user/repo.git
    fetch = +refs/heads/*:refs/remotes/origin/*
```

---

## What Happens When You: Add to Staging Area

The staging area (index) is a binary file:

```bash
# View index contents
git ls-files --stage

# Output:
100644 a1b2c3d4e5f6... 0    README.md
100644 d4e5f6g7h8i9... 0    src/main.py
```

**During `git add`:**
1. File content is hashed
1. Blob object created in object store
1. Index updated with file path → blob SHA mapping
1. Working directory unchanged

**Index format:**
- Binary file for performance
- Maps file paths to blob SHAs
- Includes file metadata (timestamps, permissions)
- Stage numbers for conflict resolution

---

## What Happens When You: Commit

Creating a commit involves multiple steps:

```bash
git commit -m "Add feature"
```

**Commit process:**
1. **Create tree from index:**
    - Read current index state
    - Create tree objects for directories
    - Write tree objects to object store

1. **Create commit object:**
    - Reference the root tree
    - Set parent to current HEAD
    - Add author/committer info
    - Include commit message

1. **Update branch pointer:**
    - Update refs/heads/branch-name
    - Move HEAD to new commit

1. **Clear merge state** (if applicable)

---

## What Happens When You: Create a Branch

Branch creation is simple:

```bash
git branch feature-branch
```

**Branch creation process:**
1. **Get current commit SHA** (from HEAD)
1. **Write SHA to new file:** `.git/refs/heads/feature-branch`
1. **No other changes** (HEAD stays on current branch)

**Switching to the branch:**
```bash
git checkout feature-branch
```

1. **Update HEAD:** Point to new branch reference
1. **Update index:** Match the branch's tree
1. **Update working directory:** Checkout files

---

## What Happens When You: Create an Annotated Tag

Annotated tags create objects:

```bash
git tag -a v1.0 -m "Release 1.0"
```

**Tag creation process:**
1. **Create tag object:**
    - Object type: tag
    - Points to current commit
    - Includes tagger info and message
    - Stored in object database

1. **Write tag reference:**
    - Create `.git/refs/tags/v1.0`
    - Contains SHA of tag object (not commit)

1. **Tag object content:**

```txt
object a1b2c3d4e5f6789...
type commit
tag v1.0
tagger John Smith <john@example.com> 1634567890 +0200

Release 1.0
```

---

## The Reflog System

`Git` maintains logs of reference changes:

```bash
# View reflog
git reflog

# Output:
a1b2c3d HEAD@{0}: commit: Add feature
d4e5f6g HEAD@{1}: checkout: moving from main to feature
g7h8i9j HEAD@{2}: commit: Fix bug
```

**Reflog storage:**
- `.git/logs/HEAD` - All HEAD movements
- `.git/logs/refs/heads/branch` - Branch-specific logs
- Default retention: 90 days for unreachable commits
- 30 days for reachable commits

**Reflog uses:**
- Recovery of lost commits
- Understanding command history
- Debugging complex operations

---

## Object Packing and Compression

`Git` optimizes storage through packing:

**Loose objects:**
- Individual files per object
- Immediate storage for new objects
- Less efficient for large repositories

**Pack files:**
- Multiple objects in single file
- Delta compression between similar objects
- Much more storage efficient

```bash
# Manual packing
git gc

# View pack information
git count-objects -v

# Output:
count 150          # loose objects
size 1500          # KB of loose objects
in-pack 5420       # objects in packs
packs 2            # number of pack files
size-pack 856      # KB in pack files
```

---

## Delta Compression

How `Git` stores similar objects efficiently:

**Delta storage:**
- Base object stored fully
- Similar objects stored as differences
- Chain of deltas for multiple versions
- Automatic during packing operations

<svg viewBox="0 0 600 250" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="20" text-anchor="middle" font-size="14" font-weight="bold">Delta Compression Example</text>

  <!-- Base object -->
  <rect x="50" y="50" width="120" height="80" fill="#3498db" rx="5"/>
  <text x="110" y="75" text-anchor="middle" fill="white" font-size="12" font-weight="bold">Base Object</text>
  <text x="110" y="95" text-anchor="middle" fill="white" font-size="10">Full Content</text>
  <text x="110" y="110" text-anchor="middle" fill="white" font-size="10">1000 bytes</text>

  <!-- Delta object -->
  <rect x="240" y="50" width="120" height="80" fill="#e74c3c" rx="5"/>
  <text x="300" y="75" text-anchor="middle" fill="white" font-size="12" font-weight="bold">Delta Object</text>
  <text x="300" y="95" text-anchor="middle" fill="white" font-size="10">Changes Only</text>
  <text x="300" y="110" text-anchor="middle" fill="white" font-size="10">50 bytes</text>

  <!-- Result -->
  <rect x="430" y="50" width="120" height="80" fill="#2ecc71" rx="5"/>
  <text x="490" y="75" text-anchor="middle" fill="white" font-size="12" font-weight="bold">Reconstructed</text>
  <text x="490" y="95" text-anchor="middle" fill="white" font-size="10">Base + Delta</text>
  <text x="490" y="110" text-anchor="middle" fill="white" font-size="10">1000 bytes</text>

  <!-- Arrows -->
  <line x1="170" y1="90" x2="230" y2="90" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="360" y1="90" x2="420" y2="90" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/>

  <text x="200" y="85" text-anchor="middle" font-size="10">+</text>
  <text x="390" y="85" text-anchor="middle" font-size="10">=</text>

  <text x="300" y="170" text-anchor="middle" font-size="12">Space saved: 95% in this example</text>

  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Garbage Collection

`Git` automatically cleans up unreferenced objects:

```bash
# Manual garbage collection
git gc

# Aggressive garbage collection
git gc --aggressive

# Prune unreferenced objects older than 2 weeks
git gc --prune=2.weeks.ago
```

**GC operations:**
1. **Pack loose objects** into pack files
1. **Remove duplicate objects** through delta compression
1. **Delete unreferenced objects** older than expiry time
1. **Optimize pack files** for better performance
1. **Update reference indexes** for faster lookups

**Automatic triggers:**
- Too many loose objects (>6700)
- Too many pack files (>50)
- After certain operations (fetch, merge)

---

## Understanding Git's Performance

**Why Git is fast:**

1. **Local operations:**
    - Most commands don't need network
    - Local object database access
    - Efficient data structures

1. **Content-addressable storage:**
    - Direct object lookup by hash
    - No linear searches needed
    - Automatic deduplication

1. **Delta compression:**
    - Efficient storage of similar content
    - Fast reconstruction algorithms
    - Reduced I/O operations

1. **Caching and indexing:**
    - Index file caches working directory state
    - Pack file indexes for fast object lookup
    - Reference caching

---

## The Index File Deep Dive

The index (staging area) is more complex than it appears:

```bash
# Low-level index inspection
git ls-files --debug

# Output includes:
# ctime: 1634567890:123456789  # creation time
# mtime: 1634567890:123456789  # modification time
# dev: 2049                    # device
# ino: 1234567                 # inode
# uid: 1000                    # user id
# gid: 1000                    # group id
# size: 1024                   # file size
# flags: 0                     # various flags
# sha1: a1b2c3d4e5f6789...    # blob SHA
# path: src/main.py            # file path
```

**Index optimization:**
- Binary format for speed
- Sorted by path for efficient lookup
- Includes file metadata to detect changes
- Extension mechanisms for additional data

---

## Symbolic References

Not all references point directly to commits:

```bash
# HEAD is often symbolic
cat .git/HEAD
# Output: ref: refs/heads/main

# Create symbolic reference
git symbolic-ref refs/heads/current refs/heads/main

# Resolve symbolic reference
git symbolic-ref refs/heads/current
# Output: refs/heads/main
```

**Symbolic reference uses:**
- `HEAD` pointing to current branch
- Branch aliases
- Remote HEAD tracking
- Workflow automation

---

## Object Validation and Fsck

`Git` can verify repository integrity:

```bash
# Check repository integrity
git fsck

# Verbose output
git fsck --full --verbose

# Check specific objects
git fsck --connectivity-only
```

**Common fsck findings:**
- **Dangling blobs:** Unreferenced file content
- **Dangling commits:** Unreachable commits
- **Missing objects:** Corrupted object database
- **Bad objects:** Corrupted object content

**Fsck output example:**

```txt
dangling blob a1b2c3d4e5f6789012345678901234567890abcd
dangling commit d4e5f6g7h8i9012345678901234567890abcdef12
```

---

## Low-Level Object Manipulation

Direct object database operations:

```bash
# Create blob from content
echo "Hello World" | git hash-object -w --stdin
# Output: 557db03de997c86a4a028e1ebd3a1ceb225be238

# Read object content
git cat-file blob 557db03

# Get object type
git cat-file -t 557db03
# Output: blob

# Get object size
git cat-file -s 557db03
# Output: 12

# Pretty-print object
git cat-file -p 557db03
# Output: Hello World
```

**Object creation tools:**
- `hash-object`: Create objects from files
- `mktree`: Create tree objects
- `commit-tree`: Create commit objects
- `update-ref`: Update references

---

## Understanding Merge Mechanics

What happens during a three-way merge:

**Merge process:**
1. **Find merge base:** Common ancestor of branches
1. **Create temporary trees:** One for each branch
1. **Compare changes:** From base to each branch
1. **Apply changes:** Combine non-conflicting changes
1. **Detect conflicts:** Mark conflicting changes
1. **Create result:** New tree with merged content
1. **Create merge commit:** With two parents

<svg viewBox="0 0 600 300" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="20" text-anchor="middle" font-size="14" font-weight="bold">Three-Way Merge Process</text>

  <!-- Merge base -->
  <circle cx="300" cy="80" r="20" fill="#95a5a6"/>
  <text x="300" y="85" text-anchor="middle" fill="white" font-size="11">Base</text>
  <text x="300" y="110" text-anchor="middle" font-size="10">Common ancestor</text>

  <!-- Branch A -->
  <circle cx="150" cy="180" r="20" fill="#3498db"/>
  <text x="150" y="185" text-anchor="middle" fill="white" font-size="11">A</text>
  <text x="150" y="210" text-anchor="middle" font-size="10">Branch A</text>

  <!-- Branch B -->
  <circle cx="450" cy="180" r="20" fill="#e74c3c"/>
  <text x="450" y="185" text-anchor="middle" fill="white" font-size="11">B</text>
  <text x="450" y="210" text-anchor="middle" font-size="10">Branch B</text>

  <!-- Merge result -->
  <circle cx="300" cy="250" r="20" fill="#2ecc71"/>
  <text x="300" y="255" text-anchor="middle" fill="white" font-size="11">M</text>
  <text x="300" y="280" text-anchor="middle" font-size="10">Merge commit</text>

  <!-- Lines showing relationships -->
  <line x1="280" y1="100" x2="170" y2="160" stroke="#333" stroke-width="1" stroke-dasharray="5,5"/>
  <line x1="320" y1="100" x2="430" y2="160" stroke="#333" stroke-width="1" stroke-dasharray="5,5"/>
  <line x1="170" y1="180" x2="280" y2="230" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="430" y1="180" x2="320" y2="230" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/>

  <text x="220" y="145" font-size="9">diff base→A</text>
  <text x="360" y="145" font-size="9">diff base→B</text>

  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Rebase Internals

Understanding how rebase works under the hood:

**Rebase process:**
1. **Find commits to replay:** From merge base to branch tip
1. **Reset to target:** Move branch to rebase target
1. **Apply commits sequentially:** Cherry-pick each commit
1. **Handle conflicts:** Stop for manual resolution if needed
1. **Update references:** Point branch to final commit

```bash
# What rebase does internally:
# 1. git checkout target-branch
# 2. For each commit in original branch:
#    git cherry-pick commit
# 3. git branch -f original-branch HEAD
```

**Rebase vs merge differences:**
- **Rebase:** Replays commits, creates new commit SHAs
- **Merge:** Combines trees, preserves original commits

---

## Configuration System Deep Dive

Git's layered configuration system:

**Configuration hierarchy:**
1. **System:** `/etc/gitconfig` (system-wide)
1. **Global:** `~/.gitconfig` (user-specific)
1. **Local:** `.git/config` (repository-specific)
1. **Worktree:** `.git/config.worktree` (worktree-specific)

```bash
# View all configuration
git config --list --show-origin

# Configuration precedence (local overrides global)
git config user.name "John Smith"           # local
git config --global user.name "J. Smith"    # global
git config --system user.name "Anonymous"   # system
# Result: "John Smith" (local wins)
```

**Configuration sections:**
```ini
[core]
    editor = vim
    autocrlf = input
[user]
    name = John Smith
    email = john@example.com
[remote "origin"]
    url = https://github.com/user/repo.git
    fetch = +refs/heads/*:refs/remotes/origin/*
```

---

## Hook System Architecture

Git hooks provide extension points:

**Hook types:**
- **Pre-hooks:** Execute before operations
- **Post-hooks:** Execute after operations
- **Update hooks:** Execute during ref updates

**Client-side hooks:**

```txt
.git/hooks/
├── pre-commit           # Before commit creation
├── prepare-commit-msg   # Before commit message editor
├── commit-msg           # After commit message written
├── post-commit          # After commit created
├── pre-rebase           # Before rebase
├── post-checkout        # After checkout
├── post-merge           # After merge
└── pre-push             # Before push
```

**Server-side hooks:**

```txt
├── pre-receive          # Before any refs updated
├── update               # Before each ref updated
└── post-receive         # After all refs updated
```

---

## Network Protocol Internals

How Git communicates over the network:

**Smart HTTP protocol:**

```txt
GET /repo.git/info/refs?service=git-upload-pack
# Server responds with reference list

POST /repo.git/git-upload-pack
# Client sends wants/haves, server responds with pack
```

**SSH protocol:**

```bash
ssh git@server.com git-upload-pack '/path/to/repo.git'
# Direct command execution over SSH
```

**Protocol phases:**
1. **Reference discovery:** List available refs
1. **Negotiation:** Determine needed objects
1. **Pack transfer:** Send compressed object data
1. **Reference update:** Update local references

---

## Advanced Object Storage

Understanding Git's object model edge cases:

**Submodule storage:**
```bash
# Submodule in tree object
160000 commit a1b2c3d4e5f6...    submodule-name
```
- Mode `160000` indicates submodule
- Points to commit in different repository
- `.gitmodules` file contains submodule configuration

**Large file handling:**
- Git LFS replaces large files with pointers
- Pointer files stored as regular blobs
- Actual content stored separately
- Transparent to most Git operations

**Binary file storage:**
- All files stored as blobs regardless of type
- No special binary file handling
- Delta compression still applies
- Line-based tools may not work well

---

## Worktree Implementation

How Git manages multiple working directories:

**Worktree structure:**

```txt
main-repo/
├── .git/                 # Main repository
└── worktrees/
    ├── feature-branch/
    │   ├── .git           # Points to main .git
    │   └── gitdir         # Path to worktree-specific data
    └── hotfix/
```

**Worktree-specific data:**

```txt
.git/worktrees/feature-branch/
├── HEAD                  # Current branch for this worktree
├── index                 # Staging area for this worktree
├── logs/                 # Reflog for this worktree
└── ORIG_HEAD            # Previous HEAD for this worktree
```

**Shared vs separate:**
- **Shared:** Object database, configuration, references
- **Separate:** HEAD, index, working directory

---

## Repository Cloning Internals

What happens during `git clone`:

```bash
git clone https://github.com/user/repo.git local-repo
```

**Clone process:**
1. **Create directory:** `local-repo/`
1. **Initialize repository:** `git init`
1. **Add remote:** `origin` pointing to source URL
1. **Fetch all references:** Download all branches and tags
1. **Create local main branch:** Usually from `origin/main`
1. **Checkout working directory:** Set up files from main branch
1. **Configure tracking:** Set up branch tracking relationships

**Clone optimizations:**
- **Shallow clone:** `--depth=1` for recent history only
- **Single branch:** `--single-branch` for one branch
- **Bare clone:** `--bare` for no working directory
- **Mirror clone:** `--mirror` for exact replica

---

## Understanding Git's Merge Algorithms

Git uses different merge strategies:

**Recursive strategy (default):**
- Handles most common cases
- Can detect renames and copies
- Resolves "criss-cross" merges
- Uses multiple merge bases when needed

**Octopus strategy:**
- Merges more than two branches
- Only works with clean merges
- Stops at first conflict
- Rarely used in practice

**Ours/Theirs strategies:**
- **Ours:** Keep our version entirely
- **Theirs:** Take their version entirely
- Useful for specific workflows
- No conflict resolution needed

**Subtree strategy:**
- Merges separate project as subdirectory
- Handles path prefix differences
- Complex but powerful
- Alternative to submodules

---

## Performance Monitoring and Tuning

Monitoring Git performance:

```bash
# Repository statistics
git count-objects -v

# Find large objects
git rev-list --objects --all | sort -k 2 | cut -f 1 -d\  | uniq | \
while read sha; do
  echo $(git cat-file -s $sha) $sha $(git cat-file -t $sha)
done | sort -nr | head -10

# Analyze pack files
git verify-pack -v .git/objects/pack/*.idx | sort -k 3 -nr | head -10
```

**Performance tuning:**
- Regular garbage collection
- Optimize pack files
- Use shallow clones when appropriate
- Consider partial clone for huge repositories
- Monitor repository size growth

---

## Debugging Git Problems

Tools for diagnosing Git issues:

```bash
# Environment debugging
git --exec-path          # Git executable path
git --git-dir           # Git directory location
git --work-tree         # Working tree location

# Object debugging
git cat-file --batch-check < object-list
git cat-file --batch < object-list

# Reference debugging
git for-each-ref --format='%(refname) %(objectname)'
git show-ref --verify refs/heads/main

# Configuration debugging
git config --list --show-origin --show-scope
```

**Common debugging scenarios:**
- Corrupted object database
- Missing references
- Configuration conflicts
- Hook execution problems
- Performance issues

---

## Security Considerations

Git security aspects:

**SHA collision attacks:**
- Git moving from SHA-1 to SHA-256
- Collision detection in modern Git
- Repository verification important

**Object verification:**

```bash
# Verify object integrity
git fsck --full

# Check for suspicious content
git log --all --full-history -p | grep -i "password\|secret"
```

**Hook security:**
- Hooks can execute arbitrary code
- Be careful with shared repositories
- Validate hook sources
- Consider hook signing

**Transport security:**
- Use HTTPS or SSH
- Verify server certificates
- Use SSH key authentication
- Consider signed commits

---

## Git Internals Best Practices

**Repository maintenance:**
1. Regular garbage collection
1. Monitor repository size
1. Use appropriate ignore files
1. Clean up old branches

**Development practices:**
1. Understand object model implications
1. Use hooks appropriately
1. Configure Git properly for your environment
1. Monitor repository health

**Performance optimization:**
1. Pack objects regularly
1. Use shallow clones for CI/CD
1. Consider partial clone for huge repos
1. Monitor object count and size

**Troubleshooting approach:**
1. Understand what Git commands actually do
1. Use low-level commands for diagnosis
1. Check object database integrity
1. Verify configuration and environment

---

## Lab Exercise: Git Internals Exploration

**Scenario:** Explore a repository's internal structure and understand how Git operations work under the hood.

**Tasks:**
1. **Object exploration:**
    - Find and examine blob, tree, and commit objects
    - Trace object relationships
    - Understand object storage format

1. **Operation analysis:**
    - Monitor `.git` directory during operations
    - Trace what happens during commit, branch, merge
    - Analyze pack file contents

1. **Performance investigation:**
    - Measure repository statistics
    - Identify large objects
    - Optimize repository storage

1. **Recovery simulation:**
    - Create "lost" commits
    - Use reflog and fsck for recovery
    - Understand reference mechanics

**Deliverables:** Detailed analysis report showing understanding of Git's internal mechanics and practical skills in repository maintenance and troubleshooting.

---

## Summary: Git Under the Hood

**Key takeaways:**

1. **Git is simple at its core:**
    - Three object types: blob, tree, commit
    - Content-addressable storage
    - References are just pointers

1. **Understanding internals helps:**
    - Better debugging capabilities
    - More efficient workflows
    - Confidence in complex operations

1. **Performance matters:**
    - Repository maintenance is important
    - Understanding when Git is slow
    - Optimization strategies available

1. **Git is robust:**
    - Strong integrity guarantees
    - Recovery mechanisms available
    - Distributed nature provides redundancy

**Remember:** Git's internals are designed to be simple and robust. Understanding these fundamentals makes you a more effective Git user and better able to handle complex scenarios and troubleshoot problems when they arise.
