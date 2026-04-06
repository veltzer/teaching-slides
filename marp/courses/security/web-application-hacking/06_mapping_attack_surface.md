# Mapping the Attack Surface

## Creating a Complete Picture

---

## What is Attack Surface Mapping?

The **attack surface** is the sum of all points where an attacker can try to enter or extract data:

- Every URL and endpoint
- Every input field and parameter
- Every authentication mechanism
- Every API endpoint
- Every file upload point
- Every inter-component communication
- Every third-party integration

---

## Attack Surface Mapping Methodology

```misc
1. Enumerate all visible functionality
2. Discover hidden content
3. Map authentication mechanisms
4. Identify authorization boundaries
5. Document data flows
6. Catalog third-party components
7. Note trust boundaries
8. Prioritize by risk
```

---

## Functionality Mapping

```misc
Target Application Map:
=======================
Public:
  /                    Home page
  /products            Product catalog
  /products/{id}       Product detail (IDOR?)
  /search?q=           Search (XSS? SQLi?)
  /login               Authentication
  /register            Account creation
  /forgot-password     Password reset

Authenticated:
  /dashboard           User dashboard
  /profile             User profile (XSS?)
  /orders              Order history (IDOR?)
  /orders/{id}         Order detail (IDOR?)
  /settings            Account settings

Admin:
  /admin               Admin panel (auth bypass?)
  /admin/users         User management
  /admin/reports       Reporting
```

---

## Data Flow Diagram

<svg xmlns="http://www.w3.org/2000/svg" width="560" height="530" font-family="sans-serif">
  <defs>
    <marker id="ah13" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
      <path d="M0,0 L0,6 L8,3 z" fill="#555"/>
    </marker>
  </defs>
  <!-- User Browser -->
  <rect x="190" y="10" width="170" height="50" rx="4" fill="#e3f2fd" stroke="#333" stroke-width="1.5"/>
  <text x="275" y="40" text-anchor="middle" font-size="13" fill="#222">User Browser</text>
  <text x="275" y="75" text-anchor="middle" font-size="11" fill="#555">HTTPS (TLS 1.3)</text>
  <line x1="275" y1="60" x2="275" y2="90" stroke="#555" stroke-width="1.5" marker-end="url(#ah13)"/>
  <!-- CDN/WAF -->
  <rect x="190" y="90" width="170" height="50" rx="4" fill="#e8f5e9" stroke="#333" stroke-width="1.5"/>
  <text x="275" y="120" text-anchor="middle" font-size="13" fill="#222">CDN / WAF</text>
  <line x1="275" y1="140" x2="275" y2="165" stroke="#555" stroke-width="1.5" marker-end="url(#ah13)"/>
  <!-- Nginx -->
  <rect x="190" y="165" width="170" height="50" rx="4" fill="#fff3e0" stroke="#333" stroke-width="1.5"/>
  <text x="275" y="190" text-anchor="middle" font-size="13" fill="#222">Nginx</text>
  <text x="380" y="190" font-size="11" fill="#555">← Reverse Proxy</text>
  <line x1="275" y1="215" x2="275" y2="240" stroke="#555" stroke-width="1.5"/>
  <!-- branch -->
  <line x1="140" y1="240" x2="410" y2="240" stroke="#555" stroke-width="1.5"/>
  <line x1="140" y1="240" x2="140" y2="265" stroke="#555" stroke-width="1.5" marker-end="url(#ah13)"/>
  <line x1="410" y1="240" x2="410" y2="265" stroke="#555" stroke-width="1.5" marker-end="url(#ah13)"/>
  <!-- App Server -->
  <rect x="60" y="265" width="160" height="50" rx="4" fill="#e3f2fd" stroke="#333" stroke-width="1.5"/>
  <text x="140" y="295" text-anchor="middle" font-size="13" fill="#222">App Server</text>
  <!-- API Server -->
  <rect x="330" y="265" width="160" height="50" rx="4" fill="#e3f2fd" stroke="#333" stroke-width="1.5"/>
  <text x="410" y="295" text-anchor="middle" font-size="13" fill="#222">API Server</text>
  <line x1="140" y1="315" x2="140" y2="345" stroke="#555" stroke-width="1.5" marker-end="url(#ah13)"/>
  <line x1="410" y1="315" x2="410" y2="345" stroke="#555" stroke-width="1.5" marker-end="url(#ah13)"/>
  <!-- MySQL -->
  <rect x="50" y="345" width="180" height="55" rx="4" fill="#f0f4f8" stroke="#333" stroke-width="1.5"/>
  <text x="140" y="368" text-anchor="middle" font-size="13" fill="#222">MySQL</text>
  <text x="140" y="388" text-anchor="middle" font-size="11" fill="#555">(Primary)</text>
  <!-- Redis -->
  <rect x="320" y="345" width="180" height="55" rx="4" fill="#f0f4f8" stroke="#333" stroke-width="1.5"/>
  <text x="410" y="368" text-anchor="middle" font-size="13" fill="#222">Redis</text>
  <text x="410" y="388" text-anchor="middle" font-size="11" fill="#555">(Cache)</text>
</svg>

---

## Trust Boundaries

<svg xmlns="http://www.w3.org/2000/svg" width="560" height="400" font-family="sans-serif">
  <defs>
    <marker id="ah14" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
      <path d="M0,0 L0,6 L8,3 z" fill="#555"/>
    </marker>
  </defs>
  <!-- Zone 1: Untrusted -->
  <rect x="10" y="10" width="530" height="80" rx="4" fill="#ffebee" stroke="#c62828" stroke-width="2"/>
  <text x="25" y="32" font-size="13" fill="#c62828" font-weight="bold">Untrusted (Internet)</text>
  <text x="25" y="54" font-size="12" fill="#222">User Browser</text>
  <text x="25" y="72" font-size="12" fill="#222">Third-party APIs</text>
  <!-- TB1 -->
  <text x="270" y="108" text-anchor="middle" font-size="11" fill="#555">▼  Trust Boundary 1  ▼</text>
  <!-- Zone 2: DMZ -->
  <rect x="10" y="115" width="530" height="80" rx="4" fill="#fff3e0" stroke="#e65100" stroke-width="2"/>
  <text x="25" y="137" font-size="13" fill="#e65100" font-weight="bold">DMZ</text>
  <text x="25" y="157" font-size="12" fill="#222">Web Server, WAF, Load Balancer</text>
  <!-- TB2 -->
  <text x="270" y="213" text-anchor="middle" font-size="11" fill="#555">▼  Trust Boundary 2  ▼</text>
  <!-- Zone 3: App Network -->
  <rect x="10" y="220" width="530" height="80" rx="4" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="25" y="242" font-size="13" fill="#2e7d32" font-weight="bold">Application Network</text>
  <text x="25" y="262" font-size="12" fill="#222">App Servers, API Gateway</text>
  <!-- TB3 -->
  <text x="270" y="318" text-anchor="middle" font-size="11" fill="#555">▼  Trust Boundary 3  ▼</text>
  <!-- Zone 4: Data Network -->
  <rect x="10" y="325" width="530" height="55" rx="4" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="25" y="347" font-size="13" fill="#1565c0" font-weight="bold">Data Network</text>
  <text x="25" y="367" font-size="12" fill="#222">Database, File Storage</text>
  <!-- Note -->
  <text x="270" y="396" text-anchor="middle" font-size="12" fill="#c62828" font-weight="bold">Each boundary crossing needs validation!</text>
</svg>

---

## Authentication Surface

<svg xmlns="http://www.w3.org/2000/svg" width="640" height="360" font-family="sans-serif">
  <text x="10" y="20" font-size="14" fill="#222" font-weight="bold">Authentication Entry Points</text>
  <!-- header -->
  <rect x="10" y="28" width="310" height="30" fill="#333"/>
  <text x="165" y="48" text-anchor="middle" font-size="13" fill="#fff" font-weight="bold">Mechanism</text>
  <rect x="320" y="28" width="310" height="30" fill="#333"/>
  <text x="475" y="48" text-anchor="middle" font-size="13" fill="#fff" font-weight="bold">Attack Vector</text>
  <!-- rows -->
  <rect x="10" y="58"  width="310" height="26" fill="#e3f2fd" stroke="#ccc" stroke-width="1"/>
  <text x="22" y="75"  font-size="12" fill="#222">Login form</text>
  <rect x="320" y="58" width="310" height="26" fill="#e3f2fd" stroke="#ccc" stroke-width="1"/>
  <text x="332" y="75" font-size="12" fill="#222">Brute force, SQLi</text>

  <rect x="10" y="84"  width="310" height="26" fill="#fff" stroke="#ccc" stroke-width="1"/>
  <text x="22" y="101" font-size="12" fill="#222">Password reset</text>
  <rect x="320" y="84" width="310" height="26" fill="#fff" stroke="#ccc" stroke-width="1"/>
  <text x="332" y="101" font-size="12" fill="#222">Token prediction, enum</text>

  <rect x="10" y="110" width="310" height="26" fill="#e3f2fd" stroke="#ccc" stroke-width="1"/>
  <text x="22" y="127" font-size="12" fill="#222">Registration</text>
  <rect x="320" y="110" width="310" height="26" fill="#e3f2fd" stroke="#ccc" stroke-width="1"/>
  <text x="332" y="127" font-size="12" fill="#222">Mass registration, abuse</text>

  <rect x="10" y="136" width="310" height="26" fill="#fff" stroke="#ccc" stroke-width="1"/>
  <text x="22" y="153" font-size="12" fill="#222">OAuth / SSO</text>
  <rect x="320" y="136" width="310" height="26" fill="#fff" stroke="#ccc" stroke-width="1"/>
  <text x="332" y="153" font-size="12" fill="#222">Token theft, redirect</text>

  <rect x="10" y="162" width="310" height="26" fill="#e3f2fd" stroke="#ccc" stroke-width="1"/>
  <text x="22" y="179" font-size="12" fill="#222">API key auth</text>
  <rect x="320" y="162" width="310" height="26" fill="#e3f2fd" stroke="#ccc" stroke-width="1"/>
  <text x="332" y="179" font-size="12" fill="#222">Key leakage, brute force</text>

  <rect x="10" y="188" width="310" height="26" fill="#fff" stroke="#ccc" stroke-width="1"/>
  <text x="22" y="205" font-size="12" fill="#222">JWT authentication</text>
  <rect x="320" y="188" width="310" height="26" fill="#fff" stroke="#ccc" stroke-width="1"/>
  <text x="332" y="205" font-size="12" fill="#222">Algorithm confusion</text>

  <rect x="10" y="214" width="310" height="26" fill="#e3f2fd" stroke="#ccc" stroke-width="1"/>
  <text x="22" y="231" font-size="12" fill="#222">MFA / 2FA</text>
  <rect x="320" y="214" width="310" height="26" fill="#e3f2fd" stroke="#ccc" stroke-width="1"/>
  <text x="332" y="231" font-size="12" fill="#222">Bypass, social engineering</text>

  <rect x="10" y="240" width="310" height="26" fill="#fff" stroke="#ccc" stroke-width="1"/>
  <text x="22" y="257" font-size="12" fill="#222">Session cookies</text>
  <rect x="320" y="240" width="310" height="26" fill="#fff" stroke="#ccc" stroke-width="1"/>
  <text x="332" y="257" font-size="12" fill="#222">Hijacking, fixation</text>

  <rect x="10" y="266" width="310" height="26" fill="#e3f2fd" stroke="#ccc" stroke-width="1"/>
  <text x="22" y="283" font-size="12" fill="#222">Remember me tokens</text>
  <rect x="320" y="266" width="310" height="26" fill="#e3f2fd" stroke="#ccc" stroke-width="1"/>
  <text x="332" y="283" font-size="12" fill="#222">Predictable tokens</text>

  <rect x="10" y="292" width="310" height="26" fill="#fff" stroke="#ccc" stroke-width="1"/>
  <text x="22" y="309" font-size="12" fill="#222">Account lockout</text>
  <rect x="320" y="292" width="310" height="26" fill="#fff" stroke="#ccc" stroke-width="1"/>
  <text x="332" y="309" font-size="12" fill="#222">DoS via lockout</text>

  <rect x="10" y="28" width="620" height="290" fill="none" stroke="#333" stroke-width="1.5"/>
</svg>

---

## Authorization Mapping

```bash
# Test authorization by comparing access across roles

# Role: Regular User (user_a)
GET /api/users/1       -> 200 (own profile)
GET /api/users/2       -> 403 or 200? (IDOR test)
GET /admin/dashboard   -> 403 (correct)
DELETE /api/users/1    -> 403 or 200? (method test)

# Role: Admin
GET /api/users/1       -> 200
GET /api/users/2       -> 200
GET /admin/dashboard   -> 200
DELETE /api/users/1    -> 200

# Key tests:
# - Can user A access user B's resources?
# - Can a regular user access admin endpoints?
# - Can unauthenticated users access protected resources?
# - Do API endpoints enforce same auth as UI?
```

---

## IDOR (Insecure Direct Object Reference) Mapping

```misc
Identify all numeric/predictable identifiers:

/api/users/123        <- Try 124, 125, 1, 0
/api/orders/ORD-001   <- Try ORD-002
/api/files/abc123     <- Enumerable?
/invoice?id=5001      <- Try 5000, 5002
/download?file=report_2024.pdf  <- Try other names

Testing strategy:
1. Log in as User A, note all IDs
2. Log in as User B, note all IDs
3. As User A, try to access User B's IDs
4. As User B, try to access User A's IDs
5. Try without authentication
```

---

## API Endpoint Discovery

```bash
# Swagger/OpenAPI documentation
curl http://target.com/swagger.json
curl http://target.com/api-docs
curl http://target.com/openapi.json
curl http://target.com/v2/api-docs      # Spring
curl http://target.com/swagger/v1/swagger.json  # .NET

# GraphQL schema discovery
curl -X POST http://target.com/graphql \
  -H "Content-Type: application/json" \
  -d '{"query":"{ __schema { queryType { name } mutationType { name } types { name kind fields { name type { name } } } } }"}'

# Common API versioning patterns
/api/v1/resource
/api/v2/resource    # Try v0, v3, etc.
/v1/api/resource
```

---

## Third-Party Component Inventory

```output
Component             Version    Known CVEs
---------             -------    ----------
jQuery                3.3.1      CVE-2019-11358 (XSS)
Bootstrap             4.1.3      None critical
Angular               8.2.0      CVE-2021-44255
lodash                4.17.11    CVE-2019-10744 (prototype)
moment.js             2.24.0     CVE-2022-31129 (ReDoS)
TinyMCE               5.0.0      Multiple XSS
CKEditor              4.11.0     Multiple XSS

# Detection tools:
# - Retire.js (browser extension or CLI)
# - npm audit / yarn audit (if you have package.json)
# - Snyk
# - OWASP Dependency-Check
```

---

## Attack Surface Prioritization

| Priority | Attack Surface | Reason |
|----------|---------------|--------|
| **Critical** | Authentication/Login | Direct access to accounts |
| **Critical** | File uploads | Potential RCE |
| **Critical** | Admin panels | Full system control |
| **High** | Search/query parameters | SQL injection, XSS |
| **High** | API endpoints | Data exposure |
| **High** | Password reset | Account takeover |
| **Medium** | User profiles | Stored XSS |
| **Medium** | Payment processing | Financial impact |
| **Low** | Static pages | Limited interaction |

---

## Creating the Attack Surface Report

```misc
Target: https://target.com
Date: 2024-01-15
Tester: [Your Name]

Technologies:
  OS: Ubuntu 20.04
  Web Server: Nginx 1.18
  Framework: Django 3.2
  Database: PostgreSQL 13
  Frontend: React 17

Entry Points: 47 total
  - 12 authenticated endpoints
  - 8 unauthenticated endpoints
  - 15 API endpoints
  - 6 file upload points
  - 4 search/query functions
  - 2 WebSocket endpoints

High-Priority Targets:
  1. /api/v1/users/{id} - IDOR candidate
  2. /search?q= - Injection candidate
  3. /upload - File upload candidate
  4. /admin/ - Authorization bypass candidate
```

---

## Automated Attack Surface Tools

```bash
# Recon-ng - Automated reconnaissance framework
recon-ng
> marketplace install all
> modules load recon/domains-hosts/hackertarget
> options set SOURCE target.com
> run

# Amass - Attack surface mapping
amass enum -d target.com -o amass-results.txt

# httpx - HTTP probing
cat urls.txt | httpx -status-code -content-length \
  -title -tech-detect -o httpx-results.txt

# Katana - Modern crawler
katana -u https://target.com -d 5 -o katana-results.txt
```

---

## Day 1 Lab: Complete Mapping Exercise

**Tasks** (60 minutes):

1. **Enumerate** all pages and functionality of DVWA
1. **Discover** hidden content with `gobuster`
1. **Identify** all entry points per page
1. **Map** authentication and authorization
1. **Document** the technology stack
1. **Create** an attack surface matrix
1. **Prioritize** targets for Day 2 testing

**Deliverable**: Complete attack surface report

---

## Common Web Application Architectures

<svg xmlns="http://www.w3.org/2000/svg" width="640" height="310" font-family="sans-serif">
  <defs>
    <marker id="ah16" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
      <path d="M0,0 L0,6 L8,3 z" fill="#555"/>
    </marker>
  </defs>
  <!-- Monolithic -->
  <rect x="10" y="10" width="610" height="60" rx="4" fill="#e3f2fd" stroke="#333" stroke-width="1.5"/>
  <text x="25" y="30" font-size="13" fill="#222" font-weight="bold">Monolithic</text>
  <text x="25" y="52" font-size="12" fill="#222">Browser  →  Web Server  →  App (all-in-one)  →  Database</text>
  <!-- Microservices -->
  <rect x="10" y="85" width="610" height="85" rx="4" fill="#e8f5e9" stroke="#333" stroke-width="1.5"/>
  <text x="25" y="105" font-size="13" fill="#222" font-weight="bold">Microservices</text>
  <text x="25" y="125" font-size="12" fill="#222">Browser  →  API Gateway  →  Service A  →  DB-A</text>
  <text x="25" y="143" font-size="12" fill="#555">                       →  Service B  →  DB-B</text>
  <text x="25" y="159" font-size="12" fill="#555">                       →  Service C  →  Cache</text>
  <!-- Serverless -->
  <rect x="10" y="183" width="610" height="55" rx="4" fill="#fff3e0" stroke="#333" stroke-width="1.5"/>
  <text x="25" y="203" font-size="13" fill="#222" font-weight="bold">Serverless</text>
  <text x="25" y="225" font-size="12" fill="#222">Browser  →  CDN  →  API Gateway  →  Lambda/Functions  →  DB</text>
  <!-- Jamstack -->
  <rect x="10" y="250" width="610" height="50" rx="4" fill="#f0f4f8" stroke="#333" stroke-width="1.5"/>
  <text x="25" y="270" font-size="13" fill="#222" font-weight="bold">Jamstack</text>
  <text x="25" y="290" font-size="12" fill="#222">Browser  →  CDN (static)  →  API calls  →  Backend services</text>
</svg>

- Architecture type affects attack strategy
- Microservices have more inter-service trust boundaries
- Serverless reduces OS-level attack surface

---

## Documenting Trust Boundaries

<svg xmlns="http://www.w3.org/2000/svg" width="640" height="370" font-family="sans-serif">
  <text x="10" y="20" font-size="14" fill="#222" font-weight="bold">Trust Boundary Matrix</text>
  <!-- header row -->
  <rect x="10"  y="28" width="130" height="30" fill="#333"/>
  <text x="75"  y="48" text-anchor="middle" font-size="12" fill="#fff" font-weight="bold">From / To</text>
  <rect x="140" y="28" width="110" height="30" fill="#333"/>
  <text x="195" y="48" text-anchor="middle" font-size="12" fill="#fff">Browser</text>
  <rect x="250" y="28" width="110" height="30" fill="#333"/>
  <text x="305" y="48" text-anchor="middle" font-size="12" fill="#fff">Web Srv</text>
  <rect x="360" y="28" width="110" height="30" fill="#333"/>
  <text x="415" y="48" text-anchor="middle" font-size="12" fill="#fff">App Srv</text>
  <rect x="470" y="28" width="160" height="30" fill="#333"/>
  <text x="550" y="48" text-anchor="middle" font-size="12" fill="#fff">DB</text>
  <!-- rows -->
  <rect x="10"  y="58" width="130" height="28" fill="#f0f4f8" stroke="#ccc" stroke-width="1"/>
  <text x="22"  y="76" font-size="12" fill="#222">Browser</text>
  <rect x="140" y="58" width="110" height="28" fill="#eee" stroke="#ccc" stroke-width="1"/>
  <text x="195" y="76" text-anchor="middle" font-size="12" fill="#888">—</text>
  <rect x="250" y="58" width="110" height="28" fill="#ffcdd2" stroke="#ccc" stroke-width="1"/>
  <text x="305" y="76" text-anchor="middle" font-size="11" fill="#c62828">Untrusted</text>
  <rect x="360" y="58" width="110" height="28" fill="#f5f5f5" stroke="#ccc" stroke-width="1"/>
  <text x="415" y="76" text-anchor="middle" font-size="11" fill="#888">N/A</text>
  <rect x="470" y="58" width="160" height="28" fill="#f5f5f5" stroke="#ccc" stroke-width="1"/>
  <text x="550" y="76" text-anchor="middle" font-size="11" fill="#888">N/A</text>

  <rect x="10"  y="86" width="130" height="28" fill="#fff" stroke="#ccc" stroke-width="1"/>
  <text x="22"  y="104" font-size="12" fill="#222">Web Server</text>
  <rect x="140" y="86" width="110" height="28" fill="#ffcdd2" stroke="#ccc" stroke-width="1"/>
  <text x="195" y="104" text-anchor="middle" font-size="11" fill="#c62828">Untrusted</text>
  <rect x="250" y="86" width="110" height="28" fill="#eee" stroke="#ccc" stroke-width="1"/>
  <text x="305" y="104" text-anchor="middle" font-size="12" fill="#888">—</text>
  <rect x="360" y="86" width="110" height="28" fill="#fff9c4" stroke="#ccc" stroke-width="1"/>
  <text x="415" y="104" text-anchor="middle" font-size="11" fill="#f57f17">Semi-trust</text>
  <rect x="470" y="86" width="160" height="28" fill="#f5f5f5" stroke="#ccc" stroke-width="1"/>
  <text x="550" y="104" text-anchor="middle" font-size="11" fill="#888">N/A</text>

  <rect x="10"  y="114" width="130" height="28" fill="#f0f4f8" stroke="#ccc" stroke-width="1"/>
  <text x="22"  y="132" font-size="12" fill="#222">App Server</text>
  <rect x="140" y="114" width="110" height="28" fill="#ffcdd2" stroke="#ccc" stroke-width="1"/>
  <text x="195" y="132" text-anchor="middle" font-size="11" fill="#c62828">Untrusted</text>
  <rect x="250" y="114" width="110" height="28" fill="#c8e6c9" stroke="#ccc" stroke-width="1"/>
  <text x="305" y="132" text-anchor="middle" font-size="11" fill="#2e7d32">Trusted</text>
  <rect x="360" y="114" width="110" height="28" fill="#eee" stroke="#ccc" stroke-width="1"/>
  <text x="415" y="132" text-anchor="middle" font-size="12" fill="#888">—</text>
  <rect x="470" y="114" width="160" height="28" fill="#c8e6c9" stroke="#ccc" stroke-width="1"/>
  <text x="550" y="132" text-anchor="middle" font-size="11" fill="#2e7d32">Trust</text>

  <rect x="10"  y="142" width="130" height="28" fill="#fff" stroke="#ccc" stroke-width="1"/>
  <text x="22"  y="160" font-size="12" fill="#222">Database</text>
  <rect x="140" y="142" width="110" height="28" fill="#f5f5f5" stroke="#ccc" stroke-width="1"/>
  <text x="195" y="160" text-anchor="middle" font-size="11" fill="#888">N/A</text>
  <rect x="250" y="142" width="110" height="28" fill="#f5f5f5" stroke="#ccc" stroke-width="1"/>
  <text x="305" y="160" text-anchor="middle" font-size="11" fill="#888">N/A</text>
  <rect x="360" y="142" width="110" height="28" fill="#c8e6c9" stroke="#ccc" stroke-width="1"/>
  <text x="415" y="160" text-anchor="middle" font-size="11" fill="#2e7d32">Trusted</text>
  <rect x="470" y="142" width="160" height="28" fill="#eee" stroke="#ccc" stroke-width="1"/>
  <text x="550" y="160" text-anchor="middle" font-size="12" fill="#888">—</text>

  <rect x="10" y="28" width="620" height="142" fill="none" stroke="#333" stroke-width="1.5"/>
  <!-- Questions -->
  <rect x="10" y="185" width="620" height="175" rx="4" fill="#fff3e0" stroke="#333" stroke-width="1.5"/>
  <text x="25" y="206" font-size="13" fill="#222" font-weight="bold">At EACH boundary crossing, ask:</text>
  <text x="25" y="228" font-size="12" fill="#222">1. Is input validated?</text>
  <text x="25" y="248" font-size="12" fill="#222">2. Is authorization checked?</text>
  <text x="25" y="268" font-size="12" fill="#222">3. Is data encrypted in transit?</text>
  <text x="25" y="288" font-size="12" fill="#222">4. Are error details exposed?</text>
  <text x="25" y="308" font-size="12" fill="#222">5. Can this boundary be bypassed?</text>
</svg>

---

## Identifying Business-Critical Functions

<svg xmlns="http://www.w3.org/2000/svg" width="640" height="375" font-family="sans-serif">
  <text x="10" y="20" font-size="14" fill="#222" font-weight="bold">High-Value Targets</text>
  <!-- header -->
  <rect x="10"  y="28" width="280" height="30" fill="#333"/>
  <text x="150" y="48" text-anchor="middle" font-size="13" fill="#fff" font-weight="bold">Function</text>
  <rect x="290" y="28" width="180" height="30" fill="#333"/>
  <text x="380" y="48" text-anchor="middle" font-size="13" fill="#fff" font-weight="bold">Risk</text>
  <rect x="470" y="28" width="160" height="30" fill="#333"/>
  <text x="550" y="48" text-anchor="middle" font-size="13" fill="#fff" font-weight="bold">Priority</text>

  <!-- rows -->
  <rect x="10"  y="58" width="280" height="27" fill="#ffebee" stroke="#ccc" stroke-width="1"/>
  <text x="22"  y="75" font-size="12" fill="#222">Payment processing</text>
  <rect x="290" y="58" width="180" height="27" fill="#ffebee" stroke="#ccc" stroke-width="1"/>
  <text x="302" y="75" font-size="12" fill="#222">Financial</text>
  <rect x="470" y="58" width="160" height="27" fill="#ffebee" stroke="#ccc" stroke-width="1"/>
  <text x="550" y="75" text-anchor="middle" font-size="12" fill="#c62828" font-weight="bold">Critical</text>

  <rect x="10"  y="85" width="280" height="27" fill="#ffebee" stroke="#ccc" stroke-width="1"/>
  <text x="22"  y="102" font-size="12" fill="#222">User authentication</text>
  <rect x="290" y="85" width="180" height="27" fill="#ffebee" stroke="#ccc" stroke-width="1"/>
  <text x="302" y="102" font-size="12" fill="#222">Account theft</text>
  <rect x="470" y="85" width="160" height="27" fill="#ffebee" stroke="#ccc" stroke-width="1"/>
  <text x="550" y="102" text-anchor="middle" font-size="12" fill="#c62828" font-weight="bold">Critical</text>

  <rect x="10"  y="112" width="280" height="27" fill="#ffebee" stroke="#ccc" stroke-width="1"/>
  <text x="22"  y="129" font-size="12" fill="#222">Admin panel</text>
  <rect x="290" y="112" width="180" height="27" fill="#ffebee" stroke="#ccc" stroke-width="1"/>
  <text x="302" y="129" font-size="12" fill="#222">Full control</text>
  <rect x="470" y="112" width="160" height="27" fill="#ffebee" stroke="#ccc" stroke-width="1"/>
  <text x="550" y="129" text-anchor="middle" font-size="12" fill="#c62828" font-weight="bold">Critical</text>

  <rect x="10"  y="139" width="280" height="27" fill="#fff3e0" stroke="#ccc" stroke-width="1"/>
  <text x="22"  y="156" font-size="12" fill="#222">File upload</text>
  <rect x="290" y="139" width="180" height="27" fill="#fff3e0" stroke="#ccc" stroke-width="1"/>
  <text x="302" y="156" font-size="12" fill="#222">RCE</text>
  <rect x="470" y="139" width="160" height="27" fill="#fff3e0" stroke="#ccc" stroke-width="1"/>
  <text x="550" y="156" text-anchor="middle" font-size="12" fill="#e65100" font-weight="bold">High</text>

  <rect x="10"  y="166" width="280" height="27" fill="#fff3e0" stroke="#ccc" stroke-width="1"/>
  <text x="22"  y="183" font-size="12" fill="#222">Search function</text>
  <rect x="290" y="166" width="180" height="27" fill="#fff3e0" stroke="#ccc" stroke-width="1"/>
  <text x="302" y="183" font-size="12" fill="#222">SQLi/XSS</text>
  <rect x="470" y="166" width="160" height="27" fill="#fff3e0" stroke="#ccc" stroke-width="1"/>
  <text x="550" y="183" text-anchor="middle" font-size="12" fill="#e65100" font-weight="bold">High</text>

  <rect x="10"  y="193" width="280" height="27" fill="#fff3e0" stroke="#ccc" stroke-width="1"/>
  <text x="22"  y="210" font-size="12" fill="#222">API endpoints</text>
  <rect x="290" y="193" width="180" height="27" fill="#fff3e0" stroke="#ccc" stroke-width="1"/>
  <text x="302" y="210" font-size="12" fill="#222">Data exposure</text>
  <rect x="470" y="193" width="160" height="27" fill="#fff3e0" stroke="#ccc" stroke-width="1"/>
  <text x="550" y="210" text-anchor="middle" font-size="12" fill="#e65100" font-weight="bold">High</text>

  <rect x="10"  y="220" width="280" height="27" fill="#fff3e0" stroke="#ccc" stroke-width="1"/>
  <text x="22"  y="237" font-size="12" fill="#222">Password reset</text>
  <rect x="290" y="220" width="180" height="27" fill="#fff3e0" stroke="#ccc" stroke-width="1"/>
  <text x="302" y="237" font-size="12" fill="#222">Account theft</text>
  <rect x="470" y="220" width="160" height="27" fill="#fff3e0" stroke="#ccc" stroke-width="1"/>
  <text x="550" y="237" text-anchor="middle" font-size="12" fill="#e65100" font-weight="bold">High</text>

  <rect x="10"  y="247" width="280" height="27" fill="#e8f5e9" stroke="#ccc" stroke-width="1"/>
  <text x="22"  y="264" font-size="12" fill="#222">User profiles</text>
  <rect x="290" y="247" width="180" height="27" fill="#e8f5e9" stroke="#ccc" stroke-width="1"/>
  <text x="302" y="264" font-size="12" fill="#222">Stored XSS</text>
  <rect x="470" y="247" width="160" height="27" fill="#e8f5e9" stroke="#ccc" stroke-width="1"/>
  <text x="550" y="264" text-anchor="middle" font-size="12" fill="#2e7d32">Medium</text>

  <rect x="10"  y="274" width="280" height="27" fill="#e8f5e9" stroke="#ccc" stroke-width="1"/>
  <text x="22"  y="291" font-size="12" fill="#222">Contact forms</text>
  <rect x="290" y="274" width="180" height="27" fill="#e8f5e9" stroke="#ccc" stroke-width="1"/>
  <text x="302" y="291" font-size="12" fill="#222">Spam/XSS</text>
  <rect x="470" y="274" width="160" height="27" fill="#e8f5e9" stroke="#ccc" stroke-width="1"/>
  <text x="550" y="291" text-anchor="middle" font-size="12" fill="#2e7d32">Medium</text>

  <rect x="10"  y="301" width="280" height="27" fill="#f0f4f8" stroke="#ccc" stroke-width="1"/>
  <text x="22"  y="318" font-size="12" fill="#222">Static pages</text>
  <rect x="290" y="301" width="180" height="27" fill="#f0f4f8" stroke="#ccc" stroke-width="1"/>
  <text x="302" y="318" font-size="12" fill="#222">Limited</text>
  <rect x="470" y="301" width="160" height="27" fill="#f0f4f8" stroke="#ccc" stroke-width="1"/>
  <text x="550" y="318" text-anchor="middle" font-size="12" fill="#555">Low</text>

  <rect x="10" y="28" width="620" height="300" fill="none" stroke="#333" stroke-width="1.5"/>
</svg>

---

## Mapping API Endpoints Systematically

```bash
# Use Burp Suite site map to export all endpoints
# Then categorize:

# CRUD Operations
POST   /api/users          -> Create (test mass assignment)
GET    /api/users           -> Read (test auth, pagination)
GET    /api/users/{id}      -> Read (test IDOR)
PUT    /api/users/{id}      -> Update (test auth, mass assign)
DELETE /api/users/{id}      -> Delete (test auth)

# Search & Filter
GET    /api/users?role=admin     -> Test parameter injection
GET    /api/users?sort=name ASC  -> Test SQL injection in ORDER BY
GET    /api/users?q=search       -> Test XSS, SQLi

# File Operations
POST   /api/upload          -> Test file upload vulns
GET    /api/files/{name}    -> Test path traversal
```

---

## Creating Attack Trees

```tree
Goal: Access Admin Panel
├── Direct Access
│   ├── Guess admin URL (/admin, /administrator)
│   └── Find admin URL via content discovery
├── Authentication Bypass
│   ├── SQL injection in login
│   ├── Default credentials
│   └── Brute-force password
├── Session Hijacking
│   ├── XSS to steal admin cookie
│   ├── Session fixation
│   └── Predictable session tokens
├── Authorization Bypass
│   ├── Modify role in JWT/cookie
│   ├── Parameter tampering (isAdmin=true)
│   └── IDOR on admin endpoint
└── Privilege Escalation
    ├── Register as user, escalate to admin
    └── Exploit admin functionality accessible to user
```

---

## Day 1 Summary

- Web applications are complex, multi-layered systems
- Every technology component is a potential attack vector
- Systematic discovery finds more than random testing
- Entry points exist in URLs, headers, cookies, and bodies
- Trust boundaries define where validation is needed
- Attack surface mapping guides efficient testing
- Prioritize by impact and likelihood

> Tomorrow: Authentication & Session Attacks
