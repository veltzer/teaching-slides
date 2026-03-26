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

<svg width="500" height="320" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrow_tp" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <polygon points="250,20 450,300 50,300" fill="none" stroke="#333" stroke-width="2"/>
  <line x1="130" y1="220" x2="370" y2="220" stroke="#333" stroke-width="1" stroke-dasharray="4"/>
  <line x1="180" y1="140" x2="320" y2="140" stroke="#333" stroke-width="1" stroke-dasharray="4"/>
  <text x="250" y="80" text-anchor="middle" font-size="13" font-weight="bold" fill="#d32f2f">E2E Tests</text>
  <text x="250" y="100" text-anchor="middle" font-size="11" fill="#555">Few, Slow, Expensive</text>
  <text x="250" y="175" text-anchor="middle" font-size="13" font-weight="bold" fill="#f57c00">Integration Tests</text>
  <text x="250" y="195" text-anchor="middle" font-size="11" fill="#555">Some, Medium Speed</text>
  <text x="250" y="265" text-anchor="middle" font-size="13" font-weight="bold" fill="#388e3c">Unit Tests</text>
  <text x="250" y="285" text-anchor="middle" font-size="11" fill="#555">Many, Fast, Cheap</text>
  <text x="30" y="165" text-anchor="middle" font-size="11" fill="#333" transform="rotate(-90,30,165)">Speed / Volume</text>
  <line x1="40" y1="280" x2="40" y2="50" stroke="#333" stroke-width="1.5" marker-end="url(#arrow_tp)"/>
</svg>

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

<svg width="550" height="250" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrow_e2e" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <line x1="60" y1="220" x2="520" y2="220" stroke="#333" stroke-width="2" marker-end="url(#arrow_e2e)"/>
  <line x1="60" y1="220" x2="60" y2="20" stroke="#333" stroke-width="2" marker-end="url(#arrow_e2e)"/>
  <text x="290" y="248" text-anchor="middle" font-size="12" fill="#333">Number of Tests</text>
  <text x="25" y="120" text-anchor="middle" font-size="12" fill="#333" transform="rotate(-90,25,120)">Maintenance Cost</text>
  <polyline points="80,200 180,180 280,140 380,80 480,30" fill="none" stroke="#d32f2f" stroke-width="3"/>
  <text x="490" y="25" font-size="11" fill="#d32f2f">E2E</text>
  <polyline points="80,205 180,195 280,180 380,160 480,135" fill="none" stroke="#f57c00" stroke-width="3"/>
  <text x="490" y="130" font-size="11" fill="#f57c00">Integration</text>
  <polyline points="80,210 180,205 280,198 380,190 480,180" fill="none" stroke="#388e3c" stroke-width="3"/>
  <text x="490" y="175" font-size="11" fill="#388e3c">Unit</text>
</svg>

---

## Finding the Right Balance

- No single correct ratio; depends on architecture
- Microservices: heavier on integration and contract tests
- Monoliths: heavier on unit tests with selective E2E
- Google's suggested ratio: 70% unit, 20% integration, 10% E2E
- The Testing Trophy alternative emphasizes integration for UI apps

---

## Shift-Left Testing Overview

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrow_sl" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <line x1="30" y1="100" x2="570" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrow_sl)"/>
  <rect x="50" y="70" width="90" height="60" fill="#c8e6c9" stroke="#333" stroke-width="1.5" rx="5"/>
  <text x="95" y="105" text-anchor="middle" font-size="11" font-weight="bold">Code</text>
  <rect x="160" y="70" width="90" height="60" fill="#b3e5fc" stroke="#333" stroke-width="1.5" rx="5"/>
  <text x="205" y="105" text-anchor="middle" font-size="11" font-weight="bold">Build</text>
  <rect x="270" y="70" width="90" height="60" fill="#fff9c4" stroke="#333" stroke-width="1.5" rx="5"/>
  <text x="315" y="105" text-anchor="middle" font-size="11" font-weight="bold">Test</text>
  <rect x="380" y="70" width="90" height="60" fill="#ffe0b2" stroke="#333" stroke-width="1.5" rx="5"/>
  <text x="425" y="105" text-anchor="middle" font-size="11" font-weight="bold">Deploy</text>
  <rect x="490" y="70" width="70" height="60" fill="#ffcdd2" stroke="#333" stroke-width="1.5" rx="5"/>
  <text x="525" y="105" text-anchor="middle" font-size="11" font-weight="bold">Prod</text>
  <path d="M400,55 C350,20 200,20 80,55" fill="none" stroke="#d32f2f" stroke-width="2" stroke-dasharray="6" marker-end="url(#arrow_sl)"/>
  <text x="240" y="18" text-anchor="middle" font-size="12" fill="#d32f2f" font-weight="bold">Shift Left</text>
  <text x="300" y="165" text-anchor="middle" font-size="11" fill="#555">Find bugs earlier = cheaper to fix</text>
</svg>

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

<svg width="580" height="140" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrow_sec" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <rect x="20" y="20" width="100" height="45" fill="#e8f5e9" stroke="#333" stroke-width="1.5" rx="5"/>
  <text x="70" y="47" text-anchor="middle" font-size="11">Pre-commit</text>
  <rect x="150" y="20" width="100" height="45" fill="#e3f2fd" stroke="#333" stroke-width="1.5" rx="5"/>
  <text x="200" y="47" text-anchor="middle" font-size="11">PR / Build</text>
  <rect x="280" y="20" width="100" height="45" fill="#fff3e0" stroke="#333" stroke-width="1.5" rx="5"/>
  <text x="330" y="47" text-anchor="middle" font-size="11">Registry</text>
  <rect x="410" y="20" width="100" height="45" fill="#ffebee" stroke="#333" stroke-width="1.5" rx="5"/>
  <text x="460" y="47" text-anchor="middle" font-size="11">Runtime</text>
  <line x1="120" y1="42" x2="150" y2="42" stroke="#333" stroke-width="1.5" marker-end="url(#arrow_sec)"/>
  <line x1="250" y1="42" x2="280" y2="42" stroke="#333" stroke-width="1.5" marker-end="url(#arrow_sec)"/>
  <line x1="380" y1="42" x2="410" y2="42" stroke="#333" stroke-width="1.5" marker-end="url(#arrow_sec)"/>
  <text x="70" y="90" text-anchor="middle" font-size="10" fill="#555">Secrets scan</text>
  <text x="70" y="105" text-anchor="middle" font-size="10" fill="#555">Lint rules</text>
  <text x="200" y="90" text-anchor="middle" font-size="10" fill="#555">SAST</text>
  <text x="200" y="105" text-anchor="middle" font-size="10" fill="#555">Dependency audit</text>
  <text x="330" y="90" text-anchor="middle" font-size="10" fill="#555">Image scan</text>
  <text x="330" y="105" text-anchor="middle" font-size="10" fill="#555">SBOM check</text>
  <text x="460" y="90" text-anchor="middle" font-size="10" fill="#555">DAST</text>
  <text x="460" y="105" text-anchor="middle" font-size="10" fill="#555">RASP</text>
</svg>

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

<svg width="580" height="280" xmlns="http://www.w3.org/2000/svg">
  <text x="145" y="20" text-anchor="middle" font-size="13" font-weight="bold" fill="#333">Contract Testing</text>
  <text x="435" y="20" text-anchor="middle" font-size="13" font-weight="bold" fill="#333">Integration Testing</text>
  <rect x="50" y="35" width="190" height="230" fill="#e8f5e9" stroke="#333" stroke-width="1.5" rx="5"/>
  <rect x="340" y="35" width="190" height="230" fill="#e3f2fd" stroke="#333" stroke-width="1.5" rx="5"/>
  <text x="145" y="65" text-anchor="middle" font-size="11">Consumer defines</text>
  <text x="145" y="80" text-anchor="middle" font-size="11">expected contract</text>
  <text x="145" y="110" text-anchor="middle" font-size="11">Provider verifies</text>
  <text x="145" y="125" text-anchor="middle" font-size="11">it meets contract</text>
  <text x="145" y="155" text-anchor="middle" font-size="11">No real service</text>
  <text x="145" y="170" text-anchor="middle" font-size="11">needed at test time</text>
  <text x="145" y="200" text-anchor="middle" font-size="11">Fast, isolated</text>
  <text x="145" y="230" text-anchor="middle" font-size="11">Independent deploys</text>
  <text x="435" y="65" text-anchor="middle" font-size="11">Tests real service</text>
  <text x="435" y="80" text-anchor="middle" font-size="11">interactions</text>
  <text x="435" y="110" text-anchor="middle" font-size="11">Requires running</text>
  <text x="435" y="125" text-anchor="middle" font-size="11">instances of services</text>
  <text x="435" y="155" text-anchor="middle" font-size="11">Catches runtime</text>
  <text x="435" y="170" text-anchor="middle" font-size="11">environment issues</text>
  <text x="435" y="200" text-anchor="middle" font-size="11">Slower, flakier</text>
  <text x="435" y="230" text-anchor="middle" font-size="11">Coupled deployments</text>
</svg>

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

<svg width="560" height="260" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrow_env" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <rect x="30" y="20" width="500" height="230" fill="#f5f5f5" stroke="#333" stroke-width="1.5" rx="5"/>
  <text x="280" y="45" text-anchor="middle" font-size="13" font-weight="bold">Test Environment Landscape</text>
  <rect x="60" y="60" width="130" height="50" fill="#c8e6c9" stroke="#333" stroke-width="1.5" rx="5"/>
  <text x="125" y="90" text-anchor="middle" font-size="11">Dev / Local</text>
  <rect x="220" y="60" width="130" height="50" fill="#b3e5fc" stroke="#333" stroke-width="1.5" rx="5"/>
  <text x="285" y="90" text-anchor="middle" font-size="11">CI Ephemeral</text>
  <rect x="380" y="60" width="130" height="50" fill="#fff9c4" stroke="#333" stroke-width="1.5" rx="5"/>
  <text x="445" y="90" text-anchor="middle" font-size="11">Staging</text>
  <rect x="140" y="160" width="130" height="50" fill="#ffe0b2" stroke="#333" stroke-width="1.5" rx="5"/>
  <text x="205" y="190" text-anchor="middle" font-size="11">Shared QA</text>
  <rect x="300" y="160" width="130" height="50" fill="#ffcdd2" stroke="#333" stroke-width="1.5" rx="5"/>
  <text x="365" y="190" text-anchor="middle" font-size="11">Production</text>
  <line x1="190" y1="110" x2="220" y2="85" stroke="#333" stroke-width="1.5" marker-end="url(#arrow_env)"/>
  <line x1="350" y1="85" x2="380" y2="85" stroke="#333" stroke-width="1.5" marker-end="url(#arrow_env)"/>
  <line x1="285" y1="110" x2="240" y2="160" stroke="#333" stroke-width="1.5" marker-end="url(#arrow_env)"/>
  <line x1="445" y1="110" x2="400" y2="160" stroke="#333" stroke-width="1.5" marker-end="url(#arrow_env)"/>
</svg>

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

<svg width="550" height="220" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrow_sv" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <rect x="30" y="80" width="120" height="60" fill="#e3f2fd" stroke="#333" stroke-width="1.5" rx="5"/>
  <text x="90" y="115" text-anchor="middle" font-size="12" font-weight="bold">Your Service</text>
  <rect x="220" y="30" width="120" height="50" fill="#c8e6c9" stroke="#333" stroke-width="1.5" rx="5"/>
  <text x="280" y="50" text-anchor="middle" font-size="11">Virtual: Payment</text>
  <text x="280" y="65" text-anchor="middle" font-size="11">API Stub</text>
  <rect x="220" y="95" width="120" height="50" fill="#c8e6c9" stroke="#333" stroke-width="1.5" rx="5"/>
  <text x="280" y="115" text-anchor="middle" font-size="11">Virtual: Auth</text>
  <text x="280" y="130" text-anchor="middle" font-size="11">API Stub</text>
  <rect x="220" y="160" width="120" height="50" fill="#c8e6c9" stroke="#333" stroke-width="1.5" rx="5"/>
  <text x="280" y="180" text-anchor="middle" font-size="11">Virtual: Email</text>
  <text x="280" y="195" text-anchor="middle" font-size="11">API Stub</text>
  <rect x="410" y="80" width="120" height="60" fill="#ffcdd2" stroke="#333" stroke-width="1.5" rx="5"/>
  <text x="470" y="105" text-anchor="middle" font-size="11">Real External</text>
  <text x="470" y="120" text-anchor="middle" font-size="11">Services</text>
  <line x1="150" y1="100" x2="220" y2="55" stroke="#333" stroke-width="1.5" marker-end="url(#arrow_sv)"/>
  <line x1="150" y1="110" x2="220" y2="120" stroke="#333" stroke-width="1.5" marker-end="url(#arrow_sv)"/>
  <line x1="150" y1="120" x2="220" y2="185" stroke="#333" stroke-width="1.5" marker-end="url(#arrow_sv)"/>
  <line x1="340" y1="55" x2="410" y2="100" stroke="#aaa" stroke-width="1.5" stroke-dasharray="5" marker-end="url(#arrow_sv)"/>
  <line x1="340" y1="120" x2="410" y2="110" stroke="#aaa" stroke-width="1.5" stroke-dasharray="5" marker-end="url(#arrow_sv)"/>
  <line x1="340" y1="185" x2="410" y2="120" stroke="#aaa" stroke-width="1.5" stroke-dasharray="5" marker-end="url(#arrow_sv)"/>
  <text x="375" y="20" text-anchor="middle" font-size="10" fill="#888">Recorded from real traffic</text>
</svg>

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

<svg width="560" height="250" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrow_ce" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <rect x="30" y="30" width="130" height="50" fill="#e8f5e9" stroke="#333" stroke-width="1.5" rx="5"/>
  <text x="95" y="50" text-anchor="middle" font-size="11" font-weight="bold">1. Steady State</text>
  <text x="95" y="65" text-anchor="middle" font-size="10">Define normal behavior</text>
  <rect x="210" y="30" width="130" height="50" fill="#fff9c4" stroke="#333" stroke-width="1.5" rx="5"/>
  <text x="275" y="50" text-anchor="middle" font-size="11" font-weight="bold">2. Hypothesis</text>
  <text x="275" y="65" text-anchor="middle" font-size="10">Predict system response</text>
  <rect x="390" y="30" width="140" height="50" fill="#ffe0b2" stroke="#333" stroke-width="1.5" rx="5"/>
  <text x="460" y="50" text-anchor="middle" font-size="11" font-weight="bold">3. Inject Fault</text>
  <text x="460" y="65" text-anchor="middle" font-size="10">Kill pod, add latency</text>
  <rect x="120" y="150" width="140" height="50" fill="#ffcdd2" stroke="#333" stroke-width="1.5" rx="5"/>
  <text x="190" y="170" text-anchor="middle" font-size="11" font-weight="bold">4. Observe</text>
  <text x="190" y="185" text-anchor="middle" font-size="10">Compare to hypothesis</text>
  <rect x="310" y="150" width="140" height="50" fill="#e3f2fd" stroke="#333" stroke-width="1.5" rx="5"/>
  <text x="380" y="170" text-anchor="middle" font-size="11" font-weight="bold">5. Learn / Fix</text>
  <text x="380" y="185" text-anchor="middle" font-size="10">Improve resilience</text>
  <line x1="160" y1="55" x2="210" y2="55" stroke="#333" stroke-width="1.5" marker-end="url(#arrow_ce)"/>
  <line x1="340" y1="55" x2="390" y2="55" stroke="#333" stroke-width="1.5" marker-end="url(#arrow_ce)"/>
  <line x1="460" y1="80" x2="460" y2="110" stroke="#333" stroke-width="1.5"/>
  <line x1="460" y1="110" x2="260" y2="150" stroke="#333" stroke-width="1.5" marker-end="url(#arrow_ce)"/>
  <line x1="260" y1="175" x2="310" y2="175" stroke="#333" stroke-width="1.5" marker-end="url(#arrow_ce)"/>
</svg>

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

<svg width="500" height="280" xmlns="http://www.w3.org/2000/svg">
  <ellipse cx="250" cy="140" rx="55" ry="35" fill="#673ab7" stroke="#333" stroke-width="2"/>
  <text x="250" y="137" text-anchor="middle" font-size="11" fill="white">Observability</text>
  <text x="250" y="152" text-anchor="middle" font-size="11" fill="white">-Driven</text>
  <ellipse cx="120" cy="60" rx="65" ry="30" fill="#e3f2fd" stroke="#333" stroke-width="1.5"/>
  <text x="120" y="57" text-anchor="middle" font-size="12" font-weight="bold">Metrics</text>
  <text x="120" y="72" text-anchor="middle" font-size="10">SLIs, latency, errors</text>
  <ellipse cx="380" cy="60" rx="65" ry="30" fill="#e8f5e9" stroke="#333" stroke-width="1.5"/>
  <text x="380" y="57" text-anchor="middle" font-size="12" font-weight="bold">Logs</text>
  <text x="380" y="72" text-anchor="middle" font-size="10">Events, exceptions</text>
  <ellipse cx="250" cy="240" rx="65" ry="30" fill="#fff3e0" stroke="#333" stroke-width="1.5"/>
  <text x="250" y="237" text-anchor="middle" font-size="12" font-weight="bold">Traces</text>
  <text x="250" y="252" text-anchor="middle" font-size="10">Request flow, spans</text>
  <line x1="200" y1="115" x2="155" y2="85" stroke="#333" stroke-width="1.5"/>
  <line x1="300" y1="115" x2="345" y2="85" stroke="#333" stroke-width="1.5"/>
  <line x1="250" y1="175" x2="250" y2="210" stroke="#333" stroke-width="1.5"/>
</svg>

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

<svg width="580" height="240" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrow_cs" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <text x="290" y="20" text-anchor="middle" font-size="13" font-weight="bold">Testing Strategy Across the Pipeline</text>
  <rect x="20" y="35" width="100" height="130" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="3"/>
  <text x="70" y="55" text-anchor="middle" font-size="11" font-weight="bold">Pre-commit</text>
  <text x="70" y="75" text-anchor="middle" font-size="9">Lint</text>
  <text x="70" y="90" text-anchor="middle" font-size="9">Type check</text>
  <text x="70" y="105" text-anchor="middle" font-size="9">Secrets scan</text>
  <rect x="135" y="35" width="100" height="130" fill="#b3e5fc" stroke="#333" stroke-width="1" rx="3"/>
  <text x="185" y="55" text-anchor="middle" font-size="11" font-weight="bold">CI Build</text>
  <text x="185" y="75" text-anchor="middle" font-size="9">Unit tests</text>
  <text x="185" y="90" text-anchor="middle" font-size="9">SAST</text>
  <text x="185" y="105" text-anchor="middle" font-size="9">Contract tests</text>
  <rect x="250" y="35" width="100" height="130" fill="#fff9c4" stroke="#333" stroke-width="1" rx="3"/>
  <text x="300" y="55" text-anchor="middle" font-size="11" font-weight="bold">CI Test</text>
  <text x="300" y="75" text-anchor="middle" font-size="9">Integration</text>
  <text x="300" y="90" text-anchor="middle" font-size="9">API tests</text>
  <text x="300" y="105" text-anchor="middle" font-size="9">DAST</text>
  <rect x="365" y="35" width="100" height="130" fill="#ffe0b2" stroke="#333" stroke-width="1" rx="3"/>
  <text x="415" y="55" text-anchor="middle" font-size="11" font-weight="bold">Staging</text>
  <text x="415" y="75" text-anchor="middle" font-size="9">E2E tests</text>
  <text x="415" y="90" text-anchor="middle" font-size="9">Perf tests</text>
  <text x="415" y="105" text-anchor="middle" font-size="9">Chaos tests</text>
  <rect x="480" y="35" width="100" height="130" fill="#ffcdd2" stroke="#333" stroke-width="1" rx="3"/>
  <text x="530" y="55" text-anchor="middle" font-size="11" font-weight="bold">Production</text>
  <text x="530" y="75" text-anchor="middle" font-size="9">Synthetics</text>
  <text x="530" y="90" text-anchor="middle" font-size="9">Canary analysis</text>
  <text x="530" y="105" text-anchor="middle" font-size="9">Observability</text>
  <line x1="120" y1="100" x2="135" y2="100" stroke="#333" stroke-width="1.5" marker-end="url(#arrow_cs)"/>
  <line x1="235" y1="100" x2="250" y2="100" stroke="#333" stroke-width="1.5" marker-end="url(#arrow_cs)"/>
  <line x1="350" y1="100" x2="365" y2="100" stroke="#333" stroke-width="1.5" marker-end="url(#arrow_cs)"/>
  <line x1="465" y1="100" x2="480" y2="100" stroke="#333" stroke-width="1.5" marker-end="url(#arrow_cs)"/>
  <text x="290" y="195" text-anchor="middle" font-size="10" fill="#333">Confidence increases ----></text>
  <text x="290" y="215" text-anchor="middle" font-size="10" fill="#333">&lt;--- Speed decreases</text>
</svg>

---

## Key Takeaways

- The test pyramid is a guide, not a rule; adapt it to your architecture
- Shift-left testing reduces defect cost significantly
- Contract tests enable independent microservice deployment
- Ephemeral environments reduce conflicts but increase setup cost
- Production testing complements pre-production; it does not replace it
- Observability data should drive your testing priorities
