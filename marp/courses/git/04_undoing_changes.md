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
<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <!-- Title -->
  <text x="300" y="20" text-anchor="middle" font-size="13" font-weight="bold" fill="#333">Danger Level: Low → High</text>
  <!-- Danger gradient bar -->
  <defs>
    <linearGradient id="dangerGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#4caf50"/>
      <stop offset="50%" style="stop-color:#ff9800"/>
      <stop offset="100%" style="stop-color:#f44336"/>
    </linearGradient>
  </defs>
  <rect x="30" y="160" width="540" height="10" rx="5" fill="url(#dangerGrad)" opacity="0.7"/>
  <text x="30" y="190" font-size="11" fill="#4caf50">Safe</text>
  <text x="545" y="190" font-size="11" fill="#f44336" text-anchor="end">Destructive</text>
  <!-- commit --amend -->
  <rect x="30" y="40" width="120" height="105" fill="#e8f5e9" stroke="#4caf50" stroke-width="2" rx="8"/>
  <text x="90" y="62" text-anchor="middle" font-size="12" font-weight="bold" fill="#2e7d32">commit</text>
  <text x="90" y="77" text-anchor="middle" font-size="12" font-weight="bold" fill="#2e7d32">--amend</text>
  <text x="90" y="97" text-anchor="middle" font-size="11" fill="#555">Fixes last</text>
  <text x="90" y="111" text-anchor="middle" font-size="11" fill="#555">commit only</text>
  <text x="90" y="135" text-anchor="middle" font-size="11" fill="#4caf50">● Low risk</text>
  <!-- rebase -i -->
  <rect x="170" y="40" width="120" height="105" fill="#e3f2fd" stroke="#1976d2" stroke-width="2" rx="8"/>
  <text x="230" y="62" text-anchor="middle" font-size="12" font-weight="bold" fill="#1565c0">rebase -i</text>
  <text x="230" y="87" text-anchor="middle" font-size="11" fill="#555">Rewrite multiple</text>
  <text x="230" y="101" text-anchor="middle" font-size="11" fill="#555">past commits</text>
  <text x="230" y="135" text-anchor="middle" font-size="11" fill="#1976d2">● Medium risk</text>
  <!-- filter-branch -->
  <rect x="310" y="40" width="120" height="105" fill="#fff3e0" stroke="#f57c00" stroke-width="2" rx="8"/>
  <text x="370" y="62" text-anchor="middle" font-size="12" font-weight="bold" fill="#e65100">filter-branch</text>
  <text x="370" y="87" text-anchor="middle" font-size="11" fill="#555">Rewrites entire</text>
  <text x="370" y="101" text-anchor="middle" font-size="11" fill="#555">repo history</text>
  <text x="370" y="135" text-anchor="middle" font-size="11" fill="#f57c00">● High risk</text>
  <!-- reset -->
  <rect x="450" y="40" width="120" height="105" fill="#ffebee" stroke="#d32f2f" stroke-width="2" rx="8"/>
  <text x="510" y="62" text-anchor="middle" font-size="12" font-weight="bold" fill="#b71c1c">reset --hard</text>
  <text x="510" y="87" text-anchor="middle" font-size="11" fill="#555">Discards commits</text>
  <text x="510" y="101" text-anchor="middle" font-size="11" fill="#555">and changes</text>
  <text x="510" y="135" text-anchor="middle" font-size="11" fill="#d32f2f">● Destructive</text>
</svg>

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
<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowReset" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <!-- Commit chain -->
  <rect x="30" y="15" width="70" height="35" fill="#e3f2fd" stroke="#1976d2" stroke-width="2" rx="5"/>
  <text x="65" y="37" text-anchor="middle" font-size="12" font-weight="bold" fill="#1565c0">C1</text>
  <line x1="100" y1="32" x2="130" y2="32" stroke="#333" stroke-width="2" marker-end="url(#arrowReset)"/>
  <rect x="135" y="15" width="70" height="35" fill="#e3f2fd" stroke="#1976d2" stroke-width="2" rx="5"/>
  <text x="170" y="37" text-anchor="middle" font-size="12" font-weight="bold" fill="#1565c0">C2</text>
  <line x1="205" y1="32" x2="235" y2="32" stroke="#333" stroke-width="2" marker-end="url(#arrowReset)"/>
  <rect x="240" y="15" width="70" height="35" fill="#e3f2fd" stroke="#1976d2" stroke-width="2" rx="5"/>
  <text x="275" y="37" text-anchor="middle" font-size="12" font-weight="bold" fill="#1565c0">C3</text>
  <text x="275" y="8" text-anchor="middle" font-size="11" fill="#d32f2f" font-weight="bold">HEAD</text>
  <!-- Reset target label -->
  <text x="400" y="20" text-anchor="middle" font-size="12" font-weight="bold" fill="#333">git reset C1</text>
  <!-- --soft row -->
  <rect x="340" y="35" width="250" height="40" fill="#e8f5e9" stroke="#4caf50" stroke-width="2" rx="6"/>
  <text x="365" y="52" font-size="12" font-weight="bold" fill="#2e7d32">--soft</text>
  <text x="430" y="52" font-size="11" fill="#555">Staged: C2+C3</text>
  <text x="430" y="67" font-size="11" fill="#555">Working dir: C2+C3</text>
  <!-- --mixed row -->
  <rect x="340" y="85" width="250" height="40" fill="#fff3e0" stroke="#f57c00" stroke-width="2" rx="6"/>
  <text x="365" y="102" font-size="12" font-weight="bold" fill="#e65100">--mixed</text>
  <text x="435" y="102" font-size="11" fill="#555">Staged: empty</text>
  <text x="435" y="117" font-size="11" fill="#555">Working dir: C2+C3</text>
  <!-- --hard row -->
  <rect x="340" y="135" width="250" height="40" fill="#ffebee" stroke="#d32f2f" stroke-width="2" rx="6"/>
  <text x="365" y="152" font-size="12" font-weight="bold" fill="#b71c1c">--hard</text>
  <text x="430" y="152" font-size="11" fill="#555">Staged: empty</text>
  <text x="430" y="167" font-size="11" fill="#555">Working dir: empty</text>
  <!-- Arrows from commit chain to each mode -->
  <line x1="275" y1="50" x2="338" y2="55" stroke="#4caf50" stroke-width="1.5" stroke-dasharray="4,3" marker-end="url(#arrowReset)"/>
  <line x1="275" y1="50" x2="338" y2="105" stroke="#f57c00" stroke-width="1.5" stroke-dasharray="4,3" marker-end="url(#arrowReset)"/>
  <line x1="275" y1="50" x2="338" y2="155" stroke="#d32f2f" stroke-width="1.5" stroke-dasharray="4,3" marker-end="url(#arrowReset)"/>
  <!-- Summary labels -->
  <text x="65" y="75" text-anchor="middle" font-size="11" fill="#888">keeps all</text>
  <text x="65" y="115" text-anchor="middle" font-size="11" fill="#888">keeps working</text>
  <text x="65" y="155" text-anchor="middle" font-size="11" fill="#888">discards all</text>
  <!-- Connecting lines from labels -->
  <line x1="110" y1="72" x2="338" y2="55" stroke="#4caf50" stroke-width="1" opacity="0.4"/>
  <line x1="120" y1="112" x2="338" y2="105" stroke="#f57c00" stroke-width="1" opacity="0.4"/>
  <line x1="110" y1="152" x2="338" y2="155" stroke="#d32f2f" stroke-width="1" opacity="0.4"/>
</svg>

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
<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowSplit" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <!-- BEFORE label -->
  <text x="140" y="18" text-anchor="middle" font-size="13" font-weight="bold" fill="#333">Before</text>
  <!-- Before: single large commit -->
  <rect x="55" y="30" width="170" height="55" fill="#f3e5f5" stroke="#7b1fa2" stroke-width="2" rx="8"/>
  <text x="140" y="52" text-anchor="middle" font-size="13" font-weight="bold" fill="#7b1fa2">Commit "ABC"</text>
  <text x="140" y="72" text-anchor="middle" font-size="11" fill="#555">3 unrelated changes</text>
  <!-- Arrow down with rebase -i edit label -->
  <line x1="140" y1="88" x2="140" y2="115" stroke="#333" stroke-width="2" marker-end="url(#arrowSplit)"/>
  <text x="200" y="107" font-size="11" font-style="italic" fill="#7b1fa2">rebase -i → edit</text>
  <!-- AFTER label -->
  <text x="300" y="140" text-anchor="middle" font-size="13" font-weight="bold" fill="#333">After</text>
  <!-- After: three small commits in a chain -->
  <rect x="30" y="150" width="100" height="40" fill="#e8f5e9" stroke="#4caf50" stroke-width="2" rx="6"/>
  <text x="80" y="175" text-anchor="middle" font-size="12" font-weight="bold" fill="#2e7d32">A</text>
  <line x1="130" y1="170" x2="160" y2="170" stroke="#333" stroke-width="2" marker-end="url(#arrowSplit)"/>
  <rect x="165" y="150" width="100" height="40" fill="#e3f2fd" stroke="#1976d2" stroke-width="2" rx="6"/>
  <text x="215" y="175" text-anchor="middle" font-size="12" font-weight="bold" fill="#1565c0">B</text>
  <line x1="265" y1="170" x2="295" y2="170" stroke="#333" stroke-width="2" marker-end="url(#arrowSplit)"/>
  <rect x="300" y="150" width="100" height="40" fill="#fff3e0" stroke="#f57c00" stroke-width="2" rx="6"/>
  <text x="350" y="175" text-anchor="middle" font-size="12" font-weight="bold" fill="#e65100">C</text>
  <!-- Steps on the right side -->
  <text x="440" y="40" font-size="11" fill="#555">1. git rebase -i HEAD~N</text>
  <text x="440" y="58" font-size="11" fill="#555">2. Mark commit as "edit"</text>
  <text x="440" y="76" font-size="11" fill="#555">3. git reset HEAD~1</text>
  <text x="440" y="94" font-size="11" fill="#555">4. git add + commit (A)</text>
  <text x="440" y="112" font-size="11" fill="#555">5. git add + commit (B)</text>
  <text x="440" y="130" font-size="11" fill="#555">6. git add + commit (C)</text>
  <text x="440" y="148" font-size="11" fill="#555">7. git rebase --continue</text>
</svg>

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
