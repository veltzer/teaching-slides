---
tags:
  - networking:rest
  - practices:design
level: intermediate
category: networking
audience:
  - audiences:developers

---
# Resource Design

---
## What This Chapter Covers

- URL design
- Collections vs singletons
- Nesting
- Query parameters
- Filtering, sorting, pagination

---
## URLs Are Nouns

- /users, /orders, /products
- Plural collections
- Specific resource: /users/123
- No verbs

---
## Do This / Avoid This

![url_design](svg/courses/networking/restful-apis/04_resource_design/url_design.svg)

---
## Hierarchical Resources

- /users/123/orders
- /orders/456/items
- Express ownership
- Don't nest more than 2 levels

---
## Collections

- GET /users: list
- POST /users: create
- Filter via query params
- Paginate

---
## Singletons

- GET /users/123: read
- PUT /users/123: replace
- PATCH /users/123: update
- DELETE /users/123: remove

---
## Sub-resources

- GET /users/123/avatar
- For: tightly coupled child data
- Operations on the relationship

---
## Filtering

- Query params: ?status=active
- Multiple: ?status=active&role=admin
- Standard for collections
- Not in path

---
## Sorting

- ?sort=created_at
- Direction: ?sort=created_at&order=desc
- Or: ?sort=-created_at
- Pick a convention; document

---
## Pagination

- Offset / limit: ?page=2&size=20
- Cursor: ?after=abc123
- Cursor scales better
- Always include total or next-link

---
## Searching

- ?q=foo: simple
- Or dedicated /search endpoint
- Beyond filters: full-text

---
## Field Selection

- ?fields=id,name
- Reduces payload
- Common at scale
- GraphQL solves this natively

---
## Bulk Operations

- POST /users with array
- Or: dedicated /users/bulk
- Errors: per-item status
- Document semantics

---
## Async Operations

- Long-running: 202 Accepted
- Return job URL
- Poll or webhook for result

---
## Naming Conventions

- snake_case or camelCase: pick one
- Consistent across the API
- Plural collections
- Lowercase URLs

---
## Common Resource Design Mistakes

- Verbs in URLs (/getUser, /createOrder)
- Inconsistent pluralisation
- Deep nesting (/a/b/c/d/e)
- Mixing snake_case and camelCase
- Filtering in path instead of query
