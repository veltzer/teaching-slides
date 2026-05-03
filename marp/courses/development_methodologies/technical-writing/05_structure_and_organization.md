---
tags:
  - practices:technical-writing
  - practices:structure
level: beginner
category: methodology
audience:
  - audiences:developers

---
# Structure and Organization

---
## Inverted Pyramid

![inverted_pyramid](svg/courses/development_methodologies/technical-writing/05_structure_and_organization/inverted_pyramid.svg)

---

## Document Structure Patterns

![structure_patterns](svg/courses/development_methodologies/technical-writing/05_structure_and_organization/structure_patterns.svg)

---
## What This Chapter Covers

- Information architecture
- Headings and hierarchy
- Tables of contents and navigation
- Progressive disclosure
- Cross-referencing
- Patterns that work across docs

---
## Why Structure Matters

- Readers scan first, then read
- A well-structured doc is scannable
- Structure helps even when readers don't read in order
- Bad structure makes the same content unusable
- Structure is the cheapest way to improve docs

---
## Information Architecture

- The shape of your information
- How readers move through it
- What they find at each step
- Card-sorting and user research used in larger doc sets
- For most teams: think about it before you start typing

---
## Headings and Hierarchy

- H1: document title (one per page)
- H2: major sections
- H3: subsections
- H4+: rare; usually a smell
- Don't skip levels (H2 directly to H4)
- Headings are how scanners find things

---
## Heading Names

- Specific, not vague
- "Configuration" is too vague; "Configuring TLS" is better
- Active verbs help: "Setting up", "Diagnosing"
- A reader scanning the headings should know what's covered
- Try to describe content, not just label

---
## Tables of Contents

- Auto-generated from headings in most tools
- Essential for any doc longer than a screen
- Static for short docs; sticky sidebar for long ones
- Linkable anchors (`#section-name`)
- Keep heading names short to fit the TOC

---
## Navigation Within Pages

- "Skip to..." links for long pages
- Anchor links shareable in chat
- "Back to top" link at the bottom of long sections
- Breadcrumbs for nested doc sites
- Mobile-friendly navigation if applicable

---
## Progressive Disclosure

- Don't dump everything on the reader at once
- Start simple; offer depth via links
- Quickstart at the top of a README; details below
- "Advanced topics" section at the end
- Lets beginners and experts read the same doc

---
## The Inverted Pyramid

- Most-important first
- Supporting detail next
- Background last
- Borrowed from journalism
- Works because readers stop reading partway through

---
## Cross-Referencing

- Link to other docs that cover related topics
- Don't repeat content; link to it
- Link from the term back to where it's defined
- Two-way links improve discovery
- Stale links are worse than no links — audit periodically

---
## Glossaries

- Define each term once; link from every use
- Useful for projects with specialised vocabulary
- Easy onboarding for new contributors
- Tools: many doc sites support `:term:` markup
- Living document; add as terms emerge

---
## Indexing

- Reference docs benefit from indexes
- Auto-generated when possible
- Some readers prefer indexes to TOCs
- Most modern doc sites: search replaces explicit indexes
- For static PDFs: indexes still matter

---
## Search

- For doc sites larger than ~20 pages
- Algolia DocSearch (free for open source)
- Built-in search in most static-site generators
- Test the search: do common queries find the right pages?
- Bad search makes the docs feel broken even if the content is good

---
## Consistent Section Patterns

- Every API doc page has: Description, Parameters, Returns, Examples, Errors
- Every ADR has: Context, Decision, Consequences
- Every tutorial has: Goal, Prerequisites, Steps, Verification, Next Steps
- Templates encourage this
- Readers learn the pattern; subsequent reading is faster

---
## When Long Is Right

- Reference: comprehensive coverage trumps brevity
- Architecture documents: depth is the point
- Onboarding guides: nothing left to assume
- Don't artificially shorten where length serves the reader

---
## When Short Is Right

- READMEs: get them started fast
- How-to guides: just the recipe
- Runbooks: each step short, total length whatever it needs
- "Brief because the topic is brief" is the goal

---
## Common Structure Mistakes

- One enormous wall of text
- Wrong heading hierarchy (H1, H4, H2 — confusing)
- TOC that doesn't match the page structure
- No linking; readers can't navigate
- Buried lede — the most important point is on page 5
