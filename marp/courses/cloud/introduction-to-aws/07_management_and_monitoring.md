---
tags:
  - infrastructure:cloud
  - infrastructure:aws
  - practices:monitoring
level: beginner
category: cloud
audience:
  - audiences:developers
  - audiences:sysadmins
  - audiences:managers

---
# Management and Monitoring

---

## Why Monitoring Matters
- Detect issues before users do
- Understand resource utilization
- Optimize costs
- Meet compliance requirements
- Data-driven scaling decisions

---

## AWS Management Tools Overview
- Amazon CloudWatch: metrics and monitoring
- AWS CloudTrail: API activity logging
- AWS Config: resource configuration tracking
- AWS Trusted Advisor: best practice checks
- AWS Systems Manager: operational management

---

## Monitoring Tools Overview

![monitoring_tools_overview](svg/courses/cloud/introduction-to-aws/07_management_and_monitoring/monitoring_tools_overview.svg)

---

## Amazon CloudWatch Overview
- Monitoring and observability service
- Collects metrics from all AWS services
- Custom metrics from your applications
- Dashboards for visualization
- Central hub for operational health

---

## CloudWatch Metrics
- Pre-built metrics for all AWS services
- EC2: CPU, network, disk, status checks
- RDS: connections, IOPS, free storage
- S3: bucket size, object count, request metrics
- 1-minute or 5-minute granularity

---

## CloudWatch Custom Metrics
- Publish your own application metrics
- Memory utilization (not collected by default)
- Application-level counters
- Business metrics (orders per minute)
- Use PutMetricData API or CloudWatch Agent

---

## CloudWatch Alarms
- Monitor a single metric over time
- Trigger actions based on thresholds
- States: OK, ALARM, INSUFFICIENT_DATA
- Actions: SNS notification, Auto Scaling, EC2 action
- Composite alarms for complex conditions

---

## CloudWatch Alarm Example
- Metric: EC2 CPUUtilization
- Threshold: > 80% for 5 minutes
- Action: send SNS notification to ops team
- Action: trigger Auto Scaling to add instances
- Prevents performance degradation

---

## CloudWatch Alarm Flow

![cloudwatch_alarm_flow](svg/courses/cloud/introduction-to-aws/07_management_and_monitoring/cloudwatch_alarm_flow.svg)

---

## CloudWatch Logs
- Collect and store log files
- Log Groups: collection of related streams
- Log Streams: individual sources
- Retention policies (1 day to indefinite)
- Real-time monitoring and search

---

## CloudWatch Logs Insights
- Interactive query language for log analysis
- Search across log groups
- Aggregate and visualize log data
- Pre-built sample queries
- Faster than manual log search

---

## CloudWatch Custom Metric Example

```bash
# Publish a custom metric
aws cloudwatch put-metric-data \
  --namespace "MyApp" \
  --metric-name "ActiveUsers" \
  --value 142 \
  --unit Count

# Create an alarm
aws cloudwatch put-metric-alarm \
  --alarm-name "HighCPU" \
  --metric-name CPUUtilization \
  --namespace AWS/EC2 \
  --threshold 80 \
  --comparison-operator GreaterThanThreshold \
  --period 300 --evaluation-periods 2 \
  --statistic Average \
  --alarm-actions arn:aws:sns:us-east-1:123:ops
```

---

## CloudWatch Dashboards
- Customizable visualizations
- Cross-service and cross-account views
- Automatic refresh intervals
- Shareable with team members
- Widgets: line graphs, numbers, text, alarms

---

## CloudWatch Agent
- Install on EC2 instances
- Collect OS-level metrics (memory, disk space)
- Collect application log files
- Send to CloudWatch Metrics and Logs
- Works on Linux and Windows

---

## AWS CloudTrail Overview
- Records all API calls in your account
- Who did what, when, and from where
- Enabled by default (90-day event history)
- Create trails for long-term storage in S3
- Essential for security auditing

---

## CloudTrail Event Types
- Management Events: control plane operations (create, delete, configure)
- Data Events: data plane operations (S3 object access, Lambda invocations)
- Insights Events: detect unusual API activity
- Management Events logged by default
- Data Events must be explicitly enabled

---

## CloudTrail Event Record
- Event time and source
- User identity (who made the call)
- Source IP address
- API action and parameters
- Response and error codes

---

## CloudTrail Use Cases
- Security investigation and incident response
- Compliance auditing (who changed what)
- Operational troubleshooting
- Change tracking and forensics
- Detect unauthorized access patterns

---

## AWS Config
- Records resource configuration changes over time
- Configuration history for every resource
- Compliance rules (managed and custom)
- Automatic remediation actions
- Answers: "What changed and when?"

---

## Config Rules
- Evaluate resource configurations
- AWS Managed Rules (pre-built)
- Custom Rules (Lambda functions)
- Example: "All EBS volumes must be encrypted"
- Example: "S3 buckets must not be public"

---

## Config vs CloudTrail
- CloudTrail: who did what (API calls)
- Config: what is the current state and how did it change
- CloudTrail: event-focused
- Config: resource-focused
- Use both together for full visibility

---

## AWS Trusted Advisor
- Best practice recommendations
- Five categories of checks
- Some checks free, full set with Business/Enterprise support
- Real-time guidance
- Actionable recommendations

---

## Trusted Advisor Categories
1. Cost Optimization: idle resources, underutilized instances
1. Performance: overutilized resources, service limits
1. Security: open ports, MFA, public access
1. Fault Tolerance: backups, multi-AZ, redundancy
1. Service Limits: approaching AWS limits

---

## AWS Systems Manager
- Operational management for AWS resources
- Patch management across fleets
- Parameter Store: configuration and secrets
- Run Command: remote execution without SSH
- Session Manager: secure browser-based shell

---

## Systems Manager Parameter Store
- Centralized configuration storage
- Hierarchical key-value pairs
- Plaintext or encrypted (KMS)
- Version tracking
- Free for standard parameters

---

## AWS Health Dashboard
- Service Health: status of all AWS services by Region
- Personal Health: events affecting your resources
- Proactive notifications
- Event log and history
- Integrate with EventBridge for automation

---

## Monitoring Best Practices
- Set alarms for critical metrics from day one
- Use dashboards for operational visibility
- Enable CloudTrail in all Regions
- Retain logs for compliance requirements
- Automate responses to common events
