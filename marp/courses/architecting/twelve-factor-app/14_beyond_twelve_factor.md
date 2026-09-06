---
tags:
  - concepts:architecture
  - concepts:best-practices
level: intermediate
category: architecture
audience:
  - audiences:architects
  - audiences:developers

---

# Beyond Twelve-Factor

---

## What's Missing From the Original

- The original twelve factors were written before observability was a discipline
- Before security became table stakes
- Before APIs became products in their own right
- Modern teams add factors to address these gaps

---

## Beyond The Original Twelve

![beyond_factors](svg/courses/architecting/twelve-factor-app/14_beyond_twelve_factor/beyond_factors.svg)

---

## API-First Design

- Define the API before writing code
- The API is the contract; implementations follow
- Generated code from API specs (OpenAPI, gRPC, GraphQL schemas)
- Consumers can build against the contract before the service exists

---

## Why API-First

- Two teams can work in parallel — consumer and producer
- Mocks for testing come from the contract
- Breaking changes are caught when the contract changes, not at runtime
- The API is the integration point; treating it as code is good discipline

---

## Telemetry

- Three pillars: logs, metrics, traces
- Logs: discrete events (factor XI)
- Metrics: numerical time series (request rate, latency, error rate)
- Traces: distributed call paths
- All three together = observability

---

## Telemetry as a Factor

- Apps should emit metrics and traces, not just logs
- OpenTelemetry as the standard
- Per-request trace context propagated across service boundaries
- The platform routes the data; the app just emits

---

## Authentication and Authorization

- Apps need to know who is making the request and what they may do
- Authentication: who? (JWT, OAuth, mTLS)
- Authorization: may they? (RBAC, ABAC, policy engines)
- Both should be standardized across services, not reinvented per service

---

## Identity Federation

- Single source of truth for users
- Each service trusts the central identity provider
- Tokens carry identity claims; services validate them
- OAuth 2.0 + OIDC is the most common pattern

---

## Security as a First-Class Concern

- HTTPS everywhere — even between internal services
- Input validation at every boundary
- Secrets never in logs, never in errors
- Dependencies scanned for known vulnerabilities
- Container images scanned before deploy

---

## Backups and Disaster Recovery

- Twelve-factor doesn't address operational backup strategy
- Backing services (databases, blob stores) need backups
- Point-in-time recovery for data
- Region failover for availability
- These are platform concerns; the app should be region-portable

---

## Cost Awareness

- Modern factor: the app should expose cost-relevant signals
- "How much does each request cost in cloud spend?"
- Metrics that include resource consumption
- Helps make architectural decisions with cost in mind

---

## The "Beyond Twelve" Lists

- Pivotal added 3: API-first, telemetry, authentication
- Some lists add 5+: failure as a feature, immutability, observability, etc.
- The exact count is less important than the direction
- The original 12 are the foundation; modern systems extend them

---

## Twelve-Factor Is a Floor, Not a Ceiling

- Following them gets you to "deployable, scalable, operable"
- Excellent systems go further: observability, security, cost, reliability
- The factors are a starting point, not the destination
- A team that doesn't even meet the factors won't reach the additions

---

## Summary

- The original twelve factors are a foundation
- Modern extensions: API-first, telemetry, security, cost awareness
- "Beyond twelve" is informal but widely practiced
- Treat the factors as a baseline; build observability and security on top
