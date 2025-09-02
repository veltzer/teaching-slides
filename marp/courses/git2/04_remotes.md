# Remote Repositories

---

## What We'll Cover

1. Understanding remote repositories
1. Setting up remotes
1. Cloning vs initializing
1. Fetching and pulling
1. Pushing changes
1. Working with multiple remotes
1. Repository hosting platforms
1. Collaboration workflows

---

## What is a Remote Repository?

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="40" text-anchor="middle" font-size="24" font-weight="bold">Local vs Remote</text>
  <rect x="50" y="80" width="300" height="250" fill="#E8F5E9" stroke="#388E3C" stroke-width="2" rx="5"/>
  <text x="200" y="110" text-anchor="middle" font-size="18" font-weight="bold">Local Repository</text>
  <circle cx="150" cy="160" r="30" fill="#4CAF50"/>
  <text x="150" y="165" text-anchor="middle" font-size="12" fill="white">.git</text>
  <text x="200" y="210" text-anchor="middle" font-size="14">Your Machine</text>
  <text x="70" y="240" font-size="12">• Full history</text>
  <text x="70" y="260" font-size="12">• All branches</text>
  <text x="70" y="280" font-size="12">• Working directory</text>
  <text x="70" y="300" font-size="12">• Can work offline</text>
  <rect x="450" y="80" width="300" height="250" fill="#E3F2FD" stroke="#1976D2" stroke-width="2" rx="5"/>
  <text x="600" y="110" text-anchor="middle" font-size="18" font-weight="bold">Remote Repository</text>
  <circle cx="550" cy="160" r="30" fill="#2196F3"/>
  <text x="550" y="165" text-anchor="middle" font-size="12" fill="white">origin</text>
  <text x="600" y="210" text-anchor="middle" font-size="14">Server/Cloud</text>
  <text x="470" y="240" font-size="12">• Central location</text>
  <text x="470" y="260" font-size="12">• Team collaboration</text>
  <text x="470" y="280" font-size="12">• Backup</text>
  <text x="470" y="300" font-size="12">• CI/CD integration</text>
  <path d="M 350 180 L 450 180" stroke="#333" stroke-width="2" marker-end="url(#arrow1)"/>
  <path d="M 450 200 L 350 200" stroke="#333" stroke-width="2" marker-end="url(#arrow1)"/>
  <text x="400" y="175" text-anchor="middle" font-size="11">push</text>
  <text x="400" y="220" text-anchor="middle" font-size="11">fetch/pull</text>
  <defs>
    <marker id="arrow1" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Remote Repository Locations

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="40" text-anchor="middle" font-size="24" font-weight="bold">Where Can Remotes Live?</text>
  <rect x="50" y="80" width="220" height="120" fill="#E8F5E9" stroke="#388E3C" stroke-width="2" rx="5"/>
  <text x="160" y="110" text-anchor="middle" font-size="16" font-weight="bold">Cloud Platforms</text>
  <text x="70" y="135" font-size="12">• GitHub</text>
  <text x="70" y="155" font-size="12">• GitLab</text>
  <text x="70" y="175" font-size="12">• Bitbucket</text>
  <rect x="290" y="80" width="220" height="120" fill="#FFF3E0" stroke="#F57C00" stroke-width="2" rx="5"/>
  <text x="400" y="110" text-anchor="middle" font-size="16" font-weight="bold">Self-Hosted</text>
  <text x="310" y="135" font-size="12">• GitLab CE/EE</text>
  <text x="310" y="155" font-size="12">• Gitea</text>
  <text x="310" y="175" font-size="12">• Bitbucket Server</text>
  <rect x="530" y="80" width="220" height="120" fill="#E3F2FD" stroke="#1976D2" stroke-width="2" rx="5"/>
  <text x="640" y="110" text-anchor="middle" font-size="16" font-weight="bold">Simple Servers</text>
  <text x="550" y="135" font-size="12">• SSH server</text>
  <text x="550" y="155" font-size="12">• HTTP server</text>
  <text x="550" y="175" font-size="12">• File system</text>
  <rect x="170" y="220" width="460" height="120" fill="#F5F5F5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="400" y="250" text-anchor="middle" font-size="16" font-weight="bold">Remote URLs</text>
  <text x="190" y="280" font-size="12" font-family="monospace">https://github.com/user/repo.git</text>
  <text x="190" y="300" font-size="12" font-family="monospace">git@github.com:user/repo.git</text>
  <text x="190" y="320" font-size="12" font-family="monospace">file:///path/to/repo.git</text>
</svg>

---

## Setting Up Your First Remote

```bash
# Method 1: Clone existing repository
git clone https://github.com/user/repo.git
# Automatically sets up 'origin' remote

# Method 2: Add remote to existing local repo
git init
git remote add origin https://github.com/user/repo.git

# View remotes
git remote -v
# origin  https://github.com/user/repo.git (fetch)
# origin  https://github.com/user/repo.git (push)

# Show remote details
git remote show origin
```

---

## Clone vs Init + Remote

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="40" text-anchor="middle" font-size="24" font-weight="bold">Two Ways to Start</text>
  <rect x="50" y="80" width="320" height="280" fill="#E8F5E9" stroke="#388E3C" stroke-width="2" rx="5"/>
  <text x="210" y="110" text-anchor="middle" font-size="18" font-weight="bold">git clone</text>
  <text x="70" y="140" font-size="12">✓ Downloads entire repository</text>
  <text x="70" y="160" font-size="12">✓ Sets up origin automatically</text>
  <text x="70" y="180" font-size="12">✓ Checks out default branch</text>
  <text x="70" y="200" font-size="12">✓ Configures tracking</text>
  <rect x="70" y="220" width="280" height="40" fill="#4CAF50" rx="3"/>
  <text x="210" y="245" text-anchor="middle" font-size="12" fill="white" font-family="monospace">git clone URL</text>
  <text x="210" y="290" text-anchor="middle" font-size="14" font-weight="bold">Use when:</text>
  <text x="70" y="315" font-size="12">• Joining existing project</text>
  <text x="70" y="335" font-size="12">• Getting copy of repository</text>
  <rect x="430" y="80" width="320" height="280" fill="#E3F2FD" stroke="#1976D2" stroke-width="2" rx="5"/>
  <text x="590" y="110" text-anchor="middle" font-size="18" font-weight="bold">git init + remote add</text>
  <text x="450" y="140" font-size="12">✓ Starts with empty repo</text>
  <text x="450" y="160" font-size="12">✓ You add remote manually</text>
  <text x="450" y="180" font-size="12">✓ No default content</text>
  <text x="450" y="200" font-size="12">✓ Full control over setup</text>
  <rect x="450" y="220" width="280" height="40" fill="#2196F3" rx="3"/>
  <text x="590" y="245" text-anchor="middle" font-size="12" fill="white" font-family="monospace">git init && git remote add</text>
  <text x="590" y="290" text-anchor="middle" font-size="14" font-weight="bold">Use when:</text>
  <text x="450" y="315" font-size="12">• Starting new project</text>
  <text x="450" y="335" font-size="12">• Converting existing code</text>
</svg>

---

## Understanding Remote Names

```bash
# Default remote name is 'origin'
git clone https://github.com/user/repo.git
# Creates remote named 'origin'

# Custom remote name
git clone -o upstream https://github.com/original/repo.git
# Creates remote named 'upstream'

# Multiple remotes
git remote add origin https://github.com/me/repo.git
git remote add upstream https://github.com/original/repo.git
git remote add backup https://gitlab.com/me/repo.git

# Rename remote
git remote rename origin github

# Remove remote
git remote remove backup
```

---

## Remote Branches

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="40" text-anchor="middle" font-size="24" font-weight="bold">Local vs Remote Branches</text>
  <rect x="50" y="80" width="300" height="150" fill="#E8F5E9" stroke="#388E3C" stroke-width="2" rx="5"/>
  <text x="200" y="110" text-anchor="middle" font-size="16" font-weight="bold">Local Branches</text>
  <rect x="70" y="130" width="100" height="30" fill="#4CAF50" rx="3"/>
  <text x="120" y="150" text-anchor="middle" font-size="12" fill="white">main</text>
  <rect x="70" y="170" width="100" height="30" fill="#4CAF50" rx="3"/>
  <text x="120" y="190" text-anchor="middle" font-size="12" fill="white">feature</text>
  <text x="200" y="215" text-anchor="middle" font-size="11">You can modify</text>
  <rect x="450" y="80" width="300" height="150" fill="#FFF3E0" stroke="#F57C00" stroke-width="2" rx="5"/>
  <text x="600" y="110" text-anchor="middle" font-size="16" font-weight="bold">Remote-Tracking Branches</text>
  <rect x="470" y="130" width="150" height="30" fill="#FF9800" rx="3"/>
  <text x="545" y="150" text-anchor="middle" font-size="12" fill="white">origin/main</text>
  <rect x="470" y="170" width="150" height="30" fill="#FF9800" rx="3"/>
  <text x="545" y="190" text-anchor="middle" font-size="12" fill="white">origin/feature</text>
  <text x="600" y="215" text-anchor="middle" font-size="11">Read-only references</text>
  <rect x="200" y="260" width="400" height="100" fill="#F5F5F5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="400" y="290" text-anchor="middle" font-size="14" font-weight="bold">Remote-tracking branches:</text>
  <text x="220" y="315" font-size="12">• Show state of remote branches</text>
  <text x="220" y="335" font-size="12">• Updated with fetch/pull</text>
  <text x="220" y="355" font-size="12">• Cannot be directly modified</text>
</svg>

---

## Fetching Changes

```bash
# Fetch from default remote (origin)
git fetch

# Fetch from specific remote
git fetch upstream

# Fetch specific branch
git fetch origin main

# Fetch all remotes
git fetch --all

# Fetch and prune deleted branches
git fetch --prune

# See what fetch will do (dry run)
git fetch --dry-run
```

---

## Fetch vs Pull

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="40" text-anchor="middle" font-size="24" font-weight="bold">Fetch vs Pull</text>
  <rect x="50" y="80" width="320" height="280" fill="#E8F5E9" stroke="#388E3C" stroke-width="2" rx="5"/>
  <text x="210" y="110" text-anchor="middle" font-size="18" font-weight="bold">git fetch</text>
  <circle cx="210" cy="160" r="25" fill="#4CAF50"/>
  <text x="210" y="165" text-anchor="middle" font-size="10" fill="white">Remote</text>
  <path d="M 210 185 L 210 215" stroke="#333" stroke-width="2" marker-end="url(#arrow2)"/>
  <circle cx="210" cy="240" r="25" fill="#FF9800"/>
  <text x="210" y="245" text-anchor="middle" font-size="10" fill="white">origin/main</text>
  <text x="210" y="280" text-anchor="middle" font-size="12">Updates references only</text>
  <text x="210" y="300" text-anchor="middle" font-size="12">Safe - no merge</text>
  <text x="210" y="320" text-anchor="middle" font-size="12">Review before integrating</text>
  <rect x="430" y="80" width="320" height="280" fill="#E3F2FD" stroke="#1976D2" stroke-width="2" rx="5"/>
  <text x="590" y="110" text-anchor="middle" font-size="18" font-weight="bold">git pull</text>
  <circle cx="590" cy="160" r="25" fill="#2196F3"/>
  <text x="590" y="165" text-anchor="middle" font-size="10" fill="white">Remote</text>
  <path d="M 590 185 L 590 215" stroke="#333" stroke-width="2" marker-end="url(#arrow2)"/>
  <circle cx="540" cy="240" r="25" fill="#FF9800"/>
  <text x="540" y="245" text-anchor="middle" font-size="10" fill="white">origin/main</text>
  <circle cx="640" cy="240" r="25" fill="#4CAF50"/>
  <text x="640" y="245" text-anchor="middle" font-size="10" fill="white">main</text>
  <path d="M 565 240 L 615 240" stroke="#333" stroke-width="2" marker-end="url(#arrow2)"/>
  <text x="590" y="280" text-anchor="middle" font-size="12">Fetch + Merge</text>
  <text x="590" y="300" text-anchor="middle" font-size="12">Updates working branch</text>
  <text x="590" y="320" text-anchor="middle" font-size="12">Can cause conflicts</text>
  <defs>
    <marker id="arrow2" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Pull Strategies

```bash
# Default pull (merge)
git pull

# Pull with rebase
git pull --rebase

# Pull with fast-forward only
git pull --ff-only

# Configure default pull strategy
git config pull.rebase true    # Always rebase
git config pull.ff only        # Only fast-forward

# Pull from specific remote and branch
git pull upstream main

# Verbose output
git pull --verbose
```

---

## Pushing Changes

```bash
# Push current branch to origin
git push

# Push specific branch
git push origin main

# Push all branches
git push --all

# Push with tags
git push --follow-tags

# Push specific tag
git push origin v1.0.0

# Force push (DANGEROUS!)
git push --force

# Safer force push
git push --force-with-lease

# Set upstream branch
git push -u origin feature
```

---

## Push Scenarios

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="40" text-anchor="middle" font-size="24" font-weight="bold">Common Push Scenarios</text>
  <rect x="50" y="80" width="350" height="80" fill="#E8F5E9" stroke="#388E3C" stroke-width="2" rx="5"/>
  <text x="225" y="105" text-anchor="middle" font-size="14" font-weight="bold">Fast-Forward Push</text>
  <circle cx="120" cy="130" r="15" fill="#4CAF50"/>
  <circle cx="170" cy="130" r="15" fill="#4CAF50"/>
  <circle cx="220" cy="130" r="15" fill="#81C784"/>
  <circle cx="270" cy="130" r="15" fill="#81C784"/>
  <line x1="135" y1="130" x2="155" y2="130" stroke="#333" stroke-width="2"/>
  <line x1="185" y1="130" x2="205" y2="130" stroke="#333" stroke-width="2"/>
  <line x1="235" y1="130" x2="255" y2="130" stroke="#333" stroke-width="2"/>
  <text x="320" y="135" font-size="11">✓ Success</text>
  <rect x="420" y="80" width="330" height="80" fill="#FFEBEE" stroke="#C62828" stroke-width="2" rx="5"/>
  <text x="585" y="105" text-anchor="middle" font-size="14" font-weight="bold">Non-Fast-Forward Push</text>
  <circle cx="480" cy="130" r="15" fill="#4CAF50"/>
  <circle cx="530" cy="110" r="15" fill="#4CAF50"/>
  <circle cx="530" cy="150" r="15" fill="#81C784"/>
  <circle cx="580" cy="150" r="15" fill="#81C784"/>
  <line x1="495" y1="130" x2="515" y2="115" stroke="#333" stroke-width="2"/>
  <line x1="495" y1="130" x2="515" y2="145" stroke="#333" stroke-width="2"/>
  <line x1="545" y1="150" x2="565" y2="150" stroke="#333" stroke-width="2"/>
  <text x="670" y="135" font-size="11">✗ Rejected</text>
  <rect x="50" y="180" width="700" height="80" fill="#FFF3E0" stroke="#F57C00" stroke-width="2" rx="5"/>
  <text x="400" y="205" text-anchor="middle" font-size="14" font-weight="bold">Force Push (Rewrites History)</text>
  <circle cx="250" cy="230" r="15" fill="#4CAF50"/>
  <circle cx="300" cy="230" r="15" fill="#FF9800" stroke-dasharray="3,3"/>
  <circle cx="350" cy="230" r="15" fill="#81C784"/>
  <circle cx="400" cy="230" r="15" fill="#81C784"/>
  <line x1="265" y1="230" x2="285" y2="230" stroke="#999" stroke-width="2" stroke-dasharray="3,3"/>
  <line x1="315" y1="230" x2="335" y2="230" stroke="#333" stroke-width="2"/>
  <line x1="365" y1="230" x2="385" y2="230" stroke="#333" stroke-width="2"/>
  <text x="500" y="235" font-size="11">⚠️ Dangerous!</text>
  <rect x="200" y="280" width="400" height="80" fill="#F5F5F5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="400" y="310" text-anchor="middle" font-size="13">Non-fast-forward? Pull first, then push</text>
  <text x="400" y="335" text-anchor="middle" font-size="12" font-family="monospace">git pull --rebase && git push</text>
</svg>

---

## Tracking Branches

```bash
# Set upstream branch while pushing
git push -u origin feature
# Now 'git push' and 'git pull' work without arguments

# Set upstream for existing branch
git branch --set-upstream-to=origin/feature

# Create local branch tracking remote
git checkout -b feature origin/feature
# or
git checkout --track origin/feature

# See tracking relationships
git branch -vv
# * main     a3d8f2c [origin/main] Latest commit
#   feature  b7c9e1a [origin/feature: ahead 2] Local changes

# Remove tracking
git branch --unset-upstream
```

---

## Working with Multiple Remotes

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="40" text-anchor="middle" font-size="24" font-weight="bold">Multiple Remotes Workflow</text>
  <circle cx="400" cy="200" r="40" fill="#4CAF50"/>
  <text x="400" y="205" text-anchor="middle" font-size="14" fill="white">Local</text>
  <circle cx="200" cy="100" r="35" fill="#2196F3"/>
  <text x="200" y="105" text-anchor="middle" font-size="12" fill="white">origin</text>
  <text x="200" y="125" text-anchor="middle" font-size="10">Your fork</text>
  <circle cx="600" cy="100" r="35" fill="#FF9800"/>
  <text x="600" y="105" text-anchor="middle" font-size="12" fill="white">upstream</text>
  <text x="600" y="125" text-anchor="middle" font-size="10">Original</text>
  <circle cx="200" cy="300" r="35" fill="#9C27B0"/>
  <text x="200" y="305" text-anchor="middle" font-size="12" fill="white">backup</text>
  <text x="200" y="325" text-anchor="middle" font-size="10">GitLab</text>
  <circle cx="600" cy="300" r="35" fill="#795548"/>
  <text x="600" y="305" text-anchor="middle" font-size="12" fill="white">deploy</text>
  <text x="600" y="325" text-anchor="middle" font-size="10">Production</text>
  <path d="M 360 180 L 235 125" stroke="#333" stroke-width="2" marker-end="url(#arrow3)" marker-start="url(#arrow3)"/>
  <path d="M 440 180 L 565 125" stroke="#333" stroke-width="2" marker-end="url(#arrow3)"/>
  <path d="M 360 220 L 235 275" stroke="#333" stroke-width="2" marker-end="url(#arrow3)"/>
  <path d="M 440 220 L 565 275" stroke="#333" stroke-width="2" marker-end="url(#arrow3)"/>
  <text x="280" y="150" font-size="10">push/pull</text>
  <text x="520" y="150" font-size="10">fetch</text>
  <text x="280" y="250" font-size="10">push</text>
  <text x="520" y="250" font-size="10">push</text>
  <defs>
    <marker id="arrow3" markerWidth="10" markerHeight="10" refX="5" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Fork Workflow Example

```bash
# 1. Fork on GitHub (via web interface)

# 2. Clone your fork
git clone https://github.com/YOU/project.git

# 3. Add upstream remote
git remote add upstream https://github.com/ORIGINAL/project.git

# 4. Keep fork updated
git fetch upstream
git checkout main
git merge upstream/main
git push origin main

# 5. Create feature branch
git checkout -b feature

# 6. Push to your fork
git push origin feature

# 7. Create Pull Request (via web interface)
```

---

## Remote URLs: HTTPS vs SSH

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="40" text-anchor="middle" font-size="24" font-weight="bold">HTTPS vs SSH</text>
  <rect x="50" y="80" width="320" height="280" fill="#E8F5E9" stroke="#388E3C" stroke-width="2" rx="5"/>
  <text x="210" y="110" text-anchor="middle" font-size="18" font-weight="bold">HTTPS</text>
  <rect x="70" y="130" width="280" height="30" fill="#81C784" rx="3"/>
  <text x="210" y="150" text-anchor="middle" font-size="10" fill="white" font-family="monospace">https://github.com/user/repo.git</text>
  <text x="70" y="185" font-size="12">✓ Works everywhere</text>
  <text x="70" y="205" font-size="12">✓ Firewall friendly</text>
  <text x="70" y="225" font-size="12">✓ Easy setup</text>
  <text x="70" y="245" font-size="12">✗ Password/token each push</text>
  <text x="70" y="265" font-size="12">✗ Less secure (without 2FA)</text>
  <text x="210" y="295" text-anchor="middle" font-size="13" font-weight="bold">Best for:</text>
  <text x="70" y="315" font-size="11">• Public repositories</text>
  <text x="70" y="335" font-size="11">• Quick clones</text>
  <rect x="430" y="80" width="320" height="280" fill="#E3F2FD" stroke="#1976D2" stroke-width="2" rx="5"/>
  <text x="590" y="110" text-anchor="middle" font-size="18" font-weight="bold">SSH</text>
  <rect x="450" y="130" width="280" height="30" fill="#64B5F6" rx="3"/>
  <text x="590" y="150" text-anchor="middle" font-size="10" fill="white" font-family="monospace">git@github.com:user/repo.git</text>
  <text x="450" y="185" font-size="12">✓ No password after setup</text>
  <text x="450" y="205" font-size="12">✓ More secure</text>
  <text x="450" y="225" font-size="12">✓ Key-based auth</text>
  <text x="450" y="245" font-size="12">✗ Initial setup required</text>
  <text x="450" y="265" font-size="12">✗ Port 22 may be blocked</text>
  <text x="590" y="295" text-anchor="middle" font-size="13" font-weight="bold">Best for:</text>
  <text x="450" y="315" font-size="11">• Regular contributors</text>
  <text x="450" y="335" font-size="11">• Private repositories</text>
</svg>

---

## Changing Remote URLs

```bash
# View current URL
git remote get-url origin

# Change from HTTPS to SSH
git remote set-url origin git@github.com:user/repo.git

# Change from SSH to HTTPS
git remote set-url origin https://github.com/user/repo.git

# Add push URL different from fetch
git remote set-url --push origin git@github.com:user/repo.git

# Verify change
git remote -v
# origin  https://github.com/user/repo.git (fetch)
# origin  git@github.com:user/repo.git (push)
```

---

## Understanding Publishing

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="40" text-anchor="middle" font-size="24" font-weight="bold">Publishing a Repository</text>
  <rect x="100" y="80" width="600" height="80" fill="#F5F5F5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="400" y="110" text-anchor="middle" font-size="16" font-weight="bold">Step 1: Create Remote Repository</text>
  <text x="400" y="135" text-anchor="middle" font-size="12">GitHub/GitLab/Bitbucket → New Repository</text>
  <text x="400" y="150" text-anchor="middle" font-size="12">Don't initialize with README if pushing existing code</text>
  <rect x="100" y="180" width="280" height="180" fill="#E8F5E9" stroke="#388E3C" stroke-width="2" rx="5"/>
  <text x="240" y="210" text-anchor="middle" font-size="16" font-weight="bold">Existing Project</text>
  <text x="120" y="240" font-size="11" font-family="monospace">git remote add origin URL</text>
  <text x="120" y="260" font-size="11" font-family="monospace">git branch -M main</text>
  <text x="120" y="280" font-size="11" font-family="monospace">git push -u origin main</text>
  <text x="240" y="310" text-anchor="middle" font-size="12">Pushes existing commits</text>
  <text x="240" y="330" text-anchor="middle" font-size="12">Sets up tracking</text>
  <rect x="420" y="180" width="280" height="180" fill="#E3F2FD" stroke="#1976D2" stroke-width="2" rx="5"/>
  <text x="560" y="210" text-anchor="middle" font-size="16" font-weight="bold">New Project</text>
  <text x="440" y="240" font-size="11" font-family="monospace">git init</text>
  <text x="440" y="260" font-size="11" font-family="monospace">git add .</text>
  <text x="440" y="280" font-size="11" font-family="monospace">git commit -m "Initial"</text>
  <text x="440" y="300" font-size="11" font-family="monospace">git remote add origin URL</text>
  <text x="440" y="320" font-size="11" font-family="monospace">git push -u origin main</text>
  <text x="560" y="345" text-anchor="middle" font-size="12">Creates first commit</text>
</svg>

---

## Remote Repository Structure

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="40" text-anchor="middle" font-size="24" font-weight="bold">Bare vs Non-Bare Repositories</text>
  <rect x="50" y="80" width="320" height="280" fill="#E8F5E9" stroke="#388E3C" stroke-width="2" rx="5"/>
  <text x="210" y="110" text-anchor="middle" font-size="18" font-weight="bold">Non-Bare (Local)</text>
  <rect x="70" y="130" width="280" height="30" fill="#81C784" rx="3"/>
  <text x="210" y="150" text-anchor="middle" font-size="12" fill="white">.git/</text>
  <rect x="70" y="170" width="280" height="30" fill="#A5D6A7" rx="3"/>
  <text x="210" y="190" text-anchor="middle" font-size="12">Working Directory</text>
  <text x="70" y="225" font-size="12">✓ Can edit files</text>
  <text x="70" y="245" font-size="12">✓ Can make commits</text>
  <text x="70" y="265" font-size="12">✓ Has working tree</text>
  <text x="70" y="285" font-size="12">✗ Not ideal for sharing</text>
  <text x="210" y="315" text-anchor="middle" font-size="13" font-weight="bold">Your local repository</text>
  <rect x="430" y="80" width="320" height="280" fill="#FFF3E0" stroke="#F57C00" stroke-width="2" rx="5"/>
  <text x="590" y="110" text-anchor="middle" font-size="18" font-weight="bold">Bare (Remote)</text>
  <rect x="450" y="130" width="280" height="30" fill="#FFB74D" rx="3"/>
  <text x="590" y="150" text-anchor="middle" font-size="12" fill="white">repo.git/</text>
  <rect x="450" y="170" width="280" height="30" fill="#FFE0B2" rx="3" stroke-dasharray="5,5" stroke="#999"/>
  <text x="590" y="190" text-anchor="middle" font-size="12" fill="#999">No Working Directory</text>
  <text x="450" y="225" font-size="12">✗ Cannot edit files directly</text>
  <text x="450" y="245" font-size="12">✗ Cannot make commits</text>
  <text x="450" y="265" font-size="12">✓ Optimized for sharing</text>
  <text x="450" y="285" font-size="12">✓ Accepts pushes safely</text>
  <text x="590" y="315" text-anchor="middle" font-size="13" font-weight="bold">GitHub/GitLab repositories</text>
</svg>

---

## Creating a Bare Repository

```bash
# Create bare repository for sharing
git init --bare myproject.git

# Structure of bare repo
ls myproject.git/
# HEAD  config  description  hooks/  info/  objects/  refs/

# Convert existing repo to bare
git clone --bare existing-repo bare-repo.git

# Push to bare repository
cd my-project
git remote add origin /path/to/bare-repo.git
git push origin main

# Serve bare repo over SSH
# Users can clone via:
git clone user@server:/path/to/bare-repo.git
```

---

## GitHub: The Platform

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="40" text-anchor="middle" font-size="24" font-weight="bold">GitHub Features</text>
  <rect x="50" y="80" width="200" height="120" fill="#24292E" rx="5"/>
  <text x="150" y="110" text-anchor="middle" font-size="16" fill="white" font-weight="bold">Core Git</text>
  <text x="150" y="135" text-anchor="middle" font-size="12" fill="white">• Repositories</text>
  <text x="150" y="155" text-anchor="middle" font-size="12" fill="white">• Branches</text>
  <text x="150" y="175" text-anchor="middle" font-size="12" fill="white">• Commits</text>
  <rect x="270" y="80" width="200" height="120" fill="#0366D6" rx="5"/>
  <text x="370" y="110" text-anchor="middle" font-size="16" fill="white" font-weight="bold">Collaboration</text>
  <text x="370" y="135" text-anchor="middle" font-size="12" fill="white">• Pull Requests</text>
  <text x="370" y="155" text-anchor="middle" font-size="12" fill="white">• Code Review</text>
  <text x="370" y="175" text-anchor="middle" font-size="12" fill="white">• Issues</text>
  <rect x="490" y="80" width="200" height="120" fill="#28A745" rx="5"/>
  <text x="590" y="110" text-anchor="middle" font-size="16" fill="white" font-weight="bold">CI/CD</text>
  <text x="590" y="135" text-anchor="middle" font-size="12" fill="white">• GitHub Actions</text>
  <text x="590" y="155" text-anchor="middle" font-size="12" fill="white">• Packages</text>
  <text x="590" y="175" text-anchor="middle" font-size="12" fill="white">• Releases</text>
  <rect x="50" y="220" width="200" height="120" fill="#6F42C1" rx="5"/>
  <text x="150" y="250" text-anchor="middle" font-size="16" fill="white" font-weight="bold">Project Mgmt</text>
  <text x="150" y="275" text-anchor="middle" font-size="12" fill="white">• Projects</text>
  <text x="150" y="295" text-anchor="middle" font-size="12" fill="white">• Milestones</text>
  <text x="150" y="315" text-anchor="middle" font-size="12" fill="white">• Wiki</text>
  <rect x="270" y="220" width="200" height="120" fill="#FD7E14" rx="5"/>
  <text x="370" y="250" text-anchor="middle" font-size="16" fill="white" font-weight="bold">Security</text>
  <text x="370" y="275" text-anchor="middle" font-size="12" fill="white">• Dependabot</text>
  <text x="370" y="295" text-anchor="middle" font-size="12" fill="white">• Code scanning</text>
  <text x="370" y="315" text-anchor="middle" font-size="12" fill="white">• Secrets</text>
  <rect x="490" y="220" width="200" height="120" fill="#DC3545" rx="5"/>
  <text x="590" y="250" text-anchor="middle" font-size="16" fill="white" font-weight="bold">Social</text>
  <text x="590" y="275" text-anchor="middle" font-size="12" fill="white">• Stars</text>
  <text x="590" y="295" text-anchor="middle" font-size="12" fill="white">• Forks</text>
  <text x="590" y="315" text-anchor="middle" font-size="12" fill="white">• Discussions</text>
</svg>

---

## GitLab: The Alternative

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="40" text-anchor="middle" font-size="24" font-weight="bold">GitLab Features</text>
  <rect x="50" y="80" width="220" height="120" fill="#FC6D26" rx="5"/>
  <text x="160" y="110" text-anchor="middle" font-size="16" fill="white" font-weight="bold">Built-in CI/CD</text>
  <text x="160" y="135" text-anchor="middle" font-size="12" fill="white">• .gitlab-ci.yml</text>
  <text x="160" y="155" text-anchor="middle" font-size="12" fill="white">• Runners</text>
  <text x="160" y="175" text-anchor="middle" font-size="12" fill="white">• Pipelines</text>
  <rect x="290" y="80" width="220" height="120" fill="#554488" rx="5"/>
  <text x="400" y="110" text-anchor="middle" font-size="16" fill="white" font-weight="bold">DevOps Platform</text>
  <text x="400" y="135" text-anchor="middle" font-size="12" fill="white">• Planning</text>
  <text x="400" y="155" text-anchor="middle" font-size="12" fill="white">• Monitoring</text>
  <text x="400" y="175" text-anchor="middle" font-size="12" fill="white">• Security</text>
  <rect x="530" y="80" width="220" height="120" fill="#FCA326" rx="5"/>
  <text x="640" y="110" text-anchor="middle" font-size="16" fill="white" font-weight="bold">Self-Hosted Option</text>
  <text x="640" y="135" text-anchor="middle" font-size="12" fill="white">• GitLab CE (free)</text>
  <text x="640" y="155" text-anchor="middle" font-size="12" fill="white">• GitLab EE</text>
  <text x="640" y="175" text-anchor="middle" font-size="12" fill="white">• Full control</text>
  <rect x="200" y="220" width="400" height="120" fill="#F5F5F5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="400" y="250" text-anchor="middle" font-size="16" font-weight="bold">GitLab vs GitHub</text>
  <text x="220" y="275" font-size="12">• All-in-one DevOps platform</text>
  <text x="220" y="295" font-size="12">• Free private repos (unlimited)</text>
  <text x="220" y="315" font-size="12">• Integrated CI/CD out of the box</text>
</svg>

---

## Bitbucket: Enterprise Focus

```bash
# Bitbucket URLs
# HTTPS
https://bitbucket.org/workspace/repo.git
# SSH
git@bitbucket.org:workspace/repo.git

# Bitbucket-specific features
# - Jira integration
# - Confluence integration
# - Built-in CI/CD (Pipelines)
# - Mercurial support (deprecated)

# Clone from Bitbucket
git clone git@bitbucket.org:team/project.git

# Add Bitbucket remote
git remote add bitbucket git@bitbucket.org:team/project.git
```

---

## Collaboration Workflows

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="40" text-anchor="middle" font-size="24" font-weight="bold">Common Collaboration Workflows</text>
  <rect x="50" y="80" width="170" height="280" fill="#E8F5E9" stroke="#388E3C" stroke-width="2" rx="5"/>
  <text x="135" y="110" text-anchor="middle" font-size="16" font-weight="bold">Centralized</text>
  <circle cx="135" cy="150" r="20" fill="#4CAF50"/>
  <text x="135" y="155" text-anchor="middle" font-size="10" fill="white">main</text>
  <circle cx="90" cy="220" r="15" fill="#81C784"/>
  <circle cx="135" cy="220" r="15" fill="#81C784"/>
  <circle cx="180" cy="220" r="15" fill="#81C784"/>
  <line x1="90" y1="205" x2="125" y2="170" stroke="#333" stroke-width="2"/>
  <line x1="135" y1="205" x2="135" y2="170" stroke="#333" stroke-width="2"/>
  <line x1="180" y1="205" x2="145" y2="170" stroke="#333" stroke-width="2"/>
  <text x="135" y="260" text-anchor="middle" font-size="11">Everyone pushes</text>
  <text x="135" y="275" text-anchor="middle" font-size="11">to main</text>
  <text x="135" y="305" text-anchor="middle" font-size="12" font-weight="bold">Simple</text>
  <text x="135" y="325" text-anchor="middle" font-size="11">Small teams</text>
  <rect x="240" y="80" width="170" height="280" fill="#E3F2FD" stroke="#1976D2" stroke-width="2" rx="5"/>
  <text x="325" y="110" text-anchor="middle" font-size="16" font-weight="bold">Feature Branch</text>
  <circle cx="325" cy="150" r="20" fill="#2196F3"/>
  <text x="325" y="155" text-anchor="middle" font-size="10" fill="white">main</text>
  <circle cx="280" cy="200" r="15" fill="#64B5F6"/>
  <circle cx="370" cy="200" r="15" fill="#64B5F6"/>
  <line x1="315" y1="170" x2="290" y2="185" stroke="#333" stroke-width="2"/>
  <line x1="335" y1="170" x2="360" y2="185" stroke="#333" stroke-width="2"/>
  <text x="280" y="225" text-anchor="middle" font-size="9">feat-1</text>
  <text x="370" y="225" text-anchor="middle" font-size="9">feat-2</text>
  <text x="325" y="260" text-anchor="middle" font-size="11">Branch per</text>
  <text x="325" y="275" text-anchor="middle" font-size="11">feature</text>
  <text x="325" y="305" text-anchor="middle" font-size="12" font-weight="bold">Popular</text>
  <text x="325" y="325" text-anchor="middle" font-size="11">Most teams</text>
  <rect x="430" y="80" width="170" height="280" fill="#FFF3E0" stroke="#F57C00" stroke-width="2" rx="5"/>
  <text x="515" y="110" text-anchor="middle" font-size="16" font-weight="bold">Gitflow</text>
  <circle cx="515" cy="150" r="15" fill="#FF9800"/>
  <text x="515" y="155" text-anchor="middle" font-size="9" fill="white">main</text>
  <circle cx="515" cy="190" r="15" fill="#FFB74D"/>
  <text x="515" y="195" text-anchor="middle" font-size="9">develop</text>
  <circle cx="470" cy="230" r="12" fill="#FFE0B2"/>
  <circle cx="560" cy="230" r="12" fill="#FFE0B2"/>
  <text x="515" y="265" text-anchor="middle" font-size="11">Multiple</text>
  <text x="515" y="280" text-anchor="middle" font-size="11">branch types</text>
  <text x="515" y="305" text-anchor="middle" font-size="12" font-weight="bold">Complex</text>
  <text x="515" y="325" text-anchor="middle" font-size="11">Releases</text>
  <rect x="620" y="80" width="130" height="280" fill="#FFEBEE" stroke="#C62828" stroke-width="2" rx="5"/>
  <text x="685" y="110" text-anchor="middle" font-size="16" font-weight="bold">Forking</text>
  <circle cx="685" cy="150" r="15" fill="#F44336"/>
  <text x="685" y="155" text-anchor="middle" font-size="9" fill="white">upstream</text>
  <circle cx="650" cy="200" r="12" fill="#EF5350"/>
  <circle cx="720" cy="200" r="12" fill="#EF5350"/>
  <text x="650" y="225" text-anchor="middle" font-size="9">fork1</text>
  <text x="720" y="225" text-anchor="middle" font-size="9">fork2</text>
  <text x="685" y="265" text-anchor="middle" font-size="11">Personal</text>
  <text x="685" y="280" text-anchor="middle" font-size="11">forks</text>
  <text x="685" y="305" text-anchor="middle" font-size="12" font-weight="bold">OSS</text>
  <text x="685" y="325" text-anchor="middle" font-size="11">Open source</text>
</svg>

---

## Pull Requests / Merge Requests

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="40" text-anchor="middle" font-size="24" font-weight="bold">Pull Request Workflow</text>
  <circle cx="100" cy="150" r="25" fill="#4CAF50"/>
  <text x="100" y="155" text-anchor="middle" font-size="12" fill="white">main</text>
  <circle cx="200" cy="150" r="25" fill="#2196F3"/>
  <text x="200" y="155" text-anchor="middle" font-size="12" fill="white">feature</text>
  <path d="M 125 150 L 175 150" stroke="#333" stroke-width="2" marker-end="url(#arrow1)"/>
  <text x="150" y="140" text-anchor="middle" font-size="10">1. Branch</text>
  <rect x="250" y="130" width="100" height="40" fill="#FF9800" rx="5"/>
  <text x="300" y="155" text-anchor="middle" font-size="12" fill="white">Commits</text>
  <path d="M 225 150 L 250 150" stroke="#333" stroke-width="2"/>
  <text x="300" y="190" text-anchor="middle" font-size="10">2. Work</text>
  <rect x="380" y="120" width="120" height="60" fill="#9C27B0" rx="5"/>
  <text x="440" y="145" text-anchor="middle" font-size="12" fill="white">Pull Request</text>
  <text x="440" y="165" text-anchor="middle" font-size="10" fill="white">Review & Discuss</text>
  <path d="M 350 150 L 380 150" stroke="#333" stroke-width="2"/>
  <text x="440" y="200" text-anchor="middle" font-size="10">3. Request merge</text>
  <circle cx="550" cy="150" r="25" fill="#4CAF50"/>
  <text x="550" y="155" text-anchor="middle" font-size="12" fill="white">main</text>
  <text x="550" y="120" text-anchor="middle" font-size="10">Updated</text>
  <path d="M 500 150 L 525 150" stroke="#333" stroke-width="2" marker-end="url(#arrow1)"/>
  <text x="550" y="200" text-anchor="middle" font-size="10">4. Merge</text>
  <rect x="200" y="250" width="400" height="100" fill="#F5F5F5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="400" y="280" text-anchor="middle" font-size="14" font-weight="bold">Pull Request Benefits:</text>
  <text x="220" y="305" font-size="12">• Code review before merge</text>
  <text x="220" y="325" font-size="12">• Discussion and feedback</text>
  <text x="420" y="305" font-size="12">• CI/CD integration</text>
  <text x="420" y="325" font-size="12">• Documentation trail</text>
  <defs>
    <marker id="arrow1" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Creating a Pull Request

```bash
# 1. Create feature branch
git checkout -b feature/add-login

# 2. Make changes and commit
git add .
git commit -m "Add login functionality"

# 3. Push to your fork/origin
git push origin feature/add-login

# 4. GitHub CLI (optional)
gh pr create --title "Add login" --body "Description"

# Or use web interface:
# - Go to GitHub/GitLab
# - Click "New Pull Request"
# - Select base and compare branches
# - Add title and description
# - Request reviewers
# - Submit
```

---

## Code Review Process

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="40" text-anchor="middle" font-size="24" font-weight="bold">Code Review Workflow</text>
  <rect x="50" y="80" width="150" height="80" fill="#E8F5E9" stroke="#388E3C" stroke-width="2" rx="5"/>
  <text x="125" y="110" text-anchor="middle" font-size="14" font-weight="bold">1. Submit PR</text>
  <text x="125" y="135" text-anchor="middle" font-size="11">Author creates</text>
  <text x="125" y="150" text-anchor="middle" font-size="11">pull request</text>
  <rect x="220" y="80" width="150" height="80" fill="#E3F2FD" stroke="#1976D2" stroke-width="2" rx="5"/>
  <text x="295" y="110" text-anchor="middle" font-size="14" font-weight="bold">2. Review</text>
  <text x="295" y="135" text-anchor="middle" font-size="11">Team reviews</text>
  <text x="295" y="150" text-anchor="middle" font-size="11">code changes</text>
  <rect x="390" y="80" width="150" height="80" fill="#FFF3E0" stroke="#F57C00" stroke-width="2" rx="5"/>
  <text x="465" y="110" text-anchor="middle" font-size="14" font-weight="bold">3. Feedback</text>
  <text x="465" y="135" text-anchor="middle" font-size="11">Comments &</text>
  <text x="465" y="150" text-anchor="middle" font-size="11">suggestions</text>
  <rect x="560" y="80" width="150" height="80" fill="#F3E5F5" stroke="#7B1FA2" stroke-width="2" rx="5"/>
  <text x="635" y="110" text-anchor="middle" font-size="14" font-weight="bold">4. Update</text>
  <text x="635" y="135" text-anchor="middle" font-size="11">Author makes</text>
  <text x="635" y="150" text-anchor="middle" font-size="11">changes</text>
  <path d="M 200 120 L 220 120" stroke="#333" stroke-width="2" marker-end="url(#arrow2)"/>
  <path d="M 370 120 L 390 120" stroke="#333" stroke-width="2" marker-end="url(#arrow2)"/>
  <path d="M 540 120 L 560 120" stroke="#333" stroke-width="2" marker-end="url(#arrow2)"/>
  <path d="M 635 160 Q 635 200 295 200 Q 295 160 295 160" stroke="#333" stroke-width="2" marker-end="url(#arrow2)"/>
  <text x="465" y="215" text-anchor="middle" font-size="10">Iterate</text>
  <rect x="100" y="250" width="600" height="100" fill="#C8E6C9" stroke="#388E3C" stroke-width="2" rx="5"/>
  <text x="400" y="280" text-anchor="middle" font-size="16" font-weight="bold">5. Approve & Merge</text>
  <text x="400" y="305" text-anchor="middle" font-size="12">✓ Tests pass</text>
  <text x="400" y="325" text-anchor="middle" font-size="12">✓ Reviews approved</text>
  <defs>
    <marker id="arrow2" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Pull Request Best Practices

```bash
# Keep PRs small and focused
# ✓ One feature per PR
# ✓ Easy to review
# ✗ Multiple unrelated changes

# Write descriptive PR descriptions
# - What changed
# - Why it changed
# - How to test
# - Screenshots if UI changes

# Keep commits clean
git rebase -i main  # Before creating PR

# Update branch before merge
git fetch origin
git rebase origin/main
git push --force-lease

# Use draft PRs for work in progress
# Mark as "Draft" in GitHub/GitLab
```

---

## Handling Merge Conflicts

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="40" text-anchor="middle" font-size="24" font-weight="bold">Merge Conflict Resolution</text>
  <rect x="100" y="80" width="600" height="80" fill="#FFEBEE" stroke="#C62828" stroke-width="2" rx="5"/>
  <text x="400" y="105" text-anchor="middle" font-size="14" font-weight="bold">Conflict Markers</text>
  <text x="120" y="125" font-family="monospace" font-size="11">&lt;&lt;&lt;&lt;&lt;&lt;&lt; HEAD</text>
  <text x="120" y="140" font-family="monospace" font-size="11">Your changes</text>
  <text x="120" y="155" font-family="monospace" font-size="11">=======</text>
  <text x="300" y="125" font-family="monospace" font-size="11">Their changes</text>
  <text x="300" y="140" font-family="monospace" font-size="11">&gt;&gt;&gt;&gt;&gt;&gt;&gt; feature-branch</text>
  <text x="500" y="140" font-size="12">← Choose one or combine</text>
  <rect x="50" y="180" width="320" height="180" fill="#FFF3E0" stroke="#F57C00" stroke-width="2" rx="5"/>
  <text x="210" y="210" text-anchor="middle" font-size="14" font-weight="bold">Resolution Steps</text>
  <text x="70" y="235" font-size="12">1. Open conflicted file</text>
  <text x="70" y="255" font-size="12">2. Find conflict markers</text>
  <text x="70" y="275" font-size="12">3. Decide what to keep</text>
  <text x="70" y="295" font-size="12">4. Remove markers</text>
  <text x="70" y="315" font-size="12">5. Stage resolved file</text>
  <text x="70" y="335" font-size="12">6. Continue merge/rebase</text>
  <rect x="430" y="180" width="320" height="180" fill="#E8F5E9" stroke="#388E3C" stroke-width="2" rx="5"/>
  <text x="590" y="210" text-anchor="middle" font-size="14" font-weight="bold">Conflict Commands</text>
  <text x="450" y="235" font-family="monospace" font-size="11">git status  # See conflicts</text>
  <text x="450" y="255" font-family="monospace" font-size="11">git diff    # View conflicts</text>
  <text x="450" y="275" font-family="monospace" font-size="11">git add file.txt  # Mark resolved</text>
  <text x="450" y="295" font-family="monospace" font-size="11">git merge --continue</text>
  <text x="450" y="315" font-family="monospace" font-size="11"># Or abort:</text>
  <text x="450" y="335" font-family="monospace" font-size="11">git merge --abort</text>
</svg>

---

## Sync Fork with Upstream

```bash
# Add upstream remote (one time)
git remote add upstream https://github.com/ORIGINAL/repo.git

# Sync fork with upstream
git fetch upstream
git checkout main
git merge upstream/main
git push origin main

# Alternative: rebase method
git fetch upstream
git checkout main
git rebase upstream/main
git push origin main --force-lease

# Sync all branches
git fetch upstream
git checkout main
git reset --hard upstream/main
git push origin main --force-lease
```

---

## Protected Branches

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="40" text-anchor="middle" font-size="24" font-weight="bold">Branch Protection Rules</text>
  <rect x="100" y="80" width="600" height="60" fill="#4CAF50" rx="5"/>
  <text x="400" y="105" text-anchor="middle" font-size="16" fill="white" font-weight="bold">Protected: main branch</text>
  <text x="400" y="125" text-anchor="middle" font-size="12" fill="white">No direct pushes allowed</text>
  <rect x="50" y="160" width="220" height="180" fill="#E8F5E9" stroke="#388E3C" stroke-width="2" rx="5"/>
  <text x="160" y="190" text-anchor="middle" font-size="14" font-weight="bold">Requirements</text>
  <text x="70" y="215" font-size="11">✓ Pull request required</text>
  <text x="70" y="235" font-size="11">✓ Code review approval</text>
  <text x="70" y="255" font-size="11">✓ Status checks pass</text>
  <text x="70" y="275" font-size="11">✓ Up-to-date with base</text>
  <text x="70" y="295" font-size="11">✓ Signed commits</text>
  <text x="70" y="315" font-size="11">✓ No admin override</text>
  <rect x="290" y="160" width="220" height="180" fill="#FFF3E0" stroke="#F57C00" stroke-width="2" rx="5"/>
  <text x="400" y="190" text-anchor="middle" font-size="14" font-weight="bold">Benefits</text>
  <text x="310" y="215" font-size="11">• Prevents accidents</text>
  <text x="310" y="235" font-size="11">• Enforces review</text>
  <text x="310" y="255" font-size="11">• Ensures CI passes</text>
  <text x="310" y="275" font-size="11">• Maintains quality</text>
  <text x="310" y="295" font-size="11">• Audit trail</text>
  <text x="310" y="315" font-size="11">• Team collaboration</text>
  <rect x="530" y="160" width="220" height="180" fill="#FFEBEE" stroke="#C62828" stroke-width="2" rx="5"/>
  <text x="640" y="190" text-anchor="middle" font-size="14" font-weight="bold">Restrictions</text>
  <text x="550" y="215" font-size="11">✗ No force push</text>
  <text x="550" y="235" font-size="11">✗ No deletion</text>
  <text x="550" y="255" font-size="11">✗ No direct commits</text>
  <text x="550" y="275" font-size="11">✗ No bypass reviews</text>
  <text x="550" y="295" font-size="11">✗ No unsigned commits</text>
  <text x="550" y="315" font-size="11">✗ No failed checks</text>
</svg>

---

## Tags and Releases

```bash
# Create lightweight tag
git tag v1.0.0

# Create annotated tag (recommended)
git tag -a v1.0.0 -m "Version 1.0.0 release"

# Tag specific commit
git tag -a v1.0.0 abc123 -m "Version 1.0.0"

# List tags
git tag
git tag -l "v1.*"  # Pattern matching

# Show tag details
git show v1.0.0

# Push tags to remote
git push origin v1.0.0      # Specific tag
git push origin --tags      # All tags
git push --follow-tags      # Annotated tags only

# Delete tag
git tag -d v1.0.0           # Local
git push origin :v1.0.0     # Remote
```

---

## Semantic Versioning

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="40" text-anchor="middle" font-size="24" font-weight="bold">Semantic Versioning (SemVer)</text>
  <rect x="200" y="80" width="400" height="100" fill="#F5F5F5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="400" y="120" text-anchor="middle" font-size="36" font-family="monospace">v2.1.3</text>
  <text x="310" y="160" text-anchor="middle" font-size="14">MAJOR</text>
  <text x="400" y="160" text-anchor="middle" font-size="14">MINOR</text>
  <text x="490" y="160" text-anchor="middle" font-size="14">PATCH</text>
  <line x1="350" y1="125" x2="350" y2="145" stroke="#666" stroke-width="1"/>
  <line x1="450" y1="125" x2="450" y2="145" stroke="#666" stroke-width="1"/>
  <rect x="50" y="200" width="220" height="140" fill="#FFEBEE" stroke="#C62828" stroke-width="2" rx="5"/>
  <text x="160" y="230" text-anchor="middle" font-size="14" font-weight="bold">MAJOR (v3.0.0)</text>
  <text x="70" y="255" font-size="11">Breaking changes</text>
  <text x="70" y="275" font-size="11">Incompatible API</text>
  <text x="70" y="295" font-size="11">Major rewrite</text>
  <text x="70" y="315" font-size="11">Example: v1.x → v2.0</text>
  <rect x="290" y="200" width="220" height="140" fill="#FFF3E0" stroke="#F57C00" stroke-width="2" rx="5"/>
  <text x="400" y="230" text-anchor="middle" font-size="14" font-weight="bold">MINOR (v2.2.0)</text>
  <text x="310" y="255" font-size="11">New features</text>
  <text x="310" y="275" font-size="11">Backwards compatible</text>
  <text x="310" y="295" font-size="11">Additions</text>
  <text x="310" y="315" font-size="11">Example: v2.1 → v2.2</text>
  <rect x="530" y="200" width="220" height="140" fill="#E8F5E9" stroke="#388E3C" stroke-width="2" rx="5"/>
  <text x="640" y="230" text-anchor="middle" font-size="14" font-weight="bold">PATCH (v2.1.4)</text>
  <text x="550" y="255" font-size="11">Bug fixes</text>
  <text x="550" y="275" font-size="11">Security patches</text>
  <text x="550" y="295" font-size="11">No new features</text>
  <text x="550" y="315" font-size="11">Example: v2.1.3 → v2.1.4</text>
</svg>

---

## GitHub/GitLab Releases

```bash
# Create release with GitHub CLI
gh release create v1.0.0 \
  --title "Version 1.0.0" \
  --notes "Release notes" \
  --target main

# Upload assets to release
gh release upload v1.0.0 dist/*

# Create draft release
gh release create v2.0.0 --draft

# Auto-generate release notes
gh release create v1.0.0 --generate-notes

# GitLab releases (via API or UI)
# Usually done through CI/CD pipeline
```

---

## Remote Housekeeping

```bash
# Remove stale remote-tracking branches
git remote prune origin

# Fetch and prune in one command
git fetch --prune

# See stale branches before pruning
git remote prune origin --dry-run

# Clean up all remotes
git fetch --all --prune

# Delete remote branch
git push origin --delete feature-branch
# or
git push origin :feature-branch

# Remove all remote-tracking branches
git branch -r | grep -v main | xargs -n 1 git push --delete origin
```

---

## Mirror Repositories

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="40" text-anchor="middle" font-size="24" font-weight="bold">Repository Mirroring</text>
  <circle cx="200" cy="200" r="40" fill="#24292E"/>
  <text x="200" y="205" text-anchor="middle" font-size="14" fill="white">GitHub</text>
  <circle cx="400" cy="200" r="40" fill="#4CAF50"/>
  <text x="400" y="205" text-anchor="middle" font-size="14" fill="white">Local</text>
  <circle cx="600" cy="200" r="40" fill="#FC6D26"/>
  <text x="600" y="205" text-anchor="middle" font-size="14" fill="white">GitLab</text>
  <path d="M 240 200 L 360 200" stroke="#333" stroke-width="2" marker-end="url(#arrow4)" marker-start="url(#arrow4)"/>
  <path d="M 440 200 L 560 200" stroke="#333" stroke-width="2" marker-end="url(#arrow4)" marker-start="url(#arrow4)"/>
  <text x="300" y="190" text-anchor="middle" font-size="11">fetch/push</text>
  <text x="500" y="190" text-anchor="middle" font-size="11">fetch/push</text>
  <rect x="150" y="280" width="500" height="80" fill="#F5F5F5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="400" y="305" text-anchor="middle" font-size="12" font-family="monospace">git clone --mirror https://github.com/user/repo.git</text>
  <text x="400" y="325" text-anchor="middle" font-size="12" font-family="monospace">cd repo.git</text>
  <text x="400" y="345" text-anchor="middle" font-size="12" font-family="monospace">git remote set-url --push origin https://gitlab.com/user/repo.git</text>
  <defs>
    <marker id="arrow4" markerWidth="10" markerHeight="10" refX="5" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Git Hooks for Remote Operations

```bash
# .git/hooks/pre-push
#!/bin/sh
# Prevent push to main branch
protected_branch='main'
current_branch=$(git symbolic-ref HEAD | sed -e 's,.*/\(.*\),\1,')

if [ $protected_branch = $current_branch ]; then
    echo "Direct push to main branch is not allowed"
    echo "Please create a pull request"
    exit 1
fi

# Run tests before push
npm test
if [ $? -ne 0 ]; then
    echo "Tests must pass before push"
    exit 1
fi
```

---

## Remote Performance Tips

```bash
# Shallow clone (faster for large repos)
git clone --depth 1 https://github.com/user/repo.git

# Clone specific branch only
git clone -b develop --single-branch https://github.com/user/repo.git

# Partial clone (Git 2.17+)
git clone --filter=blob:none https://github.com/user/repo.git

# Fetch only needed objects
git fetch --filter=tree:0 origin

# Bundle for offline transfer
git bundle create repo.bundle --all
# Transfer bundle file
git clone repo.bundle new-repo

# Use SSH connection multiplexing
# ~/.ssh/config
Host github.com
    ControlMaster auto
    ControlPath ~/.ssh/sockets/%r@%h-%p
    ControlPersist 600
```

---

## Submodules vs Subtrees

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="40" text-anchor="middle" font-size="24" font-weight="bold">Managing Dependencies</text>
  <rect x="50" y="80" width="350" height="280" fill="#E8F5E9" stroke="#388E3C" stroke-width="2" rx="5"/>
  <text x="225" y="110" text-anchor="middle" font-size="18" font-weight="bold">Git Submodules</text>
  <text x="70" y="140" font-size="12">✓ Reference to external repo</text>
  <text x="70" y="160" font-size="12">✓ Specific commit tracked</text>
  <text x="70" y="180" font-size="12">✓ Independent repository</text>
  <text x="70" y="200" font-size="12">✗ Complex workflow</text>
  <text x="70" y="220" font-size="12">✗ Extra steps to update</text>
  <rect x="70" y="240" width="310" height="40" fill="#81C784" rx="3"/>
  <text x="225" y="265" text-anchor="middle" font-size="11" fill="white" font-family="monospace">git submodule add URL path</text>
  <text x="225" y="305" text-anchor="middle" font-size="13" font-weight="bold">Use for:</text>
  <text x="70" y="325" font-size="11">• Vendor libraries</text>
  <text x="70" y="345" font-size="11">• Shared components</text>
  <rect x="420" y="80" width="330" height="280" fill="#E3F2FD" stroke="#1976D2" stroke-width="2" rx="5"/>
  <text x="585" y="110" text-anchor="middle" font-size="18" font-weight="bold">Git Subtrees</text>
  <text x="440" y="140" font-size="12">✓ Code merged into project</text>
  <text x="440" y="160" font-size="12">✓ No special commands</text>
  <text x="440" y="180" font-size="12">✓ Simple for users</text>
  <text x="440" y="200" font-size="12">✗ History mixed</text>
  <text x="440" y="220" font-size="12">✗ Larger repository</text>
  <rect x="440" y="240" width="290" height="40" fill="#64B5F6" rx="3"/>
  <text x="585" y="265" text-anchor="middle" font-size="11" fill="white" font-family="monospace">git subtree add --prefix=path URL</text>
  <text x="585" y="305" text-anchor="middle" font-size="13" font-weight="bold">Use for:</text>
  <text x="440" y="325" font-size="11">• Merged dependencies</text>
  <text x="440" y="345" font-size="11">• One-time imports</text>
</svg>

---

## Working with Submodules

```bash
# Add submodule
git submodule add https://github.com/lib/library.git libs/library

# Clone repo with submodules
git clone --recurse-submodules https://github.com/user/repo.git

# Initialize submodules after clone
git submodule init
git submodule update

# Update all submodules
git submodule update --remote --merge

# Remove submodule
git submodule deinit path/to/submodule
git rm path/to/submodule
rm -rf .git/modules/path/to/submodule
```

---

## CI/CD Integration

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="40" text-anchor="middle" font-size="24" font-weight="bold">Remote Triggers CI/CD</text>
  <circle cx="100" cy="200" r="30" fill="#4CAF50"/>
  <text x="100" y="205" text-anchor="middle" font-size="12" fill="white">Push</text>
  <path d="M 130 200 L 170 200" stroke="#333" stroke-width="2" marker-end="url(#arrow5)"/>
  <rect x="170" y="175" width="100" height="50" fill="#2196F3" rx="5"/>
  <text x="220" y="205" text-anchor="middle" font-size="12" fill="white">Webhook</text>
  <path d="M 270 200 L 310 200" stroke="#333" stroke-width="2" marker-end="url(#arrow5)"/>
  <rect x="310" y="175" width="100" height="50" fill="#FF9800" rx="5"/>
  <text x="360" y="205" text-anchor="middle" font-size="12" fill="white">CI Build</text>
  <path d="M 410 200 L 450 200" stroke="#333" stroke-width="2" marker-end="url(#arrow5)"/>
  <rect x="450" y="175" width="100" height="50" fill="#9C27B0" rx="5"/>
  <text x="500" y="205" text-anchor="middle" font-size="12" fill="white">Tests</text>
  <path d="M 550 200 L 590 200" stroke="#333" stroke-width="2" marker-end="url(#arrow5)"/>
  <rect x="590" y="175" width="100" height="50" fill="#F44336" rx="5"/>
  <text x="640" y="205" text-anchor="middle" font-size="12" fill="white">Deploy</text>
  <rect x="200" y="260" width="400" height="100" fill="#F5F5F5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="400" y="290" text-anchor="middle" font-size="14" font-weight="bold">Triggers:</text>
  <text x="220" y="315" font-size="12">• Push to branch</text>
  <text x="220" y="335" font-size="12">• Pull request</text>
  <text x="380" y="315" font-size="12">• Tag creation</text>
  <text x="380" y="335" font-size="12">• Schedule</text>
  <defs>
    <marker id="arrow5" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## GitHub Actions Example

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v2

    - name: Setup Node.js
      uses: actions/setup-node@v2
      with:
        node-version: '16'

    - name: Install dependencies
      run: npm ci

    - name: Run tests
      run: npm test

    - name: Build
      run: npm run build
```

---

## GitLab CI Example

```yaml
# .gitlab-ci.yml
stages:
  - test
  - build
  - deploy

variables:
  NODE_VERSION: "16"

test:
  stage: test
  image: node:${NODE_VERSION}
  script:
    - npm ci
    - npm test
  only:
    - merge_requests
    - main
    - develop

build:
  stage: build
  image: node:${NODE_VERSION}
  script:
    - npm ci
    - npm run build
  artifacts:
    paths:
      - dist/
  only:
    - main
```

---

## Remote Repository Security

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="40" text-anchor="middle" font-size="24" font-weight="bold">Security Best Practices</text>
  <rect x="50" y="80" width="350" height="120" fill="#FFEBEE" stroke="#C62828" stroke-width="2" rx="5"/>
  <text x="225" y="110" text-anchor="middle" font-size="16" font-weight="bold">Access Control</text>
  <text x="70" y="135" font-size="12">• Use SSH keys or tokens</text>
  <text x="70" y="155" font-size="12">• Enable 2FA</text>
  <text x="70" y="175" font-size="12">• Limit repository access</text>
  <rect x="420" y="80" width="330" height="120" fill="#FFF3E0" stroke="#F57C00" stroke-width="2" rx="5"/>
  <text x="585" y="110" text-anchor="middle" font-size="16" font-weight="bold">Sensitive Data</text>
  <text x="440" y="135" font-size="12">• Never commit secrets</text>
  <text x="440" y="155" font-size="12">• Use environment variables</text>
  <text x="440" y="175" font-size="12">• Scan for exposed keys</text>
  <rect x="50" y="220" width="350" height="120" fill="#E8F5E9" stroke="#388E3C" stroke-width="2" rx="5"/>
  <text x="225" y="250" text-anchor="middle" font-size="16" font-weight="bold">Code Integrity</text>
  <text x="70" y="275" font-size="12">• Sign commits with GPG</text>
  <text x="70" y="295" font-size="12">• Verify signatures</text>
  <text x="70" y="315" font-size="12">• Protected branches</text>
  <rect x="420" y="220" width="330" height="120" fill="#E3F2FD" stroke="#1976D2" stroke-width="2" rx="5"/>
  <text x="585" y="250" text-anchor="middle" font-size="16" font-weight="bold">Monitoring</text>
  <text x="440" y="275" font-size="12">• Audit logs</text>
  <text x="440" y="295" font-size="12">• Security alerts</text>
  <text x="440" y="315" font-size="12">• Dependency scanning</text>
</svg>

---

## Summary

## What We Learned

1. ✅ Understanding remote repositories
1. ✅ Working with multiple remotes
1. ✅ Push, pull, and fetch strategies
1. ✅ Collaboration workflows
1. ✅ Pull requests and code review
1. ✅ Conflict resolution
1. ✅ Tags and releases
1. ✅ Repository mirroring and security

---

## Key Takeaways

1. **Remotes are references** - Not the actual repository
1. **Fetch is safe, pull merges** - Fetch to review first
1. **Use branches for features** - Keep main stable
1. **Pull requests enable review** - Quality through collaboration
1. **Tags mark milestones** - Version your releases
1. **Multiple remotes are powerful** - Fork, upstream, backup
1. **Security matters** - Protect branches, sign commits, use SSH

---

## Practice Exercises

1. Set up a repository with multiple remotes
1. Create and merge a pull request
1. Resolve a merge conflict
1. Sync a fork with upstream
1. Create and push tags
1. Set up branch protection rules
1. Configure CI/CD for your repository
1. Mirror a repository between platforms

---

## Next Up: Branches

In the next session, we'll deep dive into:

1. Branch theory and internals
1. Creating and managing branches
1. Branching strategies
1. Merge vs rebase
1. Advanced branching workflows
1. Branch maintenance
1. Troubleshooting branch issues

---

## Remote Repositories Complete! 🎉

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="80" text-anchor="middle" font-size="32" font-weight="bold" fill="#4CAF50">Connected to the World!</text>
  <rect x="200" y="120" width="400" height="200" fill="#E8F5E9" stroke="#388E3C" stroke-width="3" rx="10"/>
  <text x="400" y="165" text-anchor="middle" font-size="20">You can now:</text>
  <text x="400" y="195" text-anchor="middle" font-size="16">• Share code globally</text>
  <text x="400" y="220" text-anchor="middle" font-size="16">• Collaborate with teams</text>
  <text x="400" y="245" text-anchor="middle" font-size="16">• Contribute to open source</text>
  <text x="400" y="270" text-anchor="middle" font-size="16">• Manage distributed workflows</text>
  <circle cx="250" cy="350" r="25" fill="#2196F3"/>
  <text x="250" y="357" text-anchor="middle" font-size="20">🌐</text>
  <circle cx="400" cy="350" r="25" fill="#FF9800"/>
  <text x="400" y="357" text-anchor="middle" font-size="20">🤝</text>
  <circle cx="550" cy="350" r="25" fill="#9C27B0"/>
  <text x="550" y="357" text-anchor="middle" font-size="20">🚀</text>
</svg>
