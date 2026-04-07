# Working with Large Codebases and Monoliths

## Overview
- Challenges AI faces in large, complex codebases
- Strategies for effective AI use in monoliths
- Code navigation and exploration with AI agents
- Refactoring monoliths with AI assistance
- AI-assisted code archaeology and legacy understanding

---

## Challenges of AI in Large Codebases

## Context Window Limitations
- LLM context windows are finite (even at 200K+ tokens)
- A monolith with 500K+ LOC cannot fit in a single prompt
- Naive "dump everything" approaches fail silently
- The model may hallucinate APIs it cannot see
- Strategic context selection is a core engineering skill

```misc
Monolith: 2M tokens of source
Context:  200K tokens max
Ratio:    ~10% visible at any time
```

---

## Challenges of AI in Large Codebases

## Handling Context Overflow: Symptoms and Mitigations
- Repeated or contradictory suggestions signal context saturation
- The AI starts "forgetting" instructions given earlier in the session
- Outputs become generic instead of project-specific
- Chunking strategies: split by module, layer, or feature boundary
- Summarize prior context before feeding the next chunk

```misc
Symptoms of context overflow:
1. AI re-introduces code you already deleted
1. Variable names revert to generic (e.g., `data`, `result`)
1. Suggestions contradict architectural constraints
1. Test generation targets non-existent functions

Mitigations:
1. Restart session with a focused summary
1. Use explicit "context checkpoints" between chunks
1. Feed only diffs instead of full files when possible
```

---

## Challenges of AI in Large Codebases

## Navigating Unfamiliar Code
- AI has no persistent memory of your repo structure
- Each session starts from zero understanding
- File naming conventions vary across teams and eras
- Dead code and abandoned modules create noise
- Without guidance, the AI explores randomly

---

## Challenges of AI in Large Codebases

## Implicit Conventions and Cross-Module Dependencies
- Coding standards that exist only in team culture
- Unwritten rules: "we never throw from this layer"
- Hidden coupling through shared databases or message buses
- Circular dependencies that defy static analysis
- Event-driven flows spanning dozens of files

![implicit_conventions_and_cross_module_dependencies](/svg/courses/ai/advanced-ai-powered-development/03_large_codebases_and_monoliths/implicit_conventions_and_cross_module_dependencies.svg)

---

## Challenges of AI in Large Codebases

## Cost and Performance: Token Budgeting for Large Repos
- Every token sent to the model has a dollar cost
- Large files and verbose outputs multiply expenses quickly
- Cache prompt prefixes when making repeated queries on the same module
- Measure tokens-per-task to find wasteful patterns
- Use cheaper models for exploration, capable models for generation

```misc
Cost estimation for a refactoring session:
1. Initial context loading:   ~50K tokens input
1. Iterative exploration:     ~120K tokens (6 rounds x 20K)
1. Code generation:           ~30K tokens output
1. Review and correction:     ~40K tokens
Total:                        ~240K tokens (~$2-5 per session)

Savings strategies:
- Prompt caching:             30-50% reduction on repeated prefixes
- Targeted file selection:    60-80% fewer input tokens
- Streaming partial results:  avoid regenerating full outputs
```

---

## Strategies for Effective AI Use

## Structured Project Documentation for AI
- Maintain a machine-readable project map at the repo root
- Include module boundaries, ownership, and purpose
- Document key entry points and hot paths
- Keep dependency graphs up to date
- Treat AI-facing docs as first-class artifacts

```markdown
# Project Map
## /src/billing    - Payment processing (team: payments)
## /src/auth       - Authentication & SSO (team: platform)
## /src/inventory  - Stock management (team: supply-chain)
## /src/shared/db  - Shared ORM models (owner: DBA team)
```

---

## Strategies for Effective AI Use

## Writing Effective `CLAUDE.md` / Rules Files
- Place at repo root and in key subdirectories
- Specify build commands, test commands, lint rules
- Document naming conventions and architectural constraints
- List files the AI should never modify
- Keep them concise; the AI reads them every session

```markdown
# CLAUDE.md
- Build: `make build`
- Test: `pytest tests/ -x --tb=short`
- Lint: `ruff check . --fix`
- NEVER modify files under /src/generated/
- All services return Result<T, AppError>, not exceptions
- Database migrations go in /migrations/, never inline
```

---

## Strategies for Effective AI Use

## Using `.gitignore`-style Exclusions to Reduce Noise
- AI tools scan your repo; generated code wastes context tokens
- Configure `.claudeignore`, `.cursorignore`, or equivalent files
- Exclude `node_modules/`, `vendor/`, build outputs, and lock files
- Ignore auto-generated code: protobuf stubs, ORM models, SDK clients
- Revisit exclusions when modules move or new generators are added

```gitignore
# .claudeignore
node_modules/
dist/
build/
*.generated.ts
src/proto/**/*.pb.go
vendor/
coverage/
*.min.js
__pycache__/
```

---

## Strategies for Effective AI Use

## Modular Context Feeding
- Feed only the relevant slice of the codebase per task
- Use file trees and summaries before full source
- Start with interfaces, then drill into implementations
- Leverage `@file` references in tools like Claude Code
- Chain prompts: overview first, details second

```misc
Step 1: "Here are the interface files for the billing module"
Step 2: "Here is the specific service I need to change"
Step 3: "Here are the tests that cover this service"
```

---

## Strategies for Effective AI Use

## Incremental Exploration Patterns
- Let the AI agent explore iteratively rather than front-loading
- Use `grep`, `find`, and `ast-grep` as exploration primitives
- Ask the AI to form hypotheses, then verify them
- Build understanding bottom-up: types, functions, modules

```misc
Prompt pattern:
1. "Find all implementations of PaymentProcessor"
1. "Show me the call sites for processRefund()"
1. "What error handling wraps these calls?"
1. "Now propose the change with full context"
```

---

## Strategies for Effective AI Use

## Cross-Team Coordination for AI-Assisted Refactoring
- Establish shared rules files across teams to enforce consistency
- Agree on naming conventions, error patterns, and module boundaries
- Use a central `CLAUDE.md` for org-wide constraints, local ones per team
- Coordinate extraction work to avoid conflicting AI-generated changes
- Review each team's rules files in architecture syncs

```misc
Repo structure for shared conventions:
/CLAUDE.md                    # org-wide rules
/src/billing/CLAUDE.md        # billing team overrides
/src/auth/CLAUDE.md           # auth team overrides
/src/shared/CLAUDE.md         # shared library constraints

Coordination checklist:
1. Agree on interface contracts before parallel extraction
1. Lock shared modules during cross-cutting refactors
1. Run integration tests across team boundaries after merges
1. Sync rules file changes via pull requests with multi-team review
```

---

## Code Navigation with AI Agents

## Searching by Pattern and Semantic Meaning
- Regex search: fast, precise, misses renamed concepts
- Semantic search: finds related code despite naming differences
- Combine both: regex to anchor, semantic to expand
- Tools: `ripgrep`, `ast-grep`, embedding-based search

```bash
# Pattern: find all error handlers
rg "catch|rescue|except|on_error" --type-add 'src:*.{ts,py,rb}'

# Semantic: ask the AI
# "Find all places where we handle payment failures,
#  including retry logic and dead-letter queuing"
```

---

## Code Navigation with AI Agents

## Multi-File Navigation Workflows in Practice
- Real tasks require jumping between definition, usage, and test files
- Ask the AI to locate all three for any symbol before making changes
- Verify that test files actually cover the code path you are modifying
- Use a consistent prompt pattern to avoid missing related files

```misc
Navigation workflow:
1. "Find the definition of OrderService.submitOrder()"
1. "Show all call sites of submitOrder() across the codebase"
1. "Find the test files that exercise submitOrder()"
1. "Are there integration tests that cover the full order flow?"
1. "Show me the database migration for the orders table"
```

![multi_file_navigation_workflows_in_practice](/svg/courses/ai/advanced-ai-powered-development/03_large_codebases_and_monoliths/multi_file_navigation_workflows_in_practice.svg)

---

## Code Navigation with AI Agents

## Understanding Call Graphs and Data Flow
- Ask the AI to trace a function from entry point to storage
- Use static analysis tools to generate call graphs, then feed them in
- Map the lifecycle of a request across service boundaries
- Identify shared mutable state and side effects

![understanding_call_graphs_and_data_flow](/svg/courses/ai/advanced-ai-powered-development/03_large_codebases_and_monoliths/understanding_call_graphs_and_data_flow.svg)

---

## Code Navigation with AI Agents

## Detecting and Resolving Hallucinated APIs
- AI may suggest methods, classes, or imports that do not exist
- Always verify generated calls against the actual codebase
- Watch for plausible-looking but fabricated library functions
- Use `grep` or `ast-grep` to confirm symbols before accepting code
- Build a verification habit into your AI-assisted workflow

```bash
# AI suggested: from utils.cache import distributed_lock
# Verify it actually exists:
rg "def distributed_lock" --type py
rg "class distributed_lock" --type py
rg "distributed_lock" src/utils/cache.py

# AI suggested: response.json().getOrDefault("key", fallback)
# Check if that method exists in the library version you use:
rg "def getOrDefault" --type py
# If not found: the AI hallucinated a Java-style API in Python
```

---

## Code Navigation with AI Agents

## Dependency Graph Visualization with AI
- Use tools like `madge`, `pydeps`, or `jdeps` to extract dependency data
- Feed the graph output to the AI for analysis and extraction planning
- Identify circular dependencies and tightly coupled clusters
- Plan extraction order: leaves first, shared utilities last

```bash
# JavaScript/TypeScript: madge
madge --image dep-graph.svg src/index.ts

# Python: pydeps
pydeps src/billing --max-bacon=3 --no-show

# Java: jdeps
jdeps --dot-output deps/ target/app.jar
```

```misc
AI prompt with graph data:
"Here is the dependency graph for our billing module.
Identify the optimal extraction order, starting with
modules that have zero inbound dependencies."
```

---

## Refactoring Monoliths with AI

## Identifying Extraction Candidates
- Look for modules with low afferent coupling (few inbound deps)
- Find code with its own data store or bounded context
- Detect clusters of files that change together (via `git log`)
- Ask the AI to analyze import graphs for natural seams

```bash
# Find files that always change together
git log --format=format: --name-only --since="1 year ago" \
  | sort | uniq -c | sort -rn | head -20

# Ask AI: "Given these co-change clusters,
# which module is the best extraction candidate?"
```

---

## Refactoring Monoliths with AI

## Safe Incremental Refactoring Workflows
- Never refactor and change behavior in the same commit
- Use the Strangler Fig pattern: wrap, then replace
- Have the AI generate adapter layers before extracting
- Run tests after every atomic step
- Keep refactoring PRs small and reviewable

```misc
Workflow:
1. Extract interface from concrete class
1. Introduce adapter implementing the interface
1. Redirect callers to the adapter (one by one)
1. Move implementation behind the adapter boundary
1. Remove the original class
```

---

## Refactoring Monoliths with AI

## Microservice Extraction Patterns
- The Strangler Fig pattern replaces monolith pieces incrementally
- AI can generate the facade, proxy routes, and data sync layers
- Start with read paths before migrating writes
- Use feature flags to toggle between old and new implementations
- Monitor error rates and latency at each cutover stage

```misc
Strangler Fig implementation with AI assistance:
1. Ask AI to identify the public API surface of the target module
1. Generate a thin proxy service that delegates to the monolith
1. Migrate one endpoint at a time behind the proxy
1. AI writes data synchronization logic for the transition period
1. Once all endpoints are migrated, remove monolith code
1. Retire the proxy and route directly to the new service
```

![microservice_extraction_patterns](/svg/courses/ai/advanced-ai-powered-development/03_large_codebases_and_monoliths/microservice_extraction_patterns.svg)

---

## Refactoring Monoliths with AI

## AI-Assisted Database and Schema Refactoring
- Database changes are the riskiest part of monolith decomposition
- AI can generate migration scripts that respect foreign key dependencies
- Use expand-and-contract pattern for zero-downtime schema changes
- Have the AI trace all query paths affected by a column rename
- Always generate rollback migrations alongside forward migrations

```sql
-- AI-generated expand-and-contract migration
-- Step 1: Expand (add new column)
ALTER TABLE orders ADD COLUMN customer_uuid UUID;
UPDATE orders SET customer_uuid = customers.uuid
  FROM customers WHERE orders.customer_id = customers.id;

-- Step 2: Migrate code to use customer_uuid (separate deploy)

-- Step 3: Contract (remove old column, next release)
ALTER TABLE orders DROP COLUMN customer_id;
```

---

## Refactoring Monoliths with AI

## Maintaining Test Coverage During Refactoring
- Ask the AI to generate characterization tests before touching code
- Use approval/snapshot testing to lock current behavior
- Track coverage diff per PR, not just absolute numbers
- Generate contract tests at new module boundaries
- Treat test failures as information, not obstacles

```python
# Characterization test: lock existing behavior
def test_calculate_tax_current_behavior():
    """Generated by AI to capture existing behavior
    before refactoring the tax module."""
    result = calculate_tax(amount=100, region="US-CA")
    assert result == Decimal("9.50")  # current rate
    result = calculate_tax(amount=100, region="US-OR")
    assert result == Decimal("0.00")  # no sales tax
```

---

## Refactoring Monoliths with AI

## Testing Strategies During Decomposition
- Contract tests verify that extracted services honor the original API
- Consumer-driven contracts let each caller define expected behavior
- Run old and new implementations in parallel to compare outputs
- AI can generate `Pact` or `Spring Cloud Contract` test suites
- Shadow traffic testing catches edge cases before full cutover

```python
# Consumer-driven contract test (Pact-style)
def test_billing_service_contract():
    """Verifies the extracted billing service
    matches what the order module expects."""
    pact = Pact(consumer="OrderService",
                provider="BillingService")
    pact.given("a valid customer").upon_receiving(
        "a charge request"
    ).with_request(
        method="POST", path="/charge",
        body={"customer_id": "123", "amount_cents": 5000}
    ).will_respond_with(
        status=201, body={"charge_id": Like("ch_abc")}
    )
```

---

## Refactoring Monoliths with AI

## Managing Technical Debt with AI
- Ask the AI to scan for common debt indicators in a module
- Prioritize by blast radius: debt in hot paths costs more
- Track debt items as first-class work items, not vague wishes
- Use AI to estimate refactoring effort and risk for each item
- Schedule debt paydown alongside feature work in each sprint

```misc
AI-assisted debt identification prompt:
"Analyze src/billing/ and classify technical debt:
1. Code duplication (DRY violations)
1. Missing error handling
1. Hardcoded configuration values
1. Functions exceeding 50 lines
1. Missing or outdated tests
Rank by estimated impact on maintainability."

Example output:
| File               | Issue              | Severity | Effort |
|--------------------|--------------------|----------|--------|
| charge.py:142      | 3 duplicate blocks | High     | 2h     |
| invoice.py:89      | No error handling  | Critical | 1h     |
| tax_rates.py:12    | Hardcoded values   | Medium   | 30m    |
```

---

## AI-Powered Code Review in Monoliths

## Reviewing Changes That Span Multiple Modules
- Monolith PRs often touch 10+ files across different domains
- AI can map each changed file to its module and flag cross-cutting risk
- Ask the AI to verify that all call sites are updated consistently
- Detect subtle issues: mismatched error types, missing null checks
- Generate review checklists tailored to the modules involved

```misc
AI-assisted review prompt:
"This PR modifies files in /src/billing, /src/auth,
and /src/shared/db. For each module:
1. Summarize the intent of the change
1. Identify any breaking contract changes
1. Flag inconsistencies across module boundaries
1. Check that error handling follows module conventions
1. Verify test coverage for the modified code paths"
```

---

## AI-Assisted Code Archaeology

## Understanding Legacy Code
- Feed the AI a function and ask "what does this actually do?"
- Have it rename variables from `x1`, `tmp2` to meaningful names
- Ask for invariants and preconditions the code assumes
- Detect dead code paths and unreachable branches
- Generate inline documentation for the next developer

```python
# Before: legacy code with no documentation
def proc(d, f, t):
    r = []
    for i in d:
        if i[2] > f and i[2] < t:
            r.append((i[0], i[1], i[2] - f))
    return sorted(r, key=lambda x: x[2])

# AI output: "Filters records by date range [f, t),
# shifts timestamps relative to start date,
# returns results sorted by relative offset"
```

---

## AI-Assisted Code Archaeology

## Documenting Tribal Knowledge
- Interview senior developers and feed transcripts to the AI
- Ask the AI to reconcile code behavior with verbal descriptions
- Generate architectural decision records (ADRs) from git history
- Document "why" not just "what" for critical business logic
- Create onboarding guides from accumulated context

```misc
Prompt: "Given these 47 commits touching the pricing engine
between 2019-2022, and the following notes from the team lead,
generate an ADR explaining why we moved from percentage-based
to tiered pricing, including the rollback capability."
```

---

## AI-Assisted Code Archaeology

## Architecture Decision Records with AI
- ADRs capture the context and rationale behind major decisions
- AI can draft ADRs from commit diffs, PR descriptions, and Slack threads
- Use a standard template: status, context, decision, consequences
- Store ADRs alongside code in `docs/adr/` for discoverability
- Revisit and update ADRs when the landscape changes

```markdown
# ADR-0017: Extract Notification Service from Monolith

## Status
Accepted

## Context
The notification module has grown to 12K LOC with its own
database tables. It changes independently from billing at a
3:1 commit ratio. AI analysis of the dependency graph shows
only 2 inbound call sites from the order module.

## Decision
Extract notifications into a standalone service communicating
via an event bus. Maintain a thin adapter in the monolith
during the transition period.

## Consequences
- Reduced monolith build time by ~40 seconds
- Notification team can deploy independently
- Requires event schema versioning discipline
```

---

## AI-Assisted Code Archaeology

## Mapping Undocumented APIs and Protocols
- Point the AI at network calls, serialization code, or IPC channels
- Ask it to infer request/response schemas from usage patterns
- Generate OpenAPI specs from handler implementations
- Detect protocol versioning and backward compatibility issues
- Build dependency maps of internal service communication

```python
# AI can infer this undocumented protocol from usage:
# POST /internal/ledger/entry
# Headers: X-Idempotency-Key, X-Source-Service
# Body: {"account_id": str, "amount_cents": int,
#        "type": "credit"|"debit",
#        "metadata": {"ref": str, "timestamp": iso8601}}
# Response: 201 {"entry_id": str} | 409 {"existing_id": str}
```

---

## Hands-On Exercise

## Exploring an Unfamiliar Monolith
- Clone the provided sample monolith repository
- Use AI to build a mental map without reading any documentation
- Identify module boundaries, entry points, and shared state
- Propose one extraction candidate with justification

```misc
Exercise steps (30 minutes):
1. Ask the AI: "List the top-level directory structure
   and explain what each module likely does"
1. Ask: "Find the main entry point(s) of this application"
1. Ask: "Which modules share database tables?"
1. Ask: "Identify the module with the fewest inbound
   dependencies that could be extracted first"
1. Write a one-paragraph extraction plan based on
   the AI's findings

Debrief questions:
- Where did the AI guess correctly vs. incorrectly?
- What signals helped the AI the most?
- What context would have improved its analysis?
```

---

## Key Takeaways

## Working Effectively with AI in Large Codebases
- AI is powerful but context-limited; your job is to be the guide
- Invest in `CLAUDE.md`, project maps, and structured documentation
- Feed context incrementally: interfaces first, then implementations
- Use AI for exploration loops: hypothesize, search, verify, refine
- Refactor in small, safe, tested steps with AI-generated scaffolding
- Treat legacy code archaeology as a first-class AI use case
- The best results come from developer judgment plus AI execution
