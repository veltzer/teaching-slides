---
tags:
  - architecture:openapi
  - practices:codegen
level: intermediate
category: architecture
audience:
  - audiences:developers

---

# Code Generation From OpenAPI Specs

---

## What This Chapter Covers

- Why code generation
- OpenAPI Generator and swagger-codegen
- Generating server stubs
- Generating client SDKs
- Customising templates
- CI integration
- Keeping spec and code in sync

---

## Why Generate Code

- Reduces boilerplate
- Spec is the source of truth; code derives from it
- Spec change &#8594; regenerate &#8594; type errors at compile time
- Ensures consistency across services
- Saves hours per service

---

## Codegen Outputs

![codegen_flow](svg/courses/architecting/api-first-development/04_code_generation_from_openapi_specs/codegen_flow.svg)

---

## OpenAPI Generator

- Open-source, java-based, supports many languages
- `openapi-generator-cli generate -i spec.yaml -g python -o ./out`
- Languages: Python, TypeScript, Java, Go, C#, Rust, Kotlin, ...
- Server stubs and client SDKs in one tool
- The de facto standard

---

## swagger-codegen

- The original tool; OpenAPI Generator is a fork with more activity
- Some teams still use swagger-codegen
- Both work; pick OpenAPI Generator for new projects

---

## Generating Server Stubs

```bash
openapi-generator-cli generate \
  -i api-spec.yaml \
  -g spring \
  -o server/
```

- Spring Boot, FastAPI (`python-flask`), Express (`nodejs-express-server`), Go (`go-gin-server`)
- Generates: routing, request validation, response shapes
- You implement: business logic
- Pure routing scaffolding from the spec

---

## Server-Side Pattern

- Route handlers are generated as interfaces / abstract classes
- You implement them
- Regeneration overwrites only the generated parts
- Your implementation lives in separate files
- Standard pattern across languages

---

## Generating Client SDKs

```bash
openapi-generator-cli generate \
  -i api-spec.yaml \
  -g typescript-fetch \
  -o sdk/
```

- TypeScript, Python, Java, Swift, Kotlin, Go, ...
- Generated: typed methods per endpoint, models for schemas
- Consumers import the SDK; type errors at compile time
- Updates: regenerate on spec change

---

## Client SDK Example

```typescript
import { UsersApi, Configuration } from './generated';

const api = new UsersApi(new Configuration({ basePath: 'https://api.example.com' }));
const user = await api.getUser({ id: 42 });
// user is typed as User; id, name, email all known
```

---

## Customising Templates

- Default templates work; sometimes you want changes
- Override Mustache templates per-language
- Custom error handling, naming conventions, headers
- Investment: substantial; maintenance: ongoing
- Prefer customisation via *vendor extensions* (`x-*`) where possible

---

## CI Integration

- Spec change in PR &#8594; CI generates code &#8594; checks compile
- Some teams: commit generated code; CI verifies it's up to date
- Other teams: don't commit; generate at build time
- Both work; pick one
- Drift between spec and code = bugs

---

## Should You Commit Generated Code?

- **Pro commit**: build doesn't depend on having the generator; reviewers see the actual changes
- **Con commit**: noisy diffs; code is essentially a build artifact
- Most teams: commit if generated infrequently; generate on the fly if frequent
- Don't both commit *and* re-generate without verification

---

## Spec Validation In CI

- Run `spectral lint api-spec.yaml`
- Custom rules: required fields, naming patterns, security mandates
- Fail PRs that introduce spec violations
- Catches regressions automatically

---

## Spectral Rules

```yaml
rules:
  operation-tag-defined: error
  operation-summary: error
  no-200-error-responses: warn
  contact-properties: warn
```

- Comes with default rules; add your team's
- Extends the OpenAPI standard with team-specific style
- Lives in the repo: everyone sees the same rules

---

## Keeping Spec And Implementation In Sync

- Generated server stubs handle some of this
- Tests against the spec catch the rest
- Schemathesis: generates tests *from* the spec; runs against the running server
- Dredd: similar idea
- A real "the spec is enforced" mechanism

---

## Schemathesis

```bash
schemathesis run http://localhost:8000 \
  --schema-url http://localhost:8000/openapi.json
```

- Sends generated requests
- Verifies responses match the spec
- Catches: missing required fields, wrong types, status code mismatches
- Property-based testing for APIs

---

## Common Codegen Mistakes

- Hand-editing generated code (overwritten on next gen)
- No CI check; spec drifts from implementation
- Custom templates that bit-rot
- Generating into the wrong directory (gets committed accidentally)
- Treating the generator's output as final; it's a starting point

---

## Codegen Targets

![codegen_targets](svg/courses/architecting/api-first-development/04_code_generation_from_openapi_specs/codegen_targets.svg)
