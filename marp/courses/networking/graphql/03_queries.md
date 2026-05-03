---
tags:
  - networking:graphql
level: intermediate
category: networking
audience:
  - audiences:developers

---
# Queries

---
## What This Chapter Covers

- Basic queries
- Arguments
- Aliases
- Fragments
- Variables
- Operation names

---
## GraphQL vs REST

![graphql_vs_rest](svg/courses/networking/graphql/03_queries/graphql_vs_rest.svg)

---
## Query Features

![query_features](svg/courses/networking/graphql/03_queries/query_features.svg)

---
## Basic Query

```graphql
query {
    users {
        id
        name
    }
}
```

- Field selection
- Server returns matching shape

---
## Nested Selection

```graphql
{
    user(id: "123") {
        name
        posts {
            title
            comments {
                text
            }
        }
    }
}
```

- Traverse relationships
- Single round trip

---
## Arguments

```graphql
{
    user(id: "123") { ... }
    posts(limit: 10, offset: 0) { ... }
}
```

- Per-field
- Defined in schema

---
## Aliases

```graphql
{
    me: user(id: "123") { name }
    you: user(id: "456") { name }
}
```

- Multiple of same field
- Disambiguate response

---
## Fragments

```graphql
fragment UserFields on User {
    id
    name
    email
}

{
    user(id: "1") { ...UserFields }
}
```

- Reusable selection
- DRY

---
## Inline Fragments

```graphql
{
    search(q: "x") {
        __typename
        ... on User { name }
        ... on Post { title }
    }
}
```

- Type-conditional selection
- For unions and interfaces

---
## Variables

```graphql
query GetUser($id: ID!) {
    user(id: $id) { name }
}
```

- Parameterise queries
- Variables passed alongside query
- Better than string interpolation

---
## Operation Names

- `query GetUser { ... }` not just `{ ... }`
- Required for variables
- Helps logging and debugging

---
## Default Values

```graphql
query Posts($limit: Int = 10) {
    posts(limit: $limit) { id }
}
```

- Variable defaults
- Schema arg defaults too

---
## Introspection

- `__schema`, `__type`
- Discover the API
- Enables tooling

---
## Why Field Selection Wins

- Each consumer fetches only needed fields
- Saves bandwidth on mobile
- One round trip for nested data

---
## Common Query Mistakes

- Asking for too many fields by habit
- Not using fragments; duplication
- Missing operation name; lost in logs
- Building queries via string concat instead of variables
- Deeply nested queries that nobody reviews
