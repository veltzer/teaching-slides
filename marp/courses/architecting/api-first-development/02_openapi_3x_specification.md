---
tags:
  - architecture:openapi
level: intermediate
category: architecture
audience:
  - audiences:developers

---

# OpenAPI 3.x Specification

---

## Document Structure

![openapi_structure](svg/courses/architecting/api-first-development/02_openapi_3x_specification/openapi_structure.svg)

---

## What This Chapter Covers

- The OpenAPI document structure
- Paths, operations, parameters
- Request bodies and response definitions
- Reusable components
- JSON Schema for validation
- Authentication
- Tooling

---

## Document Structure

```yaml
openapi: 3.0.3
info:
  title: My API
  version: 1.0.0
servers:
  - url: https://api.example.com
paths:
  /users:
    get: ...
components:
  schemas: ...
```

- `info`: metadata
- `servers`: where the API lives
- `paths`: every endpoint
- `components`: reusable definitions

---

## Paths and Operations

```yaml
paths:
  /users/{id}:
    get:
      summary: Get one user
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: User found
```

- One entry per URL
- One operation per HTTP method (get, post, put, patch, delete)

---

## Parameters

- **path**: in the URL (`/users/{id}`)
- **query**: after `?` (`?limit=10`)
- **header**: HTTP header
- **cookie**: cookie value
- Each typed; documented; required-or-not

---

## Request Bodies

```yaml
post:
  requestBody:
    required: true
    content:
      application/json:
        schema:
          $ref: '#/components/schemas/User'
      multipart/form-data:
        schema:
          type: object
          properties:
            file:
              type: string
              format: binary
```

- Multiple content types per body
- Schema validates the structure
- File uploads via `multipart/form-data`

---

## Response Definitions

```yaml
responses:
  '200':
    description: Success
    content:
      application/json:
        schema:
          $ref: '#/components/schemas/User'
  '404':
    description: Not found
  '422':
    description: Validation error
```

- One per status code (or pattern: `2XX`, `4XX`, `5XX`)
- Each documents content, headers
- Errors deserve documentation as much as success

---

## Reusable Components

```yaml
components:
  schemas:
    User:
      type: object
      properties:
        id: { type: integer }
        name: { type: string }
        email: { type: string, format: email }
      required: [id, name]
```

- Define once; reference with `$ref`
- Schemas, parameters, responses, request bodies, headers all reusable
- Keeps the spec DRY

---

## JSON Schema for Validation

- OpenAPI uses (a subset of) JSON Schema
- Types: integer, number, string, boolean, array, object
- Format: email, uuid, date-time, ipv4, etc.
- Constraints: minLength, maxLength, pattern, minimum, maximum
- Enums: `enum: [active, inactive, banned]`

---

## Schemas Example

```yaml
schemas:
  Order:
    type: object
    required: [id, customer_id, items]
    properties:
      id: { type: string, format: uuid }
      customer_id: { type: integer }
      total: { type: number, minimum: 0 }
      items:
        type: array
        items:
          $ref: '#/components/schemas/OrderItem'
        minItems: 1
```

---

## Authentication

```yaml
components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
    apiKey:
      type: apiKey
      in: header
      name: X-API-Key

security:
  - bearerAuth: []
```

- Top-level `security`: applies to all operations
- Per-operation `security`: overrides
- OAuth2 / OpenID Connect supported

---

## Links and Callbacks

- **Links**: navigate from one operation to another (HATEOAS-like)
- **Callbacks**: define webhooks the API will call
- Less commonly used; useful for complex APIs
- Documents the *interaction*, not just the endpoints
- Most teams skip these; they're powerful when applied

---

## Documentation Fields

- `summary`: one-liner for the operation
- `description`: longer; supports CommonMark Markdown
- `example`: concrete value for a schema
- `tags`: group operations in the rendered docs
- Take the time to write these well; users see them

---

## Examples In Specs

```yaml
schemas:
  User:
    type: object
    properties:
      name: { type: string, example: "Alice" }
      role: { type: string, example: "admin" }
    example:
      name: Alice
      role: admin
```

- Per-property: short
- Whole-object: realistic
- Multiple examples: `examples` (plural) with names
- Renderers (Swagger UI) show these in the docs

---

## Tooling

- **Swagger Editor**: web-based editor with live validation
- **Stoplight Studio**: GUI editor; commercial
- **VS Code OpenAPI extensions**: in-editor validation
- **Spectral**: lint your specs against rules
- **Swagger UI / Redoc**: render to a doc site

---

## Common Spec Mistakes

- Required fields not marked required
- Missing `description` everywhere — bare types are not docs
- Inconsistent error response shapes
- $ref typos (broken references)
- Validating only manually; should run in CI

---

## components Section Layout

![components_section](svg/courses/architecting/api-first-development/02_openapi_3x_specification/components_section.svg)
