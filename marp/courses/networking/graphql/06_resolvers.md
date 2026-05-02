---
tags:
  - networking:graphql
level: intermediate
category: networking
audience:
  - audiences:developers

---
# Resolvers

---
## N+1 Problem

![resolver_chain](svg/courses/networking/graphql/06_resolvers/resolver_chain.svg)

---
## What This Chapter Covers

- What resolvers are
- Signatures
- Default resolvers
- Context
- Async
- Error handling

---
## What Resolvers Are

- Functions that fetch field data
- One per field (or default)
- Compose to satisfy a query
- Where logic lives

---
## Resolver Signature

- `(parent, args, context, info) => value`
- parent: result from parent field
- args: field arguments
- context: per-request data (auth, loaders)
- info: query AST

---
## Default Resolvers

- If no resolver for field: read from parent
- e.g., `user.name` reads `name` from User object
- Reduces boilerplate

---
## Custom Resolvers

```javascript
{
    User: {
        fullName: (user) => `${user.first} ${user.last}`,
        posts: (user, _, ctx) => ctx.db.posts.byUser(user.id)
    }
}
```

---
## Per-Field Granularity

- Each field can have its own resolver
- Compose from many sources
- Server stitches the result

---
## Context

- Per-request object
- Auth token, user id
- DB connection
- Data loaders
- Don't mutate

---
## Async

- Resolvers can return Promise
- Awaited in parallel where possible
- Use for any IO

---
## Resolver Order

- Top-down: query, then nested
- Siblings in parallel
- Children after parent resolves

---
## Error Handling

- Throw: bubbles to errors array
- Field-level: caller sees null
- Use schema nullability deliberately
- Custom errors for clients

---
## Information Leak

- Don't expose internal errors
- Map internal exceptions to client-safe messages
- Log full info server-side

---
## Field-Level Auth

- Check in resolver
- Throw if unauthorised
- Or return null for sensitive fields

---
## Performance

- Parallel sibling resolution
- Batch via DataLoader
- Cache where appropriate

---
## Testing Resolvers

- Unit: call directly with mocks
- Integration: full query against test DB
- Both useful

---
## Common Resolver Mistakes

- Logic in resolvers that should be in services
- DB calls per field; n+1
- Mutating context
- Forgetting auth checks on nested fields
- Leaking internal errors to clients
