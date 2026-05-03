---
tags:
  - architecture:api
  - architecture:versioning
level: intermediate
category: architecture
audience:
  - audiences:developers

---
# API Versioning Strategies

---
## Deprecation Lifecycle

![deprecation_lifecycle](svg/courses/architecting/api-first-development/06_api_versioning_strategies/deprecation_lifecycle.svg)

---
## What This Chapter Covers

- Why APIs need versioning
- Breaking vs non-breaking changes
- URL versioning
- Header versioning
- Content negotiation
- Deprecation policies
- Practical versioning workflows

---
## Why Versioning

- APIs evolve
- Consumers can't update in lockstep with the producer
- Old clients keep working; new clients get new features
- Without versioning, every change risks breaking someone
- Version is the contract between you and your consumers

---
## Breaking vs Non-Breaking

- **Non-breaking**: add new optional fields, new endpoints, new optional params
- **Breaking**: remove fields, change types, rename, change required-ness, change URL
- Add freely; remove carefully
- Deprecate before removing
- "It's just a small change" often isn't

---
## URL Versioning

```http
GET /v1/users/42
GET /v2/users/42
```

- Most common
- Visible in the URL
- Easy to route in load balancers, CDNs
- Both versions can coexist
- The pragmatic default

---
## Header Versioning

```http
GET /users/42
Accept: application/vnd.example.v2+json
```

- Cleaner URLs
- More REST-purist
- Harder to test (curl needs explicit headers)
- Cache layers may not key on it
- Works; less common in practice

---
## Query Parameter Versioning

```http
GET /users/42?version=2
```

- Easy to test
- Less common
- Can clash with normal query params
- Possible but rarely the best choice

---
## Content Negotiation

- The HTTP standard way: client sends `Accept` header, server picks best match
- More flexible than fixed-version routing
- Works for content type *and* version simultaneously
- Theoretical purity high; tooling friction higher
- Use if your team understands HTTP deeply

---
## Semantic Versioning For APIs

- Major.Minor.Patch
- **Major**: breaking change
- **Minor**: backward-compatible feature
- **Patch**: backward-compatible fix
- Most public APIs only expose major (`/v1/`, `/v2/`)
- Minor and patch evolve in place

---
## Deprecation Policy

- "This endpoint is deprecated; will be removed on 2027-01-01"
- Communicate clearly: docs, response headers (`Sunset`, `Deprecation`)
- Time horizon: 6-12 months minimum for public APIs
- Internal APIs can be faster
- Without a policy, consumers have no time to migrate

---
## Sunset Header

```http
Deprecation: Sat, 31 Dec 2026 23:59:59 GMT
Sunset: Sat, 31 Dec 2027 23:59:59 GMT
Link: <https://api.example.com/v2/users>; rel="successor-version"
```

- Standard headers for deprecation
- Tools can monitor
- Self-documenting

---
## Maintaining Two Versions

- Two implementations? Painful
- Same implementation; v2 wraps v1 (or vice versa)?
- Translation layer between?
- Pick: maintenance burden vs purity
- Most teams: keep v1 alive minimally; build new in v2

---
## When To Bump Major

- Removing an endpoint or field
- Changing a field's type
- Renaming a field
- Changing required-ness
- Changing authentication mechanism
- Real breakage; not "I want a clean slate"

---
## When NOT To Bump Major

- Adding a new endpoint
- Adding a new optional field
- Adding a new optional query parameter
- Performance improvements
- Bug fixes that don't change behaviour spec'd in the contract

---
## Backward-Compatible Schema Changes

- Adding optional fields: safe
- Adding new enum values: safe IF clients ignore unknown values (most do; some don't)
- Loosening constraints: safe (`maxLength: 100 -> 200`)
- Tightening: NOT safe (will reject previously-valid input)

---
## Internal vs Public APIs

- **Internal**: deprecate quickly; teams update together
- **Public**: deprecate slowly; consumers can't all be coordinated
- Different processes; different time horizons
- Internal: 1-3 months; public: 6-24 months
- Match your process to your audience

---
## API Versioning In CI

- Spec lint: warn on potential breaking changes
- `oasdiff`: compare two specs; report breaking changes
- Block PRs that introduce breaking changes without a major version bump
- Helps a team catch what's easy to miss

---
## Common Versioning Mistakes

- Renaming things in v1 instead of bumping to v2
- "Soft" deprecation (not communicated; suddenly removed)
- Multiple major versions running for years (multiple maintenance burdens)
- No versioning, just trust ("nothing breaking happens here")
- Versioning at the wrong level (per-endpoint when you have a whole API contract)

---
## Where to Put the Version

![version_methods](svg/courses/architecting/api-first-development/06_api_versioning_strategies/version_methods.svg)
