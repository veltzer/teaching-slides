# Tagging

---

## What We'll Cover

1. Why use tags?
1. Difference between annotated and lightweight tags
1. Creating and managing tags
1. Pushing and pulling tags
1. Using tags in other Git commands
1. Tag naming conventions and best practices

---

## Why Tag?

Tags mark important points in your repository's history:

**Common use cases:**
- **Release versions:** Mark software releases (v1.0, v2.1.3)
- **Milestones:** Important project milestones
- **Stable points:** Known good states for testing
- **Deployment markers:** Track what's deployed where
- **Historical reference:** Mark significant events

**Benefits of tagging:**
- Permanent references to specific commits
- Human-readable names for releases
- Easy checkout of specific versions
- Integration with build and deployment systems
- Clear project history and versioning

```bash
# Quick example
git tag v1.0.0                    # Mark current commit
git checkout v1.0.0               # Return to this version anytime
```

---

## Lightweight vs Annotated Tags

Git supports two types of tags with different characteristics:

**Lightweight tags:**
- Simple pointer to a commit
- Just a name pointing to commit SHA
- No additional metadata
- Similar to a branch that doesn't move

**Annotated tags:**
- Full Git objects stored in database
- Contains tagger information
- Includes tagging date and message
- Can be signed with GPG
- Recommended for releases

![lightweight_vs_annotated_tags](../../../../svg/courses/git/git2/13_tagging/lightweight_vs_annotated_tags.svg)

---

## Creating Lightweight Tags

Lightweight tags are simple references:

```bash
# Create lightweight tag at current commit
git tag v1.0-beta

# Create lightweight tag at specific commit
git tag v0.9 a1b2c3d

# Tag with specific name
git tag milestone-demo HEAD~2

# List lightweight tags
git tag
```

**Lightweight tag characteristics:**
- No `-a` flag needed
- No message or metadata
- Very lightweight (just a reference)
- Quick to create
- Good for temporary markers

**When to use lightweight tags:**
- Temporary markers
- Personal bookmarks
- Quick testing references
- Internal milestones

---

## Creating Annotated Tags

Annotated tags include metadata and are recommended for releases:

```bash
# Create annotated tag with message
git tag -a v1.0.0 -m "Release version 1.0.0"

# Create annotated tag interactively (opens editor)
git tag -a v1.1.0

# Tag specific commit
git tag -a v1.0.1 -m "Hotfix release" a1b2c3d

# Tag with detailed message
git tag -a v2.0.0 -m "Major release 2.0.0

- New authentication system
- Improved performance
- Breaking API changes
- See CHANGELOG.md for details"
```

**Annotated tag benefits:**
- Complete metadata
- Proper audit trail
- Can be cryptographically signed
- Better for release management
- Professional appearance

---

## Viewing Tag Information

Examine tags and their details:

```bash
# List all tags
git tag

# List tags with pattern
git tag -l "v1.*"
git tag --list "v2.0.*"

# Show tag details
git show v1.0.0

# Show only tag object (for annotated tags)
git cat-file tag v1.0.0

# List tags with commit info
git tag -n1    # First line of tag message
git tag -n5    # First 5 lines
```

**Tag information includes:**
- Tag name and type
- Target commit SHA
- Tagger name and email
- Tag creation date
- Tag message
- GPG signature (if signed)

---

## Tag Naming Conventions

Consistent naming improves project management:

**Semantic Versioning (SemVer):**
```bash
# Format: MAJOR.MINOR.PATCH
git tag v1.0.0      # Initial release
git tag v1.0.1      # Bug fix
git tag v1.1.0      # New feature
git tag v2.0.0      # Breaking changes
```

**Pre-release versions:**
```bash
git tag v1.0.0-alpha.1
git tag v1.0.0-beta.2
git tag v1.0.0-rc.1     # Release candidate
```

**Date-based versioning:**
```bash
git tag v2024.01.15
git tag v2024.02.01
```

**Common patterns:**
- Always use consistent prefix (`v` for version)
- Follow semantic versioning principles
- Include pre-release identifiers
- Use lowercase for consistency
- Avoid spaces and special characters

---

## Deleting Tags

Remove tags when needed:

```bash
# Delete local tag
git tag -d v1.0.0-beta
git tag --delete old-tag

# Delete remote tag
git push origin --delete v1.0.0-beta
git push origin :refs/tags/v1.0.0-beta

# Delete multiple tags
git tag -d v1.0.0-alpha v1.0.0-beta

# Delete all tags matching pattern (be careful!)
git tag -d $(git tag -l "v0.*")
```

**When to delete tags:**
- Incorrect tag names
- Pre-release tags no longer needed
- Mistakenly created tags
- Cleanup of old experimental tags

**Important notes:**
- Deleting local tag doesn't affect remote
- Must explicitly delete from remote
- Consider impact on other developers
- Document tag deletion in team

---

## Pushing and Pulling Tags

Tags don't transfer automatically with commits:

**Pushing tags:**

```bash
# Push specific tag
git push origin v1.0.0

# Push all tags
git push origin --tags

# Push all tags (alternative)
git push --tags

# Push commits and tags together
git push origin main --tags
```

**Fetching tags:**

```bash
# Fetch all tags from remote
git fetch --tags

# Fetch specific tag
git fetch origin refs/tags/v1.0.0:refs/tags/v1.0.0

# Pull includes tags by default
git pull
```

**Tag sharing considerations:**
- Tags must be explicitly pushed
- `--tags` pushes all local tags
- Tags are globally visible once pushed
- Consider team coordination before pushing

---

## Checking Out Tags

Work with tagged versions:

```bash
# Checkout specific tag (creates detached HEAD)
git checkout v1.0.0

# Create branch from tag
git checkout -b hotfix-1.0.1 v1.0.0

# Show files at tagged version
git ls-tree v1.0.0

# Compare current version with tag
git diff v1.0.0

# Show commits since tag
git log v1.0.0..HEAD --oneline
```

**Detached HEAD state:**
- Checking out tag creates detached HEAD
- Can examine files and make experimental changes
- Create branch if you need to make commits
- Return to branch with `git checkout main`

---

## Using Tags in Git Commands

Tags work as commit references in most Git commands:

**Log operations:**

```bash
# Show commits between tags
git log v1.0.0..v1.1.0

# Show commits since tag
git log v1.0.0..HEAD

# Compact log since tag
git log --oneline v1.0.0..HEAD
```

**Diff operations:**

```bash
# Compare tags
git diff v1.0.0 v1.1.0

# Compare tag with current
git diff v1.0.0

# Show changes in specific file
git diff v1.0.0 v1.1.0 -- src/main.py
```

**Branch operations:**

```bash
# Create branch from tag
git branch hotfix-branch v1.0.0
git checkout -b feature-branch v1.1.0

# Merge tag into current branch
git merge v1.0.1
```

---

## Signed Tags

Add cryptographic signatures for security:

```bash
# Create signed tag
git tag -s v1.0.0 -m "Signed release 1.0.0"

# Verify signed tag
git tag -v v1.0.0

# Show signature information
git show --show-signature v1.0.0
```

**Setting up GPG signing:**

```bash
# Configure GPG key
git config user.signingkey YOUR_GPG_KEY_ID

# Set default signing
git config tag.gpgSign true
```

**Benefits of signed tags:**
- Verify authenticity of releases
- Ensure tags weren't tampered with
- Compliance and security requirements
- Trust chain for software distribution

---

## Tag Workflows

Different approaches to using tags:

**Release workflow:**

```bash
# Development continues on main
git checkout main

# When ready for release
git tag -a v1.2.0 -m "Release 1.2.0"
git push origin v1.2.0

# Deploy from tag
git checkout v1.2.0
./deploy.sh
```

**Gitflow tagging:**
```bash
# Tag on main branch after merge
git checkout main
git merge --no-ff release/1.3.0
git tag -a v1.3.0 -m "Release 1.3.0"
git push origin main --tags
```

**Hotfix tagging:**
```bash
# Create hotfix from previous release
git checkout -b hotfix-1.2.1 v1.2.0
# Fix critical bug
git tag -a v1.2.1 -m "Hotfix release 1.2.1"
```

---

## Automated Tagging

Integrate tagging with CI/CD systems:

**GitHub Actions example:**
```yaml
name: Release
on:
  push:
    branches: [main]
jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Create tag
        run: |
          VERSION=$(cat VERSION)
          git tag -a v$VERSION -m "Release $VERSION"
          git push origin v$VERSION
```

**Semantic release tools:**
- Automatically determine version numbers
- Generate changelogs
- Create tags based on commit messages
- Integrate with package managers

**Benefits:**
- Consistent tagging process
- Reduced human error
- Automated changelog generation
- Integration with deployment systems

---

## Tag Management Best Practices

**Naming consistency:**
1. Use semantic versioning
1. Consistent prefixes (v1.0.0)
1. Clear pre-release naming
1. Document naming conventions

**Release process:**
1. Test thoroughly before tagging
1. Use annotated tags for releases
1. Include meaningful messages
1. Push tags after creating them
1. Coordinate with team members

**Maintenance:**
1. Clean up development tags
1. Keep release tags permanently
1. Document important tags
1. Regular tag auditing

---

## Tag Organization Strategies

**Version branches:**

```bash
# Create maintenance branches from tags
git checkout -b maint-1.0 v1.0.0
git checkout -b maint-1.1 v1.1.0

# Apply hotfixes to maintenance branches
git checkout maint-1.0
# Apply fix
git tag -a v1.0.1 -m "Security hotfix"
```

**Environment tags:**

```bash
# Tag deployments to different environments
git tag -a staging-2024.01.15 -m "Deployed to staging"
git tag -a production-2024.01.20 -m "Deployed to production"
```

**Feature milestone tags:**

```bash
# Mark feature completion
git tag -a feature-auth-complete -m "Authentication feature complete"
git tag -a milestone-beta -m "Beta milestone reached"
```

---

## Troubleshooting Tags

**Common issues and solutions:**

### Issue: Tag already exists

```bash
# Error: tag 'v1.0.0' already exists
git tag -f v1.0.0        # Force overwrite (dangerous)
git tag -d v1.0.0        # Delete first, then recreate
git tag v1.0.0-new       # Use different name
```

### Issue: Tag not found after push

```bash
# Verify tag exists locally
git tag -l v1.0.0

# Push specific tag
git push origin v1.0.0

# Check remote tags
git ls-remote --tags origin
```

### Issue: Wrong commit tagged

```bash
# Delete and recreate
git tag -d v1.0.0
git tag -a v1.0.0 -m "Release 1.0.0" correct-commit-sha

# Or move existing tag
git tag -f v1.0.0 correct-commit-sha
```

---

## Tag Integration with Tools

**Package managers:**
```json
// package.json
{
  "name": "myproject",
  "version": "1.0.0",
  "scripts": {
    "release": "npm version patch && git push --tags"
  }
}
```

**Docker integration:**
```bash
# Build Docker image from tag
git checkout v1.0.0
docker build -t myapp:1.0.0 .
docker build -t myapp:latest .
```

**Deployment systems:**

```bash
# Deploy specific version
kubectl set image deployment/myapp myapp=myapp:v1.0.0

# Rollback using tags
kubectl set image deployment/myapp myapp=myapp:v0.9.9
```

---

## Advanced Tag Operations

**Tag ranges and queries:**

```bash
# Find tags containing specific commit
git tag --contains a1b2c3d

# Find tags merged into branch
git tag --merged main

# Find tags not merged
git tag --no-merged main

# Sort tags by version
git tag -l | sort -V

# Most recent tag
git describe --tags --abbrev=0
```

**Tag scripting:**

```bash
#!/bin/bash
# Auto-tag script
LAST_TAG=$(git describe --tags --abbrev=0)
echo "Last tag: $LAST_TAG"

# Get commits since last tag
git log $LAST_TAG..HEAD --oneline

# Interactive tag creation
read -p "Enter new tag version: " VERSION
git tag -a "v$VERSION" -m "Release $VERSION"
```

---

## Tag Security Considerations

**Protecting important tags:**
- Use signed tags for releases
- Restrict tag push permissions
- Audit tag creation and deletion
- Backup important tags

**Repository protection:**

```bash
# GitHub repository settings
# - Protect tags matching pattern: v*
# - Require signed commits
# - Restrict push access
```

**Verification workflow:**
```bash
# Verify tag signature before deployment
git tag -v v1.0.0 || exit 1
# Proceed with deployment only if verification succeeds
```

---

## Tag Migration and Cleanup

**Repository cleanup:**

```bash
# List all tags with creation date
git for-each-ref --format="%(refname:short) %(creatordate)" refs/tags

# Remove old development tags
git tag -l "dev-*" | xargs git tag -d

# Archive old tags before deletion
git tag -l "old-*" > archived-tags.txt
git tag -l "old-*" | xargs git tag -d
```

**Migration between repositories:**

```bash
# Export tags
git tag > tags-backup.txt

# Import tags to new repository
# (after setting up remotes and fetching)
git push origin --tags
```

---

## Tag Performance and Scalability

**Performance considerations:**
- Tags are lightweight references
- Large numbers of tags don't significantly impact performance
- Tag listing may be slow with thousands of tags
- Use tag patterns for filtering

**Repository size impact:**
- Lightweight tags: minimal impact
- Annotated tags: small objects in database
- Signed tags: slightly larger due to signatures
- Overall impact usually negligible

**Optimization strategies:**

```bash
# Pack refs for better performance
git pack-refs --all

# Garbage collect to optimize storage
git gc --aggressive
```

---

## Lab Exercise: Complete Tagging Workflow

**Scenario:** Implement a complete tagging strategy for a software project with proper release management.

**Setup tasks:**
1. **Create release workflow:**
   - Establish semantic versioning scheme
   - Create first release with proper tag
   - Document tagging conventions

1. **Tag management:**
   - Create both lightweight and annotated tags
   - Practice tag operations (create, delete, rename)
   - Set up signed tags with GPG

1. **Integration testing:**
   - Push and pull tags between repositories
   - Use tags in various Git commands
   - Create branches from tags

**Advanced tasks:**
1. **Automation setup:**
   - Create scripts for automated tagging
   - Set up CI/CD integration
   - Implement tag-based deployment

1. **Team workflow:**
   - Design release process documentation
   - Create tag naming guidelines
   - Implement tag protection and verification

**Deliverables:** Complete tagging strategy document, automated tagging scripts, release workflow procedures, and team guidelines for tag management.

---

## Summary: Effective Tag Management

**Key takeaways:**

1. **Choose the right tag type:**
   - Lightweight for temporary markers
   - Annotated for releases and milestones
   - Signed for security-critical releases

1. **Follow naming conventions:**
   - Use semantic versioning consistently
   - Document team conventions
   - Maintain professional appearance

1. **Integrate with workflows:**
   - Automate where possible
   - Coordinate with CI/CD systems
   - Plan for deployment and rollback

1. **Maintain tag hygiene:**
   - Clean up development tags
   - Protect important release tags
   - Regular auditing and maintenance

**Remember:** Tags are permanent markers in your project's history. Use them thoughtfully to create clear milestones, enable easy navigation through your project's evolution, and support reliable release management. Good tagging practices contribute significantly to professional software development and team collaboration.
