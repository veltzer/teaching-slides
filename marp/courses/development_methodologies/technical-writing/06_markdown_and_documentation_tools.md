---
tags:
  - practices:technical-writing
  - tools:markdown
level: beginner
category: methodology
audience:
  - audiences:developers

---
# Markdown and Documentation Tools

---
## What This Chapter Covers

- Markdown syntax basics and extensions
- Static site generators
- Documentation hosting platforms
- AsciiDoc as an alternative
- Tool selection criteria
- Setting up a docs pipeline

---
## Why Markdown Won

- Plain text, readable as written
- Renders to HTML cleanly
- Versionable in git
- Universal: every code platform speaks it
- Low barrier to contribution

---
## Tooling Layers

![doc_tools](svg/courses/development_methodologies/technical-writing/06_markdown_and_documentation_tools/doc_tools.svg)

---
## Markdown Basics

```markdown
# Heading 1
## Heading 2

bold, italic, code (use single backticks for inline)

- bullet
- list

1. numbered
2. list

[link text](https://example.com)
```

- Image syntax is `!` followed by `[alt text](path)` (rendered as image when path resolves)

- Renders the same in GitHub, GitLab, Bitbucket, most static sites

---
## Code Blocks

````markdown
```python
def hello():
    print("hi")
```misc
````

- Language tag for syntax highlighting
- Three-backtick fence to start and end
- Inside the block: literal text, no markdown processing
- For inline code: single backticks

---
## Tables

```markdown
| Header | Header |
|--------|--------|
| cell   | cell   |
| cell   | cell   |
```

- Pipe-delimited
- Header separator with dashes
- Optional alignment with `:`
- Long tables: don't try in markdown; use CSV with a renderer

---
## Markdown Flavours

- **CommonMark**: the standard
- **GFM (GitHub Flavored Markdown)**: most common; adds tables, task lists, strikethrough
- **MDX**: Markdown + JSX components (React-based)
- **Pandoc Markdown**: most extended; less commonly rendered
- Stick with GFM unless you have a specific need

---
## Static Site Generators

- Convert markdown into a website
- Most popular for docs:
    - **MkDocs** (Python; simple; great for projects)
    - **Docusaurus** (React; feature-rich)
    - **Sphinx** (Python; very mature; complex)
    - **Hugo** (Go; fast)
    - **Jekyll** (Ruby; older but stable)

---
## MkDocs

- Python; pip install
- One YAML config file
- `docs/` folder of markdown
- Themes: Material is excellent
- The fastest setup for a small project

---
## Docusaurus

- React-based
- Versioning, internationalisation, blog support
- Great for libraries with frequent releases
- More complex than MkDocs
- Used by Jest, Babel, React Native

---
## Sphinx

- Originally for Python; works for any language
- reStructuredText is the native format (markdown supported via plugins)
- Best for: cross-referenced API docs, books, large doc sets
- Steep learning curve
- The Python community standard

---
## Hosting Platforms

- **Read the Docs**: free for open-source, paid for private
- **GitHub Pages**: free, simple, GitHub-hosted
- **GitLab Pages**: same idea, GitLab-hosted
- **Vercel / Netlify**: any static site, generous free tier
- **Internal**: many companies host on private S3 + CloudFront

---
## CI for Docs

- Build on every PR
- Deploy on merge to main
- Preview deploys for PRs (Netlify, Vercel default)
- Doc errors break the build
- Treat docs like code in CI

---
## AsciiDoc

- Alternative to markdown
- More features (cross-references, complex tables, structure)
- More verbose syntax
- Used by some technical writers, less common in code repos
- Worth knowing exists; not the default

---
## Documentation Linters

- **Vale**: prose linter; configurable rules
- **markdownlint**: markdown syntax issues
- **alex**: catches insensitive language
- **write-good**: catches passive voice, weasel words
- Run in CI; gradually adopt

---
## Choosing a Tool

- Project size: small &#8594; MkDocs; large &#8594; Sphinx or Docusaurus
- Audience: open source &#8594; Read the Docs; internal &#8594; GitHub Pages or self-host
- Team familiarity: pick what they'll maintain
- Required features: search, versioning, i18n, API docs
- Don't over-tool early

---
## A Minimal Setup

```bash
pip install mkdocs mkdocs-material
mkdocs new my-docs
cd my-docs
mkdocs serve  # local dev
mkdocs gh-deploy  # publish to GitHub Pages
```

- Five commands, full doc site
- Works for many small-to-medium projects

---
## When to Outgrow

- Need versioning &#8594; Docusaurus, Sphinx
- Need API doc generation &#8594; Sphinx, MkDocs+plugins, Slate
- Multiple repositories &#8594; consider a meta-tool (Antora, GitBook)
- Translations &#8594; Docusaurus, Sphinx
- Don't switch too eagerly; switching costs are real

---
## Common Tooling Mistakes

- Picking the most powerful tool for a small project
- Picking a niche tool nobody else can maintain
- Building a custom doc system instead of using existing tools
- Not putting docs in the same repo as the code
- Letting the doc site go offline silently when CI breaks
