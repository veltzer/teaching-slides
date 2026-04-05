# Advanced Git Topics
---
## Git Internals
<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arr_internals" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#555"/>
    </marker>
  </defs>
  <!-- Commit object -->
  <rect x="10" y="10" width="120" height="55" fill="#fff3e0" stroke="#e65100" stroke-width="2" rx="6"/>
  <text x="70" y="28" text-anchor="middle" font-size="11" font-weight="bold" fill="#e65100">Commit</text>
  <text x="70" y="42" text-anchor="middle" font-size="9" fill="#555">a1b2c3d</text>
  <text x="70" y="56" text-anchor="middle" font-size="9" fill="#555">tree: f4e5d6a</text>
  <!-- Tree object -->
  <rect x="200" y="10" width="120" height="55" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2" rx="6"/>
  <text x="260" y="28" text-anchor="middle" font-size="11" font-weight="bold" fill="#2e7d32">Tree</text>
  <text x="260" y="42" text-anchor="middle" font-size="9" fill="#555">f4e5d6a</text>
  <text x="260" y="56" text-anchor="middle" font-size="9" fill="#555">entries: 3</text>
  <!-- Arrow: Commit -> Tree -->
  <line x1="130" y1="37" x2="198" y2="37" stroke="#555" stroke-width="2" marker-end="url(#arr_internals)"/>
  <!-- Blob 1 -->
  <rect x="390" y="5" width="110" height="40" fill="#e3f2fd" stroke="#1565c0" stroke-width="2" rx="6"/>
  <text x="445" y="20" text-anchor="middle" font-size="10" font-weight="bold" fill="#1565c0">Blob</text>
  <text x="445" y="34" text-anchor="middle" font-size="9" fill="#555">README.md</text>
  <!-- Blob 2 -->
  <rect x="390" y="55" width="110" height="40" fill="#e3f2fd" stroke="#1565c0" stroke-width="2" rx="6"/>
  <text x="445" y="70" text-anchor="middle" font-size="10" font-weight="bold" fill="#1565c0">Blob</text>
  <text x="445" y="84" text-anchor="middle" font-size="9" fill="#555">main.py</text>
  <!-- Subtree -->
  <rect x="390" y="105" width="110" height="40" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2" rx="6"/>
  <text x="445" y="120" text-anchor="middle" font-size="10" font-weight="bold" fill="#2e7d32">Tree</text>
  <text x="445" y="134" text-anchor="middle" font-size="9" fill="#555">src/</text>
  <!-- Arrows: Tree -> children -->
  <line x1="320" y1="30" x2="388" y2="25" stroke="#555" stroke-width="1.5" marker-end="url(#arr_internals)"/>
  <line x1="320" y1="40" x2="388" y2="72" stroke="#555" stroke-width="1.5" marker-end="url(#arr_internals)"/>
  <line x1="320" y1="50" x2="388" y2="122" stroke="#555" stroke-width="1.5" marker-end="url(#arr_internals)"/>
  <!-- Nested blob -->
  <rect x="520" y="130" width="70" height="35" fill="#e3f2fd" stroke="#1565c0" stroke-width="1.5" rx="5"/>
  <text x="555" y="145" text-anchor="middle" font-size="9" font-weight="bold" fill="#1565c0">Blob</text>
  <text x="555" y="158" text-anchor="middle" font-size="8" fill="#555">util.py</text>
  <line x1="500" y1="130" x2="518" y2="145" stroke="#555" stroke-width="1.5" marker-end="url(#arr_internals)"/>
  <!-- Parent commit -->
  <rect x="10" y="120" width="120" height="45" fill="#fff3e0" stroke="#e65100" stroke-width="1.5" rx="6"/>
  <text x="70" y="138" text-anchor="middle" font-size="10" font-weight="bold" fill="#e65100">Parent Commit</text>
  <text x="70" y="155" text-anchor="middle" font-size="9" fill="#555">9f8e7d6</text>
  <line x1="70" y1="65" x2="70" y2="118" stroke="#555" stroke-width="1.5" marker-end="url(#arr_internals)"/>
  <!-- Legend -->
  <text x="200" y="185" font-size="10" fill="#777">Git Object Model: Commit → Tree → Blobs/Trees</text>
</svg>

---
## Object Store Structure
- SHA-1 hashing
- Content addressing
- Object types
- Storage optimization
---
## Digital Signatures
- GPG signing
- Commit verification
- Tag signing
- Security implications
---
## Core Ideas
<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arr_core" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#888"/>
    </marker>
  </defs>
  <!-- Unifying theme bar -->
  <rect x="30" y="88" width="540" height="24" fill="#f5f5f5" stroke="#bbb" stroke-width="1" rx="12"/>
  <text x="300" y="105" text-anchor="middle" font-size="10" fill="#777" font-style="italic">Unified by immutable, hash-based object storage</text>
  <!-- Snapshots not Diffs -->
  <rect x="30" y="15" width="160" height="60" fill="#e3f2fd" stroke="#1565c0" stroke-width="2" rx="8"/>
  <text x="110" y="35" text-anchor="middle" font-size="11" font-weight="bold" fill="#1565c0">Snapshots</text>
  <text x="110" y="50" text-anchor="middle" font-size="10" fill="#555">not Diffs</text>
  <text x="110" y="65" text-anchor="middle" font-size="9" fill="#888">Full state per commit</text>
  <!-- Camera icon -->
  <rect x="50" y="22" width="12" height="9" fill="none" stroke="#1565c0" stroke-width="1.5" rx="2"/>
  <circle cx="56" cy="27" r="3" fill="none" stroke="#1565c0" stroke-width="1"/>
  <!-- Content-Addressable Store -->
  <rect x="220" y="15" width="160" height="60" fill="#f3e5f5" stroke="#7b1fa2" stroke-width="2" rx="8"/>
  <text x="300" y="35" text-anchor="middle" font-size="11" font-weight="bold" fill="#7b1fa2">Content-Addressable</text>
  <text x="300" y="50" text-anchor="middle" font-size="10" fill="#555">Store</text>
  <text x="300" y="65" text-anchor="middle" font-size="9" fill="#888">SHA-1 identifies data</text>
  <!-- Hash icon -->
  <text x="237" y="35" font-size="13" fill="#7b1fa2">#</text>
  <!-- DAG -->
  <rect x="410" y="15" width="160" height="60" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2" rx="8"/>
  <text x="490" y="35" text-anchor="middle" font-size="11" font-weight="bold" fill="#2e7d32">Directed Acyclic</text>
  <text x="490" y="50" text-anchor="middle" font-size="10" fill="#555">Graph</text>
  <text x="490" y="65" text-anchor="middle" font-size="9" fill="#888">History as a DAG</text>
  <!-- DAG mini-icon -->
  <circle cx="428" cy="28" r="4" fill="#2e7d32"/>
  <circle cx="440" cy="22" r="4" fill="#2e7d32"/>
  <circle cx="440" cy="34" r="4" fill="#2e7d32"/>
  <line x1="432" y1="27" x2="437" y2="23" stroke="#2e7d32" stroke-width="1.5"/>
  <line x1="432" y1="29" x2="437" y2="33" stroke="#2e7d32" stroke-width="1.5"/>
  <!-- Connecting lines to theme bar -->
  <line x1="110" y1="75" x2="110" y2="88" stroke="#1565c0" stroke-width="1.5" stroke-dasharray="4,2"/>
  <line x1="300" y1="75" x2="300" y2="88" stroke="#7b1fa2" stroke-width="1.5" stroke-dasharray="4,2"/>
  <line x1="490" y1="75" x2="490" y2="88" stroke="#2e7d32" stroke-width="1.5" stroke-dasharray="4,2"/>
  <!-- Detail row -->
  <text x="110" y="135" text-anchor="middle" font-size="9" fill="#1565c0">Each commit stores</text>
  <text x="110" y="147" text-anchor="middle" font-size="9" fill="#1565c0">a complete tree</text>
  <text x="300" y="135" text-anchor="middle" font-size="9" fill="#7b1fa2">Same content =</text>
  <text x="300" y="147" text-anchor="middle" font-size="9" fill="#7b1fa2">same hash always</text>
  <text x="490" y="135" text-anchor="middle" font-size="9" fill="#2e7d32">Commits point to</text>
  <text x="490" y="147" text-anchor="middle" font-size="9" fill="#2e7d32">parent commits</text>
  <!-- Arrows between concepts -->
  <line x1="190" y1="45" x2="218" y2="45" stroke="#888" stroke-width="1.5" marker-end="url(#arr_core)"/>
  <line x1="380" y1="45" x2="408" y2="45" stroke="#888" stroke-width="1.5" marker-end="url(#arr_core)"/>
</svg>

---
## SHA Uniqueness
- Global uniqueness
- Content verification
- History integrity
- Collision handling
---
## Git Directory Structure
- Objects directory
- Refs directory
- Config files
- Hooks directory
---
## Working with Worktrees
- Multiple workspaces
- Separate branches
- Resource sharing
- Management commands
---
## Creating Worktrees
```bash
git worktree add ../path branch
git worktree list
git worktree remove path
```
---
## Git Hooks
- Pre-commit hooks
- Post-commit hooks
- Pre-receive hooks
- Custom scripts
---
## Hook Types
<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arr_hooks" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#555"/>
    </marker>
  </defs>
  <!-- Timeline arrow -->
  <line x1="30" y1="100" x2="570" y2="100" stroke="#ccc" stroke-width="2" marker-end="url(#arr_hooks)"/>
  <text x="300" y="196" text-anchor="middle" font-size="10" fill="#999">Workflow Timeline: commit → push → receive</text>
  <!-- Client-side label -->
  <rect x="30" y="8" width="250" height="20" fill="#e3f2fd" stroke="none" rx="4"/>
  <text x="155" y="22" text-anchor="middle" font-size="11" font-weight="bold" fill="#1565c0">Client-side Hooks</text>
  <!-- Client hooks -->
  <rect x="35" y="38" width="100" height="48" fill="#e3f2fd" stroke="#1565c0" stroke-width="1.5" rx="5"/>
  <text x="85" y="55" text-anchor="middle" font-size="10" font-weight="bold" fill="#1565c0">pre-commit</text>
  <text x="85" y="68" text-anchor="middle" font-size="8" fill="#555">lint, test, format</text>
  <circle cx="85" cy="100" r="4" fill="#1565c0"/>
  <rect x="145" y="38" width="100" height="48" fill="#e3f2fd" stroke="#1565c0" stroke-width="1.5" rx="5"/>
  <text x="195" y="52" text-anchor="middle" font-size="9" font-weight="bold" fill="#1565c0">prepare-</text>
  <text x="195" y="63" text-anchor="middle" font-size="9" font-weight="bold" fill="#1565c0">commit-msg</text>
  <text x="195" y="76" text-anchor="middle" font-size="8" fill="#555">template msg</text>
  <circle cx="195" cy="100" r="4" fill="#1565c0"/>
  <!-- commit-msg -->
  <rect x="255" y="110" width="90" height="40" fill="#f3e5f5" stroke="#7b1fa2" stroke-width="1.5" rx="5"/>
  <text x="300" y="127" text-anchor="middle" font-size="10" font-weight="bold" fill="#7b1fa2">commit-msg</text>
  <text x="300" y="140" text-anchor="middle" font-size="8" fill="#555">validate msg</text>
  <circle cx="300" cy="100" r="4" fill="#7b1fa2"/>
  <!-- post-commit -->
  <rect x="355" y="110" width="90" height="40" fill="#fff3e0" stroke="#e65100" stroke-width="1.5" rx="5"/>
  <text x="400" y="127" text-anchor="middle" font-size="10" font-weight="bold" fill="#e65100">post-commit</text>
  <text x="400" y="140" text-anchor="middle" font-size="8" fill="#555">notify</text>
  <circle cx="400" cy="100" r="4" fill="#e65100"/>
  <!-- Server-side label -->
  <rect x="450" y="8" width="140" height="20" fill="#e8f5e9" stroke="none" rx="4"/>
  <text x="520" y="22" text-anchor="middle" font-size="11" font-weight="bold" fill="#2e7d32">Server-side Hooks</text>
  <!-- Server hooks -->
  <rect x="455" y="38" width="85" height="48" fill="#e8f5e9" stroke="#2e7d32" stroke-width="1.5" rx="5"/>
  <text x="497" y="55" text-anchor="middle" font-size="10" font-weight="bold" fill="#2e7d32">pre-receive</text>
  <text x="497" y="68" text-anchor="middle" font-size="8" fill="#555">policy check</text>
  <circle cx="497" cy="100" r="4" fill="#2e7d32"/>
  <rect x="455" y="110" width="85" height="40" fill="#e8f5e9" stroke="#2e7d32" stroke-width="1.5" rx="5"/>
  <text x="497" y="127" text-anchor="middle" font-size="10" font-weight="bold" fill="#2e7d32">update</text>
  <text x="497" y="140" text-anchor="middle" font-size="8" fill="#555">per-ref check</text>
  <rect x="455" y="155" width="85" height="35" fill="#e8f5e9" stroke="#2e7d32" stroke-width="1.5" rx="5"/>
  <text x="497" y="172" text-anchor="middle" font-size="10" font-weight="bold" fill="#2e7d32">post-receive</text>
  <text x="497" y="184" text-anchor="middle" font-size="8" fill="#555">CI/CD trigger</text>
  <!-- Divider -->
  <line x1="445" y1="5" x2="445" y2="190" stroke="#bbb" stroke-width="1" stroke-dasharray="5,3"/>
</svg>

---
## Custom Hook Development
- Script creation
- Permission setting
- Error handling
- Integration testing
---
## Searching History
- Complex patterns
- Content matching
- Author tracking
- Time-based search
---
## Advanced Search Commands
- git grep
- git log --grep
- git log -S
- git log -G
---
## Git Attributes
- File handling
- Line endings
- Diffing binary
- Content filters
---
## Clean and Smudge Filters
- Content modification
- File transformation
- Custom processing
- Pipeline integration
---
## Git Refs
- Branch refs
- Tag refs
- Remote refs
- Special refs
---
## Ref Management
<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arr_refs" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#555"/>
    </marker>
  </defs>
  <!-- HEAD -->
  <rect x="15" y="25" width="75" height="32" fill="#fff3e0" stroke="#e65100" stroke-width="2" rx="6"/>
  <text x="52" y="46" text-anchor="middle" font-size="12" font-weight="bold" fill="#e65100">HEAD</text>
  <!-- Arrow HEAD -> refs/heads/main -->
  <line x1="90" y1="41" x2="138" y2="41" stroke="#e65100" stroke-width="2" marker-end="url(#arr_refs)"/>
  <!-- refs/heads/main -->
  <rect x="140" y="20" width="140" height="42" fill="#e3f2fd" stroke="#1565c0" stroke-width="2" rx="6"/>
  <text x="210" y="37" text-anchor="middle" font-size="10" font-weight="bold" fill="#1565c0">refs/heads/main</text>
  <text x="210" y="52" text-anchor="middle" font-size="9" fill="#555">a1b2c3d4e5f6</text>
  <!-- Arrow to commit -->
  <line x1="280" y1="41" x2="368" y2="41" stroke="#1565c0" stroke-width="2" marker-end="url(#arr_refs)"/>
  <!-- Commit SHA -->
  <rect x="370" y="20" width="120" height="42" fill="#f5f5f5" stroke="#555" stroke-width="2" rx="6"/>
  <text x="430" y="37" text-anchor="middle" font-size="10" font-weight="bold" fill="#333">Commit</text>
  <text x="430" y="52" text-anchor="middle" font-size="9" fill="#555">a1b2c3d4e5f6</text>
  <!-- refs/tags/v1.0 -->
  <rect x="140" y="75" width="140" height="42" fill="#f3e5f5" stroke="#7b1fa2" stroke-width="2" rx="6"/>
  <text x="210" y="92" text-anchor="middle" font-size="10" font-weight="bold" fill="#7b1fa2">refs/tags/v1.0</text>
  <text x="210" y="107" text-anchor="middle" font-size="9" fill="#555">7a8b9c0d1e2f</text>
  <line x1="280" y1="96" x2="368" y2="55" stroke="#7b1fa2" stroke-width="1.5" stroke-dasharray="5,3" marker-end="url(#arr_refs)"/>
  <!-- refs/remotes/origin/main -->
  <rect x="140" y="130" width="140" height="42" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2" rx="6"/>
  <text x="210" y="147" text-anchor="middle" font-size="9" font-weight="bold" fill="#2e7d32">refs/remotes/</text>
  <text x="210" y="161" text-anchor="middle" font-size="9" font-weight="bold" fill="#2e7d32">origin/main</text>
  <line x1="280" y1="151" x2="368" y2="55" stroke="#2e7d32" stroke-width="1.5" stroke-dasharray="5,3" marker-end="url(#arr_refs)"/>
  <!-- .git/refs directory tree -->
  <rect x="500" y="70" width="90" height="120" fill="#fafafa" stroke="#bbb" stroke-width="1" rx="4"/>
  <text x="545" y="86" text-anchor="middle" font-size="9" font-weight="bold" fill="#333">.git/refs/</text>
  <text x="520" y="102" font-size="9" fill="#1565c0">heads/</text>
  <text x="530" y="115" font-size="8" fill="#555">main</text>
  <text x="520" y="132" font-size="9" fill="#7b1fa2">tags/</text>
  <text x="530" y="145" font-size="8" fill="#555">v1.0</text>
  <text x="520" y="162" font-size="9" fill="#2e7d32">remotes/</text>
  <text x="530" y="175" font-size="8" fill="#555">origin/main</text>
</svg>

---
## Git Namespaces
- Reference namespaces
- Branch organization
- Tag categorization
- Remote separation
---
## Advanced Branching
- Orphan branches
- Upstream tracking
- Remote branches
- Branch policies
---
## Repository Maintenance
- Garbage collection
- Pack optimization
- Reference pruning
- Storage cleanup
---
## Performance Tuning
- Object packing
- Delta compression
- Cache settings
- Network optimization
---
## Git Protocol
- Transfer protocols
- Network efficiency
- Security aspects
- Custom protocols
---
## Repository Migration
- History preservation
- Large repositories
- Author mapping
- Branch handling
---
## Git LFS
- Large file handling
- Binary management
- Storage optimization
- Bandwidth reduction
---
## Custom Commands
- Script integration
- Command creation
- Workflow automation
- Tool extension
---
## Security Hardening
- Access control
- Audit logging
- Secret management
- Vulnerability scanning
---
## Advanced Conflicts
- Complex merges
- Recursive resolution
- Custom strategies
- Tool integration
---
## Git Internals Deep Dive
- Object database
- Reference system
- Index structure
- Pack files
---
## Performance Monitoring
- Resource usage
- Operation timing
- Network metrics
- Storage analysis
---
## Debugging Git
- Trace settings
- Debug output
- Error analysis
- Problem solving
