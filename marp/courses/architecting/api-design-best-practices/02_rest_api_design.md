---
tags:
  - concepts:api
  - concepts:rest
level: intermediate
category: architecture
audience:
  - audiences:developers

---
# REST API Design

---
## What REST Is

- Roy Fielding's 2000 dissertation
- An architectural style, not a protocol or a framework
- A set of constraints that, when followed, produce well-behaved network APIs
- Stateless, cacheable, uniform interface, layered

---
## What REST Is Not

- Not the same as "HTTP API"
- Not the same as JSON over HTTP
- Not a framework
- Not the only good API style — gRPC and GraphQL are also valid

---
## REST in One Picture

![rest_principles](svg/courses/architecting/api-design-best-practices/02_rest_api_design/rest_principles.svg)

---
## Resources

- A resource is anything important enough to name and refer to
- Each resource has a URL
- Operations on resources use HTTP methods
- The resource is the noun; the method is the verb

---
## Resource-Oriented Design

- Identify the nouns in the domain
- Each noun becomes a resource (URL endpoint)
- Use plural nouns for collections: `/users`, `/orders`
- Use IDs for individual resources: `/users/42`

---
## HTTP Methods

| Method | Purpose | Idempotent | Safe |
|---|---|---|---|
| GET | Read | yes | yes |
| HEAD | Read headers only | yes | yes |
| POST | Create / process | no | no |
| PUT | Replace | yes | no |
| PATCH | Partial update | sometimes | no |
| DELETE | Remove | yes | no |

- Use them for what they mean

---
## Method Semantics in Practice

- `GET /users/42` — fetch user 42
- `POST /users` — create a new user; server assigns ID
- `PUT /users/42` — replace user 42 entirely
- `PATCH /users/42` — update some fields of user 42
- `DELETE /users/42` — remove user 42

---
## HTTP Status Codes

- **2xx success**: 200 OK, 201 Created, 204 No Content
- **3xx redirection**: 301 Moved, 304 Not Modified
- **4xx client error**: 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 409 Conflict, 422 Unprocessable Content, 429 Too Many Requests
- **5xx server error**: 500 Internal Error, 502 Bad Gateway, 503 Service Unavailable

---
## Status Code Discipline

- Use the right code; don't return 200 with `{"success": false}`
- 401 vs 403: 401 = "I don't know who you are"; 403 = "I know, and you can't"
- 404 vs 410: 404 = "doesn't exist"; 410 = "existed, now gone forever"
- 409 vs 422: 409 = state conflict; 422 = the request is malformed

---
## HATEOAS

- Hypermedia as the Engine of Application State
- Responses include links to related resources
- The client navigates by following links, not by hardcoding URLs
- Powerful in theory; rare in practice; usually overkill

---
## Why HATEOAS Is Rare

- Most clients are tightly coupled to specific endpoints anyway
- The benefit (discoverability) doesn't outweigh the cost (complex responses)
- API specs serve the same purpose more cheaply
- Skip HATEOAS unless you have a specific reason to use it

---
## Content Negotiation

- The client says what format it accepts (`Accept: application/json`)
- The server returns that format if possible
- Multiple formats from one endpoint: JSON, XML, MessagePack
- In practice: JSON is the default; supporting more is rarely necessary

---
## RESTful Examples

```http
GET    /orders                 # list
POST   /orders                 # create
GET    /orders/42              # read
PUT    /orders/42              # replace
PATCH  /orders/42              # update
DELETE /orders/42              # remove
GET    /orders/42/items        # nested list
POST   /orders/42/items        # add item
```

- Predictable; readable; consistent

---
## Anti-Patterns

- `POST /getUserById?id=42` — verbs in URLs
- `GET /users` returning 500 on no users — should be 200 with empty list
- `DELETE /users/42` returning the user — should be 204 No Content
- Status code 200 with `{"error": "not found"}` — should be 404

---
## Summary

- REST = resources + HTTP methods + status codes
- Resources are nouns; methods are verbs
- Use the right status code
- Skip HATEOAS unless you have a clear need
- Consistency in URL and method use trumps cleverness
