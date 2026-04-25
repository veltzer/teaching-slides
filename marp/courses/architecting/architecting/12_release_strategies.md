---
tags:
  - concepts:architecture
  - concepts:deployment
  - practices:release-management
level: advanced
category: architecture
audience:
  - audiences:developers
  - audiences:architects
  - audiences:devops

---
# Release Strategies

---
## Why Release Strategy Matters

- Deploying software is the riskiest moment in its lifecycle
- A bad release can erase a quarter of engineering work in one night
- The right strategy lets you ship small changes frequently with low blast radius
- Architecture determines which strategies are even available to you

---
## Release Goals

- Zero or near-zero downtime during deployment
- Fast rollback when a change misbehaves in production
- Ability to test a new version on real traffic before full rollout
- Ability to ship code and control its release separately
- Confidence that today's deploy will not surprise next week

---
## Deployment Strategies Overview

![deployment_strategies_overview](svg/courses/architecting/architecting/12_release_strategies/deployment_strategies_overview.svg)

---
## Rolling Update

- Gradually replace old instances with new ones over a rollout window
- At any point, both old and new versions run side-by-side
- Zero downtime if the old and new versions are wire-compatible
- Default strategy in Kubernetes Deployments

---
## Rolling Update Visualization

![rolling_update_visualization](svg/courses/architecting/architecting/12_release_strategies/rolling_update_visualization.svg)

---
## Rolling Update Trade-Offs

- **Pros**: no duplicate infra, zero-downtime, simple defaults
- **Cons**: rollback is another rolling update (slow); partial states during rollout
- Requires backward-compatible schema and API changes
- Works poorly when old and new cannot coexist (breaking protocol changes)

---
## Blue/Green Deployment

- Maintain two identical production environments: Blue and Green
- Blue runs the current version; Green receives the new version
- Switch all traffic from Blue to Green in one router change
- Keep Blue warm for instant rollback

---
## Blue/Green Architecture

![blue_green_architecture](svg/courses/architecting/architecting/12_release_strategies/blue_green_architecture.svg)

---
## Blue/Green Trade-Offs

- **Pros**: instant rollback, full pre-prod testing on real infra, simple cutover
- **Cons**: double the infrastructure, expensive for large systems
- Stateful services need careful handling — two copies of a database rarely work
- Long-lived connections (WebSockets, gRPC streams) may need to drain before cutover

---
## Canary Deployment

- Roll out the new version to a small subset of users first (1–5%)
- Monitor error rate, latency, and business metrics against the baseline
- Gradually widen the canary (5% → 25% → 50% → 100%) if metrics stay healthy
- Roll back instantly if any signal degrades

---
## Canary Deployment Flow

![canary_deployment_flow](svg/courses/architecting/architecting/12_release_strategies/canary_deployment_flow.svg)

---
## Canary Metrics to Watch

- Error rate compared to the stable version
- Latency percentiles (p50, p95, p99) — compare distributions, not averages
- CPU and memory utilization
- Business metrics: conversion rate, checkout success, signup completion
- Automated analysis tools compare canary vs baseline and abort on regression

---
## Canary Routing Options

- **Percentage-based** — route N% of all requests to the canary
- **User cohort** — route internal staff, beta users, or a specific region
- **Header-based** — route only requests with a specific header (dogfooding)
- **Shadow traffic** — mirror requests to the canary but discard responses; great for read-only comparison

---
## Progressive Delivery

- An umbrella term for canary with automated analysis
- The system gradually shifts traffic based on real-time metrics
- Human approval becomes optional once metric-based rules are trusted
- Tools: `Flagger`, `Argo Rollouts`, `Spinnaker`

---
## Progressive Delivery Pipeline

- Deploy canary at 5%
- Wait 5 minutes; compare error rate and p99 latency to baseline
- If within tolerance → raise to 20%, wait, compare
- Continue doubling until 100%
- Any failing check pauses or aborts the rollout

---
## Feature Flags

- Decouple *deployment* (the code reaches production) from *release* (the user sees the feature)
- Ship code behind a disabled flag; turn it on when business is ready
- Roll back instantly by flipping the flag — no redeploy needed
- Enables dark launches, A/B tests, and per-user targeting

---
## Feature Flag Architecture

![feature_flag_architecture](svg/courses/architecting/architecting/12_release_strategies/feature_flag_architecture.svg)

---
## Feature Flag Patterns

- **Release flags** — short-lived, turned on once the feature is stable, then removed
- **Experiment flags** — A/B testing, controlled comparison
- **Ops flags** — kill switches for expensive features under load
- **Permission flags** — customer-specific feature gating (long-lived)

Each type has different lifetime expectations. Confusing them creates tech debt.

---
## Feature Flag Tools

- `LaunchDarkly` - commercial feature management platform
- `Unleash` - open-source feature toggle service
- `Flagsmith` - open-source feature flag and remote config
- `Split` - feature delivery with experimentation
- `GrowthBook` - open-source experimentation platform
- Simple config-based flags for small teams

---
## Flag Hygiene

- Every flag is tech debt if it outlives its purpose
- Tag each flag with owner, type, and expected end-of-life
- Dashboard all flags; run a monthly cleanup pass
- Unused flag code paths become untested code paths — delete both sides promptly

---
## Dark Launches

- Deploy the new code and exercise it with real traffic, but do not show users
- Compare results silently against the old path
- Detect performance regressions, bugs, and capacity issues in production
- Extends the canary concept to features, not just versions

---
## Shadow Traffic

- Mirror real production requests to the new version
- Old version's response is returned to the user
- New version's response is compared for correctness and timing
- Perfect for refactors and rewrites where behavior must match exactly

---
## Choosing a Strategy

| Change type | Best strategy |
|-------------|--------------|
| Minor version bump | Rolling update |
| Breaking API change | Blue/Green or expand/contract |
| Risky business logic | Canary + feature flag |
| Experiment / A-B test | Feature flag |
| Rewrite of existing service | Shadow traffic, then canary |
| Database migration | Expand/contract, decoupled from app deploy |

---
## Rollback as a First-Class Concern

- Every deploy plan needs a rollback plan
- Prefer strategies with fast rollback (blue/green, feature flag) for risky changes
- Automate rollback criteria — do not rely on a human spotting the regression
- Practice rollback in non-production at least as often as you practice deploys

---
## Common Pitfalls

- **Rolling update with incompatible versions** — the overlap window breaks
- **Blue/green with shared database** — schema must be compatible with both sides
- **Canary with low traffic** — statistically meaningless until enough requests hit the canary
- **Feature flags that outlive their reason** — the codebase becomes a combinatorial nightmare
- **No rollback drill** — the first real rollback fails because nobody tested the path

---
## Summary

- Rolling updates are the default; simple and cheap but slow to roll back
- Blue/Green offers instant rollback at the cost of double infrastructure
- Canary exposes a new version to real traffic with small blast radius
- Progressive delivery automates canary analysis and traffic shifting
- Feature flags decouple deployment from release and enable instant kill switches
- Choose the strategy for the change's risk profile, not one size fits all
- Rollback must be a first-class, tested part of every deploy plan
