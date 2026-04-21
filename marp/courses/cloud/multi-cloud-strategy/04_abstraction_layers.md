---
tags:
  - infrastructure:cloud
  - infrastructure:aws
  - infrastructure:azure
  - infrastructure:gcp
  - concepts:architecture
level: advanced
category: cloud
audience:
  - audiences:architects
  - audiences:managers

---
# Abstraction Layers and Tooling

---

## Why Abstraction Layers?
- Single interface to manage multiple clouds
- Reduce cognitive load on engineering teams
- Enable workload portability
- Centralize policy enforcement
- Trade-off: abstraction always hides some capabilities

---

## The Lowest Common Denominator Problem
- Abstractions can only expose what all providers share
- Unique provider features get hidden or ignored
- Performance optimizations may be unavailable
- The abstraction becomes the ceiling
- Balance portability with capability

---

## Terraform: The Multi-Cloud Standard
- HashiCorp Configuration Language (HCL)
- Provider plugins for every major cloud
- Declarative: describe desired state, Terraform reconciles
- State management tracks what exists
- Largest community and module ecosystem

---

## Terraform: Multi-Cloud Module Pattern

```hcl
# modules/compute/main.tf
variable "cloud_provider" {
  type = string
}

variable "instance_name" {
  type = string
}

variable "instance_size" {
  type    = string
  default = "medium"
}

locals {
  size_map = {
    aws   = { small = "t3.small", medium = "t3.medium", large = "t3.large" }
    azure = { small = "Standard_B1s", medium = "Standard_B2s", large = "Standard_B4ms" }
    gcp   = { small = "e2-small", medium = "e2-medium", large = "e2-standard-4" }
  }
}
```

---

## Terraform Module: AWS Implementation

```hcl
resource "aws_instance" "this" {
  count         = var.cloud_provider == "aws" ? 1 : 0
  ami           = data.aws_ami.ubuntu.id
  instance_type = local.size_map["aws"][var.instance_size]

  tags = {
    Name = var.instance_name
  }
}

data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"]

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }
}
```

---

## Terraform Module: GCP Implementation

```hcl
resource "google_compute_instance" "this" {
  count        = var.cloud_provider == "gcp" ? 1 : 0
  name         = var.instance_name
  machine_type = local.size_map["gcp"][var.instance_size]
  zone         = var.gcp_zone

  boot_disk {
    initialize_params {
      image = "ubuntu-os-cloud/ubuntu-2204-lts"
    }
  }

  network_interface {
    network = "default"
  }
}
```

---

## Terraform Limitations for Multi-Cloud
- HCL is declarative but provider resources are unique
- Modules must map between different resource models
- State files are per-workspace — cross-cloud references are awkward
- Provider version drift creates maintenance burden
- Complex multi-cloud setups need wrapper tooling

---

## Terraform Multi-Cloud Architecture

![terraform](svg/courses/cloud/multi-cloud-strategy/04_abstraction_layers/terraform_multi_cloud.svg)

---

## Pulumi: Infrastructure as Real Code
- Use Python, TypeScript, Go, Java, C# instead of HCL
- Full programming language: loops, conditionals, abstractions
- Same provider coverage as Terraform (uses Terraform providers)
- Better for teams that prefer general-purpose languages
- Supports multi-cloud from a single program

---

## OpenTofu: The Open-Source Fork
- Fork of Terraform after HashiCorp BSL license change
- Drop-in replacement for Terraform
- Community-governed under Linux Foundation
- Same HCL language and provider ecosystem
- Consider for organizations concerned about license risk

---

## Crossplane: Kubernetes-Native Infrastructure
- Manage cloud resources using Kubernetes custom resources
- Declarative, GitOps-friendly
- Composition: define your own platform APIs
- Runs as a Kubernetes controller
- Ideal if Kubernetes is already your control plane

---

## Crossplane Composite Resource Definition

```yaml
apiVersion: apiextensions.crossplane.io/v1
kind: CompositeResourceDefinition
metadata:
  name: xdatabases.platform.example.com
spec:
  group: platform.example.com
  names:
    kind: XDatabase
    plural: xdatabases
  versions:
    - name: v1alpha1
      served: true
      referenceable: true
      schema:
        openAPIV3Schema:
          type: object
          properties:
            spec:
              type: object
              properties:
                engine:
                  type: string
                  enum: ["postgres", "mysql"]
                size:
                  type: string
                  enum: ["small", "medium", "large"]
                provider:
                  type: string
                  enum: ["aws", "azure", "gcp"]
```

---

## Crossplane Composition Example

```yaml
apiVersion: apiextensions.crossplane.io/v1
kind: Composition
metadata:
  name: xdatabase-aws
spec:
  compositeTypeRef:
    apiVersion: platform.example.com/v1alpha1
    kind: XDatabase
  resources:
    - name: rds-instance
      base:
        apiVersion: rds.aws.upbound.io/v1beta1
        kind: Instance
        spec:
          forProvider:
            engine: postgres
            engineVersion: "16"
            instanceClass: db.t3.medium
            allocatedStorage: 20
```

---

## Abstraction Trade-Offs Summary
- More abstraction: better portability, fewer provider features
- Less abstraction: full provider capabilities, harder to switch
- There is no perfect abstraction — choose based on priorities
- Internal platform APIs (Crossplane) offer a middle ground
- Document which provider features you sacrifice

---

## Abstraction Trade-Offs

![tradeoffs](svg/courses/cloud/multi-cloud-strategy/04_abstraction_layers/abstraction_trade_offs.svg)

---

## Choosing the Right Tool
- Terraform/OpenTofu: broad adoption, large ecosystem, mature
- Pulumi: strong for developer-centric teams
- Crossplane: ideal for platform teams running Kubernetes
- Cloud-specific tools (CloudFormation, ARM, Deployment Manager): avoid for multi-cloud
- Many organizations combine tools for different layers
