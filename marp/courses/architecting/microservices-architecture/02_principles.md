---
tags:
  - concepts:microservices
level: intermediate
category: architecture
audience:
  - audiences:developers
  - audiences:architects

---
# Microservices Principles

---
## Single Responsibility

- A service does one thing well
- The thing is usually a business capability, not a technical layer
- Examples: "Orders", "Inventory", "Notifications" — not "DAO", "API", "Worker"
- A service description fits in one sentence

---
## Independent Deployability

- A service can be deployed without coordinating with other services
- A change in service A doesn't require redeploying service B
- This is the key operational benefit
- Without it, you have a distributed monolith

---
## Owning Your Data

- Each service has its own database
- No service reads or writes another service's database directly
- Data needed across services flows through APIs or events
- Database-per-service is the line you don't cross

---
## Decentralized Data

- Different services may use different database technologies
- Postgres for orders, Elasticsearch for search, Redis for sessions
- Each service picks what fits its workload
- The cost: data consistency is now a distributed-systems problem

---
## API Contracts

- A service exposes a clear, versioned API
- Consumers depend on the API, not on implementation details
- Internal data structures are private
- The API is what changes the most carefully

---
## Smart Endpoints, Dumb Pipes

- Logic lives in services, not in middleware
- Message brokers transport messages but don't transform them
- Avoid putting business rules in routing layers or ESBs
- The boundary between services is the API; nothing else gets between

---
## Design for Failure

- Networks fail; services restart; nodes die
- Every cross-service call is fallible
- Services have to handle other services being down or slow
- This is a discipline; "happy path only" code dies fast in microservices

---
## Domain-Driven Boundaries

- Service boundaries follow the domain, not the org chart
- Bounded contexts (chapter 4) are the unit
- Conway's Law: the system structure mirrors the team structure — be intentional about it

---
## Conway's Law in Practice

- "Organizations design systems that mirror their communication structure"
- A service per team is the easiest match
- A team across services or a service across teams creates friction
- Inverse Conway's: design the team structure to fit the desired system structure

---
## Observability First

- A monolith is debuggable with logs and a debugger
- Microservices require distributed tracing, structured logs, metrics from day one
- "We'll add observability later" — you'll regret it
- Build the observability stack before you build the second service

---
## Automation Required

- Manual deploy of 1 service: tolerable
- Manual deploy of 50 services: impossible
- CI/CD per service is mandatory
- Service templates and platform tooling save lives

---
## The Twelve-Factor Connection

- Each microservice should be a twelve-factor app
- Stateless processes, env-based config, etc.
- Microservices and twelve-factor reinforce each other
- Violating twelve-factor in microservices is doubly painful

---
## What "Micro" Doesn't Mean

- Not "lines of code" — services can be large or small
- Not "team size" — small teams can run many services
- Not "function-per-service" — that's serverless
- "Micro" describes the boundary discipline, not the size

---
## Anti-Patterns

- Shared databases between services
- Synchronous chains: A calls B calls C calls D — long latency, fragile
- Service per CRUD entity — too granular
- Distributed transactions across services — needs sagas (separate course)
- Every service has its own platform tooling

---
## Summary

- Single responsibility per service, owned by a single team
- Independent deployment, owned data, clear API contracts
- Design for failure; build observability first
- Domain boundaries (next chapter), not technical boundaries
- The "micro" is about discipline, not size
