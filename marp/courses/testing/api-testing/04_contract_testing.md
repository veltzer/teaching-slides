---
tags:
  - testing:api
level: intermediate
category: testing
audience:
  - audiences:qa
  - audiences:developers

---
# Contract Testing

---
## Pact Flow

![pact_flow](svg/courses/testing/api-testing/04_contract_testing/pact_flow.svg)

---
## What This Chapter Covers

- Contracts and consumers
- Pact
- Spec-based contract tests
- Provider verification
- CI integration

---
## What a Contract Is

- Agreement on request and response shape
- Between consumer and provider
- Enforced via tests

---
## Why Contract Tests

- Provider changes break consumers silently
- E2E catches but is slow / flaky
- Contract tests fast and targeted

---
## Pact

- Consumer-driven contract testing
- Consumer writes expectations
- Provider verifies against them
- Ruby origin; many language clients

---
## Pact Flow

- Consumer test runs against mock
- Generates pact file
- Pact file shared via broker
- Provider verifies pact

---
## Sample Consumer (Pseudo)

- Set up Pact mock
- Define expected interaction
- Run consumer code against mock
- Pact file written

---
## Sample Provider (Pseudo)

- Load pact file
- Replay requests against real provider
- Assert real responses match

---
## Pact Broker

- Central store of pacts
- Versioned
- "Can-i-deploy" check
- CI integration

---
## Spec-Based Contract

- OpenAPI as the contract
- Validate provider responses against spec
- Validate consumer requests against spec
- No separate pact file

---
## Schemathesis

- From OpenAPI spec
- Generates test cases
- Property-based fuzzing
- Finds drift quickly

---
## Provider Verification

- Real provider receives recorded requests
- Compare actual response to expected
- Run in CI

---
## Versioning Contracts

- Tag pact with consumer version
- Provider verifies compatibility per version
- Supports gradual rollout

---
## Coverage

- Contract tests cover shape, not full logic
- Pair with functional tests
- Together: confidence

---
## Cross-Team Workflow

- Producer and consumer different teams
- Contract published; verified per change
- Block deploys on broken contract

---
## Common Contract-Testing Mistakes

- Replacing all tests with contracts
- No broker; pacts lost
- Contract tests on hot UI loop, not API
- Verifying against mock, not real provider
- Skipping verification step
