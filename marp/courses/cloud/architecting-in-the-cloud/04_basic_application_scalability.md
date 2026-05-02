---
tags:
  - infrastructure:cloud
  - concepts:scalability
  - concepts:architecture
level: intermediate
category: cloud
audience:
  - audiences:developers
  - audiences:architects
  - audiences:devops

---
# Basic Application Scalability

---
## Horizontal vs Vertical

![horizontal_vs_vertical](svg/courses/cloud/architecting-in-the-cloud/04_basic_application_scalability/horizontal_vs_vertical.svg)

---

## Why Scalability Matters
- Users expect fast, always-available applications
- Traffic is rarely constant
- Flash sales, product launches, viral content
- Under-scaled: poor user experience and lost revenue
- Over-scaled: wasted money

---

## Vertical vs Horizontal Scaling: Details
- Vertical (scale up): bigger machine, more CPU/RAM
- Horizontal (scale out): more machines
- Vertical has a ceiling (largest instance available)
- Horizontal is theoretically unlimited
- Cloud architecture favors horizontal scaling

---

## Vertical vs Horizontal Scaling

![scaling](svg/courses/cloud/architecting-in-the-cloud/04_scalability/vertical_vs_horizontal.svg)

---

## Stateless vs Stateful
- Stateless: no data stored on the instance between requests
- Stateful: instance holds session data, state
- Stateless services are easy to scale horizontally
- Move state to external stores (database, cache, session store)
- This is the most important scalability principle

---

## Making Applications Stateless
- Store sessions in Redis, DynamoDB, or Memcached
- Store files in S3 or shared file systems
- Store user data in databases
- Application instances become interchangeable
- Any instance can handle any request

---

## Load Balancers
- Distribute traffic across multiple instances
- Health checks remove unhealthy instances
- Single entry point for the application
- SSL/TLS termination
- Critical for horizontal scaling

---

## Types of Load Balancers
- Layer 4 (Network): routes based on IP/port (fast, simple)
- Layer 7 (Application): routes based on HTTP content (flexible)
- Layer 7: path-based, host-based, header-based routing
- Use Layer 7 for web apps, Layer 4 for TCP/UDP
- Managed LBs: no servers to maintain

---

## Load Balancing Algorithms
- Round Robin: equal distribution
- Least Connections: send to least busy
- Weighted: proportional distribution
- IP Hash: sticky by client IP
- Choose based on application requirements

---

## Health Checks
- Load balancer pings instances periodically
- HTTP check: expects 200 response
- TCP check: expects successful connection
- Unhealthy instances removed from rotation
- Configure thresholds and intervals carefully

---

## ALB Health Check in Terraform

```hcl
resource "aws_lb_target_group" "web" {
  name     = "web-tg"
  port     = 80
  protocol = "HTTP"
  vpc_id   = aws_vpc.main.id

  health_check {
    path                = "/health"
    healthy_threshold   = 2
    unhealthy_threshold = 3
    timeout             = 5
    interval            = 30
    matcher             = "200"
  }
}
```

---

## Auto Scaling
- Automatically add/remove instances based on demand
- Scale out on high CPU, request count, queue depth
- Scale in when demand drops
- Maintain minimum and maximum instance counts
- Cloud-native feature on all major providers

---

## Auto Scaling with Load Balancer

![auto_scaling](svg/courses/cloud/architecting-in-the-cloud/04_scalability/auto_scaling_with_lb.svg)

---

## Scaling Policies
- Target Tracking: maintain a target (e.g., 60% CPU)
- Step Scaling: add N instances when metric exceeds threshold
- Scheduled Scaling: scale at known times (business hours)
- Predictive Scaling: ML-based forecast
- Target Tracking is the simplest and recommended starting point

---

## Target Tracking Scaling Policy

```bash
aws autoscaling put-scaling-policy \
  --auto-scaling-group-name web-asg \
  --policy-name cpu-target-tracking \
  --policy-type TargetTrackingScaling \
  --target-tracking-configuration '{
    "PredefinedMetricSpecification": {
      "PredefinedMetricType":
        "ASGAverageCPUUtilization"
    },
    "TargetValue": 60.0
  }'
```

---

## Scaling Considerations
- Cooldown periods prevent rapid oscillation
- Scale out fast, scale in slow
- Test scaling behavior under load
- Monitor scaling events
- Ensure AMI/image is up to date for new instances

---

## Spreading Across Data Centers
- Deploy to multiple Availability Zones
- Load balancer distributes across AZs
- Survive the loss of an entire data center
- Slightly higher data transfer cost
- Standard practice for production workloads

---

## Multi-Region Architecture: Details
- Deploy to multiple Regions for global reach
- DNS-based routing (Route 53, Cloud DNS)
- Active-active or active-passive
- Data replication between Regions
- Significantly more complex than multi-AZ

---

## Multi-Region Architecture

![multi_region](svg/courses/cloud/architecting-in-the-cloud/04_scalability/multi_region_architecture.svg)

---

## Cross-AZ Data Transfer Costs
- Traffic between AZs is charged (typically $0.01/GB)
- Can add up for chatty services
- Optimize: keep related services in same AZ when possible
- Or accept the cost for availability
- Monitor cross-AZ traffic in billing

---

## Connection Draining
- When scaling in, allow existing connections to complete
- Load balancer deregisters target gracefully
- Configurable drain timeout (default 300 seconds)
- Prevents dropped requests during scale-in
- Always enable for production

---

## Load Testing
- Test scalability before going to production
- Tools: k6, Gatling, Locust, JMeter
- Simulate realistic traffic patterns
- Test auto-scaling triggers and response time
- Identify bottlenecks early

---

## Database Scalability
- Databases are often the scalability bottleneck
- Read replicas for read scaling
- Caching layer reduces database load
- Sharding for write scaling (complex)
- Consider NoSQL for simple access patterns at scale

---

## Microservices and Scalability
- Each service scales independently
- Scale the bottleneck, not the entire application
- Loose coupling enables independent scaling
- More operational complexity
- Not always needed: monolith can scale well too

---

## Should You Go Serverless?
- Serverless eliminates instance management entirely
- Auto-scales from zero to thousands
- Pay only for execution time
- Great for event-driven and API workloads
- Not suitable for all workloads (long-running, GPU)

---

## Serverless vs Containers vs VMs
- VMs: full control, most overhead
- Containers: good isolation, fast start, orchestration needed
- Serverless: zero management, limited control
- Each has its sweet spot
- Many architectures combine all three

---

## Global Accelerator
- AWS Global Accelerator: static IP anycast routing
- Routes to optimal Region based on health and proximity
- Improves availability and performance
- Faster failover than DNS-based
- Good for multi-Region active-active

---

## Auto Scaling Lifecycle Hooks
- Perform actions during scale-out and scale-in
- Scale-out: register with service discovery, warm cache
- Scale-in: deregister, drain connections, save state
- Integrate with SNS, SQS, Lambda
- Ensure clean instance lifecycle

---

## Capacity Planning
- Analyze historical traffic patterns
- Identify peak times (daily, weekly, seasonal)
- Set Auto Scaling minimums for baseline
- Use Predictive Scaling for known patterns
- Load test to find maximum capacity per instance

---

## Scalability Anti-Patterns
- Single instance behind a public IP (no LB)
- Session state stored in local memory
- Hard-coded instance IPs in configuration
- Synchronous calls to slow downstream services
- Database as the only integration point

---

## Throttling and Rate Limiting
- Protect your services from overload
- API Gateway rate limiting
- Application-level throttling
- Return 429 Too Many Requests
- Graceful degradation under load

---

## Session Management
- Sessions must not live on the instance
- Redis: fast, feature-rich session store
- DynamoDB: serverless, scalable
- Encrypted and time-limited session tokens
- Session stickiness as a last resort

---

## Asynchronous Processing
- Not everything needs an immediate response
- Queue work for background processing
- Return 202 Accepted, process later
- Email sending, report generation, image processing
- Decouples user experience from processing time

---

## Content Delivery Networks
- Cache and serve content at edge locations
- Reduce load on origin servers
- Lower latency for global users
- CloudFront, Akamai, Fastly, Azure CDN
- Essential for any globally-served application

---

## Scalability Checklist
1. Application is stateless
1. Load balancer in front
1. Auto Scaling configured
1. Deployed across multiple AZs
1. Health checks defined
1. External session and state stores
1. Tested under load
