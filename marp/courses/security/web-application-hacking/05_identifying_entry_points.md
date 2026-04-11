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

# Identifying Entry Points & Server-Side Technologies

## Where to Probe and What to Expect

---

## Attack Surface Mapping

![attack_surface_mapping](svg/courses/security/web-application-hacking/05_identifying_entry_points/attack_surface_mapping.svg)

---

## What is an Entry Point?

An **entry point** is any place where user-supplied data enters the application:

- URL parameters (`?id=1&name=test`)
- Form fields (login, search, contact forms)
- `HTTP` headers (`Cookie`, `Referer`, `User-Agent`)
- `JSON`/`XML` request bodies
- File uploads
- `WebSocket` messages
- URL path components (`/user/123/profile`)

---

## URL Parameters

```misc
https://target.com/products?category=electronics&sort=price&page=2

Entry points:
  category = electronics   <- Test for injection
  sort     = price         <- Test for injection
  page     = 2             <- Test for IDOR/injection

# Hidden parameters may also exist
# Try adding:
?debug=true
?admin=1
?format=json
?callback=test
?_method=PUT
```

---

## Form Inputs - Visible and Hidden

```html
<!-- Visible form fields -->
<form action="/transfer" method="POST">
  <input type="text" name="recipient" value="">
  <input type="text" name="amount" value="">

  <!-- Hidden fields - often trusted by server! -->
  <input type="hidden" name="account_id" value="12345">
  <input type="hidden" name="currency" value="USD">
  <input type="hidden" name="fee" value="2.50">

  <!-- CSRF token -->
  <input type="hidden" name="csrf_token"
         value="a8f3b2c1d4e5f6">
  <button type="submit">Transfer</button>
</form>
```

- Hidden fields are fully visible and modifiable
- Never trust client-side validation

---

## HTTP Request Analysis

![http_request_analysis](svg/courses/security/web-application-hacking/05_identifying_entry_points/http_request_analysis.svg)

---

## HTTP Headers as Entry Points

```http
# Headers the server might process:
Cookie: session=abc123; prefs=lang%3Den
User-Agent: Mozilla/5.0 (Windows NT 10.0...)
Referer: https://target.com/previous-page
X-Forwarded-For: 10.0.0.1
X-Forwarded-Host: internal.target.com
Accept-Language: en-US,en;q=0.9
Authorization: Bearer eyJhbGciOiJIUzI1NiJ9...
Content-Type: application/json
Origin: https://target.com
Host: target.com

# Many applications log User-Agent and Referer
# If logged without sanitization -> stored XSS
# X-Forwarded-For can bypass IP-based access control
```

---

## REST API Entry Points

```http
# RESTful API pattern
GET    /api/v1/users           # List users
GET    /api/v1/users/123       # Get user 123
POST   /api/v1/users           # Create user
PUT    /api/v1/users/123       # Update user 123
PATCH  /api/v1/users/123       # Partial update
DELETE /api/v1/users/123       # Delete user 123

# Entry points in REST APIs:
# 1. Path parameters (/users/123)
# 2. Query parameters (?role=admin)
# 3. Request body (JSON/XML payload)
# 4. HTTP method (try different methods)
# 5. Content-Type header
# 6. Authorization header
```

---

## JSON Request Bodies

```json
// POST /api/v1/users
// Content-Type: application/json

{
  "username": "newuser",        // Test injection
  "email": "user@test.com",    // Test injection
  "role": "user",              // Try "admin"
  "age": 25,                   // Try negative, huge numbers
  "profile": {
    "bio": "Hello",            // Test XSS
    "avatar": "http://..."     // Test SSRF
  },
  "preferences": ["a", "b"]   // Test array manipulation
}

// Try adding unexpected fields:
// "isAdmin": true
// "id": 1
// "role": "admin"
```

---

## XML Request Bodies

```xml
<!-- XML bodies are vulnerable to XXE -->
POST /api/import HTTP/1.1
Content-Type: application/xml

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<user>
  <name>&xxe;</name>
  <email>test@test.com</email>
</user>

<!-- XXE can read local files, perform SSRF,
     and sometimes achieve remote code execution -->
```

---

## File Upload Entry Points

![file_upload_entry_points](svg/courses/security/web-application-hacking/05_identifying_entry_points/file_upload_entry_points.svg)

---

## Cookie Analysis

```http
Set-Cookie: session=eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiam9obiJ9.abc123

Analysis:
1. Name: "session" -> Standard session cookie
2. Value: Base64-encoded -> Likely JWT
3. Flags present?
   - HttpOnly?   No -> Vulnerable to XSS theft
   - Secure?     No -> Sent over HTTP
   - SameSite?   No -> Vulnerable to CSRF

Decode JWT:
Header:  {"alg":"HS256"}
Payload: {"user":"john","role":"user","exp":1700000000}

Entry points:
- Modify "role" to "admin"
- Change "user" to another user
- Alter expiration time
```

---

## Identifying Server-Side Technology

```bash
# Method 1: HTTP Headers
curl -I https://target.com
# Server: Apache/2.4.41 (Ubuntu)
# X-Powered-By: PHP/7.4

# Method 2: File extensions
# .php -> PHP
# .asp/.aspx -> ASP.NET
# .jsp/.do -> Java
# .py -> Python (rare, usually no extension)

# Method 3: Cookie names
# PHPSESSID -> PHP
# JSESSIONID -> Java
# ASP.NET_SessionId -> ASP.NET
# connect.sid -> Node.js Express

# Method 4: Error pages
# PHP: "Parse error: syntax error..."
# Java: Stack trace with package names
# .NET: "Yellow Screen of Death"
```

---

## Technology-Specific Default Paths

```misc
PHP:
  /phpinfo.php, /info.php, /php-info.php
  /phpmyadmin/, /pma/
  /wp-admin/ (WordPress), /administrator/ (Joomla)

Java:
  /manager/html (Tomcat), /console (WebLogic)
  /actuator/ (Spring Boot), /swagger-ui/
  /jmx-console/ (JBoss)

ASP.NET:
  /elmah.axd (error log), /trace.axd
  /Telerik.Web.UI.WebResource.axd

Node.js:
  /.env, /api-docs/, /graphql
  /swagger.json, /package.json
```

---

## Error Page Analysis

```misc
# PHP error
Warning: mysqli_query() expects parameter 1 to be
mysqli, null given in /var/www/html/index.php on line 42

Information leaked:
- Language: PHP
- Database: MySQL (mysqli)
- File path: /var/www/html/index.php
- Line number: 42

# Java stack trace
java.sql.SQLException: ...
    at com.mysql.jdbc.ConnectionImpl.createNewIO(...)
    at com.example.app.UserDAO.findUser(UserDAO.java:87)

Information leaked:
- Language: Java
- Database: MySQL
- Package structure: com.example.app
- Class and method names
```

---

## Mapping Input Vectors Per Page

![mapping_input_vectors_per_page](svg/courses/security/web-application-hacking/05_identifying_entry_points/mapping_input_vectors_per_page.svg)

---

## Automated Entry Point Discovery

```bash
# Use Burp Suite Logger to capture all parameters
# Right-click -> Engagement Tools -> Analyze Target

# Arjun - HTTP parameter discovery
arjun -u http://target.com/page

# ParamSpider - mining parameters from web archives
python3 paramspider.py -d target.com

# Burp Extension: Param Miner
# - Discovers hidden parameters
# - Tests for cache poisoning parameters
# - Finds header-based parameters
```

---

## Testing Different HTTP Methods

```bash
# Check which methods are allowed
curl -X OPTIONS http://target.com/api/users -v

# Response: Allow: GET, POST, PUT, DELETE, OPTIONS

# Test each method for different behavior
curl -X GET http://target.com/api/users
curl -X POST http://target.com/api/users -d '{}'
curl -X PUT http://target.com/api/users/1 -d '{}'
curl -X DELETE http://target.com/api/users/1
curl -X PATCH http://target.com/api/users/1 -d '{}'

# Method override headers (bypass method restrictions)
curl -X POST http://target.com/api/users/1 \
  -H "X-HTTP-Method-Override: DELETE"
curl -X POST http://target.com/api/users/1 \
  -H "X-Method-Override: PUT"
```

---

## Content-Type Switching

```bash
# Some endpoints accept multiple content types
# Switching types can bypass validation

# Standard form submission
curl -X POST http://target.com/api/login \
  -d "username=admin&password=test"

# Switch to JSON
curl -X POST http://target.com/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"test"}'

# Switch to XML (possible XXE)
curl -X POST http://target.com/api/login \
  -H "Content-Type: application/xml" \
  -d '<login><username>admin</username><password>test</password></login>'
```

---

## Rate Limiting Detection

```bash
# Rapid requests to detect rate limiting
for i in $(seq 1 100); do
  code=$(curl -s -o /dev/null -w "%{http_code}" \
    http://target.com/api/login \
    -d "username=admin&password=test$i")
  echo "Request $i: HTTP $code"
done

# Common rate limiting indicators:
# HTTP 429 Too Many Requests
# HTTP 503 Service Unavailable
# Increasing response times
# CAPTCHA challenges
# Account lockout messages

# Bypasses to test:
# - X-Forwarded-For header rotation
# - Different user agents
# - Adding null bytes to parameters
```

---

## GraphQL Entry Points

```graphql
# GraphQL presents unique entry points
# Single endpoint, multiple operations

# Introspection query (discover schema)
query {
  __schema {
    types {
      name
      fields {
        name
        type { name }
      }
    }
  }
}

# Common GraphQL security issues:
# 1. Introspection enabled in production
# 2. No query depth limiting (DoS)
# 3. No rate limiting per query
# 4. Authorization checked per type, not per field
# 5. Batch queries bypass rate limiting

# Testing:
# POST /graphql
# Content-Type: application/json
# {"query": "{ users { id username email password } }"}

# Tools: graphql-voyager, InQL (Burp extension)
```

---

## WebSocket Entry Points

```javascript
// WebSockets maintain persistent connections
// Each message is an entry point

// Connect and intercept with Burp:
// Proxy -> WebSocket history

// Common WebSocket injection tests:
// 1. SQL injection in message parameters
ws.send(JSON.stringify({
    action: "search",
    query: "test' OR 1=1--"
}));

// 2. XSS in messages displayed to other users
ws.send(JSON.stringify({
    type: "chat",
    message: "<script>alert(document.cookie)</script>"
}));

// 3. Authorization bypass
// Change user_id in WebSocket messages
ws.send(JSON.stringify({
    action: "getProfile",
    user_id: 999  // Other user's ID
}));

// 4. Cross-Site WebSocket Hijacking (CSWSH)
// If Origin header not validated, any site can connect
```

---

## Lab Exercise: Entry Point Mapping

**Target**: DVWA

1. Log in and browse every page through Burp
1. For each page, document:
   1. URL parameters
   1. Form fields (visible and hidden)
   1. Cookies being sent
   1. Any `AJAX` requests
1. Identify the server technology stack
1. Create an entry point matrix
1. Prioritize testing targets

---

## Summary

- Entry points are everywhere: URLs, forms, headers, cookies
- Hidden form fields and `JSON` bodies are high-value targets
- Server technology identification guides attack selection
- Error pages leak critical information
- Test all `HTTP` methods and content types
- Map every entry point before beginning exploitation
- Systematic approach beats random testing

> Next: Mapping the Attack Surface
