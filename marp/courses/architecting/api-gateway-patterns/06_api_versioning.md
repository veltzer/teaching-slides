---
tags:
  - architecture:api-gateway
  - architecture:versioning
level: intermediate
category: architecture
audience:
  - audiences:developers

---
# API Versioning at the Gateway

---
## Gateway Versioning

![gateway_versioning](svg/courses/architecting/api-gateway-patterns/06_api_versioning/gateway_versioning.svg)

---
## What This Chapter Covers

- Versioning strategies revisited
- URL versioning at the gateway
- Header-based versioning
- Multiple versions in the same gateway
- Routing rules
- Deprecation at the gateway

---
## Why Version At The Gateway

- The gateway routes by version &#8594; correct service
- Clients see one URL; backends decide which version's logic
- Sunset old versions without changing client code (route to the latest mapping)
- Centralises versioning policy

---
## URL Versioning

```misc
/v1/users -> users-service-v1
/v2/users -> users-service-v2
```

- Clear, explicit
- Easy to test, cache, monitor
- Most common
- Gateway routes by URL prefix

---
## Header-Based Versioning

```http
GET /users
Accept: application/vnd.example.v2+json
```

- Cleaner URLs
- Gateway routes based on header
- Caching layers may need configuration to vary by header
- More REST-purist

---
## Routing Rules

- One service per major version (parallel deployments)
- Or: one service handles many versions internally
- Prefer: parallel services for clean separation
- Consolidate when versions diverge minimally

---
## Strategy Compared

![versioning_strategies](svg/courses/architecting/api-gateway-patterns/06_api_versioning/versioning_strategies.svg)

---
## Stages of an API Lifecycle

- New: behind a feature flag, internal users only
- GA: announced, fully supported
- Deprecated: still works; replacement announced
- Sunset: still works; end-of-life date set
- End-of-Life: returns 410 Gone

---
## Deprecation Headers

```http
Deprecation: Sat, 31 Dec 2026 23:59:59 GMT
Sunset: Sat, 31 Dec 2027 23:59:59 GMT
Link: <https://api.example.com/v2/users>; rel="successor-version"
```

- Add at the gateway for deprecated versions
- Tells consumers when to migrate
- Standard headers; tools can monitor

---
## Sunset Process

- 6+ months notice for public APIs
- Email / docs / blog announcements
- Track who's still calling (per-API-key)
- Reach out to laggard consumers
- Hard cutover only after "we tried" phase

---
## Migration Helpers

- Side-by-side examples in docs
- Version-pinning advice
- Migration scripts where automatable
- Beta period before sunset
- Lower the friction; more migrate on time

---
## Backward Compatibility At The Gateway

- Translate v1 requests to v2 backend
- "Soft" backward compatibility
- Risky: divergence creeps in
- Use sparingly; prefer parallel versions

---
## Multiple Versions, One Spec

- OpenAPI 3 doesn't natively version
- Maintain separate spec files per version
- Or: one spec with `x-api-version` extensions
- Gateway and SDK generators must agree

---
## Routing And Auth Per Version

- v1 may use API keys; v2 may use OAuth
- Gateway can apply different auth per version
- Preserve old auth for old clients
- Force new auth for new clients

---
## Monitoring Versions

- Track requests per version
- "How many calls hit v1 today?"
- Drives sunset decisions
- Surface in dashboards
- Without metrics, you sunset blindly

---
## Common Versioning Mistakes At The Gateway

- No deprecation headers
- Sudden sunset (no notice)
- Multiple major versions running for years (cost)
- Translating between versions in the gateway (complexity)
- No metrics on per-version usage
