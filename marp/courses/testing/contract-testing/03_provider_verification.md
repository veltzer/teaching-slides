---
tags:
  - testing:contract
level: intermediate
category: testing
audience:
  - audiences:developers
  - audiences:testers

---
# Provider Verification

---
## What This Chapter Covers

- Verification flow
- Provider states
- Setup and teardown
- Real provider
- CI integration

---
## What Verification Does

- Replay each consumer interaction
- Against the real provider
- Compare actual responses
- Pass or fail per interaction

---
## Verification Run

![verification_run](svg/courses/testing/contract-testing/03_provider_verification/verification_run.svg)

---
## Where It Runs

- In provider CI
- On every change
- On every pull request
- Block merges on failure

---
## Real Provider

- Actual code paths
- Real handlers
- Stubbed external dependencies
- Otherwise it is integration testing

---
## Provider States

- Translate named state to setup steps
- "User 42 exists" sets up the row
- Cleanup after each interaction
- Repeatable

---
## Setup And Teardown

- Database fixtures
- In-memory caches
- Mocked downstreams
- Reset between runs

---
## Mocking Downstreams

- Provider tests should not call other services
- Stub responses
- Or use in-memory fakes
- Keeps tests fast

---
## Pulling Contracts

- From broker
- Filtered by branch tag
- Or from a directory
- Document the source

---
## Versioning

- Contracts versioned by consumer
- Verifications recorded with provider version
- Brokers track combinations
- Useful for compatibility matrix

---
## Failure Modes

- Field missing
- Wrong type
- Wrong status code
- Wrong header

---
## Fixing Failures

- Producer change broke contract
- Consumer expectations wrong
- Or both
- Coordinate

---
## Coordinated Releases

- Provider deploys ahead of consumer
- Consumer can use new fields
- Broker tracks compatibility
- Avoid coupled deploys when possible

---
## Backward Compatibility

- Avoid breaking changes
- Add fields, do not rename
- Deprecate before removing
- Document support windows

---
## CI Integration

- Run on every PR
- Quick feedback to provider team
- Block merges on regression
- Tag verifications with branch

---
## Common Provider Mistakes

- Calling real downstreams
- Slow setup per interaction
- Skipping verification on PRs
- Breaking changes without coordination
- No compatibility tracking
