---
tags:
  - practices:sre
  - practices:release-engineering
level: intermediate
category: architecture
audience:
  - audiences:developers
  - audiences:devops
---

# Release Engineering and Capacity Planning

---

## The release engineering principle

> "How software gets to production is software."

- The release pipeline is a service with its own SLOs
- It has bugs, outages, and operational cost
- It deserves engineering attention, not duct-tape scripts
- Treat release engineering as a real engineering discipline

Most outages are caused by recent changes. The release process is therefore your highest-leverage reliability investment.

---

## Progressive rollouts

Don't deploy to 100% of users at once. Stage it:

1. **Dev/staging** — internal smoke tests
1. 1. **Canary** — 1-5% of production for hours
1. 1. **Wave 1** — 10-25% for hours-to-day
1. 1. **Wave 2** — 50%
1. 1. **Full rollout** — 100%

Each wave generates SLI data. Auto-pause if errors spike. Auto-rollback if the SLO budget is hit.

---

## Progressive Rollout

![canary](svg/courses/architecting/site-reliability-engineering/07_release_capacity/canary.svg)

---

## Feature flags

- Decouple **deploy** from **release**
- Code ships to production behind a flag, off by default
- Turn the flag on for 1% → 10% → 100%, monitoring as you go
- Turn it off in seconds if something breaks — no rollback needed

```python
if feature_flag.enabled("new_checkout", user):
    new_checkout_flow()
else:
    legacy_checkout_flow()
```

LaunchDarkly, Unleash, and homegrown systems all do this. The pattern is more important than the tool.

---

## Rollback strategies

- **Forward fix** — push another deploy to fix the issue (slow, often safe)
- **Rollback** — redeploy the previous version (fast, but state migrations may not reverse)
- **Flag flip** — toggle the feature flag off (instant, no code change)
- **Database rollback** — almost always the hardest case; design forward-compatible migrations

Rule: rollback should be the **default response** to any production regression. Forward-fix only if you're confident.

---

## Blue/green and red/black

- **Blue/green** — two parallel environments; switch traffic atomically
- **Red/black (Netflix)** — same idea, different naming
- Lets you test a full version stack before any traffic flows
- Costs 2× capacity during cutover

For services where canary is hard (state migrations, sticky sessions) blue/green is the alternative.

---

## Capacity planning basics

Plan for:

- **Steady-state load** — current traffic at expected growth
- **Peak load** — Black Friday, marketing launches, viral moments
- **Failure scenarios** — one region down, double the load on the rest
- **Headroom** — buffer for surprise

```output
required_capacity = peak × failure_factor × headroom
                  = 2× × 1.5× × 1.3×
                  = ~4× steady state
```

Cloud autoscaling helps but doesn't replace planning — autoscaling has limits and lag.

---

## Load testing

- **Synthetic load** — generate traffic with k6, Locust, JMeter
- **Replay** — capture production traffic, replay against staging
- **Shadow traffic** — duplicate production requests to a test environment in real time
- **Chaos** — kill components, partition networks (Netflix Chaos Monkey)

Load test before launches. Load test before peak season. Load test routinely so you know your service's actual limits.

---

## Demand forecasting

- Look at historic patterns (year-over-year growth)
- Factor in product launches, marketing campaigns
- Sanity-check against business projections
- Add buffer for unexpected growth

```output
Q4 capacity = Q3 actual × (1 + growth_rate)
            + Black Friday spike factor
            + 30% buffer
```

The cost of over-provisioning is money. The cost of under-provisioning is an incident. They are not symmetric.

---

## Cost optimization

- Right-size before you scale — over-provisioned services waste money
- Reserved/committed instances for steady load (1-3 year discounts)
- Spot/preemptible instances for batch and stateless work
- Multi-region only where required — egress is expensive
- Track $ per request as a real metric

The goal is **efficient reliability**, not cheap reliability. Cutting cost below safety margins creates incidents, which cost more.

---

## Release velocity vs reliability

- Faster releases → smaller, easier-to-debug changes → fewer incidents
- This is counterintuitive but proven (DORA research)
- Big batches accumulate bugs; small ones surface them quickly
- A team shipping daily has better reliability than one shipping monthly

The 2018 Accelerate book quantified this: elite teams deploy on demand, multiple times per day, with very low change failure rates. Slow ≠ safe.

---

## Reliability sprints

- When error budget is exhausted, dedicate a sprint to reliability
- All engineers (not just the SRE team) work on the top reliability bug
- Output: action items from postmortems get done, monitoring gaps closed
- Often the most productive sprint of the quarter

This is the error budget policy in action. Without sprints to act on the budget, the budget is just a number.
