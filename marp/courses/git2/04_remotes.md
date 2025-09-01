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

## First Half Summary

## What We've Learned So Far

1. ✅ Understanding remote repositories
1. ✅ Clone vs init with remote
1. ✅ Remote naming conventions
1. ✅ Fetch vs pull differences
1. ✅ Push strategies and safety
1. ✅ Working with multiple remotes
1. ✅ HTTPS vs SSH authentication
1. ✅ Bare repositories for sharing

## Coming Up Next

1. Advanced remote operations
1. Collaboration workflows
1. Pull requests
1. Conflict resolution
1. Tags and releases
