# Key DevOps Practices
Essential practices for successful DevOps implementation

---

## Infrastructure as Code (IaC)

1. Version-controlled infrastructure
1. Declarative configurations
1. Automated provisioning
1. Environment consistency
1. Reduced manual errors

---

## IaC Benefits

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <ellipse cx="300" cy="100" rx="60" ry="35" fill="#673ab7" stroke="#333" stroke-width="2"/>
  <text x="300" y="96" text-anchor="middle" font-size="11" fill="white">Infrastructure</text>
  <text x="300" y="110" text-anchor="middle" font-size="10" fill="white">as Code</text>
  <ellipse cx="120" cy="45" rx="75" ry="25" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <text x="120" y="42" text-anchor="middle" font-size="10">Reproducibility</text>
  <text x="120" y="55" text-anchor="middle" font-size="9">Identical environments</text>
  <ellipse cx="480" cy="45" rx="75" ry="25" fill="#f3e5f5" stroke="#333" stroke-width="2"/>
  <text x="480" y="42" text-anchor="middle" font-size="10">Version Control</text>
  <text x="480" y="55" text-anchor="middle" font-size="9">Track all changes</text>
  <ellipse cx="120" cy="160" rx="75" ry="25" fill="#e8f5e9" stroke="#333" stroke-width="2"/>
  <text x="120" y="157" text-anchor="middle" font-size="10">Speed</text>
  <text x="120" y="170" text-anchor="middle" font-size="9">Rapid provisioning</text>
  <ellipse cx="480" cy="160" rx="75" ry="25" fill="#fff3e0" stroke="#333" stroke-width="2"/>
  <text x="480" y="157" text-anchor="middle" font-size="10">Cost Savings</text>
  <text x="480" y="170" text-anchor="middle" font-size="9">Reduce manual effort</text>
  <line x1="250" y1="78" x2="190" y2="58" stroke="#333" stroke-width="1.5"/>
  <line x1="350" y1="78" x2="410" y2="58" stroke="#333" stroke-width="1.5"/>
  <line x1="250" y1="122" x2="190" y2="145" stroke="#333" stroke-width="1.5"/>
  <line x1="350" y1="122" x2="410" y2="145" stroke="#333" stroke-width="1.5"/>
</svg>

---

## Configuration Management

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="20" text-anchor="middle" font-size="12" font-weight="bold">Configuration Management Flow</text>
  <rect x="20" y="40" width="150" height="60" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="95" y="60" text-anchor="middle" font-size="10" font-weight="bold">Define State</text>
  <text x="95" y="75" text-anchor="middle" font-size="9">Declarative configs</text>
  <text x="95" y="88" text-anchor="middle" font-size="9">(YAML / HCL / JSON)</text>
  <rect x="225" y="40" width="150" height="60" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="60" text-anchor="middle" font-size="10" font-weight="bold">Apply Changes</text>
  <text x="300" y="75" text-anchor="middle" font-size="9">Ansible / Puppet / Chef</text>
  <text x="300" y="88" text-anchor="middle" font-size="9">Idempotent execution</text>
  <rect x="430" y="40" width="150" height="60" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="505" y="60" text-anchor="middle" font-size="10" font-weight="bold">Verify State</text>
  <text x="505" y="75" text-anchor="middle" font-size="9">Drift detection</text>
  <text x="505" y="88" text-anchor="middle" font-size="9">Compliance checks</text>
  <line x1="170" y1="70" x2="225" y2="70" stroke="#333" stroke-width="2" marker-end="url(#arrowd1_03_key_devops_practices)"/>
  <line x1="375" y1="70" x2="430" y2="70" stroke="#333" stroke-width="2" marker-end="url(#arrowd1_03_key_devops_practices)"/>
  <text x="300" y="135" text-anchor="middle" font-size="10" fill="#555">Desired state configuration ensures consistency across environments</text>
  <defs>
    <marker id="arrowd1_03_key_devops_practices" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Configuration Tools

1. Ansible - Agentless automation
1. Puppet - Configuration management
1. Chef - Infrastructure automation
1. SaltStack - Event-driven orchestration
1. Terraform - Infrastructure provisioning

---

## Monitoring Fundamentals

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="20" text-anchor="middle" font-size="12" font-weight="bold">Three Pillars of Monitoring</text>
  <rect x="20" y="40" width="150" height="60" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="95" y="58" text-anchor="middle" font-size="10" font-weight="bold">Metrics</text>
  <text x="95" y="73" text-anchor="middle" font-size="9">CPU, memory, latency</text>
  <text x="95" y="86" text-anchor="middle" font-size="9">Prometheus / Datadog</text>
  <rect x="225" y="40" width="150" height="60" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="58" text-anchor="middle" font-size="10" font-weight="bold">Logs</text>
  <text x="300" y="73" text-anchor="middle" font-size="9">Events, errors, audit</text>
  <text x="300" y="86" text-anchor="middle" font-size="9">ELK / Splunk</text>
  <rect x="430" y="40" width="150" height="60" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="505" y="58" text-anchor="middle" font-size="10" font-weight="bold">Traces</text>
  <text x="505" y="73" text-anchor="middle" font-size="9">Request flow, latency</text>
  <text x="505" y="86" text-anchor="middle" font-size="9">Jaeger / Zipkin</text>
  <line x1="170" y1="70" x2="225" y2="70" stroke="#333" stroke-width="2" marker-end="url(#arrowd2_03_key_devops_practices)"/>
  <line x1="375" y1="70" x2="430" y2="70" stroke="#333" stroke-width="2" marker-end="url(#arrowd2_03_key_devops_practices)"/>
  <text x="300" y="135" text-anchor="middle" font-size="10" fill="#555">Correlate across all three for full system visibility</text>
  <defs>
    <marker id="arrowd2_03_key_devops_practices" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Essential Metrics

1. System performance
1. Application health
1. User experience
1. Business metrics
1. Security indicators

---

## Logging Best Practices

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <ellipse cx="300" cy="100" rx="60" ry="35" fill="#673ab7" stroke="#333" stroke-width="2"/>
  <text x="300" y="96" text-anchor="middle" font-size="11" fill="white">Centralized</text>
  <text x="300" y="110" text-anchor="middle" font-size="10" fill="white">Logging</text>
  <ellipse cx="120" cy="45" rx="75" ry="25" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <text x="120" y="42" text-anchor="middle" font-size="10">Structured</text>
  <text x="120" y="55" text-anchor="middle" font-size="9">JSON format, context</text>
  <ellipse cx="480" cy="45" rx="75" ry="25" fill="#f3e5f5" stroke="#333" stroke-width="2"/>
  <text x="480" y="42" text-anchor="middle" font-size="10">Aggregated</text>
  <text x="480" y="55" text-anchor="middle" font-size="9">ELK, Fluentd, Loki</text>
  <ellipse cx="120" cy="160" rx="75" ry="25" fill="#e8f5e9" stroke="#333" stroke-width="2"/>
  <text x="120" y="157" text-anchor="middle" font-size="10">Searchable</text>
  <text x="120" y="170" text-anchor="middle" font-size="9">Index, query, filter</text>
  <ellipse cx="480" cy="160" rx="75" ry="25" fill="#fff3e0" stroke="#333" stroke-width="2"/>
  <text x="480" y="157" text-anchor="middle" font-size="10">Retained</text>
  <text x="480" y="170" text-anchor="middle" font-size="9">Rotation, compliance</text>
  <line x1="250" y1="78" x2="190" y2="58" stroke="#333" stroke-width="1.5"/>
  <line x1="350" y1="78" x2="410" y2="58" stroke="#333" stroke-width="1.5"/>
  <line x1="250" y1="122" x2="190" y2="145" stroke="#333" stroke-width="1.5"/>
  <line x1="350" y1="122" x2="410" y2="145" stroke="#333" stroke-width="1.5"/>
</svg>

---

## Monitoring Tools

1. Prometheus - Metrics collection
1. Grafana - Visualization
1. ELK Stack - Log management
1. Datadog - Application monitoring
1. Nagios - Infrastructure monitoring

---

## Observability Components

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="20" text-anchor="middle" font-size="12" font-weight="bold">Three Pillars of Observability</text>
  <rect x="20" y="40" width="150" height="60" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="95" y="58" text-anchor="middle" font-size="10" font-weight="bold">Metrics</text>
  <text x="95" y="73" text-anchor="middle" font-size="9">Quantitative measures</text>
  <text x="95" y="86" text-anchor="middle" font-size="9">Gauges, counters, hist.</text>
  <rect x="225" y="40" width="150" height="60" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="58" text-anchor="middle" font-size="10" font-weight="bold">Logs</text>
  <text x="300" y="73" text-anchor="middle" font-size="9">Discrete events</text>
  <text x="300" y="86" text-anchor="middle" font-size="9">Structured, contextual</text>
  <rect x="430" y="40" width="150" height="60" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="505" y="58" text-anchor="middle" font-size="10" font-weight="bold">Traces</text>
  <text x="505" y="73" text-anchor="middle" font-size="9">Distributed requests</text>
  <text x="505" y="86" text-anchor="middle" font-size="9">End-to-end visibility</text>
  <line x1="170" y1="70" x2="225" y2="70" stroke="#333" stroke-width="2" marker-end="url(#arrowd4_03_key_devops_practices)"/>
  <line x1="375" y1="70" x2="430" y2="70" stroke="#333" stroke-width="2" marker-end="url(#arrowd4_03_key_devops_practices)"/>
  <text x="300" y="135" text-anchor="middle" font-size="10" fill="#555">Together they answer: what, why, and where</text>
  <defs>
    <marker id="arrowd4_03_key_devops_practices" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Alert Management

1. Define thresholds
1. Set priority levels
1. Establish response plans
1. Document procedures
1. Review and improve

---

## Incident Response

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="20" text-anchor="middle" font-size="12" font-weight="bold">Incident Response Lifecycle</text>
  <rect x="20" y="40" width="150" height="60" fill="#ffebee" stroke="#c00" stroke-width="2" rx="5"/>
  <text x="95" y="58" text-anchor="middle" font-size="10" font-weight="bold">Detect + Alert</text>
  <text x="95" y="73" text-anchor="middle" font-size="9">Automated monitoring</text>
  <text x="95" y="86" text-anchor="middle" font-size="9">PagerDuty / OpsGenie</text>
  <rect x="225" y="40" width="150" height="60" fill="#fff3e0" stroke="#e65100" stroke-width="2" rx="5"/>
  <text x="300" y="58" text-anchor="middle" font-size="10" font-weight="bold">Triage + Mitigate</text>
  <text x="300" y="73" text-anchor="middle" font-size="9">Incident commander</text>
  <text x="300" y="86" text-anchor="middle" font-size="9">Rollback / hotfix</text>
  <rect x="430" y="40" width="150" height="60" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2" rx="5"/>
  <text x="505" y="58" text-anchor="middle" font-size="10" font-weight="bold">Review + Learn</text>
  <text x="505" y="73" text-anchor="middle" font-size="9">Blameless postmortem</text>
  <text x="505" y="86" text-anchor="middle" font-size="9">Preventive actions</text>
  <line x1="170" y1="70" x2="225" y2="70" stroke="#333" stroke-width="2" marker-end="url(#arrowd5_03_key_devops_practices)"/>
  <line x1="375" y1="70" x2="430" y2="70" stroke="#333" stroke-width="2" marker-end="url(#arrowd5_03_key_devops_practices)"/>
  <text x="300" y="135" text-anchor="middle" font-size="10" fill="#555">Reduce MTTR through well-defined response processes</text>
  <defs>
    <marker id="arrowd5_03_key_devops_practices" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Security Integration

1. Code scanning
1. Dependency checks
1. Compliance monitoring
1. Access controls
1. Audit logging

---

## Automation Strategy

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <ellipse cx="300" cy="100" rx="60" ry="35" fill="#673ab7" stroke="#333" stroke-width="2"/>
  <text x="300" y="96" text-anchor="middle" font-size="11" fill="white">Automation</text>
  <text x="300" y="110" text-anchor="middle" font-size="10" fill="white">Strategy</text>
  <ellipse cx="120" cy="45" rx="75" ry="25" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <text x="120" y="42" text-anchor="middle" font-size="10">CI/CD Pipelines</text>
  <text x="120" y="55" text-anchor="middle" font-size="9">Build, test, deploy</text>
  <ellipse cx="480" cy="45" rx="75" ry="25" fill="#f3e5f5" stroke="#333" stroke-width="2"/>
  <text x="480" y="42" text-anchor="middle" font-size="10">Infrastructure</text>
  <text x="480" y="55" text-anchor="middle" font-size="9">Provision + configure</text>
  <ellipse cx="120" cy="160" rx="75" ry="25" fill="#e8f5e9" stroke="#333" stroke-width="2"/>
  <text x="120" y="157" text-anchor="middle" font-size="10">Testing</text>
  <text x="120" y="170" text-anchor="middle" font-size="9">Unit, integration, E2E</text>
  <ellipse cx="480" cy="160" rx="75" ry="25" fill="#fff3e0" stroke="#333" stroke-width="2"/>
  <text x="480" y="157" text-anchor="middle" font-size="10">Monitoring</text>
  <text x="480" y="170" text-anchor="middle" font-size="9">Alerts + remediation</text>
  <line x1="250" y1="78" x2="190" y2="58" stroke="#333" stroke-width="1.5"/>
  <line x1="350" y1="78" x2="410" y2="58" stroke="#333" stroke-width="1.5"/>
  <line x1="250" y1="122" x2="190" y2="145" stroke="#333" stroke-width="1.5"/>
  <line x1="350" y1="122" x2="410" y2="145" stroke="#333" stroke-width="1.5"/>
</svg>

---

## Implementation Steps

1. Assess current state
1. Define objectives
1. Select tools
1. Start small
1. Scale gradually

---

## Common Challenges

1. Tool complexity
1. Skill gaps
1. Resource constraints
1. Legacy systems
1. Resistance to change

---

## Best Practices

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="20" text-anchor="middle" font-size="12" font-weight="bold">DevOps Best Practices</text>
  <rect x="20" y="40" width="150" height="60" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="95" y="58" text-anchor="middle" font-size="10" font-weight="bold">Automate First</text>
  <text x="95" y="73" text-anchor="middle" font-size="9">Eliminate toil</text>
  <text x="95" y="86" text-anchor="middle" font-size="9">Repeatable pipelines</text>
  <rect x="225" y="40" width="150" height="60" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="58" text-anchor="middle" font-size="10" font-weight="bold">Measure Always</text>
  <text x="300" y="73" text-anchor="middle" font-size="9">DORA metrics</text>
  <text x="300" y="86" text-anchor="middle" font-size="9">Data-driven decisions</text>
  <rect x="430" y="40" width="150" height="60" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="505" y="58" text-anchor="middle" font-size="10" font-weight="bold">Iterate Fast</text>
  <text x="505" y="73" text-anchor="middle" font-size="9">Small batch sizes</text>
  <text x="505" y="86" text-anchor="middle" font-size="9">Continuous feedback</text>
  <line x1="170" y1="70" x2="225" y2="70" stroke="#333" stroke-width="2" marker-end="url(#arrowd7_03_key_devops_practices)"/>
  <line x1="375" y1="70" x2="430" y2="70" stroke="#333" stroke-width="2" marker-end="url(#arrowd7_03_key_devops_practices)"/>
  <text x="300" y="135" text-anchor="middle" font-size="10" fill="#555">Build quality in from the start, not bolted on after</text>
  <defs>
    <marker id="arrowd7_03_key_devops_practices" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Success Metrics

1. Deployment frequency
1. Lead time for changes
1. Mean time to recovery
1. Change failure rate
1. Team velocity
