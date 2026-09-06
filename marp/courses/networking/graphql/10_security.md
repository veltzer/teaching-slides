---
tags:
  - networking:graphql
  - security:authentication
level: intermediate
category: networking
audience:
  - audiences:developers

---

# Security

---

## What This Chapter Covers

- Authentication
- Authorisation
- Query attacks
- Introspection
- Persisted queries

---

## Authentication

- Same as REST: token / JWT / session
- Verified on each request
- Set into context

---

## Security Concerns

![security_concerns](svg/courses/networking/graphql/10_security/security_concerns.svg)

---

## Authorisation

- Field-level: per resolver
- Schema-level: directives
- Service-level: middleware
- Combine layers

---

## Schema Directives

```graphql
type Query {
    secret: String! @auth(role: "ADMIN")
}
```

- Declarative auth
- Less boilerplate

---

## Resolver-Level

```javascript
{
    Query: {
        secret: (_, __, ctx) => {
            if (!ctx.user.isAdmin) throw new ForbiddenError();
            return getSecret();
        }
    }
}
```

- Fine-grained
- More flexible

---

## Common Attacks

- Excessive depth: deep recursion
- High complexity: huge result sets
- Field-level enumeration
- Introspection: schema discovery

---

## Depth Limiting

- Reject nesting beyond N
- Plugin or custom check
- Often 7-10 max

---

## Complexity Analysis

- Score each field
- Multiply by list args
- Reject above budget
- Prevents runaway queries

---

## Rate Limiting

- Per IP, per user
- Per query type
- Different from REST: same endpoint

---

## Introspection in Production

- Schema discovery via __schema
- Useful for tools, risky for security through obscurity
- Often disabled in prod
- Or auth-gated

---

## Persisted Queries as Allow-List

- Only registered queries allowed
- No arbitrary queries from clients
- Good for public APIs
- Drop introspection in prod safely

---

## Input Validation

- Schema enforces types
- Add custom checks (length, format)
- Don't trust IDs as parents

---

## Logging

- Log queries with operation name
- Sample at scale
- Don't log secrets in variables
- Correlate to user

---

## Common Security Mistakes

- Auth at gateway only; resolver bypass
- No depth or complexity limits
- Introspection open in production
- Variables in logs containing PII
- Same JWT used for everything
