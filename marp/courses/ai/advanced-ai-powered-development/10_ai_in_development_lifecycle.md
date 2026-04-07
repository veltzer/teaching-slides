# AI in the Development Lifecycle

## Overview
- AI-assisted planning and design: from requirements to architecture
- AI-powered code review: automated agents and security scanning
- AI-assisted testing: generation, fuzzing, and visual regression
- AI in CI/CD pipelines: intelligent checks and deployment decisions
- AI for incident response: detection, analysis, and remediation

---

## AI-Assisted Planning: Requirements Analysis

- LLMs parse natural-language requirements and extract structured specs
- Detect ambiguities, contradictions, and missing edge cases early
- Generate acceptance criteria from user stories automatically

```yaml
# AI-generated acceptance criteria from a user story
story: "As a user I can reset my password via email"
criteria:
  - user receives reset link within 60 seconds
  - link expires after 15 minutes
  - previous sessions are invalidated on reset
  - rate limited to 3 requests per hour
  - works with SSO-linked accounts  # AI flags edge case
```

- Senior tip: treat AI output as a first draft for team refinement

---

## AI-Assisted Planning: Architecture Exploration

![ai_assisted_planning_architecture_exploration](/svg/courses/ai/advanced-ai-powered-development/10_ai_in_development_lifecycle/ai_assisted_planning_architecture_exploration.svg)

- AI proposes multiple architecture options with tradeoff analysis
- Evaluates against non-functional requirements (latency, scale, cost)
- Generates C4 or sequence diagrams from textual descriptions

---

## AI-Assisted Planning: API and Data Modeling

- Generate `OpenAPI` specs from natural-language endpoint descriptions
- AI suggests normalized schemas, indexes, and migration strategies

```sql
-- AI-generated schema from: "users can belong to
-- multiple teams, each team has a subscription plan"
CREATE TABLE teams (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    plan_id INTEGER REFERENCES plans(id)
);
CREATE TABLE team_members (
    team_id UUID REFERENCES teams(id),
    user_id UUID REFERENCES users(id),
    role VARCHAR(50) DEFAULT 'member',
    PRIMARY KEY (team_id, user_id)
);
-- AI note: added composite PK to prevent duplicates
```

- Always validate AI-generated schemas against actual query patterns

---

## AI-Powered Code Review: Automated Agents

- Tools: `CodeRabbit`, `Ellipsis`, `Qodo Merge`, `Copilot PR Review`
- Agents read entire PR diff, understand context, post comments
- Catch logic errors, not just style issues

```yaml
# .github/workflows/ai-review.yml
name: AI Code Review
on: [pull_request]
jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: coderabbit-ai/ai-pr-reviewer@v1
        with:
          model: gpt-4
          review_scope: changed_files
          severity_threshold: medium
```

- Best results when combined with human reviewers, not replacing them

---

## Hands-On: Set Up AI Code Review on GitHub

- Configure `CodeRabbit` or a custom GitHub Action for automated PR review

```yaml
# Option A: CodeRabbit (managed service)
# 1. Install CodeRabbit GitHub App on your repo
# 2. Add .coderabbit.yaml to repo root
reviews:
  auto_review:
    enabled: true
    ignore_paths:
      - "**/*.generated.*"
      - "docs/**"
  language: en
  tone: professional

# Option B: Custom Action with OpenAI
# .github/workflows/ai-review-custom.yml
# - uses: actions/checkout@v4
# - name: AI Review
#   run: |
#     DIFF=$(git diff origin/main...HEAD)
#     curl -s https://api.openai.com/v1/chat/completions \
#       -H "Authorization: Bearer $OPENAI_KEY" \
#       -d "{\"model\":\"gpt-4\",\"messages\":[...]}"
```

- Start with a single repo, measure false-positive rate, then expand

---

## AI-Powered Review: Style and Security

- **Style enforcement**: AI learns team conventions beyond what linters catch
    - Naming patterns, error handling idioms, logging standards
    - Detects deviations from project-specific architectural patterns
- **Security scanning**: AI identifies vulnerabilities in context

```python
# AI review flags this as CWE-89: SQL Injection
def get_user(name):
    query = f"SELECT * FROM users WHERE name = '{name}'"
    return db.execute(query)

# AI suggests parameterized fix:
def get_user(name):
    return db.execute(
        "SELECT * FROM users WHERE name = %s", (name,)
    )
```

- AI reviewers catch injection, SSRF, path traversal, and secrets in code

---

## AI for Technical Debt Detection

- AI scans codebases for dead code, duplication, and outdated patterns
- Quantifies technical debt and prioritizes remediation by impact

```python
# AI technical debt scanner output
debt_report = {
    "dead_code": [
        {"file": "utils/legacy_auth.py", "lines": 342,
         "last_called": "never", "confidence": 0.95},
        {"file": "api/v1_compat.py", "lines": 128,
         "last_called": "2024-01-15", "confidence": 0.88}
    ],
    "duplication": [
        {"files": ["services/order.py", "services/invoice.py"],
         "similarity": 0.87, "extract_to": "services/billing_base.py"}
    ],
    "outdated_deps": [
        {"package": "requests==2.25.0", "latest": "2.31.0",
         "cves": 2, "effort": "low"}
    ]
}
```

- Schedule regular AI debt scans as part of your CI pipeline
- Use findings to justify dedicated refactoring sprints to stakeholders

---

## AI-Powered Review: Performance Analysis

- AI detects N+1 queries, unbounded loops, memory leaks in diffs
- Suggests caching strategies, batch operations, index additions

```python
# AI flags: N+1 query inside loop
for order in orders:
    customer = db.query(Customer).get(order.customer_id)
    results.append((order, customer))

# AI suggests: eager loading
orders = (
    db.query(Order)
    .options(joinedload(Order.customer))
    .all()
)
results = [(o, o.customer) for o in orders]
```

- AI can estimate Big-O complexity changes between base and PR branch
- Particularly effective for database-heavy code paths

---

## AI for Database Query Optimization

- AI analyzes slow query logs and suggests indexing strategies
- Detects anti-patterns: `SELECT *`, missing `WHERE` clauses, cartesian joins

```sql
-- AI analysis of slow query log
-- Original: 2.3s avg, full table scan
SELECT * FROM orders
WHERE YEAR(created_at) = 2026
  AND status = 'pending';

-- AI recommendation:
-- 1. Avoid function on indexed column
-- 2. Add composite index
-- 3. Select only needed columns
SELECT id, customer_id, total
FROM orders
WHERE created_at >= '2026-01-01'
  AND created_at < '2027-01-01'
  AND status = 'pending';

-- CREATE INDEX idx_orders_status_created
-- ON orders(status, created_at);
```

- AI explains the `EXPLAIN` plan in plain language for the team
- Monitors query performance drift over time and alerts proactively

---

## AI-Assisted Testing: Unit Test Generation

- Tools: `Qodo Gen`, `Diffblue Cover`, `Claude Code`, `Copilot`
- Generate tests from implementation, docstrings, or type signatures
- AI covers happy path, edge cases, and error conditions

```python
# Source function
def divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Division by zero")
    return a / b

# AI-generated tests
def test_divide_normal():
    assert divide(10, 2) == 5.0

def test_divide_negative():
    assert divide(-6, 3) == -2.0

def test_divide_by_zero():
    with pytest.raises(ValueError, match="Division by zero"):
        divide(1, 0)

def test_divide_float_precision():
    assert abs(divide(1, 3) - 0.3333333) < 1e-6
```

---

## AI for Code Coverage Analysis

- AI maps untested code paths by analyzing coverage reports and source
- Generates targeted tests for uncovered branches and edge cases

```python
# AI-driven coverage gap analysis
def analyze_coverage_gaps(coverage_report, source_files):
    gaps = []
    for file_path, data in coverage_report.items():
        uncovered = data["uncovered_lines"]
        if not uncovered:
            continue
        # AI analyzes uncovered lines for criticality
        risk = ai_client.assess_risk(
            file_path=file_path,
            uncovered_lines=uncovered,
            context="error handling, auth, payments"
        )
        if risk.score > 0.7:
            gaps.append({
                "file": file_path,
                "lines": uncovered,
                "risk": risk.score,
                "suggested_tests": risk.test_suggestions
            })
    return sorted(gaps, key=lambda g: -g["risk"])
```

- Prioritizes coverage gaps by business criticality, not just line count
- Integrates with CI to block merges when critical paths lack tests

---

## AI-Assisted Testing: Integration and Contract Tests

- AI generates integration tests from `OpenAPI` specs or service contracts
- Understands dependencies and mocks external services appropriately

```python
# AI-generated integration test from OpenAPI spec
class TestOrderAPI:
    def test_create_order_returns_201(self, client, auth_token):
        resp = client.post("/api/orders", json={
            "items": [{"sku": "ABC-123", "qty": 2}],
            "shipping": "express"
        }, headers={"Authorization": f"Bearer {auth_token}"})
        assert resp.status_code == 201
        assert "order_id" in resp.json()

    def test_create_order_validates_stock(self, client, auth_token):
        resp = client.post("/api/orders", json={
            "items": [{"sku": "OUT-OF-STOCK", "qty": 1}]
        }, headers={"Authorization": f"Bearer {auth_token}"})
        assert resp.status_code == 409
```

- AI identifies missing test scenarios by analyzing code paths

---

## AI-Assisted Testing: Fuzzing and Property-Based

- AI generates `Hypothesis` strategies from type annotations
- Discovers boundary conditions humans overlook

```python
from hypothesis import given, strategies as st

# AI-generated property-based test
@given(
    items=st.lists(
        st.fixed_dictionaries({
            "price": st.floats(min_value=0.01, max_value=10000),
            "qty": st.integers(min_value=1, max_value=99)
        }),
        min_size=1, max_size=50
    )
)
def test_cart_total_is_sum_of_line_items(items):
    cart = Cart(items)
    expected = sum(i["price"] * i["qty"] for i in items)
    assert abs(cart.total - expected) < 0.01
```

- AI can also generate `Protocol Buffer` fuzz targets and `AFL` harnesses
- Visual regression: AI compares screenshots and ignores expected layout shifts

---

## Visual Regression Testing with AI

- Traditional pixel-diff tools produce noisy false positives
- AI-powered tools understand layout intent and ignore acceptable shifts
- Tools: `Percy`, `Applitools Eyes`, `Chromatic`

```yaml
# Applitools visual test configuration
applitools:
  api_key: ${APPLITOOLS_KEY}
  match_level: Layout  # AI-based layout comparison
  ignore_regions:
    - selector: ".dynamic-timestamp"
    - selector: ".ad-banner"
  accessibility:
    level: AA
    guidelines: WCAG_2_1
```

- AI distinguishes between intentional redesigns and regressions
- Groups related visual changes across pages into a single review
- Reduces visual test noise by 70-90% compared to pixel diffing

---

## AI in CI/CD: Automated PR Checks

![ai_in_ci_cd_automated_pr_checks](/svg/courses/ai/advanced-ai-powered-development/10_ai_in_development_lifecycle/ai_in_ci_cd_automated_pr_checks.svg)

- AI assigns a **risk score** to each PR based on:
    - Files changed (config, auth, payments = high risk)
    - Complexity delta and test coverage delta
    - Historical defect rate for changed components
- High-risk PRs require additional human reviewers automatically

---

## AI in CI/CD: Intelligent Test Selection

- Running the full test suite on every commit is expensive
- AI predicts which tests are likely to fail based on changed code

```yaml
# .github/workflows/smart-tests.yml
jobs:
  select-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: AI test selection
        run: |
          # Analyze diff and map to test files
          CHANGED=$(git diff --name-only origin/main)
          TESTS=$(ai-test-selector predict \
            --changed-files "$CHANGED" \
            --history .test-history.json \
            --confidence 0.85)
          pytest $TESTS
```

- Reduces CI time by 60-80% while catching 95%+ of regressions
- Falls back to full suite on `main` merges and release branches

---

## AI-Powered Dependency Management

- AI scans dependencies for known vulnerabilities and license conflicts
- Prioritizes updates by risk level and breaking change probability

```yaml
# AI dependency analysis report
analysis:
  critical:
    - package: "lodash@4.17.19"
      cve: "CVE-2021-23337"
      fix: "upgrade to 4.17.21"
      breaking: false
  recommended:
    - package: "express@4.18.2"
      reason: "3 patches behind, security fixes included"
      breaking: false
    - package: "pg@8.7.1"
      reason: "major version 8.11.0 available"
      breaking: true
      migration_notes: "Connection pool API changed"
```

- AI generates migration guides for major version bumps
- Schedule automated update PRs with AI-written test patches

---

## AI in CI/CD: Deployment Risk and Rollback

- AI analyzes deployment signals in real time:
    - Error rate delta, latency percentiles, CPU/memory spikes
    - Comparison against baseline from previous deployment
- Automated rollback when anomaly confidence exceeds threshold

```python
# Deployment guardian pseudocode
class DeploymentGuardian:
    def evaluate(self, metrics: DeploymentMetrics) -> Decision:
        error_spike = metrics.error_rate > self.baseline * 1.5
        latency_spike = metrics.p99 > self.baseline_p99 * 2.0
        anomaly_score = self.model.predict(metrics.features)

        if anomaly_score > 0.9 or (error_spike and latency_spike):
            return Decision.ROLLBACK
        if anomaly_score > 0.7:
            return Decision.PAUSE_AND_ALERT
        return Decision.CONTINUE
```

- Human override always available; AI provides speed, not authority

---

## AI-Assisted Changelog and Release Notes

- AI generates changelogs from commit history, PR titles, and labels
- Groups changes by category: features, fixes, breaking changes

```bash
# Generate changelog from merged PRs since last release
ai-changelog generate \
  --from v2.14.0 \
  --to HEAD \
  --format markdown \
  --group-by label \
  --exclude "chore,deps"

# Output:
# ## v2.15.0 (2026-03-09)
# ### Features
# - Add OAuth2 login with Google (#342)
# - Support bulk CSV import for users (#338)
# ### Bug Fixes
# - Fix race condition in payment queue (#341)
# ### Breaking Changes
# - Remove deprecated `/api/v1/users` endpoint (#339)
```

- AI detects breaking changes even when not explicitly labeled
- Integrate into your release pipeline for consistent release notes

---

## Incident Response: Log Analysis and Anomaly Detection

- AI processes millions of log lines and surfaces anomalous patterns
- Correlates events across services that humans would miss

```python
# AI-assisted log analysis with an LLM
from openai import OpenAI

def analyze_incident_logs(logs: list[str]) -> dict:
    client = OpenAI()
    resp = client.chat.completions.create(
        model="gpt-4",
        messages=[{
            "role": "system",
            "content": "You are an SRE analyzing logs."
        }, {
            "role": "user",
            "content": f"Find anomalies:\n{chr(10).join(logs[-500:])}"
        }]
    )
    return {"analysis": resp.choices[0].message.content}
```

- Combine LLM analysis with statistical anomaly detection (`Prophet`, `Isolation Forest`)

---

## Measuring AI Impact on Development Velocity

- Track metrics before and after AI tool adoption to quantify ROI

![measuring_ai_impact_on_development_velocity](/svg/courses/ai/advanced-ai-powered-development/10_ai_in_development_lifecycle/measuring_ai_impact_on_development_velocity.svg)

- Measure at team level, not individual level, to avoid gaming
- Track developer satisfaction alongside productivity metrics
- Re-evaluate quarterly as AI tools and workflows evolve

---

## Incident Response: Root Cause Analysis

- AI correlates deployment events, config changes, and metric shifts
- Builds a causal timeline automatically

```misc
AI Root Cause Analysis Report
=============================
Incident: API latency spike at 14:32 UTC
Timeline:
  14:28 - Deploy v2.14.3 (changed: payment-service)
  14:30 - DB connection pool exhaustion begins
  14:32 - p99 latency exceeds 5s threshold
  14:33 - Error rate jumps from 0.1% to 12%

Root cause (confidence: 87%):
  payment-service v2.14.3 introduced an unindexed
  query on `transactions.created_at` causing full
  table scans under load.

Suggested fix:
  CREATE INDEX idx_transactions_created_at
  ON transactions(created_at);
```

- AI cross-references the diff in `v2.14.3` with the query plan changes

---

## Exercise: Build an AI-Powered Incident Runbook

- Feed your architecture diagram and service dependencies to an LLM
- Generate a structured runbook for common failure scenarios

```misc
Exercise Steps:
1. Export your service dependency graph (or describe it in text)
1. Prompt the AI with: "Generate incident runbooks for
   each service covering: detection, triage, remediation"
1. Review and refine the generated runbooks
1. Add runbooks to your on-call documentation
1. Test with a simulated incident scenario
```

- **Goal**: produce runbooks for at least 3 critical services
- **Bonus**: integrate runbook suggestions into your alerting system
- Compare AI-generated runbooks against your existing ones for gaps

---

## Incident Response: Remediation and Post-Mortem

- AI suggests immediate remediation steps ranked by impact
    - Rollback, feature flag toggle, config change, scaling
- Generates post-mortem documents from incident data

```markdown
## Post-Mortem: Payment Latency Incident (auto-generated)
**Duration**: 14:32 - 14:51 UTC (19 minutes)
**Impact**: 8% of payment requests failed
**Detection**: Automated anomaly alert at 14:33
**Resolution**: Rollback to v2.14.2 at 14:48

### Action Items
1. Add index on `transactions.created_at`
1. Add query plan regression check to CI
1. Lower anomaly alert threshold for payment path
1. Add load test covering high-cardinality date queries
```

- Post-mortem drafts save hours and ensure consistent blameless format
- Senior teams review and refine, not write from scratch

---

## AI-Assisted Documentation Generation

- AI generates API docs from code, type signatures, and docstrings
- Produces architecture decision records (ADRs) from PR discussions
- Keeps documentation in sync with code changes automatically

```python
# Generate OpenAPI docs from Flask routes using AI
def generate_api_docs(app) -> str:
    routes = []
    for rule in app.url_map.iter_rules():
        func = app.view_functions[rule.endpoint]
        routes.append({
            "path": rule.rule,
            "methods": list(rule.methods - {"HEAD", "OPTIONS"}),
            "docstring": func.__doc__,
            "annotations": get_type_hints(func)
        })
    return ai_client.generate_openapi_spec(routes)
```

- Pair with CI checks that flag stale docs when source code diverges

---

## AI in Sprint Planning

- AI estimates story points by comparing to historical velocity data
- Decomposes large stories into implementable sub-tasks automatically

```yaml
# AI-generated task decomposition
story: "Add OAuth2 login with Google"
estimated_points: 8
sub_tasks:
  - title: "Configure Google OAuth credentials"
    points: 1
  - title: "Implement authorization code flow"
    points: 3
  - title: "Add token refresh and session management"
    points: 2
  - title: "Write integration tests for OAuth flow"
    points: 2
```

- AI detects over-committed sprints by analyzing team capacity history
- Use as a starting point for team discussion, not a final decision

---

## Continuous AI Integration Patterns

![continuous_ai_integration_patterns](/svg/courses/ai/advanced-ai-powered-development/10_ai_in_development_lifecycle/continuous_ai_integration_patterns.svg)

- **Pattern 1: Gate-based** - AI runs as a required CI check before merge
- **Pattern 2: Advisory** - AI posts suggestions as non-blocking comments
- **Pattern 3: Ambient** - AI continuously monitors and files improvement PRs
- Start with advisory mode, promote to gate-based as trust grows

---

## Building an AI-Enhanced Developer Portal

- Centralized self-service hub for all AI development tools
- Developers access code generation, review, and analysis through one interface

```yaml
# developer-portal-config.yml
portal:
  services:
    - name: "AI Code Review"
      endpoint: /review
      description: "Submit code for instant AI review"
    - name: "Test Generator"
      endpoint: /generate-tests
      description: "Generate unit tests from source files"
    - name: "Incident Analyzer"
      endpoint: /analyze-incident
      description: "Upload logs for AI root-cause analysis"
    - name: "Doc Generator"
      endpoint: /generate-docs
      description: "Generate API docs from code"
  auth: SSO
  rate_limit: 100/hour/user
```

- Track usage metrics to identify which AI tools deliver the most value
- Iterate on tool offerings based on developer feedback and adoption data

---

## Putting It All Together

![putting_it_all_together](/svg/courses/ai/advanced-ai-powered-development/10_ai_in_development_lifecycle/putting_it_all_together.svg)

- AI is not a single tool but a **layer** across the entire lifecycle
- Each phase benefits from AI while keeping humans in the decision loop
- Start adoption where your team has the most pain, then expand
