# Git Branches
---
## Why We Need Branches
- Parallel development
- Feature isolation
- Experimentation
- Release management
---
## Branch Theory
<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowBT" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <!-- main branch -->
  <circle cx="80" cy="130" r="18" fill="#e8f5e9" stroke="#333" stroke-width="2"/>
  <text x="80" y="134" text-anchor="middle" font-size="10" font-family="sans-serif">C1</text>
  <circle cx="170" cy="130" r="18" fill="#e8f5e9" stroke="#333" stroke-width="2"/>
  <text x="170" y="134" text-anchor="middle" font-size="10" font-family="sans-serif">C2</text>
  <circle cx="260" cy="130" r="18" fill="#e8f5e9" stroke="#333" stroke-width="2"/>
  <text x="260" y="134" text-anchor="middle" font-size="10" font-family="sans-serif">C3</text>
  <circle cx="350" cy="130" r="18" fill="#e8f5e9" stroke="#333" stroke-width="2"/>
  <text x="350" y="134" text-anchor="middle" font-size="10" font-family="sans-serif">C4</text>
  <line x1="98" y1="130" x2="150" y2="130" stroke="#333" stroke-width="2" marker-end="url(#arrowBT)"/>
  <line x1="188" y1="130" x2="240" y2="130" stroke="#333" stroke-width="2" marker-end="url(#arrowBT)"/>
  <line x1="278" y1="130" x2="330" y2="130" stroke="#333" stroke-width="2" marker-end="url(#arrowBT)"/>
  <!-- feature branch -->
  <line x1="272" y1="114" x2="320" y2="75" stroke="#9c27b0" stroke-width="2" marker-end="url(#arrowBT)"/>
  <circle cx="340" cy="60" r="18" fill="#f3e5f5" stroke="#9c27b0" stroke-width="2"/>
  <text x="340" y="64" text-anchor="middle" font-size="10" font-family="sans-serif">F1</text>
  <circle cx="430" cy="60" r="18" fill="#f3e5f5" stroke="#9c27b0" stroke-width="2"/>
  <text x="430" y="64" text-anchor="middle" font-size="10" font-family="sans-serif">F2</text>
  <line x1="358" y1="60" x2="410" y2="60" stroke="#9c27b0" stroke-width="2" marker-end="url(#arrowBT)"/>
  <!-- labels -->
  <text x="350" y="170" text-anchor="middle" font-size="12" font-family="sans-serif" fill="#2e7d32" font-weight="bold">main</text>
  <text x="430" y="40" text-anchor="middle" font-size="12" font-family="sans-serif" fill="#9c27b0" font-weight="bold">feature</text>
  <!-- HEAD pointer -->
  <rect x="470" y="45" width="50" height="22" rx="4" fill="#fff9c4" stroke="#f57f17" stroke-width="1.5"/>
  <text x="495" y="60" text-anchor="middle" font-size="11" font-family="sans-serif" font-weight="bold" fill="#f57f17">HEAD</text>
  <line x1="470" y1="58" x2="450" y2="60" stroke="#f57f17" stroke-width="1.5" marker-end="url(#arrowBT)"/>
</svg>

---
## Local Branching Benefits
- Fast and lightweight
- Private workspace
- Easy experimentation
- Quick context switching
---
## Creating Branches
- git branch command
- Naming conventions
- Branch from specific commits
- Branch best practices
---
## Branch Commands
```bash
git branch feature_name
git checkout -b new_feature
git switch -c another_feature
```
---
## Branch Descriptions
- Adding branch descriptions
- Documentation purposes
- Team communication
- git branch --edit-description
---
## Renaming Branches
- Local branch renaming
- Remote branch considerations
- git branch -m
- Updating remote references
---
## Working on Branches
- Switching between branches
- Tracking changes
- Commit management
- Branch isolation
---
## Branch Navigation
<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowBN" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <!-- main branch -->
  <circle cx="80" cy="140" r="16" fill="#e8f5e9" stroke="#333" stroke-width="2"/>
  <text x="80" y="144" text-anchor="middle" font-size="10" font-family="sans-serif">C1</text>
  <circle cx="160" cy="140" r="16" fill="#e8f5e9" stroke="#333" stroke-width="2"/>
  <text x="160" y="144" text-anchor="middle" font-size="10" font-family="sans-serif">C2</text>
  <circle cx="240" cy="140" r="16" fill="#e8f5e9" stroke="#333" stroke-width="2"/>
  <text x="240" y="144" text-anchor="middle" font-size="10" font-family="sans-serif">C3</text>
  <line x1="96" y1="140" x2="142" y2="140" stroke="#333" stroke-width="2" marker-end="url(#arrowBN)"/>
  <line x1="176" y1="140" x2="222" y2="140" stroke="#333" stroke-width="2" marker-end="url(#arrowBN)"/>
  <text x="160" y="175" text-anchor="middle" font-size="12" font-family="sans-serif" fill="#2e7d32" font-weight="bold">main</text>
  <!-- feature branch -->
  <circle cx="80" cy="60" r="16" fill="#f3e5f5" stroke="#9c27b0" stroke-width="2"/>
  <text x="80" y="64" text-anchor="middle" font-size="10" font-family="sans-serif">F1</text>
  <circle cx="160" cy="60" r="16" fill="#f3e5f5" stroke="#9c27b0" stroke-width="2"/>
  <text x="160" y="64" text-anchor="middle" font-size="10" font-family="sans-serif">F2</text>
  <circle cx="240" cy="60" r="16" fill="#f3e5f5" stroke="#9c27b0" stroke-width="2"/>
  <text x="240" y="64" text-anchor="middle" font-size="10" font-family="sans-serif">F3</text>
  <line x1="96" y1="60" x2="142" y2="60" stroke="#9c27b0" stroke-width="2" marker-end="url(#arrowBN)"/>
  <line x1="176" y1="60" x2="222" y2="60" stroke="#9c27b0" stroke-width="2" marker-end="url(#arrowBN)"/>
  <text x="160" y="40" text-anchor="middle" font-size="12" font-family="sans-serif" fill="#9c27b0" font-weight="bold">feature</text>
  <!-- HEAD pointer switching -->
  <rect x="370" y="48" width="50" height="22" rx="4" fill="#fff9c4" stroke="#f57f17" stroke-width="1.5"/>
  <text x="395" y="63" text-anchor="middle" font-size="11" font-family="sans-serif" font-weight="bold" fill="#f57f17">HEAD</text>
  <!-- arrow to feature -->
  <line x1="370" y1="60" x2="258" y2="60" stroke="#f57f17" stroke-width="1.5" stroke-dasharray="5,3" marker-end="url(#arrowBN)"/>
  <!-- arrow to main (dimmed) -->
  <line x1="395" y1="70" x2="258" y2="135" stroke="#bbb" stroke-width="1.5" stroke-dasharray="5,3" marker-end="url(#arrowBN)"/>
  <!-- switch labels -->
  <text x="440" y="100" text-anchor="start" font-size="10" font-family="sans-serif" fill="#555">git switch feature</text>
  <text x="440" y="118" text-anchor="start" font-size="10" font-family="sans-serif" fill="#999">git switch main</text>
  <text x="425" y="100" text-anchor="end" font-size="13" fill="#f57f17">&#x2190;</text>
  <text x="425" y="118" text-anchor="end" font-size="13" fill="#bbb">&#x2190;</text>
</svg>

---
## Git Checkout vs Switch
- Traditional checkout
- Modern switch command
- When to use each
- Feature comparison
---
## Branch Visualization
- git log --graph
- git show-branch
- GUI tools
- Understanding history
---
## Branch Cleanup
- Deleting local branches
- Remote branch cleanup
- git branch -d
- git branch -D
---
## The Git Reflog
- Safety net for branches
- Recovery operations
- Historical reference
- Temporary references
---
## Branch Types
- Feature branches
- Release branches
- Hotfix branches
- Integration branches
---
## Feature Branch Workflow
<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowFW" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
    <marker id="arrowFWp" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#9c27b0"/>
    </marker>
  </defs>
  <!-- main branch commits -->
  <circle cx="50" cy="140" r="15" fill="#e8f5e9" stroke="#333" stroke-width="2"/>
  <text x="50" y="144" text-anchor="middle" font-size="10" font-family="sans-serif">C1</text>
  <circle cx="130" cy="140" r="15" fill="#e8f5e9" stroke="#333" stroke-width="2"/>
  <text x="130" y="144" text-anchor="middle" font-size="10" font-family="sans-serif">C2</text>
  <circle cx="210" cy="140" r="15" fill="#e8f5e9" stroke="#333" stroke-width="2"/>
  <text x="210" y="144" text-anchor="middle" font-size="10" font-family="sans-serif">C3</text>
  <line x1="65" y1="140" x2="113" y2="140" stroke="#333" stroke-width="2" marker-end="url(#arrowFW)"/>
  <line x1="145" y1="140" x2="193" y2="140" stroke="#333" stroke-width="2" marker-end="url(#arrowFW)"/>
  <!-- step 1: create branch -->
  <line x1="220" y1="126" x2="265" y2="80" stroke="#9c27b0" stroke-width="2" marker-end="url(#arrowFWp)"/>
  <text x="225" y="95" text-anchor="start" font-size="10" font-family="sans-serif" fill="#9c27b0" font-style="italic">1. Create</text>
  <!-- feature branch commits -->
  <circle cx="285" cy="65" r="15" fill="#f3e5f5" stroke="#9c27b0" stroke-width="2"/>
  <text x="285" y="69" text-anchor="middle" font-size="10" font-family="sans-serif">F1</text>
  <circle cx="365" cy="65" r="15" fill="#f3e5f5" stroke="#9c27b0" stroke-width="2"/>
  <text x="365" y="69" text-anchor="middle" font-size="10" font-family="sans-serif">F2</text>
  <line x1="300" y1="65" x2="348" y2="65" stroke="#9c27b0" stroke-width="2" marker-end="url(#arrowFWp)"/>
  <text x="325" y="50" text-anchor="middle" font-size="10" font-family="sans-serif" fill="#9c27b0" font-style="italic">2. Develop</text>
  <!-- main continues -->
  <line x1="225" y1="140" x2="433" y2="140" stroke="#333" stroke-width="2" stroke-dasharray="6,4"/>
  <!-- merge commit -->
  <circle cx="450" cy="140" r="15" fill="#e8f5e9" stroke="#2e7d32" stroke-width="3"/>
  <text x="450" y="144" text-anchor="middle" font-size="10" font-family="sans-serif">M</text>
  <line x1="377" y1="76" x2="438" y2="128" stroke="#9c27b0" stroke-width="2" marker-end="url(#arrowFW)"/>
  <text x="430" y="100" text-anchor="end" font-size="10" font-family="sans-serif" fill="#2e7d32" font-style="italic">3. Merge/PR</text>
  <!-- labels -->
  <text x="130" y="175" text-anchor="middle" font-size="12" font-family="sans-serif" fill="#2e7d32" font-weight="bold">main</text>
  <text x="325" y="38" text-anchor="middle" font-size="12" font-family="sans-serif" fill="#9c27b0" font-weight="bold">feature</text>
</svg>

---
## Release Branches
- Version management
- Stabilization phase
- Bugfix handling
- Maintenance support
---
## Hotfix Branches
- Emergency fixes
- Production issues
- Quick deployment
- Multiple target branches
---
## Integration Branches
- Combining features
- Testing integration
- Conflict resolution
- Quality assurance
---
## Branch Organization
- Hierarchical structure
- Naming conventions
- Lifecycle management
- Team coordination
---
## Branch Policies
- Protection rules
- Review requirements
- Automation checks
- Access control
---
## Branch Strategies
- GitFlow
- Trunk-based development
- GitHub Flow
- Custom workflows
---
## GitFlow Model
<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowGF" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto">
      <path d="M0,0 L0,6 L7,3 z" fill="#666"/>
    </marker>
  </defs>
  <!-- main branch (bottom) -->
  <line x1="80" y1="175" x2="560" y2="175" stroke="#2e7d32" stroke-width="3"/>
  <circle cx="80" cy="175" r="6" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <circle cx="280" cy="175" r="6" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <circle cx="560" cy="175" r="6" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="30" y="179" text-anchor="middle" font-size="11" font-family="sans-serif" fill="#2e7d32" font-weight="bold">main</text>
  <!-- develop branch (middle) -->
  <line x1="80" y1="120" x2="560" y2="120" stroke="#1565c0" stroke-width="3"/>
  <circle cx="80" cy="120" r="6" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <circle cx="160" cy="120" r="6" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <circle cx="320" cy="120" r="6" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <circle cx="440" cy="120" r="6" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <circle cx="560" cy="120" r="6" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="30" y="124" text-anchor="middle" font-size="11" font-family="sans-serif" fill="#1565c0" font-weight="bold">dev</text>
  <!-- feature branch -->
  <line x1="160" y1="120" x2="180" y2="70" stroke="#9c27b0" stroke-width="2"/>
  <line x1="180" y1="70" x2="280" y2="70" stroke="#9c27b0" stroke-width="2"/>
  <line x1="280" y1="70" x2="320" y2="120" stroke="#9c27b0" stroke-width="2" marker-end="url(#arrowGF)"/>
  <circle cx="180" cy="70" r="5" fill="#f3e5f5" stroke="#9c27b0" stroke-width="1.5"/>
  <circle cx="230" cy="70" r="5" fill="#f3e5f5" stroke="#9c27b0" stroke-width="1.5"/>
  <circle cx="280" cy="70" r="5" fill="#f3e5f5" stroke="#9c27b0" stroke-width="1.5"/>
  <text x="230" y="60" text-anchor="middle" font-size="10" font-family="sans-serif" fill="#9c27b0">feature</text>
  <!-- release branch -->
  <line x1="320" y1="120" x2="340" y2="70" stroke="#e65100" stroke-width="2"/>
  <line x1="340" y1="70" x2="420" y2="70" stroke="#e65100" stroke-width="2"/>
  <line x1="420" y1="70" x2="440" y2="120" stroke="#e65100" stroke-width="2" marker-end="url(#arrowGF)"/>
  <line x1="420" y1="70" x2="450" y2="175" stroke="#e65100" stroke-width="1.5" stroke-dasharray="4,3" marker-end="url(#arrowGF)"/>
  <circle cx="340" cy="70" r="5" fill="#fff3e0" stroke="#e65100" stroke-width="1.5"/>
  <circle cx="380" cy="70" r="5" fill="#fff3e0" stroke="#e65100" stroke-width="1.5"/>
  <circle cx="420" cy="70" r="5" fill="#fff3e0" stroke="#e65100" stroke-width="1.5"/>
  <text x="380" y="60" text-anchor="middle" font-size="10" font-family="sans-serif" fill="#e65100">release</text>
  <!-- hotfix branch -->
  <line x1="280" y1="175" x2="300" y2="28" stroke="#c62828" stroke-width="2"/>
  <line x1="300" y1="28" x2="360" y2="28" stroke="#c62828" stroke-width="2"/>
  <line x1="360" y1="28" x2="380" y2="120" stroke="#c62828" stroke-width="1.5" stroke-dasharray="4,3" marker-end="url(#arrowGF)"/>
  <line x1="360" y1="28" x2="370" y2="175" stroke="#c62828" stroke-width="1.5" stroke-dasharray="4,3" marker-end="url(#arrowGF)"/>
  <circle cx="300" cy="28" r="5" fill="#ffebee" stroke="#c62828" stroke-width="1.5"/>
  <circle cx="360" cy="28" r="5" fill="#ffebee" stroke="#c62828" stroke-width="1.5"/>
  <text x="330" y="20" text-anchor="middle" font-size="10" font-family="sans-serif" fill="#c62828">hotfix</text>
</svg>

---
## Trunk-Based Development
- Single main branch
- Short-lived feature branches
- Frequent integration
- Continuous delivery
---
## Working with Tags
- Annotated tags
- Lightweight tags
- Version marking
- Release management
---
## Branch Performance
- Repository size
- History complexity
- Network impact
- Optimization tips
---
## Common Patterns
- Branch per feature
- Branch per release
- Branch per environment
- Branch per team
---
## Automation
- Branch creation
- Integration testing
- Deployment flows
- Cleanup routines
---
## Best Practices
- Clear naming
- Regular cleanup
- Documentation
- Team communication
---
## Troubleshooting
- Lost branches
- Merge conflicts
- Integration issues
- Recovery procedures
---
## Advanced Topics
- Branch filtering
- Branch restrictions
- Custom attributes
- Branch hooks
