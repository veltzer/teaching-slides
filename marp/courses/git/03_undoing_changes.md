# Undoing Changes in Git
---
## Why History Matters
- Git history is a valuable resource
- Helps understand code evolution
- Crucial for debugging
- Important for collaboration
---
## The Golden Rule
- Never rewrite published history
- Changes affect all team members
- Can cause synchronization issues
- May lead to lost work
---
## History Rewriting Commands
![0](../../../out/mermaid/marp/courses/git/03_undoing_changes.md/0.png)

---
## Git Commit Amend
- Modifies the last commit
- Changes commit message
- Adds forgotten files
- Creates new SHA-1
---
## Using Amend
```bash
# Add forgotten file
git add forgotten-file.txt
git commit --amend
```
---
## Hard Reset
- Moves HEAD and branch pointer
- Discards commits and changes
- Cannot be undone
- Use with extreme caution
---
## Reset Variations
![1](../../../out/mermaid/marp/courses/git/03_undoing_changes.md/1.png)

---
## Git Revert
- Creates new commit
- Undoes previous changes
- Safe for published history
- Maintains commit history
---
## Revert vs Reset
- Revert: new commit, preserves history
- Reset: removes commits, modifies history
- Revert: safe for shared branches
- Reset: unsafe for shared branches
---
## Using Git Rebase
- Reapplies commits on new base
- Modifies commit history
- Powerful but dangerous
- Interactive mode available
---
## Interactive Rebase
- Reorder commits
- Edit commit messages
- Combine commits
- Split commits
---
## Cherry-pick Operations
- Copy specific commits
- Apply to different branches
- Selective history copying
- Maintains original authorship
---
## Cherry vs Cherry-pick
- Cherry: list commits
- Cherry-pick: apply commits
- Different use cases
- Common workflow tools
---
## Splitting Past Changes
![2](../../../out/mermaid/marp/courses/git/03_undoing_changes.md/2.png)

---
## Using Interactive Rebase
1. Start with git rebase -i
1. Mark commits for editing
1. Make necessary changes
1. Continue rebase
---
## Extreme Undoing
- History tail removal
- Multiple commit rewrites
- Branch reconstruction
- Emergency recovery
---
## Cutting History
- Remove recent commits
- Keep or discard changes
- Branch implications
- Recovery options
---
## Multiple Commit Rewrites
- Filter-branch usage
- BFG Repo Cleaner
- Large scale changes
- Performance considerations
---
## Recovery Tools
- Git reflog
- Dangling commits
- Lost and found
- Backup strategies
---
## Safe Operations
- Working directory backups
- Temporary branches
- Testing changes
- Verification steps
---
## Dangerous Operations
- Force push
- Branch deletion
- Hard reset
- Filter-branch
---
## Best Practices
- Create backups
- Use safe commands
- Test changes
- Document operations
---
## Common Scenarios
- Fixing commit messages
- Removing sensitive data
- Combining commits
- Splitting commits
---
## Working with Teams
- Communication importance
- Coordination strategies
- Branch protection
- Code review process
---
## Emergency Procedures
- Data recovery
- Branch restoration
- Commit recovery
- Remote repository fixes
---
## Prevention Strategies
- Regular backups
- Clear workflows
- Team communication
- Safety checks
---
## Documentation
- Recording changes
- Change notifications
- Team updates
- Process documentation
---
## Tools and Helpers
- Git GUI tools
- Script automation
- Safety checks
- Visualization aids
---
## Branch Management
- Temporary branches
- Feature branches
- Recovery branches
- Cleanup procedures
