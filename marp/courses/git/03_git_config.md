# Git Configuration
---
## Configuration Levels
<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <!-- Bottom layer: System -->
  <rect x="50" y="140" width="500" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="162" text-anchor="middle" font-size="13" font-weight="bold">System</text>
  <text x="300" y="178" text-anchor="middle" font-size="11" fill="#555">/etc/gitconfig</text>
  <!-- Middle layer: User -->
  <rect x="120" y="80" width="360" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="102" text-anchor="middle" font-size="13" font-weight="bold">User</text>
  <text x="300" y="118" text-anchor="middle" font-size="11" fill="#555">~/.gitconfig</text>
  <!-- Top layer: Repository -->
  <rect x="195" y="20" width="210" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="42" text-anchor="middle" font-size="13" font-weight="bold">Repository</text>
  <text x="300" y="58" text-anchor="middle" font-size="11" fill="#555">.git/config</text>
  <!-- Priority arrow on the right -->
  <defs>
    <marker id="arrowd0_03_git_config" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <line x1="570" y1="170" x2="570" y2="35" stroke="#333" stroke-width="2" marker-end="url(#arrowd0_03_git_config)"/>
  <text x="585" y="105" text-anchor="start" font-size="11" fill="#333" transform="rotate(-90,585,105)">Higher priority</text>
</svg>

---
## Configuration Files
- System-wide: /etc/gitconfig
- User-specific: ~/.gitconfig
- Repository: .git/config
- Command line overrides
---
## Basic Configuration
- User information setup
- Core settings
- Default behaviors
- Editor preferences
---
## User Identity
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```
---
## Core Settings
- Default branch name
- Line ending handling
- File mode tracking
- Credential storage
---
## Command Configuration
- Default command behavior
- Command aliases
- Output formatting
- Color settings
---
## Editor Setup
- Choosing default editor
- Commit message template
- Diff tool configuration
- Merge tool setup
---
## Alias Creation
- Creating command shortcuts
- Complex command combinations
- Custom git commands
- Productivity improvements
---
## Common Aliases
```bash
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.st status
```
---
## Color Configuration
- Enable/disable colors
- Customize color schemes
- Branch colors
- Diff colors
---
## Ignoring Files
- Creating .gitignore
- Global ignore patterns
- Local ignore patterns
- Tracking empty directories
---
## Gitignore Patterns
- Specific file patterns
- Directory patterns
- Negation patterns
- Comments in .gitignore
---
## Pattern Examples
```gitignore
*.log
build/
!important.log
node_modules/
```
---
## Pattern Matching
- Glob patterns
- Directory indicators
- Negation rules
- Pattern ordering
---
## Global Gitignore
- System-wide ignore rules
- User-specific ignores
- Core.excludesFile setting
- Common ignore patterns
---
## Whitespace Handling
- Configuring whitespace rules
- Auto-correction settings
- Line ending management
- Space vs tabs
---
## Credential Handling
- Credential storage
- Cache settings
- Helper programs
- Security considerations
---
## Signing Configuration
- GPG key setup
- Signing commits
- Signing tags
- Verification settings
---
## Remote Configuration
- Remote URL settings
- Push/pull behavior
- Fetch settings
- Branch tracking
---
## Branch Configuration
- Default remote
- Merge strategies
- Rebase preferences
- Branch protection
---
## Merge Tools
- Choosing merge tools
- Tool configuration
- Conflict resolution
- Custom commands
---
## Diff Tools
- External diff tools
- Tool configuration
- Visualization options
- Custom diff commands
---
## Advanced Settings
- Hook paths
- Template directory
- Attribute settings
- Filter settings
---
## Performance Settings
- Delta compression
- Pack settings
- Threading options
- Cache settings
---
## Security Settings
- Safe directories
- File permissions
- SSL verification
- HTTP proxy
---
## Configuration Management
- Viewing settings
- Editing configurations
- Removing settings
- Configuration files
---
## Portable Configuration
- Sharing settings
- Environment variables
- Conditional includes
- Configuration templates
---
## Common Problems
- Configuration conflicts
- Permission issues
- Path problems
- Tool integration
---
## Best Practices
- Version control configuration
- Documentation
- Security considerations
- Maintenance
---
## Troubleshooting
- Common errors
- Configuration verification
- Debug options
- Getting help
