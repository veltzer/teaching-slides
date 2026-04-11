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
# Budgets, Alerts, and Governance

---

## Why Budgets Matter
- Cloud costs can spike unexpectedly
- No budget = no accountability
- Budgets set expectations and guardrails
- Early warning system for overspending
- Foundation for cost governance

---

## Setting Up Cloud Budgets
- Define budgets per account, team, or project
- Monthly or quarterly budget periods
- Based on historical spend + growth forecast
- Include buffer for unexpected needs (10-20%)
- Review and adjust quarterly

---

## AWS Budgets
- Set custom cost, usage, and reservation budgets
- Up to 5 free budgets, then $0.02/day per budget
- Forecast alerts: predicted to exceed
- Actual alerts: already exceeded threshold
- Actions: notify, restrict IAM, stop instances

---

## Azure Cost Management Budgets
- Create budgets in Azure Cost Management
- Scope: subscription, resource group, or management group
- Alert at percentage thresholds (50%, 80%, 100%)
- Action groups for notifications
- Integrate with Azure Logic Apps for automation

---

## GCP Budget Alerts
- Set budgets in Cloud Billing
- Alert at custom percentage thresholds
- Notifications via email and Pub/Sub
- Programmatic responses via Cloud Functions
- Scope to billing account or project

---

## Alert Configuration Best Practices
- Set alerts at 50%, 80%, and 100% of budget
- Include forecast alerts (not just actual)
- Route to the right people (team leads, not just finance)
- Test alert delivery before relying on it
- Include context in alert messages

---

## Cost Anomaly Detection
- Automatically detect unusual spending patterns
- AWS Cost Anomaly Detection
- Azure Cost Management anomaly alerts
- GCP billing anomaly detection
- Catches issues faster than threshold-based alerts

---

## Cost Governance Policies
- Define what is and isn't allowed
- Maximum instance sizes per environment
- Required tags for resource creation
- Approved regions and services
- Enforce via cloud-native policy tools

---

## Policy Enforcement Tools
- AWS: Service Control Policies, AWS Config
- Azure: Azure Policy, Management Groups
- GCP: Organization Policies, Constraints
- Prevent non-compliant resources before creation
- Detect and remediate existing violations

---

## Approval Workflows
- Require approval for large resource requests
- Self-service within guardrails
- Escalation for exceptions
- ServiceNow, Jira, or custom workflows
- Balance speed with cost control

---

## Reporting and Dashboards
- Weekly or monthly cost reports
- Per-team cost breakdowns
- Trend lines and forecasts
- Top spenders and fastest-growing costs
- Make reports visible and actionable

---

## Executive Reporting
- High-level cost trends and KPIs
- Cost per unit (per customer, per transaction)
- Savings achieved through optimization
- Budget vs actual comparison
- Cloud ROI metrics
