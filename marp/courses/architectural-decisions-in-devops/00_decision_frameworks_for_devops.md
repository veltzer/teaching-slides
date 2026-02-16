# Decision Frameworks for DevOps
A systematic approach to making and documenting architectural decisions

---

## Why Decisions Matter in DevOps

- DevOps is not just tools and automation; it is a series of decisions
- Poor decisions compound over time, creating technical debt
- Good decisions accelerate delivery and reduce operational burden
- The cost of reversing a bad decision grows exponentially with time

---

## What We Will Cover

1. What makes a decision "architectural" in DevOps
1. Reversibility and cost of change
1. Organizational context and Conway's Law
1. Evaluating tradeoffs systematically
1. Documenting decisions with Architecture Decision Records (`ADRs`)

---

## What Is an Architectural Decision?

- A decision that shapes the structure of a system or organization
- Has long-lasting consequences that are difficult to reverse
- Affects multiple teams, services, or components
- Constrains future choices and design directions

---

## Architectural vs Tactical Decisions

<svg width="650" height="280" xmlns="http://www.w3.org/2000/svg">
  <rect x="30" y="30" width="280" height="220" fill="#e3f2fd" stroke="#1565c0" stroke-width="2" rx="8"/>
  <text x="170" y="60" text-anchor="middle" font-size="16" font-weight="bold" fill="#1565c0">Architectural</text>
  <text x="170" y="90" text-anchor="middle" font-size="12">Choose Kubernetes vs ECS</text>
  <text x="170" y="115" text-anchor="middle" font-size="12">Monorepo vs polyrepo</text>
  <text x="170" y="140" text-anchor="middle" font-size="12">CI/CD platform selection</text>
  <text x="170" y="165" text-anchor="middle" font-size="12">Service mesh adoption</text>
  <text x="170" y="195" text-anchor="middle" font-size="11" fill="#555">High impact, hard to reverse</text>
  <text x="170" y="215" text-anchor="middle" font-size="11" fill="#555">Cross-team scope</text>
  <rect x="340" y="30" width="280" height="220" fill="#fff3e0" stroke="#e65100" stroke-width="2" rx="8"/>
  <text x="480" y="60" text-anchor="middle" font-size="16" font-weight="bold" fill="#e65100">Tactical</text>
  <text x="480" y="90" text-anchor="middle" font-size="12">Bump library version</text>
  <text x="480" y="115" text-anchor="middle" font-size="12">Add a linting rule</text>
  <text x="480" y="140" text-anchor="middle" font-size="12">Choose test fixture format</text>
  <text x="480" y="165" text-anchor="middle" font-size="12">Rename a variable</text>
  <text x="480" y="195" text-anchor="middle" font-size="11" fill="#555">Low impact, easy to reverse</text>
  <text x="480" y="215" text-anchor="middle" font-size="11" fill="#555">Single-team scope</text>
</svg>

---

## The Litmus Test for Architectural Decisions

- **Scope**: Does it affect more than one team or service?
- **Durability**: Will it still matter in six months?
- **Reversibility**: Would reversing it require significant effort?
- **Cost**: Does it involve meaningful investment of time or money?
- If two or more answers are "yes," the decision is likely architectural

---

## Examples of Architectural Decisions in DevOps

- Which cloud provider to use (`AWS`, `GCP`, `Azure`)
- Container orchestration strategy (`Kubernetes`, `Nomad`, `ECS`)
- `GitOps` vs imperative deployment model
- Branching strategy (`trunk-based`, `GitFlow`)
- Observability stack selection (`Prometheus`, `Datadog`, `Grafana`)
- Secrets management approach (`Vault`, `SOPS`, `AWS Secrets Manager`)

---

## Examples of Non-Architectural Decisions

- Which `YAML` formatter to use in a single repo
- The naming convention for a specific microservice's internal modules
- Choice of a specific test framework for one team
- Order of steps within a single pipeline stage
- These are important but do not require formal frameworks

---

## The Decision Spectrum

<svg width="650" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="spectrum_grad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#4caf50;stop-opacity:1" />
      <stop offset="50%" style="stop-color:#ff9800;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#f44336;stop-opacity:1" />
    </linearGradient>
  </defs>
  <rect x="50" y="60" width="550" height="40" rx="20" fill="url(#spectrum_grad)" stroke="#333" stroke-width="1"/>
  <text x="100" y="50" text-anchor="middle" font-size="12" font-weight="bold" fill="#4caf50">Trivial</text>
  <text x="325" y="50" text-anchor="middle" font-size="12" font-weight="bold" fill="#e65100">Significant</text>
  <text x="550" y="50" text-anchor="middle" font-size="12" font-weight="bold" fill="#f44336">Architectural</text>
  <text x="100" y="130" text-anchor="middle" font-size="11">Decide alone</text>
  <text x="100" y="148" text-anchor="middle" font-size="11">in minutes</text>
  <text x="325" y="130" text-anchor="middle" font-size="11">Discuss with</text>
  <text x="325" y="148" text-anchor="middle" font-size="11">the team</text>
  <text x="550" y="130" text-anchor="middle" font-size="11">Formal evaluation</text>
  <text x="550" y="148" text-anchor="middle" font-size="11">and documentation</text>
  <line x1="100" y1="100" x2="100" y2="118" stroke="#333" stroke-width="1"/>
  <line x1="325" y1="100" x2="325" y2="118" stroke="#333" stroke-width="1"/>
  <line x1="550" y1="100" x2="550" y2="118" stroke="#333" stroke-width="1"/>
</svg>

---

## Reversibility: The Key Dimension

- Jeff Bezos distinguishes between "one-way doors" and "two-way doors"
- **One-way door**: Difficult or impossible to reverse once taken
    - Choosing a database engine for production data
    - Selecting a cloud provider with deep integration
- **Two-way door**: Easy to reverse if the outcome is poor
    - Trying a new linting tool
    - Switching from one log format to another

---

## The Reversibility Spectrum

<svg width="650" height="260" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrow_rev" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <line x1="80" y1="220" x2="600" y2="220" stroke="#333" stroke-width="2" marker-end="url(#arrow_rev)"/>
  <line x1="80" y1="220" x2="80" y2="30" stroke="#333" stroke-width="2" marker-end="url(#arrow_rev)"/>
  <text x="340" y="250" text-anchor="middle" font-size="12" font-weight="bold">Difficulty to Reverse</text>
  <text x="40" y="125" text-anchor="middle" font-size="12" font-weight="bold" transform="rotate(-90, 40, 125)">Cost of Change</text>
  <circle cx="150" cy="190" r="20" fill="#4caf50" opacity="0.8"/>
  <text x="150" y="195" text-anchor="middle" font-size="9" fill="white">Config</text>
  <text x="150" y="205" text-anchor="middle" font-size="9" fill="white">flag</text>
  <circle cx="240" cy="165" r="22" fill="#8bc34a" opacity="0.8"/>
  <text x="240" y="162" text-anchor="middle" font-size="9" fill="white">CI tool</text>
  <text x="240" y="173" text-anchor="middle" font-size="9" fill="white">swap</text>
  <circle cx="350" cy="120" r="25" fill="#ff9800" opacity="0.8"/>
  <text x="350" y="117" text-anchor="middle" font-size="9" fill="white">Container</text>
  <text x="350" y="128" text-anchor="middle" font-size="9" fill="white">runtime</text>
  <circle cx="460" cy="80" r="28" fill="#f44336" opacity="0.8"/>
  <text x="460" y="77" text-anchor="middle" font-size="9" fill="white">Cloud</text>
  <text x="460" y="88" text-anchor="middle" font-size="9" fill="white">provider</text>
  <circle cx="550" cy="55" r="30" fill="#b71c1c" opacity="0.8"/>
  <text x="550" y="52" text-anchor="middle" font-size="9" fill="white">Database</text>
  <text x="550" y="63" text-anchor="middle" font-size="9" fill="white">engine</text>
</svg>

---

## Cost of Change Over Time

- A decision made early in a project is cheap to change
- The same decision becomes expensive once systems depend on it
- Data migration, retraining, contract renegotiation all add cost
- This is why early architectural thinking pays off

---

## Strategies for Reducing Irreversibility

- **Abstraction layers**: Hide implementation behind interfaces
- **Feature flags**: Toggle new behaviors without redeployment
- **Strangler fig pattern**: Gradually replace old systems
- **Infrastructure as Code**: Recreate environments from scratch
- **Containerization**: Decouple applications from infrastructure

---

## Deferring Decisions Responsibly

- Not every decision needs to be made on day one
- "The Last Responsible Moment" principle from Lean
- Defer decisions until you have enough information
- But do not defer so long that options close
- Document what you are deferring and why

---

## Conway's Law: The Organizational Force

- "Organizations which design systems are constrained to produce designs which are copies of the communication structures of these organizations" -- Melvin Conway, 1967
- Your architecture will mirror your team structure
- This is not optional; it is a force of nature

---

## Conway's Law Visualized

<svg width="650" height="300" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrow_conway" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#555"/>
    </marker>
  </defs>
  <text x="160" y="25" text-anchor="middle" font-size="14" font-weight="bold">Org Structure</text>
  <text x="490" y="25" text-anchor="middle" font-size="14" font-weight="bold">System Architecture</text>
  <rect x="80" y="40" width="160" height="40" fill="#e3f2fd" stroke="#1565c0" stroke-width="2" rx="5"/>
  <text x="160" y="65" text-anchor="middle" font-size="12">Frontend Team</text>
  <rect x="80" y="100" width="160" height="40" fill="#f3e5f5" stroke="#7b1fa2" stroke-width="2" rx="5"/>
  <text x="160" y="125" text-anchor="middle" font-size="12">Backend Team</text>
  <rect x="80" y="160" width="160" height="40" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2" rx="5"/>
  <text x="160" y="185" text-anchor="middle" font-size="12">Data Team</text>
  <rect x="80" y="220" width="160" height="40" fill="#fff3e0" stroke="#e65100" stroke-width="2" rx="5"/>
  <text x="160" y="245" text-anchor="middle" font-size="12">Infra Team</text>
  <rect x="410" y="40" width="160" height="40" fill="#e3f2fd" stroke="#1565c0" stroke-width="2" rx="5"/>
  <text x="490" y="65" text-anchor="middle" font-size="12">UI Service</text>
  <rect x="410" y="100" width="160" height="40" fill="#f3e5f5" stroke="#7b1fa2" stroke-width="2" rx="5"/>
  <text x="490" y="125" text-anchor="middle" font-size="12">API Service</text>
  <rect x="410" y="160" width="160" height="40" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2" rx="5"/>
  <text x="490" y="185" text-anchor="middle" font-size="12">Data Pipeline</text>
  <rect x="410" y="220" width="160" height="40" fill="#fff3e0" stroke="#e65100" stroke-width="2" rx="5"/>
  <text x="490" y="245" text-anchor="middle" font-size="12">Infrastructure</text>
  <line x1="240" y1="60" x2="410" y2="60" stroke="#555" stroke-width="1.5" stroke-dasharray="6,3" marker-end="url(#arrow_conway)"/>
  <line x1="240" y1="120" x2="410" y2="120" stroke="#555" stroke-width="1.5" stroke-dasharray="6,3" marker-end="url(#arrow_conway)"/>
  <line x1="240" y1="180" x2="410" y2="180" stroke="#555" stroke-width="1.5" stroke-dasharray="6,3" marker-end="url(#arrow_conway)"/>
  <line x1="240" y1="240" x2="410" y2="240" stroke="#555" stroke-width="1.5" stroke-dasharray="6,3" marker-end="url(#arrow_conway)"/>
  <text x="325" y="290" text-anchor="middle" font-size="11" fill="#555">Teams mirror services 1:1</text>
</svg>

---

## Conway's Law in Practice

- A company with separate frontend and backend teams will produce a system with a clear frontend/backend split
- A company with teams organized by geography will produce a distributed system
- A company with a single platform team will produce a monolithic platform
- This applies to `CI/CD` pipelines, monitoring, and infrastructure too

---

## The Inverse Conway Maneuver

- Deliberately structure teams to produce the desired architecture
- If you want microservices, create small autonomous teams
- If you want a unified platform, create cross-functional teams
- This is a strategic tool for DevOps leaders
- Pioneered by ThoughtWorks and widely adopted in the industry

---

## Team Topologies and Decision Authority

- **Stream-aligned teams**: Own decisions for their domain end-to-end
- **Platform teams**: Own decisions about shared infrastructure
- **Enabling teams**: Help other teams make better decisions
- **Complicated-subsystem teams**: Own decisions for specialized components
- Decision authority should follow team topology

---

## Cognitive Load and Decision Boundaries

- Teams can only handle a finite amount of cognitive load
- Too many decisions slow teams down and reduce quality
- Architectural decisions should minimize cross-team coordination
- Platforms should absorb complexity and simplify choices for stream teams
- Define clear decision boundaries between teams

---

## Evaluating Tradeoffs: The DACI Framework

<svg width="650" height="250" xmlns="http://www.w3.org/2000/svg">
  <rect x="30" y="30" width="140" height="80" fill="#1565c0" stroke="#0d47a1" stroke-width="2" rx="8"/>
  <text x="100" y="60" text-anchor="middle" font-size="14" font-weight="bold" fill="white">Driver</text>
  <text x="100" y="80" text-anchor="middle" font-size="10" fill="#bbdefb">Owns the process</text>
  <text x="100" y="95" text-anchor="middle" font-size="10" fill="#bbdefb">Gathers input</text>
  <rect x="185" y="30" width="140" height="80" fill="#2e7d32" stroke="#1b5e20" stroke-width="2" rx="8"/>
  <text x="255" y="60" text-anchor="middle" font-size="14" font-weight="bold" fill="white">Approver</text>
  <text x="255" y="80" text-anchor="middle" font-size="10" fill="#c8e6c9">Makes final call</text>
  <text x="255" y="95" text-anchor="middle" font-size="10" fill="#c8e6c9">One person only</text>
  <rect x="340" y="30" width="140" height="80" fill="#e65100" stroke="#bf360c" stroke-width="2" rx="8"/>
  <text x="410" y="60" text-anchor="middle" font-size="14" font-weight="bold" fill="white">Contributors</text>
  <text x="410" y="80" text-anchor="middle" font-size="10" fill="#ffe0b2">Provide expertise</text>
  <text x="410" y="95" text-anchor="middle" font-size="10" fill="#ffe0b2">Share knowledge</text>
  <rect x="495" y="30" width="140" height="80" fill="#7b1fa2" stroke="#4a148c" stroke-width="2" rx="8"/>
  <text x="565" y="60" text-anchor="middle" font-size="14" font-weight="bold" fill="white">Informed</text>
  <text x="565" y="80" text-anchor="middle" font-size="10" fill="#e1bee7">Notified of result</text>
  <text x="565" y="95" text-anchor="middle" font-size="10" fill="#e1bee7">No input needed</text>
  <text x="325" y="160" text-anchor="middle" font-size="12" fill="#333">Assign exactly one Approver per decision to avoid deadlock</text>
  <text x="325" y="180" text-anchor="middle" font-size="12" fill="#333">The Driver is not necessarily the Approver</text>
</svg>

---

## Decision Matrix: Weighted Criteria

- List all options as columns
- List evaluation criteria as rows
- Assign weights to each criterion (importance)
- Score each option against each criterion
- Multiply scores by weights and sum for final ranking

---

## Decision Matrix Example

<svg width="650" height="280" xmlns="http://www.w3.org/2000/svg">
  <rect x="30" y="20" width="590" height="240" fill="#fafafa" stroke="#ccc" stroke-width="1" rx="4"/>
  <line x1="30" y1="60" x2="620" y2="60" stroke="#333" stroke-width="2"/>
  <line x1="170" y1="20" x2="170" y2="260" stroke="#ccc" stroke-width="1"/>
  <line x1="280" y1="20" x2="280" y2="260" stroke="#ccc" stroke-width="1"/>
  <line x1="390" y1="20" x2="390" y2="260" stroke="#ccc" stroke-width="1"/>
  <line x1="500" y1="20" x2="500" y2="260" stroke="#ccc" stroke-width="1"/>
  <text x="100" y="45" text-anchor="middle" font-size="12" font-weight="bold">Criterion (Weight)</text>
  <text x="225" y="45" text-anchor="middle" font-size="12" font-weight="bold">Jenkins</text>
  <text x="335" y="45" text-anchor="middle" font-size="12" font-weight="bold">GitLab CI</text>
  <text x="445" y="45" text-anchor="middle" font-size="12" font-weight="bold">GitHub Actions</text>
  <text x="560" y="45" text-anchor="middle" font-size="12" font-weight="bold">ArgoCD</text>
  <text x="100" y="90" text-anchor="middle" font-size="11">Ease of use (3)</text>
  <text x="225" y="90" text-anchor="middle" font-size="11">2 (6)</text>
  <text x="335" y="90" text-anchor="middle" font-size="11">4 (12)</text>
  <text x="445" y="90" text-anchor="middle" font-size="11">5 (15)</text>
  <text x="560" y="90" text-anchor="middle" font-size="11">3 (9)</text>
  <line x1="30" y1="105" x2="620" y2="105" stroke="#eee" stroke-width="1"/>
  <text x="100" y="130" text-anchor="middle" font-size="11">Extensibility (2)</text>
  <text x="225" y="130" text-anchor="middle" font-size="11">5 (10)</text>
  <text x="335" y="130" text-anchor="middle" font-size="11">4 (8)</text>
  <text x="445" y="130" text-anchor="middle" font-size="11">4 (8)</text>
  <text x="560" y="130" text-anchor="middle" font-size="11">3 (6)</text>
  <line x1="30" y1="145" x2="620" y2="145" stroke="#eee" stroke-width="1"/>
  <text x="100" y="170" text-anchor="middle" font-size="11">GitOps support (4)</text>
  <text x="225" y="170" text-anchor="middle" font-size="11">2 (8)</text>
  <text x="335" y="170" text-anchor="middle" font-size="11">3 (12)</text>
  <text x="445" y="170" text-anchor="middle" font-size="11">3 (12)</text>
  <text x="560" y="170" text-anchor="middle" font-size="11">5 (20)</text>
  <line x1="30" y1="185" x2="620" y2="185" stroke="#eee" stroke-width="1"/>
  <text x="100" y="210" text-anchor="middle" font-size="11">Cost (3)</text>
  <text x="225" y="210" text-anchor="middle" font-size="11">4 (12)</text>
  <text x="335" y="210" text-anchor="middle" font-size="11">3 (9)</text>
  <text x="445" y="210" text-anchor="middle" font-size="11">4 (12)</text>
  <text x="560" y="210" text-anchor="middle" font-size="11">5 (15)</text>
  <line x1="30" y1="225" x2="620" y2="225" stroke="#333" stroke-width="1"/>
  <text x="100" y="250" text-anchor="middle" font-size="12" font-weight="bold">Total</text>
  <text x="225" y="250" text-anchor="middle" font-size="12" font-weight="bold">36</text>
  <text x="335" y="250" text-anchor="middle" font-size="12" font-weight="bold">41</text>
  <text x="445" y="250" text-anchor="middle" font-size="12" font-weight="bold" fill="#2e7d32">47</text>
  <text x="560" y="250" text-anchor="middle" font-size="12" font-weight="bold" fill="#1565c0">50</text>
</svg>

---

## Pitfalls of Decision Matrices

- Garbage in, garbage out: biased weights produce biased results
- False precision: a score of 4 vs 5 may not be meaningful
- Missing criteria: what you forget to list can matter most
- Use as a discussion tool, not an oracle
- Always validate the result against intuition and experience

---

## The RAPID Framework

- **R**ecommend: Propose options and a recommendation
- **A**gree: Must agree before proceeding (has veto power)
- **P**erform: Implements the decision once made
- **I**nput: Provides facts, analysis, and data
- **D**ecide: Has final decision authority
- Useful for decisions involving multiple stakeholders

---

## Tradeoff Analysis: Fitness Functions

- Borrowed from evolutionary architecture
- Automated checks that validate architectural characteristics
- Examples in DevOps:
    - Deployment frequency must stay above X per week
    - `P95` latency must remain below Y milliseconds
    - Infrastructure cost must not exceed Z per month
- Run fitness functions in `CI/CD` to catch regressions

---

## Common DevOps Tradeoffs

<svg width="650" height="260" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrow_trade" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto">
      <path d="M0,0 L0,6 L7,3 z" fill="#555"/>
    </marker>
  </defs>
  <text x="325" y="25" text-anchor="middle" font-size="14" font-weight="bold">Tension Pairs</text>
  <rect x="40" y="45" width="130" height="35" fill="#e3f2fd" stroke="#1565c0" stroke-width="2" rx="5"/>
  <text x="105" y="67" text-anchor="middle" font-size="11">Speed</text>
  <line x1="170" y1="62" x2="220" y2="62" stroke="#555" stroke-width="2" marker-end="url(#arrow_trade)"/>
  <line x1="220" y1="62" x2="170" y2="62" stroke="#555" stroke-width="2" marker-end="url(#arrow_trade)"/>
  <rect x="220" y="45" width="130" height="35" fill="#ffcdd2" stroke="#c62828" stroke-width="2" rx="5"/>
  <text x="285" y="67" text-anchor="middle" font-size="11">Stability</text>
  <rect x="40" y="100" width="130" height="35" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2" rx="5"/>
  <text x="105" y="122" text-anchor="middle" font-size="11">Flexibility</text>
  <line x1="170" y1="117" x2="220" y2="117" stroke="#555" stroke-width="2" marker-end="url(#arrow_trade)"/>
  <line x1="220" y1="117" x2="170" y2="117" stroke="#555" stroke-width="2" marker-end="url(#arrow_trade)"/>
  <rect x="220" y="100" width="130" height="35" fill="#fff3e0" stroke="#e65100" stroke-width="2" rx="5"/>
  <text x="285" y="122" text-anchor="middle" font-size="11">Standardization</text>
  <rect x="390" y="45" width="130" height="35" fill="#f3e5f5" stroke="#7b1fa2" stroke-width="2" rx="5"/>
  <text x="455" y="67" text-anchor="middle" font-size="11">Security</text>
  <line x1="520" y1="62" x2="570" y2="62" stroke="#555" stroke-width="2" marker-end="url(#arrow_trade)"/>
  <line x1="570" y1="62" x2="520" y2="62" stroke="#555" stroke-width="2" marker-end="url(#arrow_trade)"/>
  <rect x="570" y="45" width="50" height="35" fill="#e3f2fd" stroke="#1565c0" stroke-width="2" rx="5"/>
  <text x="595" y="67" text-anchor="middle" font-size="11">Speed</text>
  <rect x="390" y="100" width="130" height="35" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2" rx="5"/>
  <text x="455" y="122" text-anchor="middle" font-size="11">Cost</text>
  <line x1="520" y1="117" x2="570" y2="117" stroke="#555" stroke-width="2" marker-end="url(#arrow_trade)"/>
  <line x1="570" y1="117" x2="520" y2="117" stroke="#555" stroke-width="2" marker-end="url(#arrow_trade)"/>
  <rect x="570" y="100" width="50" height="35" fill="#ffcdd2" stroke="#c62828" stroke-width="2" rx="5"/>
  <text x="595" y="122" text-anchor="middle" font-size="11">Quality</text>
  <text x="325" y="175" text-anchor="middle" font-size="12" fill="#555">Every decision involves balancing competing concerns</text>
</svg>

---

## Speed vs Stability

- Fast deployments can introduce instability
- Too much caution slows delivery to a crawl
- Resolution: progressive delivery (`canary`, `blue-green`, feature flags)
- DORA metrics help track both simultaneously
    - Deployment frequency (speed)
    - Change failure rate (stability)

---

## Flexibility vs Standardization

- Teams want freedom to choose their own tools
- The organization needs consistency for supportability
- Resolution: "paved roads" -- provide a golden path but allow divergence
- Standardize the interface, not the implementation
- Example: standardize on `OCI` containers, allow any language inside

---

## Security vs Developer Experience

- Security gates can slow developer velocity
- Skipping security checks creates risk
- Resolution: "shift left" security into the pipeline
- Automate security scans (`SAST`, `DAST`, `SCA`) as pipeline stages
- Make the secure path the easiest path

---

## What Are Architecture Decision Records?

- Lightweight documents that capture architectural decisions
- Each `ADR` records one decision, its context, and consequences
- Stored alongside the code they apply to (usually in a `docs/adr/` folder)
- Popularized by Michael Nygard in a 2011 blog post
- They create a decision log for the project

---

## Why Use ADRs?

- **Institutional memory**: New team members understand past decisions
- **Accountability**: Decisions are traceable to context and rationale
- **Reversibility**: Understanding the "why" makes it easier to change later
- **Communication**: Stakeholders can review decisions asynchronously
- **Learning**: Teams can reflect on past decisions and improve

---

## ADR Template Structure

<svg width="650" height="300" xmlns="http://www.w3.org/2000/svg">
  <rect x="30" y="10" width="590" height="280" fill="#f5f5f5" stroke="#333" stroke-width="2" rx="6"/>
  <text x="325" y="38" text-anchor="middle" font-size="15" font-weight="bold">ADR-0001: Use Kubernetes for Orchestration</text>
  <line x1="50" y1="48" x2="600" y2="48" stroke="#ccc" stroke-width="1"/>
  <text x="50" y="72" font-size="13" font-weight="bold" fill="#1565c0">Status:</text>
  <text x="120" y="72" font-size="13">Accepted</text>
  <line x1="50" y1="82" x2="600" y2="82" stroke="#eee" stroke-width="1"/>
  <text x="50" y="106" font-size="13" font-weight="bold" fill="#1565c0">Context:</text>
  <text x="50" y="124" font-size="11">We need container orchestration for 30+ microservices.</text>
  <text x="50" y="140" font-size="11">Team has experience with both Docker Swarm and Kubernetes.</text>
  <line x1="50" y1="150" x2="600" y2="150" stroke="#eee" stroke-width="1"/>
  <text x="50" y="174" font-size="13" font-weight="bold" fill="#1565c0">Decision:</text>
  <text x="50" y="192" font-size="11">We will use Kubernetes (EKS) for container orchestration.</text>
  <line x1="50" y1="202" x2="600" y2="202" stroke="#eee" stroke-width="1"/>
  <text x="50" y="226" font-size="13" font-weight="bold" fill="#1565c0">Consequences:</text>
  <text x="50" y="244" font-size="11">+ Industry standard, large ecosystem, strong hiring pool.</text>
  <text x="50" y="260" font-size="11">- Steeper learning curve, higher initial operational cost.</text>
  <text x="50" y="276" font-size="11">- Requires investment in cluster management tooling.</text>
</svg>

---

## ADR Status Lifecycle

<svg width="650" height="180" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrow_adr" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <rect x="30" y="65" width="100" height="45" fill="#fff9c4" stroke="#f9a825" stroke-width="2" rx="6"/>
  <text x="80" y="93" text-anchor="middle" font-size="12" font-weight="bold">Proposed</text>
  <rect x="170" y="65" width="100" height="45" fill="#c8e6c9" stroke="#2e7d32" stroke-width="2" rx="6"/>
  <text x="220" y="93" text-anchor="middle" font-size="12" font-weight="bold">Accepted</text>
  <rect x="310" y="35" width="110" height="45" fill="#bbdefb" stroke="#1565c0" stroke-width="2" rx="6"/>
  <text x="365" y="63" text-anchor="middle" font-size="12" font-weight="bold">Superseded</text>
  <rect x="310" y="100" width="110" height="45" fill="#ffcdd2" stroke="#c62828" stroke-width="2" rx="6"/>
  <text x="365" y="128" text-anchor="middle" font-size="12" font-weight="bold">Deprecated</text>
  <rect x="460" y="35" width="110" height="45" fill="#e1bee7" stroke="#7b1fa2" stroke-width="2" rx="6"/>
  <text x="515" y="63" text-anchor="middle" font-size="12" font-weight="bold">Replaced by</text>
  <line x1="130" y1="87" x2="170" y2="87" stroke="#333" stroke-width="2" marker-end="url(#arrow_adr)"/>
  <line x1="270" y1="77" x2="310" y2="57" stroke="#333" stroke-width="2" marker-end="url(#arrow_adr)"/>
  <line x1="270" y1="97" x2="310" y2="122" stroke="#333" stroke-width="2" marker-end="url(#arrow_adr)"/>
  <line x1="420" y1="57" x2="460" y2="57" stroke="#333" stroke-width="2" marker-end="url(#arrow_adr)"/>
  <text x="80" y="140" text-anchor="middle" font-size="10" fill="#555">Under review</text>
  <text x="220" y="140" text-anchor="middle" font-size="10" fill="#555">Active decision</text>
  <text x="365" y="170" text-anchor="middle" font-size="10" fill="#555">No longer valid</text>
  <text x="515" y="100" text-anchor="middle" font-size="10" fill="#555">New ADR linked</text>
</svg>

---

## ADR as Markdown

```markdown
# ADR-0003: Use Terraform for IaC

## Status
Accepted (2024-03-15)

## Context
We need a cloud-agnostic IaC tool.
Team has Terraform experience.

## Decision
Adopt Terraform with remote state in S3.

## Consequences
- Positive: Multi-cloud support, large community
- Negative: State management complexity
```

---

## ADR Tooling

- `adr-tools`: Shell scripts for managing `ADRs` (by Nat Pryce)
    - `adr new "Use PostgreSQL for user data"`
    - `adr list`
    - `adr link 3 "Supersedes" 1`
- `log4brains`: Web UI for browsing `ADRs`
- `adr-viewer`: Generates HTML from `ADR` files
- Many teams simply use markdown files in `Git`

---

## Where to Store ADRs

- **In the repository**: Close to the code they describe
    - `docs/adr/0001-use-kubernetes.md`
    - `docs/adr/0002-adopt-gitops.md`
- **In a central wiki**: For organization-wide decisions
- **Best practice**: Repository-level for service decisions, wiki for cross-cutting
- Always version-controlled, never in ephemeral storage

---

## ADR Anti-Patterns

- Writing `ADRs` after the fact with fabricated context
- Making `ADRs` too long (they should fit on one page)
- Never revisiting or superseding outdated `ADRs`
- Using `ADRs` as approval gates instead of documentation
- Not linking related `ADRs` together
- Storing them where nobody can find them

---

## The Decision Flow Process

<svg width="650" height="300" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrow_flow" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <rect x="250" y="10" width="150" height="40" fill="#fff9c4" stroke="#f9a825" stroke-width="2" rx="6"/>
  <text x="325" y="35" text-anchor="middle" font-size="12">Identify Decision</text>
  <line x1="325" y1="50" x2="325" y2="70" stroke="#333" stroke-width="2" marker-end="url(#arrow_flow)"/>
  <rect x="250" y="70" width="150" height="40" fill="#e3f2fd" stroke="#1565c0" stroke-width="2" rx="6"/>
  <text x="325" y="95" text-anchor="middle" font-size="12">Gather Context</text>
  <line x1="325" y1="110" x2="325" y2="130" stroke="#333" stroke-width="2" marker-end="url(#arrow_flow)"/>
  <rect x="250" y="130" width="150" height="40" fill="#f3e5f5" stroke="#7b1fa2" stroke-width="2" rx="6"/>
  <text x="325" y="155" text-anchor="middle" font-size="12">Explore Options</text>
  <line x1="325" y1="170" x2="325" y2="190" stroke="#333" stroke-width="2" marker-end="url(#arrow_flow)"/>
  <rect x="250" y="190" width="150" height="40" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2" rx="6"/>
  <text x="325" y="215" text-anchor="middle" font-size="12">Evaluate Tradeoffs</text>
  <line x1="325" y1="230" x2="325" y2="250" stroke="#333" stroke-width="2" marker-end="url(#arrow_flow)"/>
  <rect x="250" y="250" width="150" height="40" fill="#fff3e0" stroke="#e65100" stroke-width="2" rx="6"/>
  <text x="325" y="275" text-anchor="middle" font-size="12">Document in ADR</text>
  <text x="490" y="35" text-anchor="start" font-size="10" fill="#555">Is this architectural?</text>
  <text x="490" y="95" text-anchor="start" font-size="10" fill="#555">Constraints, requirements</text>
  <text x="490" y="155" text-anchor="start" font-size="10" fill="#555">PoCs, benchmarks, research</text>
  <text x="490" y="215" text-anchor="start" font-size="10" fill="#555">Decision matrix, DACI</text>
  <text x="490" y="275" text-anchor="start" font-size="10" fill="#555">Context, decision, consequences</text>
</svg>

---

## Gathering Context Effectively

- Talk to all affected stakeholders, not just your team
- Understand current constraints (budget, timeline, compliance)
- Research what others in the industry have done
- Identify non-negotiable requirements vs nice-to-haves
- Document assumptions explicitly -- they change over time

---

## Exploring Options: Spike and PoC

- A **spike** is a time-boxed investigation to reduce uncertainty
- A **proof of concept** validates a specific approach works
- Set clear success criteria before starting
- Document findings even if the option is rejected
- Time-box to prevent analysis paralysis (usually 1-2 weeks)

---

## Bias in Decision-Making

- **Sunk cost fallacy**: Continuing with a bad choice because of past investment
- **Anchoring**: Over-relying on the first option considered
- **Groupthink**: Conforming to team consensus without critical evaluation
- **Recency bias**: Choosing the newest technology because it is trending
- **Familiarity bias**: Choosing what you already know over what might be better

---

## Mitigating Decision Bias

- Assign a "devil's advocate" role in decision meetings
- Use structured frameworks (decision matrix, `DACI`) to force objectivity
- Seek external opinions from outside the immediate team
- Set evaluation criteria before looking at options
- Review past decisions periodically for patterns of bias

---

## Time-Boxing Decisions

- Not every decision deserves unlimited analysis
- Use the "two-way door" test to calibrate investment
- Low-impact, reversible decisions: 30 minutes
- Medium-impact decisions: One meeting with stakeholders
- High-impact, irreversible decisions: Formal evaluation over days or weeks
- The cost of delay often exceeds the cost of a suboptimal choice

---

## The Decision Record Review Process

- Propose the `ADR` via a pull request
- Reviewers are the Contributors in the `DACI` framework
- Use the `PR` discussion to capture dissenting views
- Merge when the Approver accepts
- This creates a natural audit trail in `Git` history

---

## Linking Decisions Together

- Decisions rarely exist in isolation
- An `ADR` to adopt `Kubernetes` links to `ADRs` about:
    - Networking (`CNI` plugin selection)
    - Storage (persistent volume strategy)
    - Secrets (`Vault` integration)
    - Monitoring (`Prometheus` vs `Datadog`)
- Use `ADR` cross-references: "See also: ADR-0005, ADR-0012"

---

## Revisiting Decisions

- Schedule periodic reviews of active `ADRs` (e.g., quarterly)
- Revisit when the original context changes:
    - Team size changes significantly
    - Technology landscape shifts
    - Business requirements evolve
    - Cost structure changes
- Supersede old `ADRs` rather than editing them in place

---

## Case Study: Choosing a CI/CD Platform

- **Context**: Growing startup with 12 microservices, 5 teams
- **Options evaluated**: `Jenkins`, `GitLab CI`, `GitHub Actions`, `CircleCI`
- **Criteria**: Cost, scalability, developer experience, ecosystem
- **Decision**: `GitHub Actions` (already using `GitHub`, lowest switching cost)
- **Consequence**: Limited self-hosted runner support required workaround
- **Documented in**: `ADR-0007`

---

## Case Study: Monorepo vs Polyrepo

- **Context**: 3 teams, 8 services, shared libraries
- **Monorepo pros**: Atomic changes, shared tooling, easier refactoring
- **Polyrepo pros**: Independent releases, clearer ownership, smaller checkouts
- **Decision**: Polyrepo with a shared library registry
- **Reason**: Teams had different release cadences
- **Revisited**: After 18 months when dependency management became painful

---

## Organizational Decision Governance

<svg width="650" height="280" xmlns="http://www.w3.org/2000/svg">
  <rect x="160" y="10" width="330" height="50" fill="#1565c0" stroke="#0d47a1" stroke-width="2" rx="8"/>
  <text x="325" y="40" text-anchor="middle" font-size="13" font-weight="bold" fill="white">Architecture Review Board</text>
  <rect x="30" y="100" width="180" height="50" fill="#2e7d32" stroke="#1b5e20" stroke-width="2" rx="8"/>
  <text x="120" y="130" text-anchor="middle" font-size="12" font-weight="bold" fill="white">Platform Team ADRs</text>
  <rect x="235" y="100" width="180" height="50" fill="#e65100" stroke="#bf360c" stroke-width="2" rx="8"/>
  <text x="325" y="130" text-anchor="middle" font-size="12" font-weight="bold" fill="white">Cross-Team ADRs</text>
  <rect x="440" y="100" width="180" height="50" fill="#7b1fa2" stroke="#4a148c" stroke-width="2" rx="8"/>
  <text x="530" y="130" text-anchor="middle" font-size="12" font-weight="bold" fill="white">Security ADRs</text>
  <rect x="30" y="200" width="120" height="40" fill="#e8f5e9" stroke="#2e7d32" stroke-width="1" rx="5"/>
  <text x="90" y="225" text-anchor="middle" font-size="10">Team A ADRs</text>
  <rect x="170" y="200" width="120" height="40" fill="#e8f5e9" stroke="#2e7d32" stroke-width="1" rx="5"/>
  <text x="230" y="225" text-anchor="middle" font-size="10">Team B ADRs</text>
  <rect x="360" y="200" width="120" height="40" fill="#e8f5e9" stroke="#2e7d32" stroke-width="1" rx="5"/>
  <text x="420" y="225" text-anchor="middle" font-size="10">Team C ADRs</text>
  <rect x="500" y="200" width="120" height="40" fill="#e8f5e9" stroke="#2e7d32" stroke-width="1" rx="5"/>
  <text x="560" y="225" text-anchor="middle" font-size="10">Team D ADRs</text>
  <line x1="325" y1="60" x2="120" y2="100" stroke="#333" stroke-width="1.5"/>
  <line x1="325" y1="60" x2="325" y2="100" stroke="#333" stroke-width="1.5"/>
  <line x1="325" y1="60" x2="530" y2="100" stroke="#333" stroke-width="1.5"/>
  <line x1="120" y1="150" x2="90" y2="200" stroke="#333" stroke-width="1"/>
  <line x1="120" y1="150" x2="230" y2="200" stroke="#333" stroke-width="1"/>
  <line x1="530" y1="150" x2="420" y2="200" stroke="#333" stroke-width="1"/>
  <line x1="530" y1="150" x2="560" y2="200" stroke="#333" stroke-width="1"/>
  <text x="325" y="270" text-anchor="middle" font-size="11" fill="#555">Decisions flow up for review, governance flows down as guidelines</text>
</svg>

---

## Lightweight vs Heavyweight Governance

- **Lightweight**: `ADRs` in repos, peer review via `PRs`, async discussion
    - Best for: Small to medium orgs, high-trust environments
- **Heavyweight**: Architecture Review Boards, formal approval processes
    - Best for: Large orgs, regulated industries, compliance requirements
- Most organizations benefit from a hybrid approach
- Start lightweight and add governance as needed

---

## Building a Decision-Making Culture

- Normalize saying "I do not know, let us investigate"
- Celebrate well-documented decisions, even if the outcome was wrong
- Make `ADRs` part of onboarding for new team members
- Share decision retrospectives across teams
- Reward structured thinking over gut instinct

---

## Measuring Decision Quality

- Track how often decisions are revisited or reversed
- Monitor time from decision to implementation
- Survey team confidence in architectural direction
- Count the number of undocumented "shadow decisions"
- Use DORA metrics as proxy for decision effectiveness
    - Lead time, deployment frequency, MTTR, change failure rate

---

## Common Mistakes in DevOps Decision-Making

- Making decisions by committee without a clear approver
- Choosing technology based on resume-driven development
- Ignoring Conway's Law and fighting the organizational structure
- Failing to document the "why" behind decisions
- Not revisiting decisions when the context changes
- Over-engineering for problems you do not have yet

---

## Decision Framework Checklist

- [ ] Is this decision architectural? (scope, durability, reversibility, cost)
- [ ] Who are the `DACI` roles for this decision?
- [ ] Have we gathered sufficient context and constraints?
- [ ] Have we explored at least three options?
- [ ] Have we evaluated tradeoffs with explicit criteria?
- [ ] Is the decision documented in an `ADR`?
- [ ] Have stakeholders reviewed and agreed?
- [ ] Is there a plan to revisit this decision?

---

## Summary: Key Takeaways

- Architectural decisions in DevOps shape systems and teams for years
- Use the reversibility test to calibrate the effort you invest
- Respect Conway's Law -- align teams and architecture intentionally
- Apply structured frameworks (`DACI`, decision matrices) to reduce bias
- Document every significant decision in an `ADR`
- Revisit decisions periodically as context evolves
