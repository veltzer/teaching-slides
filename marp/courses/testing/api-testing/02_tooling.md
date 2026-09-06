---
tags:
  - testing:api
level: intermediate
category: testing
audience:
  - audiences:qa

---

# Tooling

---

## What This Chapter Covers

- Postman ecosystem
- Code-first frameworks
- Spec-driven tools
- Mocking and stubbing
- Choosing tools

---

## Tool Landscape

![tool_landscape](svg/courses/testing/api-testing/02_tooling/tool_landscape.svg)

---

## Postman

- GUI client + scripting
- Collections of requests
- Environment variables
- Newman runs in CI
- Standard for manual + light automation

---

## Postman Collections

- Group of related requests
- Per-environment variables
- Pre-request and test scripts (JS)
- Shareable

---

## Newman

- CLI runner for Postman collections
- Run in CI / cron
- HTML / JUnit reports

---

## From Manual to Automated

![tool_workflow](svg/courses/testing/api-testing/02_tooling/tool_workflow.svg)

---

## Insomnia

- Postman alternative
- Cleaner UI
- Built-in plugin model

---

## Code-First: REST-assured

- Java DSL for HTTP tests
- Fluent given/when/then
- Use existing test runner (JUnit)

---

## Code-First: supertest

- Node.js
- Express-compatible
- Pairs with Mocha / Jest

---

## Code-First: requests + pytest

- Python ecosystem
- Plain code; full power
- Test infra reuses stdlib

---

## Spec-Driven: Schemathesis

- Generates tests from OpenAPI
- Property-based fuzzing
- Finds: schema violations, panics, edge cases

---

## Spec-Driven: Dredd

- Tests API against spec
- Each example exercised
- Quick contract check

---

## Karate

- Single-language DSL across HTTP, gRPC, web
- Java-based runner
- Strong for QA teams

---

## Mocking

- WireMock: programmable HTTP mocks
- Mockoon: GUI mock server
- Prism: from OpenAPI

---

## Service Virtualisation

- Stand in for unavailable services
- Used in test environments
- Useful when real backend is slow / costly

---

## Performance Tools

- k6: scripts, modern
- JMeter: GUI + plugins
- Locust: Python-based, distributed

---

## Choosing

- Manual + dev: Postman / Insomnia
- Code-first teams: language-native
- Spec-rich: spec-driven
- One tool can do it all; usually a mix

---

## Common Tooling Mistakes

- Postman without source-controlled collections
- Tests in Postman GUI but not in CI
- Code-first tests with no shared base
- Mocks drifting from real API behavior
- One giant collection; nobody runs it
