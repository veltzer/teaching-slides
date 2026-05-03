---
tags:
  - architecture:serverless
  - architecture:security
level: intermediate
category: architecture
audience:
  - audiences:developers

---
# Security and Operational Concerns

---
## What This Chapter Covers

- IAM and least privilege
- Secret management
- VPC / network controls
- Logging, metrics, tracing
- Vulnerability management
- Compliance considerations

---
## IAM At Function Granularity

- Each Lambda gets its own IAM role
- Principle of least privilege: only what's needed
- Don't use "*" in resource ARNs
- Audit periodically; permissions drift
- A common security failing in serverless

---
## Security Concerns

![serverless_security](svg/courses/architecting/serverless-architecture/09_security_and_operational_concerns/serverless_security.svg)

---
## Sample IAM Policy

```json
{
  "Effect": "Allow",
  "Action": ["dynamodb:GetItem", "dynamodb:PutItem"],
  "Resource": "arn:aws:dynamodb:us-east-1:123:table/orders"
}
```

- Specific actions; specific resource
- No wildcards in actions
- Resource-level permissions where supported
- Catch issues in IAM Access Analyzer

---
## Secret Management

- Never in code; never in environment variables (in plaintext)
- AWS Secrets Manager / Parameter Store (encrypted)
- Reference secrets in Lambda config
- Rotate periodically (Secrets Manager handles)
- Cache in init code; expire after N minutes

---
## Defence in Depth

![security_layers](svg/courses/architecting/serverless-architecture/09_security_and_operational_concerns/security_layers.svg)

---
## VPC Lambda

- Lambda runs in AWS-managed VPC by default
- Connect to your VPC for: RDS, ElastiCache, internal services
- Cold starts longer in VPC (was; mostly fixed now)
- ENI provisioning per concurrent execution
- Use only when needed

---
## Network Egress

- Lambda can call out to internet
- Filter via NAT Gateway or VPC endpoints
- VPC endpoints: cheaper, more secure
- Without VPC: no egress filtering
- Compliance often requires egress control

---
## Function URL Auth

- AWS Lambda Function URLs: simple HTTPS endpoints
- Auth: NONE or AWS_IAM
- Don't use NONE in production; combine with API Gateway / Cognito
- Convenient but risky if misconfigured

---
## Logging

- CloudWatch Logs: every Lambda log
- Structured (JSON) for queryability
- Don't log secrets, PII, full request bodies
- Set retention (don't keep forever)
- Forward to centralised logging (Datadog, Splunk) for production

---
## Metrics

- CloudWatch: invocations, duration, errors, throttles, concurrency
- Per-function dashboards
- Alarms on error rate, p99 latency
- Custom metrics from your code

---
## Distributed Tracing

- AWS X-Ray: distributed traces in AWS
- OpenTelemetry: vendor-neutral
- Spans across Lambda, DynamoDB, RDS, downstream services
- Find slow paths, error chains
- Critical for serverless debugging

---
## Vulnerability Management

- Lambda runtime: AWS patches the OS / language runtime
- Your dependencies: your responsibility
- Scan: Snyk, AWS Inspector
- Update libraries regularly
- A "scan in CI" + "scan deployed Lambdas" combo

---
## Code Signing

- Lambda: AWS Signer signs your code
- Verifies: deployment was authorised
- Configure: code signing config required for function
- Compliance use case primarily

---
## DDoS / Abuse

- API Gateway: throttle, AWS WAF
- Lambda concurrency limits (per function, per account)
- Without limits: a runaway client can drain your wallet
- Always set max concurrency on production Lambdas

---
## Compliance

- HIPAA, PCI, SOC2: AWS Lambda is in scope (if configured right)
- Encryption at rest (default for Lambda code)
- Encryption in transit (TLS)
- Audit log: CloudTrail
- BAA with AWS for HIPAA workloads

---
## Operational Practices

- Infra as code (SAM, CDK, Terraform)
- Per-environment accounts (dev, staging, prod)
- Deploy via CI; no manual changes
- Tagging for cost / compliance
- Runbooks for common issues

---
## Disaster Recovery

- Multi-region: deploy Lambda + DynamoDB in 2 regions
- Active-passive: failover via Route 53
- Active-active: harder; needs cross-region data sync
- DynamoDB Global Tables: makes active-active easier

---
## Common Operational Mistakes

- "Action: *" in IAM policies
- Secrets in environment variables (encrypted by default but visible in console)
- No concurrency limits (runaway costs)
- No tracing (hard to debug failures)
- Ignoring DLQs

---
## Course Wrap-Up

- Serverless: don't manage servers; pay for use
- FaaS for event-driven; BaaS for hosted backends
- Cold starts and state are the main constraints
- Cost can be cheaper or more expensive — measure
- Security: IAM granularity, secrets management
- Right tool for: bursty workloads, event processing, async pipelines
