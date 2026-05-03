---
tags:
  - practices:technical-writing
  - practices:api-docs
level: beginner
category: methodology
audience:
  - audiences:developers

---
# API Documentation

---

## Application Programming Interface Sections

![api_doc_sections](svg/courses/development_methodologies/technical-writing/09_api_documentation/api_doc_sections.svg)

---
## What This Chapter Covers

- OpenAPI / Swagger specification
- Documenting REST APIs
- Request and response examples
- Error documentation
- API doc generators
- What good API docs look like

---
## Why API Docs Matter

- Users decide to integrate based on the docs
- Bad docs &#8594; support tickets &#8594; lost users
- Good docs &#8594; self-serve adoption &#8594; growth
- Most developers won't open a chat to ask
- Docs are the API's first impression

---
## Pieces of Good API Docs

![api_doc_pieces](svg/courses/development_methodologies/technical-writing/09_api_documentation/api_doc_pieces.svg)

---
## OpenAPI Specification

- Industry-standard format for REST APIs
- YAML or JSON
- Describes endpoints, parameters, responses, schemas
- Tooling generates: docs, client SDKs, mock servers, tests
- Most modern API platforms support it

---
## A Minimal OpenAPI Spec

```yaml
openapi: 3.0.3
info:
  title: Orders API
  version: 1.0.0
paths:
  /orders/{id}:
    get:
      summary: Get one order by ID
      parameters:
        - name: id
          in: path
          required: true
          schema: { type: integer }
      responses:
        '200':
          description: The order
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Order'
```

---
## Per-Endpoint Documentation

- **Summary**: one line; what it does
- **Description**: more detail if needed
- **Parameters**: each one named, typed, described
- **Request body**: schema, examples
- **Responses**: per status code; schema, examples
- **Errors**: explicit list of error codes

---
## Schemas

- Define the shape of request and response bodies
- Reusable: define `Order` once, reference everywhere
- Includes: types, required fields, descriptions, examples
- Validation tools use these
- The single source of truth for API contracts

---
## Examples In API Docs

- Concrete example for every endpoint
- Both request and response
- Realistic data
- Common scenarios first
- "Try it out" widgets in modern API docs

---
## Documenting Authentication

- Once at the top, then per-endpoint if relevant
- API keys, OAuth, JWT — say which
- Where the token goes (header, query, body)
- How to obtain a token
- Sample auth headers

---
## Error Documentation

- List every error code that can be returned
- Per-error: when it happens, what to do about it
- Don't just document HTTP status codes — document the *application* errors
- "402 Payment Required: trial expired; upgrade plan"
- Most APIs under-document errors; users get stuck

---
## Versioning

- Document which version applies
- Deprecation notes inline
- Migration guides between versions
- Tools support multi-version sites
- Don't make users guess

---
## API Doc Generators

- **Swagger UI**: classic interactive docs from OpenAPI
- **Redoc**: cleaner alternative
- **Stoplight**: commercial, full lifecycle
- **Slate**: three-pane scrollable docs (Stripe-style)
- **Docusaurus + plugin**: docs site with API integration

---
## Auto-Generated Docs

- From source code annotations (Java, Python, Go)
- From OpenAPI spec
- Best with: spec is the source of truth, code follows
- Worst: spec drifts from implementation
- Test the spec in CI by hitting the actual API

---
## Stripe-Style Docs

- Three-pane layout: navigation, prose, code examples
- Examples in multiple languages, side by side
- Inline tutorials
- Famous example of API doc design done right
- Tools: Slate, Mintlify, custom

---
## Common Sections

- Getting started
- Authentication
- Endpoint reference
- Error reference
- Rate limits
- Webhooks (if applicable)
- Versioning policy
- Changelog

---
## Beyond REST

- GraphQL: introspection generates docs
- gRPC: `.proto` files are the schema; `protoc-gen-doc` generates docs
- WebSockets: documented manually
- Event-driven: AsyncAPI specification
- Each pattern has its own docs convention

---
## SDK Documentation

- Many APIs ship official SDKs
- SDK docs separate from API reference
- Code examples in the SDK's language
- Class / function reference (often auto-generated)
- Tutorials specific to the SDK

---
## Common API Doc Mistakes

- Out-of-date spec
- No examples
- Errors mentioned but not documented
- Auth flow buried somewhere
- "Try it out" widgets that don't actually work
- Spec different from implementation behaviour
