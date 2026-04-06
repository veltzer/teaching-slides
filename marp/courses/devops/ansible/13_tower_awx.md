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

<svg xmlns="http://www.w3.org/2000/svg" width="640" height="310" font-family="sans-serif">
<defs>
  <marker id="arrow" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
    <polygon points="0 0, 10 3.5, 0 7" fill="#555"/>
  </marker>
</defs>
<rect x="10" y="10" width="620" height="200" fill="#f5f5f5" stroke="#333" stroke-width="2" rx="4"/>
<text x="320" y="30" font-size="15" font-weight="bold" fill="#222" text-anchor="middle">Tower / AWX</text>
<rect x="25" y="45" width="180" height="55" fill="#e3f2fd" stroke="#333" stroke-width="1.5" rx="4"/>
<text x="115" y="67" font-size="12" font-weight="bold" fill="#222" text-anchor="middle">Web UI</text>
<text x="115" y="83" font-size="11" font-weight="normal" fill="#222" text-anchor="middle">(React)</text>
<rect x="225" y="45" width="180" height="55" fill="#e3f2fd" stroke="#333" stroke-width="1.5" rx="4"/>
<text x="315" y="67" font-size="12" font-weight="bold" fill="#222" text-anchor="middle">REST API</text>
<text x="315" y="83" font-size="11" font-weight="normal" fill="#222" text-anchor="middle">(Django)</text>
<rect x="425" y="45" width="180" height="55" fill="#e3f2fd" stroke="#333" stroke-width="1.5" rx="4"/>
<text x="515" y="67" font-size="12" font-weight="bold" fill="#222" text-anchor="middle">Task Engine</text>
<text x="515" y="83" font-size="11" font-weight="normal" fill="#222" text-anchor="middle">(Dispatcher)</text>
<rect x="25" y="120" width="180" height="55" fill="#e8f5e9" stroke="#333" stroke-width="1.5" rx="4"/>
<text x="115" y="142" font-size="12" font-weight="bold" fill="#222" text-anchor="middle">PostgreSQL</text>
<text x="115" y="158" font-size="11" font-weight="normal" fill="#222" text-anchor="middle">(data)</text>
<rect x="225" y="120" width="180" height="55" fill="#e8f5e9" stroke="#333" stroke-width="1.5" rx="4"/>
<text x="315" y="142" font-size="12" font-weight="bold" fill="#222" text-anchor="middle">Redis</text>
<text x="315" y="158" font-size="11" font-weight="normal" fill="#222" text-anchor="middle">(queue)</text>
<rect x="425" y="120" width="180" height="55" fill="#e8f5e9" stroke="#333" stroke-width="1.5" rx="4"/>
<text x="515" y="142" font-size="12" font-weight="bold" fill="#222" text-anchor="middle">Receptor</text>
<text x="515" y="158" font-size="11" font-weight="normal" fill="#222" text-anchor="middle">(mesh network)</text>
<line x1="320" y1="210" x2="320" y2="248" stroke="#555" stroke-width="1.5" marker-end="url(#arrow)"/>
<text x="330" y="234" font-size="11" fill="#555">SSH</text>
<rect x="20" y="250" width="230" height="45" fill="#c8e6c9" stroke="#333" stroke-width="1.5" rx="4"/>
<text x="135" y="268" font-size="12" font-weight="bold" fill="#222" text-anchor="middle">Managed Nodes</text>
<rect x="270" y="250" width="230" height="45" fill="#ffe0b2" stroke="#333" stroke-width="1.5" rx="4"/>
<text x="385" y="268" font-size="12" font-weight="bold" fill="#222" text-anchor="middle">Execution Environments</text>
<text x="385" y="284" font-size="11" font-weight="normal" fill="#222" text-anchor="middle">(containers)</text>
</svg>

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
