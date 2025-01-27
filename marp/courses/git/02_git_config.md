# Git Configuration
---
## Configuration Levels
![0](../../../out/mermaid/marp/courses/git/02_git_config.md/0.png)

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
---
## Next Steps
## Working with Remotes
- Remote repository setup
- Collaboration workflows
- Branch tracking
- Network operations
