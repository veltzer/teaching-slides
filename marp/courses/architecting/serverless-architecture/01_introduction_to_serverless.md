---
tags:
  - architecture:serverless
level: intermediate
category: architecture
audience:
  - audiences:developers

---
# Introduction to Serverless

---
## What This Chapter Covers

- What serverless means
- Functions-as-a-Service (FaaS)
- Backend-as-a-Service (BaaS)
- Pay-per-use model
- Where serverless wins; where it loses
- The major providers

---
## Serverless Anatomy

![serverless_anatomy](svg/courses/architecting/serverless-architecture/01_introduction_to_serverless/serverless_anatomy.svg)

---
## What "Serverless" Means

- You don't manage servers; the cloud does
- Code runs on demand
- Auto-scales (including to zero)
- Pay only for execution time
- Servers still exist; you just don't see them

---
## FaaS: Functions-as-a-Service

- The classic serverless: write a function; deploy
- Runs on demand, scales automatically
- Examples: AWS Lambda, Azure Functions, Google Cloud Functions
- Per-invocation billing
- Cold start on first invocation

---
## BaaS: Backend-as-a-Service

- Hosted services that replace your custom code
- Auth: Auth0, Cognito, Firebase Auth
- DB: Firebase, DynamoDB, FaunaDB
- Storage: S3, Cloudinary
- Combine BaaS + FaaS to build apps without managing servers

---
## Pay-Per-Use

- Bill by: invocations + execution time + memory
- Idle: $0
- Sporadic load: very cheap
- Sustained heavy load: more expensive than VMs
- Match the model to your traffic

---
## Where Serverless Wins

- Sporadic / unpredictable workloads
- Event-driven (S3 uploads, SQS messages, scheduled tasks)
- API backends with variable traffic
- Glue between services
- Rapid development

---
## Where Serverless Loses

- Sustained high CPU
- Long-running processes (>15 minutes typical)
- Stateful applications
- Predictable load: VMs are cheaper
- Performance-critical (cold starts hurt)

---
## Cold Starts

- First invocation after idle: slow
- Container cold start: 100ms-2s
- VM warm-up: longer
- Mitigation: provisioned concurrency, lighter runtimes
- Often-cited downside; often overstated

---
## The Major Providers

- **AWS Lambda**: dominant; deepest ecosystem
- **Azure Functions**: tight Microsoft integration
- **Google Cloud Functions / Cloud Run**: strong for events
- **Cloudflare Workers**: edge; sub-ms cold start
- **Vercel / Netlify**: web-focused; built on the above

---
## A Simple Example

```python
def lambda_handler(event, context):
    name = event.get('name', 'world')
    return {
        'statusCode': 200,
        'body': f'Hello, {name}!'
    }
```

- One function, one event
- Deploy: zip and upload
- Invoke: HTTP, scheduled, queue, ...
- Scale to zero when idle

---
## Vendor Lock-In

- Lambda code differs from Azure Functions code (interfaces, idioms)
- Migration: significant work
- Mitigation: serverless framework, abstraction layers
- Reality: most teams pick one and stay
- Trade-off: vendor lock-in for less ops burden

---
## Edge Computing

- Run functions at the network edge
- Cloudflare Workers, AWS Lambda@Edge
- Sub-ms cold start; per-request execution near the user
- Different programming model (V8 isolates, not containers)
- Where: latency-sensitive, lightweight transformations

---
## When Serverless Is The Wrong Choice

- You need persistent connections (long polls, WebSockets)
- You have very long-running jobs
- You need to control the runtime (specific kernel, drivers)
- You have cost-sensitive predictable load
- You're doing something CPU/RAM heavy 24/7

---
## What's Next

- Design patterns specific to serverless
- Cold starts in detail
- State management (you're stateless)
- Event sources and integration
- Testing, cost, security
