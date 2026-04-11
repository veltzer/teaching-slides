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
# Course Wrap-Up

---

## The Well-Architected Framework
- Six pillars for building in the cloud
- AWS Well-Architected Tool for self-review
- Best practices for each pillar
- Trade-offs between pillars
- Apply from day one of every project

---

## The Six Pillars

![well_architected_six_pillars](svg/courses/cloud/introduction-to-aws/08_wrap_up/well_architected_six_pillars.svg)

---

## Pillar: Operational Excellence
- Run and monitor systems effectively
- Automate changes and responses
- Learn from operational events
- Make frequent, small, reversible changes
- Anticipate failure and practice recovery

---

## Pillar: Security
- Protect information and systems
- Strong identity foundation (IAM)
- Enable traceability (CloudTrail)
- Apply security at all layers
- Automate security best practices

---

## Pillar: Reliability
- Recover from failures automatically
- Test recovery procedures
- Scale horizontally for availability
- Stop guessing capacity
- Manage change through automation

---

## Pillar: Performance Efficiency
- Use computing resources efficiently
- Select the right resource types and sizes
- Monitor performance metrics
- Make informed decisions with data
- Use managed services to remove burden

---

## Pillar: Cost Optimization
- Avoid unnecessary costs
- Understand and control spending
- Select the right pricing model
- Match supply with demand
- Optimize over time

---

## Pillar: Sustainability
- Minimize environmental impact
- Understand your impact
- Maximize utilization
- Adopt efficient hardware and software
- Reduce downstream impact

---

## Understanding AWS Pricing
- Pay-as-you-go: no upfront costs
- Save when you commit (Reserved, Savings Plans)
- Pay less by using more (volume discounts)
- Free Tier for getting started
- Pricing varies by Region

---

## Pricing by Service Type
- Compute: per second or per hour
- Storage: per GB per month
- Data transfer: per GB out (inbound is free)
- Requests: per API call (S3, Lambda)
- Always check the pricing page for each service

---

## AWS Pricing Calculator
- Estimate costs before deploying
- Build detailed cost models
- Compare configurations
- Export and share estimates
- Available at calculator.aws

---

## AWS Cost Explorer
- Visualize spending over time
- Filter by service, Region, tag
- Forecast future costs
- Identify cost trends
- Rightsizing recommendations

---

## AWS Budgets
- Set custom cost and usage budgets
- Alert when thresholds are exceeded
- Track Reserved Instance utilization
- Automated actions on budget breach
- Set up immediately after account creation

---

## Create a Budget with CLI

```bash
aws budgets create-budget \
  --account-id 123456789012 \
  --budget '{
    "BudgetName": "MonthlyTotal",
    "BudgetLimit": {
      "Amount": "500",
      "Unit": "USD"
    },
    "TimeUnit": "MONTHLY",
    "BudgetType": "COST"
  }' \
  --notifications-with-subscribers '[{
    "Notification": {
      "NotificationType": "ACTUAL",
      "ComparisonOperator": "GREATER_THAN",
      "Threshold": 80
    },
    "Subscribers": [{
      "SubscriptionType": "EMAIL",
      "Address": "team@example.com"
    }]
  }]'
```

---

## Cost Allocation Tags
- Tag resources by project, team, environment
- Appear in billing reports
- AWS-generated tags (e.g., aws:createdBy)
- User-defined tags (e.g., Project, Owner)
- Essential for cost attribution

---

## Avoiding Bill Surprises
- Set up billing alerts immediately
- Use AWS Budgets for thresholds
- Monitor Free Tier usage dashboard
- Clean up unused resources (EIPs, EBS volumes)
- Review Cost Explorer monthly

---

## AWS Support Plans
- Basic: free, documentation and forums
- Developer: email support, 12-hour response
- Business: 24/7 phone, 1-hour response for production down
- Enterprise On-Ramp: TAM pool, 30-minute critical response
- Enterprise: dedicated TAM, 15-minute critical response

---

## Path to AWS Certification
1. AWS Certified Cloud Practitioner (foundational)
1. AWS Certified Solutions Architect - Associate
1. AWS Certified Developer - Associate
1. AWS Certified SysOps Administrator - Associate
1. Specialty and Professional certifications

---

## AWS Certification Paths

![certification_paths](svg/courses/cloud/introduction-to-aws/08_wrap_up/certification_paths.svg)

---

## Cloud Practitioner Exam
- Entry-level certification
- Cloud concepts, security, technology, billing
- 65 questions, 90 minutes
- 700/1000 passing score
- Validates foundational AWS knowledge

---

## Additional AWS Services to Explore
- AWS Lambda: serverless compute
- Amazon SQS/SNS: messaging
- AWS Step Functions: workflow orchestration
- Amazon Kinesis: real-time data streaming
- AWS CodePipeline: CI/CD

---

## Learning Resources
- AWS Skill Builder (free and paid courses)
- AWS documentation and whitepapers
- AWS re:Invent and re:Post
- Hands-on labs with Free Tier
- AWS Architecture Center

---

## Hands-On Next Steps
- Create an AWS Free Tier account
- Launch an EC2 instance
- Create an S3 bucket and upload objects
- Set up a VPC with public and private subnets
- Deploy a simple web application

---

## Key Takeaways
- AWS is the leading cloud platform with 200+ services
- Core services: EC2, S3, VPC, IAM, RDS, DynamoDB
- Security is a shared responsibility
- Monitor everything with CloudWatch and CloudTrail
- The Well-Architected Framework guides good design
- Start small, learn hands-on, iterate

---

## Additional AWS Services Worth Knowing
- Amazon SNS: pub/sub notifications
- Amazon SQS: message queuing
- AWS Elastic Beanstalk: easy app deployment
- Amazon ECS/EKS: container orchestration
- AWS CloudFormation: infrastructure as code

---

## Thank You
- Questions and discussion
- Feedback welcome
- Continue learning with hands-on practice
- AWS Free Tier is your sandbox
- Good luck on your AWS journey
