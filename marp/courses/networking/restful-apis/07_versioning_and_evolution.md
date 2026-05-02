---
tags:
  - networking:rest
  - practices:design
level: intermediate
category: networking
audience:
  - audiences:developers

---
# Versioning and Evolution

---
## Breaking vs Non-Breaking

![breaking_changes](svg/courses/networking/restful-apis/07_versioning_and_evolution/breaking_changes.svg)

---
## What This Chapter Covers

- Why versioning
- Versioning strategies
- Backwards compatibility
- Deprecation
- Schema evolution

---
## Why Version

- APIs evolve
- Clients depend on shape
- Breaking changes break clients
- Need a path to change

---
## Breaking vs Non-Breaking

- Breaking: removes / renames / restricts
- Non-breaking: adds optional fields
- Goal: most changes non-breaking
- Plan for breaking changes deliberately

---
## Versioning Strategies

- URL path: /v1/users
- Header: Accept-Version: 1
- Query param: ?version=1
- Media type: application/vnd.example.v1+json

---
## URL Path Versioning

- Most common
- Easy to see and route
- Pollutes URLs
- Browser-friendly

---
## Header Versioning

- Cleaner URLs
- Harder to test from browser
- Routing is more complex

---
## Avoid Versioning

- Make changes additive
- New optional fields
- Don't repurpose fields
- Add new endpoints rather than mutate old

---
## Backwards Compatibility

- Old clients keep working
- New fields ignored by old clients
- Server tolerates missing new fields
- Serialise unknown fields conservatively

---
## Deprecation

- Mark as deprecated in docs
- Deprecation header in responses
- Sunset header with date
- Grace period

---
## Migration Plan

- Notify clients
- Provide migration guide
- Run old and new in parallel
- Monitor old version usage
- Switch off when usage low

---
## Schema Evolution

- Add fields: safe
- Remove fields: breaking
- Rename: breaking; add new and deprecate old
- Tighten validation: breaking

---
## Versioning Internal vs External

- Internal: coordinate with consumers; can move fast
- External: public, slow, careful
- Different policies per audience

---
## Documentation Per Version

- Each version has its own docs
- Diff between versions
- Migration notes
- Sunset dates clear

---
## Common Versioning Mistakes

- No version from the start; painful retrofit
- Bumping major for any change
- Removing without deprecation period
- No sunset policy
- Multiple incompatible "v1"s in different services
