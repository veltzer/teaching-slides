---
tags:
  - architecture:openapi
  - practices:contract-testing
level: intermediate
category: architecture
audience:
  - audiences:developers

---
# Mock Servers and Contract Testing

---
## Contract Testing

![contract_testing](svg/courses/architecting/api-first-development/05_mock_servers_and_contract_testing/contract_testing.svg)

---
## What This Chapter Covers

- Mock servers from OpenAPI specs
- Prism, WireMock, and alternatives
- Consumer-driven contract testing with Pact
- Producer contract testing
- Integration with CI
- The "tests against the spec" pattern

---
## Why Mock Servers

- Frontend / consumers need an API to develop against
- Backend isn't ready yet
- A mock server fills the gap
- Generated from the OpenAPI spec; matches the contract
- Replaces "wait for the backend" with "build in parallel"

---
## Prism

```bash
npm install -g @stoplight/prism-cli
prism mock api-spec.yaml -p 4010
```

- Reads OpenAPI; serves a mock at localhost:4010
- Returns example values from the spec
- Validates incoming requests against the spec
- Free, easy, the most common choice

---
## What Prism Returns

- If the spec has `example`: that
- Otherwise: synthesised data based on schema (random or default)
- Multiple examples: round-robin or by `Prefer` header
- Behaves like a real API for the frontend's perspective
- Errors when the request doesn't match the spec

---
## WireMock

- Java-based mock server; very flexible
- Records and replays real HTTP traffic
- Supports stub matching beyond OpenAPI
- More setup; more power
- Good for: complex scenarios, stateful mocks

---
## Mock Limitations

- Mocks return canned data; they don't have real business logic
- Two GETs return identical data unless you script it
- Use mocks for development; real servers for integration tests
- Don't test business logic against a mock

---
## Contract Testing

- Verify the *agreement* between producer and consumer
- Different from end-to-end testing
- Each side tests its assumptions about the contract
- Catches breakages without running both sides together
- Critical for microservices

---
## Consumer-Driven Contract Testing

- Consumer writes tests that capture expectations
- Producer verifies those expectations
- Failed verification = breaking change for the consumer
- Pact is the leading tool

---
## Pact Workflow

- Consumer test: "When I call POST /users with X, I expect 200 and Y"
- Pact records the interaction as a pact file (JSON)
- Pact file shared via Pact Broker
- Producer's test: "Given my code, can I satisfy this pact?"
- Producer fails CI if it can't

---
## Pact Consumer Example

```javascript
provider
  .uponReceiving('a request for user 42')
  .withRequest({ method: 'GET', path: '/users/42' })
  .willRespondWith({
    status: 200,
    body: { id: 42, name: 'Alice' }
  });

const user = await client.getUser(42);
expect(user.name).toBe('Alice');
```

---
## Pact Producer Verification

```bash
pact-verifier --provider-base-url=http://localhost:8080 \
              --pact-broker-url=https://broker.example.com
```

- Runs against your local producer
- Pulls pacts from the broker
- Replays each interaction
- Verifies the response matches the consumer's expectation
- Fails if anything diverges

---
## OpenAPI vs Pact

- **OpenAPI**: defines the *spec* (what's possible)
- **Pact**: defines the *interactions* (what consumers actually use)
- Both have a place
- OpenAPI for general structure; Pact for specific consumer needs
- Sometimes you need both

---
## Schemathesis

- Generates tests from OpenAPI; runs against the producer
- Like property-based testing for APIs
- Catches: spec drift, off-spec responses, invalid edge cases
- Runs in CI; catches regressions

---
## CI Integration

- Mock server: spin up in CI for end-to-end frontend tests
- Pact verification: run on every backend PR
- Schemathesis: run periodically (slow but thorough)
- Spec linting: every PR
- Together: high confidence the API works as designed

---
## A Realistic Workflow

- Consumer team writes Pact tests
- Pact files published to Pact Broker
- Producer's CI verifies all consumer pacts
- Producer's CI also runs Schemathesis
- Producer ships: passes both

---
## Common Mock and Contract Mistakes

- Mocks too "smart" — frontend depends on behaviour the real API doesn't have
- No CI for Pact; consumer tests pass; producer breaks consumers anyway
- Schemathesis tests skipped because slow; regressions slip through
- Treating mocks as authoritative
- Forgetting Pact when removing endpoints

---
## Mock Realism Levels

![mock_levels](svg/courses/architecting/api-first-development/05_mock_servers_and_contract_testing/mock_levels.svg)
