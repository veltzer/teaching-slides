---
tags:
  - concepts:api
  - concepts:best-practices
level: intermediate
category: architecture
audience:
  - audiences:developers

---

# API Documentation

---

## Why Documentation Matters

- An undocumented API is a hostile API
- Consumers need to know what's available, how to call it, what to expect
- Good docs reduce support burden
- A well-documented API onboards developers in minutes; a bad one takes days

---

## Doc Practices

![doc_practices](svg/courses/architecting/api-design-best-practices/08_api_documentation/doc_practices.svg)

---

## Documentation Audiences

![doc_audiences](svg/courses/architecting/api-design-best-practices/08_api_documentation/doc_audiences.svg)

---

## OpenAPI / Swagger

- The de facto standard for HTTP API specs
- A YAML or JSON file describing endpoints, parameters, request/response schemas
- Machines can generate clients, mocks, validators from it
- Humans can read it (tooling makes it pleasant)

---

## OpenAPI Sketch

```yaml
openapi: 3.0.3
info:
  title: Order API
  version: 1.0.0
paths:
  /orders/{order_id}:
    get:
      summary: Fetch an order
      parameters:
        - name: order_id
          in: path
          required: true
          schema: { type: string }
      responses:
        '200':
          description: Order found
          content:
            application/json:
              schema: { $ref: '#/components/schemas/Order' }
```

---

## What to Document Per Endpoint

- HTTP method and path
- Summary (one-line description)
- Detailed description (when to use, edge cases)
- Parameters (path, query, header)
- Request body schema with example
- Response schema with example for each status code
- Possible errors

---

## Schema Definitions

- Define request and response schemas as named components
- Reuse across endpoints
- Each schema has fields, types, constraints, descriptions
- A change in the schema is visible in the diff

---

## Examples Are Critical

- A schema without examples is a guess
- Realistic example values for every field
- Multiple examples for variants ("a paid order", "a refunded order")
- Tools can generate mock servers from examples

---

## Code Generation

- OpenAPI → client SDKs in many languages
- OpenAPI → server stubs
- OpenAPI → request validation middleware
- The spec is leverage; treat it as a first-class artifact

---

## Documentation Portals

- A web UI for browsing the API
- Examples: Swagger UI, Redoc, Stoplight
- Searchable, navigable, often with "try it" buttons
- Hosted alongside the API or on a docs site

---

## Keeping Docs in Sync With Code

- The hardest problem
- Two strategies:
    - **Spec-first**: write the spec, generate code, manual updates rare
    - **Code-first**: annotate code, generate the spec
- Spec-first is more disciplined; code-first is more pragmatic

---

## Spec-First Workflow

- Write or modify the OpenAPI spec
- Generate server stubs (or update by hand)
- Implement the endpoints
- Run contract tests against the spec
- Spec is the source of truth

---

## Code-First Workflow

- Annotate routes with metadata: parameters, responses, examples
- A library generates the OpenAPI spec from annotations
- Examples: FastAPI (Python), Springdoc (Java), NSwag (.NET)
- The code is the source of truth; the spec is a derivative

---

## What Belongs Outside the Spec

- Tutorials and onboarding guides
- Authentication setup walkthroughs
- Common workflows (multi-step examples)
- Versioning and migration guides
- These are prose, not spec

---

## A Two-Layer Documentation Set

- Reference: generated from the spec — every endpoint, every field
- Guides: hand-written prose for common tasks
- Both are needed; they serve different audiences

---

## API Design Reviews

- Review the API spec before implementation
- Check: naming, consistency, error semantics, versioning
- Catches problems while they're still cheap to fix
- Establishes a culture of intentional design

---

## Anti-Patterns

- "The code is the documentation"
- Outdated examples that no longer work
- Documentation in a wiki separate from the spec
- Per-endpoint documentation styles that diverge over time
- Documentation that needs more documentation to use

---

## Summary

- OpenAPI is the standard; use it
- Spec-first gives discipline; code-first gives pragmatism
- Examples make schemas useful
- Generated reference + hand-written guides = full coverage
- Keeping docs in sync is a process problem, not a tool problem
