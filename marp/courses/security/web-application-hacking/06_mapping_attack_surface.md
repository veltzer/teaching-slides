---
tags:
  - security:security
  - security:web-security
  - security:penetration-testing
  - security:owasp
level: advanced
category: security
audience:
  - audiences:developers
  - audiences:security-professionals

---

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

![data_flow_diagram](svg/courses/security/web-application-hacking/06_mapping_attack_surface/data_flow_diagram.svg)

---

## Trust Boundaries

![trust_boundaries](svg/courses/security/web-application-hacking/06_mapping_attack_surface/trust_boundaries.svg)

---

## Authentication Surface

![authentication_surface](svg/courses/security/web-application-hacking/06_mapping_attack_surface/authentication_surface.svg)

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

![common_web_application_architectures](svg/courses/security/web-application-hacking/06_mapping_attack_surface/common_web_application_architectures.svg)

---

## Common Web Application Architectures: Details

- Architecture type affects attack strategy
- Microservices have more inter-service trust boundaries
- Serverless reduces OS-level attack surface

---

## Documenting Trust Boundaries

![documenting_trust_boundaries](svg/courses/security/web-application-hacking/06_mapping_attack_surface/documenting_trust_boundaries.svg)

---

## Identifying Business-Critical Functions

![identifying_business_critical_functions](svg/courses/security/web-application-hacking/06_mapping_attack_surface/identifying_business_critical_functions.svg)

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
