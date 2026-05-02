---
tags:
  - practices:sre
level: intermediate
category: architecture
audience:
  - audiences:developers
  - audiences:devops
---
# SLIs, SLOs, and SLAs

---

## The three letters that anchor SRE

- **SLI** — Service Level **Indicator** — what you measure
- **SLO** — Service Level **Objective** — what you target internally
- **SLA** — Service Level **Agreement** — what you promise externally (with consequences)

Picking these is harder than it looks. Most teams measure too many things and target too many nines.

---

## What makes a good SLI

- **User-facing** — measures user experience, not infrastructure
- **Quantifiable** — a ratio of good events / valid events, not a vague metric
- **Composable** — meaningful when summed across regions, hosts, time
- **Actionable** — when it drops, you know something user-affecting is wrong

```output
availability_sli = successful_requests / valid_requests
latency_sli = requests_under_500ms / valid_requests
```

A good SLI is the kind of metric the user themselves would write down.

---

## Common SLI categories

| Service type | Typical SLIs |
|---|---|
| Request/response | availability, latency |
| Storage | durability, throughput |
| Data pipeline | freshness, correctness |
| Streaming | end-to-end latency, dropped frames |
| Batch | completion rate, on-time delivery |

Pick 2-3 SLIs per service. More SLIs means more dashboards no one reads.

---

## SLI Categories

![sli_categories](svg/courses/architecting/site-reliability-engineering/02_slos_slis/sli_categories.svg)

---

## SLI to SLO to SLA

![slo_pyramid](svg/courses/architecting/site-reliability-engineering/02_slos_slis/slo_pyramid.svg)

---

## Setting an SLO target

```output
Availability SLO: 99.9% of HTTP requests succeed over 28 days
Latency SLO: 95% of requests complete in under 500ms
```

Process:

1. Look at current performance — what does the service actually do?
1. 1. Look at user expectations — what do they need?
1. 1. Set the target slightly below current performance
1. 1. Leave room — "stretch" SLOs cause perpetual error budget drains

The SLO target sets the **error budget**, which is what enables velocity.

---

## The "nines" cost

| SLO | Annual downtime | Engineering effort |
|---|---|---|
| 90% | 36.5 days | trivial |
| 99% | 3.65 days | basic redundancy |
| 99.9% | 8.76 hours | mainstream production |
| 99.95% | 4.38 hours | careful design |
| 99.99% | 52.6 minutes | deep investment |
| 99.999% | 5.26 minutes | exotic; usually impossible |

Each nine is roughly 10× harder than the last. Decide deliberately, not by ambition.

---

## SLO is not SLA

| | SLO | SLA |
|---|---|---|
| Audience | Internal | External (customers) |
| Consequence | Engineering decisions | Money / refunds |
| Target | Tighter than SLA | Looser than SLO |
| Document | Wiki page | Legal contract |

You want your SLO **tighter** than your SLA — internal alarm before external penalty.

If SLO = SLA, you have no safety margin. If SLO < SLA, you misunderstand SRE.

---

## Choosing the measurement window

- **Rolling 28 days** — most common; matches lunar/billing cycles
- **Rolling 7 days** — fast-moving services; spots regressions quickly
- **Quarterly** — reliability-critical services with long incidents

Resist the temptation to measure SLOs hourly. Short windows make noise look like signal.

---

## Where SLIs come from

- **Server-side metrics** — easiest to gather, but server-perspective
- **Load balancer logs** — closer to the user
- **Real user monitoring (RUM)** — actual browser/app telemetry
- **Synthetic probes** — your own checks; baseline for known scenarios
- **Client-side instrumentation** — most accurate, hardest to deploy

Different sources produce different numbers. Document which one is the SLO source of truth.

---

## Documenting your SLO

Every service should have a one-page SLO document:

```output
Service: Checkout API
SLI: availability — successful HTTP responses / valid requests
SLI: latency — requests served in <500ms p95
SLO: availability ≥ 99.9% over 28 days
SLO: latency ≥ 95% under 500ms over 28 days
SLA: availability ≥ 99.5% (refund-triggering)
Owner: checkout-team@
Last reviewed: 2026-Q1
```

The doc is the deliverable. Without it, "SLO" is hand-waving.
