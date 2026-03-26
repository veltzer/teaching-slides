# Merging in Git
---
## Merge Overview
<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="75" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="250" y="75" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="450" y="75" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="105" text-anchor="middle" font-size="12">Node 1</text>
  <text x="300" y="105" text-anchor="middle" font-size="12">Node 2</text>
  <text x="500" y="105" text-anchor="middle" font-size="12">Node 3</text>
  <line x1="150" y1="100" x2="250" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd0_06_merging)"/>
  <line x1="350" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd0_06_merging)"/>
  <defs>
    <marker id="arrowd0_06_merging" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
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
  <rect x="50" y="75" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="250" y="75" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="450" y="75" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="105" text-anchor="middle" font-size="12">Node 1</text>
  <text x="300" y="105" text-anchor="middle" font-size="12">Node 2</text>
  <text x="500" y="105" text-anchor="middle" font-size="12">Node 3</text>
  <line x1="150" y1="100" x2="250" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd1_06_merging)"/>
  <line x1="350" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd1_06_merging)"/>
  <defs>
    <marker id="arrowd1_06_merging" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
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
  <rect x="50" y="75" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="250" y="75" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="450" y="75" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="105" text-anchor="middle" font-size="12">Node 1</text>
  <text x="300" y="105" text-anchor="middle" font-size="12">Node 2</text>
  <text x="500" y="105" text-anchor="middle" font-size="12">Node 3</text>
  <line x1="150" y1="100" x2="250" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd2_06_merging)"/>
  <line x1="350" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd2_06_merging)"/>
  <defs>
    <marker id="arrowd2_06_merging" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
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
  <rect x="50" y="75" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="250" y="75" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="450" y="75" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="105" text-anchor="middle" font-size="12">Node 1</text>
  <text x="300" y="105" text-anchor="middle" font-size="12">Node 2</text>
  <text x="500" y="105" text-anchor="middle" font-size="12">Node 3</text>
  <line x1="150" y1="100" x2="250" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd3_06_merging)"/>
  <line x1="350" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd3_06_merging)"/>
  <defs>
    <marker id="arrowd3_06_merging" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
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
