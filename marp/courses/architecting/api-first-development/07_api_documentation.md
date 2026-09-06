---
tags:
  - architecture:openapi
  - practices:documentation
level: intermediate
category: architecture
audience:
  - audiences:developers

---

# API Documentation

---

## What This Chapter Covers

- Why API docs matter
- Swagger UI
- Redoc
- Other rendering tools
- Hosting and CDN
- Beyond the spec: tutorials, recipes
- Documentation that consumers actually use

---

## Why API Docs Matter

- The first thing a potential consumer reads
- Determines whether they integrate at all
- Determines how fast they integrate
- Lives forever; old docs guide new users
- The single biggest UX touchpoint for many APIs

---

## Three Layers

![doc_layers](svg/courses/architecting/api-first-development/07_api_documentation/doc_layers.svg)

---

## OpenAPI Renders to Docs

- Spec describes the API
- Renderer turns spec into a doc site
- Auto-generated; always in sync (if regenerated)
- Multiple renderers; pick by aesthetics and features
- Free; the path of least resistance

---

## Swagger UI

- The classic OpenAPI renderer
- Interactive: "Try it out" against a real server
- Open source; widely deployed
- Single HTML/JS page; easy to embed
- Aesthetic: functional, not beautiful

---

## Redoc

- Three-pane layout: nav, content, code samples
- Cleaner than Swagger UI by default
- Easier to read for a long doc
- No "try it out" by default
- Open source

---

## Stoplight Studio / Elements

- Commercial product family
- Stoplight Studio: editor + docs
- Stoplight Elements: open-source docs renderer
- Polished aesthetics
- Used by some big public APIs

---

## Mintlify, Readme.com, etc.

- Hosted docs platforms
- OpenAPI in; pretty docs out
- Add: search, analytics, custom branding
- Cost: subscription
- Worth it for public-facing developer-platform APIs

---

## Which Renderer

- Internal API: Swagger UI is fine
- Public free API: Redoc or Swagger UI
- Public paid API: invest in a polished renderer
- Match the polish to the audience and stakes

---

## Renderer Catalog

![doc_renderers](svg/courses/architecting/api-first-development/07_api_documentation/doc_renderers.svg)

---

## Hosting

- Generated docs: static HTML
- GitHub Pages, Netlify, Vercel: free, fast
- CDN: cheap, scalable
- Behind auth for internal APIs
- Trivial compared to the writing

---

## Beyond The Spec

- Reference docs: what every endpoint does (auto from spec)
- Tutorials: how to do common tasks
- Recipes / cookbooks: working examples
- Migration guides: between versions
- Troubleshooting: common errors and fixes

---

## Tutorials

- Step-by-step "your first integration"
- Working code in 1-3 languages
- Should run end-to-end if followed verbatim
- Fastest way to onboarding success
- Take an hour to write; save days of support

---

## Recipes

- "How to authenticate"
- "How to handle pagination"
- "How to retry on rate limit"
- One per common task
- Concrete code; works as-is

---

## Migration Guides

- For every version bump
- "What changed; how to update your code"
- Side-by-side before / after
- Critical for public APIs
- Reduces support burden

---

## Troubleshooting

- Common error codes; what they mean; how to fix
- "Why am I getting 401?"
- "Why is my webhook not firing?"
- Searchable; first hit deflects a support ticket

---

## Documentation In CI

- Build the docs on every PR
- Preview deploys for review
- Failed builds block merging
- Same as code; same discipline
- Without CI, docs rot silently

---

## Examples Tested In CI

- Code snippets in tutorials should run
- Use doctests, snippets-from-code-files, or similar
- Broken examples found before users complain
- The strongest guarantee that docs are accurate

---

## Searchable Docs

- For more than ~20 pages, search is essential
- Algolia DocSearch: free for open-source, fast
- Built-in search in Mintlify, Readme, etc.
- Test: do common queries find the right page?
- Bad search makes good docs feel broken

---

## Common Documentation Mistakes

- Spec-only; no tutorials
- Tutorials that don't work
- No code examples in users' actual languages
- Stale: spec changed; docs didn't
- No search
- No versioning of docs (live docs always shown for the latest version)
