---
tags:
  - infrastructure:cloud
  - concepts:serverless
  - concepts:architecture
level: intermediate
category: cloud
audience:
  - audiences:developers
  - audiences:architects
  - audiences:devops

---

# Cloud Functions

---

## What is Serverless?
- Run code without provisioning servers
- Provider manages all infrastructure
- Auto-scales from zero to massive
- Pay only for execution time
- Focus entirely on business logic

---

## Cloud Function Services
- AWS Lambda
- Azure Functions
- Google Cloud Functions
- All provide similar core capabilities
- Differences in triggers, limits, and ecosystem integration

---

## How Do You Pay?
- Per request: $0.20 per million requests (Lambda)
- Per compute time: $0.0000166667 per GB-second
- No charge when not executing
- Free tier: 1M requests/month (Lambda)
- Can be extremely cost-effective for intermittent workloads

---

## Why Better Than Renting Machines?
- No idle costs: zero traffic = zero cost
- No scaling configuration: automatic
- No OS patching or server maintenance
- Faster deployment (deploy a function, not a server)
- Reduced operational complexity

---

## When Serverless Is Not Ideal
- Long-running processes (15-minute limit on Lambda)
- GPU or specialized hardware needs
- Consistent high throughput (may be cheaper with reserved instances)
- Very low latency requirements (cold start penalty)
- Stateful workloads

---

## Cold Starts
- First invocation after idle period is slower
- Runtime needs to initialize (load code, dependencies)
- Java/C# have longer cold starts than Python/Node.js
- Provisioned Concurrency eliminates cold starts (at a cost)
- Keep functions small and lean to minimize

---

## Cold Start vs Warm Start

![cold_start](svg/courses/cloud/architecting-in-the-cloud/08_cloud_functions/cold_start_timeline.svg)

---

## Function Triggers
- HTTP/API Gateway: web APIs
- Queue messages (SQS, Service Bus)
- Object storage events (S3, Blob)
- Database changes (DynamoDB Streams)
- Scheduled events (cron-like)
- Event bus (EventBridge, Pub/Sub)

---

## Serverless Event Sources

![triggers](svg/courses/cloud/architecting-in-the-cloud/08_cloud_functions/serverless_event_flow.svg)

---

## Function Design Principles
- Single responsibility: one function, one job
- Small and focused: fast cold start
- Idempotent: safe to retry
- Stateless: no local state between invocations
- Fast: minimize execution time (cost and experience)

---

## Python Lambda Handler

```python
import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Orders')

def handler(event, context):
    order_id = event['pathParameters']['id']
    response = table.get_item(Key={'orderId': order_id})

    if 'Item' not in response:
        return {'statusCode': 404,
                'body': json.dumps({'error': 'Not found'})}

    return {'statusCode': 200,
            'body': json.dumps(response['Item'])}
```

---

## Function Configuration
- Memory allocation (128 MB to 10 GB on Lambda)
- CPU scales with memory
- Timeout setting (max 15 minutes on Lambda)
- Environment variables for configuration
- IAM role for permissions

---

## Connecting Functions to Other Services
- Functions call APIs and AWS services
- Use SDKs within function code
- IAM roles grant permissions (no hardcoded keys)
- VPC access for private resources (databases)
- Keep functions focused: offload heavy work to queues

---

## Chains of Functions
- One function triggers another
- Event-driven pipeline
- S3 upload -> resize image -> store thumbnail -> update database
- Loose coupling through events
- Each function scales independently

---

## Step Functions and Orchestration
- AWS Step Functions, Azure Durable Functions, GCP Workflows
- Orchestrate multiple functions into workflows
- Visual workflow designer
- Error handling, retries, parallel execution
- Better than function-to-function chaining for complex flows

---

## Step Functions Workflow

![workflow](svg/courses/cloud/architecting-in-the-cloud/08_cloud_functions/step_functions_workflow.svg)

---

## Patterns: API Backend
- API Gateway + Lambda
- Each route maps to a function
- Auto-scaling, pay-per-request
- No servers to manage
- Standard pattern for REST APIs

---

## Patterns: Event Processing
- Queue or stream triggers a function
- Process each message/event
- Scale to handle burst traffic
- Dead letter queue for failures
- Fan-out for parallel processing

---

## Patterns: Scheduled Tasks
- Cron-like triggers (CloudWatch Events, EventBridge)
- Database cleanup, report generation
- No always-running instance needed
- Pay only for execution time
- Replace cron servers entirely

---

## Scheduled Lambda with SAM

```yaml
AWSTemplateFormatVersion: "2010-09-09"
Transform: AWS::Serverless-2016-10-31

Resources:
  CleanupFunction:
    Type: AWS::Serverless::Function
    Properties:
      Runtime: python3.12
      Handler: cleanup.handler
      Timeout: 300
      Events:
        NightlyCleanup:
          Type: Schedule
          Properties:
            Schedule: cron(0 2 * * ? *)
            Description: "Run cleanup at 2 AM UTC"
```

---

## Patterns: Data Transformation
- S3/Blob upload triggers function
- Transform, validate, or enrich data
- Store result in another location
- ETL pipelines at low cost
- Scale to millions of objects

---

## Patterns: Webhooks and Integrations
- Receive events from external services
- API Gateway + Lambda as webhook receiver
- Process GitHub events, Stripe payments, Slack commands
- No always-running server needed
- Pay only when events arrive

---

## Patterns: Real-Time File Processing
- Upload -> trigger -> process -> store result
- Image resizing, video transcoding
- Document parsing and indexing
- Virus scanning uploaded files
- Parallel processing for high volume

---

## Lambda Layers
- Shared code and dependencies across functions
- Package common libraries once
- Reduce function deployment size
- AWS-managed layers (pandas, numpy)
- Version and manage independently

---

## SAM Local Testing

```bash
# Initialize a new SAM project
sam init --runtime python3.12

# Build the application
sam build

# Test locally with a sample event
sam local invoke MyFunction \
  --event events/test.json

# Start local API Gateway
sam local start-api --port 3000

# Deploy to AWS
sam deploy --guided
```

---

## Lambda@Edge and CloudFront Functions
- Run code at CDN edge locations
- Modify requests and responses
- A/B testing, URL rewriting, auth
- Lower latency than origin functions
- Limited resources and execution time

---

## Serverless Application Model (SAM)
- AWS-specific serverless IaC
- Simplified CloudFormation syntax
- Local testing and debugging (sam local)
- CI/CD integration
- Template repository for common patterns

---

## Cost Optimization for Serverless
- Right-size memory allocation (affects CPU)
- Minimize cold starts (keep warm or provisioned concurrency)
- Reduce execution time (optimize code)
- Use ARM architecture (Graviton) for 20% savings
- Monitor cost per function invocation

---

## Serverless Frameworks
- Serverless Framework: multi-cloud
- AWS SAM: AWS-native
- AWS CDK: programmatic (TypeScript, Python)
- Terraform: infrastructure-level
- Framework handles packaging, deployment, permissions

---

## Monitoring Serverless
- CloudWatch Logs: function output
- CloudWatch Metrics: invocations, errors, duration
- X-Ray: distributed tracing
- Alerts on error rate and duration
- Monitor cold starts and throttling

---

## Concurrency and Throttling
- Concurrent executions: functions running simultaneously
- Default limit: 1,000 concurrent (AWS, can increase)
- Reserved concurrency: guarantee capacity for critical functions
- Provisioned concurrency: pre-warm instances
- Monitor for throttling errors

---

## Function Composition
- Don't chain functions directly (coupling + error handling)
- Use Step Functions/Durable Functions for workflows
- Use queues for async fan-out
- EventBridge for event-driven composition
- Keep each function independent

---

## Testing Serverless Applications
- Unit test function logic locally
- SAM Local / Azure Functions Core Tools for local testing
- Integration tests against deployed stack
- End-to-end tests for event flows
- Mock external services for unit tests

---

## Serverless Databases
- DynamoDB: serverless NoSQL
- Aurora Serverless: serverless relational
- Firestore: serverless document database
- No connection pooling issues
- Scale with function invocations

---

## Serverless Security
- IAM roles per function (least privilege)
- No OS to patch
- Input validation in function code
- Secrets in Secrets Manager (not env vars for sensitive data)
- VPC for accessing private resources

---

## Serverless Best Practices
- Keep functions small and focused
- Minimize dependencies (faster cold start)
- Use provisioned concurrency for latency-sensitive paths
- Set appropriate timeouts
- Always use dead letter queues
- Monitor cost per function
