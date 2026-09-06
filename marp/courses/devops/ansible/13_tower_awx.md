---
tags:
  - practices:devops
  - tools:ansible
  - infrastructure:configuration-management
  - infrastructure:cloud
  - practices:automation
level: intermediate
category: devops
audience:
  - audiences:developers
  - audiences:sysadmins
  - audiences:devops

---

# Ansible Tower / AWX Overview

## Topics Covered
- What is `Ansible Tower` / `AWX`
- Architecture and components
- Key features: RBAC, workflows, inventories
- Job templates and scheduling
- REST API and integrations
- Tower vs AWX comparison

---

## What is Ansible Tower / AWX?

- **Ansible Tower**: Red Hat's commercial, supported product
- **AWX**: Open-source upstream project for Tower
- Web-based UI and REST API for `Ansible`
- Enterprise features: RBAC, logging, scheduling, workflows
- Centralizes `Ansible` management for teams

---

## Tower / AWX Architecture

![tower_awx_architecture](svg/courses/devops/ansible/13_tower_awx/tower_awx_architecture.svg)

---

## Key Features

| Feature | Description |
|---------|-------------|
| **RBAC** | Role-based access control for teams |
| **Job Templates** | Reusable playbook run configurations |
| **Workflows** | Chain multiple playbooks with logic |
| **Scheduling** | Cron-like job scheduling |
| **Credentials** | Secure credential management |
| **Inventory Sync** | Auto-sync from cloud providers |
| **Notifications** | Slack, email, webhook alerts |
| **Audit Trail** | Full logging of who ran what, when |
| **REST API** | Programmatic access to everything |
| **Survey Forms** | User-friendly input collection |

---

## RBAC in Tower

```tree
Organization
  └── Teams
       ├── Team: DevOps
       │     ├── Admin: Full access to team resources
       │     ├── Member: Execute job templates
       │     └── Read: View-only access
       │
       └── Team: Developers
             ├── Can execute: Deploy App template
             ├── Cannot execute: DB Migration template
             └── Cannot access: Production inventory
```

---

## Job Templates

- Pre-configured playbook execution settings
- Specify: playbook, inventory, credentials, variables
- Optional: survey forms for runtime input
- Can be launched via UI, API, or schedule

```tree
Job Template: "Deploy Application"
  ├── Playbook: deploy.yml
  ├── Inventory: Production
  ├── Credential: SSH Key (prod)
  ├── Extra Variables:
  │     app_version: (prompted)
  │     env: production
  ├── Limit: webservers
  ├── Tags: deploy
  └── Survey:
        └── "App Version" (required, text input)
```

---

## Workflows

```tree
Start
  │
  ├── [Success] ──> Run Tests
  │                    │
  │                    ├── [Success] ──> Deploy to Staging
  │                    │                    │
  │                    │                    ├── [Success] ──> Deploy to Production
  │                    │                    │                    │
  │                    │                    │                    └── [Always] ──> Notify
  │                    │                    │
  │                    │                    └── [Failure] ──> Rollback Staging
  │                    │
  │                    └── [Failure] ──> Notify Dev Team
  │
  └── [Failure] ──> Alert Ops
```

- Chain job templates with success/failure/always paths
- Pass variables between workflow nodes
- Approval nodes for manual gates

---

## Credential Types

| Type | Use Case |
|------|----------|
| Machine | `SSH` keys for managed nodes |
| Source Control | `Git` repository access |
| Vault | `Ansible Vault` password |
| Cloud (AWS) | AWS access key + secret |
| Cloud (Azure) | Azure service principal |
| Cloud (GCP) | GCP service account |
| Container Registry | Docker Hub, ECR |
| Custom | Any credential type you define |

---

## Inventory Sources in Tower

```tree
Inventory: "Cloud Production"
  ├── Source: AWS EC2 (auto-sync every 30 min)
  │     ├── Regions: us-east-1, eu-west-1
  │     └── Filter: tag:Env=production
  │
  ├── Source: Azure RM (auto-sync every 30 min)
  │     └── Resource Groups: prod-rg
  │
  ├── Static Group: "bastion"
  │     └── Host: bastion.example.com
  │
  └── Smart Inventory:
        └── Filter: ansible_os_family:Debian AND env:production
```

---

## Tower REST API

```bash
# List job templates
curl -s -H "Authorization: Bearer $TOKEN" \
    https://tower.example.com/api/v2/job_templates/ | jq '.results[].name'

# Launch a job template
curl -s -X POST \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d '{"extra_vars": {"app_version": "2.1.0"}}' \
    https://tower.example.com/api/v2/job_templates/15/launch/

# Check job status
curl -s -H "Authorization: Bearer $TOKEN" \
    https://tower.example.com/api/v2/jobs/42/ | jq '.status'

# Get job stdout
curl -s -H "Authorization: Bearer $TOKEN" \
    https://tower.example.com/api/v2/jobs/42/stdout/?format=txt
```

---

## AWX Installation (Docker Compose)

```bash
# Clone AWX repository
git clone https://github.com/ansible/awx.git
cd awx

# Install AWX operator (Kubernetes)
# Or use docker-compose for development
cd tools/docker-compose
make docker-compose-build
docker compose up -d

# Access AWX at http://localhost:8013
# Default credentials: admin / password

# AWX CLI (awxkit)
pip install awxkit
awx --conf.host https://awx.example.com \
    --conf.username admin \
    --conf.password password \
    job_templates list
```

---

## Tower vs AWX Comparison

| Feature | AWX (Free) | Tower (Paid) |
|---------|-----------|--------------|
| Core features | Yes | Yes |
| Red Hat support | No | Yes |
| Security patches | Community | Guaranteed SLA |
| LDAP/SAML | Yes | Yes |
| Clustering | Yes | Yes |
| Certified content | No | Yes |
| SLA | None | Available |
| Updates | Frequent/unstable | Stable releases |

---

## Execution Environments

- Container images with `Ansible` + dependencies
- Replaced Python virtual environments in Tower 4.0+
- Built with `ansible-builder`

```yaml
# execution-environment.yml

---
version: 3
dependencies:
  galaxy: requirements.yml
  python: requirements.txt
  system: bindep.txt

build_arg_defaults:
  ANSIBLE_GALAXY_CLI_COLLECTION_OPTS: '--pre'

additional_build_steps:
  prepend_base:
    - RUN pip3 install --upgrade pip
  append_final:
    - RUN whoami
    - COPY custom_certs/ /etc/pki/ca-trust/source/anchors/
```

```bash
# Build execution environment
ansible-builder build -t my-custom-ee:latest
```

---

## When to Use Tower / AWX

- Multiple teams share `Ansible` automation
- Need RBAC and audit trails
- Self-service IT operations for non-`Ansible` users
- Scheduled automation (patching, compliance)
- Workflow orchestration across teams
- API-driven automation integration
- Centralized credential management
- Compliance and reporting requirements

---

## Tower and AWX Features

![tower_awx_features](svg/courses/devops/ansible/13_tower_awx/tower_awx_features.svg)
