# Merging in Git
---
## Merge Overview
<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrMO" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <!-- Main branch -->
  <circle cx="60" cy="80" r="18" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <text x="60" y="84" text-anchor="middle" font-size="11" font-family="sans-serif">C1</text>
  <circle cx="150" cy="80" r="18" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <text x="150" y="84" text-anchor="middle" font-size="11" font-family="sans-serif">C2</text>
  <circle cx="350" cy="80" r="18" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <text x="350" y="84" text-anchor="middle" font-size="11" font-family="sans-serif">C5</text>
  <circle cx="470" cy="80" r="22" fill="#fff3e0" stroke="#e65100" stroke-width="2.5"/>
  <text x="470" y="76" text-anchor="middle" font-size="10" font-weight="bold" font-family="sans-serif">Merge</text>
  <text x="470" y="89" text-anchor="middle" font-size="10" font-weight="bold" font-family="sans-serif">Commit</text>
  <!-- Feature branch -->
  <circle cx="210" cy="155" r="18" fill="#f3e5f5" stroke="#333" stroke-width="2"/>
  <text x="210" y="159" text-anchor="middle" font-size="11" font-family="sans-serif">C3</text>
  <circle cx="310" cy="155" r="18" fill="#f3e5f5" stroke="#333" stroke-width="2"/>
  <text x="310" y="159" text-anchor="middle" font-size="11" font-family="sans-serif">C4</text>
  <!-- Arrows main branch -->
  <line x1="78" y1="80" x2="130" y2="80" stroke="#333" stroke-width="2" marker-end="url(#arrMO)"/>
  <line x1="168" y1="80" x2="330" y2="80" stroke="#333" stroke-width="2" marker-end="url(#arrMO)"/>
  <line x1="368" y1="80" x2="446" y2="80" stroke="#333" stroke-width="2" marker-end="url(#arrMO)"/>
  <!-- Branch off -->
  <line x1="162" y1="96" x2="196" y2="141" stroke="#333" stroke-width="2" marker-end="url(#arrMO)"/>
  <!-- Feature arrows -->
  <line x1="228" y1="155" x2="290" y2="155" stroke="#333" stroke-width="2" marker-end="url(#arrMO)"/>
  <!-- Merge back -->
  <line x1="324" y1="141" x2="456" y2="96" stroke="#333" stroke-width="2" marker-end="url(#arrMO)"/>
  <!-- Labels -->
  <text x="60" y="45" text-anchor="middle" font-size="12" font-family="sans-serif" fill="#1565c0" font-weight="bold">main</text>
  <text x="260" y="190" text-anchor="middle" font-size="12" font-family="sans-serif" fill="#7b1fa2" font-weight="bold">feature</text>
</svg>

---
## Types of Merges
- Fast-forward merge
- Recursive merge
- Octopus merge
- Squash merge
---
## Git Fetch
- Download remote changes
- Update remote tracking
- No automatic merging
- Safe operation
---
## Git Pull
- Fetch + merge combination
- Update local branches
- Automatic merging
- Potential conflicts
---
## Git Rebase
- Linear history
- Branch reorganization
- Cleaner project history
- Workflow considerations
---
## Fast-Forward Merges
<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrFF" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <!-- BEFORE label -->
  <text x="130" y="20" text-anchor="middle" font-size="13" font-family="sans-serif" font-weight="bold" fill="#333">Before</text>
  <line x1="270" y1="10" x2="270" y2="190" stroke="#999" stroke-width="1" stroke-dasharray="5,5"/>
  <!-- AFTER label -->
  <text x="430" y="20" text-anchor="middle" font-size="13" font-family="sans-serif" font-weight="bold" fill="#333">After</text>
  <!-- Before: commits -->
  <circle cx="50" cy="70" r="18" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <text x="50" y="74" text-anchor="middle" font-size="11" font-family="sans-serif">C1</text>
  <circle cx="130" cy="70" r="18" fill="#e8f5e9" stroke="#333" stroke-width="2"/>
  <text x="130" y="74" text-anchor="middle" font-size="11" font-family="sans-serif">C2</text>
  <circle cx="210" cy="70" r="18" fill="#e8f5e9" stroke="#333" stroke-width="2"/>
  <text x="210" y="74" text-anchor="middle" font-size="11" font-family="sans-serif">C3</text>
  <line x1="68" y1="70" x2="110" y2="70" stroke="#333" stroke-width="2" marker-end="url(#arrFF)"/>
  <line x1="148" y1="70" x2="190" y2="70" stroke="#333" stroke-width="2" marker-end="url(#arrFF)"/>
  <!-- Before: branch pointers -->
  <text x="50" y="115" text-anchor="middle" font-size="11" font-family="sans-serif" fill="#1565c0" font-weight="bold">main</text>
  <line x1="50" y1="108" x2="50" y2="90" stroke="#1565c0" stroke-width="1.5" marker-end="url(#arrFF)"/>
  <text x="210" y="115" text-anchor="middle" font-size="11" font-family="sans-serif" fill="#2e7d32" font-weight="bold">feature</text>
  <line x1="210" y1="108" x2="210" y2="90" stroke="#2e7d32" stroke-width="1.5" marker-end="url(#arrFF)"/>
  <!-- After: commits -->
  <circle cx="340" cy="70" r="18" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <text x="340" y="74" text-anchor="middle" font-size="11" font-family="sans-serif">C1</text>
  <circle cx="420" cy="70" r="18" fill="#e8f5e9" stroke="#333" stroke-width="2"/>
  <text x="420" y="74" text-anchor="middle" font-size="11" font-family="sans-serif">C2</text>
  <circle cx="500" cy="70" r="18" fill="#e8f5e9" stroke="#333" stroke-width="2"/>
  <text x="500" y="74" text-anchor="middle" font-size="11" font-family="sans-serif">C3</text>
  <line x1="358" y1="70" x2="400" y2="70" stroke="#333" stroke-width="2" marker-end="url(#arrFF)"/>
  <line x1="438" y1="70" x2="480" y2="70" stroke="#333" stroke-width="2" marker-end="url(#arrFF)"/>
  <!-- After: both pointers at C3 -->
  <text x="475" y="130" text-anchor="middle" font-size="11" font-family="sans-serif" fill="#1565c0" font-weight="bold">main</text>
  <line x1="490" y1="123" x2="498" y2="90" stroke="#1565c0" stroke-width="1.5" marker-end="url(#arrFF)"/>
  <text x="530" y="115" text-anchor="middle" font-size="11" font-family="sans-serif" fill="#2e7d32" font-weight="bold">feature</text>
  <line x1="520" y1="108" x2="512" y2="90" stroke="#2e7d32" stroke-width="1.5" marker-end="url(#arrFF)"/>
  <!-- Explanation -->
  <text x="430" y="170" text-anchor="middle" font-size="10" font-family="sans-serif" fill="#555">main pointer moves forward</text>
  <text x="430" y="185" text-anchor="middle" font-size="10" font-family="sans-serif" fill="#555">No new merge commit created</text>
</svg>

---
## When to Fast-Forward
- Linear history possible
- No divergent changes
- Simple integration
- Clean history desired
---
## No Fast-Forward Option
- Create merge commit
- Document integration
- Branch history tracking
- git merge --no-ff
---
## Merge Strategies
- Recursive (default)
- Resolve
- Octopus
- Ours/Theirs
---
## Recursive Strategy
<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrRS" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
    <marker id="arrRSd" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#999"/>
    </marker>
  </defs>
  <!-- Common ancestor (Base) -->
  <circle cx="100" cy="100" r="20" fill="#fff3e0" stroke="#e65100" stroke-width="2"/>
  <text x="100" y="104" text-anchor="middle" font-size="11" font-family="sans-serif" font-weight="bold">Base</text>
  <text x="100" y="140" text-anchor="middle" font-size="10" font-family="sans-serif" fill="#e65100">Common Ancestor</text>
  <!-- Ours (main tip) -->
  <circle cx="300" cy="40" r="20" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="300" y="44" text-anchor="middle" font-size="11" font-family="sans-serif" font-weight="bold">Ours</text>
  <text x="300" y="18" text-anchor="middle" font-size="10" font-family="sans-serif" fill="#1565c0">main tip</text>
  <!-- Theirs (feature tip) -->
  <circle cx="300" cy="160" r="20" fill="#f3e5f5" stroke="#7b1fa2" stroke-width="2"/>
  <text x="300" y="164" text-anchor="middle" font-size="11" font-family="sans-serif" font-weight="bold">Theirs</text>
  <text x="300" y="195" text-anchor="middle" font-size="10" font-family="sans-serif" fill="#7b1fa2">feature tip</text>
  <!-- Merge commit -->
  <circle cx="480" cy="100" r="22" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2.5"/>
  <text x="480" y="96" text-anchor="middle" font-size="10" font-weight="bold" font-family="sans-serif">Merge</text>
  <text x="480" y="109" text-anchor="middle" font-size="10" font-weight="bold" font-family="sans-serif">Commit</text>
  <!-- Arrows: Base to Ours and Theirs -->
  <line x1="118" y1="88" x2="278" y2="46" stroke="#999" stroke-width="1.5" stroke-dasharray="5,3" marker-end="url(#arrRSd)"/>
  <line x1="118" y1="112" x2="278" y2="154" stroke="#999" stroke-width="1.5" stroke-dasharray="5,3" marker-end="url(#arrRSd)"/>
  <!-- Arrows: Ours and Theirs to Merge -->
  <line x1="320" y1="46" x2="456" y2="90" stroke="#333" stroke-width="2" marker-end="url(#arrRS)"/>
  <line x1="320" y1="154" x2="456" y2="110" stroke="#333" stroke-width="2" marker-end="url(#arrRS)"/>
  <!-- 3-way label -->
  <text x="190" y="75" text-anchor="middle" font-size="10" font-family="sans-serif" fill="#666" transform="rotate(-16,190,75)">diverged</text>
  <text x="190" y="130" text-anchor="middle" font-size="10" font-family="sans-serif" fill="#666" transform="rotate(16,190,130)">diverged</text>
</svg>

---
## Resolve Strategy
- Two heads merging
- Simple conflicts
- Three-way merge
- Historical algorithm
---
## Octopus Strategy
- Multiple branches
- No complex conflicts
- Release integration
- Feature combining
---
## Merge Conflicts
- Concurrent changes
- Same file modifications
- Manual resolution needed
- Conflict markers
---
## Conflict Resolution
```bash
<<<<<<< HEAD
Your changes
=======
Their changes
>>>>>>> feature_branch
```
---
## Using Merge Tools
- Visual diff tools
- Three-way comparison
- Resolution assistance
- Tool configuration
---
## Popular Merge Tools
- Meld
- KDiff3
- P4Merge
- Visual Studio Code
---
## Automated Merging
- Clean merges
- No conflicts
- Automatic resolution
- Integration testing
---
## Manual Merging
- Complex conflicts
- Business logic
- Code review
- Testing requirements
---
## Merge Commit Messages
- Clear descriptions
- Referenced issues
- Change documentation
- Team communication
---
## Abort and Reset
- git merge --abort
- Conflict recovery
- Clean workspace
- Start over
---
## Cherry Picking
<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrCP" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
    <marker id="arrCPr" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#e65100"/>
    </marker>
  </defs>
  <!-- Main branch -->
  <text x="20" y="54" font-size="12" font-family="sans-serif" fill="#1565c0" font-weight="bold">main</text>
  <circle cx="80" cy="50" r="18" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <text x="80" y="54" text-anchor="middle" font-size="11" font-family="sans-serif">M1</text>
  <circle cx="160" cy="50" r="18" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <text x="160" y="54" text-anchor="middle" font-size="11" font-family="sans-serif">M2</text>
  <line x1="98" y1="50" x2="140" y2="50" stroke="#333" stroke-width="2" marker-end="url(#arrCP)"/>
  <!-- Cherry-picked commit on main -->
  <circle cx="280" cy="50" r="18" fill="#fff3e0" stroke="#e65100" stroke-width="2.5"/>
  <text x="280" y="54" text-anchor="middle" font-size="12" font-family="sans-serif" font-weight="bold">C'</text>
  <line x1="178" y1="50" x2="260" y2="50" stroke="#333" stroke-width="2" marker-end="url(#arrCP)"/>
  <text x="280" y="28" text-anchor="middle" font-size="10" font-family="sans-serif" fill="#e65100">cherry-picked</text>
  <!-- Feature branch -->
  <text x="20" y="154" font-size="12" font-family="sans-serif" fill="#7b1fa2" font-weight="bold">feature</text>
  <circle cx="120" cy="150" r="18" fill="#f3e5f5" stroke="#333" stroke-width="2"/>
  <text x="120" y="154" text-anchor="middle" font-size="11" font-family="sans-serif">A</text>
  <circle cx="220" cy="150" r="18" fill="#f3e5f5" stroke="#333" stroke-width="2"/>
  <text x="220" y="154" text-anchor="middle" font-size="11" font-family="sans-serif">B</text>
  <circle cx="320" cy="150" r="18" fill="#fff3e0" stroke="#e65100" stroke-width="2.5"/>
  <text x="320" y="154" text-anchor="middle" font-size="12" font-family="sans-serif" font-weight="bold">C</text>
  <circle cx="420" cy="150" r="18" fill="#f3e5f5" stroke="#333" stroke-width="2"/>
  <text x="420" y="154" text-anchor="middle" font-size="11" font-family="sans-serif">D</text>
  <line x1="138" y1="150" x2="200" y2="150" stroke="#333" stroke-width="2" marker-end="url(#arrCP)"/>
  <line x1="238" y1="150" x2="300" y2="150" stroke="#333" stroke-width="2" marker-end="url(#arrCP)"/>
  <line x1="338" y1="150" x2="400" y2="150" stroke="#333" stroke-width="2" marker-end="url(#arrCP)"/>
  <!-- Cherry-pick arrow -->
  <path d="M 320 132 C 320 90, 280 90, 280 70" stroke="#e65100" stroke-width="2.5" fill="none" stroke-dasharray="6,3" marker-end="url(#arrCPr)"/>
  <text x="370" y="100" font-size="10" font-family="sans-serif" fill="#e65100" font-style="italic">git cherry-pick</text>
</svg>

---
## When to Cherry Pick
- Single commit needs
- Hotfix application
- Selective features
- Cross-branch updates
---
## Rebase vs Merge
- Linear history
- Branch organization
- Team workflows
- Project requirements
---
## Rebase Benefits
- Clean history
- Linear progression
- Easy to follow
- Better readability
---
## Rebase Drawbacks
- History rewriting
- Team coordination
- Complex conflicts
- Safety concerns
---
## Best Practices
- Regular merges
- Small changes
- Clear communication
- Testing strategy
---
## Common Problems
- Merge conflicts
- Lost changes
- Integration issues
- Branch confusion
---
## Advanced Merging
- Squash merges
- Interactive rebase
- Custom strategies
- Complex workflows
---
## Team Workflows
- Feature integration
- Release merging
- Hotfix applying
- Version control
---
## Continuous Integration
- Automated testing
- Merge verification
- Build validation
- Deployment checks
