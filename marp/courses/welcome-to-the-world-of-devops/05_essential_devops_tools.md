# Essential DevOps Tools
Understanding the core toolset for DevOps implementation

---

## Version Control Systems

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <ellipse cx="300" cy="100" rx="55" ry="35" fill="#673ab7" stroke="#333" stroke-width="2"/>
  <text x="300" y="105" text-anchor="middle" font-size="11" fill="white">Git</text>
  <ellipse cx="120" cy="45" rx="75" ry="25" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <text x="120" y="42" text-anchor="middle" font-size="10">GitHub</text>
  <text x="120" y="55" text-anchor="middle" font-size="9">PRs, Actions, Issues</text>
  <ellipse cx="480" cy="45" rx="75" ry="25" fill="#f3e5f5" stroke="#333" stroke-width="2"/>
  <text x="480" y="42" text-anchor="middle" font-size="10">GitLab</text>
  <text x="480" y="55" text-anchor="middle" font-size="9">CI/CD, Registry, Wiki</text>
  <ellipse cx="120" cy="160" rx="75" ry="25" fill="#e8f5e9" stroke="#333" stroke-width="2"/>
  <text x="120" y="157" text-anchor="middle" font-size="10">Bitbucket</text>
  <text x="120" y="170" text-anchor="middle" font-size="9">Jira integration</text>
  <ellipse cx="480" cy="160" rx="75" ry="25" fill="#fff3e0" stroke="#333" stroke-width="2"/>
  <text x="480" y="157" text-anchor="middle" font-size="10">Azure Repos</text>
  <text x="480" y="170" text-anchor="middle" font-size="9">MS ecosystem</text>
  <line x1="250" y1="78" x2="190" y2="58" stroke="#333" stroke-width="1.5"/>
  <line x1="350" y1="78" x2="410" y2="58" stroke="#333" stroke-width="1.5"/>
  <line x1="250" y1="122" x2="190" y2="145" stroke="#333" stroke-width="1.5"/>
  <line x1="350" y1="122" x2="410" y2="145" stroke="#333" stroke-width="1.5"/>
</svg>

---

## Git Workflows

1. Create branch
1. Make changes
1. Commit code
1. Push changes
1. Create pull request

---

## Collaboration Platforms

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="20" text-anchor="middle" font-size="12" font-weight="bold">Collaboration Platform Ecosystem</text>
  <rect x="20" y="40" width="150" height="60" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="95" y="58" text-anchor="middle" font-size="10" font-weight="bold">Communication</text>
  <text x="95" y="73" text-anchor="middle" font-size="9">Slack / MS Teams</text>
  <text x="95" y="86" text-anchor="middle" font-size="9">ChatOps integration</text>
  <rect x="225" y="40" width="150" height="60" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="58" text-anchor="middle" font-size="10" font-weight="bold">Project Tracking</text>
  <text x="300" y="73" text-anchor="middle" font-size="9">Jira / Linear / Asana</text>
  <text x="300" y="86" text-anchor="middle" font-size="9">Backlog + sprints</text>
  <rect x="430" y="40" width="150" height="60" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="505" y="58" text-anchor="middle" font-size="10" font-weight="bold">Documentation</text>
  <text x="505" y="73" text-anchor="middle" font-size="9">Confluence / Notion</text>
  <text x="505" y="86" text-anchor="middle" font-size="9">Runbooks + wikis</text>
  <line x1="170" y1="70" x2="225" y2="70" stroke="#333" stroke-width="2" marker-end="url(#arrowd1_04_essential_devops_tools)"/>
  <line x1="375" y1="70" x2="430" y2="70" stroke="#333" stroke-width="2" marker-end="url(#arrowd1_04_essential_devops_tools)"/>
  <text x="300" y="135" text-anchor="middle" font-size="10" fill="#555">Integrated toolchain enables seamless team collaboration</text>
  <defs>
    <marker id="arrowd1_04_essential_devops_tools" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## CI/CD Tools Overview

1. Jenkins - Automation server
1. GitLab CI - Integrated pipeline
1. CircleCI - Cloud-native CI
1. Travis CI - GitHub integration
1. Azure DevOps - Microsoft suite

---

## Jenkins Pipeline

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="20" text-anchor="middle" font-size="12" font-weight="bold">Jenkins Pipeline Stages</text>
  <rect x="20" y="40" width="150" height="60" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="95" y="58" text-anchor="middle" font-size="10" font-weight="bold">Build Stage</text>
  <text x="95" y="73" text-anchor="middle" font-size="9">Compile + package</text>
  <text x="95" y="86" text-anchor="middle" font-size="9">Jenkinsfile as code</text>
  <rect x="225" y="40" width="150" height="60" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="58" text-anchor="middle" font-size="10" font-weight="bold">Test Stage</text>
  <text x="300" y="73" text-anchor="middle" font-size="9">Unit + integration</text>
  <text x="300" y="86" text-anchor="middle" font-size="9">Quality gates</text>
  <rect x="430" y="40" width="150" height="60" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="505" y="58" text-anchor="middle" font-size="10" font-weight="bold">Deploy Stage</text>
  <text x="505" y="73" text-anchor="middle" font-size="9">Staging then prod</text>
  <text x="505" y="86" text-anchor="middle" font-size="9">Approval gates</text>
  <line x1="170" y1="70" x2="225" y2="70" stroke="#333" stroke-width="2" marker-end="url(#arrowd2_04_essential_devops_tools)"/>
  <line x1="375" y1="70" x2="430" y2="70" stroke="#333" stroke-width="2" marker-end="url(#arrowd2_04_essential_devops_tools)"/>
  <text x="300" y="135" text-anchor="middle" font-size="10" fill="#555">Declarative pipelines define the entire delivery workflow</text>
  <defs>
    <marker id="arrowd2_04_essential_devops_tools" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Containerization Basics

1. Image creation
1. Container management
1. Network configuration
1. Volume management
1. Resource allocation

---

## Docker Components

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <ellipse cx="300" cy="100" rx="55" ry="35" fill="#673ab7" stroke="#333" stroke-width="2"/>
  <text x="300" y="96" text-anchor="middle" font-size="11" fill="white">Docker</text>
  <text x="300" y="110" text-anchor="middle" font-size="10" fill="white">Engine</text>
  <ellipse cx="120" cy="45" rx="75" ry="25" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <text x="120" y="42" text-anchor="middle" font-size="10">Dockerfile</text>
  <text x="120" y="55" text-anchor="middle" font-size="9">Image definition</text>
  <ellipse cx="480" cy="45" rx="75" ry="25" fill="#f3e5f5" stroke="#333" stroke-width="2"/>
  <text x="480" y="42" text-anchor="middle" font-size="10">Registry</text>
  <text x="480" y="55" text-anchor="middle" font-size="9">Hub / ECR / GCR</text>
  <ellipse cx="120" cy="160" rx="75" ry="25" fill="#e8f5e9" stroke="#333" stroke-width="2"/>
  <text x="120" y="157" text-anchor="middle" font-size="10">Volumes</text>
  <text x="120" y="170" text-anchor="middle" font-size="9">Persistent storage</text>
  <ellipse cx="480" cy="160" rx="75" ry="25" fill="#fff3e0" stroke="#333" stroke-width="2"/>
  <text x="480" y="157" text-anchor="middle" font-size="10">Networks</text>
  <text x="480" y="170" text-anchor="middle" font-size="9">Bridge / overlay</text>
  <line x1="250" y1="78" x2="190" y2="58" stroke="#333" stroke-width="1.5"/>
  <line x1="350" y1="78" x2="410" y2="58" stroke="#333" stroke-width="1.5"/>
  <line x1="250" y1="122" x2="190" y2="145" stroke="#333" stroke-width="1.5"/>
  <line x1="350" y1="122" x2="410" y2="145" stroke="#333" stroke-width="1.5"/>
</svg>

---

## Kubernetes Architecture

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="20" text-anchor="middle" font-size="12" font-weight="bold">Kubernetes Architecture</text>
  <rect x="20" y="40" width="150" height="60" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="95" y="58" text-anchor="middle" font-size="10" font-weight="bold">Control Plane</text>
  <text x="95" y="73" text-anchor="middle" font-size="9">API server, etcd</text>
  <text x="95" y="86" text-anchor="middle" font-size="9">Scheduler, controller</text>
  <rect x="225" y="40" width="150" height="60" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="58" text-anchor="middle" font-size="10" font-weight="bold">Worker Nodes</text>
  <text x="300" y="73" text-anchor="middle" font-size="9">Kubelet, kube-proxy</text>
  <text x="300" y="86" text-anchor="middle" font-size="9">Container runtime</text>
  <rect x="430" y="40" width="150" height="60" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="505" y="58" text-anchor="middle" font-size="10" font-weight="bold">Workloads</text>
  <text x="505" y="73" text-anchor="middle" font-size="9">Pods, Deployments</text>
  <text x="505" y="86" text-anchor="middle" font-size="9">Services, Ingress</text>
  <line x1="170" y1="70" x2="225" y2="70" stroke="#333" stroke-width="2" marker-end="url(#arrowd4_04_essential_devops_tools)"/>
  <line x1="375" y1="70" x2="430" y2="70" stroke="#333" stroke-width="2" marker-end="url(#arrowd4_04_essential_devops_tools)"/>
  <text x="300" y="135" text-anchor="middle" font-size="10" fill="#555">Declarative orchestration for containerized applications</text>
  <defs>
    <marker id="arrowd4_04_essential_devops_tools" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Container Orchestration

1. Pod management
1. Service discovery
1. Load balancing
1. Auto-scaling
1. Self-healing

---

## Infrastructure Tools

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <ellipse cx="300" cy="100" rx="55" ry="35" fill="#673ab7" stroke="#333" stroke-width="2"/>
  <text x="300" y="96" text-anchor="middle" font-size="11" fill="white">IaC</text>
  <text x="300" y="110" text-anchor="middle" font-size="10" fill="white">Tools</text>
  <ellipse cx="120" cy="45" rx="75" ry="25" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <text x="120" y="42" text-anchor="middle" font-size="10">Terraform</text>
  <text x="120" y="55" text-anchor="middle" font-size="9">Multi-cloud IaC</text>
  <ellipse cx="480" cy="45" rx="75" ry="25" fill="#f3e5f5" stroke="#333" stroke-width="2"/>
  <text x="480" y="42" text-anchor="middle" font-size="10">Ansible</text>
  <text x="480" y="55" text-anchor="middle" font-size="9">Agentless config mgmt</text>
  <ellipse cx="120" cy="160" rx="75" ry="25" fill="#e8f5e9" stroke="#333" stroke-width="2"/>
  <text x="120" y="157" text-anchor="middle" font-size="10">CloudFormation</text>
  <text x="120" y="170" text-anchor="middle" font-size="9">AWS native IaC</text>
  <ellipse cx="480" cy="160" rx="75" ry="25" fill="#fff3e0" stroke="#333" stroke-width="2"/>
  <text x="480" y="157" text-anchor="middle" font-size="10">Pulumi</text>
  <text x="480" y="170" text-anchor="middle" font-size="9">IaC in real languages</text>
  <line x1="250" y1="78" x2="190" y2="58" stroke="#333" stroke-width="1.5"/>
  <line x1="350" y1="78" x2="410" y2="58" stroke="#333" stroke-width="1.5"/>
  <line x1="250" y1="122" x2="190" y2="145" stroke="#333" stroke-width="1.5"/>
  <line x1="350" y1="122" x2="410" y2="145" stroke="#333" stroke-width="1.5"/>
</svg>

---

## Monitoring Stack

1. Data collection
1. Storage
1. Analysis
1. Visualization
1. Alerting

---

## Security Tools

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="20" text-anchor="middle" font-size="12" font-weight="bold">DevSecOps Tool Chain</text>
  <rect x="20" y="40" width="150" height="60" fill="#ffebee" stroke="#c00" stroke-width="2" rx="5"/>
  <text x="95" y="58" text-anchor="middle" font-size="10" font-weight="bold">SAST / DAST</text>
  <text x="95" y="73" text-anchor="middle" font-size="9">SonarQube, Snyk</text>
  <text x="95" y="86" text-anchor="middle" font-size="9">Code + dependency scan</text>
  <rect x="225" y="40" width="150" height="60" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="58" text-anchor="middle" font-size="10" font-weight="bold">Secrets Mgmt</text>
  <text x="300" y="73" text-anchor="middle" font-size="9">Vault, AWS Secrets</text>
  <text x="300" y="86" text-anchor="middle" font-size="9">Rotate + encrypt</text>
  <rect x="430" y="40" width="150" height="60" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="505" y="58" text-anchor="middle" font-size="10" font-weight="bold">Compliance</text>
  <text x="505" y="73" text-anchor="middle" font-size="9">OPA, Sentinel</text>
  <text x="505" y="86" text-anchor="middle" font-size="9">Policy as code</text>
  <line x1="170" y1="70" x2="225" y2="70" stroke="#333" stroke-width="2" marker-end="url(#arrowd6_04_essential_devops_tools)"/>
  <line x1="375" y1="70" x2="430" y2="70" stroke="#333" stroke-width="2" marker-end="url(#arrowd6_04_essential_devops_tools)"/>
  <text x="300" y="135" text-anchor="middle" font-size="10" fill="#555">Shift security left: integrate into every pipeline stage</text>
  <defs>
    <marker id="arrowd6_04_essential_devops_tools" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Testing Framework

1. Unit testing tools
1. Integration testing
1. Performance testing
1. Security testing
1. Acceptance testing

---

## Tool Integration

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="20" text-anchor="middle" font-size="12" font-weight="bold">Tool Integration Pattern</text>
  <rect x="20" y="40" width="150" height="60" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="95" y="58" text-anchor="middle" font-size="10" font-weight="bold">Source (Git)</text>
  <text x="95" y="73" text-anchor="middle" font-size="9">Commit triggers</text>
  <text x="95" y="86" text-anchor="middle" font-size="9">Webhooks + events</text>
  <rect x="225" y="40" width="150" height="60" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="58" text-anchor="middle" font-size="10" font-weight="bold">CI/CD (Jenkins)</text>
  <text x="300" y="73" text-anchor="middle" font-size="9">Build + test + deploy</text>
  <text x="300" y="86" text-anchor="middle" font-size="9">Artifact registry</text>
  <rect x="430" y="40" width="150" height="60" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="505" y="58" text-anchor="middle" font-size="10" font-weight="bold">Infra (K8s)</text>
  <text x="505" y="73" text-anchor="middle" font-size="9">Deploy + monitor</text>
  <text x="505" y="86" text-anchor="middle" font-size="9">Prometheus + Grafana</text>
  <line x1="170" y1="70" x2="225" y2="70" stroke="#333" stroke-width="2" marker-end="url(#arrowd7_04_essential_devops_tools)"/>
  <line x1="375" y1="70" x2="430" y2="70" stroke="#333" stroke-width="2" marker-end="url(#arrowd7_04_essential_devops_tools)"/>
  <text x="300" y="135" text-anchor="middle" font-size="10" fill="#555">End-to-end automation from commit to production</text>
  <defs>
    <marker id="arrowd7_04_essential_devops_tools" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Automation Tools

1. Build automation
1. Test automation
1. Deployment automation
1. Infrastructure automation
1. Monitoring automation

---

## Best Practices

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <ellipse cx="300" cy="100" rx="55" ry="35" fill="#673ab7" stroke="#333" stroke-width="2"/>
  <text x="300" y="96" text-anchor="middle" font-size="11" fill="white">Tool</text>
  <text x="300" y="110" text-anchor="middle" font-size="10" fill="white">Selection</text>
  <ellipse cx="120" cy="45" rx="75" ry="25" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <text x="120" y="42" text-anchor="middle" font-size="10">Open Source</text>
  <text x="120" y="55" text-anchor="middle" font-size="9">Community, flexibility</text>
  <ellipse cx="480" cy="45" rx="75" ry="25" fill="#f3e5f5" stroke="#333" stroke-width="2"/>
  <text x="480" y="42" text-anchor="middle" font-size="10">Integration</text>
  <text x="480" y="55" text-anchor="middle" font-size="9">API-first, plugins</text>
  <ellipse cx="120" cy="160" rx="75" ry="25" fill="#e8f5e9" stroke="#333" stroke-width="2"/>
  <text x="120" y="157" text-anchor="middle" font-size="10">Scalability</text>
  <text x="120" y="170" text-anchor="middle" font-size="9">Grow with team</text>
  <ellipse cx="480" cy="160" rx="75" ry="25" fill="#fff3e0" stroke="#333" stroke-width="2"/>
  <text x="480" y="157" text-anchor="middle" font-size="10">Standardize</text>
  <text x="480" y="170" text-anchor="middle" font-size="9">Reduce tool sprawl</text>
  <line x1="250" y1="78" x2="190" y2="58" stroke="#333" stroke-width="1.5"/>
  <line x1="350" y1="78" x2="410" y2="58" stroke="#333" stroke-width="1.5"/>
  <line x1="250" y1="122" x2="190" y2="145" stroke="#333" stroke-width="1.5"/>
  <line x1="350" y1="122" x2="410" y2="145" stroke="#333" stroke-width="1.5"/>
</svg>
