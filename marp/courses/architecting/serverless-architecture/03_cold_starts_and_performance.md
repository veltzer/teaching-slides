---
tags:
  - architecture:serverless
  - architecture:performance
level: intermediate
category: architecture
audience:
  - audiences:developers

---
# Cold Starts and Performance

---
## What This Chapter Covers

- What a cold start is
- Why they matter
- Measurement
- Mitigation: provisioned concurrency, smaller runtimes
- Latency budgets
- When to accept; when to fix

---
## What A Cold Start Is

- Lambda runtime container created from scratch
- Code loaded; runtime initialised; user code begins
- After: container is "warm"; reuses for next invocation
- After idle period (5-30 min): container destroyed
- Next invocation: cold start again

---
## Cold Start Latency

- Java / .NET: 1-3 seconds
- Python / Node: 200-500ms
- Go / Rust: 100-300ms (compiled, smaller)
- WASM (Cloudflare Workers): under 5ms
- Choice of runtime matters

---
## Why It Matters

- User-facing API: 1s extra latency = noticeable
- Business: customer abandons; conversion drops
- Internal: maybe acceptable
- For sporadic traffic: most invocations are cold
- For sustained traffic: most are warm

---
## Measuring Cold Starts

- CloudWatch: duration includes init time
- X-Ray / OpenTelemetry: traces show init separately
- CloudWatch Insights queries
- Look at p99: warm hides cold
- Synthetic tests after deploy: catch initial cold start

---
## Provisioned Concurrency

- Pre-warmed Lambda containers
- Always-ready; no cold start
- Costs: even when idle (defeats free-when-idle)
- Use for: latency-sensitive APIs
- Configure: per-function, per-region

---
## Smaller Runtimes

- Less code = faster init
- Avoid: bundling unnecessary deps
- Tools: tree-shaking, esbuild, native binaries
- A smaller deploy package = faster cold start
- Profile your code; trim ruthlessly

---
## Layer Optimisation

- AWS Lambda Layers: shared libs across functions
- Faster cold start: layers cached
- But: layer size still counts toward init time
- Use sparingly; large layers don't help

---
## Init Code

- Code outside the handler runs once per cold start
- Connection pools, SDK clients, big imports
- Cache as much as possible there
- Handler stays fast on warm invocations

---
## Avoid In Hot Path

- DNS lookups
- Initialising SDKs per call
- Heavy framework startup (Spring Boot, .NET)
- Synchronous file I/O at startup
- Each adds ms to every cold start

---
## Lightweight Frameworks

- Express, FastAPI, Flask: lightweight; ~100-200ms init
- Spring Boot: ~1-3s; not great for Lambda
- Quarkus, Micronaut: GraalVM native images; sub-100ms
- Pick framework with serverless in mind

---
## Latency Budget

- Frontend: 100ms target
- API: 200-500ms acceptable
- Background jobs: seconds OK
- For each tier: pick a runtime that fits
- Don't blow the budget on cold starts

---
## Async Helps

- Async invocations: no client waiting
- Queue-driven: cold start invisible to client
- HTTP APIs: client sees the cold start latency
- Move what you can to async
- Architecture helps; not just runtime tuning

---
## Edge Functions

- Cloudflare Workers: V8 isolates; sub-ms cold start
- Lambda@Edge: traditional Lambda at edge
- For ultra-low latency: edge wins
- Trade-off: smaller runtimes, fewer features
- Worth considering for global APIs

---
## When To Accept Cold Starts

- Internal APIs with relaxed SLAs
- Sporadic / scheduled jobs
- Async pipelines
- Most cold starts hit non-user-facing code
- Optimisation cost > value

---
## Common Performance Mistakes

- Java / .NET for low-latency APIs
- Heavy init code in the handler
- No connection pooling
- Sync calls in chains (cold starts add up)
- Ignoring p99; only looking at average
