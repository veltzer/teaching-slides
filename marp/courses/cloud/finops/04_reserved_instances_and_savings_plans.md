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

# Reserved Instances and Savings Plans

---

## Commitment-Based Discounts
- All major cloud providers offer them
- Trade flexibility for lower prices
- 1-year or 3-year commitments
- Up to 72% savings vs on-demand
- The single biggest cost optimization lever

---

## How Commitments Work
- Commit to a certain level of usage
- Pay a lower rate in exchange
- Unused commitment is still charged
- The discount applies automatically
- Think of it as a volume discount over time

---

## AWS Reserved Instances (RIs)
- Specific instance type, Region, and OS
- Standard RI: fixed attributes
- Convertible RI: can change instance type
- Standard: up to 72% savings
- Convertible: up to 66% savings

---

## RI Payment Options
- All Upfront: largest discount, pay 100% now
- Partial Upfront: moderate discount, pay ~50% now
- No Upfront: smallest discount, pay monthly
- 3-year > 1-year in savings
- Choose based on cash flow and confidence

---

## AWS Savings Plans
- More flexible than Reserved Instances
- Compute Savings Plan: any family, Region, OS, tenancy
- EC2 Instance Savings Plan: specific family and Region
- Commit to $/hour of usage
- Automatically applies to matching usage

---

## Check Savings Plans Coverage

```bash
# View Savings Plans utilization
aws ce get-savings-plans-utilization \
  --time-period Start=2024-01-01,End=2024-01-31

# View coverage (what % is covered)
aws ce get-savings-plans-coverage \
  --time-period Start=2024-01-01,End=2024-01-31 \
  --group-by Type=DIMENSION,Key=INSTANCE_TYPE
```

---

## Savings Plans vs Reserved Instances
- Savings Plans: simpler, more flexible
- RIs: slightly higher savings in some cases
- Savings Plans cover Lambda and Fargate too
- RIs cover only EC2 or RDS
- For new commitments, prefer Savings Plans

---

## Commitment Options Comparison

![commitment_comparison](svg/courses/cloud/finops/04_reserved_instances/commitment_comparison.svg)

---

## Azure Reservations
- Similar concept to AWS RIs
- Available for VMs, SQL Database, Cosmos DB, etc.
- 1-year or 3-year terms
- Up to 72% savings
- Exchange and cancel with some restrictions

---

## GCP Committed Use Discounts
- Committed Use Discounts (CUDs): 1 or 3 year
- Resource-based: specific vCPU and memory
- Spend-based: commit to $ amount
- Up to 57% savings (3-year)
- Also Sustained Use Discounts (automatic, smaller)

---

## Choosing the Right Commitment Level
- Analyze historical usage (at least 3 months)
- Commit to baseline (steady-state) usage only
- Leave headroom for variable workloads
- Cover 60-80% of steady usage with commitments
- Use on-demand and spot for the rest

---

## Break-Even Analysis: Details
- Calculate when savings exceed commitment cost
- All Upfront 1-year: break-even ~7-9 months
- No Upfront 1-year: savings from day one
- 3-year: larger savings but longer commitment
- Model different scenarios before buying

---

## Break-Even Analysis

![break_even_analysis](svg/courses/cloud/finops/04_reserved_instances/break_even_analysis.svg)

---

## Managing Commitments
- Track utilization of existing RIs/Savings Plans
- Unused commitments are wasted money
- AWS Cost Explorer RI/SP utilization reports
- Set alerts for low utilization
- Review monthly and adjust strategy

---

## RI Marketplace
- AWS allows reselling unused Standard RIs
- Recover value from commitments you no longer need
- Buy RIs at a discount from other sellers
- Not available for Convertible RIs
- Azure and GCP have exchange/cancel options

---

## Commitment Strategy Best Practices
- Start with Savings Plans for flexibility
- Layer commitments gradually (don't over-commit)
- Review and renew quarterly
- Match commitment term to business confidence
- Combine with rightsizing (rightsize first, then commit)
