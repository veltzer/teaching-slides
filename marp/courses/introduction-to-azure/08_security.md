# Azure Security Services

## Security Components

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd0_07_security" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <!-- Azure AD / Entra ID -->
  <rect x="20" y="30" width="120" height="55" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="80" y="52" text-anchor="middle" font-size="11" font-weight="bold">Azure AD</text>
  <text x="80" y="72" text-anchor="middle" font-size="10">(Entra ID)</text>
  <!-- Key Vault -->
  <rect x="240" y="30" width="120" height="55" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="52" text-anchor="middle" font-size="11" font-weight="bold">Key Vault</text>
  <text x="300" y="72" text-anchor="middle" font-size="10">Secrets &amp; Keys</text>
  <!-- Defender for Cloud -->
  <rect x="460" y="30" width="120" height="55" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="520" y="52" text-anchor="middle" font-size="11" font-weight="bold">Defender</text>
  <text x="520" y="72" text-anchor="middle" font-size="10">for Cloud</text>
  <!-- Network Security -->
  <rect x="130" y="120" width="120" height="55" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="190" y="142" text-anchor="middle" font-size="11" font-weight="bold">Network</text>
  <text x="190" y="160" text-anchor="middle" font-size="10">NSG / Firewall</text>
  <!-- RBAC -->
  <rect x="350" y="120" width="120" height="55" fill="#ffebee" stroke="#333" stroke-width="2" rx="5"/>
  <text x="410" y="142" text-anchor="middle" font-size="11" font-weight="bold">RBAC</text>
  <text x="410" y="160" text-anchor="middle" font-size="10">Access Control</text>
  <!-- Connecting lines -->
  <line x1="140" y1="85" x2="240" y2="57" stroke="#333" stroke-width="1.5" marker-end="url(#arrowd0_07_security)"/>
  <line x1="360" y1="57" x2="460" y2="57" stroke="#333" stroke-width="1.5" marker-end="url(#arrowd0_07_security)"/>
  <line x1="80" y1="85" x2="150" y2="120" stroke="#333" stroke-width="1.5" marker-end="url(#arrowd0_07_security)"/>
  <line x1="300" y1="85" x2="390" y2="120" stroke="#333" stroke-width="1.5" marker-end="url(#arrowd0_07_security)"/>
</svg>

---

## Azure Active Directory
- Identity management
- Authentication
- Authorization
- Single sign-on
- Conditional access

---

## Identity Protection

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd1_07_security" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <!-- User -->
  <rect x="20" y="75" width="90" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="65" y="97" text-anchor="middle" font-size="11" font-weight="bold">User</text>
  <text x="65" y="113" text-anchor="middle" font-size="10">Sign-in</text>
  <!-- MFA -->
  <rect x="150" y="75" width="90" height="50" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="195" y="97" text-anchor="middle" font-size="11" font-weight="bold">MFA</text>
  <text x="195" y="113" text-anchor="middle" font-size="10">Verify</text>
  <!-- Conditional Access -->
  <rect x="280" y="75" width="110" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="335" y="93" text-anchor="middle" font-size="11" font-weight="bold">Conditional</text>
  <text x="335" y="110" text-anchor="middle" font-size="10">Access Policy</text>
  <!-- Access Granted -->
  <rect x="430" y="75" width="110" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="485" y="93" text-anchor="middle" font-size="11" font-weight="bold">Identity</text>
  <text x="485" y="110" text-anchor="middle" font-size="10">Protection</text>
  <!-- Flow arrows -->
  <line x1="110" y1="100" x2="148" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd1_07_security)"/>
  <line x1="240" y1="100" x2="278" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd1_07_security)"/>
  <line x1="390" y1="100" x2="428" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd1_07_security)"/>
  <!-- Labels -->
  <text x="300" y="30" text-anchor="middle" font-size="13" font-weight="bold" fill="#333">Identity Protection Flow</text>
  <text x="300" y="180" text-anchor="middle" font-size="10" fill="#666">Risk detection &#8594; Policy evaluation &#8594; Adaptive response</text>
</svg>

---

## Authentication Methods
1. Username/Password
1. Multi-factor authentication
1. Windows Hello
1. FIDO2 keys
1. Passwordless

---

## Role-Based Access Control
- Built-in roles
- Custom roles
- Scope levels
- Assignment types
- Inheritance

---

## Azure Key Vault
- Secret management
- Key management
- Certificate management
- Hardware security modules
- Access policies

---

## Data Encryption
- At-rest encryption
- In-transit encryption
- Client-side encryption
- Service encryption
- Key management

---

## Network Security

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd2_07_security" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <text x="300" y="20" text-anchor="middle" font-size="13" font-weight="bold" fill="#333">Network Security Layers</text>
  <!-- Internet -->
  <rect x="20" y="50" width="80" height="40" fill="#ffebee" stroke="#333" stroke-width="2" rx="5"/>
  <text x="60" y="75" text-anchor="middle" font-size="11" font-weight="bold">Internet</text>
  <!-- DDoS Protection -->
  <rect x="130" y="40" width="95" height="55" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="177" y="62" text-anchor="middle" font-size="11" font-weight="bold">DDoS</text>
  <text x="177" y="80" text-anchor="middle" font-size="10">Protection</text>
  <!-- WAF -->
  <rect x="255" y="40" width="95" height="55" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="302" y="62" text-anchor="middle" font-size="11" font-weight="bold">WAF</text>
  <text x="302" y="80" text-anchor="middle" font-size="10">App Gateway</text>
  <!-- NSG -->
  <rect x="380" y="40" width="95" height="55" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="427" y="62" text-anchor="middle" font-size="11" font-weight="bold">NSG</text>
  <text x="427" y="80" text-anchor="middle" font-size="10">Subnet Rules</text>
  <!-- Application -->
  <rect x="505" y="50" width="80" height="40" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="545" y="75" text-anchor="middle" font-size="11" font-weight="bold">App</text>
  <!-- Azure Firewall below -->
  <rect x="200" y="130" width="110" height="50" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="255" y="152" text-anchor="middle" font-size="11" font-weight="bold">Azure Firewall</text>
  <text x="255" y="168" text-anchor="middle" font-size="10">L3-L7 Filtering</text>
  <!-- Private Endpoint -->
  <rect x="350" y="130" width="110" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="405" y="152" text-anchor="middle" font-size="11" font-weight="bold">Private</text>
  <text x="405" y="168" text-anchor="middle" font-size="10">Endpoints</text>
  <!-- Arrows -->
  <line x1="100" y1="70" x2="128" y2="67" stroke="#333" stroke-width="1.5" marker-end="url(#arrowd2_07_security)"/>
  <line x1="225" y1="67" x2="253" y2="67" stroke="#333" stroke-width="1.5" marker-end="url(#arrowd2_07_security)"/>
  <line x1="350" y1="67" x2="378" y2="67" stroke="#333" stroke-width="1.5" marker-end="url(#arrowd2_07_security)"/>
  <line x1="475" y1="70" x2="503" y2="70" stroke="#333" stroke-width="1.5" marker-end="url(#arrowd2_07_security)"/>
  <line x1="302" y1="95" x2="275" y2="128" stroke="#333" stroke-width="1.5" marker-end="url(#arrowd2_07_security)"/>
  <line x1="427" y1="95" x2="415" y2="128" stroke="#333" stroke-width="1.5" marker-end="url(#arrowd2_07_security)"/>
</svg>

---

## Azure Firewall Features
- Application rules
- Network rules
- NAT rules
- Threat intelligence
- Logging

---

## DDoS Protection
- Basic protection
- Standard protection
- Attack analytics
- Metrics
- Alerting

---

## Web Application Firewall
- Rule sets
- Custom rules
- Bot protection
- Monitoring
- Integration

---

## Azure Security Center
- Security posture
- Threat protection
- Regulatory compliance
- Resource hygiene
- Recommendations

---

## Microsoft Defender for Cloud
- Threat detection
- Security alerts
- Investigation tools
- Automated response
- Integration

---

## Security Monitoring
- Log Analytics
- Security alerts
- Threat detection
- Audit logs
- Compliance reporting

---

## Compliance Management
- Regulatory standards
- Compliance scores
- Assessment tools
- Documentation
- Reporting

---

## Security Best Practices

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="20" text-anchor="middle" font-size="13" font-weight="bold" fill="#333">Security Best Practices Framework</text>
  <!-- Zero Trust -->
  <rect x="20" y="40" width="170" height="65" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="105" y="62" text-anchor="middle" font-size="12" font-weight="bold">Zero Trust</text>
  <text x="105" y="78" text-anchor="middle" font-size="10">Verify explicitly</text>
  <text x="105" y="93" text-anchor="middle" font-size="10">Least privilege access</text>
  <!-- Defense in Depth -->
  <rect x="215" y="40" width="170" height="65" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="62" text-anchor="middle" font-size="12" font-weight="bold">Defense in Depth</text>
  <text x="300" y="78" text-anchor="middle" font-size="10">Multiple layers</text>
  <text x="300" y="93" text-anchor="middle" font-size="10">Redundant controls</text>
  <!-- Shared Responsibility -->
  <rect x="410" y="40" width="170" height="65" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="495" y="62" text-anchor="middle" font-size="12" font-weight="bold">Shared Model</text>
  <text x="495" y="78" text-anchor="middle" font-size="10">Cloud provider duties</text>
  <text x="495" y="93" text-anchor="middle" font-size="10">Customer duties</text>
  <!-- Bottom row -->
  <rect x="70" y="130" width="140" height="50" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="140" y="152" text-anchor="middle" font-size="11" font-weight="bold">Encrypt Data</text>
  <text x="140" y="168" text-anchor="middle" font-size="10">At rest &amp; in transit</text>
  <rect x="240" y="130" width="140" height="50" fill="#ffebee" stroke="#333" stroke-width="2" rx="5"/>
  <text x="310" y="152" text-anchor="middle" font-size="11" font-weight="bold">Monitor &amp; Audit</text>
  <text x="310" y="168" text-anchor="middle" font-size="10">Logs &amp; alerts</text>
  <rect x="410" y="130" width="140" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="480" y="152" text-anchor="middle" font-size="11" font-weight="bold">Patch &amp; Update</text>
  <text x="480" y="168" text-anchor="middle" font-size="10">Stay current</text>
</svg>

---

## Data Classification
- Information types
- Sensitivity labels
- Retention policies
- Access policies
- Protection measures

---

## Secure DevOps
- Pipeline security
- Code scanning
- Secret management
- Container security
- Infrastructure as code

---

## Security Operations
- Incident response
- Threat hunting
- Vulnerability management
- Security updates
- Patch management

---

## Identity Governance
- Access reviews
- Entitlement management
- Privileged access
- Identity lifecycle
- Reporting

---

## Azure Policy
- Policy definitions
- Initiatives
- Assignments
- Compliance
- Remediation

---

## Security Assessments
- Vulnerability scanning
- Penetration testing
- Security reviews
- Compliance checks
- Risk assessment

---

## Incident Response
- Detection
- Investigation
- Containment
- Eradication
- Recovery

---

## Security Automation
- Playbooks
- Logic Apps
- Azure Functions
- Event Grid
- Automated responses

---

## Private Networking
- Private endpoints
- Service endpoints
- VNet integration
- Hybrid connectivity
- DNS security

---

## Cloud Security Posture
- Asset inventory
- Security controls
- Risk assessment
- Compliance status
- Recommendations

---

## Security Training
- Awareness programs
- Technical training
- Compliance training
- Incident response
- Best practices

---

## Security Documentation
- Policies
- Procedures
- Standards
- Guidelines
- Templates

---

## Security Metrics
- Key indicators
- Risk scores
- Compliance rates
- Incident metrics
- Performance metrics

---

## Future Security Trends
- Zero Trust evolution
- AI/ML in security
- Cloud security
- Identity innovation
- Compliance changes
