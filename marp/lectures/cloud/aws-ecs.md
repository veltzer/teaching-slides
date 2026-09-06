---
tags:
  - infrastructure:cloud
  - infrastructure:aws
  - practices:containers
level: intermediate
category: cloud
audience:
  - audiences:developers
  - audiences:sysadmins
  - audiences:devops

---

# AWS ECS: Elastic Container Service
## Mark Veltzer
## [mark.veltzer@gmail.com](mailto:mark.veltzer@gmail.com)

---

## Overview

![title](svg/lectures/cloud/aws-ecs/title.svg)

---

## What is ECS?
- Fully managed container orchestration service from AWS
- Runs and scales Docker containers without managing your own orchestrator
- Deeply integrated with the rest of the AWS ecosystem
- Two launch models: EC2 and Fargate
- A simpler alternative to running Kubernetes yourself

---

## Why Container Orchestration?
- Containers package an app with its dependencies
- Production needs more than `docker run` on one host
- Scheduling: where should each container run?
- Scaling: add and remove containers with demand
- Recovery: restart failed containers automatically
- Networking and service discovery across many hosts

---

## Where ECS Fits
- ECS is the orchestrator (the "brain")
- It decides what runs, where, and how many
- It does not build your images — that is Docker / a CI pipeline
- It does not store images — that is a registry (ECR)
- It leans on other AWS services for networking, scaling, and logs

---

## ECS vs EKS vs Kubernetes
- **ECS**: AWS-native, simpler, no control-plane to manage
- **EKS**: managed Kubernetes, portable, more complex
- **Self-managed k8s**: maximum control, maximum operational burden
- Choose ECS for AWS-centric teams wanting low overhead
- Choose EKS when you need the Kubernetes ecosystem

---

## Core Building Blocks
- **Cluster**: logical grouping of capacity
- **Task Definition**: blueprint for one or more containers
- **Task**: a running instance of a task definition
- **Service**: keeps a desired number of tasks running
- **Container Agent**: connects EC2 hosts to ECS (EC2 mode only)

---

## The Cluster
- A logical boundary for running tasks and services
- Provides isolation between workloads and environments
- Backed by EC2 instances, Fargate, or both
- A single account can have many clusters
- Often split by environment: `dev`, `staging`, `prod`

---

## Task Definitions
- JSON blueprint describing how to run containers
- Specifies image, CPU, memory, ports, and environment
- Defines volumes, logging, and IAM roles
- Immutable and versioned — each change is a new revision
- Think of it as the "recipe", not the running dish

---

## Anatomy of a Task Definition
- **Family**: name shared across revisions
- **Container definitions**: one or more containers
- **CPU / memory**: at task and container level
- **Network mode**: `awsvpc`, `bridge`, `host`, or `none`
- **Task role** and **execution role**: permissions

---

## Example Task Definition
```json
{
  "family": "web-app",
  "networkMode": "awsvpc",
  "cpu": "256",
  "memory": "512",
  "containerDefinitions": [
    {
      "name": "web",
      "image": "123456789.dkr.ecr.us-east-1.amazonaws.com/web:latest",
      "portMappings": [{ "containerPort": 8080 }],
      "essential": true
    }
  ]
}
```

---

## Tasks
- A task is a running instance of a task definition
- Can hold a single container or several tightly coupled ones
- Containers in a task share networking and lifecycle
- Tasks can be run once (batch) or kept alive (services)
- When a task stops, it is gone — not restarted by itself

---

## Services
- Maintains a desired count of running tasks
- Restarts tasks that fail or are stopped
- Integrates with load balancers to spread traffic
- Performs rolling deployments for new revisions
- The right choice for long-running applications

---

## Launch Types Overview
- **EC2**: you provide and manage the instances
- **Fargate**: AWS provides the compute, serverless
- Both run the same task definitions (mostly)
- Choice affects cost, control, and operational effort
- Can be mixed within a cluster via capacity providers

---

## EC2 Launch Type
- You run a fleet of EC2 instances in the cluster
- The ECS agent on each host reports capacity
- You control instance type, AMI, and patching
- Better for steady, high-utilization workloads
- More control, but more operational responsibility

---

## Fargate Launch Type
- Serverless — no EC2 instances to manage
- You specify CPU and memory per task
- AWS handles provisioning, patching, and scaling of hosts
- Pay per task for the resources requested
- Great for variable or spiky workloads

---

## EC2 vs Fargate
- **Control**: EC2 wins (custom AMIs, GPUs, special instances)
- **Operations**: Fargate wins (no host management)
- **Cost**: EC2 can be cheaper at high steady utilization
- **Speed to start**: Fargate is simpler to launch
- Start with Fargate; move to EC2 when you have a reason

---

## Networking: awsvpc Mode
- Each task gets its own elastic network interface (ENI)
- Tasks receive a private IP from your VPC
- Security groups apply directly to tasks
- Required for Fargate
- Cleanest model for isolation and security

---

## Other Network Modes (EC2)
- **bridge**: Docker's default virtual network
- **host**: container shares the host's network stack
- **none**: no external networking
- Used only with the EC2 launch type
- `awsvpc` is the recommended default

---

## Load Balancing
- Services register tasks with an Elastic Load Balancer
- **Application Load Balancer (ALB)**: HTTP/HTTPS, path routing
- **Network Load Balancer (NLB)**: TCP/UDP, high performance
- Dynamic port mapping lets many tasks share a host
- Health checks remove unhealthy tasks from rotation

---

## Service Discovery
- Tasks come and go, so IPs change constantly
- **AWS Cloud Map** maps service names to running tasks
- Enables DNS-based discovery within the VPC
- Lets services find each other without hardcoded IPs
- Combine with a load balancer for external traffic

---

## ECR: The Image Registry
- Elastic Container Registry stores your Docker images
- Private, secure, and integrated with IAM
- ECS pulls images directly from ECR at launch
- Supports image scanning for vulnerabilities
- Lifecycle policies clean up old images automatically

---

## Auto Scaling: Service
- **Service Auto Scaling** adjusts the task count
- Target tracking on CPU, memory, or custom metrics
- Step scaling reacts to CloudWatch alarm thresholds
- Scheduled scaling for known traffic patterns
- Keeps the desired count in line with demand

---

## Auto Scaling: Cluster (EC2)
- **Cluster capacity providers** scale the EC2 fleet
- Add instances when tasks cannot be placed
- Remove instances when capacity is idle
- Not needed with Fargate — AWS handles it
- Pairs with service auto scaling for end-to-end elasticity

---

## IAM and Permissions
- **Execution role**: lets ECS pull images and write logs
- **Task role**: permissions for the app inside the container
- Scope task roles tightly to what the app needs
- Avoid baking AWS credentials into images
- Follows the principle of least privilege

---

## Logging and Monitoring
- **awslogs** driver ships container logs to CloudWatch
- **Container Insights** gives cluster and service metrics
- Track CPU, memory, task counts, and failures
- Alarms can trigger scaling or notifications
- Centralized logs simplify debugging across tasks

---

## Deployment Strategies
- **Rolling update**: gradually replace old tasks (default)
- **Blue/green** (via CodeDeploy): shift traffic between versions
- Health checks gate the rollout
- `minimumHealthyPercent` and `maximumPercent` control pace
- Roll back automatically on failed health checks

---

## Secrets Management
- Never hardcode secrets in task definitions or images
- Pull from **AWS Secrets Manager** or **SSM Parameter Store**
- Injected as environment variables at task start
- Access controlled by the execution role
- Rotate secrets without rebuilding images

---

## Cost Considerations
- Fargate: pay per vCPU and GB-second per task
- EC2: pay for the instances regardless of task usage
- Use Spot capacity for fault-tolerant workloads
- Right-size CPU and memory in task definitions
- Savings Plans reduce cost for steady usage

---

## Best Practices
- Use `awsvpc` networking and tight security groups
- Separate task role from execution role
- One concern per task definition family
- Externalize config and secrets
- Tag everything for cost tracking and organization

---

## Common Pitfalls
- Over-provisioning CPU/memory and wasting money
- Forgetting health checks, causing bad rollouts
- Storing secrets in plain environment variables
- Ignoring log retention and ballooning costs
- Running everything in one giant cluster

---

## When to Use ECS
- You are already invested in AWS
- You want containers without running Kubernetes
- You value low operational overhead
- You need tight integration with AWS services
- Your team is small or AWS-focused

---

## Summary
- ECS is AWS-native container orchestration
- Task definitions are blueprints; services keep them running
- Fargate removes server management; EC2 gives control
- Integrates with ELB, ECR, IAM, CloudWatch, and auto scaling
- A pragmatic path to running containers in production

---

## Thank You
- Questions?
- [mark.veltzer@gmail.com](mailto:mark.veltzer@gmail.com)
