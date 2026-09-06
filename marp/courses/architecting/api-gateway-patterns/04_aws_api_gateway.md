---
tags:
  - architecture:api-gateway
  - infrastructure:aws
level: intermediate
category: architecture
audience:
  - audiences:developers

---

# AWS API Gateway

---

## What This Chapter Covers

- AWS API Gateway: REST vs HTTP vs WebSocket
- Integration types
- Custom domains and certificates
- Authorisers
- Stages and deployments
- Pricing
- When to use it

---

## Three Flavours

- **REST API**: classic; full features; expensive
- **HTTP API**: leaner; cheaper; faster (~70% of features)
- **WebSocket API**: persistent connections; for real-time
- Choose: HTTP API by default for new work; REST when you need a feature

---

## At a Glance

![aws_gateway_kinds](svg/courses/architecting/api-gateway-patterns/04_aws_api_gateway/aws_gateway_kinds.svg)

---

## Integration Types

- **Lambda Proxy**: gateway forwards request to Lambda; passes return
- **AWS Service**: direct integration with DynamoDB, S3, etc.
- **HTTP**: proxy to any HTTP backend (EC2, on-prem, ALB)
- **VPC Link**: to private resources via internal LB
- **Mock**: returns canned data; useful for testing

---

## Integration Targets

![integration_kinds](svg/courses/architecting/api-gateway-patterns/04_aws_api_gateway/integration_kinds.svg)

---

## Lambda Proxy

```yaml
paths:
  /users/{id}:
    get:
      x-amazon-apigateway-integration:
        type: aws_proxy
        httpMethod: POST
        uri: arn:aws:apigateway:.../functions/.../invocations
```

- Single Lambda per endpoint, or one Lambda for all
- Standard pattern for serverless
- Pair with Cognito or custom authoriser

---

## Custom Domains

- Map `api.example.com` to your gateway
- Requires ACM certificate
- Multiple stages on subdomains: `api-staging.example.com`
- Works with Route 53 or external DNS
- Setup once; rarely changes

---

## Authorisers

- **IAM**: AWS-signed requests
- **Cognito**: user pools
- **Lambda Authoriser**: custom logic in Lambda
- **JWT Authoriser**: HTTP API; verify a JWT
- Run before the integration; reject early on auth failure

---

## Lambda Authoriser

- Called for every request
- Returns IAM policy: allow or deny
- Cached for a configurable TTL
- Cost: extra Lambda invocation per request (or per cache miss)
- Use when standard authorisers don't fit

---

## Stages and Deployments

- "Deployment": a snapshot of the API config
- "Stage": a named environment (`prod`, `staging`)
- Each stage deploys a deployment
- Promote between stages
- Stage variables for per-environment config

---

## Throttling and Quotas

- Per-method throttling: rate + burst
- Per-API key quotas: requests per day / month
- Built-in; no plugin needed
- AWS WAF for more complex rules

---

## Pricing

- REST API: ~$3.50 per million requests + $0.09/GB out
- HTTP API: ~$1.00 per million (much cheaper)
- WebSocket: ~$1.00 per million messages + connection-minute
- Hosted everything; no servers to manage
- Adds up at scale; budget accordingly

---

## When To Use AWS API Gateway

- All-in on AWS
- Serverless backend (Lambda)
- Want managed-only (no ops)
- Don't need plugin extensibility
- Acceptable lock-in

---

## When NOT To Use

- Multi-cloud
- Need plugins / custom Lua
- High request volume (cost adds up)
- Want everything in one repo (gateway config tied to AWS)

---

## OpenAPI Import

- Import an OpenAPI 3 spec
- Gateway generates routes
- Pair with vendor extensions (`x-amazon-apigateway-*`)
- One source of truth for API + gateway config

---

## CDK / CloudFormation

- Infrastructure as code
- API Gateway resources defined in code
- `RestApi` (or `HttpApi`) constructs in CDK
- Deployed alongside Lambdas, DynamoDB, etc.
- Standard for AWS-native projects

---

## Common AWS API Gateway Mistakes

- Choosing REST API when HTTP API would suffice (3x cost)
- No throttling; runaway clients run up the bill
- Authorisers without caching (1 Lambda per request)
- One Lambda per endpoint with cold starts everywhere
- Forgetting CORS configuration; mysterious browser errors
