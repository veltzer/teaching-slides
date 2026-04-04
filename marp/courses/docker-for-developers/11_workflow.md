# Development Workflow

---

## Docker in Development

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd0_10_workflow" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <text x="300" y="20" text-anchor="middle" font-size="12" font-weight="bold">Docker Development Workflow</text>
  <rect x="20" y="35" width="110" height="55" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="75" y="55" text-anchor="middle" font-size="11" font-weight="bold">Edit Code</text>
  <text x="75" y="73" text-anchor="middle" font-size="10">Local IDE</text>
  <line x1="130" y1="62" x2="160" y2="62" stroke="#333" stroke-width="2" marker-end="url(#arrowd0_10_workflow)"/>
  <rect x="160" y="35" width="110" height="55" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="215" y="55" text-anchor="middle" font-size="11" font-weight="bold">Volume Mount</text>
  <text x="215" y="73" text-anchor="middle" font-size="10">-v src:/app</text>
  <line x1="270" y1="62" x2="300" y2="62" stroke="#333" stroke-width="2" marker-end="url(#arrowd0_10_workflow)"/>
  <rect x="300" y="35" width="110" height="55" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="355" y="55" text-anchor="middle" font-size="11" font-weight="bold">Hot Reload</text>
  <text x="355" y="73" text-anchor="middle" font-size="10">Auto-refresh</text>
  <line x1="410" y1="62" x2="440" y2="62" stroke="#333" stroke-width="2" marker-end="url(#arrowd0_10_workflow)"/>
  <rect x="440" y="35" width="140" height="55" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="510" y="55" text-anchor="middle" font-size="11" font-weight="bold">Test in Container</text>
  <text x="510" y="73" text-anchor="middle" font-size="10">Same as prod env</text>
  <rect x="120" y="120" width="360" height="50" fill="#e3f2fd" stroke="#333" stroke-width="1.5" rx="5"/>
  <text x="300" y="142" text-anchor="middle" font-size="11" font-weight="bold">docker-compose up</text>
  <text x="300" y="158" text-anchor="middle" font-size="10">Orchestrates app + database + cache + services</text>
</svg>

---

## CI/CD Pipeline Integration

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd1_10_workflow" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <text x="300" y="18" text-anchor="middle" font-size="12" font-weight="bold">CI/CD with Docker</text>
  <rect x="10" y="30" width="90" height="45" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="55" y="48" text-anchor="middle" font-size="10" font-weight="bold">git push</text>
  <text x="55" y="63" text-anchor="middle" font-size="10">Source</text>
  <line x1="100" y1="52" x2="130" y2="52" stroke="#333" stroke-width="2" marker-end="url(#arrowd1_10_workflow)"/>
  <rect x="130" y="30" width="100" height="45" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="180" y="48" text-anchor="middle" font-size="10" font-weight="bold">docker build</text>
  <text x="180" y="63" text-anchor="middle" font-size="10">CI Server</text>
  <line x1="230" y1="52" x2="260" y2="52" stroke="#333" stroke-width="2" marker-end="url(#arrowd1_10_workflow)"/>
  <rect x="260" y="30" width="90" height="45" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="305" y="48" text-anchor="middle" font-size="10" font-weight="bold">Test</text>
  <text x="305" y="63" text-anchor="middle" font-size="10">Run tests</text>
  <line x1="350" y1="52" x2="380" y2="52" stroke="#333" stroke-width="2" marker-end="url(#arrowd1_10_workflow)"/>
  <rect x="380" y="30" width="90" height="45" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="425" y="48" text-anchor="middle" font-size="10" font-weight="bold">Push Image</text>
  <text x="425" y="63" text-anchor="middle" font-size="10">Registry</text>
  <line x1="470" y1="52" x2="500" y2="52" stroke="#333" stroke-width="2" marker-end="url(#arrowd1_10_workflow)"/>
  <rect x="500" y="30" width="90" height="45" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="545" y="48" text-anchor="middle" font-size="10" font-weight="bold">Deploy</text>
  <text x="545" y="63" text-anchor="middle" font-size="10">Production</text>
  <rect x="100" y="100" width="400" height="40" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="5" stroke-dasharray="4,2"/>
  <text x="300" y="118" text-anchor="middle" font-size="10">Automated pipeline: same image from build to production</text>
  <text x="300" y="135" text-anchor="middle" font-size="10" fill="#555">Ensures consistency across all environments</text>
</svg>

---

## Local Development Best Practices

| Practice | Purpose | Implementation |
|----------|---------|----------------|
| Volume mounts | Code sync | `-v $(pwd):/app` |
| Hot reload | Quick iteration | Development servers |
| Docker Compose | Multi-container | `docker-compose.yml` |
| Environment files | Configuration | `.env` files |

---

## Multi-stage Builds

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd2_10_workflow" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <text x="300" y="18" text-anchor="middle" font-size="12" font-weight="bold">Multi-stage Build Flow</text>
  <rect x="20" y="30" width="170" height="70" fill="#fff3e0" stroke="#e65100" stroke-width="2" rx="5"/>
  <text x="105" y="50" text-anchor="middle" font-size="11" font-weight="bold" fill="#e65100">Stage 1: Build</text>
  <text x="105" y="68" text-anchor="middle" font-size="10">FROM node:18 AS build</text>
  <text x="105" y="83" text-anchor="middle" font-size="10">npm install + compile</text>
  <line x1="190" y1="65" x2="220" y2="65" stroke="#333" stroke-width="2" marker-end="url(#arrowd2_10_workflow)"/>
  <rect x="220" y="30" width="160" height="70" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="50" text-anchor="middle" font-size="11" font-weight="bold">COPY --from=build</text>
  <text x="300" y="68" text-anchor="middle" font-size="10">Only artifacts</text>
  <text x="300" y="83" text-anchor="middle" font-size="10">No dev dependencies</text>
  <line x1="380" y1="65" x2="410" y2="65" stroke="#333" stroke-width="2" marker-end="url(#arrowd2_10_workflow)"/>
  <rect x="410" y="30" width="170" height="70" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2" rx="5"/>
  <text x="495" y="50" text-anchor="middle" font-size="11" font-weight="bold" fill="#2e7d32">Stage 2: Runtime</text>
  <text x="495" y="68" text-anchor="middle" font-size="10">FROM node:18-alpine</text>
  <text x="495" y="83" text-anchor="middle" font-size="10">Minimal final image</text>
  <rect x="20" y="120" width="170" height="30" fill="#ffebee" stroke="#333" stroke-width="1" rx="4"/>
  <text x="105" y="140" text-anchor="middle" font-size="10" fill="#c62828">~900MB with build tools</text>
  <rect x="410" y="120" width="170" height="30" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="4"/>
  <text x="495" y="140" text-anchor="middle" font-size="10" fill="#2e7d32">~150MB production</text>
  <text x="300" y="180" text-anchor="middle" font-size="10" fill="#555">Build tools discarded, only runtime artifacts remain</text>
</svg>

---

## IDE Integration Tips

| IDE | Features | Setup |
|-----|----------|-------|
| VS Code | Docker extension | Remote containers |
| IntelliJ | Docker integration | Docker compose |
| Eclipse | Docker tooling | Container launch |
| Sublime | Docker syntax | Build systems |

---

## Development vs Production

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="20" y="15" width="260" height="170" fill="#fff3e0" stroke="#e65100" stroke-width="2" rx="5"/>
  <text x="150" y="35" text-anchor="middle" font-size="12" font-weight="bold" fill="#e65100">Development</text>
  <rect x="40" y="45" width="100" height="30" fill="#e3f2fd" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="90" y="65" text-anchor="middle" font-size="10">Volume mounts</text>
  <rect x="160" y="45" width="100" height="30" fill="#e3f2fd" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="210" y="65" text-anchor="middle" font-size="10">Hot reload</text>
  <rect x="40" y="85" width="100" height="30" fill="#e3f2fd" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="90" y="105" text-anchor="middle" font-size="10">Debug ports</text>
  <rect x="160" y="85" width="100" height="30" fill="#e3f2fd" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="210" y="105" text-anchor="middle" font-size="10">.env files</text>
  <rect x="40" y="125" width="220" height="30" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="4"/>
  <text x="150" y="145" text-anchor="middle" font-size="10">docker-compose.override.yml</text>
  <rect x="320" y="15" width="260" height="170" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2" rx="5"/>
  <text x="450" y="35" text-anchor="middle" font-size="12" font-weight="bold" fill="#2e7d32">Production</text>
  <rect x="340" y="45" width="100" height="30" fill="#e3f2fd" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="390" y="65" text-anchor="middle" font-size="10">Multi-stage</text>
  <rect x="460" y="45" width="100" height="30" fill="#e3f2fd" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="510" y="65" text-anchor="middle" font-size="10">Minimal image</text>
  <rect x="340" y="85" width="100" height="30" fill="#e3f2fd" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="390" y="105" text-anchor="middle" font-size="10">Non-root user</text>
  <rect x="460" y="85" width="100" height="30" fill="#e3f2fd" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="510" y="105" text-anchor="middle" font-size="10">Read-only FS</text>
  <rect x="340" y="125" width="220" height="30" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="4"/>
  <text x="450" y="145" text-anchor="middle" font-size="10">docker-compose.prod.yml</text>
</svg>

---

## Debugging Tools

| Tool | Purpose | Usage |
|------|---------|-------|
| docker exec | Shell access | Interactive debugging |
| docker logs | Log viewing | Monitoring output |
| docker inspect | Container info | Configuration check |
| docker stats | Resource usage | Performance monitoring |

---

## Code Organization

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="18" text-anchor="middle" font-size="12" font-weight="bold">Project Structure with Docker</text>
  <rect x="20" y="30" width="560" height="160" fill="none" stroke="#333" stroke-width="1" rx="5" stroke-dasharray="4,2"/>
  <rect x="40" y="45" width="120" height="40" fill="#e3f2fd" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="100" y="63" text-anchor="middle" font-size="10" font-weight="bold">Dockerfile</text>
  <text x="100" y="78" text-anchor="middle" font-size="9">Build instructions</text>
  <rect x="180" y="45" width="120" height="40" fill="#f3e5f5" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="240" y="63" text-anchor="middle" font-size="10" font-weight="bold">compose.yml</text>
  <text x="240" y="78" text-anchor="middle" font-size="9">Service definitions</text>
  <rect x="320" y="45" width="120" height="40" fill="#e8f5e9" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="380" y="63" text-anchor="middle" font-size="10" font-weight="bold">.dockerignore</text>
  <text x="380" y="78" text-anchor="middle" font-size="9">Exclude files</text>
  <rect x="460" y="45" width="100" height="40" fill="#fff3e0" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="510" y="63" text-anchor="middle" font-size="10" font-weight="bold">.env</text>
  <text x="510" y="78" text-anchor="middle" font-size="9">Environment</text>
  <rect x="40" y="100" width="250" height="40" fill="#e3f2fd" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="165" y="118" text-anchor="middle" font-size="10" font-weight="bold">src/</text>
  <text x="165" y="133" text-anchor="middle" font-size="9">Application source code</text>
  <rect x="310" y="100" width="250" height="40" fill="#f3e5f5" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="435" y="118" text-anchor="middle" font-size="10" font-weight="bold">docker/</text>
  <text x="435" y="133" text-anchor="middle" font-size="9">Config, scripts, overrides</text>
  <text x="300" y="170" text-anchor="middle" font-size="10" fill="#555">Keep Docker files at project root alongside source code</text>
</svg>

---

## Environment Management

| File | Purpose | Example |
|------|---------|---------|
| .env | Environment vars | `DB_HOST=localhost` |
| docker-compose.override.yml | Local overrides | Development settings |
| .dockerignore | Exclude files | `node_modules` |
| config files | Configuration | `config.dev.json` |

---

## Testing Strategy

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd5_10_workflow" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <text x="300" y="18" text-anchor="middle" font-size="12" font-weight="bold">Docker Testing Pipeline</text>
  <rect x="20" y="35" width="130" height="55" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="85" y="55" text-anchor="middle" font-size="11" font-weight="bold">Unit Tests</text>
  <text x="85" y="73" text-anchor="middle" font-size="10">docker run --rm</text>
  <line x1="150" y1="62" x2="175" y2="62" stroke="#333" stroke-width="2" marker-end="url(#arrowd5_10_workflow)"/>
  <rect x="175" y="35" width="140" height="55" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="245" y="55" text-anchor="middle" font-size="11" font-weight="bold">Integration Tests</text>
  <text x="245" y="73" text-anchor="middle" font-size="10">compose up + test</text>
  <line x1="315" y1="62" x2="340" y2="62" stroke="#333" stroke-width="2" marker-end="url(#arrowd5_10_workflow)"/>
  <rect x="340" y="35" width="120" height="55" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="400" y="55" text-anchor="middle" font-size="11" font-weight="bold">E2E Tests</text>
  <text x="400" y="73" text-anchor="middle" font-size="10">Full stack</text>
  <line x1="460" y1="62" x2="485" y2="62" stroke="#333" stroke-width="2" marker-end="url(#arrowd5_10_workflow)"/>
  <rect x="485" y="35" width="100" height="55" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2" rx="5"/>
  <text x="535" y="55" text-anchor="middle" font-size="11" font-weight="bold" fill="#2e7d32">Deploy</text>
  <text x="535" y="73" text-anchor="middle" font-size="10">Verified</text>
  <rect x="60" y="115" width="480" height="35" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="5" stroke-dasharray="4,2"/>
  <text x="300" y="137" text-anchor="middle" font-size="10">Each stage runs in isolated containers with disposable environments</text>
  <text x="300" y="175" text-anchor="middle" font-size="10" fill="#555">docker-compose -f docker-compose.test.yml up --abort-on-container-exit</text>
</svg>

---

## Version Control Integration

| Aspect | Practice | Purpose |
|--------|----------|---------|
| Dockerfile | Version control | Track changes |
| Images | Tagged versions | Release management |
| Compose files | Environment specific | Configuration control |
| Scripts | Build automation | Consistency |

---

## Team Collaboration

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="215" y="5" width="170" height="35" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="28" text-anchor="middle" font-size="12" font-weight="bold">Shared Registry</text>
  <rect x="20" y="70" width="130" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="85" y="90" text-anchor="middle" font-size="10" font-weight="bold">Developer A</text>
  <text x="85" y="107" text-anchor="middle" font-size="10">docker push</text>
  <rect x="170" y="70" width="130" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="235" y="90" text-anchor="middle" font-size="10" font-weight="bold">Developer B</text>
  <text x="235" y="107" text-anchor="middle" font-size="10">docker pull</text>
  <rect x="320" y="70" width="130" height="50" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="385" y="90" text-anchor="middle" font-size="10" font-weight="bold">CI Server</text>
  <text x="385" y="107" text-anchor="middle" font-size="10">auto build</text>
  <rect x="470" y="70" width="110" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="525" y="90" text-anchor="middle" font-size="10" font-weight="bold">QA Team</text>
  <text x="525" y="107" text-anchor="middle" font-size="10">docker pull</text>
  <line x1="85" y1="70" x2="250" y2="40" stroke="#333" stroke-width="1.5"/>
  <line x1="235" y1="70" x2="280" y2="40" stroke="#333" stroke-width="1.5"/>
  <line x1="385" y1="70" x2="320" y2="40" stroke="#333" stroke-width="1.5"/>
  <line x1="525" y1="70" x2="350" y2="40" stroke="#333" stroke-width="1.5"/>
  <rect x="100" y="145" width="400" height="35" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="5" stroke-dasharray="4,2"/>
  <text x="300" y="167" text-anchor="middle" font-size="10">Shared compose files + Dockerfiles in version control</text>
</svg>

---

## Performance Optimization

| Area | Technique | Benefit |
|------|-----------|---------|
| Build cache | Layer optimization | Faster builds |
| Multi-stage | Smaller images | Reduced size |
| Development mounts | Quick updates | Faster iteration |
| Network setup | Efficient communication | Better performance |
