---
tags:
  - practices:devops
  - concepts:architecture
  - practices:ci-cd
  - infrastructure:infrastructure-as-code
level: advanced
category: devops
audience:
  - audiences:architects
  - audiences:devops
  - audiences:managers

---
# Testing Strategy Tradeoffs
Balancing speed, cost, and confidence in CI/CD testing

---

## Why Testing Strategy Matters

- Testing consumes a significant portion of pipeline time
- Wrong balance leads to slow pipelines or escaped bugs
- Each test type has different maintenance costs
- Strategy must evolve with architecture and team size

---

## The Test Pyramid

![the_test_pyramid](svg/courses/devops/architectural-decisions-in-devops/15_testing_strategy_tradeoffs/the_test_pyramid.svg)

---

## Unit Tests in CI/CD

- Run on every commit or pull request
- Execute in seconds to low minutes
- No external dependencies required
- Validate individual functions and classes
- Highest return on investment for most projects

---

## Unit Test Tradeoffs

| Advantage | Disadvantage |
|-----------|-------------|
| Fast execution | Miss integration issues |
| Easy to write | Can become tightly coupled to implementation |
| Cheap to run | False sense of confidence |
| Great for TDD | Do not test real user flows |

---

## Integration Tests in CI/CD

- Validate interactions between components
- Require databases, APIs, or message queues
- Run after unit tests pass in the pipeline
- Typical execution: minutes to tens of minutes
- Environment setup and teardown adds overhead

---

## End-to-End Tests in CI/CD

- Simulate real user interactions across the full stack
- Longest execution time in the pipeline
- Most brittle and expensive to maintain
- Run less frequently (nightly, pre-release)
- Catch cross-service and UI-level defects

---

## Maintenance Cost by Test Level

![maintenance_cost_by_test_level](svg/courses/devops/architectural-decisions-in-devops/15_testing_strategy_tradeoffs/maintenance_cost_by_test_level.svg)

---

## Finding the Right Balance

- No single correct ratio; depends on architecture
- Microservices: heavier on integration and contract tests
- Monoliths: heavier on unit tests with selective E2E
- Google's suggested ratio: 70% unit, 20% integration, 10% E2E
- The Testing Trophy alternative emphasizes integration for UI apps

---

## Shift-Left Testing Overview

![shift_left_testing_overview](svg/courses/devops/architectural-decisions-in-devops/15_testing_strategy_tradeoffs/shift_left_testing_overview.svg)

---

## Cost of Defects Over Time

- Bug found during coding: cost = `1x`
- Bug found during build: cost = `5x`
- Bug found during QA: cost = `15x`
- Bug found in staging: cost = `50x`
- Bug found in production: cost = `100x` or more

---

## Static Analysis in Pipelines

- Runs without executing code
- Catches type errors, unused variables, dead code
- Tools: `ESLint`, `Pylint`, `SonarQube`, `golangci-lint`
- Should block merges on critical violations
- Fast execution, typically under 1 minute

---

## Static Analysis Pipeline Example

```yaml
name: Static Analysis
on: [pull_request]
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm install
      - run: npx eslint src/ --max-warnings 0
      - run: npx tsc --noEmit
```

---

## Linting Tradeoffs

| Approach | Pros | Cons |
|----------|------|------|
| Strict rules | Consistent code | Developer friction |
| Relaxed rules | Faster development | Inconsistent quality |
| Auto-fix on commit | Seamless workflow | May hide issues |
| Block on warnings | High quality bar | Slows velocity |

---

## Security Scanning Integration Points

![security_scanning_integration_points](svg/courses/devops/architectural-decisions-in-devops/15_testing_strategy_tradeoffs/security_scanning_integration_points.svg)

---

## SAST vs DAST Tradeoffs

- `SAST` (Static): analyzes source code, fast, many false positives
- `DAST` (Dynamic): tests running application, slower, fewer false positives
- `SAST` shifts left; `DAST` requires a running environment
- Best practice: combine both at different pipeline stages
- Tools: `Snyk`, `Trivy`, `OWASP ZAP`, `Checkmarx`

---

## Dependency and License Scanning

```yaml
- name: Audit dependencies
  run: |
    npm audit --audit-level=high
    npx license-checker --failOn "GPL-3.0"
```

- Check for known `CVEs` in dependencies
- Enforce license compliance policies
- Block builds on critical vulnerabilities
- Run on every PR and nightly for new disclosures

---

## Contract Testing vs Integration Testing

![contract_testing_vs_integration_testing](svg/courses/devops/architectural-decisions-in-devops/15_testing_strategy_tradeoffs/contract_testing_vs_integration_testing.svg)

---

## How Contract Testing Works

1. Consumer writes a test defining expected API behavior
1. Test generates a contract file (a `pact`)
1. Contract is shared with the provider team
1. Provider runs verification against the contract
1. Both sides can deploy independently with confidence

---

## Contract Testing Tools and When to Use

- `Pact` - most popular, supports many languages
- `Spring Cloud Contract` - JVM-focused
- `Specmatic` - OpenAPI-based contract testing
- Best for microservices with many consumers
- Integration tests still needed for critical data flows

---

## Test Environment Architecture

![test_environment_architecture](svg/courses/devops/architectural-decisions-in-devops/15_testing_strategy_tradeoffs/test_environment_architecture.svg)

---

## Ephemeral vs Shared Environments

| Aspect | Ephemeral | Shared |
|--------|-----------|--------|
| Isolation | Full per-branch | Shared state |
| Cost | Pay-per-use | Always running |
| Data | Fresh each run | Persistent |
| Conflicts | None | Frequent |
| Setup time | Slower startup | Instant |

---

## Test Data Strategies

1. **Seeded fixtures**: pre-built datasets loaded before tests
1. **Factory pattern**: generate data programmatically per test
1. **Production snapshots**: anonymized copies of real data
1. **Synthetic generation**: tools create realistic fake data

Notes:

- Fixtures are simple but become stale over time
- Production snapshots are realistic but raise privacy concerns

---

## Service Virtualization

- Replace real services with lightweight stubs
- Record real traffic and replay it in tests
- Tools: `WireMock`, `MockServer`, `Hoverfly`, `Mountebank`
- Eliminates dependency on third-party service uptime
- Enables testing edge cases and error scenarios

---

## Service Virtualization Architecture

![service_virtualization_architecture](svg/courses/devops/architectural-decisions-in-devops/15_testing_strategy_tradeoffs/service_virtualization_architecture.svg)

---

## Mocking Tradeoffs

- Mocks make tests faster and more reliable
- Over-mocking hides real integration failures
- Stubs can drift from actual API behavior
- Record-replay keeps stubs up to date but adds complexity
- Balance: mock at boundaries, integrate at critical paths

---

## Parallel Test Execution

- Split test suites across multiple runners
- Reduces total pipeline duration significantly
- Requires tests to be independent (no shared state)
- Tools: `pytest-xdist`, `Jest --shard`, `Gradle --parallel`
- Consider cost vs. speed tradeoff for runner count

---

## Parallel Execution Strategy

```yaml
jobs:
  test:
    strategy:
      matrix:
        shard: [1, 2, 3, 4]
    steps:
      - run: npx jest --shard=${{ matrix.shard }}/4
```

- Split by file, by test name, or by timing data
- Use historical run times for optimal distribution
- Merge coverage reports from all shards

---

## Pipeline Speed Optimization

1. Cache dependencies between runs
1. Run fast tests first (fail fast)
1. Parallelize independent test stages
1. Skip unchanged modules with path filters
1. Use incremental builds and test selection

---

## Test Selection: Run Only What Changed

```yaml
- name: Detect changes
  uses: dorny/paths-filter@v2
  id: filter
  with:
    filters: |
      api:
        - 'packages/api/**'
      web:
        - 'packages/web/**'
- name: Test API
  if: steps.filter.outputs.api == 'true'
  run: npm test --workspace=api
```

---

## Testing in Production: Why?

- Pre-production environments never fully replicate prod
- Real traffic patterns are unpredictable
- Infrastructure behavior differs at scale
- Some failures only manifest under production load
- Complements, does not replace, pre-production testing

---

## Synthetic Monitoring

- Automated scripts simulating user journeys in production
- Run on a schedule (every 1-5 minutes)
- Alert when critical paths fail or degrade
- Examples: login flow, checkout, API health checks
- Tools: `Datadog Synthetics`, `Grafana Synthetic Monitoring`

---

## Synthetic Monitor Example

```javascript
const { step } = require("@datadog/synthetics");

step("Navigate to login page", async () => {
  await page.goto("https://app.example.com/login");
});

step("Enter credentials and submit", async () => {
  await page.fill("#email", "synthetic@test.com");
  await page.click("#login-btn");
});

step("Verify dashboard loads", async () => {
  await page.waitForSelector("#dashboard");
});
```

---

## Synthetic Monitoring Tradeoffs

- Provides continuous validation of critical paths
- Does not cover all user scenarios
- Generates synthetic load (usually negligible)
- Requires dedicated test accounts and data
- Must exclude synthetic traffic from analytics

---

## Chaos Engineering as Testing

![chaos_engineering_as_testing](svg/courses/devops/architectural-decisions-in-devops/15_testing_strategy_tradeoffs/chaos_engineering_as_testing.svg)

---

## Chaos Engineering Fault Types

- **Network**: latency injection, packet loss, DNS failure
- **Compute**: CPU stress, memory exhaustion, process kill
- **Storage**: disk full, I/O errors, corrupted data
- **Application**: exception injection, thread pool exhaustion
- **Infrastructure**: AZ failure, node shutdown

---

## Chaos Engineering Tools and Tradeoffs

- `Chaos Monkey` - random instance termination (Netflix)
- `Litmus` - Kubernetes-native chaos experiments
- `Gremlin` - SaaS-based fault injection
- `Chaos Mesh` - cloud-native chaos platform
- Builds confidence but carries risk of customer impact
- Start in staging, graduate to production with blast radius controls

---

## Observability-Driven Testing

- Use production telemetry to inform testing strategy
- Identify untested paths from real usage patterns
- Three pillars: `metrics`, `logs`, `distributed traces`
- Prioritize new tests based on production traffic volume

---

## Observability Pillars for Testing

![observability_pillars_for_testing](svg/courses/devops/architectural-decisions-in-devops/15_testing_strategy_tradeoffs/observability_pillars_for_testing.svg)

---

## SLO-Based Testing

- Define `SLOs` (Service Level Objectives) for key metrics
- Write tests that validate SLO compliance
- Example: 99.9% of `/checkout` requests under 500ms
- Run load tests to verify SLO targets before release
- Monitor SLO burn rate as a production test signal

---

## Flaky Tests: The Hidden Cost

- Tests that pass and fail without code changes
- Erode team trust in the test suite
- Common causes: timing issues, shared state, network calls
- Strategy: quarantine, fix, or delete flaky tests
- Track flaky test rate as a team metric

---

## Building a Complete Testing Strategy

![building_a_complete_testing_strategy](svg/courses/devops/architectural-decisions-in-devops/15_testing_strategy_tradeoffs/building_a_complete_testing_strategy.svg)

---

## Key Takeaways

- The test pyramid is a guide, not a rule; adapt it to your architecture
- Shift-left testing reduces defect cost significantly
- Contract tests enable independent microservice deployment
- Ephemeral environments reduce conflicts but increase setup cost
- Production testing complements pre-production; it does not replace it
- Observability data should drive your testing priorities
