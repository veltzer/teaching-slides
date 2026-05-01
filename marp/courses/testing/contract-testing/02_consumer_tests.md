---
tags:
  - testing:contract
level: intermediate
category: testing
audience:
  - audiences:developers
  - audiences:testers

---
# Consumer Tests

---
## What This Chapter Covers

- Anatomy
- Mock provider
- Defining interactions
- Examples
- Pitfalls

---
## Anatomy

- Pre-conditions on the provider
- Request your code makes
- Expected response
- All in test code

---
## Mock Provider

- Library spins up local mock
- Your code calls it like real provider
- Mock matches expected request
- Returns canned response

---
## Pre-Conditions

- Set up provider state
- "User 42 exists"
- "Cart is empty"
- Provider verifies these later

---
## Defining Interactions

- One per scenario
- Happy path
- Error responses
- Edge cases

---
## Choosing What To Verify

- Fields you read
- Status codes you handle
- Headers you depend on
- Skip fields you do not use

---
## Loose Matching

- Match by type, not exact value
- Match by regex for patterns
- Avoid coupling to volatile values
- More resilient contracts

---
## Strict Matching

- Exact string equality
- Use sparingly
- Useful for enums or known constants
- Brittle otherwise

---
## Provider States

- Named states
- Configured per interaction
- Provider verifies it can produce them
- Linked back to test fixtures

---
## Generating The Contract

- Tool emits a JSON file
- One per consumer-provider pair
- Stored in a broker or repo
- Versioned with consumer code

---
## Running The Tests

- Like normal unit tests
- No network calls
- Fast and reliable
- Block PRs on failure

---
## Updating Tests

- New interaction
- Changed shape
- Old interactions removed
- Communicate to provider before merge

---
## Examples Beyond Happy Path

- 4xx responses
- 5xx with retry semantics
- Timeouts where applicable
- Pagination

---
## Coverage

- Cover all calls your code makes
- Per service-to-service pair
- Per environment if behaviors differ
- Refresh as code evolves

---
## Common Consumer Mistakes

- Over-specifying response fields
- Strict matching everywhere
- Skipping error responses
- Stale interactions kept around
- Coupling to ephemeral values
