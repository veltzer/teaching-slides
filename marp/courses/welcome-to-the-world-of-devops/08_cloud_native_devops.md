# Cloud-Native DevOps
Modern cloud architecture and practices

---

## Serverless Architecture

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <ellipse cx="300" cy="100" rx="65" ry="40" fill="#673ab7" stroke="#333" stroke-width="2"/>
  <text x="300" y="96" text-anchor="middle" font-size="12" fill="white" font-weight="bold">Serverless</text>
  <text x="300" y="112" text-anchor="middle" font-size="10" fill="white">FaaS Platform</text>
  <ellipse cx="100" cy="50" rx="55" ry="28" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <text x="100" y="47" text-anchor="middle" font-size="10" font-weight="bold">Event Source</text>
  <text x="100" y="60" text-anchor="middle" font-size="9">API / Queue</text>
  <ellipse cx="500" cy="50" rx="55" ry="28" fill="#f3e5f5" stroke="#333" stroke-width="2"/>
  <text x="500" y="47" text-anchor="middle" font-size="10" font-weight="bold">Functions</text>
  <text x="500" y="60" text-anchor="middle" font-size="9">Lambda / Azure</text>
  <ellipse cx="100" cy="160" rx="55" ry="28" fill="#e8f5e9" stroke="#333" stroke-width="2"/>
  <text x="100" y="157" text-anchor="middle" font-size="10" font-weight="bold">Auto Scale</text>
  <text x="100" y="170" text-anchor="middle" font-size="9">Zero to N</text>
  <ellipse cx="500" cy="160" rx="55" ry="28" fill="#fff3e0" stroke="#333" stroke-width="2"/>
  <text x="500" y="157" text-anchor="middle" font-size="10" font-weight="bold">Pay-per-Use</text>
  <text x="500" y="170" text-anchor="middle" font-size="9">No Idle Cost</text>
  <line x1="245" y1="75" x2="150" y2="60" stroke="#333" stroke-width="2"/>
  <line x1="355" y1="75" x2="450" y2="60" stroke="#333" stroke-width="2"/>
  <line x1="245" y1="125" x2="150" y2="145" stroke="#333" stroke-width="2"/>
  <line x1="355" y1="125" x2="450" y2="145" stroke="#333" stroke-width="2"/>
</svg>

---

## Function as a Service

1. Event-driven execution
1. Automatic scaling
1. Pay-per-use
1. Zero maintenance
1. Quick deployment

---

## Serverless Benefits

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arr08a" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <rect x="20" y="30" width="130" height="55" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="85" y="52" text-anchor="middle" font-size="11" font-weight="bold">No Servers</text>
  <text x="85" y="68" text-anchor="middle" font-size="10">Zero Maintenance</text>
  <rect x="235" y="30" width="130" height="55" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="52" text-anchor="middle" font-size="11" font-weight="bold">Auto Scale</text>
  <text x="300" y="68" text-anchor="middle" font-size="10">Elastic Capacity</text>
  <rect x="450" y="30" width="130" height="55" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="515" y="52" text-anchor="middle" font-size="11" font-weight="bold">Cost Savings</text>
  <text x="515" y="68" text-anchor="middle" font-size="10">Pay per Request</text>
  <line x1="150" y1="57" x2="235" y2="57" stroke="#333" stroke-width="2" marker-end="url(#arr08a)"/>
  <line x1="365" y1="57" x2="450" y2="57" stroke="#333" stroke-width="2" marker-end="url(#arr08a)"/>
  <rect x="100" y="120" width="400" height="55" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="8" stroke-dasharray="4"/>
  <text x="300" y="143" text-anchor="middle" font-size="11" font-weight="bold">Developer Productivity</text>
  <text x="300" y="160" text-anchor="middle" font-size="10">Focus on Code - Fast Deploy - Built-in HA</text>
</svg>

---

## Microservices Architecture

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arr08b" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <rect x="20" y="20" width="110" height="70" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="75" y="42" text-anchor="middle" font-size="10" font-weight="bold">API Gateway</text>
  <text x="75" y="58" text-anchor="middle" font-size="9">Routing</text>
  <text x="75" y="72" text-anchor="middle" font-size="9">Auth</text>
  <rect x="180" y="10" width="100" height="45" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="230" y="30" text-anchor="middle" font-size="10" font-weight="bold">User Svc</text>
  <text x="230" y="44" text-anchor="middle" font-size="9">REST API</text>
  <rect x="180" y="65" width="100" height="45" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="230" y="85" text-anchor="middle" font-size="10" font-weight="bold">Order Svc</text>
  <text x="230" y="99" text-anchor="middle" font-size="9">gRPC</text>
  <rect x="340" y="10" width="100" height="45" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="390" y="30" text-anchor="middle" font-size="10" font-weight="bold">Payment Svc</text>
  <text x="390" y="44" text-anchor="middle" font-size="9">Async</text>
  <rect x="340" y="65" width="100" height="45" fill="#ffebee" stroke="#333" stroke-width="2" rx="5"/>
  <text x="390" y="85" text-anchor="middle" font-size="10" font-weight="bold">Notify Svc</text>
  <text x="390" y="99" text-anchor="middle" font-size="9">Events</text>
  <rect x="490" y="20" width="100" height="70" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="540" y="42" text-anchor="middle" font-size="10" font-weight="bold">Message Bus</text>
  <text x="540" y="58" text-anchor="middle" font-size="9">Kafka</text>
  <text x="540" y="72" text-anchor="middle" font-size="9">RabbitMQ</text>
  <line x1="130" y1="40" x2="180" y2="32" stroke="#333" stroke-width="1" marker-end="url(#arr08b)"/>
  <line x1="130" y1="65" x2="180" y2="80" stroke="#333" stroke-width="1" marker-end="url(#arr08b)"/>
  <line x1="280" y1="32" x2="340" y2="32" stroke="#333" stroke-width="1" marker-end="url(#arr08b)"/>
  <line x1="280" y1="87" x2="340" y2="87" stroke="#333" stroke-width="1" marker-end="url(#arr08b)"/>
  <line x1="440" y1="40" x2="490" y2="45" stroke="#333" stroke-width="1" marker-end="url(#arr08b)"/>
  <line x1="440" y1="87" x2="490" y2="70" stroke="#333" stroke-width="1" marker-end="url(#arr08b)"/>
  <rect x="100" y="130" width="400" height="50" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="8" stroke-dasharray="4"/>
  <text x="300" y="152" text-anchor="middle" font-size="11" font-weight="bold">Service Mesh Layer</text>
  <text x="300" y="168" text-anchor="middle" font-size="10">Discovery - Load Balance - Circuit Break - mTLS</text>
</svg>

---

## Service Components

1. Independent deployment
1. Loose coupling
1. API contracts
1. Data ownership
1. Service discovery

---

## Container Orchestration

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <ellipse cx="300" cy="100" rx="65" ry="40" fill="#673ab7" stroke="#333" stroke-width="2"/>
  <text x="300" y="96" text-anchor="middle" font-size="12" fill="white" font-weight="bold">Kubernetes</text>
  <text x="300" y="112" text-anchor="middle" font-size="10" fill="white">Control Plane</text>
  <ellipse cx="100" cy="50" rx="55" ry="28" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <text x="100" y="47" text-anchor="middle" font-size="10" font-weight="bold">Scheduling</text>
  <text x="100" y="60" text-anchor="middle" font-size="9">Pod Placement</text>
  <ellipse cx="500" cy="50" rx="55" ry="28" fill="#f3e5f5" stroke="#333" stroke-width="2"/>
  <text x="500" y="47" text-anchor="middle" font-size="10" font-weight="bold">Scaling</text>
  <text x="500" y="60" text-anchor="middle" font-size="9">HPA / VPA</text>
  <ellipse cx="100" cy="160" rx="55" ry="28" fill="#e8f5e9" stroke="#333" stroke-width="2"/>
  <text x="100" y="157" text-anchor="middle" font-size="10" font-weight="bold">Networking</text>
  <text x="100" y="170" text-anchor="middle" font-size="9">Services / Ingress</text>
  <ellipse cx="500" cy="160" rx="55" ry="28" fill="#fff3e0" stroke="#333" stroke-width="2"/>
  <text x="500" y="157" text-anchor="middle" font-size="10" font-weight="bold">Storage</text>
  <text x="500" y="170" text-anchor="middle" font-size="9">PV / PVC</text>
  <line x1="245" y1="75" x2="150" y2="60" stroke="#333" stroke-width="2"/>
  <line x1="355" y1="75" x2="450" y2="60" stroke="#333" stroke-width="2"/>
  <line x1="245" y1="125" x2="150" y2="145" stroke="#333" stroke-width="2"/>
  <line x1="355" y1="125" x2="450" y2="145" stroke="#333" stroke-width="2"/>
</svg>

---

## Cloud Platforms

1. AWS services
1. Azure platform
1. Google Cloud
1. Private cloud
1. Hybrid solutions

---

## Service Mesh

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arr08c" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <rect x="20" y="30" width="130" height="55" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="85" y="52" text-anchor="middle" font-size="11" font-weight="bold">Data Plane</text>
  <text x="85" y="68" text-anchor="middle" font-size="10">Envoy Proxies</text>
  <rect x="235" y="30" width="130" height="55" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="52" text-anchor="middle" font-size="11" font-weight="bold">Control Plane</text>
  <text x="300" y="68" text-anchor="middle" font-size="10">Istio / Linkerd</text>
  <rect x="450" y="30" width="130" height="55" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="515" y="52" text-anchor="middle" font-size="11" font-weight="bold">Observability</text>
  <text x="515" y="68" text-anchor="middle" font-size="10">Traces / Metrics</text>
  <line x1="150" y1="57" x2="235" y2="57" stroke="#333" stroke-width="2" marker-end="url(#arr08c)"/>
  <line x1="365" y1="57" x2="450" y2="57" stroke="#333" stroke-width="2" marker-end="url(#arr08c)"/>
  <rect x="100" y="120" width="400" height="55" fill="#fff3e0" stroke="#333" stroke-width="1" rx="8" stroke-dasharray="4"/>
  <text x="300" y="143" text-anchor="middle" font-size="11" font-weight="bold">Sidecar Pattern</text>
  <text x="300" y="160" text-anchor="middle" font-size="10">mTLS - Traffic Mgmt - Retries - Circuit Breaking</text>
</svg>

---

## Monitoring Strategy

1. Metrics collection
1. Distributed tracing
1. Log aggregation
1. Performance monitoring
1. Health checks

---

## Scalability Patterns

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <ellipse cx="300" cy="100" rx="65" ry="40" fill="#673ab7" stroke="#333" stroke-width="2"/>
  <text x="300" y="96" text-anchor="middle" font-size="12" fill="white" font-weight="bold">Scaling</text>
  <text x="300" y="112" text-anchor="middle" font-size="10" fill="white">Strategies</text>
  <ellipse cx="100" cy="50" rx="55" ry="28" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <text x="100" y="47" text-anchor="middle" font-size="10" font-weight="bold">Horizontal</text>
  <text x="100" y="60" text-anchor="middle" font-size="9">Add Replicas</text>
  <ellipse cx="500" cy="50" rx="55" ry="28" fill="#f3e5f5" stroke="#333" stroke-width="2"/>
  <text x="500" y="47" text-anchor="middle" font-size="10" font-weight="bold">Vertical</text>
  <text x="500" y="60" text-anchor="middle" font-size="9">Add Resources</text>
  <ellipse cx="100" cy="160" rx="55" ry="28" fill="#e8f5e9" stroke="#333" stroke-width="2"/>
  <text x="100" y="157" text-anchor="middle" font-size="10" font-weight="bold">Auto Scale</text>
  <text x="100" y="170" text-anchor="middle" font-size="9">HPA / KEDA</text>
  <ellipse cx="500" cy="160" rx="55" ry="28" fill="#fff3e0" stroke="#333" stroke-width="2"/>
  <text x="500" y="157" text-anchor="middle" font-size="10" font-weight="bold">Geo Dist</text>
  <text x="500" y="170" text-anchor="middle" font-size="9">Multi-Region</text>
  <line x1="245" y1="75" x2="150" y2="60" stroke="#333" stroke-width="2"/>
  <line x1="355" y1="75" x2="450" y2="60" stroke="#333" stroke-width="2"/>
  <line x1="245" y1="125" x2="150" y2="145" stroke="#333" stroke-width="2"/>
  <line x1="355" y1="125" x2="450" y2="145" stroke="#333" stroke-width="2"/>
</svg>

---

## Security Implementation

1. Identity management
1. Network policies
1. Secret management
1. Access control
1. Encryption

---

## Cost Optimization

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arr08d" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <rect x="20" y="30" width="130" height="55" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="85" y="52" text-anchor="middle" font-size="11" font-weight="bold">FinOps</text>
  <text x="85" y="68" text-anchor="middle" font-size="10">Cost Visibility</text>
  <rect x="235" y="30" width="130" height="55" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="52" text-anchor="middle" font-size="11" font-weight="bold">Right-Sizing</text>
  <text x="300" y="68" text-anchor="middle" font-size="10">Resource Fit</text>
  <rect x="450" y="30" width="130" height="55" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="515" y="52" text-anchor="middle" font-size="11" font-weight="bold">Spot / Reserve</text>
  <text x="515" y="68" text-anchor="middle" font-size="10">Pricing Models</text>
  <line x1="150" y1="57" x2="235" y2="57" stroke="#333" stroke-width="2" marker-end="url(#arr08d)"/>
  <line x1="365" y1="57" x2="450" y2="57" stroke="#333" stroke-width="2" marker-end="url(#arr08d)"/>
  <rect x="100" y="120" width="400" height="55" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="8" stroke-dasharray="4"/>
  <text x="300" y="143" text-anchor="middle" font-size="11" font-weight="bold">Cloud Cost Governance</text>
  <text x="300" y="160" text-anchor="middle" font-size="10">Budgets - Alerts - Tagging - Showback/Chargeback</text>
</svg>

---

## Best Practices

1. Infrastructure as code
1. Immutable infrastructure
1. Automatic scaling
1. Security first
1. Continuous monitoring

---

## Deployment Strategies

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <ellipse cx="300" cy="100" rx="65" ry="40" fill="#673ab7" stroke="#333" stroke-width="2"/>
  <text x="300" y="96" text-anchor="middle" font-size="12" fill="white" font-weight="bold">Deploy</text>
  <text x="300" y="112" text-anchor="middle" font-size="10" fill="white">Methods</text>
  <ellipse cx="100" cy="50" rx="55" ry="28" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <text x="100" y="47" text-anchor="middle" font-size="10" font-weight="bold">Blue-Green</text>
  <text x="100" y="60" text-anchor="middle" font-size="9">Instant Switch</text>
  <ellipse cx="500" cy="50" rx="55" ry="28" fill="#f3e5f5" stroke="#333" stroke-width="2"/>
  <text x="500" y="47" text-anchor="middle" font-size="10" font-weight="bold">Canary</text>
  <text x="500" y="60" text-anchor="middle" font-size="9">Gradual Rollout</text>
  <ellipse cx="100" cy="160" rx="55" ry="28" fill="#e8f5e9" stroke="#333" stroke-width="2"/>
  <text x="100" y="157" text-anchor="middle" font-size="10" font-weight="bold">Rolling</text>
  <text x="100" y="170" text-anchor="middle" font-size="9">Zero Downtime</text>
  <ellipse cx="500" cy="160" rx="55" ry="28" fill="#fff3e0" stroke="#333" stroke-width="2"/>
  <text x="500" y="157" text-anchor="middle" font-size="10" font-weight="bold">A/B Testing</text>
  <text x="500" y="170" text-anchor="middle" font-size="9">Feature Flags</text>
  <line x1="245" y1="75" x2="150" y2="60" stroke="#333" stroke-width="2"/>
  <line x1="355" y1="75" x2="450" y2="60" stroke="#333" stroke-width="2"/>
  <line x1="245" y1="125" x2="150" y2="145" stroke="#333" stroke-width="2"/>
  <line x1="355" y1="125" x2="450" y2="145" stroke="#333" stroke-width="2"/>
</svg>
