# Merging in Git
---
## Merge Overview
![0](../../../out/mermaid/marp/courses/git/06_merging.md/0.png)

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
![1](../../../out/mermaid/marp/courses/git/06_merging.md/1.png)

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
![2](../../../out/mermaid/marp/courses/git/06_merging.md/2.png)

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
![3](../../../out/mermaid/marp/courses/git/06_merging.md/3.png)

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
---
## Next Steps
## Git Workflows
- Workflow patterns
- Team collaboration
- Process integration
- Best practices
