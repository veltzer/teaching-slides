---
tags:
  - networking:rest
  - practices:documentation
level: intermediate
category: networking
audience:
  - audiences:developers

---
# Documentation and OpenAPI

---
## What This Chapter Covers

- Why API docs matter
- OpenAPI specification
- Tooling
- Code generation
- Mock servers

---
## Why Docs Matter

- API is its docs to consumers
- Bad docs: bad adoption
- Good docs: faster integration
- Source of truth

---
## OpenAPI

- Specification for HTTP APIs
- YAML or JSON
- Describes endpoints, schemas, auth
- Formerly Swagger

---
## What OpenAPI Captures

- Paths and methods
- Parameters
- Request and response schemas
- Status codes
- Authentication

---
## Sample OpenAPI

```yaml
openapi: 3.0.0
info:
  title: Users API
  version: 1.0.0
paths:
  /users/{id}:
    get:
      summary: Get user
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: OK
```

---
## Schemas

- Reusable types under components/schemas
- $ref to reference
- DRY across endpoints
- Drives codegen

---
## Swagger UI

- HTML viewer for OpenAPI
- Interactive: try requests
- Bundle with API or host separately
- Standard for API docs

---
## Other Viewers

- Redoc: read-only, polished
- Stoplight: editor + docs
- Built-in to many frameworks

---
## Code Generation

- OpenAPI Generator: clients in many languages
- Server stubs
- Saves boilerplate
- Quality varies by language

---
## Spec-First vs Code-First

- Spec-first: write OpenAPI, generate code
- Code-first: write code, generate spec
- Spec-first: better contract discipline
- Code-first: easier to maintain

---
## Mock Servers

- Generate from OpenAPI
- Frontend can develop without backend
- Examples in spec drive responses
- Prism, Stoplight

---
## Validation

- Validate requests against schema at gateway
- Validate server responses in tests
- Catch contract violations early

---
## Beyond Reference

- Tutorials
- Quickstart
- Use cases / recipes
- Changelog
- Reference is necessary, not sufficient

---
## Common Documentation Mistakes

- Auto-generated docs without examples
- Spec drifting from implementation
- No quickstart for new users
- Missing error responses in spec
- Tutorial only for happy path

---
## OpenAPI Document Pieces

![openapi_pieces](svg/courses/networking/restful-apis/08_documentation_and_openapi/openapi_pieces.svg)
