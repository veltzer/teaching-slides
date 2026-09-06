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

# Cost Optimization Tools

---

## Cloud-Native Tools Overview
- Every major provider offers built-in cost tools
- Free or low-cost to use
- Good starting point before third-party tools
- Integrated with provider billing data
- Sufficient for many organizations

---

## Cost Tools Landscape

![cost_tools_landscape](svg/courses/cloud/finops/07_cost_optimization_tools/cost_tools_landscape.svg)

---

## AWS Cost Explorer
- Visualize spending over time
- Filter by service, Region, tag, account
- Group by dimensions (service, instance type)
- Forecasting based on historical trends
- Rightsizing recommendations for EC2

---

## AWS Cost and Usage Reports (CUR)
- Most detailed billing data available
- Hourly or daily line items for every resource
- Export to S3 for custom analysis
- Query with Athena or load into data warehouse
- Foundation for advanced FinOps analytics

---

## Query CUR Data with Athena

```sql
-- Top 10 most expensive services last month
SELECT line_item_product_code AS service,
       SUM(line_item_blended_cost) AS cost
FROM cost_and_usage_report
WHERE month = '1'
  AND year = '2024'
GROUP BY line_item_product_code
ORDER BY cost DESC
LIMIT 10;
```

---

## AWS Compute Optimizer
- ML-based rightsizing recommendations
- Analyzes CloudWatch metrics (CPU, memory, network)
- Covers EC2, Auto Scaling, EBS, Lambda
- Shows estimated savings per recommendation
- Free to use

---

## Azure Cost Management
- Cost analysis and visualization
- Budget creation and alerts
- Advisor recommendations
- Export data for custom reporting
- Power BI integration for dashboards

---

## Azure Advisor
- Personalized best practice recommendations
- Cost: idle resources, rightsizing, reservations
- Performance, security, reliability checks
- Actionable with direct links to fix
- Free service

---

## GCP Billing and Recommender
- Cloud Billing reports and export
- BigQuery export for detailed analysis
- Recommender: rightsizing, commitment suggestions
- Active Assist: actionable recommendations
- Integrated with GCP console

---

## Third-Party FinOps Platforms
- CloudHealth (VMware): multi-cloud cost management
- Spot.io (NetApp): optimization and automation
- Kubecost: Kubernetes cost allocation
- Apptio Cloudability: enterprise FinOps
- Vantage, Infracost, Env0

---

## When to Use Third-Party Tools
- Multi-cloud environments
- Need for advanced allocation and showback
- Kubernetes cost visibility
- Automated optimization actions
- When native tools aren't sufficient

---

## Infrastructure as Code for Cost Control
- Define resource sizes in code (prevent over-provisioning)
- Review cost impact in pull requests
- Infracost: estimate cost changes in CI/CD
- Prevent expensive resources from being deployed
- Policy as Code for cost guardrails

---

## Automated Scheduling
- Stop dev/test environments outside business hours
- AWS Instance Scheduler, Azure Automation
- Save 65%+ on non-production compute
- Tag-based: AutoShutdown=true
- Exclude production and critical workloads

---

## Waste Detection and Cleanup
- Automated scans for idle resources
- AWS Trusted Advisor checks
- Custom Lambda/Functions for cleanup
- Scheduled jobs to delete old snapshots
- Regular review cadence (weekly or monthly)

---

## Building a Cost Optimization Dashboard
- Combine native and third-party data
- Key metrics: spend trend, savings rate, coverage
- Per-team and per-service breakdowns
- Anomaly indicators
- Actionable: link to recommendations

---

## Cost Dashboard Layout

![cost_dashboard_layout](svg/courses/cloud/finops/07_cost_optimization_tools/cost_dashboard_layout.svg)
