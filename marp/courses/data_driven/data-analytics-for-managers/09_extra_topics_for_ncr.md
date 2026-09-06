---
tags:
  - data-and-ai:data-analytics
  - infrastructure:cloud
level: beginner
category: data-driven
audience:
  - audiences:managers

---

# Extra Topics: Cloud, Modern Architecture, Industry Examples

---

## What This Chapter Covers

- GCP tools for data analytics
- Modern application concepts: containers, serverless, microservices
- An example from retail
- How architecture choices affect what data you can collect
- A short tour for the manager who wants to ask better questions

---

## GCP Data Stack

- **BigQuery**: serverless warehouse; SQL at petabyte scale
- **Dataflow**: streaming and batch processing
- **Pub/Sub**: messaging backbone
- **Looker**: BI / semantic layer
- **Vertex AI**: ML platform
- Tightly integrated; hard to leave once committed

---

## AWS Data Stack

- **S3**: cheap storage; the "lake"
- **Athena**: serverless SQL on S3
- **Glue**: ETL and metadata catalog
- **Redshift**: warehouse
- **SageMaker**: ML
- More pieces, more flexibility, more sharp edges

---

## Azure Data Stack

- **ADLS**: data lake storage
- **Synapse**: integrated analytics platform
- **Databricks**: jointly delivered with Microsoft for spark + ML
- **Power BI**: BI layer
- Strong fit for organisations already on Microsoft enterprise stack

---

## Three Clouds Side By Side

![cloud_stack_compare](svg/courses/data_driven/data-analytics-for-managers/09_extra_topics_for_ncr/cloud_compare.svg)

---

## Containers

- Application packaged with all its dependencies
- Runs the same on a laptop and in production
- Docker is the dominant tool
- Underpins much of cloud-native infrastructure
- For data: lets you ship analytics jobs as containers, schedule with orchestrators

---

## Container Orchestration

- Kubernetes: the dominant orchestrator
- Schedules containers across many machines
- Handles restarts, scaling, networking
- Powers most cloud-native data platforms today
- Operationally complex; managed services (EKS, GKE, AKS) ease the burden

---

## Microservices

- Many small services instead of one big app
- Each service owns its data
- Independent deploys, independent scaling
- Trade-off: more complexity, more network calls, harder to reason about
- For data: many sources to integrate; analytics gets harder

---

## Serverless

- Functions-as-a-service: write a function, the cloud runs it on demand
- AWS Lambda, GCP Cloud Functions, Azure Functions
- Pay per invocation; no server management
- Great for: glue between systems, event-driven analytics, low-volume workloads
- Bad for: long-running jobs, predictable high-volume traffic

---

## Service Mesh

- Adds traffic control and observability between microservices
- Tools: Istio, Linkerd, Consul Connect
- Centralised security policies, mTLS, retries
- Strong observability data flows out (a benefit for analytics)
- Heavy operational burden; only worth it past a certain scale

---

## VMs vs Containers vs Serverless

- **VMs**: full machines; minutes to start; expensive, flexible
- **Containers**: process boundaries; seconds to start; cheap, dense
- **Serverless**: function-level; milliseconds to start; pay per invocation
- Modern apps mix all three
- For data: pick by workload shape — serverless for spiky, VMs for sustained

---

## Web Functions / Cloud Functions

- Code triggered by HTTP, file upload, queue message
- Auto-scales to zero when idle
- Useful for: data ingestion glue, on-the-fly transformations, webhooks
- Easy to start; *very* easy to lose track of
- Treat them like any other production code — observability, testing, versioning

---

## Industry Example: Retail

- POS systems generate sale events
- Inventory systems track stock by store
- Loyalty programs link customers across visits
- Online + in-store integration is hard but valuable
- Twiggle (search), recommendation engines, dynamic pricing — all data-driven

---

## Architecture Affects Analytics

- Microservices &#8594; data scattered across many DBs &#8594; harder ETL
- Containers + Kubernetes &#8594; rich operational metrics for free
- Serverless &#8594; harder to attach traditional logging
- Choose architectures with data in mind from day 1
- Retrofitting analytics-friendly logging is painful

---

## Data Architecture Patterns

- **Lambda**: batch + speed layers, merged at query time
- **Kappa**: streaming-only, batch is just stream-replay
- **Medallion** (Bronze/Silver/Gold): layered cleaning in a lakehouse
- Each pattern has merits; pick by team and workload
- Don't pick a pattern because it's trendy

---

## Why Managers Should Care

- These choices determine what's possible analytically, years out
- A "we'll figure out analytics later" architecture is a disaster
- Push back when engineering teams pick patterns without analytics input
- The right architecture makes data work easy; the wrong one makes it impossible
- Sit in the architecture review

---

## Course Wrap-Up

- Data is valuable when it changes decisions, not when it's collected
- Frameworks help focus; tools help operationalise
- BI is for consumption; data engineering is for production
- AI helps where decisions are repetitive at scale
- Architecture shapes what's analytically possible — be in those rooms
- The unique manager skill: asking the right question, then trusting the answer

---

## Where to Go Next

- Pick one decision in your area; identify the data it needs
- Map the sources; estimate the gap
- Find an analyst or analytics engineer to partner with
- Run *one* successful project
- Use it to fund the next, bigger one
