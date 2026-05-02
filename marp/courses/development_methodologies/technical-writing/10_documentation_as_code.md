---
tags:
  - practices:technical-writing
  - practices:docs-as-code
level: beginner
category: methodology
audience:
  - audiences:developers

---
# Documentation as Code

---
## What This Chapter Covers

- Why docs in the code repo
- Version control for documentation
- CI/CD for documentation
- Automated link checking
- Documentation linting
- The full pipeline

---
## What "Docs as Code" Means

- Treat documentation like source code
- Same repo, same git workflow, same review process
- Built and deployed by CI
- Linted and tested
- The modern industry default for technical docs

---
## The Pipeline

![docs_as_code](svg/courses/development_methodologies/technical-writing/10_documentation_as_code/docs_as_code.svg)

---
## Why It Wins

- Docs evolve with code (no drift)
- Same review process — quality discipline applies
- Engineers can update docs without leaving their tooling
- Versionable, diffable, reviewable
- One workflow to learn

---
## Docs In The Code Repo

- `docs/` folder alongside `src/`
- Same PR can change code and docs together
- Reviewers see both
- Atomic: shipped together, broken together (rare)
- Beats wikis that nobody updates

---
## Version Control For Docs

- Every change has an author, a date, a reason (commit message)
- "git blame" answers "why is this paragraph here?"
- Bisect to find when a doc change introduced confusion
- History preserves rationale
- Same skills you already have

---
## CI for Docs

- Build the doc site on every PR
- Fail the build if it doesn't compile
- Preview deploys (Netlify, Vercel) for visual review
- Deploy on merge to main
- Same disciplines as software CI

---
## Automated Link Checking

- Broken internal links: caught at build
- Broken external links: separate scheduled job
- Tools: `markdown-link-check`, `lychee`, `linkchecker`
- Stale link reports go to the doc owner
- One of the cheapest quality wins

---
## Documentation Linting

- **Vale**: prose linter; configurable styles
- **markdownlint**: markdown syntax issues
- **alex**: catches problematic language
- **textlint**: extensible JavaScript-based linter
- Run in CI; report inline in PRs

---
## Style Enforcement

- Vale supports custom rules (`use "we" not "us"`, `avoid "simply"`)
- Ship rules in the repo; everyone gets them
- New contributors learn the style by writing it
- Consistency without manual policing
- Effective for large doc sets

---
## Spell Check

- Surprisingly easy to break trust with typos
- `aspell`, `cspell`, `hunspell` in CI
- Custom dictionaries for technical terms
- Fail builds on typos in main; warn in PRs
- Catches what humans miss

---
## Code Examples In CI

- Run examples as tests
- Doctests (Python), executable code blocks (mdBook), litprog
- Example breaks = doc is wrong
- The strongest guarantee that examples work
- Worth the setup time

---
## Preview Deploys

- Each PR builds a temporary doc site
- Reviewers see the rendered version
- Catches formatting issues that look fine in markdown
- Netlify and Vercel make this turnkey
- Reviewing docs in raw markdown misses too much

---
## Docs Owners

- CODEOWNERS for `docs/` paths
- Docs people review docs PRs
- Engineers responsible for keeping their feature docs current
- Without owners, docs decay
- "Everyone's responsible" = nobody is

---
## Doc Reviews

- Same PR review process
- Doc reviewers check: clarity, accuracy, style, examples
- Reviewers comment on prose like they comment on code
- Two-approval requirement for major doc changes (some teams)
- Treats docs like the deliverable they are

---
## A Sample Pipeline

- Engineer writes docs in markdown alongside code
- Pre-commit: format markdown, lint, spell check
- PR: build site, deploy preview, run all checks
- Reviewers: look at preview URL
- Merge: deploy to production docs
- Schedule: monthly link-check, quarterly content review

---
## Tooling Stack

- Editor: VS Code with markdown preview
- Linters: Vale, markdownlint, cspell
- Generator: MkDocs / Docusaurus / Sphinx
- CI: GitHub Actions / GitLab CI
- Hosting: Netlify / GitHub Pages / S3 + CDN
- Total cost: usually free at small scale

---
## When Docs-As-Code Hurts

- Marketing teams who don't use git
- Brochure-like content with heavy design
- Real-time collaboration on a single doc (use Notion / Google Docs)
- Internal wikis for unstructured knowledge
- Pick the right tool for the right content

---
## Common Mistakes

- Docs in a wiki disconnected from the code
- "We'll set up CI later" — never happens
- No preview deploys — formatting issues slip through
- One doc owner who burns out
- Building a custom doc system instead of using existing tools
