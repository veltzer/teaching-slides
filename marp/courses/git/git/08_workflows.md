# Git Workflows
---
## Git's Workflow Flexibility
- No enforced workflow
- Team-specific adaptation
- Project requirements
- Scale considerations
---
## Common Workflow Types
<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <!-- Centralized -->
  <rect x="20" y="20" width="260" height="70" fill="#e3f2fd" stroke="#1565c0" stroke-width="2" rx="8"/>
  <text x="150" y="45" text-anchor="middle" font-size="13" font-weight="bold" fill="#1565c0">Centralized</text>
  <line x1="60" y1="65" x2="240" y2="65" stroke="#1565c0" stroke-width="3"/>
  <circle cx="100" cy="65" r="4" fill="#1565c0"/><circle cx="150" cy="65" r="4" fill="#1565c0"/><circle cx="200" cy="65" r="4" fill="#1565c0"/>
  <text x="150" y="80" text-anchor="middle" font-size="9" fill="#555">single branch</text>
  <!-- Feature Branch -->
  <rect x="320" y="20" width="260" height="70" fill="#f3e5f5" stroke="#7b1fa2" stroke-width="2" rx="8"/>
  <text x="450" y="45" text-anchor="middle" font-size="13" font-weight="bold" fill="#7b1fa2">Feature Branch</text>
  <line x1="360" y1="68" x2="540" y2="68" stroke="#7b1fa2" stroke-width="2"/>
  <line x1="400" y1="68" x2="420" y2="55" stroke="#7b1fa2" stroke-width="2"/><line x1="420" y1="55" x2="460" y2="55" stroke="#7b1fa2" stroke-width="2"/><line x1="460" y1="55" x2="470" y2="68" stroke="#7b1fa2" stroke-width="2"/>
  <line x1="480" y1="68" x2="490" y2="55" stroke="#7b1fa2" stroke-width="2"/><line x1="490" y1="55" x2="520" y2="55" stroke="#7b1fa2" stroke-width="2"/><line x1="520" y1="55" x2="530" y2="68" stroke="#7b1fa2" stroke-width="2"/>
  <text x="450" y="82" text-anchor="middle" font-size="9" fill="#555">short-lived branches</text>
  <!-- GitFlow -->
  <rect x="20" y="110" width="260" height="70" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2" rx="8"/>
  <text x="150" y="135" text-anchor="middle" font-size="13" font-weight="bold" fill="#2e7d32">GitFlow</text>
  <line x1="60" y1="155" x2="240" y2="155" stroke="#2e7d32" stroke-width="2"/>
  <line x1="60" y1="165" x2="240" y2="165" stroke="#2e7d32" stroke-width="1.5" stroke-dasharray="4,2"/>
  <line x1="60" y1="145" x2="240" y2="145" stroke="#2e7d32" stroke-width="1.5" stroke-dasharray="4,2"/>
  <text x="150" y="178" text-anchor="middle" font-size="9" fill="#555">multiple long-lived branches</text>
  <!-- Trunk-Based -->
  <rect x="320" y="110" width="260" height="70" fill="#fff3e0" stroke="#e65100" stroke-width="2" rx="8"/>
  <text x="450" y="135" text-anchor="middle" font-size="13" font-weight="bold" fill="#e65100">Trunk-Based</text>
  <line x1="360" y1="158" x2="540" y2="158" stroke="#e65100" stroke-width="3"/>
  <line x1="400" y1="158" x2="410" y2="150" stroke="#e65100" stroke-width="1.5"/><line x1="410" y1="150" x2="420" y2="158" stroke="#e65100" stroke-width="1.5"/>
  <line x1="460" y1="158" x2="470" y2="150" stroke="#e65100" stroke-width="1.5"/><line x1="470" y1="150" x2="480" y2="158" stroke="#e65100" stroke-width="1.5"/>
  <text x="450" y="175" text-anchor="middle" font-size="9" fill="#555">very short branches off main</text>
</svg>

---
## Centralized Workflow
- Single main branch
- Direct commits
- Simple collaboration
- Small team focus
---
## Feature Branch Workflow
- Feature isolation
- Code review process
- Clean main branch
- Team collaboration
---
## Development vs Production
<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd1_08_workflows" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <!-- develop branch (top) -->
  <text x="10" y="55" font-size="11" font-weight="bold" fill="#7b1fa2">develop</text>
  <line x1="80" y1="52" x2="560" y2="52" stroke="#7b1fa2" stroke-width="3"/>
  <circle cx="120" cy="52" r="5" fill="#f3e5f5" stroke="#7b1fa2" stroke-width="2"/>
  <circle cx="200" cy="52" r="5" fill="#f3e5f5" stroke="#7b1fa2" stroke-width="2"/>
  <circle cx="300" cy="52" r="5" fill="#f3e5f5" stroke="#7b1fa2" stroke-width="2"/>
  <circle cx="400" cy="52" r="5" fill="#f3e5f5" stroke="#7b1fa2" stroke-width="2"/>
  <circle cx="500" cy="52" r="5" fill="#f3e5f5" stroke="#7b1fa2" stroke-width="2"/>
  <!-- main/production branch (bottom) -->
  <text x="10" y="155" font-size="11" font-weight="bold" fill="#1565c0">main</text>
  <line x1="80" y1="152" x2="560" y2="152" stroke="#1565c0" stroke-width="3"/>
  <circle cx="120" cy="152" r="5" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <circle cx="300" cy="152" r="6" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <circle cx="500" cy="152" r="6" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <!-- feature branches merging into develop -->
  <line x1="140" y1="25" x2="200" y2="47" stroke="#2e7d32" stroke-width="1.5" marker-end="url(#arrowd1_08_workflows)"/>
  <text x="140" y="20" font-size="9" fill="#2e7d32">feat-A</text>
  <line x1="340" y1="25" x2="400" y2="47" stroke="#2e7d32" stroke-width="1.5" marker-end="url(#arrowd1_08_workflows)"/>
  <text x="340" y="20" font-size="9" fill="#2e7d32">feat-B</text>
  <!-- develop merging into main at release points -->
  <line x1="300" y1="57" x2="300" y2="145" stroke="#e65100" stroke-width="2" marker-end="url(#arrowd1_08_workflows)"/>
  <line x1="500" y1="57" x2="500" y2="145" stroke="#e65100" stroke-width="2" marker-end="url(#arrowd1_08_workflows)"/>
  <!-- version tags -->
  <rect x="270" y="165" width="60" height="20" fill="#fff3e0" stroke="#e65100" stroke-width="1.5" rx="4"/>
  <text x="300" y="179" text-anchor="middle" font-size="10" font-weight="bold" fill="#e65100">v1.0</text>
  <rect x="470" y="165" width="60" height="20" fill="#fff3e0" stroke="#e65100" stroke-width="1.5" rx="4"/>
  <text x="500" y="179" text-anchor="middle" font-size="10" font-weight="bold" fill="#e65100">v2.0</text>
  <text x="300" y="105" text-anchor="middle" font-size="9" fill="#e65100">release</text>
  <text x="500" y="105" text-anchor="middle" font-size="9" fill="#e65100">release</text>
</svg>

---
## GitFlow Workflow
- Master branch
- Develop branch
- Feature branches
- Release branches
- Hotfix branches
---
## GitFlow Branch Structure
<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd2_08_workflows" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <!-- Branch labels -->
  <text x="10" y="22" font-size="10" font-weight="bold" fill="#1565c0">main</text>
  <text x="10" y="62" font-size="10" font-weight="bold" fill="#c62828">hotfix</text>
  <text x="10" y="102" font-size="10" font-weight="bold" fill="#e65100">release</text>
  <text x="10" y="142" font-size="10" font-weight="bold" fill="#7b1fa2">develop</text>
  <text x="10" y="182" font-size="10" font-weight="bold" fill="#2e7d32">feature</text>
  <!-- main branch -->
  <line x1="70" y1="18" x2="580" y2="18" stroke="#1565c0" stroke-width="3"/>
  <circle cx="100" cy="18" r="4" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <circle cx="380" cy="18" r="4" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <circle cx="530" cy="18" r="4" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <!-- hotfix branch -->
  <line x1="380" y1="18" x2="400" y2="58" stroke="#c62828" stroke-width="1.5"/>
  <line x1="400" y1="58" x2="460" y2="58" stroke="#c62828" stroke-width="2"/>
  <circle cx="430" cy="58" r="4" fill="#ffebee" stroke="#c62828" stroke-width="2"/>
  <line x1="460" y1="58" x2="530" y2="18" stroke="#c62828" stroke-width="1.5" marker-end="url(#arrowd2_08_workflows)"/>
  <line x1="460" y1="58" x2="500" y2="138" stroke="#c62828" stroke-width="1.5" marker-end="url(#arrowd2_08_workflows)"/>
  <!-- release branch -->
  <line x1="300" y1="138" x2="320" y2="98" stroke="#e65100" stroke-width="1.5"/>
  <line x1="320" y1="98" x2="370" y2="98" stroke="#e65100" stroke-width="2"/>
  <circle cx="345" cy="98" r="4" fill="#fff3e0" stroke="#e65100" stroke-width="2"/>
  <line x1="370" y1="98" x2="380" y2="18" stroke="#e65100" stroke-width="1.5" marker-end="url(#arrowd2_08_workflows)"/>
  <!-- develop branch -->
  <line x1="70" y1="138" x2="580" y2="138" stroke="#7b1fa2" stroke-width="3"/>
  <circle cx="100" cy="138" r="4" fill="#f3e5f5" stroke="#7b1fa2" stroke-width="2"/>
  <circle cx="180" cy="138" r="4" fill="#f3e5f5" stroke="#7b1fa2" stroke-width="2"/>
  <circle cx="260" cy="138" r="4" fill="#f3e5f5" stroke="#7b1fa2" stroke-width="2"/>
  <circle cx="300" cy="138" r="4" fill="#f3e5f5" stroke="#7b1fa2" stroke-width="2"/>
  <circle cx="500" cy="138" r="4" fill="#f3e5f5" stroke="#7b1fa2" stroke-width="2"/>
  <circle cx="550" cy="138" r="4" fill="#f3e5f5" stroke="#7b1fa2" stroke-width="2"/>
  <!-- feature branches -->
  <line x1="120" y1="138" x2="130" y2="178" stroke="#2e7d32" stroke-width="1.5"/>
  <line x1="130" y1="178" x2="240" y2="178" stroke="#2e7d32" stroke-width="2"/>
  <circle cx="160" cy="178" r="4" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <circle cx="200" cy="178" r="4" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <line x1="240" y1="178" x2="260" y2="138" stroke="#2e7d32" stroke-width="1.5" marker-end="url(#arrowd2_08_workflows)"/>
</svg>

---
## Trunk-Based Development
- Short-lived branches
- Frequent integration
- Continuous delivery
- Fast feedback
---
## GitHub Flow
- Simple branching
- Pull requests
- Deployment focus
- Continuous delivery
---
## Forking Workflow
- Project forks
- Pull requests
- Public projects
- Open source
---
## Back Porting Changes
- Version maintenance
- Multiple releases
- Cherry-picking
- Release branches
---
## Creating Your Workflow
- Team size
- Project needs
- Release cycle
- Quality requirements
---
## Jenkins Integration
<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd3_08_workflows" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <!-- Git Push -->
  <rect x="10" y="65" width="90" height="50" fill="#e3f2fd" stroke="#1565c0" stroke-width="2" rx="8"/>
  <text x="55" y="85" text-anchor="middle" font-size="11" font-weight="bold" fill="#1565c0">Git</text>
  <text x="55" y="100" text-anchor="middle" font-size="10" fill="#1565c0">git push</text>
  <!-- Webhook arrow -->
  <line x1="100" y1="90" x2="145" y2="90" stroke="#333" stroke-width="2" marker-end="url(#arrowd3_08_workflows)"/>
  <text x="123" y="82" text-anchor="middle" font-size="8" fill="#666">webhook</text>
  <!-- Jenkins Build -->
  <rect x="150" y="55" width="110" height="70" fill="#f3e5f5" stroke="#7b1fa2" stroke-width="2" rx="8"/>
  <text x="205" y="82" text-anchor="middle" font-size="12" font-weight="bold" fill="#7b1fa2">Jenkins</text>
  <text x="205" y="100" text-anchor="middle" font-size="10" fill="#7b1fa2">Build</text>
  <text x="205" y="115" text-anchor="middle" font-size="8" fill="#999">compile + package</text>
  <!-- Arrow to Test -->
  <line x1="260" y1="90" x2="305" y2="90" stroke="#333" stroke-width="2" marker-end="url(#arrowd3_08_workflows)"/>
  <!-- Test -->
  <rect x="310" y="55" width="110" height="70" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2" rx="8"/>
  <text x="365" y="82" text-anchor="middle" font-size="12" font-weight="bold" fill="#2e7d32">Test</text>
  <text x="365" y="100" text-anchor="middle" font-size="10" fill="#2e7d32">Run Suite</text>
  <text x="365" y="115" text-anchor="middle" font-size="8" fill="#999">unit + integration</text>
  <!-- Arrow to Deploy -->
  <line x1="420" y1="90" x2="465" y2="90" stroke="#333" stroke-width="2" marker-end="url(#arrowd3_08_workflows)"/>
  <!-- Deploy -->
  <rect x="470" y="55" width="110" height="70" fill="#fff3e0" stroke="#e65100" stroke-width="2" rx="8"/>
  <text x="525" y="82" text-anchor="middle" font-size="12" font-weight="bold" fill="#e65100">Deploy</text>
  <text x="525" y="100" text-anchor="middle" font-size="10" fill="#e65100">Release</text>
  <text x="525" y="115" text-anchor="middle" font-size="8" fill="#999">staging / prod</text>
  <!-- Pipeline label -->
  <text x="300" y="25" text-anchor="middle" font-size="11" fill="#555">CI/CD Pipeline</text>
  <line x1="150" y1="32" x2="450" y2="32" stroke="#ddd" stroke-width="1" stroke-dasharray="4,3"/>
  <!-- Status indicators -->
  <circle cx="205" cy="140" r="6" fill="#4caf50"/><text x="220" y="144" font-size="8" fill="#555">pass</text>
  <circle cx="365" cy="140" r="6" fill="#4caf50"/><text x="380" y="144" font-size="8" fill="#555">pass</text>
  <circle cx="525" cy="140" r="6" fill="#4caf50"/><text x="540" y="144" font-size="8" fill="#555">live</text>
</svg>

---
## Working with Pull Requests
- Code review
- Discussion
- Automated checks
- Merge approval
---
## Pull Request Flow
- Branch creation
- Code changes
- PR submission
- Review process
- Merge completion
---
## Gerrit Workflow
- Change sets
- Code review
- Verification
- Submit requirements
---
## Release Management
- Version control
- Release branches
- Hotfix process
- Deployment strategy
---
## Environment Management
- Development
- Testing
- Staging
- Production
---
## Continuous Integration
- Automated testing
- Build verification
- Integration checks
- Deployment pipeline
---
## Branch Protection Rules
- Required reviews
- Status checks
- Branch restrictions
- Merge requirements
---
## Code Review Process
- Review assignment
- Feedback cycle
- Approval flow
- Merge criteria
---
## Documentation
- Process documentation
- Team guidelines
- Workflow diagrams
- Best practices
---
## Team Collaboration
- Communication
- Coordination
- Conflict resolution
- Knowledge sharing
---
## Quality Assurance
- Testing requirements
- Code standards
- Review process
- Automation
---
## Deployment Strategies
- Continuous deployment
- Staged rollout
- Feature flags
- Rollback plans
---
## Workflow Tools
- Git commands
- CI/CD platforms
- Code review tools
- Automation scripts
---
## Best Practices
- Clear processes
- Consistent patterns
- Team agreement
- Regular review
---
## Common Problems
- Process complexity
- Team adoption
- Tool integration
- Workflow conflicts
---
## Measuring Success
- Delivery speed
- Code quality
- Team efficiency
- Process metrics
---
## Workflow Evolution
- Regular assessment
- Process improvement
- Team feedback
- Adaptation needs
