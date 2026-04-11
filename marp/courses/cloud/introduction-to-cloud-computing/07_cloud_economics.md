---
tags:
  - infrastructure:cloud
  - practices:finops
  - concepts:cloud-economics
level: beginner
category: cloud
audience:
  - audiences:developers
  - audiences:sysadmins
  - audiences:devops
  - audiences:managers

---
# Cloud Economics and Pay-As-You-Go

---

## The Pay-As-You-Go Model
- Pay only for resources consumed
- No upfront hardware purchase
- Billing by the second, hour, GB, or request
- Scale costs with usage
- Turn off resources to stop charges

---

## CapEx vs OpEx
- CapEx: buy servers, 3-5 year depreciation
- OpEx: pay monthly for cloud usage
- Cloud shifts IT from CapEx to OpEx
- Financial flexibility and predictability
- No large upfront investments

---

## CapEx vs OpEx Cost Curves

![capex](svg/courses/cloud/introduction-to-cloud-computing/07_cloud_economics/capex_vs_opex.svg)

---

## Cloud Pricing Dimensions
- Compute: per second or per hour of CPU time
- Storage: per GB per month
- Data transfer: per GB out (inbound usually free)
- Requests: per API call or transaction
- Each service has its own pricing model

---

## Pricing Dimensions

![pricing](svg/courses/cloud/introduction-to-cloud-computing/07_cloud_economics/pricing_dimensions.svg)

---

## On-Demand Pricing
- Pay full price, no commitment
- Most flexible option
- Best for unpredictable or short-term workloads
- No discounts
- Good starting point before optimizing

---

## Reserved Instances and Commitments
- Commit to usage for 1 or 3 years
- Significant discounts (up to 72% off)
- All upfront, partial upfront, or no upfront
- Best for steady, predictable workloads
- Available for compute, databases, and more

---

## Savings Plans
- Flexible commitment-based pricing
- Commit to $/hour of usage
- Applies across instance families and Regions
- More flexible than Reserved Instances
- Available on AWS, similar concepts on other providers

---

## Spot and Preemptible Instances
- Use spare cloud capacity at deep discounts
- Up to 90% savings vs on-demand
- Can be interrupted with short notice
- Best for fault-tolerant and batch workloads
- Not suitable for stateful or critical services

---

## Spot Instance Use Cases
- CI/CD build and test pipelines
- Data processing and ETL
- Rendering and media encoding
- Machine learning training
- Stateless web servers behind load balancers

---

## Cost Monitoring Tools
- Cloud provider billing dashboards
- Cost Explorer: visualize spending trends
- Budgets and alerts: get notified on thresholds
- Cost allocation tags: track by project or team
- Third-party tools: CloudHealth, Spot.io, Kubecost

---

## AWS CLI Cost Query Example

```bash
# Query last month's costs by service
aws ce get-cost-and-usage \
  --time-period Start=2024-01-01,End=2024-01-31 \
  --granularity MONTHLY \
  --metrics "BlendedCost" \
  --group-by Type=DIMENSION,Key=SERVICE
```

---

## Cost Optimization Strategies
- Right-size instances based on actual usage
- Use auto-scaling to match demand
- Delete unused resources (unattached disks, idle IPs)
- Choose the right storage tier
- Schedule non-production environments to stop at night

---

## Total Cost of Ownership (TCO)
- Compare cloud costs vs on-premises costs
- Include: hardware, power, cooling, space, staff
- Include: networking, maintenance, refresh cycles
- Cloud TCO tools from major providers
- Often surprising how expensive on-premises really is

---

## Hidden Costs to Watch
- Data transfer between Regions or out to internet
- NAT Gateway per-GB charges
- Idle resources still incurring charges
- Over-provisioned storage
- Unused Reserved Instances

---

## Cost Governance
- Establish budgets per team and project
- Tag all resources for cost attribution
- Regular cost reviews (weekly or monthly)
- Automated enforcement of tagging policies
- FinOps culture: engineers own their costs

---

## Cloud Financial Planning
- Forecast costs based on growth projections
- Use cloud pricing calculators
- Plan commitment purchases annually
- Build cost awareness into architecture reviews
- Treat cost as an architectural constraint

---

## Pricing Calculators
- AWS Pricing Calculator
- Azure Pricing Calculator
- GCP Pricing Calculator
- Model costs before deploying
- Compare configurations and regions

---

## Cost Allocation Tags
- Tag every resource (project, team, environment)
- Tags appear in billing reports
- Enable showback and chargeback
- Enforce tagging via policies
- Essential for multi-team organizations

---

## Tagging Resources for Cost Tracking

```bash
# Tag an EC2 instance for cost tracking
aws ec2 create-tags \
  --resources i-0abc123def456 \
  --tags Key=Project,Value=WebApp \
       Key=Team,Value=Backend \
       Key=Environment,Value=production
```

---

## Automating Cost Savings
- Schedule dev/test environments to shut down at night
- Auto-delete old snapshots and AMIs
- Use Lambda/Functions for automated cleanup
- Resize instances based on CloudWatch metrics
- Set up automated spot instance management

---

## Cloud vs On-Premises TCO Example
- On-premises: $500K server purchase + $100K/year ops
- Cloud: $80K/year with right-sizing and commitments
- Break-even in 2-3 years for many workloads
- Cloud wins for variable or growing workloads
- On-premises may win for very stable, predictable workloads

---

## The Economics Advantage
- Start small, grow as revenue grows
- Experiment without financial risk
- No wasted capacity
- Global expansion at marginal cost
- Cloud economics enable innovation
