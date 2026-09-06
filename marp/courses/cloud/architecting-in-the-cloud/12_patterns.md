---
tags:
  - infrastructure:cloud
  - concepts:architecture
  - concepts:design-patterns
level: intermediate
category: cloud
audience:
  - audiences:developers
  - audiences:architects
  - audiences:devops

---

# Patterns

---

## Cloud Architecture Patterns
- Recurring solutions to common cloud problems
- Battle-tested by thousands of organizations
- Not prescriptions: adapt to your context
- Understanding patterns helps you make better decisions
- Knowing anti-patterns is equally important

---

## Pattern: Direct Download from Storage
- Client uploads/downloads directly to S3/Blob Storage
- Use pre-signed URLs (time-limited, authenticated)
- Application generates URL, client interacts with storage
- Offloads bandwidth from application servers
- Massive scale for file serving

---

## Generate a Pre-Signed URL

```python
import boto3

s3 = boto3.client('s3')

url = s3.generate_presigned_url(
    'get_object',
    Params={
        'Bucket': 'my-assets',
        'Key': 'reports/q4-2024.pdf'
    },
    ExpiresIn=3600  # 1 hour
)
# Return URL to client for direct S3 download
```

---

## Pre-Signed URL Flow: Details
1. Client requests download from application
1. Application generates pre-signed URL (valid for N minutes)
1. Application returns URL to client
1. Client downloads directly from S3/Blob Storage
1. No traffic through application server

---

## Pre-Signed URL Flow

![presigned](svg/courses/cloud/architecting-in-the-cloud/12_patterns/presigned_url_flow.svg)

---

## Pattern: Direct Upload to Storage
- Same pattern for uploads
- Client gets pre-signed POST/PUT URL
- Client uploads directly to S3
- S3 event triggers processing (Lambda)
- Handles large file uploads without proxying

---

## Pattern: CDN for Non-Data-Center Caches
- CloudFront/CDN in front of S3 or application
- Edge locations serve content globally
- Reduce latency from 200ms to 20ms
- Origin Shield: additional caching layer
- Cache API responses, not just static assets

---

## Pattern: Static Website with API
- Static frontend hosted on S3 + CloudFront
- API backend on Lambda or containers
- No web servers to manage
- Frontend scales infinitely (object storage)
- Cheapest and most scalable web architecture

---

## S3 Static Website in Terraform

```hcl
resource "aws_s3_bucket_website_configuration" "site" {
  bucket = aws_s3_bucket.site.id
  index_document { suffix = "index.html" }
  error_document { key    = "error.html" }
}

resource "aws_cloudfront_distribution" "cdn" {
  origin {
    domain_name = aws_s3_bucket.site.bucket_regional_domain_name
    origin_id   = "s3-site"
    origin_access_control_id = aws_cloudfront_origin_access_control.s3.id
  }
  enabled             = true
  default_root_object = "index.html"
  # ... viewer certificate, cache behavior
}
```

---

## Pattern: Service-to-Service via API
- REST or gRPC between microservices
- Service discovery (DNS, service mesh, cloud map)
- Circuit breakers for fault tolerance
- API Gateway for external access
- Internal APIs via private networking

---

## Pattern: Event-Driven Architecture
- Components communicate through events
- EventBridge, SNS, Pub/Sub as event bus
- Loose coupling: producers don't know consumers
- Easy to add new consumers
- Natural for microservices

---

## Event-Driven Architecture

![eda](svg/courses/cloud/architecting-in-the-cloud/12_patterns/event_driven_architecture.svg)

---

## Pattern: CQRS
- Command Query Responsibility Segregation
- Separate read and write models
- Write to primary database
- Read from optimized read store (cache, search, read replica)
- Scale reads and writes independently

---

## Pattern: Saga
- Distributed transaction across microservices
- Each step has a compensating action
- Choreography: events trigger next step
- Orchestration: central coordinator (Step Functions)
- Replace distributed transactions with eventual consistency

---

## Pattern: Strangler Fig
- Gradually migrate from monolith to microservices
- Route traffic: old system or new service
- Migrate one feature at a time
- No big-bang rewrite
- Reduce risk of migration

---

## Pattern: Sidecar
- Auxiliary container alongside main application
- Handles cross-cutting concerns
- Logging, monitoring, security, networking
- Service mesh proxies (Envoy, Istio)
- Application code stays focused on business logic

---

## Pattern: Circuit Breaker
- Detect when a downstream service is failing
- Stop calling it (open circuit)
- Return fallback or error immediately
- Periodically check if service recovered (half-open)
- Prevent cascade failures

---

## Circuit Breaker States

![circuit_breaker](svg/courses/cloud/architecting-in-the-cloud/12_patterns/circuit_breaker_states.svg)

---

## Pattern: Bulkhead
- Isolate failures to a subset of resources
- Separate thread pools or instances per dependency
- One failing dependency doesn't consume all resources
- Named after ship compartments
- Limits blast radius

---

## Pattern: Retry with Exponential Backoff
- Retry failed requests with increasing delays
- 1s, 2s, 4s, 8s... with jitter
- Handles transient failures (network blips, throttling)
- Maximum retry count to prevent infinite loops
- Standard in all AWS SDKs

---

## Pattern: Queue-Based Load Leveling
- Place a queue between producer and consumer
- Absorbs traffic spikes
- Consumer processes at its own pace
- Prevents overloading downstream services
- Natural backpressure mechanism

---

## Pattern: Backend for Frontend (BFF)
- Separate backend per frontend type
- Web, mobile, IoT each get their own API
- Optimize response for each client
- Avoid one-size-fits-all APIs
- Reduces over-fetching and under-fetching

---

## Pattern: Ambassador
- Helper service alongside main application
- Handle cross-cutting concerns
- TLS termination, logging, routing
- Similar to sidecar, often at the edge
- Simplifies application code

---

## Pattern: Competing Consumers
- Multiple consumers read from the same queue
- Each message processed by one consumer
- Auto-scale consumers based on queue depth
- Natural load distribution
- Most common pattern for async processing

---

## Pattern: Priority Queue
- Multiple queues with different priority levels
- High-priority queue: processed first
- Low-priority queue: processed when capacity allows
- Workers consume from high-priority queue first
- SQS: separate queues per priority level

---

## Anti-Pattern: Distributed Monolith
- Microservices that are tightly coupled
- All services must deploy together
- Synchronous calls everywhere
- No independent scaling
- Worse than a monolith (complexity without benefits)

---

## Anti-Pattern: Chatty Microservices
- Excessive inter-service communication
- Many round trips for a single operation
- High latency and failure risk
- Aggregate calls, use async where possible
- Consider if services should be merged

---

## Anti-Pattern: Over-Engineering
- Using microservices for a simple CRUD app
- Adding message queues when direct calls suffice
- Multi-Region when a single Region is enough
- CQRS for simple read/write workloads
- Complexity has a cost: justify every pattern

---

## Pattern: Health Endpoint Monitoring
- Expose /health endpoint on every service
- Check dependencies (database, cache, external APIs)
- Load balancers use for routing decisions
- Monitoring systems use for alerting
- Deep health checks vs shallow pings

---

## Pattern: Throttling
- Protect services from overload
- Return 429 (Too Many Requests) when exceeded
- Token bucket or sliding window algorithms
- API Gateway built-in throttling
- Per-client rate limiting

---

## Choosing Patterns
- Start simple, add complexity when needed
- Monolith is fine for many applications
- Patterns solve specific problems
- Don't add patterns to solve problems you don't have
- Measure and optimize based on real bottlenecks
