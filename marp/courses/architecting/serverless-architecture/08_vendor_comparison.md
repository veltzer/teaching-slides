---
tags:
  - architecture:serverless
  - infrastructure:cloud
level: intermediate
category: architecture
audience:
  - audiences:architects

---
# Vendor Comparison

---
## What This Chapter Covers

- AWS Lambda
- Azure Functions
- Google Cloud Functions / Cloud Run
- Cloudflare Workers
- Vercel / Netlify
- Choosing
- Multi-cloud considerations

---
## AWS Lambda

- Original FaaS; deepest ecosystem
- Triggers: dozens (every AWS service)
- Runtimes: many languages, custom runtimes
- 15-minute max execution
- Pricing: pay per ms
- The default for AWS shops

---
## AWS Lambda Strengths

- Tightest AWS integration
- Widest ecosystem of integrations
- Provisioned concurrency for cold-start mitigation
- Step Functions for orchestration
- Best-known; most learning resources

---
## AWS Lambda Weaknesses

- Cold starts (especially for Java/.NET)
- Vendor lock-in (Lambda-specific code patterns)
- Pricing complexity (memory x duration x requests)
- 15-min limit (some workloads don't fit)
- Event source quirks (e.g., max 10 messages per SQS batch)

---
## Azure Functions

- Microsoft's FaaS
- Tight integration with Azure ecosystem
- Same languages as Lambda; add F#
- Bindings declarative (input/output)
- Durable Functions for orchestration
- Standard for Azure shops

---
## Azure Functions Strengths

- Bindings simplify integration code
- Durable Functions: stateful serverless workflows
- Visual Studio integration
- Choice of Consumption (pay-per-use), Premium (warm), Dedicated (App Service)
- Strong .NET story

---
## Google Cloud Functions

- Google's original FaaS
- Triggers: GCS, Pub/Sub, HTTP, Firestore
- Recently: Cloud Functions (gen 2) is built on Cloud Run
- Languages: Node, Python, Go, Java, Ruby, .NET
- Used heavily inside GCP

---
## Cloud Run

- GCP's container-as-a-service
- Run any container; serverless billing
- HTTP-driven; scales to zero
- Long-running (up to hours)
- Sweet spot for many workloads

---
## Cloud Run vs Lambda

- Cloud Run: any container, any language, any size
- Lambda: managed runtimes, AWS deep integration
- Cloud Run more flexible; Lambda more integrated
- Both worth knowing; pick by cloud preference
- Cloud Run is closer to "serverless containers"

---
## Cloudflare Workers

- V8-based; sub-ms cold start
- Runs at the edge (200+ locations)
- JavaScript / WASM
- Generous free tier
- Different programming model: no Node APIs by default

---
## Cloudflare Workers Strengths

- Lowest cold start by far
- Cheapest at scale
- Edge: closest to users
- Workers KV, R2, D1: building a full edge platform
- Excellent for: edge logic, A/B testing, CDN customisation

---
## Cloudflare Workers Limits

- No persistent storage in the Worker itself
- Limited V8 APIs (no Node-specific)
- Smaller execution time per request
- Less mature ecosystem than Lambda
- Different mental model

---
## Vercel / Netlify

- Serverless platforms aimed at frontend / fullstack
- Built on AWS Lambda underneath (and Cloudflare for some)
- Excellent dev experience for JS/TS
- Per-deploy preview URLs
- Costs: a markup on Lambda; pay for the DX

---
## Choosing By Use Case

- Already on AWS / GCP / Azure: pick the native one
- Edge latency critical: Cloudflare Workers
- Frontend-heavy: Vercel / Netlify
- Multi-cloud: Knative (open-source Cloud Run)
- Don't fight the cloud you're already on

---
## Multi-Cloud Serverless

- Rare; expensive; hard to do well
- Usually: pick one cloud; commit
- Abstraction layers (Serverless Framework) help with build, not runtime
- Vendor-specific features lure you in
- Lock-in is the price of convenience

---
## Migration Considerations

- Code interfaces differ (event shape, context)
- Triggers differ (S3 vs Cloud Storage vs Blob Storage)
- IAM differs
- Migration: rewrite, not lift-and-shift
- Plan for it as a project, not a config change

---
## Common Vendor Mistakes

- Choosing by feature lists not real workload fit
- Multi-cloud serverless dreams; rarely worth it
- Locking in to a vendor's proprietary orchestration
- Underestimating migration cost
- Picking by familiarity vs fit
