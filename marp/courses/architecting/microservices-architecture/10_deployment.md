---
tags:
  - concepts:microservices
  - practices:ci-cd
  - infrastructure:containers
level: intermediate
category: architecture
audience:
  - audiences:developers
  - audiences:devops

---

# Deployment Strategies

---

## Why Deployment Matters in Microservices

- Many services × many deploys per day = a lot of deploys
- Manual deploys don't scale
- Each deploy is a chance to break production
- Deploy strategy is part of architecture

---

## Deploy Strategies

![deploy_strategies](svg/courses/architecting/microservices-architecture/10_deployment/deploy_strategies.svg)

---

## Deployment Pipeline

![deployment_pipeline](svg/courses/architecting/microservices-architecture/10_deployment/deployment_pipeline.svg)

---

## Containerization

- Each service runs as a container
- The image includes the runtime, dependencies, and code
- Same image runs in dev, staging, prod (twelve-factor X)
- Docker is the de facto standard

---

## Kubernetes as the Platform

- Manages containers across a cluster
- Handles scheduling, scaling, health checks
- Provides primitives: Pods, Deployments, Services, Ingress
- The dominant choice for microservices deployment

---

## CI/CD Per Service

- Each service has its own pipeline
- A change to service A triggers only A's build, test, deploy
- Service B's pipeline is unaffected
- Independent deploys = independent pipelines

---

## Pipeline Stages

- **Build**: compile, build image
- **Test**: unit, integration, contract tests
- **Push**: image to registry with version tag
- **Deploy**: update the deployment manifest, apply
- **Verify**: smoke tests against the new version

---

## Blue-Green Deployment

- Two identical environments: blue (current) and green (new)
- Deploy the new version to green
- Switch traffic from blue to green at once
- Roll back by switching back to blue
- Requires double the infrastructure during deploy

---

## Rolling Deployment

- Gradually replace old instances with new
- One instance at a time (or batches)
- Always some old and some new instances during the deploy
- Default in Kubernetes Deployments

---

## Canary Deployment

- Route a small percentage of traffic to the new version
- Watch metrics; if good, increase the percentage
- If bad, route 100% back to the old version
- Excellent for catching issues before full rollout

---

## Canary Sketch

- 1% to v2, 99% to v1 — for 10 minutes
- Watch error rate, latency, business metrics
- 10% to v2 — for 30 minutes
- 50% — for 1 hour
- 100% — done

---

## Feature Flags

- Decouple deploy from release
- Deploy v2 with a flag turned off
- Turn on the flag for some users (gradually)
- Roll back via flag, no redeploy needed
- Tools: LaunchDarkly, Unleash, in-house

---

## A/B Testing as Deployment

- Two versions running side by side
- Different users see different versions
- Measure which performs better on a metric
- Common in product experimentation

---

## Database Migrations

- The hardest part of deployment
- Schema changes must be backward-compatible during the deploy
- Pattern: expand the schema → deploy code → contract the schema
- Never break the old version's read/write during deploy

---

## Expand-and-Contract

- Phase 1: add new column/table; old version ignores it; new version writes both
- Phase 2: deploy new version everywhere
- Phase 3: backfill data into the new column
- Phase 4: remove old column; old version is gone by now

---

## Rollback Strategy

- Every deploy must be rollback-able
- Easiest: keep the previous image available, redeploy it
- Hardest: schema migrations that aren't reversible — design them differently
- Test rollback like you test deploy

---

## Anti-Patterns

- Manual deploys
- "Deploy on Friday" risk-aversion that defers and clusters changes
- Big-bang releases of multiple services together
- Schema migrations that aren't backward-compatible
- No automated rollback path

---

## Summary

- Containerize; Kubernetes; per-service CI/CD
- Rolling default, canary for high-risk, blue-green when affordable
- Feature flags decouple deploy from release
- Database migrations follow expand-contract
- Automated rollback is mandatory
