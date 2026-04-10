# API Security: Protecting the Digital Backbone

---

## API Threat Landscape

![api_threat_landscape](svg/courses/security/cyber-attacks-and-vectors/27_api_security/api_threat_landscape.svg)

---
## Why API Security Matters

- APIs (Application Programming Interfaces) are the backbone of modern applications
- Microservices, mobile apps, IoT, and cloud services all rely on APIs
- APIs expose application logic and sensitive data directly
- 83% of web traffic is now API traffic (Akamai)
- API attacks increased 681% in 2021 (Salt Security)
- APIs are now the #1 attack surface for web applications

---
## OWASP API Security Top 10 (2023)

| Rank | Vulnerability                           | Risk Level |
|------|----------------------------------------|------------|
| 1    | Broken Object Level Authorization       | Critical   |
| 2    | Broken Authentication                   | Critical   |
| 3    | Broken Object Property Level Auth       | High       |
| 4    | Unrestricted Resource Consumption       | High       |
| 5    | Broken Function Level Authorization     | High       |
| 6    | Unrestricted Access to Sensitive Flows  | Medium     |
| 7    | Server Side Request Forgery (SSRF)      | High       |
| 8    | Security Misconfiguration               | Medium     |
| 9    | Improper Inventory Management           | Medium     |
| 10   | Unsafe Consumption of APIs              | Medium     |

---
## BOLA: Broken Object Level Authorization

```bash
┌──────────────────────────────────────────────────────────┐
│          BOLA (Broken Object Level Authorization)         │
│          Also known as IDOR (Insecure Direct Object Ref.) │
│                                                          │
│  User A (ID: 1001) makes request:                        │
│  GET /api/users/1001/orders                              │
│  -> Returns User A's orders (correct)                    │
│                                                          │
│  User A changes the ID:                                  │
│  GET /api/users/1002/orders                              │
│  -> Returns User B's orders! (BOLA vulnerability)        │
│                                                          │
│  The API does not verify that the authenticated user     │
│  has permission to access the requested object           │
└──────────────────────────────────────────────────────────┘
```

```python
# VULNERABLE: No authorization check on object access
@app.route('/api/users/<int:user_id>/orders')
@require_auth
def get_orders(user_id):
    # Anyone who is authenticated can access any user's orders!
    orders = db.get_orders(user_id)
    return jsonify(orders)

# SECURE: Verify the authenticated user owns the resource
@app.route('/api/users/<int:user_id>/orders')
@require_auth
def get_orders(user_id):
    if current_user.id != user_id and not current_user.is_admin:
        return jsonify({"error": "Forbidden"}), 403
    orders = db.get_orders(user_id)
    return jsonify(orders)
```

---
## BOLA in the Real World

| Company        | Year | What Happened                                      |
|----------------|------|----------------------------------------------------|
| Facebook       | 2018 | Access tokens of 50M users leaked via BOLA          |
| Uber           | 2019 | Driver personal data accessible by changing IDs     |
| Peloton        | 2021 | Any user's private account data accessible          |
| Parler         | 2021 | All posts scraped by incrementing post IDs          |
| T-Mobile       | 2023 | 37M customer records via API BOLA                   |

**Prevention:**
- Always verify the authenticated user has permission to access the requested object
- Use UUIDs instead of sequential integers for resource IDs
- Implement centralized authorization middleware
- Log and alert on access pattern anomalies

---
## Mass Assignment

```python
┌──────────────────────────────────────────────────────────┐
│          Mass Assignment Attack                           │
│                                                          │
│  API expects:                                            │
│  PUT /api/users/me                                       │
│  { "name": "John", "email": "john@example.com" }        │
│                                                          │
│  Attacker sends:                                         │
│  PUT /api/users/me                                       │
│  { "name": "John", "email": "john@example.com",         │
│    "role": "admin", "credit_balance": 99999 }            │
│                                                          │
│  If the API blindly assigns all fields from the request  │
│  to the model, the attacker becomes admin with free      │
│  credit!                                                 │
└──────────────────────────────────────────────────────────┘
```

```python
# VULNERABLE: Accept all fields from request
@app.route('/api/users/me', methods=['PUT'])
@require_auth
def update_user():
    data = request.get_json()
    # Blindly update all fields!
    for key, value in data.items():
        setattr(current_user, key, value)
    db.session.commit()
    return jsonify(current_user.to_dict())

# SECURE: Whitelist allowed fields
ALLOWED_UPDATE_FIELDS = {'name', 'email', 'phone'}

@app.route('/api/users/me', methods=['PUT'])
@require_auth
def update_user():
    data = request.get_json()
    for key, value in data.items():
        if key in ALLOWED_UPDATE_FIELDS:
            setattr(current_user, key, value)
        else:
            return jsonify({"error": f"Cannot update field: {key}"}), 400
    db.session.commit()
    return jsonify(current_user.to_dict())
```

---

## Server-Side Request Forgery (SSRF) via APIs

![server_side_request_forgery_ssrf_via_apis](svg/courses/security/cyber-attacks-and-vectors/27_api_security/server_side_request_forgery_ssrf_via_apis.svg)

---

## Server-Side Request Forgery (SSRF) via APIs

```python
# SECURE: URL validation for SSRF prevention
from urllib.parse import urlparse
import ipaddress
BLOCKED_NETWORKS = [
    ipaddress.ip_network('169.254.0.0/16'),   # Link-local (IMDS)
    ipaddress.ip_network('10.0.0.0/8'),        # Private
    ipaddress.ip_network('172.16.0.0/12'),     # Private
    ipaddress.ip_network('192.168.0.0/16'),    # Private
    ipaddress.ip_network('127.0.0.0/8'),       # Loopback
]
def is_safe_url(url):
    parsed = urlparse(url)
    if parsed.scheme not in ('http', 'https'):
        return False
    try:
        ip = ipaddress.ip_address(parsed.hostname)
        for network in BLOCKED_NETWORKS:
            if ip in network:
                return False
    except ValueError:
        # Hostname, not IP - resolve and check
        import socket
        ip = socket.gethostbyname(parsed.hostname)
        return is_safe_url(f"{parsed.scheme}://{ip}{parsed.path}")
    return True
```

---
## Rate Limiting and Resource Consumption

```bash
┌──────────────────────────────────────────────────────────┐
│  API Rate Limiting Strategies                            │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  Fixed Window:     100 requests per minute               │
│  ├── Simple to implement                                 │
│  └── Burst issue at window boundaries                    │
│                                                          │
│  Sliding Window:   100 requests per rolling 60 seconds   │
│  ├── Smoother rate limiting                              │
│  └── More memory to track                                │
│                                                          │
│  Token Bucket:     Tokens refill at fixed rate            │
│  ├── Allows controlled bursts                            │
│  └── Most flexible approach                              │
│                                                          │
│  Rate limit by:                                          │
│  - API key / Client ID                                   │
│  - User account                                          │
│  - IP address (fallback)                                 │
│  - Endpoint (different limits per endpoint)              │
└──────────────────────────────────────────────────────────┘
```

```python
# Rate limiting with Flask-Limiter
from flask_limiter import Limiter

limiter = Limiter(
    app=app,
    key_func=lambda: request.headers.get('X-API-Key', get_remote_address()),
    storage_uri="redis://localhost:6379",
)

# Different limits per endpoint
@app.route('/api/search')
@limiter.limit("10 per minute")
def search():
    pass

@app.route('/api/login')
@limiter.limit("5 per minute")
def login():
    pass

@app.route('/api/data')
@limiter.limit("100 per minute")
def data():
    pass
```

### Rate Limit Response Headers

```asm
HTTP/1.1 429 Too Many Requests
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1609459200
Retry-After: 30

{
    "error": "Rate limit exceeded",
    "retry_after": 30
}
```

---
## JWT Attacks

### The "none" Algorithm Attack

```python
# ATTACK: Change algorithm to "none"
import base64
import json

# Original JWT header: {"alg": "HS256", "typ": "JWT"}
# Attacker changes to: {"alg": "none", "typ": "JWT"}

header = base64.b64encode(
    json.dumps({"alg": "none", "typ": "JWT"}).encode()
).decode().rstrip('=')

payload = base64.b64encode(
    json.dumps({"sub": "admin", "role": "admin"}).encode()
).decode().rstrip('=')

# No signature needed with "none" algorithm
forged_jwt = f"{header}.{payload}."

# DEFENSE: Always specify allowed algorithms explicitly
import jwt

# VULNERABLE
decoded = jwt.decode(token, SECRET, algorithms=jwt.algorithms.get_default_algorithms())

# SECURE
decoded = jwt.decode(token, SECRET, algorithms=["HS256"])
```

---
### JWT Key Confusion Attack

```asm
┌──────────────────────────────────────────────────────────┐
│          JWT Algorithm Confusion (RS256 -> HS256)         │
│                                                          │
│  Server configuration:                                   │
│  - Uses RS256 (asymmetric: RSA private/public key pair)  │
│  - Public key is known (published or extractable)        │
│                                                          │
│  Normal flow:                                            │
│  Sign with PRIVATE key -> Verify with PUBLIC key         │
│                                                          │
│  Attack:                                                 │
│  1. Attacker obtains the RSA PUBLIC key                  │
│  2. Creates token with alg: "HS256" (symmetric)          │
│  3. Signs token using PUBLIC key as HMAC secret          │
│                                                          │
│  Vulnerable verification:                                │
│  jwt.verify(token, publicKey)                            │
│  - Sees alg="HS256", uses publicKey as HMAC secret       │
│  - Token passes verification!                            │
│                                                          │
│  Defense:                                                │
│  jwt.verify(token, publicKey, algorithms=["RS256"])      │
│  - Explicitly specify allowed algorithms                 │
│  - Never allow both symmetric and asymmetric             │
└──────────────────────────────────────────────────────────┘
```

---
### Other JWT Attacks

| Attack                    | Description                                | Defense                        |
|---------------------------|--------------------------------------------|--------------------------------|
| None algorithm            | Remove signature verification              | Whitelist algorithms           |
| Key confusion             | RS256 -> HS256 with public key             | Separate key handling          |
| JWK header injection      | Embed attacker's key in JWT header         | Ignore JWK in headers          |
| KID path traversal        | `"kid": "../../../dev/null"` = empty key   | Validate KID parameter         |
| Token not expiring        | Missing or far-future `exp` claim          | Always require and check `exp` |
| Weak secret               | Brute-force HS256 secret                   | Use 256+ bit random secrets    |
| Token in URL              | Leaked via Referer header, logs            | Use Authorization header       |

```bash
# Brute-force weak JWT secrets with jwt_tool
python3 jwt_tool.py <JWT_TOKEN> -C -d wordlist.txt

# Test for JWT vulnerabilities
python3 jwt_tool.py <JWT_TOKEN> -M at  # All tests
```

---
## GraphQL API Attacks

```bash
┌──────────────────────────────────────────────────────────┐
│          GraphQL-Specific Vulnerabilities                 │
│                                                          │
│  1. Introspection Query (Information Disclosure)         │
│     Query the entire schema to discover all types,       │
│     fields, and relationships                            │
│                                                          │
│  2. Nested Query DoS (Batching Attack)                   │
│     Deeply nested queries consume exponential resources  │
│                                                          │
│  3. Field Suggestion / Enumeration                       │
│     Error messages suggest valid field names             │
│                                                          │
│  4. Authorization Bypass                                 │
│     Access unauthorized data through relationships       │
│                                                          │
│  5. Injection via Arguments                              │
│     SQL injection through GraphQL arguments              │
└──────────────────────────────────────────────────────────┘
```

### Introspection Query Attack

```graphql
# Discover the entire API schema
{
  __schema {
    types {
      name
      fields {
        name
        type { name }
        args { name type { name } }
      }
    }
    queryType { name }
    mutationType { name }
  }
}

# This reveals all types, fields, relationships
# Attacker now knows every endpoint and data structure
```

---
### GraphQL DoS: Nested Query Attack

```graphql
# Deeply nested query (exponential resource consumption)
query MaliciousQuery {
  users {
    friends {
      friends {
        friends {
          friends {
            friends {
              name
              email
            }
          }
        }
      }
    }
  }
}
# If each user has 100 friends, this could return
# 100^5 = 10 billion records!
```

```python
# DEFENSE: Query depth limiting
# Using graphene-django with depth limit

from graphene_django.views import GraphQLView
from graphql import parse
from graphql.validation import validate

MAX_DEPTH = 5
MAX_COMPLEXITY = 1000

def depth_limit_middleware(next, root, info, **args):
    """Reject queries exceeding maximum depth."""
    depth = calculate_query_depth(info)
    if depth > MAX_DEPTH:
        raise Exception(f"Query depth {depth} exceeds maximum {MAX_DEPTH}")
    return next(root, info, **args)
```

---
## GraphQL Security Best Practices

```python
# Comprehensive GraphQL security configuration

# 1. Disable introspection in production
GRAPHENE = {
    'MIDDLEWARE': [
        'graphql_jwt.middleware.JSONWebTokenMiddleware',
    ],
}

# In production settings:
# schema.graphql_schema.introspection = False

# 2. Query complexity/depth limiting
# 3. Rate limiting per operation
# 4. Persisted queries (whitelist allowed queries)
# 5. Input validation on all arguments
# 6. Authorization on every resolver (not just top-level)

# Persisted queries example:
ALLOWED_QUERIES = {
    "abc123": "query GetUser($id: ID!) { user(id: $id) { name email } }",
    "def456": "query ListProducts { products { name price } }",
}

def execute_persisted_query(query_id, variables):
    if query_id not in ALLOWED_QUERIES:
        raise PermissionError("Query not in allowlist")
    return schema.execute(ALLOWED_QUERIES[query_id], variables=variables)
```

---

## API Security Architecture

![api_security_architecture](svg/courses/security/cyber-attacks-and-vectors/27_api_security/api_security_architecture.svg)

---
## API Gateway Security

![api_gateway_security](svg/courses/security/cyber-attacks-and-vectors/27_api_security/api_gateway_security.svg)

---
## API Authentication Best Practices

| Method              | Use Case                     | Security Level |
|---------------------|------------------------------|----------------|
| API Keys            | Server-to-server, low-risk   | Low            |
| OAuth 2.0 + PKCE    | User-facing applications     | High           |
| JWT (short-lived)   | Stateless authentication     | Medium-High    |
| mTLS                | Service-to-service (mesh)    | Very High      |
| HMAC Signatures     | Webhook verification         | High           |

```python
# Secure API key validation middleware
import hmac
import hashlib
import time

def validate_api_request(request):
    """Validate API request with HMAC signature."""
    api_key = request.headers.get('X-API-Key')
    timestamp = request.headers.get('X-Timestamp')
    signature = request.headers.get('X-Signature')

    if not all([api_key, timestamp, signature]):
        return False, "Missing authentication headers"

    # Check timestamp freshness (prevent replay attacks)
    if abs(time.time() - float(timestamp)) > 300:  # 5 min
        return False, "Request expired"

    # Reconstruct and verify HMAC signature
    secret = get_api_secret(api_key)
    message = f"{request.method}{request.path}{timestamp}{request.data}"
    expected = hmac.new(
        secret.encode(), message.encode(), hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(signature, expected):
        return False, "Invalid signature"

    return True, "Valid"
```

---
## Input Validation and Schema Enforcement

```python
# API input validation with Pydantic (Python)
from pydantic import BaseModel, validator, constr
from typing import Optional
import re

class CreateUserRequest(BaseModel):
    name: constr(min_length=1, max_length=100)
    email: constr(pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    age: Optional[int] = None
    role: str = "user"

    @validator('role')
    def validate_role(cls, v):
        allowed_roles = {'user', 'editor'}  # NOT 'admin'!
        if v not in allowed_roles:
            raise ValueError(f"Role must be one of: {allowed_roles}")
        return v

    @validator('age')
    def validate_age(cls, v):
        if v is not None and (v < 0 or v > 150):
            raise ValueError("Invalid age")
        return v

@app.route('/api/users', methods=['POST'])
@require_auth
def create_user():
    try:
        user_data = CreateUserRequest(**request.get_json())
    except ValidationError as e:
        return jsonify({"errors": e.errors()}), 400
    # user_data is now validated and safe to use
```

---
## API Security Testing

```bash
# OWASP ZAP for API scanning
zap-cli quick-scan --self-contained -t http://api.example.com

# Burp Suite for API testing (manual + automated)
# Import API spec (OpenAPI/Swagger) into Burp

# Postman for API security testing
# Create test collections that check:
# - Authorization bypass (BOLA)
# - Mass assignment
# - Rate limiting
# - Input validation

# Nuclei with API templates
nuclei -u http://api.example.com -t api/

# APICheck: OWASP API security toolset
pip install apicheck
apicheck-curl http://api.example.com/openapi.json | \
    apicheck-sensitivedata
```

### API Security Checklist

```sql
┌──────────────────────────────────────────────────────────┐
│  API Security Checklist                                  │
├──────────────────────────────────────────────────────────┤
│  [ ] Authentication on every endpoint                    │
│  [ ] Object-level authorization checks                   │
│  [ ] Input validation and schema enforcement             │
│  [ ] Rate limiting per client/endpoint                   │
│  [ ] TLS everywhere (no plaintext API traffic)           │
│  [ ] JWT: whitelist algorithms, short expiry             │
│  [ ] Disable GraphQL introspection in production         │
│  [ ] API versioning and deprecation policy               │
│  [ ] Comprehensive logging and monitoring                │
│  [ ] OpenAPI spec maintained and validated                │
│  [ ] Automated security testing in CI/CD                 │
│  [ ] CORS configured restrictively                       │
│  [ ] Error messages do not leak internal details         │
│  [ ] Pagination enforced on list endpoints               │
└──────────────────────────────────────────────────────────┘
```

---
## Key Takeaways

- APIs are the most common attack surface for modern applications
- BOLA (Broken Object Level Authorization) is the #1 API vulnerability -- always check permissions
- Mass assignment can elevate privileges if you blindly accept all request fields
- JWT attacks (none algorithm, key confusion) exploit poor library configuration
- GraphQL requires specific protections: disable introspection, limit query depth and complexity
- Rate limiting prevents abuse and resource exhaustion
- API gateways centralize security controls (auth, rate limiting, validation, logging)
- SSRF through APIs can expose internal services and cloud metadata
- Automated security testing (ZAP, nuclei, Burp) should be part of CI/CD
- Defense requires: authentication + authorization + validation + rate limiting + monitoring
