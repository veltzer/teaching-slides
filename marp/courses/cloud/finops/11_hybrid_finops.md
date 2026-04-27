---
tags:
  - infrastructure:cloud
  - infrastructure:onprem
  - practices:finops
  - practices:cost-optimization
level: intermediate
category: cloud
audience:
  - audiences:devops
  - audiences:architects
  - audiences:managers

---
# Hybrid FinOps

---

## The Hybrid Reality
- Most enterprises run both cloud and on-prem
- Pure-cloud and pure-on-prem are the exceptions
- Cost discipline must span both
- Unified visibility is the hard part
- FinOps practices apply to all infrastructure

---

## Why Workloads Stay On-Prem
- Regulatory and data sovereignty requirements
- Latency-sensitive applications (factory floor, trading)
- Specialized hardware (mainframes, niche accelerators)
- Already-paid-for capacity with years of life left
- Long-running, predictable workloads where on-prem is cheaper

---

## Why Workloads Move to Cloud
- Variable or bursty demand
- Geographic reach without building datacenters
- Faster time to market
- Access to managed services and AI/ML platforms
- Disaster recovery and resilience

---

## Comparing On-Prem vs Cloud TCO
- Use the same unit (cost per vCPU-hour, per GB-month)
- Include all costs on both sides
- Account for cloud commitments and on-prem depreciation
- Match workload patterns (steady vs bursty)
- Don't forget data egress and inter-region transfer

---

## TCO Comparison Framework

![tco_comparison_framework](svg/courses/cloud/finops/11_hybrid_finops/tco_comparison_framework.svg)

---

## When On-Prem Wins
- Steady-state workloads at high utilization
- Already-purchased hardware with remaining life
- Heavy data egress (cloud egress fees are punishing)
- Extreme storage volumes at predictable growth
- Specialized hardware not available in cloud

---

## When Cloud Wins
- Bursty or unpredictable workloads
- Workloads needing global reach
- Short-lived projects and experiments
- Anything benefiting from managed services
- Workloads with strong elasticity needs

---

## The 70/20/10 Rule
- ~70% of stable production: on-prem or reserved cloud
- ~20% variable load: cloud auto-scaling
- ~10% bursty/experimental: cloud spot or serverless
- Rough heuristic, not a formula
- Adjust based on workload characteristics

---

## Workload Placement Decisions
- Start with workload requirements (latency, scale, compliance)
- Calculate cost in each environment
- Factor in migration cost and risk
- Consider operational maturity in each environment
- Decide per workload, not per organization

---

## Workload Placement Decision Tree

![workload_placement_tree](svg/courses/cloud/finops/11_hybrid_finops/workload_placement_tree.svg)

---

## Avoiding the Worst of Both Worlds
- "Lift and shift" without optimizing: pay cloud prices for on-prem patterns
- Cloud-native rewrite for steady workloads: pay rewrite cost for no benefit
- Spreading thin across both: doubled operational overhead
- Match workload to environment, not the other way around

---

## Data Gravity
- Where data lives, compute follows
- Moving petabytes between cloud and on-prem is expensive
- Egress fees are the silent killer of hybrid
- Plan data placement before compute placement
- Sometimes it's cheaper to keep both copies

---

## Egress Cost Awareness
- AWS egress to internet: $0.09/GB (first 10TB)
- Azure egress to internet: $0.087/GB
- GCP egress to internet: $0.08-0.12/GB
- 10TB monthly on AWS: $900/month ($10,800/year)
- 10TB monthly on Azure: $870/month ($10,440/year)
- 10TB monthly on GCP: $800-1,200/month
- Egress is often the deciding cost factor in hybrid

---

## Hybrid Connectivity Costs
- AWS Direct Connect: $0.30/hour port + data transfer
- Azure ExpressRoute: similar tiered pricing
- GCP Cloud Interconnect: per-port and per-VLAN
- VPN tunnels are cheaper but limited bandwidth
- Factor connectivity into hybrid TCO

---

## Unified Cost Visibility
- Cloud: native tools (Cost Explorer, Cost Management)
- On-prem: home-built or vendor metering
- Combine in a single dashboard
- Tools: Apptio, Flexera, CloudHealth (with on-prem add-ons)
- Same tags, same dimensions, same reports

---

## Hybrid Tagging Strategy
- Use the same tag schema across cloud and on-prem
- Team, Environment, CostCenter, Application
- Enforce in IaC for both VMware and Terraform
- Single source of truth for ownership
- Enables apples-to-apples reporting

---

## Hybrid Cost Dashboard

![hybrid_cost_dashboard](svg/courses/cloud/finops/11_hybrid_finops/hybrid_cost_dashboard.svg)

---

## Governance Across Environments
- Same approval workflows for cloud and on-prem
- Same budget and alert structures
- Same showback or chargeback model
- Avoid creating "cloud-only" or "on-prem-only" rules
- One FinOps team, two environments

---

## Migration Cost Planning
- Migration is not free: tooling, labor, downtime
- Plan workload-by-workload, not all-at-once
- Some workloads should never move
- Repatriation (cloud to on-prem) is also a thing
- Track cost before, during, and after migration

---

## Repatriation: Moving Back to On-Prem
- Some workloads cost less on-prem at scale
- Common for steady, high-volume databases
- Storage-heavy workloads with low elasticity
- Requires rebuilding on-prem capacity
- Real trend, not just hype (Dropbox, 37signals)

---

## Hybrid FinOps Maturity
- Crawl: separate tracking, separate teams
- Walk: unified tagging, joint reporting
- Run: workload placement decisions are data-driven
- Most organizations are still at Crawl
- Walk is where most savings are unlocked

---

## Hybrid FinOps Anti-Patterns
- Treating cloud as "someone else's problem"
- Treating on-prem as "free" because it's already paid for
- Different cost languages for different teams
- Optimizing one side while ignoring the other
- Migrating without comparing TCO

---

## Getting Started with Hybrid FinOps
1. Inventory all workloads across cloud and on-prem
1. Build a unified tagging schema
1. Establish unit costs for each environment
1. Compare workload TCO before placement decisions
1. Report combined cost to leadership monthly
1. Iterate on placement quarterly
