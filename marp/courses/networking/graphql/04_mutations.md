---
tags:
  - networking:graphql
level: intermediate
category: networking
audience:
  - audiences:developers

---
# Mutations

---
## What This Chapter Covers

- Mutation basics
- Inputs and payloads
- Conventions
- Errors
- Optimistic updates

---
## Basic Mutation

```graphql
mutation {
    createUser(input: { name: "Alice", email: "a@x.com" }) {
        id
        name
    }
}
```

- Side effect + return value
- Returns just-created or just-updated state

---
## Input Type

```graphql
input CreateUserInput {
    name: String!
    email: String!
}
```

- Single argument
- Cleaner than many positional args
- Versionable

---
## Payload Type

```graphql
type CreateUserPayload {
    user: User
    errors: [Error!]
}
```

- Returns rich result
- Errors structured, not just thrown
- Mutation-specific shape

---
## Mutation Naming

- Verb + Noun: createUser, updatePost, deleteComment
- Imperative
- Pair with input/payload type names

---
## Atomicity

- Single mutation: one transaction
- Multiple in one document: sequential
- Each runs serially server-side

---
## Multiple Mutations

```graphql
mutation {
    a: createUser(input: ...) { ... }
    b: createPost(input: ...) { ... }
}
```

- Same request
- Run in order
- Not transactional across them

---
## Errors

- Top-level errors array (transport)
- Or domain errors in payload (preferred)
- Distinguish: validation vs system errors

---
## Domain Errors Pattern

- Mutation always succeeds at transport layer
- Result: data or errors in payload
- Client handles both as data
- Fewer try/catches

---
## Idempotency

- Client-supplied key in input
- Server dedupes
- Critical for retries on flaky networks

---
## Optimistic Updates

- Client updates UI before server confirms
- Roll back on error
- Apollo / Relay support
- Better UX

---
## File Uploads

- GraphQL multipart spec
- Files alongside operation
- Apollo Server, others support

---
## Subscriptions for Side Effects

- Mutate; subscribe to changes
- Other clients see updates live
- Real-time apps

---
## Common Mutation Mistakes

- Returning bare scalars (Boolean) instead of payload
- Mixing transport errors and domain errors
- No input type; many positional args
- Mutation that returns nothing useful
- No idempotency for retryable operations
