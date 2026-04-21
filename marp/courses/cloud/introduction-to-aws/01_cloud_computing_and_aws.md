---
tags:
  - infrastructure:cloud
  - infrastructure:aws
level: beginner
category: cloud
audience:
  - audiences:developers
  - audiences:sysadmins
  - audiences:managers

---
# Introduction to Cloud Computing and AWS

---

## What is Cloud Computing?
- On-demand delivery of IT resources
- Pay-as-you-go pricing
- No upfront capital investment
- Scalable and elastic
- Accessible over the internet

---

## NIST Definition
- On-demand self-service
- Broad network access
- Resource pooling
- Rapid elasticity
- Measured service

---

## Before the Cloud
- Buy and rack physical servers
- Weeks or months to provision
- Capacity planning guesswork
- Upfront capital expenditure
- Underutilized or overloaded hardware

---

## The Cloud Shift
- Provision in minutes, not months
- Convert CapEx to OpEx
- Scale to actual demand
- Global deployment from your desk
- Focus on applications, not infrastructure

---

## Cloud Shift Comparison

![cloud_shift_comparison](svg/courses/cloud/introduction-to-aws/01_cloud_computing_and_aws/cloud_shift_comparison.svg)

---

## Benefits of the AWS Cloud
- Agility and speed
- Elasticity and scalability
- Cost savings (pay only for what you use)
- Global reach in minutes
- Broad set of managed services

---

## Trade Variable for Fixed Expense
- No more guessing capacity
- Pay only for resources consumed
- Scale up and down as needed
- No idle hardware costs
- Financial flexibility

---

## Economies of Scale
- AWS aggregates usage from hundreds of thousands of customers
- Lower pay-as-you-go prices
- Savings passed to customers
- Hardware costs amortized broadly

---

## Stop Guessing Capacity
- Over-provision: waste money
- Under-provision: performance problems
- Cloud: scale in minutes
- Auto Scaling handles demand spikes
- Right-size resources based on real data

---

## Speed and Agility
- New resources a click away
- Experiment at low cost
- Fail fast, iterate quickly
- Reduce time from idea to production
- Developer self-service

---

## Go Global in Minutes
- Deploy to multiple Regions
- Reduce latency for users worldwide
- No physical data center buildout
- Edge locations for content delivery
- Compliance with local data laws

---

## Why AWS?
- Largest cloud provider by market share
- Most mature platform (launched 2006)
- Widest range of services (200+)
- Largest global infrastructure
- Extensive partner ecosystem

---

## AWS History
- 2002: Amazon.com infrastructure ideas
- 2004: SQS launched (first service)
- 2006: S3 and EC2 launched publicly
- 2010s: explosive growth in services
- Today: 200+ services, millions of customers

---

## AWS Market Position
- ~31% of global cloud market
- Used by startups and Fortune 500
- Netflix, Airbnb, NASA, Samsung
- Strong in all verticals
- Continuous innovation pace

---

## AWS Global Infrastructure: Details
- Regions: geographic areas with data centers
- Availability Zones: isolated data centers within a region
- Edge Locations: content delivery endpoints
- Local Zones: low-latency extensions of regions

---

## AWS Global Infrastructure

![aws_global_infrastructure](svg/courses/cloud/introduction-to-aws/01_cloud_computing_and_aws/aws_global_infrastructure.svg)

---

## AWS Regions
- 30+ Regions worldwide (and growing)
- Each Region is fully independent
- Services and pricing vary by Region
- Choose Region based on compliance, latency, cost
- Region codes like us-east-1, eu-west-1

---

## Availability Zones
- Each Region has 2+ Availability Zones
- Physically separated data centers
- Independent power, cooling, networking
- Connected via low-latency fiber
- Design for multi-AZ for high availability

---

## Edge Locations
- 400+ Points of Presence globally
- Used by CloudFront (CDN)
- Cache content close to users
- Also used by Route 53 (DNS)
- Far more Edge Locations than Regions

---

## Local Zones and Wavelength
- Local Zones: AWS in metro areas (low latency)
- Wavelength: AWS in telecom 5G networks
- Outposts: AWS hardware on your premises
- Extend AWS to where your users are

---

## The AWS Management Console
- Web-based interface for all AWS services
- Service search and navigation
- Resource management dashboards
- Billing and cost overview
- Region selector in top-right corner

---

## Console Navigation Tips
- Pin frequently used services to favorites
- Use the search bar for quick access
- Check the Region selector before creating resources
- Resource Groups to organize by project
- CloudShell for CLI access from the browser

---

## AWS CLI
- Command-line tool for AWS services
- Available on Windows, macOS, Linux
- Scriptable and automatable
- Same API actions as the console
- `aws <service> <command> --options`

---

## AWS CLI Examples

```bash
# List all S3 buckets
aws s3 ls

# Describe running EC2 instances
aws ec2 describe-instances \
  --filters "Name=instance-state-name,Values=running" \
  --query "Reservations[].Instances[].InstanceId"

# Get current caller identity
aws sts get-caller-identity
```

---

## AWS SDKs
- Libraries for many programming languages
- Python (boto3), Java, JavaScript, Go, .NET, etc.
- Integrate AWS into your applications
- Handle authentication, retries, pagination
- Same underlying API as CLI and console

---

## Infrastructure as Code
- AWS CloudFormation: declarative YAML/JSON templates
- AWS CDK: define infrastructure in code (TypeScript, Python, etc.)
- Terraform: popular third-party IaC tool
- Repeatable, version-controlled deployments
- Eliminate manual console clicks

---

## CloudFormation Example

```yaml
AWSTemplateFormatVersion: "2010-09-09"
Resources:
  MyBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: my-app-data-bucket
      VersioningConfiguration:
        Status: Enabled
      BucketEncryption:
        ServerSideEncryptionConfiguration:
          - ServerSideEncryptionByDefault:
              SSEAlgorithm: AES256
```

---

## AWS Free Tier
- 12 months of free usage for many services
- Always-free tier for some services (Lambda, DynamoDB)
- Trial offers for new services
- Great for learning and experimentation
- Monitor usage to avoid unexpected charges

---

## Shared Responsibility Model: Details
- AWS manages security **of** the cloud
- Customer manages security **in** the cloud
- Shared controls (patch management, configuration)
- Varies by service type (IaaS vs PaaS vs SaaS)
- Understanding this model is fundamental

---

## Shared Responsibility Model

![shared_responsibility_model](svg/courses/cloud/introduction-to-aws/01_cloud_computing_and_aws/shared_responsibility_model.svg)
