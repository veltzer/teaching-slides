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
# Spot Instances and Preemptible Resources

---

## What Are Spot Instances?
- Unused cloud capacity offered at deep discounts
- Up to 90% savings vs on-demand
- Can be interrupted with short notice (2 minutes on AWS)
- Available on AWS, Azure (Spot VMs), GCP (Preemptible/Spot VMs)
- The cheapest compute option in the cloud

---

## How Spot Pricing Works
- Price fluctuates based on supply and demand
- When your max price < spot price, instance is reclaimed
- AWS: no longer auction-based, gradual price changes
- Azure/GCP: eviction based on capacity needs
- Check price history before choosing instance types

---

## Spot-Friendly Workload Patterns
- Stateless applications behind load balancers
- Batch processing and data pipelines
- CI/CD build and test jobs
- Machine learning training
- Rendering, encoding, scientific computing

---

## Workloads to Avoid on Spot
- Stateful databases
- Single-instance applications with no redundancy
- Long-running jobs that cannot checkpoint
- Real-time critical services
- Anything that cannot tolerate interruption

---

## Handling Interruptions
- Design for graceful shutdown
- Checkpoint progress regularly
- Use interruption notices (2 min on AWS)
- Distribute across multiple instance types and AZs
- Requeue interrupted work automatically

---

## Spot Fleet Management
- Request a mix of instance types and AZs
- Diversification reduces interruption risk
- AWS Spot Fleet, Azure VMSS, GCP MIGs
- Capacity-optimized allocation strategy
- Let the provider choose the best options

---

## Mixing Spot and On-Demand
- Base capacity on on-demand or reserved
- Burst capacity on spot
- Auto Scaling groups with mixed instances
- Example: 30% on-demand base, 70% spot burst
- Ensures minimum capacity even during interruptions

---

## Spot in Kubernetes
- Node pools with spot instances
- Pod disruption budgets handle evictions
- Cluster Autoscaler supports spot
- Karpenter (AWS): intelligent spot provisioning
- Run non-critical pods on spot, critical on on-demand

---

## Cost Savings Estimation
- Compare on-demand price vs average spot price
- Factor in interruption overhead (re-runs)
- Typical effective savings: 60-80%
- Track actual savings monthly
- Savings compound across large fleets

---

## Spot Instance Best Practices
- Diversify across at least 4 instance types
- Use capacity-optimized allocation
- Implement graceful shutdown handlers
- Use checkpointing for long jobs
- Monitor spot prices and interruption rates

---

## AWS Spot Features
- Spot Placement Score: likelihood of getting capacity
- Spot Fleet: manage a collection of spot instances
- EC2 Fleet: combine on-demand, reserved, and spot
- Capacity Rebalancing: proactive replacement
- Integrated with Auto Scaling Groups

---

## Real-World Spot Savings
- Many organizations run 50-70% of compute on spot
- Netflix, Lyft, Samsung use spot extensively
- CI/CD pipelines: nearly 100% spot
- ML training: checkpoint and resume on interruption
- Spot is the biggest hidden cost saver in cloud
