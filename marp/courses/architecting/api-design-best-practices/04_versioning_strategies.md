---
tags:
  - concepts:api
  - concepts:best-practices
level: intermediate
category: architecture
audience:
  - audiences:developers
  - audiences:architects

---
# Versioning Strategies

---
## Why Version

- APIs change; consumers depend on specific behavior
- Without versioning, every change risks breaking someone
- Versioning makes change explicit and consensual
- Lack of versioning is the #1 cause of brittle integrations

---
## URL-Based Versioning

- `/v1/users`, `/v2/users`
- Simple, visible, easy to route
- Most common in practice
- The "version" is part of the URL, like a path segment

---
## URL Versioning: Pros

- Easy to see; easy to test
- Easy to route at the gateway level
- Multiple versions can coexist on the same server
- Cacheable — different URLs are different cache keys

---
## URL Versioning: Cons

- "REST purists" argue the URL should identify the resource, not the version
- Encourages major-version explosion if used carelessly
- Migrating consumers means changing every URL they call
- Real-world: most APIs accept the trade-off

---
## Header-Based Versioning

- Version in a custom header: `X-API-Version: 2`
- Or in the Accept header: `Accept: application/vnd.example.v2+json`
- The URL stays the same across versions

---
## Header Versioning: Pros

- URL is "clean"
- Aligns with content-negotiation semantics
- Clients can negotiate: "I prefer v2; v1 is acceptable"

---
## Header Versioning: Cons

- Less visible — easy to miss in logs and debugging
- Cache keys must include the header
- Browser-based testing is harder
- Many consumers forget the header and get the default version unexpectedly

---
## Query Parameter Versioning

- `/users?api_version=2`
- Easy to add to existing URLs
- Visible like URL versioning
- But: query params are usually for filtering, not for routing

---
## Query Versioning Trade-Offs

- Easy to discover and test
- Mixing versions with filters is awkward
- Documentation is more complicated
- Less common than URL versioning

---
## Semantic Versioning for APIs

- Major (breaking), minor (additive), patch (fixes)
- Patch and minor are non-breaking; consumers don't need to opt in
- Major requires a new version number
- For HTTP APIs, only the major number usually appears in the URL

---
## Additive Changes Are Free

- Adding a new field to a response: backward-compatible
- Adding a new optional query parameter: backward-compatible
- Adding a new endpoint: backward-compatible
- Old consumers ignore what they don't know

---
## Breaking Changes Need a New Version

- Removing or renaming a field
- Changing a field's type
- Removing a parameter or making an optional one required
- Changing the meaning of a status code
- Changing default values that affect behavior

---
## Choosing a Strategy

- **URL** is the most common; recommend for new APIs
- **Header** is academically purer; viable if you control consumers tightly
- **Query** is rarely the right choice
- The strategy matters less than committing to one and applying it consistently

---
## Default Version

- Be explicit about the default
- Either: no default — version is mandatory
- Or: default to the oldest stable version (consumers don't auto-upgrade)
- Never default to "latest" — consumers will break randomly

---
## Versioning Bounded Context

- Some teams version each endpoint independently
- More flexible, more complex
- Most teams version the whole API together
- Pick what your team can maintain

---
## Anti-Patterns

- "Just add fields and hope it doesn't break"
- Multiple incompatible v1's because nobody agreed on what v1 means
- Versioning the implementation but not the contract (consumers see leakage)
- "v2 in production, v1 still here, v1.1 deprecated, v3 in beta" — version sprawl

---
## Summary

- URL versioning is the most common; pick it unless you have a reason not to
- Additive changes don't need a new version; breaking ones do
- Be explicit about default version
- Limit live versions to two: current and previous
- Migration is a separate problem (chapter 11)
