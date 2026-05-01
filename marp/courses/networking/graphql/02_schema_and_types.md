---
tags:
  - networking:graphql
level: intermediate
category: networking
audience:
  - audiences:developers

---
# Schema and Types

---
## What This Chapter Covers

- Type system
- Object types
- Scalars
- Enums
- Interfaces and unions
- Input types

---
## Schema Definition Language

- SDL: human-readable
- Standard format
- Tools generate code from SDL

---
## Object Types

```graphql
type User {
    id: ID!
    name: String!
    email: String
    posts: [Post!]!
}
```

- Fields with types
- ! means non-null
- [] means list

---
## Scalar Types

- ID, String, Int, Float, Boolean
- Built-in
- Custom scalars: Date, JSON, URL
- Encoded in JSON

---
## Enums

```graphql
enum Status {
    PENDING
    ACTIVE
    SUSPENDED
}
```

- Fixed set of values
- Type-safe

---
## Lists and Nullability

- [Post!]!: non-null list of non-null posts
- [Post!]: nullable list of non-null posts
- [Post]!: non-null list of nullable posts
- Pick deliberately

---
## Interfaces

```graphql
interface Node {
    id: ID!
}

type User implements Node {
    id: ID!
    name: String!
}
```

- Common fields
- Polymorphism

---
## Unions

```graphql
union SearchResult = User | Post | Comment
```

- One of several types
- No common fields
- Client must check `__typename`

---
## Input Types

```graphql
input CreateUserInput {
    name: String!
    email: String!
}
```

- For mutation arguments
- Cannot have resolvers
- Reusable

---
## Query Type

```graphql
type Query {
    user(id: ID!): User
    users: [User!]!
}
```

- Entry point for reads
- Required

---
## Mutation Type

```graphql
type Mutation {
    createUser(input: CreateUserInput!): User!
}
```

- Entry point for writes
- Optional but standard

---
## Subscription Type

- Entry point for live updates
- Returns stream of events
- Uses WebSocket or SSE

---
## Directives

- @deprecated, @include, @skip
- Modify schema or query behavior
- Custom directives possible

---
## Common Schema Mistakes

- Overusing nullable; clients break unexpectedly
- Underusing nullable; cascading failures
- Reusing object types as input
- No naming conventions
- Schema drift between teams
