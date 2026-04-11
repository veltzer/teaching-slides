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
# Rightsizing and Resource Optimization

---

## What is Rightsizing?
- Matching resource size to actual workload needs
- Most common source of cloud waste
- Over-provisioned instances cost too much
- Under-provisioned instances hurt performance
- Continuous process, not a one-time event

---

## The Rightsizing Opportunity
- Studies show 30-40% of cloud instances are over-provisioned
- Average CPU utilization in cloud: 10-20%
- Even small reductions multiply across fleets
- Low-hanging fruit for cost savings
- Start with the biggest instances first

---

## Rightsizing Opportunity

![rightsizing_opportunity](svg/courses/cloud/finops/03_rightsizing/rightsizing_opportunity.svg)

---

## Identifying Underutilized Resources
- CPU utilization consistently below 20%
- Memory utilization consistently below 30%
- Network throughput far below capacity
- IOPS well below provisioned levels
- Use 2-4 weeks of data for accurate assessment

---

## Identifying Idle Resources
- Instances with near-zero CPU for days
- Load balancers with no targets
- Unattached EBS volumes or disks
- Unused Elastic IPs (charged when idle)
- Old snapshots and AMIs no longer needed

---

## Rightsizing Compute Instances
- Analyze CPU, memory, network utilization
- Move to smaller instance types
- Consider burstable instances (t3) for variable workloads
- Switch generations (m5 -> m6i: better price/performance)
- Test before changing production instances

---

## Graviton and ARM Instances
- AWS Graviton (ARM-based) processors
- 20-40% better price/performance than x86
- Azure Ampere-based VMs, GCP Tau T2A
- Most workloads run without code changes
- Significant savings for compatible workloads

---

## Storage Tier Optimization
- Move infrequently accessed data to cheaper tiers
- S3 Standard -> S3 IA -> Glacier
- EBS gp3 is cheaper than gp2 with better performance
- Delete old snapshots and unused volumes
- Use lifecycle policies to automate transitions

---

## Database Rightsizing
- Review RDS instance sizes vs actual utilization
- Consider Aurora Serverless for variable workloads
- Move to reserved capacity for steady databases
- Use read replicas instead of scaling up primary
- Evaluate managed vs self-hosted cost

---

## Automated Rightsizing Recommendations
- AWS Compute Optimizer
- Azure Advisor
- GCP Recommender
- Third-party tools (Spot.io, CloudHealth, Datadog)
- Review recommendations weekly, act on them

---

## Get Rightsizing Recommendations

```bash
# Get EC2 rightsizing recommendations
aws compute-optimizer \
  get-ec2-instance-recommendations \
  --filters name=Finding,values=OVER_PROVISIONED \
  --query 'instanceRecommendations[].{
    Id: instanceArn,
    Current: currentInstanceType,
    Recommended: recommendationOptions[0].instanceType,
    Savings: recommendationOptions[0].estimatedMonthlySavings.value
  }'
```

---

## The Rightsizing Process
1. Collect utilization data (2-4 weeks minimum)
1. Identify over-provisioned and idle resources
1. Validate recommendations with application owners
1. Test changes in non-production first
1. Apply changes and monitor impact

---

## Rightsizing Process Flow

![rightsizing_process](svg/courses/cloud/finops/03_rightsizing/rightsizing_process.svg)

---

## Rightsizing Challenges
- Fear of performance degradation
- Lack of ownership ("who approved this instance?")
- Stale resources nobody remembers
- Resistance to change
- Solve with data, testing, and gradual rollout

---

## Auto Scaling as Rightsizing
- Instead of one big instance, auto-scale smaller ones
- Match capacity to demand in real time
- Scale to zero when possible (serverless)
- Target tracking: maintain 60-70% CPU utilization
- Combine with spot instances for more savings

---

## Waste Elimination Checklist
- Unattached EBS volumes
- Old snapshots (>90 days)
- Unused Elastic IPs
- Idle load balancers
- Orphaned security groups and network interfaces
- Test environments running 24/7
