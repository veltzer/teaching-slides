# Introduction to Git

---

## What We'll Cover Today

1. History of Git
1. Why Git was created
1. Who is using Git
1. Git vs other version control systems
1. Key concepts and terminology
1. Adopting Git in your organization

---

## A Brief History of Version Control

1. **No Version Control** - Copy folders, rename files
1. **Local Version Control** - RCS (1982)
1. **Centralized Version Control** - CVS, Subversion, Perforce
1. **Distributed Version Control** - Git, Mercurial, Bazaar

---

## The Linux Kernel Problem

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="700" height="300" fill="#f0f0f0" stroke="#333" stroke-width="2"/>
  <text x="400" y="100" text-anchor="middle" font-size="24" font-weight="bold">Linux Kernel Development (2002-2005)</text>
  <circle cx="200" cy="200" r="30" fill="#4CAF50"/>
  <text x="200" y="250" text-anchor="middle" font-size="14">Developer 1</text>
  <circle cx="400" cy="200" r="30" fill="#4CAF50"/>
  <text x="400" y="250" text-anchor="middle" font-size="14">Developer 2</text>
  <circle cx="600" cy="200" r="30" fill="#4CAF50"/>
  <text x="600" y="250" text-anchor="middle" font-size="14">Developer 3</text>
  <rect x="350" y="280" width="100" height="40" fill="#FF5722"/>
  <text x="400" y="305" text-anchor="middle" font-size="14" fill="white">BitKeeper</text>
  <line x1="200" y1="220" x2="380" y2="280" stroke="#333" stroke-width="2"/>
  <line x1="400" y1="220" x2="400" y2="280" stroke="#333" stroke-width="2"/>
  <line x1="600" y1="220" x2="420" y2="280" stroke="#333" stroke-width="2"/>
</svg>

---

## The Birth of Git (2005)

![h:300](../../../../raw/linus_torvalds.jpg)

**Linus Torvalds** created Git in April 2005

Requirements:
1. **Speed** - Must be fast for large projects
1. **Simple design** - Easy to understand and extend
1. **Strong support for non-linear development** - Thousands of parallel branches
1. **Fully distributed** - No single point of failure
1. **Able to handle large projects** - Like the Linux kernel

---

## Git Timeline

1. **April 3, 2005** - Development begins
1. **April 7, 2005** - Git becomes self-hosting
1. **April 18, 2005** - First merge of multiple branches
1. **April 29, 2005** - Performance matches BitKeeper
1. **June 16, 2005** - Linux 2.6.12 released using Git
1. **2008** - GitHub launches
1. **Today** - Most popular version control system

---

## Why "Git"?

Linus Torvalds quipped:

> "I'm an egotistical bastard, and I name all my projects after myself. First 'Linux', now 'git'."

**git** (British slang): an unpleasant or contemptible person

But also:
1. **Simple** - Three letter command
1. **Not taken** - Available as a command name
1. **Memorable** - Easy to remember

---

## Who is Using Git?

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="40" text-anchor="middle" font-size="24" font-weight="bold">Git Adoption</text>
  <rect x="100" y="80" width="120" height="60" fill="#1976D2" rx="5"/>
  <text x="160" y="115" text-anchor="middle" font-size="14" fill="white">Microsoft</text>
  <rect x="250" y="80" width="120" height="60" fill="#4CAF50" rx="5"/>
  <text x="310" y="115" text-anchor="middle" font-size="14" fill="white">Google</text>
  <rect x="400" y="80" width="120" height="60" fill="#FF9800" rx="5"/>
  <text x="460" y="115" text-anchor="middle" font-size="14" fill="white">Facebook</text>
  <rect x="550" y="80" width="120" height="60" fill="#9C27B0" rx="5"/>
  <text x="610" y="115" text-anchor="middle" font-size="14" fill="white">Netflix</text>
  <rect x="100" y="170" width="120" height="60" fill="#F44336" rx="5"/>
  <text x="160" y="205" text-anchor="middle" font-size="14" fill="white">Linux</text>
  <rect x="250" y="170" width="120" height="60" fill="#00BCD4" rx="5"/>
  <text x="310" y="205" text-anchor="middle" font-size="14" fill="white">Android</text>
  <rect x="400" y="170" width="120" height="60" fill="#795548" rx="5"/>
  <text x="460" y="205" text-anchor="middle" font-size="14" fill="white">Ruby</text>
  <rect x="550" y="170" width="120" height="60" fill="#607D8B" rx="5"/>
  <text x="610" y="205" text-anchor="middle" font-size="14" fill="white">Rails</text>
  <text x="400" y="280" text-anchor="middle" font-size="16">...and millions more!</text>
</svg>

---

## Git Market Share

According to Stack Overflow Developer Survey:

1. **Git** - 93.87%
1. **SVN** - 4.69%
1. **Mercurial** - 1.13%
1. **Others** - 0.31%

## Git has become the de-facto standard

---

## Git vs Centralized VCS

<svg viewBox="0 0 800 450" xmlns="http://www.w3.org/2000/svg">
  <text x="200" y="30" text-anchor="middle" font-size="20" font-weight="bold">Centralized (SVN)</text>
  <rect x="150" y="60" width="100" height="60" fill="#FF5722"/>
  <text x="200" y="95" text-anchor="middle" font-size="14" fill="white">Server</text>
  <circle cx="100" cy="220" r="25" fill="#2196F3"/>
  <text x="100" y="260" text-anchor="middle" font-size="12">Dev 1</text>
  <circle cx="200" cy="220" r="25" fill="#2196F3"/>
  <text x="200" y="260" text-anchor="middle" font-size="12">Dev 2</text>
  <circle cx="300" cy="220" r="25" fill="#2196F3"/>
  <text x="300" y="260" text-anchor="middle" font-size="12">Dev 3</text>
  <line x1="100" y1="195" x2="180" y2="120" stroke="#333" stroke-width="2" marker-end="url(#arrow)"/>
  <line x1="200" y1="195" x2="200" y2="120" stroke="#333" stroke-width="2" marker-end="url(#arrow)"/>
  <line x1="300" y1="195" x2="220" y2="120" stroke="#333" stroke-width="2" marker-end="url(#arrow)"/>
  <text x="600" y="30" text-anchor="middle" font-size="20" font-weight="bold">Distributed (Git)</text>
  <circle cx="500" cy="90" r="25" fill="#4CAF50"/>
  <text x="500" y="130" text-anchor="middle" font-size="12">Dev 1</text>
  <circle cx="600" cy="90" r="25" fill="#4CAF50"/>
  <text x="600" y="130" text-anchor="middle" font-size="12">Dev 2</text>
  <circle cx="700" cy="90" r="25" fill="#4CAF50"/>
  <text x="700" y="130" text-anchor="middle" font-size="12">Dev 3</text>
  <circle cx="550" cy="180" r="25" fill="#4CAF50"/>
  <text x="550" y="220" text-anchor="middle" font-size="12">Dev 4</text>
  <circle cx="650" cy="180" r="25" fill="#4CAF50"/>
  <text x="650" y="220" text-anchor="middle" font-size="12">Dev 5</text>
  <line x1="520" y1="105" x2="580" y2="105" stroke="#333" stroke-width="2"/>
  <line x1="620" y1="105" x2="680" y2="105" stroke="#333" stroke-width="2"/>
  <line x1="515" y1="110" x2="535" y2="160" stroke="#333" stroke-width="2"/>
  <line x1="585" y1="110" x2="565" y2="160" stroke="#333" stroke-width="2"/>
  <line x1="615" y1="110" x2="635" y2="160" stroke="#333" stroke-width="2"/>
  <line x1="685" y1="110" x2="665" y2="160" stroke="#333" stroke-width="2"/>
  <line x1="570" y1="180" x2="630" y2="180" stroke="#333" stroke-width="2"/>
  <text x="200" y="320" text-anchor="middle" font-size="14" font-style="italic">Single point of failure</text>
  <text x="600" y="320" text-anchor="middle" font-size="14" font-style="italic">Every clone is a full backup</text>
  <defs>
    <marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Key Differences from SVN

| Feature | SVN | Git |
|---------|-----|-----|
| **Architecture** | Centralized | Distributed |
| **Speed** | Slower (network) | Fast (local) |
| **Offline work** | Limited | Full capability |
| **Branching** | Expensive | Cheap and fast |
| **Storage** | Delta-based | Snapshot-based |
| **History** | Linear | DAG (Directed Acyclic Graph) |

---

## Git's Distributed Nature

1. **Every clone is a full repository**
    - Complete history
    - All branches and tags
    - Can work offline
1. **No single point of failure**
    - Any repository can be the "master"
    - Easy backup and recovery
1. **Flexible workflows**
    - Centralized workflow
    - Feature branch workflow
    - Gitflow workflow
    - Forking workflow

---

## The Git Data Model

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="30" text-anchor="middle" font-size="22" font-weight="bold">Git Objects</text>
  <rect x="100" y="80" width="120" height="60" fill="#4CAF50" rx="5"/>
  <text x="160" y="115" text-anchor="middle" font-size="16" fill="white">Blob</text>
  <text x="160" y="170" text-anchor="middle" font-size="12">File content</text>
  <rect x="340" y="80" width="120" height="60" fill="#2196F3" rx="5"/>
  <text x="400" y="115" text-anchor="middle" font-size="16" fill="white">Tree</text>
  <text x="400" y="170" text-anchor="middle" font-size="12">Directory structure</text>
  <rect x="580" y="80" width="120" height="60" fill="#FF9800" rx="5"/>
  <text x="640" y="115" text-anchor="middle" font-size="16" fill="white">Commit</text>
  <text x="640" y="170" text-anchor="middle" font-size="12">Snapshot + metadata</text>
  <line x1="220" y1="110" x2="340" y2="110" stroke="#333" stroke-width="2" marker-end="url(#arrow2)"/>
  <line x1="460" y1="110" x2="580" y2="110" stroke="#333" stroke-width="2" marker-end="url(#arrow2)"/>
  <rect x="250" y="250" width="300" height="80" fill="#f0f0f0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="400" y="280" text-anchor="middle" font-size="14" font-weight="bold">Every commit has a unique SHA-1 hash</text>
  <text x="400" y="305" text-anchor="middle" font-size="12">Example: 3b18e512dba79e4c8300dd08aeb37f8e728b8dad</text>
  <defs>
    <marker id="arrow2" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Snapshots, Not Differences

**SVN/CVS** - Stores differences (deltas)
```diagram
File A: version 1 → +5 lines → -2 lines → +1 line
File B: version 1 → +10 lines → -5 lines → +3 lines
```

**Git** - Stores snapshots
```diagram
Commit 1: [FileA-v1] [FileB-v1] [FileC-v1]
Commit 2: [FileA-v2] [FileB-v1] [FileC-v2]
Commit 3: [FileA-v2] [FileB-v2] [FileC-v3]
```

## If files don't change, Git just links to the previous identical file

---

## The Three States

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="40" text-anchor="middle" font-size="24" font-weight="bold">Git File States</text>
  <rect x="50" y="100" width="200" height="250" fill="#FFE0B2" stroke="#E65100" stroke-width="2" rx="5"/>
  <text x="150" y="130" text-anchor="middle" font-size="18" font-weight="bold">Working Directory</text>
  <text x="150" y="160" text-anchor="middle" font-size="14">Files you see</text>
  <text x="150" y="180" text-anchor="middle" font-size="14">and edit</text>
  <rect x="300" y="100" width="200" height="250" fill="#C8E6C9" stroke="#2E7D32" stroke-width="2" rx="5"/>
  <text x="400" y="130" text-anchor="middle" font-size="18" font-weight="bold">Staging Area</text>
  <text x="400" y="160" text-anchor="middle" font-size="14">Files ready to</text>
  <text x="400" y="180" text-anchor="middle" font-size="14">be committed</text>
  <rect x="550" y="100" width="200" height="250" fill="#BBDEFB" stroke="#1565C0" stroke-width="2" rx="5"/>
  <text x="650" y="130" text-anchor="middle" font-size="18" font-weight="bold">Repository</text>
  <text x="650" y="160" text-anchor="middle" font-size="14">Committed</text>
  <text x="650" y="180" text-anchor="middle" font-size="14">snapshots</text>
  <path d="M 250 225 L 290 225" stroke="#333" stroke-width="3" marker-end="url(#arrow3)"/>
  <text x="270" y="215" text-anchor="middle" font-size="12">git add</text>
  <path d="M 500 225 L 540 225" stroke="#333" stroke-width="3" marker-end="url(#arrow3)"/>
  <text x="520" y="215" text-anchor="middle" font-size="12">git commit</text>
  <path d="M 550 275 Q 400 320 250 275" stroke="#333" stroke-width="3" marker-end="url(#arrow3)" fill="none"/>
  <text x="400" y="340" text-anchor="middle" font-size="12">git checkout</text>
  <defs>
    <marker id="arrow3" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Basic Git Workflow

1. **Modify** files in your working directory
1. **Stage** the changes you want to include in the next commit
1. **Commit** the staged changes to the repository

```bash
# Edit files
vim README.md

# Stage changes
git add README.md

# Commit changes
git commit -m "Update README"
```

---

## Why Use a Staging Area?

1. **Selective commits** - Choose exactly what to commit
1. **Review changes** - See what you're about to commit
1. **Split work** - Separate logical changes into multiple commits
1. **Clean history** - Create meaningful commit history

Example:
```bash
# You changed 3 files but want to commit only 2
git add file1.txt file2.txt
git commit -m "Feature A implementation"
# file3.txt remains uncommitted for a separate commit
```

---

## Git's Integrity

### Everything in Git is checksummed

1. Git uses **SHA-1** hash (moving to SHA-256)
1. 40-character hexadecimal string
1. Calculated based on contents + metadata
1. **Impossible to change anything without Git knowing**

Example SHA-1:
```misc
24b9da6552252987aa493b52f8696cd6d3b00373
```

### You'll see these everywhere in Git

---

## Git Generally Only Adds Data

1. **Almost all operations add data** to the Git database
1. **Very hard to lose data** once committed
1. **Can experiment without fear** of losing work

After committing:
1. Snapshot is safely stored
1. Can always revert to that state
1. History is preserved

### This makes Git forgiving and encourages experimentation

---

## Branches in Git

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="40" text-anchor="middle" font-size="24" font-weight="bold">Branching is Cheap and Fast</text>
  <circle cx="150" cy="200" r="20" fill="#4CAF50"/>
  <text x="150" y="235" text-anchor="middle" font-size="12">C1</text>
  <circle cx="250" cy="200" r="20" fill="#4CAF50"/>
  <text x="250" y="235" text-anchor="middle" font-size="12">C2</text>
  <circle cx="350" cy="200" r="20" fill="#4CAF50"/>
  <text x="350" y="235" text-anchor="middle" font-size="12">C3</text>
  <circle cx="450" cy="140" r="20" fill="#2196F3"/>
  <text x="450" y="175" text-anchor="middle" font-size="12">C4</text>
  <circle cx="550" cy="140" r="20" fill="#2196F3"/>
  <text x="550" y="175" text-anchor="middle" font-size="12">C5</text>
  <circle cx="450" cy="260" r="20" fill="#FF9800"/>
  <text x="450" y="295" text-anchor="middle" font-size="12">C6</text>
  <line x1="170" y1="200" x2="230" y2="200" stroke="#333" stroke-width="2"/>
  <line x1="270" y1="200" x2="330" y2="200" stroke="#333" stroke-width="2"/>
  <line x1="370" y1="190" x2="430" y2="150" stroke="#333" stroke-width="2"/>
  <line x1="370" y1="210" x2="430" y2="250" stroke="#333" stroke-width="2"/>
  <line x1="470" y1="140" x2="530" y2="140" stroke="#333" stroke-width="2"/>
  <rect x="100" y="320" width="80" height="30" fill="#4CAF50" rx="3"/>
  <text x="140" y="340" text-anchor="middle" font-size="12" fill="white">main</text>
  <rect x="250" y="320" width="80" height="30" fill="#2196F3" rx="3"/>
  <text x="290" y="340" text-anchor="middle" font-size="12" fill="white">feature</text>
  <rect x="400" y="320" width="80" height="30" fill="#FF9800" rx="3"/>
  <text x="440" y="340" text-anchor="middle" font-size="12" fill="white">hotfix</text>
</svg>

---

## Why Branches Matter

1. **Parallel development** - Work on multiple features simultaneously
1. **Isolation** - Changes don't affect other branches
1. **Experimentation** - Try ideas without breaking main code
1. **Collaboration** - Multiple developers work independently
1. **Clean history** - Organize commits logically

### In Git, branches are just pointers to commits (41 bytes!)

---

## Git vs GitHub/GitLab/Bitbucket

**Git** is the version control system:
1. Command-line tool
1. Manages repositories locally
1. Free and open source

**GitHub/GitLab/Bitbucket** are hosting platforms:
1. Store repositories online
1. Add collaboration features
1. Provide web interface
1. Issue tracking, CI/CD, wikis

*You can use Git without any hosting platform!*

---

## Common Misconceptions

❌ **"Git is GitHub"**
✅ Git is the tool, GitHub is a hosting service

❌ **"Git is only for code"**
✅ Git can version any files (docs, configs, data)

❌ **"Git is too complex"**
✅ Daily use requires ~10 commands

❌ **"Branches are scary"**
✅ Branches are Git's superpower

---

## When to Use Git

**Perfect for:**
1. Source code (any language)
1. Configuration files
1. Documentation (Markdown, LaTeX)
1. Small data files
1. Scripts and automation

**Not ideal for:**
1. Large binary files (videos, images)
1. Generated files (build artifacts)
1. Sensitive data (passwords, keys)

---

## Git Hosting Options

1. **Cloud Platforms**
    - GitHub (Microsoft)
    - GitLab (SaaS or self-hosted)
    - Bitbucket (Atlassian)
    - Azure Repos
1. **Self-Hosted**
    - GitLab CE
    - Gitea
    - Gogs
1. **Simple Hosting**
    - SSH server
    - Network share
    - Even Dropbox (not recommended)

---

## Adopting Git in Your Organization

## Start Small

1. **Pilot project** - Start with one team
1. **Training** - Invest in proper training
1. **Documentation** - Create workflow guides
1. **Champions** - Identify Git advocates

---

## Migration Strategies

1. **Fresh start** - New projects use Git
1. **Gradual migration** - Move projects one by one
1. **Big bang** - Convert everything at once (risky!)

**Tools for migration:**
- `git svn` - Import from SVN
- `git cvsimport` - Import from CVS
- `git p4` - Import from Perforce

---

## Define Your Workflow

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="40" text-anchor="middle" font-size="22" font-weight="bold">Choose a Workflow</text>
  <rect x="50" y="80" width="150" height="100" fill="#E3F2FD" stroke="#1976D2" stroke-width="2" rx="5"/>
  <text x="125" y="110" text-anchor="middle" font-size="14" font-weight="bold">Centralized</text>
  <text x="125" y="135" text-anchor="middle" font-size="11">Like SVN</text>
  <text x="125" y="155" text-anchor="middle" font-size="11">Simple</text>
  <rect x="225" y="80" width="150" height="100" fill="#F3E5F5" stroke="#7B1FA2" stroke-width="2" rx="5"/>
  <text x="300" y="110" text-anchor="middle" font-size="14" font-weight="bold">Feature Branch</text>
  <text x="300" y="135" text-anchor="middle" font-size="11">Branch per feature</text>
  <text x="300" y="155" text-anchor="middle" font-size="11">Popular</text>
  <rect x="400" y="80" width="150" height="100" fill="#E8F5E9" stroke="#388E3C" stroke-width="2" rx="5"/>
  <text x="475" y="110" text-anchor="middle" font-size="14" font-weight="bold">Gitflow</text>
  <text x="475" y="135" text-anchor="middle" font-size="11">Structured</text>
  <text x="475" y="155" text-anchor="middle" font-size="11">Releases</text>
  <rect x="575" y="80" width="150" height="100" fill="#FFF3E0" stroke="#F57C00" stroke-width="2" rx="5"/>
  <text x="650" y="110" text-anchor="middle" font-size="14" font-weight="bold">Forking</text>
  <text x="650" y="135" text-anchor="middle" font-size="11">Open source</text>
  <text x="650" y="155" text-anchor="middle" font-size="11">Pull requests</text>
  <text x="400" y="230" text-anchor="middle" font-size="16" font-style="italic">No one-size-fits-all solution</text>
  <text x="400" y="260" text-anchor="middle" font-size="14">Choose based on:</text>
  <text x="400" y="285" text-anchor="middle" font-size="12">• Team size • Release cycle • Collaboration style</text>
</svg>

---

## Common Challenges

1. **Learning curve**
    - Solution: Proper training and documentation
1. **Merge conflicts**
    - Solution: Communicate and merge frequently
1. **Large files**
    - Solution: Use Git LFS (Large File Storage)
1. **Messy history**
    - Solution: Establish commit message conventions

---

## Best Practices from Day One

1. **Write good commit messages**
    - What changed and why
    - Present tense, imperative mood
1. **Commit frequently**
    - Small, logical units
    - Easier to review and revert
1. **Use branches**
    - Keep `main` stable
    - Feature branches for development
1. **Pull before push**
    - Avoid conflicts
    - Stay synchronized

---

## Git Commit Messages

## Good ✅
```template
Add user authentication module

- Implement login/logout functionality
- Add password hashing with bcrypt
- Create session management
```

## Bad ❌
```template
fixed stuff
```
```template
asdfasdf
```
```template
WIP
```

---

## The Power of Git History

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="40" text-anchor="middle" font-size="22" font-weight="bold">Git History is Powerful</text>
  <rect x="100" y="80" width="180" height="80" fill="#E8EAF6" stroke="#3F51B5" stroke-width="2" rx="5"/>
  <text x="190" y="110" text-anchor="middle" font-size="14" font-weight="bold">git blame</text>
  <text x="190" y="135" text-anchor="middle" font-size="12">Who changed what</text>
  <rect x="310" y="80" width="180" height="80" fill="#E0F2F1" stroke="#009688" stroke-width="2" rx="5"/>
  <text x="400" y="110" text-anchor="middle" font-size="14" font-weight="bold">git bisect</text>
  <text x="400" y="135" text-anchor="middle" font-size="12">Find breaking commits</text>
  <rect x="520" y="80" width="180" height="80" fill="#FCE4EC" stroke="#C2185B" stroke-width="2" rx="5"/>
  <text x="610" y="110" text-anchor="middle" font-size="14" font-weight="bold">git log</text>
  <text x="610" y="135" text-anchor="middle" font-size="12">Explore history</text>
  <rect x="200" y="200" width="400" height="120" fill="#FFF9C4" stroke="#F57F17" stroke-width="2" rx="5"/>
  <text x="400" y="235" text-anchor="middle" font-size="16" font-weight="bold">Your Git history is documentation</text>
  <text x="400" y="265" text-anchor="middle" font-size="14">• Why was this change made?</text>
  <text x="400" y="285" text-anchor="middle" font-size="14">• What problem did it solve?</text>
  <text x="400" y="305" text-anchor="middle" font-size="14">• Who can I ask about this?</text>
</svg>

---

## Security Considerations

1. **Never commit secrets**
    - Passwords, API keys, tokens
    - Use environment variables
    - Use `.gitignore` for sensitive files
1. **Sign commits** (optional)
    - GPG signatures
    - Verify authenticity
1. **Access control**
    - Who can push to main?
    - Protected branches
1. **Audit trail**
    - Git logs everything
    - Cannot delete history silently

---

## Git is More Than Version Control

1. **Collaboration platform**
    - Code reviews via pull requests
    - Discussions on commits
1. **Documentation system**
    - History tells the story
    - Commit messages explain decisions
1. **Backup solution**
    - Every clone is a full backup
    - Distributed = resilient
1. **Time machine**
    - Go back to any point
    - See what changed when

---

## Real-World Git Success Stories

- Linux Kernel
    - 30+ million lines of code
    - 1000+ contributors per release
    - 10+ commits per hour
- Windows
    - 3.5 million files
    - 300 GB repository
    - Moved from Source Depot to Git
- Android
    - 800+ Git repositories
    - Managed with repo tool
    - Millions of devices updated

---

## Summary

## What We Learned

1. ✅ Git's history and creation
1. ✅ Distributed vs centralized VCS
1. ✅ Git's core concepts (commits, trees, blobs)
1. ✅ The three states (working, staging, repository)
1. ✅ Why branches are powerful
1. ✅ Adopting Git in organizations
1. ✅ Best practices and workflows

---

## Key Takeaways

1. **Git is distributed** - Every clone is complete
1. **Git is fast** - Most operations are local
1. **Git is safe** - Very hard to lose committed data
1. **Git is flexible** - Multiple workflows possible
1. **Git is the standard** - 90%+ adoption rate

---

## What's Next?

In the upcoming sessions, we'll dive into:

1. **Git Basics** - Hands-on with essential commands
1. **Configuration** - Customizing Git for your needs
1. **Branching & Merging** - Advanced workflows
1. **Collaboration** - Working with remotes
1. **Under the Hood** - How Git really works
1. **Advanced Topics** - Rebase, cherry-pick, and more

---

## Resources

1. **Official Documentation**
    - https://git-scm.com/doc
1. **Pro Git Book** (free online)
    - https://git-scm.com/book
1. **Interactive Tutorials**
    - https://learngitbranching.js.org
1. **Git Cheat Sheet**
    - https://education.github.com/git-cheat-sheet-education.pdf

---

## Ready to Master Git?

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="80" text-anchor="middle" font-size="36" font-weight="bold" fill="#FF6B35">Let's Git Started!</text>
  <circle cx="400" cy="200" r="60" fill="#4ECDC4"/>
  <text x="400" y="210" text-anchor="middle" font-size="48" fill="white">Git</text>
  <path d="M 200 300 Q 400 250 600 300" stroke="#556270" stroke-width="3" fill="none"/>
  <circle cx="200" cy="300" r="8" fill="#556270"/>
  <circle cx="300" cy="275" r="8" fill="#556270"/>
  <circle cx="400" cy="265" r="8" fill="#556270"/>
  <circle cx="500" cy="275" r="8" fill="#556270"/>
  <circle cx="600" cy="300" r="8" fill="#556270"/>
  <text x="400" y="350" text-anchor="middle" font-size="18" font-style="italic">Your journey to Git mastery begins now</text>
</svg>
