---
tags:
  - infrastructure:cloud
  - practices:finops
  - practices:cost-optimization
level: intermediate
category: cloud
audience:
  - audiences:devops
  - audiences:architects
  - audiences:managers

---

# Organizational Best Practices

---

## Establishing a FinOps Team
- Dedicated or virtual team
- Cross-functional: engineering, finance, management
- Starts small (1-2 people), grows with maturity
- Reports to CTO, CFO, or VP of Engineering
- Empowered to drive change

---

## FinOps Team Responsibilities
- Maintain cost visibility and reporting
- Drive optimization initiatives
- Educate teams on cost awareness
- Negotiate with cloud providers
- Set and enforce policies

---

## Center of Excellence Model
- Central team sets standards and provides tools
- Each team owns their own cost optimization
- Central team enables, not bottlenecks
- Shared dashboards and best practices
- Regular cross-team knowledge sharing

---

## FinOps Team Model

![finops_team_model](svg/courses/cloud/finops/08_organizational_best_practices/finops_team_model.svg)

---

## Engineering Practices That Reduce Cost
- Choose the right architecture (serverless vs always-on)
- Implement caching to reduce compute and API calls
- Optimize data transfer (compress, batch, reduce)
- Use managed services vs self-managed
- Design for auto-scaling from the start

---

## Cost-Aware Architecture
- Consider cost in architecture decisions
- Serverless for intermittent workloads
- Spot for batch and CI/CD
- Reserved for steady-state
- Multi-tier storage for data lifecycle

---

## Cost in the Development Lifecycle
- Estimate costs during design phase
- Include cost in pull request reviews (Infracost)
- Cost metrics in deployment dashboards
- Post-deployment cost validation
- Cost as a non-functional requirement

---

## Infracost in CI/CD

```bash
# Estimate cost of Terraform changes
infracost breakdown --path .

# Show cost diff in pull requests
infracost diff \
  --path . \
  --compare-to infracost-base.json \
  --format json \
  --out-file infracost-diff.json

# Post comment to GitHub PR
infracost comment github \
  --path infracost-diff.json \
  --repo myorg/myrepo \
  --pull-request 42
```

---

## Vendor Negotiation
- Enterprise Discount Programs (EDPs)
- Commit to spend in exchange for discounts
- AWS: EDP, Azure: Enterprise Agreement, GCP: CUDs
- Negotiate based on actual and projected usage
- Leverage multi-cloud optionality

---

## Enterprise Agreements
- Multi-year commitments with volume discounts
- Private pricing for specific services
- Dedicated support and account management
- Typically for $1M+ annual spend
- Review terms carefully (minimum commitments)

---

## Continuous Improvement
- FinOps is never done
- Regular optimization sprints
- Quarterly business reviews of cloud spending
- Benchmark against industry and peers
- Set savings targets and track progress

---

## KPIs for FinOps
- Cost per unit (per customer, per transaction, per request)
- Savings rate (optimized vs on-demand equivalent)
- Coverage rate (% of spend under commitments)
- Waste rate (% of spend on idle/unused resources)
- Budget accuracy (actual vs forecast)

---

## Communicating Cost Savings
- Quantify savings in dollars
- Show trend over time
- Celebrate wins publicly
- Attribute savings to teams and individuals
- Connect savings to business outcomes

---

## Common FinOps Anti-Patterns
- Optimizing without visibility (measure first)
- Over-committing to reservations
- Ignoring data transfer costs
- One-time cleanup without ongoing process
- Cost optimization as punishment instead of empowerment

---

## Getting Started Checklist
1. Enable detailed billing and cost allocation tags
1. Set up budgets and alerts
1. Identify and eliminate obvious waste
1. Rightsize top 20 most expensive resources
1. Evaluate commitment-based discounts
1. Establish regular cost review cadence
