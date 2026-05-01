---
tags:
  - architecture:serverless
  - practices:testing
level: intermediate
category: architecture
audience:
  - audiences:developers

---
# Testing Serverless Applications

---
## What This Chapter Covers

- Why testing serverless is different
- Unit testing Lambda functions
- Local emulation
- Integration testing
- LocalStack and SAM CLI
- End-to-end testing
- CI/CD for serverless

---
## Why Different

- Functions run in a managed environment
- Many AWS services involved
- Async event flows
- Cold starts and infra timing
- Hard to reproduce production locally

---
## Unit Testing

- Test the handler function directly
- Mock the AWS SDK calls
- Pure logic in unit tests
- Fast; runs in CI
- The bedrock

---
## Unit Test Example

```python
def test_handler_returns_200():
    event = {'pathParameters': {'id': '42'}}
    response = handler(event, {})
    assert response['statusCode'] == 200

@patch('boto3.client')
def test_handler_writes_to_dynamodb(mock_boto):
    handler({'body': '...'}, {})
    mock_boto.return_value.put_item.assert_called_once()
```

---
## Local Emulation

- AWS SAM CLI: invoke Lambda locally
- `sam local invoke MyFunction --event event.json`
- Useful for: rapid iteration
- Doesn't perfectly replicate cloud
- Good for development, not full validation

---
## LocalStack

- Mocks ~80 AWS services locally
- Lambda, DynamoDB, S3, SQS, Step Functions, ...
- Runs in Docker
- Free tier; pro tier for advanced features
- Standard for local serverless dev

---
## LocalStack Workflow

```bash
docker run -d -p 4566:4566 localstack/localstack
aws --endpoint-url=http://localhost:4566 s3 mb s3://my-bucket
# ... deploy your serverless app pointing at LocalStack
# ... run integration tests
```

- AWS CLI works against LocalStack with `--endpoint-url`
- Same code, local execution

---
## Integration Tests

- Deploy to a real AWS account (a test environment)
- Run tests against the deployed services
- Catches: IAM issues, real timing, real service quirks
- Slower than unit; runs less often
- The most realistic check before prod

---
## Test Stages

- Unit (every commit; mocked)
- Integration (every merge; LocalStack or test AWS)
- End-to-end (before deploy; full AWS)
- Production smoke (after deploy)
- Layered confidence

---
## Async Testing

- Trigger an event; wait for the side effect
- Polling pattern: check DynamoDB / S3 / queue
- Timeout in seconds; not in milliseconds
- Build a `wait_until` helper
- Same pattern as testing any async system

---
## Testing Step Functions

- AWS Step Functions Local for execution
- Mock service integrations
- Or: deploy and run; assert on execution history
- Test each branch (success, error, retry)

---
## Testing Auth

- Mock the authoriser in unit tests
- Real Cognito / JWT in integration tests
- Don't skip auth in test environment (different code paths)

---
## CI/CD

- AWS SAM, Serverless Framework, AWS CDK
- Define infrastructure as code
- CI builds, tests, deploys
- Per-PR ephemeral environments (advanced)
- Without IaC: drift, manual deploy nightmare

---
## Canary Deployments

- Deploy new version; route 10% of traffic
- Monitor; if healthy, ramp to 100%
- AWS Lambda + CodeDeploy
- Catches problems before full rollout
- Standard for production deployments

---
## Smoke Tests After Deploy

- Hit a few endpoints; check health
- Synthetic monitoring (CloudWatch Synthetics)
- Catches: deploy that "succeeded" but doesn't work
- Quick (minutes); valuable

---
## Common Testing Mistakes

- Only unit tests; no integration with real AWS
- Tests that don't exercise IAM / permissions
- Asserting on logs (brittle)
- No tests for async event processing
- Skipping tests "to ship faster" (worse outcome)

---
## A Practical Test Pyramid

- Many: unit tests (fast, cheap)
- Some: integration tests (against LocalStack or test AWS)
- Few: end-to-end tests (against full AWS)
- Always: smoke tests after deploy
- Match cost to risk
